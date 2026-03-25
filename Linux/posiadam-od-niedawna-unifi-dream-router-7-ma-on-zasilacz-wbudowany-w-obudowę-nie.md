# Posiadam od niedawna Unifi Dream Router 7. Ma on zasilacz wbudowany w obudowę. N

**Data:** 7 lut 2026, 18:49:06 CET

---

**User:**

Posiadam od niedawna Unifi Dream Router 7. Ma on zasilacz wbudowany w obudowę. Niestety router się nagrzewa nawet gdy nie jest pod obciiążeniem. Zastanawiam się czy to dobry pomysł aby zostawiać go włączonego na noc, bo chcę do niego podłączyć kamery od unifi. Chodzi mi o ryzyko pożaru.

---

**Gemini:**

Urządzenia z linii UniFi Dream Router (UDR) charakteryzują się specyficzną konstrukcją termiczną, która sprawia, że obudowa jest ciepła lub wręcz gorąca w dotyku nawet przy minimalnym obciążeniu ruchem sieciowym. Wynika to z kilku czynników inżynieryjnych oraz zaimplementowanych mechanizmów bezpieczeństwa.

### Architektura termiczna i zasilanie wewnętrzne

UDR posiada zintegrowany zasilacz AC/DC umieszczony w dolnej części obudowy. Proces konwersji napięcia sieciowego na napięcia operacyjne (głównie 12V i 48V dla PoE) generuje straty energii w postaci ciepła, które kumuluje się wewnątrz zwartej, pionowej konstrukcji.

- **Straty na sekcji PoE:** Nawet jeśli żadne urządzenie nie jest podłączone, kontroler PoE oraz obwody regulacji napięcia pracują w stanie gotowości, generując tzw. *idle heat*.
- **Konwekcja wymuszona:** UDR posiada wewnętrzny wentylator, jednak jego krzywa prędkości jest skonfigurowana pod kątem kultury pracy (ciszy). Wentylator zazwyczaj zwiększa obroty dopiero po przekroczeniu określonych progów na sensorach `PHY` lub `CPU`.

### Ryzyko pożarowe a normy bezpieczeństwa

Z punktu widzenia inżynieryjnego, ryzyko pożaru sprawnego urządzenia certyfikowanego (CE, UL, FCC) jest marginalne.

1. **Thermal Throttling & Shutdown:** Procesor (SoC) oraz układy radiowe posiadają zdefiniowane w firmware progi krytyczne. W przypadku przegrzania (zazwyczaj okolice $100^\circ\text{C}$ na rdzeniu), urządzenie najpierw obniża taktowanie (throttling), a w ostateczności wykonuje twardy restart lub odcięcie zasilania.
2. **Zabezpieczenia zasilacza:** Wbudowany zasilacz impulsowy posiada zabezpieczenia nadprądowe (OCP), przepięciowe (OVP) oraz termiczne (OTP). W przypadku zwarcia lub krytycznego przegrzania komponentów pasywnych, bezpieczniki termiczne trwale przerywają obwód.
3. **Materiały:** Obudowa wykonana jest z poliwęglanu o wysokiej klasie odporności na palność (zgodność z normą UL94-V0), co oznacza, że materiał jest samogasnący i nie podtrzymuje płomienia.

---

### Wpływ podłączenia kamer (UniFi Protect)

Planowane podłączenie kamer zwiększy obciążenie termiczne UDR z dwóch powodów:

- **Pobór mocy PoE:** Każda kamera zwiększy zapotrzebowanie na prąd, co zmusi wewnętrzny zasilacz do cięższej pracy i zwiększy wydzielanie ciepła na tranzystorach MOSFET sekcji zasilania.
- **Zapis na kartę SD:** Ciągły zapis strumienia wideo na kartę microSD generuje dodatkowe ciepło w górnej części urządzenia, gdzie znajduje się slot.

### Optymalizacja warunków pracy

Aby zminimalizować ryzyko i obniżyć temperatury operacyjne, należy zwrócić uwagę na:

| Parametr | Zalecenie techniczne |
| --- | --- |
| **Orientacja** | Wyłącznie pionowa. Konstrukcja wykorzystuje efekt kominowy; otwory wentylacyjne na dole i na górze nie mogą być zasłonięte. |
| **Podłoże** | Unikaj powierzchni miękkich (dywany) i drewnianych wnęk o małej kubaturze. Najlepiej sprawdza się kamień, szkło lub otwarta przestrzeń. |
| **Wentylacja** | Upewnij się, że wokół routera jest minimum 10-15 cm wolnej przestrzeni z każdej strony. |
| **Monitorowanie** | W interfejsie UniFi OS (Settings -> Storage/Disk) oraz poprzez SSH (komenda `sensors` lub `mca-ctrl -t`) możesz weryfikować realne temperatury komponentów. |

### Diagnostyka przez SSH

Jeśli chcesz dokładnie sprawdzić, czy temperatura mieści się w normie projektowej, zaloguj się do urządzenia przez SSH i wykonaj:

```
# Sprawdzenie temperatur sensorów (zależnie od wersji softu)
mca-ctrl -t
# lub
ubnt-systool sensors
```

Normalne temperatury pracy dla UDR to $45^\circ\text{C}$ – $60^\circ\text{C}$ dla obudowy i do $75^\circ\text{C}$ – $85^\circ\text{C}$ dla wewnętrznych komponentów pod obciążeniem.

Czy chciałbyś, abym pomógł Ci skonfigurować powiadomienia w UniFi Protect, które poinformują Cię o ewentualnym rozłączeniu kamer lub problemach z zasilaniem?