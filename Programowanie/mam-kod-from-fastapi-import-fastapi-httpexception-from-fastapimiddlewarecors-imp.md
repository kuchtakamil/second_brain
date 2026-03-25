# Mam kod from fastapi import FastAPI, HTTPException from fastapi.middleware.cors

**Data:** 3 sty 2026, 19:30:49 CET

---

**User:**

Mam kod
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv
from typing import Optional
import uuid

# Load environment variables
load_dotenv(override=True)

app = FastAPI()

# Configure CORS
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OpenAI client
client = OpenAI()


# Load personality details
def load_personality():
    with open("me.txt", "r", encoding="utf-8") as f:
        return f.read().strip()


PERSONALITY = load_personality()


# Request/Response models
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    session_id: str


@app.get("/")
async def root():
    return {"message": "AI Digital Twin API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Generate session ID if not provided
        session_id = request.session_id or str(uuid.uuid4())

        # Create system message with personality
        # NOTE: No memory - each request is independent!
        messages = [
            {"role": "system", "content": PERSONALITY},
            {"role": "user", "content": request.message},
        ]

        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )

        return ChatResponse(
            response=response.choices[0].message.content,
            session_id=session_id
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

I dostaję 500 Internal Server Error. To za mało żeby wiedzieć co jest nie tam.Jak rozszerzyć logowaniei dlaczego raise HTTPException(status_code=500, detail=str(e)) nie wystarcza?

---

**Gemini:**

Problem z Twoim obecnym podejściem polega na tym, że `str(e)` wyciąga jedynie komunikat błędu (np. *"OpenAI connection error"*), ale całkowicie gubi **Traceback**, czyli informację o tym, w której linii i w jakim kontekście wystąpił błąd. Co więcej, zwracanie szczegółów błędu bezpośrednio do klienta w `HTTPException` jest niebezpieczne (wyciek danych o infrastrukturze) i nieczytelne.

Oto jak profesjonalnie podejść do logowania i debugowania w FastAPI.

---

### 1. Dlaczego Twoje `try-except` jest niewystarczające?

1. **Brak stosu wywołań (Stack Trace):** Sam komunikat `detail=str(e)` nie powie Ci, czy błąd rzucił klient OpenAI, czy może funkcja `load_personality()` zawiodła, bo plik zniknął.
2. **Połykanie błędów:** FastAPI ma wbudowany mechanizm obsługi błędów. Jeśli sam złapiesz błąd i rzucisz `HTTPException(500)`, standardowe logery FastAPI/Uvicorn mogą nie wypisać pełnego tracebacku na konsolę, bo uznały, że błąd został "obsłużony".
3. **Brak kontekstu:** Nie wiesz, jakie parametry (np. `session_id`) wywołały błąd.

---

### 2. Rozszerzone logowanie przy użyciu modułu `logging`

Zamiast modyfikować każdy endpoint, najlepiej skonfigurować globalny logger i użyć **Global Exception Handler**.

```
import logging
import sys

# Konfiguracja loggera
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Przykład użycia wewnątrz endpointu
@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        # ... kod ...
        pass
    except Exception as e:
        # logging.exception automatycznie dołącza traceback!
        logger.exception(f"Error processing chat request for session: {request.session_id}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
```

---

### 3. Globalny Exception Handler (Rekomendowane)

Zamiast pisać `try-except` w każdym endpoincie, usuń je i pozwól FastAPI obsłużyć błędy centralnie. Dzięki temu kod biznesowy jest czystszy.

```
from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # Logujemy pełny traceback
    logger.error(f"Global error caught: {exc}", exc_info=True)
    
    # Zwracamy generyczny błąd klientowi
    return JSONResponse(
        status_code=500,
        content={"message": "An unexpected error occurred. Please check logs."},
    )
```

---

### 4. Middleware do logowania Request/Response

Jeśli chcesz widzieć dokładnie, co przychodzi i co wychodzi z Twojego API (bardzo pomocne przy 500-tkach), użyj Middleware.

```
import time

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Logowanie wejścia
    logger.info(f"Incoming request: {request.method} {request.url.path}")
    
    response = await call_next(request)
    
    process_time = (time.time() - start_time) * 1000
    logger.info(f"Finished request: {response.status_code} (Duration: {process_time:.2f}ms)")
    
    return response
```

---

### 5. Zaawansowane debugowanie: Loguru

W środowisku Pythonowym standardowy `logging` bywa uciążliwy. Biblioteka `loguru` oferuje znacznie lepszą czytelność i automatyczne logowanie zmiennych.

```
pip install loguru
```

```
from loguru import logger

# Loguru automatycznie koloruje wyjście i lepiej formatuje tracebacki
logger.add("debug.log", rotation="500 MB", level="DEBUG")

@app.post("/chat")
async def chat(request: ChatRequest):
    # Loguru pozwala na tzw. "catch" dekorator lub prosty exception call
    with logger.catch():
        # Twój kod tutaj - jeśli wystąpi błąd, loguru wypisze 
        # CAŁY stan zmiennych w momencie crashu do konsoli.
        pass
```

### Podsumowanie - co powinieneś zmienić teraz:

1. **Usuń** `try-except` z endpointu `/chat` (pozwól aplikacji "wywalić się").
2. Zaimplementuj **Global Exception Handler** z punktu 3.
3. Używaj `logger.exception("komunikat")` zamiast `print()` lub `str(e)`. `logger.exception` to magiczna funkcja, która wyciąga `sys.exc_info()` i dołącza go do logu.

Czy chcesz, abym pomógł Ci zintegrować system Sentry do automatycznego przechwytywania tych błędów w środowisku produkcyjnym?