# Opisz async i await w Python

**Data:** 16 lip 2025, 11:03:57 CET

---

**User:**

Opisz async i await w Python

---

**Gemini:**

Słowa kluczowe `async` i `await` są częścią biblioteki `asyncio` w Pythonie i służą do pisania **asynchronicznego, współbieżnego kodu** w stylu programowania proceduralnego. Umożliwiają one obsługę operacji blokujących (głównie operacji I/O, takich jak zapytania sieciowe czy dostęp do bazy danych) bez blokowania całego wątku wykonania.

---

### `async def` - Definiowanie Korutyny

Słowo kluczowe `async` umieszczone przed `def` tworzy **korutynę** (ang. *coroutine*). Korutyna to specjalny rodzaj funkcji, której wykonanie można wstrzymać i wznowić w późniejszym czasie.

Wywołanie funkcji-korutyny nie wykonuje jej kodu natychmiast. Zamiast tego zwraca **obiekt korutyny**.

```
import asyncio

async def my_coroutine():
    print("Executing coroutine")
    return "Result"

# Calling the function returns a coroutine object, it does not execute the code inside.
coro_obj = my_coroutine()
print(coro_obj)
# Output: <coroutine object my_coroutine at 0x...>
```

Aby uruchomić korutynę, musi ona zostać przekazana do pętli zdarzeń (ang. *event loop*). Najprostszym sposobem jest użycie `asyncio.run()`.

```
# To run the coroutine and get its result:
result = asyncio.run(my_coroutine())
print(result)
# Output:
# Executing coroutine
# Result
```

---

### `await` - Wstrzymywanie Wykonania

Słowo kluczowe `await` może być używane **tylko wewnątrz funkcji `async def`**. Służy ono do wstrzymania wykonania bieżącej korutyny i przekazania kontroli z powrotem do pętli zdarzeń, aż obiekt *awaitable* (oczekiwany) zakończy swoje działanie.

Obiekt *awaitable* to:

1. Inna **korutyna**.
2. Obiekt **Task**, który opakowuje i zarządza wykonaniem korutyny.
3. Obiekt z implementacją metody `__await__()`.

Gdy pętla zdarzeń otrzymuje kontrolę, może uruchomić inne zadania, które są gotowe do wykonania. Kiedy oczekiwana operacja (np. pobranie danych z sieci) się zakończy, pętla zdarzeń wznowi wykonanie wstrzymanej korutyny od miejsca, w którym została zatrzymana.

```
import asyncio
import time

async def fetch_data():
    print("Fetching data...")
    # Simulate a non-blocking I/O operation
    await asyncio.sleep(2) 
    print("Data fetched.")
    return {"data": 123}

async def main():
    start_time = time.time()
    
    # Pause the execution of main() until fetch_data() is complete.
    # While paused, the event loop can run other tasks.
    result = await fetch_data() 
    print(f"Received: {result}")

    end_time = time.time()
    print(f"Total time: {end_time - start_time:.2f} seconds")

asyncio.run(main())
```

W powyższym przykładzie `await asyncio.sleep(2)` symuluje operację I/O. Zamiast blokować cały program na 2 sekundy (jak `time.sleep(2)`), przekazuje kontrolę do pętli zdarzeń, która mogłaby w tym czasie robić coś innego.

---

### Współbieżność z `asyncio.gather` i `asyncio.create_task`

Prawdziwa moc `async`/`await` ujawnia się, gdy uruchamiamy wiele operacji współbieżnie.

- `asyncio.create_task(coro)`: Natychmiast planuje wykonanie korutyny w pętli zdarzeń jako zadanie (`Task`) i zwraca obiekt `Task`. Zadanie zaczyna działać "w tle", gdy tylko pętla zdarzeń odzyska kontrolę.
- `asyncio.gather(*aws)`: Uruchamia wiele obiektów *awaitable* (korutyn lub zadań) współbieżnie. Czeka, aż wszystkie się zakończą i zwraca listę ich wyników w odpowiedniej kolejności.

```
import asyncio
import time

async def long_running_task(name, delay):
    print(f"Task {name}: starting...")
    await asyncio.sleep(delay)
    print(f"Task {name}: finished.")
    return f"Result of {name}"

async def main():
    start_time = time.time()

    # Create tasks to run concurrently
    task1 = asyncio.create_task(long_running_task("A", 2))
    task2 = asyncio.create_task(long_running_task("B", 3))

    # Wait for both tasks to complete.
    # The total time will be roughly the duration of the longest task (~3s),
    # not the sum of their durations (2s + 3s = 5s).
    results = await asyncio.gather(task1, task2)
    
    # An alternative, often cleaner way:
    # results = await asyncio.gather(
    #     long_running_task("A", 2),
    #     long_running_task("B", 3)
    # )

    print(f"Results: {results}")
    
    end_time = time.time()
    print(f"Total execution time: {end_time - start_time:.2f} seconds")

asyncio.run(main())
```

**Wynik działania:**

```
Task A: starting...
Task B: starting...
Task A: finished.
Task B: finished.
Results: ['Result of A', 'Result of B']
Total execution time: 3.01 seconds
```

Jak widać, oba zadania rozpoczęły się niemal jednocześnie, a całkowity czas wykonania jest ograniczony przez najdłuższe zadanie, co dowodzi współbieżnego wykonania.

---

### Kluczowe koncepcje techniczne

- **Współbieżność kooperatywna (Cooperative Multitasking)**: W przeciwieństwie do wielowątkowości z wywłaszczaniem (preemptive multitasking), gdzie system operacyjny decyduje o przełączaniu kontekstu, w `asyncio` korutyny muszą jawnie oddać kontrolę za pomocą `await`. Długotrwała, synchroniczna operacja (np. złożone obliczenia CPU) wewnątrz korutyny bez `await` zablokuje całą pętlę zdarzeń i uniemożliwi wykonanie innych zadań.
- **Pętla zdarzeń (Event Loop)**: Jest to rdzeń `asyncio`. Odpowiada za zarządzanie i dystrybucję czasu wykonania pomiędzy wszystkie aktywne zadania. Działa w jednym wątku.
- **Zastosowania**: `async`/`await` jest idealne dla programów **I/O-bound** (ograniczonych przez operacje wejścia/wyjścia), takich jak:
  - Serwery i klienty sieciowe (np. HTTP serwery z `aiohttp`, `FastAPI`).
  - Programy komunikujące się z bazami danych (`asyncpg`, `motor`).
  - Web scrapers, które wysyłają wiele zapytań HTTP jednocześnie.
  - Aplikacje czasu rzeczywistego (np. czaty).
- **Nie jest to rozwiązanie dla problemów CPU-bound**: W przypadku zadań intensywnie wykorzystujących procesor (np. przetwarzanie obrazów, skomplikowane obliczenia matematyczne), `asyncio` nie przyniesie korzyści, ponieważ pętla zdarzeń będzie zablokowana. W takich przypadkach lepszym rozwiązaniem jest użycie wieloprocesowości (`multiprocessing`).