# widzę że jest już TXT "v=spf1 mx a ~all". Czy powinienem go usunąć i dodać nowy?

**Data:** 18 sty 2026, 18:56:32 CET

---

**User:**

widzę że jest już TXT "v=spf1 mx a ~all". Czy powinienem go usunąć i dodać nowy?

---

**Gemini:**

Tak, powinieneś zmodyfikować istniejący rekord. **Domena może posiadać tylko jeden rekord SPF.** Posiadanie dwóch osobnych rekordów TXT zaczynających się od `v=spf1` jest błędem składniowym protokołu i spowoduje, że serwery odbiorców (np. Gmail, Outlook) uznają oba za nieważne (status `PermError`), co drastycznie zwiększy szansę na odrzucenie Twoich wiadomości.

Masz dwie opcje, zależnie od tego, czy planujesz wysyłać maile tylko przez Hostinger/Gmail, czy również przez skrypty PHP na serwerze w nazwa.pl (np. formularz kontaktowy na stronie):

### Opcja 1: Pełne zastąpienie (Zalecane)

Jeśli Twoja poczta ma być obsługiwana wyłącznie przez Hostinger (i docelowo zmapowana na Gmail), usuń stary rekord i dodaj nowy.

- **Stara wartość:** `v=spf1 mx a ~all`
- **Nowa wartość:** `v=spf1 include:_spf.mail.hostinger.com ~all`

### Opcja 2: Scalenie rekordów (Hybrid)

Jeśli chcesz zachować możliwość wysyłania maili przez serwer, na którym trzymasz stronę WWW (rekord `a`) oraz przez serwery wskazane w rekordach MX, a jednocześnie dodać autoryzację dla Hostingera, użyj składni łączonej:

- **Wartość scalona:** `v=spf1 mx a include:_spf.mail.hostinger.com ~all`

---

### Dlaczego to jest ważne? (Analiza techniczna)

Mechanizm SPF działa na zasadzie białej listy adresów IP uprawnionych do wysyłania poczty w imieniu Twojej domeny.

- **`mx`**: Pozwala serwerom wskazanym w rekordach MX (teraz to `mx1.hostinger.com`) na wysyłkę.
- **`a`**: Pozwala serwerowi, na który wskazuje rekord A Twojej domeny (zazwyczaj hosting strony WWW), na wysyłkę.
- **`include:_spf.mail.hostinger.com`**: Odwołuje się do dynamicznie aktualizowanej listy adresów IP infrastruktury Hostingera.
- **`~all` (SoftFail)**: Informuje serwer odbiorcy, że jeśli mail pochodzi z innego IP, powinien go przyjąć, ale oznaczyć jako podejrzany (często trafia do spamu).
- **`-all` (Fail)**: Kategorycznie nakazuje odrzucenie wiadomości z nieautoryzowanych źródeł. **Nie ustawiaj `-all`**, dopóki nie będziesz miał 100% pewności, że wszystkie Twoje usługi (mailingi, faktury automatyczne, CRM) są uwzględnione w SPF.

---

### Jak to wprowadzić w panelu nazwa.pl?

1. Jeśli edytujesz to w sekcji **"SPF"** (tam gdzie widziałeś bieżącą konfigurację):
   - Wpisz w pole wartości: `include:_spf.mail.hostinger.com`.
   - System nazwa.pl zazwyczaj sam dodaje `v=spf1` na początku i `~all` na końcu, więc upewnij się, czy nie dublujesz tych fraz.
2. Jeśli edytujesz to w **"Ręczna konfiguracja DNS"**:
   - Znajdź istniejący rekord TXT z `v=spf1`.
   - Zmień jego wartość na tę docelową. **Nie dodawaj drugiego rekordu TXT dla SPF.**

Po zapisaniu zmian możesz sprawdzić poprawność rekordu za pomocą narzędzia `dig`:

```
dig kamilkuchta.pl txt
```

W odpowiedzi powinieneś zobaczyć tylko jeden ciąg zaczynający się od `v=spf1`.

Czy chciałbyś, abym sprawdził teraz, czy Twoje rekordy MX i SPF są już widoczne w globalnej sieci DNS?