# Wyjaśnienie defaultdict w Pythonie

**Data:** 2025-12-03

---

**User:**

Na przykładach wyjaśnij defaultdict w Python

---

**Assistant:**

`defaultdict` pochodzi z modułu `collections` i działa jak zwykły słownik, ale jeśli odwołasz się do nieistniejącego klucza, automatycznie tworzy dla niego wartość domyślną. Dzięki temu nie trzeba sprawdzać, czy klucz istnieje.

---

## Podstawowy przykład

```python
from collections import defaultdict

d = defaultdict(int)  # int() zwraca 0
d['a'] += 1
d['b'] += 5

print(d)   # defaultdict(<class 'int'>, {'a': 1, 'b': 5})
print(d['c'])  # 0 – klucz nie istniał, został utworzony z wartością 0
```

Tutaj `defaultdict(int)` tworzy nowe klucze z wartością `0`.

---

## Jako lista wartości pod jednym kluczem

Częsty przypadek: grupowanie elementów.

```python
from collections import defaultdict

grouped = defaultdict(list)

items = [('A', 1), ('A', 2), ('B', 3)]

for key, value in items:
    grouped[key].append(value)

print(grouped)  
# defaultdict(<class 'list'>, {'A': [1, 2], 'B': [3]})
```

Bez `defaultdict` musiałbyś sprawdzać, czy lista istnieje.

---

## Tworzenie zagnieżdżonych struktur

Możesz zdefiniować zagnieżdżone słowniki bez pilnowania kluczy:

```python
from collections import defaultdict

nested = defaultdict(lambda: defaultdict(int))

nested['users']['count'] += 1
nested['users']['active'] += 2

print(nested)
# defaultdict(<lambda>, {'users': defaultdict(<class 'int'>, {'count': 1, 'active': 2})})
```

---

## Porównanie ze zwykłym dict

Zwykły `dict`:

```python
d = {}
d['x'] += 1   # błąd: KeyError
```

`defaultdict`:

```python
from collections import defaultdict
d = defaultdict(int)
d['x'] += 1   # działa, bo tworzy x = 0, a potem zwiększa do 1
```

---

Jeśli chcesz, mogę pokazać jeszcze przykłady z użyciem `set`, z liczeniem częstotliwości albo bardziej praktyczne zastosowania.