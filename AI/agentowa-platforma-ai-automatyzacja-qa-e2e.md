---
tags: [ai-agents, testing, qa, e2e, platform, langgraph, architecture]
date: 2026-06-07
---
# Agentowa platforma AI do automatyzacji workflow QA (E2E) — propozycja

Mój pomysł na platformę, która łączy klasyczną automatyzację testów (E2E, API) z agentami AI tak, by **realnie obniżyć dwa największe koszty testowania**: pisanie testów i ich utrzymanie (maintenance + flakiness). To nie jest „wciśnięcie AI gdzie się da", tylko świadome nałożenie LLM-ów i agentów na **cykl życia testu** — z zachowaniem twardej zasady, że źródłem prawdy pozostaje deterministyczny, wersjonowany artefakt, a nie nondeterministyczny przebieg modelu.

Dokument zakłada kontekst z [[automatyzacja-testow-przygotowanie-rozmowa-ai-engineer]] (fundamenty testów, E2E, API, gdzie AI wnosi wartość) oraz [[pytania-rekrutacyjne-ai-agents]] (architektura agentów). Tutaj składam to w **konkretną wizję produktu**: funkcje, architekturę, stos technologiczny i etapy wdrożenia.

## Spis treści

- [1. Problem i teza](#1-problem-i-teza)
- [2. Zasady projektowe (fundament całej platformy)](#2-zasady-projektowe-fundament-całej-platformy)
- [3. Proponowane funkcje (mapowane na cykl życia testu)](#3-proponowane-funkcje-mapowane-na-cykl-życia-testu)
- [4. Architektura](#4-architektura)
- [5. Kluczowe przepływy end-to-end](#5-kluczowe-przepływy-end-to-end)
- [6. Stos technologiczny (z uzasadnieniem)](#6-stos-technologiczny-z-uzasadnieniem)
- [7. Model danych i kontrakty](#7-model-danych-i-kontrakty)
- [8. Bezpieczeństwo, guardrails, budżet zaufania](#8-bezpieczeństwo-guardrails-budżet-zaufania)
- [9. Ewaluacja samej platformy (poziom meta)](#9-ewaluacja-samej-platformy-poziom-meta)
- [10. Ryzyka i trade-offy](#10-ryzyka-i-trade-offy)
- [11. Roadmapa wdrożenia (MVP → dojrzałość)](#11-roadmapa-wdrożenia-mvp--dojrzałość)
- [12. Powiązane notatki](#12-powiązane-notatki)

## 1. Problem i teza

**Co boli w automatyzacji testów dzisiaj** (rozwinięcie w [[automatyzacja-testow-przygotowanie-rozmowa-ai-engineer]]):

- **Utrzymanie E2E dominuje koszt** — każda zmiana UI unieważnia kruche selektory, a testy pęka się szybciej, niż zespół nadąża je naprawiać.
- **Flakiness niszczy zaufanie** — niedeterministyczne testy maskują prawdziwe regresje („znowu czerwony, puść jeszcze raz").
- **Pisanie testów jest wolne** — pokrycie przypadków brzegowych wymaga czasu eksperta, którego zwykle brakuje.
- **Problem wyroczni (oracle problem)** — żeby napisać asercję, ktoś musi wiedzieć, jak system *powinien* się zachować; to wąskie gardło wiedzy, nie tylko pisania.
- **Triage awarii jest ręczny** — po nocnym przebiegu CI ktoś musi przejrzeć dziesiątki czerwonych testów i rozdzielić realne buggi od flaków i od zmian wymagań.

**Teza platformy:** AI najmocniej zwraca się tam, gdzie wejście jest **ustrukturyzowane i czytelne maszynowo** (kod, OpenAPI, DOM, artefakty awarii), a nie tam, gdzie panuje dwuznaczność intencji. Dlatego platforma celuje w generowanie, utrzymanie, self-healing i triage — a *intencję* (co jest poprawne) trzyma po stronie człowieka i wymagań. Cała wartość jest ograniczona przez to, jak dobrze radzimy sobie z problemem wyroczni — stąd nacisk na grounding i human-in-the-loop.

## 2. Zasady projektowe (fundament całej platformy)

Te zasady przewijają się przez każdą funkcję i każdą decyzję architektoniczną. Bez nich powstaje „zabawka", która generuje ładne demo i niestabilną produkcję.

### 2.1 Krystalizacja: AI odkrywa, deterministyczny kod utrwala

Najważniejsza zasada. Generator (LLM/agent) jest z natury **niedeterministyczny**, ale *wygenerowany* test musi być w pełni deterministyczny. Dlatego nondeterministycznego przebiegu nigdy nie traktujemy jako zestawu regresyjnego. Schemat:

```text
   FAZA ODKRYCIA (AI, offline/online, niedeterministyczna)
   agent eksploruje • LLM generuje • multimodal ocenia
                    │
                    ▼  KRYSTALIZACJA (kompilacja do artefaktu)
   FAZA REGRESJI (deterministyczna, wersjonowana w repo)
   skompilowany test Playwright/REST • stałe selektory • zamrożone dane
                    │
                    ▼
   CI uruchamia ZAWSZE wersję deterministyczną, nie agenta na żywo
```

Konsekwencja: język naturalny i agent to **interfejs/odkrywca**, a źródłem prawdy jest skompilowany, deterministyczny test w repo.

### 2.2 AI offline vs AI online

To rozróżnienie decyduje o wymaganiach co do latencji, kosztu i determinizmu:

- **AI offline** — poza ścieżką wykonania testu (generowanie, projektowanie przypadków, auto-naprawa jako PR, analiza pokrycia). Można użyć drogiego, wolnego modelu; nondeterminizm jest akceptowalny, bo wynik i tak przechodzi review.
- **AI online** — w czasie działania testu (self-healing locator, agent eksplorujący). Tu liczy się latencja, koszt per-krok i obserwowalność; nondeterminizm jest ryzykiem, więc obwarowany progami pewności i logowaniem.

Platforma fizycznie rozdziela te dwa światy na osobne serwisy (sekcja 4).

### 2.3 Grounding ponad rozmiar modelu

Naiwna generacja ignorująca repozytorium produkuje testy, które się nie kompilują, dublują istniejące i łamią konwencje. Lekarstwo to **RAG nad repo testów** (page objects, fixtury, helpery, OpenAPI, przewodnik stylu) + **context engineering** + **structured output**. Jakość wygenerowanego testu zależy bardziej od jakości kontekstu niż od rozmiaru modelu. Por. [[testowanie-rag-techniki-warstwy-frameworki]].

### 2.4 Budżet zaufania i human-in-the-loop

Autonomię dawkujemy tam, gdzie potrzeba elastyczności (eksploracja), a resztę „zabijamy" deterministycznym kodem i bramkami. Operacje **read-only** (odczyt DOM, generacja propozycji) mogą iść autonomicznie; **mutujące** (merge testu do main, akcje na środowisku zbliżonym do produkcji) przechodzą przez approval gate. Self-healing nigdy nie przepisuje testu po cichu — proponuje poprawkę do akceptacji.

### 2.5 Shift-down: maksimum logiki poniżej E2E

Platforma aktywnie spycha weryfikację w dół piramidy: generuje przede wszystkim testy **API/kontraktowe** (deterministyczne, opisane OpenAPI — najłatwiejszy i najmniej ryzykowny target dla LLM), a kosztowne E2E rezerwuje dla nielicznych krytycznych ścieżek. To zmniejsza powierzchnię flakiness u źródła.

## 3. Proponowane funkcje (mapowane na cykl życia testu)

Funkcje porządkuję wg cyklu: **projektowanie → authoring → wykonanie → utrzymanie → diagnoza**. Każda mówi, czy jest offline czy online i jaką ma bramkę zaufania.

### 3.1 Generowanie testów z groundingiem `[offline]`

Generacja z czterech źródeł, każde o innym profilu wartości i ryzyka:

| Źródło | Wartość | Ryzyko / uwaga |
|---|---|---|
| **Wymagania / user stories** | Najwyższa — opisuje *intencję* (to, czego brak wyroczni) | Wymaga, by wymagania istniały i były precyzyjne |
| **OpenAPI / kontrakt** | Wysoka — ustrukturyzowane, deterministyczne, łatwa walidacja schematu | Najlepszy punkt startu (MVP) |
| **Kod** | Szybka | Over-fitting/tautologia — utrwala istniejące buggi (OK tylko dla characterization tests) |
| **Ruch produkcyjny / logi** | Realistyczne wzorce i dane | Wymaga anonimizacji danych wrażliwych |
| **Raport błędu** | Test reprodukujący (regression) | Najpierw failuje, po naprawie pilnuje |

Generator stosuje świadomie techniki projektowania przypadków (klasy równoważności, wartości brzegowe, tablice decyzyjne, pairwise) i emituje **structured output** w DSL projektu albo wprost w kodzie Playwright/REST. Wynik trafia do review (problem wyroczni — generacja wspiera autora, nie jest autopilotem).

### 3.2 Authoring w języku naturalnym `[offline]`

Most NL ↔ test działa w obie strony:

- **Opis → test**: tester manualny / PO opisuje scenariusz po ludzku, platforma **kompiluje** go do deterministycznego, wersjonowanego artefaktu (ewolucja BDD/Gherkin, ale bez sztywnej składni). Klucz: nie odpalamy opisu na żywo przy każdym przebiegu — kompilujemy raz.
- **Test → opis**: z istniejącego testu generujemy czytelną dokumentację „co ten test sprawdza", raport pokrycia w języku biznesu i traceability wymaganie↔test.

### 3.3 Agentowe E2E eksploracyjne `[online]`

Agent dostaje cel („dokończ zakup", „znajdź zepsute stany") i działa w pętli *postrzegaj → decyduj → działaj*, gdzie **runner (Playwright) jest narzędziem (tool)**: `click`, `fill`, `read_dom`, `screenshot`. Odkrywa ścieżki i przypadki brzegowe, których nikt nie oskryptował. Architektonicznie: planner/executor/krytyk + guardrails (żadnych destrukcyjnych akcji, praca w piaskownicy). Wynik wartościowych ścieżek **krystalizuje się** w deterministyczne regresje (zasada 2.1). Por. [[pytania-rekrutacyjne-ai-agents]], [[multi-agent-supervisor-langgraph]].

### 3.4 Self-healing locators `[online]`

Bezpośrednia odpowiedź na kruchość selektorów. Przy pisaniu zapamiętujemy o elemencie wiele cech (tekst, rola, dostępna nazwa, sąsiedzi, pozycja, embedding); po zmianie DOM dopasowujemy najlepszego kandydata heurystyką/embeddingiem/LLM-em. **Granice zaufania**: healing musi być obserwowalny (logowany jako warning), przeglądalny (proponuje poprawkę do akceptacji, nie przepisuje po cichu) i ograniczony progiem pewności — lepiej, by test padł, niż żeby zamaskował realną regresję.

### 3.5 Auto-naprawa testów jako PR `[offline]`

Gdy test pęka z powodu zmiany UI/API (a nie realnego błędu), platforma analizuje diff i otwiera **pull request** z zaktualizowanym selektorem/asercją/testem. Dodatkowo: wykrywanie i refaktoryzacja kruchych testów, usuwanie martwych i zduplikowanych, synchronizacja testów API ze zmianą w OpenAPI. Wszystko przez review — to offline, więc nondeterminizm jest bezpieczny.

### 3.6 Testy wizualne, UI i a11y z modelem multimodalnym `[online/offline]`

Vision czyta zrzuty ekranu i DOM:

- **Regresja wizualna ponad pixel-diff** — model ocenia *semantyczną* równoważność („czy to wciąż ta sama, poprawna strona?"), odróżniając zmianę zamierzoną od regresji i tnąc fałszywe alarmy.
- **Walidacja UI** — czy ekran odpowiada projektowi, czy układ się nie rozjechał.
- **Dostępność (a11y)** — braki alt-tekstu, słaby kontrast, nielogiczna struktura, poza tym, co złapie checker regułowy.

Vision pełni rolę **sędziego/triage**, a deterministyczne punkty odniesienia (baseline) trzymamy tam, gdzie się da.

### 3.7 Inteligentny triage awarii `[offline]`

Po przebiegu CI platforma klasteryzuje i klasyfikuje awarie na podstawie bogatych artefaktów (trace, DOM, zrzuty, logi sieci): **realny bug vs flaky vs zmiana wymagań vs zepsute środowisko**. Grupuje powiązane porażki (jedna przyczyna źródłowa → N czerwonych testów), proponuje przyczynę i kieruje do właściwej akcji (PR naprawiający, zgłoszenie buga, oznaczenie flaky do kwarantanny). To największa oszczędność czasu człowieka w codziennej pracy.

### 3.8 LLM jako asystent asercji `[offline, HITL]`

Najbardziej ryzykowne i najbardziej wartościowe — bezpośrednie zmierzenie się z wyrocznią. LLM proponuje asercje (autorzy notorycznie asercjonują za płytko), ale zawsze przez wzorce omijające potrzebę absolutnej wyroczni: **HITL** (człowiek zatwierdza), **testy metamorficzne** (relacje zamiast dokładnego wyniku), **property-based** (model proponuje niezmienniki, Hypothesis/jqwik generuje setki wejść).

## 4. Architektura

Architektura rozdziela **control plane** (orkiestracja, decyzje), **AI services** (offline i online osobno), **knowledge layer** (grounding), **execution layer** (farma runnerów + efemeryczne środowiska) i **data/observability**.

```text
┌──────────────────────────────────────────────────────────────────────────┐
│                              UŻYTKOWNICY                                    │
│   QA / Dev / PO  •  CI/CD (GitHub Actions)  •  Dashboard + Review UI        │
└───────────────┬───────────────────────────────────────┬───────────────────┘
                │ API (REST/GraphQL) + webhooki          │ HITL / approvale
                ▼                                         ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                    CONTROL PLANE  (orkiestracja — LangGraph)               │
│  • routing zadań  • stan przebiegu + checkpointing  • warunki stopu/limity │
│  • approval gates (HITL)  • polityki / budżet zaufania                      │
└───────┬───────────────────────┬───────────────────────┬───────────────────┘
        │                       │                        │
        ▼                       ▼                        ▼
┌───────────────┐   ┌────────────────────────┐   ┌────────────────────────┐
│  AI OFFLINE    │   │  AI ONLINE             │   │  KNOWLEDGE LAYER (RAG)  │
│  (generation)  │   │  (runtime)             │   │  • repo testów / POM    │
│ • z wymagań    │   │ • self-healing locator │   │  • fixtury, helpery     │
│ • z OpenAPI    │◀─▶│ • agent eksploracyjny  │◀─▶│  • OpenAPI / kontrakty  │
│ • z kodu/ruchu │   │ • multimodal sędzia    │   │  • przewodnik stylu     │
│ • triage/PR    │   │   (vision)             │   │  • vector DB + indeks    │
└───────┬───────┘   └───────────┬────────────┘   └────────────────────────┘
        │                       │
        ▼                       ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                          EXECUTION LAYER                                   │
│  • farma runnerów: Playwright / Selenium Grid (kontenery)                  │
│  • efemeryczne środowiska per-PR (Docker/K8s, testcontainers)             │
│  • izolacja danych (osobny user/tenant per test), zrównoleglanie           │
└───────────────┬───────────────────────────────────────────────────────────┘
                │ artefakty: trace, DOM, screenshoty, wideo, logi
                ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                    DATA  +  OBSERVABILITY  +  EVAL                          │
│  • golden datasety (wersjonowane)  • store artefaktów awarii               │
│  • tracing przebiegów agentów (LangSmith/Phoenix)  • metryki + koszt        │
│  • eval-driven dev: ocena JAKOŚCI samej platformy (sekcja 9)               │
└──────────────────────────────────────────────────────────────────────────┘
```

### 4.1 Control plane (orkiestracja)

Serce platformy. W **LangGraph** jako graf węzłów: routuje zadania (generacja vs triage vs healing), trzyma stan przebiegu z **checkpointingiem** (wznawianie, time-travel debug), egzekwuje twarde warunki stopu (max kroków, budżet tokenów, timeout) i wstrzykuje **approval gates** (interrupt → decyzja człowieka → resume). Tu mieszka „budżet zaufania" jako polityka.

### 4.2 AI offline service (generation)

Bezstanowe workery przyjmujące zadanie generacji/triage/auto-naprawy. Każdy: pobiera kontekst z knowledge layer (RAG), woła model przez warstwę abstrakcji (model routing: tańszy do prostych kroków, silniejszy do trudnych), emituje **structured output**, otwiera PR. Nondeterminizm bezpieczny — wynik idzie do review.

### 4.3 AI online service (runtime)

Niskolatencyjne serwisy wołane *w trakcie* testu: self-healing locator (z progiem pewności i logowaniem), agent eksploracyjny (pętla z runnerem-jako-tool), multimodalny sędzia wizualny. Wydzielone, bo mają zupełnie inny SLA niż offline.

### 4.4 Knowledge layer (grounding)

Indeks repozytorium testowego: page objects, fixtury, helpery, konwencje nazewnicze, OpenAPI, przewodnik stylu — w bazie wektorowej + metadane. To on sprawia, że generacja reużywa istniejące komponenty, trzyma nazewnictwo i nie duplikuje pokrycia. Aktualizowany inkrementalnie przy każdym merge.

### 4.5 Execution layer

Farma runnerów w kontenerach (Playwright preferowany dla auto-waitingu i trace viewera; Selenium Grid dla szerokiego pokrycia przeglądarek). **Efemeryczne środowiska per-PR** stawiane z kontenerów i kasowane po teście dają powtarzalność. Izolacja danych (osobny user/tenant/transakcja z rollbackiem) umożliwia bezpieczne zrównoleglanie.

### 4.6 Data, observability, eval

Wersjonowane golden datasety, store bogatych artefaktów awarii (wejście dla triage i multimodala), pełny **tracing** przebiegów agentów (co kluczowe przy diagnozie nieskończonych pętli i dryfu), metryki kosztu/latencji oraz warstwa **eval** oceniająca jakość samej platformy (sekcja 9).

## 5. Kluczowe przepływy end-to-end

**A. Od wymagania do testu (offline):**

```text
user story + kryteria akceptacji
   → control plane routuje do generation
   → RAG dociąga istniejące POM/fixtury/OpenAPI + przewodnik stylu
   → LLM generuje test (structured output, techniki: boundary/pairwise)
   → walidacja: kompiluje się? przechodzi schemat? nie duplikuje pokrycia?
   → PR + propozycja asercji (HITL)
   → human review → merge → reindeks knowledge layer
```

**B. Od awarii CI do naprawy (offline triage + auto-fix):**

```text
nocny przebieg CI → N czerwonych testów + artefakty (trace/DOM/screenshot)
   → triage klastruje i klasyfikuje: real bug / flaky / zmiana UI / zepsute env
   → dla „zmiana UI": auto-naprawa otwiera PR z nowym selektorem
   → dla „real bug": generacja testu regresyjnego + zgłoszenie
   → dla „flaky": kwarantanna + diagnoza synchronizacji
   → wszystko przez review (offline = nondeterminizm bezpieczny)
```

**C. Agent odkrywa → krystalizacja (online → offline):**

```text
cel: „eksploruj checkout i znajdź zepsute stany"
   → agent w pętli (perceive DOM → decide → act przez runner-tool)
   → znajduje ścieżkę prowadzącą do błędu
   → control plane KRYSTALIZUJE trajektorię w deterministyczny test Playwright
   → test trafia do PR jako nowa regresja (już NIE agent na żywo)
```

## 6. Stos technologiczny (z uzasadnieniem)

Konkretne narzędzia traktuję jako reprezentantów kategorii — wymienne, ale to są moje domyślne wybory.

| Warstwa | Wybór | Dlaczego |
|---|---|---|
| **Orkiestracja agentów** | LangGraph | Graf węzłów, checkpointing, conditional edges, natywny HITL (interrupt/resume), tracing przez LangSmith |
| **Warstwa LLM** | Abstrakcja + routing (Claude / GPT klasy reasoning) | Model routing: tani do prostych kroków, silny do trudnych; structured output; wersjonowanie promptów |
| **Walidacja I/O** | Pydantic / JSON Schema | Argumenty narzędzi i structured output walidowane na granicy; jedna definicja = schemat + walidator |
| **Runner E2E** | Playwright (primary), Selenium Grid (cross-browser) | Auto-waiting tnie flakiness; trace viewer = złoty standard diagnostyki; Selenium dla szerokiego pokrycia |
| **Testy API** | REST Assured / supertest / pytest+requests, schema z OpenAPI | Tańszy i stabilniejszy niż E2E; walidacja kontraktu względem schematu |
| **Testy kontraktowe** | Pact (consumer-driven) | Integracja bez kruchego pełnego E2E; łamanie kontraktu wychodzi tanio i wcześnie |
| **Property/metamorficzne** | Hypothesis (Py) / jqwik (JVM) | Deterministyczna maszyneria pod niezmienniki proponowane przez LLM |
| **Knowledge / RAG** | Vector DB (pgvector/Qdrant) + indekser repo | Grounding generacji w realnym repo testów i OpenAPI |
| **Środowiska** | Docker + Kubernetes + Testcontainers | Efemeryczne env per-PR, powtarzalność, izolacja |
| **CI/CD** | GitHub Actions + bramki na evalach | Auto-naprawa jako PR, progi jakości jako gate (eval-driven) |
| **Observability** | LangSmith / Arize Phoenix; Allure dla raportów | Tracing agentów, koszt/latencja, raporty awarii z trendami |
| **Multimodal** | Model vision (Claude / GPT-4o klasy) | Regresja semantyczna, walidacja UI, a11y ze zrzutów |

## 7. Model danych i kontrakty

Kilka pierwszorzędnych encji, na których stoi platforma:

- **TestSpec** — intencja w języku biznesu (z user story lub opisu NL) + traceability do wymagania. Wejście do generacji.
- **CompiledTest** — deterministyczny, wersjonowany artefakt (kod Playwright/REST). *Źródło prawdy.* Powiązany z TestSpec.
- **GoldenDataset** — wersjonowane pary referencyjne (wejście → oczekiwanie) do ewaluacji generacji i retrievalu; bramkują merge.
- **RunArtifact** — bogaty zapis awarii (trace, DOM, screenshot, wideo, logi). Wejście dla triage i multimodala.
- **HealingEvent** — log każdego self-healingu (stary→nowy selektor, pewność, decyzja człowieka). Audytowalność „budżetu zaufania".
- **ReviewDecision** — ślad HITL: co zaproponował AI, co zatwierdził człowiek. Dane do kalibracji platformy.

Kontrakty wewnętrzne (między serwisami) opisane schematami — to pozwala walidować I/O LLM-a na granicy i wersjonować zmiany.

## 8. Bezpieczeństwo, guardrails, budżet zaufania

- **Sekrety** — nigdy w kodzie testu; ze zmiennych środowiskowych / menedżera sekretów, maskowane w logach i raportach. Dedykowane konta testowe, nigdy produkcyjne dane.
- **Least privilege dla narzędzi agenta** — runner pracuje w piaskownicy/efemerycznym env; żadnych destrukcyjnych ani nieodwracalnych akcji na środowisku zbliżonym do produkcji.
- **Approval gates** — merge testu do main, akcje mutujące i healing powyżej progu ryzyka przechodzą przez człowieka. Read-only (generacja propozycji, odczyt DOM) — autonomicznie.
- **Idempotentność** — narzędzia mutujące z idempotency key (agent bywa ponawiany); twarde limity (maks. akcji, budżet) jako bezpieczniki.
- **Prompt injection** — treść pobierana ze stron/dokumentów jest danymi, nie instrukcjami; sanityzacja i izolacja kontekstu (zwłaszcza dla agenta eksploracyjnego). Por. [[llm-guardrails]].
- **Anonimizacja** — generacja z ruchu produkcyjnego wymaga maskowania danych wrażliwych przed użyciem.
- **Obserwowalność healingu** — każdy self-healing logowany jako warning z progiem pewności; lepiej kontrolowana porażka niż ciche zamaskowanie regresji.

## 9. Ewaluacja samej platformy (poziom meta)

Skoro platforma generuje testy, sama potrzebuje **eval-driven development** (analogicznie do [[testowanie-rag-techniki-warstwy-frameworki]]). Mierzymy nie „czy testy przechodzą", lecz **czy platforma wytwarza dobre testy**:

- **Jakość generacji** — czy wygenerowany test się kompiluje, nie duplikuje pokrycia, łapie wstrzyknięte buggi (mutation testing jako twardszy sygnał niż samo coverage).
- **Trafność triage** — precision/recall klasyfikacji real-bug vs flaky (golden dataset oznaczonych awarii).
- **Skuteczność self-healingu** — odsetek poprawnych uleczeń vs zamaskowanych regresji (to drugie jest krytyczną metryką bezpieczeństwa).
- **Koszt i latencja** — per generacja / per healing / per przebieg agenta; bramki w CI.
- **LLM-as-a-Judge z kalibracją** — do oceny jakości asercji i opisów, kalibrowany względem próbki ocen ludzkich (uwaga na verbosity / self-enhancement bias).

Progi (np. „skuteczność healingu > 0.95", „zamaskowane regresje < 1%") bramkują wdrożenie zmian w samej platformie — dokładnie jak nieprzechodzący test jednostkowy.

## 10. Ryzyka i trade-offy

- **Zamaskowana regresja przez self-healing** — najgroźniejszy tryb porażki. Mitygacja: progi pewności, obserwowalność, review, metryka „zamaskowanych regresji" w evalu.
- **Tautologia generacji z kodu** — testy utrwalające istniejące buggi. Mitygacja: priorytet generacji z *wymagań*, jawne nazywanie characterization tests.
- **Koszt i latencja AI online** — agent i vision są drogie per-krok. Mitygacja: offline gdzie się da, model routing, caching, krystalizacja (agent raz odkrywa, deterministyczny test biega zawsze).
- **Dryf i nieskończone pętle agenta** — mitygacja: limity kroków/tokenów/czasu, wykrywanie powtórzeń, tracing, HITL przy odchyleniach.
- **Złoty zbiór zbyt łatwy** — zawyża metryki platformy. Mitygacja: pytania multi-hop i negatywne, przegląd ludzkim okiem.
- **Przeinżynierowanie multi-agentem** — zacznij od single-agent z dobrymi narzędziami; dziel dopiero pod realny ból (przeładowany kontekst, potrzeba równoległości). Por. [[pytania-rekrutacyjne-ai-agents]].

## 11. Roadmapa wdrożenia (MVP → dojrzałość)

Kolejność wynika z zasady „najpierw najłatwiejszy i najmniej ryzykowny target":

1. **MVP — generacja testów API z OpenAPI** `[offline]`. Najbardziej ustrukturyzowane, deterministyczne, łatwa walidacja schematu. Najszybszy zwrot, najniższe ryzyko. + RAG nad repo od początku (bez groundingu generacja jest zabawką).
2. **Triage awarii CI** `[offline]`. Druga największa oszczędność czasu, niskie ryzyko (tylko klasyfikacja + propozycja, człowiek decyduje).
3. **Auto-naprawa jako PR + self-healing locators** `[offline + online]`. Atak na koszt utrzymania E2E; self-healing z twardymi granicami zaufania.
4. **Authoring NL → test z kompilacją do artefaktu** `[offline]`. Obniża próg wejścia dla manualnych testerów / PO.
5. **Agent eksploracyjny + krystalizacja** `[online]`. Najbardziej zaawansowane i nondeterministyczne — na końcu, z pełnym tracingiem i guardrailami.
6. **Multimodal: regresja wizualna, walidacja UI, a11y** `[online]`. Domyka pokrycie o obszary niewidoczne dla asercji funkcjonalnych.

Przez cały czas: **eval-driven development samej platformy** (sekcja 9) — bez tego nie da się bezpiecznie iterować.

## 12. Powiązane notatki

- [[automatyzacja-testow-przygotowanie-rozmowa-ai-engineer]] — fundamenty testów, E2E/API, gdzie AI wnosi wartość (baza tej propozycji)
- [[pytania-rekrutacyjne-ai-agents]] — architektura agentów: pętla, tool use, planner/executor, guardrails, multi-agent
- [[testowanie-rag-techniki-warstwy-frameworki]] — eval-driven development, golden datasety, LLM-as-a-Judge (wzorzec dla ewaluacji platformy)
- [[multi-agent-supervisor-langgraph]] — wzorzec supervisor/orchestrator dla części agentowej
- [[orkiestrator-vs-planner-w-architekturze-wieloagentowej]] — rozdział plannera od orkiestratora w control plane
- [[llm-guardrails]] — mechanizmy obronne (prompt injection, sanityzacja) dla agenta eksploracyjnego
- [[mcp-ai-engineer-interview]] — MCP jako standard podłączania narzędzi (runner, repo, OpenAPI) do agentów
