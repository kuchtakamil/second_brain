# Deprecated typing w Pythonie

**Data:** 2026-02-01

---

**User:**

typing w python jest już deprecated. czego używać zamiast tego?

---

**Assistant:**

Masz rację — **`typing` w starej formie jest de facto wygaszany**. Nie w sensie „usunięty”, ale **w sensie stylu i rekomendacji od Pythona 3.9+ oraz szczególnie 3.10+ i 3.12+**.

Dzisiaj obowiązuje zasada:

> **Nie używasz już `typing.List`, `typing.Dict`, `typing.Optional`, `typing.Union`, itd.**

Używasz **wbudowanych typów języka**.

To jest efekt PEP 585, PEP 604 i kilku kolejnych.

---

## 🔴 Stare (typing – legacy styl)

```python
from typing import List, Dict, Optional, Union

def foo(x: List[int]) -> Dict[str, Optional[int]]:
    ...
    
def bar(x: Union[int, str]) -> None:
    ...
```

To jest dzisiaj traktowane jako **legacy typing**.

---

## 🟢 Nowoczesny styl (Python 3.9+)

### List / Dict / Set / Tuple

```python
def foo(x: list[int]) -> dict[str, int | None]:
    ...
```

Bez importów z `typing`.

---

### Optional i Union (PEP 604)

```python
# było
Optional[int]
Union[int, str]

# jest
int | None
int | str
```

---

### Tuple

```python
tuple[int, str]
```

---

### Callable

Tutaj robisz import, ale z **`collections.abc`**, a nie `typing` (kolejny efekt PEP 585):

```python
from collections.abc import Callable

def f(x: Callable[[int], str]) -> None:
    ...
```

---

### Generics w klasach i funkcjach

Przed Pythonem 3.12 musieliśmy korzystać z `TypeVar` i `Generic` z modułu `typing`:

```python
from typing import TypeVar, Generic

T = TypeVar('T')

class Repo(Generic[T]):
    def get(self) -> T: ...
```

**Od Pythona 3.12 (PEP 695)** wprowadzono wbudowaną składnię. Nie potrzebujesz już żadnego importu z `typing`:

```python
class Repo[T]:
    def get(self) -> T | None: ...
    
def get_first[T](items: list[T]) -> T:
    return items[0]
```

---

### Typy aliasowane (TypeAlias / type) a NewType

Pytanie: *Czy TypeAlias (nowy sposób) to coś, co zastępuje NewType?*
**Odpowiedź: NIE.** Mają dwa zupełnie inne zastosowania! 

#### 1. Aliasy (TypeAlias / type) - skróty dla czytelności
Alias oznacza: "Będę używał krótszej nazwy `A`, ale sprawdzarka typów (np. mypy) ma to traktować DOKŁADNIE tak jakby wpisano pierwotny, długi typ `B`".

W Pythonie 3.10 dodano `TypeAlias`, a **od Pythona 3.12 (PEP 695)** wprowadzono nową wbudowaną składnię — słowo kluczowe `type`:

```python
# Python 3.10 - 3.11
from typing import TypeAlias
Matrix: TypeAlias = list[list[float]]

# Python 3.12+ (nowoczesny standard)
type Matrix = list[list[float]]
```
Z punktu widzenia sprawdzarki typów `Matrix` i `list[list[float]]` to **ta sama rzecz**.

#### 2. Nowy unikalny typ (NewType) - bezpieczeństwo logiki
`NewType` nadal jest niezwykle przydatny. Służy do zapobiegania błędom tam, gdzie obiekty posługują się tym samym bazowym typem, ale reprezentują kompletnie inne byty w domenie biznesowej. Tworzy on hermetyczny typ bazujący na typie wyjściowym.

```python
from typing import NewType

UserId = NewType('UserId', int)
OrderId = NewType('OrderId', int)

def process_user(user_id: UserId) -> None:
    pass

my_user_id = UserId(123)
process_user(my_user_id) # OK 🟢
process_user(123)        # 🔴 BŁĄD LINTERA: oczekiwano UserId, a przekazano int (pomimo wiodącego int)
```
W czasie uruchomienia ("runtime") funkcja "konstruktora" jest przezroczysta. Oznacza to, że `UserId` działa tak samo szybko jako zwykły `int`, nie wprowadza najmniejszego narzutu procesora, ale narzędzia jak mypy skutecznie uchronią Cię przed pomyłką i skrzyżowaniem obu typów przez przypadek.

---

### TypedDict / Protocol / Literal / Final

Te **zostają w `typing`**, bo nie mają odpowiedników:

```python
from typing import TypedDict, Protocol, Literal, Final
```

---

## 🧠 Mental model

Dzisiaj:

| Chcę | Używam |
|---|---|
| list | `list[int]` |
| dict | `dict[str, int]` |
| optional | `int | None` |
| union | `A | B` |
| tuple | `tuple[int, str]` |
| generics | `class A[T]` |
| callable | `collections.abc.Callable` |
| protocol | `typing.Protocol` |
| typed dict | `typing.TypedDict` |

---

## Dlaczego `typing` jest „deprecated”?

Bo:

- był workaroundem zanim język miał generics
- od 3.9 Python **ma generics wbudowane w typy**
- od 3.10 Python ma `|`
- od 3.12 Python ma prawdziwe generics w klasach

Więc `typing.List` itd. to relikt sprzed PEP 585.

---

## Jak dziś wygląda „idiomatyczny” Python typing (3.12)

```python
class Cache[K, V]:
    def __init__(self) -> None:
        self._data: dict[K, V] = {}

    def get(self, key: K) -> V | None:
        return self._data.get(key)
```

Zero `typing`.

---

## Kiedy nadal importujesz z `typing`

Tylko dla:

```python
Protocol
TypedDict
Literal
Final
NewType
Annotated
TypeAlias # (na Python < 3.12, na 3.12+ wbudowane słowo `type`)
```

Reszta — nie.

---

## TL;DR

Jeśli widzisz:

```python
from typing import List, Dict, Optional, Union
```

to w 2025 to jest sygnał:

> „ten kod ma styl z Pythona 3.7”.

Nowy kod **nie powinien** tego robić.