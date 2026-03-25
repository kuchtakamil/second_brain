# Swoją domenę kupiłem na nazwa.pl Skrzynkę email kupiłem na hostinger.com. Teraz

**Data:** 1 załączony plik

---

**User:**

Swoją domenę kupiłem na nazwa.pl
Skrzynkę email kupiłem na hostinger.com. Teraz nie wiem jak ustawić moją skrzynkę.

Dołączam screen zinstrukcji na hostinger.

Teraz wklejam jak wygląda panel konfiguracji na nazwa.pl
###
Parkowanie domeny

Jeżeli nie wiesz jeszcze gdzie chcesz utrzymywać domenę - wybierz tę opcję. Domena zostanie zaparkowana na serwerach DNS nazwa.pl i będzie wskazywała na informacyjną stronę WWW. Przekierowanie na URL ogranicza przekierowanie domeny do wywołań dotyczących WWW (aby w domenie możliwa była również obsługa poczty, konieczne jest przekierowanie jej dodatkowo na pakiet pocztowy lub ustawienie dla niej zaawansowanej konfiguracji DNS). Wpisz adres URL z http:// lub https:// i wybierz typ przekierowania.


Parkowanie domeny
Przekierowanie na adres URL
    
Adres WWW:     
    ramka (FRAME)
    przekierowanie (REDIRECT)
Ustawienia zaawansowane
CAA
CAA określa, które Urzędy Certyfikacji są uprawnione do wydania certyfikatu SSL dla domeny. CAA zmniejsza ryzyko związane z nieuprawnionym wydaniem certyfikatu SSL.

Aktualne ustawienia rekordu CAA:
Nazwa     Typ     Wartość     
kamilkuchta.pl     CAA     0 issue "certum.pl"     
kamilkuchta.pl     CAA     0 issuewild "certum.pl"
kamilkuchta.pl     CAA     0 issue "letsencrypt.org"     
kamilkuchta.pl     CAA     0 issuewild "letsencrypt.org"
+Dodaj kolejny rekord
SPF

SPF zapewnia ochronę przed próbami podszywania się pod nadawców poczty elektronicznej. Jego działanie polega na wskazaniu przez właściciela domeny, z jakich adresów IP w sieci Internet dopuszczalne jest przekazywanie poczty, ze wszystkich kont e-mail w tej domenie. Domyślna konfiguracja pozwala na wysyłanie wiadomości z serwera poczty obsługującego domenę.

Bieżąca konfiguracja:
Nazwa     Typ     Wartość     
kamilkuchta.pl         v=spf1 mx a ~all     

Wprowadź dodatkowe adresy, z których chcesz aby było możliwe wysyłanie poczty.
Nazwa     Typ     Wartość     
+Dodaj kolejny rekord

Wybierz domyślną politykę:
~all - wiadomości od innych serwerów nie spełniających reguły będą odrzucane lub przyjmowane i oznaczane jako spam
-all - wiadomości od innych serwerów nie spełniających reguły będą odrzucane
DKIM

DKIM pozwala na uwierzytelnienie serwera uprawnionego do wysyłki poczty, za pomocą asymetrycznej kryptografii. Serwery przy odbieraniu wiadomości weryfikują sygnaturę zaszyfrowaną przez nadawcę kluczem prywatnym, za pomocą klucza publicznego jaki jest umieszczony w strefie DNS domeny.
Włącz DKIM
Wyłącz DKIM

Bieżąca konfiguracja:
Nazwa     Typ     Wartość     
1757613021.internal._domainkey.kamilkuchta.pl     TXT     
v=DKIM1; k=rsa; p=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA20ZP+03TNdCbnKW7aciVQEnE7J3mskWtzNo6wXMTMUku07DS+6/Jo6jFsGaipAya7u8FYbbEL9jg+COdOI+1QIE8R7xBIwf0l8+nT8sIlZ51sQ2k2KZcqKEAksu95uhhNEShfxbGnBKvBJdl/sXrr8+a/f5823I79sQm7ybBsr6GYRR7EGB9LPeA+qr/zwq8SReoIkIgHOGmiFZxFtjKfOT8TvzGAvIktCaeLAt7qjle1p+fCThiV293YLKoDWdwkuFKgDvG2PWx/pEJQAUJ4MLHeUnKE72GcEwnUmYPbz3nzbGgJ/NmqXludNtqNIi6Ya1WJuhK1TWuocW+POfARQIDAQAB;
    rozwiń
Selektor     Akcje
+Dodaj kolejny rekord DKIM
DMARC

DMARC to mechanizm definiujący w jaki sposób ma się zachować serwer pocztowy, który otrzyma wiadomość negatywnie zweryfikowaną za pomocą zabezpieczeń SPF i DKIM. DMARC umożliwia również otrzymywanie, za pomocą poczty elektronicznej, okresowych raportów o próbach e−mail spoofingu, z serwerów pocztowych na całym świecie, które odnotowały takie naruszenia i obsługują zabezpieczenie DMARC.
Włącz DMARC
Wyłącz DMARC

Bieżąca konfiguracja:
Nazwa
    Typ
    Wartość
_dmarc.kamilkuchta.pl
    TXT
    v=DMARC1; p=quarantine;
Podaj adres e-mail, aby otrzymywać raporty dotyczące prób wysyłki wiadomości w Twojej domenie przez nieautoryzowane serwery pocztowe. Adres skrzynki pocztowej będzie w upublicznionym widoku w konfiguracji strefy DNS domeny.
Adres e-mail: @kamilkuchta.pl
Wybierz politykę działania serwerów odbiorcy, po otrzymaniu nieautoryzowanej wiadomości:
none - nie podejmuj działań
quarantine - traktuj jako podejrzaną
reject - odrzuć wiadomość
Dodatkowy rekord DNS

Dodatkowe rekordy DNS domeny pozwalają np. na zweryfikowanie prawa do domeny (rekord TXT) lub wskazanie numeru portu, na którym działa dana usługa (rekord SRV).
+Dodaj kolejny rekord
Przekierowanie poczty

Jeśli chcesz rozdzielić obsługę poczty i strony WWW dla domeny, możesz przekierować jej rekord MX na pakiet pocztowy. Po przeprowadzeniu tej czynności, konta mailowe zostaną dezaktywowane na serwerze i będą dostępne wyłącznie na wybranym pakiecie pocztowym.
Takie przekierowanie możesz wykonać również w sytuacji, gdy nie masz serwera dla strony WWW i chcesz korzystać wyłącznie z konta pocztowego we własnej domenie.

Przekieruj domenę na pakiet pocztowy
przekieruj na mój pakiet pocztowy
     
przekieruj na pakiet pocztowy w innym Panelu Klienta


Zewnętrzne serwery DNS
Jeżeli posiadasz już własny serwer u innego usługodawcy i chcesz, aby 
zamawiane domeny właśnie tam wskazywały, wybierz tę opcję. W poniższym 
formularzu podaj nazwy serwerów DNS swojego usługodawcy. Pamiętaj, aby 
nowe serwery DNS były skonfigurowane dla tej domeny (domena musi być 
"dopisana" do nowych serwerów DNS).
Uwaga! Zmiana konfiguracji domeny na "Zewnętrzne serwery DNS"
 spowoduje wyłączenie zabezpieczenia DNSSEC, przez co domena będzie 
narażona na ataki cyberprzestępców. Utrzymywanie domeny na serwerach DNS
 nazwa.pl pozwala na korzystanie w pełni z pakietu "bezpieczna domena"!

                        Serwer DNS:
                        Serwer DNS:                       
                        Dodatkowy serwer:
###

---

**Gemini:**

-  [Screenshot from 2026-01-18 11-35-49.png](Screenshot%20from%202026-01-18%2011-35--14a2eb234b5facfb.png)18 sty 2026, 11:38:13 CET

Aby Twoja skrzynka e-mail na Hostingerze zaczęła działać z domeną zarejestrowaną w nazwa.pl, musisz ręcznie zmodyfikować rekordy w sekcji **„Dodatkowy rekord DNS”** oraz zaktualizować rekordy **SPF** i **DKIM**.

Oto precyzyjna instrukcja konfiguracji:

### 1. Konfiguracja rekordów MX (Odbieranie poczty)

Przejdź do sekcji **Dodatkowy rekord DNS** w panelu nazwa.pl i dodaj dwa rekordy MX zgodnie z danymi z Twojego screena:

- **Rekord 1:**
  - **Nazwa:** `@` (lub pozostaw puste, jeśli system na to pozwala)
  - **Typ:** `MX`
  - **Wartość:** `mx1.hostinger.com`
  - **Priorytet:** `5`
- **Rekord 2:**
  - **Nazwa:** `@`
  - **Typ:** `MX`
  - **Wartość:** `mx2.hostinger.com`
  - **Priorytet:** `10`

### 2. Konfiguracja rekordu SPF (Bezpieczeństwo wysyłki)

Obecnie w Twoim panelu widnieje rekord: `v=spf1 mx a ~all`. Musisz go edytować, aby autoryzować serwery Hostingera. W sekcji **SPF** zmień wartość na:

- **Wartość:** `v=spf1 include:_spf.mail.hostinger.com ~all`

Dzięki temu serwery odbiorców (np. Gmail) będą wiedziały, że Hostinger ma prawo wysyłać maile w Twoim imieniu.

### 3. Konfiguracja DKIM i DMARC

To kluczowe kroki, aby Twoje wiadomości nie trafiały do spamu.

- **DKIM:** Musisz pobrać klucz DKIM z panelu Hostinger (zakładka *Emails -> Domain Name -> DNS Checker* lub *Mail Settings*). Będzie to rekord typu **TXT**. W nazwa.pl dodaj go w sekcji **Dodatkowy rekord DNS**.
  - **Nazwa (Host):** Zazwyczaj `hostingermail1._domainkey`
  - **Wartość:** Długi ciąg znaków zaczynający się od `v=DKIM1; k=rsa; ...` (skopiuj go z Hostinger).
  - **Ważne:** Wyłącz obecny rekord DKIM widoczny w panelu nazwa.pl, ponieważ dotyczy on serwerów nazwa.pl, a nie Hostingera.
- **DMARC:** Twój obecny rekord `v=DMARC1; p=quarantine;` jest poprawny, ale upewnij się, że w polu "Adres e-mail" w nazwa.pl wpiszesz swój nowy adres (np. `kontakt@kamilkuchta.pl`), aby otrzymywać raporty o błędach dostarczalności.

---

### 4. Mapowanie na Gmail (Konfiguracja POP3/SMTP)

Gdy rekordy DNS się rozpropagują (może to potrwać do kilku godzin), skonfiguruj Gmaila jako klienta pocztowego:

**A. Pobieranie wiadomości do Gmaila (POP3):**

1. W Gmailu: *Ustawienia -> Zobacz wszystkie ustawienia -> Konta i importowanie -> Sprawdź pocztę na innych kontach -> Dodaj konto pocztowe*.
2. **Nazwa użytkownika:** Pełny adres e-mail (np. `kontakt@kamilkuchta.pl`).
3. **Hasło:** Hasło ustawione w panelu Hostinger.
4. **Serwer POP:** `pop.hostinger.com` | **Port:** `995`.
5. Zaznacz: **Zawsze używaj bezpiecznego połączenia (SSL)**.

**B. Wysyłanie wiadomości z Gmaila (SMTP):**

1. W tej samej zakładce wybierz *Wyślij jako -> Dodaj inny adres e-mail*.
2. **Serwer SMTP:** `smtp.hostinger.com` | **Port:** `465` (SSL) lub `587` (TLS).
3. **Użytkownik i Hasło:** Takie same jak przy POP3.

---

### Tabela parametrów serwerów Hostinger

Jeśli wolisz używać protokołu IMAP (synchronizacja folderów zamiast pobierania wiadomości), użyj tych danych:

| Usługa | Host | Port (SSL) |
| --- | --- | --- |
| **IMAP (Odbieranie)** | `imap.hostinger.com` | `993` |
| **POP3 (Pobieranie)** | `pop.hostinger.com` | `995` |
| **SMTP (Wysyłanie)** | `smtp.hostinger.com` | `465` |

Czy chcesz, abym pomógł Ci sprawdzić, czy wprowadzone rekordy MX są już widoczne w sieci?