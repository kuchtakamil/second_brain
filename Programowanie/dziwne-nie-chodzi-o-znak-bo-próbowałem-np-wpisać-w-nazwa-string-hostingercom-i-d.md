# Dziwne.  Nie chodzi o znak _ bo próbowałem np. wpisać w Nazwa string  "hostinger

**Data:** 18 sty 2026, 19:47:07 CET

---

**User:**

Dziwne.
 Nie chodzi o znak _ bo próbowałem np. wpisać w Nazwa string 
"hostinger.com" i dostaję ten sam błąd. Może typ CNAME wymusza 
konieczność jakieś innej walidacji?

---

**Gemini:**

Błąd „Niedozwolony wpis w nazwie” przy próbie wpisania `hostinger.com` lub `hostingermail-a._domainkey` w polu **Nazwa** najprawdopodobniej wynika z faktu, że panel nazwa.pl w tym konkretnym polu nie akceptuje **kropek**.

W systemach DNS pole „Nazwa” (Host) zazwyczaj oczekuje jedynie **prefiksu** (poddomeny), a nie całej nazwy domeny. System automatycznie „dokleja” Twoją domenę `kamilkuchta.pl` do tego, co wpiszesz.

### 1. Dlaczego wpisanie "hostinger.com" i rekordów z kropkami kończy się błędem?

- **Zasada subdomeny:** Jeśli w polu „Nazwa” wpiszesz `hostinger.com`, system próbuje stworzyć rekord dla adresu `hostinger.com.kamilkuchta.pl`. Ponieważ zawiera on kropkę w środku, walidator nazwa.pl odrzuca go, uznając, że próbujesz wpisać pełny adres (FQDN) w miejscu, gdzie dozwolona jest tylko nazwa hosta.
- **Ograniczenia pola:** Wiele paneli u polskich rejestratorów blokuje znaki specjalne (w tym kropki) w polu hosta, aby zapobiec błędom konfiguracji.

### 2. Jak poprawnie wpisać rekordy DKIM (CNAME) w nazwa.pl?

Aby wprowadzić rekordy z Twojego screena, musisz wpisać **wyłącznie** część znajdującą się przed Twoją domeną.

W sekcji „Dodatkowy rekord DNS” lub „Ręczna konfiguracja DNS” dodaj wpisy według tego schematu:

| Nazwa (Host) | Typ | Wartość (Cel) |
| --- | --- | --- |
| `hostingermail-a._domainkey` | CNAME | `hostingermail-a.dkim.mail.hostinger.com` |
| `hostingermail-b._domainkey` | CNAME | `hostingermail-b.dkim.mail.hostinger.com` |
| `hostingermail-c._domainkey` | CNAME | `hostingermail-c.dkim.mail.hostinger.com` |

**Ważne:** Zwróć uwagę, czy w polu „Wartość” (Cel) na końcu nie jest wymagana kropka. Jeśli po zapisaniu i odświeżeniu strony wartość zmieni się na `hostingermail-a.dkim.mail.hostinger.com.kamilkuchta.pl`, to znaczy, że musisz ją wyedytować i dopisać kropkę na końcu: `hostingermail-a.dkim.mail.hostinger.com.`

---

### 3. Dlaczego nie możesz użyć CNAME dla głównej domeny?

Jeśli próbowałeś wpisać pełną domenę `kamilkuchta.pl` w polu nazwa dla rekordu typu CNAME, system zawsze zwróci błąd. Wynika to z **RFC 1034/1912** (standardy DNS):

- Rekord CNAME **nie może współistnieć** z żadnym innym rekordem dla tej samej nazwy.
- Ponieważ dla głównej domeny (`kamilkuchta.pl`) masz już rekordy **A** (na stronę WWW) oraz **MX** (na pocztę), nie możesz stworzyć dla niej rekordu CNAME.
- CNAME może być używany wyłącznie dla poddomen (np. `www`, `poczta`, `hostingermail-a._domainkey`).

---

### 4. Alternatywa: Konwersja CNAME na TXT

Jeśli panel nazwa.pl kategorycznie odrzuca podkreślnik `_` w rekordzie CNAME (co zdarza się w ich starszych interfejsach), musisz zmienić typ rekordu na **TXT**.

Rekordy DKIM od Hostingera to w rzeczywistości "skróty" (aliasy) do kluczy publicznych. Możesz sprawdzić, co kryje się pod tymi adresami i wpisać to bezpośrednio jako tekst.

**Przykład (jak uzyskać wartość TXT):**
Możesz użyć narzędzia `dig` w terminalu, aby sprawdzić wartość klucza:

```
dig hostingermail-a.dkim.mail.hostinger.com txt
```

W odpowiedzi otrzymasz długi ciąg znaków (np. `v=DKIM1; k=rsa; p=MIIB...`). Ten ciąg możesz wpisać w nazwa.pl jako:

- **Typ:** `TXT`
- **Nazwa:** `hostingermail-a._domainkey`
- **Wartość:** (wklejasz to, co zwrócił `dig`)

---

### Co zrobić teraz?

1. Spróbuj wpisać w polu nazwa dokładnie: `hostingermail-a._domainkey` (bez kropki na końcu i bez nazwy Twojej domeny).
2. Jeśli błąd nadal występuje, oznacza to, że nazwa.pl blokuje znak `_` dla typu CNAME. W takim przypadku najszybszym rozwiązaniem będzie powrót do **Metody 1** (zmiana serwerów DNS na te od Hostingera) – wtedy wszystkie te rekordy zostaną ustawione automatycznie bez walki z panelem nazwa.pl.

Czy chcesz, abym sprawdził dla Ciebie aktualne wartości TXT dla tych rekordów DKIM, abyś mógł je wpisać ręcznie?