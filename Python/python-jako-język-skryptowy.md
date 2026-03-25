# Python jako język skryptowy

**Data:** 2026-02-05

---

**User:**

dlaczego pythona opisuje się często jako język skryptowy, interpretowalny?

---

**Assistant:**

To określenie jest historyczne i częściowo mylące, ale ma techniczne uzasadnienie.

Python **nie jest „czysto interpretowany”** w sensie akademickim. Jest językiem **kompilowanym do bytecode**, który następnie jest **interpretowany przez maszynę wirtualną (PVM — Python Virtual Machine)**.

Dlatego mówi się o nim jednocześnie:

- *język skryptowy*
- *język interpretowany*
- a rzadziej, ale poprawniej: *język kompilowany do bytecode + VM*

### Co faktycznie dzieje się przy uruchomieniu pliku `.py`

1. Kod źródłowy → kompilacja do **bytecode** (`.pyc`)
2. Bytecode → wykonywany przez **interpreter Pythona (VM)**

Ten krok kompilacji jest:
- automatyczny
- niewidoczny
- bardzo szybki
- bez osobnego etapu build

To daje wrażenie, że „Python się interpretuje”.

---

### Dlaczego mówi się „język skryptowy”

Historycznie „języki skryptowe” to były języki:

- bez etapu kompilacji widocznego dla programisty
- używane do automatyzacji (shell, Perl, Tcl, Python)
- dynamicznie typowane
- łatwe do uruchomienia jednym poleceniem

Python idealnie wpasował się w tę kategorię, mimo że **pod spodem działa jak JVM**.

W praktyce:

| Cecha | C / Java | Python |
|---|---|---|
| jawny build | tak | nie |
| generuje kod pośredni | Java tak | Python tak |
| VM | JVM | PVM |
| plik wykonywalny | .class/.jar | .pyc (ukryty) |
| odczucie programisty | kompilacja | interpretacja |

To **UX uruchamiania** decyduje o tej etykiecie, nie architektura.

---

### Dlaczego mówi się „interpretowany”

Bo:

- kod nie jest tłumaczony do natywnego kodu maszynowego przed uruchomieniem
- wykonuje go interpreter VM
- można wykonywać linia po linii (REPL)

To spełnia klasyczną definicję języka interpretowanego z lat 80/90.

---

### Dlaczego to jest dziś nieprecyzyjne

Bo Python jest bliżej **Javy niż Basha**:

- ma kompilator
- ma bytecode
- ma VM
- ma cache `.pyc`
- ma loader, linker, runtime

Technicznie:

> Python = **bytecode-compiled, VM-interpreted language**

---

### Dlaczego ta narracja się utrzymała

Marketing + historia + zastosowania:

- Python był używany jako glue language, skrypty administracyjne
- był alternatywą dla Perla i Basha
- nie był postrzegany jako język do „poważnych systemów”

Ta łatka została, mimo że architektura jest poważna i bardzo zbliżona do JVM.

---

### Najbardziej poprawne określenie (technicznie)

> Python jest językiem kompilowanym do bytecode wykonywanego przez maszynę wirtualną.

Ale to nie brzmi tak chwytliwie jak „język skryptowy, interpretowany”, więc uproszczenie wygrało.

---

### Ciekawostka, która to dobrze pokazuje

Gdy usuniesz pliki `.py` i zostawisz `.pyc` — program nadal działa.

To nie jest możliwe w prawdziwie interpretowanym języku.

---

**User:**

czy tworząc serwery API np. w fastapi, taka aplikacja w pythonie jest przygotowana na bardzo dużo równoległych requestów? czy to w ogóle jest skalowalne? z uwagi na GIL wątpię że tak jest chyba że używa się multitaskingu

---

**Assistant:**

Krótka odpowiedź: **tak, FastAPI potrafi obsłużyć bardzo dużą liczbę równoległych requestów i jest normalnie skalowalne w produkcji** — ale **nie dzięki wątkom**, tylko dzięki:

- asynchronicznemu I/O (event loop),
- wieloprocesowości,
- oraz temu, że GIL **nie ma znaczenia** dla typowego API I/O-bound.

Twoja intuicja o GIL jest słuszna… ale dotyczy **CPU-bound**, a większość API jest **I/O-bound**.

---

## Co naprawdę robi FastAPI pod spodem

Stack wygląda tak:

```
FastAPI
  ↓
Starlette (ASGI)
  ↓
Uvicorn / Hypercorn (ASGI server)
  ↓
asyncio / uvloop (event loop)
```

To jest **czysty model event-loop**, jak w Node.js, nie model wątków.

Jeden worker ≠ jeden request.

Jeden worker potrafi trzymać **tysiące otwartych requestów** równocześnie, bo:

- czeka na DB
- czeka na HTTP
- czeka na Redis
- czeka na IO

i w tym czasie obsługuje inne.

---

## Dlaczego GIL tu nie przeszkadza

GIL blokuje tylko gdy:

> Python wykonuje bytecode CPU-bound

Natomiast gdy kod robi:

- `await db.fetch()`
- `await httpx.get()`
- `await redis.get()`
- `await sleep()`

to interpreter **oddaje GIL** i event loop obsługuje inne korutyny.

Dla API to jest 90% czasu.

---

## Co się dzieje przy 10 000 równoległych requestów

Przy dobrze napisanym async kodzie:

- 1 worker uvicorn może obsłużyć tysiące jednoczesnych połączeń
- bez tworzenia tysięcy wątków
- bez kosztów context switch

To dokładnie ten sam model, który dał Node.js sławę.

---

## Kiedy GIL staje się problemem

Gdy w endpoint wrzucisz:

```python
for _ in range(10**9):
    ...
```

albo:

- parsowanie dużych JSONów
- kompresję
- szyfrowanie
- ML inference
- generowanie PDF
- cokolwiek CPU-heavy

Wtedy **blokujesz cały worker**.

I tu wiele osób myśli: „Python się nie skaluje”.

Nie — po prostu użyli złego modelu do złego typu pracy.

---

## Jak to się robi poprawnie w produkcji

### 1. Skalowanie przez procesy (nie wątki)

```
gunicorn -k uvicorn.workers.UvicornWorker -w 8 app:app
```

Masz 8 procesów → 8 GIL → liniowe skalowanie CPU.

To dokładnie to, co robi Node w cluster mode.

---

### 2. CPU-bound wyrzucasz poza event loop

- Celery / RQ / Dramatiq
- osobny microservice
- threadpool / processpool executor

API robi tylko orchestration I/O.

---

### 3. DB i HTTP klient muszą być async

To jest kluczowe. Jeśli użyjesz:

- psycopg2 ❌
- requests ❌

to zabijesz skalowalność.

Musisz mieć:

- asyncpg
- httpx (async)
- aioredis
- itd.

---

## Dlaczego FastAPI jest dziś używane w systemach high-throughput

Bo architektura jest **lepsza od klasycznych wątkowych serwerów Javy** dla I/O:

| Model | Koszt |
|---|---|
| Java thread per request | duży narzut pamięci + context switch |
| Python async event loop | minimalny narzut |

Dlatego przy I/O FastAPI potrafi mieć **lepszą przepustowość na rdzeń niż Spring MVC**.

---

## Gdzie Python przegrywa

W systemach typu:

- trading engine
- silnik gier
- heavy compute API
- image processing API bez offloadu

Czyli CPU-bound.

---

## Mentalny model, który jest poprawny

FastAPI ≈ Node.js, nie ≈ Java servlet.

GIL ≈ nieistotny dla API, bardzo istotny dla obliczeń.

---

## Prawdziwa odpowiedź na Twoje pytanie

> Czy FastAPI jest przygotowane na bardzo dużo równoległych requestów?

Tak — **jeśli kod jest async i I/O-bound**.

> Czy jest skalowalne?

Tak — przez procesy + event loop.

> Czy GIL jest problemem?

Tylko gdy robisz w API to, czego robić nie powinieneś.