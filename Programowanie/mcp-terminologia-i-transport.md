# MCP terminologia i transport

**Data:** 2025-09-24

---

**User:**

Czuję się zagubiony w terminologi MCP. W specyfikacji jest napisane że MCP używa JSON-RPC, jednak FastMCP podobno używa http. Jak to jest, wyjaśnij szczegółowo i technicznie. Przeszukaj internet jeśli potrzeba

---

**Assistant:**

# Krótkie podsumowanie (na start)
Obie rzeczy, które czytałeś, są prawdziwe, ale dotyczą **różnych warstw** protokołu.  
**MCP** definiuje **format wiadomości** (JSON-RPC 2.0) — to jest *jak* wygląda pojedyncza wiadomość. **Transport** (stdio / Streamable HTTP) mówi *jak* te wiadomości są przesyłane między procesami/serwerami. FastMCP to konkretna implementacja/ramka, która **udostępnia** MCP i potrafi wystawić ten JSON-RPC zarówno przez **stdin/stdout** (stdio), jak i przez **HTTP (Streamable HTTP / SSE / http app)**. citeturn3view0turn0search1turn4search7

---

# Szczegóły techniczne — warstwy i ich rola

## 1) Warstwa wiadomości — JSON-RPC 2.0
MCP używa JSON-RPC 2.0 jako *wire format* (tzn. wszystkie request/response/notification są JSON-owymi obiektami zgodnymi z JSON-RPC). Typowe pola to `jsonrpc:"2.0"`, `id`, `method`, `params` (żądania), albo `result` / `error` (odpowiedzi). Przykładowe MCP-owe wywołanie narzędzia to metoda `tools/call` z odpowiednimi `params`. citeturn3view0turn5search11

Przykład JSON-RPC (czysty payload):
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "get_weather",
    "arguments": { "location": "Warsaw" }
  }
}
```

---

## 2) Warstwa transportu — stdio vs. Streamable HTTP
**StdIO** — typowe użycie: lokalny proces-serwer komunikujący się z klientem poprzez stdin/stdout (np. Claude Desktop uruchamia serwer jako proces). W takim trybie trzeba zwrócić uwagę na *framing* (odczyt/oddzielenie kolejnych JSON-ów) i na to, żeby **nie pisać nic poza protokołem na stdout** (printy/logi do stdout popsują komunikację). Standardowo stosuje się nagłówkowe ramkowanie typu `Content-Length: N\r\n\r\n<JSON>` (LSP-style), chociaż w praktyce spotykane są też newline-delimited JSON; dobre implementacje potrafią autodetekcji/obsługi obu wariantów. citeturn3view0turn1search7

**Streamable HTTP** — transport zdalny/HTTP-owy: klient wysyła JSON-RPC w ciele żądania HTTP (zwykle POST na endpoint, np. `/mcp`), a serwer może zwracać pojedyncze odpowiedzi, albo (opcjonalnie) *streamować* komunikaty do klienta (historycznie SSE — Server-Sent Events — było powszechne; nowsze wersje MCP rekomendują/wyjaśniają model „Streamable HTTP”, który używa POST dla client→server i opcjonalnych mechanizmów streamingu dla server→client). Innymi słowy: JSON-RPC = format wiadomości, HTTP/stdio = kanał transportu. citeturn2search0turn0search1

---

# Konkretne przykłady (praktyczne)

## A) StdIO — przykładowe ramkowanie (Content-Length)
Jeżeli używasz framingu w stylu Content-Length, sekwencja wygląda tak (CRLF oznaczę `\r\n`):

```
Content-Length: 75\r\n
\r\n
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"version":"1.0.0"}}
```

(Uwaga: powyżej `75` to **dokładna długość bajtów** payloadu w UTF-8 dla tego przykładu — jeżeli będziesz składać własne payloady, musisz liczyć bajty UTF-8 przed wysłaniem). Serwer czyta nagłówki aż do pustego wiersza, potem czyta dokładnie `Content-Length` bajtów i parsuje JSON. Implementacje produkcyjne zachowują się tak, żeby NIE pisać zwykłych `print()` na stdout (logi na stderr lub do pliku). citeturn1search7turn3view0

## B) HTTP POST — wysłanie pojedynczego żądania (Streamable HTTP)
Przykład curl (client → server):
```bash
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_weather","arguments":{"location":"Warsaw"}}}'
```
Serwer zwróci standardową odpowiedź JSON (200 + ciało JSON-RPC) albo — jeśli serwer udostępnia streaming — będzie mógł wysłać serię komunikatów (zależnie od konfiguracji: SSE albo specjalny stream HTTP). Z punktu widzenia MCP, treść POST to po prostu JSON-RPC w body. citeturn2search0turn0search14

## C) SSE (server → client) — przykład wydarzenia
Jeżeli serwer używa SSE do streamingu komunikatów (opcjonalne), po stronie klienta GET na endpoint i odczytujemy kolejne eventy. Przykładowy fragment SSE (serwer wysyła linię `data:` zawierającą JSON-RPC):

```
data: {"jsonrpc":"2.0","id":1,"result":{"partial":"..."}}

data: {"jsonrpc":"2.0","id":1,"result":{"final":"..."}}
```

Klient parsuje każde `data:` jako string JSON i zamienia na obiekt JSON-RPC. (Uwaga: MCP ewoluuje — niektóre nowsze serwisy preferują „Streamable HTTP” bez wymogu ciągłego długiego połączenia; ale SSE nadal bywa używane jako opcja streamingu). citeturn2search0turn2search2

---

# FastMCP — co robi w praktyce?
FastMCP to biblioteka/ramka ułatwiająca budowę serwerów MCP w Pythonie. Umożliwia:
- definiowanie narzędzi (dekorator `@mcp.tool()` itd.),
- uruchomienie serwera w trybie **stdio** (lokalnie) lub w trybie **streamable HTTP / ASGI** (mount jako aplikacja Starlette/FastAPI),
- pomocne utilities (generowanie schematu narzędzi, mounting `/mcp` endpoint itp.).  
W dokumentacji i przykładach FastMCP widać zarówno `mcp.run(transport='stdio')`, jak i funkcje które zwracają ASGI app (`streamable_http_app()` / `http_app()`), więc FastMCP może mapować *ten sam* JSON-RPC na różne transporty. citeturn3view0turn4search7

Przykład minimalny (schematycznie):
```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("myserver")

@mcp.tool()
def greet(name: str) -> str:
    return f"Hi {name}"

# lokalnie:
mcp.run(transport='stdio')

# albo jako HTTP (ASGI):
app = mcp.streamable_http_app()
# mount app w FastAPI/uvicorn itd.
```

---

# Najczęstsze pułapki / praktyczne wskazówki
- **Jeżeli serwer ma być użyty lokalnie (np. Claude Desktop)** — zadbaj o pełną zgodność stdio: dokładne ramkowanie (Content-Length), brak printów na stdout, logi na stderr. Klienci desktopowi zwykle oczekują stdio. citeturn3view0  
- **Jeżeli serwer ma być zdalny** — wybierz Streamable HTTP; ułatwia skalowanie i integrację z infrastrukturą (API Gateway, reverse proxies). Zwróć uwagę na zabezpieczenia (Bearer token, Origin allowlist itp.). citeturn0search14turn2search0  
- **Kompatybilność framingu** — różne implementacje mogą używać `Content-Length` lub newline-delimited JSON; jeśli chcesz być odporny — albo wymuszaj Content-Length, albo implementuj autodetekcję. Niektóre serwery/SDKi robią to automatycznie. citeturn1search16

---

# Podsumowanie (jedno zdanie)
MCP = **JSON-RPC (format wiadomości)** + **transporty** (głównie stdio i Streamable HTTP). FastMCP to framework implementujący MCP i **eksponujący** ten JSON-RPC albo przez stdio (lokalnie), albo przez HTTP (z obsługą streamingu). Dlatego w specyfikacji przeczytasz JSON-RPC, a w dokumentacji FastMCP — HTTP: obie rzeczy są spójne (różne warstwy). citeturn3view0turn0search1turn4search7

---

Jeżeli chcesz, przygotuję od razu:
- minimalny przykład FastMCP w Pythonie uruchamiany jako stdio (z poprawnym Content-Length framing), **lub**
- przykład FastMCP wystawiony jako Streamable HTTP + przykładowe curl → POST i curl → SSE do testów.

Napisz, który wariant chcesz — zrobię kod i przykłady krok po kroku.

---

**User:**

Nie rozumiem tego: "Jeżeli serwer ma być użyty lokalnie (np. Claude Desktop)". Czy mój nowy, własnoręcznie napisany serwer MCP musi być jakoś połączony z Claude Desktop?

---

**Assistant:**

Twój własny serwer MCP **nie musi być związany z Claude Desktop** – możesz go napisać i uruchamiać zupełnie niezależnie, np. jako proces HTTP/ASGI, czy nawet jako prosty `stdio`-based serwis.  

Wspomniałem o Claude Desktop dlatego, że **to jest obecnie najpopularniejszy klient MCP**. MCP to tylko **protokół** (JSON-RPC + transport), a klientem musi być jakieś oprogramowanie, które potrafi się z tym serwerem dogadać. Przykłady:

- **Claude Desktop** – potrafi ładować lokalne serwery MCP przez `stdio`. Wtedy, gdy użytkownik coś wpisuje w Claude, model może wywoływać Twoje narzędzia z MCP.  
- **Inne implementacje** – możesz samemu napisać klienta MCP w Pythonie, Node.js itp., który połączy się z Twoim serwerem (po HTTP albo po `stdio`).  
- **FastMCP** – to framework, który pozwala szybko wystawić taki serwer, a Ty decydujesz, czy będzie działał jako `stdio` (np. dla Claude Desktop) czy jako aplikacja HTTP (np. do podłączenia zdalnie).  

Czyli:  
- **Specyfikacja MCP nie wymusza Claude** – możesz pisać swój serwer niezależnie.  
- **Jeżeli chcesz, żeby Claude korzystał z Twojego serwera** – wtedy najprościej wystawić go w trybie `stdio`, bo Claude Desktop tak się komunikuje.  
- **Jeżeli chcesz używać swojego serwera w innym środowisku** – wystaw go po HTTP i napisz klienta, który gada JSON-RPC.  

Chcesz, żebym rozpisał Ci krok po kroku, **jak Claude Desktop wykrywa i uruchamia serwery MCP**, czy bardziej interesuje Cię, **jak podłączyć swój serwer MCP w zupełnie niezależnej aplikacji** (np. własny klient HTTP)?