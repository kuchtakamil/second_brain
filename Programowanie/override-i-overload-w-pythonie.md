# Override i Overload w Pythonie

**Data:** 2025-07-15

---

**User:**

Z Javy znam dobrze pojęcia Override oraz Overload w odniesieniu do metod w OOP. Jak wygląda to w Python? Podaj przykłady.

---

**Assistant:**

W Pythonie pojęcia **override** (nadpisywanie metod) i **overload** (przeciążanie metod) również istnieją, ale działają inaczej niż w Javie.

---

## 🔁 Override (nadpisywanie metod)

Działa podobnie jak w Javie. Jeśli klasa potomna zdefiniuje metodę o tej samej nazwie co w klasie bazowej, to nadpisuje ją.

### Przykład:
```python
class Animal:
    def speak(self):
        return "Some sound"

class Dog(Animal):
    def speak(self):  # override
        return "Woof!"

a = Animal()
d = Dog()

print(a.speak())  # Some sound
print(d.speak())  # Woof!
```

> Nie trzeba używać żadnego dekoratora jak `@Override` w Javie — Python opiera się na dynamicznym typowaniu i konwencji.

---

## ➕ Overload (przeciążanie metod)

Python **nie wspiera przeciążania metod w taki sposób jak Java** – nie można mieć kilku metod o tej samej nazwie, ale różnych sygnaturach. Ostatnia definicja metody nadpisze poprzednią.

### Błędny sposób (nie działa jak w Javie):
```python
class Example:
    def greet(self):
        print("Hello")

    def greet(self, name):  # nadpisuje poprzednią metodę
        print(f"Hello, {name}")

e = Example()
e.greet("John")    # OK
e.greet()          # TypeError: greet() missing 1 required positional argument
```

### Poprawne podejście — argumenty domyślne lub `*args` / `**kwargs`:
```python
class Example:
    def greet(self, name=None):
        if name:
            print(f"Hello, {name}")
        else:
            print("Hello")

e = Example()
e.greet()          # Hello
e.greet("John")    # Hello, John
```

---

## 🧠 `functools.singledispatch` — alternatywa dla overload

Python 3.4+ wprowadza `@singledispatch`, który pozwala na przeciążanie funkcji na podstawie typu **pierwszego argumentu**.

```python
from functools import singledispatch

@singledispatch
def process(arg):
    print("Default processing", arg)

@process.register(int)
def _(arg):
    print("Processing an int:", arg)

@process.register(str)
def _(arg):
    print("Processing a string:", arg)

process(10)        # Processing an int: 10
process("hello")   # Processing a string: hello
process([1, 2, 3]) # Default processing [1, 2, 3]
```

---

## Podsumowanie:

| Pojęcie      | Java                            | Python                              |
|--------------|----------------------------------|--------------------------------------|
| Override     | `@Override` + ta sama sygnatura | po prostu metoda o tej samej nazwie |
| Overload     | różne sygnatury metod           | nie wspierane bezpośrednio; używaj domyślnych argumentów, `*args`, `@singledispatch` |

Jeśli chcesz, mogę też pokazać przykład `@singledispatchmethod` dla metod klasowych (Python 3.8+).