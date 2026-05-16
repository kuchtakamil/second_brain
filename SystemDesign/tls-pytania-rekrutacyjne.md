# TLS: Pytania Rekrutacyjne

Lista pytań na rozmowę kwalifikacyjną z zakresu **TLS (Transport Layer Security)**. Pytania obejmują fundamenty protokołu, proces nawiązywania połączenia, zarządzanie certyfikatami oraz praktyczne aspekty wdrożeniowe. Poziom: Mid – Senior.

---

## 1. Podstawy protokołu

1. Czym jest TLS i jaki problem rozwiązuje? Jakie trzy właściwości bezpieczeństwa gwarantuje?

**Odpowiedź:**  
TLS (Transport Layer Security) to protokół zabezpieczający komunikację sieciową między klientem a serwerem, np. między przeglądarką a serwisem HTTPS. Rozwiązuje problem przesyłania danych przez niezaufaną sieć, w której ktoś może podsłuchiwać ruch, modyfikować pakiety albo podszywać się pod jedną ze stron.

TLS zapewnia trzy kluczowe właściwości bezpieczeństwa:

1. **Poufność** - dane są szyfrowane, więc osoba podsłuchująca ruch sieciowy nie powinna być w stanie odczytać treści komunikacji.
2. **Integralność** - odbiorca może wykryć, czy dane zostały zmienione po drodze.
3. **Uwierzytelnienie** - klient może zweryfikować, że rozmawia z właściwym serwerem, zwykle dzięki certyfikatowi X.509 podpisanemu przez zaufane CA. Opcjonalnie TLS może też uwierzytelniać klienta, np. w mTLS.


2. Czym różni się TLS od SSL i dlaczego SSL nie powinien być już używany?

**Odpowiedź:**  
SSL był starszym poprzednikiem TLS. TLS powstał jako jego bezpieczniejsza, standaryzowana kontynuacja. W praktyce nadal spotyka się określenia typu "certyfikat SSL", ale technicznie nowoczesne połączenia powinny używać TLS, nie SSL.

SSL nie powinien być już używany, ponieważ jego wersje, np. SSL 2.0 i SSL 3.0, mają znane podatności kryptograficzne i projektowe. Przykładem jest atak POODLE na SSL 3.0. Starsze wersje protokołu wspierają słabe algorytmy, gorsze mechanizmy negocjacji i nie spełniają obecnych wymagań bezpieczeństwa.

W praktyce należy wyłączyć SSL oraz stare wersje TLS, szczególnie TLS 1.0 i TLS 1.1, a używać TLS 1.2 albo TLS 1.3.

3. Na której warstwie modelu OSI działa TLS i jakie to ma konsekwencje dla protokołów wyższych warstw?

**Odpowiedź:**  
TLS działa pomiędzy warstwą transportową a aplikacyjną. Najczęściej działa nad TCP, ale pod protokołem aplikacyjnym. Przykładowo HTTP uruchomiony nad TLS daje HTTPS, a SMTP, IMAP czy gRPC również mogą korzystać z TLS do zabezpieczenia transmisji.

W modelu OSI TLS często opisuje się jako protokół warstwy sesji lub prezentacji, choć praktycznie najważniejsze jest to, że tworzy bezpieczny kanał dla protokołu aplikacyjnego.

Konsekwencją jest to, że protokoły wyższych warstw mogą korzystać z szyfrowania, integralności i uwierzytelnienia bez samodzielnego implementowania kryptografii. HTTP, SMTP czy IMAP zachowują swoją logikę, ale ich dane są przesyłane przez chroniony kanał TLS. TLS nie rozwiązuje jednak problemów bezpieczeństwa samej aplikacji, takich jak błędy autoryzacji, SQL injection czy wycieki danych po stronie serwera.

---

## 2. Handshake i nawiązywanie połączenia

4. Opisz ogólny przebieg **TLS Handshake** — jakie są jego główne kroki i cel każdego z nich?

**Odpowiedź:**  
TLS Handshake to faza inicjalizacji bezpiecznego połączenia. Jej celem nie jest jeszcze przesyłanie właściwych danych aplikacyjnych, tylko uzgodnienie parametrów bezpieczeństwa i zbudowanie wspólnego sekretu, z którego obie strony wyprowadzą klucze szyfrujące.

W uproszczeniu handshake odpowiada na kilka pytań:

1. **Jakiej wersji TLS używamy?**  
   Klient i serwer muszą uzgodnić np. TLS 1.2 albo TLS 1.3.

2. **Jakich algorytmów używamy?**  
   Strony negocjują cipher suite, czyli zestaw algorytmów do szyfrowania, uwierzytelniania i ochrony integralności.

3. **Z kim klient faktycznie rozmawia?**  
   Serwer przedstawia certyfikat, a klient weryfikuje jego poprawność, nazwę domeny i łańcuch zaufania.

4. **Jak ustalamy wspólny sekret?**  
   Najczęściej przez ephemeral Diffie-Hellman, np. ECDHE albo X25519, dzięki czemu obie strony ustalają sekret bez przesyłania go po sieci.

5. **Czy ktoś zmodyfikował handshake po drodze?**  
   Komunikaty `Finished` zawierają kryptograficzne potwierdzenie całej wcześniejszej wymiany.

6. **Kiedy można zacząć wysyłać dane aplikacyjne?**  
   Dopiero po wyprowadzeniu kluczy sesyjnych i potwierdzeniu integralności handshaku.

### Typowy pełny handshake w TLS 1.3

TLS 1.3 upraszcza handshake i zwykle kończy go w jednym round-tripie po stronie TLS, zakładając że połączenie transportowe, np. TCP, już istnieje.

```text
Klient                                               Serwer
  |                                                    |
  | ClientHello                                       |
  | - supported_versions                              |
  | - cipher_suites                                   |
  | - key_share                                       |
  | - SNI                                             |
  | - ALPN                                            |
  |--------------------------------------------------->|
  |                                                    |
  |                                      ServerHello   |
  |                                      - version     |
  |                                      - cipher      |
  |                                      - key_share   |
  |<---------------------------------------------------|
  |                                                    |
  |        Obie strony wyliczają sekrety handshake     |
  |                                                    |
  |                              EncryptedExtensions   |
  |                              Certificate           |
  |                              CertificateVerify     |
  |                              Finished              |
  |<---------------------------------------------------|
  |                                                    |
  | Finished                                           |
  |--------------------------------------------------->|
  |                                                    |
  |        Dane aplikacyjne szyfrowane kluczami TLS    |
  |<==================================================>|
```

#### 1. `ClientHello`

Klient zaczyna handshake i wysyła zestaw informacji potrzebnych do negocjacji:

- obsługiwane wersje TLS, np. TLS 1.2 i TLS 1.3,
- listę obsługiwanych cipher suites,
- losowe dane klienta,
- `key_share`, czyli publiczną część ephemeral Diffie-Hellman dla jednej lub kilku grup kryptograficznych,
- `SNI` (Server Name Indication), czyli nazwę domeny, z którą klient chce się połączyć,
- `ALPN` (Application-Layer Protocol Negotiation), np. propozycję `h2` dla HTTP/2 albo `http/1.1`,
- obsługiwane algorytmy podpisu,
- opcjonalnie informacje do wznowienia sesji, np. PSK/session ticket.

Cel tego kroku: klient mówi "oto co obsługuję, oto domena, z którą chcę rozmawiać, i oto materiał do ustalenia kluczy".

#### 2. `ServerHello`

Serwer wybiera parametry z propozycji klienta:

- wersję TLS,
- cipher suite,
- grupę wymiany kluczy,
- swój `key_share`,
- ewentualnie tryb wznowienia sesji.

Po `ClientHello` i `ServerHello` obie strony mają już wystarczająco dużo danych, aby policzyć wspólny sekret Diffie-Hellmana. Ten sekret nie został przesłany przez sieć. Każda strona wylicza go lokalnie z własnego klucza prywatnego ephemeral i publicznego udziału drugiej strony.

Cel tego kroku: serwer wybiera konkretny zestaw parametrów i dostarcza materiał potrzebny do ustalenia wspólnego sekretu.

#### 3. Wyprowadzenie kluczy handshake

Po wymianie `key_share` obie strony wykonują key schedule, czyli z uzgodnionego sekretu i transkryptu handshaku wyprowadzają klucze tymczasowe. W TLS 1.3 dalsze komunikaty handshaku są już szyfrowane.

Cel tego kroku: przejść z publicznej negocjacji do chronionej kryptograficznie części handshaku.

#### 4. `EncryptedExtensions`

Serwer wysyła dodatkowe uzgodnione parametry, które nie muszą być widoczne publicznie, np. wynik negocjacji ALPN.

Cel tego kroku: przekazać rozszerzenia wybrane przez serwer już w zaszyfrowanym kanale handshake.

#### 5. `Certificate`

Serwer wysyła swój certyfikat oraz zwykle certyfikaty pośrednie potrzebne do zbudowania łańcucha zaufania.

Klient sprawdza m.in.:

- czy certyfikat pasuje do domeny z URL/SNI,
- czy certyfikat nie wygasł i nie jest jeszcze nieważny,
- czy łańcuch prowadzi do zaufanego root CA,
- czy certyfikat ma właściwe użycie, np. server authentication,
- czy podpisy w łańcuchu są poprawne,
- czy algorytmy i długości kluczy są akceptowalne,
- opcjonalnie status unieważnienia, np. przez OCSP stapling, CRL albo mechanizmy przeglądarki.

Cel tego kroku: klient ma dostać materiał do uwierzytelnienia serwera.

#### 6. `CertificateVerify`

Sam certyfikat nie wystarcza. Serwer musi jeszcze udowodnić, że posiada klucz prywatny odpowiadający kluczowi publicznemu z certyfikatu. Robi to przez podpisanie transkryptu handshaku.

Cel tego kroku: uniemożliwić atakującemu samo skopiowanie cudzego certyfikatu i podszycie się pod serwer bez posiadania klucza prywatnego.

#### 7. `Finished` od serwera

Serwer wysyła MAC wyliczony z sekretu i całego dotychczasowego transkryptu handshaku.

Cel tego kroku: klient może wykryć, czy wcześniejsze komunikaty nie zostały zmienione po drodze. To chroni m.in. przed manipulacją negocjowanymi algorytmami.

#### 8. `Finished` od klienta

Klient, po zweryfikowaniu certyfikatu i komunikatu `Finished` serwera, odsyła własny `Finished`.

Cel tego kroku: serwer również dostaje potwierdzenie, że klient zna właściwe sekrety i widział ten sam, niezmodyfikowany transcript handshaku.

#### 9. Dane aplikacyjne

Po zakończeniu handshaku obie strony wyprowadzają klucze do danych aplikacyjnych. Od tego momentu HTTP, gRPC, SMTP albo inny protokół aplikacyjny działa wewnątrz szyfrowanego kanału.

```text
HTTP request:

GET /account HTTP/1.1
Host: example.com

Po stronie sieci widoczne jest tylko szyfrowane TLS Application Data,
a nie jawna treść requestu.
```

### Typowy pełny handshake w TLS 1.2

TLS 1.2 ma bardziej rozbudowany handshake. W nowoczesnej konfiguracji używa ECDHE, ale nadal historycznie wspierał też starsze mechanizmy, np. RSA key exchange, którego nie należy już używać.

```text
Klient                                               Serwer
  |                                                    |
  | ClientHello                                       |
  |--------------------------------------------------->|
  |                                                    |
  |                                      ServerHello   |
  |                                      Certificate   |
  |                              ServerKeyExchange     |
  |                         CertificateRequest?        |
  |                              ServerHelloDone       |
  |<---------------------------------------------------|
  |                                                    |
  | ClientKeyExchange                                 |
  | Certificate?                                      |
  | CertificateVerify?                                |
  | ChangeCipherSpec                                  |
  | Finished                                          |
  |--------------------------------------------------->|
  |                                                    |
  |                              ChangeCipherSpec      |
  |                              Finished              |
  |<---------------------------------------------------|
  |                                                    |
  |        Dane aplikacyjne szyfrowane kluczami TLS    |
  |<==================================================>|
```

Różnice praktyczne:

- TLS 1.2 zwykle wymaga większej liczby kroków niż TLS 1.3.
- W TLS 1.2 część informacji, np. certyfikat serwera, leci jawnie.
- TLS 1.2 ma `ChangeCipherSpec`, czyli jawny sygnał przełączenia na szyfrowanie.
- TLS 1.3 usunął wiele starych i ryzykownych opcji, m.in. statyczny RSA key exchange.
- W TLS 1.3 Perfect Forward Secrecy jest właściwie standardem dzięki ephemeral Diffie-Hellman.

### Co dzieje się w przypadkach brzegowych i awaryjnych?

#### Brak wspólnej wersji TLS

Jeśli klient obsługuje tylko wersje, których serwer nie akceptuje, handshake kończy się błędem, zwykle alertem typu `protocol_version`.

Przykład:

```text
Klient:  obsługuję TLS 1.0
Serwer:  akceptuję tylko TLS 1.2 i TLS 1.3
Wynik:   handshake przerwany
```

To jest pożądane zachowanie. Serwer nie powinien schodzić do przestarzałej wersji protokołu tylko po to, aby utrzymać kompatybilność.

#### Brak wspólnego cipher suite

Jeśli klient i serwer nie mają żadnego wspólnego zestawu algorytmów, serwer nie może bezpiecznie kontynuować.

```text
Klient:  TLS_AES_128_GCM_SHA256, TLS_CHACHA20_POLY1305_SHA256
Serwer:  tylko stare RSA_WITH_3DES_EDE_CBC_SHA
Wynik:   handshake_failure albo insufficient_security
```

W praktyce taki problem pojawia się przy bardzo starych klientach, zbyt agresywnie utwardzonym serwerze albo błędnej konfiguracji bibliotek TLS.

#### `HelloRetryRequest` w TLS 1.3

TLS 1.3 zakłada, że klient od razu wyśle `key_share`. Jeśli jednak klient wyśle udział dla grupy, której serwer nie chce użyć, serwer może odpowiedzieć `HelloRetryRequest`.

```text
Klient                                               Serwer
  | ClientHello: key_share = P-256                    |
  |--------------------------------------------------->|
  | HelloRetryRequest: użyj X25519                    |
  |<---------------------------------------------------|
  | ClientHello: key_share = X25519                   |
  |--------------------------------------------------->|
  | ServerHello ...                                   |
  |<---------------------------------------------------|
```

To dodaje dodatkowy round-trip, ale pozwala uniknąć wysyłania przez klienta zbyt wielu udziałów klucza naraz.

#### Błąd certyfikatu serwera

Klient powinien przerwać handshake, jeżeli certyfikat jest niepoprawny. Typowe przypadki:

- certyfikat wygasł,
- certyfikat jest wystawiony na inną domenę,
- brakuje certyfikatu pośredniego,
- root CA nie jest zaufany,
- certyfikat został odwołany,
- użyto zbyt słabego algorytmu podpisu,
- certyfikat jest poprawny technicznie, ale narusza politykę klienta, np. certificate pinning.

Przykład:

```text
URL:          https://api.example.com
Certyfikat:  CN/SAN = internal.local
Wynik:       hostname verification failed
```

W przeglądarce użytkownik zobaczy ostrzeżenie. W backendach, klientach HTTP i komunikacji service-to-service poprawnym zachowaniem jest zwykle twarde przerwanie połączenia, a nie ignorowanie błędu.

#### Serwer nie ma właściwego certyfikatu dla SNI

SNI pozwala serwerowi wybrać certyfikat dla konkretnej domeny, gdy wiele domen działa pod tym samym adresem IP.

```text
Klient: ClientHello, SNI = shop.example.com
Serwer: wybiera certyfikat dla shop.example.com
```

Jeśli klient nie wyśle SNI albo wyśle błędne SNI, serwer może zwrócić certyfikat domyślny. Wtedy klient prawdopodobnie odrzuci połączenie, bo domena z certyfikatu nie będzie pasować do żądanej domeny.

#### ALPN nie wybierze wspólnego protokołu aplikacyjnego

ALPN negocjuje protokół aplikacyjny wewnątrz TLS, np. HTTP/2 albo HTTP/1.1.

```text
Klient:  ALPN = h2, http/1.1
Serwer:  wybiera h2
```

Jeśli nie ma wspólnej opcji, serwer może nie wybrać żadnego protokołu albo przerwać handshake, zależnie od konfiguracji. Dla HTTP najczęściej następuje fallback do HTTP/1.1, jeśli obie strony go obsługują. Dla protokołów bardziej restrykcyjnych, np. niektórych konfiguracji gRPC, brak `h2` może oznaczać błąd połączenia.

#### Mutual TLS, czyli certyfikat klienta

W standardowym HTTPS uwierzytelniany jest głównie serwer. W mTLS serwer żąda również certyfikatu klienta.

TLS 1.3 wygląda wtedy koncepcyjnie tak:

```text
Klient                                               Serwer
  | ClientHello                                       |
  |--------------------------------------------------->|
  | ServerHello                                       |
  | EncryptedExtensions                               |
  | CertificateRequest                                |
  | Certificate                                       |
  | CertificateVerify                                 |
  | Finished                                          |
  |<---------------------------------------------------|
  | Certificate                                       |
  | CertificateVerify                                 |
  | Finished                                          |
  |--------------------------------------------------->|
```

Serwer sprawdza certyfikat klienta podobnie jak klient sprawdza certyfikat serwera: łańcuch zaufania, ważność, przeznaczenie certyfikatu, polityki i ewentualne mapowanie certyfikatu na tożsamość aplikacyjną.

Przypadki brzegowe:

- klient nie ma certyfikatu, a serwer go wymaga - handshake kończy się błędem,
- klient wysyła certyfikat z niezaufanego CA - serwer odrzuca połączenie,
- certyfikat klienta jest poprawny kryptograficznie, ale nie ma uprawnień biznesowych - TLS może się udać, a aplikacja zwróci np. `403 Forbidden`.

#### Session resumption

TLS może wznowić wcześniejszą sesję, aby skrócić handshake. W TLS 1.3 często używa się PSK/session ticket.

```text
Pierwsze połączenie:
  pełny handshake -> serwer wydaje ticket

Kolejne połączenie:
  klient wysyła ticket/PSK -> krótszy handshake
```

Cel: mniej opóźnień i mniej kosztownych operacji kryptograficznych.

Ważne konsekwencje:

- resumption nadal musi być chronione przed replay i błędną konfiguracją,
- bilety sesyjne powinny mieć rozsądny czas życia,
- rotacja kluczy do szyfrowania ticketów jest istotna,
- przy źle zarządzanych ticketach można osłabić właściwości forward secrecy dla wznowionych sesji.

#### 0-RTT / Early Data

TLS 1.3 pozwala przy wznowieniu sesji wysłać dane aplikacyjne bardzo wcześnie, czasem razem z pierwszym komunikatem. To przyspiesza połączenie, ale takie dane mogą być podatne na replay.

```text
Klient                                               Serwer
  | ClientHello + Early Data                          |
  |--------------------------------------------------->|
  |                         ServerHello + Finished    |
  |<---------------------------------------------------|
```

Dlatego 0-RTT powinno być używane tylko dla operacji idempotentnych albo takich, dla których aplikacja ma osobną ochronę przed powtórzeniem. Dobre przykłady to niektóre odczyty. Złe przykłady to płatność, złożenie zamówienia albo zmiana hasła.

#### Atak downgrade i manipulacja negocjacją

Atakujący mógłby próbować wymusić słabszą wersję TLS lub słabszy algorytm. TLS chroni przed tym przez:

- podpisy i MAC obejmujące transcript handshaku,
- `Finished`, który wykrywa modyfikację wcześniejszych komunikatów,
- mechanizmy downgrade protection w nowoczesnych wersjach,
- politykę klienta i serwera, która zabrania starych wersji i słabych algorytmów.

Jeśli ktoś zmieni po drodze np. listę cipher suites w `ClientHello`, końcowe sprawdzenie transkryptu nie przejdzie i handshake zostanie zerwany.

#### Zerwanie połączenia w trakcie handshaku

Handshake może zostać przerwany zanim powstanie bezpieczny kanał:

- TCP connection reset,
- timeout,
- błędny alert TLS,
- load balancer zamknie połączenie,
- serwer jest przeciążony,
- middlebox nie rozumie nowszej wersji TLS,
- klient wysyła niepoprawny format komunikatu.

Z perspektywy aplikacji zwykle objawia się to jako błąd połączenia, np. timeout, `TLS handshake failed`, `connection reset by peer` albo `remote error: tls: handshake failure`.

#### TLS termination na load balancerze lub reverse proxy

W wielu systemach klient nie zestawia TLS bezpośrednio z aplikacją, tylko z load balancerem, ingress controllerem albo reverse proxy.

```text
Klient --TLS--> Load Balancer --HTTP albo TLS--> Aplikacja
```

W takim przypadku handshake kończy się na komponencie terminującym TLS. To on posiada certyfikat, wybiera parametry TLS i odszyfrowuje ruch. Dalej do aplikacji ruch może iść:

- plaintextem HTTP w zaufanej sieci prywatnej,
- ponownie szyfrowany TLS-em,
- mTLS-em między proxy a backendem.

To ważne operacyjnie, bo "mamy HTTPS" nie zawsze oznacza, że cały ruch wewnętrzny między komponentami też jest szyfrowany.

### Podsumowanie na rozmowie

Na rozmowie można odpowiedzieć krótko tak:

> TLS Handshake to proces, w którym klient i serwer negocjują wersję protokołu oraz algorytmy, wykonują wymianę kluczy, uwierzytelniają serwer przez certyfikat, opcjonalnie uwierzytelniają klienta, a następnie potwierdzają integralność całej negocjacji komunikatami `Finished`. Po tym obie strony mają wspólne klucze sesyjne i mogą przesyłać dane aplikacyjne w szyfrowanym kanale. W TLS 1.3 jest to prostsze i szybsze niż w TLS 1.2, a większość nowoczesnych konfiguracji używa ephemeral Diffie-Hellman, dzięki czemu zapewnia Perfect Forward Secrecy.

5. Czym różni się handshake w **TLS 1.2** od **TLS 1.3** pod względem liczby round-tripów i wydajności?

**Odpowiedź:**  
TLS 1.3 upraszcza handshake względem TLS 1.2. Typowy pełny handshake TLS 1.3 wymaga jednego round-tripa po zestawieniu TCP, bo klient już w `ClientHello` wysyła materiał do wymiany kluczy (`key_share`). W TLS 1.2 pełny handshake jest zwykle dłuższy i wymaga większej liczby komunikatów przed rozpoczęciem przesyłania danych aplikacyjnych.

TLS 1.3 jest dzięki temu szybszy, ma mniejsze opóźnienie startowe i usuwa stare, ryzykowne mechanizmy, np. statyczny RSA key exchange. Dodatkowo TLS 1.3 lepiej wspiera session resumption i opcjonalne 0-RTT, choć 0-RTT ma osobne ryzyka bezpieczeństwa.

6. Czym jest **0-RTT (Early Data)** w TLS 1.3 i jakie ryzyka bezpieczeństwa ze sobą niesie?

**Odpowiedź:**  
0-RTT, czyli Early Data, pozwala klientowi wysłać dane aplikacyjne już na początku połączenia TLS 1.3, jeżeli wznawia wcześniejszą sesję na podstawie PSK/session ticket. Zaletą jest mniejsze opóźnienie, bo klient nie musi czekać na zakończenie pełnego handshaku.

Główne ryzyko to podatność na replay. Atakujący może spróbować powtórzyć przechwycone early data. Dlatego 0-RTT powinno być używane tylko dla operacji idempotentnych, np. bezpiecznych odczytów. Nie powinno się go używać dla operacji typu płatność, zmiana hasła, utworzenie zamówienia czy wykonanie przelewu, chyba że aplikacja ma własną skuteczną ochronę przed powtórzeniem.

---

## 3. Certyfikaty i infrastruktura klucza publicznego (PKI)

7. Czym jest **certyfikat X.509** i jakie kluczowe informacje zawiera?

**Odpowiedź:**  
Certyfikat X.509 to cyfrowy dokument wiążący klucz publiczny z konkretną tożsamością, np. domeną internetową. W TLS serwer pokazuje taki certyfikat klientowi, aby klient mógł sprawdzić, że rozmawia z właściwym serwerem.

Certyfikat zawiera m.in. nazwę podmiotu, klucz publiczny, okres ważności, issuer, czyli wystawcę certyfikatu, numer seryjny, algorytm podpisu, rozszerzenia oraz listę nazw domen w polu SAN. Dla HTTPS najważniejsze jest, aby domena z URL pasowała do SAN, certyfikat był ważny czasowo i łańcuch prowadził do zaufanego CA.

8. Jak działa **łańcuch zaufania** (certificate chain) i jaka jest rola **Certificate Authority (CA)**?

**Odpowiedź:**  
Łańcuch zaufania łączy certyfikat serwera z zaufanym certyfikatem głównym, który klient ma w swoim trust store. Zwykle wygląda to tak: certyfikat serwera został podpisany przez intermediate CA, intermediate CA został podpisany przez root CA, a root CA jest zaufany przez system operacyjny, przeglądarkę albo środowisko uruchomieniowe.

CA, czyli Certificate Authority, potwierdza tożsamość podmiotu i podpisuje certyfikat. Klient nie ufa automatycznie każdemu certyfikatowi, tylko sprawdza podpisy, ważność certyfikatów, przeznaczenie certyfikatu i zgodność domeny. Jeżeli łańcuch jest niepełny, wygasły albo prowadzi do niezaufanego root CA, połączenie powinno zostać odrzucone.

9. Czym jest **mutual TLS (mTLS)** i w jakich scenariuszach się go stosuje?

**Odpowiedź:**  
mTLS to wariant TLS, w którym nie tylko klient weryfikuje certyfikat serwera, ale także serwer weryfikuje certyfikat klienta. Dzięki temu obie strony są uwierzytelnione na poziomie kanału TLS.

Stosuje się go często w komunikacji service-to-service, mikroserwisach, service mesh, integracjach B2B, dostępie do API o wysokim poziomie bezpieczeństwa oraz w systemach wewnętrznych, gdzie samo hasło albo token nie wystarcza. mTLS dobrze potwierdza tożsamość techniczną klienta, ale autoryzacja biznesowa nadal zwykle należy do aplikacji.

10. Czym jest **certificate pinning** i jakie są jego zalety oraz wady?

**Odpowiedź:**  
Certificate pinning polega na tym, że klient akceptuje tylko konkretny certyfikat, konkretny klucz publiczny albo wskazane CA, zamiast ufać całemu standardowemu zestawowi zaufanych CA. Najczęściej spotyka się to w aplikacjach mobilnych i klientach kontrolowanych przez właściciela systemu.

Zaletą jest ograniczenie skutków błędnie wydanego certyfikatu przez inne CA. Wadą jest ryzyko awarii przy rotacji certyfikatów lub kluczy. Jeśli pin nie zostanie zaktualizowany na czas, aplikacja może przestać łączyć się z backendem. Pinning utrudnia też diagnostykę i legalne przechwytywanie ruchu w środowiskach testowych.

---

## 4. Szyfrowanie i bezpieczeństwo

11. Czym jest **cipher suite** i z jakich elementów się składa? Podaj przykład nowoczesnego cipher suite.

**Odpowiedź:**  
Cipher suite to zestaw algorytmów kryptograficznych używanych przez TLS do ochrony połączenia. W TLS 1.2 nazwa cipher suite zwykle obejmuje wymianę kluczy, uwierzytelnienie, szyfrowanie symetryczne i funkcję skrótu, np. `TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256`.

W TLS 1.3 cipher suites są prostsze, bo wymiana kluczy i uwierzytelnienie są negocjowane osobno. Przykład nowoczesnego cipher suite to `TLS_AES_128_GCM_SHA256` albo `TLS_CHACHA20_POLY1305_SHA256`. W praktyce preferuje się algorytmy AEAD, takie jak AES-GCM lub ChaCha20-Poly1305.

12. Czym jest **Perfect Forward Secrecy (PFS)** i dlaczego jest ważne? Jakie algorytmy wymiany kluczy ją zapewniają?

**Odpowiedź:**  
Perfect Forward Secrecy oznacza, że przechwycenie długoterminowego klucza prywatnego serwera w przyszłości nie pozwala odszyfrować wcześniej nagranych sesji TLS. Jest to ważne, bo atakujący może zapisywać ruch dzisiaj i próbować odszyfrować go dopiero po latach, gdy zdobędzie klucz prywatny.

PFS zapewniają efemeryczne mechanizmy Diffie-Hellmana, np. DHE, ECDHE oraz grupy takie jak X25519. Nie zapewnia go stary statyczny RSA key exchange, gdzie sekret sesji był zależny od długoterminowego klucza prywatnego serwera. TLS 1.3 w praktyce wymusza podejście zgodne z PFS.

---

## 5. Aspekty operacyjne i wdrożeniowe

13. Czym jest **TLS termination** i w którym miejscu architektury najczęściej się ją stosuje? Jakie są kompromisy?

**Odpowiedź:**  
TLS termination oznacza zakończenie połączenia TLS na konkretnym komponencie infrastruktury, np. load balancerze, reverse proxy, ingress controllerze albo API gatewayu. To ten komponent posiada certyfikat, wykonuje handshake i odszyfrowuje ruch.

Zaletą jest prostsze zarządzanie certyfikatami, centralna konfiguracja TLS, łatwiejsze logowanie, routing i odciążenie aplikacji. Kompromis polega na tym, że za punktem terminacji ruch może iść dalej plaintextem, jeśli nie zostanie ponownie zaszyfrowany. W środowiskach o wyższych wymaganiach bezpieczeństwa często stosuje się TLS albo mTLS również między proxy a backendami.

14. Jak działa **SNI (Server Name Indication)** i jaki problem rozwiązuje w kontekście hostowania wielu domen na jednym adresie IP?

**Odpowiedź:**  
SNI to rozszerzenie TLS, w którym klient podaje nazwę domeny już w `ClientHello`. Dzięki temu serwer może wybrać właściwy certyfikat zanim zakończy się handshake.

Bez SNI serwer widziałby tylko adres IP i port, więc przy wielu domenach na jednym IP nie wiedziałby, który certyfikat pokazać. SNI umożliwia więc hostowanie wielu serwisów HTTPS na tym samym adresie IP. Jeśli klient nie wyśle SNI albo poda błędną nazwę, serwer może zwrócić certyfikat domyślny, który nie będzie pasował do oczekiwanej domeny.

15. Jak monitorować i zarządzać **wygasaniem certyfikatów** w środowisku produkcyjnym? Czym jest **ACME / Let's Encrypt** i jak automatyzuje ten proces?

**Odpowiedź:**  
Wygasanie certyfikatów warto monitorować automatycznie, np. przez alerty z systemu monitoringu, syntetyczne testy HTTPS, skanery certyfikatów, metryki z load balancerów oraz regularne sprawdzanie dat ważności dla domen publicznych i wewnętrznych. Alert powinien pojawić się z wyprzedzeniem, np. 30, 14 i 7 dni przed wygaśnięciem.

ACME to protokół automatyzujący wystawianie i odnawianie certyfikatów. Let's Encrypt jest publicznym CA, które używa ACME i pozwala automatycznie uzyskiwać darmowe certyfikaty po udowodnieniu kontroli nad domeną, np. przez HTTP-01 albo DNS-01 challenge. W praktyce używa się narzędzi takich jak certbot, cert-manager w Kubernetes albo integracji w load balancerach i platformach cloud.

---

## Powiązane materiały

- [Mikroserwisy: Pytania Rekrutacyjne](mikroserwisy-pytania-rekrutacyjne.md)
- [System Design: Pytania Rekrutacyjne](system-design-pytania-rekrutacyjne.md)
