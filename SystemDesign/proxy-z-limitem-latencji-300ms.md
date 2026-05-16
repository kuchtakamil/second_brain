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

### 2. Connection pooling i keep-alive do downstream

Ustanawianie nowego połączenia TCP (a tym bardziej TLS handshake) przy każdej wiadomości pochłania od 30 do 150 ms. To niedopuszczalne w budżecie 300 ms.

**Rozwiązanie:**
- **Pula połączeń (Connection Pool):** Utrzymywanie aktywnych, gotowych połączeń z systemem docelowym. Wiadomość trafia natychmiast na wolne połączenie z puli.
- **HTTP/2 multiplexing:** Jeśli downstream wspiera HTTP/2, wiele wiadomości przechodzi jednym połączeniem TCP, eliminując overhead ustanawiania nowych połączeń.
- **Keep-alive i health check:** Regularne sprawdzanie zdrowia połączeń w puli, usuwanie martwych, utrzymywanie pre-warmed connections.

### 3. Timeout propagation i deadline budgeting

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

### 4. Przeniesienie ciężkich operacji poza ścieżkę krytyczną (Off the hot path)

Wszystko, co **nie jest wymagane** do udzielenia odpowiedzi w 300 ms, musi zostać zdjęte ze ścieżki krytycznej:

| Operacja | Na ścieżce krytycznej? | Strategia |
|---|---|---|
| Walidacja schematu | ✅ Tak | Zoptymalizowane walidatory (skompilowane schematy) |
| Logowanie pełnej wiadomości | ❌ Nie | Asynchroniczny zapis do bufora / kolejki logów |
| Metryki i tracing | ❌ Nie | Fire-and-forget do kolektora (OpenTelemetry) |
| Enrichment z bazy danych | ⚠️ Warunkowo | Cache w pamięci (Caffeine / local HashMap) z TTL |
| Audyt compliance | ❌ Nie | Emitowanie zdarzenia na kolejkę (Kafka) |

**Kluczowa zasada:** Ścieżka krytyczna powinna wykonywać **zero operacji dyskowych** i **zero synchronicznych wywołań** do usług pobocznych.

### 5. Cache w pamięci (in-memory cache) dla enrichmentu

Jeśli proxy musi wzbogacać wiadomości danymi referencyjnymi (np. mapowanie ID klienta na region), odpytywanie bazy lub innego serwisu na każdą wiadomość to samobójstwo budżetowe.

**Rozwiązanie:**
- **Cache lokalny** (np. Caffeine w Javie, Guava Cache, `sync.Map` w Go) z krótkim TTL (5–60 s).
- **Proaktywne odświeżanie** (refresh-ahead): cache odświeża dane w tle przed ich wygaśnięciem, dzięki czemu żaden request nie czeka na „cold miss".
- **Rozmiar cache'a** należy ograniczyć (max entries) i monitorować hit ratio — cel: >95%.

### 6. Backpressure i ochrona przed przeciążeniem

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

### 7. Optymalizacja GC i alokacji pamięci (JVM-specific)

Na platformie JVM pauzy Garbage Collectora mogą dodawać od 5 ms do nawet 200 ms do tail latency. Techniki minimalizacji:

- **Low-latency GC:** ZGC (pauzy <1 ms) lub Shenandoah zamiast domyślnego G1.
- **Object pooling:** Ponowne użycie buforów bajtowych (`ByteBuffer`) i obiektów wiadomości zamiast ciągłej alokacji.
- **Off-heap memory:** Przechowywanie dużych payloadów poza stertą JVM (np. Netty `DirectByteBuf`), co zmniejsza presję na GC.
- **Unikanie autoboxingu:** Wykorzystanie primitive collections (Eclipse Collections, HPPC) zamiast `HashMap<Integer, Long>`.

### 8. Monitoring i alertowanie na budżet latencji

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
