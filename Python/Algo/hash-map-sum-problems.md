# Hash Map – zadania sumacyjne

Klasyczne zadania z rozmów kwalifikacyjnych oparte na wzorcu **hash map** (słownik) i pochodnych (prefix sum, bucket sort). Wspólny motyw: zamiast sprawdzać każdą parę/trójkę w pętli $O(n^2)$ lub $O(n^3)$, używamy słownika, żeby w $O(1)$ sprawdzić, czy brakujący element już widzieliśmy.

---

## 1. Two Sum

Mając listę liczb `nums` i cel `target`, zwróć indeksy dwóch liczb, które sumują się do `target`.

**Przykład:** `nums = [2, 7, 11, 15]`, `target = 9` → `[0, 1]`

> Liczby **nie muszą sąsiadować** — szukamy dowolnych dwóch indeksów `i ≠ j`.

**Idea:** dla każdego elementu `x` sprawdź, czy `target - x` jest już w słowniku.

**Złożoność:** $O(n)$ czasowa, $O(n)$ pamięciowa

```python
# Wariant klasyczny – zwraca pierwszą znalezioną parę
def two_sum(nums: list[int], target: int) -> list[int]:
    seen = {}  # value -> index

    for i, x in enumerate(nums):
        complement = target - x
        if complement in seen:
            return [seen[complement], i]
        seen[x] = i

    return []

# Usage:
print(two_sum([2, 7, 11, 15], 9))   # [0, 1]
print(two_sum([3, 2, 4], 6))        # [1, 2]
print(two_sum([3, 3], 6))           # [0, 1]
```

```python
# Wariant – zwraca WSZYSTKIE pary indeksów
def two_sum_all(nums: list[int], target: int) -> list[list[int]]:
    seen = {}   # value -> list of indices (może być wielokrotność tej samej wartości)
    result = []

    for i, x in enumerate(nums):
        complement = target - x
        if complement in seen:
            for j in seen[complement]:  # każdy poprzedni indeks z tą wartością
                result.append([j, i])
        seen.setdefault(x, []).append(i)
        # to samo co:
        # if x not in seen:
        # seen[x] = []
        # seen[x].append(i)


    return result

# Usage:
print(two_sum_all([2, 7, 2, 11], 9))    # [[0, 1], [2, 1]] – dwie pary (2+7)
print(two_sum_all([1, 5, 3, 3, 3], 6))  # [[1,2],[1,3],[1,4]] – trzy pary (5+... nie, 3+3)
print(two_sum_all([1, 2, 3], 10))       # []
```

---

## 2. Three Sum

Mając listę `nums`, znajdź wszystkie **unikalne** trójki `[a, b, c]` takie, że `a + b + c == 0`.

**Przykład:** `nums = [-1, 0, 1, 2, -1, -4]` → `[[-1, -1, 2], [-1, 0, 1]]`

**Złożoność:** $O(n^2)$ czasowa, $O(1)$ pamięciowa (bez wyjściowej listy)

### Intuicja

Naiwne rozwiązanie — trzy zagnieżdżone pętle — daje $O(n^3)$. Możemy zejść do $O(n^2)$ kombinując dwie techniki:

**Krok 1 — Sortowanie.** Po posortowaniu tablicy zyskujemy dwie rzeczy:
- wiemy, że `nums[left] ≤ nums[right]`, więc możemy świadomie przesuwać wskaźniki,
- łatwo pomijamy duplikaty — jednakowe wartości leżą obok siebie.

**Krok 2 — Kotwica + Two Pointers.** Zewnętrzna pętla `for` ustala **kotwicę** (`anchor`) — jeden z trzech elementów. Dla pozostałych dwóch używamy dwóch wskaźników: `left` (tuż za kotwicą) i `right` (koniec tablicy).

```
posortowana:  [-4, -1, -1, 0, 1, 2]
               ^anchor  ^left      ^right
```

W każdej iteracji wewnętrznej sprawdzamy `current_sum = anchor + nums[left] + nums[right]`:

| `current_sum` | co robimy | dlaczego |
|---|---|---|
| `== 0` | zapisujemy trójkę, `left += 1` | znaleźliśmy parę — szukamy kolejnej |
| `< 0` | `left += 1` | suma za mała — potrzebujemy większej liczby z lewej |
| `> 0` | `right -= 1` | suma za duża — potrzebujemy mniejszej liczby z prawej |

**Krok 3 — Pomijanie duplikatów.** Zadanie wymaga **unikalnych** trójek, więc po każdym kroku przeskakujemy powtarzające się wartości — zarówno na poziomie kotwicy, jak i wskaźnika `left`.

```python
def three_sum(nums: list[int]) -> list[list[int]]:
    nums.sort()
    result = []

    for anchor_idx, anchor in enumerate(nums):
        # skip duplicate values for the anchor element
        if anchor_idx > 0 and nums[anchor_idx] == nums[anchor_idx - 1]:
            continue

        left, right = anchor_idx + 1, len(nums) - 1
        while left < right:
            current_sum = anchor + nums[left] + nums[right]
            if current_sum == 0:
                result.append([anchor, nums[left], nums[right]])
                left += 1
                # skip duplicates for the left pointer
                while left < right and nums[left] == nums[left - 1]:
                    left += 1
            elif current_sum < 0:
                left += 1
            else:
                right -= 1

    return result

# Usage:
print(three_sum([-1, 0, 1, 2, -1, -4]))  # [[-1, -1, 2], [-1, 0, 1]]
print(three_sum([0, 0, 0]))              # [[0, 0, 0]]
print(three_sum([1, 2, -2, -1]))         # []
```

### Kiedy sortowanie jest niedozwolone?

Sortowanie jest ok, gdy zadanie pyta o **wartości** (jak klasyczny LeetCode 15). Sortowanie **niszczy oryginalne indeksy**, więc jeśli zadanie żąda **trójek indeksów** — nie możemy tego zrobić.

### Wariant: Three Sum — zwróć indeksy

Mając listę `nums`, zwróć wszystkie trójki indeksów `(i, j, k)` takie, że `i < j < k` i `nums[i] + nums[j] + nums[k] == 0`.

**Złożoność:** $O(n^2)$ czasowa, $O(n)$ pamięciowa

#### Intuicja

Zewnętrzna pętla ustala **kotwicę** `anchor_idx`. Dla każdej kotwicy przeglądamy pozostałe elementy pętlą wewnętrzną — jak w Two Sum All Pairs, z tym że `seen` mapuje `wartość → indeks`.

Kluczowa obserwacja: gdy jesteśmy na pozycji `j`, słownik `seen` zawiera **tylko indeksy między `anchor_idx + 1` a `j - 1`**. Dzięki temu znaleziony indeks `k` spełnia zawsze `anchor_idx < k < j` — trójka `(anchor_idx, k, j)` jest już z definicji posortowana rosnąco, bez sortowania tablicy.

```
nums = [0, -1, 2, -3, 1]

anchor_idx=0 (anchor=0):
  j=1  seen={}           szukam -(0 + -1) =  1  → nie ma; seen={-1: 1}
  j=2  seen={-1:1}       szukam -(0 +  2) = -2  → nie ma; seen={-1:1, 2:2}
  j=3  seen={-1:1, 2:2}  szukam -(0 + -3) =  3  → nie ma; seen={...,-3:3}
  j=4  seen={...}        szukam -(0 +  1) = -1  → JEST! k=1
                         → trójka (0, 1, 4): nums=[0,-1,1] ✓
```

```python
def three_sum_indices(nums: list[int]) -> list[tuple[int, int, int]]:
    result = []

    for anchor_idx in range(len(nums) - 2):
        # seen maps value -> index, reset for each anchor
        seen: dict[int, int] = {}

        for j in range(anchor_idx + 1, len(nums)):
            complement = -(nums[anchor_idx] + nums[j])

            if complement in seen:
                # seen[complement] is index k, where anchor_idx < k < j
                result.append((anchor_idx, seen[complement], j))

            # add AFTER the lookup to avoid using j as its own complement
            seen[nums[j]] = j

    return result

# Usage:
print(three_sum_indices([0, -1, 2, -3, 1]))  # [(0, 1, 4), (0, 2, 3)]
print(three_sum_indices([-1, 0, 1, 2]))      # [(0, 1, 2)]
print(three_sum_indices([1, 2, 3]))          # []
```

> **Uwaga:** jeśli `nums` zawiera duplikaty wartości, wynik może zawierać trójki o tych samych wartościach, ale **różnych indeksach** — to poprawne zachowanie, bo zadanie pyta o indeksy, nie o unikalne wartości.

---

## 3. Subarray Sum Equals K

Mając listę `nums` i liczbę `k`, zwróć **liczbę** ciągłych podtablic, których suma wynosi `k`.

**Przykład:** `nums = [1, 2, 3]`, `k = 3` → `2` (podtablice `[1,2]` i `[3]`)

**Złożoność:** $O(n)$ czasowa, $O(n)$ pamięciowa

### Krok 1 — Co to jest prefix sum?

**Prefix sum** (suma prefiksowa) w pozycji `i` to suma **wszystkich elementów od początku tablicy do indeksu `i` włącznie**.

```
nums    =  [1,  2,  3,  4]
prefix  =  [1,  3,  6, 10]
            ↑   ↑   ↑   ↑
           1  1+2 1+2+3 1+2+3+4
```

### Krok 2 — Jak prefix sum pomaga znaleźć sumę podtablicy?

Suma elementów między indeksami `j+1` a `i` to:

```
suma[j+1..i] = prefix[i] - prefix[j]
```

Przykład: suma `[2, 3]` (indeksy 1–2):
```
prefix[2] - prefix[0] = 6 - 1 = 5  ✓  (2+3=5)
```

Czyli zamiast sumować od nowa za każdym razem, **odejmujemy dwa prefiksy**.

### Krok 3 — Kiedy podtablica ma sumę = k?

Szukamy par `(j, i)` takich, że:

```
prefix[i] - prefix[j] == k
```

Co to samo co:

```
prefix[j] == prefix[i] - k
```

Dla każdego `i` znamy `prefix[i]`. Pytamy: **ile razy widzieliśmy wcześniej wartość `prefix[i] - k`?** — każde takie wystąpienie odpowiada jednej podtablicy kończącej się na `i`, której suma = `k`.

### Krok 4 — Śledź prefiksy słownikiem (nie tablicą)

Zamiast budować pełną tablicę prefixów, przechodzimy po `nums` i na bieżąco:
1. obliczamy `prefix += x` (bieżąca suma prefiksowa)
2. sprawdzamy, ile razy `prefix - k` już widzieliśmy → dodajemy do wyniku
3. zapisujemy bieżący `prefix` w słowniku

### Ślad wykonania

```
nums = [1, 2, 3],  k = 3
counts = {0: 1}   ← "pusty prefiks" (suma = 0) widziany raz — patrz niżej
prefix = 0,  result = 0

i=0  x=1:  prefix=1,  szukam 1-3=-2  → counts[-2]=0  result=0;  counts={0:1, 1:1}
i=1  x=2:  prefix=3,  szukam 3-3= 0  → counts[0] =1  result=1;  counts={0:1,1:1,3:1}
i=2  x=3:  prefix=6,  szukam 6-3= 3  → counts[3] =1  result=2;  counts={...,6:1}

wynik: 2  ✓  ([1,2] i [3])
```

### Dlaczego `counts[0] = 1`?

Jeśli podtablica zaczyna się od indeksu `0`, to `prefix[j]` odpowiada "pustemu prefiksowi" (suma = 0 **przed** pierwszym elementem). Bez `counts[0] = 1` takie podtablice nie byłyby zliczane.

**Przykład:** `nums = [3]`, `k = 3` → szukamy `prefix[0] - k = 3 - 3 = 0`. Bez `counts[0]=1` wynik = 0 zamiast 1.

```python
from collections import defaultdict

def subarray_sum(nums: list[int], k: int) -> int:
    counts = defaultdict(int)
    counts[0] = 1  # "empty prefix" before index 0
    prefix = 0
    result = 0

    for x in nums:
        prefix += x
        # how many earlier prefixes satisfy: current_prefix - earlier_prefix == k?
        result += counts[prefix - k]
        counts[prefix] += 1

    return result

# Usage:
print(subarray_sum([1, 1, 1], 2))      # 2
print(subarray_sum([1, 2, 3], 3))      # 2  ([1,2] i [3])
print(subarray_sum([-1, -1, 1], 0))    # 1
```

---

## 4. Product of Array Except Self

Mając listę `nums`, zwróć listę `output`, gdzie `output[i]` to iloczyn wszystkich elementów z `nums` poza `nums[i]`. **Bez użycia dzielenia.**

**Przykład:** `nums = [1, 2, 3, 4]` → `[24, 12, 8, 6]`

**Idea:** dwa przebiegi — **prefix product** (iloczyn od lewej) i **suffix product** (iloczyn od prawej). Wynik dla pozycji `i` = prefix[i] × suffix[i].

**Złożoność:** $O(n)$ czasowa, $O(1)$ dodatkowej pamięci (poza wyjściową listą)

```python
def product_except_self(nums: list[int]) -> list[int]:
    n = len(nums)
    output = [1] * n

    # forward pass: output[i] = product of all elements to the left
    prefix = 1
    for i in range(n):
        output[i] = prefix
        prefix *= nums[i]

    # backward pass: multiply by product of all elements to the right
    suffix = 1
    for i in range(n - 1, -1, -1):
        output[i] *= suffix
        suffix *= nums[i]

    return output

# Usage:
print(product_except_self([1, 2, 3, 4]))   # [24, 12, 8, 6]
print(product_except_self([-1, 1, 0, -3, 3]))  # [0, 0, 9, 0, 0]
```

---

## 5. Top K Frequent Elements

Mając listę `nums` i liczbę `k`, zwróć `k` najczęściej występujących elementów.

**Przykład:** `nums = [1, 1, 1, 2, 2, 3]`, `k = 2` → `[1, 2]`

**Idea:** zlicz częstości słownikiem, a następnie użyj **bucket sort** — wiadra indeksowane częstością (od 0 do n). Zbieraj elementy od najliczniejszego wiadra.

**Złożoność:** $O(n)$ czasowa, $O(n)$ pamięciowa

```python
def top_k_frequent(nums: list[int], k: int) -> list[int]:
    count = {}
    for x in nums:
        count[x] = count.get(x, 0) + 1

    # buckets[i] = list of numbers that appear exactly i times
    buckets: list[list[int]] = [[] for _ in range(len(nums) + 1)]
    for num, freq in count.items():
        buckets[freq].append(num)

    result = []
    for freq in range(len(buckets) - 1, 0, -1):
        for num in buckets[freq]:
            result.append(num)
            if len(result) == k:
                return result

    return result

# Usage:
print(top_k_frequent([1, 1, 1, 2, 2, 3], 2))  # [1, 2]
print(top_k_frequent([1], 1))                  # [1]
```

---

## Podsumowanie

| Problem | Kluczowa technika | Złożoność czas. |
|---|---|---|
| **Two Sum** | Hash map `wartość → indeks` | $O(n)$ |
| **Three Sum** | Sortowanie + Two Pointers | $O(n^2)$ |
| **Subarray Sum Equals K** | Prefix Sum + Hash map licznika | $O(n)$ |
| **Product of Array Except Self** | Prefix × Suffix product | $O(n)$ |
| **Top K Frequent Elements** | Hash map + Bucket Sort | $O(n)$ |

**Powiązane tematy:**

- [Sliding Window](sliding-window.md)
- [Implementacje Binary Search](implementacje-binary-search.md)
- [Tablice dwuwymiarowe w Pythonie](tablice-dwuwymiarowe-w-pythonie.md)
