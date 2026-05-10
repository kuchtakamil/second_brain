# Streaming w LangGraph

## Czym jest streaming w LangGraph

Streaming pozwala odbierać dane z grafu **w trakcie wykonania** — zamiast czekać na finalny wynik z `invoke()`. Dotyczy to zarówno pośrednich stanów grafu, jak i pojedynczych tokenów generowanych przez LLM.

W LangGraph ≥ 1.0 metoda `graph.stream()` (sync) lub `graph.astream()` (async) przyjmuje parametr `stream_mode`, który definiuje **co** jest streamowane. Zalecane jest używanie formatu wyjściowego `version="v2"`, który zwraca ustandaryzowane obiekty `StreamPart`.

---

## Dlaczego streaming, a nie invoke

- **Responsywność UI** — użytkownik widzi tekst pojawiający się token po tokenie, zamiast pustego ekranu.
- **Monitoring postępu** — widoczność, który węzeł aktualnie pracuje.
- **Debugowanie** — podgląd zmian stanu po każdym kroku.
- **Redukcja perceived latency** — wynik „pojawia się" szybciej, mimo że pełne przetwarzanie trwa tyle samo.

---

## Format wyjściowy v2

Używaj `version="v2"` w wywołaniu `stream()` / `astream()`. Każdy chunk to `StreamPart` z ustandaryzowaną strukturą:

```python
{
    "type": "values" | "updates" | "messages" | "custom" | "checkpoints" | "tasks" | "debug",
    "ns": (),        # namespace — tuple, niepusty dla zdarzeń z subgrafów
    "data": ...,     # payload — format zależy od stream_mode
}
```

Bez `version="v2"` output ma starszy format (tuple), który jest mniej czytelny i trudniejszy do rozszerzania.

---

## Tryby streamowania (stream_mode)

| Tryb | Co emituje | Kiedy używać |
|---|---|---|
| `"updates"` | Tylko zmienione klucze stanu po każdym węźle | Dashboard, progress tracker |
| `"values"` | Pełny snapshot stanu po każdym węźle | Pełny podgląd stanu, UI odtwarzające cały stan |
| `"messages"` | Tokeny LLM jako `(message_chunk, metadata)` | Efekt "pisania" w chatbocie |
| `"custom"` | Dane emitowane przez `get_stream_writer()` | Progress bary, statusy, logi |
| `"debug"` | Pełny trace wykonania grafu | Debugging, diagnostyka |
| `"checkpoints"` | Checkpointy (jak `get_state()`) po każdym kroku | Inspekcja persisted state |
| `"tasks"` | Start/koniec tasków (węzłów) z wynikami | Monitoring tasków |

---

## stream_mode="updates" — tylko zmiany stanu

Emituje **delta stanu** — wyłącznie klucze zmienione przez dany węzeł.

```python
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    topic: str
    joke: str

def refine_topic(state: State):
    return {"topic": state["topic"] + " and cats"}

def generate_joke(state: State):
    return {"joke": f"This is a joke about {state['topic']}"}

graph = (
    StateGraph(State)
    .add_node(refine_topic)
    .add_node(generate_joke)
    .add_edge(START, "refine_topic")
    .add_edge("refine_topic", "generate_joke")
    .add_edge("generate_joke", END)
    .compile()
)

for chunk in graph.stream(
    {"topic": "ice cream"},
    stream_mode="updates",
    version="v2",
):
    if chunk["type"] == "updates":
        for node_name, state in chunk["data"].items():
            print(f"Node `{node_name}` updated: {state}")
```

**Output:**
```
Node `refine_topic` updated: {'topic': 'ice cream and cats'}
Node `generate_joke` updated: {'joke': 'This is a joke about ice cream and cats'}
```

Każdy chunk zawiera `{nazwa_węzła: {zmienione_klucze}}`. Węzeł `refine_topic` zmienił tylko `topic`, więc `joke` nie pojawia się w jego updacie.

---

## stream_mode="values" — pełny stan po każdym węźle

Emituje **kompletny snapshot stanu** po każdym węźle, włącznie z kluczami, które się nie zmieniły.

```python
for chunk in graph.stream(
    {"topic": "ice cream"},
    stream_mode="values",
    version="v2",
):
    if chunk["type"] == "values":
        print(f"topic: {chunk['data']['topic']}, joke: {chunk['data'].get('joke', '')}")
```

**Output:**
```
topic: ice cream, joke:
topic: ice cream and cats, joke:
topic: ice cream and cats, joke: This is a joke about ice cream and cats
```

Pierwszy emit to stan wejściowy (po `START`), kolejne to stan po każdym węźle. Widać pełny stan — również puste klucze.

### Kiedy `updates` vs `values`

| Scenariusz | Tryb |
|---|---|
| UI odtwarzające pełny stan (np. formularz) | `values` |
| Dashboard pokazujący ostatnią zmianę | `updates` |
| Oszczędność transferu (duży stan) | `updates` |
| Debugowanie — chcesz widzieć cały kontekst | `values` |

---

## stream_mode="messages" — tokeny LLM na żywo

Streamuje tokeny generowane przez LLM w trakcie wywołania. Każdy chunk to tuple `(message_chunk, metadata)`.

```python
from dataclasses import dataclass
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START

@dataclass
class MyState:
    topic: str
    joke: str = ""

model = init_chat_model(model="gpt-4o-mini")

def call_model(state: MyState):
    # Tokeny emitowane nawet przy .invoke() — nie wymaga .stream() na modelu
    response = model.invoke(
        [{"role": "user", "content": f"Generate a joke about {state.topic}"}]
    )
    return {"joke": response.content}

graph = (
    StateGraph(MyState)
    .add_node(call_model)
    .add_edge(START, "call_model")
    .compile()
)

for chunk in graph.stream(
    {"topic": "ice cream"},
    stream_mode="messages",
    version="v2",
):
    if chunk["type"] == "messages":
        message_chunk, metadata = chunk["data"]
        if message_chunk.content:
            print(message_chunk.content, end="|", flush=True)
```

LangGraph automatycznie przechwytuje tokeny z LLM — nawet jeśli wewnątrz węzła użyto `model.invoke()` zamiast `model.stream()`.

### Filtrowanie po węźle

Metadata zawiera pole `langgraph_node` — nazwa węzła, z którego pochodzi token:

```python
for chunk in graph.stream(inputs, stream_mode="messages", version="v2"):
    if chunk["type"] == "messages":
        msg, metadata = chunk["data"]
        if msg.content and metadata["langgraph_node"] == "write_poem":
            print(msg.content, end="", flush=True)
```

### Filtrowanie po tagu LLM

Tagowanie modeli pozwala rozróżnić tokeny z różnych wywołań LLM w tym samym węźle:

```python
from langchain.chat_models import init_chat_model

joke_model = init_chat_model(model="gpt-4o-mini", tags=["joke"])
poem_model = init_chat_model(model="gpt-4o-mini", tags=["poem"])

# Przy streamowaniu:
for chunk in graph.stream(inputs, stream_mode="messages", version="v2"):
    if chunk["type"] == "messages":
        msg, metadata = chunk["data"]
        if metadata["tags"] == ["joke"]:
            print(msg.content, end="", flush=True)
```

### Wyłączanie streamowania tokenów (nostream)

Tag `"nostream"` na modelu wyklucza jego tokeny ze streama `messages`. Przydatne gdy LLM służy do wewnętrznej logiki (np. structured output), a nie do wyświetlania:

```python
internal_model = ChatAnthropic(model_name="claude-haiku-4-5-20251001").with_config(
    {"tags": ["nostream"]}
)
# Tokeny z internal_model NIE pojawią się w stream_mode="messages"
```

---

## stream_mode="custom" — własne zdarzenia

Pozwala emitować dowolne dane z wnętrza węzła lub narzędzia za pomocą `get_stream_writer()`.

### Użycie w węźle (sync, Python ≥ 3.11)

```python
from typing import TypedDict
from langgraph.config import get_stream_writer
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    query: str
    answer: str

def node(state: State):
    writer = get_stream_writer()
    writer({"status": "processing", "progress": 50})
    # ... logika ...
    writer({"status": "done", "progress": 100})
    return {"answer": "result"}

graph = (
    StateGraph(State)
    .add_node(node)
    .add_edge(START, "node")
    .add_edge("node", END)
    .compile()
)

for chunk in graph.stream({"query": "test"}, stream_mode="custom", version="v2"):
    if chunk["type"] == "custom":
        print(f"{chunk['data']['status']}: {chunk['data']['progress']}%")
```

### Użycie w narzędziu (@tool)

```python
from langchain.tools import tool
from langgraph.config import get_stream_writer

@tool
def query_database(query: str) -> str:
    """Query the database."""
    writer = get_stream_writer()
    writer({"data": "Retrieved 0/100 records", "type": "progress"})
    # ... wykonanie zapytania ...
    writer({"data": "Retrieved 100/100 records", "type": "progress"})
    return "result"
```

### Async — Python < 3.11

W Pythonie < 3.11 `get_stream_writer()` **nie działa** w async nodach/toolach. Zamiast tego użyj parametru `writer: StreamWriter` w sygnaturze funkcji — LangGraph wstrzyknie go automatycznie:

```python
from langgraph.types import StreamWriter

async def generate_joke(state: State, writer: StreamWriter):
    writer({"custom_key": "Generating..."})
    return {"joke": f"Joke about {state['topic']}"}
```

---

## Łączenie wielu trybów

Przekazanie listy trybów do `stream_mode` pozwala odbierać różne typy zdarzeń w jednym strumieniu. Typ rozróżniasz po `chunk["type"]`:

```python
for part in graph.stream(
    {"topic": "ice cream"},
    stream_mode=["values", "updates", "messages", "custom"],
    version="v2",
):
    if part["type"] == "values":
        print(f"State: {part['data']}")

    elif part["type"] == "updates":
        for node_name, state in part["data"].items():
            print(f"Node `{node_name}` updated: {state}")

    elif part["type"] == "messages":
        msg, metadata = part["data"]
        print(msg.content, end="", flush=True)

    elif part["type"] == "custom":
        print(f"Progress: {part['data']}")
```

---

## Streamowanie z subgrafów

Jeśli graf zawiera subgrafy, ustaw `subgraphs=True` aby otrzymać zdarzenia z zagnieżdżonych grafów. Pole `ns` w `StreamPart` identyfikuje źródło:

```python
for chunk in graph.stream(
    {"foo": "bar"},
    subgraphs=True,
    stream_mode="updates",
    version="v2",
):
    if chunk["type"] == "updates":
        if chunk["ns"]:
            print(f"Subgraph {chunk['ns']}: {chunk['data']}")
        else:
            print(f"Root: {chunk['data']}")
```

Format `ns`: pusta krotka `()` dla roota, `("node_name:<task_id>",)` dla subgrafów.

---

## Async streaming (astream)

Asynchroniczny odpowiednik `stream()`:

```python
async for chunk in graph.astream(
    {"topic": "ice cream"},
    stream_mode="messages",
    version="v2",
):
    if chunk["type"] == "messages":
        message_chunk, metadata = chunk["data"]
        if message_chunk.content:
            print(message_chunk.content, end="", flush=True)
```

### Python < 3.11 — wymagania

W Pythonie < 3.11 kontekst nie propaguje się automatycznie do async tasków. Wymagane jest:

1. **Jawne przekazywanie `config`** do `ainvoke()` / `astream()` na modelu:
   ```python
   async def call_model(state, config):
       response = await model.ainvoke(messages, config)  # config jawnie
       return {"result": response.content}
   ```

2. **Użycie `writer: StreamWriter` zamiast `get_stream_writer()`** w sygnaturze async nodów.

---

## Wyłączanie streamowania dla modelu

Niektóre modele nie wspierają streamowania (np. `o1-preview`). Wyłączenie:

```python
from langchain.chat_models import init_chat_model

model = init_chat_model("claude-sonnet-4-6", streaming=False)
```

Lub bezpośrednio na klasie modelu:

```python
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="o1-preview", streaming=False)
```

---

## Streamowanie dowolnego LLM (bez LangChain)

Jeśli LLM nie jest opakowany w LangChain, tryb `messages` nie zadziała. Użyj `stream_mode="custom"` z `get_stream_writer()`:

```python
from langgraph.config import get_stream_writer
from openai import OpenAI

client = OpenAI()

def call_arbitrary_model(state):
    writer = get_stream_writer()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": state["query"]}],
        stream=True,
    )
    full_response = ""
    for chunk in response:
        token = chunk.choices[0].delta.content or ""
        full_response += token
        writer({"token": token})
    return {"answer": full_response}

# Konsumpcja:
for chunk in graph.stream(inputs, stream_mode="custom", version="v2"):
    if chunk["type"] == "custom":
        print(chunk["data"]["token"], end="", flush=True)
```

---

## Powiązane pliki

- [Pamięć i Persistence — Checkpointers](pamiec-i-persistence-checkpointers-langgraph.md)
- [Narzędzia dla agentów (Tool Use)](narzedzia-dla-agentow-tool-use-langgraph.md)
- [Human-in-the-Loop — Interrupt](human-in-the-loop-interrupt-langgraph.md)
- [Równoległe węzły (Fan-out / Fan-in)](rownolegle-wezly-fan-out-fan-in-langgraph.md)
- [Multi-Agent z Supervisorem](multi-agent-supervisor-langgraph.md)
