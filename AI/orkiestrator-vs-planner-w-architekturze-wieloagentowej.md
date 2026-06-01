# Orkiestrator vs Planner w Architekturze Wieloagentowej

## Krótko

W systemie wieloagentowym **planner** odpowiada głównie za wymyślenie planu działania, a **orkiestrator** za sterowanie wykonaniem tego planu przez agentów, narzędzia i przepływy systemowe.

Inaczej:
- **Planner** decyduje: *co trzeba zrobić i w jakiej kolejności logicznej*.
- **Orkiestrator** decyduje: *kto, kiedy i jak ma to wykonać oraz co zrobić, gdy coś pójdzie nie tak*.

## Planner

Planner bierze ogólny cel użytkownika i rozbija go na mniejsze, bardziej konkretne kroki.

Przykład celu:

> Przygotuj analizę konkurencji dla produktu SaaS.

Planner może zwrócić plan:

1. Zidentyfikować głównych konkurentów.
2. Zebrać informacje o cenach.
3. Porównać funkcje produktów.
4. Wskazać mocne i słabe strony.
5. Przygotować końcowe podsumowanie.

Planner nie musi sam wykonywać tych kroków. Jego główną rolą jest przygotowanie sensownej struktury pracy.

Typowe odpowiedzialności plannera:
- dekompozycja celu na podzadania,
- ustalenie kolejności kroków,
- wskazanie zależności między krokami,
- czasem aktualizacja planu po otrzymaniu nowych informacji,
- przygotowanie planu w formacie zrozumiałym dla reszty systemu.

## Orkiestrator

Orkiestrator zarządza rzeczywistym przebiegiem pracy w systemie. Wie, jacy agenci i jakie narzędzia są dostępne, przekazuje im zadania, zbiera wyniki i pilnuje stanu całego procesu.

Dla powyższego przykładu orkiestrator może:

1. Wysłać zadanie wyszukiwania konkurentów do agenta researchowego.
2. Przekazać znalezione firmy do agenta analizującego cenniki.
3. Uruchomić równolegle agentów porównujących funkcje produktów.
4. Zebrać wyniki.
5. Przekazać całość do agenta syntetyzującego raport.
6. W razie błędu ponowić krok, zmienić model, użyć fallbacku albo poprosić człowieka o decyzję.

Typowe odpowiedzialności orkiestratora:
- routing zadań do właściwych agentów,
- wywoływanie narzędzi i usług,
- zarządzanie stanem workflowu,
- obsługa błędów, retry i fallbacków,
- uruchamianie zadań równoległych,
- łączenie wyników z wielu agentów,
- kontrola zakończenia procesu.

## Najważniejsza różnica

| Obszar | Planner | Orkiestrator |
|---|---|---|
| Główna rola | Tworzy plan | Wykonuje i koordynuje przebieg |
| Pytanie, na które odpowiada | Co trzeba zrobić? | Kto ma to zrobić i jak sterować wykonaniem? |
| Poziom pracy | Logika zadania | Logika wykonawcza systemu |
| Kontakt z agentami | Może tylko wskazać potrzebne role | Faktycznie deleguje zadania agentom |
| Stan procesu | Zwykle zna plan i cel | Zna aktualny stan workflowu |
| Obsługa błędów | Może zmienić plan | Wykonuje retry, fallback, eskalację |
| Przykład wyniku | Lista kroków | Przepływ wykonania między agentami |

## Przykład w architekturze multi-agent

Użytkownik prosi:

> Znajdź informacje o trzech konkurencyjnych produktach i przygotuj tabelę porównawczą.

Możliwy przebieg:

1. **Planner** tworzy plan:
   - wyszukać produkty,
   - zebrać ceny,
   - zebrać funkcje,
   - zbudować tabelę,
   - napisać wnioski.

2. **Orkiestrator** wykonuje plan:
   - uruchamia agenta `research_agent`,
   - przekazuje wyniki do `pricing_agent`,
   - równolegle uruchamia `feature_analysis_agent`,
   - scala wyniki,
   - jeśli dane są niekompletne, wraca do researchu,
   - na końcu przekazuje dane do `report_writer_agent`.

## Czy orkiestrator i planner mogą być tym samym?

Tak. W prostych systemach jeden agent może jednocześnie planować i orkiestracyjnie sterować wykonaniem. To często wystarcza dla małych workflowów.

W większych systemach warto je rozdzielić, ponieważ:
- planner może skupić się na jakości strategii,
- orkiestrator może być bardziej deterministyczny i techniczny,
- łatwiej testować i debugować przepływ,
- można ograniczyć nieprzewidywalność LLM-a w części wykonawczej,
- łatwiej dodać retry, timeouty, fallbacki i kontrolę stanu.

## Dobra intuicja

Planner jest jak osoba, która przygotowuje listę zadań i kolejność pracy.

Orkiestrator jest jak system zarządzający wykonaniem: przydziela zadania konkretnym wykonawcom, pilnuje zależności, zbiera wyniki i reaguje na problemy.

W praktycznej architekturze:

```text
User goal
   |
   v
Planner -> plan kroków
   |
   v
Orkiestrator -> routing, stan, agenci, narzędzia, retry, wynik końcowy
```

## Powiązane

- [Wzorce Projektowe Systemów Agentowych](wzorce-projektowe-systemow-agentowych.md)
- [Agentic Workflows i Multi-Agent Orchestration](agentic-workflows-multi-agent-orchestration.md)
- [Multi-Agent Supervisor w LangGraph](multi-agent-supervisor-langgraph.md)
