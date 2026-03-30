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

**Kiedy używać?** 
- W każdym rozwiązaniu produkcyjnym w Pythonie oraz na większości zadań programistycznych, gdzie ręczna implementacja nie jest celem samym w sobie, a jedynie narzędziem optymalizacji. Moduł `bisect` sprawdza się również świetnie do lokalizowania miejsca na wstawienie elementu (`bisect.insort`).

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
