# Znalazłem taki screen w konfiguracji routera UPC. Jak myślisz, czy to jest miejs

**Data:** 1 załączony plik

---

**User:**

Znalazłem taki screen w konfiguracji routera UPC. Jak myślisz, czy to jest miejsce gdzie można przełączyć w tryb mostu?

---

**Gemini:**

-  [Screenshot from 2025-12-30 16-08-40.png](Screenshot%20from%202025-12-30%2016-08--ed878db5a76d31cf.png)30 gru 2025, 16:09:36 CET

Niestety, **nie**. To menu nie służy do włączenia trybu Bridge (Mostu).

To, co widzisz na ekranie, to specyficzne ustawienie dekodera Horizon, które decyduje o tym, jak **on sam** uczestniczy w sieci domowej, a nie jak przekazuje Internet dalej.

Oto techniczne wyjaśnienie opcji ze zrzutu ekranu:

1. **"Użyj sieci bezprzewodowej z Horizon"** (zaznaczone): To standardowy tryb routera. Horizon tworzy sieć WiFi i działa jako brama (Gateway).
2. **"Chcę się podłączyć do sieci domowej"**: Ta opcja zmienia Horizona w tzw. **klienta sieci**. Służy to temu, aby dekoder podłączył się do *innego* istniejącego routera (np. żeby pobierać pliki multimedialne z domowego serwera DLNA). Włączenie tego **nie zrobi z niego przezroczystego modemu**, a może wręcz odciąć Ci dostęp do Internetu, jeśli nie masz drugiego działającego routera z wyjściem na świat.

### Diagnoza sytuacji (Horizon Box)

Urządzenie, które posiadasz (dekoder Horizon z wbudowanym modemem), jest w środowisku sieciowców znane z tego, że **zazwyczaj nie posiada w ogóle opcji trybu Bridge**. Operatorzy blokują tę funkcję w tych konkretnych urządzeniach, ponieważ są one zintegrowane z usługą telewizyjną i telefonem VoIP.

### Co musisz zrobić (Rozmowa z Operatorem)

Skoro planujesz zakup własnego, mocnego routera i zabawę z VPN, **musisz pozbyć się Internetu z dekodera Horizon**.

Twoja ścieżka działania wygląda tak:

1. **Kontakt z Play/UPC:** Zadzwoń na infolinię techniczną.
2. **Argumentacja:** Powiedz: *"Chcę rozdzielić usługę telewizji od Internetu. Mój obecny dekoder Horizon nie pozwala mi na konfigurację własnej sieci (brak trybu Bridge). Proszę o przysłanie osobnego modemu (np. Connect Box) do obsługi Internetu, a Horizon ma zostać tylko do telewizji".*
3. **Koszty:** Zazwyczaj jest to bezpłatne lub kosztuje jednorazową opłatę aktywacyjną, ale technicznie jest to **konieczne** dla Twoich potrzeb.
4. **Po wymianie:** Gdy dostaniesz **Connect Boxa** (lub Giga Connect Boxa), w nim bez problemu włączysz tryb Bridge (po uprzednim poproszeniu o IPv4, o czym pisałem wcześniej).

### Plan B: Jeśli nie wymienią sprzętu (Scenariusz DMZ)

Jeśli operator odmówi wymiany urządzenia i zostaniesz z Horizonem:

1. Zostawiasz opcję ze screena na **"Użyj sieci bezprzewodowej z Horizon"**.
2. Podłączasz swój nowy router kablem do Horizona.
3. W panelu Horizona wyłączasz całkowicie jego WiFi (żeby nie siało zakłóceń).
4. Szukasz w menu Horizona zakładki **DMZ** i wpisujesz tam adres IP, który Horizon przydzielił Twojemu nowemu routerowi.

To jedyne wyjście na tym sprzęcie, ale **wymiana na osobny modem to priorytet**, jeśli zależy Ci na stabilnym VPN i niskich opóźnieniach.

Czy chcesz, abym przygotował Ci listę argumentów technicznych dla konsultanta, gdyby twierdził, że "nie da się" wymienić modemu?