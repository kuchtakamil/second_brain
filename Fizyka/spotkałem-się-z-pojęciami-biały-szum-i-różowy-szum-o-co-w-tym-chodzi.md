# Spotkałem się z pojęciami biały szum i różowy szum. O co w tym chodzi?

**Data:** 3 sty 2026, 23:14:13 CET

---

**User:**

Spotkałem się z pojęciami biały szum i różowy szum. O co w tym chodzi?

---

**Gemini:**

Pojęcia koloru szumu (ang. *noise colors*) odnoszą się do kształtu gęstości widmowej mocy (PSD – *Power Spectral Density*), czyli tego, jak energia sygnału rozkłada się w dziedzinie częstotliwości. Klasyfikacja ta opiera się na analogii do widma światła widzialnego.

### Biały szum (White Noise)

Biały szum charakteryzuje się płaską gęstością widmową mocy w skali liniowej. Oznacza to, że w każdym równym przedziale częstotliwości (np. 100 Hz – 200 Hz oraz 10 000 Hz – 10 100 Hz) zawarta jest dokładnie taka sama ilość energii.

- **Charakterystyka matematyczna:** $S(f) = \text{const}$. Widmo jest niezależne od częstotliwości.
- **Percepcja:** Dla ludzkiego ucha biały szum brzmi bardzo "ostro" i wysokotonowo (przypomina syczenie starego telewizora lub radioodbiornika nieustawionego na stację). Wynika to z faktu, że nasz słuch pracuje w skali logarytmicznej, a nie liniowej. Skoro każda kolejna oktawa ma dwa razy większy zakres częstotliwości niż poprzednia, biały szum kumuluje znacznie więcej energii w wysokich rejestrach.
- **Zastosowania:** Testowanie odpowiedzi częstotliwościowej systemów audio, synteza dźwięku, generatory liczb losowych.

---

### Różowy szum (Pink Noise / 1/f Noise)

Różowy szum ma gęstość widmową mocy odwrotnie proporcjonalną do częstotliwości. Jest to najbardziej powszechny rodzaj szumu występujący w naturze (biologii, ekonomii, a nawet w strukturze muzyki).

- **Charakterystyka matematyczna:** $S(f) \propto \frac{1}{f}$. Spadek mocy wynosi **3 dB na oktawę**.
- **Percepcja:** Różowy szum jest postrzegany przez człowieka jako "zbalansowany" lub "płaski". Dzieje się tak, ponieważ każda oktawa (np. 440–880 Hz i 880–1760 Hz) niesie taką samą ilość energii. Brzmi bardziej naturalnie, przypominając szum deszczu, wiatru lub wodospadu.
- **Zastosowania:** Kalibracja systemów nagłośnieniowych w profesjonalnej akustyce (wyrównywanie charakterystyki pomieszczeń), maskowanie hałasu w biurach, badania nad procesami biologicznymi (rytm serca, fale mózgowe).

---

### Porównanie techniczne

Główna różnica sprowadza się do sposobu dystrybucji energii względem pasm częstotliwości:

| Cecha | Biały Szum | Różowy Szum |
| --- | --- | --- |
| **Gęstość mocy** | Stała na jednostkę częstotliwości (Hz) | Stała na oktawę / dekadę |
| **Spadek mocy** | 0 dB / oktawę | ~3 dB / oktawę |
| **Profil dźwiękowy** | Syczący, jasny, agresywny | Głęboki, miękki, naturalny |
| **Wzór (PSD)** | $S(f) = k$ | $S(f) = \frac{k}{f}$ |

---

### Zaawansowane aspekty: Transformacja i Generowanie

Generowanie szumu białego w systemach cyfrowych jest trywialne – sprowadza się do wygenerowania ciągu liczb pseudolosowych o rozkładzie jednostajnym lub normalnym (Gaussowskim).

Generowanie szumu różowego jest trudniejsze obliczeniowo, ponieważ wymaga nałożenia filtra na biały szum, który będzie tłumił wysokie częstotliwości o 3 dB na oktawę. W praktyce stosuje się algorytmy takie jak **Voss-McCartney** (uśrednianie wielu generatorów o różnych częstotliwościach próbkowania) lub projektuje się filtry IIR/FIR o specyficznej odpowiedzi częstotliwościowej.

#### Inne kolory szumów (kontekst rozszerzony)

- **Szum brązowy (Brownian/Red):** $1/f^2$. Spadek o 6 dB na oktawę. Bardzo głęboki, basowy dźwięk. Powstaje poprzez całkowanie białego szumu (proces Wienera).
- **Szum niebieski (Blue):** Proporcjonalny do $f$. Wzrost o 3 dB na oktawę. Wykorzystywany w ditheringu (technika redukcji błędów kwantyzacji w grafice i audio).
- **Szum fioletowy (Violet):** Proporcjonalny do $f^2$. Powstaje przez różniczkowanie białego szumu.

Chcesz, abym przygotował implementację algorytmu generującego szum różowy (np. algorytm Vossa) w języku Python lub C++?