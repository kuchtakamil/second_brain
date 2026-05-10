# Mechanizmy zarządzania historią czatu w LangChain i LangGraph

## Krótki opis

Modele LLM (Large Language Models) działają w sposób bezstanowy (ang. *stateless*) — każdą nową iterację wejściowych tokenów traktują jako zupełnie niezależny problem, pozbawiony pamięci o poprzednich interakcjach. Aby stworzyć klasyczny czat, należy do kolejnych żądań doklejać poprzednie pytania użytkownika i wynikowe odpowiedzi asystenta. Zarówno ekosystem **LangChain**, jak i **LangGraph** oferują wbudowane narzędzia oraz abstrakcje rozwiązujące ten problem w warstwie orkiestracyjnej, jednak bazują one na zupełnie innej architekturze.

## Dlaczego jest to ważne / Kiedy to stosować?

Zarządzanie historią jest wymagane wszędzie tam, gdzie aplikacja zakłada wieloetapowe dialogi lub sekwencje:
- **Konwersacyjne boty RAG / wirtualni asystenci:** Użytkownik może dopytywać o kontekst w swoim bieżącym pytaniu bazując na odpowiedzi wygenerowanej trzy zapytania wcześniej.
- **Agenty AI (ReAct):** Agenty wykorzystujące narzędzia (ang. *tools*) muszą "pamiętać", jakich narzędzi użyły chwilę wcześniej i jakie były ich surowe wyniki.
- **Optymalizacja zapytań:** Poza zapisem wiadomości, przetrzymywanie historii wymaga w końcu zaadresowania technik przycinania lub podsumowywania zapytań (ang. *trimming*, *summarization*), aby asystent nie przekroczył dostępnego limitu *Context Window* modelu.

---

## LangChain: Klasy ChatMessageHistory oraz Wrapper Historyczny

W klasycznym LangChain (opartym głownie na LangChain Expression Language - LCEL), problem historii adresowany jest dzięki dedykowanemu wrapperowi modyfikującemu wejście i wyjście do łańcucha operacji.

### Jak to działa w LangChain?

Najważniejszą mechaniką utrzymania historii w LCEL jest zastosowanie klasy `RunnableWithMessageHistory`. Działa ona jako pośrednik, który:
1. Pobiera przeszłe zaudytowane wiadomości ze wskazanej na początku warstwy fizycznej.
2. Formatuje pod spodem prompt LLMa (dodając pobraną historię, zazwyczaj przez obiekt podziału `MessagesPlaceholder`).
3. Czeka na wykonanie wywołania LLM.
4. Zapisuje asynchronicznie nowo przesłane zapytanie użytkownika i najnowszą wygenerowaną odpowiedź modelu do wybranej bazy danych (sposób zapisu definiujemy wstrzykując własną funkcję, tzw. factory function, ładującą i tworzącą połączenie do bazy pod dane ID sesji).

Aby warstwa pamięci wiedziała, który kontekst wyciągnąć, łańcuchy takie pobierają parametr konfiguracyjny (np. `session_id`). 
Same wiadomości na drodze utrwalania reprezentowane są bazową klasą `BaseChatMessageHistory`, od której dziedziczą konkretne implementacje np. `InMemoryChatMessageHistory` (do testów w programie RAM) czy instancje bazodanowe takie jak `RedisChatMessageHistory`, `PostgresChatMessageHistory` itd.

### Przykład – LangChain LCEL

```python
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

model = ChatOpenAI(model="gpt-4o")

prompt = ChatPromptTemplate.from_messages([
    ("system", "Jesteś pomocnym asystentem."),
    # Miejsce, gdzie podczas wywołania wstrzyknięte zostaną archiwalne wiadomości
    MessagesPlaceholder(variable_name="chat_history"),   
    ("human", "{question}"),
])

chain = prompt | model

# Składzik przechowujący obiekty w testach (w pamięci RAM)
session_store = {}

def get_session_history(session_id: str):
    # To tutaj definiuje się sposób zapisu do bazy! 
    # Wrapper `RunnableWithMessageHistory` uruchomi tę funkcję za każdym razem, gdy padnie zapytanie.
    # Podmieniając `InMemoryChatMessageHistory` na np. `RedisChatMessageHistory(session_id, url="redis://...")`, 
    # wskazujesz LangChainowi, żeby asynchronicznie odczytywał i zapisywał wiadomości dla tej sesji w bazie Redis.
    if session_id not in session_store:
        session_store[session_id] = InMemoryChatMessageHistory()
    return session_store[session_id]

# Stworzenie opakowanego powtarzalnego łańcucha wspierającego historię
with_message_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="question",
    history_messages_key="chat_history",
)

# Wywołanie z podaniem klucza 'session_id' w bloku 'config'
response = with_message_history.invoke(
    {"question": "Cześć, mam na imię Kamil."},
    config={"configurable": {"session_id": "sesja_123"}}
)
```

---

## LangGraph: Reducery i Checkpointery

**LangGraph** to podejście architektoniczne celujące bardziej w skomplikowanych agentów AI. Proces wnioskowania opiera się na cyklicznym przepływie między węzłami grafu, które ze swojej natury współdzielą tzw. *State* (Stan). Stan jest modyfikowany iteracyjnie.

### Jak to działa w LangGraph?

O ile w LCEL zarządzanie dotyczy łańcucha konwersacji, o tyle mechanizm odkładania historii dla agentów budowanych w LangGraph implementowany jest wprost jako część utrwalania całego grafu (nie tylko wiadomości).

1. **State i Reducer:** Obiekt `State` najczęściej dziedziczy po `TypedDict` i składa się z pola na listę wiadomości, ale w parze z tak zwanym reducerem, standardowo jest to `add_messages`. Reducer informuje LangGraph, że każdy wierzchołek zwracający np. krotkę wpisów wiadomości po stronie wejścia ma doczytywać całą poprzednią listę wiadomości, a operacja dodania nowej wartości spowoduje dopisanie jej na sam koniec listy z archiwum (albo re-aktualizowanie starszej, gdy zwrócone wiadomość posiada ten sam ID).
2. **Checkpointer:** Żeby utrwalić fizycznie między wywołaniami listę tych zgromadzonych w Stanie obiektów, uruchamia się **Checkpointer** (`MemorySaver`, `PostgresSaver`, `SqliteSaver`). Robi on dokładny snopshot całej zawartości `State` (w tym zgromadzonej do tej pory listy `messages`). 
3. Podczas wywołania całości grafu za pomocą `app.invoke`, identyfikatorem grupującym dla checkpointera parametrem wywołania jest `thread_id` (wątek).

### Przykład – LangGraph Checkpointers

```python
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI
from typing import Annotated, TypedDict

# 1. Definicja stanu. Reducer `add_messages` odpowiada za łączenie i aktualizację listy wiadomości.
class State(TypedDict):
    messages: Annotated[list, add_messages]

# Węzeł wywołujący bezpośrednio model LLM
def chatbot_node(state: State):
    llm = ChatOpenAI(model="gpt-4o")
    # Zmienna state["messages"] gwarantuje tu odczyt wszystkich zebranych jak dotąd wpisów, włącznie ze starymi
    response = llm.invoke(state["messages"])
    # LangGraph doda tą jedną modyfikację na koniec stosu dzięki reducerowi w `State`
    return {"messages": [response]}

# Składanie Grafu
graph = StateGraph(State)
graph.add_node("chatbot", chatbot_node)
graph.add_edge(START, "chatbot")
graph.add_edge("chatbot", END)

# Inicjujemy checkpointer. MemorySaver pozwala na przechowywanie snapshotów w procesach w pamięci RAM.
memory = MemorySaver()
# Kompilujemy aplikację przekazując utworzony obiekt Checkpointer
app = graph.compile(checkpointer=memory)

# Konfiguracja i identyfikator wątku zapisywania snapshotu
config = {"configurable": {"thread_id": "watek_xyz"}}

# Pierwsza wymiana wiadomości
app.invoke(
    {"messages": [("human", "Cześć, mam na imię Kamil.")]}, 
    config=config
)

# W kolejnej ramce LangGraph sam załaduje z pomycią Checkpointera zapisaną listę `messages`. Model bez problemu odpowie znając kontekst z poprzedniej wywołanej ramki.
app.invoke(
    {"messages": [("human", "Jak mam na imię?")]}, 
    config=config
)
```

## Podsumowanie Różnic

1. **Zakres zapisywania:** W `LangChain` zapisywane i zarysowane po API są wyłącznie same przesyłki rozmowy (konwersacje w obiektach ChatMessageHistory). Po stronie `LangGraph`, ustrukturyzowana pamięć (Checkpointer) zapisuje pod postacią Snapshota w jednym locie całą pamięć węzła `State` i listę `messages` redukowanych w locie przez funkcję np. `add_messages`.
2. **Klucze referencyjne:** Z historycznego punktu widzenia Langchain nazywa te bloki i instancje z reguły wspólną zmienną konfiguracyjną `session_id`. W Langgraph koncepcja przeszła drobną modyfikację i standardowym identyfikatorem grupowania wątku historii stała się nazwa klucza `thread_id`.

## Powiązane pliki

- [checkpointers-langgraph.md](checkpointers-langgraph.md)
- [komunikacja-z-llm-w-langchain.md](komunikacja-z-llm-w-langchain.md)
- [pamięć-długoterminowa-ai.md](pamięć-długoterminowa-ai.md)
