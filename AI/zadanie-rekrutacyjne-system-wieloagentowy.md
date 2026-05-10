# Zadanie rekrutacyjne: System wieloagentowy

## Czym jest to zadanie

Symulowane zadanie rekrutacyjne na stanowisko **AI/ML Engineer** lub **AI Architect**, polegające na zaprojektowaniu systemu wieloagentowego od podstaw. Kandydat nie pisze kodu — przedstawia architekturę, definiuje agentów, przepływy i mechanizmy koordynacji.

## Dlaczego warto ćwiczyć takie zadania

- Rekruterzy coraz częściej pytają o **projektowanie systemów agentowych** zamiast o klasyczne system design.
- Wymaga połączenia wiedzy z zakresu LLM, orkiestracji, obsługi błędów i inżynierii promptów.
- Pokazuje zdolność do myślenia architektonicznego, a nie tylko kodowania.

---

## 🎯 Treść zadania

### Scenariusz: „Autonomiczny Zespół Due Diligence"

Jesteś architektem AI w firmie venture capital. Zarząd zlecił Ci zaprojektowanie **autonomicznego systemu wieloagentowego**, który przeprowadza wstępną analizę due diligence startupu ubiegającego się o finansowanie.

System otrzymuje na wejściu:
- **Pitch deck** startupu (PDF, 10–30 slajdów)
- **Stronę internetową** startupu (URL)
- **Profil założyciela** (link do LinkedIn / bio)
- **Opcjonalnie**: repozytorium GitHub, artykuły prasowe

System powinien wygenerować **raport due diligence** zawierający:

1. **Analiza produktu** — czym jest produkt, jaki problem rozwiązuje, jak wygląda rynek (TAM/SAM/SOM), kto jest konkurencją
2. **Analiza techniczna** — ocena stosu technologicznego, jakości kodu (jeśli repo dostępne), skalowalności rozwiązania
3. **Analiza zespołu** — doświadczenie założycieli, luki kompetencyjne, red flags
4. **Analiza finansowa** — weryfikacja prognoz z pitch decka, porównanie z benchmarkami branżowymi
5. **Analiza sentymentu rynkowego** — co mówi internet o startupie, trendach w branży, potencjalnych zagrożeniach
6. **Ocena ryzyk** — zbiorczy scoring z wagami + lista czerwonych flag
7. **Rekomendacja** — invest / pass / need more info, z uzasadnieniem

### Wymagania do projektu

Kandydat powinien dostarczyć:

#### 1. Definicja agentów
Dla każdego agenta określ:
- **Nazwa i rola** — co robi agent i za co odpowiada
- **Narzędzia (tools)** — z jakich zewnętrznych API/narzędzi korzysta (web scraping, API LinkedIn, GitHub API, GPT-4 do analizy tekstu, kalkulatory finansowe itp.)
- **Wejście i wyjście** — co dostaje na wejściu, co produkuje na wyjściu (format danych)
- **Prompt systemowy** — zarys promptu definiującego zachowanie agenta
- **Ograniczenia** — limity czasowe, budżetowe (tokeny), zakres odpowiedzialności

#### 2. Architektura przepływu
- **Diagram przepływu** (np. Mermaid) pokazujący kolejność działań agentów
- Zidentyfikuj, które zadania mogą być wykonywane **równolegle** (fan-out), a które wymagają **sekwencyjnego** przetwarzania
- Wskaż punkty **synchronizacji** (fan-in), gdzie wyniki są agregowane
- Określ, czy stosujesz wzorzec **Supervisor**, **Planner**, **Hierarchiczny**, czy inny — i uzasadnij wybór

#### 3. Zarządzanie stanem
- Zdefiniuj **wspólny stan** (shared state) — jakie dane przepływają między agentami
- Jak wygląda **schemat stanu** (TypedDict / Pydantic model)
- Jak agenci **aktualizują stan** — czy używają reducerów, nadpisują pola, czy dodają do list

#### 4. Obsługa błędów i edge cases
- Co się dzieje, gdy:
  - Agent nie może pobrać danych ze strony (np. strona za paywallem)
  - GitHub repo jest prywatne
  - Pitch deck jest w języku innym niż angielski
  - Dwa agenty produkują sprzeczne wnioski
  - LLM halucynuje i wymyśla dane finansowe
- Jak system **waliduje** wyniki agentów przed włączeniem do raportu końcowego

#### 5. Human-in-the-Loop
- Zidentyfikuj **punkty decyzyjne**, w których człowiek powinien zatwierdzić / odrzucić / skorygować wynik agenta
- Jak wygląda mechanizm **interrupt → review → resume**
- Czy analityk może **nadpisać** ocenę agenta, i jak to wpływa na resztę przepływu

#### 6. Aspekty produkcyjne
- **Persistence** — jak zachować stan między sesjami (jaki checkpointer)
- **Koszty** — szacunkowy koszt analizy jednego startupu (liczba tokenów, wywołań API)
- **Czas** — szacunkowy czas przetwarzania z podziałem na fazy
- **Bezpieczeństwo** — jak chronić wrażliwe dane startupu, kto ma dostęp do raportów
- **Monitoring** — jak logować decyzje agentów, jak debugować błędne analizy

---

## 🧪 Kryteria oceny

| Kryterium | Waga | Opis |
|-----------|------|------|
| Kompletność architektury | 25% | Czy wszystkie wymagane elementy zostały zaadresowane |
| Jakość definicji agentów | 20% | Czy agenci mają jasno zdefiniowane role, narzędzia i granice |
| Realizm techniczny | 20% | Czy rozwiązanie jest implementowalne z istniejącymi narzędziami |
| Obsługa błędów | 15% | Czy kandydat przewidział edge cases i zaproponował rozwiązania |
| Myślenie produkcyjne | 10% | Koszty, bezpieczeństwo, monitoring, skalowalność |
| Komunikacja | 10% | Czytelność diagramów, jasność opisu, struktura dokumentu |

---

## 💡 Wskazówki dla kandydata

- Nie musisz pisać kodu — to jest **zadanie architektoniczne**
- Użyj diagramów Mermaid do wizualizacji przepływów
- Pokaż, że rozumiesz trade-offy (np. równoległość vs. zależności danych)
- Nie bój się powiedzieć „tu potrzebny jest człowiek" — nadmierna autonomia to red flag
- Skup się na tym, **dlaczego** wybrałeś dany wzorzec, a nie tylko **co** wybrałeś
- Pomyśl o tym, jak system zachowa się przy 100 startupach dziennie, nie tylko przy jednym

---

## Powiązane tematy

- [Wzorce projektowe systemów agentowych](wzorce-projektowe-systemow-agentowych.md)
- [Multi-Agent Supervisor LangGraph](multi-agent-supervisor-langgraph.md)
- [Agentic Workflows i Multi-Agent Orchestration](agentic-workflows-multi-agent-orchestration.md)
- [Obsługa błędów w systemach wieloagentowych](obsluga-bledow-system-wieloagentowy.md)
- [Human-in-the-Loop w LangGraph](human-in-the-loop-interrupt-langgraph.md)
- [Narzędzia dla agentów (Tool Use)](narzedzia-dla-agentow-tool-use-langgraph.md)
- [Równoległe węzły (Fan-out/Fan-in)](rownolegle-wezly-fan-out-fan-in-langgraph.md)
- [Streaming w LangGraph](streaming-langgraph.md)
