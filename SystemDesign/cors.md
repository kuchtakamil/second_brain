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

### Żądania proste (simple requests)

Niektóre żądania są „proste" i przeglądarka wysyła je bezpośrednio, bez poprzedzającego preflightu. Warunki, które musi spełnić żądanie proste:

- Metoda: `GET`, `POST` lub `HEAD`
- Nagłówki: wyłącznie standardowe (`Accept`, `Content-Type` z wartością `application/x-www-form-urlencoded`, `multipart/form-data` lub `text/plain`, `Accept-Language`, `Content-Language`)

Przeglądarka dołącza nagłówek `Origin`, a serwer odpowiada nagłówkiem `Access-Control-Allow-Origin`:

```
Klient (app.example.com)                      Serwer (api.example.com)
  |                                                  |
  | GET /data                                        |
  | Origin: https://app.example.com                 |
  |------------------------------------------------->|
  |                                                  |
  |       200 OK                                     |
  |       Access-Control-Allow-Origin: https://app.example.com
  |<-------------------------------------------------|
```

Jeśli nagłówek `Access-Control-Allow-Origin` nie jest obecny albo nie pasuje do origin klienta, przeglądarka blokuje odczyt odpowiedzi (serwer i tak ją wysłał, ale JavaScript nie uzyska do niej dostępu).

### Preflight request

Dla żądań „niebezpiecznych" — niestandardowe metody (`PUT`, `DELETE`, `PATCH`), niestandardowe nagłówki (`Authorization`, `X-Custom-Header`), `Content-Type: application/json` — przeglądarka wysyła najpierw żądanie `OPTIONS`, zwane **preflightem**:

```
Klient                                          Serwer
  |                                               |
  | OPTIONS /api/resource                         |
  | Origin: https://app.example.com              |
  | Access-Control-Request-Method: DELETE        |
  | Access-Control-Request-Headers: Authorization|
  |---------------------------------------------->|
  |                                               |
  |   204 No Content                              |
  |   Access-Control-Allow-Origin: https://app.example.com
  |   Access-Control-Allow-Methods: GET, POST, DELETE
  |   Access-Control-Allow-Headers: Authorization
  |   Access-Control-Max-Age: 86400              |
  |<----------------------------------------------|
  |                                               |
  | DELETE /api/resource                          |
  | Authorization: Bearer <token>                |
  |---------------------------------------------->|
  |   200 OK                                      |
  |<----------------------------------------------|
```

`Access-Control-Max-Age` określa, ile sekund przeglądarka może cache'ować odpowiedź preflightową, zanim wyśle kolejną. Dzięki temu nie każde żądanie musi poprzedzać preflight.

---

## Kluczowe nagłówki CORS

### Nagłówki odpowiedzi serwera

| Nagłówek                           | Opis                                                              |
|------------------------------------|-------------------------------------------------------------------|
| `Access-Control-Allow-Origin`      | Origin, któremu zezwolono na dostęp. `*` oznacza wszystkich.      |
| `Access-Control-Allow-Methods`     | Lista dozwolonych metod HTTP.                                     |
| `Access-Control-Allow-Headers`     | Lista dozwolonych nagłówków żądania.                              |
| `Access-Control-Expose-Headers`    | Nagłówki odpowiedzi widoczne dla JavaScript.                     |
| `Access-Control-Allow-Credentials` | Czy cookies i nagłówki `Authorization` mogą być dołączone.       |
| `Access-Control-Max-Age`           | Czas cache'owania preflightu w sekundach.                         |

### Nagłówki żądania klienta

| Nagłówek                            | Opis                                                         |
|-------------------------------------|--------------------------------------------------------------|
| `Origin`                            | Źródło, z którego pochodzi żądanie.                          |
| `Access-Control-Request-Method`     | Metoda, którą klient chce użyć (w preflighcie).              |
| `Access-Control-Request-Headers`    | Nagłówki, które klient chce wysłać (w preflighcie).          |

---

## CORS a Credentials (cookies, Authorization)

Domyślnie przeglądarka **nie** dołącza cookies ani nagłówka `Authorization` do żądań cross-origin. Aby to zmienić, klient musi wysłać żądanie z flagą `credentials`:

```javascript
fetch('https://api.example.com/data', {
  credentials: 'include',  // dołącz cookies i Authorization
});
```

Serwer musi wtedy odpowiedzieć **jednocześnie** z:

```
Access-Control-Allow-Origin: https://app.example.com  // NIE może być *
Access-Control-Allow-Credentials: true
```

Jeśli serwer zwróci `Access-Control-Allow-Origin: *` przy `credentials: 'include'`, przeglądarka i tak zablokuje odpowiedź. Wildcard `*` i credentials są wzajemnie wykluczone.

---

## Typowe błędy i pułapki

### 1. Wildcard z credentials

```
// Błąd po stronie serwera:
Access-Control-Allow-Origin: *
Access-Control-Allow-Credentials: true
```

Przeglądarka zablokuje dostęp. Serwer musi podać konkretny origin.

### 2. CORS ustawiony tylko na preflighcie

Zdarza się, że serwer poprawnie odpowiada na `OPTIONS`, ale właściwa odpowiedź (np. `DELETE`) już nie zawiera nagłówków CORS. Przeglądarka zablokuje odczyt wyniku.

### 3. CORS to nie jest zabezpieczenie serwera

CORS jest egzekwowany **wyłącznie przez przeglądarkę**. Curl, Postman czy inne klienty HTTP po prostu ignorują nagłówki CORS. CORS chroni użytkownika końcowego przed nieautoryzowanym odczytem danych przez skrypt cross-origin — nie jest ochroną API przed bezpośrednimi wywołaniami.

### 4. Brak expose-headers

JavaScript może domyślnie odczytać tylko ograniczony zestaw nagłówków odpowiedzi (np. `Content-Type`, `Cache-Control`). Aby JS mógł odczytać własne nagłówki serwera, np. `X-Request-Id` albo `X-Total-Count`, należy je jawnie wylistować:

```
Access-Control-Expose-Headers: X-Request-Id, X-Total-Count
```

### 5. Nadmierne użycie wildcard `*`

`Access-Control-Allow-Origin: *` pozwala każdej stronie czytać odpowiedzi serwera. Dla publicznych API bez uwierzytelnienia jest to w porządku, ale dla API zwracającego dane prywatne lub wrażliwe oznacza problem.

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

## Powiązane materiały

- [HTTP: Pytania Rekrutacyjne](http-pytania-rekrutacyjne.md)
- [TLS: Pytania Rekrutacyjne](tls-pytania-rekrutacyjne.md)
- [Mikroserwisy: Pytania Rekrutacyjne](mikroserwisy-pytania-rekrutacyjne.md)
