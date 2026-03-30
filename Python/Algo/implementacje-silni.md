# Implementacje silni (factorial) w Pythonie

Silnia liczby całkowitej dodatniej $n$ (oznaczana jako $n!$) to iloczyn wszystkich liczb naturalnych od 1 do $n$. Na przykład:
$5! = 1 \cdot 2 \cdot 3 \cdot 4 \cdot 5 = 120$

Poniżej przedstawiono różne iteracyjne i rekurencyjne podejścia do obliczania silni, w tym wersje wykorzystujące generatory oraz zwracające pełne listy wyników.

---

## 1. Generator z `yield`

Podejście lazily generujące kolejne wartości silni (od $1!$ do $n!$). Idealne do iterowania przez kolejne wyniki bez obciążania pamięci.

```python
def factorial_yield(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
        yield result

# Użycie:
for val in factorial_yield(5):
    print(val)  # wypisze: 1, 2, 6, 24, 120
```

**Kluczowe cechy:**
- Bardzo wydajne pod względem pamięci (złożoność pamięciowa O(1)).
- `yield` zamienia funkcję w generator — kolejne wywołania pamiętają stan zmiennej `result`.

---

## 2. Iteracyjna bez `yield` (zwraca pojedynczą wartość)

Klasyczna wersja pętlowa, która na samym końcu po prostu zwraca obliczoną silnię dla zadanego $n$. 

```python
def factorial_iterative(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

# Użycie:
print(factorial_iterative(5))  # 120
```

**Zaleta:** Najprostsza, najszybsza i najbardziej optymalna do jednorazowego obliczenia silni.

---

## 3. Iteracyjna z `print` (wypisuje wyniki bezpośrednio)

Wersja "efekciarska", która w trakcie pracy sama drukuje postęp i wyniki, zamiast je zwracać.

```python
def factorial_print(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
        print(f"{i}! = {result}")

# Użycie:
factorial_print(5)
# Wyjście:
# 1! = 1
# 2! = 2
# 3! = 6
# 4! = 24
# 5! = 120
```

**Uwaga:** Funkcja zwraca `None`. Nadaje się do debugowania lub wizualizacji, ale zwracanego wyniku nie da się przypisać do zmiennej.

---

## 4. Wersja bez `print`, zwracająca listę

Zbiera wszystkie częściowe wyniki silni (od $1!$ aż do $n!$) i na koniec zwraca w formie lity. Pełni podobną funkcję co generator, ale w pamięci od razu trzyma wszystkie pre-kalkulowane elementy.

```python
def factorial_list(n):
    results = []
    current = 1
    for i in range(1, n + 1):
        current *= i
        results.append(current)
    return results

# Użycie:
factorials = factorial_list(5)
print(factorials)  # [1, 2, 6, 24, 120]
```

**Zaleta:** Jeżeli będziemy wielokrotnie odczytywać poszczególne wyniki (np. potrzebujemy nagle wartości $3!$), możemy to zrobić operując na zwróconej tablicy. Złożoność pamięciowa to O(n).

---

## 5. Rekurencyjna

Czysto matematyczne podejście do silni oparte na definicji: $n! = n \cdot (n-1)!$

```python
def factorial_recursive(n):
    # Warunek brzegowy (przypadek bazowy)
    if n == 0 or n == 1:
        return 1
    
    # Wywołanie rekurencyjne
    return n * factorial_recursive(n - 1)

# Użycie:
print(factorial_recursive(5))  # 120
```

**Problem:** Posiada próg głębokości rekurencji (domyślnie ok. 1000 w Pythonie). Obliczenie np. `factorial_recursive(2000)` natychmiast wrzuci błąd `RecursionError`. Ponadto odkładanie na stos za każdym wywołaniem sprawia, że zużywa więcej pamięci O(n).

---

## Podsumowanie

| Wersja | Co zwraca | Złożoność Czas. | Złożoność Pamięć. | Kiedy używać |
|---|---|---|---|---|
| **Z `yield`** | Generator | O(n) | O(1) | Potrzebujemy kolejnych wyników krok po kroku |
| **Iteracyjna** (bez yield) | Wartość `int` | O(n) | O(1) | Szybkie obliczenie jednej, konkretnej silni |
| **Z `print`** | `None` | O(n) | O(1) | Szybkie debugowanie wizualne |
| **Zwracająca listę** | O(n) | O(n) | Lista `list` | Jeśli przechowujesz ciąg wyników dla innych algorytmów |
| **Rekurencyjna** | Wartość `int` | O(n) | O(n) (na stos. wywołań) | Kodowanie "matematyczne" lub akademickie definicje |

Python posiada też wbudowaną obsługę silni dla najszybszych, gotowych do użycia obliczeń: 
```python
from math import factorial
print(factorial(5)) # 120
```
