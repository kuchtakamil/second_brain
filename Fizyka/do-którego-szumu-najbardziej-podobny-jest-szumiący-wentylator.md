# Do którego szumu najbardziej podobny jest szumiący wentylator?

**Data:** 3 sty 2026, 23:17:32 CET

---

**User:**

Do którego szumu najbardziej podobny jest szumiący wentylator?

---

**Gemini:**

Szumiący wentylator jest technicznie najbliższy **szumowi różowemu (pink noise)** lub **szumowi brązowemu (brown noise)**, mimo że potocznie niemal zawsze nazywa się go "białym szumem".

Z punktu widzenia fizyki i akustyki, dźwięk wentylatora nie jest idealnym białym szumem z kilku kluczowych powodów:

### 1. Spadek energii w wysokich częstotliwościach

Biały szum ma taką samą energię dla każdej częstotliwości, co sprawia, że brzmi bardzo ostro (jak syk). Wentylatory generują dźwięk poprzez turbulencje powietrza i ruch mechaniczny. Fizyka przepływu powietrza wokół łopatek (aerodynamika) naturalnie faworyzuje niższe częstotliwości.

- **Duże wentylatory domowe:** Ich widmo mocy spada wraz ze wzrostem częstotliwości, co zbliża je do **szumu brązowego** (głębokiego, basowego huku).
- **Mniejsze wentylatory (np. biurkowe):** Mają więcej energii w średnich pasmach, co plasuje je najbliżej **szumu różowego**.

### 2. Składowe tonalne (Blade Passing Frequency)

W przeciwieństwie do czystych szumów kolorowych, które są sygnałami całkowicie losowymi (stochastycznymi), wentylator generuje tzw. **BPF (Blade Passing Frequency)**. Jest to stały, niski pomruk wynikający z częstotliwości, z jaką łopatki mijają dany punkt (np. wspornik obudowy).
$$f\_{BPF} = n \cdot \text{liczba łopatek}$$
Gdzie $n$ to prędkość obrotowa w hercach. To sprawia, że szum wentylatora ma w swoim widmie wyraźne "piki" (wzmocnienia), których nie znajdziesz w czystym szumie różowym czy białym.

### 3. Dlaczego więc mówimy "biały szum"?

Termin "biały szum" stał się w języku potocznym synonimem każdego **szumu szerokopasmowego**, który maskuje inne dźwięki otoczenia. Wentylator świetnie maskuje nagłe hałasy (np. trzaśnięcie drzwiami), ponieważ wypełnia szerokie spektrum częstotliwości, do których przyzwyczaja się nasz mózg (proces habituacji).

---

### Porównanie w skrócie:

| Źródło dźwięku | Najbliższy kolor szumu | Dlaczego? |
| --- | --- | --- |
| **Mały wentylator PC** | Różowy / Niebieski | Dużo turbulencji o wysokiej częstotliwości, "świszczący" dźwięk. |
| **Wentylator stojący** | **Różowy** | Zbalansowany rozkład energii, przypomina szum deszczu. |
| **Duży cyrkulator** | **Brązowy** | Dominacja niskich tonów, potężny ruch masy powietrza. |

Większość aplikacji "White Noise" do snu, które oferują dźwięk wentylatora, w rzeczywistości odtwarza nagrania o charakterystyce **różowej**, ponieważ jest ona najlepiej tolerowana przez ludzkie ucho podczas długotrwałego słuchania.

Czy chciałbyś, abym wyjaśnił, jak matematycznie przefiltrować biały szum, aby uzyskać charakterystykę dźwiękową typową dla wentylatora (np. za pomocą filtrów dolnoprzepustowych)?