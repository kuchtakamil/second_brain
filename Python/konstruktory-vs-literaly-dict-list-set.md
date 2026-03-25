# Konstruktory vs Literały: `dict()` / `list()` / `set()` a `{}` / `[]`

## Podsumowanie

Python oferuje dwa sposoby tworzenia podstawowych kolekcji: za pomocą **literałów** (`{}`, `[]`, `{1, 2}`) lub za pomocą **konstruktorów** (`dict()`, `list()`, `set()`). Oba sposoby są poprawne, ale różnią się czytelnością, wydajnością i przypadkami użycia.

---

## `list()` vs `[]`

### Kiedy używać `[]` (literał) — **preferowane**

Literał jest szybszy i bardziej idiomatyczny w Pythonie. Używaj go domyślnie.

```python
# Tworzenie pustej listy
items = []

# Tworzenie listy z elementami
numbers = [1, 2, 3]
```

### Kiedy używać `list()` (konstruktor)

Konstruktora używaj, gdy chcesz **skonwertować inny iterowalny obiekt** na listę:

```python
# Konwersja z krotki
t = (1, 2, 3)
l = list(t)  # [1, 2, 3]

# Konwersja ze stringa (każdy znak jako element)
chars = list("abc")  # ['a', 'b', 'c']

# Konwersja z generatora / range
squares = list(range(5))  # [0, 1, 2, 3, 4]

# Konwersja ze setu — żeby uzyskać indeksowanie
unique = {3, 1, 4}
as_list = list(unique)
```

> `list()` bez argumentów to odpowiednik `[]`, ale wolniejszy — interpreter musi jeszcze wyszukać nazwę `list` w przestrzeni nazw.

### Porównanie wydajności

```python
import timeit

# list() jest wolniejszy niż [] o ~10-20%
timeit.timeit("[]", number=10_000_000)       # ~0.08s
timeit.timeit("list()", number=10_000_000)   # ~0.14s
```

---

## `dict()` vs `{}`

### Kiedy używać `{}` (literał) — **preferowane**

```python
# Pusta mapa
config = {}

# Mapa z parami klucz-wartość
person = {"name": "Marek", "age": 30}
```

### Kiedy używać `dict()` (konstruktor)

**1. Konwersja z listy par (lub dowolnego iterable of pairs):**

```python
pairs = [("a", 1), ("b", 2)]
d = dict(pairs)  # {'a': 1, 'b': 2}
```

**2. Tworzenie słownika z kluczami jako keyword arguments (bardziej czytelne dla prostych kluczy-stringów):**

```python
# Zamiast {"host": "localhost", "port": 5432}
config = dict(host="localhost", port=5432)
```

> ⚠️ Ta składnia działa **tylko** gdy klucze są poprawnymi identyfikatorami Pythona (bez spacji, myślników itp.).

**3. Łączenie / kopiowanie słownika (historycznie):**

```python
defaults = {"debug": False, "timeout": 30}
copy = dict(defaults)           # płytka kopia (shallow copy)
merged = dict(defaults, timeout=60)  # nadpisanie wybranego klucza
```

> **Płytka kopia** kopiuje tylko zewnętrzny słownik. Jeśli wartości to mutowalne obiekty (np. listy, inne słowniki), oba słowniki wciąż wskazują na te **same** obiekty w pamięci.

```python
original = {"config": {"debug": True, "timeout": 30}}
shallow = dict(original)

shallow["config"]["debug"] = False
print(original["config"]["debug"])  # False — oryginał też się zmienił! ⚠️
```

**Głęboka kopia (deep copy)** — kopiuje rekurencyjnie cały graf obiektów:

```python
import copy

original = {"config": {"debug": True, "timeout": 30}}
deep = copy.deepcopy(original)

deep["config"]["debug"] = False
print(original["config"]["debug"])  # True — oryginał nienaruszony ✅
```

| Metoda | Zewnętrzny dict | Zagnieżdżone obiekty |
|---|---|---|
| `dict(d)` / `d.copy()` | nowa kopia | **te same referencje** |
| `copy.deepcopy(d)` | nowa kopia | **nowe kopie** (rekurencyjnie) |

> W Pythonie 3.9+ prościej użyć operatora `|`:
> ```python
> merged = defaults | {"timeout": 60}
> ```

### Porównanie wydajności

```python
import timeit

timeit.timeit("{}", number=10_000_000)       # ~0.06s
timeit.timeit("dict()", number=10_000_000)   # ~0.12s
```

Literał `{}` jest szybszy z tego samego powodu co `[]`: nie wymaga wyszukiwania nazwy w przestrzeni nazw.

---

## `set()` vs `{1, 2, 3}` — szczególny przypadek!

### Uwaga: `{}` to pusty `dict`, NIE set!

```python
type({})        # <class 'dict'>   — SŁOWNIK!
type({1, 2, 3}) # <class 'set'>    — zbiór
type(set())     # <class 'set'>    — pusty zbiór
```

> ⚠️ **Aby stworzyć pusty zbiór, MUSISZ użyć `set()`** — nie ma literałowej składni dla pustego seta.

### Kiedy używać `{1, 2, 3}` (literał)

Gdy tworzysz zbiór z góry znanych elementów:

```python
vowels = {"a", "e", "i", "o", "u"}
primes = {2, 3, 5, 7, 11}
```

### Kiedy używać `set()` (konstruktor)

Konwersja z iterowalnego — najczęstszy przypadek:

```python
# Usunięcie duplikatów z listy
numbers = [1, 2, 2, 3, 3, 3]
unique = set(numbers)  # {1, 2, 3}

# Ze stringa — unikalne znaki
chars = set("banana")  # {'b', 'a', 'n'}

# Z generatora
evens = set(range(0, 10, 2))  # {0, 2, 4, 6, 8}
```

---

## `frozenset()` — niemutowalny zbiór

Dla `frozenset` nie istnieje żadna składnia literałowa — jedynym sposobem jest konstruktor:

```python
fs = frozenset({1, 2, 3})
fs = frozenset([1, 1, 2, 3])  # działa jak set(), usuwa duplikaty

# frozenset można użyć jako klucz słownika (jest haszowalny!)
cache = {frozenset([1, 2]): "result"}
```

---

## `tuple()` vs `(1, 2, 3)`

### Kiedy używać `(1, 2, 3)` (literał) — **preferowane**

```python
point = (10, 20)
rgb = (255, 128, 0)
```

> Uwaga: sam nawias `()` to **NIE jest** pusta krotka. Pusty tuple to `()`, ale krotka z jednym elementem wymaga przecinka: `(42,)`.

```python
type(())     # <class 'tuple'>  — pusta krotka ✅
type((42))   # <class 'int'>    — to tylko liczba w nawiasach!
type((42,))  # <class 'tuple'>  — krotka jednoelementowa ✅
```

### Kiedy używać `tuple()` (konstruktor)

Konwersja z innego iterowalnego:

```python
as_tuple = tuple([1, 2, 3])    # (1, 2, 3)
as_tuple = tuple("abc")        # ('a', 'b', 'c')
as_tuple = tuple(range(3))     # (0, 1, 2)
```

---

## Tabela podsumowująca

| Kolekcja    | Literał preferowany?   | Konstruktor — kiedy użyć                          |
|-------------|------------------------|---------------------------------------------------|
| `list`      | `[]` ✅                | Konwersja `list(iterable)` — range, tuple, str   |
| `dict`      | `{}` ✅                | Konwersja par, składnia keyword: `dict(a=1)`     |
| `set`       | `{1, 2}` ✅            | **Pusty set** (`set()`), konwersja `set(iterable)` |
| `frozenset` | brak — tylko `frozenset()` | Zawsze konstruktor                           |
| `tuple`     | `(1, 2)` ✅            | Konwersja `tuple(iterable)` — lista, range, str  |

---

## Powiązane pliki

- [Kiedy używać `Dict`/`List` (typing) a `dict`/`list`](kiedy-uzywac-dict-list-a-kiedy-dict-list.md)
- [Krotki vs Listy: Pamięć, Wydajność i Haszowalność](krotki-vs-listy-pamiec-i-wydajnosc.md)
- [Porównywanie list i setów](porownywanie-list-i-setow.md)
- [Typy danych w Python i zużycie pamięci](typy-danych-w-python-i-zuzycie-pamieci.md)
