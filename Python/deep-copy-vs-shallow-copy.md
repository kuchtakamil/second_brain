# Deep Copy vs Shallow Copy w Pythonie

Kopiowanie obiektów w Pythonie dzieli się na dwa rodzaje:

- **Shallow copy (płytka kopia)** — tworzy nowy obiekt, ale zawartość (elementy wewnątrz) nadal wskazuje na te same obiekty w pamięci co oryginał.
- **Deep copy (głęboka kopia)** — tworzy nowy obiekt **i rekurencyjnie kopiuje wszystkie zagnieżdżone obiekty**. Kopia jest w pełni niezależna od oryginału.

---

## Dlaczego to ważne?

Python domyślnie **nie kopiuje** obiektów przy przypisaniu — tworzy tylko nowe odwołanie do tego samego miejsca w pamięci:

```python
a = [1, 2, 3]
b = a        # b i a wskazują na ten sam obiekt!
b.append(4)
print(a)     # [1, 2, 3, 4] — oryginał został zmieniony!
```

Jeśli chcesz naprawdę niezależną kopię, musisz użyć shallow copy lub deep copy.

---

## Moduł `copy`

Python udostępnia moduł standardowy `copy` do kopiowania obiektów:

```python
import copy

copy.copy(obj)      # shallow copy
copy.deepcopy(obj)  # deep copy
```

---

## Shallow Copy — płytka kopia

Tworzy nowy kontener (np. listę), ale **elementy wewnątrz nie są kopiowane** — są współdzielone z oryginałem.

### `list`

```python
import copy

original = [[1, 2], [3, 4]]
shallow = copy.copy(original)

shallow[0].append(99)
print(original)  # [[1, 2, 99], [3, 4]] — wewnętrzna lista ZMIENIONA!
print(shallow)   # [[1, 2, 99], [3, 4]]

# Ale zmiana samego kontenera nie wpływa na oryginał:
shallow.append([5, 6])
print(original)  # [[1, 2, 99], [3, 4]] — oryginał bez zmian
```

**Skróty dla list** (bez `copy`):

```python
original = [1, 2, 3]
shallow1 = original[:]         # slice
shallow2 = list(original)      # konstruktor
shallow3 = original.copy()     # metoda .copy()
```

### `dict`

```python
import copy

original = {"a": [1, 2], "b": [3, 4]}
shallow = copy.copy(original)
# Równoważnie: shallow = original.copy() lub shallow = dict(original)

shallow["a"].append(99)
print(original)  # {'a': [1, 2, 99], 'b': [3, 4]} — lista wewnątrz ZMIENIONA!

shallow["c"] = [5, 6]
print(original)  # {'a': [1, 2, 99], 'b': [3, 4]} — nowy klucz nie dotarł do oryginału
```

**Skróty dla dict**:

```python
original = {"x": 1, "y": 2}
shallow1 = original.copy()
shallow2 = dict(original)
shallow3 = {**original}    # unpacking
```

### `set`

Sety przechowują tylko obiekty hashowalne (np. liczby, stringi) — nie mogą zawierać list czy słowników, więc shallow i deep copy dają ten sam efekt praktyczny.

```python
import copy

original = {1, 2, 3}
shallow = copy.copy(original)
# Równoważnie: shallow = original.copy() lub shallow = set(original)

shallow.add(99)
print(original)  # {1, 2, 3} — oryginał bez zmian (elementy niemutowalne)
```

### `tuple`

Tuple są niemutowalne — `copy.copy()` zwraca **ten sam obiekt** (optymalizacja Pythona), bo nie ma sensu kopiować czegoś, co nie może się zmienić.

```python
import copy

original = (1, 2, 3)
shallow = copy.copy(original)
print(original is shallow)  # True — to ten sam obiekt!
```

---

## Deep Copy — głęboka kopia

Kopiuje **rekurencyjnie wszystko** — zarówno kontener, jak i wszystkie zagnieżdżone obiekty. Kopia jest w pełni niezależna.

### `list`

```python
import copy

original = [[1, 2], [3, 4]]
deep = copy.deepcopy(original)

deep[0].append(99)
print(original)  # [[1, 2], [3, 4]] — oryginał NIEZMIENIONY
print(deep)      # [[1, 2, 99], [3, 4]]
```

### `dict`

```python
import copy

original = {"a": [1, 2], "b": {"nested": [10, 20]}}
deep = copy.deepcopy(original)

deep["b"]["nested"].append(99)
print(original)  # {'a': [1, 2], 'b': {'nested': [10, 20]}} — NIEZMIENIONY
print(deep)      # {'a': [1, 2], 'b': {'nested': [10, 20, 99]}}
```

### `set`

Ponieważ sety mogą zawierać tylko niemutowalne elementy, deep copy zachowuje się tak samo jak shallow copy:

```python
import copy

original = frozenset({1, 2, 3})     # frozenset jest hashable, może być elementem
deep = copy.deepcopy(original)
print(original is deep)  # True — Python optymalizuje niemutowalne obiekty
```

### `tuple` z mutowalnymi elementami

```python
import copy

original = ([1, 2], [3, 4])   # tuple zawierający listy
deep = copy.deepcopy(original)

deep[0].append(99)
print(original)  # ([1, 2], [3, 4]) — NIEZMIENIONY
print(deep)      # ([1, 2, 99], [3, 4])
```

---

## Porównanie — tabela

| Operacja | Nowy kontener? | Zagnieżdżone obiekty skopiowane? |
|---|---|---|
| `b = a` (przypisanie) | ❌ | ❌ |
| `copy.copy(a)` | ✅ | ❌ (współdzielone) |
| `copy.deepcopy(a)` | ✅ | ✅ (w pełni niezależne) |

---

## Kiedy używać której kopii?

| Sytuacja | Wybór |
|---|---|
| Prosta, płaska lista/słownik z wartościami prostymi (`int`, `str`) | Shallow copy wystarczy |
| Zagnieżdżone struktury (lista list, słownik ze słownikami czy listami) | **Deep copy** |
| Zależy Ci na wydajności i wiesz, że zagnieżdżenia nie będą mutowane | Shallow copy |
| Budujesz niezależne kopie dla wielowątkowości lub immutability | **Deep copy** |

> **Uwaga:** `copy.deepcopy()` jest **wolniejsze** niż `copy.copy()`, bo musi rekurencyjnie przejść przez cały obiekt. Nie używaj go bez potrzeby.

---

## Powiązane pliki

- [Typy danych w Pythonie i zużycie pamięci](typy-danych-w-python-i-zuzycie-pamieci.md)
- [Dodawanie list do słownika](dodawanie-list-do-słownika.md)
- [Porównywanie list i setów](porównywanie-list-i-setów.md)
- [Konstruktory vs literały dict, list, set](konstruktory-vs-literaly-dict-list-set.md)
