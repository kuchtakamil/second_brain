# W Python do czego służy pydantic i jego BaseModel oraz Field? Podaj przykłady

**Data:** 28 lis 2025, 17:52:11 CET

---

**User:**

W Python do czego służy pydantic i jego BaseModel oraz Field? Podaj przykłady

---

**Gemini:**

**Pydantic** to biblioteka do parsowania i walidacji danych w Pythonie, która wykorzystuje standardowe podpowiedzi typów (type hints). W przeciwieństwie do narzędzi statycznej analizy kodu (jak Mypy), Pydantic działa w **czasie rzeczywistym (runtime)**.

Jej głównym zadaniem jest zagwarantowanie, że dane wejściowe (np. JSON z API, zmienne środowiskowe, argumenty funkcji) są zgodne z zadeklarowaną strukturą. Pydantic nie tylko sprawdza typy, ale także dokonuje ich **koercji** (rzutowania) – np. zamienia string `"123"` na integer `123`, jeśli taki typ został zadeklarowany.

Oto szczegółowe omówienie kluczowych komponentów: `BaseModel` oraz `Field`.

---

### 1. `BaseModel` – Fundament struktury

`BaseModel` to klasa bazowa, z której dziedziczą wszystkie twoje modele danych. Definiuje ona schemat danych oraz dostarcza mechanizmy do ich walidacji, serializacji i deserializacji.

#### Główne funkcje `BaseModel`:

- **Parsowanie danych:** Automatycznie konwertuje dane wejściowe na zadeklarowane typy.
- **Walidacja:** Jeśli konwersja jest niemożliwa lub dane nie spełniają warunków, rzucany jest wyjątek `ValidationError`.
- **Serializacja:** Metody takie jak `.model_dump()` (zwraca słownik) oraz `.model_dump_json()` (zwraca string JSON) pozwalają na łatwy eksport danych.
- **JSON Schema:** Metoda `.model_json_schema()` generuje schemat JSON zgodny ze standardem OpenAPI.

#### Przykład podstawowy:

```
from pydantic import BaseModel, ValidationError
from typing import List, Optional

# Defining the schema
class UserProfile(BaseModel):
    id: int
    username: str
    is_active: bool = True  # Default value
    tags: List[str] = []    # Default mutable value (safe in Pydantic)
    metadata: Optional[dict] = None

# 1. Valid data with type coercion
input_data = {
    "id": "550",          # String "550" will be cast to int 550
    "username": "jdoe",
    "tags": ["admin", "editor"]
}

user = UserProfile(**input_data)

print(f"ID Type: {type(user.id)}")  # <class 'int'>
print(user.model_dump_json(indent=2))

# 2. Invalid data handling
try:
    UserProfile(id="not-an-number", username="jdoe")
except ValidationError as e:
    print("\nValidation Error:")
    print(e.json())
```

Warto zauważyć, że w Pydantic (w przeciwieństwie do standardowych `dataclasses`) użycie mutowalnego domyślnego argumentu (np. `tags: List[str] = []`) jest bezpieczne, ponieważ Pydantic tworzy nową kopię listy dla każdej instancji modelu.

---

### 2. `Field` – Zaawansowana konfiguracja pól

Funkcja `Field` służy do dostosowywania metadanych oraz reguł walidacji dla pojedynczych atrybutów modelu. Używa się jej, gdy sama adnotacja typu (np. `int`) jest niewystarczająca.

#### Kluczowe zastosowania `Field`:

- **Ograniczenia wartości:** Definiowanie zakresów liczbowych (`gt`, `lt`, `ge`, `le`), długości stringów (`min_length`, `max_length`) czy dopasowania do wyrażeń regularnych (`pattern`).
- **Aliasy:** Obsługa nazw pól, które nie są poprawnymi identyfikatorami w Pythonie (np. `user-id` w JSON vs `user_id` w Pythonie) lub mapowanie między konwencjami camelCase a snake\_case.
- **Wartości domyślne dynamiczne:** `default_factory` dla wartości generowanych w momencie tworzenia instancji (np. `uuid4`, `datetime.now`).
- **Metadane dokumentacji:** `title`, `description`, `examples` – używane przy generowaniu dokumentacji API (np. w Swagger UI przy użyciu FastAPI).
- **Wykluczanie z serializacji:** Parametr `exclude=True`.

#### Przykład zaawansowany z użyciem `Field`:

```
from pydantic import BaseModel, Field, EmailStr
from uuid import UUID, uuid4
from datetime import datetime
from typing import Annotated

class AdvancedProduct(BaseModel):
    # Dynamic default value using a factory
    uid: UUID = Field(default_factory=uuid4, title="Unique Identifier")
    
    # String constraints and metadata
    name: str = Field(
        ...,  # "..." means the field is required (no default)
        min_length=3, 
        max_length=50, 
        description="Name of the product"
    )
    
    # Numeric constraints
    price: float = Field(
        gt=0, 
        le=10000, 
        description="Price strictly greater than 0"
    )
    
    # Alias handling (e.g., receiving 'manufacturing-date' from API)
    created_at: datetime = Field(
        default_factory=datetime.now, 
        alias="manufacturing-date"
    )
    
    # Data that should be validated but not exposed in dumps
    internal_code: str = Field(exclude=True)

# Simulating external API data with aliases
external_data = {
    "name": "Super Widget",
    "price": 199.99,
    "manufacturing-date": "2023-10-27T10:00:00",
    "internal_code": "SECRET_123"
}

product = AdvancedProduct(**external_data)

# Accessing via Python attribute name
print(f"Created at: {product.created_at}")

# Serializing (internal_code is excluded, alias can be used)
print(product.model_dump(by_alias=True))
```

---

### 3. Zaawansowane mechanizmy i Pydantic V2

Od wersji 2.0 Pydantic został przepisany w języku Rust (`pydantic-core`), co drastycznie zwiększyło wydajność. Wprowadzono również nowe koncepcje dotyczące konfiguracji i walidacji.

#### ConfigDict (Konfiguracja modelu)

Zamiast wewnętrznej klasy `Config`, w V2 używa się słownika `model_config` do sterowania zachowaniem całego modelu.

```
from pydantic import BaseModel, ConfigDict

class StrictModel(BaseModel):
    # Configuration:
    # - strict=True: Disables type coercion (e.g., string "123" won't become int 123)
    # - frozen=True: Makes the instance immutable (hashable)
    # - str_strip_whitespace=True: Trims strings automatically
    model_config = ConfigDict(
        strict=True, 
        frozen=True, 
        str_strip_whitespace=True
    )

    age: int
    name: str

try:
    # This raises an error because strict=True forbids string-to-int coercion
    model = StrictModel(age="30", name=" Alice ")
except Exception as e:
    print("Strict validation failed intendedly.")

# Correct usage
model = StrictModel(age=30, name=" Alice ")
print(f"Name stripped: '{model.name}'") # Output: 'Alice'

# model.age = 31  # This would raise ValidationError because frozen=True
```

#### Annotated Validators (Nowoczesne podejście)

Zamiast używać `Field` do wszystkiego, Pydantic promuje użycie `typing.Annotated`, co pozwala na lepszą separację logiki typów od logiki biznesowej i wielokrotne użycie definicji.

```
from typing import Annotated
from pydantic import BaseModel, Field, AfterValidator

def validate_even(v: int) -> int:
    if v % 2 != 0:
        raise ValueError("Number must be even")
    return v

# Reusable type definition
EvenInt = Annotated[int, Field(gt=0), AfterValidator(validate_even)]

class Config(BaseModel):
    cpu_cores: EvenInt
    worker_threads: EvenInt

cfg = Config(cpu_cores=4, worker_threads=8)
```

### Podsumowanie różnic

| Cecha | `BaseModel` | `Field` |
| --- | --- | --- |
| **Rola** | Kontener (klasa) definiujący strukturę całego obiektu. | Konfigurator pojedynczego atrybutu wewnątrz kontenera. |
| **Odpowiedzialność** | Serializacja, parsowanie całego wejścia, zarządzanie konfiguracją. | Walidacja szczegółowa, metadane, aliasy, wartości domyślne. |
| **Użycie** | Dziedziczenie (`class X(BaseModel)`). | Przypisanie do zmiennej (`x: int = Field(...)`). |

Czy chcesz, abym pokazał, jak zintegrować modele Pydantic z FastAPI lub jak napisać niestandardowe walidatory (custom validators) dla bardziej złożonej logiki biznesowej?