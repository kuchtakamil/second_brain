# Programowanie dynamiczne (Dynamic Programming)

**Kategoria:** technika algorytmiczna

Nie jest to jeden konkretny algorytm, lecz **paradygmat rozwiązywania problemów**. Idea jest prosta:

1. **Rozbij** problem na mniejsze podproblemy
2. **Rozwiąż** każdy podproblem **tylko raz**
3. **Zapamiętaj** wynik (memoizacja / tabulacja)
4. **Złóż** rozwiązanie z zapamiętanych wyników

> [!IMPORTANT]
> DP działa wtedy i tylko wtedy, gdy problem ma dwie właściwości:
> - **Optimal substructure** — optymalne rozwiązanie składa się z optymalnych rozwiązań podproblemów
> - **Overlapping subproblems** — te same podproblemy pojawiają się wielokrotnie

---

## Dlaczego jest ważny?

- Transformuje rozwiązania wykładnicze $O(2^n)$ w wielomianowe $O(n^2)$ lub $O(n \cdot W)$
- Jeden z najczęstszych tematów na rozmowach rekrutacyjnych (FAANG)
- Uczy rozpoznawania struktury optymalnych podproblemów i nakładających się podproblemów

---

## Dwa podejścia: Top-Down vs Bottom-Up

DP można implementować na dwa sposoby. Oba dają ten sam wynik, ale różnią się kierunkiem rozwiązywania.

```
┌─────────────────────────────────────────────────────────────────┐
│                    TOP-DOWN (memoizacja)                        │
│                                                                 │
│  Zacznij od DUŻEGO problemu → rozbijaj na mniejsze → cache'uj  │
│                                                                 │
│  fib(5) ──→ fib(4) ──→ fib(3) ──→ fib(2) ──→ return 1         │
│                          │          ↑  cache hit!               │
│              fib(3) ─────┘──→ fib(1) ──→ return 1              │
│              ↑ cache hit!                                       │
│                                                                 │
│  Implementacja: rekurencja + słownik/lru_cache                  │
│  Kierunek: od n w dół do base case                              │
│  Zaleta: oblicza TYLKO potrzebne podproblemy                    │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                   BOTTOM-UP (tabulacja)                         │
│                                                                 │
│  Zacznij od NAJMNIEJSZYCH podproblemów → buduj w górę           │
│                                                                 │
│  dp[0]=0  dp[1]=1  dp[2]=1  dp[3]=2  dp[4]=3  dp[5]=5         │
│    ↑        ↑       ↑ ↑      ↑ ↑      ↑ ↑      ↑ ↑            │
│   base    base     0+1      1+1      1+2      2+3             │
│                                                                 │
│  Implementacja: pętla + tablica dp[]                            │
│  Kierunek: od base case w górę do n                             │
│  Zaleta: brak narzutu rekurencji, zwykle szybsza                │
└─────────────────────────────────────────────────────────────────┘
```

### Porównanie

| Cecha | Top-Down (memoizacja) | Bottom-Up (tabulacja) |
|---|---|---|
| Kierunek | Od problemu do base case | Od base case do problemu |
| Implementacja | Rekurencja + cache | Pętla + tablica `dp[]` |
| Pamięć stosu | $O(n)$ (stos rekurencji) | $O(1)$ (brak rekurencji) |
| Oblicza | Tylko potrzebne podproblemy | Wszystkie podproblemy |
| Łatwość myślenia | Bardziej naturalna | Wymaga określenia kolejności |
| W Pythonie | `@lru_cache` / `dict` | `list` / `dict` |
| Ryzyko | `RecursionError` przy dużym $n$ | Brak |

> [!TIP]
> **Reguła kciuka:** zacznij od top-down (łatwiej myśleć rekurencyjnie), potem przepisz na bottom-up (szybsza, bezpieczniejsza). Na rozmowie rekrutacyjnej pokaż oba.

---

## 🔍 Wizualizacja: dlaczego naiwna rekurencja jest zła

Przykład: Fibonacci naiwnie vs z DP

```
Naiwne fib(5) — DRZEWO REKURENCJI (overlapping subproblems):

                         fib(5)
                        /       \
                   fib(4)        fib(3)
                  /     \        /    \
             fib(3)    fib(2)  fib(2)  fib(1)
             /   \       |      |       |
         fib(2) fib(1)   1      1       1
           |      |
           1      1

Liczba wywołań: 9    (rośnie wykładniczo → O(2^n))
fib(3) obliczony 2 razy ❌
fib(2) obliczony 3 razy ❌
```

```
fib(5) z MEMOIZACJĄ — każdy podproblem obliczony RAZ:

fib(5) → fib(4) → fib(3) → fib(2) → return 1  (base case)
                      ↓
                   fib(1) → return 1  (base case)
                   return 1+1 = 2     (cache: fib(3)=2)
              ↓
           fib(2) → cache hit! = 1
           return 2+1 = 3             (cache: fib(4)=3)
         ↓
      fib(3) → cache hit! = 2
      return 3+2 = 5                  (cache: fib(5)=5)

Liczba wywołań: 5    (liniowo → O(n))  ✅
```

```
fib(5) z TABULACJĄ — wypełniaj tablicę od dołu:

Indeks:   0    1    2    3    4    5
         ┌────┬────┬────┬────┬────┬────┐
dp:      │ 0  │ 1  │ 1  │ 2  │ 3  │ 5  │
         └────┴────┴────┴────┴────┴────┘
          base base  ↑    ↑    ↑    ↑
                    0+1  1+1  1+2  2+3

dp[i] = dp[i-1] + dp[i-2]

Wynik: dp[5] = 5  ✅
```

---

## Kluczowe problemy DP

### 1. Ciąg Fibonacci

Najprostszy przykład DP — idealny do nauki konceptu.

**Relacja rekurencyjna:**
```
fib(n) = fib(n-1) + fib(n-2)
fib(0) = 0, fib(1) = 1
```

**Złożoność:**
| Podejście | Czas | Pamięć |
|---|---|---|
| Naiwna rekurencja | $O(2^n)$ | $O(n)$ stos |
| Memoizacja | $O(n)$ | $O(n)$ cache + stos |
| Tabulacja | $O(n)$ | $O(n)$ tablica |
| Tabulacja (zoptym.) | $O(n)$ | $O(1)$ dwie zmienne |

```python
# TODO: Implementacja — patrz pełny artykuł
# Top-down (memoizacja z @lru_cache)
# Bottom-up (tabulacja z tablicą dp[])
# Bottom-up zoptymalizowana (dwie zmienne a, b)
pass
```

📎 Pełny artykuł: [Implementacje ciągu Fibonacci](implementacje-ciagu-fibonacci.md)

---

### 2. Coin Change (problem wydawania reszty)

**Problem:** mając zbiór nominałów monet, jaka jest **minimalna liczba monet** potrzebna do wydania kwoty `amount`?

**Relacja rekurencyjna:**
```
dp[amount] = min(dp[amount - coin] + 1)  dla każdego coin w coins
dp[0] = 0  (base case: 0 monet na kwotę 0)
```

#### 🔍 Wizualizacja

Monety: `[1, 3, 4]`, kwota: `6`

```
Budowanie tablicy dp (bottom-up):

amount:   0    1    2    3    4    5    6
         ┌────┬────┬────┬────┬────┬────┬────┐
dp:      │ 0  │ 1  │ 2  │ 1  │ 1  │ 2  │ 2  │
         └────┴────┴────┴────┴────┴────┴────┘

Szczegóły:
dp[0] = 0                                    ← base case
dp[1] = min(dp[1-1]+1) = dp[0]+1 = 1         ← moneta 1
dp[2] = min(dp[2-1]+1) = dp[1]+1 = 2         ← moneta 1+1
dp[3] = min(dp[3-1]+1, dp[3-3]+1)
      = min(dp[2]+1, dp[0]+1)
      = min(3, 1) = 1                        ← moneta 3  ✅
dp[4] = min(dp[4-1]+1, dp[4-3]+1, dp[4-4]+1)
      = min(dp[3]+1, dp[1]+1, dp[0]+1)
      = min(2, 2, 1) = 1                     ← moneta 4  ✅
dp[5] = min(dp[5-1]+1, dp[5-3]+1, dp[5-4]+1)
      = min(dp[4]+1, dp[2]+1, dp[1]+1)
      = min(2, 3, 2) = 2                     ← monety 4+1 lub 3+?
dp[6] = min(dp[6-1]+1, dp[6-3]+1, dp[6-4]+1)
      = min(dp[5]+1, dp[3]+1, dp[2]+1)
      = min(3, 2, 3) = 2                     ← monety 3+3  ✅

Odpowiedź: dp[6] = 2 (monety: 3 + 3)
```

> [!NOTE]
> Zachłanne podejście (greedy: bierz największą monetę) dałoby tutaj `4+1+1 = 3 monety` — **nie jest optymalne!** DP gwarantuje optimum.

```python
# TODO: Implementacja
# def coin_change(coins: list[int], amount: int) -> int:
#     ...
pass
```

---

### 3. Problem plecakowy — 0/1 Knapsack

**Problem:** masz plecak o pojemności $W$ i $n$ przedmiotów (każdy z wagą i wartością). Zmaksymalizuj wartość, nie przekraczając pojemności. Każdy przedmiot możesz wziąć **raz** (0/1).

**Relacja rekurencyjna:**
```
dp[i][w] = max(
    dp[i-1][w],                          ← nie bierz przedmiotu i
    dp[i-1][w - weight[i]] + value[i]    ← weź przedmiot i (jeśli się mieści)
)
```

#### 🔍 Wizualizacja

Przedmioty: `[(waga=1, wartość=1), (w=3, v=4), (w=4, v=5), (w=5, v=7)]`
Pojemność plecaka: $W = 7$

```
Budowanie tablicy dp[i][w]:

              Pojemność w →
              0    1    2    3    4    5    6    7
         ┌────┬────┬────┬────┬────┬────┬────┬────┐
  brak   │ 0  │ 0  │ 0  │ 0  │ 0  │ 0  │ 0  │ 0  │
         ├────┼────┼────┼────┼────┼────┼────┼────┤
  (1,1)  │ 0  │ 1  │ 1  │ 1  │ 1  │ 1  │ 1  │ 1  │
         ├────┼────┼────┼────┼────┼────┼────┼────┤
  (3,4)  │ 0  │ 1  │ 1  │ 4  │ 5  │ 5  │ 5  │ 5  │
         ├────┼────┼────┼────┼────┼────┼────┼────┤
  (4,5)  │ 0  │ 1  │ 1  │ 4  │ 5  │ 6  │ 6  │ 9  │
         ├────┼────┼────┼────┼────┼────┼────┼────┤
  (5,7)  │ 0  │ 1  │ 1  │ 4  │ 5  │ 7  │ 8  │ 9  │
         └────┴────┴────┴────┴────┴────┴────┴────┘
                                                ↑
                                          Odpowiedź: 9

Przykład obliczenia dp[3][7] (przedmioty 1-3, pojemność 7):
  Nie bierz (4,5): dp[2][7] = 5
  Weź (4,5):       dp[2][7-4] + 5 = dp[2][3] + 5 = 4 + 5 = 9  ← lepsze!
  dp[3][7] = max(5, 9) = 9  (bierzemy przedmioty (3,4) i (4,5))
```

**Złożoność:** $O(n \cdot W)$ czasowa i pamięciowa (pseudo-wielomianowa)

```python
# TODO: Implementacja
# def knapsack(weights: list[int], values: list[int], capacity: int) -> int:
#     ...
pass
```

---

### 4. Longest Common Subsequence (LCS)

**Problem:** znajdź najdłuższy wspólny podciąg dwóch stringów (nie musi być ciągły!).

**Relacja rekurencyjna:**
```
Jeśli s1[i] == s2[j]:
    dp[i][j] = dp[i-1][j-1] + 1       ← znaki się zgadzają, rozszerz LCS
W przeciwnym razie:
    dp[i][j] = max(dp[i-1][j], dp[i][j-1])  ← weź lepszy wynik pomijając jeden znak
```

#### 🔍 Wizualizacja

s1 = `"ABCBDAB"`, s2 = `"BDCAB"`

```
Budowanie tablicy dp[i][j]:

            ""   B    D    C    A    B
       ┌────┬────┬────┬────┬────┬────┐
  ""   │ 0  │ 0  │ 0  │ 0  │ 0  │ 0  │
       ├────┼────┼────┼────┼────┼────┤
  A    │ 0  │ 0  │ 0  │ 0  │ 1  │ 1  │
       ├────┼────┼────┼────┼────┼────┤
  B    │ 0  │ 1  │ 1  │ 1  │ 1  │ 2  │
       ├────┼────┼────┼────┼────┼────┤
  C    │ 0  │ 1  │ 1  │ 2  │ 2  │ 2  │
       ├────┼────┼────┼────┼────┼────┤
  B    │ 0  │ 1  │ 1  │ 2  │ 2  │ 3  │
       ├────┼────┼────┼────┼────┼────┤
  D    │ 0  │ 1  │ 2  │ 2  │ 2  │ 3  │
       ├────┼────┼────┼────┼────┼────┤
  A    │ 0  │ 1  │ 2  │ 2  │ 3  │ 3  │
       ├────┼────┼────┼────┼────┼────┤
  B    │ 0  │ 1  │ 2  │ 2  │ 3  │ 4  │
       └────┴────┴────┴────┴────┴────┘
                                    ↑
                              LCS = 4 → "BCAB"

Odtworzenie LCS (backtracking po tablicy):
dp[7][5] → B matches B → dodaj B, idź ↖ dp[6][4]
dp[6][4] → A matches A → dodaj A, idź ↖ dp[5][3]
dp[5][3] → D≠C → idź ← dp[5][2] (większe)
dp[5][2] → D matches D → dodaj D... itd.

Wynik: "BCAB" (czytany od końca)
```

**Złożoność:** $O(m \cdot n)$ czasowa i pamięciowa

```python
# TODO: Implementacja
# def lcs(s1: str, s2: str) -> str:
#     ...
pass
```

---

### 5. Edit Distance (Levenshtein)

**Problem:** jaka jest minimalna liczba operacji (wstaw / usuń / zamień znak), żeby przekształcić string `s1` w `s2`?

**Relacja rekurencyjna:**
```
Jeśli s1[i] == s2[j]:
    dp[i][j] = dp[i-1][j-1]              ← znaki się zgadzają, brak operacji
W przeciwnym razie:
    dp[i][j] = 1 + min(
        dp[i-1][j],      ← usuń znak z s1
        dp[i][j-1],      ← wstaw znak do s1
        dp[i-1][j-1]     ← zamień znak
    )
```

#### 🔍 Wizualizacja

s1 = `"kitten"`, s2 = `"sitting"`

```
Budowanie tablicy dp[i][j]:

            ""   s    i    t    t    i    n    g
       ┌────┬────┬────┬────┬────┬────┬────┬────┐
  ""   │ 0  │ 1  │ 2  │ 3  │ 4  │ 5  │ 6  │ 7  │
       ├────┼────┼────┼────┼────┼────┼────┼────┤
  k    │ 1  │ 1  │ 2  │ 3  │ 4  │ 5  │ 6  │ 7  │
       ├────┼────┼────┼────┼────┼────┼────┼────┤
  i    │ 2  │ 2  │ 1  │ 2  │ 3  │ 4  │ 5  │ 6  │
       ├────┼────┼────┼────┼────┼────┼────┼────┤
  t    │ 3  │ 3  │ 2  │ 1  │ 2  │ 3  │ 4  │ 5  │
       ├────┼────┼────┼────┼────┼────┼────┼────┤
  t    │ 4  │ 4  │ 3  │ 2  │ 1  │ 2  │ 3  │ 4  │
       ├────┼────┼────┼────┼────┼────┼────┼────┤
  e    │ 5  │ 5  │ 4  │ 3  │ 2  │ 2  │ 3  │ 4  │
       ├────┼────┼────┼────┼────┼────┼────┼────┤
  n    │ 6  │ 6  │ 5  │ 4  │ 3  │ 3  │ 2  │ 3  │
       └────┴────┴────┴────┴────┴────┴────┴────┘
                                              ↑
                                   Edit Distance = 3

Operacje:  kitten → sitten (zamień k→s)
           sitten → sittin (zamień e→i)
           sittin → sitting (wstaw g)
```

**Złożoność:** $O(m \cdot n)$ czasowa i pamięciowa

**Zastosowania:** spell-checker, diff narzędzia, bioinformatyka (porównywanie DNA)

```python
# TODO: Implementacja
# def edit_distance(s1: str, s2: str) -> int:
#     ...
pass
```

---

## Schemat rozwiązywania problemu DP

Universalny przepis na rozmowę rekrutacyjną:

```
┌─────────────────────────────────────────────────────────┐
│  1. ZDEFINIUJ STAN                                      │
│     Co oznacza dp[i]? (lub dp[i][j])                    │
│     Przykład: dp[i] = min monet do kwoty i              │
│                                                         │
│  2. ZNAJDŹ RELACJĘ REKURENCYJNĄ                         │
│     Jak dp[i] zależy od mniejszych podproblemów?        │
│     Przykład: dp[i] = min(dp[i-coin]+1) for coin        │
│                                                         │
│  3. USTAL BASE CASE                                     │
│     Jakie są wartości początkowe?                        │
│     Przykład: dp[0] = 0                                 │
│                                                         │
│  4. OKREŚL KOLEJNOŚĆ OBLICZANIA                         │
│     Od małych do dużych (bottom-up)                     │
│     Lub rekurencyjnie z cache (top-down)                │
│                                                         │
│  5. ODCZYTAJ ODPOWIEDŹ                                  │
│     Zwykle dp[n] lub dp[m][n]                           │
│                                                         │
│  6. (OPCJONALNIE) ODTWÓRZ ROZWIĄZANIE                  │
│     Backtracking po tablicy dp                          │
└─────────────────────────────────────────────────────────┘
```

---

## Wzorce DP — rozpoznawanie typów problemów

| Wzorzec | Przykład problemu | Stan dp | Złożoność |
|---|---|---|---|
| **Linear DP** | Fibonacci, Climbing Stairs | `dp[i]` | $O(n)$ |
| **Grid DP** | Unique Paths, Min Path Sum | `dp[i][j]` | $O(m \cdot n)$ |
| **String DP** | LCS, Edit Distance | `dp[i][j]` | $O(m \cdot n)$ |
| **Knapsack** | 0/1 Knapsack, Coin Change | `dp[i][w]` lub `dp[w]` | $O(n \cdot W)$ |
| **Interval DP** | Matrix Chain Multiplication | `dp[i][j]` | $O(n^3)$ |
| **Tree DP** | Max path sum in tree | rekurencja + return | $O(n)$ |

> [!TIP]
> **Sygnały, że problem wymaga DP:**
> - „Znajdź **minimum/maximum** czegoś"
> - „Policz **liczbę sposobów** na..."
> - „Czy **da się** osiągnąć...?" (True/False)
> - Problem ma ograniczone wejście ($n \leq 1000$, co sugeruje $O(n^2)$)

---

## Optymalizacja pamięci w DP

Wiele problemów 2D można zoptymalizować do 1D, jeśli bieżący wiersz zależy tylko od poprzedniego:

```
Pełna tablica:                    Zoptymalizowana (2 wiersze):
dp[n][W]  → O(n·W) pamięci       dp[W] → O(W) pamięci

┌────┬────┬────┬────┐             ┌────┬────┬────┬────┐
│    │    │    │    │  wiersz i-1  │ prev                │
├────┼────┼────┼────┤     ↓       ├────┼────┼────┼────┤
│    │    │ ←  │    │  wiersz i   │ curr                │
└────┴────┴────┴────┘             └────┴────┴────┴────┘

Jeśli dp[i][j] zależy TYLKO od dp[i-1][...]:
→ wystarczą dwa wiersze (prev, curr)
→ lub nawet jeden wiersz (iteruj od prawej do lewej w knapsack)
```

---

## Powiązane tematy

- [Implementacje ciągu Fibonacci](implementacje-ciagu-fibonacci.md) — Fibonacci jako najprostszy przykład DP
- [Top 10 algorytmów informatyka](top-10-algorytmow-informatyka.md) — sekcja 6: DP
- [Algorytmy zachłanne (Greedy)](top-10-algorytmow-informatyka.md#8-algorytmy-zachłanne-greedy) — DP vs Greedy: greedy nie zawsze daje optimum
