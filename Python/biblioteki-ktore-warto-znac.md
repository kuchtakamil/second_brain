# Biblioteki Python dla programisty z 3-letnim stażem

## Po co to wiedzieć?

Po 3 latach pracy z Pythonem powinieneś swobodnie poruszać się po ekosystemie — znać nie tylko składnię, ale też **właściwe narzędzia do typowych zadań**. Poniżej znajdziesz listę bibliotek (standardowych i zewnętrznych), które są oczekiwane na tym poziomie doświadczenia.

---

## 🌐 HTTP i komunikacja sieciowa

| Biblioteka | Opis |
|---|---|
| `requests` | Najpopularniejsza biblioteka do synchronicznych zapytań HTTP — GET, POST, obsługa nagłówków, ciasteczek i sesji. |
| `httpx` | Nowoczesna alternatywa dla `requests` z natywnym wsparciem dla `async/await` i HTTP/2. |
| `aiohttp` | Asynchroniczny klient i serwer HTTP — idealny do wysokowydajnych aplikacji opartych na `asyncio`. |
| `urllib3` | Niskopoziomowy klient HTTP, na którym zbudowany jest `requests` — przydatny gdy potrzebujesz pełnej kontroli nad połączeniami. |
| `websockets` | Biblioteka do komunikacji w czasie rzeczywistym przez protokół WebSocket z pełnym wsparciem async. |

---

## 📁 Praca z plikami i systemem plików

| Biblioteka | Opis |
|---|---|
| `pathlib` *(std)* | Obiektowa obsługa ścieżek i plików — nowoczesny zamiennik `os.path`. |
| `shutil` *(std)* | Kopiowanie, przenoszenie, usuwanie plików i katalogów oraz tworzenie archiwów. |
| `os` *(std)* | Niskopoziomowe operacje systemowe — zmienne środowiskowe, procesy, uprawnienia plików. |
| `tempfile` *(std)* | Tworzenie plików i katalogów tymczasowych, automatycznie usuwanych po użyciu. |
| `glob` *(std)* | Wyszukiwanie plików pasujących do wzorca (np. `*.csv`, `**/*.json`). |
| `watchdog` | Monitorowanie zmian w systemie plików w czasie rzeczywistym (zdarzenia: tworzenie, modyfikacja, usunięcie). |

---

## 📊 Formaty danych i serializacja

| Biblioteka | Opis |
|---|---|
| `json` *(std)* | Kodowanie i dekodowanie danych w formacie JSON — codzienne narzędzie przy pracy z API. |
| `csv` *(std)* | Odczyt i zapis plików CSV — prosty, ale wystarczający do wielu zadań. |
| `PyYAML` | Parsowanie i generowanie plików YAML — konfiguracje, CI/CD, Kubernetes manifesty. |
| `toml` / `tomllib` *(std od 3.11)* | Obsługa formatu TOML, używanego m.in. w `pyproject.toml`. |
| `pickle` *(std)* | Serializacja obiektów Pythona do formatu binarnego — szybka, ale niebezpieczna z niezaufanymi danymi. |
| `orjson` | Ultra-szybka serializacja/deserializacja JSON napisana w Rust — popularna w FastAPI i mikroserwisach. |
| `pydantic` | Walidacja i parsowanie danych z użyciem typów Pythona — fundament FastAPI i wielu nowoczesnych projektów. |

---

## 🗄️ Bazy danych

| Biblioteka | Opis |
|---|---|
| `sqlite3` *(std)* | Wbudowana obsługa baz danych SQLite — idealna do prototypów, testów i małych aplikacji. |
| `SQLAlchemy` | Najpopularniejszy ORM w Pythonie — obsługuje zarówno surowe SQL jak i mapowanie obiektowo-relacyjne. |
| `asyncpg` | Bardzo szybki, asynchroniczny sterownik do PostgreSQL. |
| `psycopg2` / `psycopg3` | Standardowy sterownik do PostgreSQL — synchroniczny, dojrzały, wszechobecny w projektach. |
| `redis-py` | Klient do Redis — cache, kolejki, sesje, pub/sub. |
| `motor` | Asynchroniczny sterownik do MongoDB oparty na `asyncio`. |

---

## 🧪 Testowanie

| Biblioteka | Opis |
|---|---|
| `pytest` | De facto standard testowania w Pythonie — fixtures, parametrize, pluginy. |
| `unittest` *(std)* | Wbudowany framework testowy wzorowany na JUnit — znany, choć mniej elastyczny niż pytest. |
| `unittest.mock` *(std)* | Mockowanie zależności w testach — `patch()`, `MagicMock`, `AsyncMock`. |
| `pytest-cov` | Plugin do pytest generujący raporty pokrycia kodu testami. |
| `hypothesis` | Testy property-based — automatycznie generuje dane wejściowe i szuka edge-case'ów. |
| `factory_boy` | Fabryki obiektów testowych — czytelna alternatywa dla ręcznego tworzenia fixtures. |
| `faker` | Generowanie realistycznych danych testowych — imiona, adresy, daty, numery telefonów. |

---

## ⚡ Asynchroniczność i współbieżność

| Biblioteka | Opis |
|---|---|
| `asyncio` *(std)* | Rdzeń asynchroniczności w Pythonie — pętla zdarzeń, korutyny, taski. |
| `threading` *(std)* | Wątki — przydatne do operacji I/O-bound, ograniczone przez GIL w CPU-bound. |
| `multiprocessing` *(std)* | Procesy potomne — omijają GIL, idealne do zadań CPU-bound. |
| `concurrent.futures` *(std)* | Wysokopoziomowy interfejs do puli wątków (`ThreadPoolExecutor`) i procesów (`ProcessPoolExecutor`). |
| `celery` | Rozproszona kolejka zadań — tło, harmonogramy, retry — standard w projektach Django/Flask. |

---

## 🌐 Web i API

| Biblioteka | Opis |
|---|---|
| `FastAPI` | Nowoczesny framework do budowy API — automatyczna dokumentacja, walidacja danych, async. |
| `Flask` | Lekki mikroframework webowy — prosty, elastyczny, ogromny ekosystem rozszerzeń. |
| `Django` | Full-stack framework — ORM, admin, auth, szablony — "batteries included". |
| `uvicorn` | Serwer ASGI do uruchamiania aplikacji FastAPI/Starlette z pełnym wsparciem async. |
| `gunicorn` | Produkcyjny serwer WSGI dla Flask/Django — zarządzanie workerami, graceful restart. |

---

## 🔧 Narzędzia deweloperskie i jakość kodu

| Biblioteka | Opis |
|---|---|
| `ruff` | Błyskawiczny linter i formatter Pythona napisany w Rust — zastępuje flake8, isort, black. |
| `mypy` | Statyczny analizator typów — weryfikuje adnotacje typów bez uruchamiania kodu. |
| `black` | Opinionated formatter kodu — "one true style", eliminuje dyskusje o formatowaniu. |
| `pre-commit` | Framework do hooków Git — automatyczne sprawdzanie kodu przed każdym commitem. |
| `bandit` | Skaner bezpieczeństwa kodu — wykrywa typowe podatności (np. hardcoded passwords, eval). |

---

## 📦 Zarządzanie zależnościami i środowiskiem

| Biblioteka / Narzędzie | Opis |
|---|---|
| `pip` *(std)* | Podstawowy menedżer pakietów Pythona. |
| `venv` *(std)* | Tworzenie izolowanych środowisk wirtualnych — wbudowane od Python 3.3. |
| `poetry` | Zarządzanie zależnościami + budowanie paczek — lockfile, grupy dev, publikacja na PyPI. |
| `uv` | Ultra-szybki menedżer pakietów i środowisk napisany w Rust — nowoczesna alternatywa dla pip + venv. |

---

## 📝 Logowanie i monitoring

| Biblioteka | Opis |
|---|---|
| `logging` *(std)* | Wbudowany system logowania — handlery, formattery, poziomy logów, rotacja plików. |
| `structlog` | Strukturalne logowanie — logi w formacie JSON, łatwe do parsowania przez narzędzia monitorujące. |
| `sentry-sdk` | Automatyczne raportowanie błędów do Sentry — stack traces, kontekst, breadcrumbs. |
| `rich` | Piękne formatowanie w terminalu — kolorowy output, tabele, progress bary, logi. |

---

## 🔐 Bezpieczeństwo i kryptografia

| Biblioteka | Opis |
|---|---|
| `hashlib` *(std)* | Funkcje haszujące — SHA256, SHA512, MD5 — do sum kontrolnych i weryfikacji integralności. |
| `secrets` *(std)* | Generowanie kryptograficznie bezpiecznych tokenów, haseł i losowych wartości. |
| `cryptography` | Kompletna biblioteka kryptograficzna — szyfrowanie symetryczne/asymetryczne, certyfikaty, HMAC. |
| `PyJWT` | Kodowanie i dekodowanie tokenów JWT — standard w uwierzytelnianiu API. |
| `python-dotenv` | Ładowanie zmiennych środowiskowych z pliku `.env` — bezpieczne przechowywanie sekretów. |

---

## 🐳 DevOps, CLI i automatyzacja

| Biblioteka | Opis |
|---|---|
| `subprocess` *(std)* | Uruchamianie zewnętrznych procesów i komend systemowych z poziomu Pythona. |
| `argparse` *(std)* | Parsowanie argumentów linii poleceń — wbudowane, ale dość rozwlekłe. |
| `click` | Elegancka biblioteka do budowy CLI — dekoratory, grupy komend, automatyczna pomoc. |
| `typer` | Nowoczesne CLI oparte na typach Pythona — zbudowane na bazie Click, mniej boilerplate'u. |
| `boto3` | Oficjalny SDK do AWS — S3, Lambda, DynamoDB, SQS i setki innych usług. |
| `docker-py` | Sterowanie Dockerem z poziomu Pythona — budowanie obrazów, zarządzanie kontenerami. |
| `paramiko` | Klient SSH w Pythonie — zdalne wykonywanie poleceń, transfer plików (SFTP). |

---

## 🕷️ Web scraping i parsowanie HTML

| Biblioteka | Opis |
|---|---|
| `BeautifulSoup` | Parsowanie HTML/XML — wygodne wyszukiwanie elementów, ekstrakcja danych ze stron. |
| `lxml` | Szybki parser XML/HTML napisany w C — obsługuje XPath i XSLT. |
| `scrapy` | Kompletny framework do web scrapingu — spider, pipeline, middleware, obsługa throttlingu. |
| `selenium` / `playwright` | Automatyzacja przeglądarki — testy E2E, scraping stron renderowanych przez JavaScript. |

---

## 🧰 Pozostałe przydatne biblioteki

| Biblioteka | Opis |
|---|---|
| `re` *(std)* | Wyrażenia regularne — wyszukiwanie, dopasowywanie i zamiana wzorców w tekście. |
| `datetime` *(std)* | Operacje na datach i czasie — parsowanie, formatowanie, strefy czasowe. |
| `collections` *(std)* | Rozszerzone kontenery — `defaultdict`, `Counter`, `deque`, `namedtuple`, `OrderedDict`. |
| `itertools` *(std)* | Zaawansowane iteratory — `chain`, `product`, `groupby`, `combinations`, `permutations`. |
| `functools` *(std)* | Narzędzia funkcyjne — `lru_cache`, `partial`, `reduce`, `wraps`, `singledispatch`. |
| `dataclasses` *(std)* | Dekorator `@dataclass` — automatyczne generowanie `__init__`, `__repr__`, `__eq__` dla klas danych. |
| `typing` *(std)* | Adnotacje typów — `List`, `Dict`, `Optional`, `Union`, `Protocol`, `TypeVar`. |
| `Pillow` | Przetwarzanie obrazów — otwieranie, przycinanie, konwersja formatów, filtry. |
| `Jinja2` | Silnik szablonów — renderowanie HTML, e-maili, plików konfiguracyjnych z dynamicznymi danymi. |
| `tenacity` | Dekorator do automatycznych ponowień (retry) — backoff, warunki stopu, limity. |
| `pendulum` | Lepsza obsługa dat i czasu niż `datetime` — strefy czasowe, humanizacja, intuicyjne API. |

---

## Powiązane notatki

- [Biblioteki Pythona](biblioteki-pythona.md) — ogólny przegląd popularnych bibliotek
- [Biblioteka functools Python](biblioteka-functools-python.md) — szczegóły modułu `functools`
- [Biblioteki do typów Python](biblioteki-do-typów-python.md) — moduł `typing` w praktyce
- [Asyncio cheatsheet](asyncio-cheatsheet.md) — ściąga z `asyncio`
- [Pytest: Przykłady i Scenariusze Testowania](PyTest_%20Przykłady%20i%20Scenariusze%20Testowania.md) — praktyczne testy w pytest
