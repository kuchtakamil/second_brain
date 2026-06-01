# Jak rozpoznać złożoność O(log n) i O(n log n)

Złożoności O(1), O(n), O(n²) i O(n³) są intuicyjne — wystarczy policzyć zagnieżdżone pętle. Złożoności logarytmiczne (O(log n)) i liniowo-logarytmiczne (O(n log n)) bywają mniej oczywiste, ale opierają się na jednym prostym mechanizmie: **dzieleniu problemu na mniejsze części**.

---

## Skąd się bierze logarytm?

Logarytm odpowiada na pytanie: **ile razy muszę podzielić n przez stałą (najczęściej 2), żeby dojść do 1?**

```
n = 16
16 → 8 → 4 → 2 → 1   ←  4 kroki  =  log₂(16) = 4
```

Kiedy algorytm w każdym kroku **odrzuca stałą frakcję danych** (np. połowę), wykonuje O(log n) kroków. To właśnie jest serce logarytmicznej złożoności.

---

## O(log n) — jak rozpoznać

### Reguła ogólna

> Jeśli w każdej iteracji rozmiar problemu **dzieli się** przez stałą (najczęściej 2), złożoność wynosi O(log n).

### Wzorzec 1: Wyszukiwanie binarne

Klasyczny przykład. Na posortowanej tablicy w każdym kroku odrzucamy połowę:

```python
def binary_search(arr, target):
    lo, hi = 0, len(arr) - 1
    while lo <= hi:               # ile razy ta pętla się wykona?
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            lo = mid + 1          # odrzucamy lewą połowę
        else:
            hi = mid - 1          # odrzucamy prawą połowę
    return -1
```

Zakres `[lo, hi]` kurczy się o połowę w każdej iteracji. Jeśli tablica ma 1 000 000 elementów, pętla wykona się co najwyżej ~20 razy (log₂(1 000 000) ≈ 20). **Nie 1 000 000 razy, lecz 20.**

### Wzorzec 2: Pętla z mnożeniem / dzieleniem indeksu

Drugi klasyczny sygnał — pętla, w której zmienna sterująca **nie jest inkrementowana o 1**, lecz mnożona lub dzielona:

```python
# O(log n) — zmienna i podwaja się w każdym kroku
i = 1
while i < n:
    print(i)
    i *= 2        # 1, 2, 4, 8, 16, ... → log₂(n) kroków

# O(log n) — zmienna i dzieli się w każdym kroku
i = n
while i >= 1:
    print(i)
    i //= 2       # n, n/2, n/4, ... → log₂(n) kroków
```

Kluczowy sygnał: `i *= 2`, `i //= 2`, `i *= 3`, `i //= 3` itp.

### Wzorzec 3: Rekurencja z podziałem problemu (jedna gałąź)

Jeśli funkcja rekurencyjna w każdym wywołaniu przetwarza **jedną** połówkę danych:

```python
def find_peak(arr, lo, hi):
    if lo == hi:
        return lo
    mid = (lo + hi) // 2
    if arr[mid] < arr[mid + 1]:
        return find_peak(arr, mid + 1, hi)   # tylko prawa połowa
    else:
        return find_peak(arr, lo, mid)        # tylko lewa połowa
```

Jedno wywołanie rekurencyjne, rozmiar problemu ½ → O(log n).

### Wzorzec 4: Struktury drzew zbalansowanych

Operacje na zbalansowanych drzewach binarnych (BST, AVL, Red-Black Tree, B-Tree) mają złożoność O(log n), ponieważ drzewo o n węzłach ma ~log₂(n) poziomów, a operacja wyszukiwania/dodawania schodzi co najwyżej od korzenia do liścia:

```
         50                    ← poziom 0
       /    \
     25      75                ← poziom 1
    /  \    /  \
  10   30  60   90             ← poziom 2
```

Dla n = 7 węzłów mamy 3 poziomy = ⌊log₂(7)⌋ + 1. Wyszukiwanie w takim drzewie to O(log n).

### Szybki test mentalny

Zadaj sobie pytanie: **„Jeśli podwoję rozmiar danych wejściowych, ile dodatkowych operacji będzie potrzebnych?"**

- Jeśli odpowiedź to **„jedna więcej"** → O(log n)
- Jeśli odpowiedź to **„dwa razy więcej"** → O(n)
- Jeśli odpowiedź to **„cztery razy więcej"** → O(n²)

Dla wyszukiwania binarnego: tablica 1000 elementów → ~10 kroków, tablica 2000 elementów → ~11 kroków. Podwojenie danych = 1 dodatkowy krok.

---

## O(n log n) — jak rozpoznać

### Reguła ogólna

> Jeśli algorytm **dzieli problem na mniejsze części** (log n poziomów), ale na **każdym poziomie przetwarza wszystkie n elementów**, to złożoność wynosi O(n log n).

Inaczej mówiąc: O(n log n) = „robimy coś O(n) razy, a to coś ma w sobie O(log n)" **lub** „mamy O(log n) poziomów podziału i na każdym poziomie przeglądamy O(n) elementów".

### Wzorzec 1: Algorytmy dziel i zwyciężaj z łączeniem (Merge Sort)

```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])     # rekurencja na lewą połowę
    right = merge_sort(arr[mid:])    # rekurencja na prawą połowę
    return merge(left, right)        # scalanie — O(n) pracy
```

Wizualizacja podziałów:

```
Poziom 0:  [8, 3, 5, 1, 4, 7, 2, 6]              ← n elementów do scalenia
Poziom 1:  [8, 3, 5, 1]  [4, 7, 2, 6]             ← n elementów do scalenia
Poziom 2:  [8, 3] [5, 1]  [4, 7] [2, 6]           ← n elementów do scalenia
Poziom 3:  [8][3] [5][1]  [4][7] [2][6]           ← n elementów do scalenia
           ─────────────────────────────
           log₂(n) poziomów × n pracy na poziom = O(n log n)
```

Na **każdym** z log₂(n) poziomów, łączna praca scalania (merge) obejmuje **wszystkie n elementów**. Stąd: n × log n.

### Wzorzec 2: Pętla liniowa z operacją logarytmiczną w środku

```python
# Budowanie posortowanego zbioru — n wstawień, każde O(log n)
import bisect

sorted_list = []
for x in data:                      # n iteracji
    bisect.insort(sorted_list, x)   # wstawienie w O(log n) ← wyszukiwanie binarne
```

Pętla zewnętrzna: O(n). Operacja wewnątrz: O(log n). Razem: O(n log n).

Inne przykłady tego wzorca:
- n razy wstawiamy element do kopca (heap) → O(n log n)
- n razy szukamy binarnie w tablicy → O(n log n)
- iteracja po elementach z operacją na zbalansowanym drzewie → O(n log n)

### Wzorzec 3: Quick Sort (średni przypadek)

```python
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]     # partycjonowanie — O(n)
    mid = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + mid + quicksort(right)
```

Przy dobrym pivocie podział jest mniej więcej na pół → log n poziomów rekurencji, O(n) pracy partycjonowania na każdym poziomie → O(n log n) średnio.

(W najgorszym przypadku, gdy pivot zawsze jest skrajny, Quick Sort degeneruje się do O(n²), bo zamiast log n poziomów mamy n poziomów.)

---

## Twierdzenie o rekurencji (Master Theorem) — skrócona wersja

Jeśli algorytm rekurencyjny ma postać:

```
T(n) = a · T(n/b) + O(nᵈ)
```

gdzie:
- **a** = liczba podproblemów (ile razy się wywołujemy rekurencyjnie)
- **b** = przez ile dzielimy rozmiar problemu
- **d** = koszt pracy poza rekurencją

To złożoność wynosi:

| Warunek | Złożoność | Przykład |
|---|---|---|
| a < bᵈ | O(nᵈ) | Praca zdominowana przez najwyższy poziom |
| a = bᵈ | O(nᵈ · log n) | Praca rozłożona równomiernie po poziomach |
| a > bᵈ | O(n^(log_b(a))) | Praca zdominowana przez liście drzewa |

**Przykłady:**

| Algorytm | Rekurencja | a | b | d | Warunek | Złożoność |
|---|---|---|---|---|---|---|
| Binary Search | T(n) = 1·T(n/2) + O(1) | 1 | 2 | 0 | 1 = 2⁰ = 1 → a = bᵈ | O(log n) |
| Merge Sort | T(n) = 2·T(n/2) + O(n) | 2 | 2 | 1 | 2 = 2¹ = 2 → a = bᵈ | O(n log n) |
| Przelot liniowy | T(n) = 1·T(n/2) + O(n) | 1 | 2 | 1 | 1 < 2¹ = 2 → a < bᵈ | O(n) |
| Strassen (mnożenie macierzy) | T(n) = 7·T(n/2) + O(n²) | 7 | 2 | 2 | 7 > 4 → a > bᵈ | O(n^2.81) |

Nie musisz pamiętać wzoru, ale warto zapamiętać intuicję:
- **Binary Search**: 1 wywołanie na połowie → a=1, b=2, praca O(1) → O(log n)
- **Merge Sort**: 2 wywołania na połówkach + scalanie O(n) → O(n log n)

---

## Ściągawka — kiedy pojawia się jaká złożoność

| Złożoność | Sygnał rozpoznawczy | Typowe algorytmy |
|---|---|---|
| O(1) | Brak pętli, bezpośredni dostęp | HashMap lookup, indeksowanie tablicy |
| O(log n) | Problem **kurczy się** o stałą frakcję w każdym kroku | Binary search, operacje na BST, szybkie potęgowanie |
| O(n) | Jedna pętla po wszystkich elementach | Przeszukiwanie liniowe, sumowanie tablicy |
| O(n log n) | log n poziomów podziału × n pracy na poziom **lub** n operacji × log n każda | Merge sort, heap sort, budowanie drzewa BST |
| O(n²) | Dwie zagnieżdżone pętle po n | Bubble sort, porównanie każda-z-każdą |
| O(2ⁿ) | Rozgałęzienie rekurencyjne bez memoizacji | Brute-force podzbiorów, naiwny Fibonacci |

---

## Praktyczne rady na rozmowę rekrutacyjną

1. **Szukaj dzielenia** — jeśli widzisz, że coś jest dzielone na pół (tablica, drzewo, zakres), myśl „log".
2. **Policz pętle i co jest w środku** — pętla O(n) z operacją O(log n) w środku = O(n log n).
3. **Narysuj drzewo rekurencji** — policz liczbę poziomów (to „log") i pracę na każdym poziomie.
4. **Test podwojenia** — podwój n i sprawdź ile dodatkowej pracy dochodzi:
   - +1 operacja → log n
   - +n operacji → n log n
   - ×2 operacji → n
   - ×4 operacji → n²

---

## Powiązane materiały

- [System Design: Pytania Rekrutacyjne](system-design-pytania-rekrutacyjne.md)
- [Zaawansowane Struktury Danych](../Python/zaawansowane-struktury-danych.md)
