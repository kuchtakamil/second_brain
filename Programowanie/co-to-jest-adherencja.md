# co to jest adherencja?

**Data:** 25 gru 2025, 18:01:48 CET

---

**User:**

co to jest adherencja?

---

**Gemini:**

**Adherencja** (ang. *medication adherence*), czyli **przestrzeganie zaleceń terapeutycznych**, to stopień, w jakim zachowanie pacjenta (przyjmowanie leków, stosowanie diety, zmiana stylu życia) jest zgodne z planem uzgodnionym wspólnie z pracownikiem ochrony zdrowia. W kontekście medycyny przewlekłej, a szczególnie w IBD, termin ten zastąpił starsze pojęcie „compliance” (podporządkowanie się), podkreślając partnerską relację między lekarzem a pacjentem.

---

### Taksonomia Adherencji (Model ABC)

Według standardów naukowych (np. klasyfikacja Vrijens i wsp.), proces adherencji dzieli się na trzy krytyczne fazy:

1. **Inicjacja (Initiation):** Moment, w którym pacjent przyjmuje pierwszą dawkę przepisanego leku. W IBD problemem bywa lęk przed immunosupresją lub terapią biologiczną.
2. **Implementacja (Implementation):** Stopień, w jakim rzeczywiste dawkowanie pacjenta odpowiada przepisanemu schematowi (np. czy pacjent przyjmuje mesalazynę 3x dziennie, czy pomija dawki południowe).
3. **Persystencja (Persistence):** Czas trwania terapii od inicjacji do całkowitego zaprzestania przyjmowania leku. W chorobach przewlekłych persystencja drastycznie spada po pierwszym roku leczenia.

---

### Adherencja vs. Compliance – Kluczowe Różnice

| Cecha | Compliance (Podporządkowanie) | Adherencja (Współpraca) |
| --- | --- | --- |
| **Relacja** | Hierarchiczna (lekarz nakazuje) | Partnerska (wspólna decyzja) |
| **Rola pacjenta** | Pasywny odbiorca | Aktywny uczestnik procesu |
| **Przyczyny odstępstw** | Traktowane jako "nieposłuszeństwo" | Analizowane jako bariery (koszty, skutki uboczne) |

---

### Znaczenie Kliniczne w IBD

W nieswoistych zapaleniach jelit adherencja jest krytycznym czynnikiem determinującym przebieg choroby. Niska adherencja prowadzi do:

- **Loss of Response (LOR):** Nieregularne przyjmowanie leków biologicznych (np. infliksymabu, adalimumabu) prowadzi do wahań stężenia leku we krwi (trough levels), co sprzyja powstawaniu **przeciwciał przeciwko lekowi (ADA - Anti-Drug Antibodies)**. Skutkuje to bezpowrotną utratą skuteczności danej cząsteczki.
- **Ryzyko zaostrzeń:** Pacjenci z wrzodziejącym zapaleniem jelita grubego (WZJG), którzy nie przestrzegają terapii podtrzymującej mesalazyną, mają **pięciokrotnie wyższe ryzyko nawrotu** choroby.
- **Progresja nowotworowa:** Stałe podtrzymywanie remisji dzięki adherencji redukuje przewlekły stan zapalny, co jest kluczowe w chemoprewencji raka jelita grubego.

---

### Przyczyny Non-adherencji (Bariery)

Analiza adherencji w systemach takich jak zaproponowany IBD-Nexus musi uwzględniać dwa typy nieprzestrzegania zaleceń:

- **Niezamierzone (Unintentional):** Zapominanie, brak dostępu do apteki, skomplikowany schemat dawkowania.
- **Zamierzone (Intentional):** Pacjent świadomie odstawia lek, np. z powodu poprawy samopoczucia („czuję się dobrze, nie potrzebuję chemii”) lub strachu przed skutkami ubocznymi (np. steroidofobia).

### Monitorowanie Techniczne (Digital Adherence Monitoring)

W zaawansowanych systemach (jak IBD-Nexus) adherencję mierzy się poprzez:

- **MEMS (Medical Event Monitoring Systems):** Inteligentne nakrętki na opakowania leków rejestrujące każde otwarcie.
- **TDM (Therapeutic Drug Monitoring):** Korelacja logów przyjmowania leku z poziomem leku oznaczonym we krwi.
- **Analiza semantyczna (LLM):** Model analizuje wypowiedzi głosowe pacjenta (np. „źle się czuję po tych tabletkach, wziąłem tylko połowę”) i automatycznie flaguje spadek adherencji w raporcie klinicznym.

Czy chciałbyś, abyśmy rozbudowali moduł analizy adherencji w skrypcie Python, integrując go z systemem powiadomień IoT, który reaguje na pominiętą dawkę?