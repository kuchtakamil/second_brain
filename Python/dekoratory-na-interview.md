# Dekoratory na interview – dwa praktyczne przykłady

Dekorator to wzorzec, w którym **funkcja opakowuje inną funkcję**, dodając jej nową logikę bez modyfikowania jej ciała. Jest to zastosowanie wzorca Proxy/Wrapper, mocno osadzone w tzw. programowaniu wyższego rzędu.

Poniżej dwa realne przykłady z uzasadnieniem — idealne jako odpowiedź na interview.

---

## Przykład 1 – Dekorator bez parametru: `@retry`

### Problem

Wywołujesz zewnętrzne API lub bazę danych. Czasem operacja kończy się błędem nie z Twojej winy (timeout, chwilowy brak połączenia). Zamiast przerywać, chcesz automatycznie ponowić próbę — ale tylko parę razy.

### Rozwiązanie

```python
import time
from functools import wraps


def retry(func):
    """
    Decorator that retries a failing function up to 3 times
    with a 1-second delay between attempts.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        last_exception = None
        for attempt in range(1, 4):  # attempts: 1, 2, 3
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                print(f"[retry] Attempt {attempt} failed: {e}. Retrying...")
                time.sleep(1)
        raise RuntimeError(
            f"All 3 attempts failed for '{func.__name__}'"
        ) from last_exception
    return wrapper
```

### Użycie

```python
call_count = 0

@retry
def fetch_data():
    global call_count
    call_count += 1
    if call_count < 3:
        raise ConnectionError("Service temporarily unavailable")
    return {"status": "ok", "data": [1, 2, 3]}


result = fetch_data()
print(result)
```

### Wyjście

```
[retry] Attempt 1 failed: Service temporarily unavailable. Retrying...
[retry] Attempt 2 failed: Service temporarily unavailable. Retrying...
{'status': 'ok', 'data': [1, 2, 3]}
```

### Kluczowe rzeczy do omówienia na interview

- `@wraps(func)` — zachowuje `__name__`, `__doc__` i `__wrapped__` oryginalnej funkcji; bez tego debuggery i frameworki (np. FastAPI) mogą się mylić
- `*args, **kwargs` — wrapper jest transparentny: przyjmuje i przekazuje dowolne argumenty
- przechwytujemy ogólny `Exception` i re-raise'ujemy jako `RuntimeError` z kontekstem (`from last_exception`)

---

## Przykład 2 – Dekorator z parametrem: `@retry(max_attempts=5, delay=2.0)`

### Problem

Wróćmy do `@retry`, ale tym razem chcemy skonfigurować liczbę prób i czas oczekiwania z poziomu wywołania — bo różne endpointy mogą mieć różną tolerancję na błędy.

### Dlaczego potrzebny jest dodatkowy poziom zagnieżdżenia?

Kiedy piszesz `@retry`, Python wywołuje `retry(func)`.  
Kiedy piszesz `@retry(max_attempts=5)`, Python najpierw wywołuje `retry(max_attempts=5)`, a **wynik tego wywołania** musi być właściwym dekoratorem przyjmującym `func`.

Stąd trzy poziomy:

```
retry(max_attempts, delay)   ← przyjmuje konfigurację, zwraca decorator
  └─ decorator(func)         ← przyjmuje funkcję, zwraca wrapper
       └─ wrapper(*args)     ← faktycznie wykonywany zamiast func
```

### Rozwiązanie

```python
import time
from functools import wraps


def retry(max_attempts: int = 3, delay: float = 1.0, exceptions: tuple = (Exception,)):
    """
    Configurable retry decorator.

    Args:
        max_attempts: Maximum number of retry attempts.
        delay: Seconds to wait between attempts.
        exceptions: Tuple of exception types that trigger a retry.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    print(
                        f"[retry] '{func.__name__}' attempt {attempt}/{max_attempts} "
                        f"failed: {e}. Waiting {delay}s..."
                    )
                    if attempt < max_attempts:
                        time.sleep(delay)
            raise RuntimeError(
                f"'{func.__name__}' failed after {max_attempts} attempts"
            ) from last_exception
        return wrapper
    return decorator
```

### Użycie

```python
call_count = 0

@retry(max_attempts=5, delay=0.5, exceptions=(ConnectionError, TimeoutError))
def fetch_user(user_id: int) -> dict:
    """Fetches user data from remote service."""
    global call_count
    call_count += 1
    if call_count < 4:
        raise ConnectionError(f"Cannot reach service (attempt {call_count})")
    return {"id": user_id, "name": "Alice"}


user = fetch_user(42)
print(user)
```

### Wyjście

```
[retry] 'fetch_user' attempt 1/5 failed: Cannot reach service (attempt 1). Waiting 0.5s...
[retry] 'fetch_user' attempt 2/5 failed: Cannot reach service (attempt 2). Waiting 0.5s...
[retry] 'fetch_user' attempt 3/5 failed: Cannot reach service (attempt 3). Waiting 0.5s...
{'id': 42, 'name': 'Alice'}
```

### Introspekcja działa poprawnie

```python
print(fetch_user.__name__)    # fetch_user (nie wrapper!)
print(fetch_user.__doc__)     # Fetches user data from remote service.
print(fetch_user.__wrapped__) # <function fetch_user at 0x...>
```

---

## Dlaczego 2 funkcje vs 3 funkcje?

To najważniejsza rzecz do zrozumienia na interview. Wynika wprost z tego, **co Python robi pod spodem** gdy napotka `@`.

### Co Python robi z `@dekorator`?

Składnia `@` to tylko cukier składniowy. Poniższe dwa zapisy są **identyczne**:

```python
@retry
def fetch_data(): ...

# to samo co:
fetch_data = retry(fetch_data)
```

Python bierze funkcję `fetch_data` i **podaje ją jako argument** do `retry`. Dlatego `retry` musi przyjmować `func` — to jest jego jedyny argument.

### Co Python robi z `@dekorator(...)`?

```python
@retry(max_attempts=5)
def fetch_data(): ...

# to samo co:
fetch_data = retry(max_attempts=5)(fetch_data)
```

Zauważ różnicę: `retry(max_attempts=5)` jest **wywoływane najpierw**, zanim Python jeszcze wie cokolwiek o `fetch_data`. Wynik tego wywołania musi być **funkcją**, którą Python może następnie wywołać z `fetch_data` jako argumentem.

Innymi słowy: `retry(max_attempts=5)` musi zwrócić coś, co zachowuje się jak `retry` z poprzedniego przykładu — czyli funkcję przyjmującą `func`.

### Krok po kroku — skąd wynika liczba poziomów

**Dekorator bez parametru — 2 poziomy:**

```
retry(func)                  ← Python wywołuje to bezpośrednio
  └─ wrapper(*args, **kwargs) ← to jest zwracane jako nowa "func"
```

`retry` ma jeden obowiązek: dostać `func` i zwrócić `wrapper`. Wystarczą 2 funkcje.

**Dekorator z parametrem — 3 poziomy:**

```
retry(max_attempts, delay)   ← Python wywołuje to NAJPIERW (po napotkaniu @)
  └─ decorator(func)         ← wynik musi być dekoratorem; dostaje func
       └─ wrapper(*args)     ← to jest zwracane jako nowa "func"
```

`retry(max_attempts, delay)` ma jeden obowiązek: zapamiętać konfigurację i **zwrócić dekorator**. Dopiero ten dekorator dostaje `func`. Potrzebny jest więc dodatkowy poziom — stąd 3 funkcje.

### Prosta reguła do zapamiętania

> **Ile argumentów "przyjmuje" `@`?**  
> — Żadnych (samo `@retry`) → funkcja zewnętrzna przyjmuje `func` → **2 poziomy**  
> — Jakieś (`@retry(...)`) → funkcja zewnętrzna przyjmuje konfigurację, zwraca dekorator → **3 poziomy**

### Domknięcie (closure) jako klej

W obu przypadkach `wrapper` może używać zmiennych z zewnętrznych zakresów dzięki **domknięciu**:

```python
# Dekorator bez parametru — wrapper "widzi" func z zakresu retry:
def retry(func):
    def wrapper(*args, **kwargs):
        return func(...)  # func pochodzi z domknięcia
    return wrapper

# Dekorator z parametrem — wrapper "widzi" func i max_attempts z dwóch zakresów:
def retry(max_attempts):
    def decorator(func):
        def wrapper(*args, **kwargs):
            # max_attempts pochodzi z zakresu retry (domknięcie)
            # func pochodzi z zakresu decorator (domknięcie)
            for attempt in range(max_attempts):
                return func(...)
        return wrapper
    return decorator
```

To jest właśnie powód, dla którego funkcje są zagnieżdżone — każda zewnętrzna funkcja "zamraża" swoje argumenty w domknięciu, które staje się dostępne dla funkcji wewnętrznych.

---

## Porównanie obu podejść

| Cecha                     | `@retry` (bez parametru)         | `@retry(...)` (z parametrem)                  |
|---------------------------|----------------------------------|-----------------------------------------------|
| Liczba zagnieżdżeń        | 2 (`decorator` + `wrapper`)      | 3 (`outer` + `decorator` + `wrapper`)         |
| Wywołanie w kodzie        | `@retry`                         | `@retry(max_attempts=5)`                      |
| Ekwiwalent                | `func = retry(func)`             | `func = retry(max_attempts=5)(func)`          |
| Konfigurowalność          | stała (hardcoded)                | dynamiczna per-użycie                         |
| Kiedy stosować            | prosta, jednorazowa reguła       | różne warianty dla różnych kontekstów         |

---

## Powiązane tematy

- [dekoratory-w-pythonie.md](dekoratory-w-pythonie.md) — ogólny opis dekoratorów, `@wraps`, dekoratory na klasach
- [biblioteka-functools-python.md](biblioteka-functools-python.md) — `functools.wraps`, `lru_cache`, `partial`
- [currying-w-pythonie.md](currying-w-pythonie.md) — pokrewna technika: funkcje zwracające funkcje z domkniętymi argumentami
