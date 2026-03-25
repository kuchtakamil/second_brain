# Co oznacza xDSL w opisie routera wifi?

**Data:** 14 sty 2026, 20:23:23 CET

---

**User:**

Co oznacza xDSL w opisie routera wifi?

---

**Gemini:**

Oznaczenie **xDSL** w opisie routera występuje w dwóch kontekstach: technicznym (jako rodzina technologii) oraz handlowym (często spotykanym w polskich sklepach i u dostawców).

### 1. Definicja techniczna: Rodzina technologii DSL

Technicznie **xDSL** (x Digital Subscriber Line) to zbiorcza nazwa technologii umożliwiających szerokopasmowy przesył danych przez miedziane pary przewodów telefonicznych. Litera „x” jest symbolem zastępczym dla konkretnych wariantów standardu:

- **ADSL/ADSL2+ (Asymmetric DSL):** Najpopularniejsza technologia asymetryczna (prędkość pobierania znacznie wyższa od wysyłania). Pracuje na częstotliwościach do 2.2 MHz (Annex A dla linii analogowych POTS, Annex B dla ISDN). Maksymalna przepustowość to ok. 24 Mbps (down) / 3.5 Mbps (up).
- **VDSL/VDSL2 (Very-high-bit-rate DSL):** Rozwinięcie ADSL wykorzystujące szersze pasmo (do 17 MHz lub 30 MHz w profilach 17a/30a). Pozwala na prędkości rzędu 100-200 Mbps na krótkich dystansach (do 300-500m od szafy dostępowej DSLAM).
- **SDSL (Symmetric DSL):** Wariant symetryczny, gdzie upload i download są identyczne, stosowany głównie w sektorze biznesowym.
- **G.fast:** Najnowszy standard xDSL (G.9701), wykorzystujący pasmo do 212 MHz, co pozwala na osiągnięcie prędkości zbliżonych do 1 Gbps na bardzo krótkich odcinkach miedzianych (ostatnie metry od światłowodu).

### 2. Rozróżnienie rynkowe: "Router xDSL" vs "Router ADSL"

W nomenklaturze sklepów internetowych i operatorów (np. Orange, Netia) przyjęło się specyficzne rozróżnienie, które technicznie jest pewnym uproszczeniem, ale kluczowym przy zakupie:

- **Router ADSL/VDSL:** Urządzenie posiada **wbudowany modem**. Gniazdo wejściowe (WAN) to zazwyczaj **RJ-11** (wąskie gniazdo telefoniczne). Podłączasz je bezpośrednio do gniazdka telefonicznego w ścianie.
- **Router xDSL (w rozumieniu handlowym):** Urządzenie **nie posiada modemu**. Zamiast tego posiada port WAN w standardzie **RJ-45** (Ethernet). Służy do podłączenia sygnału z zewnętrznego modemu, terminala ONT (światłowód), modemu kablowego (DOCSIS) lub innej sieci osiedlowej.

### 3. Kluczowe aspekty techniczne (Advanced)

Przy wyborze routera wspierającego technologie DSL (z modemem), należy zwrócić uwagę na parametry warstwy fizycznej:

#### Modulacja i technologia Vectoring (G.993.5)

VDSL2 Vectoring to technologia redukcji przesłuchów (**FEXT - Far-End Crosstalk**) pomiędzy parami przewodów w tej samej wiązce kablowej. Działa na zasadzie zbliżonej do aktywnej redukcji szumów w słuchawkach. Jeśli operator wspiera Vectoring, router musi go obsługiwać sprzętowo, aby osiągnąć prędkości powyżej 50-80 Mbps.

#### Profile VDSL2

Urządzenia xDSL różnią się obsługiwanymi profilami, które determinują maksymalną moc sygnału i pasmo:

- **Profil 8b, 12a:** Podstawowe, mniejsza przepustowość.
- **Profil 17a:** Standard dla ofert 100 Mbps.
- **Profil 30a / 35b (Supervectoring):** Niezbędny dla prędkości rzędu 250-300 Mbps (Vplus).

#### Obsługa Annexów

Standardy xDSL definiują podział pasma między telefon (głos) a dane:

- **Annex A:** Dane przesyłane nad pasmem analogowej telefonii (POTS). Najczęstszy w Polsce.
- **Annex B:** Dane przesyłane nad pasmem cyfrowym ISDN (często spotykane w urządzeniach z rynku niemieckiego).
- **Annex J / M:** Rozszerzają pasmo wysyłania (upload) kosztem pasma głosowego lub downloadu.

### Porównanie interfejsów

| Cecha | Router z modemem (ADSL/VDSL) | Router "xDSL" (Ethernet WAN) |
| --- | --- | --- |
| **Gniazdo WAN** | RJ-11 (4/6 pin) | RJ-45 (8 pin) |
| **Medium wejściowe** | Miedziana linia telefoniczna | Skrętka komputerowa / Światłowód (przez ONT) |
| **Zadanie urządzenia** | Modulacja/Demodulacja + Routing | Wyłącznie Routing i obsługa sesji (np. PPPoE) |
| **Przykładowe użycie** | Neostrada (stary typ), Netia na linii miedzianej | FTTH (Światłowód), Kablówka, Starlink |

Chcesz, abym przeanalizował specyfikację konkretnego modelu routera pod kątem obsługi standardów VDSL2 Vectoring lub profilu 35b?