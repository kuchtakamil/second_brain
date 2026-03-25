# Context Manager w Pythonie

**Data:** 2025-05-03

---

**User:**

Opisz w Python askepkt:
Context managers – with, __enter__, __exit__, contextlib.

---

**Assistant:**

W Pythonie *context managers* (menedżery kontekstu) służą do zarządzania zasobami w sposób bezpieczny i czytelny — na przykład plikami, połączeniami sieciowymi, blokadami itp. Głównym zastosowaniem jest zapewnienie, że zasoby są poprawnie otwierane i zamykane, nawet jeśli wystąpi wyjątek.

## 1. Słowo kluczowe `with`

Najbardziej popularny sposób korzystania z context managerów to użycie słowa kluczowego `with`. Przykład:

```python
with open('plik.txt', 'r') as f:
    dane = f.read()
```

Tutaj `open()` zwraca obiekt, który działa jako menedżer kontekstu — `__enter__` otwiera plik, `__exit__` go zamyka automatycznie, nawet jeśli wewnątrz bloku wystąpi wyjątek.

---

## 2. Metody `__enter__` i `__exit__`

Aby stworzyć własny menedżer kontekstu, można zaimplementować metody `__enter__` i `__exit__` w klasie:

```python
class MyContextManager:
    def __enter__(self):
        print("Wchodzę do kontekstu")
        return self  # opcjonalnie jakiś zasób

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Wychodzę z kontekstu")
        if exc_type:
            print(f"Wystąpił wyjątek: {exc_val}")
        # można zwrócić True, żeby "stłumić" wyjątek
```

Użycie:

```python
with MyContextManager():
    print("W środku")
```

---

## 3. `contextlib` — uproszczenie tworzenia context managerów

Moduł `contextlib` pozwala pisać menedżery kontekstu jako funkcje, co jest prostsze i bardziej zwięzłe.

### Przykład z dekoratorem `@contextmanager`:

```python
from contextlib import contextmanager

@contextmanager
def my_context():
    print("Wchodzę do kontekstu")
    yield "zasób"
    print("Wychodzę z kontekstu")

with my_context() as val:
    print(f"W środku z wartością: {val}")
```

Zamiast `__enter__` i `__exit__`, funkcja dzieli się na część przed `yield` (setup) i po `yield` (cleanup).

---

## Podsumowanie

| Element           | Opis                                                        |
|-------------------|-------------------------------------------------------------|
| `with`            | Słowo kluczowe do użycia menedżera kontekstu                |
| `__enter__`       | Wywoływane na wejściu do bloku `with`                       |
| `__exit__`        | Wywoływane przy wyjściu (nawet przy wyjątku)                |
| `contextlib`      | Moduł wspierający pisanie context managerów jako funkcji    |
| `@contextmanager` | Dekorator do tworzenia menedżera kontekstu z funkcji       |

Chcesz przykład context managera do zarządzania połączeniem do bazy, plikiem, czy może czymś innym?