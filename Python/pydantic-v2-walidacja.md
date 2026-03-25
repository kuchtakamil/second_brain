# Pydantic V2: Sposoby Walidacji Danych

W Pydantic V2 podejście do walidacji danych uległo sporym zmianom w porównaniu do wersji V1. Pod maską zmieniono silnik walidacyjny na napisany w języku Rust (biblioteka `pydantic-core`), co drastycznie poprawiło wydajność. Ponadto, API zostało unowocześnione i mocno zintegrowane z mechanizmem `Annotated` ze standardowej biblioteki `typing` Pythona.

Twierdzenie, że `Field` jest całkowicie przestarzałe, to pewne uproszczenie. Funkcja `Field` wciąż jest absolutnie kluczowa w Pydantic, jednak **zmienił się (i to bardzo) sposób, w jaki najlepiej jej używać**, a także **jak deklarować własne, niestandardowe funkcje walidujące**.

Poniżej znajdziesz szczegółowe omówienie ewolucji walidacji w Pydantic V2.

---

## 1. Walidacja za pomocą `Field` (Podejścia stare vs nowe)

`Field` to konstruktor metadanych służący do nakładania predefiniowanych ograniczeń na pola, ustawiania wartości domyślnych, aliasów czy opisów.

Pozwala na dodanie takich reguł, jak:

- Wartości minimalne/maksymalne dla liczb (`gt`, `ge`, `lt`, `le`)
- Minimalna/maksymalna długość znaków/elementów (`min_length`, `max_length`)
- Dopasowanie do wyrażenia regularnego (`pattern`)

### Sposób klasyczny (znany z V1)

Historycznie podawało się `Field` po prawej stronie znaku równości, traktując je niemal jak wartość domyślną.

```python
from pydantic import BaseModel, Field

class User(BaseModel):
    # Wiek musi być >= 18 i < 100
    age: int = Field(ge=18, lt=100)
    
    # Nazwa użytkownika musi mieć od 3 do 20 znaków
    username: str = Field(min_length=3, max_length=20, pattern=r"^[a-zA-Z0-9_]+$")
    
    # Wartość domyślna była podawana jako argument wewnątrz Field
    score: int = Field(default=0, ge=0)
```

**Dlaczego odchodzi się od tej składni?**

1. **Zły wpływ na systemy kontroli typów (MyPy/Pyright):** Analizatory statyczne często miały problem ze zrozumieniem przypisania wywołania funkcji `Field(...)` jako domyślnej wartości dla typu.
2. **Brak "Reużywalności":** Gdy walidacja "wiek od 18 do 100" pojawiała się w pięciu modelach, kod trzeba było kopiować.
3. **Mieszanie domyślnych wartości z walidacją:** Syntaktycznie zabierało to naturalne miejsce na przypisanie prostej wartości domyślnej (`k=v`).

### Sposób nowoczesny (Pydantic V2): Wykorzystanie `Annotated`

W Pydantic V2 **rekomendowanym standardem układania prostych reguł walidacyjnych** jest użycie `typing.Annotated` w połączeniu z `Field`.

`Annotated` pozwala na dołączenie dowolnych metadanych do typu, które nie wpływają bezpośrednio na właściwy typ działania zmiennej z perspektywy języka Python, ale Pydantic potrafi je odczytać.

```python
from typing import Annotated
from pydantic import BaseModel, Field

# 1. Tworzymy reużywalny typ w jednym miejscu!
AdultAge = Annotated[int, Field(ge=18, lt=100)]
Username = Annotated[str, Field(min_length=3, max_length=20, pattern=r"^[a-zA-Z0-9_]+$")]

class User(BaseModel):
    # Model staje się niesamowicie czysty i zwięzły
    age: AdultAge
    username: Username
    
    # Można też użyć bezpośrednio (jednorazowo), a wartość domyślna ląduje po prawej stronie!
    score: Annotated[float, Field(ge=0.0, le=10.0)] = 5.5 
```

---

## 2. Niestandardowa logika walidacji (Dekoratory)

`Field` rozwiązuje tylko proste, statyczne ograniczenia matematyczne/znakowe. Gdy weryfikacja danych wymaga **logiki w Pythonie** (np. podział po przecinku, wyciąganie po stringu, sprawdzenie w zewnętrznym API, operacje logiczne), stosujemy zaawansowane walidatory.

Tu zaszły duże zmiany koncepcyjne i nazewnicze. Dawne `@validator` i `@root_validator` zniknęły na rzecz nowych i znacznie bardziej czytelnych: `@field_validator` oraz `@model_validator`.

### A. Dekorator `@field_validator`

Służy do pisania skryptowej logiki walidującej konkretne, wskazane pole wewnątrz klasy modelu. Można zdefiniować tryb uruchomienia:

- **`mode='before'`** – uruchamia się *ZANIM* Pydantic w ogóle spróbuje upewnić się, czy wartość to oczekiwany typ. Idealne do luźnego, elastycznego parsowania wejścia.
- **`mode='after'`** (domyślnie) – uruchamia się *PO* walidacji z rdzenia Pydantica. Dostajemy gwarancję, że argument jest na 100% typem zdefiniowanym w adnotacji bocznej.

```python
from pydantic import BaseModel, field_validator
from typing import List

class Post(BaseModel):
    title: str
    tags: List[str]

    @field_validator('title')
    @classmethod
    def check_title_no_bad_words(cls, v: str) -> str:
        # Tryb domyślny (after), mamy już pewność że `v` to czysty string
        if 'spam' in v.lower():
            raise ValueError('Tytuł nie może zawierać słowa "spam"')
        return v.title()  # Przy okazji możemy ZMODYFIKOWAĆ wartość

    @field_validator('tags', mode='before')
    @classmethod
    def split_tags_if_string(cls, v):
        # Tryb before: wejściowa wartość jeszcze nie została zmieniona w listę.
        # Umożliwia nam to łatwą, manualną konwersję z pojedynczego Stringa!
        if isinstance(v, str):
            return [tag.strip() for tag in v.split(',')]
        return v
```

*(Uwaga: w V2 metody oznaczane dekoratorem w zasadzie powinny być metodami klasy `@classmethod` choć Pydantic potrafi inteligentnie poradzić sobie też z innymi podziałami).*

### B. Dekorator `@model_validator`

Zawsze, gdy musimy zbadać i zwalidować stan **całego obiektu na raz**, gdzie jedno pole zależy od drugiego. Najlepszy przykład to dwuetapowa rejestracja usera.

```python
from pydantic import BaseModel, model_validator

class UserRegistration(BaseModel):
    password: str
    password_confirm: str

    @model_validator(mode='after')
    def check_passwords_match(self) -> 'UserRegistration':
        # W trybie 'after' (dla modeli) `self` odnosi się już do stworzonego całego modelu
        if self.password != self.password_confirm:
            raise ValueError('Hasła nie polegają identycznie!')
        return self
```

---

## 3. Kompletna rewolucja w V2: Funkcyjne walidatory `Annotated`

Dlaczego wiele osób mówi, że "stare metody definiowania walidatorów w modelu to przeszłość"? Ze względu na wkraczające przebojem walidatory funkcyjne z rodziny `pydantic.functional_validators`.

Zamiast pisać metod wewnątrz `BaseModel` za pomocą dekoratorów, Pydantic V2 pozwala na wstrzykiwanie do typów w `Annotated` **zwykłych funkcji** używając metadanych `AfterValidator`, `BeforeValidator` czy `PlainValidator`.

**To podejście całkowicie deklasuje tworzenie metod klas (jak `@field_validator`) pod kątem reużywalności!**

### Różnice między `BeforeValidator`, `AfterValidator` i `PlainValidator`

Kluczowe w nowym mechanizmie jest **kiedy** Pydantic uruchomi Twoją funkcję względem swojego potężnego silnika wbudowanego (napisanego w Rust):

1. **`BeforeValidator(func)` – Zanim Pydantic cokolwiek sprawdzi**
   - **Moment uruchomienia:** Od razu na samym początku cyklu parsowania. Silnik Pydantica jeszcze nawet nie próbował rzutować danych na oczekiwany typ.
   - **Wejście dla funkcji:** Zupełnie surowe dane w postaci, w jakiej przyszły do obiektu (`Any`).
   - **Kiedy używać:** Zawsze wtedy, gdy wiesz, że przychodzące dane mogą mieć dziwny i niestandardowy format, a chcesz najpierw je "ostrugać" do poprawnego typu (np. wyciągnąć ze skomplikowanego słownika prosty string, usunąć śmieciowy przedrostek z identyfikatora ze starego API). Przygotowujesz tu dane tak, aby za chwilę Pydantic zrozumiał, z jakim typem ma do czynienia.

2. **`AfterValidator(func)` – Po upewnieniu się, że typ danych jest poprawny**
   - **Moment uruchomienia:** Najbardziej standardowy wariant. Uruchamia się po tym, jak główny silnik z powodzeniem odczyta i sparsuje odpowiednią zmienną.
   - **Wejście dla funkcji:** Gwarantowane poprawne dane w oczekiwanym typie. Jeśli w `Annotated` użyłeś typu `int`, to w tej funkcji gwarantowanie pracujesz już z Pythonowym integerem.
   - **Kiedy używać:** Do nakładania logiki biznesowej, z którą nie poradzi sobie proste `Field`. Przydaje się np. by zwalidować logikę "czy taki użytkownik dzisiaj stworzył już artykuł?", albo "czy dana liczba jest liczbą parzystą".

3. **`PlainValidator(func)` – Całkowite obejście Pydantica**
   - **Moment uruchomienia:** Tylko i wyłącznie ta funkcja zostanie wywołana. Całkowicie omijamy weryfikację rdzenia Pydantica.
   - **Wejście dla funkcji:** Dowolne dane bazowe (`Any`).
   - **Wyjście:** Musi zwracać w stu procentach gotowy, sfinalizowany obiekt docelowy.
   - **Kiedy używać:** Jeśli używasz dziwnych typów z obcych bibliotek (np. z dziwnych systemów czasu lub geometrii przestrzennej), których struktura parsująca zawarta wewnątrz Pydantic-core mogłaby nie zrozumieć lub na których by się po prostu wywaliła wyrzucając błędy o niewspartym formacie.

### Konwersja typów (Koercja) a Walidatory

Bardzo częstym pytaniem jest: **"Co się stanie, jeśli moje pole oczekuje `int`, przyjdzie string `"10"`, a ja mam włączony `AfterValidator`?"**.

Pydantic domyślnie działa w trybie **Zezwalającym na Konwersję (Koercję)** (tzw. *Lax mode*). Oznacza to, że silnik Rust zawsze będzie próbował być "pomocny" i zrzutuje oczywiste typy z jednego na drugi, *zanim* przekaże wynik dalej.

**Jak to wygląda w praktyce dla `AfterValidator`:**

1. Przychodzi string `"10"`.
2. Pydantic widzi, że pole oczekuje typu `int`.
3. Silnik pydantic-core (Rust) udanie parsuje `"10"` na Pythonowe `10` (integer).
4. Następnie to rzutowane `10` trafia do Twojej funkcji zdefiniowanej w `AfterValidator`. Twoja funkcja **nie zobaczy nigdy stringa `"10"`**, ponieważ otrzyma już wyczyszczonego i przekonwertowanego integera.

Z drugiej strony – jeśli w tym samym trybie przyjdzie `"10abc"`, Pydantic wyrzuci błąd `ValidationError` (bo nie da się tego w sposób jawny zrzutować na `int`), a Twój `AfterValidator` **w ogóle się nie uruchomi**. Twoja funkcja ma gwarancję uruchomienia się tylko, jeśli Pydantic pomyślnie zwaliduje i ewentualnie sprocesuje bazowy typ.

**Jak to wygląda w praktyce dla `BeforeValidator`:**
W `BeforeValidator` funkcja wykonuje się PRZED procesem opisanym wyżej.
Jeśli przyjdzie `"10abc"`, model przekaże do funkcji `"10abc"` – i to ona odpowiada teraz za wyczyszczenie tej wartości na np. int `10`. Dopiero potem wyczyszczone wynikowe `10` trafi do standardowego silnika (który uzna typ za poprawny).

#### Jak zablokować "pomocną" konwersję Pydantica? (Tryb Strict)

Jako programista masz pełną kontrolę nad tym mechanizmem. Jeśli **nie chcesz**, żeby Pydantic magicznie zmieniał `"10"` na `10` (ponieważ Twoje API musi być bezwzględnie poprawne i wymaga wejścia równego liczbie), włączasz **Tryb Strict**. Wtedy string `"10"` dla oczekiwanego `int` natychmiast wyrzuci błąd.

Możesz to zrobić na dwa sposoby:

1. **Globalnie dla całego modelu** we wbudowanej konfiguracji `ConfigDict`:

```python
from pydantic import BaseModel, ConfigDict

class User(BaseModel):
    model_config = ConfigDict(strict=True)
    age: int  # Próba wprowadzenia age="10" od razu zakończy się błędem
```

1. **Jako metadane (wymuszenie)** tylko dla konkretnego pola bezpośrednio z poziomu `Field` (dzięki temu jedno pole będzie super rygorystyczne, a pozostałe będą konwertowane):

```python
from typing import Annotated
from pydantic import BaseModel, Field

# Przekazanie StrictType zadziała dla tego jednego pola, ignorując domyślną zgodę na konwersję
StrictInt = Annotated[int, Field(strict=True)]

class Product(BaseModel):
    id: StrictInt     # Wymusza dokładne podanie inta: 10
    stock: int        # Zezwali na konwersję ze stringa: "10"
```

Poniżej typowy przykład z dominującym w pracy programisty `AfterValidator` (ponieważ najczęściej chcemy operować na już przygotowanym do pracy ciągłym typie):

```python
from typing import Annotated
from pydantic import BaseModel, AfterValidator

# 1. Definiujemy ZWYKŁĄ funkcję pracującą na konkretnym typie i zwracającą ten typ 
def normalize_and_check_phone(phone: str) -> str:
    phone = phone.replace(" ", "").replace("-", "")
    if not phone.startswith("+"):
        raise ValueError("Numer telefonu musi zaczynać się od + i posiadać prefiks kraju")
    if len(phone) < 10:
        raise ValueError("Numer telefonu jest za krótki")
    return phone

# 2. Rejestrujemy funkcję jako sprawdzacz dla danego typu w Annotated
PhoneNumber = Annotated[str, AfterValidator(normalize_and_check_phone)]

class ContactInfo(BaseModel):
    home_phone: PhoneNumber
    work_phone: PhoneNumber  # Zastosowaliśmy walidator dwukrotnie, bez pisania kodu klasy

class Company(BaseModel):
    # Możemy tego samego walidatora użyć w kompletnie niezwiązanym innym modelu i w innym pliku
    support_phone: PhoneNumber 
```

Tego podejścia nie dawało się zrealizować w Pydantic V1 łatwym domyślnym kodowaniem, przez co architektura i modele mocno zarastały po wielokroć powtarzanym kodem.

## Podsumowanie - Jaka jest "nowa droga (V2)"?

Zarówno `Field()` (ale przez `Annotated`!) jak i wbudowane walidatory mają stałe miejsce w Pydantic V2. Architektura projektów Pythona dąży jednak do poniższej ewolucji:

1. **Sztywne ograniczenia (min_length, znaki, itp)**:
   - Zastępujemy `pole: str = Field(...)` strukturą `pole: Annotated[str, Field(...)]` (często wydzielając do osobnego typu).
2. **Zaawansowana logika pojedynczego pola (np. regex to za mało)**:
   - Zastępujemy `@field_validator` we wpół-zrównanych modelach na rzecz budowania funkcji i pakowania ich w `Annotated[Typ, AfterValidator(func)]`. Tworzy to reużywalność niczym z definicji generycznych typów bazy danych. Dekorator zostawiamy tylko gdy logika tyczy się *wyłącznie* bardzo niszowego zachowania konkretnego modelu.
3. **Zależności pomiędzy wieloma kolumnami w modelu**:
   - Wykorzystujemy tylko `@model_validator(mode='after')`.
