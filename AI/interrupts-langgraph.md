# Interrupts w LangGraph — przerwania, HITL, wznowienie

## Czym są Interrupts

Interrupt to mechanizm **wstrzymania wykonania grafu** w dowolnym miejscu, zapisania stanu przez checkpointer i oczekiwania na zewnętrzny input (człowiek, API, inny system). Po otrzymaniu odpowiedzi graf **wznawia się** dokładnie w węźle, który wywołał przerwanie.

| Prymityw | Import | Rola |
|---|---|---|
| `interrupt(value)` | `from langgraph.types import interrupt` | Wstrzymuje węzeł, emituje `value` do wywołującego |
| `Command(resume=v)` | `from langgraph.types import Command` | Wznawia graf — `v` staje się wartością zwracaną przez `interrupt()` |
| `Command(resume=map)` | j.w. | Wznawia wiele równoległych przerwań naraz (mapowanie `id → value`) |
| Checkpointer | `MemorySaver`, `InMemorySaver`, `SqliteSaver`, `PostgresSaver` | Persystencja stanu — **wymagany** do działania przerwań |

---

## Czy istnieje klasa HumanInTheLoop?

**Nie.** W LangGraph ≥ 1.0 nie ma klasy `HumanInTheLoop` ani middleware HITL w stylu LangChain. Cały mechanizm Human-in-the-Loop opiera się na:

1. **`interrupt()`** — wbudowana funkcja prymitywna (nie middleware)
2. **`Command(resume=...)`** — wznowienie z wartością od człowieka
3. **Checkpointer** — zapis stanu między przerwaniem a wznowieniem

Starsze podejścia (`NodeInterrupt` exception, middleware `HumanInTheLoop`) zostały zastąpione przez `interrupt()`. Jeśli napotkasz te nazwy w tutorialach — są nieaktualne.

---

## Model mentalny — cykl życia przerwania

```
1. Graf wykonuje węzeł → trafia na interrupt(payload)
2. Checkpointer zapisuje stan grafu
3. Wykonanie WSTRZYMANE
4. Payload dostępny dla wywołującego:
   - invoke():  result["__interrupt__"]        (v1)
   - invoke():  result.interrupts              (v2, ≥ 1.1)
   - stream():  chunk z __interrupt__ w updates
5. Człowiek / system podejmuje decyzję
6. graph.invoke(Command(resume=odpowiedź), config)
7. Węzeł RESTARTUJE SIĘ OD POCZĄTKU
8. interrupt() zwraca wartość z resume
9. Reszta węzła wykonuje się normalnie
```

**Kluczowe**: po wznowieniu węzeł restartuje się **od początku**. Kod przed `interrupt()` wykonuje się ponownie — musi być **idempotentny**.

---

## Wymagania

```python
from langgraph.checkpoint.memory import MemorySaver  # dev
# lub InMemorySaver, SqliteSaver, PostgresSaver

graph = builder.compile(checkpointer=MemorySaver())
config = {"configurable": {"thread_id": "unique-id"}}
```

1. **Checkpointer** — bez niego `interrupt()` rzuci błąd
2. **`thread_id`** — identyfikuje sesję; ten sam ID przy invoke i resume
3. **JSON-serializowalny payload** — string, dict, list, number, bool

---

## Wykrywanie przerwań

### Sposób 1: `invoke()` z `version="v2"` (zalecane od LangGraph ≥ 1.1)

```python
result = graph.invoke({"input": "data"}, config=config, version="v2")

# result to GraphOutput z atrybutami .value i .interrupts
if result.interrupts:
    for intr in result.interrupts:
        print(f"Przerwanie: {intr.value}")
        print(f"ID: {intr.id}")
```

### Sposób 2: `invoke()` z `version="v1"` (domyślne)

```python
result = graph.invoke({"input": "data"}, config=config)

if "__interrupt__" in result:
    for intr in result["__interrupt__"]:
        print(f"Przerwanie: {intr.value}")
```

### Sposób 3: `get_state()` — inspekcja stanu wątku

```python
snapshot = graph.get_state(config)
if snapshot.tasks and snapshot.tasks[0].interrupts:
    for intr in snapshot.tasks[0].interrupts:
        print(f"Oczekujące przerwanie: {intr.value}")
```

#### Na czym polega oddzielenie procesów

W trybie `invoke()` / `stream()` wywołujący proces **blokuje się** do momentu przerwania i od razu widzi `__interrupt__` w wyniku. To działa w skryptach i notebookach, ale **nie w web appach**, gdzie:

1. **Proces A** (worker / background task) uruchamia graf — `graph.invoke(input, config)` — i kończy swoje działanie po napotkaniu `interrupt()`.
2. **Proces B** (HTTP endpoint) — obsługuje request od użytkownika minuty/godziny później. Nie ma referencji do oryginalnego `result`. Musi **samodzielnie** sprawdzić, czy dany wątek czeka na odpowiedź.

`get_state(config)` pozwala **dowolnemu procesowi** w dowolnym momencie odpytać checkpointer o aktualny stan wątku — bez konieczności trzymania referencji do wyniku `invoke()`. Wystarczy znać `thread_id`.

#### Co zwraca `get_state()`

```python
snapshot = graph.get_state(config)

snapshot.values          # aktualny stan grafu (dict)
snapshot.next            # tuple nazw węzłów do wykonania (puste = graf zakończony)
snapshot.tasks           # lista PregelTask — aktywne taski
snapshot.tasks[0].interrupts  # lista Interrupt jeśli węzeł jest wstrzymany
snapshot.config          # config z checkpoint_id (do time-travel)
```

Jeśli `snapshot.tasks` jest niepuste i zawiera `interrupts` — graf czeka na `Command(resume=...)`.

#### Przykład: FastAPI + background worker

Architektura:
- **POST /expenses** — endpoint przyjmuje wydatek, uruchamia graf w tle
- **GET /expenses/{thread_id}/status** — sprawdza czy graf czeka na input
- **POST /expenses/{thread_id}/resume** — wysyła decyzję i wznawia graf

```python
from contextlib import asynccontextmanager

from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel

from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.types import Command

from expense_graph import build_graph  # graf z przykładu wyżej


# Checkpointer współdzielony między procesami — dlatego PostgreSQL
DB_URI = "postgresql://user:pass@localhost:5432/langgraph"
checkpointer = PostgresSaver.from_conn_string(DB_URI)


@asynccontextmanager
async def lifespan(app: FastAPI):
    checkpointer.setup()  # tworzy tabele jeśli nie istnieją
    yield


app = FastAPI(lifespan=lifespan)
graph = build_graph(checkpointer)


class ExpenseRequest(BaseModel):
    description: str
    amount: float


class ResumeRequest(BaseModel):
    value: dict  # np. {"approved": True, "note": "ok"} lub True


# ── PROCES A: uruchom graf w tle ────────────────────

def run_graph_background(thread_id: str, data: dict):
    """Worker — uruchamia graf. Po interrupt() funkcja wraca."""
    config = {"configurable": {"thread_id": thread_id}}
    graph.invoke(data, config=config)
    # Jeśli graf trafił na interrupt() — invoke() wraca z wynikiem,
    # stan jest zapisany w PostgreSQL. Worker kończy pracę.


@app.post("/expenses")
def create_expense(req: ExpenseRequest, bg: BackgroundTasks):
    thread_id = f"expense-{req.description[:20]}-{req.amount}"
    bg.add_task(run_graph_background, thread_id, req.model_dump())
    return {"thread_id": thread_id, "status": "started"}


# ── PROCES B: sprawdź stan i wznów ─────────────────

@app.get("/expenses/{thread_id}/status")
def get_status(thread_id: str):
    """Odpytaj checkpointer — czy graf czeka na input?"""
    config = {"configurable": {"thread_id": thread_id}}
    snapshot = graph.get_state(config)

    if not snapshot.values:
        raise HTTPException(404, "Wątek nie istnieje")

    # Czy są oczekujące przerwania?
    pending = []
    for task in snapshot.tasks:
        for intr in task.interrupts:
            pending.append({
                "id": intr.id,
                "value": intr.value,  # payload z interrupt()
            })

    return {
        "thread_id": thread_id,
        "state": snapshot.values,
        "next_nodes": snapshot.next,          # co graf chce wykonać dalej
        "pending_interrupts": pending,        # [] = nie czeka
        "is_waiting": len(pending) > 0,
    }


@app.post("/expenses/{thread_id}/resume")
def resume_expense(thread_id: str, req: ResumeRequest):
    """Wznów graf z decyzją użytkownika."""
    config = {"configurable": {"thread_id": thread_id}}

    # Sprawdź czy faktycznie czeka
    snapshot = graph.get_state(config)
    has_interrupts = any(
        task.interrupts for task in snapshot.tasks
    )
    if not has_interrupts:
        raise HTTPException(400, "Graf nie czeka na input")

    result = graph.invoke(Command(resume=req.value), config=config)

    # Sprawdź czy jest kolejny interrupt (np. po classify → approve)
    new_snapshot = graph.get_state(config)
    new_pending = []
    for task in new_snapshot.tasks:
        for intr in task.interrupts:
            new_pending.append({"id": intr.id, "value": intr.value})

    return {
        "state": result if isinstance(result, dict) else result.value,
        "pending_interrupts": new_pending,
        "is_complete": len(new_pending) == 0 and not new_snapshot.next,
    }
```

#### Przepływ z perspektywy klienta (curl / frontend)

```bash
# 1. Utwórz wydatek — graf startuje w tle
curl -X POST localhost:8000/expenses \
  -d '{"description": "Hotel PyCon", "amount": 3200}'
# -> {"thread_id": "expense-Hotel PyCon-3200.0", "status": "started"}

# 2. Po chwili — sprawdź czy graf czeka (polling)
curl localhost:8000/expenses/expense-Hotel%20PyCon-3200.0/status
# -> {
#   "is_waiting": true,
#   "pending_interrupts": [{
#     "id": "abc123",
#     "value": {"type": "confirm_category", "suggested_category": "podróże", ...}
#   }]
# }

# 3. Zatwierdź kategorię
curl -X POST localhost:8000/expenses/expense-Hotel%20PyCon-3200.0/resume \
  -d '{"value": true}'
# -> {
#   "pending_interrupts": [{"value": {"type": "manager_approval", ...}}],
#   "is_complete": false
# }

# 4. Manager zatwierdza
curl -X POST localhost:8000/expenses/expense-Hotel%20PyCon-3200.0/resume \
  -d '{"value": {"approved": true, "note": "OK"}}'
# -> {"is_complete": true, "state": {"approval_status": "approved", ...}}
```

#### Dlaczego to wymaga trwałego checkpointera

`MemorySaver` trzyma stan w pamięci jednego procesu. Jeśli worker (proces A) i HTTP server (proces B) to osobne procesy — nie współdzielą pamięci. Dlatego w tym wzorcu **wymagany** jest `PostgresSaver` lub `SqliteSaver` — stan jest w bazie danych, dostępny z dowolnego procesu.

| Checkpointer | Oddzielne procesy | Produkcja |
|---|---|---|
| `MemorySaver` / `InMemorySaver` | ❌ Nie — tylko ten sam proces | Nie |
| `SqliteSaver` | ✅ Tak — plik na dysku | Dev / staging |
| `PostgresSaver` | ✅ Tak — baza sieciowa | Tak |

### Sposób 4: Streaming z detekcją przerwań

```python
for chunk in graph.stream(
    initial_input,
    stream_mode=["messages", "updates"],
    subgraphs=True,
    config=config,
    version="v2",
):
    if chunk["type"] == "updates":
        if "__interrupt__" in chunk["data"]:
            interrupt_info = chunk["data"]["__interrupt__"][0]
            print(f"Przerwanie: {interrupt_info.value}")
            break
    elif chunk["type"] == "messages":
        msg, _ = chunk["data"]
        if hasattr(msg, "content") and msg.content:
            print(msg.content, end="", flush=True)
```

> `subgraphs=True` jest wymagane do wykrywania przerwań w zagnieżdżonych grafach.

---

## Wznowienie grafu

```python
from langgraph.types import Command

# Prosty resume — wartość trafia jako return z interrupt()
graph.invoke(Command(resume=True), config=config)
graph.invoke(Command(resume="odpowiedź tekstowa"), config=config)
graph.invoke(Command(resume={"action": "approve", "note": "ok"}), config=config)
```

### Command z dodatkowymi opcjami

```python
# resume + goto — wznów i wymuś przejście do konkretnego węzła
Command(resume=value, goto="target_node")

# resume + update — wznów i zmodyfikuj stan grafu
Command(resume=value, update={"key": "new_value"})
```

### Wznowienie breakpointów (interrupt_before / interrupt_after)

```python
# Breakpointy nie używają Command — wznowienie przez None
graph.invoke(None, config=config)
```

---

## Wzorce użycia

### Approve / Reject

```python
from typing import Literal
from langgraph.types import interrupt, Command


def approval_node(state) -> Command[Literal["proceed", "cancel"]]:
    decision = interrupt({
        "question": "Zatwierdzasz tę operację?",
        "details": state["action"],
    })
    return Command(goto="proceed" if decision else "cancel")
```

### Review & Edit

```python
def review_node(state):
    edited = interrupt({
        "instruction": "Sprawdź i popraw treść",
        "content": state["generated_text"],
    })
    # edited = wartość z Command(resume="poprawiony tekst")
    return {"generated_text": edited}
```

### Walidacja w pętli

```python
def collect_age_node(state):
    prompt = "Ile masz lat?"
    while True:
        answer = interrupt(prompt)
        if isinstance(answer, int) and 0 < answer < 150:
            return {"age": answer}
        prompt = f"'{answer}' nie jest prawidłowym wiekiem. Podaj liczbę."
```

Każda iteracja pętli to osobne przerwanie → osobne wznowienie. Graf zatrzymuje się na każdym `interrupt()`.

### Interrupt wewnątrz narzędzia (@tool)

```python
from langchain.tools import tool
from langgraph.types import interrupt


@tool
def send_email(to: str, subject: str, body: str):
    """Wysyła e-mail po zatwierdzeniu."""
    response = interrupt({
        "action": "send_email",
        "to": to,
        "subject": subject,
        "body": body,
        "message": "Zatwierdź wysłanie e-maila",
    })

    if response.get("action") == "approve":
        final_to = response.get("to", to)
        final_subject = response.get("subject", subject)
        final_body = response.get("body", body)
        return f"Wysłano do {final_to}: {final_subject}"
    return "Anulowano przez użytkownika"
```

Użytkownik może nie tylko zatwierdzić, ale też **edytować** parametry narzędzia przed wykonaniem.

---

## Wiele przerwań w równoległych węzłach

Gdy wiele węzłów wywołuje `interrupt()` w tym samym superstepie, wszystkie przerwania zbierane są razem. Wznowienie wymaga mapowania `interrupt_id → resume_value`:

```python
import operator
from typing import Annotated, TypedDict
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import START, END, StateGraph
from langgraph.types import Command, interrupt


class State(TypedDict):
    vals: Annotated[list[str], operator.add]


def node_a(state):
    answer = interrupt("Pytanie A")
    return {"vals": [f"a:{answer}"]}


def node_b(state):
    answer = interrupt("Pytanie B")
    return {"vals": [f"b:{answer}"]}


graph = (
    StateGraph(State)
    .add_node("a", node_a)
    .add_node("b", node_b)
    .add_edge(START, "a")
    .add_edge(START, "b")  # równoległe
    .add_edge("a", END)
    .add_edge("b", END)
    .compile(checkpointer=InMemorySaver())
)

config = {"configurable": {"thread_id": "parallel-1"}}

result = graph.invoke({"vals": []}, config)
# result["__interrupt__"] zawiera 2 obiekty Interrupt z unikalnymi id

resume_map = {
    i.id: f"odpowiedź na {i.value}" for i in result["__interrupt__"]
}
final = graph.invoke(Command(resume=resume_map), config)
print(final["vals"])
# -> ['a:odpowiedź na Pytanie A', 'b:odpowiedź na Pytanie B']
```

---

## Interrupts w subgrafach

Gdy subgraf zawiera `interrupt()`, przerwanie propaguje się do grafu nadrzędnego. Przy wznowieniu cały stos jest odtwarzany:

```python
def node_in_parent(state):
    some_code()            # ← wykona się ponownie przy resume
    result = subgraph.invoke(input_data)
    return {"result": result}


def node_in_subgraph(state):
    other_code()           # ← wykona się ponownie przy resume
    answer = interrupt("Pytanie z subgrafu")
    return {"answer": answer}
```

Detekcja w streamingu wymaga `subgraphs=True`. Pole `ns` w `StreamPart` identyfikuje źródło (pusta krotka = root).

---

## Breakpointy: `interrupt_before` / `interrupt_after`

Prostszy mechanizm — zatrzymanie **przed** lub **po** konkretnym węźle. Służy do **debugowania**, nie do logiki HITL:

```python
# Przy kompilacji
graph = builder.compile(
    checkpointer=checkpointer,
    interrupt_before=["critical_node"],
    interrupt_after=["analysis_node"],
)

# Lub w runtime (bez zmiany kompilacji)
graph.invoke(
    inputs,
    interrupt_before=["node_a"],
    interrupt_after=["node_b"],
    config=config,
)

# Wznowienie — None zamiast Command
graph.invoke(None, config=config)
```

---

## Zasady korzystania z interrupt()

### ✅ Poprawne

| Zasada | Dlaczego |
|---|---|
| Oddzielaj `interrupt()` od `try/except` | `interrupt()` rzuca wewnętrzny wyjątek — bare `except` go złapie |
| Stała kolejność wywołań | LangGraph dopasowuje resume values indeksem — zmiana kolejności = błąd |
| Proste typy w payload | Muszą być JSON-serializowalne |
| Idempotentne operacje przed `interrupt()` | Kod przed interrupt wykona się ponownie po wznowieniu |
| Side-effecty po `interrupt()` lub w osobnym węźle | Unikaj duplikatów |

### ❌ Błędy

```python
# ❌ try/except łapie wewnętrzny wyjątek interrupt
try:
    interrupt("pytanie")
except Exception:
    pass  # interrupt nigdy nie zadziała

# ❌ Warunkowe pomijanie interrupt — zmienia indeksowanie
if state.get("needs_age"):
    age = interrupt("Wiek?")  # pomijane = shift indeksów

# ❌ Nieserializowalny payload
interrupt({"validator": lambda x: x > 0})  # funkcja

# ❌ db.create_record() przed interrupt — duplikaty po resume
db.create_audit_log(...)  # użyj db.upsert(...) zamiast tego
```

---

## Porównanie mechanizmów

| Mechanizm | Kiedy użyć | Elastyczność |
|---|---|---|
| `interrupt()` + `Command(resume=...)` | Produkcyjna logika HITL | Wysoka — dynamiczne, warunkowe |
| `interrupt_before` / `interrupt_after` | Debugowanie, proste breakpointy | Niska — stałe punkty |
| `NodeInterrupt` (legacy) | **Nie używaj** — usunięte | — |
| `HumanInTheLoop` middleware | **Nie istnieje** w LangGraph | — |

---

## Kompleksowy przykład: System zatwierdzania wydatków firmowych

Wieloetapowy graf z przerwaniami na różnych poziomach — klasyfikacja, zatwierdzanie, eskalacja, powiadomienie:

```python
"""
System zatwierdzania wydatków firmowych.

Przepływ:
  START → classify → [próg kwotowy] → approve / escalate → notify → END
                                    → auto_approve → notify → END

Przerwania:
  1. classify    → interrupt z prośbą o potwierdzenie kategorii
  2. approve     → interrupt z prośbą o zatwierdzenie wydatku (≤5000 PLN)
  3. escalate    → interrupt z prośbą o zatwierdzenie przez dyrektora (>5000 PLN)
"""
from typing import Literal, Optional, TypedDict

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command, interrupt


class ExpenseState(TypedDict):
    description: str
    amount: float
    category: Optional[str]
    category_confirmed: Optional[bool]
    approval_status: Optional[Literal["approved", "rejected", "auto"]]
    approver: Optional[str]
    approver_note: Optional[str]
    notification: Optional[str]


# ── Węzły ──────────────────────────────────────────────


def classify_node(state: ExpenseState):
    """Klasyfikuje wydatek i pyta użytkownika o potwierdzenie kategorii."""
    # Prosta heurystyka (w produkcji: LLM)
    desc = state["description"].lower()
    if "hotel" in desc or "lot" in desc or "bilet" in desc:
        suggested = "podróże"
    elif "obiad" in desc or "kawa" in desc or "catering" in desc:
        suggested = "reprezentacja"
    elif "licencja" in desc or "subskrypcja" in desc or "saas" in desc:
        suggested = "oprogramowanie"
    else:
        suggested = "inne"

    # PRZERWANIE 1: potwierdzenie kategorii
    user_response = interrupt({
        "type": "confirm_category",
        "suggested_category": suggested,
        "description": state["description"],
        "amount": state["amount"],
        "instruction": (
            "Potwierdź kategorię (True) lub podaj poprawną "
            "jako string: 'podróże'|'reprezentacja'|'oprogramowanie'|'inne'"
        ),
    })

    if user_response is True:
        return {"category": suggested, "category_confirmed": True}
    else:
        return {"category": user_response, "category_confirmed": True}


def route_by_amount(state: ExpenseState) -> str:
    """Routing na podstawie kwoty."""
    if state["amount"] <= 500:
        return "auto_approve"
    elif state["amount"] <= 5000:
        return "approve"
    else:
        return "escalate"


def auto_approve_node(state: ExpenseState):
    """Automatyczne zatwierdzenie wydatków ≤500 PLN."""
    return {
        "approval_status": "auto",
        "approver": "system",
        "approver_note": "Auto-approved (≤500 PLN)",
    }


def approve_node(state: ExpenseState):
    """Manager zatwierdza wydatek 500-5000 PLN."""
    # PRZERWANIE 2: zatwierdzenie przez managera
    decision = interrupt({
        "type": "manager_approval",
        "description": state["description"],
        "amount": state["amount"],
        "category": state["category"],
        "instruction": (
            "Odpowiedz słownikiem: "
            "{'approved': True/False, 'note': 'opcjonalna uwaga'}"
        ),
    })

    if decision.get("approved"):
        return {
            "approval_status": "approved",
            "approver": "manager",
            "approver_note": decision.get("note", ""),
        }
    return {
        "approval_status": "rejected",
        "approver": "manager",
        "approver_note": decision.get("note", "Odrzucono"),
    }


def escalate_node(state: ExpenseState):
    """Dyrektor zatwierdza wydatek >5000 PLN."""
    # PRZERWANIE 3: eskalacja do dyrektora
    decision = interrupt({
        "type": "director_approval",
        "description": state["description"],
        "amount": state["amount"],
        "category": state["category"],
        "warning": f"Wydatek przekracza 5000 PLN ({state['amount']} PLN)",
        "instruction": (
            "Odpowiedz słownikiem: "
            "{'approved': True/False, 'note': 'uzasadnienie'}"
        ),
    })

    if decision.get("approved"):
        return {
            "approval_status": "approved",
            "approver": "director",
            "approver_note": decision.get("note", ""),
        }
    return {
        "approval_status": "rejected",
        "approver": "director",
        "approver_note": decision.get("note", "Odrzucono przez dyrektora"),
    }


def notify_node(state: ExpenseState):
    """Generuje powiadomienie o wyniku."""
    status = state["approval_status"]
    if status == "auto":
        msg = f"✅ Wydatek '{state['description']}' ({state['amount']} PLN) zatwierdzony automatycznie."
    elif status == "approved":
        msg = (
            f"✅ Wydatek '{state['description']}' ({state['amount']} PLN) "
            f"zatwierdzony przez {state['approver']}. "
            f"Uwaga: {state.get('approver_note', '-')}"
        )
    else:
        msg = (
            f"❌ Wydatek '{state['description']}' ({state['amount']} PLN) "
            f"odrzucony przez {state['approver']}. "
            f"Powód: {state.get('approver_note', '-')}"
        )
    return {"notification": msg}


# ── Budowa grafu ───────────────────────────────────────


builder = StateGraph(ExpenseState)
builder.add_node("classify", classify_node)
builder.add_node("auto_approve", auto_approve_node)
builder.add_node("approve", approve_node)
builder.add_node("escalate", escalate_node)
builder.add_node("notify", notify_node)

builder.add_edge(START, "classify")
builder.add_conditional_edges("classify", route_by_amount)
builder.add_edge("auto_approve", "notify")
builder.add_edge("approve", "notify")
builder.add_edge("escalate", "notify")
builder.add_edge("notify", END)

graph = builder.compile(checkpointer=MemorySaver())
```

### Diagram przepływu

```
START → classify ──(interrupt: potwierdź kategorię)──→ route_by_amount
                                                       │
                                          ≤500 PLN ────→ auto_approve → notify → END
                                          ≤5000 PLN ───→ approve ──(interrupt)──→ notify → END
                                          >5000 PLN ───→ escalate ──(interrupt)──→ notify → END
```

### Uruchomienie krok po kroku

```python
config = {"configurable": {"thread_id": "expense-001"}}

# ── KROK 1: Uruchom graf ──
result = graph.invoke(
    {
        "description": "Hotel na konferencji PyCon",
        "amount": 3200.0,
    },
    config=config,
)

# Graf zatrzymał się na classify_node → interrupt
print(result["__interrupt__"][0].value)
# -> {
#   "type": "confirm_category",
#   "suggested_category": "podróże",
#   "description": "Hotel na konferencji PyCon",
#   "amount": 3200.0,
#   "instruction": "Potwierdź kategorię (True) lub podaj poprawną..."
# }

# ── KROK 2: Potwierdź kategorię ──
result = graph.invoke(Command(resume=True), config=config)

# Kwota 3200 → route do approve_node → kolejny interrupt
print(result["__interrupt__"][0].value)
# -> {
#   "type": "manager_approval",
#   "description": "Hotel na konferencji PyCon",
#   "amount": 3200.0,
#   "category": "podróże",
#   "instruction": "Odpowiedz słownikiem..."
# }

# ── KROK 3: Manager zatwierdza ──
final = graph.invoke(
    Command(resume={"approved": True, "note": "OK, konferencja branżowa"}),
    config=config,
)

print(final["notification"])
# -> "✅ Wydatek 'Hotel na konferencji PyCon' (3200.0 PLN)
#     zatwierdzony przez manager. Uwaga: OK, konferencja branżowa"
print(final["approval_status"])  # -> "approved"
```

### Scenariusz z odrzuceniem (>5000 PLN)

```python
config2 = {"configurable": {"thread_id": "expense-002"}}

result = graph.invoke(
    {"description": "Licencja SaaS roczna", "amount": 12000.0},
    config=config2,
)
# interrupt: confirm_category → suggested "oprogramowanie"

result = graph.invoke(Command(resume=True), config=config2)
# interrupt: director_approval (>5000 PLN → escalate)

final = graph.invoke(
    Command(resume={"approved": False, "note": "Budżet na Q2 wyczerpany"}),
    config=config2,
)
print(final["notification"])
# -> "❌ Wydatek 'Licencja SaaS roczna' (12000.0 PLN)
#     odrzucony przez director. Powód: Budżet na Q2 wyczerpany"
```

### Inspekcja stanu między przerwaniami

```python
config3 = {"configurable": {"thread_id": "expense-003"}}

graph.invoke(
    {"description": "Kawa dla zespołu", "amount": 120.0},
    config=config3,
)

# Sprawdź stan wątku
snapshot = graph.get_state(config3)
print(snapshot.tasks[0].interrupts[0].value["suggested_category"])
# -> "reprezentacja"

# Popraw kategorię na inną
result = graph.invoke(Command(resume="inne"), config=config3)
# amount ≤500 → auto_approve → notify → END
print(result["category"])        # -> "inne"
print(result["approval_status"]) # -> "auto"
```

---

## Podsumowanie

```
┌──────────────────────────────────────────────────────┐
│                    INTERRUPTS                        │
│                                                      │
│  interrupt(payload)   →  wstrzymaj węzeł             │
│  Checkpointer         →  zapisz stan                 │
│  __interrupt__ / .interrupts → payload do callera    │
│  Command(resume=v)    →  wznów z wartością           │
│  Command(resume=map)  →  wznów wiele naraz (id→v)   │
│                                                      │
│  Wykrywanie:                                         │
│  • invoke v2 → result.interrupts                     │
│  • invoke v1 → result["__interrupt__"]               │
│  • stream   → chunk["data"]["__interrupt__"]         │
│  • get_state → snapshot.tasks[0].interrupts          │
│                                                      │
│  Zasady:                                             │
│  • Checkpointer WYMAGANY                             │
│  • thread_id identyfikuje sesję                      │
│  • Kod przed interrupt() musi być idempotentny       │
│  • Nie owijaj interrupt() w try/except               │
│  • Nie zmieniaj kolejności wywołań interrupt()        │
│  • Payload musi być JSON-serializowalny              │
│  • HumanInTheLoop middleware NIE ISTNIEJE            │
└──────────────────────────────────────────────────────┘
```

---

## Powiązane pliki

- [Human-in-the-Loop — Interrupt (scenariusze)](human-in-the-loop-interrupt-langgraph.md)
- [Pamięć i Persistence — Checkpointers](pamiec-i-persistence-checkpointers-langgraph.md)
- [Persistence: SQLite i PostgreSQL](persistence-sqlite-postgres-langgraph.md)
- [Streaming w LangGraph](streaming-langgraph.md)
- [Narzędzia dla agentów (Tool Use)](narzedzia-dla-agentow-tool-use-langgraph.md)
- [Równoległe węzły (Fan-out / Fan-in)](rownolegle-wezly-fan-out-fan-in-langgraph.md)
