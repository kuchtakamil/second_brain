# Dekoratory w Pythonie

**Data:** 2025-05-03

---

**User:**

Omów Dekoratory w Python. Podaj bardziej skomplikowany przykład niż timer i logger. Czy można użyć więcej niż 1 dekorator na funkcji? Czy można ich użyć na klasie lub innych miejscach?

---

**Assistant:**

### Dekoratory w Pythonie – zaawansowane omówienie

#### Czym są dekoratory?

Dekoratory w Pythonie to funkcje, które przyjmują inną funkcję (lub klasę) jako argument i zwracają funkcję (lub klasę) opakowaną nową logiką. Najczęściej służą do dodawania funkcjonalności bez modyfikowania oryginalnej funkcji lub klasy (np. walidacja, cache, retry, kontrola dostępu).

---

### Możliwość użycia wielu dekoratorów

Tak – można używać wielu dekoratorów naraz:

```python
@decorator1
@decorator2
def my_function():
    pass
```

To jest równoważne z:
```python
my_function = decorator1(decorator2(my_function))
```

---

### Gdzie można używać dekoratorów?

1. **Funkcje** – najczęstsze użycie.
2. **Metody klas** – identycznie jak funkcje.
3. **Klasy** – dekoratory mogą przyjmować klasę jako argument i zwracać zmodyfikowaną klasę.

---

### Zaawansowany przykład: **kontrola uprawnień z kontekstem użytkownika**

Załóżmy, że mamy system z aktualnym użytkownikiem, i chcemy, aby niektóre funkcje były dostępne tylko dla administratora.

#### Kod:

```python
from functools import wraps

# Przykładowy kontekst użytkownika
class UserContext:
    current_user = {"name": "alice", "role": "user"}

# Dekorator sprawdzający uprawnienia
def require_role(required_role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user_role = UserContext.current_user["role"]
            if user_role != required_role:
                raise PermissionError(f"Access denied for role: {user_role}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Inny dekorator – logowanie wywołania
def audit_log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Audit: calling {func.__name__} as {UserContext.current_user['name']}")
        return func(*args, **kwargs)
    return wrapper

# Przykład funkcji z dwoma dekoratorami
@audit_log
@require_role("admin")
def delete_database():
    print("Database deleted!")

# Przykład użycia
try:
    delete_database()
except PermissionError as e:
    print(e)

# Zmiana kontekstu na admina
UserContext.current_user = {"name": "bob", "role": "admin"}
delete_database()
```

#### Wynik:
```
Audit: calling delete_database as alice
Access denied for role: user

Audit: calling delete_database as bob
Database deleted!
```

---

### Dekorator na klasie – przykład rejestratora klas

```python
registry = []

def register_class(cls):
    registry.append(cls)
    return cls

@register_class
class MyService:
    pass

print(registry)  # [<class '__main__.MyService'>]
```

---

Chcesz, żebym pokazał też przykład dekoratora klasy modyfikującego metody, np. automatyczne logowanie wywołań wszystkich metod instancji?

---

**User:**

co to jest  @wraps(func) i czy jest niezbędne? Dlaczego są aż 3 funkcje require_role, decorator, wrapper? do tej pory spotykałem dekoratory złożone z 2 np. logger, wrapper.

---

**Assistant:**

Świetne pytania – przejdźmy przez nie krok po kroku.

---

## 🧩 1. Co to jest `@wraps(func)` i czy jest niezbędne?

Dekorator `@wraps` pochodzi z modułu `functools` i **kopiuje metadane** (takie jak `__name__`, `__doc__`, `__module__`, itp.) z dekorowanej funkcji do funkcji wrappera.

### Przykład bez `@wraps`:

```python
def simple_decorator(f):
    def wrapper(*args, **kwargs):
        return f(*args, **kwargs)
    return wrapper

@simple_decorator
def greet():
    """Greets the user."""
    print("Hello")

print(greet.__name__)  # wrapper, nie greet
print(greet.__doc__)   # None
```

### Przykład z `@wraps(f)`:

```python
from functools import wraps

def better_decorator(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return f(*args, **kwargs)
    return wrapper

@better_decorator
def greet():
    """Greets the user."""
    print("Hello")

print(greet.__name__)  # greet
print(greet.__doc__)   # "Greets the user."
```

➡ **Nie jest niezbędne technicznie**, ale **zalecane** – szczególnie, jeśli chcesz:
- używać introspekcji (`help()`, `__name__`, `__doc__`, debuggery)
- mieć czytelne logi, tracebacks
- pisać testy jednostkowe

---

## 🧱 2. Dlaczego `require_role` ma 3 poziomy funkcji?

```python
def require_role(required_role):  # 1. Funkcja przyjmująca argument dekoratora
    def decorator(func):          # 2. Właściwy dekorator
        @wraps(func)
        def wrapper(*args, **kwargs):  # 3. Wrapper funkcji
            # logika
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

To jest **tzw. dekorator z parametrem**. 

### Porównanie:

#### 🔹 Zwykły dekorator – 2 funkcje:
```python
def logger(func):
    def wrapper(*args, **kwargs):
        print("Calling", func.__name__)
        return func(*args, **kwargs)
    return wrapper
```

#### 🔹 Dekorator z parametrem – 3 funkcje:
```python
@require_role("admin")
def func(): ...
```

To wywołuje:

```python
func = require_role("admin")(func)
```

Czyli:
- `require_role("admin")` → zwraca dekorator
- dekorator → opakowuje `func` w `wrapper`

---

### Kiedy są potrzebne 3 poziomy?
Kiedy dekorator **musi przyjmować argument**, np. `@retry(3)`, `@require_role("admin")`, `@throttle(100ms)`, itd.

---

Chcesz, żebym pokazał przykład dekoratora z parametrem, ale w wersji z klasą zamiast funkcji?

---

**User:**

Napisz więcej szczegółów dlaczego użycie  @wraps(f) jest zalecane

---

**Assistant:**

Jasne! Użycie `@wraps(f)` z `functools` jest bardzo **zalecane**, a nie tylko kosmetyczne. Poniżej znajdziesz konkretne powody, **dlaczego** warto go stosować.

---

## 🔍 Co dokładnie robi `@wraps(f)`?

```python
from functools import wraps

@wraps(original_function)
def wrapper(...):
    ...
```

To jest skrót od:
```python
wrapper = functools.update_wrapper(wrapper, original_function)
```

`update_wrapper()`:
- Kopiuje:
  - `__module__`
  - `__name__`
  - `__qualname__`
  - `__annotations__`
  - `__doc__`
- Przypisuje: `__wrapped__ = original_function` (ważne dla introspekcji!)

---

## ✅ Dlaczego to jest **zalecane**:

### 1. 🔎 **Zachowanie nazw i dokumentacji (`__name__`, `__doc__`)**

Bez `@wraps`:

```python
print(my_func.__name__)  # 'wrapper'
help(my_func)            # brak docstringa
```

Z `@wraps`:

```python
print(my_func.__name__)  # 'my_func'
help(my_func)            # pokazuje docstring
```

➡️ Pomaga w dokumentacji, debugowaniu, logach, tracebackach.

---

### 2. 🛠️ **Lepsze wsparcie dla narzędzi introspekcyjnych**

Bez `@wraps`, narzędzia takie jak `inspect`, `help()`, linters, IDE (np. IntelliSense w PyCharm, VSCode) mogą nie działać poprawnie.

Przykład:

```python
from inspect import signature

@logger
def my_func(a, b):
    pass

print(signature(my_func))  # bez wraps może się nie udać
```

---

### 3. 🔄 **Działa `functools.wraps` → `__wrapped__` → dostajesz oryginalną funkcję**

Dzięki temu można:
- testować oryginalną funkcję pomijając dekoratory
- stosować techniki meta-programowania, np. re-wrap
- ułatwia to np. `unittest.mock.patch` lub frameworki typu `pytest`

```python
f.__wrapped__()  # działa tylko z @wraps
```

---

### 4. 🧪 **Testy jednostkowe / mocking / monkey patching**

Bez `@wraps`, niektóre frameworki testowe (np. `pytest`, `unittest`) mogą mieć problemy z analizą oryginalnej funkcji lub jej podmienieniem (mockowaniem).

---

### 5. 🤖 **Frameworki i biblioteki (np. Flask, FastAPI, Django)**

Wiele frameworków używa introspekcji, np. sprawdzania sygnatury funkcji, `__doc__`, `__name__`, `__annotations__`.

Brak `@wraps` może prowadzić do trudnych do znalezienia błędów lub nieoczekiwanych zachowań (np. brak dokumentacji endpointu w Swaggerze/FastAPI).

---

### 🔚 Podsumowanie

Użycie `@wraps(f)` to:

✅ Lepsza debuggowalność  
✅ Wsparcie dla introspekcji  
✅ Kompatybilność z narzędziami  
✅ Poprawne działanie testów i mocków  
✅ Unikanie ukrytych bugów w frameworkach  

➡ **Nie psuje niczego, ale daje sporo.** W praktyce **prawie zawsze powinieneś go używać**, gdy piszesz własne dekoratory.

---

Chcesz, żebym pokazał przypadek, gdzie brak `@wraps` psuje coś konkretnego, np. w `pytest` lub `FastAPI`?