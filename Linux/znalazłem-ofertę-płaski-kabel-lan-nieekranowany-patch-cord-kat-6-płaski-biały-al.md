# ZNalazłem ofertę "Płaski kabel LAN nieekranowany Patch cord kat. 6 płaski biały"

**Data:** 22 sty 2026, 13:35:40 CET

---

**User:**

ZNalazłem ofertę "Płaski kabel LAN nieekranowany Patch cord kat. 6 płaski biały", ale ktoś w opinii pisze że przepustowość 100 Mbps. No i niepokoi mnie "nieekranowany"

---

**Gemini:**

Płaskie przewody LAN (flat cables) są konstrukcjami specyficznymi, które często przedkładają estetykę nad parametry transmisyjne. Opinia o przepustowości rzędu **100 Mbps** przy kablu kategorii 6 nie musi być błędem użytkownika – może wynikać z fizycznych ograniczeń tanich konstrukcji płaskich oraz mechanizmów negocjacji standardu Ethernet.

### Dlaczego płaski kabel może ograniczać prędkość do 100 Mbps?

Standard Gigabit Ethernet (**1000BASE-T**) wymaga do poprawnej pracy wszystkich **8 żył (4 par)**. Standard Fast Ethernet (**100BASE-TX**) wykorzystuje tylko **4 żyły (2 pary)**. Jeśli w opinii mowa o 100 Mbps, przyczyny mogą być następujące:

1. **Błędy terminacji lub uszkodzenia mechaniczne:** Płaskie kable są znacznie delikatniejsze. Wystarczy mikropęknięcie jednej z żył w parach niebieskiej lub brązowej, a karta sieciowa automatycznie „zejdzie” do 100 Mbps (tzw. **autonegocjacja** do najniższego stabilnego standardu).
2. **Brak pełnego skrętu par (Twisted Pair):** Istotą standardu Cat 6 jest precyzyjny splot par (określona liczba splotów na cal). W bardzo cienkich kablach płaskich żyły często biegną niemal równolegle. Powoduje to drastyczny wzrost przesłuchów zbliżnych (**NEXT - Near-End Crosstalk**). Przy dystansie 15 metrów poziom błędów może być tak wysoki, że kontroler Ethernet uzna pasmo 1 Gbps za nieosiągalne ze względu na niski współczynnik **SNR (Signal-to-Noise Ratio)**.
3. **Zastosowanie CCA (Copper Clad Aluminum):** Wiele tanich kabli płaskich zamiast czystej miedzi wykorzystuje aluminium miedziowane. Aluminium ma wyższą rezystancję, co przy 15 metrach powoduje większą atenuację (tłumienie sygnału) niż przewiduje norma dla Cat 6.

### Problem braku ekranowania (U/UTP)

Oznaczenie „nieekranowany” (**U/UTP**) samo w sobie nie jest wadą – większość standardowych kabli Cat 6 to konstrukcje nieekranowane. Jednak w przypadku kabli płaskich brak ekranu w połączeniu z ich budową generuje konkretne ryzyka:

- **Brak separacji par:** W okrągłym kablu Cat 6 zazwyczaj znajduje się plastikowy separator (spline), który fizycznie oddziela pary od siebie. W kablu płaskim pary leżą obok siebie w jednej płaszczyźnie, co bez ekranowania folią (FTP) czyni je ekstremalnie podatnymi na zakłócenia zewnętrzne (EMI) oraz przesłuchy między parami.
- **Przekrój żył (AWG):** Standardowe kable Cat 6 mają żyły o grubości **23 lub 24 AWG**. Kable płaskie często schodzą do **30 lub nawet 32 AWG** (są znacznie cieńsze). Cieńsza żyła to większa oporność i mniejsza odporność na zakłócenia, co przy 15 metrach jest już dystansem granicznym dla stabilnego 1 Gbps w tak niskiej jakości.

### Analiza porównawcza dla dystansu 15m

| Cecha | Płaski Patchcord Cat 6 (Tani) | Standardowy Okrągły Cat 6 (U/UTP) |
| --- | --- | --- |
| **Materiał** | Często CCA (Aluminium) | Zazwyczaj BC (Czysta miedź) |
| **Średnica żyły** | 30-32 AWG (Bardzo cienkie) | 23-24 AWG (Grube) |
| **Odporność na zgięcia** | Wysoka (elastyczność) | Średnia (wymagany promień gięcia) |
| **Stabilność 1 Gbps** | Niepewna przy 15m | Gwarantowana do 100m |
| **Przesłuchy (NEXT)** | Wysokie (równoległe ułożenie) | Niskie (precyzyjny splot + separator) |

### Rekomendacja techniczna

Jeśli planujesz przesyłać dane na dystansie 15 metrów i zależy Ci na stabilnym 1 Gbps (lub przyszłościowym 10 Gbps), odradzam kable płaskie typu „no-name”. Jeśli musisz użyć kabla płaskiego (np. pod panelami podłogowymi):

1. Upewnij się, że przewodnik to **100% miedź (BC - Bare Copper)**, a nie CCA.
2. Szukaj wersji **ekranowanej (np. U/FTP)**, która w konstrukcjach płaskich pomaga zniwelować brak splotu par.
3. Sprawdź parametr **AWG** – im niższa liczba (np. 26-28 AWG zamiast 32 AWG), tym lepiej dla sygnału na tym dystansie.

Czy chcesz, abym pomógł Ci zweryfikować konkretną specyfikację AWG i materiału z oferty, którą znalazłeś?