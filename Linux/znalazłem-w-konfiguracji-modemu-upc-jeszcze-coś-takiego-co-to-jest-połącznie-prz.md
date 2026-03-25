# Znalazłem w konfiguracji modemu UPC jeszcze coś takiego, co to jest? "Połącznie

**Data:** 30 gru 2025, 16:45:58 CET

---

**User:**

Znalazłem w konfiguracji modemu UPC jeszcze coś takiego, co to jest?
"Połącznie przez zewnętrzny modem. Dostęp do internetu zapewnia aktualnie modem w dekoderze. Naciśnij OK aby połączyć się z zewnętrznym modemem"

---

**Gemini:**

To nie jest Tryb Mostu (Bridge Mode), którego szukasz. To funkcja działająca dokładnie odwrotnie.

Opcja **„Połączenie przez zewnętrzny modem”** służy do sytuacji, w której masz już w domu inny, główny modem (np. Connect Box, o który sugerowałem poprosić), a dekoder Horizon chcesz zdegradować jedynie do roli „klienta” lub dodatkowego punktu WiFi.

Oto co dokładnie się stanie, jeśli to włączysz, a co to oznacza dla Twoich planów:

### Co to robi?

- **Zmienia źródło Internetu:** Mówisz dekoderowi: *„Przestań brać Internet z kabla koncentrycznego w ścianie. Zacznij brać Internet kablem LAN z innego routera”*.
- **Rola urządzenia:** Horizon przestaje być bramą do Internetu. Staje się zwykłym urządzeniem w sieci (jak komputer czy konsola), które ewentualnie może też rozsyłać WiFi (działać jako Access Point).

### Dlaczego to NIE jest Tryb Bridge?

- **W Trybie Bridge:** Urządzenie bierze Internet ze ściany i przekazuje go „surowego” (publiczne IP) kablem LAN do Twojego routera.
- **W tej opcji:** Urządzenie oczekuje, że to ono dostanie Internet kablem LAN **od kogoś innego**.

### Ostrzeżenie

Jeśli wybierzesz tę opcję teraz, mając tylko ten jeden dekoder podłączony do kabla koncentrycznego, **najprawdopodobniej odetniesz sobie Internet**, ponieważ Horizon przestanie używać swojego wbudowanego modemu do łączenia się z siecią operatora, a zacznie szukać Internetu w gnieździe LAN (do którego nic nie dostarcza sygnału).

### Wniosek: To potwierdza moją wcześniejszą radę

Ta opcja w menu jest dowodem na to, że ten sprzęt jest przewidziany do pracy w parze z **osobnym modemem**.
Idealna konfiguracja, do której dążysz, wygląda tak:

1. **Nowy modem od Play (np. Connect Box):** Odbiera Internet, działa w trybie Bridge, wysyła sygnał do Twojego routera.
2. **Twój nowy router:** Zarządza siecią, VPN-em i WiFi.
3. **Stary Horizon:** Podłączasz go kablem do swojego routera i włączasz właśnie tę opcję **„Połączenie przez zewnętrzny modem”**. Dzięki temu Horizon ma Internet do obsługi VOD/aplikacji, ale nie miesza w Twojej sieci.

**Rekomendacja:** Nie klikaj „OK”, dopóki nie dostaniesz od operatora oddzielnego modemu.