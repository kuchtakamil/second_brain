# Implementacje wyszukiwania binarnego (Binary Search) w Pythonie

Wyszukiwanie binarne (binary search) to wysoce wydajny algorytm używany do znajdowania pozycji elementu w **posortowanej** tablicy. Wyszukiwanie to polega na dzieleniu przedziału poszukiwań na pół. Jeśli szukana wartość jest mniejsza od elementu środkowego, kontynuujemy poszukiwania w lewej połowie, a jeśli większa — w prawej.

**Złożoność czasowa:** $O(\log n)$
**Złożoność pamięciowa:** $O(1)$ dla wersji iteracyjnej, $O(\log n)$ dla wersji rekurencyjnej (ze względu na stos wywołań).

Poniżej przedstawiono różne podejścia do implementacji wyszukiwania binarnego w języku Python.

---

## 1. Wersja iteracyjna (najpopularniejsza)

Podejście klasyczne oparte na pętli `while`. Utrzymujemy wskaźniki na początek (`left`) i koniec (`right`) przeszukiwanego przedziału. Jest to najbardziej optymalne pamięciowo rozwiązanie w Pythonie.

```python
def binary_search_iterative(arr, target):
    left = 0
    right = len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        # Check if target is present at mid
        if arr[mid] == target:
            return mid
            
        # If target is greater, ignore left half
        elif arr[mid] < target:
            left = mid + 1
            
        # If target is smaller, ignore right half
        else:
            right = mid - 1
            
    # Target is not present in the array
    return -1

# Usage:
sorted_list = [2, 3, 4, 10, 40]
target_value = 10
result = binary_search_iterative(sorted_list, target_value)
print(f"Element index: {result}")  # Element index: 3
```

**Zalety:**
- Szybka pamięciowo i unikająca problemów z przepełnieniem stosu wywołań (co jest istotne dla długich list w Pythonie).

---

## 2. Wersja rekurencyjna

Czysto teoretyczne, algorytmiczne podejście wykorzystujące wywołania funkcji. Warto zauważyć, że wymaga ono przekazywania aktualnych indeksów `left` i `right`.

```python
def binary_search_recursive(arr, left, right, target):
    # Base case
    if right >= left:
        mid = (left + right) // 2
        
        # Check if target is present at mid
        if arr[mid] == target:
            return mid
            
        # If target is smaller than mid, it can only be present in left subarray
        elif arr[mid] > target:
            return binary_search_recursive(arr, left, mid - 1, target)
            
        # Else the element can only be present in right subarray
        else:
            return binary_search_recursive(arr, mid + 1, right, target)
            
    # Target is not present in the array
    else:
        return -1

# Usage:
sorted_list = [2, 3, 4, 10, 40]
target_value = 10
result = binary_search_recursive(sorted_list, 0, len(sorted_list)-1, target_value)
print(f"Element index: {result}")  # Element index: 3
```

**Problemy:**
- Podatna na limit głębokości rekurencji w Pythonie (`RecursionError` przy bardzo dużych danych).
- Złożoność pamięciowa to $O(\log n)$ poprzez alokację na stos wywołań funkcji.

---

## 3. Użycie wbudowanej biblioteki `bisect`

Python posiada wbudowany moduł `bisect`, który implementuje wyszukiwanie binarne pod maską w języku C, co czyni to najszybszym sposobem, gdy tylko zależy nam na wynikach.

### 3.1 Kompletny przegląd API modułu `bisect`

Moduł udostępnia **6 funkcji** podzielonych na dwie kategorie:

| Funkcja | Kategoria | Opis |
|---|---|---|
| `bisect_left(a, x)` | Wyszukiwanie | Punkt wstawienia **przed** istniejącymi duplikatami |
| `bisect_right(a, x)` | Wyszukiwanie | Punkt wstawienia **za** istniejącymi duplikatami |
| `bisect(a, x)` | Wyszukiwanie | Alias dla `bisect_right` |
| `insort_left(a, x)` | Wstawianie | Wstawia element **przed** duplikatami |
| `insort_right(a, x)` | Wstawianie | Wstawia element **za** duplikatami |
| `insort(a, x)` | Wstawianie | Alias dla `insort_right` |

> Wszystkie funkcje przyjmują opcjonalne parametry `lo` i `hi` ograniczające zakres przeszukiwania, oraz `key` (od **Python 3.10**) — funkcję transformującą elementy przed porównaniem.

---

### 3.2 `bisect_left` vs `bisect_right` — kluczowa różnica

Obie funkcje zwracają **indeks wstawienia**, ale różnią się zachowaniem przy duplikatach:

```python
import bisect

arr = [1, 3, 3, 3, 5, 7]
#      0  1  2  3  4  5

# bisect_left → indeks PRZED pierwszym duplikatem
print(bisect.bisect_left(arr, 3))   # 1  (wstawienie przed trójkami)

# bisect_right → indeks ZA ostatnim duplikatem
print(bisect.bisect_right(arr, 3))  # 4  (wstawienie za trójkami)

# Dla elementu bez duplikatów — wynik identyczny
print(bisect.bisect_left(arr, 5))   # 4
print(bisect.bisect_right(arr, 5))  # 5
```

**Wizualizacja na tablicy `[1, 3, 3, 3, 5, 7]` dla `x = 3`:**

```
Indeks:         0   1   2   3   4   5
Wartość:       [1,  3,  3,  3,  5,  7]
                    ^               ^
                    |               |
              bisect_left(3)=1   bisect_right(3)=4
                    ↑               ↑
           "wstaw PRZED trójki"  "wstaw ZA trójki"
```

**Wzorzec: wyszukiwanie binarne elementu za pomocą `bisect_left`:**

```python
import bisect

def binary_search_bisect(arr, target):
    # bisect_left locates the insertion point for target in arr 
    # to maintain sorted order
    index = bisect.bisect_left(arr, target)
    
    # Check if the target is actually present at the located index
    if index != len(arr) and arr[index] == target:
        return index
    return -1

# Usage:
sorted_list = [2, 3, 4, 10, 40]
target_value = 10
result = binary_search_bisect(sorted_list, target_value)
print(f"Element index: {result}")  # Element index: 3
```

---

### 3.3 `insort_left` i `insort_right` — wstawianie z zachowaniem porządku

Funkcje `insort` łączą dwa kroki: **znajdowanie pozycji** + **wstawianie** elementu. Wyszukiwanie trwa $O(\log n)$, ale samo `list.insert()` zajmuje $O(n)$ (przesuwanie elementów).

```python
import bisect

scores = [70, 80, 85, 90]

# insort_right (alias: insort) — wstawia ZA duplikatami
bisect.insort(scores, 85)
print(scores)  # [70, 80, 85, 85, 90]

# insort_left — wstawia PRZED duplikatami
scores2 = [70, 80, 85, 90]
bisect.insort_left(scores2, 85)
print(scores2)  # [70, 80, 85, 85, 90]
# Wynik wygląda identycznie, ale NOWY element jest na indeksie 2 (przed starym 85)
```

> **Kiedy to ważne?** Gdy elementy to obiekty o dodatkowych polach — kolejność wstawienia duplikatów wpływa na stabilność sortowania.

---

### 3.4 Parametry `lo`, `hi` i `key`

#### `lo` i `hi` — ograniczenie zakresu przeszukiwania

```python
import bisect

arr = [10, 20, 30, 40, 50, 60, 70, 80]

# Szukaj tylko w zakresie indeksów [2, 6) → [30, 40, 50, 60]
idx = bisect.bisect_left(arr, 45, lo=2, hi=6)
print(idx)  # 4 (między 40 a 50)
```

#### `key` (Python 3.10+) — transformacja elementów przy porównywaniu

Pozwala przeszukiwać listę obiektów bez konieczności tworzenia osobnej listy kluczy:

```python
import bisect
from dataclasses import dataclass

@dataclass
class Student:
    name: str
    grade: float

students = [
    Student("Anna", 3.5),
    Student("Jan", 4.0),
    Student("Kasia", 4.5),
    Student("Marek", 5.0),
]

# Znajdź miejsce dla studenta z oceną 4.2
idx = bisect.bisect_left(students, 4.2, key=lambda s: s.grade)
print(idx)  # 2 (między Janem a Kasią)

# Wstaw z zachowaniem porządku
bisect.insort(students, Student("Ewa", 4.2), key=lambda s: s.grade)
print([s.name for s in students])  # ['Anna', 'Jan', 'Ewa', 'Kasia', 'Marek']
```

---

### 3.5 Praktyczne wzorce zastosowań

#### Klasyfikacja do przedziałów (grade bucketing)

```python
import bisect

def letter_grade(score):
    breakpoints = [60, 70, 80, 90]
    grades = ['F', 'D', 'C', 'B', 'A']
    return grades[bisect.bisect(breakpoints, score)]

print(letter_grade(55))   # F
print(letter_grade(72))   # C
print(letter_grade(91))   # A
```

#### Znajdowanie zakresu duplikatów

```python
import bisect

arr = [1, 2, 4, 4, 4, 4, 7, 8, 9]

# Ile razy występuje wartość 4?
left = bisect.bisect_left(arr, 4)   # 2  (pierwszy indeks z 4)
right = bisect.bisect_right(arr, 4)  # 6  (pierwszy indeks ZA 4)
count = right - left                 # 4
print(f"Wartość 4 występuje {count} razy, na indeksach [{left}:{right})")
```

#### Utrzymywanie posortowanej listy w czasie rzeczywistym

```python
import bisect

sorted_events = []

# Nowe wydarzenia wstawiane z zachowaniem porządku
for timestamp in [1500, 1200, 1800, 1350, 1600]:
    bisect.insort(sorted_events, timestamp)

print(sorted_events)  # [1200, 1350, 1500, 1600, 1800]
```

**Kiedy używać modułu `bisect`?** 
- W każdym rozwiązaniu produkcyjnym w Pythonie oraz na większości zadań programistycznych, gdzie ręczna implementacja nie jest celem samym w sobie, a jedynie narzędziem optymalizacji.
- Do utrzymywania posortowanych list (`insort`), klasyfikacji wartości do przedziałów, zliczania elementów w zakresach i szybkiego wyszukiwania w posortowanych danych.

---

## Podsumowanie i linki

| Wersja | Co zwraca | Złożoność Czas. | Złożoność Pamięć. | Kiedy używać |
|---|---|---|---|---|
| **Iteracyjna** | Wartość `int` | $O(\log n)$ | $O(1)$ | Zawsze, jeśli ręcznie piszesz algorytm na rozmowie kwalifikacyjnej. |
| **Rekurencyjna** | Wartość `int` | $O(\log n)$ | $O(\log n)$ | Dla nauki poprawnego modelowania podziałów algorytmicznych (Divide & Conquer). |
| **Moduł `bisect`** | Wartość `int` | $O(\log n)$ | $O(1)$ | Szybki kod produkcyjny bez konieczności tworzenia powtarzalnej logiki. |

**Powiązane tematy (Algorytmy i struktury w Pythonie):**
- [Implementacje silni](implementacje-silni.md)
- [Implementacje ciągu Fibonacci](implementacje-ciagu-fibonacci.md)
