---
tags: [ai-agents, testing, qa, e2e, human-in-the-loop, oracle-problem, interview]
date: 2026-06-08
---
# Jak wpiąć człowieka w system QA i czy weryfikacja jest automatyczna

Pytanie w kontekście [[agentowa-platforma-ai-automatyzacja-qa-e2e]]: **gdzie i jak wpina się
człowiek**, i czy **weryfikacja** jest automatyczna, czy człowiek musi ingerować?

## Najpierw doprecyzuj: o jakiej „weryfikacji" mowa

Słowo „weryfikacja" jest tu wieloznaczne — i na rozmowie warto to nazwać, zamiast zgadywać.
W kontekście platformy do automatyzacji testów E2E „weryfikacja" to **sprawdzenie, że
artefakt albo decyzja wyprodukowana przez AI jest poprawna, zanim jej zaufamy**. A AI
produkuje tu cztery rzeczy, które trzeba zweryfikować:

1. **Wygenerowany test** — czy jest poprawny, kompiluje się, nie dubluje pokrycia, łapie regresje?
2. **Asercja / wyrocznia** — czy test sprawdza *właściwą* rzecz (czy to, co uznaje za poprawne,
   faktycznie jest poprawne)? To problem wyroczni.
3. **Decyzja triage** — czy klasyfikacja „bug vs zmiana vs flaky" jest trafna?
   (por. [[rozroznienie-bledu-od-zmiany-w-wygenerowanym-tescie]])
4. **Self-healing** — czy uleczony selektor jest poprawny, a nie **maskuje regresji**?

Zakładam, że pytanie celuje głównie w (1) i (2): **czy platforma sama waliduje to, co
wygeneruje, czy musi to robić człowiek.** Odpowiadam na całość, bo mechanizm wpięcia
człowieka jest wspólny.

## Główna teza: weryfikacja jest WARSTWOWA, nie binarna

Zła odpowiedź to „automatyczna" albo „ręczna". Dobra odpowiedź: **podział pracy wynikający z
problemu wyroczni**:

> **AI weryfikuje to, co jest maszynowo sprawdzalne. Człowiek weryfikuje INTENCJĘ
> (wyrocznię) — to, czego AI nie potrafi ugruntować.**

Bo dokładnie to jest granica: maszyna sprawdzi, czy test się kompiluje, czy zgadza się ze
schematem, czy łapie wstrzyknięte buggi — ale **nie wie, co jest „poprawne"** w sensie
biznesowym. To wiedza, która żyje w wymaganiach i głowach ludzi (zasada 2.4 i sekcja 3.8
platformy).

## Co weryfikuje automat (deterministyczne bramki, bez człowieka)

To filtruje przytłaczającą większość przypadków i odciąża człowieka:

- **Kompilacja / wykonalność** — czy wygenerowany test w ogóle się uruchamia.
- **Zgodność ze schematem** — structured output walidowany Pydantic/JSON Schema na granicy;
  test API zgodny z OpenAPI.
- **Nie-duplikacja pokrycia** — RAG nad repo wykrywa, że test dubluje istniejący.
- **Mutation testing** — twardszy sygnał niż coverage: czy test faktycznie łapie buggi
  (wstrzykujemy mutacje, test musi je wykryć).
- **Regresja na golden dataset** — czy generacja/triage nie pogorszyły się względem
  oznaczonego zbioru referencyjnego.
- **Próg pewności + klaster + powtarzalność** — sygnały triage (sekcja o sygnałach w
  [[rozroznienie-bledu-od-zmiany-w-wygenerowanym-tescie]]).

Jeśli output **nie przejdzie** którejkolwiek bramki → wraca do generatora (pętla korekcyjna)
albo do człowieka, ale **nie awansuje** automatycznie.

## Co MUSI weryfikować człowiek (granica wyroczni + akcje mutujące)

Tu automat z definicji nie wystarcza:

- **Intencja / asercja (wyrocznia)** — czy test sprawdza właściwą rzecz. LLM *proponuje*
  asercje (bo autorzy notorycznie asercjonują za płytko), ale człowiek **zatwierdza** — albo
  obchodzimy potrzebę absolutnej wyroczni wzorcami: **testy metamorficzne** (relacje zamiast
  dokładnego wyniku) i **property-based** (LLM proponuje niezmiennik, Hypothesis generuje
  setki wejść). Sekcja 3.8 platformy.
- **Merge testu do `main`** — wygenerowany test staje się źródłem prawdy (regresją) dopiero
  po review. Świeżo wygenerowany test to **niezwalidowane założenie**, nie zaufany artefakt.
- **Akcje mutujące / nieodwracalne** — cokolwiek na środowisku zbliżonym do produkcji,
  akcje wysokiego ryzyka.
- **Self-healing powyżej progu ryzyka** — healing **proponuje PR**, nigdy nie przepisuje
  testu po cichu (inaczej maskuje regresję — najgroźniejszy tryb porażki).
- **Dwuznaczny triage / niskie confidence** — gdy sygnały się nie zgadzają, decyduje człowiek.

## Jak technicznie wpiąć człowieka: interrupt → review → resume

Mechanizm to **approval gate** w control plane (LangGraph), nie ad-hoc maile:

```text
graf przebiegu (LangGraph)
   → węzeł generacji/triage/healing produkuje propozycję + confidence + dowody
   → węzeł APPROVAL GATE:
        if risk(action) <= próg AND confidence >= próg:  auto-approve  ─┐
        else:                                                            │
            INTERRUPT  →  zapis stanu (checkpoint)                        │
                       →  zadanie czeka w Review UI (asynchronicznie)     │
                       →  człowiek: approve / reject / edit               │
                       →  RESUME z checkpointu z decyzją człowieka  ──────┤
   → akcja (merge PR / zgłoszenie / kwarantanna)  ◀───────────────────────┘
```

Cechy kluczowe:
- **Asynchroniczność** — `interrupt` zapisuje stan (checkpointer) i **nie blokuje** workera;
  człowiek decyduje, gdy może, a przebieg wznawia się z dokładnie tego miejsca
  (por. [[human-in-the-loop-interrupt-langgraph]], [[interrupts-langgraph]]).
- **Review UI** — człowiek widzi: co AI proponuje, dlaczego (uzasadnienie + dowody:
  diff, trace, screenshot), i jaki jest poziom pewności. Decyzja to approve / reject / **edit**.
- **Audytowalność** — każda decyzja zapisana jako `ReviewDecision` (co proponował AI, co
  zatwierdził człowiek). To dane do kalibracji platformy.

## Budżet zaufania: nie wszystko idzie do człowieka

Gdyby każdy output wymagał człowieka, platforma nic by nie przyspieszyła. Klucz to
**routing po ryzyku i pewności** (zasada 2.4):

| Output AI | Ryzyko | Tryb weryfikacji |
|-----------|--------|------------------|
| Odczyt DOM, propozycja (read-only) | niskie | **automat** |
| Test API z OpenAPI, wysokie confidence | niskie | automat + bramki, merge za approvalem |
| Asercja na wynik biznesowy | wysokie (wyrocznia) | **człowiek** (HITL) |
| Triage „flaky → kwarantanna" | niskie | automat |
| Triage „bug vs zmiana", niskie confidence | wysokie | **człowiek** |
| Self-healing poniżej progu | niskie | automat + log (warning) |
| Self-healing powyżej progu / merge do main | wysokie | **człowiek** (PR review) |

Operacje **read-only** (generacja propozycji, odczyt) idą autonomicznie; **mutujące** (merge,
akcje na środowisku) przechodzą bramkę. To „dawkowanie autonomii": elastyczność tam, gdzie
trzeba eksplorować, twardy kod i bramki tam, gdzie liczy się bezpieczeństwo.

## Pętla uczenia: z czasem mniej ingerencji

Decyzje człowieka (`ReviewDecision`) nie są tylko bramką — to **dane do kalibracji**. Gdy
platforma dowodzi, że w danej klasie zadań jej propozycje są trafne (np. healing selektorów
z confidence > 0.95 akceptowany w 99% przypadków), **podnosisz próg autonomii** dla tej
klasy. Odwrotnie — gdy triage myli się w jakiejś kategorii, obniżasz próg i kierujesz więcej
do człowieka. To jest świadome przesuwanie „budżetu zaufania" w oparciu o evidencję, nie
jednorazowa decyzja.

## Odpowiedź wprost: automatyczna czy ręczna?

**Hybrydowa i warstwowa — i to nie jest wymijająca odpowiedź, tylko konsekwencja problemu
wyroczni:**

- **Automat** robi ciężką pracę: filtruje, waliduje maszynowo sprawdzalne własności
  (kompilacja, schemat, mutation, duplikacja, progi), odrzuca oczywiste przypadki. Dzięki
  temu człowiek nie ogląda 95% outputów.
- **Człowiek jest nieusuwalny** dokładnie na **granicy wyroczni** (co jest „poprawne") i przy
  **akcjach mutujących/nieodwracalnych** (merge do main, akcje na env). Tego nie da się w
  pełni zautomatyzować bez ryzyka cichej regresji.

Pełna autonomia (zero człowieka) w tej domenie to **red flag**: oznacza albo zaufanie
nieugruntowanej wyroczni, albo ciche maskowanie regresji. Cel to **minimalizować** ingerencję
człowieka kalibracją i bramkami — nie eliminować ją.

## Puenta na rozmowę

*„Weryfikacja jest warstwowa. Automat weryfikuje to, co maszynowo sprawdzalne — kompilację,
zgodność ze schematem/OpenAPI, brak duplikacji, mutation testing, progi pewności — i tym
filtruje większość przypadków. Człowiek weryfikuje to, czego AI nie ugruntuje: intencję,
czyli wyrocznię (czy asercja sprawdza właściwą rzecz), oraz autoryzuje akcje mutujące — merge
testu do main, healing powyżej progu. Wpinam go przez approval gate: interrupt zapisuje stan,
zadanie czeka asynchronicznie w Review UI, człowiek approve/reject/edit, graf wznawia się z
checkpointu. Nie wszystko idzie do człowieka — routuję po ryzyku i pewności (budżet zaufania),
a decyzje ludzi kalibrują progi, więc z czasem ingerencji jest mniej. Pełna autonomia tutaj
to red flag — maskowałaby regresje."*

## Powiązane notatki

- [[agentowa-platforma-ai-automatyzacja-qa-e2e]] — budżet zaufania (2.4), asystent asercji HITL (3.8), approval gates w control plane (4.1)
- [[rozroznienie-bledu-od-zmiany-w-wygenerowanym-tescie]] — triage, problem wyroczni, provenance asercji
- [[human-in-the-loop-interrupt-langgraph]] — mechanizm interrupt → review → resume
- [[interrupts-langgraph]] — interrupty i wznawianie z checkpointu
- [[automatyzacja-testow-przygotowanie-rozmowa-ai-engineer]] — problem wyroczni, fundamenty testów
- [[testowanie-rag-techniki-warstwy-frameworki]] — eval-driven dev, golden datasety, LLM-as-a-Judge z kalibracją
