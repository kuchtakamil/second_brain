# Transmitery sieciowe np. TP-LINK Powerline TL-WPA4220 WIFI. Czy będą one działał

**Data:** 22 sty 2026, 12:05:11 CET

---

**User:**

Transmitery sieciowe np. TP-LINK Powerline TL-WPA4220 WIFI. Czy będą one działały w blokach z 2005 roku w dużym mieście w Polsce? Mam wątpliwości czy tak stary kabel prądowy jest w obsłużyć taką usługę?

---

**Gemini:**

Instalacje elektryczne w budynkach oddanych do użytku w 2005 roku w Polsce są zazwyczaj w pełni kompatybilne z technologią Powerline (PLC - Power Line Communication). W tym okresie standardem było już stosowanie miedzianych przewodów trójżyłowych ($3 \times 2,5\text{ mm}^2$ dla obwodów gniazd wtykowych), co jest warunkiem optymalnego działania tych urządzeń.

### Stan instalacji elektrycznej z 2005 roku

Budownictwo z pierwszej dekady XXI wieku w dużych miastach charakteryzuje się nowoczesnym podejściem do infrastruktury elektrycznej:

- **Miedź zamiast aluminium:** W 2005 roku nie stosowano już w nowym budownictwie przewodów aluminiowych, które są główną przeszkodą dla transmiterów PLC ze względu na wysoką rezystancję i podatność na utlenianie styków.
- **Rozdzielnice modułowe:** Instalacje te posiadają nowoczesne zabezpieczenia nadprądowe i wyłączniki różnicowoprądowe (RCD). Choć RCD mogą wprowadzać pewne tłumienie sygnału wysokiej częstotliwości, rzadko całkowicie uniemożliwiają komunikację.
- **Układ sieci TNS:** Obecność oddzielnego przewodu ochronnego (PE) jest kluczowa dla nowszych standardów PLC (np. AV2-HomePlug), które wykorzystują technologię MIMO (transmisja po parach fazowy-neutralny oraz fazowy-ochronny). Model TL-WPA4220 to standard AV600 (SISO), więc korzysta głównie z pary fazowy-neutralny, ale nowoczesna instalacja zapewnia mu stabilne środowisko pracy.

---

### Kluczowe czynniki wpływające na działanie w bloku

Mimo że wiek kabla nie jest problemem, w bloku mieszkalnym musisz zwrócić uwagę na inne aspekty techniczne:

| Czynniki sukcesu | Opis zagrożenia |
| --- | --- |
| **Przynależność do fazy** | W mieszkaniach z instalacją trójfazową (często przy płytach indukcyjnych), gniazdka w różnych pokojach mogą być na różnych fazach ($L1, L2, L3$). Sygnał PLC przechodzi między fazami tylko przez tzw. przesłuchy, co drastycznie obniża prędkość. |
| **Szumy i zakłócenia** | Zasilacze impulsowe (ładowarki, tanie LED-y) oraz urządzenia z silnikami (odkurzacze, pralki) generują szum EMI, który PLC musi filtrować. |
| **Listwy antyprzepięciowe** | **Nigdy** nie wpinaj transmitera do listwy z filtrami. Filtry w listwach są zaprojektowane do wycinania wysokich częstotliwości – dokładnie tych, których PLC używa do transmisji danych. |

---

### Wydajność modelu TP-LINK TL-WPA4220 (AV600)

Model TL-WPA4220 to urządzenie klasy budżetowej. Choć nazwa sugeruje 600 Mb/s, jest to wartość teoretyczna warstwy fizycznej. W praktyce:

1. **Porty Ethernet:** Urządzenie posiada porty 10/100 Mb/s. Oznacza to, że realna prędkość po kablu nigdy nie przekroczy **100 Mb/s**, nawet jeśli instalacja elektryczna jest idealna.
2. **Standard Wi-Fi:** Wbudowany punkt dostępowy pracuje w standardzie Wi-Fi 4 (N300) w paśmie 2.4 GHz, co w gęstej zabudowie bloku (dużo sieci sąsiadów) może skutkować niską przepustowością i wysokimi opóźnieniami.

---

### Rekomendacje techniczne

Jeśli Twoje łącze internetowe jest szybsze niż 100 Mb/s, model TL-WPA4220 stanie się wąskim gardłem. W takim przypadku warto rozważyć standard **AV1000 lub AV1200** z portami Gigabit Ethernet.

**Aby zminimalizować problemy w bloku z 2005 roku:**

- Wpinaj transmitery bezpośrednio do gniazdek ściennych.
- Jeśli to możliwe, wybierz gniazdka, które są obsługiwane przez ten sam bezpiecznik (małe prawdopodobieństwo różnych faz).
- Jeśli prędkość będzie niezadowalająca, konieczne może być zainstalowanie w rozdzielnicy **sprzęgacza fazowego**, który umożliwi swobodny przepływ sygnału PLC między różnymi fazami w mieszkaniu.

Czy chcesz, abym pomógł Ci sprawdzić, czy Twoje gniazdka są na tej samej fazie, lub dobrał model o wyższej przepustowości?