# Pamięć i Persistence w LangGraph — Checkpointers w praktyce

## Krótki opis

Modele LLM z natury są **bezstanowe** — każde wywołanie traktują jako zupełnie nowe zapytanie. LangGraph rozwiązuje ten problem za pomocą mechanizmu **Checkpointerów**, które automatycznie zapisują i odtwarzają pełen stan grafu (w tym historię wiadomości) pomiędzy kolejnymi turami konwersacji. Dzięki temu agent „pamięta" wcześniejsze interakcje bez konieczności ręcznego zarządzania kontekstem.

Niniejszy dokument koncentruje się na **praktycznym wdrożeniu** persystencji: od dodania `MemorySaver` przy kompilacji grafu, przez identyfikację sesji za pomocą `thread_id`, aż po demonstrację wznawiania przerwanej rozmowy.

## Dlaczego to ważne / Kiedy stosować?

- **Wieloturowe konwersacje** — użytkownik może wrócić do wątku po godzinach lub dniach i kontynuować rozmowę bez utraty kontekstu.
- **Agenty z narzędziami (tools)** — agent musi pamiętać, jakich narzędzi użył w poprzednich krokach i jakie uzyskał wyniki.
- **Odporność na awarie** — jeśli proces się przerwie (rate limit, restart serwera), checkpointer pozwala wznowić pracę dokładnie od miejsca przerwania.
- **Human-in-the-Loop** — możliwość wstrzymania agenta w określonym kroku, aby człowiek mógł zatwierdzić lub skorygować akcję.

---

## Kluczowe koncepty

### 1. `MemorySaver` — checkpointer w pamięci RAM

`MemorySaver` to najprostsza implementacja checkpointera dostarczana przez LangGraph. Przechowuje snapshoty stanu w pamięci procesu Pythona.

```python
from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()
```

| Cecha | Wartość |
|---|---|
| **Backend** | Pamięć RAM (słownik Pythona) |
| **Przeznaczenie** | Prototypowanie, testy, lokalne eksperymenty |
| **Trwałość** | Dane giną po zakończeniu procesu |
| **Wydajność** | Błyskawiczny zapis i odczyt |
| **Alternatywy produkcyjne** | `SqliteSaver`, `PostgresSaver`, `AsyncPostgresSaver` |

> **Uwaga:** Na produkcji należy zastąpić `MemorySaver` trwałym backendem (np. `PostgresSaver`), aby dane przetrwały restarty aplikacji.

### 2. `thread_id` — identyfikator wątku konwersacji

Każda sesja rozmowy identyfikowana jest unikalnym kluczem `thread_id`, przekazywanym w bloku `config` przy każdym wywołaniu grafu:

```python
config = {"configurable": {"thread_id": "session-1"}}
```

- **Różne `thread_id`** → oddzielne, niezależne konwersacje (osobna historia, osobny stan).
- **Ten sam `thread_id`** → kontynuacja tej samej konwersacji (checkpointer automatycznie załaduje poprzedni stan).

Dzięki temu jeden skompilowany graf może jednocześnie obsługiwać wielu użytkowników — wystarczy przypisać każdemu unikalne `thread_id`.

### 3. Wznowienie przerwanej konwersacji

Jedną z najważniejszych zalet checkpointera jest możliwość **wznowienia przerwanej rozmowy**. Wystarczy podać to samo `thread_id`, a checkpointer automatycznie odtworzy pełen stan sprzed przerwania:

```python
# Sesja przerwana np. przez restart serwera
# Po ponownym uruchomieniu wystarczy ponownie skompilować graf
# i wywołać go z tym samym thread_id — MemorySaver (w RAM) tego nie przetrwa,
# ale PostgresSaver czy SqliteSaver tak.

config = {"configurable": {"thread_id": "session-1"}}
result = app.invoke(
    {"messages": [("human", "Kontynuujmy naszą rozmowę.")]},
    config=config
)
# Agent ma dostęp do pełnej historii z tego wątku
```

---

## Krok po kroku: wdrożenie persystencji

### Krok 1 — Definicja stanu z reducerem `add_messages`

Reducer `add_messages` informuje LangGraph, że nowe wiadomości mają być **dopisywane** do istniejącej listy (nie nadpisywane). Dodatkowo obsługuje on deduplikację po ID wiadomości.

```python
from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[list, add_messages]
```

### Krok 2 — Utworzenie węzła (node) czatbota

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o")

def chatbot_node(state: State):
    # state["messages"] zawiera CAŁĄ historię wątku
    # (załadowaną automatycznie przez checkpointer)
    response = llm.invoke(state["messages"])
    return {"messages": [response]}
```

### Krok 3 — Budowa i kompilacja grafu z checkpointerem

```python
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

# Budujemy graf
graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot_node)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

# Tworzymy checkpointer
memory = MemorySaver()

# Kompilujemy graf Z checkpointerem
app = graph_builder.compile(checkpointer=memory)
```

### Krok 4 — Uruchomienie z `thread_id` i demonstracja persystencji

```python
config = {"configurable": {"thread_id": "session-1"}}

# === Tura 1 ===
result_1 = app.invoke(
    {"messages": [("human", "Cześć! Mam na imię Kamil.")]},
    config=config
)
print(result_1["messages"][-1].content)
# → "Cześć Kamil! Miło Cię poznać. W czym mogę Ci pomóc?"

# === Tura 2 ===
result_2 = app.invoke(
    {"messages": [("human", "Jak mam na imię?")]},
    config=config
)
print(result_2["messages"][-1].content)
# → "Masz na imię Kamil! Powiedziałeś mi to przed chwilą."

# === Weryfikacja: nowy thread_id = nowa sesja ===
config_new = {"configurable": {"thread_id": "session-2"}}
result_3 = app.invoke(
    {"messages": [("human", "Jak mam na imię?")]},
    config=config_new
)
print(result_3["messages"][-1].content)
# → "Nie wiem, jak masz na imię. Nie przedstawiłeś się jeszcze."
```

Powyższy kod demonstruje trzy kluczowe aspekty:
1. **Persystencja historii** — w turze 2 model zna imię użytkownika, bo checkpointer zachował historię z tury 1.
2. **Automatyczne ładowanie** — nie trzeba ręcznie doklejać wcześniejszych wiadomości; `MemorySaver` robi to „pod maską".
3. **Izolacja wątków** — nowy `thread_id` oznacza czystą kartę (sesja `session-2` nie zna kontekstu z `session-1`).

---

## Inspekcja stanu checkpointera

LangGraph pozwala podejrzeć aktualny stan zachowany przez checkpointer za pomocą metody `get_state`:

```python
snapshot = app.get_state(config)

# Pełna lista wiadomości w wątku
for msg in snapshot.values["messages"]:
    print(f"{msg.type}: {msg.content}")

# Sprawdzenie, który węzeł ma się wykonać jako następny
print(snapshot.next)  # () — pusta krotka oznacza, że graf zakończył przetwarzanie
```

Metoda `get_state` jest nieoceniona przy debugowaniu — pozwala sprawdzić, co dokładnie widzi agent w danym punkcie przepływu.

---

## Kiedy stosować który checkpointer?

| Checkpointer | Zastosowanie | Trwałość |
|---|---|---|
| `MemorySaver` | Prototypy, testy jednostkowe, lokalne eksperymenty | ❌ Ginie z procesem |
| `SqliteSaver` | Proste aplikacje jednowęzłowe, lokalne narzędzia CLI | ✅ Zapis na dysku |
| `PostgresSaver` | Produkcja, wielowęzłowe serwisy, wieloużytkownikowe API | ✅ Baza danych |
| `AsyncPostgresSaver` | Produkcja z asynchronicznym frameworkiem (FastAPI, aiohttp) | ✅ Baza danych |

---

## Najczęstsze pułapki

1. **Brak `thread_id` w `config`** — jeśli graf został skompilowany z checkpointerem, a `thread_id` nie zostanie podany przy `invoke`, LangGraph rzuci wyjątkiem. Każde wywołanie grafu z checkpointerem **wymaga** podania `thread_id`.
2. **Użycie `MemorySaver` na produkcji** — dane giną po restarcie procesu. Na produkcji zawsze używaj trwałego backendu.
3. **Jeden `thread_id` dla wielu użytkowników** — prowadzi do mieszania historii konwersacji. Każdy użytkownik/sesja powinien mieć unikalne `thread_id`.
4. **Nieograniczone gromadzenie wiadomości** — historia rośnie z każdą turą. Przy długich konwersacjach może przekroczyć *Context Window* modelu. Rozważ techniki przycinania (`trim_messages`) lub podsumowywania historii.

---

## Powiązane pliki

- [Checkpointers w LangGraph — teoria](checkpointers-langgraph.md)
- [Mechanizmy historii czatu: LangChain vs LangGraph](chat-history-langchain-langgraph.md)
- [Pamięć długoterminowa AI](pamięć-długoterminowa-ai.md)
- [Komunikacja z LLM w LangChain](komunikacja-z-llm-w-langchain.md)
