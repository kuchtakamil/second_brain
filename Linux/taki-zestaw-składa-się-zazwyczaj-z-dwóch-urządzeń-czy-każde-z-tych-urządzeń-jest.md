# taki zestaw składa się zazwyczaj z dwóch urządzeń. Czy każde z tych urządzeń jes

**Data:** 22 sty 2026, 12:11:43 CET

---

**User:**

taki zestaw składa się zazwyczaj z dwóch urządzeń. Czy każde z tych urządzeń jest access pointem i rozgłasza swoją sieć wifi? czy te dwa urządzenia rozgłaszają tą samą sieć wifi i w przypadku gdy przechodzę między pokojami to muszę się przełączać między sieciami wifi czy nie?

---

**Gemini:**

W typowym zestawie (KIT) urządzenia pełnią dwie różne role techniczne, co determinuje sposób rozgłaszania sieci bezprzewodowej.

### Architektura zestawu TL-WPA4220 KIT

Zestaw ten składa się zazwyczaj z dwóch różnych jednostek:

1. **Transmiter (np. TL-PA4010):** Jest to jednostka "wejściowa", którą wpinasz do gniazdka przy routerze i łączysz z nim kablem Ethernet. To urządzenie **nie posiada modułu Wi-Fi** – służy jedynie do modulacji sygnału cyfrowego na częstotliwości sieci elektrycznej (tzw. iniekcja sygnału).
2. **Ekstender (TL-WPA4220):** Jest to jednostka "wyjściowa", która posiada wbudowany punkt dostępowy (Access Point). To ona odbiera sygnał z instalacji prądowej i rozgłasza sieć Wi-Fi w nowym pomieszczeniu.

### Rozgłaszanie sieci i funkcja Wi-Fi Clone

Urządzenia te domyślnie mogą rozgłaszać własną sieć o nazwie fabrycznej (np. *TP-Link\_XXXX*), ale standardowo korzysta się z funkcji **Wi-Fi Clone**:

- Po naciśnięciu przycisku Wi-Fi Clone na transmiterze i przycisku WPS na głównym routerze, urządzenie kopiuje **SSID** (nazwę sieci) oraz **hasło** z Twojego routera.
- W efekcie w całym domu widzisz **tylko jedną nazwę sieci**.

### Przełączanie między pokojami (Roaming)

W przypadku modelu TL-WPA4220 musisz mieć świadomość ograniczeń technicznych w zakresie roamingu:

- **Brak standardów Mesh:** TL-WPA4220 nie wspiera protokołów szybkiego roamingu (802.11k/v/r). Nie jest to system Mesh, lecz tradycyjny Extender.
- **Decyzja klienta:** To Twoje urządzenie końcowe (smartfon, laptop) decyduje, kiedy przełączyć się na silniejszy sygnał. Często występuje zjawisko tzw. **"sticky client"** – telefon trzyma się słabego sygnału z routera w salonie, mimo że stoisz tuż obok transmitera w sypialni, dopóki sygnał z salonu całkowicie nie zaniknie.
- **Przerwa w transmisji:** Podczas przełączania następuje zazwyczaj krótka przerwa (kilkaset milisekund do kilku sekund), co może być odczuwalne podczas rozmów VoIP (np. Teams, WhatsApp) lub w grach online.

---

### Porównanie rozwiązań

| Cecha | TL-WPA4220 (Standard PLC) | Powerline Mesh (np. TP-Link Deco PX50) |
| --- | --- | --- |
| **Nazwa sieci (SSID)** | Taka sama (po sklonowaniu) | Taka sama (natywnie) |
| **Płynność przełączania** | Zależna od klienta (możliwe przerwy) | Płynna (aktywne sterowanie roamingiem) |
| **Zarządzanie** | Każde urządzenie osobno | Centralne przez aplikację |
| **Technologia** | Wi-Fi 4 (N300) | Wi-Fi 6 (AX) |

Jeśli zależy Ci na tym, aby przechodzenie między pokojami było całkowicie niezauważalne dla aplikacji, lepszym wyborem będzie system **Powerline Mesh**. Standardowy zestaw TL-WPA4220 sprawdzi się dobrze jako "stacjonarne" rozszerzenie sieci dla telewizora czy komputera, ale przy częstym przemieszczaniu się po mieszkaniu z telefonem może irytować brakiem płynnego roamingu.

Czy chciałbyś, abym przedstawił konkretne modele systemów Mesh wykorzystujących sieć elektryczną, które rozwiązują problem "przełączania się" między sieciami?

[Jak skonfigurować Wi-Fi Clone w transmiterach TP-Link](https://www.youtube.com/watch?v=LUrF6Lcx8_k)
Ten film pokazuje krok po kroku, jak zsynchronizować ustawienia sieci Wi-Fi między routerem a transmiterem PLC, aby uniknąć konieczności ręcznego łączenia się z nową siecią.