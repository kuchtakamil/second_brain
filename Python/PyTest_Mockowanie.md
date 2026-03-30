# Mockowanie i Monkeypatching w PyTest

Poniższy dokument systematyzuje wiedzę na temat różnych sposobów mockowania w testach z wykorzystaniem frameworka PyTest. Metody zostały podzielone ze względu na ich logikę i zastosowanie. Oznaczono również ich aktualny status, czyli to, czy dane podejście jest nowoczesne i rekomendowane, czy też powoli odchodzi do lamusa.

## 1. Mockowanie Zewnętrznych Zapytań Sieciowych (HTTP)

Gdy nasz kod komunikuje się ze światem zewnętrznym (np. zewnętrzne API), nie chcemy w testach wykonywać prawdziwych zapytań (by uniezależnić test od awarii w sieci lub uniknąć opłat). Wymaga to odpowiedniego kontrolowania bibliotek klienckich (jak `requests` czy asynchroniczny `httpx`).

### Ręczne mockowanie z wbudowanym `monkeypatch`

- **Status:** 🟡 **Odradzane / Przestarzałe** (tylko w kontekście zapytań HTTP)
- **Opis:** Wbudowany w PyTest fixture `monkeypatch` pozwala na dynamiczną podmianę atrybutów. Jest genialny do modyfikacji zmiennych środowiskowych, jednak do podmiany zapytań HTTP brakuje mu elegancji. Wymaga on rzeźbienia sztucznych klas, które udają obiekty odpowiedzi (wyposażonych w metody wywoływane przez kod produkcyjny jak np. `.json()`), co prowadzi do mocno nadmiarowego i zanieczyszczonego kodu (tzw. "boilerplate").

```python
import requests

def get_weather(city: str) -> dict:
    response = requests.get(f"https://api.weather.com/{city}")
    return response.json()

def test_get_weather_mocked(monkeypatch):
    class MockResponse:
        def json(self):
            return {"temp": 20}

    # Patching requests.get with a lambda returning our MockResponse instance
    monkeypatch.setattr(requests, "get", lambda _: MockResponse())
    
    result = get_weather("Warsaw")
    assert result["temp"] == 20
```

### Dedykowane biblioteki do HTTP synchronicznego (`responses` / `requests-mock`)

- **Status:** 🟢 **Aktualny standard** (dla biblioteki `requests`)
- **Opis:** W przypadku korzystania ze standardowej biblioteki `requests`, w profesjonalnych projektach stosuje się sprawdzone dedykowane narzędzia. "Przechwytują" one zapytania bezpośrednio ze sprzęgU testującego bez potrzeby ręcznego ucinania metod za pomocą `monkeypatch`. Znacznie zwiększa to czytelność kodu.

```python
import requests
import responses

@responses.activate
def test_get_weather_with_responses():
    # Define how the HTTP mock should answer for a specific URL
    responses.add(
        responses.GET,
        "https://api.weather.com/Warsaw",
        json={"temp": 20},
        status=200
    )
    
    # Executing our code - library intercepts the request under the hood
    response = requests.get("https://api.weather.com/Warsaw")
    assert response.json()["temp"] == 20
```

### Dedykowane biblioteki do HTTP asynchronicznego (`respx` / `pytest-httpx`)

- **Status:** 🟢 **Nowoczesny standard** (dla klienta `httpx`)
- **Opis:** Pracując dziś w nowoczesnych frameworkach opartych o `async`/`await` (np. FastAPI), powszechnie zrównano do klienta `httpx` zamiast klasycznego `requests`. Do tego potężnego, współbieżnego połączenia dedykuje są specjalne biblioteki asynchroniczne symulujące ruch, z których najpopularniejsze to `respx` oraz `pytest-httpx`.

---

## 2. Mockowanie Własnych Modułów i Zależności

Drugą grupą testowania jest izolowanie sprawdzanych mechanizmów wewnątrz własnej architektury projektu. Przykładowo, badając moduł sprawdzający zamówienie, pragniemy odciąć go od wysyłania komend do bazy danych lub własnego serwisu wysyłającego e-maile.

### Fixture `mocker` (wtyczka `pytest-mock`)

- **Status:** 🟢 **Nowoczesny standard** (zdecydowanie preferowane)
- **Opis:** Zewnętrzna wtyczka ułatwiająca życie (`pytest-mock`), która jest tak powszechna, że traktowana jak kanon. Wrzuca ona w scope testów prosty fixture `mocker`, łączący się bezpośrednio z logiką Pythonowego `unittest.mock`. To tzw. mechanizm bezstanowy, co w prostych słowach oznacza, że rewelacyjnie likwiduje problem ogromu napuchających dekoratorów nad głowicami argumentów w sygnaturze samej funkcji (`def test_...()`).

> **Złota zasada mockowania (Where to patch):** Podmieniaj dany obiekt w przestrzeni nazw tego modułu, gdzie jest on _aktywnie eksploatowany i zaimportowany_ ("miejsce użytku"), absolutnie nie celując w plik macierzysty, w którym znajduje się jego oryginalna definicja.

**Kod produkcyjny (`payment_gateway.py`):**

```python
# payment_gateway.py  –  zewnętrzny moduł z prawdziwymi implementacjami

def check_fraud_risk(user_id: int) -> bool:
    # w rzeczywistości: zapytanie do zewnętrznego serwisu antyfraudowego
    ...

def process_payment(amount: float) -> bool:
    # w rzeczywistości: komunikacja z bramką płatności
    ...
```

**Kod produkcyjny (`order_service.py`):**

```python
# order_service.py  –  importuje funkcje z payment_gateway
# Python tworzy LOKALNE referencje: order_service.check_fraud_risk, order_service.process_payment
from payment_gateway import process_payment, check_fraud_risk

def place_order(user_id: int, item_name: str, price: float) -> str:
    if check_fraud_risk(user_id):            # ← szuka nazwy w SWOJEJ przestrzeni nazw
        return "Order blocked due to fraud risk."
    process_payment(price)                   # ← j.w.
    return f"Order for {item_name} placed successfully."
```

**Testy (`test_order_service.py`):**

```python
def test_place_order_success(mocker):
    # Patching AT THE USAGE SITE (within the order_service domain scope)
    mocked_fraud = mocker.patch("order_service.check_fraud_risk", return_value=False)
    mocked_payment = mocker.patch("order_service.process_payment", return_value=True)
    
    result = place_order(user_id=123, item_name="Laptop", price=5000.0)
    
    assert result == "Order for Laptop placed successfully."
    
    # Asserting if the patched objects were called with proper arguments
    mocked_fraud.assert_called_once_with(123)
    mocked_payment.assert_called_once_with(5000.0)

def test_place_order_blocked_by_fraud(mocker):
    # Simulating elevated user risk behavior
    mocked_fraud = mocker.patch("order_service.check_fraud_risk", return_value=True)
    mocked_payment = mocker.patch("order_service.process_payment")
    
    result = place_order(user_id=999, item_name="Phone", price=2000.0)
    
    assert result == "Order blocked due to fraud risk."
    mocked_fraud.assert_called_once_with(999)
    # Checking implementation safety cut-off - payment method MUST NOT execute!
    mocked_payment.assert_not_called()
```

#### 🔍 Jak mock trafia do testowanej funkcji bez przekazywania go jako argument?

To sedno mechanizmu `patch`. Gdy Python ładuje `order_service.py`, tworzy w jego wewnętrznej przestrzeni nazw (`order_service.__dict__`) wpisy:

```text
order_service.check_fraud_risk  → <prawdziwa funkcja z payment_gateway>
order_service.process_payment   → <prawdziwa funkcja z payment_gateway>
```

`mocker.patch("order_service.check_fraud_risk", ...)` **nadpisuje ten wpis** obiektem `MagicMock`. Od tej chwili pod kluczem `check_fraud_risk` w słowniku modułu siedzi mock, a nie oryginał.

Gdy `place_order()` wykonuje wewnętrznie `check_fraud_risk(user_id)`, Python szuka tej nazwy **we własnej przestrzeni nazw modułu `order_service`** — a tam już siedzi podmieniony mock. Funkcja ani nie wie, ani nie musi wiedzieć, że coś zostało podmienione.

Zmienne `mocked_fraud` i `mocked_payment` to jedynie **uchwyty** do tych samych obiektów `MagicMock`, które siedzą w `order_service.__dict__`. Nie przekazujesz ich do `place_order` — ona **już na nie trafia**, szukając funkcji po nazwie.

```text
mocker.patch(...)  →  nadpisuje wpis w order_service.__dict__
place_order()      →  szuka check_fraud_risk w order_service.__dict__  →  trafia na mock
mocked_fraud       →  uchwyt do tego samego obiektu  →  służy do asercji
```

> **Analogia:** `order_service` to biuro z książką telefoniczną. `mocker.patch` podmienia numer pod hasłem `check_fraud_risk`. Gdy biuro zadzwoni pod tę nazwę, trafi na aktora (mock) — nie na oryginalny dział. Aktor odgrywa rolę (`return_value=False`), a ty sprawdzasz czy i jak biuro dzwoniło (`assert_called_once_with`).

#### 💡 Alternatywa: Dependency Injection — przekazywanie zależności jako argumentów

Tak, taka reguła istnieje i ma swoją nazwę: **Dependency Injection (DI)**. Polega na tym, że zamiast importować zależności na sztywno wewnątrz funkcji/klasy, przekazujesz je z zewnątrz jako argumenty. Dzięki temu w teście możesz podać mocka bezpośrednio — bez żadnego `patch`.

**Ten sam przykład przepisany z DI:**

```python
# order_service.py — zależności wstrzykiwane jako argumenty
def place_order(
    user_id: int,
    item_name: str,
    price: float,
    fraud_checker=check_fraud_risk,   # domyślnie prawdziwa funkcja
    payment_processor=process_payment,
) -> str:
    if fraud_checker(user_id):
        return "Order blocked due to fraud risk."
    payment_processor(price)
    return f"Order for {item_name} placed successfully."
```

**Test bez `patch` — mock przekazany wprost:**

```python
from unittest.mock import MagicMock

def test_place_order_success_di():
    mock_fraud    = MagicMock(return_value=False)
    mock_payment  = MagicMock(return_value=True)

    result = place_order(
        user_id=123,
        item_name="Laptop",
        price=5000.0,
        fraud_checker=mock_fraud,
        payment_processor=mock_payment,
    )

    assert result == "Order for Laptop placed successfully."
    mock_fraud.assert_called_once_with(123)
    mock_payment.assert_called_once_with(5000.0)
```

**Kiedy stosować które podejście?**

| Kryterium | `patch()` | Dependency Injection |
| --- | --- | --- |
| Istniejący kod bez DI | ✅ działa bez zmian | ❌ wymaga refactoru |
| Czytelność testu | 🟡 mock "pojawia się magicznie" | ✅ mock widoczny wprost w wywołaniu |
| Izolacja w klasach/serwisach | 🟡 trzeba znać ścieżkę do patcha | ✅ czytelne przez konstruktor |
| Frameworki (FastAPI, Django) | ✅ powszechne i wygodne | ✅ faworyzowane w architekturze DDD |

> **Wnioski:** W Pythonie **obie strategie koegzystują**. `patch()` dominuje w projektach, które nie zostały zaprojektowane z myślą o DI (legacowy kod, zewnętrzne biblioteki). DI jest preferowane w nowej, dobrze zaprojektowanej architekturze (szczególnie w OOP z serwisami/repozytoriami), bo sprawia, że zależności są **jawne i łatwe do podmiany** bez znajomości wewnętrznych ścieżek importów.

---

### Dekorator `@patch` (`unittest.mock`)

- **Status:** 🟡 **Starsze podejście** (mocno zakorzenione, acz kłopotliwe)
- **Opis:** Rodzime rozwiązanie pochodzące z rdzenia samego języka Pythona. Działa na zasadzie przyrządzania zestawu tzw. dekoratorów ustawionych piętrowo nad funkcją i podpinających obiekty atrap bezpośrednio do wejściowych atrybutów samej funkcji. Ma ewidentne wady – generuje "Piekło dekoratorów", zaś pomyłka w kolejności przypisywania symulantów (lecących strumieniowo "od góry do dołu" ale rzutowanych finalnie od najbliższego w dół w sygnaturze "od dołu do góry parametrycznie") jest nagminnym powodem bezgłośnych anomalii, a w następstwie – fałszywych wniosków o pomyślnych wdrożeniach.

```python
from unittest.mock import patch
from order_service import place_order

# Defining @patch decorators (indicating by string path what we intercept)
@patch("order_service.process_payment")
@patch("order_service.check_fraud_risk")
def test_place_order_with_patch_decorator(mock_check_fraud_risk, mock_process_payment):
    # BEWARE OF PARAMETER ORDER! 
    # Objects are chained from "bottom to top" (counting up from the 'def' core definition).
    # Being so, the closest bottom patch maps directly to the first left function parameter!
    
    mock_check_fraud_risk.return_value = False
    mock_process_payment.return_value = True
    
    result = place_order(user_id=123, item_name="Laptop", price=5000.0)
    
    assert result == "Order for Laptop placed successfully."
    
    mock_check_fraud_risk.assert_called_once_with(123)
    mock_process_payment.assert_called_once_with(5000.0)
```

---

## 3. Zaawansowane Mockowanie Protokołów Pythona (`MagicMock`)

Istnieją struktury głęboko zakorzenione w rdzeniu gramatyki i składni Pythona, charakteryzujące się wykorzystaniem ukrytych tzw. metod magicznych (dunder methods – np. `__len__`, `__iter__`, `__enter__`). W ich przypadku "surowy" mock standardowy okaże się bezradny i zawiesi działanie kodu.

### Klasa `MagicMock` (`unittest.mock`)

- **Status:** 🟢 **Aktualnie używane / Niezbędne i wiodące**
- **Opis:** Niesamowicie potężna, ewolucyjna podklasa klasycznego `Mock`-a. Jej olbrzymią przewagą jest wdrożona z góry wstępna konfiguracja metod dunder, pozwalająca m.in. na bezpieczne ujęcie jej po instrukcjach iteracji (samo użycie klauzuli `for`), czy ujęcie jej instrukcji w polecenie `with`.
- **Uwaga:** Należy w tym miejscu jasno zaznaczyć, że metody uproszczone wymienione w poprzednich akapitach (zarówno natywny `@patch` jak i genialny `mocker.patch()`) używają właśnie implementacji bazujących na instancji `MagicMock` "pod maską", jako wariantu domyślnego, w głównej mierze ze względu na chęć maksymalnego zmniejszenia ryzyka bezlitosnych błędów typu `TypeError`.

#### Przykład A: Mockowanie menedżera kontekstu (polecenie `with`)

Menedżer kontekstu obudowany wokół otwarcia np. zasobu zapisu pliku operuje na metodach `__enter__` i `__exit__`. Blok czerpie wartość po stronie przypisania (`as f`) w oparciu o obiekt zwracany z metody operacyjnej wejścia (`__enter__`).

```python
from unittest.mock import MagicMock

def read_first_line(file_path: str) -> str:
    with open(file_path, "r") as f:
        return f.readline()

def test_read_first_line(mocker):
    # Initialize a MagicMock to explicitly rig its context-sharing capabilities
    mock_file = MagicMock()
    
    # 'with' acts over whatever stands under __enter__'s evaluated result
    mock_file.__enter__.return_value.readline.return_value = "Mocked first line"
    
    # Finally, override the standard 'builtins.open' global 
    mocker.patch("builtins.open", return_value=mock_file)
    
    result = read_first_line("dummy.txt")
    assert result == "Mocked first line"
```

*(W praktycznym programowaniu posługujemy się dla uproszczenia obiektem klasy pomocniczej `mock_open()`, niemniej ten przykład dogłębnie klaruje rzeczywisty fundament obsługi interfejsów pod skapami instrukcji `with`.)_

#### Przykład B: Mockowanie pojęcia długości iteracyjnej obiektu

Instrukcja zrzutu iteracyjnego (np. wymuszona pętla `for...in`) opiera funkcjonowanie rdzenia nadpisywania o wywołanie metody `__iter__`, tudzież zapytanie weryfikujące `len()` budzi sygnał z gałęzi `__len__`. Surowy mock rzuciłby w takim incydencie wyjątkowy blokujący błąd wykonania.

```python
from unittest.mock import MagicMock

def process_items(container) -> list:
    # Triggering the length operator evaluates __len__ underneath
    if len(container) == 0:
        return ["Empty structure"]
        
    results = []
    # Activating loop implicitly summons the __iter__ yielding
    for item in container:
        results.append(item * 2)
    return results

def test_process_items_with_magicmock():
    mock_container = MagicMock()
    
    # Manual overriding of protocols
    mock_container.__len__.return_value = 3
    mock_container.__iter__.return_value = iter([10, 20, 30])
    
    result = process_items(mock_container)
    
    # Logic validates correctly simulating actual physical built-in sets length
    assert result == [20, 40, 60]
```

---

## Mockowanie - cheatsheet – `unittest.mock` + `pytest-mock`

```bash
pip install pytest-mock   # dostarcza fixture `mocker` (opakowuje unittest.mock)
```

---

### 🔧 MagicMock – tworzenie i konfiguracja mocka

> Biblioteka: `unittest.mock` (wbudowana w Python 3.3+)

```python
from unittest.mock import MagicMock, call

# MagicMock automatycznie tworzy atrybuty i metody "na żądanie" –
# odpowie na każde wywołanie bez rzucania AttributeError
mock = MagicMock()

# Wywołanie dowolnej metody – mock ją "zapamiętuje"
mock.method(1, 2)

# Sprawdzenie czy metoda była wywołana dokładnie raz z podanymi argumentami
mock.method.assert_called_once_with(1, 2)

# Ile razy metoda była wywołana
mock.method.call_count          # → 1

# Ustawiamy co mock ma zwrócić gdy metoda zostanie wywołana
mock.method.return_value = 42

# Można też ustawić zwracaną wartość od razu przy tworzeniu
mock_with_value = MagicMock(return_value="hello")

# Zwracanie różnych wartości przy kolejnych wywołaniach (side_effect jako lista)
mock.method.side_effect = [10, 20, 30]
mock.method()  # → 10
mock.method()  # → 20

# Atrybut zagnieżdżony – mock też go wygeneruje automatycznie
mock.config.database.host = "localhost"
```

---

### 🔧 patch – podmiana obiektu na czas testu

> Biblioteka: `unittest.mock` (wbudowana w Python 3.3+)

```python
from unittest.mock import patch, MagicMock

# --- Wariant 1: jako dekorator nad funkcją testową ---
# Podmienia "requests.get" w przestrzeni nazw modułu "mymodule"
# na czas trwania tego testu; po zakończeniu przywraca oryginał
@patch("mymodule.requests.get")
def test_api(mock_get):
    # mock_get to MagicMock przekazany automatycznie jako argument funkcji
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"ok": True}
    # ... tu wywołujemy kod produkcyjny, który wewnętrznie używa requests.get

# --- Wariant 2: jako context manager (with) ---
# Patch jest aktywny tylko wewnątrz bloku with
def test_open():
    with patch("builtins.open", MagicMock(return_value=...)) as mock_open:
        # wewnątrz bloku open() jest podmieniony
        pass
    # tutaj open() działa już normalnie
```

---

### 🔧 mocker – czystszy styl bez dekoratorów (zalecane)

> Biblioteka: `pytest-mock` (zewnętrzna: `pip install pytest-mock`)

```python
# mocker to fixture z pytest-mock; używamy go jako argument funkcji testowej
# Patch jest automatycznie cofany po zakończeniu testu – brak potrzeby cleanup

def test_service(mocker):
    # patch() działa identycznie jak unittest.mock.patch, ale czystej
    mock_db = mocker.patch("myapp.db.get_user")

    # Ustawiamy co ma zwrócić podmieniona funkcja
    mock_db.return_value = {"id": 1, "name": "Alice"}

    # Wywołujemy testowaną funkcję (która wewnętrznie woła db.get_user)
    result = get_user_name(1)

    assert result == "Alice"
    # Weryfikujemy że funkcja była wywołana z właściwym argumentem
    mock_db.assert_called_once_with(1)
```

---

### 🔧 side_effect – wyjątki, sekwencje i własna logika

> Biblioteka: `unittest.mock` (wbudowana) lub przez `mocker` z `pytest-mock`

```python
from unittest.mock import MagicMock

mock = MagicMock()

# Wariant A: mock rzuca wyjątek przy każdym wywołaniu
# Przydatne do testowania obsługi błędów (try/except w kodzie produkcyjnym)
mock.side_effect = ValueError("boom")

# Wariant B: mock zwraca kolejne wartości z listy (wyczerpuje się po 3 wywołaniach)
# Przydatne gdy testujemy pętle lub retry logic
mock.side_effect = [1, 2, 3]

# Wariant C: własna funkcja – mock zachowuje się jak prawdziwa funkcja
# Przydatne gdy logika odpowiedzi zależy od argumentów
mock.side_effect = lambda x: x * 2

# --- side_effect z mocker (pytest-mock) ---
def test_retry_logic(mocker):
    mock_fetch = mocker.patch("myapp.client.fetch")
    # Pierwsze dwa wywołania rzucają wyjątek, trzecie zwraca wartość
    mock_fetch.side_effect = [ConnectionError(), ConnectionError(), {"data": "ok"}]
```

---

### 🔧 spy – śledzenie prawdziwego obiektu bez podmiany

> Biblioteka: `pytest-mock` (zewnętrzna: `pip install pytest-mock`)

```python
# spy NIE podmienia metody – pozwala jej działać normalnie,
# ale jednocześnie nagrywa każde wywołanie (argumenty, wynik)
# Przydatne gdy chcemy ZWERYFIKOWAĆ jak metoda jest wywoływana,
# ale nie chcemy izolować jej od prawdziwej implementacji

def test_spy(mocker):
    spy = mocker.spy(SomeClass, "some_method")

    obj = SomeClass()
    obj.some_method(42)  # metoda działa normalnie (prawdziwy kod)

    # Ale możemy sprawdzić jak była wywołana
    spy.assert_called_once_with(obj, 42)
    # Możemy też sprawdzić co zwróciła
    # spy.spy_return  → wartość zwrócona przez prawdziwą metodę
```

---

### 🔧 assert helpers – weryfikacja wywołań mocka

> Biblioteka: `unittest.mock` (wbudowana) – dostępne na każdym obiekcie `Mock`/`MagicMock`

```python
from unittest.mock import MagicMock

mock = MagicMock()
mock(1)
mock(1)
mock(2, key="val")

mock.assert_called()                        # OK – wywołany co najmniej raz
mock.assert_called_once()                   # FAIL – wywołano 3 razy, nie raz
mock.assert_called_with(2, key="val")       # sprawdza OSTATNIE wywołanie
mock.assert_any_call(1)                     # OK – gdziekolwiek w historii był call(1)
mock.assert_not_called()                    # FAIL – był wywoływany

mock.call_args                              # argumenty ostatniego wywołania
mock.call_args_list                         # pełna lista wszystkich wywołań
mock.call_count                             # liczba wywołań
```

---

### ⚠️ Zasada: mockuj na poziomie modułu który importuje

> Biblioteka: `unittest.mock` / `pytest-mock` – dotyczy KAŻDEJ formy patch()

Gdy moduł `myapp/service.py` importuje funkcję przez `from requests import get`,
Python tworzy **lokalną referencję** `myapp.service.get`. Patch musi celować w tę
lokalną referencję, a nie w oryginał w bibliotece `requests`.

**Przykładowy kod produkcyjny (`myapp/service.py`):**

```python
# myapp/service.py
from requests import get  # Python tworzy lokalną referencję: myapp.service.get

def fetch_user(user_id: int) -> dict:
    response = get(f"https://api.example.com/users/{user_id}")
    return response.json()
```

**❌ ŹLE – patch celuje w oryginalne źródło, nie w miejsce użycia:**

```python
# unittest.mock / pytest-mock
from unittest.mock import patch

@patch("requests.get")           # ← BŁĄD: patching oryginalnej biblioteki
def test_fetch_user_wrong(mock_get):
    mock_get.return_value.json.return_value = {"id": 1, "name": "Alice"}

    result = fetch_user(1)

    # TEST SIĘ WYKONA, ALE... mock nigdy nie zostanie użyty!
    # myapp.service nadal trzyma starą referencję do prawdziwego requests.get
    # Test wycofa błąd połączenia LUB (jeśli sieć dostępna) zwróci prawdziwe dane
    assert result == {"id": 1, "name": "Alice"}  # może nie przejść!
```

**✅ DOBRZE – patch celuje w referencję tam gdzie funkcja jest UŻYWANA:**

```python
# unittest.mock / pytest-mock
from unittest.mock import patch

@patch("myapp.service.get")      # ← POPRAWNIE: podmiana lokalnej referencji w module
def test_fetch_user_correct(mock_get):
    # Teraz mock_get zastępuje `get` wewnątrz myapp/service.py
    mock_get.return_value.json.return_value = {"id": 1, "name": "Alice"}

    result = fetch_user(1)

    # Test jest w pełni izolowany – żadne prawdziwe zapytanie HTTP nie jest wysyłane
    assert result == {"id": 1, "name": "Alice"}
    mock_get.assert_called_once_with("https://api.example.com/users/1")

# --- Ten sam przykład z pytest-mock (mocker) – zalecany styl ---
def test_fetch_user_with_mocker(mocker):
    mock_get = mocker.patch("myapp.service.get")   # ← lokalny namespace modułu
    mock_get.return_value.json.return_value = {"id": 1, "name": "Alice"}

    result = fetch_user(1)

    assert result == {"id": 1, "name": "Alice"}
    mock_get.assert_called_once_with("https://api.example.com/users/1")
```

> **Reguła kciuka:** Jeśli w pliku `foo.py` masz `from bar import baz`,
> patch pod adresem `"foo.baz"` – nie `"bar.baz"`.

---

**Szybkie kompendium - jak decydować?**

1. Do komunikacji HTTP synchronicznej - chwytajmy paczkę **`responses`**.
2. W asynchronicznych rewirach HTTP (`httpx`) - stosujmy sprawne obwody **`respx`**.
3. Do całej lokalnej reszty operacyjnej w Pythonie - inwestujmy wyłącznie w łatwy obwód **`mocker`** (ze swoim rezerwuarem klasy **`MagicMock`**), powoli porzucając stare dekorowanie kaskadowe z udziałem prehistorycznego `@patch`.
