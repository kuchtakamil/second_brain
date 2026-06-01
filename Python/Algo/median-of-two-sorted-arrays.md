# Mediana dwóch posortowanych tablic (Median of Two Sorted Arrays)

Jednym z klasycznych i zarazem najtrudniejszych problemów algorytmicznych (często oznaczanym jako "Hard" na platformie LeetCode) jest znalezienie mediany dwóch posortowanych tablic w czasie logarytmicznym.

**Treść problemu:**
Mając dwie posortowane tablice `nums1` i `nums2` o rozmiarach odpowiednio `m` i `n`, zwróć medianę tych dwóch posortowanych tablic. Całkowita złożoność czasowa musi wynosić $O(\log(m+n))$.

---

## Dlaczego ten problem jest ważny?

- Wymóg złożoności czasowej $O(\log(m+n))$ od razu sugeruje, że nie możemy scalić (ang. *merge*) tych dwóch tablic do jednej, co zajęłoby $O(m+n)$ czasu.
- Zamiast tego zmuszeni jesteśmy wykorzystać **wyszukiwanie binarne (Binary Search)** bezpośrednio na indeksach obu tablic.
- Stanowi to świetne sprawdzenie głębokiego zrozumienia wyszukiwania binarnego oraz umiejętności manipulowania przedziałami i warunkami brzegowymi (edge cases).

---

## Jak to działa (Rozwiązanie O(log(min(m, n))))

Idea opiera się na **podziale (ang. *partition*)**. Chcemy podzielić połączone tablice na dwie równe połówki: "lewą" (zawierającą mniejsze elementy) i "prawą" (zawierającą większe elementy). Jeśli nam się to uda i największy element z lewej połówki będzie mniejszy (lub równy) najmniejszemu z prawej, to mediana znajduje się na granicy tych połówek.

### Algorytm krok po kroku

1. **Ustalenie krótszej tablicy:** Zawsze wykonujemy wyszukiwanie binarne na mniejszej tablicy. Zmniejsza to przestrzeń poszukiwań do $O(\log(\min(m, n)))$, co jest jeszcze lepsze niż wymóg $O(\log(m+n))$. Załóżmy, że `nums1` (rozmiar `m`) jest krótsza niż `nums2` (rozmiar `n`). Jeśli nie, zamieniamy je.
2. **Definicja połowy długości:** Sumaryczna długość obu tablic to `total = m + n`. Lewa połowa połączonych tablic musi zawierać `half = (total + 1) // 2` elementów. (Dodanie 1 poprawnie obsługuje zarówno nieparzystą, jak i parzystą całkowitą liczbę elementów).
3. **Wyszukiwanie binarne (Binary Search):** 
   - Ustawiamy wskaźniki `left = 0` i `right = m` dla tablicy `nums1`.
   - W pętli wyliczamy podział: 
     - `i = (left + right) // 2` (ile elementów bierzemy z `nums1`)
     - `j = half - i` (ile elementów musimy dobrać z `nums2`)
4. **Sprawdzanie poprawności podziału:**
   Pobieramy wartości po lewej i prawej stronie podziału (lub `-inf` / `inf` dla przypadków brzegowych):
   - `nums1_left` = `nums1[i - 1]`
   - `nums1_right` = `nums1[i]`
   - `nums2_left` = `nums2[j - 1]`
   - `nums2_right` = `nums2[j]`

   Prawidłowy podział ma miejsce, gdy `nums1_left <= nums2_right` oraz `nums2_left <= nums1_right`.
5. **Korekta wskaźników:**
   - Jeśli `nums1_left > nums2_right`, wzięliśmy za dużo elementów z `nums1`, więc przesuwamy się w lewo: `right = i - 1`.
   - Jeśli `nums2_left > nums1_right`, wzięliśmy za mało elementów z `nums1`, więc przesuwamy się w prawo: `left = i + 1`.
6. **Obliczenie mediany po znalezieniu podziału:**
   - Jeśli `total` jest **nieparzyste**: mediana to największy element z lewej strony, czyli `max(nums1_left, nums2_left)`.
   - Jeśli `total` jest **parzyste**: mediana to średnia z największego z lewej strony i najmniejszego z prawej strony: `(max(nums1_left, nums2_left) + min(nums1_right, nums2_right)) / 2`.

---

## Przykładowa implementacja w Pythonie

```python
def findMedianSortedArrays(nums1: list[int], nums2: list[int]) -> float:
    # Zawsze wykonujemy binary search na krótszej tablicy
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1
        
    m, n = len(nums1), len(nums2)
    left, right = 0, m
    half_len = (m + n + 1) // 2
    is_even = (m + n) % 2 == 0
    
    while left <= right:
        i = (left + right) // 2   # podział w nums1
        j = half_len - i          # podział w nums2
        
        # Obsługa przypadków brzegowych (jeśli podział jest na krawędzi tablicy)
        nums1_left = nums1[i - 1] if i > 0 else float('-inf')
        nums1_right = nums1[i] if i < m else float('inf')
        
        nums2_left = nums2[j - 1] if j > 0 else float('-inf')
        nums2_right = nums2[j] if j < n else float('inf')
        
        # Sprawdzamy, czy znaleźliśmy poprawny podział
        if nums1_left <= nums2_right and nums2_left <= nums1_right:
            # Prawidłowy podział
            if not is_even:
                return float(max(nums1_left, nums2_left))
            else:
                return (max(nums1_left, nums2_left) + min(nums1_right, nums2_right)) / 2.0
                
        elif nums1_left > nums2_right:
            # Jesteśmy za daleko z prawej w nums1. Musimy przesunąć w lewo.
            right = i - 1
        else:
            # Jesteśmy za daleko z lewej w nums1. Musimy przesunąć w prawo.
            left = i + 1

    raise ValueError("Tablice nie są posortowane poprawnie.")
```

---

## Podsumowanie

Wymóg złożoności logarytmicznej w problemie Mediany Dwóch Posortowanych Tablic zmusza do szukania odpowiedniego podziału połączonych elementów bez ich fizycznego złączania. Zastosowanie Binary Search na długości krótszej tablicy pozwala optymalnie rozwiązać problem ze złożonością czasową $O(\log(\min(m, n)))$ i złożonością pamięciową $O(1)$.

**Powiązane tematy:**
- [Implementacje Binary Search](implementacje-binary-search.md)
