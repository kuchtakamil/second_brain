# Regex Cheatsheet & Python `re`

Krótki i zwięzły przewodnik (cheatsheet) po składni wyrażeń regularnych (Regex) oraz sposobach ich użycia w Pythonie wyłącznie przy pomocy wbudowanego modułu `re`.

---

## Część 1: Składnia wyrażeń regularnych (Regex)

### 1. Klasy znaków (Character Classes)
*   `.` — dowolny znak oprócz nowej linii (`\n`).
*   `\d` — dowolna cyfra; odpowiednik `[0-9]`.
*   `\D` — dowolny znak niebędący cyfrą; odpowiednik `[^0-9]`.
*   `\w` — znak alfanumeryczny (litera, cyfra, podkreślnik `_`); odpowiednik `[a-zA-Z0-9_]`.
*   `\W` — znak niebędący alfanumerycznym; odpowiednik `[^a-zA-Z0-9_]`.
*   `\s` — dowolny biały znak (spacja, tabulacja, nowa linia itp.); odpowiednik `[ \t\n\r\f\v]`.
*   `\S` — dowolny znak niebędący białym znakiem; odpowiednik `[^ \t\n\r\f\v]`.

### 2. Kotwice i granice (Anchors & Boundaries)
*   `^` — początek ciągu znaków (lub linii w trybie wieloliniowym).
*   `$` — koniec ciągu znaków (lub linii w trybie wieloliniowym).
*   `\b` — granica słowa (przejście między znakiem alfanumerycznym a niealfanumerycznym).
*   `\B` — negacja granicy słowa.

### 3. Kwantyfikatory (Quantifiers)
*   `*` — 0 lub więcej powtórzeń.
*   `+` — 1 lub więcej powtórzeń.
*   `?` — 0 lub 1 powtórzenie (opcjonalność).
*   `{n}` — dokładnie $n$ powtórzeń.
*   `{n,}` — co najmniej $n$ powtórzeń.
*   `{n,m}` — od $n$ do $m$ powtórzeń.

> [!TIP]
> Domyślnie kwantyfikatory są **zachłanne** (greedy). Dodaj `?` po kwantyfikatorze (np. `*?`, `+?`), aby uczynić go **leniwym** (lazy/non-greedy) — dopasuje wtedy minimalną konieczną liczbę znaków.

### 4. Grupy i warunki (Groups & Alternation)
*   `a|b` — dopasowuje `a` lub `b`.
*   `(...)` — grupa przechwytująca (capturing group).
*   `(?:...)` — grupa nieprzechwytująca (non-capturing group) — służy tylko do grupowania.
*   `(?P<name>...)` — nazwana grupa przechwytująca (dostępna w Pythonie po nazwie).

### 5. Mechanizmy Lookaround (Behind & Forward)
Lookaround pozwala sprawdzić obecność wzorca przed lub za bieżącą pozycją, **nie włączając** go do dopasowanego tekstu (tzw. zero-width assertions).

| Typ Lookaround | Składnia | Opis |
| :--- | :--- | :--- |
| **Positive Lookahead** (W przód) | `(?=...)` | Sprawdza, czy bezpośrednio *po* bieżącej pozycji znajduje się dany wzorzec. |
| **Negative Lookahead** (W przód) | `(?!...)` | Sprawdza, czy bezpośrednio *po* bieżącej pozycji **nie** znajduje się dany wzorzec. |
| **Positive Lookbehind** (W tył) | `(?<=...)` | Sprawdza, czy bezpośrednio *przed* bieżącą pozycją znajduje się dany wzorzec. |
| **Negative Lookbehind** (W tył) | `(?<!...)` | Sprawdza, czy bezpośrednio *przed* bieżącą pozycją **nie** znajduje się dany wzorzec. |

> [!IMPORTANT]
> W standardowym module `re` Pythona **lookbehind musi mieć stałą długość** (np. `(?<=cat)` lub `(?<=.{3})`). Próba użycia kwantyfikatorów o zmiennej długości (np. `(?<=cat*)`) w lookbehind zgłosi błąd `re.error`.

---

## Część 2: Używanie Regex w Pythonie (tylko moduł `re`)

Zawsze importuj wbudowany moduł `re` i stosuj **surowe ciągi znaków** (raw strings, z przedrostkiem `r`), aby uniknąć problemów ze znakami ucieczki `\`.

```python
import re

text = "Kontakt: jan.kowalski@email.com, tel: 123-456-789. Kod: ABC-1234."
```

### 1. Kompilacja wzorców (Kompilowany Regex)
Zalecana przy wielokrotnym używaniu tego samego wzorca (zwiększa wydajność).
```python
# Kompilacja wzorca do obiektu Pattern
phone_pattern = re.compile(r"\d{3}-\d{3}-\d{3}")

# Wywołanie bezpośrednio na obiekcie Pattern
has_phone = phone_pattern.search(text)
```

### 2. Główne funkcje wyszukiwania i dopasowywania
*   `re.search(pattern, string)` — Szuka **pierwszego** dopasowania w dowolnym miejscu tekstu. Zwraca obiekt `Match` lub `None`.
*   `re.match(pattern, string)` — Sprawdza dopasowanie wyłącznie **od samego początku** tekstu.
*   `re.fullmatch(pattern, string)` — Sprawdza, czy **cały tekst** pasuje do wzorca (od początku do końca).

```python
# 1. search()
match = re.search(r"\bjan\.\w+", text)
if match:
    print(f"Znaleziono: {match.group()}")  # Znaleziono: jan.kowalski

# 2. match()
is_start = re.match(r"Kontakt", text)
print(bool(is_start))  # True

# 3. fullmatch()
is_full = re.fullmatch(r"ABC-\d{4}", "ABC-1234")
print(bool(is_full))  # True
```

### 3. Pobieranie wielu dopasowań
*   `re.findall(pattern, string)` — Zwraca listę wszystkich dopasowań jako stringi. Jeśli wzorzec zawiera grupy `()`, zwraca listę krotek zawierających te grupy.
*   `re.finditer(pattern, string)` — Zwraca generator obiektów `Match`. **Bardzo wydajne pamięciowo** przy dużych tekstach.

```python
# findall()
emails = re.findall(r"[\w.-]+@[\w.-]+\.\w+", text)
print(emails)  # ['jan.kowalski@email.com']

# finditer()
for m in re.finditer(r"\d{3}-\d{3}-\d{3}", text):
    print(f"Telefon: {m.group()} na pozycji {m.start()}:{m.end()}")
    # Telefon: 123-456-789 na pozycji 37:48
```

### 4. Podmienianie i dzielenie tekstu
*   `re.sub(pattern, replacement, string)` — Zastępuje dopasowane fragmenty nowym tekstem.
*   `re.split(pattern, string)` — Dzieli tekst na liście przy użyciu wzorca jako separatora.

```python
# sub() - ukrywanie numeru telefonu
masked = re.sub(r"\d{3}-\d{3}-\d{3}", "[UKRYTE]", text)
print(masked)  # Kontakt: jan.kowalski@email.com, tel: [UKRYTE]. Kod: ABC-1234.

# split() - rozbijanie po przecinkach lub średnikach
data = "python;java,rust;c++"
languages = re.split(r"[;,]", data)
print(languages)  # ['python', 'java', 'rust', 'c++']
```

### 5. Pobieranie grup z obiektu `Match`
```python
# Wykorzystanie nazwanych grup
log = "ERROR: 404 - Not Found"
pattern = re.compile(r"(?P<level>[A-Z]+): (?P<code>\d+) - (?P<message>.*)")

match = pattern.search(log)
if match:
    print(match.group(0))        # Całe dopasowanie: "ERROR: 404 - Not Found"
    print(match.group(1))        # Grupa 1 (pozycyjna): "ERROR"
    print(match.group("code"))   # Po nazwie: "404"
    print(match.groups())        # Wszystkie grupy pozycyjne: ('ERROR', '404', 'Not Found')
    print(match.groupdict())     # Wszystkie grupy jako słownik: {'level': 'ERROR', 'code': '404', 'message': 'Not Found'}
```

### 6. Flagi (Modyfikatory)
Flagi można przekazywać jako ostatni argument funkcji (np. `re.search(..., flags=re.I)`) lub w `re.compile()`. Łączy się je operatorem bitowym `|`.

*   `re.IGNORECASE` (lub `re.I`) — Ignoruje wielkość liter.
*   `re.MULTILINE` (lub `re.M`) — Sprawia, że `^` i `$` dopasowują początek/koniec każdej linii w tekście, a nie tylko całego stringa.
*   `re.DOTALL` (lub `re.S`) — Sprawia, że kropka `.` dopasowuje również znak nowej linii `\n`.
*   `re.VERBOSE` (lub `re.X`) — Pozwala na czytelne pisanie wyrażeń wieloliniowych z komentarzami (ignoruje białe znaki).

```python
# Przykład użycia flag
pattern = re.compile(r"""
    ^kontakt    # początek linii, słowo kontakt
    :\s+        # dwukropek i spacja
    (?P<user>[\w.]+)
    @
    (?P<domain>[\w.]+)
""", re.VERBOSE | re.IGNORECASE | re.MULTILINE)
```

---

## Powiązane pliki
*   [Praca z Regex w nowoczesnym Pythonie](praca-z-regex-w-nowoczesnym-pythonie.md)
*   [Wyjaśnienie regexa w pythonie](wyjaśnienie-regexa-w-pythonie.md)
*   [Nawiasy w wyrażeniu regularnym](nawiasy-w-wyrażeniu-regularnym.md)
