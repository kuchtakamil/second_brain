# Biblioteka functools Python

**Data:** 2025-07-15

---

**User:**

Biblioteka functools w Python. Podaj jej najważniejsze cechy i zastosowania.

---

**Assistant:**

Biblioteka `functools` w Pythonie to moduł standardowy zawierający funkcje i dekoratory wspomagające programowanie funkcyjne oraz operacje na funkcjach. Oto jej najważniejsze cechy i zastosowania:

---

### 🔧 **Najważniejsze cechy:**

1. **Wsparcie dla programowania funkcyjnego**  
   `functools` umożliwia traktowanie funkcji jako obiektów pierwszoklasowych – można je przekazywać, modyfikować i komponować.

2. **Optymalizacja wydajności**  
   Niektóre narzędzia w `functools` (np. `lru_cache`) pomagają w cache'owaniu wyników funkcji, co może znacząco przyspieszyć działanie programów.

3. **Dekoratory funkcji**  
   Moduł udostępnia gotowe dekoratory lub ułatwia tworzenie własnych.

4. **Tworzenie funkcji częściowo zastosowanych (partial application)**  
   Pozwala „przywiązać” część argumentów funkcji i stworzyć nową wersję funkcji z domyślnymi wartościami.

---

### 📌 **Najważniejsze funkcje i zastosowania:**

| Funkcja / Klasa            | Zastosowanie |
|---------------------------|--------------|
| `@lru_cache(maxsize=128)` | Cache'owanie wyników funkcji – przyspiesza np. rekurencję. |
| `partial(func, *args, **kwargs)` | Tworzy nową funkcję z ustalonymi domyślnymi argumentami. |
| `wraps(wrapped_func)`     | Dekorator pomagający zachować metadane (nazwę, docstring) oryginalnej funkcji przy tworzeniu dekoratorów. |
| `cached_property`         | Zamienia metodę klasy w właściwość z cache'em (od Python 3.8). |
| `reduce(function, iterable[, initializer])` | Agreguje dane w kolekcji do jednej wartości (np. suma, iloczyn). |
| `singledispatch`          | Dekorator umożliwiający przeciążenie funkcji na podstawie typu pierwszego argumentu. |
| `total_ordering`          | Generuje brakujące metody porównania (`__le__`, `__ge__` itd.) na podstawie jednej lub dwóch. |
| `cmp_to_key(func)`        | Zamienia funkcję porównującą dwa elementy (cmp-style) w klucz sortujący (key-style). |
| `cache`                   | Jak `lru_cache`, ale bez ograniczenia rozmiaru cache'a (od Python 3.9). |

---

### 📘 **Przykłady zastosowań:**

#### 1. Cache'owanie funkcji rekurencyjnej
```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)
```

#### 2. Użycie `partial`
```python
from functools import partial

def pow(base, exp):
    return base ** exp

square = partial(pow, exp=2)
cube = partial(pow, exp=3)
```

#### 3. Tworzenie dekoratora z `wraps`
```python
from functools import wraps

def logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper
```

#### 4. Przeciążenie funkcji z `singledispatch`
```python
from functools import singledispatch

@singledispatch
def process(arg):
    raise NotImplementedError("Unsupported type")

@process.register(int)
def _(arg):
    return arg + 1

@process.register(str)
def _(arg):
    return arg.upper()
```

---

Jeśli chcesz, mogę przygotować też zestaw przykładów do nauki lub ćwiczeń z tej biblioteki.