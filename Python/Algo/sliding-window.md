# Sliding Window – technika okna przesuwnego

Technika **sliding window** (okno przesuwne) polega na utrzymywaniu podzbioru danych (okna) wewnątrz tablicy lub napisu i przesuwaniu jego granic bez konieczności ponownego przeglądania już sprawdzonych elementów. Dzięki temu rozwiązania, które naiwnie wymagałyby $O(n^2)$, można sprowadzić do $O(n)$.

**Kiedy stosować?**

- Szukasz najdłuższego / najkrótszego podciągu spełniającego jakiś warunek.
- Pracujesz na ciągłej sekwencji (string, lista).

---

## 1. Longest Substring Without Repeating Characters

Znajdź długość najdłuższego podciągu bez powtarzających się znaków.

**Przykład:** `"abcabcbb"` → `3` (podciąg `"abc"`)

**Złożoność:** $O(n)$ czasowa, $O(k)$ pamięciowa (k = rozmiar alfabetu)

```python
def length_of_longest_substring(s: str) -> int:
    char_index = {}  # stores last seen index of each character
    left = 0
    max_len = 0

    for right, char in enumerate(s):
        # if char was seen and is inside the current window, shrink from left
        if char in char_index and char_index[char] >= left:
            left = char_index[char] + 1

        char_index[char] = right
        max_len = max(max_len, right - left + 1)

    return max_len

# Usage:
print(length_of_longest_substring("abcabcbb"))  # 3
print(length_of_longest_substring("bbbbb"))     # 1
print(length_of_longest_substring("pwwkew"))    # 3
```

---

## 2. Longest Repeating Character Replacement

Mając napis `s` i liczbę `k`, możesz zamienić dowolne `k` znaków w napisie. Znajdź długość najdłuższego podciągu zawierającego tylko jeden rodzaj znaku po dokonaniu tych zamian.

**Przykład:** `s = "AABABBA"`, `k = 1` → `4` (zamień jedno `B` w `"AABA"` → `"AAAA"`)

**Kluczowy warunek:** okno jest poprawne, gdy `(rozmiar okna) - (najczęstszy znak w oknie) <= k`

**Złożoność:** $O(n)$ czasowa, $O(1)$ pamięciowa

```python
def character_replacement(s: str, k: int) -> int:
    count = {}       # frequency of chars in current window
    left = 0
    max_count = 0    # count of the most frequent char seen so far
    max_len = 0

    for right, char in enumerate(s):
        count[char] = count.get(char, 0) + 1
        max_count = max(max_count, count[char])

        # window size - most frequent char count = chars to replace
        window_size = right - left + 1
        if window_size - max_count > k:
            # shrink window from left
            count[s[left]] -= 1
            left += 1

        max_len = max(max_len, right - left + 1)

    return max_len

# Usage:
print(character_replacement("ABAB", 2))    # 4
print(character_replacement("AABABBA", 1)) # 4
```

---

## 3. Minimum Window Substring

Znając napis `s` i wzorzec `t`, znajdź najkrótsze okno w `s` zawierające wszystkie znaki z `t` (z uwzględnieniem wielokrotności).

**Przykład:** `s = "ADOBECODEBANC"`, `t = "ABC"` → `"BANC"`

**Złożoność:** $O(n + m)$ czasowa (n = len(s), m = len(t)), $O(m)$ pamięciowa

```python
from collections import Counter

def min_window(s: str, t: str) -> str:
    if not t or not s:
        return ""

    need = Counter(t)   # required char frequencies
    have = {}           # current window char frequencies
    formed = 0          # how many unique chars satisfy their required count
    required = len(need)

    left = 0
    best = ""

    for right, char in enumerate(s):
        have[char] = have.get(char, 0) + 1

        # check if this char now satisfies its required count
        if char in need and have[char] == need[char]:
            formed += 1

        # try to shrink window from left while it's still valid
        while formed == required:
            window = s[left:right + 1]
            if not best or len(window) < len(best):
                best = window

            left_char = s[left]
            have[left_char] -= 1
            if left_char in need and have[left_char] < need[left_char]:
                formed -= 1
            left += 1

    return best

# Usage:
print(min_window("ADOBECODEBANC", "ABC"))  # "BANC"
print(min_window("a", "a"))               # "a"
print(min_window("a", "aa"))              # ""
```

---

## 4. Find All Anagrams in a String

Mając napis `s` i wzorzec `p`, zwróć listę indeksów startowych wszystkich anagramów `p` w `s`.

**Przykład:** `s = "cbaebabacd"`, `p = "abc"` → `[0, 6]`

### 💡 Intuicja

**Anagram** = te same litery, innej kolejności. Np. `"bca"`, `"cab"`, `"abc"` to wszystko anagramy siebie nawzajem.

Zamiast generować wszystkie permutacje `p` i szukać każdej z osobna (co byłoby wolne), wystarczy zauważyć:

> Dwa napisy są anagramami ⟺ mają identyczny rozkład częstości liter.

Dlatego przesuwamy **okno stałej szerokości** `len(p)` po napisie `s` i w każdej pozycji porównujemy liczniki liter — jeśli się zgadzają, znaleźliśmy anagram.

### 🔍 Wizualizacja (krok po kroku)

```
s = "c b a e b a b a c d"
p = "abc"   →   need = {a:1, b:1, c:1}

Krok 0:  [c b a] e b a b a c d   window = {c:1, b:1, a:1} ✅  → wynik: [0]
Krok 1:   c[b a e] b a b a c d   window = {b:1, a:1, e:1} ❌
Krok 2:   c b[a e b] a b a c d   window = {a:1, e:1, b:1} ❌
Krok 3:   c b a[e b a] b a c d   window = {e:1, b:1, a:1} ❌
Krok 4:   c b a e[b a b] a c d   window = {b:2, a:1}      ❌
Krok 5:   c b a e b[a b a] c d   window = {a:2, b:1}      ❌
Krok 6:   c b a e b a[b a c] d   window = {b:1, a:1, c:1} ✅  → wynik: [0, 6]
Krok 7:   c b a e b a b[a c d]   window = {a:1, c:1, d:1} ❌
```

**Kluczowa obserwacja:** przy każdym przesunieciu okna o 1 w prawo:

- **dodajemy** znak wchodzący z prawej (`s[i + k - 1]`)
- **usuwamy** znak wychodzący z lewej (`s[i - 1]`)

Dzięki temu unikamy przeliczania całego okna od zera — to właśnie daje nam $O(n)$.

**Złożoność:** $O(n)$ czasowa, $O(1)$ pamięciowa (alfabet stały – maks. 26 kluczy)

### Implementacja

Zamiast sprawdzać pierwsze okno ręcznie przed pętlą, wciągnijmy ten proces do środka. W każdej iteracji:
1. Sprawdzamy stan okna startującego od `i`.
2. Aktualizujemy okno przygotowując je dla iteracji `i + 1`.

```python
from collections import Counter

def find_anagrams(s: str, p: str) -> list[int]:
    if len(p) > len(s):
        return []

    k = len(p)
    need = Counter(p)              # referencyjna "sygnatura" wzorca, np. {a:1, b:1, c:1}
    window = Counter(s[:k])        # Counter pierwszego okna (indeksy 0..k-1)
    result = []

    # i to indeks STARTOWY okna (0, 1, 2, ...)
    for i in range(len(s) - k + 1):
        # 1. Sprawdź okno dla obecnego startu 'i'
        if window == need:        
            result.append(i)      

        # 2. Zaktualizuj okno dla następnej iteracji (i + 1)
        # (pomijamy aktualizację, jeśli sprawdziliśmy okno na samym końcu stringa)
        if i < len(s) - k:
            new_char = s[i + k]   # znak wchodzący (tuż za prawą krawędzią obecnego okna)
            old_char = s[i]       # znak opuszczający (lewa krawędź obecnego okna)

            window[new_char] += 1
            window[old_char] -= 1
            
            if window[old_char] == 0:
                del window[old_char]  # posprzątaj, żeby Counter == need działało poprawnie

    return result

# Usage:
print(find_anagrams("cbaebabacd", "abc"))  # [0, 6]
print(find_anagrams("abab", "ab"))         # [0, 1, 2]
```

> [!TIP]
> `del window[old_char]` jest kluczowe! `Counter({a:1}) != Counter({a:1, b:0})` — Python porównuje słowniki dosłownie, więc klucze z wartością `0` psują porównanie.

---

## 5. Permutation in String

Sprawdź, czy jakakolwiek permutacja napisu `s1` jest podciągiem napisu `s2`.

**Przykład:** `s1 = "ab"`, `s2 = "eidbaooo"` → `True` (podciąg `"ba"` to permutacja `"ab"`)

To uproszczona wersja *Find All Anagrams* — zamiast zbierać wszystkie indeksy, zwracamy `True` przy pierwszym trafieniu.

**Złożoność:** $O(n)$ czasowa, $O(1)$ pamięciowa

```python
from collections import Counter

def check_inclusion(s1: str, s2: str) -> bool:
    if len(s1) > len(s2):
        return False

    need = Counter(s1)
    window = Counter(s2[:len(s1)])  # initial window
    k = len(s1)

    if window == need:
        return True

    for i in range(1, len(s2) - k + 1):
        new_char = s2[i + k - 1]
        old_char = s2[i - 1]

        window[new_char] += 1
        window[old_char] -= 1
        if window[old_char] == 0:
            del window[old_char]

        if window == need:
            return True

    return False

# Usage:
print(check_inclusion("ab", "eidbaooo"))  # True
print(check_inclusion("ab", "eidboaoo"))  # False
```

---

## Podsumowanie

| Problem | Technika okna | Złożoność Czas. |
|---|---|---|
| **Longest Substring Without Repeating Chars** | Variable window + hash map indeksów | $O(n)$ |
| **Longest Repeating Character Replacement** | Variable window + licznik najczęstszego znaku | $O(n)$ |
| **Minimum Window Substring** | Variable window + licznik wymaganych znaków | $O(n + m)$ |
| **Find All Anagrams in a String** | Fixed window + porównanie Counterów | $O(n)$ |
| **Permutation in String** | Fixed window + porównanie Counterów | $O(n)$ |

**Powiązane tematy:**

- [Implementacje Binary Search](implementacje-binary-search.md)
- [Tablice dwuwymiarowe w Pythonie](tablice-dwuwymiarowe-w-pythonie.md)
