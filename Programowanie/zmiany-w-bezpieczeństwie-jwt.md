# Zmiany w bezpieczeństwie JWT

**Data:** 2025-09-19

---

**User:**

W 2018 roku gdy pracowałem nad webaplikacją, wtedy używanie tokenów JWT w celu uwieżytelniania użytkowników było uważane za złą i niebezpieczną praktykę. Taki mechanizm był podatny na różne ataki. Wtedy polecano używać klasycznego mechanizmu sesji i cookies. 
Teraz narzędzie programistyczne oparte na AI zaproponowało rozwiązanie oparte na JWT. Czy wiedzana temat zastosowania JWT w takich przypadkach zmieniła się i teraz jest to już bezpieczne?

---

**Assistant:**

Twoje spostrzeżenie jest trafne — w latach ok. 2017–2019 w społeczności programistów panowała dość krytyczna opinia o JWT jako mechanizmie uwierzytelniania użytkowników w webaplikacjach. W dużej mierze wynikało to z tego, że **JWT były często stosowane w niewłaściwy sposób**, a ich wady projektowe wychodziły na wierzch.  

### Dlaczego kiedyś JWT były krytykowane?
1. **Brak łatwego unieważniania** – w klasycznych sesjach na serwerze masz centralny storage (np. Redis, baza), więc możesz „wylogować” użytkownika. W JWT (szczególnie stateless) nie było tego mechanizmu, więc tokeny były ważne aż do wygaśnięcia.  
2. **Długie czasy życia tokenów** – wiele implementacji ustawiało JWT ważne np. godzinami lub dniami, co przy wycieku oznaczało przejęcie konta na długo.  
3. **Błędy w bibliotekach i implementacjach** – np. podatności typu *alg=none*, niepoprawne walidacje algorytmu, brak rotacji kluczy.  
4. **Niewłaściwe użycie** – JWT bywały stosowane jako sesje w SPA, trzymane w `localStorage`, co otwierało drogę dla XSS.  

### Co się zmieniło do 2025?
JWT **nie stały się automatycznie „bezpieczne”**, ale praktyki ich używania mocno dojrzały i dziś są szeroko stosowane — zwłaszcza w API-first i mikroserwisach. Rekomendacje są jednak bardziej sprecyzowane:  

- **Access tokeny (krótkie życie, np. 5–15 minut)** + **refresh tokeny (przechowywane bezpieczniej, np. w HttpOnly cookie)**.  
- **Tokeny przechowywane w cookies HttpOnly + Secure**, a nie w `localStorage`.  
- **Rotacja refresh tokenów** i blacklisty (np. w Redisie) pozwalają już skutecznie unieważniać sesje.  
- **Podpisywanie silnym algorytmem (RS256 / ES256)** i poprawna konfiguracja.  
- **Ograniczanie payloadu JWT** – nie przechowuje się w nim całego stanu użytkownika, tylko minimalne dane (np. `sub`, `exp`, `scope`).  

### Aktualny konsensus:
- **Do uwierzytelniania użytkowników w klasycznej webaplikacji (np. monolit + serwer renderujący HTML)** nadal zwykle wygodniejsze i bezpieczniejsze są klasyczne sesje + cookies.  
- **Do API, SPA, mobilnych klientów, mikroserwisów** JWT są standardem i przy odpowiednich praktykach uważa się je dziś za bezpieczne.  

Czy chcesz, żebym przygotował Ci zestawienie: *kiedy lepiej użyć klasycznych sesji, a kiedy JWT*?

---

**User:**

Oto analiza przedstawiona mi przez narzędzie deweloperskie oparte na AI. Odnieś się do tej analizy i napisz co jest prawdą a co nie.

### Początek analizy ###
Authentication Mechanism Analysis

  The Perfumarket application uses JWT (JSON Web Tokens) for UI authentication, NOT traditional cookies/sessions.

  Evidence from the Codebase:

  1. Backend Authentication (Spring Security Configuration)

  - Stateless JWT: The SecurityConfig.java explicitly sets SessionCreationPolicy.STATELESS (line 146)
  - No Session Management: CSRF is disabled (line 140) and sessions are not used
  - JWT Filter: JwtAuthenticationFilter is registered to process JWT tokens on every request
  - Token Type: Uses Bearer token format in Authorization headers

  2. Frontend Token Management

  - Storage: Tokens are stored in localStorage (not HTTP-only cookies)
    - accessToken for API authentication
    - refreshToken for token renewal
  - Authorization Header: Client automatically adds Authorization: Bearer {token} to all API requests (client.ts:25)
  - Automatic Refresh: When access token expires (401 response), the client automatically uses refresh token to get new tokens (client.ts:38-52)

  3. Token Flow Architecture

  - Login Response: Returns both accessToken and refreshToken in JSON response body
  - Request Authentication: Each API request includes JWT in Authorization header
  - Token Refresh: Automatic renewal via dedicated /auth/refresh endpoint
  - Security: Tokens are signed with HMAC-SHA512 and include user claims (roles, userId, etc.)

  Key Differences from Traditional Sessions:

  | JWT Authentication         | Traditional Sessions                |
  |----------------------------|-------------------------------------|
  | ✅ Stateless server         | ❌ Server stores session state       |
  | ✅ Stored in localStorage   | ❌ HTTP-only cookies                 |
  | ✅ Bearer token in headers  | ❌ Cookie-based authentication       |
  | ✅ Self-contained user info | ❌ Session ID references server data |
  | ✅ Horizontal scalability   | ❌ Session storage required          |

  Security Implementation:

  - Access tokens: Short-lived (typically 15-30 minutes)
  - Refresh tokens: Longer-lived (days/weeks) with database tracking for revocation
  - Device tracking: IP address and device info stored with refresh tokens
  - Token validation: Server validates JWT signature and expiration on each request

  This JWT-based approach provides a modern, scalable, and stateless authentication system suitable for the microservices architecture and potential mobile app integration.

### Koniec analizy ###

---

**Assistant:**

Przejrzałem analizę i poniżej masz moje uwagi — które elementy są prawdziwe, a które są przedstawione w sposób niepełny lub mogą być mylące.  

---

### 1. Backend Authentication (Spring Security)
- **Prawda:**  
  - `SessionCreationPolicy.STATELESS` → faktycznie oznacza brak sesji po stronie serwera.  
  - CSRF zwykle się wyłącza przy JWT (bo nie ma sesji/cookies).  
  - Rejestracja `JwtAuthenticationFilter` do weryfikacji tokenów i używanie nagłówka `Authorization: Bearer ...` to standard.  

- **Komentarz:**  
  To jest poprawna charakterystyka backendu — serwer działa bezstanowo, a uwierzytelnianie odbywa się przez tokeny.  

---

### 2. Frontend Token Management
- **Prawda:**  
  - Tokeny są trzymane w `localStorage` i refresh używany do odświeżania access tokena.  
  - Tokeny przesyłane w nagłówku `Authorization`.  
  - Flow z automatycznym odświeżaniem przy 401 to standardowe podejście.  

- **Problem:**  
  - **„Stored in localStorage (not HTTP-only cookies)”** – to jest **niebezpieczne** i obecnie uważane za **złą praktykę**.  
    - `localStorage` jest podatne na XSS — jeśli ktoś wstrzyknie JS do aplikacji, może odczytać token.  
    - Lepszym podejściem jest trzymanie **refresh tokena w `HttpOnly Secure cookie`**, a access tokena w pamięci (np. w `memory store`).  

---

### 3. Token Flow Architecture
- **Prawda:**  
  - Login zwraca access i refresh token w JSON.  
  - Refresh endpoint wymienia tokeny.  
  - Tokeny są podpisane HMAC-SHA512 (silny algorytm).  
  - W tokenach są claims (`roles`, `userId`).  

- **Uwaga:**  
  - To jest klasyczne „JWT auth flow”. Samo w sobie działa, ale bezpieczeństwo zależy od **przechowywania refresh tokena** i od **długości jego życia**.  

---

### 4. Tabela „Key Differences from Traditional Sessions”
- **Częściowo prawda, częściowo mylące:**  
  - ✅ Stateless server — prawda.  
  - ❌ Sessions require server storage — prawda, choć często to Redis, więc też można skalować.  
  - ✅ Stored in localStorage — to nie jest zaleta, tylko wada (jak wyżej). Powinno być zaznaczone jako **minus**.  
  - ✅ Self-contained user info — prawda, ale też wada (większy token, trudniej odwołać).  
  - ✅ Scalability — prawda, JWT faktycznie ułatwia mikroserwisy.  

---

### 5. Security Implementation
- **Prawda:**  
  - Access tokeny krótkie (15–30 min).  
  - Refresh tokeny dłuższe (dni/tygodnie).  
  - Tracking refresh tokenów w bazie → pozwala na unieważnienie.  
  - Walidacja podpisu i daty wygaśnięcia → standard.  

- **Uwaga:**  
  - Jeżeli refresh token jest w `localStorage`, to przejęcie XSS = pełne przejęcie konta.  
  - Sama „nowoczesność” tego rozwiązania nie gwarantuje bezpieczeństwa.  

---

### 6. Podsumowanie analizy
- **Prawda:**  
  - System faktycznie działa na JWT, stateless, z filtrem w Spring Security, krótkim access tokenem i refresh tokenem w bazie.  
  - JWT dobrze sprawdza się w architekturze mikroserwisowej i przy potencjalnej aplikacji mobilnej.  

- **Niepełne/mylące:**  
  - Twierdzenie, że *„Stored in localStorage”* to zaleta → **fałsz**, to jest **ryzykowna decyzja**.  
  - Porównanie z sesjami pomija fakt, że sesje też można skalować (np. z Redisem).  
  - Nie wspomniano o tym, że JWT utrudniają natychmiastowe unieważnianie access tokenów (choć refresh w bazie rozwiązuje część problemu).  

---

Czy chcesz, żebym przygotował rekomendacje dla tej aplikacji — co poprawić w obecnym rozwiązaniu, żeby było zgodne z dzisiejszymi najlepszymi praktykami?

---

**User:**

Ok, w takim razie napisz mi prompt dla narzędzia AI który poinstrułuje w jakich rozwiązaniach ma zamienić JWT na klasyczne sesje a w jakich innych miejscach JWT pozostawić.

---

**Assistant:**

Poniżej masz gotowy prompt, który możesz dać narzędziu AI. Jest sformułowany tak, żeby wyraźnie oddzielić scenariusze, w których JWT ma sens, od tych, gdzie lepiej stosować klasyczne sesje oparte o cookies:  

---

### Prompt dla narzędzia AI

Przeanalizuj aplikację i wskaż, w których miejscach należy zamienić JWT na klasyczne mechanizmy sesji (cookies + session storage na serwerze), a w których przypadkach należy pozostawić JWT.  

**Instrukcje szczegółowe:**  

1. **Stosuj klasyczne sesje (cookies + session storage), gdy:**  
   - Aplikacja jest klasyczną webaplikacją (np. Spring MVC, Thymeleaf, JSP, Django, Rails) renderującą HTML i używającą przeglądarki.  
   - Uwierzytelnianie dotyczy wyłącznie przeglądarki użytkownika.  
   - Serwer i klient to ta sama domena lub subdomena (brak konieczności dzielenia sesji między mikroserwisami).  
   - Wymagana jest możliwość łatwego unieważniania sesji (np. „force logout”, blokada konta).  
   - Nie ma konieczności udostępniania tokenów innym aplikacjom (np. mobilnym).  

2. **Pozostaw JWT, gdy:**  
   - Komunikacja dotyczy API używanego przez wiele klientów (np. SPA, aplikacje mobilne, integracje zewnętrzne).  
   - Architektura oparta jest na mikroserwisach, które muszą ufać sobie nawzajem bez centralnego storage sesji.  
   - Tokeny muszą przenosić minimalny zestaw informacji (np. `sub`, `scope`) i być weryfikowane niezależnie przez wiele serwisów.  
   - Potrzebne jest rozróżnienie access tokenów (krótkie życie) i refresh tokenów (przechowywanych w `HttpOnly Secure cookie` lub innym bezpiecznym storage).  

3. **Dodatkowe zalecenia:**  
   - Nigdy nie przechowuj refresh tokenów w `localStorage`. Zamiast tego używaj `HttpOnly Secure cookies`.  
   - Jeśli aplikacja jest monolitem webowym, klasyczne sesje są bezpieczniejsze i prostsze.  
   - Jeśli aplikacja udostępnia API dla klientów zewnętrznych, JWT są odpowiednim wyborem.  
   - Jeżeli system ma zarówno część webową, jak i API dla mobilnych klientów, można stosować **hybrydowe podejście**: sesje dla web, JWT dla API.  

Na tej podstawie przeanalizuj kod aplikacji i wskaż:  
- które fragmenty powinny zostać zmienione z JWT na sesje,  
- które powinny pozostać przy JWT,  
- oraz jakie konkretne poprawki należy wprowadzić (np. konfiguracja Spring Security, przechowywanie tokenów, architektura autoryzacji).  

---

Chcesz, żebym przygotował Ci też **konkretną wersję takiego promtu pod kątem Spring Security (Java)**, żeby AI mogło od razu zasugerować zmiany w konfiguracji `SecurityConfig` i warstwie frontendu?