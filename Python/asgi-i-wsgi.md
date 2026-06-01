# Czym są ASGI i WSGI w aplikacjach Pythona

**WSGI** (Web Server Gateway Interface) oraz **ASGI** (Asynchronous Server Gateway Interface) to standardy interfejsów w Pythonie, które definiują, w jaki sposób serwer WWW (np. Gunicorn, Uvicorn) komunikuje się z aplikacją webową (np. Django, Flask, FastAPI).

Służą one jako "tłumacze" lub pośrednicy pomiędzy serwerem obsługującym ruch sieciowy a kodem aplikacji napisanym w Pythonie.

## Dlaczego są ważne? / Kiedy mają zastosowanie?

Bez standardów takich jak WSGI i ASGI, każdy framework webowy musiałby być projektowany pod konkretny serwer WWW. Dzięki nim, możemy używać dowolnego serwera kompatybilnego z danym interfejsem dla dowolnej aplikacji, która go implementuje. Oznacza to, że tę samą aplikację napisaną we Flasku możemy uruchomić na serwerze Gunicorn, uWSGI lub innych obsługujących ten sam interfejs.

- **WSGI** stosuje się do tradycyjnych, **synchronicznych** aplikacji webowych. Został wprowadzony w 2003 roku (PEP 333, później PEP 3333) i stał się absolutnym standardem w świecie Pythona.
- **ASGI** to nowszy standard, stworzony jako ewolucja i duchowy następca WSGI. Ma zastosowanie w **asynchronicznych** aplikacjach webowych, które muszą wydajnie obsługiwać dziesiątki tysięcy jednoczesnych połączeń, np. przy użyciu WebSockets, long-polling, czy strumieniowaniu w czasie rzeczywistym.

## Jak to działa?

### 1. WSGI (Web Server Gateway Interface)

W modelu WSGI żądania są przetwarzane **synchronicznie**. Oznacza to, że jeden wątek roboczy (worker) obsługuje tylko jedno żądanie w danym czasie. Jeśli worker wysyła zapytanie do bazy danych, blokuje się i czeka na odpowiedź. W tym czasie nie może obsługiwać innych użytkowników.

Interfejs WSGI wymaga, aby aplikacja była funkcją (lub obiektem wywoływalnym), która przyjmuje dwa argumenty.

**Przykład prostej aplikacji WSGI:**
```python
def application(environ, start_response):
    # environ: słownik zawierający dane żądania (np. ścieżka, nagłówki, zmienne środowiskowe)
    # start_response: funkcja inicjująca odpowiedź (zwraca status HTTP i nagłówki)
    
    status = '200 OK'
    headers = [('Content-Type', 'text/plain; charset=utf-8')]
    
    # Inicjalizacja odpowiedzi
    start_response(status, headers)
    
    # Zwracana jest wartość iterowalna (np. lista) z ciągami bajtów (body)
    return [b"Witaj ze swiata WSGI!"]
```

- **Popularne frameworki WSGI:** Flask, tradycyjne Django, Pyramid, Bottle.
- **Popularne serwery WSGI:** Gunicorn, uWSGI, Waitress.

### 2. ASGI (Asynchronous Server Gateway Interface)

ASGI zostało zaprojektowane z myślą o asynchroniczności (korzystając z pętli zdarzeń, zazwyczaj `asyncio`). Dzięki temu jeden worker może obsługiwać tysiące żądań współbieżnie. Gdy jedno żądanie czeka na odpowiedź z zewnętrznego API (operacja wejścia/wyjścia - I/O bound), worker nie blokuje się, ale przełącza się na obsługę kolejnego żądania.

Interfejs ASGI opiera się na coroutine'ach (funkcjach `async def`) i przyjmuje trzy argumenty.

**Przykład prostej aplikacji ASGI:**
```python
async def application(scope, receive, send):
    # scope: słownik z informacjami o połączeniu i żądaniu (podobny do environ)
    # receive: asynchroniczna funkcja do odbierania wiadomości od serwera (np. ciało HTTP, wiadomości WebSocket)
    # send: asynchroniczna funkcja do wysyłania wiadomości do serwera
    
    if scope['type'] == 'http':
        # Rozpoczęcie wysyłania odpowiedzi
        await send({
            'type': 'http.response.start',
            'status': 200,
            'headers': [(b'content-type', b'text/plain; charset=utf-8')],
        })
        # Wysłanie treści odpowiedzi
        await send({
            'type': 'http.response.body',
            'body': b"Witaj ze swiata ASGI!",
        })
```

- **Popularne frameworki ASGI:** FastAPI, Starlette, Quart, nowoczesne Django (od wersji 3.0).
- **Popularne serwery ASGI:** Uvicorn, Daphne, Hypercorn.

## Podsumowanie - co wybrać?

- Używaj **WSGI**, jeśli Twoja aplikacja jest czysto synchroniczna, nie potrzebuje WebSockets i opiera się na klasycznych rozwiązaniach i bibliotekach, które są blokujące z natury.
- Wybierz **ASGI**, jeśli planujesz używać asynchronicznego kodu w celu lepszego radzenia sobie z operacjami wejścia/wyjścia (I/O) i skalowania, a także kiedy korzystasz z nowoczesnych frameworków takich jak FastAPI lub budujesz system czasu rzeczywistego (np. czat, streaming wideo).

## Powiązane tematy
- [Async i Await w Pythonie](async-await-w-pythonie.md)
- [Opisz async i await w Python](opisz-async-i-await-w-python.md)
- [Błąd modułu FastAPI](błąd-modułu-fastapi.md)
