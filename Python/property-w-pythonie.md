# @Property w Pythonie

**Data:** 2026-02-15

---

**User:**

w python widuję @property. Co to jest i po co?

---

**Assistant:**

`@property` w Pythonie to **dekorator**, który pozwala zdefiniować metodę tak, aby była używana jak atrybut (pole) obiektu — bez wywołania z nawiasami.

Innymi słowy: wywołujesz metodę jak zmienną, ale pod spodem wykonuje się logika.

---

## 🔹 Problem, który rozwiązuje

Załóżmy klasę:

```python
class User:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    def full_name(self):
        return f"{self.first_name} {self.last_name}"
```

Użycie:

```python
u = User("Jan", "Kowalski")
print(u.full_name())  # trzeba wywołać metodę
```

Ale koncepcyjnie `full_name` to **właściwość obiektu**, a nie akcja. Semantycznie chcielibyśmy:

```python
print(u.full_name)
```

I tu wchodzi `@property`.

---

## 🔹 Jak działa `@property`

```python
class User:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
```

Teraz:

```python
u = User("Jan", "Kowalski")
print(u.full_name)  # działa bez ()
```

Metoda została opakowana w descriptor (`property`), który przechwytuje dostęp do atrybutu.

---

## 🔹 Getter, Setter, Deleter

`@property` to tylko getter. Możesz też zdefiniować setter:

```python
class User:
    def __init__(self, first_name, last_name):
        self._first_name = first_name
        self._last_name = last_name

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        if not value:
            raise ValueError("First name cannot be empty")
        self._first_name = value
```

Użycie:

```python
u.first_name = "Adam"  # wywoła setter
```

Pod spodem nie przypisujesz bezpośrednio do pola — wykonuje się kontrolowana logika.

---

## 🔹 Dlaczego to jest ważne (praktycznie)

### 1️⃣ Enkapsulacja bez psucia API

Załóżmy, że pierwotnie miałeś:

```python
class Product:
    def __init__(self, price):
        self.price = price
```

A potem chcesz dodać walidację. Bez `@property` musiałbyś zmienić API (`set_price()`), łamiąc kompatybilność.

Z `@property` możesz przejść z pola na logikę bez zmiany sposobu użycia klasy.

To jest bardzo "clean" w sensie projektowym.

---

### 2️⃣ Obliczane właściwości

Typowy use case:

```python
@property
def total(self):
    return sum(item.price for item in self.items)
```

`total` nie jest przechowywane — liczy się dynamicznie.

---

### 3️⃣ Lazy evaluation / cache

Możesz kontrolować kosztowne obliczenia:

```python
@property
def config(self):
    if self._config is None:
        self._config = load_config()
    return self._config
```

W Pythonie 3.8+ masz też `functools.cached_property`.

---

## 🔹 Co się dzieje technicznie

`property` to klasa implementująca protokół descriptorów:

- `__get__`
- `__set__`
- `__delete__`

Czyli dostęp do `obj.attr` nie jest prostym odczytem z `__dict__`, tylko przechodzi przez descriptor.

To bardzo potężny mechanizm — używany też w ORM-ach (np. pola modelu w Django działają przez deskriptory).

---

## 🔹 Kiedy używać

Używaj `@property`, gdy:

- logicznie masz właściwość, nie akcję
- chcesz walidować dane
- chcesz zachować kompatybilność API
- chcesz obliczaną wartość bez zmiany składni użycia

Nie używaj, gdy:

- metoda robi ciężką operację (np. request HTTP) — wtedy brak nawiasów jest mylący
- semantycznie to akcja, a nie stan

---

## 🔹 Analogicznie do Javy

Jako że masz background w Javie:

Pythonowe:

```python
user.full_name
```

To odpowiednik:

```java
user.getFullName();
```

Tyle że w Pythonie możesz później zmienić implementację bez zmiany kontraktu.

---

Jeśli chcesz, mogę też pokazać:

- jak `@property` działa od strony bytecode
- jak napisać własny descriptor
- albo jak to wpływa na `dataclasses` i `pydantic` (co może być ciekawe przy Twoich eksperymentach z AI-asystentem).

---
