# Kategorie przewodów LAN RJ45 i ich realne przepustowości, przydługości ok 15 met

**Data:** 22 sty 2026, 13:33:22 CET

---

**User:**

Kategorie przewodów LAN RJ45 i ich realne przepustowości, przydługości ok 15 metrów

---

**Gemini:**

Wybór kategorii okablowania strukturalnego przy dystansie 15 metrów determinuje nie tylko maksymalną przepustowość, ale także odporność na przesłuchy (crosstalk) oraz zakłócenia elektromagnetyczne (EMI). Przy tak krótkim odcinku standardy często pozwalają na osiągnięcie parametrów wykraczających poza ich nominalną specyfikację przewidzianą dla 100 metrów.

### Zestawienie kategorii i parametrów przy 15 metrach

| Kategoria | Częstotliwość | Standardowa przepustowość (do 100m) | Realna przepustowość przy 15m | Zastosowanie / Uwagi |
| --- | --- | --- | --- | --- |
| **Cat 5e** | 100 MHz | 1 Gbps | **1 Gbps / 2.5 Gbps** | Wspiera 2.5GBASE-T na krótkich dystansach (NBASE-T). |
| **Cat 6** | 250 MHz | 1 Gbps | **10 Gbps** | Oficjalnie wspiera 10 Gbps do ok. 37-55m w środowisku o niskim poziomie zakłóceń. |
| **Cat 6a** | 500 MHz | 10 Gbps | **10 Gbps** | Standard dla 10GbE. Pełna wydajność dzięki lepszemu tłumieniu przesłuchów obcych (AXT). |
| **Cat 7** | 600 MHz | 10 Gbps | **10 Gbps+** | Standard ISO/IEC. Wymaga ekranowania każdej pary (S/FTP). |
| **Cat 7a** | 1000 MHz | 10 Gbps | **40 Gbps** | Przy 15m może teoretycznie obsłużyć 40GBASE-T, choć brak oficjalnej ratyfikacji IEEE dla RJ45. |
| **Cat 8.1** | 2000 MHz | 25 / 40 Gbps | **40 Gbps** | Zaprojektowana dla centrów danych na dystansie do 30m. |

---

### Analiza techniczna poszczególnych rozwiązań

#### Cat 5e (Category 5 Enhanced)

Mimo że standard przewiduje 1 Gbps, przy 15 metrach przewody wysokiej jakości (czysta miedź BC, nie CCA) bez problemu radzą sobie ze standardem **2.5GBASE-T**. Wąskim gardłem jest tutaj budżet łącza i margines szumu (SNR), który na krótkim odcinku jest bardzo wysoki.

#### Cat 6 – "Sweet spot" dla 15 metrów

Kategoria 6 jest najczęstszym wyborem dla domowych instalacji 10 Gbps na krótkich dystansach. O ile przy 100 metrach Cat 6 gwarantuje tylko 1 Gbps, o tyle limit dla **10GBASE-T** wynosi 55 metrów (w idealnych warunkach) lub 37 metrów (w środowiskach o dużym zagęszczeniu kabli). Przy 15 metrach Cat 6 oferuje pełne 10 Gbps z bardzo niską stopą błędów (BER).

#### Cat 6a (Augmented)

Kluczową różnicą względem Cat 6 jest rygorystyczne podejście do **Alien Crosstalk (AXT)**, czyli zakłóceń między sąsiednimi kablami. Przy 15 metrach w gęstych wiązkach (np. w korytach kablowych), Cat 6a zapewnia stabilność, której Cat 6 może nie utrzymać przy pełnym obciążeniu 10 Gbps.

#### Cat 7 i 7a

Warto zauważyć, że Cat 7/7a nie jest oficjalnie uznawana przez TIA/EIA (amerykański standard), lecz przez ISO/IEC. Wykorzystuje złącza typu GG45 lub TERA, choć na rynku powszechne są "patchcordy Cat 7" zakończone zwykłymi wtykami RJ45. Przy 15 metrach ich realna przewaga nad Cat 6a jest znikoma, chyba że pracujemy w środowisku o ekstremalnych zakłóceniach przemysłowych, gdzie ekranowanie S/FTP jest niezbędne.

#### Cat 8.1

To rozwiązanie dedykowane do komunikacji **Switch-to-Switch** w serwerowniach. Przy 15 metrach pozwala na uzyskanie **40 Gbps**. Wymaga stosowania dedykowanych modułów Keystone oraz wtyków ekranowanych, aby zachować ciągłość ekranu i integralność sygnału przy częstotliwościach rzędu 2 GHz.

---

### Kluczowe czynniki wpływające na wydajność przy 15m

1. **Konstrukcja przewodnika:**
   - **Pure Copper (BC):** Pełna miedź. Niezbędna dla PoE i stabilnych wysokich przepustowości.
   - **CCA (Copper Clad Aluminum):** Aluminium miedziowane. Przy 15m może powodować problemy z rezystancją DC i nie osiągać parametrów Cat 6/6a.
2. **Ekranowanie (Shielding):**
   - **U/UTP:** Brak ekranu. Podatny na zakłócenia zewnętrzne, ale najbardziej elastyczny.
   - **F/UTP / S/FTP:** Ekranowanie folią lub oplotem. Przy 15 metrach w pobliżu kabli elektrycznych 230V, ekranowanie (szczególnie w Cat 6a) znacząco poprawia SNR.
3. **Promień gięcia:** Przy wysokich kategoriach (Cat 6a i wyżej), zbyt mocne zagięcie kabla (poniżej 4x średnica kabla) powoduje deformację skrętu par, co drastycznie zwiększa odbicia sygnału (Return Loss) i obniża realną przepustowość.

Czy chciałbyś, abym przygotował specyfikację dotyczącą wyboru konkretnych komponentów (patchpanele, moduły Keystone) dla wybranej kategorii?