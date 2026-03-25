# Pydantic vs Dataclasses: Kiedy używać którego?

Zarówno wbudowane w Pythona `dataclasses`, jak i biblioteka zewnętrzna `Pydantic`, służą do tworzenia klas przechowujących dane, redukując ilość powtarzalnego kodu (tzw. *boilerplate*). Mimo podobnej składni, ich przeznaczenie i sposób działania są zupełnie inne.

Zrozumienie tych różnic jest kluczowe dla pisania bezpiecznego i wydajnego kodu w Pythonie.

---

## 1. `dataclasses` (Wbudowana biblioteka standardowa)

`dataclass` został wprowadzony w Pythonie 3.7. Służy **wyłącznie do generowania metod specjalnych**, takich jak `__init__`, `__repr__`, `__eq__` itp., na podstawie adnotacji typów.

### Kluczowe cechy

- **Brak walidacji (Type Hinting to tylko wskazówka):** `dataclass` **nie sprawdza i nie konwertuje typów w czasie wykonania**. Jeśli przypiszesz string do pola, które powinno być intem, `dataclass` tego nie wyłapie.
- **Szybkość:** Działa bardzo szybko, ponieważ nie wprowadza narzutu związanego z walidacją w czasie wykonywania.
- **Brak zewnętrznych zależności:** Biblioteka wbudowana w interpreter.

### Kiedy używać `dataclasses`?

1. **Wewnętrzne struktury danych:** Kiedy potrzebujesz stworzyć klasę reprezentującą dane dla wewnętrznej logiki aplikacji, i **ufasz** danym wejściowym (np. pochodzą z już zwalidowanego źródła).
2. **Krytyczna wydajność:** Kiedy tworzysz obiekty w bardzo dużej ilości i zależy Ci na najmniejszym możliwym narzucie czasowym i pamięciowym.
3. **Proste DTO (Data Transfer Objects):** Gdy służą głównie do uporządkowania kodu i zgrupowania kilku zmiennych w jedną strukturę.

### Przykład użycia `dataclass`

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: int
    y: int

# Poprawne użycie
p1 = Point(10, 20)
print(p1)  # Output: Point(x=10, y=20)

# Użycie niezgodne z typem - dataclass na to ZEZWALA!
p2 = Point("dziesięć", 20.5)
print(p2)  # Output: Point(x='dziesięć', y=20.5) - NIE ZWRÓCI BŁĘDU!
```

---

## 2. `Pydantic` (Zewnętrzna biblioteka)

`Pydantic` to popularna biblioteka do parsowania i walidacji danych. Koncentruje się na zagwarantowaniu, że typy danych i ich zawartość są zgodne z definicją w czasie działania programu. Pod maską korzysta z Rust (w wersji V2), co czyni ją bardzo szybką jak na bibliotekę walidującą.

### Kluczowe cechy

- **Silna walidacja i rzutowanie typów (Coercion):** Jeśli system oczekuje typu `int`, a otrzyma stringa np. `"10"`, Pydantic spróbuje przekonwertować go na wartość `10`. Jeśli konwersja się nie uda, zgłosi jasny błąd (`ValidationError`).
- **Rozbudowana walidacja niestandardowa:** Pozwala wymuszać długości list, przedziały liczb (np. `x > 0`), wyrażenia regularne i tworzyć niestandardowe metody walidujące (`@field_validator`).
- **Ekosystem:** Jest fundamentem dla wielu nowoczesnych narzędzi, takich jak **FastAPI** (walidacja payloadów API).
- **Serializacja do/z formatu JSON:** Łatwe parsowanie ze słowników/JSONów do obiektów i na odwrót (`model_dump`, `model_dump_json`).

### Kiedy używać `Pydantic`?

1. **Dane z zewnątrz (Brak zaufania):** Kiedy dane pochodzą od użytkownika, z żądania HTTP, zewnętrznego API, formularza lub pliku konfiguracyjnego (JSON, YAML).
2. **Walidacja biznesowa:** Gdy wymagany jest nie tylko konkretny typ, ale też konkretna zawartość (np. string musi być poprawnym e-mailem, a wiek w przedziale 18-99).
3. **Tworzenie API (np. FastAPI):** Do definiowania schematów żądań (Request) i odpowiedzi (Response).
4. **Zarządzanie konfiguracją:** (m.in. pakiet pydantic-settings) Pydantic jest świetny do bezpiecznego wczytywania i walidowania zmiennych środowiskowych i konfiguracji.

### Przykład użycia `Pydantic`

```python
from pydantic import BaseModel, ValidationError, EmailStr, Field

class User(BaseModel):
    id: int
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    age: int = Field(ge=18, description="Wiek musi wynosić co najmniej 18")

# Poprawne utworzenie
user = User(id="123", username="johndoe", email="john@example.com", age=25)
print(user.id) # Output: 123 - zauważ, że "123" jako str zostało rzutowane na int!

# Błędne wejścia - zostanie rzucony błąd walidacji
try:
    bad_user = User(
        id=456, 
        username="jo", # Błąd: za krótki string (min_length=3)
        email="invalid-email", # Błąd: nieprawidłowy format email
        age=16 # Błąd: poniżej min. wartości
    )
except ValidationError as e:
    print(e.json(indent=2))
```

---

## Podsumowanie i Porównanie: Zasada Kciuka

| Cechy | `dataclasses` | `Pydantic` |
| :--- | :--- | :--- |
| **Typ biblioteki** | Wbudowana (Standard Library) | Zewnętrzna (`pip install pydantic`) |
| **Główny Cel** | Ograniczenie boilerplate'u, kontener na dane | Parsowanie danych i gwarancja typu/struktury |
| **Walidacja typu w czasie wykonania** | ❌ Nie | ✅ Tak (zwraca błędy) |
| **Konwersja typów (Casting/Coercion)**| ❌ Nie | ✅ Tak (`"5"` -> `5`) |
| **Serializacja JSON** | Skomplikowana (wymaga obejść/dodatkowego kodu) | Wbudowana, łatwa w użyciu (`.model_dump_json()`) |
| **Zależności i pakiety zależne** | Brak (gotowa do użycia) | Polegają na nim m.in. FastAPI, LangChain |
| **Wydajność** | Bardzo wysoka | Wolniejsza od dataclass (narzut na walidację)* |

**\* Ciekawostka dot. wydajności Pydantic:** W `Pydantic` v2, cała logika walidująca została przepisana w języku **Rust** (biblioteka `pydantic-core`), dzięki czemu biblioteka działa niesamowicie szybko. Wprawdzie nadal jest odrobinę wolniejsza niż sam `dataclass`, jednak dla 99% projektów różnica jest niedostrzegalna, z kolei zysk płynący z posiadania bezpiecznego i sprawdzonego zestawu danych jest ogromny.

---

### 💡 Wnioski (Zasada kciuka)

- Traktuj **`Pydantic`** jako **"bramkarza" na wejściu do Twojego systemu.** Używaj go na krawędziach systemu, tam gdzie odbierasz dane i musisz mieć 100% pewności, że są one poprawne i zgodne ze schematem (np. Requesty do API, wysyłanie formularzy, parsowanie plików konfiguracyjnych).
- Traktuj **`dataclass`** jako **"magazyniera" wewnątrz Twojego systemu.** Używaj go głęboko pod maską: tam, gdzie dane zostały już wcześniej sprawdzone (np. przez Pydantic), ufasz ich wartościom i zależy Ci po prostu na ich zebraniu w ustrukturyzowaną formę w celu przetworzenia, unikając jednocześnie narzutu czasowego połączonego z ponowną walidacją.
