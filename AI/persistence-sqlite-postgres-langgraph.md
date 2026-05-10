# Persistence z SQLite / PostgreSQL w LangGraph

## Czym jest trwała persystencja

`InMemorySaver` (dawniej `MemorySaver`) przechowuje checkpointy w RAM — dane giną po restarcie procesu. Trwałe checkpointery (`SqliteSaver`, `PostgresSaver`) zapisują stan grafu do bazy danych, dzięki czemu:

- konwersacja przetrwa restart aplikacji
- możliwy jest dostęp do historii z wielu instancji serwera
- Human-in-the-Loop i Time Travel działają między sesjami

## Kiedy który backend

| Backend | Pakiet | Zastosowanie |
|---|---|---|
| `InMemorySaver` | `langgraph-checkpoint` (wbudowany) | Testy, prototypy |
| `SqliteSaver` / `AsyncSqliteSaver` | `langgraph-checkpoint-sqlite` | Lokalne narzędzia CLI, jednowęzłowe aplikacje |
| `PostgresSaver` / `AsyncPostgresSaver` | `langgraph-checkpoint-postgres` | Produkcja, wieloinstancyjne API, wieloużytkownikowe systemy |

## Instalacja

```bash
# SQLite
pip install langgraph-checkpoint-sqlite

# PostgreSQL
pip install langgraph-checkpoint-postgres
```

Pakiet `langgraph-checkpoint-postgres` wymaga drivera `psycopg` (psycopg3):

```bash
pip install "psycopg[binary,pool]"
```

---

## SqliteSaver — persystencja lokalna

### Synchroniczny

```python
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from typing import Annotated, TypedDict

class State(TypedDict):
    messages: Annotated[list, add_messages]

llm = ChatOpenAI(model="gpt-4o")

def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}

builder = StateGraph(State)
builder.add_node("chatbot", chatbot)
builder.add_edge(START, "chatbot")
builder.add_edge("chatbot", END)

# Context manager gwarantuje poprawne zamknięcie połączenia
with SqliteSaver.from_conn_string("chat.db") as checkpointer:
    checkpointer.setup()  # tworzy tabele przy pierwszym uruchomieniu
    graph = builder.compile(checkpointer=checkpointer)

    config = {"configurable": {"thread_id": "user-session-1"}}

    # Tura 1
    result = graph.invoke(
        {"messages": [("human", "Cześć, jestem Kamil.")]},
        config=config,
    )
    print(result["messages"][-1].content)

    # Tura 2 — agent pamięta imię z tury 1
    result = graph.invoke(
        {"messages": [("human", "Jak mam na imię?")]},
        config=config,
    )
    print(result["messages"][-1].content)
```

### Asynchroniczny

```python
import asyncio
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

async def main():
    async with AsyncSqliteSaver.from_conn_string("chat.db") as checkpointer:
        await checkpointer.setup()
        graph = builder.compile(checkpointer=checkpointer)

        config = {"configurable": {"thread_id": "async-session-1"}}
        result = await graph.ainvoke(
            {"messages": [("human", "Hello")]},
            config=config,
        )
        print(result["messages"][-1].content)

asyncio.run(main())
```

### Ograniczenia SQLite

- Brak wsparcia dla współbieżnych zapisów (jeden writer naraz)
- Nieodpowiedni dla wieloinstancyjnych deploymentów
- Brak natywnej replikacji

---

## PostgresSaver — persystencja produkcyjna

### Synchroniczny z connection pool

```python
from langgraph.checkpoint.postgres import PostgresSaver
from psycopg_pool import ConnectionPool

DB_URI = "postgresql://user:pass@localhost:5432/langgraph_db"

pool = ConnectionPool(conninfo=DB_URI, max_size=20)

with pool.connection() as conn:
    checkpointer = PostgresSaver(conn)
    checkpointer.setup()  # tworzy tabele: checkpoints, checkpoint_blobs, checkpoint_writes

graph = builder.compile(checkpointer=PostgresSaver(pool))

config = {"configurable": {"thread_id": "prod-session-42"}}
result = graph.invoke(
    {"messages": [("human", "Raport sprzedaży za Q1")]},
    config=config,
)
```

### Asynchroniczny (FastAPI / aiohttp)

```python
import asyncio
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from psycopg_pool import AsyncConnectionPool
from psycopg.rows import dict_row

DB_URI = "postgresql://user:pass@localhost:5432/langgraph_db"

async def main():
    async with AsyncConnectionPool(
        conninfo=DB_URI,
        max_size=20,
        kwargs={"autocommit": True, "row_factory": dict_row},
    ) as pool:
        checkpointer = AsyncPostgresSaver(pool)
        await checkpointer.setup()

        graph = builder.compile(checkpointer=checkpointer)

        config = {"configurable": {"thread_id": "async-prod-1"}}
        result = await graph.ainvoke(
            {"messages": [("human", "Podsumuj ostatni sprint")]},
            config=config,
        )
        print(result["messages"][-1].content)

asyncio.run(main())
```

### Kluczowe wymagania dla PostgresSaver

| Parametr | Wartość | Dlaczego |
|---|---|---|
| `autocommit` | `True` | Checkpointer zarządza transakcjami samodzielnie |
| `row_factory` | `dict_row` | Dostęp do kolumn po nazwie |
| `setup()` | Wywoływany raz | Tworzy tabele migracyjne |

---

## Wczytywanie historii po restarcie aplikacji

Kluczowa zaleta trwałych checkpointerów — po restarcie procesu wystarczy ponownie skompilować graf z tym samym backendem i podać ten sam `thread_id`:

```python
# === Po restarcie aplikacji ===
from langgraph.checkpoint.sqlite import SqliteSaver

# Ten sam plik bazy
with SqliteSaver.from_conn_string("chat.db") as checkpointer:
    checkpointer.setup()
    graph = builder.compile(checkpointer=checkpointer)

    # Ten sam thread_id — pełna historia jest dostępna
    config = {"configurable": {"thread_id": "user-session-1"}}

    # Inspekcja zapisanego stanu
    snapshot = graph.get_state(config)
    print(f"Wiadomości w wątku: {len(snapshot.values['messages'])}")
    print(f"Następny węzeł: {snapshot.next}")

    # Kontynuacja konwersacji
    result = graph.invoke(
        {"messages": [("human", "Kontynuujmy naszą rozmowę.")]},
        config=config,
    )
```

### Przeglądanie historii checkpointów

```python
config = {"configurable": {"thread_id": "user-session-1"}}

# Wszystkie checkpointy wątku (od najnowszego)
for snapshot in graph.get_state_history(config):
    print(f"Step {snapshot.metadata['step']}: "
          f"next={snapshot.next}, "
          f"source={snapshot.metadata['source']}")
```

### Wyszukiwanie konkretnego checkpointu

```python
history = list(graph.get_state_history(config))

# Checkpoint sprzed wykonania konkretnego węzła
before_tool = next(s for s in history if s.next == ("tool_node",))

# Checkpoint po kroku nr 3
step_3 = next(s for s in history if s.metadata["step"] == 3)

# Replay od wybranego checkpointu
replay_config = before_tool.config
result = graph.invoke(None, replay_config)
```

---

## Szyfrowanie checkpointów

Na produkcji checkpointy mogą zawierać dane wrażliwe. LangGraph dostarcza `EncryptedSerializer`:

```python
from langgraph.checkpoint.serde.encrypted import EncryptedSerializer
from langgraph.checkpoint.postgres import PostgresSaver

# Klucz AES odczytywany ze zmiennej środowiskowej LANGGRAPH_AES_KEY
serde = EncryptedSerializer.from_pycryptodome_aes()

checkpointer = PostgresSaver.from_conn_string(
    "postgresql://user:pass@localhost:5432/db",
    serde=serde,
)
checkpointer.setup()
```

Wymaga pakietu `pycryptodome` i ustawienia zmiennej:

```bash
export LANGGRAPH_AES_KEY="32-bajtowy-klucz-base64"
```

---

## Bezpieczeństwo deserializacji

Domyślny `JsonPlusSerializer` może deserializować dowolne obiekty Pythona. Na produkcji:

```bash
export LANGGRAPH_STRICT_MSGPACK=true
```

To ogranicza deserializację wyłącznie do znanych bezpiecznych typów, eliminując ryzyko zdalnego wykonania kodu w razie kompromitacji bazy.

---

## Zarządzanie rozmiarem bazy

Checkpointy rosną z każdym super-stepem. Strategie kontroli:

1. **Przycinanie wiadomości** — `trim_messages` w stanie grafu ogranicza liczbę wiadomości wysyłanych do LLM (nie kasuje checkpointów, ale redukuje rozmiar nowych)
2. **Czyszczenie starych wątków** — cron/job usuwający checkpointy starsze niż X dni
3. **Nie przechowuj blobów w stanie** — duże pliki trzymaj w S3/GCS, w stanie tylko URL/referencja

---

## Kompletny przykład: FastAPI + AsyncPostgresSaver

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from psycopg_pool import AsyncConnectionPool
from psycopg.rows import dict_row
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from typing import Annotated, TypedDict

DB_URI = "postgresql://user:pass@localhost:5432/langgraph_db"

class State(TypedDict):
    messages: Annotated[list, add_messages]

llm = ChatOpenAI(model="gpt-4o")

def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}

builder = StateGraph(State)
builder.add_node("chatbot", chatbot)
builder.add_edge(START, "chatbot")
builder.add_edge("chatbot", END)

# Globalne zmienne
pool = None
graph = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global pool, graph
    pool = AsyncConnectionPool(
        conninfo=DB_URI,
        max_size=20,
        kwargs={"autocommit": True, "row_factory": dict_row},
    )
    await pool.open()

    checkpointer = AsyncPostgresSaver(pool)
    await checkpointer.setup()
    graph = builder.compile(checkpointer=checkpointer)

    yield

    await pool.close()

app = FastAPI(lifespan=lifespan)

@app.post("/chat/{thread_id}")
async def chat(thread_id: str, message: str):
    config = {"configurable": {"thread_id": thread_id}}
    result = await graph.ainvoke(
        {"messages": [("human", message)]},
        config=config,
    )
    return {"response": result["messages"][-1].content}

@app.get("/history/{thread_id}")
async def history(thread_id: str):
    config = {"configurable": {"thread_id": thread_id}}
    snapshot = await graph.aget_state(config)
    return {
        "message_count": len(snapshot.values.get("messages", [])),
        "next_node": snapshot.next,
    }
```

---

## Powiązane pliki

- [Checkpointers w LangGraph — teoria](checkpointers-langgraph.md)
- [Pamięć i Persistence — MemorySaver w praktyce](pamiec-i-persistence-checkpointers-langgraph.md)
- [Human-in-the-Loop i interrupt w LangGraph](human-in-the-loop-interrupt-langgraph.md)
- [Streaming w LangGraph](streaming-langgraph.md)
