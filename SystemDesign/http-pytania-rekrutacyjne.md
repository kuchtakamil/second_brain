# HTTP: Pytania Rekrutacyjne

Lista pytań na rozmowę kwalifikacyjną z zakresu **protokołu HTTP**. Pytania pogrupowane tematycznie — od fundamentów semantyki protokołu po zaawansowane mechanizmy wydajnościowe, bezpieczeństwa i ewolucji HTTP. Poziom: Senior / Expert.

---

## 1. Fundamenty protokołu i model żądanie-odpowiedź

1. Czym jest HTTP jako protokół warstwy aplikacji? Na jakiej warstwie modelu OSI działa i jaki model komunikacji realizuje?

   HTTP (Hypertext Transfer Protocol) to protokół warstwy aplikacji (7. warstwa modelu OSI). Służy do przesyłania dokumentów hipertekstowych, a w nowoczesnym ujęciu — dowolnych danych (JSON, wideo, binarki). 
   Realizuje model komunikacji **klient-serwer** oraz **żądanie-odpowiedź** (request-response). Klient inicjuje komunikację, wysyłając żądanie, a serwer przetwarza je i odsyła odpowiedź. Wersje HTTP/1.1 i starsze są synchroniczne na poziomie aplikacji (klient czeka na odpowiedź), choć od HTTP/2 wprowadzono asynchroniczne strumieniowanie. Wymaga pod spodem niezawodnego protokołu transportowego — historycznie TCP (w HTTP/1.x i 2), a w HTTP/3 używa QUIC (opartego na UDP).

2. Czym różni się HTTP jako protokół **bezstanowy** od protokołów stanowych? Jakie mechanizmy pozwalają budować sesyjność ponad bezstanowym HTTP?

   Bezstanowość (statelessness) HTTP oznacza, że serwer nie przechowuje żadnego kontekstu (stanu) pomiędzy kolejnymi żądaniami od tego samego klienta. Każde żądanie musi zawierać komplet informacji niezbędnych do jego obsłużenia. Protokoły stanowe (np. FTP, Telnet) utrzymują otwartą sesję, w której serwer pamięta wcześniejsze komendy.

   Zalety bezstanowości to łatwość skalowania horyzontalnego (żadne serwery nie muszą synchronizować pamięci o kliencie) i odporność na awarie.
   Aby zbudować sesyjność (np. logowanie) na wierzchu bezstanowego HTTP, używa się mechanizmów przekazujących stan w każdym żądaniu:
   **Cookies**: serwer wysyła `Set-Cookie`, klient odsyła nagłówek `Cookie`.
   **Tokeny (np. JWT)**: przekazywane w nagłówku `Authorization: Bearer <token>`.
   **Parametry URL** lub **ukryte pola formularzy** (rzadziej stosowane z powodów bezpieczeństwa).

3. Jaka jest różnica między **URI**, **URL** i **URN**? Jakie elementy składowe ma URL i jakie mają znaczenie dla routingu żądań?

   **URI** (Uniform Resource Identifier): Nadrzędny termin na identyfikator zasobu. Może być URL-em, URN-em lub oboma.
   **URN** (Uniform Resource Name): Identyfikuje zasób po nazwie w danej przestrzeni, nie mówiąc, jak go znaleźć (np. `urn:isbn:9788328373752`).
   **URL** (Uniform Resource Locator): To URI, które nie tylko identyfikuje zasób, ale też mówi, *jak* do niego dotrzeć (np. `https://api.example.com/users`). Każdy URL jest URI, ale nie każde URI jest URL-em.

   Składowe URL: `schemat://użytkownik:hasło@host:port/ścieżka?zapytanie#fragment`
   Znaczenie dla routingu:
   **Host (domena/IP)**: Używany przez DNS oraz na load balancerach (SNI, nagłówek `Host`), by skierować ruch do właściwego serwera.
   **Port**: Wskazuje proces nasłuchujący na serwerze (np. 443 dla HTTPS).
   **Ścieżka (path)**: Używana przez routery warstwy 7 i kod aplikacji do wywołania konkretnego handlera/kontrolera.
   **Zapytanie (query string)**: Przekazuje dodatkowe parametry (filtry, paginacja) do handlera.
   **Fragment (hash)**: Przetwarzany wyłącznie po stronie klienta (przeglądarki), **nie jest wysyłany do serwera**.

4. Opisz pełny cykl życia żądania HTTP — od momentu wpisania URL w przeglądarkę do wyrenderowania odpowiedzi. Jakie warstwy i komponenty biorą w tym udział?

   1. **Parsowanie URL**: Przeglądarka rozdziela URL na schemat, domenę, port, ścieżkę. Sprawdza HSTS (czy od razu wymusić HTTPS).
   2. **Rozwiązanie DNS**: Sprawdza cache przeglądarki, systemowy (plik `hosts`), routera, a na końcu odpytuje serwery DNS (rekursywne -> root -> TLD -> autorytatywne), by zamienić domenę na adres IP.
   3. **Nawiązanie połączenia (L4/L6)**: 
      - Wykonywany jest **TCP 3-way handshake** (SYN -> SYN-ACK -> ACK). 
      - Następnie, jeśli używamy HTTPS, następuje **TLS Handshake** (negocjacja kluczy, weryfikacja certyfikatu, wyliczenie wspólnego sekretu).
   4. **Wysłanie żądania HTTP (L7)**: Przeglądarka buduje pakiet (metoda, ścieżka, nagłówki w tym np. `Host`, `Cookie`, opcjonalne body) i wysyła zaszyfrowany przez ustanowiony tunel.
   5. **Przetwarzanie przez infrastrukturę (Proxy/LB)**: Żądanie przechodzi przez firewalle, CDN-y, Load Balancery, Reverse Proxy, trafiając ostatecznie do aplikacji webowej.
   6. **Obsługa na serwerze**: Aplikacja webowa dekoduje HTTP, routuje żądanie, wykonuje logikę biznesową (np. odpytuje bazę danych), buduje odpowiedź (np. JSON lub HTML z kodem 200 OK) i odsyła do klienta.
   7. **Odbiór i renderowanie**: Przeglądarka odbiera dane. Jeśli to HTML, parsuje DOM, wysyła kolejne żądania po zasoby powiązane (CSS, JS, obrazki) — często wielowątkowo z wykorzystaniem HTTP/2 multiplexing. Ostatecznie renderuje stronę i wykonuje kod JS.
   8. **Zakończenie**: Połączenie TCP z reguły nie jest zamykane od razu (dzięki mechanizmowi keep-alive), lecz czeka w puli na ewentualne kolejne żądania.


5. Czym jest **persistent connection** (keep-alive) w HTTP/1.1 i jakie problemy rozwiązywało w porównaniu z HTTP/1.0?

   W HTTP/1.0 każde żądanie wymagało ustanowienia nowego połączenia TCP, a po wysłaniu odpowiedzi serwer natychmiast je zamykał. To powodowało ogromny narzut na **TCP handshake**, **TLS handshake** i problem związany z **TCP Slow Start** (każde nowe połączenie zaczyna od niskiej przepustowości okna i powoli "rozpędza" się w miarę potwierdzeń). 

   W HTTP/1.1 wprowadzono domyślnie **persistent connections** (znane też jako `Connection: keep-alive`). Dzięki temu wiele żądań/odpowiedzi (w trybie sekwencyjnym) może współdzielić to samo, już otwarte połączenie TCP. Rozwiązało to problem wysokiej latencji przy ładowaniu stron z wieloma zasobami statycznymi. Serwer i klient utrzymują otwarte gniazdo przez określony czas (timeout) lub do wysłania wyraźnego nagłówka `Connection: close`.

   **Czas trwania w stanie bezczynności (timeout):**
   Jeśli przez otwarte połączenie nie są przesyłane nowe żądania, serwer nie trzyma go w nieskończoność, by uniknąć wyczerpania zasobów (braku wolnych gniazd i wątków). Typowy czas utrzymywania takiego "bezczynnego" połączenia (Keep-Alive Timeout) jest krótki i zależy od domyślnej konfiguracji serwera, np.:
   - **Apache:** domyślnie **5 sekund**.
   - **Node.js:** domyślnie **5 sekund** (parametr `keepAliveTimeout`).
   - **Nginx:** domyślnie **75 sekund** (parametr `keepalive_timeout`).
   Po upływie tego czasu bezczynności serwer bezpiecznie zamyka gniazdo z poziomu protokołu TCP.

6. Czym jest **pipelining** w HTTP/1.1? Dlaczego w praktyce był rzadko używany i jakie miał ograniczenia?

   Pipelining to mechanizm w HTTP/1.1 pozwalający na wysłanie wielu żądań jednym połączeniem TCP bez czekania na odpowiedź do poprzednich. 

   W praktyce napotkał na ogromny problem **Head-of-Line (HoL) Blocking na warstwie HTTP**. Zgodnie z protokołem, serwer musiał zwracać odpowiedzi w dokładnie takiej samej kolejności, w jakiej nadeszły żądania. Jeśli pierwsze żądanie było ciężkie (np. wygenerowanie dużego raportu z bazy) lub pakiet TCP uległ utracie, wszystkie kolejne gotowe już odpowiedzi musiały czekać w kolejce. Ponadto, wiele serwerów proxy i firewalli błędnie implementowało pipelining, gubiąc żądania lub mieszając odpowiedzi, przez co większość przeglądarek wyłączyła ten mechanizm. Został on zastąpiony przez prawdziwy **multiplexing w HTTP/2**.

7. Opisz **szczegółowo proces nawiązania połączenia HTTP** — od rozwiązania DNS, przez TCP 3-way handshake, po wymianę pierwszego żądania i odpowiedzi. Ile round-tripów wymaga każdy etap?

   **RTT (Round-Trip Time)** to czas potrzebny na przebycie drogi pakietu w obu kierunkach — wysłanie sygnału od klienta do serwera i powrót odpowiedzi (potwierdzenia) od serwera do klienta. Zależy on w głównej mierze od fizycznej odległości, infrastruktury sieciowej oraz czasu przetwarzania przez routery. W sieciach mierzony jest w milisekundach (ms). Każdy etap wymagający pełnego RTT to moment, w którym sieć musi bezczynnie czekać na sygnał zwrotny, co sumuje się w postaci opóźnienia i wydłuża czas do pierwszego bajtu (TTFB).

   Proces (zakładając brak cache i świeże połączenie):
   1. **DNS Lookup (zwykle 1+ RTT):** Klient odpytuje serwer DNS (UDP lub TCP) o rekord A/AAAA dla domeny.
   2. **TCP 3-way Handshake (1 RTT):**
      - Klient wysyła `SYN`.
      - Serwer odpowiada `SYN-ACK`.
      - Klient wysyła `ACK` (często już z pierwszymi danymi, o ile nie ma TLS).
   3. **Wysłanie żądania HTTP i odbiór odpowiedzi (min. 1 RTT):**
      - Klient wysyła żądanie HTTP (np. `GET / HTTP/1.1`).
      - Serwer przetwarza i odsyła odpowiedź.

   Łącznie dla zwykłego HTTP/1.1 (bez TLS) daje to **2 RTT (TCP + HTTP) + czas DNS**. Dopiero po tym czasie (Time to First Byte - TTFB) klient zaczyna otrzymywać dane.

8. Jak **zastosowanie TLS** wpływa na proces nawiązania połączenia HTTP? Ile dodatkowych round-tripów wprowadza TLS 1.2 vs TLS 1.3? Jak techniki takie jak TLS 1.3 0-RTT, TCP Fast Open i session resumption redukują łączny czas do pierwszego bajtu odpowiedzi?

   Dodanie HTTPS wydłuża proces inicjalizacji o tzw. TLS Handshake, który następuje zaraz po TCP Handshake.
   **TLS 1.2:** Wymaga **2 dodatkowych RTT** (wymiana informacji o algorytmach `ClientHello`/`ServerHello`, przesłanie certyfikatu, weryfikacja kluczy `ClientKeyExchange`, zgoda na zmianę szyfru `ChangeCipherSpec` i `Finished`). Pełny start to 3 RTT (1 TCP + 2 TLS) przed żądaniem HTTP.
   **TLS 1.3:** Redukuje handshake do **1 RTT**. `ClientHello` od razu zawiera "zgadywane" parametry wymiany kluczy (key share). Start to 2 RTT (1 TCP + 1 TLS).

   Techniki optymalizacji (redukcja RTT):
   **TCP Fast Open (TFO):** Pozwala na wysłanie danych aplikacji (np. `ClientHello`) już w pierwszym pakiecie `SYN` (pojawia się 0 RTT na poziomie TCP dla kolejnych połączeń do tego samego hosta).
   **Session Resumption (TLS):** Użycie wcześniejszych kluczy sesji (Session IDs / Tickets) skraca handshake w TLS 1.2 do 1 RTT.
   **TLS 1.3 0-RTT (Early Data):** Pozwala wysłać pierwsze żądanie HTTP (np. GET) wraz z TLS `ClientHello` przy wznawianiu sesji. Redukuje narzut TLS do zera. Niesie ryzyko ataków *Replay Attack*, dlatego należy go stosować wyłącznie dla żądań idempotentnych (safe).

---

## 2. Metody HTTP i ich semantyka

9. Opisz semantykę metod **GET**, **POST**, **PUT**, **PATCH**, **DELETE**, **HEAD**, **OPTIONS** i **TRACE**. Kiedy stosowanie każdej z nich jest poprawne, a kiedy stanowi naruszenie konwencji REST?

   **GET**: Pobranie zasobu. Safe, idempotentna. Naruszenie REST: zmienianie stanu serwera (np. `GET /deleteUser?id=1`).
   **POST**: Utworzenie nowego zasobu podporządkowanego (często używane też jako "catch-all" dla operacji, które nie pasują do reszty). Niesafe, nieidempotentna.
   **PUT**: Całkowite nadpisanie (wymiana) zasobu pod wskazanym URL lub utworzenie go, jeśli URL jest znany klientowi. Idempotentna.
   **PATCH**: Częściowa modyfikacja zasobu (np. zmiana tylko pola `status`). Teoretycznie nie musi być idempotentna, ale najczęściej jest tak projektowana.
   **DELETE**: Usunięcie zasobu. Idempotentna (kolejne wywołania powinny zwracać np. 404 lub 200, ale ostateczny stan serwera to wciąż brak zasobu).
   **HEAD**: Działa jak GET, ale serwer zwraca same nagłówki, bez `body`. Służy do sprawdzania nagłówków (rozmiar, cache, `Last-Modified`) bez pobierania danych.
   **OPTIONS**: Zwraca metody HTTP obsługiwane dla danego zasobu (używane głównie w CORS Preflight).
   **TRACE**: Serwer odsyła z powrotem to, co otrzymał od klienta. Używane do debugowania proxy (często wyłączane, bo ułatwia ataki XST - Cross-Site Tracing).


10. Czym różni się metoda **PUT** od **PATCH**? Opisz sytuację, w której użycie PUT zamiast PATCH prowadzi do utraty danych.

   **PUT** służy do **całkowitego zastąpienia** (replace) zasobu nowym stanem. Jeśli przesyłasz payload `{ "name": "Kamil" }` na obiekt, który miał też pole `"age": 30`, to pole "age" powinno zostać skasowane (lub ustawione na null), ponieważ nadpisałeś cały obiekt.
   **PATCH** służy do **częściowej modyfikacji** (update). Przesłanie `{ "name": "Kamil" }` powinno zmienić tylko imię, a wiek pozostawić nienaruszony.

   **Sytuacja utraty danych:** 
   Mamy zasób `/users/1` z danymi `{"email": "a@b.com", "role": "admin"}`. Programista frontendu tworzy formularz tylko do zmiany e-maila. Wysyła: `PUT /users/1 {"email": "new@b.com"}`. Serwer, postępując zgodnie z semantyką PUT, podmienia cały obiekt na przekazany. Użytkownik traci pole `role` (nadpisane na null/wartość domyślną), tym samym tracąc uprawnienia administratora. W tym wypadku powinno się użyć PATCH.

11. Co oznacza, że metoda HTTP jest **idempotentna**? Które metody są idempotentne, a które nie? Dlaczego POST nie jest idempotentny i jakie ma to konsekwencje w systemach rozproszonych?

   Metoda jest idempotentna, jeśli jej wielokrotne, identyczne wywołanie przynosi na serwerze taki sam efekt (skutek uboczny) jak pojedyncze wywołanie.
   **Idempotentne:** GET, HEAD, PUT, DELETE, OPTIONS, TRACE.
   **Nieidempotentne:** POST, PATCH (najczęściej traktowane jako nieidempotentne, choć zależy to od implementacji).

   **Dlaczego POST nie jest:** Jeśli dwukrotnie wyślesz `POST /orders`, serwer utworzy dwa zamówienia, co zmienia stan systemu. W systemach rozproszonych oznacza to, że w przypadku awarii sieci (np. brak otrzymania odpowiedzi `201 Created` od serwera) klient nie może bezpiecznie ponowić (retry) żądania POST bez ryzyka zduplikowania operacji (np. podwójnego obciążenia karty kredytowej). Wymaga to implementacji mechanizmów po stronie biznesowej, np. nagłówków `Idempotency-Key`.

12. Co oznacza, że metoda HTTP jest **safe** (bezpieczna)? Jakie metody spełniają tę właściwość i jaki ma to związek z cachowaniem i prefetchingiem?

   Metoda jest *safe*, jeśli służy wyłącznie do pobierania danych i (z założenia) nie zmienia stanu na serwerze.
   **Metody bezpieczne:** GET, HEAD, OPTIONS, TRACE.

   **Związek z cachowaniem i prefetchingiem:**
   Ponieważ bezpieczne metody nie wprowadzają modyfikacji, infrastruktura sieciowa (CDN, proxy) oraz przeglądarki mogą swobodnie cachować ich odpowiedzi. Ponadto przeglądarki mogą "w ciemno" wysyłać żądania (prefetching), aby szybciej załadować linki, w które użytkownik może kliknąć. Gdyby metoda (np. GET) kasowała obiekt, prefetching doprowadziłby do niezamierzonego usunięcia zasobów. Z tego samego powodu web crawlery skanują tylko używając GET.

13. Jak działa metoda **OPTIONS** w kontekście mechanizmu **CORS preflight**? Kiedy przeglądarka wysyła preflight request i co musi zawierać odpowiedź serwera?

   CORS (Cross-Origin Resource Sharing) używa żądań typu preflight (przy użyciu metody OPTIONS), aby przed wysłaniem właściwego zapytania sprawdzić, czy serwer docelowy zezwala na zapytania cross-origin od danej domeny.

   Przeglądarka wysyła preflight, jeśli żądanie:
   Używa metody innej niż GET, HEAD, POST (np. PUT, DELETE).
   Zawiera niestandardowe nagłówki (np. `Authorization`, `X-Custom-Header`).
   Ma `Content-Type` inny niż trzy domyślne (`application/x-www-form-urlencoded`, `multipart/form-data`, `text/plain` — czyli np. popularny `application/json` wymusza preflight).

   **Odpowiedź serwera na preflight musi zawierać:**
   Status `200 OK` (lub 204).
   Nagłówek `Access-Control-Allow-Origin` (np. wskazujący na domenę klienta).
   Nagłówki `Access-Control-Allow-Methods` oraz `Access-Control-Allow-Headers`, potwierdzające akceptację tego, co przeglądarka zadeklarowała w żądaniu preflight.
   Opcjonalnie `Access-Control-Max-Age`, aby przeglądarka scachowała wynik preflightu.

14. Czym jest metoda **CONNECT** i jakie ma zastosowanie w kontekście tunelowania HTTPS przez proxy?

   Metoda `CONNECT` prosi proxy serwer HTTP o ustanowienie przezroczystego tunelu TCP do serwera docelowego (podanego jako parametr URL tej metody, np. `CONNECT api.example.com:443 HTTP/1.1`).

   **Zastosowanie (tunelowanie HTTPS):**
   Gdy klient znajdujący się za zaporą (proxy) chce połączyć się do zewnętrznego zasobu HTTPS, proxy nie może wejrzeć w zawartość, bo jest zaszyfrowana przez TLS, ani zmodyfikować nagłówków. Dlatego klient wysyła do proxy `CONNECT`. Gdy proxy otworzy połączenie L4 (TCP) do serwera docelowego, odpowiada klientowi statusem `200 Connection Established`. Od tego momentu proxy tylko bezwiednie przekazuje bajty w obie strony, a klient zaczyna TLS Handshake z docelowym serwerem całkowicie przez przezroczysty tunel.

---

## 3. Kody odpowiedzi i ich zaawansowana semantyka

15. Jaka jest struktura kodów odpowiedzi HTTP (klasy 1xx–5xx)? Opisz przynajmniej jeden mniej oczywisty kod z każdej klasy i jego zastosowanie.

   **1xx (Informational)**: Żądanie przyjęte, trwa procesowanie.
     - *Przykład:* `103 Early Hints` – serwer pozwala zasygnalizować przeglądarce, aby rozpoczęła preloading zasobów (np. CSS/JS), zanim główne żądanie (np. wygenerowanie HTML) zostanie zakończone.
   **2xx (Success)**: Żądanie zostało przyjęte i pomyślnie przetworzone.
     - *Przykład:* `206 Partial Content` – odpowiedź na Range request (używane przy streamingu wideo, pobieraniu dużych plików we fragmentach).
   **3xx (Redirection)**: Należy podjąć dalsze kroki (najczęściej zmiana URL), aby zakończyć żądanie.
     - *Przykład:* `304 Not Modified` – zasób nie zmienił się od czasu podanego w `If-None-Match` / `If-Modified-Since`. Klient powinien wczytać go z lokalnego cache.
   **4xx (Client Error)**: Błąd w żądaniu klienta (zła składnia, brak autoryzacji).
     - *Przykład:* `422 Unprocessable Entity` – payload jest poprawny syntaktycznie (np. to prawidłowy JSON), ale zawiera błędy semantyczne/walidacyjne (np. brakujący znak @ w adresie e-mail).
   **5xx (Server Error)**: Serwer napotkał problem przy poprawnym żądaniu.
     - *Przykład:* `502 Bad Gateway` – serwer (działający jako proxy lub gateway) otrzymał nieprawidłową lub brakującą odpowiedź od serwera upstream (np. nginx nie może połączyć się z padniętą aplikacją Node.js/Java).

16. Czym różni się **301 Moved Permanently** od **308 Permanent Redirect**? Kiedy przeglądarka może zmienić metodę HTTP przy przekierowaniu i dlaczego to stanowi problem?

   Oba kody informują o permanentnym przeniesieniu zasobu. Różnica polega na zachowaniu metody HTTP.
   Przy kodzie **301**, przeglądarki historycznie potrafiły zmienić metodę żądania z POST na GET przy podążaniu za przekierowaniem (co często gubiło też body żądania). 
   Kod **308** to nowszy standard z HTTP/1.1 (wprowadzony w RFC 7538), który **kategorycznie zabrania** zmiany metody i usuwania body. Jeśli klient wysłał POST, na nowy adres też musi wysłać POST.

   Zmiana metody przy 301 stanowiła problem np. przy wysyłaniu formularzy do zmigrowanego API, gdzie nagle endpoint otrzymywał GET zamiast POST, co prowadziło do błędów `405 Method Not Allowed`.

17. Czym różni się **302 Found** od **303 See Other** i **307 Temporary Redirect**? Dlaczego historyczne zachowanie 302 było problematyczne?

   Wszystkie kody dotyczą tymczasowego przekierowania, ale powstały, by naprawić niejednoznaczność kodu 302.
   **302 Found**: Historycznie miał oznaczać "spróbuj tego adresu tym razem", zachowując metodę. Jednak wczesne przeglądarki zmieniały POST na GET.
   **303 See Other**: Wymusza zmianę na metodę GET. Używane powszechnie we wzorcu *Post/Redirect/Get* (PRG). Po pomyślnym odebraniu formularza przez POST, serwer zwraca 303, a klient ładuje widok sukcesu używając GET, by zapobiec podwójnemu wysłaniu danych po odświeżeniu strony.
   **307 Temporary Redirect**: Stanowczo zakazuje zmiany metody (podobnie jak 308 dla przekierowań stałych). Jeśli wysłałeś POST, zrób POST na nowy adres.

18. Opisz scenariusze użycia kodów **409 Conflict**, **412 Precondition Failed** i **428 Precondition Required**. Jak wspierają one optymistyczną kontrolę współbieżności?

   **409 Conflict**: Zwracany, gdy żądanie kłóci się z obecnym stanem zasobu po stronie biznesowej, np. próba rejestracji użytkownika na e-mail, który już istnieje.
   **428 Precondition Required**: Wymusza na kliencie użycie nagłówków warunkowych (np. `If-Match`). Serwer mówi: "Nie pozwolę ci zaktualizować tego zasobu, jeśli nie udowodnisz, że znasz jego najnowszą wersję".
   **412 Precondition Failed**: Klient dołączył nagłówek warunkowy (np. `If-Match: "v1"`), ale stan na serwerze jest już inny (np. "v2"). Serwer odrzuca żądanie.

   **Optymistyczna kontrola współbieżności (Optimistic Locking):**
   Klient pobiera zasób (otrzymuje ETag "v1"). Edytuje go, po czym wysyła PUT wraz z `If-Match: "v1"`. Jeśli ktoś inny w międzyczasie zmodyfikował ten zasób na serwerze, ETag wynosi "v2". Serwer zobaczy niezgodność i zwróci `412 Precondition Failed`, co zapobiegnie nadpisaniu czyjejś pracy (lost update problem). Jeśli klient nie podałby `If-Match`, a serwer go wymaga, zwróci `428`.

19. Kiedy stosuje się **429 Too Many Requests**? Jakie nagłówki towarzyszą tej odpowiedzi i jak klient powinien reagować?

   Stosuje się go, gdy klient przekroczył ustalony limit wywołań (rate limiting), by zabezpieczyć serwer przed przeciążeniem lub wymusić progi licencyjne. 

   Serwer często (i powinien) dołączać nagłówek **`Retry-After`**, wskazując (w sekundach lub formacie daty), kiedy klient może podjąć kolejną próbę.
   Klient w odpowiedzi powinien zastosować mechanizm wstrzymania żądań (backoff) oparty na wartości z `Retry-After`. Powszechną praktyką jest implementacja *Exponential Backoff with Jitter* (dla innych błędów) lub dostosowanie się precyzyjnie do wskazań tego nagłówka.

20. Czym różni się **502 Bad Gateway** od **503 Service Unavailable** i **504 Gateway Timeout**? Jak te kody wpływają na strategię retry po stronie klienta?

   Te błędy pojawiają się w architekturach wielowarstwowych (np. proxy -> mikroserwis).
   **502 Bad Gateway**: Proxy (lub LB) zdołało połączyć się z upstreamem, ale otrzymało nieprawidłową odpowiedź (lub upstream natychmiast zerwał połączenie/wycrashował).
   **504 Gateway Timeout**: Proxy połączyło się z upstreamem, wysłało zapytanie, ale nie otrzymało odpowiedzi przed upływem określonego limitu czasu (timeout).
   **503 Service Unavailable**: Aplikacja/serwer działa, ale nie może obecnie obsłużyć żądania (np. przeciążenie, brak wolnych wątków w puli, trwa maintenance/draining, nie przeszedł health-checków).

   **Strategia retry:** 
   Dla 502/503/504 retry (z opóźnieniem / exponential backoff) ma zwykle sens (bo to problemy tranzytowe), ale z zastrzeżeniem: przy 504 nie wiemy, czy upstream *nie wykonał* zadania, czy *tylko zbyt wolno odpowiedział*. Retry metod non-idempotentnych (jak POST) przy 504 jest bardzo niebezpieczne. Warto też nasłuchiwać nagłówka `Retry-After`, który często towarzyszy kodowi 503.

21. Kiedy serwer powinien zwrócić **204 No Content** zamiast **200 OK** z pustym body? Jaka jest semantyczna różnica?

   Kod `204 No Content` semantycznie oznacza "żądanie powiodło się, ale nie mam nic więcej do zwrócenia, a klient nie musi zmieniać swojego widoku dokumentu". Jest on idealny dla operacji, które realizują jedynie skutki uboczne na serwerze i nie wymagają odświeżenia UI (np. pomyślne usunięcie zasobu metodą DELETE, zapisanie dokumentu w tle przez PUT).
   Kod `200 OK` z pustym body oznacza "sukces", ale sugeruje, że odpowiedź jest właściwym dokumentem (nawet jeśli ma 0 bajtów długości). Przeglądarka traktuje 200 jako nowy zasób i może spróbować wyrenderować pusty dokument, podczas gdy przy 204 celowo pozostanie na dotychczasowej stronie.

22. Czym jest kod **100 Continue** i w jakim scenariuszu klient wysyła nagłówek `Expect: 100-continue`? Jakie korzyści to daje przy dużych payloadach?

   Kod `100 Continue` to status informacyjny. Scenariusz jego użycia pojawia się, gdy klient chce wysłać do serwera bardzo duże żądanie (np. upload pliku wideo przez POST), ale najpierw chce się upewnić, czy serwer w ogóle zechce je przyjąć.
   Zamiast wysyłać cały plik w ciemno, klient wysyła najpierw tylko nagłówki (w tym `Content-Length`, `Authorization`) oraz nagłówek `Expect: 100-continue` i wstrzymuje wysyłanie body.
   Serwer analizuje nagłówki. Jeśli klient nie ma uprawnień lub payload jest zbyt duży, serwer od razu zwraca błąd (np. 401 lub 413 Payload Too Large). Jeśli serwer akceptuje żądanie, zwraca tymczasowy status `100 Continue`, po czym klient rozpoczyna transfer danych. Pozwala to na ogromną oszczędność przepustowości przy odrzucanych żądaniach.

---

## 4. Nagłówki HTTP — zaawansowane użycie

23. Czym jest **content negotiation** i jakie nagłówki biorą w nim udział (`Accept`, `Accept-Language`, `Accept-Encoding`, `Accept-Charset`)? Jak serwer podejmuje decyzję w przypadku wielu wariantów?

   Content negotiation (negocjacja zawartości) to mechanizm pozwalający serwerowi zwrócić różne warianty tego samego zasobu w zależności od preferencji klienta.
   Wysłane nagłówki określają preferencje:
   `Accept`: Oczekiwany format zasobu (np. `application/json`, `text/html`).
   `Accept-Language`: Oczekiwany język (np. `pl-PL`, `en-US`).
   `Accept-Encoding`: Obsługiwane algorytmy kompresji (np. `gzip`, `br`).
   `Accept-Charset`: Obsługiwane kodowanie znaków (obecnie dominuje utf-8).

   Serwer opiera decyzję na tzw. wartościach jakości (parametr `q` w zakresie 0.0-1.0, np. `Accept-Language: pl;q=1.0, en;q=0.5`). Serwer analizuje te wagi i wybiera dostępny wariant, który najlepiej odpowiada preferencjom klienta. Jeśli nie jest w stanie dopasować żadnego wariantu, zwraca domyślny lub błąd `406 Not Acceptable`.

24. Opisz działanie nagłówka **`Transfer-Encoding: chunked`**. Kiedy jest niezbędny i jak wpływa na streaming odpowiedzi?

   W HTTP/1.1 `Transfer-Encoding: chunked` pozwala przesyłać odpowiedź w podzielonych fragmentach (chunkach), z pominięciem nagłówka `Content-Length` (kiedy całkowity rozmiar body nie jest początkowo znany). Każdy chunk rozpoczyna się jego rozmiarem szesnastkowym, po którym następują dane, a transmisję kończy specjalny pusty chunk o rozmiarze 0.
   **Niezbędny, gdy:** Serwer generuje odpowiedź na bieżąco w locie (np. strumieniowanie bardzo dużego raportu z bazy danych lub komunikacja Server-Sent Events).
   Mechanizm ten skraca Time to First Byte (TTFB), ponieważ serwer może natychmiast wysyłać wygenerowane fragmenty odpowiedzi bez oczekiwania na zakończenie budowy całego payloadu i bez buforowania go w pamięci operacyjnej. W HTTP/2 został wyparty przez natywne ramkowanie protokołu.

25. Czym jest nagłówek **`Content-Encoding`** i czym różni się od `Transfer-Encoding`? Jak działają razem?

   **`Content-Encoding`** (End-To-End) informuje, w jaki sposób zdekodowano lub skompresowano ostateczny zasób (np. algorytmem `gzip` czy `br`), aby zmniejszyć jego rozmiar. Wymaga to odpowiedniej dekompresji po stronie końcowej aplikacji klienta przed jej przetworzeniem.
   **`Transfer-Encoding`** (Hop-By-Hop) określa sposób na bezpieczne dzielenie strumienia i przesyłanie samego komunikatu HTTP poprzez sieć na poziomie protokołu (najczęściej w `chunked`).

   **Jak działają razem:** Serwer aplikacji generujący duży wynik może go w locie kompresować (ustawiając `Content-Encoding: gzip`). Ponieważ rozmiar końcowy skompresowanego pliku nie jest znany do końca, poszczególne skompresowane części wysyła strumieniem przez sieć ubrane w chunki (ustawiając `Transfer-Encoding: chunked`). Klient odbiera z sieci łączone chunki, tworząc z nich ciągły plik zip, który w czasie rzeczywistym dekompresuje.

26. Opisz mechanizm **conditional requests** — jakie nagłówki (`If-Modified-Since`, `If-None-Match`, `If-Match`, `If-Unmodified-Since`) biorą w nim udział i w jakich scenariuszach?

   Mechanizm "conditional requests" (żądania warunkowe) pozwala na wykonanie żądanej metody HTTP tylko wtedy, gdy stan zasobu na serwerze spełnia określone warunki sprawdzane na podstawie walidatorów (takich jak `ETag` lub `Last-Modified`).
   Scenariusze:
   **Rewalidacja pamięci podręcznej (Cache):** Klient chcąc pobrać zasób (GET) wysyła do serwera walidatory ze swojego cache używając `If-None-Match: <ETag>` lub `If-Modified-Since: <Date>`. Jeśli zasób nie został zmieniony, serwer zwraca kod `304 Not Modified`, powiadamiając, by klient użył swojego lokalnego pliku, co oszczędza transfer payloadu.
   **Optymistyczna kontrola współbieżności:** Przy modyfikacjach (PUT/PATCH) klient wysyła `If-Match: <ETag>`, wnosząc: "Zaktualizuj ten zasób pod warunkiem, że jego bieżąca wersja na serwerze to wciąż mój ETag". Chroni to przed przypadkowym nadpisaniem zmian (tzw. "lost update problem"), gdy ktoś inny w międzyczasie zmodyfikował zasób. W razie niezgodności serwer odrzuca żądanie ze statusem `412 Precondition Failed`.

27. Czym jest nagłówek **`Vary`** i jaki ma wpływ na cachowanie odpowiedzi? Podaj przykład, w którym brak `Vary` prowadzi do serwowania błędnych treści z cache.

   Nagłówek `Vary` instruuje wszystkie serwery pośredniczące (proxy, CDN) oraz przeglądarki o tym, że odpowiedź jest negocjowana i zależy od zawartości konkretnych nagłówków z żądania klienta. Innymi słowy, wymusza on włączenie podanych nagłówków do "klucza pamięci podręcznej" (cache key), aby cache nie traktował samego URL-a jako jedynego wyznacznika zasobu.

   **Przykład braku `Vary`:** Endpoint `/api/data` zwraca JSON lub XML w zależności od tego, co klient wyśle w nagłówku `Accept`. Gdy pierwszy klient żąda XML (`Accept: application/xml`), odpowiedź XML trafia do CDN. Jeśli serwer nie dołączył w niej `Vary: Accept`, CDN uzna ten plik XML za uniwersalnie pasujący dla dowolnego żądania `/api/data`. Kiedy następnie przyjdzie żądanie od klienta oczekującego formatu JSON (`Accept: application/json`), CDN wyda mu błędny, scachowany XML. Poprawne dołączenie `Vary: Accept` zmusza CDN do trzymania osobnej kopii pliku dla XML i osobnej dla JSON pod tym samym URL.

28. Czym jest nagłówek **`Host`** i dlaczego jest wymagany w HTTP/1.1? Jak ma się do **`:authority`** pseudo-nagłówka w HTTP/2?

   Nagłówek `Host` definiuje nazwę domeny docelowej (oraz opcjonalnie port) i jest **jedynym nagłówkiem bezwzględnie wymaganym w żądaniach w standardzie HTTP/1.1**.
   Istnienie tego wymogu wynika z powszechności wirtualnego hostingu (Virtual Hosting). Wraz z wyczerpywaniem się publicznych adresów IPv4, dostawcy hostingu zaczęli utrzymywać tysiące różnych witryn (domen) na jednym, wspólnym fizycznym adresie IP serwera (np. za pomocą Nginx lub Apache). Pakiet wędrujący przez protokół TCP/IP dociera na ten adres IP nie wiedząc o domenie. Dopiero tekstowy nagłówek `Host` zawarty w HTTP mówi serwerowi na L7, o którą konkretnie aplikację prosi klient, pozwalając na poprawny routing wewnętrzny (do konkretnego vhosta).
   W specyfikacji binarnej HTTP/2 koncepcja tego nagłówka została przeniesiona do standaryzowanego pseudo-nagłówka o nazwie **`:authority`**, który dziedziczy jego przeznaczenie oraz semantykę.

29. Jak działa nagłówek **`Forwarded`** (i starsze `X-Forwarded-For`, `X-Forwarded-Proto`)? Jakie problemy bezpieczeństwa wiążą się z ich niekontrolowanym zaufaniem?

   Te nagłówki stanowią mechanizm demaskowania oryginalnego adresata w architekturach zawierających bramki. Główna aplikacja ukryta w prywatnej sieci, do której ruch trafia przez Load Balancer lub Reverse Proxy, widziałaby w logach połączeń L4 jedynie adres IP tego własnego proxy. By ocalić wiedzę o oryginalnym użytkowniku, proxy wstrzykuje informacje do żądania używając starszych nagłówków: `X-Forwarded-For` (Oryginalny IP klienta) czy `X-Forwarded-Proto` (Początkowy protokół np. https). RFC w nowym standardzie ujednolica to pod postacią scentralizowanego nagłówka `Forwarded: for=192.168.0.1;proto=https`.

   **Problemy bezpieczeństwa (IP Spoofing):**
   Bezwarunkowe zaufanie zawartości tych nagłówków prowadzi do luk bezpieczeństwa. Dowolny haker wysyłający żądanie bezpośrednio ze swojego komputera może samodzielnie dołączyć zmanipulowany nagłówek `X-Forwarded-For: 127.0.0.1`. Aplikacja naiwnie zdekoduje ten "wewnętrzny" adres i może go przepuścić przez rate limity czy logikę dostępów z Intranetu, dając mu uprawnienia administratora. Aplikacja powinna respektować `X-Forwarded-*` tylko wtedy, jeśli połączenie L4 nadeszło bezpośrednio ze zbadanego i w pełni zaufanego lokalnego klastra proxy (który przedtem czyści oszukane nagłówki użytkowników zewnętrznych).

30. Czym jest nagłówek **`Trailer`** i kiedy ma zastosowanie w kontekście chunked transfer encoding?

   Nagłówek `Trailer` to sposób na poinformowanie klienta z góry o tym, że zaraz po przetransferowaniu właściwego ciała zasobu (body), w samej końcówce przesyłanego żądania znajdą się dołączone specjalne dodatkowe nagłówki.
   **Zastosowanie:** Rozwiązuje ułomności streamingu podziałowego `Transfer-Encoding: chunked`. Otwierając długi transfer wielkiego pliku generowanego w locie, serwer HTTP na początku transmisji nie jest w stanie przewidzieć pewnych parametrów metadanych dla całego wyniku, takich jak suma kontrolna całego pliku dla weryfikacji. Wysyłając więc w standardowych pierwszych nagłówkach deklarację `Trailer: Content-MD5`, serwer obiecuje wyliczenie i dowiezienie hashów pod sam koniec transmisji, po zamknięciu strumienia zerowym chunkiem, zapewniając integralność. Z mechanizmu Trailerów namiętnie korzystają systemy gRPC (przesyłając w ogonie opóźnione statusy kodów błędów asynchronicznej operacji nad HTTP/2).

---

## 5. Cachowanie HTTP

31. Opisz pełny model cachowania HTTP. Jakie komponenty mogą cachować odpowiedzi (przeglądarka, CDN, reverse proxy, shared cache)?

   Model buforowania HTTP wielowarstwowo minimalizuje potrzebę wysyłania pełnych zapytań do serwera aplikacyjnego, drastycznie zmniejszając opóźnienia i redukując obciążenie sieci:
   1. **Prywatny Cache Przeglądarki (Private / Local Cache)**: Pierwsza warstwa, pamięć podręczna na urządzeniu docelowego użytkownika. Pozwala przeglądarce omijać konieczność korzystania z sieci przy odświeżeniach. Pamięć ta jest izolowana i w pełni dedykowana tylko dla tego pojedynczego użytkownika.
   2. **Reverse Proxy / Gateway Cache (np. Nginx, Varnish)**: Serwery buforujące na granicy infrastruktury organizacji (często tuż przed API). Zatrzymują żądania blisko aplikacji chroniąc bazy danych przed koniecznością renderowania stałych wyników na tysiące takich samych zapytań.
   3. **CDN (Content Delivery Network / Edge Cache)**: Ogólnoświatowe klastry typu Shared Cache utrzymujące skopiowane i zoptymalizowane zasoby z głównego serwera na geograficznie rozproszonych serwerach (Edge). Dostarczają ogromnemu tłumowi (współdzielenie plików publicznych) szybkie pobrania zasobów zlokalizowane blisko nich fizycznie.
   4. **Forward Proxy / Proxy Firmowe**: Rzadko używane na skutek powszechnego szyfrowania end-to-end w HTTPS (co uniemożliwia im wgląd w zapytania i zapisywania ciał wiadomości), są to brzegowe proxy operatorów sieci LAN (np. w korporacjach czy na uczelniach).

32. Czym różni się dyrektywa **`Cache-Control: no-cache`** od **`no-store`**? Dlaczego `no-cache` nie oznacza „nie cachuj"?

   Nazewnictwo tych atrybutów bywa często źródłem krytycznych błędów konfiguracyjnych u deweloperów.
   **`no-cache`**: Oznacza, że warstwy cache (np. przeglądarka) mają pełne prawo zapisać odpowiedź u siebie na dysku, jednak z bezwzględnym zakazem zaserwowania tego pliku bez dokonania asynchronicznej twardej **rewalidacji**. Przeglądarka przy każdym wejściu musi spytać serwer używając walidatora (np. ETag), czy ten zachowany plik jest wciąż aktualny (na co serwer zazwyczaj oszczędnie odpowiada pustym ciałem 304 Not Modified).
   **`no-store`**: To dyrektywa "nigdy nie buforuj". Stanowczo i kategorycznie zabrania zapisywania odpowiedzi w jakiejkolwiek skrytce cache i zmusza do usuwania powiązań z nią, wymuszając by przy każdej próbie pełne i nowo wygenerowane od góry do dołu pobieranie zawartości i pliku (stosowane dla ściśle wrażliwych danych).

33. Opisz różnicę między **`Cache-Control: private`** a **`public`**. W jakich scenariuszach `private` jest krytyczne dla bezpieczeństwa?

   Kontrolują one zakres pozwoleń na miejsce składowania i uprawnień podziału bufora wśród architektury sieci.
   **`public`**: Informuje, że każda istniejąca po drodze skrytka z buforem w sieci jest uprawniona w pełni zapisać odpowiedź dla wszystkich mas by serwować ją ogółowi po URL-u bez ograniczeń (np. współdzielone sieci CDN).
   **`private`**: Zezwala na zachowanie i zbuforowanie wywoływanej odpowiedzi wyłącznie w prywatnej skrytce z ograniczonym dostępem dedykowanej autoryzowanemu, wywołującemu klientowi (w cache docelowej aplikacji jego przeglądarki). Bezwzględnie zabrania CDN-om przechowywania i re-serwowania tego zasobu innym użytkownikom.

   **Scenariusz krytyczny:** Jeśli endpoint `/user/dashboard` serwuje dane osobiste i stan subskrypcji zalogowanego usera jako `public` (lub zapomni nałożyć `private` a na serwerze CDN trzyma cache pod ten URI), żądanie i widok spersonalizowany wyrenderowany przy pierwszym odwiedzeniu zostanie pochłonięty przez klaster krawędziowy CDN. Każdy inny anonimowy z tłumu, kto zapyta o ścieżkę tegoż endpointu, zostanie obdarzony prywatnymi informacjami spersonalizowanymi należącymi stricte do pierwszego usera z pobrania.

34. Jak działa mechanizm **rewalidacji** cache z użyciem **ETag** i **Last-Modified**? Czym różni się strong ETag od weak ETag?

   Gdy zachowanemu w pamięci cache plikowi skończy się dopuszczalny z góry limit czasu ważności (określony atrybutem `Max-Age`), przeglądarka przed jego nadpisaniem wywołuje żądanie rewalidacyjne pytające API serwera: "Moja zapisana dotychczas wersja właśnie wygasła, czy wciąż jest poprawna, czy mam pobierać nową?". 
   Dla weryfikacji aplikacja wysyła powiązane zachowane wartości ze starych nagłówków: np. zachowany podpis Hash pliku w `If-None-Match` uderzając w `ETag`, lub starą datę dla `If-Modified-Since`.
   Serwer aplikacyjny w logice weryfikuje token, jeśli na produkcji nowszych modyfikacji nie ma po poświadczeniach — serwer przedłuża plik odsyłając bardzo szybki i pusty status `304 Not Modified`, wyłączając narzut pełnego body.

   **ETag Strong vs Weak:**
   **Silny "Strong" (np. `ETag: "94x"`):** Wymaga, by po serwerze cała zawartość pliku (łącznie z odstępami bitowymi układu całego body) była bezwzględnie identycznie sformatowana do kopii u klienta. Działa w rygorze na potrzebach HTTP Resume Download do wznawiania plików po ucięciu rwania sieci.
   **Słaby "Weak" (np. `ETag: W/"94x"`):** Ręczy tylko i wyłącznie o poprawności semantycznej wiedzy zawartej w pliku pod treści i znaczenia merytoryczne zasobu. Pozwala ominąć rewalidacje i zignorować drobne zmiany np. u w rotującej banerami reklamowej treści HTML generowanych artykułów.

35. Czym jest **`stale-while-revalidate`** i **`stale-if-error`**? Jak te dyrektywy wpływają na dostępność i wydajność?

   Te atrybuty do nagłówka Cache-Control to potężne narzędzia optymalizacyjne skrajnie poprawiające UX i maskujące niestabilności infrastruktury.
   **`stale-while-revalidate`**: Gdy kopia pliku wygaśnie pod limitem czasowym `max-age`, klient (lub CDN) nie zatrzymuje procesu renderowania na czas żądania upewniającego. Zamiast tego od razu serwuje "nieświeży" (stale) plik z cache z zerowym narzutem TTFB, a "asynchronicznie w tle" serwer CDN odpala żądanie rewalidacyjne do oryginalnego API, aktualizując cache dla przyszłych użytkowników bez spowalniania obecnej sesji.
   **`stale-if-error`**: Tolerancja w przypadku awarii. Kiedy infrastruktura padnie i główny serwer zaczyna rzucać błędami `5xx` lub timeoutami, a w cache CDN leży już wygasły plik, serwer CDN nie wyrzuci błędu dla użytkownika. Awaryjnie wydłuży okno i zaserwuje ostatni znany (stary, ale wciąż działający) stan odpowiedzi, jako fallback do momentu podniesienia backendu.

36. Jak zaprojektować strategię **cache busting** dla zasobów statycznych? Jakie podejścia (query string, fingerprinting, immutable) mają jakie kompromisy?

   Cache Busting to przymusowe natychmiastowe unieważnienie długoterminowo zbuforowanych plików (np. u wszystkich klientów naraz), wymuszając pobranie nowych tuż po deploymencie.
   **Query String (np. `main.css?v=2`)**: Łatwe w implementacji (zmiana argumentu URL), ale obecnie odradzane. Cześć starych pośredników (proxy) ignoruje parametry przy budowaniu klucza cache i nadal zaserwuje stary plik.
   **File Fingerprinting / Content Hashing (np. `main.b13x.css`)**: Standard dzisiejszych narzędzi jak Webpack/Vite. Skrót z zawartości pliku staje się częścią jego nazwy. Gwarantuje natychmiastowe odświeżenie (bo odnośnik ze zmodyfikowanego pliku HTML wskazuje na całkowicie nowy i unikalny adres URI w sieci). Wymusza to jednak generowanie wielu martwych artefaktów plików przy buildach.
   W profesjonalnym środowisku nowoczesny cache busting to połączenie File Fingerprintingu ze statycznym ustawieniem na nich atrybutu `immutable`.

37. Czym jest **`Cache-Control: immutable`** i kiedy jego użycie jest bezpieczne?

   Dyrektywa `immutable` to zobowiązanie oznaczające "Ten zasób w tej fizycznej inkarnacji i pod tym dokładnie linkiem nigdy w czasie swojego istnienia nie ulegnie modyfikacji". Jej wprowadzenie ostatecznie redukuje do zera wymuszanie niepotrzebnych rewalidacji u użytkownika w sytuacjach odświeżenia okna. Klasycznie, wymuszone odświeżenie (F5) przerywało domyślny `max-age` wysyłając tysiące zapytań o pliki skryptów prosząc o kod `304 Not Modified`. Atrybut ten zmusza przeglądarkę do bezwzględnego zaufania dyskowi, omijając w ogóle uderzenia po 304.

   Użycie `immutable` jest w pełni bezpieczne **tylko** wtedy, gdy adres pliku bazuje na Content Hashingu (`app.13dfz.js`). Dzięki temu, nawet jeśli kod ulegnie zmianie, to nie próbujemy uaktualnić pliku pod aktualnym adresem (co przy immutable by się nie udało i trwale powiesiło użytkownika na błędnej wersji pliku), lecz kompilator po prostu zmienia nazwę wyjściowego pliku i podmienia referencje URL w dokumencie HTML na całkowicie nowy adres.


38. Jak CDN-y obsługują **cache invalidation** i dlaczego jest to trudne operacyjnie? Jakie strategie purge/invalidation stosują nowoczesne CDN-y?

   Czyszczenie (Purging) to przedwczesne usuwanie buforowanych kopii u masowych węzłów krawędziowych CDN w celu wymuszenia uderzenia klientów po nową zawartość do źródła (Origin API). Jest to wybitnie skomplikowane operacyjnie z uwagi na potężną dystrybucję serwerów globalnych i nieuniknione opóźnienia, przez które w zjawisku propagacji część regionów na świecie odbiera inne stany dla pliku niż inne z racji opóźnień asynchronicznego usuwania na każdym sprzęcie. Dodatkowo globalne twarde unieważnienie wielkiego zasobu uderzy natychmiastowym tłumem odwiedzających w jeden mały docelowy API backend zjawiskiem "**Cache Stampede**", co dławi pule połączeń w bazach i powala oryginalny serwer na kolana.

   Strategie u nowoczesnych dostawców:
   **Soft Purging:** Usuwanie w stanie miękkim. Zamienia znacznik plików na "wygaśnięcia awaryjnego (stale)". Żądania masowe od usera od razu załagodzone starym, czerstwym plikiem od ratunku nie wywołują stampede i odciążają bazę, a CDN sam wykonuje z tyłu rewalidacyjne jedno asynchroniczne zapytanie ratując serwer z API przed uśmierceniem od uderzeń.
   **Surrogate Keys (Tag-based Invalidation):** Rewolucja opierająca się o grupowanie niewidocznymi tokenami podłączonymi pod dany zasób od serwera (np. wpisany meta nagłówek z `Surrogate-Key: user-1, posts`). Wysłanie komendy by "wyczyścić wszystkie skrytki dla tagu posts" potrafi grupowo kaskadowo skasować na całym świecie setki podstron zależnych od API bloga o nieznanych mu i trudnych do wylistowania ręcznie URL-ach.

---

## 6. Bezpieczeństwo w HTTP

39. Opisz mechanizm **CORS** (Cross-Origin Resource Sharing). Jakie nagłówki kontrolują politykę CORS i jakie błędy konfiguracyjne prowadzą do podatności?

   CORS to mechanizm wbudowany w przeglądarki, łagodzący rygorystyczną politykę Same-Origin Policy (SOP). Pozwala on aplikacjom na jednej domenie (np. `frontend.com`) w sposób kontrolowany żądać zasobów z innej domeny (np. `api.backend.com`). Działa poprzez wymianę nagłówków między przeglądarką a serwerem docelowym (często poprzedzoną żądaniem Preflight z użyciem metody OPTIONS).
   **Główne nagłówki:**
   `Access-Control-Allow-Origin`: (Najważniejszy) Określa, jakie domeny mogą czytać odpowiedź.
   `Access-Control-Allow-Methods`: Jakie metody (GET, POST itp.) są dozwolone.
   `Access-Control-Allow-Headers`: Jakie customowe nagłówki klient może wysłać.
   `Access-Control-Allow-Credentials`: Czy przeglądarka może dołączyć ciasteczka uwierzytelniające (cookies) do żądania cross-origin.
   **Błędy konfiguracyjne (Podatności):**
   1. Ustawienie `Access-Control-Allow-Origin: *` w połączeniu z `Access-Control-Allow-Credentials: true` (choć specyfikacja tego zabrania, niektóre stare parsery to puszczały, co pozwalało na kradzież sesji).
   2. Dynamiczne, bezkrytyczne odbijanie nagłówka `Origin`. Jeśli serwer czyta `Origin: https://evil.com` i automatycznie odpowiada `Access-Control-Allow-Origin: https://evil.com`, atakujący może stworzyć złośliwą stronę, a API zaakceptuje jej żądania jak z zaufanego frontendu.

40. Czym jest atak **CSRF** (Cross-Site Request Forgery)? Jakie mechanizmy HTTP (tokeny, SameSite cookies, Origin/Referer checking) chronią przed nim?

   Atak CSRF polega na zmuszeniu uwierzytelnionego użytkownika do nieświadomego wykonania akcji w systemie, w którym jest aktualnie zalogowany. Ponieważ przeglądarki historycznie automatycznie dołączały ciasteczka sesyjne do każdego żądania (nawet tych inicjowanych z innych domen, np. po kliknięciu w złośliwy link `<img src="http://bank.com/transfer?amount=1000&to=hacker">`), żądanie wyglądało dla serwera na w pełni autoryzowane.

   **Mechanizmy obrony:**
   1. **Atrybut `SameSite` w Cookies:** Obecnie najważniejsza obrona wbudowana w HTTP. Ustawienie `SameSite=Lax` lub `Strict` sprawia, że przeglądarka po prostu nie wyśle ciasteczka sesyjnego, jeśli żądanie POST (lub dowolne przy Strict) pochodzi z innej domeny.
   2. **Anti-CSRF Tokens (Synchronizer Token Pattern):** Serwer wstrzykuje w formularz na stronie unikalny, jednorazowy token kryptograficzny. Przy wysłaniu formularza, token ten musi zostać przesłany z powrotem w payloadzie (a nie w cookie). Atakujący, nie mając dostępu do DOM strony (przez SOP), nie zna tego tokenu i nie może spreparować poprawnego zapytania POST.
   3. **Weryfikacja nagłówków `Origin` i `Referer`:** Serwer sprawdza, z jakiej domeny pochodzi żądanie. Wymaga to jednak staranności, gdyż nagłówki te mogą czasem nie być wysyłane ze względów prywatności.

41. Jak działają nagłówki bezpieczeństwa: **`Content-Security-Policy`**, **`Strict-Transport-Security`**, **`X-Content-Type-Options`**, **`X-Frame-Options`**, **`Referrer-Policy`**? Opisz konsekwencje ich braku.

   To krytyczne deklaracje informujące przeglądarkę o dozwolonych zachowaniach, chroniące przed atakami po stronie klienta.
   **`Content-Security-Policy` (CSP):** Definiuje białą listę źródeł, z których przeglądarka może ładować zasoby (np. `default-src 'self'; script-src https://trusted.cdn.com`). Konsekwencja braku: Aplikacja jest podatna na ataki XSS (Cross-Site Scripting), bo przeglądarka wykona każdy wstrzyknięty złośliwy skrypt.
   **`Strict-Transport-Security` (HSTS):** Zmusza przeglądarkę do bezwzględnego używania protokołu HTTPS dla domeny przez określony czas (`max-age`). Brak: Ryzyko ataków Man-in-the-Middle (MitM) przy początkowych żądaniach na porcie 80 (np. ssl-stripping).
   **`X-Content-Type-Options: nosniff`**: Blokuje zjawisko MIME-sniffingu (gdzie przeglądarka zgaduje typ pliku zamiast ufać nagłówkowi `Content-Type`). Brak: Przeglądarka może zinterpretować plik `avatar.jpg` (zawierający złośliwy kod w metadanych EXIF) jako plik HTML/JS i go uruchomić.
   **`X-Frame-Options` (XFO):** Zapobiega renderowaniu strony w ramkach (`<iframe>`). Brak: Podatność na ataki Clickjacking (strona jest ładowana w niewidocznej ramce nad złośliwym przyciskiem). Obecnie funkcję tę przejmuje dyrektywa CSP `frame-ancestors`.
   **`Referrer-Policy`:** Kontroluje, jak dużo informacji o poprzednim adresie URL jest wysyłane w nagłówku `Referer`. Brak (lub złe ustawienie): Ryzyko wycieku wrażliwych danych (np. tokenów resetu hasła w URL) do zewnętrznych systemów analitycznych przy przechodzeniu w linki.

42. Czym jest atak **HTTP Request Smuggling**? Jak rozbieżności w parsowaniu `Content-Length` i `Transfer-Encoding` między proxy a backendem prowadzą do tej podatności?

   HTTP Request Smuggling to potężny atak na aplikacje używające łańcucha proxy-backend złączonych połączeniem keep-alive (wielokrotnego użytku TCP). Zjawisko to występuje, gdy serwer Proxy front-endowy i serwer Backendowy w różny sposób interpretują, gdzie dokładnie w strumieniu bajtów kończy się jedno żądanie HTTP, a zaczyna drugie.
   Atak bazuje na luce w specyfikacji HTTP/1.1 dotyczącej priorytetów użycia nagłówków długości body. Haker wysyła złośliwe żądanie zawierające **jednocześnie** oba te nagłówki: `Content-Length` i `Transfer-Encoding: chunked` (co często maskuje mutacjami, np. `Transfer-Encoding: xchunked`).
   Jeśli Proxy użyje `Content-Length` do wyznaczenia końca wiadomości, przekaże cały pakiet jako jedno żądanie na backend.
   Jeśli Backend zignoruje `Content-Length` (lub ze względu na błąd odrzuci niepoprawny nagłówek) i użyje parsowania po chunkach (`Transfer-Encoding`), uzna, że wiadomość skończyła się wcześniej w połowie body (przy chunku 0). Pozostała (złośliwa) reszta body zostaje "przemycona" i traktowana przez Backend jako zupełnie **nowe żądanie HTTP**, które leży w buforze gniazda TCP i czeka. Gdy po ułamku sekundy autentyczny, niewinny użytkownik przyśle swoje żądanie, serwer doklei je do końcówki złośliwego żądania hakera, wykonując w jego sesji niebezpieczne operacje (np. modyfikację haseł). Zjawisko to wymaga bezwzględnej sanitacji nagłówków na obrzeżach.

43. Czym jest atak **HTTP Response Splitting** i jak nagłówki z niekontrolowanym inputem użytkownika mogą go umożliwić?

   HTTP Response Splitting (podział odpowiedzi HTTP) to atak z grupy wstrzykiwania CRLF (Carriage Return Line Feed - `\r\n`). Następuje, gdy aplikacja bierze niezaufane, nieprzefiltrowane dane od użytkownika (np. z parametru URL) i umieszcza je bezpośrednio w nagłówku odpowiedzi HTTP (np. w `Location` przy przekierowaniu, lub `Set-Cookie`).

   Atakujący przesyła ciąg znaków zawierający sekwencje `\r\n\r\n`. Ponieważ sekwencja ta w protokole HTTP oznacza koniec nagłówków i początek ciała (body), pozwala to hakerowi przedwcześnie zamknąć oryginalną odpowiedź wygenerowaną przez serwer i wstrzyknąć całkowicie nową, spreparowaną odpowiedź HTTP (ze swoim własnym złośliwym ciałem HTML/JS), która zostanie odczytana przez przeglądarkę lub zatruta w pamięci podręcznej proxy (Cache Poisoning).

44. Jak działa flaga **`Secure`**, **`HttpOnly`** i **`SameSite`** w cookies? Jakie ataki mityguje każda z nich?

   Są to fundamentalne flagi bezpieczeństwa dla nagłówka `Set-Cookie`:
   **`Secure`**: Cookie zostanie wysłane przez przeglądarkę z powrotem do serwera tylko i wyłącznie po szyfrowanym połączeniu (HTTPS). Mityguje: kradzież sesji przy atakach **Man-in-the-Middle** na niezabezpieczonych sieciach (np. otwarte publiczne Wi-Fi).
   **`HttpOnly`**: Cookie jest ukryte przed interfejsem DOM i nie ma do niego dostępu poprzez JavaScript (`document.cookie` go nie pokaże). Mityguje: kradzież tokenów sesyjnych przy ataku **XSS** (skrypt atakującego nie jest w stanie go wyciągnąć).
   **`SameSite`**: (Wartości `Strict` lub `Lax`) Zabrania wysyłania ciasteczka wraz z żądaniami inicjowanymi z innej domeny. Mityguje: w 100% ataki **CSRF** (Cross-Site Request Forgery), ponieważ serwer nie otrzyma autoryzacji przy ataku "z zewnątrz".

45. Czym jest **HSTS Preload List** i jaki problem rozwiązuje w porównaniu ze zwykłym nagłówkiem `Strict-Transport-Security`?

   Zwykły nagłówek HSTS (`Strict-Transport-Security`) zmusza przeglądarkę do używania HTTPS, ale ma krytyczną lukę: problem "pierwszego żądania" (Trust on First Use). Zanim przeglądarka kiedykolwiek otrzyma ten nagłówek z bezpiecznego połącznia, przy pierwszym w historii wpisaniu w pasek adresu `example.com`, z reguły łączy się po HTTP, gdzie może paść ofiarą ataku ssl-stripping.

   **HSTS Preload List** to wbudowana w kod źródłowy każdej nowoczesnej przeglądarki (Chrome, Firefox, Safari) twarda lista domen, które zadeklarowały, że można na nie wejść tylko i wyłącznie po HTTPS. Administrator domeny musi zgłosić swój serwis do tej listy. Od momentu dodania, przeglądarka nawet przy pierwszym użyciu nigdy nie pozwoli na wysłanie pakietu w nieszyfrowanym protokole HTTP (port 80). Rozwiązuje to całkowicie wektor podatności pierwszego żądania.

46. Jak działa mechanizm **Subresource Integrity (SRI)** i dlaczego jest ważny przy ładowaniu zasobów z CDN-ów?

   SRI to funkcja bezpieczeństwa pozwalająca przeglądarkom upewnić się, że zewnętrzne zasoby statyczne (skrypty JS, style CSS) pobrane na stronę nie zostały nieoczekiwanie zmodyfikowane.
   Realizuje się to przez atrybut `integrity` w tagu `<script>` lub `<link>`, podając skrót kryptograficzny (np. SHA-384) zaufanej zawartości pliku:
   `<script src="https://cdn.example.com/lib.js" integrity="sha384-oqVuAfXR..."></script>`

   **Znaczenie (Zabezpieczenie przed przejęciem CDN):**
   Jeśli ładujemy biblioteki z publicznego, darmowego CDN-a (np. cdnjs), powierzamy bezpieczeństwo naszej strony podmiotowi trzeciemu. Gdyby ten CDN padł ofiarą ataku (lub jego infrastruktura została złośliwie zmodyfikowana) i w oryginalnym skrypcie biblioteki umieszczono by złośliwy keylogger lub koparkę kryptowalut, zaraziłoby to wszystkie ufające mu strony. Dzięki SRI przeglądarka po pobraniu zarażonego pliku z CDN przelicza hash. Ponieważ hash zmodyfikowanego pliku nie zgodzi się z tym wpisanym na sztywno w atrybucie `integrity`, przeglądarka natychmiast zablokuje wczytanie i wykonanie biblioteki.

---

## 7. HTTP/2 — multipleksowanie i wydajność

47. Jakie fundamentalne problemy HTTP/1.1 rozwiązuje HTTP/2? Opisz kluczowe różnice architektoniczne.

48. Czym jest **multipleksowanie strumieni** w HTTP/2 i jak eliminuje problem **head-of-line blocking** na warstwie aplikacyjnej?

49. Opisz mechanizm **HPACK** — kompresji nagłówków w HTTP/2. Dlaczego standardowa kompresja (np. gzip) nagłówków byłaby niebezpieczna (atak CRIME/BREACH)?

50. Czym jest **Server Push** w HTTP/2? Dlaczego w praktyce okazał się problematyczny i został usunięty z niektórych implementacji?
51. Jak działa **flow control** (kontrola przepływu) w HTTP/2? Na jakich poziomach jest realizowana (połączenie vs strumień)?
52. Czym jest **priorytetyzacja strumieni** w HTTP/2 i jak przeglądarki wykorzystują ją do optymalizacji ładowania zasobów?
53. Dlaczego HTTP/2 nadal ma problem **head-of-line blocking na warstwie TCP**? Jak to wpływa na wydajność przy stratach pakietów?
54. Jak wygląda **upgrade z HTTP/1.1 do HTTP/2** — czym jest ALPN i dlaczego HTTP/2 w praktyce wymaga TLS?

---

## 8. HTTP/3 i QUIC

55. Czym jest **HTTP/3** i dlaczego zastępuje TCP na rzecz **QUIC** (opartego na UDP)? Jaki fundamentalny problem rozwiązuje?
56. Jak QUIC eliminuje problem **head-of-line blocking na warstwie transportowej**, który występował w HTTP/2 nad TCP?
57. Czym jest **0-RTT connection establishment** w QUIC i jakie ryzyka bezpieczeństwa wiążą się z early data (analogicznie do TLS 1.3 0-RTT)?
58. Jak działa **connection migration** w QUIC? Dlaczego zmiana sieci (np. WiFi → LTE) nie wymaga nowego handshake?
59. Czym jest **QPACK** — kompresja nagłówków w HTTP/3 — i czym różni się od HPACK w HTTP/2?
60. Jakie wyzwania operacyjne wiążą się z wdrożeniem HTTP/3 (firewalle blokujące UDP, brak widoczności w narzędziach sieciowych, debugowanie)?
61. Jak serwer ogłasza wsparcie dla HTTP/3 — czym jest nagłówek **`Alt-Svc`** i jak przeglądarka przechodzi z HTTP/2 na HTTP/3?

---

## 9. Cookies, sesje i zarządzanie stanem

62. Opisz pełny cykl życia **cookie** — od ustawienia przez serwer (`Set-Cookie`) do wysłania przez klienta. Jakie atrybuty kontrolują zasięg, czas życia i bezpieczeństwo cookie?

   Cykl życia:
   1. **Ustawienie:** Serwer w odpowiedzi na żądanie wysyła nagłówek `Set-Cookie: session_id=12345; Secure; HttpOnly`.
   2. **Składowanie:** Przeglądarka odbiera nagłówek, waliduje atrybuty (np. czy zgadza się domena) i zapisuje w wewnętrznej bazie pamięci podręcznej przypisanej do domeny.
   3. **Wysyłanie:** Przy każdym kolejnym żądaniu pasującym do zakresu domeny i ścieżki, przeglądarka automatycznie dorzuca to ciasteczko: `Cookie: session_id=12345`.
   4. **Wygasanie/Usunięcie:** Przeglądarka usuwa cookie, gdy minie czas `Expires` / `Max-Age` lub gdy użytkownik zamknie sesję/wyczyści dane. Serwer może wymusić usunięcie wysyłając `Set-Cookie` z tą samą nazwą i datą wygaśnięcia z przeszłości (np. `Expires=Thu, 01 Jan 1970 00:00:00 GMT`).

   **Kluczowe atrybuty:**
   **Zasięg:** `Domain` (dla jakich domen podrzędnych ważne), `Path` (do jakiego prefiksu ścieżki ograniczyć wysyłanie).
   **Czas życia:** `Expires` (sztywna data wygaśnięcia), `Max-Age` (liczba sekund od teraz).
   **Bezpieczeństwo:** `Secure` (tylko przez HTTPS), `HttpOnly` (zakaz odczytu w JS), `SameSite` (ochrona CSRF).

63. Czym różni się **session cookie** od **persistent cookie**? Jak przeglądarki traktują cookies bez atrybutu `Expires`/`Max-Age`?

   Różnica polega wyłącznie na braku lub obecności atrybutów czasu życia, co dyktuje moment ich destrukcji.
   **Session Cookie (Ciasteczko sesyjne):** To ciastko, które na etapie `Set-Cookie` nie otrzymało ani atrybutu `Expires`, ani `Max-Age`. Przeglądarka traktuje je jako ulotne. Zostanie zniszczone w momencie zamknięcia "sesji przeglądania", czyli całkowitego wyłączenia przeglądarki. (Uwaga: Nowoczesne przeglądarki posiadające funkcję "przywracania zamkniętych kart" potrafią niefortunnie utrzymywać ciastka sesyjne przy życiu nawet po restarcie).
   **Persistent Cookie (Ciasteczko trwałe):** Otrzymało konkretną datę `Expires` lub czas `Max-Age`. Przeglądarka zapisuje je trwale na dysku i nie usunie ich zamknięciem programu. Wyśle je natychmiast przy kolejnym włączeniu komputera i wizycie na stronie wciąż używając tego samego tokena, o ile nie upłynął jego zakodowany na twardo limit daty ważności.

64. Jaki jest limit rozmiaru cookies i liczby cookies na domenę? Jakie ma to konsekwencje dla architektury aplikacji?

   Standardy RFC i powszechna implementacja przeglądarek wprowadzają ścisłe restrykcje:
   **Rozmiar:** Maksymalny rozmiar pojedynczego ciasteczka (nazwa + wartość + atrybuty) to zwykle około **4 KB (4096 bajtów)**.
   **Liczba:** Przeglądarki ograniczają liczbę ciastek dla jednej domeny zwykle do około **50-180**. Próba ustawienia nowszego nadmiarowego ciasteczka najczęściej wyprze najstarsze (Algorytm LRU).

   **Konsekwencje architektoniczne:**
   Nie można traktować mechanizmu Cookies jako pełnoprawnego zamiennika bazy danych po stronie klienta. Tokeny zawierające zbyt dużo zaszyfrowanych informacji (np. monstrualne "fat JWT" z dużą ilością ról i atrybutów uprawnień użytkownika) mogą przerosnąć limit 4KB, co skończy się odcięciem ciastka w połowie bez zwrócenia wyrazistego błędu w HTTP. W aplikacjach SPA lepiej umieszczać mniejsze referencje sesyjne (np. Session ID) i pobierać większe obiekty po stronie backendu, lub korzystać po stronie klienta z pojemnych mechanizmów `localStorage` czy `IndexedDB` zamiast rozpychania ciastek (które są wysyłane fizycznie do backendu z każdym zapytaniem tworząc wielki, ciężki nagłówek HTTP, zapychając sieć).

65. Jak atrybut **`SameSite`** (Strict, Lax, None) zmienia zachowanie cookies w kontekście cross-site requests? Jakie ma to implikacje dla integracji z third-party systemami?

   `SameSite` zarządza polityką przeglądarki decydującą, czy dołączyć ciasteczko do żądań wychodzących "na zewnątrz" z innej witryny (np. z `a.com` do `b.com`).
   **`Strict`:** Przeglądarka dołączy ciasteczko TYLKO, gdy żądanie pochodzi z tej samej domeny, na której je wystawiono (z `b.com` na `b.com`). Wyklucza to nawet kliknięcie linku na zewnątrz.
   **`Lax` (Domyślne od 2020r.):** Przeglądarka nie dołączy ciastka do żądań pobocznych modyfikujących (jak złośliwe formularze POST, ataki CSRF, żądania z JavaScriptu XHR/Fetch API z innej domeny). Jednak litościwie dołączy ciastko dla bezpiecznych nawigacji na poziomie najwyższym (tzw. top-level navigation, np. gdy ktoś kliknie `<a href>` do Twojej strony lub użyje GET), aby użytkownik zachował status zalogowania wchodząc z zewnątrz.
   **`None`:** Wyłącza blokadę — ciasteczko wysyłane jest ze wszystkimi (nawet POST/XHR) żądaniami cross-site. **Wymaga obowiązkowo atrybutu `Secure`**.

   **Implikacje (Third-party integrations):** Systemy takie jak osadzone i-frame'y z bramkami płatności, systemy Single Sign-On (SSO) czy widżety analityczne na zewnętrznych stronach przestaną działać (zgubią sesje/tokeny), jeśli ich twórcy nie ustawią jawnie `SameSite=None; Secure`. Utrudnia to bardzo śledzenie użytkowników po sieci (third-party tracking cookies).

66. Czym jest **cookie partitioning** (CHIPS — Cookies Having Independent Partitioned State) i jaki problem prywatności rozwiązuje?

   CHIPS to odpowiedź na ostateczną i całkowitą śmierć śledzących plików "third-party cookies".
   Tradycyjnie, gdy widżet reklamowy `tracker.com` ustawiał z poziomu domeny `sklep.com` cookie `id=123` (z `SameSite=None`), widział to samo cookie wędrując z użytkownikiem po innej stronie, np. `wiadomosci.com`, co umożliwiało śledzenie użytkownika w sieci.

   **Partitioning (Partyjonowanie):** CHIPS (dzięki dodaniu atrybutu `Partitioned` do nagłówka `Set-Cookie`) tworzy nową strukturę izolacji ciastek. Zamiast dzielić słoik z ciasteczkami tylko po nazwie domeny hostującej (`tracker.com`), dzieli go również po **domenie z najwyższego poziomu (top-level site)**, na której użytkownik się obecnie znajduje.
   Oznacza to, że widżet `tracker.com` osadzony na stronie A otrzyma zupełnie osobne środowisko ciasteczek, niewidoczne, kiedy użytkownik znajdzie się na stronie B. Pozwala to na poprawne funkcjonowanie widżetów stron trzecich (które potrzebują np. zapisać sesję własnego wewnętrznego panelu), eliminując bezpowrotnie możliwość wykorzystania ich do globalnego śledzenia (cross-site tracking).

67. Czym jest mechanizm **cookie prefixes** (`__Secure-`, `__Host-`) i jakie dodatkowe gwarancje bezpieczeństwa zapewniają?

   Dawniej serwer z domeny głównej (`example.com`) nie mógł bezpiecznie zweryfikować, skąd pochodzi odebrane cookie (które atrybuty i flagi pierwotnie posiadało na etapie tworzenia, bo przysłano tylko parę nazwa=wartość). Słabo napisana, zainfekowana XSS-em subdomena (np. `stary-blog.example.com`) mogła celowo nadpisać ciasteczko z domeny głównej w pamięci przeglądarki własną, pozbawioną zabezpieczeń, sfałszowaną wersją tego ciasteczka na ułamek sekundy na niebezpiecznym połączeniu HTTP.

   Z tego powodu standard wprowadził **Magiczne Prefiksy**:
   `__Secure-nazwa_ciastka`: Wymusza absolutnie, że ciastko zostanie zaakceptowane przez przeglądarkę z żądania HTTP jedynie jeśli odpowiedź `Set-Cookie` przyszła po bezpiecznym połączeniu z nałożonym atrybutem `Secure`.
   `__Host-nazwa_ciastka`: Dodaje potężny rygor w postaci blokady przed jakimikolwiek modyfikacjami na zewnątrz z subdomen lub ścieżek. Wymusza nie tylko flagę `Secure`, ale żąda, by ciasteczko zawsze miało domyślną ścieżkę (`Path=/`) i *nie* miało atrybutu `Domain`. Gwarantuje to, że ciasteczko mogło pochodzić wyłącznie z uderzenia do głównej ściśle powiązanej domeny i nie zostało podmienione, wstrzyknięte z zewnątrz ani ograniczone.

---

## 10. Wydajność i optymalizacja

68. Jak zaprojektować strategię **kompresji** odpowiedzi HTTP? Porównaj **gzip**, **Brotli** i **zstd** pod kątem współczynnika kompresji, szybkości i wsparcia.

   Wymuszenie kompresji tekstowych payloadów (JSON, HTML, JS) to absolutna podstawa optymalizacji. Strategia polega na negocjacji w locie (nagłówek `Accept-Encoding`).
   **Gzip:** Złoty standard, wspierany absolutnie wszędzie od dekad. Oferuje przyzwoity współczynnik kompresji i szybkość, idealny jako fallback.
   **Brotli (`br`):** Algorytm od Google dedykowany dla sieci Web. Znacznie lepszy współczynnik kompresji niż Gzip (o ok. 20%) dla plików tekstowych. Jest jednak wolniejszy przy najwyższych poziomach kompresji "w locie". Strategia: używać Brotli na średnim poziomie (np. 4) dla dynamicznego API, a najwyższy poziom (11) zarezerwować do wcześniejszej, statycznej pre-kompresji plików na dysku (podczas fazy build). Wymaga poświadczenia HTTPS.
   **Zstandard (`zstd`):** Najnowszy algorytm od Facebooka, rewolucjonizujący kompresję z powodu wybitnej szybkości i genialnego współczynnika kompresji deklasującego Brotli i Gzip w zastosowaniach strumieniowych. Wsparcie w przeglądarkach rośnie (Chrome wspiera zstd od wersji 123 z marca 2024r.). To przyszły faworyt w kodowaniu szybkiego JSON API.

69. Czym jest **HTTP Range Requests** i jak wspiera pobieranie plików z możliwością wznowienia (resumable downloads)?

   Range Requests (żądania zakresowe) to mechanizm pobierania pliku "w kawałkach". Jest niezbędny dla odtwarzaczy wideo przeskakujących po osi czasu oraz pauzowanych menedżerów pobierania.
   **Działanie:**
   Serwer ogłasza w pierwszej odpowiedzi nagłówek `Accept-Ranges: bytes`. Gdy klient ułamie połączenie i zechce wznowić pobieranie pobranej do połowy instalki 10GB, wysyła żądanie z nagłówkiem `Range: bytes=5000000000-` (czyli "daj mi resztę pliku zaczynając od 5-go gigabajta").
   Serwer odpowiada statusem **`206 Partial Content`**, odsyłając wyłącznie żądany wycinek bajtów. Do poprawnego działania przy wznawianiu po długim czasie klient dołącza walidator `If-Range: <ETag>`, by upewnić się, że plik na serwerze nie został w międzyczasie zaktualizowany (bo wtedy sklejanie starej połowy z nową zepsułoby cały plik).

70. Jak działa **Connection Coalescing** w HTTP/2 i HTTP/3? W jakich warunkach przeglądarka może współdzielić połączenie dla różnych domen?

   Connection Coalescing (łączenie połączeń) to zjawisko, gdzie przeglądarka optymalizuje zasoby drastycznie i nie otwiera nowego gniazda TCP/TLS dla nowo napotkanej domeny. Zamiast tego "podpina się" pod wcześniej otwarte już połączenie fizyczne z inną, starszą domeną.
   **Warunki łączenia:**
   Przeglądarka może użyć tego samego, trwającego połączenia (np. otwartego wcześniej do pobrania zasobów na `api.example.com`) dla nowo wymaganego strzału do `images.example.com`, jeżeli oba te warunki są rygorystycznie spełnione:
   1. Nazwy obu tych domen posiadają ten sam rekord adresowy (DNS resolveuje obie domeny do identycznego adresu IP).
   2. Otwarty uprzednio tunel TLS posiada certyfikat uwierzytelniający autentyczność wystawiony na tzw. "wildcard", który legalnie i kryptograficznie pokrywa nazwę nowej domeny (`*.example.com` pokrywa zarówno api jak i images) lub certyfikat ma zaszyty Subject Alternative Name (SAN) wymieniający te domeny na liście rzędem.

71. Czym jest technika **domain sharding** z czasów HTTP/1.1? Dlaczego w erze HTTP/2 jest antypattern?

   Domain sharding było sztuczką architektoniczną pozwalającą obejść drastyczne limity wbudowane w przeglądarki na żądania współbieżne.
   W HTTP/1.1 przeglądarki limitowały maksymalną ilość połączonych otwartych gniazd TCP na jedną domenę do ~6. Jeśli strona miała 50 obrazków, ładowały się one zatorami partiami po 6. By obejść limit 6 żądań dla `cdn.site.com`, inżynierowie kopiowali to samo na wiele subdomen: `cdn1.site.com`, `cdn2.site.com`, wymuszając na przeglądarce otwarcie 24 połączeń TCP (rozbicie szklanego sufitu).

   **W erze HTTP/2 jest to antypattern (błąd w sztuce):**
   HTTP/2 używa protokołu binarnego i *multipleksuje* setki zapytań asynchronicznie przez to samo, zaledwie jedno fizyczne połączenie (brak restrykcji rzędu 6). Jeśli frontend jest "shardowany" z czasów HTTP/1.1 po HTTP/2, zmusza to przeglądarkę na siłę do negocjowania potrójnych rozwiązań DNS, potrójnego wolnego uścisku TCP (3-way) i trzech negocjacji wolnych kluczy TLS dla każdej ze sztucznych subdomen, ograbiając system z całej idei HTTP/2. Rozwiązaniem jest wrzucenie wszystkiego z powrotem na jedną domenę bazową.

72. Jak **Early Hints (103)** pozwalają serwerowi zasugerować przeglądarce zasoby do preloadu jeszcze przed wysłaniem właściwej odpowiedzi?

   Kod `103 Early Hints` to mechanizm ratujący wydajność przy "ciężkich" żądaniach.
   Zanim serwer bazy danych wygeneruje pełen HTML dla skomplikowanego kokpitu u użytkownika (co zajmuje np. 800ms), serwer WWW (Reverse Proxy lub sam App Server) może już po 50ms wysłać do przeglądarki klienta *wstępną, informacyjną odpowiedź* HTTP z kodem `103`, zawierającą wyłącznie nagłówki `Link: </style.css>; rel=preload`.
   Przeglądarka, otrzymując status 103, wie, że główne żądanie wciąż się przetwarza (nie zrywa połączenia), ale już w międzyczasie asynchronicznie rozpoczyna pobieranie plików `style.css` z CDN. Gdy po 800ms przyjdzie w końcu nagle gotowy kod HTML (`200 OK`), przeglądarka ma już w buforze pobrany i gotowy arkusz stylów, natychmiast renderując stronę. Eliminuje to bezczynność sieci podczas oczekiwania na generowanie dokumentu.

73. Czym są nagłówki **`Link: rel=preload`** i **`Link: rel=preconnect`**? Jak wpływają na Critical Rendering Path?

   Nagłówki te sterują priorytetowym zachowaniem przeglądarki przed przetworzeniem całego DOM, przyspieszając tzw. Krytyczną Ścieżkę Renderowania (Critical Rendering Path).
   **`rel=preload`**: Mówi: "Ten konkretny zasób (np. główny font `.woff2` lub logo) będzie absolutnie i bezwarunkowo potrzebny za chwilę na tej stronie. Pobierz go z najwyższym priorytetem od razu, zanim w ogóle dojdziesz do tagu, który go wymusza". Chroni przed zjawiskiem FOUT (migających fontów) i opóźnieniami renderowania.
   **`rel=preconnect`**: Mówi: "Nie wiem jeszcze, o jakie konkretnie pliki poproszę, ale gwarantuję ci, że na 100% będę za ułamek sekundy musiał wykonać żądanie do zewnętrznej domeny `https://api.example.com`". Przeglądarka widząc to, zawczasu otwiera procesy i rezerwuje czas na wykonanie żmudnego TCP Handshake oraz TLS Negocjacji z tym obcym serwerem, oszczędzając ok 150-300ms w momencie, w którym faktyczny skrypt wywoła na tę domenę operację `fetch()`.

74. Jak zaprojektować optymalną strategię **timeoutów** w łańcuchu reverse proxy → API gateway → mikroserwisy? Jakie problemy powodują źle dobrane timeouty?

   Złotą i najważniejszą zasadą rozproszonych architektur jest to, że **timeouty muszą bezwzględnie maleć w miarę zanurzania się głębiej w głąb kaskady architektury** (licząc od klienta na zewnątrz).
   **Przykład strategii:**
   **LB / Reverse Proxy:** 30 sekund
   **API Gateway:** 25 sekund
   **Mikroserwis A (agregujący):** 20 sekund
   **Mikroserwis B (baza / worker):** 15 sekund
   **Klient HTTP w MS B (np. zapytanie do bazy db):** 10 sekund

   **Skutki złego doboru:**
   Jeśli zewnętrzny Gateway ma timeout 5s, a wewnętrzny Mikroserwis 10s (odwrócona kaskada), to przy opóźnieniu bazy rzędu 8s, zewnętrzny Gateway zrzuci u klienta połączenie statusem `504 Gateway Timeout` (po upływie 5s), ucinając logikę. Poważnym problemem jest jednak to, że głęboki Mikroserwis **nie został wcale przerwany** — wciąż wykonuje niepotrzebnie i do końca to kosztowne, sieroce obliczenie przez pozostałe 3 sekundy. Przy masowym ruchu zapycha to zupełnie pule połączeń bazy danych tzw. "żądaniami-widmo", po czym cały system zapada się (cascading failure), a klienci i tak widzą same błędy 504. Dodatkowo bezwarunkowo należy zaimplementować mechanizm przekazywania propagacji przerwań do głębszych warstw (np. używając kontekstów gRPC lub sprawdzając w HTTP czy gniazdo TCP nie zostało przedwcześnie zamknięte przez klienta przed wysłaniem odpowiedzi).

---

## 11. WebSocket, SSE i komunikacja w czasie rzeczywistym

75. Czym jest **WebSocket** i jak wygląda **HTTP Upgrade handshake** do protokołu WebSocket? Jaki jest związek WebSocketa z HTTP?

   **WebSocket** to protokół komunikacyjny zapewniający ciągłe, dwukierunkowe (full-duplex) przesyłanie strumieniowe nad jednym gniazdem TCP, używane przy bardzo niskich opóźnieniach.
   **Handshake:** Klient inicjuje komunikację standardowym żądaniem HTTP z nagłówkami negocjacyjnymi `Upgrade: websocket` i `Connection: Upgrade`, wymieniając także kryptograficzny klucz `Sec-WebSocket-Key`. Związek z HTTP kończy się jednak zaraz po potwierdzeniu przez serwer wymiany statusem `101 Switching Protocols`. Od tego momentu połączenie wychodzi całkowicie poza warstwę HTTP, zostaje otwarte, a strony zaczynają swobodnie wymieniać niezależne, binarne lub tekstowe ramki z minimalnym narzutem — znikają całkowicie klasyczne nagłówki żądania i odpowiedzi.

76. Czym są **Server-Sent Events (SSE)** i czym różnią się od WebSocketów? Kiedy SSE jest lepszym wyborem?

   **SSE** to jednokierunkowy strumień powiadomień HTTP (server-to-client). Wykorzystuje długotrwale utrzymane połączenie HTTP, wysyłając jako typ zawartości `Content-Type: text/event-stream`.
   **Różnice:** SSE to czyste HTTP wspierane w przeglądarce za pomocą Web API EventSource; jest w pełni tekstowe i może przepływać przez proxy lub firewalle wspierające tylko czyste protokoły aplikacji (w przeciwieństwie do binarnego formatu WebSocketów, które zmieniają protokół).
   **Lepszy wybór:** SSE jest preferowane, gdy architektura wymaga wysyłania powiadomień stricte jednostronnych (od serwera do klienta, np. tablica notowań giełdowych lub logi deploymentu na żywo), bez wymogu wkładu klienta w dwustronną komunikację. SSE ma wbudowany mechanizm automatycznego wznawiania połączeń i obsługę wznawiania po identyfikatorach zdarzeń (Last-Event-ID), co przy WebSocketach trzeba by implementować w aplikacji od zera.

77. Jak **HTTP/2 Server Push** i **SSE nad HTTP/2** zmieniają podejście do komunikacji push w porównaniu z klasycznym long polling?

   Zarówno Server Push jak i SSE niwelują wymuszanie ogromnego zużycia wątków aplikacyjnych i TCP znanych w klasycznym Long Pollingu.
   **HTTP/2 Server Push:** Miało służyć wpychaniu do klienta powiązanych zasobów statycznych (takich jak skrypty CSS, by uniknąć drugiego RTT dla pobrania ich przez przeglądarkę). Mechanizm jest jednak wycofywany (usunięto go np. z Chrome) ze względu na skomplikowaną integrację z pamięcią cache i brak zauważalnych zysków wydajnościowych. Nigdy nie było to API dla notyfikacji biznesowych z serwera.
   **SSE nad HTTP/2:** Multipleksowanie H2 to game-changer dla SSE. W HTTP/1.1 przeglądarki limitowały żądania do maksymalnie np. 6 strumieni trzymanych połączeń TCP do jednej domeny, przez co odpalenie 6 połączeń SSE całkowicie odcinało inne żądania i ładowanie grafik. Dzięki połączeniom w HTTP/2, ogrom otwartych kanałów EventSource wędruje kompletnie niezależnie jako lekkie strumienie wewnątrz jednej fizycznej rury TLS, nie zatykając kolejek sieciowych.

78. Czym jest **long polling** i jakie problemy wydajnościowe i skalowalności generuje w porównaniu z WebSocketami i SSE?

   **Long polling** to przestarzała symulacja zdarzeń w czasie rzeczywistym. Klient uderza do serwera po dane, lecz serwer (zamiast zwrócić pustą odpowiedź jeśli brak zmian) celowo zamraża wykonanie żądania HTTP, czekając dopóki nie otrzyma nowego zdarzenia z tła. Gdy takowe nadejdzie, zamyka proces odsyłając odpowiedź. Klient po jej odebraniu z miejsca odpala natychmiastowe kolejne uśpione zapytanie.
   **Problemy w skalowalności:** Architektura żąda otwierania w kółko pełnych połączeń TCP (narzut 3-way handshake) dla każdej notyfikacji oraz przetworzenia nagłówków. Czekające requesty konsumują pulę wątków serwera (każde uśpione żądanie to potencjalnie jeden zablokowany worker). Wymusza to marnotrawstwo deskryptorów plików i RAMu dla setek tysięcy bezczynnych klientów, podczas gdy WebSockety/SSE wykorzystują w pełni zoptymalizowane asynchroniczne i oszczędne połączenia na event-loopach utrzymując ciągły kontakt.

79. Jak load balancery i reverse proxy obsługują **połączenia WebSocket** — jakie specjalne konfiguracje są wymagane?

   Typowe serwery (jak Nginx czy HAProxy) z definicji przyjmują, że połączenie HTTP powinno żyć krótko, a przesył po paru sekundach uśpienia oznacza martwego i rozłączonego klienta, co skutkuje ich brutalnym ucinaniem przez reverse proxy (np. błąd `504 Gateway Timeout`).
   **Specjalne wymogi konfiguracji:**
   Jawne zezwolenie na protokół przesyłu w standardzie Upgrade – ustawienie przechodzenia w nagłówkach wartości `Upgrade` i `Connection` od klienta (które inaczej serwer sam w locie usunie próbując wymusić tradycyjne HTTP/1.1).
   Zwiększenie opóźnień (Timeoutów) – drastyczne wydłużenie czasu limitu na odczyty z sieci dla trwającej paczki (np. `proxy_read_timeout` na 1 godzinę), aby uciszone i nieaktywne WebSockety mogły stać otwarte w oczekiwaniu na powiadomienia.
   Ponieważ protokół na żywo działa trwale łącząc i przypinając klienta i jeden docelowy węzeł w parę procesów, Load Balancer dla WebSocketów nie działa jak typowy round-robin na pojedyncze zapytania – nie przerzuca requestów między instancjami w trwającym uścisku tunelu WS po negocjacji i upgrade'owaniu pakietów.

---

## 12. Proxy, load balancing i architektura HTTP

80. Czym różni się **forward proxy** od **reverse proxy**? Jakie zastosowania ma każdy z nich?

   **Forward proxy (Proxy klienta):** Serwer stojący pomiędzy siecią lokalną (np. w firmie) a Internetem. Jego głównym celem jest obsługa zapytań pochodzących od *chronionych klientów* do świata zewnętrznego. Zastosowanie: filtrowanie ruchu (blokowanie stron), anonimizacja (ukrywanie IP klienta), cachowanie plików ściąganych do sieci wewnętrznej czy monitorowanie ruchu pracowników. Klient zazwyczaj wie o jego istnieniu i musi być na niego skonfigurowany.
   **Reverse proxy (Proxy serwera):** Serwer stojący przed serwerami docelowymi aplikacji jako jedyny punkt dostępowy z Internetu. Jego celem jest ochrona serwerów i routing. Zastosowanie: Load balancing (rozdzielanie ruchu), SSL/TLS Termination (kończenie szyfrowania), WAF (zapora aplikacji sieciowych) czy caching odpowiedzi. Klient w Internecie (przeglądarka) myśli, że rozmawia bezpośrednio ze wspaniałym serwerem docelowym.

81. Jak działa **HTTP load balancing** na warstwie 7? Czym różni się od load balancingu na warstwie 4 (TCP)?

   **Warstwa 4 (L4 - TCP/UDP):** Load balancer działa jako błyskawiczny router. Bazuje jedynie na informacjach z poziomu pakietu: docelowy adres IP oraz Port. Nie widzi zawartości (URL, ciasteczek, zaszyfrowanych payloadów). Rozdziela w ślepo połączenia na serwery aplikacyjne używając np. algorytmu Round Robin. Niesamowicie wydajny z bardzo małym narzutem (np. AWS NLB, HAProxy).
   **Warstwa 7 (L7 - HTTP):** Aplikacyjny load balancer deszyfruje TLS (jeśli włączony) i w pełni parsje żądanie HTTP. Ponieważ zyskuje "świadomość aplikacji", może podejmować niezwykle wyrafinowane decyzje biznesowe — routować dany URL po ścieżce (np. endpoint `/api/videos` skierować na potężniejsze instancje, a `/auth` do strefy uwierzytelniającej), odczytywać i sterować ciastkami, blokować wybrane User-Agenty. Narzut procesora jest dużo większy, bo rozrywa i tłumaczy pakiety (jedno TCP od klienta do proxy, drugie od proxy do serwera).

82. Czym jest **sticky session** (session affinity) na load balancerze i jakie ma konsekwencje dla skalowalności?

   **Sticky Session (przypinanie sesji)** to mechanizm L7 gwarantujący użytkownikowi (często zidentyfikowanemu poprzez wstrzyknięty mu w odpowiedzi ciasteczkowy identyfikator od load balancera), że absolutnie wszystkie jego kolejne żądania z jednej sesji zawsze trafią na ten sam konkretny i fizyczny serwer węzła w grupie klastrowej, użyty przy pierwszym dostępie. 
   **Konsekwencje dla skalowalności:**
   Mocno utrudnia i podważa koncepcję poziomej chmury "horizontal scaling" i bezstanowości (Stateless) u mikrousług. Przy przypięciu nie ma szans na idealnie obciążone, równomiernie rosnące maszyny: węzeł do którego przypięto wyjątkowo aktywnych/kosztownych klientów zostanie przeciążony (powstanie tzw. "Hot Spot"), podczas gdy inne stoją w bezczynności i cichną. Uniemożliwia to także agresywne auto-skalowanie i bezpieczne wdrożenia z wyłączaniem procesów na produkcji (bo ucięty węzeł z pamięcią gubi stany przypiętych dla niego nagle ludzi przerywając zalogowania). Zawsze lepiej przenosić i scentralizować stan logowania do bazy w pamięci in-memory dla całej floty aplikacji (jak np. w ustandaryzowanym użyciu Redis), co umożliwia klasyczne odrzucenie ciastka affinity przez proxy na losowo działającą rotację.

83. Jak reverse proxy obsługuje **HTTP/2 downstream** a **HTTP/1.1 upstream** do backendu? Jakie kompromisy to wprowadza?

   Reverse proxy (jak Nginx na granicy klastra) w standardzie nawiązuje dla frontowego użytkownika i świata wejście przez HTTPS zaawansowanym i superszybkim multipleksowanym protokołem HTTP/2. Następnie Nginx przyjmując pakiety i setki binarnego strumienia de-multipleksuje je (rozkleja), tworząc serię osobnych, klasycznych zapytania HTTP/1.1 i wystrzeliwuje te dekodowane potoki do wewnętrznych serwerów bazy (np. w Springu lub Node.js) działających po lokalnej zamkniętej sieci z czystym starym HTTP (tzw. architekturą up-stream na LANie z zerowymi opóźnieniami RTT).
   **Kompromisy:** Odcina i ułatwia starszym serwerom monolitycznym pracę na starych gniazdach bez ich przebudowy by przyjmować binarki gRPC, a sam daje w świat klientom zyski przyspieszeń HTTP/2. Stracone są za to atuty użycia oszczędności nagłówków z HPACK z tyłu pod narzut CPU na dekompresję dwukrotną i obciąża znacząco użycie limitowanych dostępnych portów lokalnych pod połączenia TCP z tyłu za proxy. 

84. Czym jest **request buffering** i **response buffering** na reverse proxy? Kiedy wyłączenie bufferingu jest konieczne (np. SSE, streaming)?

   **Buffering:** Mechanizm ochronny odwrotnego proxy. Chroni serwery aplikacyjne przed klientami działającymi powolnie lub celowymi atakami złośliwego obniżania przepustowości pod zawieszenie procesu (jak atak Slowloris). Zamiast połączyć klienta z serwerem i zająć jego cenny i ograniczony wątek (Thread) w backendzie na 5 minut podczas wrzucania pliku kilobajt po kilobajcie przez 3G na telefonie, Nginx bierze to na własny bufor na małych obciążeniach na gnieździe, i na koniec sekundy potężnym kablem na lokalnej szynie i z całą prędkością przesyła ostateczny gotowy plik uwalniając proces logiki z serwera po paruset milisekundach. To samo tyczy się odpowiedzi: pobiera z backendu megabajty od razu (by backend wrócił do pracy w puli), i wysyła te fragmenty z użyciem własnej pamięci w tempie klienta komórkowego.
   **Kiedy wyłączyć (`proxy_buffering off`):** Buforowanie zniszczy zupełnie asynchroniczne i otwarte aplikacje i kanały strumieniowe. Przy działaniu Server-Sent Events czy chunked Streamowaniu binarnego video z zapisu kamer na żywo proxy będzie nieustannie powstrzymywać ramki i czekać w pamięci, by wysłać je dopiero "jak odpowiedź osiągnie całkowity rozmiar zamknięcia HTTP", więc paczki z zablokowanego złącza nigdy nie wylecą od serwera pod okno UI u użytkownika rzucając time-outem, zamiast lecieć ciągiem i wywoływać animację od początku i w czasie live.

85. Jak działa mechanizm **graceful shutdown** serwera HTTP — czym jest nagłówek `Connection: close` i jak load balancer obsługuje **draining**?

   **Graceful shutdown (Łagodne zamykanie)** chroni przed twardym zerwaniem połączeń z błędami w czasie zrzutu aplikacji do aktualizacji nowej paczki (Zero-Downtime Deployment). 
   1. System dostaje polecenie do zamykania węzła w API (sygnał SIGTERM do procesu). 
   2. Aplikacja lub wewnętrzny Web Server, zamiast umrzeć nagle w zrzucie ramu w środku bazy psując plik, oznacza węzeł na czerwono jako niedziałający i wstrzymuje natychmiastowe ubijanie samego siebie (dając w bufor np 30 sekund czekania). W tym samym czasie przestaje rygorystycznie i całkowicie nasłuchiwać od klientów zewnętrznych wejść na głównym porcie socketu TCP i powiadamia natychmiast load balancer.
   3. Load balancer przechodzi w stan tzw. **Connection Draining (odprowadzanie)** – zdejmuje wejście z routing-listy serwerów (round-robin) dla ruchu do nowo-utworzonych, a pod starym powieszonym wstrzymuje ubijanie dla asynchronicznie docierających opóźnionych zwrotek z baz by ratować akcje dla zalogowanych, chroniąc przed sypaniem klientów pod kodem `502/503`.
   4. Węzeł aplikacyjny wszystkim obsługiwanym w tle z przedawnionych żądań z pulą klientów w trwających uściskach odpisuje wywołane dane w rezultacie z bazy, ale dodając twardy nagłówek `Connection: close`. Gdy go otrzymają – zakończą sesję, a LoadBalancer dla tego użytkownika rzuci nowe uderzenia rotacyjnie z nowo podniesionych instancji paczki w chmurze obok zaktualizowanego kodu z bazy. Zamknięty i stary serwer po wygaszaniu powolnym reszty uciśnień pada gładko bez siania paniki, a wdrożenie powiodło się pomyślnie.

---

## 13. API Design i REST w kontekście HTTP

86. Czym jest **HATEOAS** (Hypermedia as the Engine of Application State) i dlaczego jest rzadko implementowany mimo bycia kluczowym ograniczeniem REST?

   **HATEOAS** to najwyższy z wymogów w ścisłym i "ortodoksyjnym" REST wg. Modelu Dojrzałości Richardsona (Poziom 3). Oznacza on, że odpowiedź zwracana przez API zawiera dodatkowo nawigacyjne łącza hipermediowe. Dzięki nim odpowiedź od API uczy i instruuje klienta z miejsca jak nawigować się po maszynie stanu i strukturze bez posiadania własnego schematu przed nosem. Przykład: żądanie danych konta `/accounts/123` oprócz salda zwraca zagnieżdżoną listę w formacie `"_links": { "deposit": { "href": "/accounts/123/deposit" } }`.
   **Dlaczego rzadki:** HATEOAS okazał się zbyt skomplikowany, bo dramatycznie powiększał payloady w sieci (przesyłając masę zbędnych linków), narzucał skomplikowane do tworzenia maszyny widoków, a przede wszystkim – współcześni klienci tacy jak aplikacje SPA (React/Angular) czy frontendy w Mobile z natury muszą mieć po stronie aplikacji zaszyte "na twardo" i zakodowane ekrany zachowań dla endpointów (by kompilować logikę UI i buttonów z dokumentacji do API po Swagger/OpenAPI) z wyprzedzeniem i na wczesnym etapie budowania logiki. Pusty rzut w ciemno po zmiennych hipermediach rozbiłby formę układu widżetów. W elastycznym łączeniu zasobów wyparł go potem model wymuszonych schematów zdefiniowanych w kodzie jak np. GraphQL.

87. Jak poprawnie zaprojektować **paginację** w API REST? Porównaj podejścia: offset-based, cursor-based, keyset pagination. Jakie nagłówki HTTP wspierają paginację?

   Zbyt duże zbiory rzędów z baz należy zwracać po podziale okiennym:
   **Offset-based:** (np. `?limit=10&offset=500`). Banalnie proste użycie składni SQL (LIMIT OFFSET), ale katastrofalnie skalujące się z czasem: jeśli użytkownik zażąda 10 milionów offesetu bazy, silnik bazy przelicza po drodze w zaporowym koszcie wszystkie wykluczone rekordy w kółko od 1 na starcie. Łatwo też dublować odczytane elementy, jeśli inni użytkownicy dodadzą nowy wiersz z inserta podczas, gdy przeglądasz środek wyników (przesunięcie okienkowe).
   **Cursor-based / Keyset:** (np. `?limit=10&after=token_hash_ID_wiersza`). Klient otrzymuje klucz (hash/cursor) na wiersz. Wywołanie wyszukuje natychmiast od danego miejsca z pełnym zyskiem indeksu tabeli `WHERE id > token_baza LIMIT 10`. Mechanika nie ulega uszkodzeniom przy pracy równoległych wstawieniach, i zwraca natychmiastowe obciążenie bez przegrzewania tabel w tle. Używana masowo w Infinite-scroll na np. Facebooku. Wadą podejścia od frontu – klient z API absolutnie nie przeskoczy na np. konkretną i wybraną "57 stronę widoku danych paginacji" – może klikać wyłącznie w przód albo w dół u tablic ze zbiorem o okno 10 kafelków po podanym parametrze After, a nie offsetowym numerze.
   **Nagłówki wspierające:** Dawniej często zaszywano gotowe odnośniki dla frontu w postaci linków z użyciem natywnego RFC nagłówka `Link: <https://api.../?page=3>; rel="next"`, oraz dodawano u góry parametry pod niestandardowy header w zwrotce z informacją o sumarycznej wielkości całej paczki np `X-Total-Count: 405` w obiekcie, ale ostatecznie zjawisko porzucono dla zaszywania wszystkiego w zwracanej i gotowej zagnieżdżonej nad-tabeli body z plikiem wyjściowym od JSONA wewnątrz meta-właściwości.

88. Jak obsłużyć **partial updates** zasobu? Opisz standard **JSON Patch (RFC 6902)** i **JSON Merge Patch (RFC 7386)** i ich związek z metodą PATCH.

   Metoda **PATCH** służy do częściowej aktualizacji modyfikującej w dokumencie merytorycznym u URL (w przeciwieństwie do zasady używania nadpisującego z użyciem PUT). Odbywa się to standardowymi formami dokumentowymi wysyłanymi do parsowania w locie:
   **JSON Merge Patch (RFC 7386):** Klient przesyła "ułamek encji dokumentu" – prosty malutki obiekt JSON ilustrujący jak docelowy wygląd zasobu powinieneś zmienić u góry u API, np `{ "city": "Kraków" }`. Scalenie odświeża wskazane klucze po nazwie a puste pola z boku chroni. Niesie ułomny problem z operacją czystego ustawiania modyfikacji i usunięcia fizycznego atrybutów, wymuszając wymuszone operacje na ustawieniach na `null`. Uszkadza całkowicie całe wewnętrzne tablice i struktury niszcząc pule rzutem po podtablicach.
   **JSON Patch (RFC 6902):** Klient nie przesyła wartości tylko tablicę ściśle sprecyzowanych instrukcji z komendami dla API (jak np strukturalny program do zmian w dokumencie – forma np: `[{ "op": "replace", "path": "/users/2/city", "value": "Kraków" }, { "op": "remove", "path": "/surname" }]`). Daje to bezkolizyjne gwarancje dla operacji u ujemnych null-i dając w tym również sprawdzane transakcje ("test") i idealne przenoszenie klocków dokumentu ("move") na skomplikowanym wielkim dokumencie. Używa rzadszego Content-Type w nagłówku `application/json-patch+json`.

89. Jak zaprojektować **bulk operations** w REST API, nie łamiąc semantyki HTTP? Jakie podejścia (batch endpoint, multipart) stosuje się w praktyce?

   Używanie RESTowych standardowych reguł HTTP u PUT i DELETE nakazuje rzetelnie uderzać odpytywaną operację pod URL bezpośrednio wskazujący na tylko i wyłącznie JEDEN odnalezolny z bazy ID element. Konstrukcje np kasowania 5 usunięć u jednego URI `DELETE /users/1,2,3` łamią REST.
   **Podejścia i standardy obronne:**
   1. **Endpointy Batch/RPC (Operacyjne API z POST):** Np wymuszone w API URL nadrzędnej i celowej operacji masowej rzucanej na zasób zbiorowy za pomocą uniwersalnego HTTP `POST /users/batch-delete`, podając w ciele listę IDs jako ułamkowy job procesu do uderzenia przez backend pod tablicą, ratując czyste wytyczne na pojedynczych obiektowych URI.
   2. **Pakowanie w Batch przez Multipart / OData:** Odpytywane przy projektowaniu zapytań złożonych dla klientów z zewnątrz od front-end API. Posyłamy zbiorczą transakcję dla systemu przy headerze `Content-Type: multipart/mixed` (lub z jsonową kolekcją i customowym formatem), np endpoint pod URI w root (`POST /api/$batch`) dając u użytkownika zlepek odizolowanych różnych merytorycznie żądań u frontendu (jedno o stworzenie zasobu, dwa o wywołanie updatu statusów, trzy zapytania GET do powiązań). Powoduje to ogromny zysk optymalizacji zasobu na rzetelnie obsłużonym zapytaniu (jeden uścisk 1 connection TCP, zamiast po jednym na wszystkie 5 pytań zlecenia na raz), zmniejszając użycie rurek w API i dając wielki zysk i skalowanie dla ogromnych wektorów API Enterprise.

90. Czym jest **content negotiation** w kontekście wersjonowania API? Porównaj wersjonowanie przez URL, nagłówek `Accept` i custom header.

   **Wersjonowanie przez URL (np. `/api/v2/users`):** Najprostsze do wdrożenia. Intuicyjne, cache jest dla tego w 100% rzetelny za rogiem z automatu, testowanie u curl u developerów banalne. Ale: łamie założenia REST (połączenie strukturalnego pojęcia jednego zbadanego zasobu dla danego adresu w z URL i śmiecenie merytorycznie wersji kodu aplikacji pod docelową tabelą), a aktualizacja z `v1` na `v2` przy gigantycznej operacji od frontendowej strony u klienta w oprogramowaniu zmusza go do bezczelnego nadpisywania i modyfikowania tysięcy endpointowych wpisanych na rygor linek w strukturze.
   **Wersjonowanie przez negocjacje z Accept (np. `Accept: application/vnd.myapi.v2+json`):** W 100% poprawne semantycznie i zgodne z czystym dogmatem REST – adres URI po zasób pozostaje czysty, nietknięty, jeden i wieloletni (`/api/users`), a w rzucie z zapytaniem u HTTP jedynie prosisz, w jaki logiczny wzorzec z API ci tę formę oblec do odbioru. Trudne do wprowadzania dynamicznych wdrożeń u klienta w deweloperskich oknach po ręcznych testach przeglądarki z wbudowanymi narzędziami, utrudnia mocno mechanizmy dla zapytań Proxy czy pamięci na buforowaniu i obciążeniach z nagłówkami `Vary: Accept` rzutów proxy o błędy do CDN w cache po starym pliku, rozbijając obciążenia dla load-balancerów w parsowaniu ścieżki po ruterze.
   **Custom Header (np. `X-API-Version: 2`):** Dobry i mądry balans. Odciąża u front-endu problem trudnej merytoryki z rozkodowaniem Accept w złożone formy `application/vnd...` wymuszając do czytelności od góry ostrego numeru z nagłówkiem z czystego strzału i chroniąc stałe niewersjonowane URI po wyjściu.

91. Jak poprawnie zaimplementować **asynchroniczne operacje** w REST API? Opisz wzorzec z kodem **202 Accepted** i polling statusu.

   Aby długa i czasochłonna dla backendu w API operacja wektorów generowania raportów miesięcznych nie zrywała opóźnieniami zrzutów timeout przy uścisku proxy z timeout na HTTP w zawieszaniu klienta, API stosuje w rozwiązaniach wzorzec Asynchronous Request-Reply z mechaniką powrotów Pollingu z frontendem:
   1. Klient frontendu inicjuje i narzuca w paczce żądanie na REST, np `POST /reports/yearly`.
   2. Odbierający to backend API rzuca akcje jako wydelegowane zadanie we wstrzykniętego w tło podłączonego do RabbitMQ Workera z kodem i z miejsca (w dosłownie po sekundzie i małym milisekundowym odbiciu z potwierdzenia) wysyła sygnał z odpisanym wyjściem dla połączenia HTTP ze zrzuconym odpowiedziowym statusem **`202 Accepted`** ("Żądanie poprawne, przyjęto. Kiedyś wykonamy w tle. Rzucę proces"). 
   3. W tym samym zrzucie dla 202 na wejściu o akceptacji serwer narzuca na front w nagłówku HTTP obligatoryjny docelowy stan odpowiedzi, np link pod adresem z `Location: /reports/status/xyz123`.
   4. Front-end (klient z UI powiązany i znający na nowo wektor Location) odpala nową pętlę i timer - zaczyna i odpytuje natrętnie używając po bezpiecznym i darmowym GET dla API w interwałowych ułamkach uderzając w dopytywania API pod nowym URI (`GET /reports/status/xyz123`), dopytując z zyskiem czy proces obrobił dane, dając za odpowiedź `200 OK` i obiekt jsona pod UI na powiadomieniu `{"status": "W TRAKCIE"}` z wbudowanymi nowymi szacunkami czasu.
   5. Po 30s asynchroniczne odciążone tło Worker po wyjściu z długiej pętli na bazy danych dla paczki, aktualizuje z powodzeniem z tyłu bazę stanu i zapis dla endpointu i pod /reports/status/xyz123 wystrzeliwuje na docelowy front nowym strzałem wyczekiwanym powiązany rzutem status w sieci `303 See Other` i podaną nowym statusem Location pod wycelowany dla wygenerowanego raportu PDF adresem i z pod zasobem `/reports/file/xyz123`, a klient ze swoim i wyizolowanym plikiem na HTTP po rzuceniu o ten wyciąg pliku z URL odbiera w pełnym zadowoleniu operację pobraną na nowo statusem o kodzie operacji po starym formacie GET na 200 OK z dokumentem bez psucia logiki zaporowych pętli w limitach w puli API.

---

## 14. Ewolucja i standardy

92. Opisz kluczowe różnice między **HTTP/1.0**, **HTTP/1.1**, **HTTP/2** i **HTTP/3** pod kątem modelu połączenia, multipleksowania i warstwy transportowej.
93. Czym jest **Structured Headers (RFC 8941)** i jak standaryzują parsowanie nagłówków HTTP?
94. Czym jest inicjatywa **HTTP Signatures** i jak umożliwia podpisywanie żądań HTTP na poziomie protokołu?
95. Czym jest **RFC 9110** i jak konsoliduje semantykę HTTP niezależnie od wersji protokołu?
96. Jak wygląda przyszłość HTTP — jakie propozycje i drafty IETF mogą zmienić protokół w najbliższych latach?

---

## Powiązane materiały

- [Mikroserwisy: Pytania Rekrutacyjne](mikroserwisy-pytania-rekrutacyjne.md)
- [System Design: Pytania Rekrutacyjne](system-design-pytania-rekrutacyjne.md)
- [TLS: Pytania Rekrutacyjne](tls-pytania-rekrutacyjne.md)
