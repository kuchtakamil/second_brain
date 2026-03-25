# metoda 1 jest kusząca ale zostawię ją jako ostateczność. Znalazłem miejsce gdzie

**Data:** 1 załączony plik

---

**User:**

metoda 1 jest kusząca ale zostawię ją jako ostateczność.
Znalazłem miejsce gdzie mogę pwisać rekordy MX. Są w "Ręczna konfiguracja DNS".
Hostinger napisał żeby skonfiguraować rekordy tak jak na dołączonym screenie.
Jednak w panelu nazwa.pl w kolumnie Nazwa nie można wisać znaku at (@). Wpisałem tam nazwę domeny czyli kamilkuchta.pl
Co zrobić z rekordem typu TXT gdzie znowu zalecany jest znak at (@) ?

---

**Gemini:**

-  [Screenshot from 2026-01-18 00-13-22.png](Screenshot%20from%202026-01-18%2000-13--3c3dc93896bd5d1a.png)18 sty 2026, 18:42:38 CET

W systemach DNS znak `@` jest skrótem oznaczającym **domenę główną**. Jeśli panel `nazwa.pl` nie akceptuje tego symbolu, wpisanie pełnej nazwy domeny (`kamilkuchta.pl`) jest działaniem całkowicie poprawnym i technicznie równoważnym.

Oto jak dokładnie powinieneś skonfigurować rekordy z Twoich screenów w panelu "Ręczna konfiguracja DNS":

### 1. Rekordy MX (Odbieranie poczty)

Zgodnie z instrukcją Hostingera, wprowadź dwa wpisy:

| Nazwa (Host) | Typ | Wartość (Cel) | Priorytet |
| --- | --- | --- | --- |
| `kamilkuchta.pl` | MX | `mx1.hostinger.com` | 5 |
| `kamilkuchta.pl` | MX | `mx2.hostinger.com` | 10 |

### 2. Rekord TXT (SPF - Autoryzacja nadawcy)

Dla rekordu TXT (SPF) stosujesz tę samą zasadę co przy MX – zamiast `@` używasz pełnej nazwy domeny.

- **Nazwa:** `kamilkuchta.pl`
- **Typ:** `TXT`
- **Wartość:** `v=spf1 include:_spf.mail.hostinger.com ~all`

### 3. Rekordy CNAME (DKIM i Autokonfiguracja)

Tutaj sprawa wygląda inaczej. W kolumnie "Nazwa" wpisujesz tylko **prefiks** (poddomenę) podany przez Hostinger. System DNS automatycznie doklei do nich Twoją domenę.

**Dla DKIM (poprawa dostarczalności):**
Wpisz trzy rekordy CNAME:

1. Nazwa: `hostingermail-a._domainkey` | Wartość: `hostingermail-a.dkim.mail.hostinger.com`
2. Nazwa: `hostingermail-b._domainkey` | Wartość: `hostingermail-b.dkim.mail.hostinger.com`
3. Nazwa: `hostingermail-c._domainkey` | Wartość: `hostingermail-c.dkim.mail.hostinger.com`

**Dla Autokonfiguracji (ułatwia logowanie w apkach):**

1. Nazwa: `autoconfig` | Wartość: `autoconfig.mail.hostinger.com`
2. Nazwa: `autodiscover` | Wartość: `autodiscover.mail.hostinger.com`

---

### Techniczne uwagi dotyczące nazwa.pl

- **Kropka na końcu:** Niektóre zaawansowane panele DNS wymagają postawienia kropki na końcu nazwy domeny w polach wartości (np. `mx1.hostinger.com.`), aby system nie dokleił tam automatycznie Twojej domeny. Jeśli po zapisaniu zobaczysz błąd lub dziwny adres typu `mx1.hostinger.com.kamilkuchta.pl`, dodaj kropkę na końcu wartości.
- **Propagacja:** Zmiany w DNS nie działają natychmiast. Standardowo zajmuje to od 1 do 24 godzin (zależy od parametru TTL).
- **Konflikt rekordów:** Upewnij się, że w sekcji "Ręczna konfiguracja DNS" nie ma innych rekordów typu **MX** ani rekordów **TXT** zaczynających się od `v=spf1`. Jeśli są – usuń stare, aby nie kolidowały z tymi od Hostingera.

### Jak sprawdzić czy poprawnie "zmapowałeś" domenę?

Gdy już zapiszesz te ustawienia w `nazwa.pl`, możesz wrócić do panelu Hostinger. Tam, gdzie masz screeny z instrukcją, powinien znajdować się przycisk **"Verify Records"** lub **"Check DNS"**. Jeśli wszystko wpisałeś poprawnie, status zmieni się na zielony ("Active").

Dopiero gdy status będzie aktywny, będziesz mógł przejść do mapowania skrzynki na Gmaila za pomocą protokołów POP3/SMTP, o których pisałem wcześniej.

Czy chciałbyś, abym po wprowadzeniu przez Ciebie zmian sprawdził zdalnie, czy rekordy MX są już widoczne w sieci?