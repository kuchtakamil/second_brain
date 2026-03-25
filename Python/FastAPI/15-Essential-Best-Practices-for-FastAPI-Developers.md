## <https://www.youtube.com/watch?v=kmJz8w5ij8Y>

Here is an educational guide based on the transcript, structured for clarity and easy reading.

---

# 15 Essential Best Practices for FastAPI Developers

FastAPI is a powerful, high-performance web framework for Python, but to truly unlock its potential and build production-ready applications, you need to understand its mechanics.

Whether you are dealing with async rules, database connections, logging, or deployments, following these 15 best practices will help you avoid common pitfalls and build highly responsive, scalable APIs.

To make these easier to digest, they have been grouped into five core categories.

---

## Part 1: Mastering Async Programming & Performance

FastAPI is highly optimized for asynchronous I/O operations. However, misusing async functions is the number one cause of frozen or slow FastAPI applications.

**1. Never use `async def` for blocking operations**
Blocking operations pause your program until they finish (e.g., `time.sleep()`, synchronous database queries via `pymongo`, or standard `requests`). FastAPI runs `async def` endpoints in the main thread. If you put a blocking operation in an `async def` function, your entire application will freeze and stop processing other requests.
*Rule of thumb:* If you must use blocking code, define your endpoint with a regular `def`. FastAPI will intelligently run it in a separate thread, keeping your app responsive.

**2. Write "async-friendly" code**
To maximize performance, use non-blocking asynchronous libraries so you can safely use `async def`.

* Examples: Use `asyncio.sleep` instead of `time.sleep()`; use `httpx.AsyncClient` instead of `requests`; use `motor` instead of `pymongo`.

**3. Deleguj ciężkie obliczenia (Offload heavy computation)**
FastAPI jest stworzone do obsługi zadań wejścia/wyjścia (I/O-bound), a nie do zadań obciążających procesor (CPU-bound). Uruchamianie ciężkich modeli uczenia maszynowego, przetwarzanie wideo lub skomplikowanych obliczeń matematycznych bezpośrednio w endpoincie zablokuje serwer (Event Loop) i sprawi, że aplikacja przestanie odpowiadać na inne żądania.

* *Lekkie modele ML (poniżej 100ms):* Mogą być uruchamiane bezpośrednio w endpoincie (najlepiej jako funkcje `def`, uruchamiane w puli wątków).
* *Ciężkie modele ML:* Używaj dedykowanych serwerów inferencyjnych (Triton, TensorFlow Serving, TorchServe). W takiej architekturze FastAPI pełni jedynie rolę lekkiego routera (API Gateway), który przyjmuje żądanie od klienta, wysyła je asynchronicznie (np. przez `httpx` lub gRPC) do serwera inferencyjnego, a następnie zwraca wynik.
* *Długotrwałe obliczenia i procesy w tle:* Używaj systemów kolejkowych i workerów (np. Celery z RabbitMQ/Redis), aby wykonywać zadania na osobnych maszynach.

**Przykłady integracji FastAPI z serwerami inferencyjnymi:**

**A. TensorFlow Serving (przez REST API z `httpx`)**
TensorFlow Serving udostępnia gotowe API REST. FastAPI asynchronicznie przekazuje dane do modelu, unikając zablokowania głównego wątku.

```python
from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI()

TF_SERVING_URL = "http://localhost:8501/v1/models/my_model:predict"

@app.post("/predict/tf/")
async def predict_tensorflow(input_data: list[float]):
    payload = {"instances": [input_data]}
    
    async with httpx.AsyncClient() as client:
        response = await client.post(TF_SERVING_URL, json=payload)
        
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Błąd predykcji TF Serving")
        
    result = response.json()
    return {"prediction": result["predictions"][0]}
```

**B. TorchServe (PyTorch, przez public API REST)**
Podobnie jak TF Serving, TorchServe oferuje endpointy REST m.in. na porcie 8080. Jest zaprojektowany tak, aby z łatwością obsługiwać modele wywodzące się ze środowiska PyTorch.

```python
from fastapi import FastAPI, UploadFile, File
import httpx

app = FastAPI()

TORCHSERVE_URL = "http://localhost:8080/predictions/resnet-18"

@app.post("/predict/torch/")
async def predict_torchserve(file: UploadFile = File(...)):
    # Odczytanie obrazu
    image_bytes = await file.read()
    
    async with httpx.AsyncClient() as client:
        # Wysyłanie pliku bezpośrednio do TorchServe
        response = await client.post(
            TORCHSERVE_URL, 
            content=image_bytes,
            headers={"Content-Type": file.content_type}
        )
        
    return response.json()
```

**C. Triton Inference Server (NVIDIA, przez gRPC)**
Triton jest niezwykle wydajny i obsługuje modele z wielu frameworków (TensorFlow, PyTorch, ONNX). Dla maksymalnej wydajności w komunikacji z serwerem inference często używa się protokołu gRPC.

```python
from fastapi import FastAPI
import numpy as np
import tritonclient.grpc.aio as grpcclient

app = FastAPI()

TRITON_URL = "localhost:8001"
MODEL_NAME = "my_onnx_model"

@app.post("/predict/triton/")
async def predict_triton(input_data: list[float]):
    # Inicjalizacja klienta gRPC (asynchronicznego) wstrzyknięta na potrzeby requestu
    client = grpcclient.InferenceServerClient(url=TRITON_URL)
    
    # Przygotowanie danych wejściowych zgodnie z oczekiwaniami modelu (np. wektor FP32 o konkretnym kształcie)
    input_array = np.array([input_data], dtype=np.float32)
    inputs = [grpcclient.InferInput('INPUT__0', input_array.shape, "FP32")]
    inputs[0].set_data_from_numpy(input_array)
    
    # Przygotowanie definicji zwracanego outputu
    outputs = [grpcclient.InferRequestedOutput('OUTPUT__0')]
    
    # Wywołanie asynchroniczne do serwera Triton
    response = await client.infer(model_name=MODEL_NAME, inputs=inputs, outputs=outputs)
    
    # Dekodowanie surowego wyniku z pamięci formatu NumPy
    result = response.as_numpy('OUTPUT__0')
    return {"prediction": result.tolist()}
```

**4. Apply async rules to FastAPI Dependencies**
The rules for endpoints apply to your dependencies as well. If your dependency performs a blocking operation, define it with `def`. If it is entirely non-blocking, use `async def`.

**5. Don't make users wait for background operations**
For small, non-critical tasks that don't need to block the user's response (like sending a confirmation email or logging an event), use FastAPI’s built-in `BackgroundTasks`.

* *Note:* Because these run in the same event loop, they share the same memory and will fail if the server crashes. For guaranteed delivery and retries, use a dedicated worker like Celery.

---

## Part 2: Data Validation and Pydantic

Pydantic is the engine behind FastAPI's data validation. Leveraging it correctly keeps your code clean and your OpenAPI documentation accurate.

**6. Utwórz niestandardowy model bazowy (Create a Custom Base Model)**
Zamiast dziedziczyć bezpośrednio z `BaseModel` we wszystkich modelach Pydantic, utwórz jedną klasę bazową i używaj jej w całej aplikacji. Pozwala to na globalne zarządzanie konfiguracją, np. automatyczne dostosowanie nazw pól (przyjmowanie `camelCase` z frontendu, a trzymanie `snake_case` w Pythonie) lub definiowanie niestandardowych koderów JSON dla typów takich jak `datetime`, `Decimal` czy `ObjectId` z MongoDB.

**Przykład:**

```python
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

class CustomBaseModel(BaseModel):
    # Konfiguracja współdzielona przez wszystkie modele dziedziczące
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        json_encoders={datetime: lambda v: v.strftime("%Y-%m-%dT%H:%M:%SZ")}
    )

class UserResponse(CustomBaseModel):
    first_name: str
    created_at: datetime

# Zwrócony JSON będzie wyglądał tak: {"firstName": "Jan", "createdAt": "2023-10-25T12:00:00Z"}
```

**7. Nie twórz ręcznie obiektów modeli odpowiedzi (Don't manually construct response models)**
Jeśli zdefiniowałeś `response_model` w dekoratorze endpointu, nie musisz ręcznie tworzyć i zwracać instancji tego modelu wewnątrz funkcji. Wystarczy, że zwrócisz standardowy słownik Pythona lub obiekt modelu ORM (np. z SQLAlchemy). FastAPI automatycznie przefiltruje dane względem `response_model`, usunie pola, których nie ma w schemacie (np. hasła), i skonwertuje wynik na JSON.

**Zły przykład (niepotrzebne ręczne mapowanie):**

```python
@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    user_data = db.get_user(user_id) # Zwraca np. {"id": 1, "first_name": "Jan", "password": "..."}
    return UserResponse(**user_data) # Nie rób tego!
```

**Dobry przykład:**

```python
@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    user_data = db.get_user(user_id)
    return user_data # FastAPI automatycznie zwaliduje model i odrzuci pole "password"
```

**8. Waliduj dane w Pydantic, a nie w kodzie (Validate with Pydantic, not your code)**
Przenieś jak najwięcej logiki walidacji biznesowej do modeli Pydantic, unikając w ten sposób zaśmiecania endpointów instrukcjami `if` wyrzucającymi różne błędy. Jeśli Pydantic nie ma wbudowanej walidacji dla danego przypadku, stwórz własne walidatory w modelu (np. `@field_validator` / `@model_validator`). Gwarantuje to spójne i ujednolicone formatowanie błędów (HTTP 422 w formacie JSON), a zdefiniowane reguły będą automatycznie udokumentowane w OpenAPI (Swagger).

**Przykład zastosowania niestandardowych walidatorów w Pydantic (v2):**

```python
from pydantic import BaseModel, field_validator, model_validator
import re

class UserCreate(BaseModel):
    username: str
    password: str
    password_confirm: str

    @field_validator('username')
    @classmethod
    def username_alphanumeric(cls, v: str) -> str:
        if not re.match(r'^[a-zA-Z0-9]+$', v):
            raise ValueError('Nazwa użytkownika może zawierać tylko litery i cyfry')
        return v

    @model_validator(mode='after')
    def check_passwords_match(self) -> 'UserCreate':
        if self.password != self.password_confirm:
            raise ValueError('Hasła się nie zgadzają')
        return self

@app.post("/users/")
async def create_user(user: UserCreate):
    # Endpoint pozostaje czysty, dane 'user' są tu w 100% sprawdzone
    return {"message": "User created", "username": user.username}
```

**9. Używaj Zależności (Dependencies) do walidacji opartej na bazie danych**
Jeżeli proces walidacji wymaga odpytania bazy danych (np. chcemy sprawdzić, czy artykuł o danym ID w ogóle istnieje, albo czy użytkownik ma do niego uprawnienia), nie rób tego w modelach Pydantic. Zamiast tego zdefiniuj nową zależność (Dependency) z FastAPI. Zależności są reużywalne, świetnie czyszczą kod endpointów i są domyślnie cachowane w ramach jednego żądania HTTP, więc nawet kilkukrotne wywołanie zależności nie wykona uciążliwych i zbędnych zapytań do bazy.

**Przykład walidacji zasobu przy użyciu Dependency:**

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# Funkcja służąca jako zależność z wstrzyknięciem połączenia bazowego
def check_article_exists(article_id: int, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Artykuł o podanym ID nie został znaleziony"
        )
    return article

@app.get("/articles/{article_id}")
async def read_article(article: Article = Depends(check_article_exists)):
    # Zależność dba o zwrócenie '404', jeśli nie ma artykułu. 
    # Tutaj operujemy już na pewnym, wczytanym z bazy obiekcie.
    return article

@app.delete("/articles/{article_id}")
async def delete_article(article: Article = Depends(check_article_exists), db: Session = Depends(get_db)):
    # Ponowne wykorzystanie tej samej zależności w innym miejscu
    db.delete(article)
    db.commit()
    return {"message": "Usunięto pomyślnie"}
```

---

## Part 3: Resource & State Management

**10. Używaj puli połączeń do bazy danych (Use a Database Connection Pool)**
Nigdy nie otwieraj nowego połączenia z bazą danych wewnątrz endpointu (np. wywołując `connect()` przy każdym żądaniu HTTP). Nawiązywanie połączenia to kosztowna i powolna operacja. Zamiast tego utwórz pulę połączeń (connection pool) podczas startu aplikacji. Nowoczesną i zalecaną praktyką jest inicjalizacja puli i przechowywanie jej w obiekcie stanu aplikacji: `app.state`. Następnie możesz użyć wstrzykiwania zależności (często z blokiem `async with` lub `yield`), aby sprawnie pobierać i zwalniać połączenia dla każdego żądania.

**Dlaczego to ważne?**
Pula utrzymuje zestaw otwartych połączeń w gotowości. Gdy nadchodzi request, aplikacja po prostu "wypożycza" jedno gotowe połączenie, a po zakończeniu zwraca je do puli. Zwiększa to drastycznie przepustowość i chroni bazę danych przed przeciążeniem z powodu zbyt wielu jednoczesnych połączeń.

**Przykład z użyciem `asyncpg` (PostgreSQL):**

```python
from fastapi import FastAPI, Depends
import asyncpg
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicjalizacja puli połączeń przy starcie
    app.state.pool = await asyncpg.create_pool("postgresql://user:pass@localhost/dbname")
    yield
    # Zamknięcie puli przy wyłączaniu aplikacji
    await app.state.pool.close()

app = FastAPI(lifespan=lifespan)

# Zależność do pobierania połączenia
async def get_db_connection():
    async with app.state.pool.acquire() as connection:
        yield connection

@app.get("/users/")
async def get_users(conn: asyncpg.Connection = Depends(get_db_connection)):
    # Wykorzystanie wypożyczonego połączenia
    users = await conn.fetch("SELECT * FROM users")
    return [dict(u) for u in users]
```

**11. Używaj zdarzeń `lifespan` do zarządzania zasobami aplikacji (Use the `lifespan` event for App-level Resources)**
Unikaj korzystania z przestarzałych dekoratorów `@app.on_event("startup")` i `@app.on_event("shutdown")`. Zamiast nich używaj nowoczesnego menedżera kontekstu we FastAPI, zwanego `lifespan`. Zapewnia to jedno, scentralizowane miejsce do konfigurowania i usuwania zasobów na poziomie aplikacji (takich jak pule połączeń z bazą danych, klienty HTTP, czy połączenia z Redisem/Cache).

**Zalety menedżera kontekstu `lifespan`:**

1. **Bezpieczeństwo typów:** Możesz przekazywać typy wewnątrz `lifespan` i łatwo się do nich odwoływać.
2. **Gwarancja sprzątania:** Kod po słowie kluczowym `yield` zawsze wykona się przy zamykaniu aplikacji, niezależnie od tego, co działo się wcześniej.
3. **Współdzielenie stanu:** Pozwala to na wprost kontrolować, co trafia do `app.state` lub przekazywać dane bezpośrednio (w nowszych wersjach FastAPI/Starlette).

**Przykład użycia `lifespan`:**

```python
from fastapi import FastAPI
import httpx
from contextlib import asynccontextmanager

# Przykładowy klient ML lub zewnętrznego API
ml_models = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Kod wykonywany podczas startu (startup)
    print("Ładowanie modelu ML lub otwieranie klienta HTTP...")
    app.state.http_client = httpx.AsyncClient()
    ml_models["sentiment_analyzer"] = lambda text: "positive" if "dobry" in text else "negative"
    
    yield # Tu aplikacja zaczyna obsługiwać żądania
    
    # Kod wykonywany podczas zamykania (shutdown)
    print("Zamykanie klienta HTTP, czyszczenie zasobów...")
    await app.state.http_client.aclose()
    ml_models.clear()

app = FastAPI(lifespan=lifespan)

@app.get("/analyze/")
async def analyze_text(text: str):
    # Dostęp do globalnych, zarządzanych zasobów
    result = ml_models["sentiment_analyzer"](text)
    return {"text": text, "sentiment": result}
```

---

## Part 4: Configuration & Security

**12. Hide API docs in production**
FastAPI automatically generates interactive Swagger and ReDoc documentation. While excellent for development, exposing these in production can reveal incomplete endpoints or attack vectors. If your API is not meant to be public-facing, disable them in production by setting `docs_url`, `redoc_url`, and `openapi_url` to `None`.

**13. Nigdy nie wpisuj sekretów na sztywno w kodzie (Never hardcode secrets)**
Nigdy, ale to przenigdy nie umieszczaj haseł, kluczy API, tokenów dostępu (np. JWT secret) ani adresów produkcyjnych baz danych bezpośrednio w kodzie źródłowym. Jest to najprostsza droga do wycieku danych, szczególnie jeśli twój kod znajduje się w systemie kontroli wersji (np. GitHub).

**Jak robić to poprawnie:**

1. **Używaj plików `.env` dla statycznych konfiguracji:** Przechowuj porty, adresy URL baz danych, czy klucze API w lokalnym pliku `.env`. Bezwzględnie upewnij się, że plik ten jest dodany do Twojego `.gitignore`. Ponadto zawsze twórz plik `.env.example` ze sztucznymi lub pustymi wartościami, aby inni programiści wiedzieli, jak skonfigurować środowisko.
2. **Używaj `pydantic-settings` zamiast `os.environ`:** Unikaj porozrzucanego po całym kodzie odczytywania zmiennych w stylu `os.getenv("DATABASE_URL")`. Zamiast tego zcentralizuj konfigurację używając paczki `pydantic-settings` (dawniej części `pydantic` v1 jako `BaseSettings`). Dzięki temu zyskujesz:
   * Walidację typów (np. jeśli port musi być liczbą całkowitą, Pydantic to sprawdzi).
   * Wczesne błędy (fail-fast) – aplikacja nie uruchomi się, jeśli brakuje wymaganej zmiennej konfiguracyjnej, co zapobiega nagłym awariom w czasie runtime'u.

**Przykład zarządzania konfiguracją z użyciem `pydantic-settings`:**

Najpierw zainstaluj paczkę: `pip install pydantic-settings`

```python
from fastapi import FastAPI, Depends
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

# 1. Definicja modelu ustawień
class Settings(BaseSettings):
    app_name: str = "My Awesome API"
    admin_email: str
    database_url: str
    secret_key: str
    debug_mode: bool = False
    
    # 2. Konfiguracja Pydantic, aby wczytywał zmienne z pliku .env
    model_config = SettingsConfigDict(env_file=".env")

# 3. Użycie lru_cache zapewnia, że plik .env czytany jest tylko raz
@lru_cache()
def get_settings():
    return Settings()

app = FastAPI()

# 4. Aplikacja failuje na start jeśli brakuje np. admin_email lub database_url
# Możemy wstrzykiwać ustawienia jako zależność:
@app.get("/info/")
async def info(settings: Settings = Depends(get_settings)):
    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email,
        # Nigdy nie zwracaj secret_key w API!
    }
```

---

## Part 5: Logging and Deployment

**14. Używaj ustrukturyzowanego logowania zamiast `print()` (Use Structured Logging, not `print()`)**
Zwykłe polecenia `print()` są całkowicie nieodpowiednie do debugowania w środowisku produkcyjnym. Brakuje im poziomów logowania (INFO, ERROR, DEBUG), znaczników czasu (timestamps) oraz ważnych danych kontekstowych (np. identyfikatora żądania lub danego użytkownika). Co gorsza, użycie `print()` jest synchroniczną operacją I/O.

* **Nowoczesne biblioteki:** Używaj standardowego modułu `logging` Pythona wraz z nowocześniejszymi bibliotekami takimi jak **Loguru** lub **Structlog**. Ułatwiają one zapis logów w łatwym do przeszukiwania formacie JSON oraz wstrzykiwanie kontekstu.
* **Poziomy logowania (Log levels):** Skonfiguruj odpowiednie poziomy logów (`DEBUG` na środowisku deweloperskim, `INFO` lub `ERROR` na produkcji). Pozwala to na uniknięcie przepełnienia nośników logami i redukuje szum informacyjny.
* **Formatowanie JSON:** W rozproszonych architekturach z mikroserwisami formatter powinien wypluwać każdy wpis w pojedynczej linijce JSON. Umożliwia to prostą agregację i analizę logów w narzędziach takich jak ELK Stack (Elasticsearch, Logstash, Kibana) lub systemach Datadog i Grafana Loki.
* **Kontekstowanie logów (Contextual data):** Wykorzystując mechanizmy *middleware* oferowane przez FastAPI i zmienne kontekstowe we wbudowanym `contextvars`, dodawaj unikalny Request ID (id żądania HTTP) do logów. Dzięki temu powiążesz ze sobą poszczególne akcje i błędy wywołane pod jednym wspólnym Requestem.

**Przykład ustrukturyzowanego logowania z użyciem biblioteki Loguru i tworzenia lokalnego kontekstu (Request ID):**

```python
from fastapi import FastAPI, Request
from loguru import logger
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
import contextvars

# Opcjonalnie: Utworzenie zmiennej kontekstowej dla asynchronicznego przesyłania id
request_id_context = contextvars.ContextVar("request_id", default="UNKNOWN")

app = FastAPI()

# Middleware do auto-generowania Request ID
class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        req_id = str(uuid.uuid4())
        request_id_context.set(req_id)
        
        # Wiązanie (bindowanie) konkretnego wywołania / requestu ze zmienną loguru `req_id`
        with logger.contextualize(request_id=req_id):
            logger.info(f"Otrzymano żądanie: {request.method} {request.url.path}")
            response = await call_next(request)
            logger.info(f"Odesłano odpowiedź ze statusem: {response.status_code}")
            
            # Warto dodać takie ID w nagłówku dla klienta, ułatwia to reklamacje oraz pomoc techniczną 
            response.headers["X-Request-ID"] = req_id
            return response

app.add_middleware(RequestIDMiddleware)

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    # Dzięki mechanizmowi contextualize w middleware, ten kawałek automatycznie
    # zapisze również wartość wygenerowanego na starcie przypisanego Request ID "request_id"
    logger.debug(f"Zaczynam processowanie przedmiotu o ID: {item_id}")
    
    if item_id == 0:
        logger.error("Wysłano błędne zapytanie z ID 0")
        return {"error": "Invalid item_id"}
        
    return {"item_id": item_id}
```

**15. Wdrażaj aplikacje używając Gunicorn, Uvicorn i uvloop (Deploy with Gunicorn, Uvicorn, and uvloop)**
O ile bezpośrednie uruchomienie serwera devowego przez standardowe polecenie `uvicorn main:app --reload` jest przydatne do lokalnej pracy, w środowisku produkcyjnym wymaga się architektury gwarantującej niezawodność, równoległość i ponowne uruchamianie uśpionych wątków.

* **Menedżer procesów (Process Manager):** Wykorzystaj narzędzie zarządzania stanami jakim jest **Gunicorn**, pod którym umiejscowisz klasę pracującą (workera) serwera `uvicorn`. W ten sposób Gunicorn odpowiada za zarządzanie odseparowanymi instancjami (utrzymaniem ich działania) a sam "schowany" w nich Uvicorn za ultraszybkie mapowanie z i do zapytań HTTP na sygnały ASGI.
* **Potężne przyspieszenie z uvloop:** Upewnij się, że w swoim docelowym (lub kontenerowym) wirtualnym środowisku zainstalowano moduł **uvloop** (`pip install uvloop`). FastAPI dostrzeże fakt jego obecności i naturalnie wejdzie z nim we współpracę podmieniając typowy wolniejszy wariant pętli (asyncio) w architekturę operującą wewnętrznie na mechanice środowiska C (i potężnej warstwie libuv - silniku obecnym m.in w Node.js). To przełożenie pozwoli zmaksymalizować wolumen przechodzących żądań.
* **Dostrajanie workerów (Tuning):** Podstawowy wzór stosowany rynkowo do ustalenia ilości procesów to zależność z liczbą wirtualnych bądź fizycznych operacyjnych rdzeni obliczeniowych: `(Liczba Rdzeni CPU * 2) + 1`. Jeżeli więc wdrażana maszyna w chmurze liczy dwa procesory – powinno być tu zdefiniowanych aż 5 workerów. Nie jest to reguła niepodważalna – testując własne wdrożenia eksperymentalnie będziesz w stanie oszacować właściwą dla obciążenia skalę.
* **Konteneryzacja Dockera:** Spakuj logikę, wszystkie pliki środowiska i systemową zależność we własny i zbudowany proces obrazu Docker. Będziesz miał gwarancję, że raz zbudowany sprawnie uruchomi się w tych samych zależnościach docelowo na każdej innej wspierającej mechanizm maszynie - i zapewni proste powielanie aplikacji przy ogromnych obciążeniach klastrowych (np w rejonie Amazon lub mechanice K8s (Kubernetes)).

**Przykłady implementacyjne dotyczące wdrożenia:**

**Komenda do wpisania wymuszająca start za wykorzystaniem 4 rdzeni z gunicorna (Terminal/Shell):**

```bash
# Określanie parametrów "załączania", narzucenie ilości używanych wątków i powiązania sieci.
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

**Minimalistyczny sprawdzony model wdrożeniowego pliku "Dockerfile" dla serwera w FastAPI:**

```dockerfile
# Oparcie na zwinnym systemowo sprawdzonym i zmniejszonym szkielecie dla 3.11. 
FROM python:3.11-slim

# Deklaracja stałych uodparniających na blokujące przetrzymywanie w pamięci tymczasowej
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Zakreślenie głównej architektury
WORKDIR /app

# Narzucenie paczek systemowych (na przykładzie obecnego w pliku zbioru, ale musisz tu ręcznie doinstalować "uvicorn standard", "gunicorn", jak i "uvloop")
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Transport zawartości lokalnej programu do obrazu
COPY . .

# Odbezpieczenie i rezerwacja powiązanego gniazda portalu
EXPOSE 8000

# Określenie finałowego wywołania i zablokowania programu w terminalu, Gunicorn startujący procesy robocze przez bibliotekę pracującą (worker-class) Uvicorna
CMD ["gunicorn", "main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
```
