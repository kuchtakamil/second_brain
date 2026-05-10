# BFS i DFS na gridzie

**Grid = graf niejawny.** Każda komórka `(row, col)` to wierzchołek, a krawędzie prowadzą do 4 sąsiadów (góra, dół, lewo, prawo) — o ile są w granicach siatki i są przejezdne. Dwa podstawowe algorytmy przeszukiwania takiego grafu to **BFS** i **DFS**.

---

## BFS (Breadth-First Search)

**BFS (przeszukiwanie wszerz)** eksploruje wierzchołki **warstwa po warstwie** — najpierw wszystkie sąsiednie, potem sąsiadów sąsiadów itd. Dzięki temu BFS zawsze znajduje **najkrótszą ścieżkę** (w sensie liczby kroków) w grafie nieważonym.

---

## Kiedy stosować BFS na gridzie?

- Szukasz **najkrótszej ścieżki** między dwoma komórkami (w sensie liczby ruchów).
- Komórki mają jednakowy "koszt" przejścia (graf nieważony).
- Musisz **zbadać wszystkie komórki** osiągalne z danego startu (np. znaleźć spójne wyspy, wypełnić flood-fill itp.).

> [!TIP]
> Jeśli krawędzie mają różne wagi — zamiast BFS użyj algorytmu Dijkstry.

---

## Schemat BFS na gridzie

```python
from collections import deque

def bfs_grid(grid, start_row, start_col):
    rows, cols = len(grid), len(grid[0])
    visited = set()
    visited.add((start_row, start_col))
    queue = deque([(start_row, start_col, 0)])   # (wiersz, kolumna, dystans)

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # góra, dół, lewo, prawo

    while queue:
        row, col, distance = queue.popleft()

        # --- tutaj sprawdzasz warunek celu ---

        for d_row, d_col in directions:
            new_row, new_col = row + d_row, col + d_col
            if 0 <= new_row < rows and 0 <= new_col < cols and (new_row, new_col) not in visited and grid[new_row][new_col] == '0':
                visited.add((new_row, new_col))
                queue.append((new_row, new_col, distance + 1))

    return -1  # cel nieosiągalny
```

### Kluczowe elementy

| Element | Rola |
|---|---|
| `deque` (kolejka) | Zapewnia przetwarzanie FIFO — najpierw bliższe komórki |
| `visited` | Zapobiega wielokrotnemu odwiedzaniu tej samej komórki (i nieskończonym pętlom) |
| `directions` | Cztery możliwe ruchy: ↑ ↓ ← → |
| `distance` | Dystans od startu — rośnie o 1 z każdą warstwą BFS |

> [!IMPORTANT]
> Komórkę dodajemy do `visited` **w momencie wkładania do kolejki**, a nie w momencie wyjmowania. To zapobiega wielokrotnym wstawkom tej samej komórki (duplikatom w kolejce), co poprawia zarówno wydajność, jak i poprawność algorytmu.

---

## 🔍 Wizualizacja BFS (warstwa po warstwie)

```
Grid:            BFS od (0,0):

0 0 + 0          0 1 . .     ← warstwa 0, potem 1
0 + + 0          1 . . .     ← ...
0 0 0 0          2 3 4 5     ← itd.
+ 0 + 0          . 4 . 6
```

BFS odwiedza komórki w kolejności rosnącego dystansu — dlatego pierwsza znaleziona komórka celu jest jednocześnie najbliższą.

---

## Zadanie: Najkrótszy BFS z rogu do rogu

> Mamy siatkę 2D złożoną z `'0'` (przejezdne) i `'+'` (zablokowane). Startujemy z jednego rogu siatki. Trzeba dotrzeć do **dowolnego innego przejezdnego rogu** z **minimalnym dystansem**. Zwróć współrzędne celu lub `-1`, jeśli to niemożliwe.

### Analiza

1. **Rogi siatki** mają współrzędne: `(0,0)`, `(0, cols-1)`, `(rows-1, 0)`, `(rows-1, cols-1)`.
2. Start to jeden z rogów. Cele to **pozostałe rogi**, ale tylko jeśli są przejezdne (`'0'`).
3. BFS gwarantuje, że pierwszy osiągnięty róg ma minimalny dystans.

### Rozwiązanie

```python
from collections import deque

def shortest_corner_path(grid: list[list[str]], start_row: int, start_col: int) -> tuple | int:
    rows, cols = len(grid), len(grid[0])

    # all four corners
    corners = {(0, 0), (0, cols - 1), (rows - 1, 0), (rows - 1, cols - 1)}
    corners.discard((start_row, start_col))  # remove start corner

    # start must be passable
    if grid[start_row][start_col] != '0':
        return -1

    visited = set()
    visited.add((start_row, start_col))
    queue = deque([(start_row, start_col, 0)])

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        row, col, distance = queue.popleft()

        # check if we reached a target corner
        if (row, col) in corners and grid[row][col] == '0':
            return (row, col)

        for d_row, d_col in directions:
            new_row, new_col = row + d_row, col + d_col
            if 0 <= new_row < rows and 0 <= new_col < cols and (new_row, new_col) not in visited and grid[new_row][new_col] == '0':
                visited.add((new_row, new_col))
                queue.append((new_row, new_col, distance + 1))

    return -1  # no reachable corner
```

### Krok po kroku na przykładzie

```
Grid (4×4):         Start: (0, 0)

0  0  +  0          Rogi: (0,0)✓start  (0,3)  (3,0)  (3,3)
0  +  +  0
0  0  0  0
+  0  +  0

BFS:
Warstwa 0:  (0,0)
Warstwa 1:  (0,1), (1,0)
Warstwa 2:  (2,0)            ← (0,2) zablokowane, (1,1) zablokowane
Warstwa 3:  (2,1), (3,0)←ZABLOKOWANY
Warstwa 4:  (2,2), (3,1)
Warstwa 5:  (2,3)
Warstwa 6:  (1,3), (3,3)←ZABLOKOWANY

Pierwszy osiągalny róg: (1,3) → nie jest rogiem.
Korekta: (0,3)? Sprawdźmy: grid[0][3] = '0', ale jest zablokowana droga od (1,3)?
Nie — (0,3) sąsiaduje z (1,3) ← BFS w warstwie 7: (0,3) ✅

Wynik: (0, 3)
```

### Testy

```python
grid1 = [
    ['0', '0', '+', '0'],
    ['0', '+', '+', '0'],
    ['0', '0', '0', '0'],
    ['+', '0', '+', '0'],
]
print(shortest_corner_path(grid1, 0, 0))  # (0, 3) or (3, 3)

# Grid without reachable corner
grid2 = [
    ['0', '+'],
    ['+', '0'],
]
print(shortest_corner_path(grid2, 0, 0))  # -1

# Direct neighbor corner
grid3 = [
    ['0', '0'],
    ['0', '0'],
]
print(shortest_corner_path(grid3, 0, 0))  # (0, 1) or (1, 0) — distance 1
```

---

## Złożoność

| | Wartość |
|---|---|
| **Czasowa** | $O(R \times C)$ — każda komórka odwiedzana co najwyżej raz |
| **Pamięciowa** | $O(R \times C)$ — zbiór `visited` + kolejka |

---

## DFS (Depth-First Search)

**DFS (przeszukiwanie w głąb)** eksploruje jedną ścieżkę tak daleko jak się da, a dopiero potem cofa się i próbuje kolejną gałąź. DFS **nie gwarantuje** najkrótszej ścieżki, ale zużywa mniej pamięci i jest naturalny w problemach, gdzie trzeba **odwiedzić lub oznaczyć cały spójny obszar** (np. zliczanie wysp, flood-fill).

**Kiedy stosować DFS na gridzie?**

- Chcesz **odwiedzić wszystkie komórki** spójnego obszaru (wyspy, regiony).
- Nie potrzebujesz najkrótszej ścieżki — wystarczy Ci informacja, czy cel jest osiągalny.
- Potrzebujesz **rekurencyjnego** podejścia (prostszy kod).

> [!TIP]
> Jeśli potrzebujesz najkrótszej ścieżki — użyj BFS. DFS świetnie nadaje się do problemów typu "odwiedź cały spójny komponent".

---

### Schemat DFS na gridzie (rekurencyjny)

```python
def dfs_grid(grid, row, col, visited):
    rows, cols = len(grid), len(grid[0])

    # out of bounds, already visited, or blocked
    if row < 0 or row >= rows or col < 0 or col >= cols:
        return
    if (row, col) in visited or grid[row][col] == '+':
        return

    visited.add((row, col))

    # explore all 4 neighbors
    dfs_grid(grid, row - 1, col, visited)  # góra
    dfs_grid(grid, row + 1, col, visited)  # dół
    dfs_grid(grid, row, col - 1, visited)  # lewo
    dfs_grid(grid, row, col + 1, visited)  # prawo
```

**Kluczowa różnica vs BFS:** zamiast kolejki FIFO mamy **stos wywołań rekurencyjnych** (LIFO) — algorytm "wchodzi w głąb" jednej ścieżki, zanim wróci do rozwidlenia.

---

### Schemat DFS na gridzie (iteracyjny)

Dla dużych gridów rekurencja może spowodować `RecursionError`. Wersja iteracyjna używa jawnego stosu:

```python
def dfs_grid_iterative(grid, start_row, start_col):
    rows, cols = len(grid), len(grid[0])
    visited = set()
    stack = [(start_row, start_col)]

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while stack:
        row, col = stack.pop()

        if (row, col) in visited:
            continue
        visited.add((row, col))

        # --- tutaj przetwarzasz komórkę ---

        for d_row, d_col in directions:
            new_row, new_col = row + d_row, col + d_col
            if 0 <= new_row < rows and 0 <= new_col < cols and (new_row, new_col) not in visited and grid[new_row][new_col] == '0':
                stack.append((new_row, new_col))

    return visited
```

> [!IMPORTANT]
> W iteracyjnym DFS `visited` sprawdzamy przy **zdejmowaniu ze stosu** (nie przy wkładaniu), bo na stos mogą trafić duplikaty. Alternatywnie można dodawać do `visited` przy wkładaniu — wtedy kolejność odwiedzin będzie inna, ale poprawność zachowana.

---

### Zadanie: Number of Islands (zliczanie wysp)

> Mamy siatkę 2D złożoną z `'1'` (ląd) i `'0'` (woda). **Wyspa** to grupa sąsiadujących komórek `'1'` (góra, dół, lewo, prawo). Policz liczbę wysp.

**Przykład:**

```text
1 1 0 0 0
1 1 0 0 0
0 0 1 0 0
0 0 0 1 1

Odpowiedź: 3
```

**Podejście:** iterujemy po gridzie. Gdy napotkamy nieodwiedzone `'1'`, uruchamiamy DFS, który oznaczy całą wyspę jako odwiedzoną. Każde takie uruchomienie DFS = +1 wyspa.

```python
def num_islands(grid: list[list[str]]) -> int:
    if not grid:
        return 0

    rows, cols = len(grid), len(grid[0])
    visited = set()
    island_count = 0

    def dfs(row, col):
        if row < 0 or row >= rows or col < 0 or col >= cols:
            return
        if (row, col) in visited or grid[row][col] == '0':
            return

        visited.add((row, col))
        dfs(row - 1, col)
        dfs(row + 1, col)
        dfs(row, col - 1)
        dfs(row, col + 1)

    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == '1' and (row, col) not in visited:
                dfs(row, col)
                island_count += 1

    return island_count

# Usage:
grid = [
    ['1', '1', '0', '0', '0'],
    ['1', '1', '0', '0', '0'],
    ['0', '0', '1', '0', '0'],
    ['0', '0', '0', '1', '1'],
]
print(num_islands(grid))  # 3
```

**Złożoność:** $O(R \times C)$ czasowa i pamięciowa.

---

## BFS vs DFS na gridzie

| Cecha | BFS | DFS |
|---|---|---|
| Struktura danych | Kolejka (FIFO) | Stos / rekurencja (LIFO) |
| Gwarantuje najkrótszą ścieżkę? | ✅ Tak | ❌ Nie |
| Zużycie pamięci | Większe (cała warstwa w kolejce) | Mniejsze (tylko aktualna gałąź) |
| Typowe zastosowania | Najkrótsza ścieżka, poziomy grafu | Wykrywanie cykli, topological sort, DFS wysp |

---

## Podsumowanie

- **Grid → graf niejawny** — komórki to wierzchołki, ruchy ↑↓←→ to krawędzie.
- **BFS** gwarantuje najkrótszą ścieżkę — idealne do "znajdź closest X".
- **DFS** odwiedza cały spójny komponent — idealne do "policz wyspy / oznacz region".
- Zawsze pamiętaj o zbiorze `visited`, żeby uniknąć nieskończonych pętli.

**Powiązane tematy:**

- [Sliding Window](sliding-window.md)
- [Tablice dwuwymiarowe w Pythonie](tablice-dwuwymiarowe-w-pythonie.md)
