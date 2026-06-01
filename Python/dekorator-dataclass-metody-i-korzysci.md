# Dekorator `@dataclass` w Pythonie: Metody i Korzyści

Dekorator `@dataclass` (wprowadzony w Pythonie 3.7 w ramach PEP 557) to potężne narzędzie wbudowane w moduł standardowy `dataclasses`. Jego głównym zadaniem jest automatyczne generowanie metod specjalnych (tzw. *dunder methods*) dla klas, które służą głównie do przechowywania stanu (danych). Dzięki temu programista unika pisania powtarzalnego kodu (*boilerplate*).

Poniżej znajduje się szczegółowe kompendium omawiające, jakie metody są automatycznie implementowane pod maską dekoratora `@dataclass`, jak nimi sterować oraz dlaczego warto korzystać z dataclass w codziennej pracy.

---

## 1. Jakie metody są automatycznie generowane?

W zależności od konfiguracji dekoratora, `@dataclass` może wygenerować lub zmodyfikować zestaw metod specjalnych. Oto one:

### 1.1. `__init__(self, ...)`
Konstruktor klasy jest generowany automatycznie na podstawie zdefiniowanych adnotacji typów.
- Przyjmuje zadeklarowane pola jako argumenty (w kolejności ich definicji w klasie).
- Automatycznie przypisuje wartości do pól instancji (`self.pole = wartość`).
- Obsługuje domyślne wartości pól.

### 1.2. `__repr__(self)`
Generuje czytelną reprezentację tekstową obiektu.
- Zwraca ciąg znaków w formacie: `NazwaKlasy(pole1=wartość1, pole2=wartość2, ...)`.
- Jest niezwykle pomocna podczas debugowania i logowania zdarzeń.

### 1.3. `__eq__(self, other)`
Umożliwia porównywanie obiektów za pomocą operatora `==`.
- Porównuje dwa obiekty tej samej klasy jako krotki (tuple) ich wartości w kolejności zdefiniowanych pól.
- Zwraca `True` tylko wtedy, gdy wszystkie pola obu obiektów są równe.
- Jeśli porównywany obiekt jest innej klasy, zwraca `NotImplemented` (co zazwyczaj skutkuje `False`).

### 1.4. `__match_args__` (od Pythona 3.10)
To nie jest metoda, lecz atrybut klasy (krotka zawierająca nazwy pól w kolejności ich definicji).
- Umożliwia bezproblemowe używanie obiektów dataclass w dopasowywaniu wzorców (Structural Pattern Matching) za pomocą instrukcji `match ... case`.

### 1.5. Metody porównania: `__lt__`, `__le__`, `__gt__`, `__ge__` (opcjonalne)
Generowane tylko wtedy, gdy dekorator zostanie wywołany z parametrem `@dataclass(order=True)`.
- Pozwalają na porównywanie obiektów przy użyciu operatorów `<`, `<=`, `>`, `>=` oraz ich sortowanie (np. za pomocą `sorted()`).
- Porównanie odbywa się leksykograficznie – obiekty są traktowane jak krotki ich wartości. Najpierw porównywane jest pierwsze pole; jeśli są równe, drugie itd.

### 1.6. `__hash__(self)` (opcjonalne)
Zwraca unikalną wartość skrótu (hash) obiektu.
- Sposób generowania tej metody zależy od parametrów `frozen` oraz `unsafe_hash`:
  - **Domyślnie (`frozen=False`, `unsafe_hash=False`)**: `__hash__` jest ustawiane na `None`. Oznacza to, że obiekty są **niehaszowalne** (nie można ich dodać do zbioru `set` ani użyć jako klucza w słowniku `dict`). Jest to bezpieczne zachowanie, ponieważ modyfikacja obiektu zmieniłaby jego hash, co popsułoby strukturę słownika.
  - **Gdy `frozen=True`**: Klasa staje się niemodyfikowalna, a `@dataclass` automatycznie generuje bezpieczną metodę `__hash__` bazującą na wartościach wszystkich pól.
  - **Gdy `unsafe_hash=True`**: Wymusza generowanie metody `__hash__` mimo mutowalności obiektu (stosować z dużą ostrożnością!).

### 1.7. `__setattr__(self, name, value)` oraz `__delattr__(self, name)` (opcjonalne)
Generowane tylko wtedy, gdy dekorator zostanie wywołany z parametrem `@dataclass(frozen=True)`.
- Rzucają wyjątek `FrozenInstanceError` przy próbie przypisania nowej wartości do pola lub próbie usunięcia atrybutu. Gwarantuje to niemodyfikowalność obiektu po jego utworzeniu.

---

## 2. Parametry konfiguracyjne dekoratora `@dataclass`

Zachowaniem dekoratora sterujemy za pomocą parametrów przekazywanych podczas jego wywołania. Oto ich pełna lista wraz z domyślnymi wartościami:

| Parametr | Domyślnie | Opis |
| :--- | :--- | :--- |
| **`init`** | `True` | Generuje metodę `__init__`. Jeśli w klasie ręcznie zdefiniujesz `__init__`, ten parametr zostanie zignorowany. |
| **`repr`** | `True` | Generuje metodę `__repr__`. |
| **`eq`** | `True` | Generuje metodę `__eq__`. |
| **`order`** | `False` | Generuje metody porównania (`__lt__`, `__le__`, `__gt__`, `__ge__`). |
| **`unsafe_hash`**| `False` | Jeśli `True`, wymusza wygenerowanie metody `__hash__` (nawet dla klas mutowalnych). |
| **`frozen`** | `False` | Jeśli `True`, czyni obiekt niemodyfikowalnym i generuje bezpieczną metodę `__hash__`. |
| **`match_args`** | `True` | (Od Python 3.10) Generuje atrybut `__match_args__` na potrzeby Pattern Matchingu. |
| **`kw_only`** | `False` | (Od Python 3.10) Jeśli `True`, wszystkie pola klasy stają się polami wyłącznie nazwanymi (*keyword-only*). |
| **`slots`** | `False` | (Od Python 3.10) Tworzy klasę zoptymalizowaną pamięciowo za pomocą `__slots__` (brak dynamicznego słownika `__dict__`). |

---

## 3. Dlaczego warto używać `@dataclass`? (Korzyści i zaawansowane funkcje)

Poza automatycznym generowaniem metod specjalnych, `dataclass` oferuje szereg zaawansowanych mechanizmów, które sprawiają, że pisanie czystego kodu staje się znacznie łatwiejsze.

### 3.1. Eliminacja pułapki mutowalnych wartości domyślnych (*Mutable Default Arguments*)
W standardowych klasach Pythona przypisanie pustej listy jako domyślnego argumentu konstruktora prowadzi do współdzielenia tej samej listy przez wszystkie instancje. `dataclass` całkowicie eliminuje ten problem, zabraniając bezpośredniego przypisywania mutowalnych obiektów i zmuszając do użycia funkcji `field` z fabryką:

```python
from dataclasses import dataclass, field
from typing import List

@dataclass
class Group:
    name: str
    # Błąd: members: List[str] = [] (Python zgłosi ValueError w czasie parsowania!)
    members: List[str] = field(default_factory=list) # Poprawne i bezpieczne rozwiązanie
```

### 3.2. Metoda `__post_init__(self)`
Często po przypisaniu argumentów w konstruktorze zachodzi potrzeba zwalidowania danych lub wyliczenia dodatkowych pól pochodnych. Służy do tego metoda `__post_init__`, która jest automatycznie wywoływana na samym końcu wygenerowanej metody `__init__`.

```python
@dataclass
class Employee:
    first_name: str
    last_name: str
    salary: float
    email: str = field(init=False) # Pole wykluczone z konstruktora

    def __post_init__(self):
        # Walidacja
        if self.salary < 0:
            raise ValueError("Wynagrodzenie nie może być ujemne!")
        
        # Obliczenie pola pochodnego
        self.email = f"{self.first_name.lower()}.{self.last_name.lower()}@company.com"

emp = Employee("Kamil", "Kowalski", 5000)
print(emp.email)  # Output: kamil.kowalski@company.com
```

### 3.3. Łatwa konwersja i serializacja (`asdict` i `astuple`)
Moduł `dataclasses` dostarcza wbudowane funkcje pomocnicze, które pozwalają na rekurencyjną konwersję instancji na standardowe typy Pythona (słowniki i krotki):

```python
from dataclasses import asdict, astuple

@dataclass
class Point:
    x: int
    y: int

p = Point(5, 10)
print(asdict(p))   # Output: {'x': 5, 'y': 10} (idealne do serializacji do JSON)
print(astuple(p))  # Output: (5, 10)
```

### 3.4. Funkcja `replace` i praca z obiektami zamrożonymi (`frozen=True`)
Podczas programowania funkcyjnego bardzo często korzysta się z obiektów niemodyfikowalnych (immutable). Kiedy chcemy "zmodyfikować" taki obiekt, zamiast zmieniać jego stan, tworzymy jego nową kopię z podmienionymi niektórymi wartościami pól. W tym celu używamy funkcji `replace`:

```python
from dataclasses import dataclass, replace

@dataclass(frozen=True)
class Configuration:
    host: str
    port: int
    timeout: int

config1 = Configuration("localhost", 8080, 30)

# Tworzymy nowy obiekt z zmienionym portem, zachowując resztę wartości
config2 = replace(config1, port=9000)

print(config1) # Output: Configuration(host='localhost', port=8080, timeout=30)
print(config2) # Output: Configuration(host='localhost', port=9000, timeout=30)
```

### 3.5. Drastyczne ograniczenie zużycia pamięci za pomocą `slots=True` (od Pythona 3.10)
Domyślnie każda klasa w Pythonie posiada dynamiczny słownik `__dict__`, który przechowuje atrybuty instancji. Słownik ten zużywa sporo pamięci RAM. Użycie `slots=True` sprawia, że `@dataclass` optymalizuje strukturę wewnętrzną obiektu.
- Brak atrybutu `__dict__` sprawia, że instancje zużywają nawet **o 40-50% mniej pamięci RAM**.
- Dostęp do pól obiektu staje się minimalnie szybszy.
- Uniemożliwia dynamiczne dodawanie nowych atrybutów spoza definicji klasy (zabezpieczenie przed literówkami).

```python
@dataclass(slots=True)
class HeavyData:
    id: int
    payload: str
```

### 3.6. Pełne wsparcie dla typowania (Typing) i podpowiedzi w IDE
Dekorator `@dataclass` opiera się na adnotacjach typów. Dzięki temu nowoczesne edytory kodu (VS Code, PyCharm) oraz narzędzia do statycznej analizy kodu (mypy, pyright) mogą:
- Dostarczać doskonałe autouzupełnianie pól klasy podczas pisania kodu.
- Ostrzegać o niezgodności typów przekazywanych parametrów przed uruchomieniem kodu.
- Generować automatyczną dokumentację klasy.

---

## 4. Podsumowanie: Dataclass vs Zwykła klasa

Porównajmy bezpośrednio nakład pracy programisty w obu przypadkach:

### Zwykła Klasa (dużo pisania):
```python
class TraditionalUser:
    def __init__(self, username: str, email: str, age: int):
        self.username = username
        self.email = email
        self.age = age

    def __repr__(self):
        return f"TraditionalUser(username={self.username!r}, email={self.email!r}, age={self.age})"

    def __eq__(self, other):
        if not isinstance(other, TraditionalUser):
            return NotImplemented
        return (self.username, self.email, self.age) == (other.username, other.email, other.age)
```

### Odpowiednik z `@dataclass` (czysto, zwięźle i czytelnie):
```python
from dataclasses import dataclass

@dataclass
class ModernUser:
    username: str
    email: str
    age: int
```

Obie klasy zachowują się w programie niemal identycznie (mają ten sam konstruktor, reprezentację tekstową i porównanie logiczne), jednak wersja z `@dataclass` zajmuje zaledwie 5 linijek kodu zamiast 14. 

Korzystanie z dekoratora `@dataclass` to standard we współczesnym, profesjonalnym kodzie Python. Zwiększa czytelność projektów, poprawia ich bezpieczeństwo oraz redukuje ryzyko popełnienia błędów w powtarzalnych fragmentach kodu.

---
## Powiązane materiały
- [Niemodyfikowalne struktury danych w Pythonie](niemodyfikowalne-struktury-danych-w-pythonie.md)
- [Pydantic vs Dataclasses: Kiedy używać którego?](Pydantic_vs_Dataclasses.md)
