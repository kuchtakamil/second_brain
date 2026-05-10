# Top 10 algorytmów na studiach informatycznych

Poniżej zestawienie **10 najbardziej fundamentalnych algorytmów**, które poznaje się na typowych studiach informatycznych. To algorytmy, które pojawiają się w niemal każdym programie nauczania, na rozmowach rekrutacyjnych i w codziennej praktyce programistycznej.

---

## 1. Binary Search (wyszukiwanie binarne)

**Kategoria:** wyszukiwanie

Dziel tablicę (posortowaną!) na pół, porównuj element środkowy z szukanym i odrzucaj nieodpowiednią połówkę. Powtarzaj aż znajdziesz element lub wyczerpiesz zakres.

**Dlaczego jest ważny?**
- Złożoność $O(\log n)$ vs $O(n)$ w wyszukiwaniu liniowym.
- Fundament wielu technik optymalizacyjnych (np. binary search on answer).
- Stosowany w bazach danych, systemach plików, algorytmach kompresji.

**Złożoność:** $O(\log n)$ czasowa, $O(1)$ pamięciowa (iteracyjna) / $O(\log n)$ pamięciowa (rekurencyjna)

### 🔍 Wizualizacja (krok po kroku)

Szukamy wartości `10` w tablicy `[2, 3, 4, 10, 40]`:

```
Krok 1:  [2, 3, 4, 10, 40]    left=0, right=4, mid=2
          L     M         R    arr[2]=4 < 10 → szukaj w prawej połowie

Krok 2:  [2, 3, 4, 10, 40]    left=3, right=4, mid=3
                    L  M   R   arr[3]=10 == 10 → ZNALEZIONO ✅ (indeks 3)
```

Zamiast sprawdzać 5 elementów ($O(n)$), znaleźliśmy wynik w 2 krokach ($O(\log n)$).

### Implementacja iteracyjna (zalecana)

Podejście klasyczne z pętlą `while`. Najbardziej optymalne pamięciowo — brak narzutu stosu wywołań.

```python
def binary_search(arr: list[int], target: int) -> int:
    left = 0
    right = len(arr) - 1

    while left <= right:
        mid = (left + right) // 2

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1       # target jest w prawej połowie
        else:
            right = mid - 1      # target jest w lewej połowie

    return -1  # element nie znaleziony


# Usage:
nums = [2, 3, 4, 10, 40]
print(binary_search(nums, 10))   # 3
print(binary_search(nums, 5))    # -1
print(binary_search(nums, 2))    # 0
print(binary_search(nums, 40))   # 4
```

> [!IMPORTANT]
> Warunek `left <= right` (z `=`) jest kluczowy — bez niego pominiemy przypadek, gdy `left == right` i element jest właśnie na tej pozycji.

### Implementacja rekurencyjna

Podejście divide and conquer z jawnym przekazywaniem granic przedziału:

```python
def binary_search_recursive(arr: list[int], target: int, left: int, right: int) -> int:
    if left > right:
        return -1  # base case: przedział pusty

    mid = (left + right) // 2

    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, right)
    else:
        return binary_search_recursive(arr, target, left, mid - 1)


# Usage:
nums = [2, 3, 4, 10, 40]
print(binary_search_recursive(nums, 10, 0, len(nums) - 1))   # 3
print(binary_search_recursive(nums, 5, 0, len(nums) - 1))    # -1
```

> [!WARNING]
> Wersja rekurencyjna zużywa $O(\log n)$ pamięci na stos wywołań i może rzucić `RecursionError` dla bardzo dużych tablic. W produkcji preferuj wersję iteracyjną.

### Wersja z modułem `bisect` (produkcyjna)

Python ma wbudowany moduł `bisect` — implementacja w C, najszybsza opcja:

```python
import bisect

def binary_search_bisect(arr: list[int], target: int) -> int:
    index = bisect.bisect_left(arr, target)
    if index != len(arr) and arr[index] == target:
        return index
    return -1


# Usage:
nums = [2, 3, 4, 10, 40]
print(binary_search_bisect(nums, 10))  # 3
print(binary_search_bisect(nums, 5))   # -1
```

### Podsumowanie Binary Search

| Wersja | Złożoność czas. | Złożoność pamięć. | Kiedy używać |
|---|---|---|---|
| Iteracyjna | $O(\log n)$ | $O(1)$ | Rozmowa rekrutacyjna, produkcja |
| Rekurencyjna | $O(\log n)$ | $O(\log n)$ | Nauka divide & conquer |
| `bisect` | $O(\log n)$ | $O(1)$ | Kod produkcyjny w Pythonie |

📎 Pełny artykuł: [Implementacje Binary Search](implementacje-binary-search.md)

---

## 2. Algorytmy sortowania: Merge Sort i Quick Sort

**Kategoria:** sortowanie

Dwa flagowe algorytmy sortowania o złożoności $O(n \log n)$, oparte na strategii **divide and conquer**:

- **Merge Sort** — dzieli tablicę na połowy, sortuje rekurencyjnie, scala wyniki. Stabilny, zawsze $O(n \log n)$, ale wymaga dodatkowej pamięci $O(n)$.
- **Quick Sort** — wybiera pivot, dzieli elementy na mniejsze i większe, sortuje rekurencyjnie. W praktyce najszybszy, ale w najgorszym przypadku $O(n^2)$.

**Dlaczego są ważne?**
- Sortowanie to najczęstsza operacja w informatyce — zrozumienie *jak* i *dlaczego* działa jest kluczowe.
- Uczą strategii divide and conquer, rekurencji i analizy złożoności.
- `sorted()` w Pythonie używa TimSort — hybrydy Merge Sort i Insertion Sort.

---

### Merge Sort

#### 🔍 Wizualizacja (krok po kroku)

Sortujemy tablicę `[38, 27, 43, 3, 9, 82, 10]`:

```
                 [38, 27, 43, 3, 9, 82, 10]          ← dziel
                /                           \
        [38, 27, 43, 3]              [9, 82, 10]
        /            \                /         \
    [38, 27]      [43, 3]        [9, 82]      [10]
    /     \       /     \        /     \         |
  [38]   [27]  [43]   [3]     [9]   [82]      [10]   ← base case (1 element)
    \     /       \     /        \     /         |
    [27, 38]      [3, 43]       [9, 82]        [10]   ← scalaj (merge)
        \            /                \         /
        [3, 27, 38, 43]              [9, 10, 82]
                \                       /
           [3, 9, 10, 27, 38, 43, 82]                 ← wynik ✅
```

**Kluczowa idea:** dziel tablicę na pół aż do elementów pojedynczych, potem scalaj posortowane połówki. Cała „magia" dzieje się w kroku **merge**.

#### Szczegóły operacji merge

```
Scalanie [27, 38] i [3, 43]:

  left:  [27, 38]     right: [3, 43]     result: []
          i=0                  j=0

  Krok 1: 27 vs 3  → 3 mniejsze       result: [3]         j=1
  Krok 2: 27 vs 43 → 27 mniejsze      result: [3, 27]     i=1
  Krok 3: 38 vs 43 → 38 mniejsze      result: [3, 27, 38] i=2
  Krok 4: left wyczerpana → dopisz 43  result: [3, 27, 38, 43] ✅
```

#### Implementacja

```python
def merge_sort(arr: list[int]) -> list[int]:
    # base case: tablica 0- lub 1-elementowa jest posortowana
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])     # sortuj lewą połowę
    right = merge_sort(arr[mid:])    # sortuj prawą połowę

    return merge(left, right)


def merge(left: list[int], right: list[int]) -> list[int]:
    result = []
    i = j = 0

    # porównuj elementy z obu list i dodawaj mniejszy
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:      # <= zapewnia stabilność sortowania
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # dopisz pozostałe elementy (jedna z list jest już wyczerpana)
    result.extend(left[i:])
    result.extend(right[j:])

    return result


# Usage:
nums = [38, 27, 43, 3, 9, 82, 10]
print(merge_sort(nums))  # [3, 9, 10, 27, 38, 43, 82]

# Test stabilności — elementy o tej samej wartości zachowują kolejność
print(merge_sort([5, 2, 5, 1]))  # [1, 2, 5, 5]
print(merge_sort([]))             # []
print(merge_sort([1]))            # [1]
```

> [!TIP]
> **Stabilność** oznacza, że elementy o równych wartościach zachowują swoją oryginalną kolejność. Merge Sort jest stabilny dzięki warunkowi `<=` w porównaniu. Quick Sort **nie jest** stabilny.

#### Złożoność Merge Sort

| | Wartość | Dlaczego |
|---|---|---|
| **Czasowa (zawsze)** | $O(n \log n)$ | $\log n$ poziomów podziału × $O(n)$ scalanie na każdym poziomie |
| **Pamięciowa** | $O(n)$ | Tworzymy nowe listy przy każdym scalaniu |

---

### Quick Sort

#### 🔍 Wizualizacja (krok po kroku)

Sortujemy `[10, 7, 8, 9, 1, 5]` z pivotem = ostatni element:

```
[10, 7, 8, 9, 1, 5]     pivot = 5
                          ↓ partition: elementy ≤5 | pivot | elementy >5
[1, 5, 8, 9, 10, 7]     pivot 5 na pozycji 1
 ↓                ↓
[1]    5    [8, 9, 10, 7]     pivot = 7
             ↓ partition
        [7, 9, 10, 8]         pivot 7 na pozycji 0
         ↓         ↓
         7   [9, 10, 8]       pivot = 8
               ↓ partition
             [8, 10, 9]       pivot 9 na pozycji 1 (relatywnie)
              ↓     ↓
             [8]  9  [10]

Wynik: [1, 5, 7, 8, 9, 10] ✅
```

**Kluczowa idea:** wybierz **pivot**, podziel tablicę na elementy mniejsze i większe od pivota (partition), rekurencyjnie sortuj obie części. Pivot po partycji trafia na swoją docelową pozycję.

#### Czym jest partycja (Partition)?

Partycja to serce algorytmu Quick Sort. Jej zadaniem jest:
1. Wybrać element jako **pivot** (punkt odniesienia).
2. Przeorganizować tablicę tak, aby wszystkie elementy $\le$ pivot znalazły się po jego lewej stronie, a $>$ pivot po prawej.
3. Umieścić pivot na jego **ostatecznym, posortowanym miejscu**.
4. Zwrócić indeks pivota, by algorytm główny wiedział, gdzie podzielić tablicę na lewą i prawą część.

#### Szczegóły operacji partition (schemat Lomuto)

```
arr = [10, 7, 8, 9, 1, 5]    pivot = arr[5] = 5
                               i = -1  (granica "małych" elementów)

j=0: arr[0]=10 > 5  → nic
j=1: arr[1]=7  > 5  → nic
j=2: arr[2]=8  > 5  → nic
j=3: arr[3]=9  > 5  → nic
j=4: arr[4]=1  ≤ 5  → i=0, swap arr[0]↔arr[4] → [1, 7, 8, 9, 10, 5]

Koniec pętli: swap arr[i+1]↔arr[high] → swap arr[1]↔arr[5]
Wynik: [1, 5, 8, 9, 10, 7]    pivot_index = 1
        ≤5  pivot    >5
```

#### Implementacja (in-place, schemat Lomuto)

```python
def quick_sort(arr: list[int], low: int = 0, high: int | None = None) -> None:
    if high is None:
        high = len(arr) - 1

    if low < high:
        pivot_index = partition(arr, low, high)
        quick_sort(arr, low, pivot_index - 1)     # sortuj lewą część
        quick_sort(arr, pivot_index + 1, high)     # sortuj prawą część


def partition(arr: list[int], low: int, high: int) -> int:
    pivot = arr[high]     # pivot = ostatni element
    i = low - 1           # granica "małych" elementów

    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]   # swap mniejszego na lewą stronę

    # umieść pivot na właściwej pozycji
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


# Usage:
nums = [10, 7, 8, 9, 1, 5]
quick_sort(nums)
print(nums)  # [1, 5, 7, 8, 9, 10]

nums2 = [38, 27, 43, 3, 9, 82, 10]
quick_sort(nums2)
print(nums2)  # [3, 9, 10, 27, 38, 43, 82]
```

> [!IMPORTANT]
> Quick Sort sortuje **in-place** (modyfikuje oryginalną tablicę) — nie zwraca nowej listy. To kluczowa różnica w porównaniu z Merge Sort.

#### Implementacja iteracyjna (in-place)

Aby pozbyć się rekurencji (i ryzyka `RecursionError`), możemy użyć jawnego stosu do zapamiętywania indeksów podtablic do posortowania. Złożoność pamięciowa to wciąż $O(\log n)$ ze względu na rozmiar stosu, a algorytm operuje in-place.

```python
def quick_sort_iterative(arr: list[int]) -> None:
    if len(arr) <= 1:
        return
        
    # Stos przechowuje pary indeksów (low, high)
    stack = [(0, len(arr) - 1)]
    
    while stack:
        low, high = stack.pop()
        
        if low < high:
            # Używamy tej samej funkcji partition co wyżej
            pivot_index = partition(arr, low, high)
            
            # Wrzucamy na stos prawą i lewą część
            stack.append((low, pivot_index - 1))
            stack.append((pivot_index + 1, high))

# Usage:
nums3 = [10, 7, 8, 9, 1, 5]
quick_sort_iterative(nums3)
print(nums3)  # [1, 5, 7, 8, 9, 10]
```

#### Wersja uproszczona (pythonic, nie in-place)

Prostsza do zrozumienia, ale tworzy nowe listy (traci przewagę pamięciową):

```python
def quick_sort_simple(arr: list[int]) -> list[int]:
    if len(arr) <= 1:
        return arr

    pivot = arr[-1]
    left = [x for x in arr[:-1] if x <= pivot]
    right = [x for x in arr[:-1] if x > pivot]

    return quick_sort_simple(left) + [pivot] + quick_sort_simple(right)


# Usage:
print(quick_sort_simple([10, 7, 8, 9, 1, 5]))   # [1, 5, 7, 8, 9, 10]
print(quick_sort_simple([3, 1, 4, 1, 5, 9, 2]))  # [1, 1, 2, 3, 4, 5, 9]
```

> [!WARNING]
> Wersja uproszczona jest $O(n)$ pamięciowo i nie jest prawdziwym Quick Sortem (traci in-place). Używaj jej tylko do nauki — na rozmowie rekrutacyjnej pokaż wersję in-place z partycją.

#### Złożoność Quick Sort

| | Wartość | Kiedy |
|---|---|---|
| **Czasowa (średnia)** | $O(n \log n)$ | Pivot dzieli tablicę mniej więcej równomiernie |
| **Czasowa (najgorsza)** | $O(n^2)$ | Pivot jest zawsze min lub max (np. posortowana tablica!) |
| **Pamięciowa** | $O(\log n)$ | Stos rekurencji (in-place — nie alokuje dodatkowych tablic) |

#### Strategie wyboru pivota

Największą bolączką Quick Sorta jest to, co się stanie, gdy wybierzemy "zły" pivot (co prowadzi do koszmarnej złożoności $O(n^2)$). Istnieje kilka strategii, jak tego uniknąć:

1. **Ostatni / Pierwszy element (Naiwna):** Domyślne podejście w schemacie Lomuto. Łatwe do implementacji, ale bardzo podatne na najgorszy przypadek (gdy tablica jest już posortowana).
2. **Median-of-three (Mediana z trzech):** Wybieramy pierwszy, środkowy i ostatni element, i jako pivot bierzemy ich medianę (wartość środkową). Trik ten niemal całkowicie eliminuje $O(n^2)$ w praktyce (dla posortowanych lub częściowo posortowanych tablic).
3. **Randomized pivot (Losowy):** Losujemy dowolny indeks z przedziału `[low, high]` i zamieniamy z ostatnim elementem przed wykonaniem partycji. Skutecznie uodparnia algorytm na pesymistyczne, spreparowane złośliwie dane wejściowe.
4. **Mediana z median (Magiczne piątki):** Deterministyczny algorytm, który matematycznie gwarantuje, że podział będzie proporcjonalny, zapewniając sztywne $O(n \log n)$. W praktyce ma jednak spory narzut obliczeniowy i rzadko używa się go poza teorią.

---

### Merge Sort vs Quick Sort

| Cecha | Merge Sort | Quick Sort |
|---|---|---|
| Złożoność (średnia) | $O(n \log n)$ | $O(n \log n)$ |
| Złożoność (najgorsza) | $O(n \log n)$ ✅ | $O(n^2)$ ❌ |
| Pamięć dodatkowa | $O(n)$ ❌ | $O(\log n)$ ✅ |
| Stabilność | ✅ Stabilny | ❌ Niestabilny |
| In-place | ❌ Nie | ✅ Tak |
| Cache-friendliness | Gorsza (alokacje) | Lepsza (sekwencyjny dostęp) |
| W praktyce szybszy? | Nie | **Tak** (mniejszy stały czynnik) |

**Kiedy który wybrać?**
- **Merge Sort** → gdy potrzebujesz stabilności lub gwarancji $O(n \log n)$ (np. sortowanie linked list, external sort).
- **Quick Sort** → domyślny wybór w większości przypadków (sortuje in-place, szybszy w praktyce).
- **Python `sorted()`** → TimSort (hybryda Merge + Insertion Sort) — najlepszy wybór produkcyjny.

---

## 3. BFS (Breadth-First Search)

**Kategoria:** przeszukiwanie grafów

Przeszukiwanie grafu **wszerz** — eksploruje wierzchołki warstwa po warstwie, zaczynając od źródła. Używa kolejki (FIFO).

**Dlaczego jest ważny?**
- Gwarantuje najkrótszą ścieżkę w grafie nieważonym.
- Podstawa algorytmów sieciowych (np. routing).
- Stosowany w: najkrótsza ścieżka na gridzie, level-order traversal drzew, web crawling.

**Złożoność:** $O(V + E)$ czasowa, $O(V)$ pamięciowa

### 🔍 Wizualizacja (krok po kroku)

Graf (lista sąsiedztwa) — start z wierzchołka `A`:

```
    A --- B --- E
    |     |
    C --- D --- F
```

```
Kolejka (FIFO)          Visited                 Warstwa

[A]                     {A}                     0
 ↓ zdejmij A, dodaj sąsiadów B, C
[B, C]                  {A, B, C}               1
 ↓ zdejmij B, dodaj sąsiadów E, D (A już visited)
[C, E, D]               {A, B, C, E, D}         1→2
 ↓ zdejmij C, dodaj sąsiadów D (już visited)
[E, D]                  {A, B, C, E, D}         2
 ↓ zdejmij E (brak nowych sąsiadów)
[D]                     {A, B, C, E, D}         2
 ↓ zdejmij D, dodaj F
[F]                     {A, B, C, E, D, F}      3
 ↓ zdejmij F
[]                      {A, B, C, E, D, F}      3 ✅

Kolejność odwiedzin: A → B → C → E → D → F
```

**Kluczowa obserwacja:** BFS odwiedza **wszystkie wierzchołki w odległości $k$** zanim przejdzie do odległości $k+1$. Dlatego pierwszy raz, gdy dotrzemy do celu, mamy gwarancję najkrótszej ścieżki.

### Implementacja na liście sąsiedztwa

Najbardziej ogólna forma BFS — graf reprezentowany jako `dict[str, list[str]]`:

```python
from collections import deque


def bfs(graph: dict[str, list[str]], start: str) -> list[str]:
    visited = set()
    visited.add(start)
    queue = deque([start])
    order = []                    # kolejność odwiedzin

    while queue:
        node = queue.popleft()    # FIFO — zdejmij z przodu
        order.append(node)

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)       # oznacz PRZED wrzuceniem do kolejki
                queue.append(neighbor)

    return order


# Usage:
graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'D'],
    'D': ['B', 'C', 'F'],
    'E': ['B'],
    'F': ['D'],
}

print(bfs(graph, 'A'))  # ['A', 'B', 'C', 'D', 'E', 'F']
```

> [!IMPORTANT]
> Wierzchołek dodajemy do `visited` **w momencie wkładania do kolejki**, nie przy wyjmowaniu. Zapobiega to duplikatom w kolejce i poprawia wydajność.

### Najkrótsza ścieżka (BFS + śledzenie dystansu)

BFS naturalnie znajduje najkrótszą ścieżkę w grafie nieważonym. Wystarczy śledzić dystans i rodzica:

```python
from collections import deque


def bfs_shortest_path(graph: dict[str, list[str]], start: str, target: str) -> list[str]:
    visited = set()
    visited.add(start)
    queue = deque([(start, [start])])   # (wierzchołek, ścieżka do niego)

    while queue:
        node, path = queue.popleft()

        if node == target:
            return path                  # pierwsza znaleziona = najkrótsza

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    return []  # brak ścieżki


# Usage:
graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'D'],
    'D': ['B', 'C', 'F'],
    'E': ['B'],
    'F': ['D'],
}

print(bfs_shortest_path(graph, 'A', 'F'))  # ['A', 'B', 'D', 'F']
print(bfs_shortest_path(graph, 'A', 'E'))  # ['A', 'B', 'E']
print(bfs_shortest_path(graph, 'E', 'F'))  # ['E', 'B', 'D', 'F']
```

```
Wizualizacja najkrótszej ścieżki A → F:

    A --- B --- E          Ścieżka: A → B → D → F
    |     |                Dystans: 3
    C --- D --- F
    ·  ·  ·     ·
    A ──→ B ──→ D ──→ F    (BFS gwarantuje minimum)
```

### BFS na gridzie (2D)

BFS świetnie sprawdza się na siatkach 2D — każda komórka to wierzchołek, 4 sąsiedzi to krawędzie:

```python
from collections import deque


def bfs_grid(grid: list[list[str]], start: tuple[int, int], target: tuple[int, int]) -> int:
    rows, cols = len(grid), len(grid[0])
    visited = set()
    visited.add(start)
    queue = deque([(start[0], start[1], 0)])   # (row, col, dystans)

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]   # ↑ ↓ ← →

    while queue:
        row, col, dist = queue.popleft()

        if (row, col) == target:
            return dist

        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if (0 <= nr < rows and 0 <= nc < cols
                    and (nr, nc) not in visited
                    and grid[nr][nc] == '.'):
                visited.add((nr, nc))
                queue.append((nr, nc, dist + 1))

    return -1   # cel nieosiągalny


# Usage:
grid = [
    ['.', '.', '#', '.'],
    ['.', '#', '.', '.'],
    ['.', '.', '.', '#'],
    ['#', '.', '.', '.'],
]

print(bfs_grid(grid, (0, 0), (3, 3)))  # 5
print(bfs_grid(grid, (0, 0), (0, 3)))  # -1 (zablokowane)
```

```
Grid:                    BFS od (0,0) do (3,3):

.  .  #  .               0  1  #  .
.  #  .  .               1  #  .  .
.  .  .  #               2  3  4  #
#  .  .  .               #  4  5  5 ← dystans

Najkrótsza ścieżka: 5 kroków
```

### Level-order traversal drzewa (BFS na drzewie)

BFS na drzewie binarnym = przechodzenie **poziom po poziomie**:

```python
from collections import deque


class TreeNode:
    def __init__(self, val: int, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def level_order(root: TreeNode | None) -> list[list[int]]:
    if not root:
        return []

    result = []
    queue = deque([root])

    while queue:
        level_size = len(queue)        # ile węzłów na tym poziomie
        level = []

        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        result.append(level)

    return result


# Usage:
#       3
#      / \
#     9   20
#        /  \
#       15    7

tree = TreeNode(3,
    TreeNode(9),
    TreeNode(20, TreeNode(15), TreeNode(7))
)

print(level_order(tree))  # [[3], [9, 20], [15, 7]]
```

```
Drzewo:         Level-order:

     3          Poziom 0: [3]
    / \         Poziom 1: [9, 20]
   9   20       Poziom 2: [15, 7]
      / \
    15    7     Wynik: [[3], [9, 20], [15, 7]]
```

### Podsumowanie BFS

| Wariant | Zastosowanie | Złożoność |
|---|---|---|
| BFS na grafie | Traversal, spójne składowe | $O(V + E)$ |
| BFS + ścieżka | Najkrótsza ścieżka (nieważony) | $O(V + E)$ |
| BFS na gridzie | Labirynt, flood-fill, shortest path 2D | $O(R \times C)$ |
| Level-order | Przechodzenie drzewa poziomami | $O(n)$ |

> [!TIP]
> **Kiedy BFS, a kiedy DFS?**
> - **BFS** → najkrótsza ścieżka, przechodzenie warstwami, gdy cel jest blisko startu.
> - **DFS** → odwiedzenie całego komponentu, wykrywanie cykli, backtracking (patrz sekcja 4).

📎 Pełny artykuł: [BFS i DFS na gridzie](bfs-dfs-na-gridzie.md)

---

## 4. DFS (Depth-First Search)

**Kategoria:** przeszukiwanie grafów

Przeszukiwanie grafu **w głąb** — podąża jedną ścieżką tak daleko jak to możliwe, potem się cofa (backtracking). Używa stosu (jawnego lub rekurencji).

**Dlaczego jest ważny?**
- Fundament wielu algorytmów grafowych (topological sort, wykrywanie cykli, SCC).
- Naturalny dla problemów z backtrackingiem (sudoku, n-queens, generowanie permutacji).
- Prostszy w implementacji niż BFS (rekurencja).

**Złożoność:** $O(V + E)$ czasowa, $O(V)$ pamięciowa

### 🔍 Wizualizacja (krok po kroku)

Ten sam graf co w BFS — ale teraz DFS idzie **w głąb**, nie wszerz:

```
    A --- B --- E
    |     |
    C --- D --- F
```

```
Stos (LIFO)             Visited                 Ścieżka

push A
[A]                     {A}
 ↓ zdejmij A, push sąsiadów C, B
[C, B]                  {A, B, C}               A
 ↓ zdejmij B, push sąsiadów E, D (A już visited)
[C, E, D]               {A, B, C, E, D}         A → B
 ↓ zdejmij D, push F (B,C już visited)
[C, E, F]               {A, B, C, E, D, F}      A → B → D
 ↓ zdejmij F (brak nowych sąsiadów)
[C, E]                  {A, B, C, E, D, F}      A → B → D → F
 ↓ zdejmij E (brak nowych sąsiadów)
[C]                     {A, B, C, E, D, F}      A → B → D → F → E
 ↓ zdejmij C (sąsiedzi A,D już visited)
[]                      {A, B, C, E, D, F}      A → B → D → F → E → C ✅

Kolejność odwiedzin: A → B → D → F → E → C
```

**Kluczowa różnica vs BFS:** DFS „wchodzi w głąb" jednej gałęzi zanim wróci do rozwidlenia. Nie gwarantuje najkrótszej ścieżki, ale zużywa mniej pamięci (tylko aktualna gałąź na stosie).

### Implementacja rekurencyjna

Najprostsza i najczytelniejsza forma DFS — stos wywołań pełni rolę jawnego stosu:

```python
def dfs_recursive(graph: dict[str, list[str]], node: str, visited: set | None = None) -> list[str]:
    if visited is None:
        visited = set()

    visited.add(node)
    order = [node]

    for neighbor in graph[node]:
        if neighbor not in visited:
            order.extend(dfs_recursive(graph, neighbor, visited))

    return order


# Usage:
graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'D'],
    'D': ['B', 'C', 'F'],
    'E': ['B'],
    'F': ['D'],
}

print(dfs_recursive(graph, 'A'))  # ['A', 'B', 'D', 'C', 'F', 'E']
```

> [!WARNING]
> Rekurencja w Pythonie ma domyślny limit 1000 wywołań (`sys.getrecursionlimit()`). Dla dużych grafów użyj wersji iteracyjnej.

### Implementacja iteracyjna (z jawnym stosem)

Bezpieczna dla dużych grafów — brak ryzyka `RecursionError`:

```python
def dfs_iterative(graph: dict[str, list[str]], start: str) -> list[str]:
    visited = set()
    stack = [start]
    order = []

    while stack:
        node = stack.pop()          # LIFO — zdejmij z góry

        if node in visited:
            continue
        visited.add(node)
        order.append(node)

        # dodaj sąsiadów w odwróconej kolejności (żeby pierwszy sąsiad
        # znalazł się na szczycie stosu i był przetworzony jako pierwszy)
        for neighbor in reversed(graph[node]):
            if neighbor not in visited:
                stack.append(neighbor)

    return order


# Usage:
graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'D'],
    'D': ['B', 'C', 'F'],
    'E': ['B'],
    'F': ['D'],
}

print(dfs_iterative(graph, 'A'))  # ['A', 'B', 'D', 'C', 'F', 'E']
```

> [!IMPORTANT]
> W iteracyjnym DFS `visited` sprawdzamy przy **zdejmowaniu ze stosu** (nie przy wkładaniu), bo na stos mogą trafić duplikaty tego samego wierzchołka. Alternatywnie — dodawaj do `visited` przy wkładaniu, ale wtedy kolejność odwiedzin będzie inna.

### Wykrywanie cykli (graf skierowany)

Jednym z kluczowych zastosowań DFS jest wykrywanie cykli. Używamy trzech stanów wierzchołka:

```
WHITE (0) = nieodwiedzony
GRAY  (1) = w trakcie przetwarzania (na stosie rekurencji)
BLACK (2) = przetworzony (wszystkie potomki sprawdzone)

Cykl istnieje ⟺ natrafimy na wierzchołek GRAY (wracamy do węzła, który jest jeszcze na stosie)
```

```python
def has_cycle(graph: dict[str, list[str]]) -> bool:
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {node: WHITE for node in graph}

    def dfs(node: str) -> bool:
        color[node] = GRAY              # zaczynamy przetwarzanie

        for neighbor in graph[node]:
            if color[neighbor] == GRAY:  # cykl! wracamy do węzła w trakcie
                return True
            if color[neighbor] == WHITE:
                if dfs(neighbor):
                    return True

        color[node] = BLACK              # zakończono przetwarzanie
        return False

    # sprawdź każdy komponent (graf może być niespójny)
    for node in graph:
        if color[node] == WHITE:
            if dfs(node):
                return True

    return False


# Usage:
# Graf acykliczny (DAG):
dag = {
    'A': ['B', 'C'],
    'B': ['D'],
    'C': ['D'],
    'D': [],
}
print(has_cycle(dag))  # False

# Graf z cyklem A → B → D → A:
cyclic = {
    'A': ['B'],
    'B': ['C', 'D'],
    'C': [],
    'D': ['A'],        # ← krawędź powrotna → cykl
}
print(has_cycle(cyclic))  # True
```

```
Wizualizacja cyklu:

DAG (brak cyklu):           Graf z cyklem:

A → B → D                  A → B → D
  ↘   ↗                         ↓   ↑
    C                            C   |
                                 └───┘  ← back edge (D → A)
```

### Number of Islands (DFS na gridzie)

Klasyczny problem: policz liczbę wysp (`'1'` = ląd, `'0'` = woda). DFS oznacza całą wyspę jako odwiedzoną:

```python
def num_islands(grid: list[list[str]]) -> int:
    if not grid:
        return 0

    rows, cols = len(grid), len(grid[0])
    visited = set()
    count = 0

    def dfs(row: int, col: int) -> None:
        # warunki stopu: poza granicami, woda, lub już odwiedzone
        if (row < 0 or row >= rows or col < 0 or col >= cols
                or grid[row][col] == '0' or (row, col) in visited):
            return

        visited.add((row, col))
        dfs(row - 1, col)   # ↑
        dfs(row + 1, col)   # ↓
        dfs(row, col - 1)   # ←
        dfs(row, col + 1)   # →

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1' and (r, c) not in visited:
                dfs(r, c)    # oznacz całą wyspę
                count += 1

    return count


# Usage:
grid = [
    ['1', '1', '0', '0', '0'],
    ['1', '1', '0', '0', '0'],
    ['0', '0', '1', '0', '0'],
    ['0', '0', '0', '1', '1'],
]
print(num_islands(grid))  # 3
```

```
Grid:                Wyspy:

1 1 0 0 0            ① ① .  .  .
1 1 0 0 0            ① ① .  .  .
0 0 1 0 0            .  .  ② .  .
0 0 0 1 1            .  .  .  ③ ③

DFS startuje 3 razy → 3 wyspy
```

### Podsumowanie DFS

| Wariant | Zastosowanie | Złożoność |
|---|---|---|
| DFS rekurencyjny | Traversal, spójne składowe | $O(V + E)$ |
| DFS iteracyjny | Duże grafy (bez RecursionError) | $O(V + E)$ |
| Wykrywanie cykli | Walidacja DAG, dependency graphs | $O(V + E)$ |
| DFS na gridzie | Wyspy, flood-fill, labirynty | $O(R \times C)$ |

### BFS vs DFS — kiedy co wybrać?

| Kryterium | BFS | DFS |
|---|---|---|
| Najkrótsza ścieżka | ✅ Gwarantuje | ❌ Nie gwarantuje |
| Pamięć | Cała warstwa w kolejce | Tylko aktualna gałąź |
| Cel blisko startu | ✅ Szybko znajdzie | ❌ Może iść daleko |
| Cel daleko / cały graf | Wolniejszy | ✅ Naturalny |
| Wykrywanie cykli | Możliwe, ale trudniejsze | ✅ Naturalne (WHITE/GRAY/BLACK) |
| Topological sort | Algorytm Kahna (BFS) | ✅ Algorytm Tarjana (DFS) |
| Backtracking | ❌ | ✅ Naturalne podejście |

📎 Pełny artykuł: [BFS i DFS na gridzie](bfs-dfs-na-gridzie.md)

---

## 5. Algorytm Dijkstry

**Kategoria:** najkrótsza ścieżka (graf ważony)

Znajduje najkrótszą ścieżkę z jednego źródła do wszystkich pozostałych wierzchołków w grafie z **nieujemnymi** wagami. Używa kolejki priorytetowej (min-heap).

**Dlaczego jest ważny?**
- Algorytm nr 1 do najkrótszej ścieżki w grafach ważonych.
- Stosowany w GPS/nawigacji, routingu sieciowym, grach (pathfinding).
- Uczy strategii zachłannej (greedy) i pracy z kolejką priorytetową.

**Złożoność:** $O((V + E) \log V)$ z min-heap

### Jak działa? (intuicja)

Dijkstra to algorytm **zachłanny** (greedy). W każdym kroku:

1. Wybierz wierzchołek o **najmniejszym dotychczasowym dystansie** (stąd min-heap).
2. Dla każdego sąsiada sprawdź, czy przejście przez wybrany wierzchołek daje **krótszą ścieżkę** niż dotychczasowa (**relaksacja**).
3. Jeśli tak — zaktualizuj dystans i dodaj sąsiada do kolejki.

```
Relaksacja krawędzi (u → v, waga w):

Jeśli dist[u] + w < dist[v]:
    dist[v] = dist[u] + w     ← znaleźliśmy krótszą ścieżkę do v!
    prev[v] = u                ← zapamiętaj skąd przyszliśmy
```

> [!IMPORTANT]
> Dijkstra **nie działa** z ujemnymi wagami. Krawędź o wadze ujemnej może "unieważnić" wcześniej ustaloną najkrótszą ścieżkę. Do ujemnych wag użyj algorytmu **Bellman-Ford**.

### 🔍 Wizualizacja (krok po kroku)

Graf ważony — szukamy najkrótszych ścieżek z wierzchołka `A`:

```
        A
       / \
     (1)  (4)
     /     \
    B       C
    |      / \
   (2)   (1) (5)
    |   /     \
    D--       E
     \       /
     (3)  (2)
       \ /
        F
```

Lista sąsiedztwa (z wagami):
```
A: [(B,1), (C,4)]
B: [(A,1), (D,2)]
C: [(A,4), (D,1), (E,5)]
D: [(B,2), (C,1), (F,3)]
E: [(C,5), (F,2)]
F: [(D,3), (E,2)]
```

```
Krok 0 — inicjalizacja:
  dist = {A:0, B:∞, C:∞, D:∞, E:∞, F:∞}
  prev = {A:-, B:-, C:-, D:-, E:-, F:-}
  heap = [(0, A)]
  visited = {}

Krok 1 — zdejmij A (dist=0):
  → sąsiad B: dist[A]+1 = 1 < ∞    → dist[B]=1, prev[B]=A
  → sąsiad C: dist[A]+4 = 4 < ∞    → dist[C]=4, prev[C]=A
  dist = {A:0, B:1, C:4, D:∞, E:∞, F:∞}
  heap = [(1,B), (4,C)]
  visited = {A}

Krok 2 — zdejmij B (dist=1):       ← najniższy dystans w heap
  → sąsiad A: już visited, pomiń
  → sąsiad D: dist[B]+2 = 3 < ∞    → dist[D]=3, prev[D]=B
  dist = {A:0, B:1, C:4, D:3, E:∞, F:∞}
  heap = [(3,D), (4,C)]
  visited = {A, B}

Krok 3 — zdejmij D (dist=3):
  → sąsiad B: już visited, pomiń
  → sąsiad C: dist[D]+1 = 4 = 4    → nie lepsze, pomiń (≥ obecny dist)
  → sąsiad F: dist[D]+3 = 6 < ∞    → dist[F]=6, prev[F]=D
  dist = {A:0, B:1, C:4, D:3, E:∞, F:6}
  heap = [(4,C), (6,F)]
  visited = {A, B, D}

Krok 4 — zdejmij C (dist=4):
  → sąsiad A: już visited, pomiń
  → sąsiad D: już visited, pomiń
  → sąsiad E: dist[C]+5 = 9 < ∞    → dist[E]=9, prev[E]=C
  dist = {A:0, B:1, C:4, D:3, E:9, F:6}
  heap = [(6,F), (9,E)]
  visited = {A, B, D, C}

Krok 5 — zdejmij F (dist=6):
  → sąsiad D: już visited, pomiń
  → sąsiad E: dist[F]+2 = 8 < 9    → dist[E]=8, prev[E]=F  ← RELAKSACJA! ✅
  dist = {A:0, B:1, C:4, D:3, E:8, F:6}
  heap = [(8,E), (9,E)]              ← stary wpis (9,E) zostanie zignorowany
  visited = {A, B, D, C, F}

Krok 6 — zdejmij E (dist=8):
  → sąsiad C: już visited, pomiń
  → sąsiad F: już visited, pomiń
  dist = {A:0, B:1, C:4, D:3, E:8, F:6}  ← WYNIK KOŃCOWY ✅
  visited = {A, B, D, C, F, E}
```

**Odtworzenie ścieżki** (przez tablicę `prev`):

```
A → E:  prev[E]=F, prev[F]=D, prev[D]=B, prev[B]=A
        Ścieżka: A → B → D → F → E  (koszt: 8)

A → F:  prev[F]=D, prev[D]=B, prev[B]=A
        Ścieżka: A → B → D → F       (koszt: 6)

A → C:  prev[C]=A
        Ścieżka: A → C               (koszt: 4)
```

> [!TIP]
> Wierzchołek E początkowo miał dystans 9 (przez C), ale w kroku 5 został **zrelaksowany** do 8 (przez F). Dlatego w heap mogą znajdować się nieaktualne wpisy — ignorujemy je sprawdzając `visited`.

### Implementacja z min-heap (zalecana)

Standardowa implementacja z `heapq` — najefektywniejsza w Pythonie:

```python
import heapq


def dijkstra(graph: dict[str, list[tuple[str, int]]], start: str) -> dict[str, int]:
    # dystanse od startu do każdego wierzchołka (domyślnie nieskończoność)
    dist = {node: float('inf') for node in graph}
    dist[start] = 0

    # min-heap: (dystans, wierzchołek)
    heap = [(0, start)]

    # zbiór wierzchołków, dla których znamy najkrótszy dystans
    visited = set()

    while heap:
        current_dist, u = heapq.heappop(heap)

        # jeśli wierzchołek już przetworzony — pomiń (stary wpis w heap)
        if u in visited:
            continue
        visited.add(u)

        # relaksacja wszystkich krawędzi wychodzących z u
        for v, weight in graph[u]:
            if v not in visited:
                new_dist = current_dist + weight
                if new_dist < dist[v]:
                    dist[v] = new_dist
                    heapq.heappush(heap, (new_dist, v))

    return dist


# Usage:
graph = {
    'A': [('B', 1), ('C', 4)],
    'B': [('A', 1), ('D', 2)],
    'C': [('A', 4), ('D', 1), ('E', 5)],
    'D': [('B', 2), ('C', 1), ('F', 3)],
    'E': [('C', 5), ('F', 2)],
    'F': [('D', 3), ('E', 2)],
}

print(dijkstra(graph, 'A'))
# {'A': 0, 'B': 1, 'C': 4, 'D': 3, 'E': 8, 'F': 6}
```

> [!IMPORTANT]
> Sprawdzamy `if u in visited: continue` po zdjęciu z heap, ponieważ ten sam wierzchołek może trafić do heap wielokrotnie (z różnymi dystansami). Przetwarzamy go tylko raz — przy pierwszym zdjęciu (z najmniejszym dystansem).

### Dijkstra z odtwarzaniem ścieżki

Rozszerzona wersja śledząca **poprzednika** każdego wierzchołka — pozwala odtworzyć pełną ścieżkę:

```python
import heapq


def dijkstra_path(
    graph: dict[str, list[tuple[str, int]]],
    start: str,
    target: str,
) -> tuple[int, list[str]]:
    dist = {node: float('inf') for node in graph}
    dist[start] = 0
    prev = {node: None for node in graph}

    heap = [(0, start)]
    visited = set()

    while heap:
        current_dist, u = heapq.heappop(heap)

        if u in visited:
            continue
        visited.add(u)

        # early exit — dotarliśmy do celu
        if u == target:
            break

        for v, weight in graph[u]:
            if v not in visited:
                new_dist = current_dist + weight
                if new_dist < dist[v]:
                    dist[v] = new_dist
                    prev[v] = u
                    heapq.heappush(heap, (new_dist, v))

    # odtwarzanie ścieżki od target do start
    path = []
    node = target
    while node is not None:
        path.append(node)
        node = prev[node]
    path.reverse()

    # jeśli ścieżka nie zaczyna się od start → cel nieosiągalny
    if path[0] != start:
        return float('inf'), []

    return dist[target], path


# Usage:
graph = {
    'A': [('B', 1), ('C', 4)],
    'B': [('A', 1), ('D', 2)],
    'C': [('A', 4), ('D', 1), ('E', 5)],
    'D': [('B', 2), ('C', 1), ('F', 3)],
    'E': [('C', 5), ('F', 2)],
    'F': [('D', 3), ('E', 2)],
}

cost, path = dijkstra_path(graph, 'A', 'E')
print(f"Koszt: {cost}, Ścieżka: {' → '.join(path)}")
# Koszt: 8, Ścieżka: A → B → D → F → E

cost, path = dijkstra_path(graph, 'A', 'F')
print(f"Koszt: {cost}, Ścieżka: {' → '.join(path)}")
# Koszt: 6, Ścieżka: A → B → D → F
```

> [!TIP]
> Optymalizacja **early exit** (`if u == target: break`) — jeśli szukamy ścieżki do konkretnego wierzchołka, nie musimy eksplorować całego grafu. Algorytm gwarantuje, że przy pierwszym zdjęciu `target` z heap, jego dystans jest optymalny.

### Dijkstra na gridzie (2D z wagami)

Wariant na siatce 2D, gdzie komórki mają różne koszty przejścia (np. teren w grze):

```python
import heapq


def dijkstra_grid(
    grid: list[list[int]],
    start: tuple[int, int],
    target: tuple[int, int],
) -> int:
    rows, cols = len(grid), len(grid[0])
    dist = [[float('inf')] * cols for _ in range(rows)]
    dist[start[0]][start[1]] = grid[start[0]][start[1]]

    heap = [(grid[start[0]][start[1]], start[0], start[1])]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]   # ↑ ↓ ← →

    while heap:
        d, r, c = heapq.heappop(heap)

        if (r, c) == target:
            return d

        if d > dist[r][c]:    # stary wpis — pomiń
            continue

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                new_dist = d + grid[nr][nc]
                if new_dist < dist[nr][nc]:
                    dist[nr][nc] = new_dist
                    heapq.heappush(heap, (new_dist, nr, nc))

    return -1   # cel nieosiągalny


# Usage — każda komórka ma koszt przejścia:
grid = [
    [1, 3, 1, 2],
    [1, 5, 1, 1],
    [4, 2, 1, 3],
    [1, 1, 1, 1],
]

print(dijkstra_grid(grid, (0, 0), (3, 3)))  # 7
# Ścieżka: (0,0)→(1,0)→(0,0)... optymalnie: 1→1→3→1→1→1 = 7
```

```
Grid (koszty):               Najkrótszy dystans od (0,0):

1  3  1  2                   1  4  5  7
1  5  1  1                   2  7  6  7
4  2  1  3                   6  4  5  8
1  1  1  1                   7  5  6  7 ← dist[3][3] = 7 ✅

Optymalna ścieżka (jedna z możliwych):
(0,0) → (1,0) → (2,0)? Nie! Dijkstra znajdzie:
(0,0)→(1,0)→(2,1)→(2,2)→(1,2)→(1,3)→(0,3)?
Najlepsza: 1→1→2→1→1→1 = 7  ✅
```

> [!WARNING]
> W grid Dijkstra zamiast `visited` sprawdzamy `if d > dist[r][c]` — to szybsza alternatywa, bo unikamy tworzenia i przeszukiwania zbioru `visited`. Semantycznie równoważne: jeśli zdjęty dystans jest gorszy niż znany, to wierzchołek był już przetworzony.

### Złożoność Dijkstry

| Implementacja | Czasowa | Pamięciowa | Uwagi |
|---|---|---|---|
| **Min-heap (heapq)** | $O((V + E) \log V)$ | $O(V + E)$ | Standardowa, zalecana |
| Tablica (naiwna) | $O(V^2)$ | $O(V)$ | Prosta, lepsza dla gęstych grafów |
| Fibonacci heap | $O(V \log V + E)$ | $O(V)$ | Teoretycznie optymalna, rzadko w praktyce |

### Dijkstra vs BFS vs Bellman-Ford

| Kryterium | BFS | Dijkstra | Bellman-Ford |
|---|---|---|---|
| Wagi krawędzi | Brak (nieważony) | Nieujemne ($\geq 0$) | Dowolne (ujemne OK) |
| Złożoność | $O(V + E)$ | $O((V+E) \log V)$ | $O(V \cdot E)$ |
| Struktura danych | Kolejka (FIFO) | Min-heap | Tablice |
| Ujemne cykle | N/A | ❌ Nie obsługuje | ✅ Wykrywa |
| Kiedy używać | Najkrótsza ścieżka bez wag | Mapy, GPS, routing | Arbitraż walut, ujemne koszty |

> [!TIP]
> **Reguła kciuka:** jeśli graf nie ma wag → **BFS**. Jeśli wagi $\geq 0$ → **Dijkstra**. Jeśli mogą być ujemne wagi → **Bellman-Ford**. Jeśli potrzebujesz wszystkich par → **Floyd-Warshall**.

### Podsumowanie Dijkstry

| Wariant | Zastosowanie | Złożoność |
|---|---|---|
| Dijkstra (min-heap) | Najkrótsza ścieżka z jednego źródła | $O((V+E) \log V)$ |
| Dijkstra + path | Ścieżka + koszt (GPS, nawigacja) | $O((V+E) \log V)$ |
| Dijkstra na gridzie | Pathfinding w grach, koszty terenu | $O(R \cdot C \cdot \log(R \cdot C))$ |

📎 Powiązane sekcje: [BFS](#3-bfs-breadth-first-search) (najkrótsza ścieżka w grafie nieważonym), [Greedy](#8-algorytmy-zachłanne-greedy) (Dijkstra to algorytm zachłanny)

---

## 6. Programowanie dynamiczne (Dynamic Programming)

**Kategoria:** technika algorytmiczna

Nie jest to jeden konkretny algorytm, lecz **paradygmat rozwiązywania problemów** — rozbij problem na podproblemy, rozwiąż je raz, zapamiętaj wyniki (memoizacja / tabulacja), złóż rozwiązanie.

**Kluczowe problemy:**
- Ciąg Fibonacci
- Problem plecakowy (Knapsack)
- Longest Common Subsequence (LCS)
- Edit Distance (Levenshtein)
- Coin Change

**Dlaczego jest ważny?**
- Transformuje rozwiązania wykładnicze $O(2^n)$ w wielomianowe $O(n^2)$ lub $O(n \cdot W)$.
- Jeden z najczęstszych tematów na rozmowach rekrutacyjnych (FAANG).
- Uczy rozpoznawania struktury optymalnych podproblemów (optimal substructure) i nakładających się podproblemów (overlapping subproblems).

> [!IMPORTANT]
> DP działa wtedy i tylko wtedy, gdy problem ma dwie właściwości:
> - **Optimal substructure** — optymalne rozwiązanie składa się z optymalnych rozwiązań podproblemów
> - **Overlapping subproblems** — te same podproblemy pojawiają się wielokrotnie

### Dwa podejścia: Top-Down vs Bottom-Up

| Cecha | Top-Down (memoizacja) | Bottom-Up (tabulacja) |
|---|---|---|
| Kierunek | Od problemu do base case | Od base case do problemu |
| Implementacja | Rekurencja + cache (`@lru_cache`) | Pętla + tablica `dp[]` |
| Pamięć stosu | $O(n)$ (stos rekurencji) | $O(1)$ (brak rekurencji) |
| Oblicza | Tylko potrzebne podproblemy | Wszystkie podproblemy |
| Ryzyko | `RecursionError` | Brak |

### 🔍 Wizualizacja: dlaczego naiwna rekurencja jest zła

```
Naiwne fib(5) — DRZEWO REKURENCJI (overlapping subproblems):

                         fib(5)
                        /       \
                   fib(4)        fib(3)       ← fib(3) obliczony 2×!
                  /     \        /    \
             fib(3)    fib(2)  fib(2)  fib(1)  ← fib(2) obliczony 3×!
             /   \       |      |       |
         fib(2) fib(1)   1      1       1

Wywołań: 9  (rośnie wykładniczo → O(2^n))  ❌
```

```
fib(5) z TABULACJĄ — wypełniaj tablicę od dołu:

Indeks:   0    1    2    3    4    5
         ┌────┬────┬────┬────┬────┬────┐
dp:      │ 0  │ 1  │ 1  │ 2  │ 3  │ 5  │
         └────┴────┴────┴────┴────┴────┘
          base base  ↑    ↑    ↑    ↑
                    0+1  1+1  1+2  2+3

dp[i] = dp[i-1] + dp[i-2]    Wynik: dp[5] = 5  ✅  O(n)
```

### Schemat rozwiązywania (rozmowa rekrutacyjna)

```
1. ZDEFINIUJ STAN       → Co oznacza dp[i]? (np. min monet do kwoty i)
2. RELACJA REKURENCYJNA → dp[i] = min(dp[i-coin]+1) for coin in coins
3. BASE CASE            → dp[0] = 0
4. KOLEJNOŚĆ            → Bottom-up (od małych do dużych) lub top-down
5. ODCZYTAJ ODPOWIEDŹ   → dp[n] lub dp[m][n]
6. (OPCJ.) ODTWÓRZ      → Backtracking po tablicy dp
```

### Kluczowe problemy — podsumowanie

| Problem | Relacja rekurencyjna | Złożoność |
|---|---|---|
| **Fibonacci** | $dp[i] = dp[i-1] + dp[i-2]$ | $O(n)$ |
| **Coin Change** | $dp[i] = \min(dp[i-coin]+1)$ | $O(n \cdot k)$ |
| **0/1 Knapsack** | $dp[i][w] = \max(skip, take)$ | $O(n \cdot W)$ |
| **LCS** | match → $dp[i-1][j-1]+1$, else → $\max$ | $O(m \cdot n)$ |
| **Edit Distance** | match → $dp[i-1][j-1]$, else → $1+\min(3)$ | $O(m \cdot n)$ |

```python
# TODO: Pełne implementacje — Fibonacci, Coin Change, Knapsack, LCS, Edit Distance
# Patrz dedykowany artykuł poniżej
pass
```

> [!TIP]
> **Sygnały, że problem wymaga DP:** „Znajdź minimum/maximum", „Policz liczbę sposobów", „Czy da się...?" + ograniczone wejście ($n \leq 1000$).

📎 Pełny artykuł: [Programowanie dynamiczne](programowanie-dynamiczne.md)
📎 Powiązane: [Implementacje ciągu Fibonacci](implementacje-ciagu-fibonacci.md)

---

## 7. Algorytmy na drzewach binarnych (traversal)

**Kategoria:** struktury danych / drzewa

Trzy klasyczne porządki przechodzenia drzewa binarnego (DFS) + przechodzenie poziomami (BFS):

- **Inorder** (lewy → korzeń → prawy) — w BST daje posortowaną kolejność.
- **Preorder** (korzeń → lewy → prawy) — serializacja drzewa, kopiowanie.
- **Postorder** (lewy → prawy → korzeń) — usuwanie drzewa, obliczanie wyrażeń.
- **Level-order** (BFS, warstwa po warstwie) — patrz sekcja [BFS](#3-bfs-breadth-first-search).

**Dlaczego są ważne?**
- Drzewa binarne to fundament struktur danych (BST, heap, trie).
- Traversal to podstawa dla: walidacji BST, znajdowania LCA, serializacji/deserializacji.
- Uczą rekurencji i myślenia o strukturach hierarchicznych.
- Najczęstszy typ zadań na rozmowach rekrutacyjnych (LeetCode: ~30% zadań to drzewa).

**Złożoność:** $O(n)$ czasowa, $O(h)$ pamięciowa (gdzie $h$ = wysokość drzewa)

### Struktura węzła (TreeNode)

Standardowa definicja używana we wszystkich implementacjach poniżej:

```python
class TreeNode:
    def __init__(self, val: int = 0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

Przykładowe drzewo używane w wizualizacjach:

```
        4
       / \
      2    6
     / \  / \
    1   3 5   7
```

```python
# Budowa drzewa:
tree = TreeNode(4,
    TreeNode(2, TreeNode(1), TreeNode(3)),
    TreeNode(6, TreeNode(5), TreeNode(7)),
)
```

> [!NOTE]
> To jest drzewo BST (Binary Search Tree) — dla każdego węzła: wszystkie wartości w lewym poddrzewie < węzeł < wszystkie wartości w prawym poddrzewie. Traversal **inorder** zwróci wartości posortowane.

### 🔍 Wizualizacja trzech porządków (krok po kroku)

```
Drzewo:
        4
       / \
      2    6
     / \  / \
    1   3 5   7

═══════════════════════════════════════════════════════════════

INORDER (lewy → korzeń → prawy):

Krok 1: idź w lewo od 4 → 2 → 1 (liść, brak lewego)
Krok 2: odwiedź 1 ✓
Krok 3: wróć do 2, odwiedź 2 ✓
Krok 4: idź w prawo od 2 → 3, odwiedź 3 ✓
Krok 5: wróć do 4, odwiedź 4 ✓
Krok 6: idź w prawo od 4 → 6 → 5, odwiedź 5 ✓
Krok 7: wróć do 6, odwiedź 6 ✓
Krok 8: idź w prawo od 6 → 7, odwiedź 7 ✓

Wynik: [1, 2, 3, 4, 5, 6, 7]  ← posortowane! (bo to BST) ✅

═══════════════════════════════════════════════════════════════

PREORDER (korzeń → lewy → prawy):

Krok 1: odwiedź 4 ✓ (korzeń pierwszy!)
Krok 2: idź w lewo → odwiedź 2 ✓
Krok 3: idź w lewo → odwiedź 1 ✓
Krok 4: wróć, idź w prawo → odwiedź 3 ✓
Krok 5: wróć do 4, idź w prawo → odwiedź 6 ✓
Krok 6: idź w lewo → odwiedź 5 ✓
Krok 7: wróć, idź w prawo → odwiedź 7 ✓

Wynik: [4, 2, 1, 3, 6, 5, 7]  ← korzeń zawsze pierwszy ✅

═══════════════════════════════════════════════════════════════

POSTORDER (lewy → prawy → korzeń):

Krok 1: idź w lewo od 4 → 2 → 1 (liść)
Krok 2: odwiedź 1 ✓
Krok 3: wróć do 2, idź w prawo → 3, odwiedź 3 ✓
Krok 4: oba dzieci 2 przetworzone → odwiedź 2 ✓
Krok 5: idź w prawo od 4 → 6 → 5, odwiedź 5 ✓
Krok 6: wróć do 6, idź w prawo → 7, odwiedź 7 ✓
Krok 7: oba dzieci 6 przetworzone → odwiedź 6 ✓
Krok 8: oba dzieci 4 przetworzone → odwiedź 4 ✓

Wynik: [1, 3, 2, 5, 7, 6, 4]  ← korzeń zawsze ostatni ✅
```

**Mnemonik:**

```
              Inorder           Preorder          Postorder
              L → N → R         N → L → R         L → R → N

              N = Node (korzeń), L = Left, R = Right

Kiedy odwiedzamy korzeń?
              w środku           na początku        na końcu
```

### Implementacja rekurencyjna (wszystkie 3 porządki)

Najprostsza forma — rekurencja naturalna dla drzew:

```python
def inorder(root: TreeNode | None) -> list[int]:
    if not root:
        return []
    return inorder(root.left) + [root.val] + inorder(root.right)


def preorder(root: TreeNode | None) -> list[int]:
    if not root:
        return []
    return [root.val] + preorder(root.left) + preorder(root.right)


def postorder(root: TreeNode | None) -> list[int]:
    if not root:
        return []
    return postorder(root.left) + postorder(root.right) + [root.val]


# Usage:
tree = TreeNode(4,
    TreeNode(2, TreeNode(1), TreeNode(3)),
    TreeNode(6, TreeNode(5), TreeNode(7)),
)

print(inorder(tree))    # [1, 2, 3, 4, 5, 6, 7]
print(preorder(tree))   # [4, 2, 1, 3, 6, 5, 7]
print(postorder(tree))  # [1, 3, 2, 5, 7, 6, 4]
```

> [!TIP]
> Wersja z konkatenacją list (`+`) jest czytelna, ale tworzy nowe listy na każdym wywołaniu ($O(n)$ dodatkowej pamięci na każdy poziom). Wydajniejsza wersja z `append` poniżej.

### Implementacja rekurencyjna (wydajna, z append)

Jedna wspólna lista `result` modyfikowana w miejscu — brak narzutu alokacji:

```python
def inorder_fast(root: TreeNode | None) -> list[int]:
    result = []

    def _dfs(node: TreeNode | None) -> None:
        if not node:
            return
        _dfs(node.left)
        result.append(node.val)    # ← inorder: między lewym a prawym
        _dfs(node.right)

    _dfs(root)
    return result


def preorder_fast(root: TreeNode | None) -> list[int]:
    result = []

    def _dfs(node: TreeNode | None) -> None:
        if not node:
            return
        result.append(node.val)    # ← preorder: przed dziećmi
        _dfs(node.left)
        _dfs(node.right)

    _dfs(root)
    return result


def postorder_fast(root: TreeNode | None) -> list[int]:
    result = []

    def _dfs(node: TreeNode | None) -> None:
        if not node:
            return
        _dfs(node.left)
        _dfs(node.right)
        result.append(node.val)    # ← postorder: po dzieciach

    _dfs(root)
    return result


# Usage:
tree = TreeNode(4,
    TreeNode(2, TreeNode(1), TreeNode(3)),
    TreeNode(6, TreeNode(5), TreeNode(7)),
)

print(inorder_fast(tree))    # [1, 2, 3, 4, 5, 6, 7]
print(preorder_fast(tree))   # [4, 2, 1, 3, 6, 5, 7]
print(postorder_fast(tree))  # [1, 3, 2, 5, 7, 6, 4]
```

> [!IMPORTANT]
> Jedyna różnica między trzema porządkami to **pozycja linii `result.append(node.val)`** — przed, między, lub po wywołaniach rekurencyjnych. To kluczowa obserwacja!

### Implementacja iteracyjna (z jawnym stosem)

Bezpieczna dla głębokich drzew — brak ryzyka `RecursionError`:

#### Inorder iteracyjny

```python
def inorder_iterative(root: TreeNode | None) -> list[int]:
    result = []
    stack = []
    current = root

    while current or stack:
        # idź w lewo aż do końca
        while current:
            stack.append(current)
            current = current.left

        # zdejmij ze stosu, odwiedź, idź w prawo
        current = stack.pop()
        result.append(current.val)
        current = current.right

    return result


# Usage:
tree = TreeNode(4,
    TreeNode(2, TreeNode(1), TreeNode(3)),
    TreeNode(6, TreeNode(5), TreeNode(7)),
)

print(inorder_iterative(tree))  # [1, 2, 3, 4, 5, 6, 7]
```

```
Symulacja stosu (inorder iteracyjny):

current=4 → push 4, go left
current=2 → push 2, go left
current=1 → push 1, go left
current=None → pop 1, visit 1, go right (None)
              → pop 2, visit 2, go right (3)
current=3 → push 3, go left
current=None → pop 3, visit 3, go right (None)
              → pop 4, visit 4, go right (6)
current=6 → push 6, go left
current=5 → push 5, go left
current=None → pop 5, visit 5, go right (None)
              → pop 6, visit 6, go right (7)
current=7 → push 7, go left
current=None → pop 7, visit 7, go right (None)

Wynik: [1, 2, 3, 4, 5, 6, 7] ✅
```

#### Preorder iteracyjny

```python
def preorder_iterative(root: TreeNode | None) -> list[int]:
    if not root:
        return []

    result = []
    stack = [root]

    while stack:
        node = stack.pop()
        result.append(node.val)        # odwiedź przy zdejmowaniu

        # prawy PIERWSZY na stos → lewy będzie na szczycie (przetworzony pierwszy)
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)

    return result


# Usage:
tree = TreeNode(4,
    TreeNode(2, TreeNode(1), TreeNode(3)),
    TreeNode(6, TreeNode(5), TreeNode(7)),
)

print(preorder_iterative(tree))  # [4, 2, 1, 3, 6, 5, 7]
```

> [!WARNING]
> W preorder iteracyjnym dodajemy **prawe dziecko przed lewym** na stos (LIFO), żeby lewe zostało przetworzone jako pierwsze. Częsty błąd na rozmowach!

#### Postorder iteracyjny

```python
def postorder_iterative(root: TreeNode | None) -> list[int]:
    if not root:
        return []

    result = []
    stack = [root]

    while stack:
        node = stack.pop()
        result.append(node.val)

        # lewy PIERWSZY na stos → prawy będzie przetworzony pierwszy
        if node.left:
            stack.append(node.left)
        if node.right:
            stack.append(node.right)

    return result[::-1]   # odwróć wynik → postorder!


# Usage:
tree = TreeNode(4,
    TreeNode(2, TreeNode(1), TreeNode(3)),
    TreeNode(6, TreeNode(5), TreeNode(7)),
)

print(postorder_iterative(tree))  # [1, 3, 2, 5, 7, 6, 4]
```

> [!TIP]
> **Trik:** postorder iteracyjny = zmodyfikowany preorder (korzeń → prawy → lewy) **odwrócony**. Zamiast walczyć ze skomplikowaną logiką stosu, po prostu odwracamy wynik na końcu.

### Level-order (BFS na drzewie)

Przechodzenie **warstwa po warstwie** — użyte wcześniej w sekcji [BFS](#3-bfs-breadth-first-search):

```python
from collections import deque


def level_order(root: TreeNode | None) -> list[list[int]]:
    if not root:
        return []

    result = []
    queue = deque([root])

    while queue:
        level_size = len(queue)
        level = []

        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        result.append(level)

    return result


# Usage:
tree = TreeNode(4,
    TreeNode(2, TreeNode(1), TreeNode(3)),
    TreeNode(6, TreeNode(5), TreeNode(7)),
)

print(level_order(tree))  # [[4], [2, 6], [1, 3, 5, 7]]
```

```
Wizualizacja level-order:

        4          Poziom 0: [4]
       / \
      2    6       Poziom 1: [2, 6]
     / \  / \
    1   3 5   7    Poziom 2: [1, 3, 5, 7]

Wynik: [[4], [2, 6], [1, 3, 5, 7]]
```

### Porównanie czterech porządków

```
Drzewo:        4
              / \
             2    6
            / \  / \
           1   3 5   7

Inorder:    [1, 2, 3, 4, 5, 6, 7]    L → N → R   ← posortowane (BST)
Preorder:   [4, 2, 1, 3, 6, 5, 7]    N → L → R   ← korzeń pierwszy
Postorder:  [1, 3, 2, 5, 7, 6, 4]    L → R → N   ← korzeń ostatni
Level-order: [[4], [2, 6], [1, 3, 5, 7]]          ← warstwa po warstwie
```

| Porządek | Kolejność | Struktura | Kiedy używać |
|---|---|---|---|
| **Inorder** | L → N → R | DFS (stos/rekurencja) | Posortowana kolejność BST, walidacja BST |
| **Preorder** | N → L → R | DFS (stos/rekurencja) | Serializacja, kopiowanie drzewa |
| **Postorder** | L → R → N | DFS (stos/rekurencja) | Usuwanie drzewa, obliczanie wyrażeń |
| **Level-order** | warstwa po warstwie | BFS (kolejka) | Najkrótsza ścieżka, wizualizacja poziomów |

---

### Klasyczne problemy na drzewach binarnych

#### Maksymalna głębokość drzewa

Najprostszy problem rekurencyjny — fundament myślenia o drzewach:

```python
def max_depth(root: TreeNode | None) -> int:
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))


# Usage:
tree = TreeNode(4,
    TreeNode(2, TreeNode(1), TreeNode(3)),
    TreeNode(6, TreeNode(5), TreeNode(7)),
)

print(max_depth(tree))   # 3
print(max_depth(None))   # 0
```

```
        4         ← głębokość 1
       / \
      2    6      ← głębokość 2
     / \  / \
    1   3 5   7   ← głębokość 3

max_depth = 3
```

#### Walidacja BST (validate BST)

Sprawdź, czy drzewo jest poprawnym BST. **Inorder traversal BST musi być ściśle rosnący:**

```python
def is_valid_bst(root: TreeNode | None) -> bool:
    def _validate(node: TreeNode | None, min_val: float, max_val: float) -> bool:
        if not node:
            return True

        # wartość musi być w zakresie (min_val, max_val)
        if node.val <= min_val or node.val >= max_val:
            return False

        # lewe poddrzewo: wartości < node.val
        # prawe poddrzewo: wartości > node.val
        return (_validate(node.left, min_val, node.val) and
                _validate(node.right, node.val, max_val))

    return _validate(root, float('-inf'), float('inf'))


# Usage:
#   Poprawny BST:        Niepoprawny BST:
#       4                     4
#      / \                   / \
#     2    6                2    6
#    / \                   / \
#   1   3                 1   5  ← 5 > 4, ale jest w lewym poddrzewie!

valid_tree = TreeNode(4,
    TreeNode(2, TreeNode(1), TreeNode(3)),
    TreeNode(6),
)

invalid_tree = TreeNode(4,
    TreeNode(2, TreeNode(1), TreeNode(5)),  # 5 > 4!
    TreeNode(6),
)

print(is_valid_bst(valid_tree))    # True
print(is_valid_bst(invalid_tree))  # False
```

> [!WARNING]
> Częsty błąd: sprawdzanie tylko `node.left.val < node.val < node.right.val` **nie wystarczy**. Wartość musi być poprawna względem **wszystkich przodków**, nie tylko rodzica. Dlatego przekazujemy `min_val` i `max_val` w dół drzewa.

#### Odwracanie drzewa (invert binary tree)

Słynny problem z rozmowy w Google — zamiana lewego i prawego poddrzewa na każdym poziomie:

```python
def invert_tree(root: TreeNode | None) -> TreeNode | None:
    if not root:
        return None

    # zamień lewe i prawe poddrzewo
    root.left, root.right = root.right, root.left

    # rekurencyjnie odwróć oba poddrzewa
    invert_tree(root.left)
    invert_tree(root.right)

    return root


# Usage:
tree = TreeNode(4,
    TreeNode(2, TreeNode(1), TreeNode(3)),
    TreeNode(7, TreeNode(6), TreeNode(9)),
)

inverted = invert_tree(tree)
print(inorder_fast(inverted))  # [9, 7, 6, 4, 3, 2, 1]
```

```
Przed:              Po odwróceniu:

     4                   4
    / \                 / \
   2    7              7    2
  / \  / \            / \  / \
 1   3 6   9         9   6 3   1
```

#### Najniższy wspólny przodek (LCA — Lowest Common Ancestor)

Znajdź najniższy węzeł, który jest przodkiem obu podanych węzłów:

```python
def lowest_common_ancestor(
    root: TreeNode | None,
    p: TreeNode,
    q: TreeNode,
) -> TreeNode | None:
    if not root:
        return None

    # jeśli bieżący węzeł to p lub q → to jest LCA (lub kandydat)
    if root == p or root == q:
        return root

    # szukaj w lewym i prawym poddrzewie
    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)

    # jeśli znalezione w obu poddrzewach → bieżący węzeł to LCA
    if left and right:
        return root

    # w przeciwnym razie → LCA jest w tym poddrzewie, gdzie coś znaleźliśmy
    return left if left else right


# Usage:
#        3
#       / \
#      5    1
#     / \  / \
#    6   2 0   8

node6 = TreeNode(6)
node2 = TreeNode(2)
node0 = TreeNode(0)
node8 = TreeNode(8)
node5 = TreeNode(5, node6, node2)
node1 = TreeNode(1, node0, node8)
root = TreeNode(3, node5, node1)

print(lowest_common_ancestor(root, node5, node1).val)   # 3
print(lowest_common_ancestor(root, node6, node2).val)   # 5
print(lowest_common_ancestor(root, node6, node8).val)   # 3
```

```
LCA(6, 2) = 5:              LCA(6, 8) = 3:

        3                          [3]  ← LCA
       / \                        / \
     [5]   1   ← LCA            5    1
     / \                        /     \
   [6] [2]                    [6]    [8]
```

> [!TIP]
> Dla **BST** (nie zwykłego drzewa binarnego) LCA można znaleźć szybciej: jeśli oba węzły < root → idź w lewo; jeśli oba > root → idź w prawo; w przeciwnym razie root to LCA. Złożoność $O(h)$ zamiast $O(n)$.

### Podsumowanie Traversal

| Wariant | Złożoność czas. | Złożoność pam. | Zastosowanie |
|---|---|---|---|
| Inorder (rekurencyjny) | $O(n)$ | $O(h)$ | Posortowana kolejność BST |
| Preorder (rekurencyjny) | $O(n)$ | $O(h)$ | Serializacja, kopiowanie |
| Postorder (rekurencyjny) | $O(n)$ | $O(h)$ | Usuwanie, ewaluacja wyrażeń |
| Iteracyjny (stos) | $O(n)$ | $O(h)$ | Duże drzewa (bez RecursionError) |
| Level-order (BFS) | $O(n)$ | $O(w)$ | Przechodzenie poziomami ($w$ = max szerokość) |
| Max depth | $O(n)$ | $O(h)$ | Wysokość drzewa |
| Validate BST | $O(n)$ | $O(h)$ | Sprawdzanie poprawności BST |
| LCA | $O(n)$ | $O(h)$ | Najniższy wspólny przodek |

> [!NOTE]
> $h$ = wysokość drzewa. Dla zbalansowanego drzewa $h = O(\log n)$, ale dla zdegenerowanego (liniowego) $h = O(n)$. Dlatego w najgorszym przypadku pamięć stosu rekurencji to $O(n)$.

---

## 8. Algorytmy zachłanne (Greedy)

**Kategoria:** technika algorytmiczna

Strategia polegająca na podejmowaniu **lokalnie optymalnej decyzji** w każdym kroku, z nadzieją na osiągnięcie globalnego optimum. Nie zawsze daje najlepsze rozwiązanie — działa tylko gdy problem ma własność zachłanności (greedy choice property).

**Kluczowe problemy:**
- Activity Selection / Interval Scheduling
- Coin Change (gdy nominały są „ładne")
- Fractional Knapsack (plecak ułamkowy)
- Jump Game
- Algorytm Dijkstry (patrz sekcja [5](#5-algorytm-dijkstry))
- Minimum Spanning Tree (Kruskal, Prim)
- Algorytm Huffmana (kompresja)

**Dlaczego są ważne?**
- Proste i szybkie rozwiązania, gdy da się udowodnić poprawność.
- Uczą rozpoznawania, kiedy zachłanność działa, a kiedy nie (w przeciwieństwie do DP).
- Powszechne w zadaniach optymalizacyjnych i harmonogramowaniu.

**Złożoność:** zależna od problemu (często $O(n \log n)$ — dominuje sortowanie)

### Jak działa? (intuicja)

Algorytm zachłanny w każdym kroku wybiera **najlepszą dostępną opcję** bez oglądania się wstecz:

```
Greedy = w każdym kroku wybierz lokalnie najlepszą opcję
         i NIGDY nie cofaj decyzji

Przykład z życia:
  "Wydawanie reszty" → zawsze daj największą monetę, która się mieści
  42 gr = 20 + 20 + 2  ✅ (greedy działa dla PLN)
```

### Kiedy greedy działa?

Algorytm zachłanny daje **optymalny wynik** tylko gdy problem spełnia dwa warunki:

```
1. Greedy Choice Property (własność zachłannego wyboru):
   Lokalnie optymalna decyzja prowadzi do globalnie optymalnego rozwiązania.

2. Optimal Substructure (optymalna podstruktura):
   Optymalne rozwiązanie zawiera optymalne rozwiązania podproblemów.
```

> [!IMPORTANT]
> Jeśli problem **nie ma** greedy choice property, algorytm zachłanny da **błędny wynik**. Nie ma ogólnego sposobu na sprawdzenie tego — trzeba to udowodnić lub znaleźć kontrprzykład. Jeśli greedy nie działa → użyj **Dynamic Programming**.

### 🔍 Wizualizacja: Greedy vs inne podejścia

```
Problem: znajdź najlepszą ścieżkę (max suma) od korzenia do liścia

         7
        / \
       3    12
      / \   / \
     99  1 5   6

Greedy (wybierz max na każdym kroku):
  7 → 12 → 6 = 25   ❌ (zachłannie wybrał 12 zamiast 3)

Optymalne (sprawdź wszystkie ścieżki):
  7 → 3 → 99 = 109  ✅

Greedy NIE DZIAŁA dla tego problemu!
Potrzebny: DFS / Dynamic Programming
```

```
Problem: wydawanie reszty monetami [1, 5, 10, 25]

Kwota: 36 centów

Greedy (zawsze największa moneta):
  36 - 25 = 11     → bierz 25 ✓
  11 - 10 = 1      → bierz 10 ✓
  1  - 1  = 0      → bierz 1  ✓
  Wynik: 3 monety [25, 10, 1] ✅

Greedy DZIAŁA dla standardowych nominałów!
(ale NIE działa dla dowolnych, np. [1, 3, 4] → kwota 6)
```

---

### Activity Selection (Interval Scheduling)

Wybierz **maksymalną liczbę nieprzekrywających się aktywności** (przedziałów). Klasyczny problem greedy — sortuj po czasie zakończenia i zawsze wybieraj najwcześniej kończącą się aktywność.

#### 🔍 Wizualizacja

```
Aktywności (start, end):
  A: [1, 4)
  B: [3, 5)
  C: [0, 6)
  D: [5, 7)
  E: [3, 9)
  F: [5, 9)
  G: [6, 10)
  H: [8, 11)
  I: [8, 12)
  J: [2, 14)

Oś czasu:
0  1  2  3  4  5  6  7  8  9  10 11 12 13 14
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |
   [A A A]
      [B B B]
[C C C C C C]
               [D D D]
      [E E E E E E E]
               [F F F F F]
                  [G G G G G]
                        [H H H H]
                        [I I I I I I]
   [J J J J J J J J J J J J J J]

Sortuj po end time: A(4), B(5), C(6), D(7), E(9), F(9), G(10), H(11), I(12), J(14)

Greedy:
  1. Wybierz A [1,4)     ✓ (najwcześniej kończy się)
  2. B [3,5) koliduje z A → pomiń
  3. C [0,6) koliduje z A → pomiń
  4. D [5,7) start≥4    → ✓ wybierz
  5. E [3,9) koliduje z D → pomiń
  6. F [5,9) koliduje z D → pomiń
  7. G [6,10) koliduje z D → pomiń
  8. H [8,11) start≥7   → ✓ wybierz
  9. I [8,12) koliduje z H → pomiń
  10. J [2,14) koliduje z H → pomiń

Wynik: {A, D, H} = 3 aktywności ✅ (maksimum)

0  1  2  3  4  5  6  7  8  9  10 11
|  |  |  |  |  |  |  |  |  |  |  |
   [A A A]
               [D D D]
                        [H H H H]
```

#### Implementacja

```python
def activity_selection(
    activities: list[tuple[int, int]],
) -> list[tuple[int, int]]:
    # sortuj po czasie zakończenia (end time)
    sorted_acts = sorted(activities, key=lambda x: x[1])

    selected = [sorted_acts[0]]       # zawsze bierz pierwszą (najwcześniej kończy się)
    last_end = sorted_acts[0][1]

    for start, end in sorted_acts[1:]:
        if start >= last_end:          # nie koliduje z ostatnią wybraną
            selected.append((start, end))
            last_end = end

    return selected


# Usage:
activities = [
    (1, 4), (3, 5), (0, 6), (5, 7), (3, 9),
    (5, 9), (6, 10), (8, 11), (8, 12), (2, 14),
]

result = activity_selection(activities)
print(f"Wybrane: {result}")          # [(1, 4), (5, 7), (8, 11)]
print(f"Liczba: {len(result)}")      # 3
```

> [!TIP]
> **Dlaczego sortujemy po end time, a nie start time?** Bo chcemy jak najszybciej „zwolnić" oś czasu dla kolejnych aktywności. Aktywność, która kończy się najwcześniej, zostawia najwięcej miejsca.

---

### Coin Change (Greedy — nominały standardowe)

Wydaj resztę **minimalną liczbą monet**. Greedy działa dla „ładnych" systemów monetarnych (np. PLN, USD):

#### 🔍 Wizualizacja

```
Nominały: [1, 2, 5, 10, 20, 50]  (grosze PLN)
Kwota: 93 gr

Greedy (największa moneta, która się mieści):
  93 - 50 = 43    → bierz 50
  43 - 20 = 23    → bierz 20
  23 - 20 = 3     → bierz 20
  3  - 2  = 1     → bierz 2
  1  - 1  = 0     → bierz 1

Wynik: [50, 20, 20, 2, 1] = 5 monet ✅
```

#### Implementacja

```python
def coin_change_greedy(coins: list[int], amount: int) -> list[int]:
    coins_sorted = sorted(coins, reverse=True)   # od największej
    result = []

    for coin in coins_sorted:
        while amount >= coin:
            result.append(coin)
            amount -= coin

    if amount > 0:
        return []   # nie da się wydać (np. brak monety 1)

    return result


# Usage (nominały PLN):
print(coin_change_greedy([1, 2, 5, 10, 20, 50], 93))
# [50, 20, 20, 2, 1]

print(coin_change_greedy([1, 5, 10, 25], 36))
# [25, 10, 1]
```

> [!WARNING]
> Greedy **NIE DZIAŁA** dla dowolnych nominałów!
>
> Kontrprzykład: nominały `[1, 3, 4]`, kwota `6`:
> - Greedy: `4 + 1 + 1 = 3 monety` ❌
> - Optymalne: `3 + 3 = 2 monety` ✅
>
> Dla dowolnych nominałów użyj **Dynamic Programming** (sekcja [6](#6-programowanie-dynamiczne-dynamic-programming)).

#### Coin Change — kiedy greedy, kiedy DP?

```
Nominały „ładne" (kanoniczne):        Nominały dowolne:
[1, 5, 10, 25]  → GREEDY ✅           [1, 3, 4]  → DP ✅
[1, 2, 5, 10]   → GREEDY ✅           [1, 5, 6, 9] → DP ✅
[1, 2, 5, 10, 20, 50] → GREEDY ✅     [7, 13]  → DP ✅

Reguła: jeśli każdy nominał jest ≥ 2× poprzedniego → greedy OK
        w przeciwnym razie → użyj DP
```

---

### Fractional Knapsack (plecak ułamkowy)

Mamy plecak o pojemności $W$ i $n$ przedmiotów z wagą i wartością. Możemy brać **ułamki** przedmiotów. Greedy: sortuj po **wartości na jednostkę wagi** (value/weight) i bierz od najcenniejszych.

#### 🔍 Wizualizacja

```
Pojemność plecaka: W = 50 kg

Przedmioty:
  Przedmiot   Waga   Wartość   Wartość/kg
  A           10     60        6.0        ← najcenniejszy per kg
  B           20     100       5.0
  C           30     120       4.0

Greedy (bierz od najwyższego value/kg):
  1. Weź A w całości: waga=10, wartość=60    → zostaje 40 kg
  2. Weź B w całości: waga=20, wartość=100   → zostaje 20 kg
  3. Weź C częściowo: 20/30 = 2/3 z C       → wartość=120×(2/3)=80

  Łączna wartość: 60 + 100 + 80 = 240 ✅ (maksimum)

  Plecak: [A:100%, B:100%, C:66.7%]
```

#### Implementacja

```python
def fractional_knapsack(
    capacity: int,
    items: list[tuple[int, int]],     # [(waga, wartość), ...]
) -> float:
    # sortuj po wartości/kg malejąco
    sorted_items = sorted(items, key=lambda x: x[1] / x[0], reverse=True)

    total_value = 0.0

    for weight, value in sorted_items:
        if capacity <= 0:
            break

        if weight <= capacity:
            # weź cały przedmiot
            total_value += value
            capacity -= weight
        else:
            # weź ułamek przedmiotu (tyle, ile się zmieści)
            fraction = capacity / weight
            total_value += value * fraction
            capacity = 0

    return total_value


# Usage:
items = [(10, 60), (20, 100), (30, 120)]   # (waga, wartość)
print(fractional_knapsack(50, items))        # 240.0

items2 = [(5, 40), (10, 50), (15, 60), (20, 90)]
print(fractional_knapsack(30, items2))       # 155.0
```

> [!IMPORTANT]
> **Fractional Knapsack** (ułamkowy) → **Greedy** działa ✅
> **0/1 Knapsack** (bierzesz cały przedmiot lub nic) → **Greedy NIE działa** ❌ → użyj DP
>
> Różnica: w wersji 0/1 nie możemy „dobrać" kawałka — greedy może wybrać duży, ale nieefektywny przedmiot, blokując lepsze kombinacje.

---

### Jump Game

Klasyczny problem z LeetCode: tablica `nums`, gdzie `nums[i]` = maksymalna długość skoku z pozycji $i$. Czy można dotrzeć z pozycji 0 do ostatniej?

#### 🔍 Wizualizacja

```
nums = [2, 3, 1, 1, 4]

Pozycja:   0   1   2   3   4
Wartość:   2   3   1   1   4
           ↓
           i=0: max_reach = max(0, 0+2) = 2
           i=1: max_reach = max(2, 1+3) = 4  ← osiągnęliśmy koniec!
           Wynik: True ✅

nums = [3, 2, 1, 0, 4]

Pozycja:   0   1   2   3   4
Wartość:   3   2   1   0   4
           ↓
           i=0: max_reach = max(0, 0+3) = 3
           i=1: max_reach = max(3, 1+2) = 3
           i=2: max_reach = max(3, 2+1) = 3
           i=3: max_reach = max(3, 3+0) = 3  ← utknęliśmy!
           i=4: i(4) > max_reach(3) → STOP
           Wynik: False ❌ (zero na pozycji 3 blokuje)
```

#### Implementacja

```python
def can_jump(nums: list[int]) -> bool:
    max_reach = 0

    for i in range(len(nums)):
        if i > max_reach:
            return False              # nie możemy dotrzeć do pozycji i
        max_reach = max(max_reach, i + nums[i])

        if max_reach >= len(nums) - 1:
            return True               # early exit — cel osiągalny

    return True


# Usage:
print(can_jump([2, 3, 1, 1, 4]))   # True
print(can_jump([3, 2, 1, 0, 4]))   # False
print(can_jump([0]))                # True  (już na miejscu)
print(can_jump([2, 0, 0]))          # True
```

#### Jump Game II (minimum skoków)

Wariant: jaka jest **minimalna liczba skoków** do końca?

```python
def jump(nums: list[int]) -> int:
    jumps = 0
    current_end = 0       # koniec zasięgu bieżącego skoku
    farthest = 0          # najdalszy punkt osiągalny

    for i in range(len(nums) - 1):
        farthest = max(farthest, i + nums[i])

        if i == current_end:         # musisz skoczyć
            jumps += 1
            current_end = farthest

            if current_end >= len(nums) - 1:
                break

    return jumps


# Usage:
print(jump([2, 3, 1, 1, 4]))       # 2  (0→1→4)
print(jump([2, 3, 0, 1, 4]))       # 2  (0→1→4)
```

```
nums = [2, 3, 1, 1, 4]

Skok 1: z pozycji 0, zasięg [0..2]
        farthest = max(0+2, 1+3) = 4
        → skocz do najdalszego punktu (logicznie do pos 1)

Skok 2: z pozycji 1, zasięg [1..4]
        farthest ≥ koniec → GOTOWE

Wynik: 2 skoki ✅
```

> [!TIP]
> Jump Game to BFS „w przebraniu" — każdy „skok" to nowa warstwa BFS. Greedy eliminuje potrzebę kolejki, śledząc tylko `current_end` i `farthest`.

---

### Greedy vs Dynamic Programming

| Kryterium | Greedy | Dynamic Programming |
|---|---|---|
| Podejmowanie decyzji | Lokalnie optymalna, **bez cofania** | Rozważa **wszystkie** opcje |
| Poprawność | Tylko z dowodem greedy choice property | Zawsze (jeśli poprawna rekurencja) |
| Złożoność (typowa) | $O(n \log n)$ lub $O(n)$ | $O(n^2)$, $O(n \cdot W)$, itp. |
| Implementacja | Prosta (sortuj + iteruj) | Złożona (memoizacja/tabulacja) |
| Kiedy działa | Activity Selection, Dijkstra, Huffman | Knapsack 0/1, Edit Distance, LCS |
| Kiedy **nie** działa | 0/1 Knapsack, dowolne Coin Change | — (zawsze daje poprawny wynik) |

```
Reguła kciuka:

1. Spróbuj GREEDY (prostsze, szybsze)
2. Znajdź kontrprzykład? → GREEDY nie działa → użyj DP
3. Nie znajdziesz kontrprzykładu? → Udowodnij poprawność lub użyj DP dla pewności
```

> [!WARNING]
> Na rozmowie rekrutacyjnej, jeśli zaproponujesz rozwiązanie greedy, **musisz umieć uzasadnić**, dlaczego działa. Samo „działa na przykładach" nie wystarczy — rekruter zapyta o dowód lub kontrprzykład.

### Podsumowanie Greedy

| Problem | Złożoność | Strategia greedy | Działa? |
|---|---|---|---|
| Activity Selection | $O(n \log n)$ | Sortuj po end time, bierz najwcześniej kończące się | ✅ Zawsze |
| Coin Change (standardowe nominały) | $O(n)$ | Największa moneta, która się mieści | ✅ Dla kanonicznych |
| Fractional Knapsack | $O(n \log n)$ | Sortuj po value/weight, bierz od najcenniejszych | ✅ Zawsze |
| Jump Game | $O(n)$ | Śledź max_reach | ✅ Zawsze |
| Dijkstra | $O((V+E) \log V)$ | Wierzchołek o min dystansie | ✅ Nieujemne wagi |
| Coin Change (dowolne) | — | — | ❌ Użyj DP |
| 0/1 Knapsack | — | — | ❌ Użyj DP |

📎 Powiązane sekcje: [Dijkstra](#5-algorytm-dijkstry) (algorytm zachłanny), [Dynamic Programming](#6-programowanie-dynamiczne-dynamic-programming) (alternatywa, gdy greedy nie działa)

---

## 9. Algorytm wyszukiwania w tablicy haszującej (Hashing)

**Kategoria:** struktury danych

Technika mapowania kluczy na indeksy za pomocą **funkcji haszującej**, umożliwiająca operacje wstawiania, wyszukiwania i usuwania w średnim czasie $O(1)$.

**Kluczowe zagadnienia:**
- Funkcje haszujące i kolizje
- Rozwiązywanie kolizji: chaining (łańcuchowanie) vs open addressing (adresowanie otwarte)
- Load factor i rehashing

**Dlaczego jest ważny?**
- `dict` i `set` w Pythonie to tablice haszujące — używasz ich codziennie.
- Fundamentalny w rozwiązywaniu problemów typu Two Sum, zliczanie częstości, deduplikacja.
- Uczy kompromisów czas-pamięć i analizy złożoności amortyzowanej.

**Złożoność:** $O(1)$ średnio, $O(n)$ w najgorszym przypadku

### Jak działa? (intuicja)

Tablica haszująca to **tablica + funkcja haszująca**. Klucz → hash → indeks → wartość:

```
Klucz "alice" → hash("alice") = 2078442    → indeks = 2078442 % 8 = 2

Tablica (rozmiar 8):
Index:  [0]    [1]    [2]         [3]    [4]    [5]    [6]    [7]
Value:  None   None   ("alice",   None   None   None   None   None
                       95)

Operacje:
  INSERT("alice", 95)  → hash % 8 = 2 → wstaw na pozycję 2     O(1)
  GET("alice")         → hash % 8 = 2 → odczytaj z pozycji 2   O(1)
  DELETE("alice")      → hash % 8 = 2 → usuń z pozycji 2       O(1)
```

> [!NOTE]
> Funkcja haszująca musi być **deterministyczna** — ten sam klucz zawsze daje ten sam hash. W Pythonie `hash()` zwraca `int`, a indeks to `hash(key) % len(table)`.

### 🔍 Wizualizacja: kolizje

Problem: dwa różne klucze mogą trafić na **ten sam indeks** (kolizja):

```
hash("alice") % 8 = 2
hash("bob")   % 8 = 5
hash("carol") % 8 = 2    ← KOLIZJA z "alice"!
hash("dave")  % 8 = 5    ← KOLIZJA z "bob"!
hash("eve")   % 8 = 7

Jak obsłużyć kolizje?
  1. Chaining (łańcuchowanie) — lista na każdym indeksie
  2. Open addressing (adresowanie otwarte) — szukaj wolnego miejsca
```

---

### Rozwiązywanie kolizji: Chaining

Każdy slot tablicy zawiera **listę (linked list)** elementów o tym samym indeksie:

```
Wstawiamy: alice→95, bob→87, carol→72, dave→91, eve→88

Index: [0]  →  []
       [1]  →  []
       [2]  →  [("alice", 95)] → [("carol", 72)]   ← łańcuch
       [3]  →  []
       [4]  →  []
       [5]  →  [("bob", 87)] → [("dave", 91)]       ← łańcuch
       [6]  →  []
       [7]  →  [("eve", 88)]

GET("carol"):
  1. hash("carol") % 8 = 2
  2. Przejdź listę na indeksie 2: "alice" ≠ "carol", "carol" = "carol" ✓
  3. Zwróć 72

Złożoność:
  Średnia: O(1) — jeśli łańcuchy krótkie (load factor < 0.75)
  Najgorsza: O(n) — wszystkie klucze na jednym indeksie (zdegenerowana hash)
```

### Rozwiązywanie kolizji: Open Addressing (Linear Probing)

Brak list — szukaj **następnego wolnego slotu** w tablicy:

```
Wstawiamy: alice→95 (idx=2), carol→72 (idx=2, kolizja!)

Krok 1: indeks 2 zajęty ("alice") → spróbuj 3
Krok 2: indeks 3 wolny → wstaw "carol" na 3

Index: [0]         [1]         [2]              [3]              [4]  ...
       None        None        ("alice", 95)    ("carol", 72)    None

GET("carol"):
  1. hash("carol") % 8 = 2
  2. Indeks 2: "alice" ≠ "carol" → spróbuj 3
  3. Indeks 3: "carol" = "carol" ✓ → zwróć 72

DELETE wymaga specjalnego markera "DELETED" (tombstone),
żeby nie przerwać łańcucha probing:

  DELETE("alice"):
  Index: [0]  [1]  [2]          [3]              [4]
         None None [DELETED]    ("carol", 72)    None

  GET("carol") nadal działa — "DELETED" ≠ "carol", idź dalej → 3 ✓
```

> [!WARNING]
> Open addressing jest wrażliwy na **clustering** — grupy zajętych slotów rosną i spowalniają operacje. Python `dict` używa open addressing z **perturbacją** (nie linear probing), żeby zredukować ten problem.

### Implementacja: HashTable z chaining

Pełna implementacja tablicy haszującej z łańcuchowaniem i automatycznym rehashingiem:

```python
class HashTable:
    def __init__(self, capacity: int = 8):
        self.capacity = capacity
        self.size = 0
        self.buckets: list[list[tuple]] = [[] for _ in range(capacity)]

    def _hash(self, key: str) -> int:
        return hash(key) % self.capacity

    def put(self, key: str, value) -> None:
        index = self._hash(key)
        bucket = self.buckets[index]

        # jeśli klucz istnieje — nadpisz
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return

        # nowy klucz
        bucket.append((key, value))
        self.size += 1

        # rehash jeśli load factor > 0.75
        if self.size / self.capacity > 0.75:
            self._rehash()

    def get(self, key: str):
        index = self._hash(key)
        for k, v in self.buckets[index]:
            if k == key:
                return v
        raise KeyError(key)

    def delete(self, key: str) -> None:
        index = self._hash(key)
        bucket = self.buckets[index]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                self.size -= 1
                return
        raise KeyError(key)

    def _rehash(self) -> None:
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0
        for bucket in old_buckets:
            for key, value in bucket:
                self.put(key, value)

    def __contains__(self, key: str) -> bool:
        index = self._hash(key)
        return any(k == key for k, _ in self.buckets[index])

    def __repr__(self) -> str:
        items = []
        for bucket in self.buckets:
            for k, v in bucket:
                items.append(f"{k!r}: {v!r}")
        return '{' + ', '.join(items) + '}'


# Usage:
ht = HashTable()
ht.put("alice", 95)
ht.put("bob", 87)
ht.put("carol", 72)

print(ht.get("alice"))      # 95
print(ht.get("carol"))      # 72
print("bob" in ht)          # True
print("dave" in ht)         # False

ht.put("alice", 99)         # nadpisanie
print(ht.get("alice"))      # 99

ht.delete("bob")
print("bob" in ht)          # False
print(ht)                   # {'alice': 99, 'carol': 72}
```

> [!IMPORTANT]
> **Load factor** = `size / capacity`. Gdy przekracza **0.75**, podwajamy tablicę i przenosimy wszystkie elementy (rehash). Bez tego łańcuchy rosną i operacje stają się $O(n)$.

### Load Factor i Rehashing

```
Load Factor = n / m   (n = liczba elementów, m = rozmiar tablicy)

LF < 0.75  →  krótkie łańcuchy  →  O(1) średnio ✅
LF > 0.75  →  długie łańcuchy   →  O(n) zbliżone  ❌ → REHASH!

Rehashing:
  1. Utwórz nową tablicę 2× większą
  2. Przelicz hash % nowy_rozmiar dla KAŻDEGO elementu
  3. Wstaw elementy do nowej tablicy

  Stara (capacity=4, size=3, LF=0.75):
  [0] → [("a", 1)]
  [1] → [("b", 2), ("d", 4)]    ← łańcuch 2 elementów
  [2] → []
  [3] → [("c", 3)]

  Nowa (capacity=8, size=3, LF=0.375):  ← elementy rozrzucone
  [0] → []
  [1] → [("a", 1)]
  [2] → [("d", 4)]              ← "d" trafiło na inny indeks!
  [3] → []
  [4] → []
  [5] → [("b", 2)]              ← "b" też na innym indeksie
  [6] → [("c", 3)]
  [7] → []

  Rehash: O(n) — ale amortyzowany koszt wstawienia to O(1)
```

---

### Klasyczne problemy z Hash Map

#### Two Sum

Najpopularniejsze zadanie na LeetCode (#1). Znajdź dwa elementy, które sumują się do `target`:

```python
def two_sum(nums: list[int], target: int) -> list[int]:
    seen = {}   # wartość → indeks

    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i

    return []


# Usage:
print(two_sum([2, 7, 11, 15], 9))    # [0, 1]  (2 + 7 = 9)
print(two_sum([3, 2, 4], 6))         # [1, 2]  (2 + 4 = 6)
print(two_sum([3, 3], 6))            # [0, 1]  (3 + 3 = 6)
```

```
Wizualizacja Two Sum: nums=[2,7,11,15], target=9

i=0: num=2,  complement=7,  seen={}         → 7 ∉ seen → seen={2:0}
i=1: num=7,  complement=2,  seen={2:0}      → 2 ∈ seen ✅ → return [0, 1]

Brute force: O(n²) — sprawdź wszystkie pary
Hash Map:    O(n)  — jedno przejście!
```

> [!TIP]
> Two Sum to **wzorzec**: „czy widziałem complement?" Używaj go w wariacjach: Two Sum II (posortowana), 3Sum, 4Sum, Two Sum w BST.

#### Zliczanie częstości (Frequency Counter)

Wzorzec hash map do zliczania wystąpień — fundament wielu zadań:

```python
from collections import Counter


def top_k_frequent(nums: list[int], k: int) -> list[int]:
    count = Counter(nums)
    # sortuj po częstości malejąco, weź k pierwszych
    return [num for num, _ in count.most_common(k)]


# Usage:
print(top_k_frequent([1, 1, 1, 2, 2, 3], 2))   # [1, 2]
print(top_k_frequent([4, 4, 4, 6, 6, 2], 1))    # [4]
```

```
nums = [1, 1, 1, 2, 2, 3]

Counter:  {1: 3, 2: 2, 3: 1}
           ↑ najczęstszy

Top 2: [1, 2]
```

#### Group Anagrams

Grupuj słowa, które są anagramami (te same litery w innej kolejności):

```python
from collections import defaultdict


def group_anagrams(strs: list[str]) -> list[list[str]]:
    groups = defaultdict(list)

    for word in strs:
        # posortowane litery jako klucz — anagramy mają ten sam klucz
        key = ''.join(sorted(word))
        groups[key].append(word)

    return list(groups.values())


# Usage:
print(group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]))
# [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]
```

```
Wizualizacja Group Anagrams:

Słowo     sorted()    Klucz
"eat"  →  "aet"    →  groups["aet"] = ["eat"]
"tea"  →  "aet"    →  groups["aet"] = ["eat", "tea"]
"tan"  →  "ant"    →  groups["ant"] = ["tan"]
"ate"  →  "aet"    →  groups["aet"] = ["eat", "tea", "ate"]
"nat"  →  "ant"    →  groups["ant"] = ["tan", "nat"]
"bat"  →  "abt"    →  groups["abt"] = ["bat"]

Wynik: [["eat","tea","ate"], ["tan","nat"], ["bat"]]
```

#### First Unique Character

Znajdź pierwszy znak, który nie powtarza się w stringu:

```python
def first_unique_char(s: str) -> int:
    count = {}

    # zlicz wystąpienia
    for char in s:
        count[char] = count.get(char, 0) + 1

    # znajdź pierwszy z count == 1
    for i, char in enumerate(s):
        if count[char] == 1:
            return i

    return -1


# Usage:
print(first_unique_char("leetcode"))     # 0  ('l')
print(first_unique_char("loveleetcode")) # 2  ('v')
print(first_unique_char("aabb"))         # -1
```

---

### Python `dict` i `set` — jak działają pod spodem?

```
Python dict (CPython 3.12+):
  - Open addressing z perturbacją (nie linear probing)
  - Funkcja hash: SipHash (odporny na ataki hash flooding)
  - Load factor max: ~2/3 (0.667) — rehash przy przekroczeniu
  - Compact dict: oddzielna tablica indeksów + tablica (hash, key, value)
  - Zachowuje kolejność wstawiania (od Python 3.7+)

Python set:
  - Ta sama implementacja co dict, ale bez wartości (tylko klucze)
  - Operacje: add(), remove(), in → O(1) średnio

collections.Counter:
  - Podklasa dict specjalizowana do zliczania
  - Counter("aabbc") → Counter({'a': 2, 'b': 2, 'c': 1})

collections.defaultdict:
  - dict z domyślną wartością dla brakujących kluczy
  - defaultdict(list) → brak klucza zwraca [] zamiast KeyError
```

> [!TIP]
> W Pythonie prawie **nigdy** nie musisz implementować własnej hash table — `dict` jest zaimplementowany w C i jest wyjątkowo szybki. Znajomość wewnętrznej mechaniki jest ważna na rozmowach rekrutacyjnych i do rozumienia złożoności.

### Hash Table vs inne struktury

| Operacja | Hash Table | Posortowana tablica | BST (zbalansowane) | Linked List |
|---|---|---|---|---|
| Wyszukiwanie | $O(1)$ avg | $O(\log n)$ | $O(\log n)$ | $O(n)$ |
| Wstawianie | $O(1)$ avg | $O(n)$ | $O(\log n)$ | $O(1)$ |
| Usuwanie | $O(1)$ avg | $O(n)$ | $O(\log n)$ | $O(n)$ |
| Min/Max | $O(n)$ | $O(1)$ | $O(\log n)$ | $O(n)$ |
| Posortowane dane | ❌ Nie | ✅ Tak | ✅ Tak | ❌ Nie |
| Worst case | $O(n)$ | $O(\log n)$ | $O(\log n)$ | $O(n)$ |

> [!WARNING]
> Hash Table **nie zachowuje porządku** (nawet jeśli Python `dict` zachowuje kolejność wstawiania, to nie jest porządek sortowania). Jeśli potrzebujesz posortowanych danych → użyj BST lub `SortedDict` z modułu `sortedcontainers`.

### Podsumowanie Hashing

| Problem / Wzorzec | Złożoność | Kluczowa technika |
|---|---|---|
| Two Sum | $O(n)$ | `complement in seen` |
| Frequency Counter | $O(n)$ | `Counter()` / `dict.get()` |
| Group Anagrams | $O(n \cdot k \log k)$ | Sorted key → `defaultdict(list)` |
| First Unique | $O(n)$ | Dwa przejścia: zlicz + znajdź |
| Deduplikacja | $O(n)$ | `set()` |
| Implementacja Hash Table | — | Chaining / Open addressing + rehash |

📎 Powiązany artykuł: [Hash Map Sum Problems](hash-map-sum-problems.md)

---

## 10. Topological Sort (sortowanie topologiczne)

**Kategoria:** grafy skierowane (DAG)

Liniowe uporządkowanie wierzchołków grafu skierowanego acyklicznego (DAG) tak, aby dla każdej krawędzi $(u, v)$ wierzchołek $u$ występował przed $v$.

**Dwie klasyczne implementacje:**
- **DFS + stos** — algorytm oparty na DFS (Tarjan).
- **BFS + in-degree** — algorytm Kahna z kolejką.

**Dlaczego jest ważny?**
- Rozwiązywanie zależności: kompilacja (Makefile), menedżery pakietów (pip, npm), planowanie zadań.
- Wykrywanie cykli w grafie skierowanym.
- Fundament w: harmonogramowaniu kursów (Course Schedule), pipeline'ach CI/CD.

**Złożoność:** $O(V + E)$

---

## Podsumowanie

| # | Algorytm | Kategoria | Złożoność (typowa) |
|---|---|---|---|
| 1 | Binary Search | Wyszukiwanie | $O(\log n)$ |
| 2 | Merge Sort / Quick Sort | Sortowanie | $O(n \log n)$ |
| 3 | BFS | Przeszukiwanie grafów | $O(V + E)$ |
| 4 | DFS | Przeszukiwanie grafów | $O(V + E)$ |
| 5 | Dijkstra | Najkrótsza ścieżka | $O((V+E) \log V)$ |
| 6 | Dynamic Programming | Paradygmat | zależna od problemu |
| 7 | Tree Traversal | Drzewa | $O(n)$ |
| 8 | Greedy Algorithms | Paradygmat | zależna od problemu |
| 9 | Hashing | Struktury danych | $O(1)$ średnio |
| 10 | Topological Sort | Grafy (DAG) | $O(V + E)$ |

> [!TIP]
> Ta lista to punkt wyjścia. Następnym krokiem będzie implementacja każdego z tych algorytmów w Pythonie — krok po kroku, z wizualizacjami i testami.

**Powiązane tematy:**

- [Implementacje Binary Search](implementacje-binary-search.md)
- [Implementacje ciągu Fibonacci](implementacje-ciagu-fibonacci.md)
- [BFS i DFS na gridzie](bfs-dfs-na-gridzie.md)
- [Sliding Window](sliding-window.md)
- [Hash Map Sum Problems](hash-map-sum-problems.md)
