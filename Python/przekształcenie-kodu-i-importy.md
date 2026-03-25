# Przekształcenie kodu i importy

**Data:** 2025-12-15

---

**User:**

```python
from __future__ import annotations

from pydantic import BaseModel, BeforeValidator, ConfigDict
from annotated_types import MinLen
from typing import Annotated
import hashlib


def _hash(v: str) -> str:
    """Hash password string to SHA-256."""
    return hashlib.sha256(v.encode()).hexdigest()


class UserDataPydanticTypes(BaseModel):
    username: str
    nickname: str
    password_hash: Annotated[str, MinLen(8), AfterValidator(_hash)]

    model_config = ConfigDict(extra='forbid')


if __name__ == "__main__":
    user = UserDataPydanticTypes(
        username="johndoe",
        nickname="John",
        password_hash="hello",
    )
```

Wyjasnij importy, przede wszystkim **future** i annoteted_types

---

**Assistant:**

> Uwaga: na screenie w importach jest `BeforeValidator`, ale w adnotacji pola użyty jest `AfterValidator`. Zakładam, że to literówka na screenie i faktycznie chodzi o `AfterValidator`.

---

## Wyjaśnienie importów

### `from __future__ import annotations`

To jest **future import**, który zmienia sposób interpretacji adnotacji typów w Pythonie.

Co robi konkretnie:

- **odracza ewaluację adnotacji typów**
- wszystkie adnotacje są przechowywane jako **stringi**, a nie realne obiekty w momencie definicji klasy / funkcji

Dlaczego to jest ważne:

1. **Brak problemów z forward references**

   ```python
   class A:
       b: B  # bez future import -> NameError
   ```

   Z `__future__ import annotations` to działa bez cudzysłowów.

2. **Lepsza współpraca z bibliotekami typu Pydantic**
   - Pydantic v2 intensywnie korzysta z adnotacji
   - stringowe adnotacje są lżejsze i szybsze w imporcie
   - mniej problemów z cyklicznymi zależnościami

3. **Od Pythona 3.11 to zachowanie jest domyślne**, więc ten import jest głównie:
   - wymagany w 3.9 / 3.10
   - często dodawany dla kompatybilności wstecznej

---

### `from annotated_types import MinLen`

`annotated_types` to **mała biblioteka pomocnicza**, z której korzystają m.in.:

- Pydantic
- FastAPI
- inne frameworki oparte o `typing.Annotated`

Zawiera **czyste, niezależne od frameworków ograniczenia semantyczne**, np.:

- `MinLen`
- `MaxLen`
- `Gt`, `Ge`, `Lt`, `Le`
- `MultipleOf`

`MinLen(8)` oznacza:
> minimalna długość wartości to 8

Samo w sobie:

- **nie waliduje niczego**
- jest tylko **metadanymi**

Dopiero Pydantic interpretuje te metadane i wykonuje walidację.

---

### `from typing import Annotated`

`Annotated` pozwala dołączyć **dodatkowe metadane do typu**.

Schemat:

```python
Annotated[typ, metadata1, metadata2, ...]
```

W Twoim przypadku:

```python
password_hash: Annotated[
    str,
    MinLen(8),
    AfterValidator(_hash)
]
```

Znaczenie:

- typ bazowy: `str`
- ograniczenie: minimum 8 znaków
- po walidacji: uruchom `_hash`

`Annotated`:

- nie zmienia typu z punktu widzenia Pythona
- jest nośnikiem informacji dla narzędzi (Pydantic, FastAPI, mypy)

---

### `from pydantic import BaseModel, BeforeValidator, ConfigDict`

- **`BaseModel`**
  - bazowa klasa modeli Pydantic
  - odpowiada za:
    - walidację
    - konwersję typów
    - serializację

- **`BeforeValidator` / `AfterValidator`**
  - hooki walidacyjne dla `Annotated`
  - `BeforeValidator(fn)` – uruchamiany **przed** walidacją typu
  - `AfterValidator(fn)` – uruchamiany **po** walidacji typu

W tym kodzie:

- najpierw sprawdzane jest `MinLen(8)`
- potem wykonywany jest `_hash`
- efekt końcowy w modelu to już **hash**, nie surowe hasło

- **`ConfigDict`**
  - konfiguracja modelu w Pydantic v2
  - zastępuje starą klasę `Config`

```python
model_config = ConfigDict(extra='forbid')
```

Oznacza:

- każde nieznane pole → błąd
- brak „cichego” ignorowania nadmiarowych danych

---

Jeśli chcesz, mogę:

- rozpisać dokładną kolejność walidacji krok po kroku
- pokazać różnicę `BeforeValidator` vs `AfterValidator` na przykładzie
- porównać to podejście z klasycznymi `@field_validator` w Pydantic v2

---

**User:**

odnośnie "from **future** import annotations" wyjaśnij szczegółowo kiedy i jak kod byłby ewoluowany z i bez tegoo importu.

---

**Assistant:**

Poniżej masz **techniczne, krok-po-kroku** wyjaśnienie, **kiedy**, **jak** i **dlaczego** kod jest ewaluowany **z** i **bez**  
`from __future__ import annotations`.

Skupię się na tym, co faktycznie robi interpreter CPythona, a nie na ogólnikach.

---

## 1. Co znaczy „ewaluacja adnotacji”

Adnotacje typów są **normalnymi wyrażeniami Pythona**. Pytanie brzmi:

> **kiedy** te wyrażenia są wykonywane?

### Bez `__future__ import annotations`

➡ **w czasie definicji** funkcji / klasy

### Z `__future__ import annotations`

➡ **nigdy automatycznie** – są zapisywane jako stringi

---

## 2. Przykład bazowy – bez future importu

```python
class A:
    x: int
```

### Co robi interpreter

1. Interpreter wchodzi w definicję klasy
2. Widzi adnotację `int`
3. **natychmiast**:
   - rozwiązuje nazwę `int`
   - zapisuje ją jako obiekt `<class 'int'>`

Efekt:

```python
A.__annotations__ == {'x': <class 'int'>}
```

---

## 3. To samo z `from __future__ import annotations`

```python
from __future__ import annotations

class A:
    x: int
```

### Co robi interpreter

1. Interpreter **nie rozwiązuje `int`**
2. Zapisuje adnotację jako **string**

Efekt:

```python
A.__annotations__ == {'x': 'int'}
```

Nie ma:

- lookupu nazw
- importów
- wywołań
- zależności

---

## 4. Forward references – realny problem

### Bez future importu

```python
class User:
    manager: User
```

#### Co się dzieje

1. Interpreter czyta `manager: User`
2. Próbuje znaleźć `User`
3. `User` **jeszcze nie istnieje**
4. `NameError`

Jedyny sposób:

```python
class User:
    manager: "User"
```

---

### Z future importem

```python
from __future__ import annotations

class User:
    manager: User
```

#### Co się dzieje

1. `User` **nie jest rozwiązywany**
2. Zapis:

   ```python
   {'manager': 'User'}
   ```

3. Problem znika

---

## 5. Przypadek złożony: `Annotated`

### Kod

```python
password: Annotated[str, MinLen(8)]
```

### Bez future importu

Interpreter:

1. Rozwiązuje `Annotated`
2. Importuje `str`
3. Wywołuje `MinLen(8)`
4. Tworzy obiekt `MinLen`

To wszystko dzieje się:

- **przy imporcie modułu**
- nawet jeśli model nigdy nie zostanie użyty

Ryzyka:

- cykliczne importy
- koszt importu
- side-effecty w konstruktorach

---

### Z future importem

Interpreter:

```python
'Annotated[str, MinLen(8)]'
```

Nie ma:

- wywołań
- importów runtime
- zależności kolejności

Pydantic:

- sam decyduje **kiedy** i **jak** to sparsować

---

## 6. Wpływ na wydajność i import time

### Bez future importu

- adnotacje są **kodem wykonywalnym**
- każdy import:
  - tworzy obiekty
  - może inicjalizować klasy
  - może odpalić logikę bibliotek

### Z future importu

- adnotacje są **danymi**
- parsing jest:
  - leniwy
  - kontrolowany przez framework
  - cache’owalny

Dlatego:

- FastAPI
- Pydantic v2
- SQLAlchemy 2
wprost zalecają ten import

---

## 7. Gdzie następuje ewaluacja *z* future importem

Adnotacje **w końcu muszą być zrozumiane**. Ale:

- **nie przez interpreter**
- tylko przez:
  - `typing.get_type_hints`
  - framework (Pydantic, dataclasses, FastAPI)

Przykład:

```python
from typing import get_type_hints

get_type_hints(UserDataPydanticTypes)
```

Dopiero tu:

- string `"Annotated[str, MinLen(8)]"`
- jest parsowany
- w kontekście lokalnym i globalnym klasy

To jest **kontrolowana ewaluacja**.

---

## 8. Dlaczego to było future, a nie od razu standard

Zmiana:

- łamie introspekcję
- zmienia `__annotations__`
- wpływa na mypy / pylint / IDE

Dlatego:

- Python 3.7–3.10 → opt-in
- Python 3.11 → default

---

## 9. Podsumowanie w jednej tabeli

| Cecha | Bez future | Z future |
|-----|-----------|----------|
| Moment ewaluacji | przy definicji | leniwie |
| Typ adnotacji | obiekty | stringi |
| Forward references | problem | brak problemu |
| Import time | wolniejszy | szybszy |
| Cykliczne importy | możliwe | znacznie rzadsze |
| Kontrola | interpreter | framework |

---

## 10. Kiedy **nie** używać

Praktycznie nigdy w nowym kodzie.

Wyjątki:

- bardzo stary kod (<3.9)
- ręczna manipulacja `__annotations__` bez `get_type_hints`
- metaprogramowanie zależne od obiektów typów **w czasie importu**

---

Jeżeli chcesz, mogę:

- pokazać **dokładny bytecode** dla obu wersji
- rozpisać, jak Pydantic v2 parsuje stringowe adnotacje
- porównać to z Java annotations (bo mechanizm mentalnie jest podobny)

---

**User:**

nigdy nie używać w nowym kodzie? a w takim razie Pydantic v2 i przykład który został użyty na początku czyli "Annotated[str, MinLen(8), AfterValidator(_hash)]" nie wymaga obecności from **future** import annotations?

---

**Assistant:**

Masz rację — **tu trzeba to jednoznacznie sprostować**, bo w poprzedniej odpowiedzi padło zdanie, które bez kontekstu brzmi myląco.

### Krótka odpowiedź

**Nie, Pydantic v2 *nie wymaga* `from __future__ import annotations`.**  
**Tak, Pydantic v2 *zaleca* jego użycie (lub Pythona ≥ 3.11, gdzie to jest domyślne).**

A teraz precyzyjnie: **kiedy to działa, kiedy nie, i co dokładnie się stanie**.

---

## 1. Czy `Annotated[str, MinLen(8), AfterValidator(_hash)]` działa bez future importu?

### Tak, działa

```python
password_hash: Annotated[str, MinLen(8), AfterValidator(_hash)]
```

Bez `from __future__ import annotations`:

- `Annotated` zostanie **rozwiązane natychmiast**
- `MinLen(8)` zostanie **wywołane przy imporcie**
- `AfterValidator(_hash)` zostanie **wywołane przy imporcie**
- Pydantic dostanie **gotowe obiekty**

Pydantic v2 **to obsługuje bez problemu**.

---

## 2. Co się zmienia, gdy *dodasz* future import?

Z `from __future__ import annotations`:

```python
password_hash: "Annotated[str, MinLen(8), AfterValidator(_hash)]"
```

- interpreter **nic nie wywołuje**
- nic nie jest importowane „na twardo”
- Pydantic sam:
  - parsuje string
  - rozwiązuje symbole
  - buduje walidatory

Efekt końcowy w runtime:
➡ **identyczny model**, inna ścieżka dojścia.

---

## 3. Dlaczego więc Pydantic v2 *rekomenduje* future import?

Nie dlatego, że `Annotated` bez niego nie działa.

Powody są **systemowe**, nie funkcjonalne.

### 3.1 Forward references w modelach

```python
class Node(BaseModel):
    parent: Node | None
```

Bez future importu:

- ❌ `NameError`

Z future importem:

- ✅ działa
- bez `"Node"`

---

### 3.2 Modele rozproszone po modułach

```python
# a.py
class A(BaseModel):
    b: B

# b.py
class B(BaseModel):
    a: A
```

Bez future:

- bardzo łatwo o cykliczny import

Z future:

- adnotacje są stringami
- Pydantic rozwiązuje je później

---

### 3.3 Import time i cold start

W dużych projektach:

- setki modeli
- tysiące adnotacji

Bez future:

- wszystko się buduje przy imporcie

Z future:

- Pydantic:
  - cache’uje
  - rozwiązuje leniwie
  - robi to tylko raz

---

## 4. Kiedy **nie ma żadnej różnicy**

Jeżeli:

- Python ≥ 3.11
- brak forward references
- brak cyklicznych importów
- małe modele

➡ `from __future__ import annotations` **nic nie zmienia**, bo:

> Python 3.11 ma to zachowanie **domyślnie**

---

## 5. Dlaczego zdanie „praktycznie nigdy nie używać” było mylące

Poprawna wersja:

> **W nowym kodzie nie ma sensu *unikać* `from __future__ import annotations`.**

Albo jeszcze precyzyjniej:

- Python 3.11+ → **nie trzeba pisać**, bo już działa
- Python ≤ 3.10 → **warto pisać**, jeśli:
  - używasz Pydantic / FastAPI
  - masz modele wzajemnie zależne
  - używasz `Annotated`

---

## 6. Rekomendacja praktyczna (bez marketingu)

| Python | Rekomendacja |
|------|-------------|
| 3.11+ | nic nie rób |
| 3.10 | dodaj future import |
| 3.9  | dodaj future import |
| 3.8  | dodaj future import albo używaj stringów |

---

## 7. Najważniejsza konkluzja

- `Annotated[str, MinLen(8), AfterValidator(_hash)]`
  - **działa z i bez** `__future__ import annotations`
- future import:
  - **nie jest wymagany**
  - **nie zmienia semantyki walidacji**
  - **zmienia moment ewaluacji**
- Pydantic v2 jest zaprojektowany tak, aby:
  - działać poprawnie w obu trybach
  - ale **najlepiej skaluje się** z adnotacjami leniwymi

Jeżeli chcesz, mogę:

- pokazać dokładnie **co trafia do `__annotations__`** w obu wariantach
- rozrysować pipeline walidacji Pydantic v2 krok po kroku
- porównać to z mechanizmem adnotacji w Javie (JSR-380 vs runtime)
