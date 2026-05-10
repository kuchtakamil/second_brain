# Checkpointers w LangGraph (Orkiestracja Agentów)

W kontekście orkiestracji agentami AI, **Checkpointer** (czyli mechanizm persystencji, zapisu punktów kontrolnych) to kluczowy element utrzymywania stanu (state persistence). Jego głównym zadaniem jest ciągłe i bezpieczne zapisywanie oraz wczytywanie stanu grafu (agenta) po każdym wykonanym przez niego kroku (tzw. *superstepie*). Dzięki checkpointerom nasz przepływ (workflow) przestaje być bezstanowy (stateless) – zyskuje on pamięć i staje się w pełni zarządzalny w czasie.

## Dlaczego stanowią klucz w orkiestracji agentami?

Zastosowanie Checkpointerów na produkcji odblokowuje szereg fundamentalnych funkcji i zaawansowanych wzorców dla AI:

- **Pamięć konwersacyjna (Memory):** Stałe śledzenie historii konwersacji. Umożliwia asystentom pamiętanie wcześniejszych interakcji i obcowanie z szerszym zbiorem kontekstu bez konieczności ciągłego ponawiania przesyłu tych samych paczek zapytań (często rozróżnialna na short / long-term memory z zapisywaniem wektorowym).
- **Human-in-the-Loop (HITL):** Możliwość zatrzymania przebiegu automatycznego (np. agent przygotowuje się do usunięcia tabeli z bazy danych z użyciem skonfigurowanego narzędzia). Wykonanie grafu jest wstrzymywane ze zrzutem stanu; człowiek może ręcznie zaakceptować, skorygować lub zablokować akcję. Dopiero potem Checkpointer podnosi stan i cykl rusza dalej.
- **Time Travel:** Z racji tego, że agent rzuca snapshota (zrzut Checkpointa) po *każdym* kroku, w frameworkach takich jak LangGraph możemy:
  - **Przewijać operacje do tyłu ("rewind")**: np. spojrzeć na historyczny zrzut "jak agent doszedł do obecnych przemyśleń".
  - **Rozgałęziać akcje (Forking)**: cofnąć się do kroku sprzed błędu, skorygować intencje i kazać iść inną drogą.
- **Odporność na awarie (Fault Tolerance):** Przydaje się, gdy na napotkamy restrykcje takie jak Rate Limity modelu (np. 429 Too Many Requests), limitację chmury, czy utratę sieci. Agent wie, na którym Checkpoincie się zatrzymał i wznowi pracę krok po przerwie.

## Jak to działa (Przykład na LangGraph)

Aby dołączyć checkpointer do naszego rozwiązania opartego na `StateGraph` dodajemy przy metodzie kompilacji grafu pożądany backend przypisując argument `checkpointer=`. Obowiązkowe staje się też podawanie klucza sesji (często jako `thread_id` w zmiennej konfiguracyjnej). Wokół tego ID agent kategoryzuje postęp z przebiegów dla indywidualnych rozmówców.

### Kod demonstrujący mechanizm

```python
from langgraph.graph import StateGraph, START, END
# A built-in saver for storing checkpoint states in RAM
from langgraph.checkpoint.memory import MemorySaver 
from typing import TypedDict, Annotated
import operator

# 1. Define the simple State schema
class AgentState(TypedDict):
    # Using operator.add means we append messages rather than overwrite
    messages: Annotated[list, operator.add]

# 2. Define a basic node simulating an LLM response
def chatbot_node(state: AgentState):
    interaction_count = len(state.get("messages", []))
    response = f"Assistant: I received your message. Total messages in state: {interaction_count}"
    return {"messages": [response]}

# 3. Build the graph structure
builder = StateGraph(AgentState)
builder.add_node("chatbot", chatbot_node)
builder.add_edge(START, "chatbot")
builder.add_edge("chatbot", END)

# 4. Instantiate the Checkpointer
# MemorySaver is usually appropriate for dev testing, while SQLiteSaver or PostgresSaver is meant for production
memory_checkpointer = MemorySaver()

# 5. Compile the graph passing the checkpointer
# This simple assignment enables the memory and state persistence capabilities
graph = builder.compile(checkpointer=memory_checkpointer)

# 6. Usage: You MUST pass a 'thread_id' to load/store states correctly
config = {"configurable": {"thread_id": "session_alpha_101"}}

# Execute the first turn
print("--- RUN 1 ---")
result_1 = graph.invoke({"messages": ["User: Hello!"]}, config=config)
print(result_1["messages"][-1])

# Execute again with the SAME thread_id
# The Checkpointer automatically pulls our previous "User: Hello!" history 
print("--- RUN 2 ---")
result_2 = graph.invoke({"messages": ["User: Are you tracking my state?"]}, config=config)
print(result_2["messages"][-1])
```

W bardziej zaawansowanych aplikacjach można importować pakiety bazo-danowe:
- `SqliteSaver` dla prostszych implementacji dyskowych
- `PostgresSaver` / `AsyncPostgresSaver` dla architektur odpornych na duże zrównoleglenie operacji od strzałów wielu jednoczesnych użytkowników.

## Powiązane pliki

- [Wzorce Multi-Agent w LangChain](langchain-multi-agent-patterns.md)
- [Pamięć długoterminowa AI](pamięć-długoterminowa-ai.md)
- [Middlewares w LangChain](langchain-middlewares.md)
- [Wzorce projektowe systemów agentowych](wzorce-projektowe-systemow-agentowych.md)
