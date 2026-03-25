# Odnośnie "Konfiguracja rekordów MX" w "Dodatkowy rekord DNS" to dostępne są typy

**Data:** 18 sty 2026, 14:05:53 CET

---

**User:**

Odnośnie "Konfiguracja rekordów MX" w "Dodatkowy rekord DNS" to dostępne są typy: TXT, SRV,CNAME,AAAA,A. Nie ma MX

---

**Gemini:**

W panelu **nazwa.pl** rekordy MX są traktowane jako rekordy główne, dlatego nie znajdziesz ich na liście "Dodatkowych rekordów DNS" (tam są tylko rekordy uzupełniające, takie jak TXT czy CNAME).

W tej sytuacji masz dwie drogi. Rekomenduję **Metodę 1**, ponieważ jest znacznie prostsza i automatyzuje konfigurację SPF/DKIM/MX po stronie Hostingera.

---

### Metoda 1: Zmiana serwerów DNS na Hostinger (Zalecane)

Zamiast ręcznie wpisywać każdy rekord w nazwa.pl, możesz przekazać całe zarządzanie strefą DNS do Hostingera. Dzięki temu Hostinger sam ustawi poprawne MX, SPF i DKIM.

1. W panelu nazwa.pl przejdź do sekcji **Zewnętrzne serwery DNS** (widocznej na dole Twojego opisu).
2. W polach "Serwer DNS" wpisz adresy serwerów Hostingera:
   - `ns1.dns-parking.com`
   - `ns2.dns-parking.com`
3. Zatwierdź zmiany.

**Co to zmieni?**

- Od teraz rekordy DNS będziesz edytować tylko w panelu Hostinger.
- Wszystkie rekordy pocztowe (MX, SPF, DKIM) zostaną tam skonfigurowane automatycznie.
- **Uwaga:** Jeśli masz już stronę WWW na innym serwerze niż Hostinger, będziesz musiał w panelu Hostingera dodać rekord `A` wskazujący na IP Twojej strony.

---

### Metoda 2: Ręczna edycja MX w nazwa.pl

Jeśli chcesz zostać przy serwerach DNS nazwa.pl, musisz znaleźć sekcję dedykowaną wyłącznie dla poczty.

1. Spójrz na sekcję **Przekierowanie poczty** w panelu nazwa.pl.
2. W interfejsie nazwa.pl, aby wpisać własne serwery MX (te od Hostingera), zazwyczaj należy wybrać opcję **"Zewnętrzny serwer poczty"** lub **"Własna konfiguracja"**.
3. Jeśli po wybraniu opcji "Przekieruj domenę na pakiet pocztowy" widnieją tylko usługi nazwa.pl, oznacza to, że musisz przełączyć widok panelu na **"Zaawansowana konfiguracja DNS"** (często dostępna jako osobna zakładka lub przycisk przy liście domen).

**Dlaczego nie ma MX w "Dodatkowych"?**
Systemy takie jak nazwa.pl separują rekordy MX, aby użytkownicy przypadkiem ich nie usunęli, co skutkowałoby natychmiastowym przerwaniem odbierania poczty. Jeśli panel nie pozwala na wpisanie `mx1.hostinger.com` w dedykowanej sekcji poczty, jedynym wyjściem jest **Metoda 1**.

---

### Jak sprawdzić, czy dane już działają?

Po wprowadzeniu zmian (niezależnie od metody), możesz zweryfikować poprawność konfiguracji w terminalu lub narzędziach webowych.

**Sprawdzenie rekordów MX (Linux/macOS/Windows):**

```
nslookup -q=mx kamilkuchta.pl
```

Lub użyj narzędzia online: [Google Admin Toolbox Dig](https://www.google.com/search?q=https://toolbox.googleapps.com/apps/dig/%23MX/).

---

### Co z mapowaniem na Gmail?

Gdy już poprawnie ustawisz rekordy MX (tak aby poczta trafiała na serwery Hostinger), możesz wrócić do konfiguracji Gmaila (POP3/SMTP), o której pisałem wcześniej.

W Gmailu jako **Serwer SMTP/POP3** używaj adresów:

- `smtp.hostinger.com`
- `pop.hostinger.com`

Czy chciałbyś, abym pomógł Ci teraz zweryfikować rekordy DKIM po stronie Hostingera, abyś mógł je dodać jako rekord TXT w nazwa.pl?