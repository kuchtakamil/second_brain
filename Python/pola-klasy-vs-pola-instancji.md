# Pola klasy vs Pola instancji (obiektu) w Pythonie

Często w Pythonie można spotkać różne sposoby definiowania "pól" w klasie. Aby to zrozumieć, musimy podzielić to na trzy główne kategorie: zmienne instancji (obiektu), zmienne klasy (odpowiednik `static` w Javie) oraz adnotacje typów (często używane z `@dataclass` lub Pydantic).

## 1. Pola instancji (dotyczące konkretnego obiektu)

Zdecydowana większość zmiennych, z którymi pracujesz w klasach, to **pola instancji**. Każdy nowo utworzony obiekt (instancja klasy) ma swoją **własną, niezależną kopię** tych pól.

Zgodnie z regułami Pythona, pola instancji powinny być definiowane i inicjalizowane wewnątrz metody specjalnej `__init__` przy użyciu odniesienia do samego siebie, czyli `self`.

```python
class User:
    def __init__(self, name: str, age: int):
        self.name = name  # Pole instancji (tylko dla tego obiektu)
        self.age = age    # Pole instancji (tylko dla tego obiektu)

user1 = User("Jan", 30)
user2 = User("Anna", 25)

# Zmiana u jednego użytkownika nie wpływa na drugiego
user1.name = "Adam"
print(user1.name)  # Adam
print(user2.name)  # Anna
```

**Kiedy używać:** Jeśli chcesz, aby pole należało do konkretnego obiektu i żeby każdy obiekt mógł mieć inną jego wartość.

## 2. Pola klasy (odpowiednik `static` z Javy)

Pola klasy to zmienne definiowane **bezpośrednio w ciele klasy**, poza jakimikolwiek metodami (i bez użycia słowa `self`). Istnieje tylko **jedna kopia** takiego pola, która jest **współdzielona** przez wszystkie obiekty danej klasy. Zachowują się więc identycznie jak pola ze słowem kluczowym `static` w Javie.

```python
class Car:
    wheels = 4  # Pole klasy (współdzielone między wszystkimi samochodami)

    def __init__(self, brand: str):
        self.brand = brand  # Pole instancji

car1 = Car("Toyota")
car2 = Car("Ford")

print(car1.wheels)  # 4
print(car2.wheels)  # 4

# Zmiana pola na poziomie klasy zmienia je dla WSZYSTKICH istniejących obiektów
Car.wheels = 5
print(car1.wheels)  # 5
print(car2.wheels)  # 5
```

**Kiedy używać:** Używaj pól klasy dla stałych (np. konfiguracji) lub wartości, które definitywnie są wspólne dla wszystkich instancji tej klasy. Dobrą praktyką jest odwoływanie się do nich poprzez nazwę klasy (np. `Car.wheels`).

## 3. Adnotacje typów w ciele klasy (tylko typ, bez przypisania wartości)

Zastanawiasz się zapewne skąd bierze się zapis, który widujesz:

```python
class User:
    name: str
    surname: str
    age: int
```

Taki zapis to nic innego jak **adnotacje typów (Type Hints)**. Zostały one wprowadzone w Pythonie w PEP 526, aby poprawić czytelność kodu i ułatwić pracę narzędziom (jak IDE czy MyPy).

Co najważniejsze: **sam z siebie ten kod NIE tworzy pól klasy, ani nie tworzy pól instancji**. Zmienne zapisane w ten sposób w ogóle nie otrzymują żadnej wartości w pamięci podczas działania programu (ich definicje trafiają jedynie do specjalnego słownika `__annotations__` na poziomie klasy).

**Dlaczego więc ten zapis jest tak popularny?**

Ponieważ w nowoczesnym Pythonie inne biblioteki wykorzystują te adnotacje, aby **automatycznie generować kod** za programistę (w tym metody `__init__`).

W 99% przypadków widząc taki zapis, w kodzie będzie użyta zewnętrzna biblioteka lub dekorator. Najpopularniejsze to:

### A. Dekorator `@dataclass` (biblioteka standardowa Pythona)
```python
from dataclasses import dataclass

@dataclass
class User:
    name: str
    surname: str
    age: int

# Dekorator pod spodem czyta te gołe typy i sam potajemnie tworzy metodę:
# def __init__(self, name: str, surname: str, age: int):
#     self.name = name
#     ...

user = User("Jan", "Kowalski", 30) # To działa dzięki wygenerowanemu __init__
```

### B. Biblioteka Pydantic (np. w FastAPI)
Używa identycznej składni w klasach dziedziczących po `BaseModel`. Dzięki temu tworzy odpowiedni konstruktor i automatycznie pilnuje walidacji typów w runtime:
```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int
```

## Podsumowanie - jak z tego korzystać?

1. **Standardowe klasy:** Jeżeli samodzielnie piszesz tradycyjną klasę (bez `@dataclass`), zmienne obiektu (instancji) deklarujesz **zawsze** w funkcji `__init__`.
2. **Odpowiednik `static`:** Jeżeli zależy Ci na tym, by wartość była jedna i stała dla wszystkich instancji, piszesz np. `ZMIENNA = wartość` prosto w ciele klasy.
3. **Konstrukcje "magiczne" (Dataclasses / Pydantic):** Jeżeli widzisz klasę złożoną z samego wylistowania pól z dwukropkami bez przypisania do nich wartości (`name: str`), oznacza to, że używany jest mechanizm (np. `@dataclass`), który te wpisy odczyta i potraktuje jako szablon do wygenerowania za Ciebie odpowiedniej metody `__init__` i finalnie przypisze te pola jako **zwykłe pola instancji**.
