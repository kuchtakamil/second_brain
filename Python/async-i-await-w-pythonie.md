# Async i await w Pythonie

**Data:** 2025-07-16

---

**User:**

Czy w Python istnieją słowa kluczowe async i await? 
Widziałem słowo async prze definiowaniu endpointów w fastapi. Co to zmienia? Czy to jedyne zastosowanie async?

---

**Assistant:**

Tak, w Pythonie istnieją słowa kluczowe `async` i `await`. Zostały one wprowadzone w Pythonie 3.5 jako część wsparcia dla programowania asynchronicznego (ang. *asynchronous programming*), które pozwala na pisanie kodu współbieżnego w bardziej przejrzysty sposób niż klasyczne podejście oparte na wątkach lub callbackach.

---

### 📌 Co robi `async def`?

Słowo kluczowe `async` przed `def` oznacza, że dana funkcja jest **asynchroniczna** i zwraca obiekt typu `coroutine`, czyli korutynę. Przykład:

```python
async def my_function():
    return 42
```

---

### 📌 Co robi `await`?

Słowo kluczowe `await` można stosować **tylko wewnątrz funkcji oznaczonej jako `async def`**. Służy do „czekania” na wynik innej asynchronicznej operacji bez blokowania głównego wątku.

Przykład:

```python
import asyncio

async def my_coroutine():
    await asyncio.sleep(1)
    return "done"
```

---

### 📌 Dlaczego `async` w FastAPI?

FastAPI używa `async def` do definiowania endpointów, ponieważ potrafi wykorzystać **asynchroniczność** do obsługi wielu zapytań HTTP naraz bez potrzeby tworzenia wielu wątków.

Porównanie:

```python
# synchroniczny endpoint
@app.get("/sync")
def sync_endpoint():
    data = slow_io_call()
    return {"data": data}

# asynchroniczny endpoint
@app.get("/async")
async def async_endpoint():
    data = await async_slow_io_call()
    return {"data": data}
```

Jeśli `async_slow_io_call` to operacja I/O (np. żądanie HTTP, zapytanie do bazy, odczyt pliku), to użycie `await` pozwala serwerowi na obsługę innych zapytań w międzyczasie.

---

### 📌 Czy `async` i `await` tylko w FastAPI?

Nie, to **uniwersalne mechanizmy Pythona**, które mogą być stosowane w:

- **komunikacji sieciowej** (np. `aiohttp`, `websockets`, `httpx`)
- **obsłudze plików lub baz danych** (np. `databases`, `aiomysql`, `motor` dla MongoDB)
- **kolejkach i event loopach** (np. `asyncio.Queue`, `asyncio.Event`)
- **równoległym przetwarzaniu danych** (np. z `asyncio.gather()`)

Przykład pełnego użycia:

```python
import asyncio

async def fetch_data():
    await asyncio.sleep(1)
    return "data"

async def main():
    result = await fetch_data()
    print(result)

asyncio.run(main())
```

---

### 📌 Kiedy nie warto używać `async`?

- Gdy Twój kod **nie zawiera operacji I/O** ani niczego, co mogłoby blokować (np. tylko obliczenia CPU).
- Gdy używasz bibliotek **nieskompatybilnych z async** (np. klasycznych klientów baz danych, jak `psycopg2` zamiast `asyncpg`).

---

Jeśli chcesz, mogę pokazać różnice w wydajności lub napisać prosty przykład z asynchronicznym pobieraniem danych z kilku URL-i.