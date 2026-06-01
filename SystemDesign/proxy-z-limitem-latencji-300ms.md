# Proxy z limitem latencji 300 ms na wiadomość

Opis problemu projektowego i potencjalnych rozwiązań dla aplikacji proxy, która musi przetwarzać i przekazywać wiadomości z **maksymalnym opóźnieniem 300 ms** od momentu odebrania do dostarczenia do systemu docelowego.

---

## Opis problemu

Aplikacja proxy pełni rolę pośrednika między klientem (producentem) a systemem docelowym (konsumentem). Każda wiadomość trafiająca do proxy musi zostać przetworzona — np. zwalidowana, wzbogacona, zlogowana — i przekazana dalej **w czasie nie dłuższym niż 300 ms** (end-to-end na proxy, czyli od momentu odebrania request'a do wysłania response'a lub przekazania wiadomości downstream).

### Dlaczego to jest trudne?

1. **Wąskie okno czasowe.** 300 ms to zaledwie tyle, ile trwa jedno mrugniecie oka. Musi wystarczyć na:
   - Deserializację wiadomości (parsing payloadu).
   - Walidację i ewentualne wzbogacenie (enrichment) danych.
   - Komunikację sieciową z systemem docelowym (downstream latency).
   - Serializację odpowiedzi i odesłanie jej klientowi.

2. **Zmienność latencji downstream.** System docelowy może odpowiadać w 10 ms, ale też w 250 ms pod obciążeniem — co drastycznie ogranicza budżet czasowy na przetwarzanie wewnętrzne proxy.

3. **Tail latency (p99/p999).** Utrzymanie limitu 300 ms nie na średniej, lecz na percentylach p99 czy p999 wymaga eliminacji wszelkich „długich ogonów" — GC pauz, lock contention, cold startów połączeń.

4. **Skalowalność pod obciążeniem.** Przy gwałtownym wzroście ruchu (spike'ach) proxy nie może przekroczyć budżetu, nawet jeśli CPU i pamięć zbliżają się do limitów.

---

## Budżet latencji (Latency Budget)

Kluczową techniką projektową jest **rozbicie 300 ms na „budżet" dla każdego etapu** przetwarzania, co pozwala monitorować, gdzie czas jest konsumowany:

```
┌──────────────────────────────────────────────────────────────────┐
│                       Budżet 300 ms                              │
│                                                                  │
│  [Receive]  [Parse]  [Validate]  [Enrich]  [Forward]  [Respond]  │
│    10 ms     15 ms     20 ms      25 ms     200 ms      30 ms    │
│                                                                  │
│  ◄─────────── Przetwarzanie lokalne ──────────►  ◄── Sieć ──►   │
│               ~70 ms                                ~230 ms      │
└──────────────────────────────────────────────────────────────────┘
```

Największy „konsument" budżetu to zwykle **komunikacja z systemem docelowym** (Forward). Cała logika wewnętrzna proxy musi zmieścić się w pozostałym marginesie.

---

## Rozwiązanie architektoniczne

### 1. Model współbieżności oparty na nieblokującym I/O (Non-blocking / Event-driven)

Proxy **nie może** używać klasycznego modelu „wątek per request", gdzie każdy wątek blokuje się czekając na odpowiedź downstream. Przy tysiącach jednoczesnych połączeń prowadzi to do wyczerpania puli wątków i dramatycznego wzrostu latencji z powodu context switchingu.

**Rozwiązanie:** Zastosowanie modelu reaktywnego / event-loop:
- **Java:** Project Reactor / WebFlux (Netty pod spodem), Vert.x.
- **Go:** Goroutyny z natywnym multipleksowaniem I/O.
- **Node.js:** Natywny event loop (libuv).
- **C/C++:** epoll/kqueue z bibliotekami typu libevent, libuv.

Dzięki temu tysiące współbieżnych wiadomości mogą być przetwarzane na kilku wątkach bez blokowania, a każda z nich wykorzystuje pełnię dostępnego budżetu.

Ważne doprecyzowanie: **event loop nie oznacza, że cała aplikacja działa na jednym wątku**. Jeden event loop to zwykle jeden wątek obsługujący operacje I/O, ale produkcyjny serwer ma najczęściej **grupę event loopów** — np. 4, 8 albo 16 wątków, często dobranych do liczby rdzeni CPU. Każdy taki wątek obsługuje wiele połączeń naraz, ponieważ gdy request czeka na odpowiedź z downstream, wątek nie śpi zablokowany na `read()`/`recv()`, tylko wraca do obsługi innych socketów. System operacyjny informuje go później mechanizmem typu `epoll`/`kqueue`/IOCP, że dane są gotowe.

To różni się od klasycznej puli wątków „jeden request = jeden aktywny wątek”. Pula wątków uruchomiona cały czas nadal ma problem, jeśli te wątki blokują się na I/O. Przy 10 000 jednoczesnych requestów i downstream latency 200 ms potrzebowalibyśmy ogromnej liczby wątków tylko po to, żeby większość z nich czekała. To zużywa pamięć na stosy, powoduje context switching i zwiększa tail latency. W modelu nieblokującym te same 10 000 requestów może być „w toku”, ale tylko te, które akurat mają gotowe dane albo wykonują krótki fragment CPU, zajmują wątek.

To nie znaczy, że pula wątków jest zła. Jest potrzebna, ale do innych rzeczy:
- **Event loop / I/O threads:** obsługa socketów, parsowanie prostych ramek, przekazywanie requestów dalej. Te wątki nie powinny wykonywać długich ani blokujących operacji.
- **Worker pool:** cięższe CPU-bound operacje, np. kosztowna walidacja, kompresja, kryptografia, transformacja dużego payloadu.
- **Osobna pula dla legacy blocking I/O:** jeśli musimy wywołać bibliotekę lub klienta, który blokuje wątek, izolujemy to w dedykowanej puli z twardym limitem i timeoutem.

Praktyczny model to więc nie „jeden event loop zamiast puli wątków”, tylko **mała pula event loopów do nieblokującego I/O plus kontrolowane pule workerów do pracy, której nie da się wykonać nieblokująco**. Kluczowe jest to, żeby wątek I/O nigdy nie czekał bezczynnie na zewnętrzny system, bo wtedy tracimy największą zaletę tego modelu.

```
┌───────────────────────────────────────────────────────┐
│               Proxy – model reaktywny                 │
│                                                       │
│   Klient A ──►┐                                       │
│   Klient B ──►├──► Event Loop ──► [Pipeline] ──► Out  │
│   Klient C ──►┘    (non-blocking)                     │
│                                                       │
│   Wątki: 2–4 (CPU cores)                              │
│   Jednoczesne połączenia: dziesiątki tysięcy           │
└───────────────────────────────────────────────────────┘
```

### 2. Wybór języka programowania i runtime'u

Wybór języka ma znaczenie, bo przy limicie 300 ms liczy się nie tylko średni czas wykonania kodu, ale też **stabilność p99/p999**, narzut runtime'u, model współbieżności, GC, koszt serializacji i dojrzałość bibliotek sieciowych.

**Rust** jest bardzo dobrym wyborem dla takiego proxy, jeśli zespół potrafi go utrzymać:
- Brak garbage collectora, więc odpadają pauzy GC wpływające na tail latency.
- Bardzo niski narzut runtime'u i przewidywalne zużycie pamięci.
- Dobre biblioteki async I/O, np. Tokio, Hyper, Axum.
- Łatwiej utrzymać wysoką przepustowość przy małym koszcie CPU.

Minusem Rust'a jest koszt developmentu: trudniejszy język, dłuższy onboarding, bardziej wymagające debugowanie problemów z lifetimes, ownership i async. W systemach latency-critical to może się opłacać, ale nie zawsze jest najlepszym wyborem organizacyjnie.

**Go** jest często najbardziej pragmatycznym wyborem:
- Goroutyny są tanie i dobrze pasują do dużej liczby jednoczesnych requestów.
- Standardowa biblioteka HTTP jest dojrzała i szybka.
- Deployment jest prosty.
- GC istnieje, ale przy dobrze napisanym kodzie i umiarkowanych alokacjach zwykle da się utrzymać niskie pauzy.

Go bywa dobrym kompromisem między wydajnością Rust'a a szybkością developmentu.

**Java/Kotlin na Netty/WebFlux/Vert.x** też są sensownym wyborem:
- Bardzo dojrzały ekosystem sieciowy.
- Dobre narzędzia do observability, connection pooling, backpressure i tuningu.
- ZGC/Shenandoah potrafią ograniczyć pauzy GC.

Ryzykiem jest większy narzut pamięciowy i konieczność pilnowania alokacji, GC oraz blokujących operacji w reaktywnym pipeline.

**Python może się nadawać, ale tylko w ograniczonych warunkach.** Nie jest pierwszym wyborem dla proxy z twardym limitem 300 ms przy dużej skali i wymaganiach p99/p999. Główne problemy:
- Wyższy narzut wykonania kodu niż w Rust/Go/Java.
- GIL ogranicza równoległe wykonywanie CPU-bound kodu w jednym procesie.
- Większe ryzyko niestabilnej tail latency przez GC, alokacje i dynamiczny runtime.
- Łatwo przypadkowo użyć blokującej biblioteki w async endpointcie i zablokować event loop.

Python może być akceptowalny, jeśli:
- Proxy wykonuje bardzo mało logiki CPU-bound.
- Większość czasu i tak idzie na oczekiwanie na downstream.
- Używamy prawdziwego async I/O, np. `asyncio`, `uvloop`, `aiohttp`/`httpx.AsyncClient`, FastAPI/Starlette uruchomione na Uvicornie.
- Uruchamiamy wiele procesów workerów, np. przez Gunicorn/Uvicorn, żeby obejść ograniczenie jednego procesu i lepiej wykorzystać rdzenie.
- Mamy twarde timeouty, connection pooling, limity współbieżności i bardzo dobrą obserwowalność.

Przykładowo Python może wystarczyć dla umiarkowanego ruchu, prostego routingu i downstream latency rzędu 100-200 ms, gdzie lokalne przetwarzanie trwa kilka milisekund. Natomiast jeśli proxy musi obsługiwać bardzo duży RPS, ciężką walidację, transformację payloadów, kompresję, kryptografię albo SLA na p99 blisko 300 ms, Python staje się ryzykowny.

Praktyczna rekomendacja:

| Język / runtime | Ocena dla proxy 300 ms | Kiedy wybrać |
|---|---|---|
| Rust | Bardzo dobry technicznie | Gdy liczy się minimalna latencja, niski narzut i zespół zna Rust'a |
| Go | Bardzo dobry pragmatycznie | Gdy potrzebna jest wysoka wydajność i szybki development |
| Java/Kotlin + Netty/WebFlux | Dobry | Gdy zespół ma mocny JVM stack i umie stroić GC/reaktywność |
| Node.js | Warunkowo dobry | Gdy logika jest głównie I/O-bound i nie blokujemy event loopa |
| Python | Warunkowo akceptowalny | Gdy ruch jest umiarkowany, logika lekka, a async jest konsekwentnie użyty |

Najważniejsza zasada: **język nie uratuje złej architektury, ale zły runtime może zjeść margines latencji**. Dla systemu z limitem 300 ms Python nie jest automatycznie wykluczony, ale wymaga ostrożności i zwykle ma mniejszy zapas bezpieczeństwa niż Rust, Go czy dobrze skonfigurowana JVM.

### 3. Connection pooling i keep-alive do downstream

Ustanawianie nowego połączenia TCP (a tym bardziej TLS handshake) przy każdej wiadomości pochłania od 30 do 150 ms. To niedopuszczalne w budżecie 300 ms.

**Rozwiązanie:**
- **Pula połączeń (Connection Pool):** Utrzymywanie aktywnych, gotowych połączeń z systemem docelowym. Wiadomość trafia natychmiast na wolne połączenie z puli.
- **HTTP/2 multiplexing:** Jeśli downstream wspiera HTTP/2, wiele wiadomości przechodzi jednym połączeniem TCP, eliminując overhead ustanawiania nowych połączeń.
- **Keep-alive i health check:** Regularne sprawdzanie zdrowia połączeń w puli, usuwanie martwych, utrzymywanie pre-warmed connections.

### 4. Timeout propagation i deadline budgeting

Proxy musi aktywnie zarządzać limitem czasu na każdym etapie przetwarzania:

- **Globalny deadline:** Od momentu odebrania wiadomości startuje zegar 300 ms. Każdy kolejny etap otrzymuje budżet = `300 ms - czas_już_zużyty`.
- **Downstream timeout:** Jeśli po przejściu walidacji i enrichmentu zostało np. 210 ms, to timeout na połączenie z downstream wynosi **210 ms**, nie więcej.
- **Fail-fast:** Jeśli przed rozpoczęciem etapu `Forward` budżet jest już wyczerpany (np. enrichment był wyjątkowo wolny), proxy **natychmiast zwraca błąd** klientowi zamiast próbować bezcelowej komunikacji downstream.

```java
// Pseudokod deadline propagation
Instant deadline = Instant.now().plusMillis(300);

Message parsed = parse(request);                    // ~15 ms
validate(parsed);                                    // ~20 ms

long remainingMs = Duration.between(Instant.now(), deadline).toMillis();
if (remainingMs <= 0) {
    return Response.timeout("Budget exceeded before forwarding");
}

// Downstream call z dynamicznym timeoutem
Response downstream = httpClient.send(parsed, Timeout.ofMillis(remainingMs - 30)); 
// -30 ms rezerwujemy na serializację odpowiedzi
```

### 5. Przeniesienie ciężkich operacji poza ścieżkę krytyczną (Off the hot path)

Wszystko, co **nie jest wymagane** do udzielenia odpowiedzi w 300 ms, musi zostać zdjęte ze ścieżki krytycznej:

| Operacja | Na ścieżce krytycznej? | Strategia |
|---|---|---|
| Walidacja schematu | ✅ Tak | Zoptymalizowane walidatory (skompilowane schematy) |
| Logowanie pełnej wiadomości | ❌ Nie | Asynchroniczny zapis do bufora / kolejki logów |
| Metryki i tracing | ❌ Nie | Fire-and-forget do kolektora (OpenTelemetry) |
| Enrichment z bazy danych | ⚠️ Warunkowo | Cache w pamięci (Caffeine / local HashMap) z TTL |
| Audyt compliance | ❌ Nie | Emitowanie zdarzenia na kolejkę (Kafka) |

**Kluczowa zasada:** Ścieżka krytyczna powinna wykonywać **zero operacji dyskowych** i **zero synchronicznych wywołań** do usług pobocznych.

### 6. Cache w pamięci (in-memory cache) dla enrichmentu

Jeśli proxy musi wzbogacać wiadomości danymi referencyjnymi (np. mapowanie ID klienta na region), odpytywanie bazy lub innego serwisu na każdą wiadomość to samobójstwo budżetowe.

**Rozwiązanie:**
- **Cache lokalny** (np. Caffeine w Javie, Guava Cache, `sync.Map` w Go) z krótkim TTL (5–60 s).
- **Proaktywne odświeżanie** (refresh-ahead): cache odświeża dane w tle przed ich wygaśnięciem, dzięki czemu żaden request nie czeka na „cold miss".
- **Rozmiar cache'a** należy ograniczyć (max entries) i monitorować hit ratio — cel: >95%.

### 7. Backpressure i ochrona przed przeciążeniem

Gdy system docelowy zaczyna odpowiadać wolniej niż zwykle, proxy musi się **bronić**, a nie kumulować opóźnienia:

- **Rate limiting na wejściu:** Token Bucket lub Sliding Window na poziomie proxy ogranicza liczbę przyjmowanych wiadomości per sekundę.
- **Circuit Breaker na downstream:** Gdy procent timeoutów do downstream przekroczy próg (np. >50% w oknie 10 s), obwód się otwiera — proxy natychmiast zwraca `503 Service Unavailable` zamiast konsumować budżet na próżno.
- **Adaptive concurrency limits:** Dynamiczne dostosowywanie limitu jednoczesnych połączeń do downstream na podstawie mierzonej latencji (np. algorytm AIMD — Additive Increase Multiplicative Decrease, popularyzowany przez Netflix Concurrency Limits).

```
              Normalny ruch                    Spike / degradacja downstream
         ┌─────────────────────┐          ┌─────────────────────────────┐
         │  Proxy przetwarza   │          │  Circuit Breaker OPEN       │
         │  100% wiadomości    │          │  → 503 dla nowych           │
         │  Latency: ~120 ms   │          │  → Retry po cooldown        │
         └─────────────────────┘          │  → Alert do on-call         │
                                          └─────────────────────────────┘
```

### 8. Optymalizacja GC i alokacji pamięci (JVM-specific)

Na platformie JVM pauzy Garbage Collectora mogą dodawać od 5 ms do nawet 200 ms do tail latency. Techniki minimalizacji:

- **Low-latency GC:** ZGC (pauzy <1 ms) lub Shenandoah zamiast domyślnego G1.
- **Object pooling:** Ponowne użycie buforów bajtowych (`ByteBuffer`) i obiektów wiadomości zamiast ciągłej alokacji.
- **Off-heap memory:** Przechowywanie dużych payloadów poza stertą JVM (np. Netty `DirectByteBuf`), co zmniejsza presję na GC.
- **Unikanie autoboxingu:** Wykorzystanie primitive collections (Eclipse Collections, HPPC) zamiast `HashMap<Integer, Long>`.

### 9. Monitoring i alertowanie na budżet latencji

Nie da się utrzymać limitu 300 ms bez **ciągłego monitoringu**:

- **Metryki histogramowe:** Zbieranie percentyli latencji (p50, p90, p95, p99) per etap przetwarzania, nie tylko średniej.
- **Alerty na p99:** Alert gdy p99 latencji proxy > 250 ms (margines ostrzegawczy przed przekroczeniem 300 ms).
- **Distributed tracing:** Każda wiadomość ma trace ID, pozwalający prześledzić, który etap (parse → validate → enrich → forward → respond) konsumuje najwięcej budżetu.
- **Dashboard z breakdown:** Wizualizacja budżetu czasowego per etap w czasie rzeczywistym (np. Grafana z Prometheus).

---

## Wzorzec odporności: co robić, gdy 300 ms jest zagrożone?

Scenariusze awaryjne i odpowiadające im strategie:

| Scenariusz | Strategia |
|---|---|
| Downstream odpowiada w >250 ms | Circuit Breaker otwiera się, proxy zwraca 503 |
| Enrichment cache miss | Graceful degradation: przekaż wiadomość bez wzbogacenia |
| GC pauza >50 ms | Zmiana na ZGC, monitoring allocation rate |
| Spike ruchu 10x | Autoscaling + rate limiting na wejściu |
| Wiadomość jest zbyt duża | Limit rozmiaru payloadu na wejściu (np. max 1 MB) |
| DNS resolution wolne | Cache DNS lokalnie (TTL 30 s), unikanie DNS per request |

---

## Podsumowanie kluczowych zasad

1. **Budżetuj czas** — rozbij 300 ms na etapy i monitoruj każdy z osobna.
2. **Nie blokuj** — używaj asynchronicznego, nieblokującego I/O.
3. **Utrzymuj połączenia** — connection pool + keep-alive + HTTP/2 multiplexing.
4. **Zdejmij z hot path** — logowanie, audyt, metryki poza ścieżką krytyczną.
5. **Cacheuj agresywnie** — enrichment z pamięci, nie z sieci.
6. **Broń się przed przeciążeniem** — circuit breaker, rate limiter, adaptive concurrency.
7. **Eliminuj tail latency** — low-latency GC, object pooling, off-heap.
8. **Monitoruj na percentylach** — p99, nie średnia, decyduje o dotrzymaniu SLA.

---

## Powiązane materiały

- [System Design: Pytania Rekrutacyjne](system-design-pytania-rekrutacyjne.md)
- [Mikroserwisy: Pytania Rekrutacyjne](mikroserwisy-pytania-rekrutacyjne.md)
