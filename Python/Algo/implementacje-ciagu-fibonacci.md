# Implementacje ciągu Fibonacci w Pythonie

Ciąg Fibonacci to klasyczny problem algorytmiczny, w którym każdy element jest sumą dwóch poprzednich: **1, 1, 2, 3, 5, 8, 13, 21, ...**

Poniżej przedstawiono różne podejścia do jego implementacji — od generatorów, przez iterację, rekurencję, aż po funkcje zwracające listę.

---

## 1. Generator z `yield` (nieskończony)

Najbardziej „pythonowy" sposób — leniwa ewaluacja, generuje kolejne elementy na żądanie bez limitu.

```python
def fib():
    a, b = 1, 1
    while True:
        yield a
        a, b = b, a + b

# Użycie — wypisanie 10 pierwszych elementów:
for index, x in enumerate(fib()):
    if index == 10:
        break
    print(x)
```

**Kluczowe cechy:**
- `yield` zamienia funkcję w generator — nie oblicza wszystkiego z góry
- Nieskończona pętla `while True` jest bezpieczna, bo generator produkuje wartości leniwie
- Nadaje się do strumieniowego przetwarzania danych

---

## 2. Generator z parametrem `n`

Wersja z parametrem ograniczającym liczbę generowanych elementów.

```python
def fib(n):
    a, b = 1, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

# Użycie:
for x in fib(10):
    print(x)
```

**Różnica vs wersja 1:** nie wymaga zewnętrznego `break` — sam generator wie, kiedy się zatrzymać.

---

## 3. Iteracyjna (bez `yield`)

Klasyczna pętla — wypisuje elementy bezpośrednio przez `print`.

```python
def fib(n):
    a, b = 1, 1
    for _ in range(n):
        print(a)
        a, b = b, a + b

# Użycie:
fib(10)
```

**Uwaga:** ta wersja nie zwraca żadnej wartości — tylko wypisuje. Nie nadaje się do dalszego przetwarzania wyniku.

---

## 4. Iteracyjna — zwraca listę

Zamiast drukować, zbiera wyniki do listy i ją zwraca.

```python
def fib(n):
    result = []
    a, b = 1, 1
    for _ in range(n):
        result.append(a)
        a, b = b, a + b
    return result

# Użycie:
numbers = fib(10)
print(numbers)  # [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
```

**Zaleta:** wynik można dalej przetwarzać (filtrować, mapować, sortować itp.).

---

## 5. Rekurencyjna (klasyczna)

Najprostsza koncepcyjnie, ale **najwolniejsza** — złożoność wykładnicza O(2ⁿ).

```python
def fib(n):
    if n <= 2:
        return 1
    return fib(n - 1) + fib(n - 2)

# Użycie — wypisanie 10 pierwszych elementów:
for i in range(1, 11):
    print(fib(i))
```

**Problem:** powtarza te same obliczenia wielokrotnie. Np. `fib(5)` oblicza `fib(3)` dwa razy.

```
fib(5)
├── fib(4)
│   ├── fib(3)
│   │   ├── fib(2) = 1
│   │   └── fib(1) = 1
│   └── fib(2) = 1
└── fib(3)          ← powtórzenie!
    ├── fib(2) = 1
    └── fib(1) = 1
```

---

## 6. Rekurencyjna z memoizacją (`lru_cache`)

Rozwiązanie problemu powtarzających się obliczeń — cache'owanie wyników.

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    if n <= 2:
        return 1
    return fib(n - 1) + fib(n - 2)

# Użycie:
print([fib(i) for i in range(1, 11)])
# [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
```

**Złożoność:** O(n) zamiast O(2ⁿ) — każda wartość obliczana jest tylko raz.

---

## 7. Rekurencyjna — zwraca listę

Rekurencyjna funkcja, która buduje i zwraca listę wynikową.

```python
def fib(n):
    if n == 1:
        return [1]
    if n == 2:
        return [1, 1]
    prev = fib(n - 1)
    prev.append(prev[-1] + prev[-2])
    return prev

# Użycie:
print(fib(10))  # [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
```

---

## Porównanie

| Wersja | Zwraca | Złożoność | Pamięć | Kiedy używać |
|---|---|---|---|---|
| Generator nieskończony | leniwie po 1 | O(n) | O(1) | Przetwarzanie strumieniowe |
| Generator z parametrem | leniwie po 1 | O(n) | O(1) | Znana liczba elementów |
| Iteracyjna (print) | nic | O(n) | O(1) | Szybkie debugowanie |
| Iteracyjna (lista) | `list` | O(n) | O(n) | Dalsze przetwarzanie |
| Rekurencyjna | `int` | O(2ⁿ) | O(n) stos | Nigdy w produkcji |
| Rekursja + cache | `int` | O(n) | O(n) | Programowanie dynamiczne |
| Rekursja → lista | `list` | O(n) | O(n) | Ćwiczenie rekurencji |

---

## Powiązane tematy

- [yield w Pythonie](../yield-w-pythonie.md)
- [Dekoratory w Pythonie](../dekoratory-w-pythonie.md) — `@lru_cache` to dekorator
- [Biblioteka functools](../biblioteka-functools-python.md) — `lru_cache` pochodzi z `functools`
