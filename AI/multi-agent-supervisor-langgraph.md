# Multi-Agent z Supervisorem w LangGraph

## Krótki opis

Wzorzec **Supervisor** to hierarchiczna architektura multi-agent, w której centralny węzeł (supervisor) koordynuje pracę wyspecjalizowanych agentów-workerów. Supervisor analizuje zadanie, decyduje który worker powinien działać, odbiera wyniki i kieruje przepływ dalej — do kolejnego workera lub do zakończenia (`END`).

W LangGraph ≥ 1.0 zalecanym podejściem jest **ręczna implementacja supervisora** z użyciem prymitywu `Command` do dynamicznego routingu. Biblioteka `langgraph-supervisor` z funkcją `create_supervisor` istnieje, ale jest przeznaczona do szybkiego prototypowania — w produkcji daje mniej kontroli nad kontekstem i routingiem.

---

## Dlaczego supervisor, a nie jeden agent?

- **Izolacja kontekstu** — każdy worker ma wąski system prompt i ograniczony zestaw narzędzi. Supervisor nie wysyła 20 narzędzi do jednego LLM.
- **Redukcja halucynacji** — mniejsze context window = mniejsze ryzyko zgubienia się modelu.
- **Niezależne testowanie** — każdy worker testuje się osobno.
- **Specjalizacja modeli** — supervisor może używać droższego modelu do routingu, a workerzy tańszego do wykonania zadania.

---

## Architektura wzorca Supervisor

```
                    ┌──────────────┐
                    │  Supervisor  │
           ┌───────┤  (router)    ├───────┐
           │       └──────┬───────┘       │
           ▼              │               ▼
    ┌─────────────┐       │       ┌─────────────┐
    │  Worker A   │       │       │  Worker B   │
    │ (research)  │       │       │  (coder)    │
    └──────┬──────┘       │       └──────┬──────┘
           │              │               │
           └──────────────┼───────────────┘
                          ▼
                    ┌─────────────┐
                    │    END      │
                    └─────────────┘
```

### Przepływ:

1. Wiadomość użytkownika trafia do **supervisora**.
2. Supervisor analizuje stan i decyduje: `"research_agent"`, `"code_agent"` lub `"FINISH"`.
3. Wybrany worker wykonuje zadanie i zapisuje wynik do wspólnego stanu.
4. Kontrola wraca do supervisora.
5. Supervisor ponownie ewaluuje — deleguje kolejne zadanie lub kończy pracę.

---

## Wspólny stan (Shared State)

Wszyscy agenci (supervisor + workerzy) operują na tym samym obiekcie `State`. Klucz `messages` z reducerem `add_messages` pełni rolę wspólnej pamięci konwersacyjnej.

```python
import operator
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[list, add_messages]
    next: str  # nazwa następnego węzła (ustawiana przez supervisora)
```

Każdy worker i supervisor czyta z `messages` i dopisuje do nich swoje wyniki. Reducer `add_messages` gwarantuje poprawne scalanie wiadomości z wielu węzłów (deduplikacja po ID).

---

## Implementacja ręczna (zalecane podejście)

### Sposób 1: Supervisor z `Command` (routing bezpośrednio z węzła)

Prymityw `Command` pozwala węzłowi jednocześnie zaktualizować stan **i** wskazać następny węzeł — bez definiowania statycznych krawędzi warunkowych. Daje to architekturę „edgeless".

```python
from typing import Literal
from typing_extensions import TypedDict
from pydantic import BaseModel, Field

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.types import Command

# ============================================================
# 1. STAN
# ============================================================

class State(TypedDict):
    messages: Annotated[list, add_messages]

# ============================================================
# 2. MODELE
# ============================================================

llm = ChatOpenAI(model="gpt-4o")

# Structured output do decyzji supervisora
class SupervisorDecision(BaseModel):
    next: Literal["research_agent", "code_agent", "FINISH"] = Field(
        description="Który agent powinien działać następny, lub FINISH jeśli zadanie jest zakończone."
    )
    reasoning: str = Field(
        description="Krótkie uzasadnienie decyzji."
    )

supervisor_llm = llm.with_structured_output(SupervisorDecision)

# ============================================================
# 3. SUPERVISOR — decyduje kto działa dalej
# ============================================================

SUPERVISOR_PROMPT = """Jesteś supervisorem koordynującym zespół agentów:
- research_agent: wyszukuje informacje, analizuje dane
- code_agent: pisze i debuguje kod

Na podstawie dotychczasowej konwersacji zdecyduj, który agent powinien działać następny.
Jeśli zadanie jest zakończone, zwróć FINISH."""

def supervisor(state: State) -> Command[Literal["research_agent", "code_agent", "__end__"]]:
    decision = supervisor_llm.invoke(
        [SystemMessage(content=SUPERVISOR_PROMPT)] + state["messages"]
    )

    if decision.next == "FINISH":
        return Command(goto=END, update={
            "messages": [("ai", "Zadanie zakończone.")]
        })

    return Command(goto=decision.next)

# ============================================================
# 4. WORKERZY
# ============================================================

def research_agent(state: State) -> Command[Literal["supervisor"]]:
    response = llm.invoke([
        SystemMessage(
            content="Jesteś ekspertem od researchu. Analizuj pytanie i dostarcz szczegółowe informacje."
        )
    ] + state["messages"])

    return Command(
        goto="supervisor",
        update={"messages": [response]}
    )

def code_agent(state: State) -> Command[Literal["supervisor"]]:
    response = llm.invoke([
        SystemMessage(
            content="Jesteś ekspertem od programowania. Pisz czysty, dobrze udokumentowany kod."
        )
    ] + state["messages"])

    return Command(
        goto="supervisor",
        update={"messages": [response]}
    )

# ============================================================
# 5. BUDOWA GRAFU
# ============================================================

builder = StateGraph(State)

builder.add_node("supervisor", supervisor)
builder.add_node("research_agent", research_agent)
builder.add_node("code_agent", code_agent)

# Jedyna statyczna krawędź — punkt wejścia
builder.add_edge(START, "supervisor")

# Brak add_conditional_edges! 
# Command w supervisor i workerach obsługuje cały routing dynamicznie.

graph = builder.compile()
```

### Przepływ danych krok po kroku

```
1. START → supervisor
   Supervisor analizuje messages, zwraca Command(goto="research_agent")

2. research_agent
   Generuje odpowiedź, zwraca Command(goto="supervisor", update={messages: [...]})

3. supervisor (ponownie)
   Widzi nowe wyniki w messages, decyduje: Command(goto="code_agent")

4. code_agent
   Pisze kod, zwraca Command(goto="supervisor", update={messages: [...]})

5. supervisor (ponownie)
   Uznaje zadanie za zakończone, zwraca Command(goto=END)
```

### Uruchomienie

```python
from langchain_core.messages import HumanMessage

result = graph.invoke({
    "messages": [HumanMessage(
        content="Znajdź najlepsze praktyki testowania API REST i napisz przykładowy test w pytest."
    )]
})

for msg in result["messages"]:
    print(f"[{msg.type}]: {msg.content[:200]}")
```

---

### Sposób 2: Supervisor z `add_conditional_edges` (klasyczny)

Alternatywa bez `Command` — supervisor zapisuje decyzję do stanu, a `add_conditional_edges` routuje przepływ na podstawie wartości klucza `next`:

```python
from typing import Annotated, Literal
from typing_extensions import TypedDict
from pydantic import BaseModel, Field

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

# ============================================================
# STAN
# ============================================================

class State(TypedDict):
    messages: Annotated[list, add_messages]
    next: str

# ============================================================
# SUPERVISOR
# ============================================================

class RouteDecision(BaseModel):
    next: Literal["research_agent", "code_agent", "FINISH"] = Field(
        description="Następny agent lub FINISH."
    )

llm = ChatOpenAI(model="gpt-4o")
supervisor_llm = llm.with_structured_output(RouteDecision)

def supervisor(state: State):
    decision = supervisor_llm.invoke(
        [SystemMessage(content="Zdecyduj który agent działa dalej.")] + state["messages"]
    )
    return {"next": decision.next}

# ============================================================
# WORKERZY
# ============================================================

def research_agent(state: State):
    response = llm.invoke(
        [SystemMessage(content="Jesteś ekspertem od researchu.")] + state["messages"]
    )
    return {"messages": [response]}

def code_agent(state: State):
    response = llm.invoke(
        [SystemMessage(content="Jesteś ekspertem od kodu.")] + state["messages"]
    )
    return {"messages": [response]}

# ============================================================
# ROUTING
# ============================================================

def route_next(state: State) -> str:
    if state["next"] == "FINISH":
        return END
    return state["next"]

# ============================================================
# GRAF
# ============================================================

builder = StateGraph(State)
builder.add_node("supervisor", supervisor)
builder.add_node("research_agent", research_agent)
builder.add_node("code_agent", code_agent)

builder.add_edge(START, "supervisor")
builder.add_conditional_edges("supervisor", route_next)

# Po wykonaniu pracy worker wraca do supervisora
builder.add_edge("research_agent", "supervisor")
builder.add_edge("code_agent", "supervisor")

graph = builder.compile()
```

---

## Sygnał FINISH

Supervisor kończy przepływ na dwa sposoby (zależnie od wariantu implementacji):

| Wariant | Mechanizm FINISH |
|---|---|
| `Command` | `Command(goto=END)` — supervisor bezpośrednio kieruje do `END` |
| `add_conditional_edges` | Supervisor ustawia `next="FINISH"`, a funkcja `route_next` mapuje to na `END` |

W obu przypadkach LLM supervisora podejmuje decyzję o zakończeniu na podstawie analizy dotychczasowej konwersacji — np. gdy widzi kompletną odpowiedź w historii wiadomości.

---

## Prebuilt: `create_supervisor` (prototypowanie)

Biblioteka `langgraph-supervisor` (`pip install langgraph-supervisor`) upraszcza boilerplate:

```python
from langchain_openai import ChatOpenAI
from langgraph_supervisor import create_supervisor
from langgraph.prebuilt import create_react_agent

# Workerzy jako gotowe agenty ReAct
research_agent = create_react_agent(
    model="openai:gpt-4o",
    tools=[search_tool],
    name="research_expert",
)

code_agent = create_react_agent(
    model="openai:gpt-4o",
    tools=[execute_code_tool],
    name="code_expert",
)

# Supervisor — jedna linijka
workflow = create_supervisor(
    [research_agent, code_agent],
    model=ChatOpenAI(model="gpt-4o"),
    prompt="Koordynuj pracę agentów research_expert i code_expert."
)

app = workflow.compile()
result = app.invoke({
    "messages": [{"role": "user", "content": "Napisz scraper w Pythonie"}]
})
```

### Kiedy używać `create_supervisor`:

- Szybki prototyp lub proof-of-concept
- Proste scenariusze bez skomplikowanej logiki routingu

### Kiedy NIE używać:

- Produkcja wymagająca kontroli nad kontekstem (co dokładnie trafia do LLM workera)
- Scenariusze z niestandardowym stanem, walidacją, równoległością
- Gdy trzeba optymalizować koszty (mniej tokenów w kontekście)

---

## Supervisor vs Planner — to NIE jest to samo

Supervisor i Planner to **dwa różne wzorce** rozwiązujące inny problem. Oba koordynują wielu agentów, ale różnią się fundamentalnie w sposobie podejmowania decyzji.

### Supervisor: reaktywny koordynator

- Podejmuje decyzję **krok po kroku** — po każdym wykonaniu workera ponownie ewaluuje sytuację.
- Nie tworzy z góry planu — dynamicznie reaguje na wyniki workerów.
- Przepływ: **cykliczny** (supervisor → worker → supervisor → worker → ... → END).
- Analogia: **menedżer na spotkaniu standup** — słucha co się dzieje i na bieżąco przydziela zadania.

### Planner: strategiczny architekt

- **Najpierw tworzy pełny plan** (listę kroków), **potem** wykonuje go sekwencyjnie.
- Separacja faz: **planowanie** i **wykonanie** to oddzielne węzły grafu.
- Opcjonalny **re-planner** po każdym kroku sprawdza, czy plan wymaga korekty.
- Przepływ: **liniowy z opcjonalną pętlą re-planowania**.
- Analogia: **architekt projektu** — rysuje blueprint przed budową.

### Porównanie

| Cecha | Supervisor | Planner |
|---|---|---|
| **Decyzja** | Krok po kroku, reaktywnie | Pełny plan z góry |
| **Struktura** | Cykliczna (hub-and-spoke) | Liniowa (plan → execute → re-plan) |
| **Stan** | `messages` + `next` | `plan: list[str]`, `past_steps`, `response` |
| **Koszt LLM** | Wywołanie supervisora po każdym workerze | Jedno duże wywołanie planera + tańsze wykonania |
| **Najlepsze do** | Zadania nieprzewidywalne, iteracyjne | Zadania dekomponowalne na znane z góry kroki |
| **Obsługa błędów** | Supervisor reaguje na wynik workera | Re-planner adaptuje plan po błędzie |

---

## Planner (Plan-and-Execute) — implementacja w LangGraph

```python
import operator
from typing import Annotated, List
from typing_extensions import TypedDict
from pydantic import BaseModel, Field

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from langgraph.graph import StateGraph, START, END

# ============================================================
# 1. STAN PLANNER-EXECUTOR
# ============================================================

class PlanExecuteState(TypedDict):
    input: str                                          # cel użytkownika
    plan: List[str]                                     # lista kroków do wykonania
    past_steps: Annotated[List[tuple], operator.add]    # (krok, wynik)
    response: str                                       # finalna odpowiedź

# ============================================================
# 2. STRUCTURED OUTPUT DLA PLANERA I RE-PLANERA
# ============================================================

class Plan(BaseModel):
    steps: List[str] = Field(
        description="Lista kroków do wykonania, w kolejności."
    )

class ReplanDecision(BaseModel):
    action: str = Field(
        description="'replan' jeśli plan wymaga zmian, 'finish' jeśli cel osiągnięty."
    )
    updated_plan: List[str] = Field(
        default_factory=list,
        description="Zaktualizowana lista kroków (tylko przy action='replan')."
    )
    response: str = Field(
        default="",
        description="Finalna odpowiedź (tylko przy action='finish')."
    )

llm = ChatOpenAI(model="gpt-4o")
planner_llm = llm.with_structured_output(Plan)
replanner_llm = llm.with_structured_output(ReplanDecision)

# ============================================================
# 3. WĘZŁY
# ============================================================

def planner(state: PlanExecuteState):
    """Tworzy plan kroków na podstawie celu użytkownika."""
    plan = planner_llm.invoke([
        SystemMessage(content="Stwórz plan realizacji zadania. Zwróć listę kroków."),
        HumanMessage(content=state["input"]),
    ])
    return {"plan": plan.steps}

def executor(state: PlanExecuteState):
    """Wykonuje pierwszy krok z planu."""
    current_step = state["plan"][0]
    remaining = state["plan"][1:]

    result = llm.invoke([
        SystemMessage(content="Wykonaj poniższy krok i zwróć wynik."),
        HumanMessage(content=f"Krok: {current_step}\n\nDotychczasowe wyniki: {state['past_steps']}"),
    ])

    return {
        "plan": remaining,
        "past_steps": [(current_step, result.content)],
    }

def replanner(state: PlanExecuteState):
    """Sprawdza czy plan wymaga korekty po wykonaniu kroku."""
    decision = replanner_llm.invoke([
        SystemMessage(
            content="Oceń dotychczasowe postępy. Jeśli cel osiągnięty, zwróć finish. "
                    "Jeśli nie, zwróć zaktualizowany plan."
        ),
        HumanMessage(
            content=f"Cel: {state['input']}\n"
                    f"Wykonane kroki: {state['past_steps']}\n"
                    f"Pozostały plan: {state['plan']}"
        ),
    ])

    if decision.action == "finish":
        return {"response": decision.response}
    return {"plan": decision.updated_plan}

# ============================================================
# 4. ROUTING
# ============================================================

def should_continue(state: PlanExecuteState) -> str:
    if state.get("response"):
        return END
    if not state["plan"]:
        return END
    return "executor"

# ============================================================
# 5. BUDOWA GRAFU
# ============================================================

builder = StateGraph(PlanExecuteState)

builder.add_node("planner", planner)
builder.add_node("executor", executor)
builder.add_node("replanner", replanner)

builder.add_edge(START, "planner")
builder.add_edge("planner", "executor")
builder.add_edge("executor", "replanner")
builder.add_conditional_edges("replanner", should_continue, {
    "executor": "executor",
    END: END,
})

graph = builder.compile()
```

### Przepływ Planner

```
1. START → planner
   LLM generuje: plan = ["zbadaj temat", "napisz wstęp", "napisz konkluzję"]

2. executor
   Wykonuje "zbadaj temat", wynik → past_steps
   plan = ["napisz wstęp", "napisz konkluzję"]

3. replanner
   Ocenia postęp. Plan nadal aktualny → action="replan"

4. executor
   Wykonuje "napisz wstęp"...

5. replanner → executor → replanner...

6. replanner
   Cel osiągnięty → action="finish", response="Gotowe: ..."
   → END
```

---

## Kiedy który wzorzec wybrać?

| Scenariusz | Wzorzec |
|---|---|
| Chatbot obsługi klienta (billing, support, escalation) | **Supervisor** |
| Generowanie raportu z wielu sekcji | **Planner** (lub Orchestrator-Worker) |
| Debugging kodu z nieznanymi przyczynami błędów | **Supervisor** |
| Migracja danych w 5 znanych krokach | **Planner** |
| Asystent z dynamicznym doborem ekspertów | **Supervisor** |
| Pipeline przetwarzania dokumentu | **Planner** |

---

## Powiązane pliki

- [Wzorce Multi-Agentowe (Subagents, Handoffs, Skills, Router)](langchain-multi-agent-patterns.md)
- [Równoległe węzły (Fan-out / Fan-in)](rownolegle-wezly-fan-out-fan-in-langgraph.md)
- [Human-in-the-Loop — Interrupt](human-in-the-loop-interrupt-langgraph.md)
- [Narzędzia dla agentów (Tool Use)](narzedzia-dla-agentow-tool-use-langgraph.md)
- [Pamięć i Persistence — Checkpointers](pamiec-i-persistence-checkpointers-langgraph.md)
- [Wzorce projektowe systemów agentowych](wzorce-projektowe-systemow-agentowych.md)
