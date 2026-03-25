# TypedDict w Pythonie - Kompendium Wiedzy

## Wprowadzenie: Co to jest `TypedDict`?

W klasycznym Pythonie słowniki (`dict`) są niezwykle elastyczną i powszechnie używaną strukturą danych. Niestety, ta elastyczność ma swoją cenę: ze względu na dynamiczne, niezbyt restrykcyjne typowanie standardowych słowników (zazwyczaj opisywane jako `Dict[str, Any]`), tracimy wsparcie dla podpowiedzi kodu ze strony IDE, a narzędzia do analizy statycznej (jak `mypy` czy `pyright`) nie mogą wyłapać pomyłek w nazwach kluczy lub typach przypisywanych do nich wartości.

Rozwiązaniem tego problemu jest **`TypedDict`**, wprowadzony w Pythonie 3.8 (w ramach dokumentu **PEP 589** - dodany do modułu `typing`). `TypedDict` to sposób użycia adnotacji typów do zadeklarowania słowników, które mają z góry zdefiniowany ('sztywny') zbiór kluczy typu ciąg znaków (`str`), a każdemu kluczowi przypisywany jest określony typ wartości.

**Kluczowa cecha:** `TypedDict` to mechanizm działający wyłącznie na poziomie **statycznego sprawdzania typów / linterów / IDE**. W czasie działania programu (w tzw. runtime) instancje struktury TypedDict są po prostu zwykłymi, wbudowanymi słownikami Pythona (`dict`). Podobnie jak inne elementy modułu `typing`, TypedDict **nie wykonuje absolutnie żadnej walidacji danych w czasie działania aplikacji**.

---

## Do czego służy?

1. **Typowanie danych wymiennych i payloadów JSON:** Najpopularniejszym zastosowaniem dla `TypedDict` jest operowanie danymi pochodzącymi z (lub wysyłanymi do) REST API. Takie obiekty w Pythonie deserializują się na słowniki o znanych, konkretnych kluczach. Zamiast używać `Dict[str, Any]` (co zataja strukturę ułatwiając popełnienie literówki kluczom), tworzymy jednoznaczny kontrakt strukturalny.
2. **Adnotacja starszego (legacy) kodu:** Praca ze starszymi systemami, w których wszechobecne było przesyłanie między funkcjami obszernych słowników o zróżnicowanej architekturze kluczy-wartości, jest niesamowicie trudna bez podpowiedzi typów. TypedDict stanowi pierwszy, całkowicie bezpieczny krok (bez jakiejkolwiek zmiany logiki runtime!) do poprawy jakości i czytelności starego kodu.
3. **Zastąpienie `**kwargs`:** Typowanie nienazwanych elastycznych argumentów przesyłanych w `**kwargs` jest zazwyczaj problematycznym tematem. Od Pythona 3.12 (PEP 692), `TypedDict` użyty wspólnie z adnotacją `Unpack` drastycznie ułatwia wprowadzanie silnie typowanych parametrów dla funkcji bez definiowania ich jeden po drugim.

---

## Detale techniczne i Sposoby użycia (Przykłady)

Z `TypedDict` można korzystać na dwa sposoby: definiując nową klasę dziedziczącą po `TypedDict` (tzw. styl deklaratywny, współcześnie preferowany) lub wywołując funkcyjny mechanizm `TypedDict(name, fields)`.

### 1. Podstawowe użycie (Składnia oparta na klasie - z PEP 589)

```python
from typing import TypedDict

class UserInfo(TypedDict):
    username: str
    age: int
    is_admin: bool

# ✅ Prawidłowe użycie
user: UserInfo = {"username": "Jan", "age": 30, "is_admin": False}

# ❌ Linter, mypy i IDE zgłosi błędy w poniższych przypadkach:
user_err1: UserInfo = {"username": 12, "age": 30, "is_admin": False}  # Błąd typu (12 zamiast stringa)
user_err2: UserInfo = {"username": "Anna", "age": 22}                 # Brak klucza "is_admin"
user_err3: UserInfo = {"username": "Ewa", "age": 25, "is_admin": True, "token": "xyz"} # Nadmiarowy klucz "token"
```

*Co otrzymujemy na poziomie kodu uruchomieniowego?* - Wyłącznie wywołanie `dict` oraz `dict["key"]`.

### 2. Słowniki z opcjonalnymi kluczami (`total=False` oraz nowsze `NotRequired` / `Required`)

W trybie domyślnym podawanie i istnienie wszystkich kluczy od razu jest wymagane. Są jednak sytuacje (np. endpointy PATCH API), w których obecność pewnych kluczy w zdefiniowanym słowniku może zachowywać się opcjonalnie.

**Historyczne podejście (Python 3.8+): Parametr `total=False` na klasie**

```python
from typing import TypedDict

class PartialUpdate(TypedDict, total=False):
    username: str
    age: int

# Możemy zapisać obiekt częściowy lub pusty. Nie zostaniemy tu zrugani za braki.
update1: PartialUpdate = {"age": 25}
update2: PartialUpdate = {}
```

Wada? Nie pozwalało to w prosty sposób ustalić, by z puli wielu pól *aż jedno* pozostało kategorycznie obowiązkowym do przekazania, podczas gdy reszta nie. Często skutkowało to tworzeniem wielu klas TypedDict rozszerzających jedna drugą by wyegzekwować logikę wymogów.

**Podejście klasyczne nowoczesne (Python 3.11+, PEP 655): Markery `NotRequired` i `Required`**

Używając atrybutów `NotRequired` możemy pojedyncze wpisy potraktować specjalnie względem domyślnie rygorystycznego formatu `total=True`.

```python
from typing import TypedDict, NotRequired, Required

class UpdateUserPayload(TypedDict):
    id: int                     # Dziedziczy total=True; obecność jest OBOWIĄZKOWA 
    username: NotRequired[str]  # Pole całkowicie opcjonalne 
    email: NotRequired[str]     # Pole całkowicie opcjonalne 

payload: UpdateUserPayload = {"id": 123} # To jest w pełni poprawna definicja
```

Alternatywnie przy klasie stworzonej parametryzacją na `total=False`, używamy flagi `Required`:

```python
class SearchParams(TypedDict, total=False):
    filter_by: str             # Opcjonalnie wejdzie bez bójek
    page: int                  # Tu tak samo
    query: Required[str]       # Te zapytanie musi być w słowniku bezwzględnie wylistowane!
```

### 3. Składnia oparta na wywołaniu funkcji

Składnia funkcyjna jest wykorzystywana w bardzo rygorystycznych lub patologicznych z punktu widzenia poprawności typowania przypadkach. Kiedy klucze słownika nie są zgodne z ograniczeniami nazywania zmiennych w Pythonie (np. nazwa klucza HTTP Header zawiera myślniki lub używa wyrazów zastrzeżonych jak "in").

```python
from typing import TypedDict

# Stringowa składnia chroni nas przed błędami kompilacji
HeadersDict = TypedDict('HeadersDict', {
    'Content-Type': str,
    'X-API-Key': str,
    'Accept': str,
    'in': str  # "in" nie może być definiowane konwencjonalnie w klasach. To keyword.
})

headers: HeadersDict = {
    'Content-Type': 'application/json',
    'X-API-Key': 'secret_xyz_123',
    'Accept': '*/*',
    'in': 'body'
}
```

### 4. Dziedziczenie z innych `TypedDict`

Python umożliwia na rozwijanie TypedDict z użyciem modelarności klasowej, dziedzicząc wspólne pola dla podklas. Wszystkie klucze z klas bazowych kumulują się.

```python
from typing import TypedDict

class BaseUser(TypedDict):
    name: str

class ExtendedUser(BaseUser):
    age: int

# ExtendedUser ma pole z Base i z siebie `name` oraz `age`.
user: ExtendedUser = {"name": "Bartek", "age": 34}
```

*Uwaga:* Dziedziczenie z parametru `total=False` w klasie wyższej *nie propaguje się* do klas dziedziczących. Rozbudowany typ trzeba adnotować przez podanie własnego `total=False` – w przeciwnym razie wszystkie nowe zdefiniowane pola w podklasie stają się obligatoryjnymi wymaganiami, niezależnie jak zdefiniowała zasady baza w swojej puli z kluczami.

---

## Wątki poboczne, Nowości i Porównanie z rozwiązaniami obok

### Nowości: Rozpakowywanie TypedDict do Typowania `**kwargs` – Mniej kodu a więcej profitu (Python 3.12+, PEP 692)

W erze Pythona >= 3.12 dodano oficjalnie do słownika funkcjonalności systemowej marker `Unpack` z modułu `typing`. Rozwiązuje to zjawisko, nazywane w społeczności Pythona „Type-blackhole dla Kwargs”, gdzie podawaliśmy np. w docstringu opcje `**kwargs`, zmuszając developerów domyślać się na ślepo struktury przesyłu.

Uruchomienie `Unpack` rozwiązuje ból w trymiga:

```python
from typing import Unpack, TypedDict, NotRequired

class RequestOptions(TypedDict):
    timeout: NotRequired[int]
    verify_ssl: NotRequired[bool]

def make_request(url: str, **kwargs: Unpack[RequestOptions]) -> dict:
    # Wewnątrz funkcji zmienna 'kwargs' w magiczny sposób zidentyfikuje się jako 
    # instancja TypedDict z poprawną statycznie adnotowaną podbudową 'RequestOptions'.
    
    timeout = kwargs.get('timeout', 30) # IDE podpowie dostępne opcje dla kwargs ze struktury
    verify = kwargs.get('verify_ssl', True)
    
    return {"status": "ok", "url": url}

# Dobre wywołanie (IDE wie co jest wspierane jako keyword argumenty)
make_request("https://api.test", timeout=15)

# Błędne wywołanie – Linter odrzuci kompilację i krzyknie: "Parametr 'retries' jako **kwargs unassigned":
make_request("https://api.test", retries=3) 
```

### Wykorzystanie `Annotated` i `TypedDict` (np. w LangGraph z `add_messages`)

Często w nowoczesnych frameworkach (takich jak **LangGraph**, **FastAPI** czy **Pydantic**) można spotkać połączenie `TypedDict` z atrybutem `Annotated` z modułu `typing`. Świetnym przykładem jest Twój fragment kodu:

```python
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages  # Przykładowy import

class State(TypedDict):
    messages: Annotated[list, add_messages]
```

**Wyjaśnienie, o co w tym chodzi:**

1. **`TypedDict` definiuje bazową strukturę**: Wymusza, by pod kluczem `"messages"` znajdowała się jakaś wartość.
2. **`Annotated` podrzuca dodatkowe metadane**: Konstrukcja `Annotated[Typ, Metadane]` mówi linterom i IDE (np. `mypy`, PyCharm, VSCode): *"Traktuj ten obiekt po prostu jako standardowy `Typ` (w tym wypadku: `list`). Zignoruj to, co jest dalej!"*. Dlatego dla analizatorów kodu `messages` to nadal najzwyklejsza lista.
3. **Moc w czasie wykonania (runtime)**: To "coś, co jest dalej" (czyli funkcja `add_messages`) staje się niezwykle użytecznym tagiem dla samego frameworka, który może odczytać te informacje w trakcie działania programu poprzez `typing.get_type_hints(State, include_extras=True)`.

**Dlaczego jest to kluczowe w LangGraph?**
W architekturze LangGraph stan (często właśnie klasa `State`) jest przekazywany od węzła do węzła w postaci słownika. Standardowo podczas aktualizacji wartości w słowniku w Pythonie, dochodzi do całkowitego **nadpisania** (`state["messages"] = nowe_wiadomosci`).
Zastosowanie znacznika `add_messages` (tzw. *"reducer"*) zmienia ten proces: The framework widzi, że klucz ten ma "doczepioną" operację `add_messages`, więc zamiast zastępować historię wiadomości, automatycznie używa tej funkcji do doklejenia / złączenia (zestawienia) starych i nowych wiadomości ze sobą.

Dzięki temu rozwiązaniu otrzymujemy jednocześnie świetne autouzupełnianie w IDE udające zwykłą strukturę danych i ukryte, eleganckie polecenie dla zewnętrznego frameworka, jak ma reagować na nowe aktualizacje stanu.

### Podejrzewanie Pydantica a bytem klas 'Dataclass' - Kiedy uczyć i wykorzystywać jakie narzędzie do wymiany logiki bazowej?

Często padają pytania ze standardu „Dlaczego TypedDict a nie Dataclass lub sprawdzony Pydantic?”. Na podparciu solidnych wskaźników zaimplementujmy perspektywę decyzyjną:

| Cecha rozwiązania | `TypedDict` | Wbudowana z biblioteki `dataclass` | `Pydantic` (`BaseModel`) |
| :--- | :--- | :--- | :--- |
| **Prawdziwy Typ w Runtime** | Przewidywalny i szybki natywny C-bazowy `dict` Pythona. | Rozbudowana i spreparowana `class()` będąca obiektem. Posiada obiektywne ślady logiki. | Niesamowicie potężna pełnoprawna struktura klasowa, trzyma skomplikowane systemy meta-schematów. |
| **Koszt Inicjalizacji (Wydajność)** | Zbliżony do wahania granicy zera, czyli wprost "tylko odczyty i przypisania w rzucający do kluczy RAMie jako najzwyklejszy słownik" - Najlepszy na liście. | Narzut ze względu procesów przypisywania typów metod np. **hash**. Umiarkowany na wydajności. | Najmniejsza wydajność podczas inicjalizacji struktury, największe wymagania. Musi zbudować logikę modelu. |
| **Walidacja Danych na Żywo! (Runtime) - czy sprawdzi przy wejściu typ 12 vs '12'?** | Brak. ⚠️ Rzuci do wnętrza co popadnie. Jest ślepe. | Brak. | **TAK – SILNIE WYMIUSZA.** Odrzuci pozycję w runtime bądź zdeserializuje do prawidłowego typu. Wspaniale rzuca ValidationError'ami z pełnymi raportami objaśnień wad wprowadzonych danych. |
| **IDE Autocomplete / Mypy / Pyright** | Tak | Tak | Tak |
| **Możliwość definowania i obsługi własnych metod funkcji (Custom Behavior)** | **Nie** (to tylko notacja wspierająca goły słownik 'dict') | **Tak** | **Tak** |

**Reguły Kciuka:**

1. **Pydantica** Używaj ZAWSZE kiedy ładunku danego nie ufasz (Dane wejściowe pochodzące z wejść API, Web-formularze użytkowników, konfiguracje z plików JSON, parsu danych z bazy/serwisu). Pydantic jest Twoim ubezpieczycielem przed korupcją procesora danych w głębi aplikacji.
2. **Dataclass** Używaj jako pojemnika na węższą architekturę wymiany sygnału pomiędzy zaufaną wewnętrzną logiką kiedy ten kontener potrzebuje funkcje zachowawcze (np properties / metody konwertujące formę po zbudowaniu).
3. **TypedDict** Używaj wtedy gdy potrzebujesz absolutnej **prędkiej elastyczności standardowego słownika `dict`**. Tam, gdzie po deserializacji nie używasz już walidacji bo "i tak działa szybko" albo rzutujesz na zewnętrzne skrypty co pragną klasycznych systemowych obiektów (zwrotki do Jsonów pod REST frameworki co robią dump, silniki bazy przyjmujące mapping pod kwargs logiki).

### Czego ABSOLUTNIE NIE robić z TypedDict: Pomyłka z `isinstance()` na żywym obiekcie

Najczęstszy, katastroficzny błąd początkujących to zapomnienie faktu, że `TypedDict` "kompilacyjnie znika" pod maską wyegzekwowanego Pythona z konsoli z włączoną instrukcją działania, tak więc sprawdzenie logiki nie zadziała naturalne. Spójrzmy na typowy fail z testowań instancji:

```python
from typing import TypedDict

class MyData(TypedDict):
    a: int

data_sample = {"a": 1}

# BŁĄD O POZIOMIE TYPE ERROR NA ŚRODOWISKU ПРОДУКCYJNYM! 
# Zniszczy aplikację w runtime z następującym powodem: "TypeError: TypedDict does not support instance and class checks"
if isinstance(data_sample, MyData): 
    pass 
```

Jeśli musisz wykonać typ-checking operujący sprawdzaniem poszczególnych kluczy słownika celem zagwarantowania wymogów - skorzystaj z manualnych mechanizmów jak adnotowane procedury wyznaczające prawdy modułowe pod Mypy a mianowicie procedur `TypeGuard` - pisząc ręczny checker iterujący po kluczach na istnienie odpowiednich atrybutów dla słownika bez użycia isinstance do nazwy podmiotu TypDictu - lub przesiądź się definitywnie na Pydantic.

## Podsumowanie i słowo końcowe

Typ `TypedDict` wprowadzony przez mechanizmy PEP i Typing stanowi swoiste "odkrycie skarbu" dla inżynierów operujących na dużej liczbie złożonych słowników gdzie klasowe schematy w stylu `dataclasses` stanowią rażący *over-engineering* z uwagi na wysokie paradygmaty strukturowe niepasujące do prostej natury operowania parą `KLUCZ : WARTOŚĆ` - natomiast puste opieranie się na naiwnym `dict`, grozi destrukcyjnymi błędami `KeyError` na każdy niesamowity błąd pomyłkowy jak literówki – a ponadto w konsekwencji zabija możliwości wykorzystywania narzędzi wsparcia IDE w postaci auto-complete. Razem z unikalnymi konstruktami takimi jak markery **Required**, **NotRequired** i współczesnym dekompresowaniem flag pod adnotacje elastycznych wejść `kwargs` o nazwie **Unpack**, stał i na pewno wciąż się staje jednym z kluczowych form i formatorów bezpiecznego, szybkiego, czytelnego kodu bazującego silnie na klasycznym słowniku języka Python.
