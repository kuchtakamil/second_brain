# Kolejny problem. Przy wpisaniu hostingermail-a._domainkey pokazuje error "Niedoz

**Data:** 18 sty 2026, 18:59:11 CET

---

**User:**

Kolejny problem. Przy wpisaniu hostingermail-a._domainkey pokazuje error "Niedozwolony wpis w nazwie"

---

**Gemini:**

Błąd „Niedozwolony wpis w nazwie” w panelu **nazwa.pl** wynika najprawdopodobniej z faktu, że ich walidator w polach tekstowych często blokuje znak podkreślenia (`_`) dla rekordów typu **CNAME**, traktując go jako znak niedozwolony w standardowych nazwach hostów (mimo że jest on wymagany w protokole DKIM).

Oto jak możesz to obejść lub naprawić:

### 1. Spróbuj użyć pełnej nazwy domeny

W niektórych wersjach panelu nazwa.pl, wpisanie samego prefiksu z podkreśleniem powoduje błąd. Spróbuj wpisać w polu „Nazwa” pełny adres zakończony kropką:

- **Nazwa:** `hostingermail-a._domainkey.kamilkuchta.pl.`
- *(Kropka na końcu jest kluczowa – informuje serwer, że to pełna ścieżka).*

### 2. Wykorzystaj dedykowaną sekcję DKIM w nazwa.pl

Na liście, którą wkleiłeś wcześniej, widnieje sekcja **DKIM** z przyciskiem **+Dodaj kolejny rekord DKIM**.

1. Kliknij ten przycisk.
2. W polu **Selektor** wpisz: `hostingermail-a` (lub `hostingermail-a._domainkey` – sprawdź, co przyjmie formularz).
3. Jako **Typ** wybierz **CNAME** (jeśli panel na to pozwala w tej sekcji).
4. Wklej wartość od Hostingera.

### 3. Dlaczego to jest problemem w nazwa.pl?

Nazwa.pl posiada bardzo sztywne reguły walidacji rekordów w "podstawowym" widoku. Jeśli powyższe metody zawiodą, masz dwa wyjścia techniczne:

- **Obejście przez TXT (jeśli Hostinger na to pozwoli):** Rekordy DKIM typu CNAME to tak naprawdę „wskaźniki” na inny rekord TXT. Jeśli panel nazwa.pl kategorycznie odmawia przyjęcia podkreślenia w CNAME, zazwyczaj pozwala na nie w rekordach typu **TXT**.

  - *Problem:* Hostinger nie podaje bezpośredniej wartości TXT w Twoim screenie, tylko CNAME. Aby uzyskać wartość TXT, musiałbyś „odpytać” serwer `hostingermail-a.dkim.mail.hostinger.com` o jego rekord TXT.
- **Powrót do Metody 1 (Zmiana serwerów DNS):** To jest moment, w którym zmiana serwerów DNS na te od Hostingera (`ns1.dns-parking.com`, `ns2.dns-parking.com`) staje się najbardziej racjonalnym rozwiązaniem.

  - **Zaleta:** W panelu Hostinger te rekordy (z podkreśleniami) pojawią się **automatycznie** jednym kliknięciem.
  - **Bezpieczeństwo:** Nie tracisz własności domeny, nadal opłacasz ją w nazwa.pl, jedynie „mózg” kierujący ruchem (DNS) przenosi się do Hostingera.

---

### Co z mapowaniem na Gmail?

Nawet jeśli teraz pominiesz rekordy DKIM (te z błędem), Twoja poczta **będzie działać**, ale może mieć problem z „wiarygodnością” (niektóre maile mogą trafiać do spamu).

Możesz kontynuować konfigurację w Gmailu:

1. W Gmailu dodaj konto przez **POP3** (pobieranie).
2. Dodaj konto przez **SMTP** (wysyłanie).

**Dane do wpisania w Gmailu (zgodnie z Hostinger):**

- **SMTP Server:** `smtp.hostinger.com`
- **Port:** `465` (z SSL)
- **POP3 Server:** `pop.hostinger.com`
- **Port:** `995` (z SSL)

### Rekomendacja na ten moment:

Jeśli nazwa.pl nadal blokuje rekord `_domainkey` w sekcji CNAME:

1. Skonfiguruj rekordy **MX** oraz **SPF** (te już masz i one działają bez podkreśleń).
2. Sprawdź w panelu Hostinger, czy po kilku godzinach „zapaliły się na zielono”.
3. Jeśli tak – Twoja poczta już działa. Rekordami DKIM (tymi z błędem) zajmiemy się w drugiej kolejności (możesz je dodać później dla poprawy bezpieczeństwa).

Czy chcesz, abym pomógł Ci sprawdzić, co dokładnie Hostinger widzi pod tymi adresami CNAME, abyś mógł spróbować wpisać je jako rekordy TXT (co nazwa.pl powinna przyjąć)?