# Cykl życia żądania HTTP/1.1: Co się dzieje po wysłaniu requestu?

Ten dokument szczegółowo wyjaśnia na poziomie eksperckim, co dokładnie dzieje się pod spodem, gdy aplikacja (klient) wysyła standardowe żądanie HTTP/1.1 do serwera przez sieć Internet, z pominięciem omawiania wariantów kodów odpowiedzi, a skupiając się na przepływie sieciowym, protokołach transportowych i infrastrukturze.

## Dlaczego to jest ważne?

Dogłębne zrozumienie cyklu życia żądania HTTP jest fundamentalne dla architektów systemów, inżynierów DevOps i programistów backendu. Pozwala na:
- **Analizę i debugowanie opóźnień** (latency) oraz poprawną interpretację metryk takich jak DNS Lookup Time, TCP Connection Time, TLS Handshake czy TTFB (Time To First Byte).
- **Rozwiązywanie problemów warstwy sieciowej** (np. błędy 502/504, utraty pakietów, zrywane połączenia).
- **Optymalizację infrastruktury** (zarządzanie pulą połączeń, konfiguracja Load Balancerów, strojenie mechanizmu Keep-Alive).

## Jak to działa w praktyce?

Proces od momentu zainicjowania żądania przez kod aplikacji (np. `HttpClient.send()`, czy wywołanie funkcji `fetch()` w przeglądarce) do otrzymania odpowiedzi można podzielić na kilka ścisłych warstw.

### 1. Parsowanie URI i weryfikacja HSTS
Zanim jakikolwiek pakiet trafi do sieci, biblioteka klienta rozkłada docelowy URL na składowe (schemat, host, port, ścieżka). 
Jeżeli żądanie było pierwotnie wykonane przez zwykłe `http://`, zaawansowany klient (np. przeglądarka) sprawdza swoją wewnętrzną pamięć podręczną **HSTS (Strict-Transport-Security)**. Jeśli domena znajduje się na liście (lub zaszytej w kodzie *Preload List*), klient natychmiast i bez puszczania ruchu sieciowego podmienia schemat na bezpieczne `https://`, co neutralizuje wektor ataków *SSL-stripping* i MitM.

### 2. Rozwiązywanie nazw DNS (Domain Name System)
Klient musi zamienić czytelną nazwę domeny (np. `api.example.com`) na docelowy adres IP, aby warstwa sieciowa wiedziała, gdzie wysłać pakiet.
- Proces zaczyna się od szybkiego sprawdzenia lokalnego bufora (DNS cache przeglądarki, potem cache systemu operacyjnego - np. demona `systemd-resolved` lub pliku `/etc/hosts`).
- W przypadku "Miss", biblioteka resolvera OS wysyła asynchroniczne zapytanie po protokole UDP (port 53) do wskazanego w konfiguracji serwera DNS (np. dostawcy ISP, lub `1.1.1.1`).
- Resolver rekursywny "chodzi" po serwerach od odgórnych (Root Servers, potem TLD dla `.com`, aż po Authoritative Server dla `example.com`), by w końcu zwrócić do klienta rekord A (adres IPv4) lub AAAA (adres IPv6). Ten krok wprowadza pierwsze opóźnienie mierzalne w RTT (Round Trip Time).

### 3. Nawiązanie połączenia L4 (TCP 3-way Handshake)
Ponieważ HTTP/1.1 historycznie używa protokołu TCP w warstwie transportowej (w przeciwieństwie do QUIC z HTTP/3), konieczne jest fizyczne ustanowienie rury komunikacyjnej zapewniającej gwarancję dostarczenia danych.
1. Klient wysyła pakiet TCP z flagą **SYN** (Synchronize) na docelowy port (443).
2. Serwer (lub Load Balancer frontujący aplikację) odbiera pakiet i odpowiada **SYN-ACK**.
3. Klient kwituje odebranie wysyłając flagę **ACK**.
W tym momencie socket TCP po stronie klienta uznaje się za otwarty do dwustronnego (full-duplex) przesyłania strumienia bajtów. Ten etap to kolejne 1 pełne RTT opóźnienia.

### 4. Zabezpieczenie tunelu kryptograficznego (TLS Handshake)
Jeśli używamy szyfrowania (HTTPS), tuż po handshake'u TCP, klient i serwer muszą wynegocjować szyfr na poziomie warstwy prezentacji.
- **ClientHello**: Klient wysyła swoje wspierane wersje protokołu (np. TLS 1.3), zestawy szyfrów (Cipher Suites) oraz, co krytyczne – rozszerzenie **SNI (Server Name Indication)**. SNI podaje nazwę domenową "na zewnątrz" TLS-a. Jest to konieczne dla Load Balancerów i wirtualnego hostingu, aby wiedziały, z jakim certyfikatem mają odpowiedzieć, zanim jeszcze rozszyfrują jakikolwiek pakiet L7.
- **ServerHello**: Serwer odrzuca niechciane szyfry, wybiera standard i prezentuje klientowi swój podpisany certyfikat z kluczem publicznym.
- Klient weryfikuje ważność certyfikatu z lokalnym magazynem urzędów certyfikacji (Root CA) i weryfikuje łańcuch zaufania. Klient oblicza "pre-master secret" lub wykorzystuje asymetryczną wymianę kluczy (np. Diffie-Hellman), po czym obie strony generują wysoce wydajny, **symetryczny klucz sesji**.
Od teraz wszystkie bajty HTTP są zamknięte w hermetycznym, odpornym na podsłuch i manipulację strumieniu.

### 5. Kompresja i pakowanie żądania L7 (HTTP)
Klient HTTP buduje w pamięci czysto tekstową reprezentację żądania. Składa się na nią:
```http
POST /api/orders HTTP/1.1
Host: api.example.com
Connection: keep-alive
Content-Type: application/json
Accept-Encoding: gzip, br
Content-Length: 42

{"item":"book","qty":1}
```
Całość jest szyfrowana w TLS. Z uwagi na limity infrastruktury fizycznej, strumień cięty jest na tzw. segmenty (odpowiednie do MTU – Maximum Transmission Unit, standardowo 1500 bajtów). Warstwa TCP odpowiada za nałożenie mechanizmów unikania zatorów (*Congestion Control*, jak TCP BBR czy CUBIC), by nie zapchać routerów na trasie.

> **Warto wiedzieć: Czy istnieje "HTTP Handshake"?**
> W klasycznym protokole HTTP/1.1 **nie istnieje pojęcie handshake'u** negocjującego parametry sesji na warstwie aplikacji (tak jak to ma miejsce w L4/L6). Klient, po poprawnym zestawieniu tunelu niższych warstw, od razu wysyła strumień bajtów z właściwym żądaniem (architektura bezstanowa). Obecność poszczególnych "uścisków dłoni" zależy od siebie sekwencyjnie: handshake TCP jest **bezwzględnie wymagany** i warunkuje przejście dalej. Handshake TLS zaczyna się dopiero w otwartym TCP, jest wymagany przy HTTPS (i warunkuje wysłanie requestu, jeśli szyfrowanie jest nakazane). Samo HTTP natomiast wpada "na gotowe" i w 1.1 nie ma własnego wstępnego komunikatu (poza rzadkim negocjowaniem przesyłania dużego body przez nagłówek `Expect: 100-continue`).

### 6. Podróż przez infrastrukturę (Edge, Load Balancing i Reverse Proxy)
Pakiety przebywają kolejne fizyczne węzły internetu w warstwie 3 (IP routing za pomocą m.in. protokołu BGP). Często nie docierają do samego serwera, ale do brzegu chmury:
- Przy standardowym ruchu trafiamy na rozkład obciążenia (**L7 Load Balancer** / Nginx / HAProxy / Ingress), który kończy negocjacje TLS (zjawisko *TLS Termination*). Posiada on klucz prywatny serwera.
- **Hierarchiczny Load Balancing:** Przy bardzo dużym natężeniu ruchu (np. w systemach Big Tech), pojedyncza maszyna czy zwykły klaster L7 Load Balancera szybko stałby się wąskim gardłem. Wówczas stosuje się infrastrukturę kaskadową. Ruch najpierw rozdzielany jest na poziomie DNS (np. w podejściu Geo-DNS lub Round Robin) i przez globalne mechanizmy Anycast IP, a potem wchodzi na ultra-wydajne, nie wnikające w payload **L4 Load Balancery** (działające na poziomie sprzętu lub w kernelu, bazujące np. na technice ECMP). Te Load Balancery L4 rozrzucają strumienie TCP z ogromną przepustowością do olbrzymiej farmy węzłów działających w warstwie 7.
- Odtwarza tekstowe zapytanie HTTP węzeł L7 i bada je – analizuje ścieżkę, pliki cookie, by podjąć decyzję o rutingu, np. skierować `/api` do mikroserwisu A, a `/assets` do CDN.
- Proxy wstrzykuje dodatkowe nagłówki dla backendu, ułatwiające trace'owanie: np. `X-Forwarded-For` (z adresem IP oryginalnego klienta), `X-Request-Id` (UUID dla logów).
- Następnie wysyła ruch wewnątrz bezpiecznej sieci prywatnej na serwer aplikacyjny, zwykle oszczędzając czas poprzez uderzenie już dawno otwartym po stronie proxy włączonym **Connection Pooling** w stronę upstreamu.

### 7. Przetwarzanie przez aplikację Backendową
Serwer aplikacyjny (np. Node.js, Kestrel, Tomcat) parsuje dotarłe bajty z wewnętrznego gniazda i wywołuje przypisany handler w aplikacji webowej.
Kod domenowy wykonuje operacje (zapytania po TCP do bazy danych, szyny zdarzeń). 
W optymalizowanym procesie, by skrócić TTFB (Time to First Byte), serwer może rozpocząć przesyłanie wygenerowanej odpowiedzi w częściach jeszcze zanim pełny zasób zostanie zmontowany w RAM-ie (wykorzystując nagłówek `Transfer-Encoding: chunked`). Serwer nakłada w locie również kompresję wskazaną w zapytaniu, np. `Content-Encoding: br` (Brotli).

### 8. Odpowiedź i utrzymanie stanu połączenia (Keep-Alive)
Klient odbiera wszystkie zaszyfrowane pakiety, defragmentuje je warstwą TCP, rozszyfrowuje silnikiem TLS, upewniając się na podstawie sum kontrolnych (MAC), że nie uległy zniekształceniu. Następnie dekompresuje bajty algorytmem wskazanym w odpowiedzi, przekazując wynik pod wywołanie aplikacji czy silnik renderowania przeglądarki.

Na sam koniec wkracza mechanika fundamentalna dla zysku z protokołu HTTP/1.1: **Keep-Alive (Persistent Connection)**. **W standardzie HTTP/1.1 połączenie TCP nie jest zrywane natychmiast po otrzymaniu odpowiedzi przez klienta.** Zamiast tego serwer i klient powstrzymują się przed zamknięciem użytego, "gorącego" i wynegocjowanego gniazda TCP. Gniazdo zostaje bezczynne w wewnętrznej puli klienta i czeka na ewentualne kolejne strzały do danej domeny `api.example.com`. Dopiero gdy minie nałożony *Keep-Alive Timeout* (np. po 60 sekundach), serwer jako pierwszy prześle flagę `FIN`, ostatecznie zamykając otwarty w kroku trzecim strumień i uwalniając zasoby OS.

## Powiązane materiały

- [HTTP: Pytania Rekrutacyjne](http-pytania-rekrutacyjne.md)
- [Proxy z limitem latencji (System Design)](proxy-z-limitem-latencji-300ms.md)
- [CORS (Cross-Origin Resource Sharing)](cors.md)
- [TLS: Pytania Rekrutacyjne](tls-pytania-rekrutacyjne.md)
