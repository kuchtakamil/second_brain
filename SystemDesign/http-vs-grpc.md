# HTTP (REST) vs gRPC — kiedy użyć czego?

## Krótkie podsumowanie
HTTP REST i gRPC to dwa najpopularniejsze podejścia do komunikacji między serwisami. **REST** opiera się na protokole HTTP/1.1 (lub HTTP/2), formacie JSON i architekturze zasobowej. **gRPC** to framework RPC od Google, który używa HTTP/2 jako transportu, **Protocol Buffers (Protobuf)** jako formatu serializacji i generuje klienta oraz serwer z pliku `.proto`. Nie są to technologie wymienne — działają na różnych poziomach abstrakcji i rozwiązują różne problemy.

## Dlaczego to ma znaczenie?
Wybór protokołu komunikacji wpływa na:
*   **Wydajność** — gRPC jest wielokrotnie szybszy dzięki binarnej serializacji i multipleksowaniu HTTP/2.
*   **Developer experience** — REST jest prostszy do debugowania (curl, Postman), gRPC wymaga specjalnych narzędzi.
*   **Interoperacyjność** — REST jest uniwersalny (przeglądarki, mobile, IoT), gRPC wymaga dedykowanego klienta.
*   **Ewolucję kontraktu** — Protobuf ma wbudowaną kompatybilność wsteczną, JSON nie ma formalnego schematu (chyba że użyjesz OpenAPI).

Zły wybór oznacza albo niepotrzebny narzut wydajnościowy (REST w komunikacji inter-service o niskiej latencji), albo niepotrzebną złożoność (gRPC jako publiczne API dla przeglądarki).

## Jak działają — kluczowe różnice

### HTTP REST — architektura zasobowa

REST (Representational State Transfer) to styl architektoniczny, który mapuje operacje na zasoby za pomocą metod HTTP:

**Co dostajesz:**
*   Prostotę — każdy endpoint to URL, każda odpowiedź to JSON.
*   Uniwersalność — działanie w przeglądarce, curl, Postman, dowolnym języku.
*   Cacheowanie — natywne wsparcie HTTP cache (ETag, Cache-Control).
*   HATEOAS — możliwość nawigacji po API przez linki w odpowiedzi.
*   Czytelność — human-readable format (JSON), łatwe debugowanie.

**Czego NIE dostajesz:**
*   Wydajności binarnej serializacji — JSON jest tekstowy, wolniejszy do parsowania.
*   Typowania kontraktu — brak formalnego schematu (OpenAPI/Swagger to addon, nie natywna cecha).
*   Streamingu — HTTP/1.1 nie wspiera natywnie bidirectional streaming.
*   Generowania kodu — klient musi być napisany ręcznie lub generowany z OpenAPI.

```bash
# Typowe REST API — prosty, czytelny, debugowalny
curl -X POST https://api.example.com/orders \
  -H "Content-Type: application/json" \
  -d '{"customer_id": "c-123", "items": [{"sku": "A1", "qty": 2}]}'

# Odpowiedź — human-readable JSON
{
  "id": "ord-456",
  "status": "CREATED",
  "total": 49.99,
  "_links": {
    "self": "/orders/ord-456",
    "cancel": "/orders/ord-456/cancel"
  }
}
```

---

### gRPC — zdalne wywołanie procedury

gRPC (gRPC Remote Procedure Call) to framework, w którym definiujesz kontrakt w pliku `.proto`, a narzędzie `protoc` generuje klienta i serwer w wybranym języku.

**Co dostajesz:**
*   **Protocol Buffers** — binarna serializacja, 3-10× mniejszy payload niż JSON.
*   **HTTP/2** — multipleksowanie, header compression, bidirectional streaming.
*   **Generowanie kodu** — z jednego pliku `.proto` dostajesz gotowego klienta i serwer w Java, Python, Go, C#, Rust…
*   **4 typy komunikacji** — Unary, Server Streaming, Client Streaming, Bidirectional Streaming.
*   **Deadline/Timeout propagation** — wbudowany mechanizm propagacji timeoutów przez łańcuch serwisów.
*   **Interceptory** — middleware na poziomie frameworka (auth, logging, tracing).
*   **Kompatybilność wsteczna** — Protobuf gwarantuje backward/forward compatibility przez numery pól.

**Czego NIE dostajesz:**
*   Prostoty debugowania — binarny format, nie da się użyć curl (potrzebujesz `grpcurl` lub `grpc-web`).
*   Natywnego wsparcia w przeglądarce — wymagany proxy (Envoy, grpc-web).
*   Cacheowania HTTP — brak natywnych mechanizmów cache (POST na HTTP/2).
*   Czytelności payloadu — Protobuf jest binarny, nie odczytasz go w logach bez dekodera.

```protobuf
// Definicja kontraktu — orders.proto
syntax = "proto3";

package orders;

service OrderService {
  // Unary — jedno żądanie, jedna odpowiedź
  rpc CreateOrder(CreateOrderRequest) returns (OrderResponse);

  // Server streaming — serwer wysyła strumień aktualizacji
  rpc TrackOrder(TrackOrderRequest) returns (stream OrderStatus);

  // Bidirectional streaming — oba kierunki jednocześnie
  rpc LiveChat(stream ChatMessage) returns (stream ChatMessage);
}

message CreateOrderRequest {
  string customer_id = 1;
  repeated OrderItem items = 2;
}

message OrderItem {
  string sku = 1;
  int32 quantity = 2;
}

message OrderResponse {
  string id = 1;
  string status = 2;
  double total = 3;
}
```

```java
// Wygenerowany klient (Java) — typowane, bezpieczne wywołanie
ManagedChannel channel = ManagedChannelBuilder
    .forAddress("order-service", 50051)
    .usePlaintext()
    .build();

OrderServiceGrpc.OrderServiceBlockingStub stub =
    OrderServiceGrpc.newBlockingStub(channel);

OrderResponse response = stub.createOrder(
    CreateOrderRequest.newBuilder()
        .setCustomerId("c-123")
        .addItems(OrderItem.newBuilder().setSku("A1").setQuantity(2))
        .build()
);
```

## Porównanie w tabeli

| Cecha | **HTTP REST** | **gRPC** |
|---|---|---|
| **Protokół** | HTTP/1.1 lub HTTP/2 | HTTP/2 (wymagany) |
| **Format danych** | JSON (tekstowy) | Protobuf (binarny) |
| **Rozmiar payloadu** | Większy (JSON + nagłówki) | 3-10× mniejszy |
| **Latencja** | Wyższa (parsowanie JSON) | Niższa (binarny + HTTP/2) |
| **Streaming** | Ograniczony (SSE, WebSocket osobno) | Natywny (4 tryby) |
| **Schemat/kontrakt** | Opcjonalny (OpenAPI) | Wymagany (.proto) |
| **Generowanie kodu** | Opcjonalne (OpenAPI Generator) | Natywne (protoc) |
| **Kompatybilność wsteczna** | Brak gwarancji (zależy od konwencji) | Wbudowana (numery pól Protobuf) |
| **Debugowalność** | Wysoka (curl, Postman, logi) | Niska (binarny, wymaga narzędzi) |
| **Wsparcie przeglądarki** | Natywne | Wymaga grpc-web + proxy |
| **Cacheowanie** | Natywne (HTTP cache) | Brak (POST na HTTP/2) |
| **Ekosystem narzędzi** | Ogromny (Swagger, Postman…) | Mniejszy (grpcurl, BloomRPC) |
| **Krzywa uczenia się** | Niska | Średnia/wysoka |
| **Nadaje się do** | API publiczne, CRUD, web | Komunikacja inter-service, streaming |

## 4 tryby komunikacji w gRPC

gRPC wyróżnia się natywnym wsparciem dla streamingu — coś, czego REST nie oferuje bez dodatkowych technologii:

```
1. Unary (jak REST)
   Klient ──żądanie──▶ Serwer
   Klient ◀──odpowiedź── Serwer

2. Server Streaming
   Klient ──żądanie──▶ Serwer
   Klient ◀──strumień── Serwer (wiele odpowiedzi)

3. Client Streaming
   Klient ──strumień──▶ Serwer (wiele żądań)
   Klient ◀──odpowiedź── Serwer

4. Bidirectional Streaming
   Klient ◀──strumień──▶ Serwer (oba kierunki jednocześnie)
```

**Kiedy streaming ma znaczenie:**
*   Real-time monitoring / dashboardy → Server Streaming
*   Upload dużych plików w kawałkach → Client Streaming
*   Chat / współpraca w czasie rzeczywistym → Bidirectional Streaming
*   Propagacja zdarzeń między mikroserwisami → Server Streaming

## Wydajność — liczby

Benchmarki z typowego środowiska mikroserwisowego (mała wiadomość ~1 KB):

| Metryka | REST (JSON/HTTP1.1) | gRPC (Protobuf/HTTP2) | Różnica |
|---|---|---|---|
| Rozmiar payloadu | ~1 000 B | ~200 B | **5× mniejszy** |
| Czas serializacji | ~50 µs | ~5 µs | **10× szybszy** |
| Latencja (p50) | ~5 ms | ~1 ms | **5× niższa** |
| Throughput (req/s) | ~10 000 | ~50 000 | **5× wyższy** |
| Zużycie CPU (serializacja) | Wysokie | Niskie | **3-5× mniej** |

> Uwaga: wartości orientacyjne. Rzeczywiste wyniki zależą od wielkości payload, infrastruktury i implementacji. Przewaga gRPC rośnie wraz z rozmiarem i liczbą wiadomości.

## Kiedy użyć HTTP REST?

| Scenariusz | Dlaczego REST jest lepszym wyborem |
|---|---|
| Publiczne API (dla zewnętrznych klientów) | Uniwersalność, czytelność, łatwe onboarding |
| Aplikacja webowa (SPA, SSR) | Natywne wsparcie przeglądarki, bez proxy |
| CRUD na zasobach (users, orders, products) | REST naturalnie modeluje zasoby i operacje |
| Potrzeba cacheowania HTTP | ETag, Cache-Control, CDN |
| Szybkie prototypowanie | curl + JSON = natychmiastowy feedback |
| Integracja z third-party (webhooks, Stripe, Slack) | Standardowy format, zero konfiguracji |
| API mobilne (publiczne) | JSON parsery dostępne wszędzie |
| SEO / crawling | Boilerplate REST endpoint jest crawlowalny |

## Kiedy użyć gRPC?

| Scenariusz | Dlaczego gRPC jest lepszym wyborem |
|---|---|
| Komunikacja inter-service (mikroserwisy) | Niska latencja, typowany kontrakt, generowanie kodu |
| Wysoki throughput (>10k req/s) | Binarny format + HTTP/2 multipleksowanie |
| Real-time streaming (monitoring, czat) | Natywny bidirectional streaming |
| Polyglot architecture (wiele języków) | Jeden .proto → klienty w Java, Go, Python, C#… |
| Niska latencja jest krytyczna | Binarna serializacja, zero parsowania JSON |
| Duże payloady (ML modele, dane sensorowe) | Protobuf kompresuje znacznie lepiej niż JSON |
| Strict contract-first development | .proto jako single source of truth |
| Deadline propagation w łańcuchu serwisów | Wbudowany mechanizm timeout/deadline |

## Drzewo decyzyjne

```
Czy to publiczne API (przeglądarki, third-party, mobile)?
├── TAK → REST ✅
│         (uniwersalność, cacheowanie, prostota)
└── NIE → Czy potrzebujesz streamingu?
          ├── TAK → gRPC ✅
          │         (natywny bidirectional streaming)
          └── NIE → Czy latencja/throughput jest krytyczny?
                    ├── TAK → gRPC ✅
                    │         (binarny format, HTTP/2)
                    └── NIE → Czy masz wiele serwisów w różnych językach?
                              ├── TAK → gRPC ✅
                              │         (generowanie kodu z .proto)
                              └── NIE → REST ✅
                                        (prostota, debugowalność)
```

## Częsty błąd: „gRPC wszędzie"

gRPC jest świetne do komunikacji wewnętrznej, ale wystawianie go jako publiczne API to pułapka:
*   Przeglądarki **nie obsługują** natywnie gRPC — potrzebujesz grpc-web + Envoy proxy.
*   Zewnętrzni developerzy **nie znają** Protobuf — JSON jest lingua franca web.
*   **Debugowanie** jest trudniejsze — brak curl, brak Postman (bez pluginów).
*   **Dokumentacja** — Swagger/OpenAPI to standard, Protobuf docs to niszowe narzędzia.

**Rozwiązanie:** wzorzec **gRPC wewnętrznie + REST gateway na zewnątrz**:

```
                          ┌──────────────────────────┐
  Przeglądarka/Mobile     │      API Gateway         │     Mikroserwisy
  ─────REST/JSON────────▶ │  (Envoy / Kong / gRPC    │ ────gRPC/Protobuf────▶
                          │   Gateway)                │
                          └──────────────────────────┘
```

Narzędzia takie jak **grpc-gateway** (Go) lub **Envoy** automatycznie tłumaczą REST ↔ gRPC na podstawie pliku `.proto` z adnotacjami:

```protobuf
import "google/api/annotations.proto";

service OrderService {
  rpc CreateOrder(CreateOrderRequest) returns (OrderResponse) {
    option (google.api.http) = {
      post: "/v1/orders"
      body: "*"
    };
  }
}
```

## Częsty błąd: „REST wystarczy do wszystkiego"

W architekturze mikroserwisowej, gdzie serwisy wywołują się wzajemnie setki razy na sekundę, REST z JSON to:
*   **Marnowanie CPU** — serializacja/deserializacja JSON na każdym hopie.
*   **Marnowanie bandwidth** — tekstowy format 5-10× większy niż Protobuf.
*   **Brak formalnego kontraktu** — zmiana pola w jednym serwisie łamie inny serwis bez ostrzeżenia (chyba że masz rygorystyczny OpenAPI workflow).
*   **Brak streamingu** — REST wymaga pollingu lub oddzielnego WebSocket.

## Hybrydowe podejście — najlepsza praktyka

W dojrzałych systemach najczęściej stosuje się podejście hybrydowe:

```
┌─────────────────────────────────────────────────────────────┐
│                        SYSTEM                               │
│                                                             │
│  [Przeglądarka] ──REST/JSON──▶ [API Gateway]               │
│                                     │                       │
│                              ┌──────┴──────┐                │
│                              │             │                │
│                    gRPC ◀────┤             ├────▶ gRPC      │
│                              │             │                │
│                 [Order Svc]  │  [User Svc] │  [Payment Svc] │
│                       │      │             │       │        │
│                       └──────┤   Kafka     ├───────┘        │
│                              │  (eventy)   │                │
│                              └─────────────┘                │
└─────────────────────────────────────────────────────────────┘

REST  → publiczne API, web, mobile
gRPC  → synchroniczna komunikacja inter-service
Kafka → asynchroniczna komunikacja event-driven
```

## Protobuf — dlaczego jest tak szybki?

Protobuf koduje dane w formacie binarnym z tagami (numer pola + typ):

```
JSON:   {"customer_id": "c-123", "quantity": 2}
         → 43 bajtów (tekst, parsowanie klucz-wartość)

Protobuf: 0a 05 63 2d 31 32 33 10 02
           → 9 bajtów (binarny, pozycyjny)
           │  │                    │
           │  └─ pole 1 (string)   └─ pole 2 (varint)
           └─ tag: pole 1, typ 2 (length-delimited)
```

**Dlaczego szybszy:**
*   Brak parsowania kluczy tekstowych — pola identyfikowane numerycznie.
*   Varint encoding — małe liczby zajmują 1 bajt zamiast 1-10 znaków.
*   Zero allocation parsing — Protobuf może deserializować bez alokacji (w C++/Rust).
*   Brak whitespace, cudzysłowów, przecinków.

## Powiązane pliki
*   [Cykl życia żądania HTTP/1.1](cykl-zycia-zadania-http-1-1.md)
*   [Pytania rekrutacyjne HTTP](http-pytania-rekrutacyjne.md)
*   [CORS — Cross-Origin Resource Sharing](cors.md)
*   [Pytania rekrutacyjne z mikroserwisów](mikroserwisy-pytania-rekrutacyjne.md)
*   [Kafka vs RabbitMQ vs ActiveMQ](kafka-rabbitmq-activemq-redis-pubsub.md)
*   [Handling API request failures](handling-api-request-failures.md)
