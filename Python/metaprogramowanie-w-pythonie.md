# Metaprogramowanie w Pythonie

**Data:** 2025-05-02

---

**User:**

Opisz Metaprogramowanie w Python:
getattr, setattr, hasattr, __getattr__, __setattribute__.
Tworzenie klas dynamicznie (type, metaclasses).

---

**Assistant:**

Metaprogramowanie w Pythonie oznacza pisanie kodu, który **manipuluje kodem** – czyli dynamicznie tworzy klasy, modyfikuje obiekty, przechwytuje dostęp do atrybutów, itp. Python, jako język dynamiczny, ma wbudowane potężne narzędzia do tego typu operacji. Oto najważniejsze z nich:

---

## 🔧 Funkcje: `getattr`, `setattr`, `hasattr`

Służą do **dynamicznej manipulacji atrybutami obiektów**:

- `getattr(obj, name[, default])`: pobiera wartość atrybutu `name` z obiektu `obj`.
  ```python
  class User:
      name = "Anna"

  u = User()
  print(getattr(u, "name"))  # => "Anna"
  ```
- `setattr(obj, name, value)`: ustawia wartość atrybutu `name` na `value`.
  ```python
  setattr(u, "age", 30)
  print(u.age)  # => 30
  ```
- `hasattr(obj, name)`: sprawdza, czy obiekt `obj` ma atrybut `name`.
  ```python
  hasattr(u, "name")  # => True
  ```

---

## 🧩 Metody specjalne: `__getattr__`, `__setattr__`, `__getattribute__`

Te metody pozwalają **przechwytywać dostęp do atrybutów** i modyfikować jego zachowanie.

- `__getattr__(self, name)`: wywoływana **tylko jeśli atrybut nie istnieje**.
  ```python
  class Demo:
      def __getattr__(self, name):
          return f"{name} is not defined"

  d = Demo()
  print(d.foo)  # => "foo is not defined"
  ```

- `__setattr__(self, name, value)`: wywoływana przy każdej próbie ustawienia atrybutu.
  ```python
  class Demo:
      def __setattr__(self, name, value):
          print(f"Setting {name} = {value}")
          self.__dict__[name] = value
  ```

- `__getattribute__(self, name)`: wywoływana **zawsze przy próbie odczytu atrybutu**, nawet jeśli istnieje.
  > ⚠️ Należy uważać na nieskończoną rekurencję – trzeba używać `super().__getattribute__`.
  ```python
  class Demo:
      def __getattribute__(self, name):
          print(f"Accessing {name}")
          return super().__getattribute__(name)
  ```

---

## 🏗️ Dynamiczne tworzenie klas: `type`

W Pythonie `type` to nie tylko funkcja zwracająca typ – to **metaklasa**, która pozwala tworzyć klasy dynamicznie:

```python
MyClass = type("MyClass", (object,), {"x": 42, "hello": lambda self: "Hi!"})

obj = MyClass()
print(obj.x)          # => 42
print(obj.hello())    # => "Hi!"
```

Składnia:  
`type(class_name, bases, dict_of_attributes)`

---

## 🧬 Metaklasy

Metaklasy to **"klasy dla klas"** – definiują, **jak powstają klasy**. Domyślną metaklasą jest `type`.

Przykład:

```python
class Meta(type):
    def __new__(cls, name, bases, dct):
        print(f"Creating class {name}")
        dct["added_method"] = lambda self: "I'm added by metaclass"
        return super().__new__(cls, name, bases, dct)

class MyClass(metaclass=Meta):
    pass

obj = MyClass()
print(obj.added_method())  # => "I'm added by metaclass"
```

Metaklasy najczęściej używa się do:
- walidacji klas podczas ich tworzenia,
- automatycznego dodawania metod,
- rejestrowania klas (np. pluginy).

---

## 🔚 Podsumowanie

| Narzędzie            | Cel                                      |
|----------------------|-------------------------------------------|
| `getattr/setattr`    | Dynamiczny dostęp / modyfikacja atrybutów |
| `__getattr__`        | Niestandardowa obsługa brakujących pól    |
| `__setattr__`        | Przechwycenie przypisywania               |
| `__getattribute__`   | Przechwycenie każdego odczytu             |
| `type()`             | Dynamiczne tworzenie klasy                |
| Metaklasy            | Kontrola procesu tworzenia klas           |

Chcesz, żebym pokazał przykład użycia tych technik w praktycznym kodzie (np. rejestrator klas lub obiekt proxy)?