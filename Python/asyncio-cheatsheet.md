# Asyncio Cheatsheet

Zwięzły cheatsheet obejmujący najważniejsze elementy `asyncio` w Pythonie. Patrząc na tę stronę powinieneś być w stanie rozwiązać większość typowych zadań asynchronicznych.

---

## 1. Uruchamianie event loopa

```python
import asyncio

async def main():
    print("start")

asyncio.run(main())  # jedyny punkt wejścia z sync → async
```

## 2. Definiowanie i wywoływanie coroutine

```python
async def fetch(url: str) -> str:
    await asyncio.sleep(1)      # symulacja I/O
    return f"data from {url}"

result = await fetch("https://example.com")
```

## 3. Równoległe uruchamianie zadań

| Funkcja | Zachowanie | Zwraca |
|:---|:---|:---|
| `asyncio.gather(*coros)` | Czeka na **wszystkie**; domyślnie pierwszy wyjątek przerywa | lista wyników (w kolejności) |
| `asyncio.TaskGroup()` | Jak gather, ale **structured concurrency** (Python 3.11+) | wyniki przez zmienne |
| `asyncio.wait(tasks, ...)` | Elastyczne czekanie (`FIRST_COMPLETED` / `ALL_COMPLETED`) | `(done, pending)` — zbiory tasków |

```python
# gather — najprostsze
results = await asyncio.gather(fetch("a"), fetch("b"), fetch("c"))

# TaskGroup — bezpieczniejsze (3.11+)
async with asyncio.TaskGroup() as tg:
    t1 = tg.create_task(fetch("a"))
    t2 = tg.create_task(fetch("b"))
print(t1.result(), t2.result())

# wait — np. pierwszy wynik
done, pending = await asyncio.wait(
    [asyncio.create_task(fetch(u)) for u in urls],
    return_when=asyncio.FIRST_COMPLETED
)
```

## 4. Tworzenie i zarządzanie taskami

```python
task = asyncio.create_task(fetch("x"))   # uruchamia w tle
result = await task                       # czeka na wynik
task.cancel()                             # żądanie anulowania
```

## 5. Timeouty

```python
# timeout na pojedynczą operację
try:
    result = await asyncio.wait_for(fetch("slow"), timeout=3.0)
except asyncio.TimeoutError:
    print("za wolno!")

# timeout jako context manager (3.11+)
async with asyncio.timeout(3.0):
    result = await fetch("slow")
```

## 6. Kolejki (producent–konsument)

```python
queue: asyncio.Queue[str] = asyncio.Queue(maxsize=10)

async def producer():
    await queue.put("item")

async def consumer():
    item = await queue.get()
    queue.task_done()          # sygnał zakończenia

await queue.join()             # czeka aż wszystko przetworzone
```

## 7. Synchronizacja

```python
lock = asyncio.Lock()
async with lock:
    # sekcja krytyczna — tylko 1 coroutine naraz

sem = asyncio.Semaphore(5)
async with sem:
    # max 5 coroutine jednocześnie (np. rate limiting)

event = asyncio.Event()
event.set()                    # odblokuj czekających
await event.wait()             # czekaj na set()
```

## 8. Iterowanie asynchroniczne

```python
# async generator
async def stream():
    for i in range(5):
        await asyncio.sleep(0.1)
        yield i

async for item in stream():
    print(item)

# async comprehension
data = [item async for item in stream()]
```

## 9. Async context manager

```python
class AsyncDB:
    async def __aenter__(self):
        self.conn = await connect()
        return self.conn
    async def __aexit__(self, *exc):
        await self.conn.close()

async with AsyncDB() as conn:
    await conn.execute("SELECT 1")
```

## 10. Integracja sync ↔ async

```python
import functools

# Uruchomienie blokującego kodu w wątku (nie blokuje event loop!)
loop = asyncio.get_running_loop()
result = await loop.run_in_executor(None, blocking_function, arg1)

# Z functools.partial dla wielu argumentów
result = await loop.run_in_executor(
    None, functools.partial(blocking_fn, key="value")
)
```

## 11. as_completed — wyniki w kolejności zakończenia

```python
for coro in asyncio.as_completed([fetch("a"), fetch("b"), fetch("c")]):
    result = await coro        # pierwszy zakończony → pierwszy wynik
    print(result)
```

## 12. Obsługa wyjątków w gather

```python
results = await asyncio.gather(
    fetch("ok"), fetch("fail"),
    return_exceptions=True     # wyjątki jako wartości zamiast propagacji
)
for r in results:
    if isinstance(r, Exception):
        print(f"Błąd: {r}")
```

---

## Powiązane pliki

*   [Async await w Pythonie](async-await-w-pythonie.md)
*   [Async i await w Pythonie](async-i-await-w-pythonie.md)
*   [Co to jest async i await](co-to-jest-async-i-await.md)
*   [Generatory, yield, coroutine](generatory-yield-coroutine.md)
*   [GIL w Pythonie](gil-w-pythonie.md)
