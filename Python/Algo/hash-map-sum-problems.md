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

    return result

# Usage:
print(two_sum_all([2, 7, 2, 11], 9))    # [[0, 1], [2, 1]] – dwie pary (2+7)
print(two_sum_all([1, 5, 3, 3, 3], 6))  # [[1,2],[1,3],[1,4]] – trzy pary (5+... nie, 3+3)
print(two_sum_all([1, 2, 3], 10))       # []
```

---

## 2. Three Sum

Mając listę `nums`, znajdź wszystkie unikalne trójki `[a, b, c]` takie, że `a + b + c == 0`.

**Przykład:** `nums = [-1, 0, 1, 2, -1, -4]` → `[[-1, -1, 2], [-1, 0, 1]]`

**Idea:** posortuj tablicę, iteruj po pierwszym elemencie (`a`), a dla pozostałych dwóch użyj techniki **two pointers** (lewa/prawa granica). Pomijaj duplikaty po każdym kroku.

**Złożoność:** $O(n^2)$ czasowa, $O(1)$ pamięciowa (bez wyjściowej listy)

```python
def three_sum(nums: list[int]) -> list[list[int]]:
    nums.sort()
    result = []

    for i, a in enumerate(nums):
        # skip duplicate values for the first element
        if i > 0 and nums[i] == nums[i - 1]:
            continue

        left, right = i + 1, len(nums) - 1
        while left < right:
            s = a + nums[left] + nums[right]
            if s == 0:
                result.append([a, nums[left], nums[right]])
                left += 1
                # skip duplicates for the second element
                while left < right and nums[left] == nums[left - 1]:
                    left += 1
            elif s < 0:
                left += 1
            else:
                right -= 1

    return result

# Usage:
print(three_sum([-1, 0, 1, 2, -1, -4]))  # [[-1, -1, 2], [-1, 0, 1]]
print(three_sum([0, 0, 0]))              # [[0, 0, 0]]
print(three_sum([1, 2, -2, -1]))         # []
```

---

## 3. Subarray Sum Equals K

Mając listę `nums` i liczbę `k`, zwróć liczbę ciągłych podtablic, których suma wynosi `k`.

**Przykład:** `nums = [1, 1, 1]`, `k = 2` → `2`

**Idea:** użyj **prefix sum** (suma prefiksowa). Dla każdego indeksu `i` oblicz `prefix[i]`. Podtablica `[j+1..i]` ma sumę `k` wtedy i tylko wtedy, gdy `prefix[i] - prefix[j] == k`, czyli `prefix[j] == prefix[i] - k`. Zliczaj widziane prefiksy w słowniku.

**Złożoność:** $O(n)$ czasowa, $O(n)$ pamięciowa

```python
from collections import defaultdict

def subarray_sum(nums: list[int], k: int) -> int:
    counts = defaultdict(int)
    counts[0] = 1  # empty prefix (sum = 0) seen once
    prefix = 0
    result = 0

    for x in nums:
        prefix += x
        # how many prefixes ended with (prefix - k)?
        result += counts[prefix - k]
        counts[prefix] += 1

    return result

# Usage:
print(subarray_sum([1, 1, 1], 2))      # 2
print(subarray_sum([1, 2, 3], 3))      # 2  ([1,2] and [3])
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
