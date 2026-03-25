# Pydantic przykłady i zastosowania

**Data:** 2025-09-21

---

**User:**

Podaj powót używania biblioteki pydantic i przykłady

---

**Assistant:**

Biblioteka **Pydantic** w Pythonie jest używana głównie do:  

1. **Walidacji danych** – automatycznie sprawdza, czy przekazane dane mają odpowiednie typy i spełniają zadane ograniczenia.  
2. **Serializacji i deserializacji** – pozwala łatwo zamieniać dane między Pythonem a JSON-em (lub innymi formatami).  
3. **Wymuszania typów** – dzięki wykorzystaniu *type hints* zapewnia, że dane wejściowe i wyjściowe są zgodne z oczekiwaniami.  
4. **Łatwej integracji z API i bazami danych** – np. w FastAPI Pydantic jest podstawą walidacji requestów i response’ów.  

---

### Przykład 1 – Walidacja danych
```python
from pydantic import BaseModel, Field

class User(BaseModel):
    id: int
    name: str
    age: int = Field(..., ge=18, description="Użytkownik musi mieć co najmniej 18 lat")

# poprawne dane
user = User(id=1, name="Jan", age=25)
print(user)

# niepoprawne dane -> wyjątek ValidationError
user = User(id=2, name="Anna", age=15)
```

Tutaj Pydantic automatycznie sprawdzi, czy `age >= 18`.  

---

### Przykład 2 – Konwersja typów
```python
class Product(BaseModel):
    id: int
    price: float
    available: bool

product = Product(id="123", price="19.99", available="true")
print(product)
# wynik: id=123 price=19.99 available=True
```
Pydantic automatycznie przekonwertuje stringi na odpowiednie typy.  

---

### Przykład 3 – Serializacja do JSON
```python
user = User(id=1, name="Jan", age=30)
print(user.json())
# {"id": 1, "name": "Jan", "age": 30}
```

---

Chcesz, żebym podał też przykład użycia **Pydantic w FastAPI** (najpopularniejsze zastosowanie), czy interesuje Cię tylko czysty Python?

---

**User:**

Wymuszania typów - jest chyba jeszcze jakaś inna popularna biblioteka do tego?

---

**Assistant:**

Tak, oprócz **Pydantic** do walidacji i wymuszania typów w Pythonie dość popularna jest też biblioteka **marshmallow**.  

Różnice:  
- **Pydantic** – mocno oparty na *type hints* (Python ≥3.6), waliduje dane i robi konwersję typów automatycznie.  
- **marshmallow** – bardziej tradycyjne podejście: definiujesz schematy (fields, validators) i samodzielnie mapujesz dane; daje większą elastyczność, ale mniej integruje się z adnotacjami typów.  

---

### Przykład w **marshmallow**
```python
from marshmallow import Schema, fields, ValidationError

class UserSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    age = fields.Int(required=True)

schema = UserSchema()

# poprawne dane
result = schema.load({"id": "1", "name": "Jan", "age": 30})
print(result)  # {'id': 1, 'name': 'Jan', 'age': 30}

# błędne dane
try:
    schema.load({"id": "2", "name": "Anna", "age": "abc"})
except ValidationError as err:
    print(err.messages)
    # {'age': ['Not a valid integer.']}
```

---

Poza marshmallow czasem używa się też:  
- **Cerberus** – prosty walidator danych z własnym DSL do reguł.  
- **Voluptuous** – walidacja zdefiniowana w postaci Pythonowych struktur danych.  

Chcesz, żebym przygotował porównanie **Pydantic vs Marshmallow** pod kątem wydajności i ergonomii, czy wystarczy Ci lista alternatyw?

---

**User:**

a co z biblioteką types?

---

**Assistant:**

W Pythonie standardowa biblioteka **`types`** istnieje, ale ona **nie służy do walidacji ani wymuszania typów** w sensie takim jak Pydantic czy marshmallow.  

`types` zawiera **definicje specjalnych typów i obiektów** używanych wewnętrznie w interpreterze Pythona – np.:  
- `types.FunctionType` – typ dla funkcji,  
- `types.MethodType` – typ dla metod,  
- `types.ModuleType` – typ dla modułów,  
- `types.SimpleNamespace` – prosty obiekt działający jak słownik z atrybutami,  
- `types.MappingProxyType` – niemodyfikowalny widok na słownik.  

Przykład:  

```python
import types

def foo(): 
    return 42

print(isinstance(foo, types.FunctionType))  # True

ns = types.SimpleNamespace(a=1, b=2)
print(ns.a, ns.b)  # 1 2
```

---

Jeśli chodzi o **wymuszanie typów** w Pythonie, to zazwyczaj korzysta się z:  
- **`typing`** (a nie `types`) – moduł standardowy, który dostarcza adnotacje typów (`List[int]`, `Optional[str]`, `TypedDict` itp.).  
- **mypy** / **pyright** – narzędzia do statycznej analizy typów, które potrafią sprawdzać poprawność kodu względem adnotacji.  
- **Pydantic**, **marshmallow**, **Cerberus** – gdy chcemy runtime’ową walidację danych.  

---

Czy miałeś na myśli **`types`** z biblioteki standardowej, czy może raczej **`typing`** albo coś związanego z analizą typów (np. mypy)?

---

**User:**

czyli pydantic i typing mogą służyć do wymuszenia typów tak?

---

**Assistant:**

Nie do końca w ten sam sposób 🙂  

- **`typing`**  
  - to moduł standardowy Pythona, który daje **adnotacje typów** (np. `list[int]`, `dict[str, float]`, `Optional[str]`).  
  - samo w sobie **nie wymusza** typów w runtime — Python adnotacje ignoruje podczas wykonywania.  
  - używa się ich głównie do statycznej analizy przez narzędzia typu **mypy**, **pyright**, **PyCharm inspections**.  

Przykład (`typing` + `mypy`):  
```python
from typing import List

def total(values: List[int]) -> int:
    return sum(values)

print(total([1, 2, 3]))       # ok
print(total(["a", "b", "c"])) # w runtime przejdzie, ale mypy zgłosi błąd
```

---

- **Pydantic**  
  - korzysta z adnotacji typów (tych z `typing`), ale dodatkowo robi **walidację i konwersję typów w runtime**.  
  - jeśli podasz niepoprawny typ, rzuci `ValidationError`.  
  - w odróżnieniu od `typing` faktycznie **wymusza poprawność danych w czasie działania programu**.  

Przykład (Pydantic):  
```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str

# poprawne
print(User(id="1", name="Jan"))  # id zostanie przekonwertowane na int

# niepoprawne -> ValidationError
print(User(id="abc", name=123))
```

---

Podsumowanie:  
- **`typing` + mypy/pyright** → sprawdzanie *przed uruchomieniem* (statyczna analiza).  
- **Pydantic** → sprawdzanie *podczas uruchomienia* (runtime validation).  

Chcesz, żebym rozpisał dokładniej **kiedy lepiej używać Pydantic, a kiedy wystarczy typing+mypy**?