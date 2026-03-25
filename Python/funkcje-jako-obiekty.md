# Funkcje jako obiekty

**Data:** 2025-05-02

---

**User:**

Jestem doświadczonym programistą i uczę się pythona. Przedstaw zaawansowane zaganienie
Funkcje jako obiekty pierwszoklasowe – przekazywanie, zwracanie funkcji, functools.

---

**Assistant:**

Użytkownik jest doświadczonym programistą i uczy się Pythona.

---

**Assistant:**

Świetnie! W Pythonie funkcje są **obiektami pierwszoklasowymi**, co oznacza, że można je:

- przypisywać do zmiennych,
- przekazywać jako argumenty do innych funkcji,
- zwracać jako wynik z funkcji,
- przechowywać w strukturach danych (np. listach, słownikach),
- dekorować i modyfikować.

Poniżej przedstawiam zaawansowane zagadnienie z tym związane:

---

## 📌 Funkcje jako obiekty pierwszoklasowe – przekazywanie, zwracanie, `functools`

### 1. **Przekazywanie funkcji jako argumentów**
```python
def greet(name):
    return f"Hello, {name}!"

def execute(fn, arg):
    return fn(arg)

print(execute(greet, "Alice"))  # Hello, Alice!
```

### 2. **Zwracanie funkcji z funkcji**
```python
def multiplier(factor):
    def multiply(x):
        return x * factor
    return multiply

double = multiplier(2)
print(double(10))  # 20
```

To przykład **funkcji domkniętej** (*closure*) – `multiply` zapamiętuje wartość `factor` mimo, że `multiplier` już się zakończył.

### 3. **`functools.partial` – częściowa aplikacja argumentów**
```python
from functools import partial

def power(base, exponent):
    return base ** exponent

square = partial(power, exponent=2)
print(square(5))  # 25
```

`partial` tworzy nową funkcję z domyślnie „wstrzykniętymi” argumentami.

### 4. **`functools.lru_cache` – cache wyników**
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def fibonacci(n):
    if n in (0, 1):
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(30))  # Szybko, dzięki cache
```

Przydatne np. w rekurencji, optymalizacji wydajności.

### 5. **Dekoratory funkcji (bazujące na tym, że funkcje można przekazywać)**
```python
def logger(fn):
    def wrapper(*args, **kwargs):
        print(f"Calling {fn.__name__} with {args}, {kwargs}")
        return fn(*args, **kwargs)
    return wrapper

@logger
def add(a, b):
    return a + b

add(2, 3)  # Loguje wywołanie i wynik
```

Dekoratory to wyższy poziom abstrakcji, szeroko wykorzystywany np. w Flasku, Django, testach, metaprogramowaniu.

---

Chcesz przykład praktycznego mini-projektu z wykorzystaniem tych koncepcji?