# AI i HATEOAS – Czy sztuczna inteligencja wykorzystuje dane hipermedialne z REST API?

Tak — i to coraz intensywniej. HATEOAS (Hypermedia as the Engine of Application State), historycznie uważany za „nadmiarowy" element REST API, okazał się jednym z kluczowych mechanizmów umożliwiających bezpieczną i autonomiczną nawigację agentów AI po usługach sieciowych.

Poniżej opisano konkretne zastosowania, wzorce architektoniczne i korzyści wynikające z połączenia AI z danymi HATEOAS.

---

## 1. Czym jest HATEOAS w skrócie?

HATEOAS to zasada, w której odpowiedź serwera REST API zawiera **linki hipermedialne** (`_links`, nagłówki `Link`) opisujące dostępne akcje i przejścia stanowe dla danego zasobu. Zamiast zmuszać klienta do znajomości wszystkich endpointów, serwer mówi: „oto co możesz teraz zrobić".

```json
{
  "orderId": 42,
  "status": "confirmed",
  "_links": {
    "self":   { "href": "/orders/42" },
    "ship":   { "href": "/orders/42/ship",   "method": "POST" },
    "cancel": { "href": "/orders/42/cancel", "method": "POST" }
  }
}
```

W powyższym przykładzie zamówienie w stanie `confirmed` udostępnia tylko akcje `ship` i `cancel`. Gdyby zamówienie było już wysłane, link `ship` zniknąłby, a pojawił się np. `track`.

To jest **poziom 3** modelu dojrzałości Richardsona (Richardson Maturity Model) — najwyższy stopień projektowania REST API.

---

## 2. Dlaczego HATEOAS jest „idealny" dla agentów AI?

### Problem tradycyjnego podejścia

Gdy agent AI korzysta z klasycznego REST API (poziom 2), musi:

*   Znać z góry **wszystkie endpointy** i kolejność ich wywoływania.
*   Polegać na **statycznej dokumentacji** (np. OpenAPI spec), która może być nieaktualna.
*   Samodzielnie rozumieć **maszynę stanów** zasobów — kiedy wolno wysłać zamówienie, kiedy anulować.

To prowadzi do:
*   **Halucynacji** — agent zgaduje ścieżki URL lub parametry.
*   **Prób i błędów** — agent próbuje niedozwolonych akcji i traci tokeny na obsługę błędów 4xx.
*   **Kruchych integracji** — zmiana URL-a po stronie serwera łamie całą logikę agenta.

### Rozwiązanie HATEOAS

API HATEOAS działa jak **samoopisująca się mapa** — serwer mówi agentowi, co może zrobić w danym momencie:

| Cecha | Tradycyjny REST (dla agenta) | HATEOAS (dla agenta) |
|:---|:---|:---|
| **Lokalizacja logiki** | Klient (prompt / kod agenta) | Serwer (maszyna stanów) |
| **Odkrywanie akcji** | Statyczna dokumentacja | Dynamiczne linki w odpowiedzi |
| **Bezpieczeństwo** | Ryzyko wywołań nieprawidłowych | Tylko dozwolone akcje są widoczne |
| **Odporność na zmiany** | Silne powiązanie (hardcoded URL) | Luźne powiązanie (agent podąża za linkami) |

---

## 3. Konkretne zastosowania AI + HATEOAS

### 3.1. Autonomiczni agenci workflow (Agent-driven Enterprise Automation)

Agent zarządza złożonym procesem biznesowym (np. łańcuch dostaw, pipeline zamówieniowy, system płatności). API w odpowiedzi na zapytanie zwraca linki opisujące **dokładnie te operacje, które są teraz dozwolone**.

**Przykład**: Agent obsługujący system zamówień „MoneyMate" nie musi znać diagramu stanów. Zamówienie w stanie `pending` zwraca jedynie link `confirm`. Po potwierdzeniu pojawiają się `ship` i `cancel`. Agent po prostu **podąża za linkami**, a serwer egzekwuje reguły biznesowe.

### 3.2. Nawigacja po API jako alternatywa dla crawlingu

Inteligentny agent „przegląda" API w sposób analogiczny do tego, jak człowiek klika linki na stronie WWW. Agent nie potrzebuje pełnej mapy endpointów — startuje od jednego zasobu (entry point) i odkrywa powiązane zasoby poprzez osadzone linki.

Narzędzia takie jak **Firecrawl** czy **BrowserUse** już dziś robią to na stronach WWW. HATEOAS jest odpowiednikiem tego podejścia w świecie API — agent „crawluje" maszynę stanów API, zbierając dane z powiązanych zasobów.

### 3.3. HATEOAS + MCP (Model Context Protocol)

To jedno z najciekawszych połączeń architektonicznych w 2025/2026 roku. MCP i HATEOAS pełnią **komplementarne role**:

*   **MCP** mówi agentowi **co może zrobić** (lista narzędzi / capabilities).
*   **HATEOAS** mówi agentowi **kiedy i w jakiej kolejności** może to zrobić (nawigacja stanowa).

MCP zapewnia standardowe „rury" do wywoływania narzędzi. HATEOAS dodaje **warstwę polityki i kontekstu** — linki mogą być filtrowane na podstawie uprawnień agenta, stanu zasobu czy polityki bezpieczeństwa.

```
[Agent / LLM]
     │
     ▼
[MCP Client]  ─── "Jakie narzędzia mam?" ──▶  [MCP Server]
     │                                              │
     │           ◀── lista: place_order,            │
     │               confirm_order, ship_order      │
     │                                              │
     ▼                                              │
[Wywołanie: GET /orders/42]                         │
     │                                              │
     ▼                                              ▼
[HATEOAS Response]                          [Filtrowanie linków
  _links: { ship, cancel }                  wg uprawnień agenta]
     │
     ▼
[Agent wie: mogę TYLKO ship lub cancel — nie próbuje niczego innego]
```

### 3.4. Semantic Hypermedia — zrozumiałe API dla LLM-ów

Projekty takie jak **Hydra** (W3C) rozszerzają HATEOAS o **semantykę linked data**. Zamiast surowych linków, odpowiedź zawiera słownik opisujący znaczenie każdej akcji w sposób zrozumiały dla modelu językowego:

```json
{
  "@context": "http://schema.org/",
  "@type": "Order",
  "orderStatus": "OrderConfirmed",
  "potentialAction": [
    {
      "@type": "ShipAction",
      "target": "/orders/42/ship",
      "description": "Wyślij zamówienie do klienta"
    }
  ]
}
```

LLM nie musi „zgadywać" co robi dany endpoint — dostaje opis semantyczny wprost w payloadzie.

### 3.5. Guardrails i bezpieczeństwo agentów

HATEOAS pełni rolę **runtime guardrails** na poziomie API:

*   Agent **nie może wykonać akcji, której link nie został mu zwrócony**.
*   Serwer może dynamicznie ukrywać linki na podstawie roli agenta, polityki compliance lub stanu zasobu.
*   To przenosi odpowiedzialność za bezpieczeństwo z promptu (kruchego) na serwer (kontrolowanego).

---

## 4. Wzorzec „Menu" — fail-safe dla agentów

Zaawansowane implementacje wprowadzają uniwersalny link `menu` (analogiczny do paska nawigacji na stronie WWW), który jest zawsze obecny w odpowiedzi. Gdy agent „utknąłem" — np. trafił w ślepy zaułek lub zmienił kontekst zadania — może wrócić do punktu startowego bez konieczności „pamiętania" URL-i.

```json
{
  "_links": {
    "menu":   { "href": "/api", "title": "Punkt startowy API" },
    "self":   { "href": "/orders/42" },
    "ship":   { "href": "/orders/42/ship" }
  }
}
```

---

## 5. Podsumowanie — dlaczego HATEOAS przeżywa renesans?

HATEOAS był przez dekady uważany za zbyt skomplikowany dla ludzkich deweloperów, którzy woleli proste REST API + dokumentację. Paradoksalnie, agenci AI okazali się **idealnym klientem** dla tego wzorca:

*   **Ludzie** czytają dokumentację i potrafią zrozumieć kontekst → HATEOAS jest dla nich „over-engineering".
*   **Agenci AI** nie czytają dokumentacji, zgadują i halucynują → HATEOAS daje im **mapę nawigacyjną w runtime**.

HATEOAS to nie przyszłość — to wzorzec, który znalazł swojego „idealnego użytkownika" dopiero po 20 latach istnienia.

---

## Powiązane tematy

*   [Model Context Protocol (MCP)](mcp-ai-engineer-interview.md) — protokół standaryzujący komunikację agentów z narzędziami
*   [Wzorce projektowe systemów agentowych](wzorce-projektowe-systemow-agentowych.md) — architektura multi-agent
*   [Narzędzia dla agentów (Tool Use)](narzedzia-dla-agentow-tool-use-langgraph.md) — jak agenci wywołują narzędzia w LangGraph
*   [LLM Guardrails](llm-guardrails.md) — mechanizmy bezpieczeństwa dla modeli językowych
