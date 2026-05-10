# Python Cheatsheet

## 1. Sortowanie struktur danych

```python
# list
lst = [3, 1, 2]
lst.sort()                    # in-place, zwraca None
sorted(lst)                   # nowa lista, działa na każdym iterable

# tuple / set / dict
sorted((3,1,2))               # → [1, 2, 3]  (tuple → list)
sorted({3,1,2})               # → [1, 2, 3]  (set → list)
sorted({"b":2,"a":1})         # → ['a', 'b'] (klucze)

# dict po wartościach
d = {"b": 2, "a": 1}
sorted(d.items(), key=lambda x: x[1])   # → [('a',1), ('b',2)]

# własny klucz
words = ["banana", "fig", "apple"]
words.sort(key=len)           # ['fig', 'apple', 'banana']
words.sort(key=str.lower)     # case-insensitive

# reverse
sorted(lst, reverse=True)

# obiekty
class Person:
    def __init__(self, name, age): self.name, self.age = name, age
people = [Person("Alice", 30), Person("Bob", 25)]
people.sort(key=lambda p: p.age)
```

> `sort()` – tylko listy, in-place. `sorted()` – każdy iterable, zwraca nową listę.

---

## 2. Metody stringów – szybki przegląd

```python
c = "Hello"
c.lower()        # 'hello'
c.upper()        # 'HELLO'
c.title()        # 'Hello'
c.strip()        # usuwa whitespace z obu stron
c.lstrip("H")    # 'ello'
c.replace("l","L")  # 'HeLLo'
c.startswith("He")  # True
c.endswith("lo")    # True
c.count("l")     # 2
c.find("l")      # 2  (indeks lub -1)
c.index("l")     # 2  (lub ValueError)

# sprawdzanie znaków
"A".isupper()    # True
"a".islower()    # True
"a".isalpha()    # True    (tylko litery)
"3".isdigit()    # True
"a3".isalnum()   # True    (litery + cyfry)
" ".isspace()    # True
```

---

## 3. Slicing stringów (i list)

Składnia: `seq[start:stop:step]` – `start` włącznie, `stop` wyłącznie. Ujemne indeksy liczą od końca.

```python
text = "hello world"
#       0123456789...

# podstawowe
text[4:]      # 'o world'  – od indeksu 4 do końca
text[:4]      # 'hell'     – od początku do indeksu 4 (wyłącznie)
text[2:7]     # 'llo w'    – od 2 do 7 (wyłącznie)

# ujemne indeksy
text[-5:]     # 'world'    – ostatnie 5 znaków
text[:-5]     # 'hello '   – wszystko oprócz ostatnich 5
text[-5:-2]   # 'wor'      – wycinek od końca

# step (krok)
text[::2]     # 'hlowrd'   – co drugi znak
text[1::2]    # 'el ol'    – co drugi, start=1
text[::-1]    # 'dlrow olleh' – odwrócony string
text[10:2:-1] # 'dlrow oll'  – od 10 do 2 (wyłącznie), wstecz

# listy – te same zasady
lst = [0, 1, 2, 3, 4, 5, 6]
lst[3:]       # [3, 4, 5, 6]
lst[:3]       # [0, 1, 2]
lst[1:5]      # [1, 2, 3, 4]
lst[::2]      # [0, 2, 4, 6]
lst[::-1]     # [6, 5, 4, 3, 2, 1, 0]
lst[1:5:2]    # [1, 3]

# slice jako obiekt (reużywalny)
s = slice(1, 5, 2)
lst[s]        # [1, 3]
```

> `text[-4:]` → ostatnie 4 znaki &nbsp;|&nbsp; `text[:-4]` → wszystko oprócz ostatnich 4

---

## 4. Substring

```python
text = "hello world"
"world" in text          # True  – najszybszy, pythonic
text.find("world")       # 6     (-1 jeśli brak)
text.index("world")      # 6     (ValueError jeśli brak)
text.count("l")          # 3
text.startswith("hello") # True
text.endswith("world")   # True

# wszystkie wystąpienia (pozycje)
import re
[m.start() for m in re.finditer("l", text)]  # [2, 3, 9]
```

---

## 5. split() i join()

```python
"a,b,c".split(",")          # ['a', 'b', 'c']
"  a  b  c  ".split()       # ['a', 'b', 'c']  – domyślnie whitespace + strip
"a.b.c".split(".", 1)       # ['a', 'b.c']  – max 1 podział
"hello\nworld".splitlines() # ['hello', 'world']

# join – odwrotność split
",".join(["a","b","c"])     # 'a,b,c'
" ".join(["hello","world"]) # 'hello world'
```

---

## 6. Wydajny string concatenation

```python
# ŹLE – O(n²), tworzy nowy string za każdym razem
result = ""
for s in ["a","b","c","d"]:
    result += s

# DOBRZE – O(n)
result = "".join(["a","b","c","d"])

# f-string dla małej liczby elementów
name, age = "Alice", 30
s = f"Name: {name}, Age: {age}"

# %-formatting (legacy) i .format()
"Hello %s" % name
"Hello {}".format(name)

# io.StringIO dla bardzo dużych buforów
import io
buf = io.StringIO()
buf.write("hello")
buf.write(" world")
result = buf.getvalue()  # 'hello world'
```

---

## 7. list.pop() i inne metody listy

```python
lst = [1, 2, 3, 4, 5]
lst.pop()       # usuwa i zwraca ostatni element → 5
lst.pop(0)      # usuwa i zwraca element o indeksie 0 → 1
lst.append(6)   # dodaje na koniec
lst.insert(1, 9)# wstawia 9 na index 1
lst.remove(9)   # usuwa pierwsze wystąpienie wartości
lst.extend([7,8])    # łączy listy in-place
lst.index(2)    # indeks pierwszego wystąpienia
lst.count(2)    # liczba wystąpień
lst.reverse()   # in-place
lst.clear()     # usuwa wszystkie elementy

# list jako stack
stack = []
stack.append("a")
stack.pop()     # LIFO

# list jako queue (lepiej collections.deque)
from collections import deque
q = deque(["a","b","c"])
q.appendleft("z")
q.popleft()     # FIFO
```

---

## 8. set() i operacje na zbiorach

```python
import string

letters = set("hello")        # {'h', 'e', 'l', 'o'}
set(string.ascii_lowercase)   # wszystkie małe litery a-z

# sprawdzenie czy string zawiera wszystkie małe litery
letters = set("thequickbrownfoxjumpsoverthelazydog")
letters >= set(string.ascii_lowercase)   # True (superset)
set(string.ascii_lowercase).issubset(letters)  # True

# operacje
a = {1,2,3}
b = {2,3,4}
a | b    # {1,2,3,4}  unia
a & b    # {2,3}      część wspólna
a - b    # {1}        różnica
a ^ b    # {1,4}      różnica symetryczna
```

---

## 9. collections.Counter

```python
from collections import Counter

c = Counter("aabbcc")           # Counter({'a':2,'b':2,'c':2})
c = Counter([1,1,2,3,3,3])     # Counter({3:3, 1:2, 2:1})
c = Counter({"a":3,"b":1})

c["a"]          # 3

print(c)                  # Zwróci: Counter({'a': 3, 'b': 1})
print(list(c.elements())) # Zwróci: ['a', 'a', 'a', 'b']
print(c.most_common(1))   # Zwróci: [('a', 3)]
print(c.total())          # suma wszystkich, Zwróci: 4

c.most_common(2)# [('a',3),('b',1)]

# arytmetyka
c1 = Counter("aab")
c2 = Counter("abb")
c1 + c2         # Counter({'a':3,'b':3})
c1 - c2         # Counter({'a':1})
c1 & c2         # Counter({'a':1,'b':1})  min
c1 | c2         # Counter({'a':2,'b':2})  max

# anagram check
Counter("listen") == Counter("silent")  # True
```

---

## 10. collections – reszta modułu

```python
from collections import defaultdict, OrderedDict, namedtuple, deque, ChainMap

# defaultdict – brak KeyError
dd = defaultdict(list)
dd["key"].append(1)     # nie trzeba inicjować

dd = defaultdict(int)
for c in "hello":
    dd[c] += 1          # zliczanie

# namedtuple
Point = namedtuple("Point", ["x","y"])
p = Point(1, 2)
p.x, p.y    # 1, 2
p._asdict() # {'x':1,'y':2}

# deque – O(1) z obu stron
dq = deque(maxlen=3)    # automatycznie usuwa stare elementy
dq.append(1); dq.appendleft(0)

# ChainMap – wiele dict jako jeden widok
defaults = {"color": "red"}
user     = {"color": "blue"}
merged   = ChainMap(user, defaults)
merged["color"]  # 'blue' (priorytet pierwszy dict)
```

---

## 11. Słowniki (dict) – przydatne wzorce

```python
d = {"a": 1, "b": 2}

d.get("c", 0)           # 0 – bezpieczny dostęp
d.setdefault("c", 0)    # dodaje "c":0 jeśli nie istnieje, zwraca wartość
d.items()               # widok par (k,v)
d.keys()                # widok kluczy
d.values()              # widok wartości
d.update({"c": 3})      # łączenie

# merge (Python 3.9+)
merged = {"a":1} | {"b":2}   # {'a':1,'b':2}

# dict comprehension
squares = {x: x**2 for x in range(5)}

# inwersja dict
inv = {v: k for k, v in d.items()}

# grupowanie
from itertools import groupby
data = [("a",1),("b",2),("a",3)]
from collections import defaultdict
grouped = defaultdict(list)
for k, v in data:
    grouped[k].append(v)
```

---

## 12. List / Set / Dict Comprehensions

```python
# list comprehension
[x**2 for x in range(10) if x % 2 == 0]   # [0,4,16,36,64]

# set comprehension
{c.lower() for c in "Hello World" if c.isalpha()}

# dict comprehension
{k: v for k, v in zip("abc", [1,2,3])}

# generator expression (leniwy, oszczędny pamięciowo)
total = sum(x**2 for x in range(10**6))

# zagnieżdżony
matrix = [[1,2],[3,4],[5,6]]
flat = [x for row in matrix for x in row]  # [1,2,3,4,5,6]
```

---

## 13. Lambda, map, filter, zip, enumerate

```python
# lambda
fn = lambda x, y: x + y
fn(2, 3)   # 5

# map
list(map(lambda x: x**2, [1,2,3]))   # [1,4,9]
list(map(str, [1,2,3]))              # ['1','2','3']

# filter
list(filter(lambda x: x > 2, [1,2,3,4]))  # [3,4]

# zip
list(zip([1,2,3], ["a","b","c"]))    # [(1,'a'),(2,'b'),(3,'c')]
dict(zip("abc", [1,2,3]))            # {'a':1,'b':2,'c':3}

# unzip
pairs = [(1,'a'),(2,'b')]
nums, chars = zip(*pairs)            # (1,2), ('a','b')

# enumerate
for i, val in enumerate(["a","b"], start=1):
    print(i, val)   # 1 a, 2 b
```

---

## 14. *args i **kwargs

```python
def func(*args, **kwargs):
    print(args)    # tuple
    print(kwargs)  # dict

func(1, 2, a=3, b=4)
# (1, 2)
# {'a': 3, 'b': 4}

# unpacking przy wywołaniu
def add(a, b, c): return a+b+c
add(*[1,2,3])
add(**{"a":1,"b":2,"c":3})
```

---

## 15. Dekoratory

```python
from functools import wraps

def my_decorator(func):
    @wraps(func)   # zachowuje __name__, __doc__
    def wrapper(*args, **kwargs):
        print("before")
        result = func(*args, **kwargs)
        print("after")
        return result
    return wrapper

@my_decorator
def greet(name): return f"Hello {name}"

# dekorator z parametrem
def repeat(n):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(n):
                func(*args, **kwargs)
        return wrapper
    return decorator

@repeat(3)
def hi(): print("hi")
```

---

## 16. Generatory i yield

```python
# generator function
def countdown(n):
    while n > 0:
        yield n
        n -= 1

list(countdown(5))   # [5,4,3,2,1]

# yield from
def chain(*iters):
    for it in iters:
        yield from it

# generator expression
gen = (x**2 for x in range(10))
next(gen)   # 0
next(gen)   # 1

# send() – coroutine
def accumulator():
    total = 0
    while True:
        value = yield total
        total += value

acc = accumulator()
next(acc)     # inicjalizacja → 0
acc.send(10)  # → 10
acc.send(5)   # → 15
```

---

## 17. Context Managers

```python
# with statement
with open("file.txt", "r") as f:
    content = f.read()

# własny context manager
class MyCM:
    def __enter__(self):
        print("start")
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("end")
        return False   # True = tłumi wyjątki

# dekorator @contextmanager
from contextlib import contextmanager

@contextmanager
def managed():
    print("setup")
    try:
        yield "resource"
    finally:
        print("teardown")

with managed() as r:
    print(r)
```

---

## 18. Wyjątki

```python
try:
    x = 1 / 0
except ZeroDivisionError as e:
    print(e)
except (TypeError, ValueError) as e:
    print(e)
else:
    print("brak wyjątku")
finally:
    print("zawsze")

# własny wyjątek
class AppError(Exception):
    def __init__(self, msg, code=None):
        super().__init__(msg)
        self.code = code

raise AppError("coś poszło nie tak", code=404)

# re-raise
try:
    risky()
except Exception:
    raise   # ponownie rzuca ten sam wyjątek
```

---

## 19. Klasy – kluczowe koncepty

```python
class Animal:
    species = "Animalia"   # class variable

    def __init__(self, name):
        self.name = name   # instance variable

    def speak(self):       # instance method
        return f"{self.name} says ..."

    @classmethod
    def create(cls, name): # class method
        return cls(name)

    @staticmethod
    def is_animal(): return True   # static method

    def __repr__(self): return f"Animal({self.name!r})"
    def __str__(self):  return self.name
    def __eq__(self, other): return self.name == other.name

class Dog(Animal):
    def speak(self):
        return super().speak().replace("...", "Woof!")

# dataclass (Python 3.7+)
from dataclasses import dataclass, field

@dataclass
class Point:
    x: float
    y: float
    z: float = 0.0
    tags: list = field(default_factory=list)

# __init__
# __repr__
# __eq__
# __order__ (opt)
# __hash__ (opt)
# __match_args__ (opt)
```

---

## 20. Typing – type hints

```python
from typing import Optional, Union, Any
from collections.abc import Callable, Iterator, Generator

def greet(name: str, times: int = 1) -> str:
    return name * times

# Python 3.10+ – X | Y zamiast Union
def foo(x: int | str) -> None: ...

# Optional
def bar(x: int | None = None) -> None: ...

# generyki (Python 3.9+)
def first(lst: list[int]) -> int: return lst[0]
def keys(d: dict[str, int]) -> list[str]: return list(d.keys())

# Callable
def apply(fn: Callable[[int], int], x: int) -> int:
    return fn(x)

# TypeVar (stary styl, < 3.12)
from typing import TypeVar
T = TypeVar("T")
def identity(x: T) -> T: return x

# Generyczna funkcja – nowy styl Python 3.12+  (bez TypeVar)
def identity[T](x: T) -> T: return x

# Generyczna klasa – Python 3.12+
class Stack[T]:
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()

    def peek(self) -> T:
        return self._items[-1]

# użycie – T jest inferred lub podany jawnie
s = Stack[int]()   # typ jawny
s.push(1)
s.push(2)
s.pop()   # → 2

s2 = Stack()       # T inferred z pierwszego .push()
s2.push("hello")
```

---

## 21. Itertools – przydatne funkcje

```python
import itertools as it

# Łączy wiele iterables w jeden ciąg
list(it.chain([1,2],[3,4]))            # [1,2,3,4]

# Działa jak chain, ale przyjmuje jeden iterable (np. listę list) - "spłaszcza" strukturę
list(it.chain.from_iterable([[1,2],[3]])) # [1,2,3]

# Zwraca wycinek (slice) z iteratora (tu: 5 pierwszych elementów)
list(it.islice(range(100), 5))         # [0,1,2,3,4]

# Iloczyn kartezjański podanych iterables (każdy z każdym)
list(it.product([1,2],["a","b"]))      # [(1,'a'),(1,'b'),(2,'a'),(2,'b')]

# Permutacje o długości r (kolejność elementów ma znaczenie)
list(it.permutations([1,2,3], 2))      # [(1,2),(1,3),(2,1),...]

# Kombinacje o długości r (kolejność elementów nie ma znaczenia)
list(it.combinations([1,2,3], 2))      # [(1,2),(1,3),(2,3)]

# Skumulowane wyniki funkcji (domyślnie sumuje) dla kolejnych elementów
list(it.accumulate([1,2,3,4]))         # [1,3,6,10]

# Powtarza podany element wskazaną liczbę razy
list(it.repeat(0, 3))                  # [0,0,0]

# Pobiera elementy dopóki funkcja zwraca True, przerywa iterację przy pierwszym False
list(it.takewhile(lambda x: x<3, [1,2,3,4]))  # [1,2]

# Odrzuca elementy dopóki funkcja zwraca True, potem zwraca całą resztę (nawet jeśli False)
list(it.dropwhile(lambda x: x<3, [1,2,3,4]))  # [3,4]

# Podobnie jak zip(), ale wyrównuje do najdłuższego iterable (uzupełnia wartością fillvalue)
list(it.zip_longest([1,2],[3], fillvalue=0))   # [(1,3),(2,0)]
```

---

## 22. functools

```python
from functools import reduce, partial, lru_cache, cache

# reduce
reduce(lambda acc, x: acc + x, [1,2,3,4])  # 10

# partial – zamrożenie argumentów
def power(base, exp): return base ** exp
square = partial(power, exp=2)
square(5)   # 25

# lru_cache – memoizacja (zapamiętuje wyniki funkcji dla danych argumentów).
# maxsize ogranicza liczbę zapamiętanych wyników (usuwa najdawniej używane - LRU).
@lru_cache(maxsize=128)
def fib(n):
    if n < 2: return n
    return fib(n-1) + fib(n-2)

fib.cache_info()   # CacheInfo(hits=..., misses=..., ...)

# cache (Python 3.9+) – uproszczona wersja lru_cache bez limitu zapamiętanych wyników (unbounded).
# Używaj ostrożnie, jeśli liczba unikalnych wywołań może wyczerpać dostępną pamięć RAM.
@cache
def fib2(n): ...
```

---

## 23. Złożoność (Big O) – kluczowe struktury

| Operacja              | list       | dict / set | deque  |
|-----------------------|------------|------------|--------|
| Access by index       | O(1)       | –          | O(n)   |
| Search (in)           | O(n)       | O(1) avg   | O(n)   |
| Insert na końcu       | O(1)       | O(1) avg   | O(1)   |
| Insert na początku    | O(n)       | –          | O(1)   |
| Delete by value       | O(n)       | O(1) avg   | O(n)   |
| Sort                  | O(n log n) | –          | –      |

---

## 24. Przydatne built-ins

```python
abs(-5)           # 5
round(3.14159, 2) # 3.14
min([3,1,2])      # 1
max([3,1,2])      # 3
sum([1,2,3])      # 6
all([True,True])  # True
any([False,True]) # True
len("hello")      # 5

# konwersje
int("42")         # 42
float("3.14")     # 3.14
str(42)           # '42'
bool(0)           # False
list(range(5))    # [0,1,2,3,4]
tuple([1,2,3])    # (1,2,3)
set([1,1,2])      # {1,2}

# inne
ord("A")          # 65
chr(65)           # 'A'
bin(10)           # '0b1010'
hex(255)          # '0xff'
id(obj)           # adres w pamięci
type(obj)         # typ
isinstance(1, int)# True
vars(obj)         # __dict__ obiektu
dir(obj)          # lista atrybutów/metod
```

---

## 25. Kopiowanie – shallow vs deep

```python
import copy

lst = [[1,2],[3,4]]

# przypisanie – ten sam obiekt
a = lst              # a is lst → True

# shallow copy – nowy kontener, te same referencje wewnątrz
b = lst.copy()       # lub lst[:]  lub list(lst)
b = copy.copy(lst)

# deep copy – rekurencyjnie kopiuje wszystko
c = copy.deepcopy(lst)

lst[0].append(99)
# b[0] → [1,2,99]  (shallow – te same wewnętrzne listy!)
# c[0] → [1,2]     (deep – niezależna kopia)
```

---

## 26. Testowanie – pytest

```bash
pip install pytest pytest-cov
pytest                  # uruchamia wszystkie testy
pytest -v               # verbose
pytest -k "login"       # tylko testy zawierające "login" w nazwie
pytest -x               # zatrzymaj po pierwszym błędzie
pytest --cov=src        # pokrycie kodu
```

```python
# test_math.py  –  plik musi zaczynać się od test_

def add(a, b): return a + b

# --- podstawowy test ---
def test_add():
    assert add(2, 3) == 5

# --- oczekiwany wyjątek ---
import pytest

def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        1 / 0

def test_raises_with_message():
    with pytest.raises(ValueError, match="invalid"):
        raise ValueError("invalid input")

# --- parametrize – wiele przypadków w jednym teście ---
@pytest.mark.parametrize("a, b, expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 1, 0),
])
def test_add_param(a, b, expected):
    assert add(a, b) == expected

# --- fixture – wspólne dane / zasoby ---
@pytest.fixture
def sample_list():
    return [1, 2, 3]

def test_length(sample_list):
    assert len(sample_list) == 3

# fixture z setup i teardown
@pytest.fixture
def db_connection():
    conn = {"connected": True}   # setup
    yield conn
    conn["connected"] = False    # teardown (po teście)

# fixture o szerszym scope (raz na moduł/sesję)
@pytest.fixture(scope="module")
def heavy_resource():
    return {"data": list(range(1000))}

# --- marks ---
@pytest.mark.skip(reason="not implemented yet")
def test_pending(): ...

@pytest.mark.skipif(condition=True, reason="skipped on CI")
def test_ci(): ...

@pytest.mark.xfail(reason="known bug")
def test_known_bug():
    assert 1 == 2
```

> Konwencja: pliki `test_*.py` lub `*_test.py`, funkcje/klasy/metody z prefiksem `test_` / `Test`.

---

## 27. Mockowanie – `unittest.mock` + `pytest-mock`

```bash
pip install pytest-mock   # dostarcza fixture `mocker`
```

```python
from unittest.mock import MagicMock, patch, call

# --- MagicMock – podstawowy mock ---
mock = MagicMock()
mock.method(1, 2)
mock.method.assert_called_once_with(1, 2)
mock.method.call_count          # 1
mock.method.return_value = 42   # ustawianie wartości zwracanej

# --- patch – zamiana obiektu na czas testu ---
# jako dekorator
from unittest.mock import patch

@patch("mymodule.requests.get")
def test_api(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"ok": True}
    # ... wywołaj kod który używa requests.get

# jako context manager
def test_open():
    with patch("builtins.open", MagicMock(return_value=...)):
        pass

# --- pytest-mock (mocker fixture) – czystszy styl ---
def test_service(mocker):
    mock_db = mocker.patch("myapp.db.get_user")
    mock_db.return_value = {"id": 1, "name": "Alice"}

    result = get_user_name(1)
    assert result == "Alice"
    mock_db.assert_called_once_with(1)

# --- side_effect – wyjątek lub sekwencja ---
mock = MagicMock()
mock.side_effect = ValueError("boom")       # rzuca wyjątek
mock.side_effect = [1, 2, 3]               # kolejne wywołania zwracają kolejne wartości
mock.side_effect = lambda x: x * 2         # własna funkcja

# --- spy – prawdziwy obiekt + śledzenie wywołań ---
def test_spy(mocker):
    spy = mocker.spy(SomeClass, "some_method")
    obj = SomeClass()
    obj.some_method(42)
    spy.assert_called_once_with(obj, 42)

# --- assert helpers ---
mock.assert_called()                        # wywołany co najmniej raz
mock.assert_called_once()                   # dokładnie raz
mock.assert_called_with(1, key="val")       # ostatnie wywołanie
mock.assert_any_call(1)                     # którekolwiek wywołanie
mock.assert_not_called()
mock.call_args                              # ostatnie argumenty
mock.call_args_list                         # lista wszystkich wywołań
```

> Zasada: mockuj **na poziomie modułu który importuje**, nie tam gdzie jest zdefiniowane.
> `patch("myapp.service.requests.get")` → nie `patch("requests.get")`.

---

## 28. GIL (Global Interpreter Lock)

- **Czym jest GIL?** W CPythonie (standardowej implementacji Pythona) jest to mechanizm blokady (mutex), który pozwala tylko jednemu wątkowi na wykonywanie bajtkodu Pythona w danym momencie.
- **Konsekwencje:** Wielowątkowość **nie przyspieszy** programów silnie obciążających procesor (**CPU-bound**), ponieważ wątki nie mogą działać równolegle na wielu rdzeniach CPU.
- **Do czego używamy wątków?** Do zadań oczekujących na wejście/wyjście (**I/O-bound**), takich jak zapytania sieciowe, odczyt/zapis dysku, operacje na bazie danych. Podczas oczekiwania na I/O wątek zwalnia GIL, pozwalając innym wątkom na działanie.
- **Jak ominąć GIL (dla CPU-bound)?** Używając modułu `multiprocessing` (procesy mają własną pamięć i kopię interpretera) lub zewnętrznych bibliotek w C/C++ (np. NumPy), które potrafią zwalniać GIL podczas szybkich obliczeń na tablicach.

---

## 29. Moduł `threading` – tworzenie i uruchamianie wątków

```python
import threading
import time

def worker(name, delay):
    print(f"Wątek {name} startuje")
    time.sleep(delay)
    print(f"Wątek {name} kończy")

# 1. Tworzenie instancji wątków
t1 = threading.Thread(target=worker, args=("A", 2))
t2 = threading.Thread(target=worker, args=("B", 1))

# 2. Uruchomienie (wątki startują i kontynuują asynchronicznie)
t1.start()
t2.start()

# 3. Oczekiwanie na zakończenie (blokuje główny program dopóki wątki żyją)
t1.join()
t2.join()

# Wątki w tle (Daemon threads) - giną automatycznie wraz z głównym programem
# t_daemon = threading.Thread(target=worker, args=("Daemon", 5), daemon=True)
# t_daemon.start()
```

---

## 30. Synchronizacja wątków i Race Conditions

Dostęp do współdzielonych zmiennych globalnych/w pamięci w środowisku wielowątkowym może skutkować błędami, gdy dwa wątki modyfikują ten sam zasób jednocześnie (**Race Condition**). Wykorzystuje się mechanizmy synchronizacji tj. `Lock`.

```python
import threading

counter = 0
lock = threading.Lock()

def increment():
    global counter
    for _ in range(100000):
        # Ciekawostka: przez GIL samo dopisanie do listy (lst.append()) jest atomowe,
        # jednak operacje read-modify-write (x += 1) NIE SĄ atomowe.
        
        # Bez locka wątki mogłyby utracić inkrementacje:
        with lock:  # to samo co lock.acquire() i docelowo lock.release()
            counter += 1

threads = [threading.Thread(target=increment) for _ in range(5)]
for t in threads: t.start()
for t in threads: t.join()

print(counter) # Z Lockiem: zawsze równe 500000. Bez niego: rozbieżne wyniki.

# Inne przydatne mechanizmy synchronizacji (z threading):
# RLock (Reentrant Lock) - wątek może ponownie nałożyć ten sam zamek bez zakleszczenia
# Semaphore - dopuszcza ustaloną maksymalną liczbę wątków naraz
# Event - prosta flaga do powiadamiania między wątkami (wait, set, clear)
```

---

## 31. `concurrent.futures` – Pule Wątków (ThreadPoolExecutor)

O wiele nowocześniejszy, bezpieczniejszy i najbardziej zalecany interfejs dla uruchamiania zadań asynchronicznie, ograniczający "ręczne" pisanie pętli `.start()` i `.join()`.

```python
import concurrent.futures
import time

def task(n):
    time.sleep(0.5)
    return n * 10

# ThreadPoolExecutor dla zadań wejścia-wyjścia (I/O)
# Dla CPU-heavy -> zmiana słowa na ProcessPoolExecutor
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    
    numbers = [1, 2, 3, 4, 5]
    
    # --- Podejście 1: executor.map ---
    # Zwraca iterator, pod którym kryją się wyniki W TAKIEJ KOLEJNOŚCI w jakiej wysłaliśmy argumenty.
    # Wątki robią robotę asynchronicznie i czekamy.
    results = executor.map(task, numbers)
    print(list(results))  # [10, 20, 30, 40, 50]
    

    # --- Podejście 2: executor.submit (bardziej granulowane) ---
    # Zwraca obiekty typu Future, które reprezentują wykonanie funkcji w przyszłości.
    futures = [executor.submit(task, num) for num in numbers]
    
    # as_completed zwraca iterator podającym Futures w miarę, GDY SĄ gotowe 
    # (nie zachowuje kolejności argumentów, oddaje "kto pierwszy ten lepszy")
    for future in concurrent.futures.as_completed(futures):
        try:
            result = future.result()  # metoda blokująca, czeka do zwrotu lub odczytuje natychmiast
            print(f"Wynik z thread poola: {result}")
        except Exception as exc:
            print(f"Zadanie się wyrzuciło błędem: {exc}")
```

---

## 32. `asyncio` – Programowanie asynchroniczne (Single-thread I/O)

`asyncio` pozwala na wykonywanie asynchronicznego kodu (w obrębie **jednego wątku**) przy pomocy pętli zdarzeń (Event Loop). Jest to potężne rozwiązanie dla zadań mocno uzależnionych od wejścia/wyjścia (I/O-bound), takich jak tysiące jednoczesnych połączeń sieciowych, gdzie narzut pamięciowy i tzw. *context switching* dla tradycyjnych wątków systemu operacyjnego byłby zbyt duży.

- Współprogramy (**Coroutines**) definiuje się za pomocą `async def`.
- Samo wywołanie takiej funkcji nic nie oblicza – zwraca niedziałający obiekt coroutine. Aby go uruchomić i poczekać na wynik, potrzebujemy `await` (lub `asyncio.run()`).
- Operator `await` **zwraca sterowanie do Event Loop**, co pozwala innym zadaniom w tym samym wątku na wykonanie w czasie, gdy to konkretne (np. pobieranie SQL) czeka na zwrot z dysku lub sieci.

```python
import asyncio
import time

async def fetch_data(task_id, delay):
    print(f"Zadanie {task_id}: Rozpoczynam (czekam {delay}s)...")
    
    # asyncio.sleep reprezentuje asynchroniczną operację wejścia/wyjścia.
    # Użycie `time.sleep(delay)` całkowicie zablokowałoby całą pętlę!
    await asyncio.sleep(delay)
    
    print(f"Zadanie {task_id}: Zakończono!")
    return {"id": task_id, "data": "sukces"}

async def main():
    start = time.time()
    
    # Uruchamiamy współprogramy. asyncio.gather() przyjmuje wiele coroutines,
    # rejestruje je do wykonania w Event Loop i zwraca wyniki w liście,
    # gdy wszystkie się zakończą.
    results = await asyncio.gather(
        fetch_data(1, 2),
        fetch_data(2, 1),
        fetch_data(3, 3)
    )
    
    # Pomimo 3 zadań trwających 2s, 1s, i 3s – całkowity czas działania
    # to około 3 sekundy (wynika z najdłuższego sleepa), nie 6 sekund.
    print(f"\nWyniki: {results}")
    print(f"Całkowity czas: {time.time() - start:.2f}s")


# Rozpoczyna całkowicie od zera Event Loop, wykonuje główną funkcję i zamyka pętlę.
if __name__ == "__main__":
    asyncio.run(main())
```

> **Podsumowując – Kiedy używać czego?**
>
> - **Silne obciążenie procesora (np. AI, obróbka wideo):** `multiprocessing` / `ProcessPoolExecutor` (aby uciec z GIL na inne rdzenie).
> - **Operacje I/O z użyciem starych/blokujących bibliotek (np. `requests`):** `threading` / `ThreadPoolExecutor`.
> - **Operacje I/O asynchroniczne na ogromną skalę (np. WebSockets, chat w locie, `aiohttp`):** `asyncio`.

---

## 33. Pydantic V2

Pydantic V2 to popularna biblioteka do walidacji danych i zarządzania ustawieniami prosto z adnotacji typów (type hints). W wersji 2 logika rdzeniowa została przepisana w j. Rust, drastycznie podnosząc wydajność. V2 silnie promuje użycie `typing.Annotated` do definiowania walidacji.

```python
from typing import Optional, Annotated
from pydantic import BaseModel, Field, EmailStr, field_validator, model_validator

class User(BaseModel):
    id: int
    # V2: Rekomendowane użycie Annotated do ograniczeń (zamiast = Field(...))
    name: Annotated[str, Field(min_length=2, max_length=50)]
    email: EmailStr  # wymaga zainstalowania dodatku: pip install "pydantic[email]"
    age: Optional[int] = None
    
    # V2: Niestandardowy walidator konkretnego pola
    @field_validator('age')
    @classmethod
    def check_age(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and v < 18:
            raise ValueError('Age must be at least 18')
        return v

    # V2: Walidator całego modelu (np. zależności między polami)
    @model_validator(mode='after')
    def check_email_contains_name(self) -> 'User':
        if self.name.lower() not in self.email.lower():
            raise ValueError('Email must contain user name')
        return self

# 1. Tworzenie obiektu
user = User(id=1, name="Alice", email="alice@example.com", age=25)

# 2. Eksportowanie danych (V2: używamy metod z prefixem model_ )
print(user.model_dump())          # Zwraca dict
print(user.model_dump_json())     # Zwraca string JSON z danymi

# 3. Walidacja z podanych danych na wejściu (V2: metody model_validate_ )
# Z wczytanego słownika:
user_dict = {"id": 2, "name": "Bob", "email": "bob@example.com", "age": 30}
user2 = User.model_validate(user_dict)

# Ze stringa JSON:
user_json = '{"id": 3, "name": "Charlie", "email": "charlie.brown@example.com"}'
user3 = User.model_validate_json(user_json)

# 4. Generowanie JSON Schema modelu (V2: model_json_schema)
schema = User.model_json_schema()
```
