# Wyjaśnienie SSE szczegółowo

**Data:** 2025-09-25

---

**User:**

Czym jest SSE - Server Side Events. Wyjaśnij szczegółowo i technicznie.

---

**Assistant:**

# Co to jest SSE (Server-Sent Events)
SSE (Server-Sent Events) to prosty, standardowy mechanizm strumieniowania wiadomości z serwera do przeglądarki przez pojedyncze, długotrwałe połączenie HTTP. Po stronie klienta SSE jest obsługiwane przez interfejs `EventSource` (specyfikacja W3C). SSE jest **jednokierunkowe** — serwer → klient (jeśli klient ma wysyłać dane do serwera, trzeba użyć XHR/fetch/WebSocket/inne).

---

# Protokół i format wiadomości
Połączenie SSE to zwykła odpowiedź HTTP ze specjalnym typem MIME i strumieniowym formatem tekstowym:

- Nagłówki (przykład):
  ```
  HTTP/1.1 200 OK
  Content-Type: text/event-stream; charset=utf-8
  Cache-Control: no-cache
  Connection: keep-alive
  ```
- Ciało: tekst składający się z linii zakończonych `\n` (lub `\r\n`) i bloków wiadomości zakończonych pustą linią `\n\n`.
- Pola (na linię):
  - `data: <treść>` — zawartość wiadomości. Można mieć wiele `data:` linii — łączą się w jedną wiadomość z wstawionymi znakami nowej linii.
  - `id: <identyfikator>` — ustawia last-event id (używane przy ponownym łączeniu).
  - `event: <nazwa>` — typ zdarzenia; klient może subskrybować nazwy zdarzeń.
  - `retry: <ms>` — instruuje klienta, po ilu ms próbować ponownie po rozłączeniu.
  - Linia zaczynająca się od `:` to komentarz (często używany jako heartbeat / keep-alive).

Przykład wiadomości:
```
id: 42
event: price-update
data: {"symbol":"BTC","price":57320}
\n
```
Jeżeli chcesz wysłać wieloliniowe dane:
```
data: first line
data: second line

```

---

# Po stronie klienta (przeglądarka)
API:
```js
const es = new EventSource('/events');

es.onopen = () => console.log('open');
es.onmessage = e => console.log('message', e.data); // domyślne "message"
es.onerror = e => console.error('error', e);

// nasłuchiwanie zdarzeń o nazwie:
es.addEventListener('price-update', e => {
  const payload = JSON.parse(e.data);
});
```
Właściwości:
- `es.readyState` — 0 CONNECTING, 1 OPEN, 2 CLOSED.
- `e.lastEventId` — id ostatniej otrzymanej wiadomości.
- Przy ponownym połączeniu przeglądarka wysyła nagłówek `Last-Event-ID` z ostatnim `id` (jeśli był ustawiony).

Ograniczenia:
- Standardowy `EventSource` **nie pozwala** na ustawianie niestandardowych nagłówków (np. `Authorization`). W praktyce do autoryzacji stosuje się ciasteczka (cookie) lub token w query string, albo własne rozwiązanie (fetch + ReadableStream).
- SSE jest tekstowe — nie ma natywnego binarnego trybu (można przesyłać base64 lub JSON).

---

# Po stronie serwera — praktyka
Ważne nagłówki i zachowania:
- `Content-Type: text/event-stream; charset=utf-8`
- `Cache-Control: no-cache`
- nie ustawiaj `Content-Length` (połączenie jest otwarte).
- konieczne: od razu wypchnąć nagłówki/flush (np. `res.flushHeaders()` w Node/Express) i wysyłać dane strumieniowo.
- wysyłaj okresowy „heartbeat” (np. komentarz `:\n\n`) żeby zapobiegać timeoutom na proxy.

Prosty przykład Node.js + Express:
```js
app.get('/sse', (req, res) => {
  res.setHeader('Content-Type', 'text/event-stream; charset=utf-8');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');
  res.flushHeaders();

  // Obsługa last-event-id z nagłówka:
  const lastId = req.headers['last-event-id'];

  let idCounter = 1;
  const interval = setInterval(() => {
    const payload = JSON.stringify({ t: Date.now() });
    res.write(`id: ${idCounter}\n`);
    res.write(`event: tick\n`);
    res.write(`data: ${payload}\n\n`);
    idCounter++;
  }, 1000);

  req.on('close', () => {
    clearInterval(interval);
  });
});
```

---

# Reconnecty i trwałość
- Przeglądarkowy klient automatycznie próbuje ponownie się połączyć (domyślnie ~3s — implementacja może się różnić). Serwer może wysłać `retry: <ms>`.
- Jeśli serwer ustawi `id:` dla wiadomości, klient zapisuje to i przy reconnect wysyła `Last-Event-ID` — serwer może na tej podstawie wznowić wysyłkę od konkretnego miejsca.
- Implementacja serwera powinna być przygotowana na powtarzanie wiadomości i zapewnić idempotentność / możliwość wznowienia (np. pamiętając offsety lub kolejki).

---

# Skalowanie i problemy operacyjne
- Każdy klient utrzymuje otwarte połączenie TCP — skaluje gorzej niż krótkie requesty. Przy dużej liczbie klientów:
  - trzeba brać pod uwagę limity plików/gniazdek, zużycie pamięci i wątków.
  - zwykle stosuje się: event broker (Redis pub/sub, Kafka), serwery asynchroniczne (async I/O), nginx jako reverse proxy, sticky sessions jeśli wymagane.
- Proxy / load balancery: wiele usług (nginx, Varnish) buforuje odpowiedź — trzeba wyłączyć buforowanie dla SSE:
  - nginx: `proxy_buffering off; proxy_cache off; proxy_read_timeout 3600s;`
  - upewnij się, że proxy nie zamyka połączeń zbyt agresywnie.
- Utrzymuj keep-alive / heartbeat aby uniknąć rozłączeń przez firewalle i proxy.

---

# Bezpieczeństwo i CORS
- SSE działa po HTTPS i powinno być stosowane przez TLS (ochrona przed MITM).
- CORS: jeśli klient jest z innego origin, serwer musi zwrócić odpowiednie nagłówki `Access-Control-Allow-Origin` itd.
- Nie wkładaj tokenów w URL jeśli są wrażliwe (można użyć cookie httpOnly). Standardowe `EventSource` nie pozwala na custom headers, dlatego często stosuje się cookie albo mechanizm uwierzytelniania przed otwarciem streamu.

---

# Porównanie z innymi technologiami
- **WebSocket** — pełne duplex, binarne, niższe narzuty protokołu dla dwukierunkowej komunikacji. Lepsze, gdy klient często wysyła dane do serwera.
- **Long polling / Comet** — kompatybilne z prostymi serwerami, ale mniej efektywne (więcej requestów).
- **HTTP/2 server push** — inny mechanizm (pchanie zasobów przy żądaniu), nie zastąpi SSE dla ciągłych zdarzeń aplikacyjnych.
- **SSE** — prosty model dla wydarzeń server→client: automatyczne ponowne połączenie, obsługa eventów, łatwiejszy do debugowania i skalowania w środowisku opartym na HTTP.

---

# Najczęstsze pułapki i dobre praktyki
- Pamiętaj o `res.flush()` / flushHeaders natychmiast po ustawieniu nagłówków.
- Nie ustawiaj `Content-Length`.
- Wysyłaj okresowe komentarze `: \n\n` co np. 15–30s, aby utrzymać połączenie przez proxy.
- Używaj `id:` i `Last-Event-ID` do wznowienia przesyłu po rozłączeniu (ważne dla niezawodności).
- Do autoryzacji preferuj ciasteczka lub mechanizmy, które nie wymagają custom headers.
- Monitoruj liczbę otwartych połączeń i zasoby systemowe; testuj z podobnym obciążeniem jak produkcja.

---

# Kiedy użyć SSE?
Użyj SSE gdy:
- potrzebujesz prostego, niezawodnego streamu serwer → klient (np. powiadomienia, feedy, aktualizacje statusu),
- nie potrzebujesz komunikacji klient → serwer w czasie rzeczywistym,
- chcesz prostszej integracji z infrastrukturą HTTP (proste skalowanie, użycie istniejących serwerów/proxy).

---

Jeśli chcesz, mogę:
- dać pełny, gotowy przykład serwera SSE w twoim ulubionym języku (Java/Spring, Node.js, Go itp.),
- pokazać przykładową konfigurację nginx dla SSE,
- albo napisać prosty polyfill / alternatywę (fetch + ReadableStream) jeśli potrzebujesz wysyłać nagłówki autoryzacyjne.

Napisz, co preferujesz — przygotuję konkretny kod.