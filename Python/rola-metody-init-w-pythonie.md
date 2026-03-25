# Rola metody __init__ w Pythonie

**Data:** 2025-04-27

---

**User:**

Po co w Python w kodzie klasy umieszcza się metodę __init__(self), czy jest to konstruktor?

---

**Assistant:**

Tak! W Pythonie metoda `__init__(self, ...)` **pełni rolę konstruktora**.

Kiedy tworzysz nową instancję klasy, np. `obj = MyClass()`, Python:
1. **Tworzy** pusty obiekt (to robi technicznie metoda `__new__`, o której rzadko trzeba myśleć),
2. **Następnie wywołuje** metodę `__init__(self, ...)`, przekazując nowo utworzony obiekt jako `self`.

`__init__` służy więc do **inicjalizacji** tego obiektu — możesz tam ustawiać wartości pól, wykonywać jakieś przygotowawcze operacje itd.

Przykład:

```python
class Person:
    def __init__(self, name, age):
        self.name = name  # ustawiamy atrybuty obiektu
        self.age = age

p = Person("Alice", 30)
print(p.name)  # wypisze "Alice"
```

Czy chcesz, żebym też pokazał, czym się różni `__init__` od `__new__` albo jak wygląda konstruktor w innych językach (np. w Javie) porównując to z Pythonem? 🚀