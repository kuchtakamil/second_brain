# CORS: Cross-Origin Resource Sharing

CORS to mechanizm bezpieczeństwa wbudowany w przeglądarki, który kontroluje, czy skrypt uruchomiony na jednej domenie może wysyłać żądania HTTP do innej domeny. Jest rozszerzeniem polityki Same-Origin Policy i pozwala serwerom jawnie zadeklarować, którym źródłom zezwalają na dostęp do swoich zasobów.

---

## Czym jest Same-Origin Policy i dlaczego CORS istnieje?

Przeglądarka domyślnie blokuje skryptom JavaScript dostęp do odpowiedzi z innych źródeł. Reguła ta nosi nazwę **Same-Origin Policy** (SOP). Dwa URL-e mają to samo źródło (origin), jeżeli zgadzają się wszystkie trzy elementy:

| Element   | Przykład               |
|-----------|------------------------|
| Protokół  | `https`                |
| Domena    | `api.example.com`      |
| Port      | `443`                  |

Poniższe pary mają **różne originy**:

```
https://app.example.com    ≠   https://api.example.com   (inna subdomena)
https://example.com        ≠   http://example.com         (inny protokół)
https://example.com        ≠   https://example.com:8080   (inny port)
```

Bez SOP złośliwa strona mogłaby w tle wysyłać requesty do banku użytkownika i czytać odpowiedzi w imieniu zalogowanego użytkownika, korzystając z jego cookies. SOP blokuje odczyt odpowiedzi cross-origin, ale CORS daje serwerom możliwość selektywnego poluzowania tego ograniczenia.

---

## Jak działa CORS?

Mechanizm CORS opiera się na swoistym „dialogu” pomiędzy przeglądarką użytkownika a serwerem, z którym próbuje się połączyć aplikacja (skrypt JavaScript). Ten dialog odbywa się za pomocą specjalnych nagłówków HTTP.

Kluczowe jest zrozumienie, że **CORS nie jest mechanizmem, w którym przeglądarka pyta serwer o zgodę na *wysłanie* zapytania (z małymi wyjątkami). CORS to mechanizm, w którym przeglądarka pyta, czy może *pokazać wynik* tego zapytania kodowi JavaScript.**

Aby zachować kompatybilność z historycznym zachowaniem sieci Web (kiedy to zwykłe formularze HTML mogły wysyłać zapytania GET i POST w dowolne miejsce, ale bez możliwości odczytu odpowiedzi), specyfikacja CORS dzieli żądania HTTP na dwie kategorie: **żądania proste** oraz te wymagające **zapytania wstępnego (preflight)**.

### 1. Żądania proste (Simple requests)

Są to zapytania, które historycznie mogły zostać wygenerowane przez zwykły, stary formularz HTML `<form>`, jeszcze zanim wymyślono zaawansowane aplikacje SPA i mechanizm CORS. Ponieważ serwery od zawsze musiały radzić sobie z takimi żądaniami, specyfikacja CORS uznaje je za stosunkowo mało ryzykowne.

**Kiedy żądanie jest „proste”?** Musi spełniać ściśle określone warunki:
- **Metoda HTTP:** Może to być tylko `GET`, `POST` lub `HEAD`.
- **Nagłówki:** Może zawierać tylko standardowe nagłówki (m.in. `Accept`, `Accept-Language`, `Content-Language`). Zabronione są własne nagłówki typu `Authorization` czy `X-Custom-Header`.
- **Content-Type:** W przypadku żądań POST, typ danych musi być jednym z historycznie wspieranych przez formularze: `application/x-www-form-urlencoded`, `multipart/form-data` lub `text/plain`. Jeśli używasz `application/json`, żądanie przestaje być proste!

**Przebieg żądania prostego:**
1. Kod JavaScript wykonuje np. `fetch('https://api.example.com/data')`.
2. Przeglądarka widzi, że to cross-origin, więc automatycznie dokleja do żądania nagłówek `Origin: https://twoja-strona.com`.
3. **Zapytanie trafia na serwer i zostaje przez niego normalnie przetworzone** (np. dane z bazy zostają pobrane).
4. Serwer odsyła odpowiedź.
5. Przeglądarka analizuje odpowiedź serwera. Jeśli brakuje w niej nagłówka CORS zezwalającego na dostęp (czyli `Access-Control-Allow-Origin`), **przeglądarka ukrywa odpowiedź przed kodem JavaScript** i rzuca błąd w konsoli. 

Warto to podkreślić: przy żądaniu prostym **serwer wykonuje akcję**, ale przeglądarka nie pozwala skryptowi zobaczyć jej rezultatu.

### 2. Żądania złożone i zapytanie wstępne (Preflight request)

Zupełnie inaczej sytuacja wygląda, gdy nasza aplikacja chce wysłać bardziej nowoczesne, „niebezpieczne” żądanie. Należą do nich zapytania używające metod `PUT`, `DELETE`, `PATCH`, przesyłające dane w formacie JSON (`Content-Type: application/json`) lub dołączające niestandardowe nagłówki (np. token w nagłówku `Authorization`).

Takich żądań stary internet nie znał, więc ich niespodziewane wysłanie mogłoby uszkodzić lub naruszyć bezpieczeństwo nieprzygotowanego serwera. Dlatego przeglądarka używa mechanizmu **Preflight**.

**Przebieg zapytania z preflightem:**
1. Aplikacja JS próbuje wysłać żądanie `DELETE /users/1` z nagłówkiem `Authorization`.
2. Przeglądarka wstrzymuje to żądanie. Zamiast niego, całkowicie w tle, **wysyła specjalne zapytanie zwiadowcze** (preflight) używając metody HTTP `OPTIONS`.
3. W tym zwiadowczym zapytaniu przeglądarka „pyta” serwer: *„Hej, skrypt z domeny X chce do ciebie wysłać zapytanie DELETE i użyć nagłówka Authorization. Czy się na to zgadzasz?”*.
4. Serwer musi poprawnie odpowiedzieć na to żądanie `OPTIONS` (zazwyczaj statusem `200 OK` lub `204 No Content`), dołączając odpowiednie nagłówki CORS, które mówią: *„Tak, zgadzam się na DELETE z domeny X i akceptuję ten nagłówek”*.
5. Dopiero po otrzymaniu takiej pozytywnej „promesy”, przeglądarka **wysyła właściwe żądanie** `DELETE`.

Jeśli serwer nie odpowie na preflight lub odpowie negatywnie (np. brak odpowiednich nagłówków CORS), przeglądarka od razu rzuca błąd i **właściwe żądanie nigdy nie opuszcza przeglądarki użytkownika**.

---

## Kluczowe nagłówki CORS

Zrozumienie CORS to w dużej mierze umiejętność czytania nagłówków HTTP. Dzielą się one na te, które przeglądarka wysyła do serwera (żądanie) oraz te, którymi serwer instruuje przeglądarkę (odpowiedź).

### Nagłówki wysyłane przez przeglądarkę (Żądanie)

Przeglądarka automatycznie zarządza tymi nagłówkami – programista frontendowy z reguły nie musi (a wręcz ze względów bezpieczeństwa nie może) ich ręcznie modyfikować.

- **`Origin`**
  Najważniejszy nagłówek ze strony klienta. Informuje serwer, pod jakim adresem aktualnie znajduje się użytkownik (gdzie uruchomiony jest skrypt JS). Zawiera zawsze schemat (protokół), domenę i ewentualnie port (np. `https://sklep.pl`). Serwer używa go, by zdecydować, czy chce rozmawiać z tą stroną.
  
- **`Access-Control-Request-Method`**
  Wysyłany **tylko** podczas zapytania zwiadowczego (preflight `OPTIONS`). Mówi serwerowi, jakiej metody HTTP (np. `PUT` czy `DELETE`) skrypt będzie chciał użyć we właściwym żądaniu.

- **`Access-Control-Request-Headers`**
  Również wysyłany tylko w preflighcie. Przeglądarka wylistowuje w nim po przecinku wszystkie niestandardowe nagłówki, które programista próbuje dołączyć do właściwego żądania (np. `authorization, content-type, x-api-key`).

### Nagłówki wysyłane przez serwer (Odpowiedź)

To serwer ma ostateczny głos w polityce CORS. Musi on poprawnie reagować na nagłówki żądania i odsyłać swoje instrukcje, które przeglądarka zinterpretuje.

- **`Access-Control-Allow-Origin`**
  Najważniejszy nagłówek odpowiedzi. To nim serwer mówi przeglądarce, kto ma prawo odczytać dane.
  - Może zawierać konkretną domenę, która wysłała żądanie: `Access-Control-Allow-Origin: https://sklep.pl`.
  - Może zawierać znak gwiazdki: `Access-Control-Allow-Origin: *`, co oznacza „każda strona w internecie może odczytać tę odpowiedź” (częste w publicznych API).
  
- **`Access-Control-Allow-Methods`**
  Odsyłany w odpowiedzi na preflight. Serwer listuje w nim wszystkie metody HTTP, na które zezwala z danego źródła (np. `GET, POST, DELETE, OPTIONS`).

- **`Access-Control-Allow-Headers`**
  Odsyłany w odpowiedzi na preflight. Jeśli przeglądarka w `Access-Control-Request-Headers` zapytała o zgodę na użycie np. `Authorization`, serwer musi go tutaj wymienić, by potwierdzić: *„Tak, akceptuję zapytania z nagłówkiem Authorization”*.

- **`Access-Control-Expose-Headers`**
  Bardzo ważny, często pomijany nagłówek. Domyślnie ze względów bezpieczeństwa, nawet przy prawidłowym CORS, JavaScript może odczytać z odpowiedzi serwera tylko kilka standardowych nagłówków (np. `Content-Type`). Jeśli Twój serwer zwraca jakieś ważne dane w nagłówkach własnych, np. `X-Total-Pages` dla paginacji lub `X-RateLimit-Remaining`, musisz je jawnie wylistować w `Access-Control-Expose-Headers`. W przeciwnym razie będą niewidoczne dla Twojego kodu JS.

- **`Access-Control-Allow-Credentials`**
  Zwraca wartość `true`. Używany w scenariuszach, gdzie do żądania dołączone są ciasteczka (cookies) uwierzytelniające lub nagłówki `Authorization`. Oznacza zgodę serwera na udostępnienie odpowiedzi, gdy żądanie było spersonalizowane. **Ważne:** Jeśli serwer odsyła ten nagłówek, `Access-Control-Allow-Origin` **nie może** być gwiazdką `*` – musi być dokładnie wskazaną domeną.

- **`Access-Control-Max-Age`**
  Mówi przeglądarce, przez ile sekund może "pamiętać" (cache'ować) wynik zapytania preflight. Dzięki temu, jeśli aplikacja wysyła serię żądań `DELETE`, przeglądarka nie musi przed każdym z nich wysyłać zapytania `OPTIONS`. Znacząco poprawia to wydajność aplikacji.

---

## CORS a Credentials (cookies, Authorization)

Standardowe żądania cross-origin są z założenia „anonimowe”. Oznacza to, że ze względów bezpieczeństwa przeglądarka domyślnie **nie dołącza** do nich ciasteczek (cookies), danych z sesji HTTP ani nagłówka `Authorization`. Jest to kluczowe zabezpieczenie – dzięki niemu złośliwa strona nie może tak po prostu wysłać zapytania do Twojego banku, korzystając z Twojej aktywnej sesji.

Aby uwierzytelnione żądanie cross-origin mogło się powieść, muszą zostać spełnione warunki po obu stronach – zarówno na frontendzie, jak i na backendzie. Wymaga to tzw. "podwójnego potwierdzenia" (opt-in).

**1. Zgoda po stronie klienta (Frontend)**
Programista piszący aplikację w JavaScript musi jawnie poinstruować przeglądarkę, że chce dołączyć poświadczenia do zapytania. W przypadku API `fetch` robi się to za pomocą flagi `credentials`:

```javascript
fetch('https://api.example.com/dane-prywatne', {
  method: 'GET',
  credentials: 'include' // Kluczowa flaga: dołącz cookies i nagłówki autoryzacyjne
});
```

**2. Zgoda po stronie serwera (Backend)**
Nawet jeśli przeglądarka wyśle ciasteczka, to zablokuje możliwość odczytania odpowiedzi, chyba że serwer jednoznacznie potwierdzi: *„Tak, to zapytanie dotyczyło prywatnych danych i zgadzam się, aby ta konkretna domena je odczytała”*. Serwer robi to odesłaniem nagłówka:

```http
Access-Control-Allow-Credentials: true
```

**Krytyczna zasada bezpieczeństwa:**
Mechanizm CORS posiada bardzo restrykcyjną regułę, o którą rozbija się wielu programistów. **Jeżeli serwer zwraca `Access-Control-Allow-Credentials: true`, to absolutnie zabronione jest używanie gwiazdki (`*`) w nagłówku `Access-Control-Allow-Origin`.**

Serwer nie może powiedzieć: *„Pozwalam na odczyt moich prywatnych, uwierzytelnionych danych komukolwiek”*. Musi podać dokładny adres (origin), który o te dane prosi, na przykład:

```http
Access-Control-Allow-Origin: https://moja-zaufana-aplikacja.pl
Access-Control-Allow-Credentials: true
```

Próba połączenia gwiazdki `*` z flagą credentials zawsze skończy się błędem CORS w konsoli przeglądarki.

---

## Typowe błędy i pułapki

Praca z mechanizmem CORS bywa frustrująca. Poniżej znajduje się omówienie najczęściej spotykanych problemów, ich przyczyn oraz sposobów rozwiązania.

### 1. Zderzenie gwiazdki z poświadczeniami (Wildcard + Credentials)

Jest to najczęstszy błąd konfiguracji. Aplikacja frontendowa wysyła zapytanie z `credentials: 'include'`, a serwer odpowiada:
```http
Access-Control-Allow-Origin: *
Access-Control-Allow-Credentials: true
```
**Efekt:** Przeglądarka stanowczo blokuje dostęp do odpowiedzi i rzuca błędem.
**Rozwiązanie:** Serwer musi dynamicznie odczytywać nagłówek `Origin` z żądania i, jeśli znajduje się on na liście zaufanych domen, "odbijać" go w odpowiedzi:
```http
Access-Control-Allow-Origin: <wartość_odczytana_z_nagłówka_Origin_żądania>
```

### 2. CORS ustawiony wyłącznie dla zapytań Preflight (OPTIONS)

Zdarza się, że programiści konfigurują routing w swoim frameworku tak, by poprawnie odpowiadał na zapytania zwiadowcze `OPTIONS` (zwracając `204 No Content` i odpowiednie nagłówki). Jednak zapominają dodać te same nagłówki do właściwego kontrolera (np. dla metody `DELETE` czy `POST`).
**Efekt:** Preflight przechodzi pomyślnie (w zakładce Network widzisz zielone 200/204 dla OPTIONS), ale natychmiast po nim właściwe zapytanie kończy się błędem CORS.
**Rozwiązanie:** Nagłówek `Access-Control-Allow-Origin` musi być obecny **w każdej** odpowiedzi serwera – zarówno w preflighcie, jak i we właściwej odpowiedzi z danymi. Najlepiej zarządzać tym globalnie przez middleware.

### 3. Mylenie CORS z firewallem (Brak zrozumienia modelu zagrożeń)

Wielu deweloperów uważa, że skoro ich API nie zwraca nagłówków CORS, to jest "zabezpieczone" przed nieautoryzowanym użyciem. Nic bardziej mylnego. CORS jest egzekwowany **wyłącznie przez przeglądarki internetowe**. Narzędzia takie jak curl, Postman, skrypty w Pythonie czy komunikacja serwer-serwer całkowicie ignorują CORS. 
**Efekt:** Atakujący może bez problemu pobrać dane z Twojego API używając skryptu, pomimo braku nagłówków CORS.
**Rozwiązanie:** CORS służy do ochrony przeglądarki i użytkownika, a nie samego API. Do ochrony serwera przed niepowołanym dostępem należy używać uwierzytelniania (np. OAuth, JWT, klucze API) oraz limitowania ruchu (Rate Limiting).

### 4. Widmo w zakładce Network, ale "null" w kodzie (Brak Expose-Headers)

To bardzo podstępna pułapka. Uruchamiasz narzędzia deweloperskie przeglądarki, widzisz w zakładce Network, że serwer odesłał nagłówek `X-Total-Count: 42`. Jednak gdy próbujesz odczytać go w JavaScript (`response.headers.get('X-Total-Count')`), otrzymujesz wartość `null`.
**Efekt:** Kod nie może odczytać niestandardowych nagłówków pomimo ich fizycznej obecności w odpowiedzi sieciowej.
**Rozwiązanie:** Domyślnie JS w przeglądarce działa w tzw. "bezpiecznym trybie" i ma dostęp tylko do kilku podstawowych nagłówków. Aby udostępnić inne, serwer musi jawnie wskazać je po imieniu w nagłówku `Access-Control-Expose-Headers: X-Total-Count`.

### 5. Zbyt leniwa konfiguracja (Nadmierne użycie `*`)

Konfiguracja `Access-Control-Allow-Origin: *` dla całego API to kusząca droga na skróty, pozwalająca szybko pozbyć się błędów CORS podczas developmentu.
**Efekt:** Jeśli API udostępnia dane wrażliwe (nawet jeśli nie używa cookies, ale np. uwierzytelniania opartego na IP lub innych mechanizmach ukrytych za proxy), pozwalasz dosłownie każdej stronie w internecie napisać skrypt, który odczyta te dane. 
**Rozwiązanie:** Znak gwiazdki (`*`) powinien być zarezerwowany wyłącznie dla w pełni publicznych API (np. pogoda, publiczne słowniki). W każdym innym przypadku serwer powinien posiadać "białą listę" (whitelist) dozwolonych domen.

---

## Konfiguracja CORS na popularnych backendach

### Node.js (Express)

```javascript
import cors from 'cors';

app.use(cors({
  origin: ['https://app.example.com', 'https://admin.example.com'],
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Authorization', 'Content-Type'],
  credentials: true,
  maxAge: 86400,
}));
```

### Nginx

```nginx
location /api/ {
    if ($request_method = 'OPTIONS') {
        add_header 'Access-Control-Allow-Origin' 'https://app.example.com';
        add_header 'Access-Control-Allow-Methods' 'GET, POST, DELETE, OPTIONS';
        add_header 'Access-Control-Allow-Headers' 'Authorization, Content-Type';
        add_header 'Access-Control-Max-Age' 86400;
        return 204;
    }
    add_header 'Access-Control-Allow-Origin' 'https://app.example.com';
    proxy_pass http://backend;
}
```

### Spring Boot (Java)

```java
@CrossOrigin(
    origins = "https://app.example.com",
    allowedHeaders = {"Authorization", "Content-Type"},
    allowCredentials = "true",
    maxAge = 86400
)
@RestController
public class ApiController { ... }
```

---

## CORS w kontekście mikroserwisów i API Gateway

W architekturze mikroserwisowej CORS najlepiej konfiguruje się **raz**, centralnie w API Gateway lub reverse proxy. Unikamy wtedy rozbieżności konfiguracji między różnymi serwisami.

```
Przeglądarka --> API Gateway (CORS tutaj) --> Mikroserwis A
                                          --> Mikroserwis B
```

Każdy mikroserwis nie musi wtedy sam obsługiwać preflightów i nagłówków CORS, co upraszcza konfigurację i eliminuje ryzyko niespójności.

---

## CORS a CSRF

CORS i CSRF to różne problemy, które ludzie często mylą:

| Aspekt      | CORS                                      | CSRF                                    |
|-------------|-------------------------------------------|-----------------------------------------|
| Co chroni   | Odczyt odpowiedzi cross-origin przez JS   | Nieautoryzowane akcje w imieniu ofiary  |
| Kto wymusza | Przeglądarka (blokada odczytu)            | Serwer (tokeny CSRF, SameSite cookies)  |
| Atak        | Złośliwy JS czyta prywatne dane           | Złośliwa strona wysyła requesty z session
| Rozwiązanie | Nagłówki CORS po stronie serwera          | CSRF tokeny, `SameSite=Strict/Lax`      |

CORS **nie zastępuje** ochrony CSRF. Nawet poprawna konfiguracja CORS nie chroni przed CSRF, bo przeglądarka i tak wyśle cookies dla żądań nawigacyjnych (np. form submit), na które SOP nie ma wpływu.

---

## Podsumowanie

- CORS to rozszerzenie Same-Origin Policy, które pozwala serwerom selektywnie zezwalać na cross-origin requests.
- Przeglądarka egzekwuje CORS — curl i Postman go ignorują.
- Preflight (`OPTIONS`) poprzedza niestandardowe żądania, aby upewnić się, że serwer je akceptuje.
- Wildcard `*` i credentials (`cookies`, `Authorization`) są wzajemnie wykluczone.
- W mikroserwisach CORS najlepiej konfigurować centralnie w API Gateway.
- CORS chroni odczyt danych przez skrypty cross-origin, ale nie zastępuje ochrony CSRF.

---

## Czy złośliwy skrypt Python mógłby odczytać sesję bankową użytkownika?

To ważny niuans: SOP i CORS to mechanizmy **wyłącznie przeglądarkowe**. Skrypt Python, curl czy Postman w ogóle ich nie widzą — mogą wysyłać dowolne żądania HTTP bez żadnych ograniczeń cross-origin.

**Ale to nie znaczy, że Python automatycznie ma dostęp do sesji bankowej użytkownika.**

### Gdzie jest bariera?

Zalogowana sesja w banku istnieje jako cookie (np. `session_id=abc123`) przechowywane przez **przeglądarkę w jej własnej, odizolowanej przestrzeni** — najczęściej w zaszyfrowanej bazie SQLite (`Cookies` w profilu Chrome/Firefox). Zwykły proces Python uruchomiony przez użytkownika **nie ma dostępu do tych cookies automatycznie**.

```
Przeglądarka (Chrome)           Skrypt Python
┌──────────────────────┐        ┌──────────────────────┐
│  Cookie store        │        │                      │
│  session_id=abc123   │   ✗    │  requests.get(...)   │
│  (zaszyfrowane)      │        │  # nie ma cookies    │
└──────────────────────┘        └──────────────────────┘
```

Plik cookie Chrome jest szyfrowany kluczem powiązanym z kontem systemowym (DPAPI na Windows, Keychain na macOS, Secret Service na Linux). Odczyt wymaga tych samych uprawnień systemowych co przeglądarka — czyli nie jest to trywialne, ale na tym samym koncie użytkownika jest możliwe dla złośliwego procesu z wystarczającymi uprawnieniami.

### Kiedy Python faktycznie może to zrobić?

| Scenariusz | Czy Python dostaje cookies? |
|---|---|
| Zwykły skrypt Python bez uprawnień | ✗ nie, brak dostępu do cookie store |
| Złośliwe oprogramowanie z uprawnieniami systemowymi | ✓ tak, może odczytać i odszyfrować plik cookies |
| Użytkownik sam wklei ciasteczka (np. z DevTools) | ✓ tak |
| XSS: JS na stronie banku wyśle cookie do atakującego | ✓ tak (jeśli cookie nie jest `HttpOnly`) |
| Złośliwe rozszerzenie przeglądarki | ✓ tak, rozszerzenia mają dostęp do cookies |
| MITM / przechwycenie ruchu sieciowego | ✓ tak, jeśli brak HTTPS lub pinning |

### Kluczowa różnica

SOP chroni przed scenariuszem gdzie **złośliwy JavaScript uruchomiony w przeglądarce** (np. na `evil.com`) próbuje odczytać odpowiedź z `bank.com`. Tu przeglądarka i SOP stoją na straży.

Skrypt Python to **zupełnie inny model zagrożenia** — on nie działa w kontekście przeglądarki, więc SOP go nie dotyczy. Problem sprowadza się do pytania: *skąd skrypt wziął sesję?* Jeśli ją ma, to żaden CORS mu nie przeszkodzi. Jeśli jej nie ma, to CORS nic tutaj nie zmienia — sesja po prostu nie istnieje poza przeglądarką.

```
Zagrożenie A: evil.com (JS w przeglądarce) → SOP/CORS chroni
Zagrożenie B: złośliwy proces na komputerze → SOP/CORS nie chroni (inny wektor ataku)
```

Zagrożenie B to już domena **bezpieczeństwa systemu operacyjnego**, a nie protokołu HTTP. Środki ochrony to: antywirus, izolacja procesów, uprawnienia systemowe, wykrywanie anomalii, a po stronie banku — HttpOnly cookies (JS nie odczyta), Secure cookies (tylko HTTPS), krótki czas życia sesji i weryfikacja user-agenta / IP.

---

## Powiązane materiały

- [HTTP: Pytania Rekrutacyjne](http-pytania-rekrutacyjne.md)
- [TLS: Pytania Rekrutacyjne](tls-pytania-rekrutacyjne.md)
- [Mikroserwisy: Pytania Rekrutacyjne](mikroserwisy-pytania-rekrutacyjne.md)
