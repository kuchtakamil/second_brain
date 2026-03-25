# dla 802.11n w 5GHz prędkość byłaby wyższa?

**Data:** 22 sty 2026, 10:10:57 CET

---

**User:**

dla 802.11n w 5GHz prędkość byłaby wyższa?

---

**Gemini:**

Tak, przy standardzie **802.11n (Wi-Fi 4)** w paśmie **5 GHz** prędkość zestawionego łącza (Link Speed) byłaby wyższa, osiągając zazwyczaj **300 Mbps**.

Wynika to bezpośrednio z możliwości wykorzystania szerszego kanału radiowego, co w paśmie 2.4 GHz jest technicznie utrudnione.

### Dlaczego 5 GHz jest szybsze dla 802.11n?

Głównym czynnikiem jest **szerokość kanału (Channel Width)**. Prędkość 144 Mbps, którą obecnie widzisz, to limit dla kanału 20 MHz przy dwóch strumieniach danych (2x2 MIMO).

1. **Zatłoczenie pasma 2.4 GHz:** W tym paśmie dostępne są tylko trzy nienachodzące na siebie kanały 20 MHz (1, 6, 11). Próba wymuszenia kanału 40 MHz (co pozwoliłoby na 300 Mbps) w 2.4 GHz zazwyczaj kończy się niepowodzeniem, ponieważ mechanizmy *Coexistence* wykrywają inne sieci i automatycznie degradują szerokość do 20 MHz, aby uniknąć kolizji.
2. **Pojemność pasma 5 GHz:** To pasmo jest znacznie szersze i mniej zatłoczone. Pozwala na swobodne stosowanie kanałów **40 MHz** dla standardu 802.11n bez zakłócania sąsiednich sieci.

---

### Porównanie teoretycznych prędkości PHY dla 802.11n (2x2 MIMO)

Poniższa tabela przedstawia różnice w prędkościach w zależności od konfiguracji pasma:

| Pasmo | Szerokość kanału | Modulacja | Max Link Speed (PHY) |
| --- | --- | --- | --- |
| **2.4 GHz** | 20 MHz | 64-QAM | **144.4 Mbps** |
| **2.4 GHz** | 40 MHz | 64-QAM | 300 Mbps (rzadko osiągalne) |
| **5 GHz** | 20 MHz | 64-QAM | 144.4 Mbps |
| **5 GHz** | **40 MHz** | 64-QAM | **300 Mbps** |

### Dlaczego AX211 nadal pracuje w standardzie "n"?

Twoja karta **Intel AX211** to jednostka klasy Wi-Fi 6E, która jest w stanie obsługiwać prędkości do **2402 Mbps**. Jeśli widzisz ograniczenia standardu 802.11n (Wi-Fi 4), oznacza to jeden z dwóch problemów:

1. **Stary router:** Twój router może nie obsługiwać standardów Wi-Fi 5 (802.11ac) ani Wi-Fi 6 (802.11ax). W takim przypadku karta AX211 pracuje w trybie kompatybilności wstecznej.
2. **Konfiguracja SSID:** Często routery rozdzielają sieci na dwie nazwy (np. "MojaSiec" dla 2.4 GHz i "MojaSiec\_5G"). Prawdopodobnie jesteś połączony z tą pierwszą.

> **Ważna uwaga techniczna:** Przejście na pasmo 5 GHz w standardzie 802.11n podwoi Twoją prędkość linku do 300 Mbps, ale dopiero zmiana standardu na **Wi-Fi 5 (ac)** lub **Wi-Fi 6 (ax)** pozwoli karcie AX211 rozwinąć pełną moc (866 Mbps - 2402 Mbps) dzięki kanałom 80/160 MHz i modulacji 1024-QAM.

Czy chcesz, abym sprawdził w specyfikacji Twojego modelu routera (jeśli go podasz), jakie są jego maksymalne możliwości i jak go skonfigurować pod tę kartę?