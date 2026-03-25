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

```python
# Assuming order_service.py has lines like: 
# from payment_gateway import process_payment, check_fraud_risk

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
*(W praktycznym programowaniu posługujemy się dla uproszczenia obiektem klasy pomocniczej `mock_open()`, niemniej ten przykład dogłębnie klaruje rzeczywisty fundament obsługi interfejsów pod skapami instrukcji `with`.)*

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

**Szybkie kompendium - jak decydować?**
1. Do komunikacji HTTP synchronicznej - chwytajmy paczkę **`responses`**.
2. W asynchronicznych rewirach HTTP (`httpx`) - stosujmy sprawne obwody **`respx`**.
3. Do całej lokalnej reszty operacyjnej w Pythonie - inwestujmy wyłącznie w łatwy obwód **`mocker`** (ze swoim rezerwuarem klasy **`MagicMock`**), powoli porzucając stare dekorowanie kaskadowe z udziałem prehistorycznego `@patch`.
