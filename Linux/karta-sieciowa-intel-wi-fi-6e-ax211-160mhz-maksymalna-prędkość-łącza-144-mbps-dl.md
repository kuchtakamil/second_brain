# Karta sieciowa:  Intel Wi-Fi 6E AX211 160MHz Maksymalna prędkość łącza: 144 Mbps

**Data:** 22 sty 2026, 10:02:43 CET

---

**User:**

Karta sieciowa:  Intel Wi-Fi 6E AX211 160MHz
Maksymalna prędkość łącza: 144 Mbps
Dlaczego max prędkość jest tak niska?

---

**Gemini:**

Wartość **144 Mbps** (dokładnie 144,4 Mbps) jest parametrem charakterystycznym dla standardu **802.11n (Wi-Fi 4)** przy wykorzystaniu dwóch strumieni przestrzennych (2x2 MIMO) oraz szerokości kanału **20 MHz**.

Oto szczegółowa analiza techniczna przyczyn ograniczenia wydajności karty Intel AX211:

### 1. Praca w paśmie 2.4 GHz zamiast 5 GHz lub 6 GHz

Intel AX211 to karta Wi-Fi 6E, która potrafi osiągać prędkości rzędu 2.4 Gbps, ale tylko przy modulacji 1024-QAM i kanale 160 MHz. Prędkość 144 Mbps sugeruje, że karta zestawiła połączenie w paśmie **2.4 GHz**.

- W paśmie 2.4 GHz domyślna szerokość kanału to zazwyczaj 20 MHz, co przy standardzie 802.11n i 2 strumieniach daje właśnie 144.4 Mbps.
- Nawet jeśli router obsługuje Wi-Fi 6 (802.11ax) w paśmie 2.4 GHz, przy szerokości 20 MHz prędkość PHY wyniosłaby około 286 Mbps. Wynik 144 Mbps jednoznacznie wskazuje na fallback do starszego protokołu lub ograniczenia szerokości pasma.

### 2. Konfiguracja szerokości kanału (Channel Width)

Karta AX211 wspiera kanały **160 MHz**, które są kluczowe dla wysokich transferów. Jeśli w ustawieniach routera lub sterownika szerokość kanału jest ustawiona na "Auto" lub sztywno na "20 MHz", prędkość zostanie drastycznie ograniczona.

- **Weryfikacja w systemie Windows:**
  1. Menedżer Urządzeń -> Karty sieciowe -> Intel(R) Wi-Fi 6E AX211.
  2. Właściwości -> Zaawansowane.
  3. Sprawdź ustawienia: `802.11n/ac/ax Wireless Mode` (powinno być 802.11ax) oraz `Channel Width for 5GHz` (ustaw na Auto lub 160MHz).

### 3. Tabela MCS (Modulation and Coding Scheme)

Link speed 144 Mbps odpowiada konkretnemu indeksowi **MCS 15** w standardzie 802.11n. Oznacza to, że system używa modulacji **64-QAM** przy Guard Interval (GI) o długości 400ns.

| Standard | Strumienie (MIMO) | Szerokość kanału | Modulacja | Max Rate (PHY) |
| --- | --- | --- | --- | --- |
| **802.11n** | **2x2** | **20 MHz** | **64-QAM** | **144.4 Mbps** |
| 802.11ac | 2x2 | 80 MHz | 256-QAM | 866.7 Mbps |
| 802.11ax | 2x2 | 160 MHz | 1024-QAM | 2402 Mbps |

### 4. Standard zabezpieczeń (Encryption Bottleneck)

Karty Intel Wi-Fi 6/6E wymagają nowoczesnych metod szyfrowania do pracy z pełną prędkością. Jeśli router używa **WPA2-TKIP** lub szyfrowania **WEP**, prędkość połączenia zostanie ograniczona do standardu 802.11g (54 Mbps) lub podstawowego 802.11n (właśnie okolice 144 Mbps), ponieważ sprzętowa akceleracja szyfrowania AES nie jest wtedy w pełni wykorzystywana.

- **Rozwiązanie:** Zmień szyfrowanie w routerze na **WPA2-AES (CCMP)** lub **WPA3-SAE**.

### 5. Mechanizm Power Management i MIMO Power Save Mode

W ustawieniach zaawansowanych sterownika karty Intel AX211 znajduje się funkcja `MIMO Power Save Mode`.

- Jeśli jest ustawiona na **Spatial Multiplexing Power Save (SMPS)** w trybie agresywnym, karta może wyłączać jeden z łańcuchów odbiorczych (radio chains), co redukuje połączenie z 2x2 do 1x1, tnąc prędkość o połowę.
- Ustaw tę wartość na **Disabled** lub **No SMPS**.

---

### Diagnostyka krok po kroku

Aby zdiagnozować dokładną przyczynę, wykonaj w terminalu (PowerShell/CMD) komendę:

```
netsh wlan show interfaces
```

Zwróć uwagę na pola:

- **Radio type:** Jeśli widzisz `802.11n`, router lub karta wymusza stary standard.
- **Band:** Jeśli widnieje `2.4 GHz`, to jest główny powód niskiego link rate.
- **Receive / Transmit rate:** Czy są symetryczne?

Czy chciałbyś, abym pomógł Ci skonfigurować konkretne parametry w sterowniku karty Intel AX211 dla uzyskania maksymalnej przepustowości w paśmie 5/6 GHz?