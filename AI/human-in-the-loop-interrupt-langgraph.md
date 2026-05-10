# Human-in-the-Loop (Interrupt) w LangGraph

## Krótki opis

LangGraph (≥ 1.0) pozwala **zatrzymać wykonanie grafu w dowolnym miejscu** i poczekać na decyzję lub dane od człowieka, a następnie **wznowić** obliczenia dokładnie tam, gdzie zostały przerwane. Mechanizm opiera się na trzech filarach:

| Element | Import | Rola |
|---|---|---|
| `interrupt()` | `from langgraph.types import interrupt` | Zatrzymuje węzeł i zwraca payload do wywołującego |
| `Command(resume=...)` | `from langgraph.types import Command` | Wznawia graf z wartością podaną przez użytkownika |
| **Checkpointer** | np. `MemorySaver`, `SqliteSaver`, PostgresSaver | Zapisuje stan grafu — bez niego wznowienie jest niemożliwe |

> **Uwaga**: W LangGraph ≥ 1.0 zalecanym sposobem przerywania jest **dynamiczna funkcja `interrupt()`** wywoływana wewnątrz węzła. Starsze podejście `NodeInterrupt` (exception class) zostało zastąpione właśnie przez `interrupt()`. Opcje kompilacji `interrupt_before` / `interrupt_after` nadal istnieją, ale służą głównie do **debugowania** (breakpointy), a nie do logiki HITL.

## Dlaczego to ważne / Kiedy stosować?

- **Zatwierdzanie akcji** — pytanie użytkownika „czy na pewno?" przed wykonaniem nieodwracalnej operacji (wysłanie e-maila, przelew, zapis do bazy).
- **Przegląd i edycja** — LLM generuje treść, człowiek ją poprawia zanim trafi dalej.
- **Walidacja danych** — zbieranie danych od użytkownika z walidacją i re-promptem.
- **Moderacja treści** — automatyczne zatrzymanie grafu, gdy wykryto wrażliwą treść.
- **Nadzór nad klasyfikacją** — pokazanie użytkownikowi wyniku klasyfikacji do potwierdzenia.

---

## Jak działa `interrupt()` — model mentalny

```
1. Graf dochodzi do wywołania interrupt(payload)
2. Stan jest zapisywany przez checkpointer
3. Wykonanie jest WSTRZYMANE
4. Payload trafia do wywołującego (result["__interrupt__"])
5. Użytkownik podejmuje decyzję
6. Wywołanie: graph.invoke(Command(resume=odpowiedź), config)
7. Węzeł z interrupt() RESTARTUJE SIĘ od początku
8. interrupt() zwraca wartość z Command(resume=...)
9. Reszta węzła wykonuje się normalnie
```

**Kluczowa zasada**: po wznowieniu węzeł restartuje się **od początku**. Cały kod przed `interrupt()` wykonuje się ponownie. Dlatego side-effecty przed `interrupt()` muszą być **idempotentne**.

---

## Wymagania

1. **Checkpointer** — graf musi być skompilowany z checkpointerem:

```python
from langgraph.checkpoint.memory import MemorySaver

graph = builder.compile(checkpointer=MemorySaver())
```

2. **`thread_id`** — każde wywołanie wymaga identyfikatora wątku:

```python
config = {"configurable": {"thread_id": "my-thread-1"}}
```

3. **JSON-serializowalny payload** — wartość przekazywana do `interrupt()` musi być serializowalna (string, dict, list, number, bool).

---

## Podstawowy wzorzec: Approve / Reject

Najprostszy scenariusz — zatrzymaj graf, zapytaj o zgodę, kontynuuj lub anuluj:

```python
from typing import Literal, Optional, TypedDict

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command, interrupt


class ApprovalState(TypedDict):
    action_details: str
    status: Optional[Literal["pending", "approved", "rejected"]]


def approval_node(state: ApprovalState) -> Command[Literal["proceed", "cancel"]]:
    """Zatrzymuje graf i pyta użytkownika o zatwierdzenie."""
    decision = interrupt({
        "question": "Czy zatwierdzasz tę akcję?",
        "details": state["action_details"],
    })

    # Po wznowieniu — decision to wartość z Command(resume=...)
    return Command(goto="proceed" if decision else "cancel")


def proceed_node(state: ApprovalState):
    return {"status": "approved"}


def cancel_node(state: ApprovalState):
    return {"status": "rejected"}


# Budowa grafu
builder = StateGraph(ApprovalState)
builder.add_node("approval", approval_node)
builder.add_node("proceed", proceed_node)
builder.add_node("cancel", cancel_node)

builder.add_edge(START, "approval")
builder.add_edge("proceed", END)
builder.add_edge("cancel", END)

graph = builder.compile(checkpointer=MemorySaver())
```

### Uruchomienie i wznowienie

```python
config = {"configurable": {"thread_id": "approval-001"}}

# Krok 1: invoke — graf zatrzymuje się na interrupt()
result = graph.invoke(
    {"action_details": "Przelew 500 PLN", "status": "pending"},
    config=config,
)
print(result["__interrupt__"])
# -> [Interrupt(value={'question': 'Czy zatwierdzasz...', 'details': 'Przelew 500 PLN'})]

# Krok 2: wznowienie z decyzją użytkownika
final = graph.invoke(Command(resume=True), config=config)
print(final["status"])
# -> "approved"
```

---

## Scenariusz 1: Terapeuta proponuje ćwiczenie

Graf terapeutyczny, w którym AI proponuje ćwiczenie relaksacyjne, a użytkownik decyduje czy chce je wykonać:

```python
from typing import Optional, TypedDict
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command, interrupt


class TherapyState(TypedDict):
    user_message: str
    proposed_exercise: Optional[str]
    exercise_accepted: Optional[bool]
    final_response: Optional[str]


llm = ChatOpenAI(model="gpt-4o")


def analyze_node(state: TherapyState):
    """Analizuje wiadomość użytkownika i proponuje ćwiczenie."""
    response = llm.invoke([
        SystemMessage(
            content="Jesteś terapeutą. Na podstawie wiadomości użytkownika "
                    "zaproponuj jedno konkretne ćwiczenie relaksacyjne lub "
                    "terapeutyczne. Opisz je w 2-3 zdaniach."
        ),
        HumanMessage(content=state["user_message"]),
    ])
    return {"proposed_exercise": response.content}


def approval_node(state: TherapyState):
    """Zatrzymuje graf i pyta użytkownika czy chce wykonać ćwiczenie."""
    decision = interrupt({
        "question": "Czy chcesz wykonać proponowane ćwiczenie?",
        "exercise": state["proposed_exercise"],
    })
    return {"exercise_accepted": decision}


def exercise_node(state: TherapyState):
    """Prowadzi użytkownika przez ćwiczenie (gdy zaakceptował)."""
    response = llm.invoke([
        SystemMessage(
            content="Poprowadź użytkownika krok po kroku przez to ćwiczenie: "
                    f"{state['proposed_exercise']}"
        ),
        HumanMessage(content="Prowadź mnie przez ćwiczenie."),
    ])
    return {"final_response": response.content}


def skip_node(state: TherapyState):
    """Użytkownik odrzucił ćwiczenie."""
    return {"final_response": "Rozumiem. Jeśli zmienisz zdanie, jestem tu dla Ciebie."}


def route_after_approval(state: TherapyState):
    if state.get("exercise_accepted"):
        return "exercise"
    return "skip"


# Budowa grafu
builder = StateGraph(TherapyState)
builder.add_node("analyze", analyze_node)
builder.add_node("approval", approval_node)
builder.add_node("exercise", exercise_node)
builder.add_node("skip", skip_node)

builder.add_edge(START, "analyze")
builder.add_edge("analyze", "approval")
builder.add_conditional_edges("approval", route_after_approval)
builder.add_edge("exercise", END)
builder.add_edge("skip", END)

graph = builder.compile(checkpointer=MemorySaver())
```

### Przepływ

```
START → analyze → approval ──(interrupt)──→ exercise → END
                                        └→ skip    → END
```

### Uruchomienie

```python
config = {"configurable": {"thread_id": "therapy-session-1"}}

# AI analizuje i proponuje ćwiczenie, potem STOP
result = graph.invoke(
    {"user_message": "Czuję się bardzo zestresowany po całym dniu"},
    config=config,
)
print(result["__interrupt__"][0].value["exercise"])
# -> "Proponuję ćwiczenie głębokiego oddychania 4-7-8..."

# Użytkownik akceptuje
final = graph.invoke(Command(resume=True), config=config)
print(final["final_response"])
# -> Szczegółowe instrukcje ćwiczenia krok po kroku
```

---

## Scenariusz 2: Weryfikacja klasyfikacji

Graf klasyfikuje intencję użytkownika, pokazuje wynik i pyta czy się zgadza. Jeśli nie — użytkownik podaje poprawną klasyfikację:

```python
from typing import Optional, TypedDict
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command, interrupt


class ClassificationState(TypedDict):
    user_message: str
    ai_classification: Optional[str]
    final_classification: Optional[str]
    response: Optional[str]


llm = ChatOpenAI(model="gpt-4o")

CATEGORIES = ["emocjonalne", "praktyczne", "medyczne", "relacyjne"]


def classify_node(state: ClassificationState):
    """AI klasyfikuje wiadomość."""
    response = llm.invoke([
        SystemMessage(
            content=f"Sklasyfikuj wiadomość użytkownika do jednej z kategorii: "
                    f"{', '.join(CATEGORIES)}. Zwróć TYLKO nazwę kategorii."
        ),
        HumanMessage(content=state["user_message"]),
    ])
    return {"ai_classification": response.content.strip().lower()}


def verify_node(state: ClassificationState):
    """Pokazuje klasyfikację i pyta użytkownika czy się zgadza."""
    user_decision = interrupt({
        "question": "Czy zgadzasz się z tą klasyfikacją?",
        "classification": state["ai_classification"],
        "available_categories": CATEGORIES,
        "instruction": "Odpowiedz True jeśli tak, lub podaj poprawną kategorię jako string.",
    })

    if user_decision is True:
        return {"final_classification": state["ai_classification"]}
    else:
        # Użytkownik podał poprawną kategorię
        return {"final_classification": user_decision}


def respond_node(state: ClassificationState):
    """Generuje odpowiedź dopasowaną do kategorii."""
    response = llm.invoke([
        SystemMessage(
            content=f"Odpowiedz użytkownikowi. Jego problem został sklasyfikowany "
                    f"jako: {state['final_classification']}. Dopasuj ton odpowiedzi."
        ),
        HumanMessage(content=state["user_message"]),
    ])
    return {"response": response.content}


builder = StateGraph(ClassificationState)
builder.add_node("classify", classify_node)
builder.add_node("verify", verify_node)
builder.add_node("respond", respond_node)

builder.add_edge(START, "classify")
builder.add_edge("classify", "verify")
builder.add_edge("verify", "respond")
builder.add_edge("respond", END)

graph = builder.compile(checkpointer=MemorySaver())
```

### Uruchomienie

```python
config = {"configurable": {"thread_id": "classification-1"}}

result = graph.invoke(
    {"user_message": "Kłócę się z partnerem o finanse"},
    config=config,
)
print(result["__interrupt__"][0].value)
# -> {'question': 'Czy zgadzasz się...', 'classification': 'relacyjne', ...}

# Użytkownik zgadza się z klasyfikacją
final = graph.invoke(Command(resume=True), config=config)
print(final["final_classification"])  # -> "relacyjne"

# LUB użytkownik poprawia klasyfikację
final = graph.invoke(Command(resume="praktyczne"), config=config)
print(final["final_classification"])  # -> "praktyczne"
```

---

## Scenariusz 3: Moderacja treści wrażliwej

Graf sprawdza czy treść jest wrażliwa. Jeśli tak — zatrzymuje się i czeka na decyzję moderatora:

```python
from typing import Literal, Optional, TypedDict
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command, interrupt


class ModerationState(TypedDict):
    user_message: str
    is_sensitive: Optional[bool]
    sensitivity_reason: Optional[str]
    moderator_decision: Optional[Literal["allow", "block", "edit"]]
    final_message: Optional[str]


llm = ChatOpenAI(model="gpt-4o")


def detect_node(state: ModerationState):
    """Wykrywa czy treść jest wrażliwa."""
    response = llm.invoke([
        SystemMessage(
            content="Oceń czy poniższa wiadomość zawiera wrażliwe treści "
                    "(przemoc, dyskryminacja, dane osobowe, treści seksualne). "
                    "Odpowiedz w formacie JSON: "
                    '{\"is_sensitive\": true/false, \"reason\": \"opis\"}'
        ),
        HumanMessage(content=state["user_message"]),
    ])
    import json
    result = json.loads(response.content)
    return {
        "is_sensitive": result["is_sensitive"],
        "sensitivity_reason": result.get("reason", ""),
    }


def route_after_detection(state: ModerationState):
    if state.get("is_sensitive"):
        return "moderate"
    return "pass_through"


def moderate_node(state: ModerationState):
    """Zatrzymuje graf i czeka na decyzję moderatora."""
    decision = interrupt({
        "alert": "Wykryto wrażliwą treść!",
        "message": state["user_message"],
        "reason": state["sensitivity_reason"],
        "options": ["allow", "block", "edit"],
        "instruction": (
            "Odpowiedz słownikiem: {'action': 'allow'|'block'|'edit', "
            "'edited_message': '...' (tylko gdy action='edit')}"
        ),
    })

    action = decision.get("action", "block")

    if action == "edit":
        return {
            "moderator_decision": "edit",
            "final_message": decision.get("edited_message", state["user_message"]),
        }
    elif action == "allow":
        return {
            "moderator_decision": "allow",
            "final_message": state["user_message"],
        }
    else:
        return {
            "moderator_decision": "block",
            "final_message": "[Treść zablokowana przez moderatora]",
        }


def pass_through_node(state: ModerationState):
    """Treść przechodzi bez moderacji."""
    return {
        "moderator_decision": "allow",
        "final_message": state["user_message"],
    }


builder = StateGraph(ModerationState)
builder.add_node("detect", detect_node)
builder.add_node("moderate", moderate_node)
builder.add_node("pass_through", pass_through_node)

builder.add_edge(START, "detect")
builder.add_conditional_edges("detect", route_after_detection)
builder.add_edge("moderate", END)
builder.add_edge("pass_through", END)

graph = builder.compile(checkpointer=MemorySaver())
```

### Uruchomienie

```python
config = {"configurable": {"thread_id": "moderation-1"}}

result = graph.invoke(
    {"user_message": "Wiadomość z potencjalnie wrażliwą treścią..."},
    config=config,
)

if "__interrupt__" in result:
    print(result["__interrupt__"][0].value)
    # -> {'alert': 'Wykryto wrażliwą treść!', 'message': '...', ...}

    # Moderator decyduje — edytuje treść
    final = graph.invoke(
        Command(resume={"action": "edit", "edited_message": "Poprawiona treść"}),
        config=config,
    )
    print(final["final_message"])   # -> "Poprawiona treść"
    print(final["moderator_decision"])  # -> "edit"
```

---

## Wiele interrupt() w równoległych węzłach

Gdy wiele węzłów wywołuje `interrupt()` w tym samym superstepie, wszystkie przerwania są zbierane razem. Wznowienie wymaga mapowania `interrupt_id → resume_value`:

```python
import operator
from typing import Annotated, TypedDict

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, END, StateGraph
from langgraph.types import Command, interrupt


class State(TypedDict):
    vals: Annotated[list[str], operator.add]


def node_a(state):
    answer = interrupt("Pytanie od węzła A")
    return {"vals": [f"a:{answer}"]}


def node_b(state):
    answer = interrupt("Pytanie od węzła B")
    return {"vals": [f"b:{answer}"]}


graph = (
    StateGraph(State)
    .add_node("a", node_a)
    .add_node("b", node_b)
    .add_edge(START, "a")
    .add_edge(START, "b")   # a i b uruchamiają się równolegle
    .add_edge("a", END)
    .add_edge("b", END)
    .compile(checkpointer=MemorySaver())
)

config = {"configurable": {"thread_id": "parallel-1"}}

# Oba węzły trafiają na interrupt()
result = graph.invoke({"vals": []}, config)
print(result["__interrupt__"])
# -> [Interrupt(value='Pytanie od węzła A', id='...'),
#     Interrupt(value='Pytanie od węzła B', id='...')]

# Wznów oba naraz — mapowanie id → odpowiedź
resume_map = {
    i.id: f"odpowiedź na {i.value}" for i in result["__interrupt__"]
}
final = graph.invoke(Command(resume=resume_map), config)
print(final["vals"])
# -> ['a:odpowiedź na Pytanie od węzła A', 'b:odpowiedź na Pytanie od węzła B']
```

---

## Walidacja inputu z pętlą

`interrupt()` można wywołać wielokrotnie w pętli — graf zatrzymuje się na każdym wywołaniu i wraca z odpowiedzią:

```python
from langgraph.types import interrupt


def collect_age_node(state):
    prompt = "Ile masz lat?"
    while True:
        answer = interrupt(prompt)
        if isinstance(answer, int) and answer > 0:
            return {"age": answer}
        prompt = f"'{answer}' nie jest prawidłowym wiekiem. Podaj liczbę dodatnią."
```

```python
# Pierwsze wywołanie — pyta o wiek
result = graph.invoke({"age": None}, config)
# -> Interrupt(value='Ile masz lat?')

# Użytkownik podaje tekst — walidacja nie przechodzi
retry = graph.invoke(Command(resume="trzydzieści"), config)
# -> Interrupt(value="'trzydzieści' nie jest prawidłowym wiekiem...")

# Użytkownik podaje liczbę — sukces
final = graph.invoke(Command(resume=30), config)
print(final["age"])  # -> 30
```

---

## Breakpointy kompilacji: `interrupt_before` / `interrupt_after`

Alternatywny, prostszy mechanizm — przerwanie **przed** lub **po** konkretnym węźle. Głównie do **debugowania**, nie do złożonej logiki HITL:

```python
graph = builder.compile(
    checkpointer=checkpointer,
    interrupt_before=["critical_node"],    # zatrzymaj PRZED
    interrupt_after=["analysis_node"],     # zatrzymaj PO
)

config = {"configurable": {"thread_id": "debug-1"}}

# Graf zatrzymuje się przed critical_node
graph.invoke(inputs, config=config)

# Wznów — bez Command, po prostu None
graph.invoke(None, config=config)
```

Można też ustawić breakpointy w **runtime** (bez zmiany kompilacji):

```python
graph.invoke(
    inputs,
    interrupt_before=["node_a"],
    interrupt_after=["node_b"],
    config=config,
)
```

---

## Zasady korzystania z `interrupt()`

### ✅ Poprawne użycie

| Zasada | Przykład |
|---|---|
| Oddzielaj `interrupt()` od `try/except` | Najpierw `interrupt()`, potem `try: fetch_data()` |
| Stała kolejność wywołań | `name = interrupt(...)` → `age = interrupt(...)` — zawsze ta sama kolejność |
| Proste typy w payload | `interrupt("pytanie")`, `interrupt({"key": "value"})` |
| Idempotentne operacje przed `interrupt()` | `db.upsert(...)` zamiast `db.insert(...)` |

### ❌ Błędy

| Błąd | Dlaczego |
|---|---|
| `try: interrupt(...) except:` | `interrupt()` rzuca wewnętrzny wyjątek — `except` go złapie |
| Warunkowe pomijanie `interrupt()` | Zmienia kolejność wywołań między executions |
| Przekazywanie funkcji/klas do `interrupt()` | Nie da się serializować do JSON |
| `db.create_record()` przed `interrupt()` | Wykona się ponownie po wznowieniu → duplikaty |

---

## Porównanie podejść do HITL

| Mechanizm | Kiedy użyć | Elastyczność | Złożoność |
|---|---|---|---|
| `interrupt()` + `Command(resume=...)` | Logika HITL w produkcji | Wysoka — dynamiczne, warunkowe | Średnia |
| `interrupt_before` / `interrupt_after` | Debugowanie, proste breakpointy | Niska — stałe punkty zatrzymania | Niska |
| `NodeInterrupt` (legacy) | **Nie używaj** — zastąpione przez `interrupt()` | — | — |

---

## Podsumowanie

```
┌─────────────────────────────────────────────────┐
│              HUMAN-IN-THE-LOOP                  │
│                                                 │
│  1. interrupt(payload)  →  zatrzymaj graf       │
│  2. Checkpointer        →  zapisz stan          │
│  3. Payload             →  pokaż użytkownikowi  │
│  4. Command(resume=v)   →  wznów z odpowiedzią  │
│  5. Węzeł restartuje    →  interrupt() zwraca v │
│                                                 │
│  Pamiętaj:                                      │
│  • Checkpointer jest WYMAGANY                   │
│  • thread_id identyfikuje sesję                 │
│  • Kod przed interrupt() musi być idempotentny  │
│  • Payload musi być JSON-serializowalny         │
└─────────────────────────────────────────────────┘
```

---

## Powiązane pliki

- [Pamięć i Persistence — Checkpointers](pamiec-i-persistence-checkpointers-langgraph.md)
- [Narzędzia dla agentów (Tool Use)](narzedzia-dla-agentow-tool-use-langgraph.md)
- [Równoległe węzły (Fan-out / Fan-in)](rownolegle-wezly-fan-out-fan-in-langgraph.md)
- [Wzorce projektowe systemów agentowych](wzorce-projektowe-systemow-agentowych.md)
- [Wzorce Multi-Agentowe (Subagents, Handoffs, Skills, Router)](langchain-multi-agent-patterns.md)
