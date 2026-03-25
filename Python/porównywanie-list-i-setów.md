# Porównywanie list i setów

**Data:** 2026-02-09

---

**User:**

Python: jak wygląda prównywanie list i set?

---

**Assistant:**

W Pythonie porównywanie `list` i `set` **różni się semantycznie**, bo to są inne struktury danych z inną logiką:

- `list` → **kolejność ma znaczenie**, duplikaty mają znaczenie
- `set` → **kolejność nie ma znaczenia**, duplikaty nie istnieją

To wpływa bezpośrednio na to, jak działa operator `==` i operatory porównania.

---

## 🔹 Porównywanie list

Listy są porównywane **element po elemencie, w kolejności**.

```python
[1, 2, 3] == [1, 2, 3]      # True
[1, 2, 3] == [3, 2, 1]      # False (inna kolejność)
[1, 2, 2] == [1, 2]         # False (duplikaty mają znaczenie)
```

Python robi to tak, jakby:

```
len(list1) == len(list2)
i każdy element pod tym samym indeksem jest równy
```

---

## 🔹 Porównywanie setów

Sety są porównywane jako **zbiory matematyczne**.

```python
{1, 2, 3} == {3, 2, 1}      # True (kolejność ignorowana)
{1, 2, 2} == {1, 2}         # True (duplikaty ignorowane)
{1, 2} == {1, 2, 3}         # False
```

Liczy się tylko to, **czy oba zbiory zawierają dokładnie te same elementy**.

---

## 🔹 Najczęstszy błąd: porównywanie list jak setów

Bardzo częsty błąd:

```python
list1 == list2
```

gdy tak naprawdę chcemy:

> „czy zawierają te same elementy, niezależnie od kolejności”

Wtedy poprawnie:

```python
set(list1) == set(list2)
```

ALE to działa **tylko gdy duplikaty nie mają znaczenia**.

---

## 🔹 Gdy duplikaty mają znaczenie, ale kolejność nie

To już nie jest ani `list`, ani `set`, tylko **multiset (bag)**.

W Pythonie robi się to przez `collections.Counter`:

```python
from collections import Counter

Counter([1,2,2,3]) == Counter([3,2,1,2])  # True
Counter([1,2,2,3]) == Counter([1,2,3])    # False
```

To jest **najbardziej poprawny semantycznie sposób** na:
> porównanie list ignorując kolejność, ale uwzględniając liczbę wystąpień.

---

## 🔹 Operatory porównania (`<`, `>`, `<=`, `>=`)

Tu wychodzi kolejna różnica:

### Listy – leksykograficznie (jak stringi)

```python
[1, 2, 3] < [1, 2, 4]   # True
[1, 5] > [1, 2, 100]    # True
```

Porównywane element po elemencie.

---

### Sety – relacje zbiorów

```python
{1, 2} < {1, 2, 3}     # True  (subset)
{1, 2, 3} > {1, 2}     # True  (superset)
{1, 2} < {2, 3}        # False (nie jest podzbiorem)
```

To **nie jest** porównanie wartości, tylko relacja podzbioru.

---

## 🔹 TL;DR — co właściwie porównujesz?

| Chcesz sprawdzić | Poprawny sposób |
|---|---|
| Te same elementy w tej samej kolejności | `list1 == list2` |
| Te same elementy, kolejność nieważna, duplikaty nieważne | `set(list1) == set(list2)` |
| Te same elementy, kolejność nieważna, duplikaty ważne | `Counter(list1) == Counter(list2)` |
| Czy jedna kolekcja zawiera wszystkie elementy drugiej | `set(a) >= set(b)` |

---

## 🔥 Mentalny model

- `list` → sekwencja
- `set` → zbiór
- `Counter` → multizbiór

I porównujesz je zgodnie z ich **matematyczną naturą**, nie „bo to kolekcja”.

---

**User:**

co z porównywaniem elementów list kiedy są złożonymi obiektami i mają lub nie mają przeciążone __eq__?

---

**Assistant:**

To jest **kluczowy, często pomijany aspekt** porównań kolekcji w Pythonie.

Bo tak naprawdę:

> `list == list` **nie porównuje list**  
> tylko wykonuje **serię wywołań `__eq__` na elementach**.

Czyli semantyka porównania listy/seta **w 100% zależy od tego, jak elementy implementują `__eq__` (i czasem `__hash__`)**.

---

# 🔹 Jak Python porównuje listy pod spodem

Dla:

```python
list1 == list2
```

Python robi logicznie:

```python
if len(list1) != len(list2):
    return False

for a, b in zip(list1, list2):
    if not (a == b):   # <- TU wywołuje się a.__eq__(b)
        return False

return True
```

Więc wszystko zależy od tego, co robi `a == b`.

---

# 🔹 Przypadek 1 — brak `__eq__`

```python
class User:
    def __init__(self, id):
        self.id = id

u1 = User(1)
u2 = User(1)

[u1] == [u2]   # False
```

Dlaczego?

Bo domyślne `__eq__` z `object` to:

```
porównanie tożsamości (is)
```

Czyli:

```
u1 == u2  <=>  u1 is u2
```

---

# 🔹 Przypadek 2 — jest `__eq__`, brak `__hash__`

```python
class User:
    def __init__(self, id):
        self.id = id
    def __eq__(self, other):
        return self.id == other.id
```

Teraz:

```python
[User(1)] == [User(1)]   # True
```

Ale:

```python
set([User(1)])           # TypeError: unhashable type
```

Bo Python wykrywa, że masz `__eq__`, ale nie masz spójnego `__hash__`.

---

# 🔹 Przypadek 3 — jest `__eq__` i `__hash__`

```python
class User:
    def __init__(self, id):
        self.id = id
    def __eq__(self, other):
        return self.id == other.id
    def __hash__(self):
        return hash(self.id)
```

Teraz:

```python
set([User(1)]) == set([User(1)])   # True
```

I to jest jedyny moment, gdy `set` zaczyna działać semantycznie tak, jak oczekujesz.

---

# 🔥 Kluczowa różnica: list vs set przy custom obiektach

| | list | set |
|---|---|---|
| używa `__eq__` | ✅ | ✅ |
| używa `__hash__` | ❌ | ✅ |
| wymaga spójności `eq/hash` | ❌ | ✅ (krytyczne) |
| brak `__eq__` | porównuje referencje | porównuje referencje |
| złe `__hash__` | działa | daje *losowe, trudne bugi* |

---

# 🔴 Najgorszy możliwy bug w Pythonie (bardzo częsty)

```python
class User:
    def __init__(self, id):
        self.id = id
    def __eq__(self, other):
        return self.id == other.id
    def __hash__(self):
        return id(self)   # ❌ BŁĄD
```

Teraz:

```python
u1 = User(1)
u2 = User(1)

u1 == u2           # True
set([u1]) == set([u2])   # False  🤯
```

Bo set najpierw używa `__hash__`, a dopiero potem `__eq__`.

Jeśli hash nie wskazuje na równość → obiekty nigdy się nie spotkają do porównania.

---

# 🔹 Co z Counter(list) przy złożonych obiektach?

`Counter` używa **hash + eq**, tak jak `set`.

Czyli ma dokładnie te same wymagania co `set`.

---

# 🔥 Dlaczego czasem `list == list` działa, a `set(list) == set(list)` nie?

Bo:

- list potrzebuje tylko `__eq__`
- set potrzebuje **spójnego** `__eq__` i `__hash__`

To jest klasyczna pułapka przy DTO, ORM encjach, modelach domenowych.

---

# 🔹 Dataclasses i ten problem

```python
@dataclass(eq=True, frozen=True)
class User:
    id: int
```

To automatycznie daje:

- poprawne `__eq__`
- poprawne `__hash__`

Dlatego dataclasses często „magicznie naprawiają” te problemy.

---

# 🔥 Mentalny model seniora Pythona

Jeśli obiekty mają trafić do:

- list → potrzebujesz tylko sensownego `__eq__`
- set / dict / Counter → potrzebujesz **spójnego `eq + hash`**
- porównań kolekcji → tak naprawdę projektujesz semantykę `__eq__` dla klasy

Bo kolekcje są tylko „multiplikatorem” Twojej definicji równości.

---

# TL;DR

To nie `list`/`set` definiuje równość.  
**Twoje `__eq__` i `__hash__` definiują, co znaczy równość kolekcji.**

---

**User:**

czy wywołanie list1 is list2 skutkuje wywołaniem is na każdej parze elementów?

---

**Assistant:**

Nie.

```python
list1 is list2
```

**nigdy nie zagląda do elementów listy.**

To jest czyste porównanie **tożsamości obiektu na poziomie referencji** (pointer equality).

---

## Co dokładnie robi `is`

`is` sprawdza:

> czy obie zmienne wskazują na **ten sam obiekt w pamięci**

Logika jest równoważna:

```python
id(list1) == id(list2)
```

Koniec. Bez pętli. Bez `__eq__`. Bez dotykania elementów.

---

## Kontrast z `==`

To:

```python
list1 == list2
```

powoduje:

- iterację po elementach
- wywołania `a.__eq__(b)`

To:

```python
list1 is list2
```

nie robi absolutnie nic poza sprawdzeniem wskaźnika.

---

## Przykład

```python
a = [User(1)]
b = a
c = [User(1)]

a is b   # True
a is c   # False

a == c   # zależy od __eq__ User
```

---

## Dlaczego to ważne

Czasem ludzie myślą, że:

> „może Python optymalizuje i sprawdza elementy przez `is`”

Nie. `is` to operacja na poziomie CPython C-struct, nie na poziomie semantyki Pythona.

To jest porównanie dwóch wskaźników w C.

Koszt: **O(1)**.

---

## TL;DR

| Operacja | Dotyka elementów? | Wywołuje `__eq__`? | Złożoność |
|---|---|---|---|
| `list1 is list2` | ❌ | ❌ | O(1) |
| `list1 == list2` | ✅ | ✅ | O(n) |