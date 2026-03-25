# Odpowiedniki equals hashCode w Pythonie

**Data:** 2025-12-27

---

**User:**

W Java są metody equals i hashCode oraz odpowiednie reguły jak te dwie metody odnoszą się do siebie. Czy w Python są odpowiedniki tych metod?

---

**Assistant:**

Tak — w Pythonie też są odpowiedniki **`equals`** i **`hashCode`**, tylko mają trochę inną formę i *kilka ważnych niuansów*.

---

## Odpowiednik `equals` → `__eq__`

W Pythonie porównywanie obiektów realizuje metoda specjalna:

```python
__eq__(self, other)
```

Przykład:

```python
class User:
    def __init__(self, user_id):
        self.user_id = user_id

    def __eq__(self, other):
        if not isinstance(other, User):
            return NotImplemented
        return self.user_id == other.user_id
```

Użycie:

```python
u1 = User(1)
u2 = User(1)

u1 == u2   # True
u1 is u2   # False (tożsamość obiektu, jak == vs == w Javie)
```

📌 `==` wywołuje `__eq__`  
📌 `is` sprawdza tożsamość (jak `==` na referencjach w Javie)

---

## Odpowiednik `hashCode` → `__hash__`

Python ma metodę:

```python
__hash__(self)
```

która zwraca liczbę typu `int`.

Przykład:

```python
class User:
    def __init__(self, user_id):
        self.user_id = user_id

    def __eq__(self, other):
        if not isinstance(other, User):
            return NotImplemented
        return self.user_id == other.user_id

    def __hash__(self):
        return hash(self.user_id)
```

---

## Zasada relacji `__eq__` ↔ `__hash__` (jak w Javie)

Reguła jest **identyczna jak w Javie**:

> Jeśli `a == b` jest `True`, to `hash(a) == hash(b)` **musi** być prawdą.

Python **nie wymusza** tego technicznie — to odpowiedzialność programisty.

---

## ⚠️ Bardzo ważny niuans Pythona (częsta pułapka)

Jeśli **nadpiszesz `__eq__`**, ale **nie zdefiniujesz `__hash__`**, to:

```python
__hash__ = None
```

czyli obiekt **staje się niehashowalny** ❌

```python
u = User(1)
hash(u)       # TypeError
set([u])      # TypeError
```

To jest *celowe* — Python chroni przed łamaniem kontraktu hash/eq.

W Javie łatwo popełnić błąd, w Pythonie trzeba się bardziej postarać 😉

---

## Domyślne zachowanie (bez nadpisywania)

Jeśli **nic nie nadpiszesz**:

| Metoda | Zachowanie |
|------|-----------|
| `__eq__` | porównanie referencji (jak `==` w Javie) |
| `__hash__` | oparty o identyfikator obiektu |

---

## Immutable vs mutable (ważniejsze niż w Javie)

Zasada praktyczna:

> Jeśli obiekt jest **mutowalny** i używany jako klucz → **nie implementuj `__hash__`**

Dlaczego?

```python
class User:
    def __init__(self, user_id):
        self.user_id = user_id

    def __hash__(self):
        return hash(self.user_id)

u = User(1)
s = {u}

u.user_id = 2   # 💥 hash się zmienia
u in s          # False (!)
```

To dokładnie ten sam problem co z mutable key w `HashMap` w Javie — tylko w Pythonie łatwiej go sobie zrobić.

---

## Pythonowy skrót: `@dataclass`

Jeśli znasz Lomboka, to to będzie znajome 😉

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class User:
    user_id: int
```

Efekt:
- `__eq__` — automatycznie
- `__hash__` — automatycznie
- `frozen=True` → immutable → bezpieczne do `set` / `dict`

---

## TL;DR (Java → Python mapping)

| Java | Python |
|----|------|
| `equals()` | `__eq__()` |
| `hashCode()` | `__hash__()` |
| `==` (prymitywy) | `==` |
| `==` (referencje) | `is` |
| `HashMap` | `dict` |
| `HashSet` | `set` |

---

Jeśli chcesz, mogę:
- porównać **kontrakty Java vs Python punkt po punkcie**
- pokazać **jak Python łamie kontrakt w praktyce**
- albo doradzić **jak projektować obiekty domenowe w Pythonie w stylu DDD**

Daj znać 👍