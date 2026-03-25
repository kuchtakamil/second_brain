# Wytłumacz rodzaje rekordów DNS.

**Data:** 18 sty 2026, 18:08:00 CET

---

**User:**

Wytłumacz rodzaje rekordów DNS.

---

**Gemini:**

System DNS (Domain Name System) opiera się na rozproszonej bazie danych zawierającej wpisy zwane rekordami zasobów (**Resource Records – RR**). Każdy rekord posiada określony typ, klasę (zazwyczaj IN dla Internet), czas wygasania (TTL) oraz dane (RDATA).

### Podstawowe rekordy adresowe i aliasy

- **A (Address Record):** Mapuje nazwę hosta na jego 32-bitowy adres IPv4. Jest to fundamentalny rekord używany do kierowania ruchu na konkretny serwer.
- **AAAA (IPv6 Address Record):** Pełni tę samą funkcję co rekord A, ale mapuje nazwę na 128-bitowy adres IPv6.
- **CNAME (Canonical Name Record):** Tworzy alias dla istniejącej nazwy kanonicznej. Wskazuje jedną nazwę domeny na inną (np. `www.example.com` -> `example.com`).
  - *Uwaga techniczna:* Zgodnie z RFC 1034, rekord CNAME nie powinien współistnieć z innymi rekordami dla tej samej nazwy (co wyklucza jego użycie w wierzchołku domeny – *Apex Zone* – gdzie wymagane są rekordy NS i SOA). Rozwiązaniem tego problemu są niestandardowe rekordy typu **ALIAS** lub **ANAME** oferowane przez niektórych dostawców.

---

### Obsługa poczty i metadane strefy

- **MX (Mail Exchange):** Określa serwery pocztowe odpowiedzialne za przyjmowanie wiadomości e-mail w obrębie domeny. Składa się z wartości priorytetu (im niższa liczba, tym wyższy priorytet) oraz nazwy hosta serwera SMTP.
- **NS (Name Server):** Deleguje strefę DNS do konkretnych serwerów nazw. Wskazuje, które serwery są autorytatywne dla danej domeny.
- **SOA (Start of Authority):** Zawiera kluczowe informacje o strefie DNS, w tym:
  - `MNAME`: Główny serwer nazw dla strefy.
  - `RNAME`: Adres e-mail administratora (kropka zamiast `@`).
  - `Serial`: Numer seryjny używany do replikacji strefy (Secondary DNS).
  - `Refresh/Retry/Expire`: Parametry czasowe dla serwerów zapasowych.

---

### Rekordy informacyjne i weryfikacyjne

- **TXT (Text Record):** Przechowuje dowolny tekst w formacie ASCII. Współcześnie wykorzystywany głównie do implementacji protokołów bezpieczeństwa poczty:
  - **SPF (Sender Policy Framework):** Definiuje adresy IP uprawnione do wysyłki maili.
  - **DKIM (DomainKeys Identified Mail):** Przechowuje klucze publiczne do weryfikacji podpisów cyfrowych wiadomości.
  - **DMARC:** Instrukcje dla serwerów odbiorczych dotyczące postępowania z wiadomościami, które nie przeszły testów SPF/DKIM.
- **CAA (Certification Authority Authorization):** Pozwala właścicielowi domeny określić, które urzędy certyfikacji (CA) są uprawnione do wystawiania certyfikatów SSL/TLS dla tej domeny.

---

### Rekordy specjalistyczne i zaawansowane

| Typ rekordu | Pełna nazwa | Zastosowanie |
| --- | --- | --- |
| **SRV** | Service Record | Definiuje lokalizację specyficznych usług (np. SIP, XMPP, Active Directory). Zawiera port, priorytet i wagę. |
| **PTR** | Pointer Record | Wykorzystywany w strefach odwrotnych (Reverse DNS) do mapowania adresu IP na nazwę hosta (odwrotność rekordu A). |
| **DS** | Delegation Signer | Używany w **DNSSEC** do zabezpieczenia delegacji strefy; zawiera skrót klucza KSK strefy podrzędnej. |
| **DNSKEY** | DNS Key | Zawiera klucz publiczny używany do weryfikacji podpisów cyfrowych w DNSSEC. |
| **TLSA** | TLSA Certificate Association | Służy do protokołu DANE, wiążąc certyfikat TLS lub klucz publiczny z nazwą domeny w systemie DNS. |

---

### Struktura rekordu w pliku strefy (BIND format)

Poniżej znajduje się przykład technicznej reprezentacji rekordów w formacie używanym przez serwer BIND:

```
; Example Zone File
$TTL 3600
@       IN      SOA     ns1.example.com. admin.example.com. (
                        2026011801 ; Serial
                        7200       ; Refresh
                        3600       ; Retry
                        1209600    ; Expire
                        86400 )    ; Minimum TTL

; Name Servers
@       IN      NS      ns1.example.com.
@       IN      NS      ns2.example.com.

; A and AAAA Records
@       IN      A       192.0.2.1
@       IN      AAAA    2001:db8::1
web     IN      CNAME   @

; Mail Exchange
@       IN      MX      10 mail.example.com.
@       IN      MX      20 backup-mail.example.com.

; Service Discovery
_sip._tcp IN    SRV     10 60 5060 sipserver.example.com.

; Security (TXT)
@       IN      TXT     "v=spf1 ip4:192.0.2.1 -all"
```

### Mechanizmy TTL i Propagacja

Każdy rekord posiada parametr **TTL (Time To Live)**, określający w sekundach czas, przez który serwery rekurencyjne (np. Google DNS 8.8.8.8) mogą przechowywać rekord w pamięci podręcznej (cache). Niskie wartości TTL (np. 60-300s) są kluczowe podczas migracji, natomiast wysokie (np. 86400s) redukują obciążenie serwerów i przyspieszają rozwiązywanie nazw dla użytkowników końcowych.

Chciałbyś, abym omówił szczegółowo mechanizm działania DNSSEC i sposób, w jaki rekordy RRSIG oraz NSEC zabezpieczają odpowiedzi przed atakami typu Cache Poisoning?