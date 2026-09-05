# REST API vs HTTP API — czym się różnią?

## Krótkie podsumowanie

Rozróżnienie „REST API" vs „HTTP API" funkcjonuje na **dwóch poziomach** i to jest źródło zamieszania:

1. **Ogólny (architektoniczny)** — REST to styl architektoniczny z konkretnymi ograniczeniami (Fielding, 2000). HTTP API to dowolne API działające po HTTP. Każde REST API jest HTTP API, ale nie każde HTTP API jest RESTful.
2. **Konkretny (AWS API Gateway)** — Amazon ma dwa produkty: **REST API (v1)** i **HTTP API (v2)**. To nazwy marketingowe dwóch generacji ich gateway'a, a nie formalne kategorie architektoniczne.

Tabelka, którą znalazłeś, prawie na pewno dotyczy kontekstu AWS. Ale żeby ją zrozumieć, trzeba najpierw ogarnąć różnicę ogólną.

## Dlaczego to ma znaczenie?

*   Na rozmowie rekrutacyjnej pytają: „czym jest REST?" — chcą usłyszeć o ograniczeniach Fieldinga, nie o AWS.
*   Przy wyborze narzędzia w AWS pytają: „REST API czy HTTP API?" — chcą usłyszeć o cenach i feature'ach gateway'a.
*   Jeśli pomylisz konteksty, to albo przesadzisz z teorią, albo nie będziesz wiedział dlaczego „v2 nie ma walidacji requestów".

---

## Poziom 1: różnica architektoniczna (ogólna)

### HTTP API — „dowolny interfejs po HTTP"

HTTP API to szerokie pojęcie oznaczające **każdy interfejs, który komunikuje się za pomocą protokołu HTTP**. Wystawiasz endpointy, wysyłasz żądania GET/POST/PUT/DELETE, dostajesz odpowiedzi — masz HTTP API.

**Zero wymagań architektonicznych.** Możesz mieć:
*   `POST /doSomething` — RPC-style, akcja jako czasownik → to nadal HTTP API.
*   `GET /getUser?id=5` — brak zasobowego modelu → to nadal HTTP API.
*   Stan sesji po stronie serwera → łamie statelessness, ale to nadal HTTP API.

```bash
# Typowe HTTP API w stylu RPC — działa, ale to nie jest RESTful
POST /api/loginUser
POST /api/getUserOrders
POST /api/cancelOrder
```

### REST API — „HTTP API z ograniczeniami"

REST (Representational State Transfer) to **styl architektoniczny** zdefiniowany przez Roya Fieldinga w 2000 roku. Aby API było naprawdę RESTful, musi spełniać **6 ograniczeń**:

| Ograniczenie | Co oznacza |
|---|---|
| **Client-Server** | Separacja front-endu od back-endu |
| **Stateless** | Każde żądanie zawiera pełny kontekst — serwer nie trzyma stanu sesji |
| **Cacheable** | Odpowiedzi deklarują, czy mogą być cache'owane (ETag, Cache-Control) |
| **Uniform Interface** | Zasoby identyfikowane URI, manipulowane przez reprezentacje (JSON/XML), self-descriptive messages |
| **Layered System** | Klient nie wie, czy rozmawia z serwerem czy pośrednikiem (load balancer, CDN) |
| **HATEOAS** | Odpowiedź zawiera linki nawigacyjne — klient odkrywa co może zrobić dalej |

```bash
# RESTful — zasoby jako rzeczowniki, metody HTTP jako operacje
GET    /users/123           # pobranie zasobu
POST   /users               # utworzenie zasobu
PUT    /users/123           # aktualizacja zasobu
DELETE /users/123           # usunięcie zasobu

# Odpowiedź z HATEOAS — klient wie co dalej
{
  "id": 123,
  "name": "Kamil",
  "_links": {
    "self": "/users/123",
    "orders": "/users/123/orders",
    "delete": "/users/123"
  }
}
```

### Kluczowy wniosek

> **REST to podzbiór HTTP API.** Twoja intuicja była prawidłowa — REST działa po HTTP i jest stylem architektonicznym. Ale w praktyce 90% API nazywanych „REST" nie spełnia wszystkich ograniczeń (zwłaszcza HATEOAS). To są de facto HTTP API ze stylem zasobowym.

Poziomy dojrzałości REST (Richardson Maturity Model):

```
Level 0: Jedno URI, jedna metoda (POST /api) ......... HTTP API (RPC-style)
Level 1: Wiele URI, jedna metoda ...................... Zasoby, ale nie REST
Level 2: Wiele URI, poprawne metody HTTP .............. „REST" potoczne (tu jest 90% API)
Level 3: HATEOAS — linki w odpowiedziach .............. Prawdziwy REST (rzadko spotykany)
```

---

## Poziom 2: REST API vs HTTP API w AWS API Gateway

Tabelka, którą znalazłeś (v1 / v2), dotyczy konkretnych produktów AWS:

| Cecha | **REST API (v1)** | **HTTP API (v2)** |
|---|---|---|
| **Rok wprowadzenia** | 2015 | 2019 |
| **Filozofia** | Feature-rich, enterprise governance | Minimalistyczny, szybki, tani |
| **Cena** | ~$3.50 / milion requestów | ~$1.00 / milion requestów |
| **Latencja** | Standardowa | ~60% niższa |
| **Routing** | Hierarchiczne drzewo zasobów | Płaska struktura route'ów |
| **Deployment** | Wymagany jawny „Deployment" do stage'a | Automatyczny / natychmiastowy |
| **Walidacja requestów** | ✅ Schema-based | ❌ Brak |
| **Transformacja request/response** | ✅ VTL (Velocity Template Language) | ❌ Brak |
| **Usage plans / API Keys** | ✅ Per-client throttling | ❌ Brak |
| **Caching** | ✅ Wbudowany TTL cache | ❌ Brak |
| **Autoryzacja JWT (OIDC/OAuth2)** | ❌ Wymaga Lambda authorizer | ✅ Natywna |
| **CORS** | Ręczna konfiguracja | ✅ Prosty toggle |
| **Canary deployments** | ✅ | ❌ |
| **Private endpoints (VPC)** | ✅ | ❌ |
| **WebSocket** | ❌ | ✅ |
| **AWS WAF** | ✅ | ✅ |

### Kiedy REST API (v1)?

*   Potrzebujesz **usage plans** — limitowanie requestów per-klient (np. tier darmowy vs płatny).
*   Potrzebujesz **walidacji requestów** na poziomie gateway'a (JSON Schema).
*   Potrzebujesz **transformacji** request/response (VTL templates).
*   Potrzebujesz **canary deployments** — 10% ruchu na nową wersję.
*   Masz istniejący system z private API endpoints przez VPC.

### Kiedy HTTP API (v2)?

*   Budujesz standardowe serverless API (Lambda + API Gateway).
*   Chcesz **niski koszt** — 3.5× tańszy.
*   Chcesz **niską latencję** — 60% szybszy.
*   Potrzebujesz **natywnej autoryzacji JWT** (Cognito, Auth0, Okta).
*   Potrzebujesz **WebSocket**.
*   Nie potrzebujesz zaawansowanych feature'ów enterprise.

### Drzewo decyzyjne (AWS)

```
Czy potrzebujesz usage plans, API keys lub request validation?
├── TAK → REST API (v1) ✅
└── NIE → Czy potrzebujesz canary deployments lub VTL transformacji?
          ├── TAK → REST API (v1) ✅
          └── NIE → HTTP API (v2) ✅
                    (tańszy, szybszy, prostszy)
```

---

## Podsumowanie: skąd to zamieszanie?

```
                    ┌────────────────────────────────────┐
                    │         Wszystkie API               │
                    │                                     │
                    │    ┌──────────────────────────┐     │
                    │    │       HTTP API            │     │
                    │    │  (dowolne API po HTTP)    │     │
                    │    │                           │     │
                    │    │   ┌──────────────────┐   │     │
                    │    │   │    REST API       │   │     │
                    │    │   │ (spełnia 6        │   │     │
                    │    │   │  ograniczeń       │   │     │
                    │    │   │  Fieldinga)       │   │     │
                    │    │   └──────────────────┘   │     │
                    │    │                           │     │
                    │    └──────────────────────────┘     │
                    │                                     │
                    │    gRPC, GraphQL, SOAP, WebSocket…  │
                    └────────────────────────────────────┘
```

*   **Architektonicznie** — REST API to podzbiór HTTP API. Różnica jest w ograniczeniach projektowych, nie w protokole.
*   **W AWS** — REST API (v1) i HTTP API (v2) to dwa produkty z różnymi feature'ami i ceną. Nazwy są mylące, bo **oba działają po HTTP** i żaden nie wymusza pełnego REST.
*   **Potocznie** — ludzie mówią „REST API" na każde HTTP API z JSON-em i metodami GET/POST. To niedokładne, ale powszechne.

Twoja intuicja była poprawna: REST to styl architektoniczny działający po HTTP. Tabelka v1/v2 to nazewnictwo wewnętrzne AWS, które niestety zaciemnia ogólne pojęcia.

## Powiązane pliki

*   [HTTP vs gRPC — kiedy użyć czego?](http-vs-grpc.md)
*   [Cykl życia żądania HTTP/1.1](cykl-zycia-zadania-http-1-1.md)
*   [Pytania rekrutacyjne HTTP](http-pytania-rekrutacyjne.md)
*   [CORS — Cross-Origin Resource Sharing](cors.md)
*   [Handling API request failures](handling-api-request-failures.md)
