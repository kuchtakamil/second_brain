# Mam internet z kablówki Play dawne UPC a mój obecny router to czarna skrzynka od

**Data:** 10 gru 2025, 12:31:52 CET

---

**User:**

Mam internet z kablówki Play dawne UPC a mój obecny router to czarna skrzynka od UPC, nazywana chyba Horizon Go. 
Chcę dokupić swój mocniejszy zasięgiem router aby polepszyć zasięg wifi. Chcę połączyć nowy i stary router kablem LAN.
Chciałbym żeby router miał możliwość uruchomienia VPN i może innych usług o których teraz nie wiem a które mogą mi się przydać. Czego w odniesieniu do technicznych aspektów powinienem się dowiedzieć od operatora zanim kupię router.

---

**Gemini:**

Aby zbudować wydajną sieć z własnym routerem i serwerem VPN, musisz wyeliminować ograniczenia narzucane przez sprzęt operatora. W infrastrukturze Play/UPC kluczowe są kwestie trybu pracy modemu oraz adresacji IP.

Oto lista konkretnych, technicznych pytań i zagadnień, które musisz poruszyć z operatorem:

### 1. Możliwość przełączenia urządzenia w tryb Bridge (Tryb Mostu)

To absolutnie najważniejsza kwestia. Obecny "czarny router" (prawdopodobnie Horizon Recorder lub Connect Box) domyślnie działa jako router (NAT).

- **Pytanie do operatora:** "Czy na moim obecnym urządzeniu mogę włączyć tryb Bridge (Bridge Mode)?"
- **Dlaczego to ważne:**
  - W trybie Bridge urządzenie operatora staje się "przezroczystym" modemem. Cały ruch trafia bezpośrednio na port WAN Twojego nowego routera.
  - Unikasz problemu **Double NAT** (podwójnego NAT-owania), który jest zabójczy dla VPN, gier online i przekierowywania portów.
  - Twój nowy router otrzymuje publiczny adres IP bezpośrednio na interfejsie WAN.

### 2. Protokół IP: IPv4 vs IPv6 (DS-Lite / CGNAT)

Play/UPC często wdraża protokół IPv6 z mechanizmem **DS-Lite**. W tej konfiguracji nie posiadasz publicznego adresu IPv4, lecz dzielisz go z innymi użytkownikami (CGNAT – Carrier Grade NAT).

- **Pytanie do operatora:** "Czy moje łącze jest na pełnym, publicznym adresie IPv4, czy na IPv6 z DS-Lite? Jeśli mam DS-Lite, czy możecie przełączyć mnie na pełne IPv4?"
- **Dlaczego to ważne dla VPN:**
  - Jeśli chcesz postawić serwer VPN (np. WireGuard lub OpenVPN) na swoim routerze, aby łączyć się *do domu* z zewnątrz, **musisz mieć publiczny adres IPv4**.
  - Przy DS-Lite jest to niemożliwe bez stosowania zewnętrznych serwerów relay (np. Tailscale, ZeroTier), co komplikuje konfigurację i może spowalniać transfer.
  - Przełączenie na IPv4 jest zazwyczaj wymagane, aby opcja "Tryb Bridge" w ogóle pojawiła się w panelu urządzenia operatora.

### 3. Rodzaj urządzenia (Horizon vs Connect Box)

Wspomniałeś o "Horizon Go" (to nazwa usługi/aplikacji), ale urządzenie to prawdopodobnie **Dekoder Horizon z wbudowanym routerem**.

- **Problem:** Stare dekodery Horizon często miały zablokowaną możliwość pracy w trybie Bridge oraz bardzo słabą wydajność sieciową (częste zrywanie połączeń, wysokie opóźnienia).
- **Żądanie do operatora:** Jeśli posiadasz dekoder Horizon obsługujący internet, zażądaj wymiany na oddzielny modem (np. **Connect Box** lub **Giga Connect Box**), zachowując Horizon tylko do TV.
- **Uzasadnienie:** Oddzielny modem jest znacznie bardziej stabilny i zazwyczaj bezproblemowo obsługuje tryb Bridge po zmianie na IPv4.

---

### Czego szukać w nowym routerze (Advanced Features)

Skoro interesują Cię zaawansowane usługi i VPN, Twój nowy router powinien spełniać poniższe kryteria techniczne:

1. **Wsparcie dla WireGuard:**
   - WireGuard jest znacznie szybszy i lżejszy dla procesora routera niż OpenVPN (nawet 5-10x wyższa przepustowość na tym samym sprzęcie). Szukaj routera z natywną obsługą serwera i klienta WireGuard.
2. **Oprogramowanie (Firmware):**
   - Szukaj sprzętu, który wspiera alternatywne oprogramowanie, takie jak **OpenWrt**, **Asuswrt-Merlin** lub **PfSense/OPNsense** (jeśli budujesz router na platformie x86).
   - Daje to pełną kontrolę nad firewallem, VLAN-ami (izolacja sieci gościnnej lub IoT) oraz umożliwia instalację dodatkowych pakietów.
3. **Hardware Offloading & AES-NI:**
   - Procesor routera musi wspierać akcelerację sprzętową szyfrowania, aby VPN nie "dławił" łącza.
4. **Konteneryzacja / Docker (opcjonalnie):**
   - Niektóre routery (np. wyższe modele MikroTik, QNAP, czy sprzęt na OpenWrt) pozwalają na uruchamianie kontenerów. Możesz wtedy uruchomić na routerze:
     - **Pi-hole / AdGuard Home:** Blokowanie reklam w całej sieci domowej na poziomie DNS.
     - **Home Assistant:** Do automatyki domowej.

### Sugerowane ścieżki sprzętowe:

- **Dla entuzjasty (Consumer High-End):** ASUS (modele RT-AX86U Pro lub GT-AX6000) – koniecznie z wgranym softem **Asuswrt-Merlin**. Łatwy w obsłudze, świetny zasięg, natywny WireGuard, skrypty blokujące reklamy.
- **Dla zaawansowanego (Prosumer):** Ubiquiti UniFi (Dream Router / Dream Machine) – wymaga wejścia w ekosystem UniFi, świetne zarządzanie VLAN-ami i interfejs.
- **Dla eksperta sieciowego:** MikroTik (np. RB5009) – ogromne możliwości, ale bardzo stroma krzywa uczenia się (RouterOS). Pełna kontrola nad każdym pakietem.
- **Open Source:** Urządzenia **GL.iNet** (np. Flint 2) – fabrycznie preinstalowany OpenWrt z nakładką producenta. Bardzo mocne wsparcie dla VPN i AdGuard Home "out of the box".

### Next Step

Would you like me to recommend specific router models based on your budget and technical expertise level, or explain how to configure WireGuard once you have the equipment?