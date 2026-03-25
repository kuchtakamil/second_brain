# PyTest: Przykłady i Scenariusze Testowania

**Exported:** 3/2/2026 17:37:59  
**Link:** [https://gemini.google.com/u/2/app/d6c92e6cd5e69448?pageId=none](https://gemini.google.com/u/2/app/d6c92e6cd5e69448?pageId=none)

## Prompt

Temat: PyTest.

Napisz tak dużo różnych przykładów, scenariuszy testowania jak tylko zdołasz. Cel - edukacyjny.

## Response

Treść wiadomości Gemini
-----------------------

1\. Fundamenty: Proste Asercje i Intuicja
-----------------------------------------

W PyTest nie musisz dziedziczyć po klasach typu `TestCase`. Intuicja polega na tym, że test jest po prostu funkcją, która używa standardowego słowa kluczowego `assert`. PyTest "podmaskowo" nadpisuje ten mechanizm (assert rewriting), aby w razie błędu dostarczyć szczegółowy opis tego, co poszło nie tak.

```
def add(a, b):
    return a + b

def test_add_integers():
    assert add(1, 2) == 3

def test_add_strings():
    assert add("Py", "Test") == "PyTest"
```

**Dlaczego?** To podejście minimalizuje "boilerplate". W porównaniu do biblioteki `unittest` (`self.assertEqual(a, b)`), kod jest czytelniejszy i bardziej "pythonic".

* * *

2\. Parametryzacja: Jedna Logika, Wiele Scenariuszy
---------------------------------------------------

Często chcesz przetestować tę samą funkcję dla różnych zestawów danych. Zamiast pisać 10 niemal identycznych testów, używasz `@pytest.mark.parametrize`.

```
import pytest

@pytest.mark.parametrize("input_val, expected", [
    (5, 10),
    (0, 0),
    (-1, -2),
    (100, 200),
])
def test_double_value(input_val, expected):
    assert input_val * 2 == expected
```

**Kompromisy i pułapki:** \* **Zaleta:** Czytelność i łatwość dodawania nowych przypadków brzegowych.

* **Pułapka:** Jeśli test zawiera bardzo skomplikowaną logikę setupu, która różni się dla każdego parametru, parametryzacja może stać się nieczytelna. Wtedy lepiej rozbić to na osobne testy lub użyć dynamicznych fixture'ów.

* * *

3\. Fixtures: Zarządzanie Stanem i Zasobami
-------------------------------------------

Fixture'y to serce PyTest. Służą do dostarczania stałego bazowego stanu (baseline) na którym opierają się testy. Klasycznie używa się ich do przygotowania środowiska (setup) i późniejszego sprzątania po nim (teardown). Dzięki nim kod testujący staje się modułowy, izolowany i pozbawiony powtórzeń (DRY).

### 3.1 Proste przykłady: Czym może być Fixture?

Fixture w PyTest wcale nie musi być skomplikowanym menedżerem kontekstu czy połączeniem do bazy danych. Może zwracać **zupełnie dowolny typ zmiennej lub obiekt** widoczny w Pythonie. Oto kilka bardzo prostych wariantów, które spotkasz na co dzień:

#### 1. Zwykła stała wartość (String, Int, Słownik z danymi testowymi)

Idealne do centralnego trzymania testowych URL-i z tokenami lub zestawów tzw. "dummy data". Dzięki temu rozwiązaniu omijasz konieczność "magicznego" powtarzania ręcznego wklejania danych wejściowych z osobna w każdym teście.

```python
import pytest

@pytest.fixture
def base_api_url():
    return "https://staging.api.my-app.com/v1"

@pytest.fixture
def test_user_payload():
    return {"username": "tester", "email": "test@domain.com"}

def test_endpoint_construction(base_api_url):
    assert base_api_url.startswith("https")
    assert "/v1" in base_api_url

def test_user_email_domain(test_user_payload):
    assert "@domain.com" in test_user_payload["email"]
```

#### 2. Instancja własnej klasy (Gotowy i skonfigurowany obiekt)

Zamiast za każdym razem kopiować kod typu `moj_serwis = CustomerService("test_db")` we wszystkich testach danej funkcjonalności z osobna, po prostu zwracasz raz zainicjalizowaną referencję.

```python
class DiscountCalculator:
    def __init__(self, default_discount):
        self.default_discount = default_discount

@pytest.fixture
def standard_calculator():
    # Inicjalizujemy raz i bezpowrotnie udostępniamy gotową instancję logiki
    return DiscountCalculator(default_discount=20)

def test_promo_discount_value(standard_calculator):
    assert standard_calculator.default_discount == 20
```

### 3.2 Fixture jako menedżer zasobów z użyciem Yield (Teardown)

#### 3. Słownik jako imitacja Bazy Danych w pamięci w bloku Setup

Użycie słowa kluczowego `yield` zamiast `return` wewnątrz fixture'a to standardowy idiom w PyTest. Kod przed `yield` wykonuje się przed testem (taki sam efekt jak `setUp` w starym `unittest`), a powrót z `yield` następuje tuż po zakończeniu testu (działając jako `tearDown`), i automatycznie wykonuje sprzątanie przydzielonych zasobów.

```python
import pytest

@pytest.fixture
def db_connection():
    # Setup: Inicjalizacja "bazy"
    db = {"users": [], "active": True}
    yield db  # Tu następuje wykonanie testu i zwrócenie referencji do 'db'
    # Teardown: Czyszczenie zasobów po zakończeniu testu
    db.clear()

def test_user_addition(db_connection):
    db_connection["users"].append("Admin")
    assert "Admin" in db_connection["users"]
```

### 3.3 Zależności między Fixture'ami (Wstrzykiwanie Zależności)

Fixture'y w PyTest mają rewelacyjną zdolność do korzystania z innych fixture'ów. Framework sam rozwiązuje graf zależności (Dependency Graph) pod maską i dba o to, by fixture'y wywoływały się w precyzyjnie określonej, odpowiedniej kolejności.

```python
import pytest

@pytest.fixture
def temp_directory(tmp_path):
    # tmp_path to wbudowany fixture z PyTest
    data_dir = tmp_path / "test_data"
    data_dir.mkdir()
    yield data_dir

@pytest.fixture
def config_file(temp_directory):
    # Wstrzyknięcie fixture'a temp_directory do config_file
    config = temp_directory / "config.json"
    config.write_text('{"environment": "test"}')
    return config

def test_config_parsing(config_file):
    # Kod testujący
    assert "environment" in config_file.read_text()
    assert config_file.name == "config.json"
```

### 3.4 Zasięg Fixture'ów (Scopes)

**Szersza perspektywa:** W `unittest` używało się `setUp` i `tearDown`, które zawsze uruchamiały się przed każdą weryfikacją w klasie. Problem polegał na tym, że te metody uruchamiały się dla _każdego_ testu. W PyTest my sterujemy zakresem żywotności obiektu konfiguracyjnego poprzez argument `scope`.

Możesz kontrolować **scope** (zakres):

* `function`: (Domyślny) Inicjalizacja odbywa się od nowa dla każdego pojedynczego testu pobierającego ten fixture. Izolacja jest silna, ale wolna, jeśli stan jest "ciężki".
* `class`: Wykonuje się raz dla całej klasy grupującej.
* `module`: Wykonany jeden raz per plik `.py`. Idealne do cachowania zasobów unikalnych dla danego fragmentu logiki, żeby nie spowalniać testów (np. wczytanie bardzo dużego datasetu w trybie read-only).
* `package`: Raz dla pakietu w obrębie danego folderu (tam gdzie `__init__.py`). Nowość od strony architektury PyTest.
* `session`: Raz na cały cykl wywołania polecenia `pytest` (idealne do podnoszenia kontenera Docker z bazą danych lub postawienia całego klastra na czas masowego wykonywania testów).

```python
import pytest
import time

@pytest.fixture(scope="session")
def expensive_db_setup():
    print("\n[Uruchamiam ciężki setup...]")
    time.sleep(3) # Symulacja łączenia
    db_pool = "Połączenie do relacyjnej bazy postawione"
    yield db_pool
    print("\n[Zakończenie całego cyklu testów... teardown bazy]")

def test_query_one(expensive_db_setup):
    assert expensive_db_setup.startswith("Połączenie")

def test_query_two(expensive_db_setup):
    # Pula bazy 'expensive_db_setup' jest z powrotem używana bez czekania!
    # Obiekt został przekazany błyskawicznie dzięki Session scope.
    assert len(expensive_db_setup) > 0
```

### 3.5 Fixture'y Autouse (Automatycznie używane - Autouse)

Jeśli posiadasz fixture, który absolutnie musi uruchomić się przed daną pulą testów (np. odcinający zapytania HTTP w celu upewnienia się, że nie uderzasz w API w testach), ale nie chcesz przekazywać go jawnie w argumencie do każdej definicji np. `def test_1...()`, użyj flagi `autouse=True`.

```python
import pytest
import datetime

@pytest.fixture(autouse=True)
def ensure_deterministic_time(monkeypatch):
    """
    Zawsze zamraża czas dla wszystkich testów w danym pliku, 
    nawet jeśli nie biorą 'ensure_deterministic_time' parametrycznie.
    """
    class MockedDatetime(datetime.datetime):
        @classmethod
        def now(cls):
            return datetime.datetime(2023, 1, 1)
            
    monkeypatch.setattr(datetime, "datetime", MockedDatetime)

def test_time_is_frozen():
    # Nie podajemy jawnie fixture'a w nawiasach testu, 
    # a i tak mamy podmieniony globalnie czas na rok 2023!
    assert datetime.datetime.now().year == 2023
```

### 3.6 Przydatne Wbudowane Fixture'y (Builtins)

PyTest posiada zestaw potężnych fixture'ów, które są zawsze od samego początku gotowe do zaimportowania:

* `tmp_path` (lub w starszych projektach `tmpdir`) - Tworzy dynamicznie nowe drzewo katalogów tymczasowych w systemie, odizolowane specjalnie dla procesu testów do celów operacji IO. PyTest sam czyści te pliki po skończonej paczce testów.
* `mocker` - (Wtyczka `pytest-mock` ułatwiająca mockowanie bez pisania wielu dekoratorów).
* `monkeypatch` - Pozwala dynamicznie zmodyfikować klasy lub zmienne systemowe (`os.environ`) z idealną gwarancją resetu zmian pod koniec testu do normalnego środowiska.
* `capsys` - Przechwytuje i sprawdza wyrzucone przez skrypty stringi standardowego wyjścia (output stream) - przechwytuje np. wykonanie `print()` w kodzie.

```python
def print_greetings(name: str):
    print(f"Hello, {name}!")

def test_terminal_output(capsys):
    print_greetings("PyTest")
    
    # capsys snapshotuje i sprawdza uwięziony z 'printa' output
    captured = capsys.readouterr()
    assert captured.out == "Hello, PyTest!\n"
```

* * *

4\. Testowanie Wyjątków (Exceptions)
------------------------------------

Dobry test sprawdza nie tylko, czy kod działa, ale też czy poprawnie "wybucha", gdy otrzyma błędne dane.

```
def divide(a, b):
    if b == 0:
        raise ValueError("Division by zero is not allowed")
    return a / b

def test_divide_by_zero():
    with pytest.raises(ValueError) as excinfo:
        divide(10, 0)
    assert "Division by zero" in str(excinfo.value)
```

* * *

5\. Mockowanie i Monkeypatching
-------------------------------

Gdy Twój kod zależy od zewnętrznych API, systemów plików, baz danych lub innych modułów Twojej aplikacji, z pomocą przychodzi mockowanie. Pozwala ono "podmienić" prawdziwą implementację na atrapę kontrolowaną w teście.

### Standardowy mechanizm wbudowany: `monkeypatch`

Mechanizm `monkeypatch` to wbudowana w PyTest funkcja (fixture), pozwalająca na dynamiczną zmianę atrybutów, słowników czy zmiennych środowiskowych na czas trwania testu.
Najczęściej używamy jej, gdy chcemy zmodyfikować zachowanie globalnego obiektu, takiego jak moduł `requests`, aby uniknąć prawdziwych zapytań sieciowych.

```python
import requests

def get_weather(city):
    response = requests.get(f"https://api.weather.com/{city}")
    return response.json()

def test_get_weather_mocked(monkeypatch):
    class MockResponse:
        def json(self):
            return {"temp": 20}

    # Podmieniamy metodę requests.get na naszą atrapę (lambdę zwracającą MockResponse)
    monkeypatch.setattr(requests, "get", lambda _: MockResponse())
    
    result = get_weather("Warsaw")
    assert result["temp"] == 20
```

**Dlaczego?** Izolacja i powtarzalność. W takich testach nie interesuje nas, czy prawdziwe API pogody jest dostępne, ale czy nasza funkcja umie przetworzyć to, co potencjalnie dostanie.
**Ograniczenia:** Kiedy API jest bardzo złożone, ręczne budowanie mocków z użyciem klas takich jak `MockResponse` staje się rozwlekłe i trudne do czytania.

### Czy pokazany wcześniej `monkeypatch` to najpopularniejszy sposób mockowania zapytań HTTP?

**Nie, w profesjonalnych projektach rzadko robi się to ręcznie w ten sposób.**
Wykorzystywanie `monkeypatch` (lub surowego `unittest.mock.patch`) do bezpośredniego uderzania w `requests.get` bywa na dłuższą metę uciążliwe (trzeba ręcznie tworzyć "fałszywe" klasy udające obiekty Response z metodami takimi jak `.json()` czy polami ze statusem HTTP).

**Co jest popularniejsze?**

1. Do biblioteki `requests` najpopularniejsze są dedykowane pakiety do symulowania infrastruktury sieciowej takie jak **`responses`** lub **`requests-mock`**.
2. W nowoczesnym kodzie asynchronicznym korzystającym z biblioteki `httpx`, rynkowym standardem jest biblioteka **`respx`** lub pakiet **`pytest-httpx`**.

_Przykład z użyciem biblioteki `responses`:_

```python
import requests
import responses

@responses.activate
def test_get_weather_with_responses():
    # Definiujemy, jak ma odpowiedzieć mock HTTP na konkretny adres URL
    responses.add(
        responses.GET,
        "https://api.weather.com/Warsaw",
        json={"temp": 20},
        status=200
    )
    
    # Wywołujemy nasz kod - biblioteka przechwytuje zapytanie pod maską
    response = requests.get("https://api.weather.com/Warsaw")
    assert response.json()["temp"] == 20
```

Jak widać, dedykowane narzędzie zapewnia dużo mniejszy "boilerplate", lepiej odzwierciedla zachowanie sieci i jest bardziej czytelne.

### Jak zamockować swój własny, napisany moduł Python z wieloma funkcjami?

Bardzo często do testowania własnych, rozdzielonych modułów korzystamy z wtyczki **`pytest-mock`**, która udostępnia niezwykle przydatny fixture `mocker` (jest to wygodniejsza, bezstanowa nakładka na Pythonowe `unittest.mock`).

Załóżmy, że napisałeś dwa pliki w swoim projekcie. Plik `payment_gateway.py` (np. kontaktuje się z API banku i osobnym systemem antyfraudowym) oraz `order_service.py` (który importuje i używa obydwu funkcji, by przetworzyć zamówienie):

**payment_gateway.py**

```python
def check_fraud_risk(user_id: int) -> bool:
    # Uderza do zew. systemu oceny ryzyka
    raise NotImplementedError("Nie uderzaj do prawdziwego systemu w testach!")

def process_payment(amount: float) -> bool:
    # Skomplikowana logika łączenia z bankiem...
    raise NotImplementedError("Nie uderzaj do prawdziwego banku w testach!")
```

**order_service.py**

```python
from payment_gateway import process_payment, check_fraud_risk

def place_order(user_id: int, item_name: str, price: float) -> str:
    # Najpierw sprawdzamy ryzyko dla danego użytkownika
    if check_fraud_risk(user_id):
        return "Order blocked due to fraud risk."
        
    # Następnie procesujemy płatność
    if process_payment(price):
        return f"Order for {item_name} placed successfully."
        
    return "Payment failed."
```

Teraz chcemy napisać trzy testy dla samego serwisu zamówień (`place_order`), w pełni izolując go przez mockowanie _obu_ funkcji zewnętrznych naraz. Pozwoli to dokładnie przetestować logikę naszego serwisu (`order_service`) dla każdej odnogi `if`/`else`.

**test_orders.py**

```python
# Zauważ, że w parametrach przekazujemy fixture 'mocker'
# Wymaga on zainstalowania pakietu: pip install pytest-mock

def test_place_order_success(mocker):
    # WAŻNE: Patchujemy w MIEJSCU UŻYCIA, czyli w dziedzinie modułu 'order_service'
    mocked_fraud = mocker.patch("order_service.check_fraud_risk", return_value=False)
    mocked_payment = mocker.patch("order_service.process_payment", return_value=True)
    
    result = place_order(user_id=123, item_name="Laptop", price=5000.0)
    
    assert result == "Order for Laptop placed successfully."
    
    # Mocker pozwala upewnić się, czy podmienione funkcje zostały zawołane
    # z odpowiednimi argumentami oraz we właściwej sekwencji
    mocked_fraud.assert_called_once_with(123)
    mocked_payment.assert_called_once_with(5000.0)

def test_place_order_blocked_by_fraud(mocker):
    # W tym teście chcemy symulować podwyższone ryzyko dla użytkownika
    mocked_fraud = mocker.patch("order_service.check_fraud_risk", return_value=True)
    mocked_payment = mocker.patch("order_service.process_payment")
    
    result = place_order(user_id=999, item_name="Phone", price=2000.0)
    
    assert result == "Order blocked due to fraud risk."
    mocked_fraud.assert_called_once_with(999)
    # Wykryto oszustwo, testujemy naszą logikę odcięcia: metoda od płatności 
    # absolutnie NIE powinna zostać uruchomiona!
    mocked_payment.assert_not_called()

def test_place_order_payment_failure(mocker):
    # Użytkownik przetestowany pomyślnie, ale odrzuca go bank na etapie płatności
    mocked_fraud = mocker.patch("order_service.check_fraud_risk", return_value=False)
    mocked_payment = mocker.patch("order_service.process_payment", return_value=False)
    
    result = place_order(user_id=111, item_name="Tablet", price=1500.0)
    
    assert result == "Payment failed."
    mocked_fraud.assert_called_once()
    mocked_payment.assert_called_once()
```

**Podsumowanie i złota zasada (Where to patch):**
Kiedy używasz narzędzi takich jak `mocker.patch()`, podmieniaj obiekt w module, w którym jest on _aktywnie używany_ (tam gdzie wykonano `from ... import ...`), a nie w module, w którym został zdefiniowany.

### Alternatywa wbudowana w Python: Dekorator `@patch` (`unittest.mock`)

Zanim biblioteka `pytest-mock` (czyli fixture `mocker`) stała się standardem w środowisku PyTest, powszechnym sposobem mockowania było użycie wbudowanego dekoratora `@patch` z modułu `unittest.mock`. Podejście to jest wciąż niezwykle popularne i często spotykane w dzisiejszym kodzie.

Zasada działania opiera się na tym, że podajesz "ścieżkę" do mockowanego obiektu (string) w parametrze dekoratora. Następnie biblioteka automatycznie "wstrzykuje" ten przekształcony w atrapę obiekt do Twojej funkcji testowej jako jej argument.

```python
from unittest.mock import patch
# importujemy funkcję, którą będziemy testować
from order_service import place_order

# Używamy dekoratorów @patch (wskazujemy jako string, co mockujemy)
@patch("order_service.process_payment")
@patch("order_service.check_fraud_risk")
def test_place_order_with_patch_decorator(mock_check_fraud_risk, mock_process_payment):
    # UWAGA NA KOLEJNOŚĆ PARAMETRÓW! 
    # Obiekty są wstrzykiwane od "dołu do góry" (od najbliższego dekoratora nad 'def').
    # Zatem pierwszy wyłapany dekorator (ten na dole) trafia do pierwszego parametru, drugi do drugiego itd.
    
    mock_check_fraud_risk.return_value = False
    mock_process_payment.return_value = True
    
    result = place_order(user_id=123, item_name="Laptop", price=5000.0)
    
    assert result == "Order for Laptop placed successfully."
    
    # Podobnie jak przy użyciu fixture 'mocker', weryfikujemy wywołania przypisane do argumentów
    mock_check_fraud_risk.assert_called_once_with(123)
    mock_process_payment.assert_called_once_with(5000.0)
```

**Zalety i Wady tego podejścia:**

* **Zaleta:** Nie wymaga instalowania zewnętrznych wtyczek takich jak `pytest-mock`, ponieważ wszystko to wbudowana biblioteka standardowa Pythona.
* **Wada:** "Piekło dekoratorów" i pułapki kolejności. Jeśli musisz zamockować 5 zależności, funkcja obrasta w 5 dekoratorów, po czym jej sygnatura puchnie o 5 argumentów. Pomylenie ich kolejności (zapomnienie, że wstrzykują się "od dołu do góry") to niezwykle częsty powód niewidocznych na pierwszy rzut oka błędów w testach. Z tego powodu bardziej płaski fixture `mocker` bywa obecnie częściej preferowany.

### Kiedy używać `MagicMock`?

`MagicMock` to specjalna podklasa standardowego `Mock` (dostępna z `unittest.mock`), która ma domyślnie zaimplementowaną większość tzw. metod magicznych w Pythonie (tzw. "dunder methods", np. `__str__`, `__len__`, `__iter__`, `__getitem__`, `__enter__`, `__exit__`).

**Kiedy go używamy?**
Używamy `MagicMock` wszędzie tam, gdzie mockowany obiekt ma być używany w sposób, który wywołuje automatycznie pod maską metody magiczne. Przykłady to:

1. **Menedżery kontekstu (`with ...`)**: Wymagają metod `__enter__` oraz `__exit__`.
2. **Iteracja (`for x in ...`)**: Wymaga metody `__iter__`.
3. **Pobieranie długości (`len(...)`)**: Wymaga metody `__len__`.
4. **Dostęp do elementów jak w kolekcjach (`obj["klucz"]`)**: Wymaga metody `__getitem__`.
5. **Konwersje rzutowania (`str(...)`, `int(...)`)**.

Gdy używasz fixture `mocker.patch()` lub dekoratora `@patch`, biblioteka domyślnie tworzy i zwraca instancję `MagicMock` zamiast zwykłego `Mock`, aby mieć pewność, że większość standardowych natywnych operacji w Pythonie na atrapie zadziała bez rzucenia niespodziewanego wyjątku. Podstawowego `Mock` używamy znacznie rzadziej – głównie wtedy, gdy celowo zależy nam na tym, aby atrapie brakowało wsparcia dla iteracji, kontekstu z "with" (aby test "wywalił się" rzucając `TypeError`, chroniąc nas przed błędnym wywołaniem, na przykład iterowaniem po obiekcie, który w rzeczywistości nie służy do iteracji).

**Przykłady użycia `MagicMock`:**

#### 1. Mockowanie menedżera kontekstu (np. otwieranie pliku)

Gdy funkcja otwiera plik przy pomocy instrukcji `with open(...)`, użyty obiekt musi posiadać metody wchodzące do kontekstu i wychodzące z niego.

```python
from unittest.mock import MagicMock

def read_first_line(file_path):
    with open(file_path, "r") as f:
        return f.readline()

def test_read_first_line(mocker):
    # Tworzymy MagicMock, aby zaprogramować jego zachowanie po otwarciu instrukcją 'with'
    mock_file = MagicMock()
    # Pamiętaj, że instrukcja 'with' pod spodem pracuje na obiekcie zwracanym przez blok __enter__
    mock_file.__enter__.return_value.readline.return_value = "Zmockowana pierwsza linia"
    
    # Podmieniamy globalną i standardową funkcję 'open'
    mocker.patch("builtins.open", return_value=mock_file)
    
    result = read_first_line("dummy.txt")
    assert result == "Zmockowana pierwsza linia"
```

_Wskazówka: W codziennej praktyce do samego pliku Python udostępnia ułatwienie `mock_open()`, ale powyższy kod doskonale obrazuje mechanikę, jaka dzieje się pod spodem przy wszelkich obiektach używanych za pomocą bloku `with`._

#### 2. Mockowanie obiektu obsługującego protokół iteracji i długości

Jeśli twoja aplikacja przyjmuje obiekt, który udaje kolekcję lub prostą listę (można po nim przeiterować wywołując pętlę `for` lub też ustalić wielkość instrukcją `len()`), to `MagicMock` będzie strzałem w dziesiątkę. Poniższy kod na podstawowym obiekcie `Mock` wyrzuciłby natychmiastowo `TypeError`.

```python
from unittest.mock import MagicMock

def process_items(container):
    # Operator len aktywuje w atrapie funkcję __len__
    if len(container) == 0:
        return "Pusto"
        
    results = []
    # Pętla aktywuje w atrapie funkcję __iter__
    for item in container:
        results.append(item * 2)
    return results

def test_process_items_with_magicmock():
    mock_container = MagicMock()
    
    # Konfigurujemy własne, symulowane zwracane z protokołów wartości!
    mock_container.__len__.return_value = 3
    mock_container.__iter__.return_value = iter([10, 20, 30])
    
    result = process_items(mock_container)
    
    # Weryfikujemy, że program użył atrybutów MagickMock prawidłowo obliczając wynik
    assert result == [20, 40, 60]
```

* * *

6\. Własne Markery i Filtrowanie Testów
---------------------------------------

Możesz tagować testy, aby uruchamiać tylko ich podzbiór (np. tylko te powolne lub tylko te integracyjne).

```
import pytest

@pytest.mark.slow
def test_heavy_computation():
    import time
    time.sleep(2)
    assert True

@pytest.mark.integration
def test_external_api_connection():
    assert True
```

**Uruchamianie:** \* `pytest -m slow` – uruchomi tylko wolne testy.

* `pytest -m "not slow"` – pominie wolne testy.

* * *

7\. Obsługa Kodu Asynchronicznego (`pytest-asyncio`)
----------------------------------------------------

W nowoczesnym Pythonie (np. FastAPI, Tortoise ORM, `aiohttp`) większość kodu wykorzystuje współbieżność opartą o `async`/`await`. Ponieważ standardowy PyTest operuje synchronicznie, nie potrafi on bezpośrednio uruchamiać testów asynchronicznych. Konieczne jest użycie oficjalnej wtyczki **`pytest-asyncio`**.

### Podstawowe Użycie

Aby uświadomić PyTest, że dana funkcja testowa jest asynchroniczna, dodajemy dekorator `@pytest.mark.asyncio`.

```python
import pytest
import asyncio

async def async_fetch_data():
    await asyncio.sleep(0.1)  # Symulacja zapytania I/O
    return {"data": 1}

@pytest.mark.asyncio
async def test_async_fetch():
    result = await async_fetch_data()
    assert result["data"] == 1
```

### Tryb Automatyczny (`asyncio_mode = auto`)

Jeśli cały Twój projekt jest oparty na kodzie asynchronicznym (np. tworzysz API korzystając z FastAPI), pisanie `@pytest.mark.asyncio` przed _każdym_ testem asynchronicznym staje się bardzo uciążliwe. Wtyczka daje możliwość konfiguracji globalnej. Tworząc plik np. `pytest.ini` lub `pyproject.toml`, możemy to zautomatyzować:

**pytest.ini**

```ini
[pytest]
asyncio_mode = auto
```

Mając to ustawienie, PyTest automatycznie rozpozna każdą funkcję zaczynającą się od `async def test_...` jako test asynchroniczny. Dekoratory `@pytest.mark.asyncio` nie będą już w ogóle potrzebne:

```python
async def test_auto_async():
    result = await async_fetch_data()
    assert result["data"] == 1
```

### Asynchroniczne Fixture'y (Async Fixtures)

Często chcemy skonfigurować asynchronicznego klienta bazy danych (np. asynchroniczne połączenie z Postgres przez `asyncpg`) na potrzeby testu. `pytest-asyncio` potrafi z łatwością obsługiwać asynchroniczne generatory, umożliwiając przygotowanie operacji setup i teardown używających `await`.

```python
import pytest
import asyncio

# Dzięki pytest-asyncio, fixture może być asynchroniczny i używać 'yield'
@pytest.fixture
async def async_db_connection():
    # Setup: Nawiązanie testowego "połączenia" asynchronicznego
    print("\n[Setup] Connecting to async DB...")
    connection = {"is_connected": True}
    await asyncio.sleep(0.05)
    
    yield connection
    
    # Teardown: Zamknięcie "połączenia" po zakończeniu testu
    print("\n[Teardown] Disconnecting from async DB...")
    connection["is_connected"] = False
    await asyncio.sleep(0.05)

# Pamiętaj o dekoratorze (lub użyj 'auto' w configu tak jak opisałem wyżej!)
@pytest.mark.asyncio
async def test_db_connection(async_db_connection):
    assert async_db_connection["is_connected"] is True
```

### Testowanie Wyjątków w Asynchronicznym Kodzie

Weryfikacja tego, czy wyrzucono asynchroniczny błąd, pozostaje tak samo intuicyjna, jak przy testach synchronicznych. Standardowy `pytest.raises` działa płynnie z wywołaniami `await`.

```python
import pytest

async def fetch_item(item_id):
    if item_id < 0:
        raise ValueError("Item ID cannot be negative")
    return "Valid Item"

@pytest.mark.asyncio
async def test_fetch_item_error():
    # Context manager radzi sobie z wywołaniami będącymi korutynami
    with pytest.raises(ValueError, match="cannot be negative"):
        await fetch_item(-1)
```

### Testowanie Sieci Asynchronicznej (`httpx`)

Do wysyłania asynchronicznych requestów HTTP w projektach `async` standardem produkcyjnym stał się klient **`httpx`** (wspierający `async` i `await`, co jest dużą przewagą nad archaicznymi przy programowaniu asynchronicznym `requests`). Testując kod sieciowy, możemy używać PyTest bez żadnych przeszkód.

```python
import pytest
import httpx

@pytest.mark.asyncio
async def test_external_api_call():
    # Uwaga: dla silnie izolowanych testów jednostkowych często korzysta się z 'respx' 
    # (podobnie jak opisywano wyżej dla 'responses'), by zmocować ruch sieciowy. 
    # Przy testach uderzających realnie w sieć użyjesz asynchronicznego menadżera kontekstu:
    async with httpx.AsyncClient() as client:
        response = await client.get("https://httpbin.org/get")
        assert response.status_code == 200
```

* * *

8\. Konfiguracja Globalna: `conftest.py`
----------------------------------------

Jeśli masz fixture'y, które mają być dostępne w wielu plikach testowych, umieść je w pliku o nazwie `conftest.py`. PyTest automatycznie go wykryje.

| Funkcjonalność | Lokalny test | conftest.py |
| --- | --- | --- |
| **Dostępność** | Tylko w tym pliku | W całym katalogu i podkatalogach |
| **Importy** | Wymagane jawnie | Automatyczne (magic) |
| **Zastosowanie** | Specyficzne dane | Mocki API, sesje DB, logowanie |

* * *

9\. Przykładowe Scenariusze Testowe (Tabela Porównawcza)
--------------------------------------------------------

| Scenariusz | Narzędzie PyTest | Intuicja |
| --- | --- | --- |
| Testowanie różnych stawek VAT | `@pytest.mark.parametrize` | Ta sama formuła, inne liczby. |
| Dostęp do tymczasowego folderu | Fixture `tmp_path` | PyTest sam tworzy i sprząta folder na dysku. |
| Sprawdzenie, czy funkcja wysłała email | `mocker` (pytest-mock) | Nie wysyłamy maila, sprawdzamy czy "próbowano". |
| Test pominięty na Windowsie | `@pytest.mark.skipif` | Wyłączamy test, jeśli OS się nie zgadza. |
| Spodziewany błąd (XFAIL) | `@pytest.mark.xfail` | Wiemy, że kod ma buga, ale nie chcemy, by test psuł CI. |

* * *

10\. Zaawansowane: Hooks i Dynamiczna Rejestracja
-------------------------------------------------

Możesz modyfikować zachowanie PyTesta poprzez hooki w `conftest.py`, np. dodając własne kolumny do raportu lub dynamicznie generując testy na podstawie plików JSON w folderze.

```
# conftest.py
def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="dev", help="Environment to run tests against")

@pytest.fixture
def environment(request):
    return request.config.getoption("--env")
```

To pozwala na uruchomienie testów komendą `pytest --env=production`, co zmienia zachowanie testów w zależności od środowiska.

Chciałbyś, abym przygotował konkretny zestaw testów dla wybranej architektury (np. API w Flask/FastAPI) czy skupił się na głębszym wyjaśnieniu mechanizmu `mocker` i izolacji warstwowej?

---
Powered by [Gemini Exporter](https://www.ai-chat-exporter.com)
