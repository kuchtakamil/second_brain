# Instrukcja `match ... case` w Pythonie (Structural Pattern Matching)

Wprowadzona w Pythonie 3.10 (w ramach PEP 634, PEP 635 i PEP 636) instrukcja `match ... case` przyniosła do języka mechanizm dopasowywania wzorców (ang. *Structural Pattern Matching*). Choć na pierwszy rzut oka przypomina ona konstrukcję `switch ... case` znaną z innych języków programowania (takich jak C, C++ czy Java), w rzeczywistości jest to narzędzie **o wiele potężniejsze**.

`match ... case` nie ogranicza się do prostego porównywania wartości. Pozwala na sprawdzanie struktury obiektów, dekompozycję (rozpakowywanie) danych, filtrowanie za pomocą warunków (tzw. *guards*) oraz automatyczne bindowanie (przypisywanie) wartości do zmiennych lokalnych.

---

## 1. Dlaczego to nie jest zwykły `switch ... case`?

W klasycznych instrukcjach typu `switch` sprawdzamy, czy dana zmienna jest równa konkretnej wartości (liczbie, ciągowi znaków itp.). W Pythonie dopasowywanie wzorców działa **strukturalnie**:
1. **Dopasowanie typu i struktury:** Możemy określić, czy dopasowywany obiekt jest np. listą zawierającą dokładnie trzy elementy, z których pierwszy to napis `"HTTP"`.
2. **Ekstrakcja danych (Destructuring):** Jeśli wzorzec pasuje, Python automatycznie wyciąga wartości z wewnątrz struktury i przypisuje je do wskazanych zmiennych.
3. **Typowanie klas (Class patterns):** Pozwala na dopasowanie obiektów własnych klas, sprawdzanie ich typów oraz wartości ich atrybutów.

---

## 2. Podstawowa składnia i proste dopasowania

Zacznijmy od najprostszych zastosowań, aby oswoić się ze składnią.

### 2.1. Dopasowanie do literałów (Literal Patterns)

To najbardziej klasyczne użycie. Sprawdzamy wartość zmiennej i wykonujemy odpowiedni blok kodu.

```python
def handle_http_status(status: int) -> str:
    match status:
        case 200:
            return "OK"
        case 400:
            return "Bad Request"
        case 404:
            return "Not Found"
        case 500:
            return "Internal Server Error"
        case _:
            return "Unknown Status Code"
```

> [!NOTE]
> Znak podkreślenia `_` działa jako tzw. **wildcard pattern** (wzorzec wieloznaczny). Pasuje do absolutnie wszystkiego i służy jako gałąź domyślna (*catch-all*), odpowiednik `else` w instrukcjach `if` lub `default` w klasycznym `switch`.

### 2.2. Alternatywy wzorców za pomocą operatora `|` (Or Pattern)

Możemy połączyć kilka wzorców w jednej linii za pomocą pionowej kreski (`|`), co eliminuje powtarzanie kodu.

```python
def is_weekend(day: str) -> bool:
    match day.lower():
        case "saturday" | "sunday":
            return True
        case "monday" | "tuesday" | "wednesday" | "thursday" | "friday":
            return False
        case _:
            raise ValueError(f"Invalid day: {day}")
```

---

## 3. Zaawansowane dopasowywanie i dekompozycja (Destructuring)

Prawdziwa moc instrukcji `match ... case` ujawnia się, gdy zaczynamy rozpakowywać złożone struktury danych.

### 3.1. Dopasowywanie sekwencji (Sequence Patterns)

Możemy dopasowywać listy lub krotki. Python sprawdzi zarówno długość sekwencji, jak i wartości jej elementów.

```python
def process_command(command: list[str]) -> str:
    match command:
        # Pasuje tylko do pustej listy
        case []:
            return "No command provided."
        
        # Pasuje do jednoelementowej listy, np. ["quit"]
        case ["quit"]:
            return "System is shutting down..."
            
        # Pasuje do dwuelementowej listy, gdzie pierwszy element to "go", 
        # a drugi przypisujemy do zmiennej 'direction'
        case ["go", direction]:
            return f"Moving in direction: {direction}"
            
        # Pasuje do trójelementowej listy o strukturze ["teleport", x, y]
        case ["teleport", x, y]:
            return f"Teleporting to X: {x}, Y: {y}"
            
        # Rozpakowywanie pozostałych elementów (analogicznie do *args)
        # Pasuje do listy zaczynającej się od "run", a resztę elementów binduje do listy 'args'
        case ["run", *args]:
            return f"Executing job with parameters: {args}"
            
        # Każda inna sekwencja
        case _:
            return "Command not recognized."
```

### 3.2. Dopasowywanie słowników (Mapping Patterns)

Możemy weryfikować zawartość i strukturę słowników. Wzorzec pasuje, jeśli słownik zawiera wskazane klucze (może mieć też dodatkowe klucze, chyba że jawnie je zablokujemy).

```python
def process_api_response(response: dict) -> str:
    match response:
        # Pasuje, jeśli słownik ma klucz "status" o wartości "error" oraz klucz "message"
        case {"status": "error", "message": err_msg}:
            return f"An error occurred: {err_msg}"
            
        # Pasuje, jeśli słownik ma klucz "status" o wartości "success" oraz klucz "data"
        case {"status": "success", "data": {"id": user_id, "name": user_name}}:
            return f"User successfully loaded. ID: {user_id}, Name: {user_name}"
            
        # Przechwycenie pozostałych kluczy za pomocą **rest
        case {"status": "pending", **additional_details}:
            return f"Request pending. Extra info: {additional_details}"
            
        case _:
            return "Invalid payload format."
```

---

## 4. Dopasowywanie obiektów klas i Dataclasses (Class Patterns)

`match ... case` doskonale integruje się z programowaniem zorientowanym obiektowo (OOP). Możemy sprawdzać instancje konkretnych klas, dopasowywać wartości ich atrybutów oraz przypisywać je do zmiennych.

### 4.1. Dopasowywanie za pomocą argumentów nazwanych (Keyword Arguments)

Możemy filtrować obiekty na podstawie klasy i wartości ich właściwości.

```python
class User:
    def __init__(self, username: str, role: str):
        self.username = username
        self.role = role

def check_permission(actor: object) -> str:
    match actor:
        # Pasuje, jeśli actor jest instancją klasy User, a jego role to "admin"
        case User(role="admin", username=name):
            return f"Access granted. Welcome Admin {name}!"
            
        # Pasuje dla każdego innego użytkownika
        case User(username=name):
            return f"Access limited for standard user: {name}"
            
        case _:
            return "Access denied. Unknown entity."
```

### 4.2. Dopasowywanie za pomocą argumentów pozycyjnych i atrybut `__match_args__`

Aby móc dopasowywać atrybuty klas pozycyjnie (np. `case Point(0, y):` zamiast `case Point(x=0, y=y):`), klasa musi definiować specjalny atrybut klasy o nazwie `__match_args__`. Jest to krotka zawierająca nazwy atrybutów w kolejności ich dopasowywania.

Dekorator `@dataclass` automatycznie generuje ten atrybut!

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: int
    y: int
    
# Dzięki temu, że Point jest dataclass, pod maską wygenerowane zostało:
# Point.__match_args__ = ('x', 'y')

def analyze_point(point: Point) -> str:
    match point:
        # Pasuje, gdy x=0 i y=0
        case Point(0, 0):
            return "Point is at the origin (0, 0)."
            
        # Pasuje, gdy x=0 (oś Y). Wartość y jest bindowana do zmiennej
        case Point(0, y):
            return f"Point is on the Y-axis at height {y}."
            
        # Pasuje, gdy y=0 (oś X). Wartość x jest bindowana do zmiennej
        case Point(x, 0):
            return f"Point is on the X-axis at position {x}."
            
        # Każdy inny punkt
        case Point(x, y):
            return f"Point is at ({x}, {y})."
```

> [!TIP]
> Jeśli tworzysz zwykłą klasę (bez `@dataclass`) i chcesz używać dopasowań pozycyjnych, zdefiniuj `__match_args__` ręcznie:
> ```python
> class Color:
>     __match_args__ = ("r", "g", "b")
>     def __init__(self, r: int, g: int, b: int):
>         self.r, self.g, self.b = r, g, b
> ```

---

## 5. Warunki dodatkowe (Guards) oraz słowo kluczowe `as`

### 5.1. Strażnicy wzorca (Guards)

Do dowolnej gałęzi `case` możemy dodać warunek logiczny `if` na samym końcu. Wzorzec zostanie dopasowany tylko wtedy, gdy cała struktura pasuje **oraz** warunek po `if` zwraca prawdę.

```python
def check_temperature(reading: dict) -> str:
    match reading:
        # Pasuje, jeśli sensor zwraca typ "celsius", a wartość jest powyżej 100
        case {"type": "celsius", "value": val} if val > 100:
            return f"Critical! Temperature is extremely high: {val}°C"
            
        case {"type": "celsius", "value": val}:
            return f"Temperature is normal: {val}°C"
            
        case _:
            return "Unknown sensor data."
```

### 5.2. Słowo kluczowe `as` (AS Patterns)

Umożliwia przypisanie pasującej części wzorca do zmiennej. Jest to niezwykle przydatne, gdy dopasowujemy skomplikowaną strukturę, ale jednocześnie potrzebujemy zachować referencję do całego dopasowanego fragmentu.

```python
def handle_event(event: dict) -> str:
    match event:
        # Dopasowujemy typ wydarzenia, ale chcemy mieć dostęp do całego obiektu
        case {"type": "click", "payload": {"x": _, "y": _}} as full_click_event:
            return f"Click detected. Logged action: {full_click_event}"
            
        # Możemy również używać 'as' przy alternatywach wzorców
        case "err" | "error" as status_str:
            return f"Status matches error token: {status_str}"
```

---

## 6. Dobre praktyki i kiedy używać `match ... case`?

Dopasowywanie wzorców to rewelacyjne narzędzie, ale nie należy stosować go ślepo w każdym miejscu zamiast `if-else`.

### Kiedy warto stosować `match ... case`?
- **Przetwarzanie zagnieżdżonych struktur:** takich jak drzewa składniowe, odpowiedzi z API (JSON/dict), pliki konfiguracyjne.
- **Implementacja maszyn stanowych:** gdzie zachowanie zależy od aktualnego stanu i rodzaju zdarzenia.
- **Refaktoryzacja rozbudowanych łańcuchów `if-elif-else`:** które badają typy obiektów (`isinstance`) lub rozpakowują krotki.

### Kiedy lepiej pozostać przy `if-else`?
- **Proste porównania logiczne:** Jeśli sprawdzasz tylko jedną prostą nierówność (np. `if age >= 18`), instrukcja `match` jest przerostem formy nad treścią.
- **Warunki niezależne od struktury danych:** Kiedy badasz różne, niezwiązane ze sobą zmienne w poszczególnych gałęziach warunkowych.

---

## 7. Podsumowanie: match-case vs if-elif-else

| Cecha | `if ... elif ... else` | `match ... case` |
| :--- | :--- | :--- |
| **Główny cel** | Sprawdzanie warunków logicznych (True/False) | Analiza strukturalna danych i ekstrakcja |
| **Dekompozycja** | Ręczna (np. `x, y = point.x, point.y`) | Automatyczna (wbudowana we wzorzec) |
| **Sprawdzanie typów** | Poprzez `isinstance(obj, ClassName)` | Wbudowane w składnię klasy (np. `case ClassName()`) |
| **Wydajność** | Liniowa (sprawdza po kolei każdy warunek) | Zoptymalizowana przez kompilator pod kątem skoków |

---
## Powiązane materiały
- [Dekorator `@dataclass` w Pythonie: Metody i Korzyści](dekorator-dataclass-metody-i-korzysci.md)
- [Niemodyfikowalne struktury danych w Pythonie](niemodyfikowalne-struktury-danych-w-pythonie.md)
- [Pydantic vs Dataclasses: Kiedy używać którego?](Pydantic_vs_Dataclasses.md)
