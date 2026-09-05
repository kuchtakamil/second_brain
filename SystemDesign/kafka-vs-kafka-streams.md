# Kafka Consumer/Producer API vs Kafka Streams — kiedy użyć czego?

## Krótkie podsumowanie
Apache Kafka oferuje dwa sposoby pracy z danymi: niskopoziomowe **Consumer/Producer API** oraz bibliotekę przetwarzania strumieniowego **Kafka Streams**. Nie konkurują ze sobą — działają na różnych poziomach abstrakcji. Consumer/Producer API to „surowe" narzędzie do wysyłania i odbierania wiadomości, natomiast Kafka Streams to biblioteka kliencka (JVM), która **na bazie tych samych API** dostarcza deklaratywny DSL do transformacji, agregacji, joinów i okienkowania (windowing) z wbudowanym zarządzaniem stanem i exactly-once semantics.

## Dlaczego to ma znaczenie?
Wybór złego poziomu abstrakcji oznacza albo:
*   **Niepotrzebny nakład pracy** — pisanie setek linii kodu na ręczne zarządzanie stanem, offsetami i okienkami, gdy Kafka Streams robi to out-of-the-box.
*   **Niepotrzebną złożoność** — wciąganie Kafka Streams do scenariusza, w którym wystarczy prosty consumer, który czyta wiadomość i zapisuje do bazy.

Zrozumienie granicy między nimi pozwala dobrać narzędzie do problemu, zamiast wymyślać koło na nowo.

## Jak działają — kluczowe różnice

### Consumer/Producer API — niskopoziomowa kontrola

Consumer i Producer API to fundament Kafki. Producent serializuje rekord i wysyła go na partycję topiku. Konsument odpytuje brokera (`poll()`), przetwarza rekordy i commituje offset.

**Co dostajesz:**
*   Pełną kontrolę nad pollingiem, commitowaniem offsetów i partycjonowaniem.
*   Możliwość pracy w **dowolnym języku** (Java, Python, Go, C#, …).
*   Lekkość — żadnych dodatkowych zależności poza klientem Kafki.

**Czego NIE dostajesz (musisz zrobić sam):**
*   Zarządzanie stanem (np. liczniki, agregaty) — potrzebujesz zewnętrznej bazy (Redis, Postgres).
*   Okienkowanie czasowe (windowing) — ręczna logika wygaszania starych wpisów.
*   Joiny między topikami — ręczna korelacja danych.
*   Exactly-once semantics — możliwe, ale wymagają ręcznej koordynacji transakcji.
*   Fault tolerance stanu — jeśli aplikacja padnie, musisz sam odbudować stan.

```java
// Prosty consumer — odczyt i zapis do bazy
try (KafkaConsumer<String, String> consumer = new KafkaConsumer<>(props)) {
    consumer.subscribe(List.of("orders"));
    while (true) {
        ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(100));
        for (ConsumerRecord<String, String> record : records) {
            // prosta logika: odczyt → działanie
            orderRepository.save(parseOrder(record.value()));
        }
        consumer.commitSync();
    }
}
```

---

### Kafka Streams — deklaratywne przetwarzanie strumieniowe

Kafka Streams to **biblioteka kliencka** (nie osobny klaster!), która działa wewnątrz Twojej aplikacji JVM. Pod spodem korzysta z Consumer/Producer API, ale abstrahuje zarządzanie stanem, rebalansowanie i fault recovery.

**Co dostajesz:**
*   **KStream** — nieskończony strumień rekordów (każdy rekord to niezależne zdarzenie).
*   **KTable** — materializowany widok ostatniego stanu dla danego klucza (changelog).
*   **GlobalKTable** — replika pełnego topiku na każdej instancji (lookup table).
*   **State Stores** — lokalny magazyn stanu (domyślnie RocksDB), automatycznie backupowany do changelog topiców w Kafce.
*   **Windowing** — okienka czasowe, sesyjne i sliding jednym wywołaniem.
*   **Joiny** — stream-stream, stream-table, table-table.
*   **Exactly-once semantics** — wbudowane (processing.guarantee=exactly_once_v2).
*   **Automatyczny fault recovery** — po awarii stan jest odbudowywany z changelog topiku.

```java
// Kafka Streams — zliczanie zamówień per klient w okienku 5 minut
StreamsBuilder builder = new StreamsBuilder();

builder.<String, Order>stream("orders")
    .filter((key, order) -> order.getStatus() == Status.COMPLETED)
    .groupByKey()
    .windowedBy(TimeWindows.ofSizeWithNoGrace(Duration.ofMinutes(5)))
    .count(Materialized.as("orders-per-customer-5min"))
    .toStream()
    .to("order-counts");

KafkaStreams streams = new KafkaStreams(builder.build(), config);
streams.start();
```

> Powyższy kod robi to, co w surowym Consumer API wymagałoby ~200 linii kodu + zewnętrzny store + ręczna logika okienkowania.

## Porównanie w tabeli

| Cecha | **Consumer/Producer API** | **Kafka Streams** |
|---|---|---|
| **Typ** | Niskopoziomowe API klienta | Biblioteka przetwarzania strumieniowego |
| **Język** | Dowolny (Java, Python, Go…) | JVM (Java, Kotlin, Scala) |
| **Infrastruktura** | Tylko klient Kafki | Tylko klient Kafki (bez osobnego klastra!) |
| **Zarządzanie stanem** | Ręczne (zewnętrzny store) | Wbudowane (RocksDB + changelog topics) |
| **Windowing** | Ręczna implementacja | Natywne (Time, Session, Sliding) |
| **Joiny** | Ręczna korelacja | Natywne (stream×stream, stream×table) |
| **Exactly-once** | Możliwe (ręczne transakcje) | Wbudowane (jedna flaga konfiguracji) |
| **Fault tolerance stanu** | Ręczne (backup/restore) | Automatyczne (changelog topics) |
| **Skalowanie** | Ręczne partycjonowanie logiki | Automatyczne (1 task per partycja) |
| **Złożoność kodu** | Wysoka przy logice stanowej | Niska (deklaratywny DSL) |
| **Latencja** | Kontrolowana ręcznie | Niska (ms) — ale zależna od commit interval |
| **Nadaje się do** | Prostych operacji bezstanowych | Złożonych transformacji stanowych |

## Kiedy użyć Consumer/Producer API?

| Scenariusz | Dlaczego surowe API wystarczy |
|---|---|
| Odczyt wiadomości → zapis do bazy danych | Prosta operacja bezstanowa, brak potrzeby joinów/agregacji |
| Wysłanie e-maila / notyfikacji po zdarzeniu | Fire-and-forget, brak stanu |
| Proste przekierowanie z topiku A do topiku B | Brak transformacji stanowej |
| Aplikacja w Pythonie / Go / Rust | Kafka Streams dostępny tylko na JVM |
| Integracja z Kafka Connect sink/source | Connect używa Consumer/Producer pod spodem |
| Potrzeba pełnej kontroli nad offset commit | Ręczne zarządzanie pozycją w logu |
| Batch processing (przetwarzanie wsadowe) | Konsument czyta partię, przetwarza, commituje |

## Kiedy użyć Kafka Streams?

| Scenariusz | Dlaczego Kafka Streams jest lepszym wyborem |
|---|---|
| Zliczanie zdarzeń w okienku czasowym | Wbudowane windowing, brak ręcznej logiki expiry |
| Join strumienia zamówień z topikiem klientów | Natywny KStream–KTable join |
| Wzbogacanie zdarzeń danymi z innego topiku | GlobalKTable jako lookup table |
| Detekcja anomalii w czasie rzeczywistym | Stateful processing + windowing |
| Deduplikacja zdarzeń | State store z TTL jako filtr duplikatów |
| CQRS — materializacja widoków odczytu | KTable automatycznie utrzymuje najnowszy stan per klucz |
| Routing zdarzeń na podstawie logiki biznesowej | `branch()` / `split()` w DSL |
| Exactly-once przetwarzanie end-to-end | Jedna flaga konfiguracji zamiast ręcznych transakcji |

## Drzewo decyzyjne

```
Czy przetwarzanie wymaga stanu (agregacje, joiny, okienka)?
├── NIE → Czy aplikacja jest na JVM?
│         ├── TAK → Consumer/Producer API (lub Kafka Streams, jeśli chcesz DSL)
│         └── NIE → Consumer/Producer API
└── TAK → Czy aplikacja jest na JVM?
          ├── TAK → Kafka Streams ✅
          └── NIE → Consumer API + zewnętrzny state store (Redis/Postgres)
                    lub rozważ Apache Flink / inny framework
```

## Częsty błąd: „użyję Kafka Streams do wszystkiego"

Kafka Streams to **biblioteka procesująca**, nie zamiennik dla każdego consumera. Jeśli Twój use case to:

```
Kafka topic → przeczytaj rekord → zapisz do PostgreSQL
```

…to nie potrzebujesz Kafka Streams. Wystarczy zwykły consumer (albo jeszcze lepiej — **Kafka Connect JDBC Sink**). Wciąganie Kafka Streams dodaje złożoność (state stores, changelog topics, RocksDB), która w tym scenariuszu jest zbędna.

## Częsty błąd: „napiszę sam windowing w Consumer API"

Jeśli Twój use case to:

```
Kafka topic → zlicz eventy per klucz co 5 minut → wynik do innego topiku
```

…to pisanie ręcznego windowing w Consumer API (z `HashMap`, `ScheduledExecutor` i ręcznym flush) jest:
*   **Podatne na błędy** — edge cases przy rebalansowaniu, opóźnionych eventach (late arrivals), awariach.
*   **Nieodporne na awarie** — restart = utrata stanu in-memory.
*   **Niepotrzebne** — Kafka Streams robi to w 5 liniach z fault tolerance.

## A co z alternatywami dla nie-JVM?

Jeśli potrzebujesz przetwarzania stanowego, ale nie jesteś na JVM:

| Alternatywa | Język | Uwagi |
|---|---|---|
| **Apache Flink** | Java/Python/SQL | Osobny klaster, ale potężniejszy niż Kafka Streams |
| **Faust** | Python | Inspirowany Kafka Streams, ale mniej dojrzały |
| **Quix Streams** | Python | Nowoczesna alternatywa, lekka |
| **ksqlDB** | SQL | Kafka Streams pod spodem, ale ekspozycja SQL |
| **Redpanda + WASM transforms** | Dowolny (WASM) | Transformacje inline w brokerze |

## Przykład: system e-commerce — obie warstwy razem

```
[Zamówienie złożone]
       │
       ▼
  Kafka topic: "orders"
       │
       ├── Consumer API (Python)
       │     └── Wysyła e-mail potwierdzenia         ← bezstanowe, prosty consumer
       │
       ├── Kafka Streams (Java)
       │     ├── Join z topikiem "customers"           ← wzbogacenie danych klienta
       │     ├── Windowed count per region (5 min)    ← monitoring w czasie rzeczywistym
       │     └── Wynik → topic "enriched-orders"       ← materializacja
       │
       └── Kafka Connect JDBC Sink
             └── Zapis surowych zamówień do PostgreSQL ← pipeline danych
```

W powyższym przykładzie **Consumer API** obsługuje prostą, bezstanową operację (email), **Kafka Streams** wykonuje złożoną logikę stanową (join + windowing), a **Kafka Connect** zajmuje się integracją z bazą danych — każde narzędzie na swoim poziomie abstrakcji.

## Powiązane pliki
*   [Kafka vs RabbitMQ vs ActiveMQ — porównanie](kafka-rabbitmq-activemq-redis-pubsub.md)
*   [Frameworki replikacji i elekcji](frameworki-replikacji-i-elekcji.md)
*   [Twierdzenie CAP](cap-theorem.md)
*   [Pytania rekrutacyjne z mikroserwisów](mikroserwisy-pytania-rekrutacyjne.md)
