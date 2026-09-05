---
tags: [ai-agents, testing, qa, e2e, scalability, architecture, cost, interview]
date: 2026-06-08
---
# Jak skalować platformę QA pod większe obciążenie

Pytanie w kontekście [[agentowa-platforma-ai-automatyzacja-qa-e2e]]: jak ta platforma ma
działać przy **większym obciążeniu**? Najpierw doprecyzuj, co rośnie — bo „obciążenie" ma tu
kilka osi, a każda skaluje się inaczej.

## Co właściwie rośnie (osie obciążenia)

- **Liczba testów / wielkość suite** — więcej deterministycznych regresji w CI.
- **Liczba PR-ów / przebiegów CI** — więcej równoległych żądań generacji, triage, healingu.
- **Wielkość repo testowego** — większy indeks RAG (knowledge layer).
- **Liczba równoległych eksploracji agentowych** — najdroższa, najbardziej zasobożerna oś.
- **Bursty** — nocny przebieg CI albo „wszyscy mergują przed releasem" = piki, nie stały ruch.

**Kluczowa obserwacja na rozmowę:** prawdziwym sufitem przy skali **nie jest CPU/RAM, tylko
koszt i latencja LLM-a** (zwłaszcza AI-online: agent eksploracyjny, vision, self-healing).
Skalowanie tej platformy to w 80% **redukcja drogiej pracy AI**, a dopiero potem klasyczne
poziome skalowanie infrastruktury.

## Lever 0 (najważniejszy): skaluj przez NIE-uruchamianie drogiej pracy AI

Zanim dorzucisz maszyny, wykorzystaj zasady projektowe platformy — to one decydują o
skalowalności bardziej niż infra:

- **Krystalizacja (2.1)** — agent odkrywa *raz*, a skrystalizowany, deterministyczny test
  biega w CI *zawsze*. Najtańsze obciążenie to to, którego nie puszczasz jako agenta na żywo.
  Im więcej trajektorii skrystalizowanych, tym mniej AI-online przy każdym przebiegu.
- **Shift-down (2.5)** — generuj przede wszystkim tanie, deterministyczne testy API/kontraktowe,
  a kosztowne E2E rezerwuj dla nielicznych krytycznych ścieżek. To redukuje flakiness i koszt
  *u źródła*, zamiast skalować drogie E2E.
- **Offline ponad online (2.2)** — wszystko, co da się zrobić poza ścieżką wykonania
  (generacja, triage, auto-naprawa jako PR), rób offline w batchu, nie w czasie testu.

Innymi słowy: **najlepsza optymalizacja skali jest architektoniczna**, nie sprzętowa.

## Skalowanie warstwa po warstwie

| Warstwa | Wąskie gardło przy skali | Jak skalować |
|---------|--------------------------|--------------|
| **Execution (farma runnerów)** | Liczba równoległych testów E2E | Kontenery + K8s **HPA**; sharding/balansowanie suite; **efemeryczne env per-PR**; izolacja danych (per-tenant/user, rollback) → bezpieczne zrównoleglanie |
| **AI offline (generacja/triage)** | Throughput zadań, koszt tokenów | **Bezstanowe workery za kolejką**, skalowane poziomo; batching; model routing; cache; async |
| **AI online (agent/vision/healing)** | Koszt i latencja per-krok | **Minimalizuj** (Lever 0); cache decyzji healingu; heurystyki/embeddingi **przed** LLM; progi pewności; krystalizacja |
| **Knowledge layer (RAG)** | Rozmiar indeksu, latencja retrievalu | Vector DB z indeksem ANN (HNSW/IVF), repliki/sharding; **indeksowanie inkrementalne** przy merge, nie pełny reindeks; cache embeddingów |
| **Control plane (orkiestracja)** | SPoF + przepustowość huba | **Hub bezstanowy + stan w bazie + repliki + kolejka** — patrz [[architektura-agentowa-50-serwerow-hub-and-spoke]] |
| **Data / observability** | Wolumen artefaktów, koszt trace'ów | Object storage (S3) na trace/screenshoty; **sampling** trace'ów; polityki retencji; monitoring kosztu |

### Execution layer — najprostsza do poziomego skalowania
E2E jest „embarrassingly parallel", jeśli testy są **izolowane**. Klucz to izolacja danych
(osobny user/tenant/transakcja z rollbackiem), żeby N runnerów nie deptało sobie po stanie.
K8s z autoskalowaniem podów, efemeryczne środowiska per-PR stawiane z kontenerów i kasowane
po teście. Balansowanie czasu suite (test splitting), żeby najdłuższe testy nie wydłużały
całego przebiegu.

### AI offline — wzorzec kolejka + bezstanowe workery
To jest dokładnie **hub-and-spoke z [[architektura-agentowa-50-serwerow-hub-and-spoke]]**:
control plane (LangGraph) wrzuca zadania generacji/triage do kolejki, pula bezstanowych
workerów je pulluje, autoskalowanie po **głębokości kolejki**. Bursty (nocne CI) lądują w
buforze kolejki, a nie wywracają systemu. Hub bezstanowy + checkpointy → repliki + brak SPoF.

### AI online — tu pilnujesz kosztu, nie throughputu
Agent eksploracyjny i vision są drogie per-krok. Skalowanie = **kontrola, nie mnożenie**:
cache wyników healingu (ten sam zmieniony selektor naprawiasz raz), tania heurystyka/embedding
**przed** wywołaniem LLM, progi pewności (poniżej progu → fallback, nie kolejne wywołania),
twarde limity kroków/tokenów/czasu. I znów: krystalizuj, żeby online biegało rzadziej.

## Koszt jako twardy sufit skali

Przy skali rachunek za tokeny dominuje nad rachunkiem za compute. Dźwignie kosztowe:

- **Model routing / kaskadowanie** — tani/mały model do prostych kroków (większość),
  silny/drogi tylko do trudnych. Por. [[wyjasnij-teraz-model-routing-kaskadowanie-modeli]].
- **Caching** — prompt cache, cache retrievalu RAG, cache decyzji healingu, memoizacja
  identycznych wywołań. Cache nie może jednak maskować potrzeby świeżych danych.
- **Batching offline** — generacja i triage poza ścieżką krytyczną można grupować i puszczać
  w tańszym, wolniejszym trybie.
- **Krystalizacja** (znowu) — najtańszy token to ten, którego nie wywołujesz, bo test jest
  już deterministyczny.

## Autoskalowanie: na czym oprzeć trigger

- **Głębokość kolejki** zadań AI-offline → skaluj pulę workerów generacji/triage.
- **Liczba oczekujących przebiegów E2E** → skaluj farmę runnerów (HPA).
- **Harmonogram** — predykcyjnie podnoś pojemność przed nocnym CI / oknem release'owym,
  zamiast reagować po fakcie na pik.
- **Rate limit LLM API** — globalny limiter/token bucket na hubie, **nie** lokalny retry w
  każdym workerze (inaczej retry storm przy fan-out).

## HITL nie skaluje się liniowo — pamiętaj o tym wąskim gardle

Gdy wolumen rośnie, **człowiek w pętli staje się wąskim gardłem**, jeśli każdy output wymaga
review. Skalowanie HITL to nie „więcej ludzi", tylko **podnoszenie progów autonomii w oparciu
o kalibrację** (por. [[human-in-the-loop-platforma-qa-weryfikacja]]): klasy zadań, w których
platforma dowiodła trafności, przechodzą automatycznie; człowiek skupia się na granicy
wyroczni i akcjach mutujących. Bez tego skala rozbije się o przepustowość recenzentów, nie o
infrastrukturę.

## Czego pilnować przy skali (tryby porażki)

- **Retry storm** przy fan-out na LLM API (`429`) — globalny limiter, backoff+jitter.
- **Pełny reindeks RAG** jako koszt rosnący z repo — rób inkrementalnie przy merge.
- **Eksplozja artefaktów** (trace/wideo) — retencja + sampling, inaczej storage i koszt rosną liniowo.
- **Dryf jakości pod presją throughputu** — eval-driven dev (sekcja 9 platformy) bramkuje, żeby
  „szybciej" nie znaczyło „gorsze testy".
- **Flakiness rosnący z równoległością** — izolacja danych i auto-waiting, nie więcej maszyn.

## Puenta na rozmowę

*„Najpierw doprecyzowuję, co rośnie — liczba testów, PR-ów, eksploracji — i zaznaczam, że
sufitem przy skali jest koszt/latencja LLM, nie CPU. Dlatego skaluję najpierw architektonicznie:
krystalizuję (agent odkrywa raz, deterministyczny test biega zawsze), spycham logikę w dół do
tanich testów API i robię maksimum offline. Potem klasyka: execution layer poziomo na K8s z
izolacją danych, AI-offline jako bezstanowe workery za kolejką z autoskalowaniem po głębokości
kolejki — czyli hub-and-spoke. AI-online trzymam w ryzach cache'em, progami i model routingiem,
bo to tam jest koszt. Knowledge layer to vector DB z indeksowaniem inkrementalnym. I pamiętam,
że HITL nie skaluje się liniowo — podnoszę progi autonomii kalibracją, żeby człowiek nie stał
się wąskim gardłem."*

## Powiązane notatki

- [[agentowa-platforma-ai-automatyzacja-qa-e2e]] — krystalizacja (2.1), shift-down (2.5), execution layer (4.5), stos (6)
- [[architektura-agentowa-50-serwerow-hub-and-spoke]] — skalowanie agentów: kolejka, bezstanowy hub, autoskalowanie, backpressure
- [[human-in-the-loop-platforma-qa-weryfikacja]] — HITL jako wąskie gardło, kalibracja progów autonomii
- [[wyjasnij-teraz-model-routing-kaskadowanie-modeli]] — kaskadowanie modeli jako dźwignia kosztowa
- [[budowa-pipeline-danych-i-praca-w-skali-produkcyjnej]] — praca w skali produkcyjnej, pipeline danych
- [[benchmarki-ewaluacja-koszt-skalowalnosc-ml-ai]] — koszt i skalowalność systemów ML/AI
- [[indeksowanie-w-bazach-qdrant]] — indeksy ANN i skalowanie vector DB
