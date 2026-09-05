---
tags: [ai-agents, testing, qa, e2e, triage, oracle-problem, interview]
date: 2026-06-08
---
# Jak rozróżnić błąd od zmiany w wygenerowanym teście

Pytanie pada w kontekście [[agentowa-platforma-ai-automatyzacja-qa-e2e]]: test (zwłaszcza
**wygenerowany przez AI**) świeci na czerwono — skąd wiesz, czy to **realny bug w aplikacji**,
czy **zamierzona zmiana** (UI/API/wymagań), do której test trzeba dostosować, czy po prostu
**zły test** (generator się pomylił)? To nie jest detal — to jest **problem wyroczni (oracle
problem)** w czystej postaci i serce triage z sekcji 3.7 tamtej platformy.

## Najpierw: to nie są dwie, tylko cztery kategorie

„Błąd vs zmiana" to mylące uproszczenie. Czerwony test ma **cztery** możliwe przyczyny
źródłowe i każda ma inną akcję naprawczą:

| Przyczyna | Co to znaczy | Właściwa reakcja |
|-----------|--------------|------------------|
| **Realny bug (regresja)** | Aplikacja zachowuje się źle wobec niezmienionych wymagań | Zgłoś buga + wygeneruj test regresyjny |
| **Zamierzona zmiana** | Wymaganie/UI/kontrakt celowo się zmieniły, test jest przestarzały | Auto-naprawa testu jako **PR** (sekcja 3.5) |
| **Wadliwy test** | Generator pomylił asercję / over-fitted / kruchy selektor | Popraw/przegeneruj test, oznacz problem generacji |
| **Flaky / środowisko** | Niedeterminizm, zepsute env, timing | Kwarantanna + diagnoza synchronizacji |

Pytanie „błąd czy zmiana" tak naprawdę pyta o rozdzielenie wiersza 1 od wiersza 2 — ale
**przy teście wygenerowanym przez AI dochodzi wiersz 3**, którego nie ma w klasycznym
testowaniu: porażka może oznaczać, że **to generator się pomylił, a nie aplikacja**.

## Dlaczego z samego testu nie da się tego rozstrzygnąć

Test koduje **założoną wyrocznię** — czyjeś przekonanie, jak system *powinien* się
zachować. Jeśli test świeci czerwono, znaczy to tylko tyle, że **rzeczywistość ≠ założenie**.
Z samej tej nierówności **nie wynika**, która strona jest błędna:

- aplikacja jest zła (bug), albo
- założenie testu jest przestarzałe (zmiana), albo
- założenie testu od początku było złe (wadliwa generacja).

**Wniosek kluczowy na rozmowę:** rozróżnienia nie da się zrobić *wewnątrz* testu. Trzeba
sięgnąć po **niezależne źródło prawdy** (grounding) i porównać z nim. To jest istota
problemu wyroczni — i powód, dla którego pełna automatyzacja jest niemożliwa bez
human-in-the-loop dla przypadków granicznych.

## Sygnały, które klasyfikują przyczynę

Triage to nie zgadywanie — to zbieranie sygnałów i ważenie ich. Od najmocniejszych:

### 1. Niezależne źródło prawdy (grounding wyroczni) — sygnał rozstrzygający
To jedyny sposób, by odróżnić bug od zmiany, a nie tylko zgadnąć:

- **Wymaganie / user story (traceability TestSpec ↔ CompiledTest).** Jeśli wymaganie
  **się nie zmieniło**, a zachowanie tak → **realny bug**. Jeśli wymaganie **zmieniono** →
  **zamierzona zmiana**, test do aktualizacji. To dlatego traceability wymaganie↔test
  (sekcja 7) jest tak ważne — bez niego nie masz wyroczni.
- **OpenAPI / kontrakt.** Test API pęka, bo schemat się zmienił → zamierzona zmiana
  (synchronizuj test). Test pęka mimo niezmienionego kontraktu → bug.
- **Git diff / opis PR.** Czy commit, który „zazielenił na czerwono", **celowo** ruszał ten
  obszar? Zmiana opisana w PR jako feature → prawdopodobnie zamierzona. Zmiana w logice
  biznesowej bez wzmianki → podejrzenie buga.

### 2. Pochodzenie (provenance) wygenerowanej asercji — specyficzne dla AI
**To jest gwóźdź dla testów AI.** Skąd generator wziął asercję, decyduje, czy porażka w
ogóle może świadczyć o bugu (por. tabela źródeł generacji, sekcja 3.1):

- Asercja **z wymagań** → może autorytatywnie wskazać buga (koduje intencję).
- Asercja **z kodu** → **tautologia**: utrwala obecne zachowanie, więc jej porażka znaczy
  tylko „zachowanie się zmieniło" — *nie odróżnia* buga od zmiany. To characterization test.
- Asercja **z ruchu produkcyjnego** → koduje „jak było", nie „jak ma być" — podobne ryzyko.

Dlatego platforma musi **zapisywać pochodzenie każdej asercji** (provenance), żeby triage
wiedział, jak bardzo czerwonemu można ufać.

### 3. Warstwa, na której test pęka — szybka heurystyka
- **Selektor nie znaleziony / element zniknął / 404 / niezgodność schematu** → zwykle
  **zmiana strukturalna** (UI/API), kandydat na auto-naprawę.
- **Asercja na wartości / wyniku biznesowym jest błędna** (np. zła kwota, zły status) →
  częściej **realny bug**.
- **Timeout / błąd sieci / przerywany** → **flaky/środowisko**.

### 4. Historia i powtarzalność testu
- **Nowy, wygenerowany test, który nigdy nie był zielony** → *nie* jest dowodem buga.
  Jest **niezwalidowany** — patrz sekcja niżej. Nie traktuj pierwszego czerwonego jak regresji.
- Test **kiedyś zielony, teraz czerwony po deployu ruszającym ten obszar** → bug albo zmiana.
- **Deterministycznie czerwony co przebieg** → realne (bug/zmiana). **Przerywany** → flaky.

### 5. Klasteryzacja wielu porażek (jedna przyczyna → N czerwonych)
- Jedna zmiana wywala **wiele niepowiązanych** testów → częściej **zmiana współdzielonego
  komponentu / zepsute środowisko**, nie N osobnych bugów.
- **Izolowana, pojedyncza** asercja w jednym przepływie → częściej realny bug.

### 6. Sędzia semantyczny / multimodalny (dla UI)
Model wizyjny ocenia *semantyczną* równoważność: „czy to wciąż ta sama, poprawna strona,
tylko przestylowana?" → **zamierzona zmiana wizualna**, nie regresja. Tnie fałszywe alarmy
pixel-diffa (sekcja 3.6).

## Twist dla testów generowanych przez AI: walidacja przed zaufaniem

Najważniejsza zasada specyficzna dla tego pytania, wynikająca z **krystalizacji** (zasada
2.1): **świeżo wygenerowany test, który pada na pierwszym uruchomieniu, NIE jest sygnałem
buga** — jest **niezwalidowanym założeniem generatora**. Zanim taki test stanie się
regresją bramkującą CI, musi przejść walidację względem wyroczni (review / porównanie z
wymaganiem). Mylenie „mój nowy test jest czerwony" z „znalazłem buga" to klasyczny błąd
platform AI do testów.

Innymi słowy: kierunek wnioskowania zależy od **dojrzałości** testu:
- **Test już skrystalizowany i kiedyś zielony** → czerwony = sygnał o aplikacji (bug/zmiana).
- **Test dopiero co wygenerowany** → czerwony = najpierw podejrzenie o sam test, dopiero po
  walidacji wyrocznią rozważasz buga.

## Pipeline triage (jak to spiąć w system)

```text
czerwony test + bogate artefakty (trace, DOM, screenshot, logi, diff)
   │
   ▼  1. ZBIERZ KONTEKST: historia testu, provenance asercji, git diff, wymaganie, OpenAPI
   ▼  2. SYGNAŁY DETERMINISTYCZNE: warstwa błędu, powtarzalność, klaster, zgodność schematu
   ▼  3. GROUNDING WYROCZNI: porównaj z wymaganiem / kontraktem (zmieniło się czy nie?)
   ▼  4. LLM-as-triage: klasyfikuj {bug | zmiana | wadliwy test | flaky} + uzasadnienie + confidence
   ▼  5. ROUTING:
        bug          → zgłoszenie + test regresyjny
        zmiana       → auto-naprawa jako PR (NIGDY po cichu)
        wadliwy test → popraw/przegeneruj + sygnał do generatora
        flaky        → kwarantanna + diagnoza synchronizacji
   ▼  6. NISKIE confidence / dwuznaczność → HUMAN-IN-THE-LOOP
```

## Żelazna zasada bezpieczeństwa: nigdy nie „naprawiaj" przez zazielenienie

Najgroźniejszy tryb porażki to **zamaskowana regresja**: platforma widzi czerwony test,
„naprawia" go (aktualizuje asercję/selektor), żeby przeszedł — i tym samym **ukrywa
realnego buga**. Dlatego:

- self-healing i auto-naprawa **proponują PR z dowodami**, nie przepisują testu po cichu
  (zasada 2.4, sekcja 3.4/3.5),
- każda decyzja triage jest **obserwowalna i audytowalna** (HealingEvent, ReviewDecision),
- kluczowa metryka jakości to **odsetek zamaskowanych regresji** (`< 1%`), nie tylko
  „skuteczność healingu" (sekcja 9).

Lepiej, żeby test **kontrolowanie padł**, niż żeby po cichu zamaskował regresję.

## Puenta na rozmowę

*„Z samego testu się nie da — czerwony znaczy tylko 'rzeczywistość ≠ założenie testu'. Żeby
odróżnić buga od zmiany, sięgam po niezależną wyrocznię: czy zmieniło się wymaganie /
kontrakt? Jeśli nie, a zachowanie tak — bug; jeśli tak — zamierzona zmiana, test do
aktualizacji jako PR. Przy teście generowanym przez AI dochodzi trzecia opcja: to generator
się pomylił — dlatego świeżo wygenerowany, nigdy niezielony test traktuję jako niezwalidowane
założenie, nie jako dowód buga, i zapisuję pochodzenie każdej asercji (z wymagań vs z kodu
— ta druga jest tautologią). Triage łączy sygnały deterministyczne (warstwa błędu,
powtarzalność, klaster) z LLM-em i groundingiem, a dwuznaczne przypadki idą do człowieka.
I twarda zasada: nigdy nie zazieleniam testu po cichu — to maskuje regresje."*

## Powiązane notatki

- [[agentowa-platforma-ai-automatyzacja-qa-e2e]] — platforma, triage (3.7), krystalizacja (2.1), self-healing (3.4)
- [[automatyzacja-testow-przygotowanie-rozmowa-ai-engineer]] — problem wyroczni, flakiness, fundamenty
- [[testowanie-rag-techniki-warstwy-frameworki]] — eval-driven dev, golden datasety, LLM-as-a-Judge
- [[obsluga-bledow-system-wieloagentowy]] — silent failures, transient vs permanent, wykrywanie stagnacji
- [[architektura-agentowa-50-serwerow-hub-and-spoke]] — pętla samonaprawcza agenta Playwright (Verify/Heal)
- [[llm-guardrails]] — guardrails dla części agentowej
