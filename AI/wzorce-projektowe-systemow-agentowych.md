# Wzorce Projektowe Systemów Agentowych

## Czym to jest?
Wzorce projektowe w systemach agentowych (agentic systems) to sprawdzone na poziomie architektury szablony ułatwiające budowę aplikacji wykorzystujących Modele Językowe (LLM-y) nie tylko jako generatory tekstu, ale jako decyzyjne byty (agenty) rozwiązujące złożone problemy. Określają one sposoby komunikacji pomiędzy LLM-em, środowiskiem, pamięcią i narzędziami, a także zasady kooperacji pomiędzy wieloma autonomicznymi agentami.

## Dlaczego jest to ważne i kiedy się przydaje?
Pojedyncze, liniowe zapytanie do modelu jęzkowego (single-shot prompt) świetnie sprawdza się w generowaniu tekstów. Zawodzi jednak, gdy chcemy by system wykonał nieliniowy prosces, wymagający adaptacji (np. "znajdź 3 polskie startupy, przeanalizuj ich strony internetowe i podsumuj je w tabeli").

Wzorce agentowe wprowadzają:
- **Rozdzielenie ról (Separation of Concerns)** – oddelegowanie wyspecjalizowanych kompetencji do pod-agentów, co ułatwia debugowanie.
- **Niezawodność (Reliability)** – samonaprawianie błędów w reakcji na nieudane wykonanie akcji (np. zła składnia w API).
- **Planowanie działania na dużą skalę** – możliwość wyciągnięcia kroków z globalnego planu z zachowaniem kontroli.
- **Reakcyjność w izolowanych systemach** – agent na bieżąco odpytuje narzędzia odczytujące np. pliki lub bazy danych i na bieżąco kształtuje dalszą drogę.

## Jak to działa? (Najważniejsze Wzorce)

### 1. ReAct (Reasoning and Acting)
Wzorzec bazowy definiujący główną pętlę decyzyjną. Zamiast od razu generować ostateczną odpowiedź, agent przechodzi przez cykl: 
- **Thought (Myśl)**: analizuje sytuację i decyduje co zrobić.
- **Action (Akcja)**: wywołuje ustalone do tego narzędzie.
- **Observation (Obserwacja)**: konsumuje wyjście z wyniku i uaktualniając swój kontekst ponawia cykl ReAct, dopóki cel nie ustali poprawnej odpowiedzi końcowej.

### 2. Tool / Function Calling (Wywoływanie Narzędzi)
Agent dostaje na start zestaw dozwolonych funkcji w określonym schemacie (JSON Schema). Jeśli model uzna, że potrzebuje interakcji ze światem zewnętrznym (kalkulatora, zapytania SQL, itp.), zwraca odpowiednie formatowanie zamiast tekstu. Po stronie inżynieryjnej jest to zintegrowane mocno ze zdefiniowanym ustrukturyzowanym formatowaniem powrotu (zobacz też: [Structured Output z LLM](structured-output-z-llm.md)).

### 3. Plan-and-Execute (Praca w trybie Planisty)
Zamiast obciążać zawiłymi pętlami jednego modelu, architektura jest rozdzielona na dwoje wyspecjalizowanych typów ról:
- **Planner Agent**: Bierze ogólny cel wejściowy i przygotowuje z niego uporządkowaną listę małych i weryfikowalnych kroków (sub-tasków).
- **Executor Agent**: Bierze zadanie i je zamyka. Nie posiada kontekstu całości i globalnego problemu, dzięki czemu jest o wiele tańszy do użycia wielokrotnie i nie gubi uwagi.

### 4. Router / Supervisor (Przekierowanie i Nadzorowanie)
Zarządca i Router zadania. Pojedynczy LLM interpretuje intencję wejściowej komendy, a następnie przekazuje wykonanie do jednego z innych mniejszych agentów i czeka na odpowiedź. Zwraca zagregowany wynik. Dobre rozwiązanie przy rozległych systemach w których chcemy izolować odpowiedzialność agentów (jeden robi tylko przegląd sieci, drugi obsługuje tylko bazę SQL w firmie).

### 5. Koordynacja Multi-Agent System (Baza z frameworków takich jak AutoGen, CrewAI)
Zamiast scentralizowanej orkiestracji, agenci konwersują ze sobą w cyklach z różnymi rolami (np. programista, code reviewer, business analyst) dążąc wspólnie do celu. System sam wymienia dialogi dopóki wszyscy nie zgodzą się z outputem. Konfiguracje orkiestracji obejmują:
- **Hierarchię / Supervisor**: jeden model rozdziela i łączy wszystko.
- **Sekwencyjność**: agent numer jeden przekazuje wyniki zadania bezpośrednio agentowi numer dwa i tak do końca jak na taśmie produkcyjnej.

### 6. Reflection / Reflexion (Samo-ocena i poprawa)
System zakłada użycie "krytyka". Agent po wygenerowaniu odpowiedzi w pierwszym podejściu wcale jej nie wysyła. Przekazuje ją do drugiego agenta (ewaluatora) lub w kolejnym wezwaniu sam jako nowe zadanie dostaje prośbę o krytyczną ocenę, poszukiwanie braku spójności czy obejścia założeń w swoim kodzie wyjściowym przed wypuszczeniem akcji. Pozytywnie wpływa to na jakość końcową a także stanowi filar polityk bezpieczeństwa (zobacz [LLM Guardrails](llm-guardrails.md)).

### 7. Trwałość i Pamięć (State Management)
Sam model nie posiada pamięci krótkotrwałej z wywołania na wywołanie z frameworku. Zamiast budować jeden ciągnący się tekst czatu (memory bloating), stan zapisywany jest jako zdefiniowane parametry "grafu" (np. biblioteka LangGraph). Stan w węzłach jest modyfikowany bezpośrednio bez przekazywania wszystkiego w wektorowej formie w obrębie każdego zadania co zwiększa wierność powtórzeń. W przypadku danych archiwalnych posługuje się najczęściej wzorcami RAG z bazy skalarnej.

### 8. Node Factory Pattern (Fabryka Węzłów)
Wzorzec programistyczny szczególnie popularny w budowie systemów agentowych opartych na grafach (np. LangGraph). Zamiast statycznego, sztywnego deklarowania (hardcodowania) kodu zachowania każdego węzła, wykorzystuje się wzorzec **Factory**. Generuje on obiekty lub funkcje z odpowiednio wstrzykniętymi zależnościami – specjalistycznym promptem systemowym, określoną temperaturą czy podzbiorem udostępnionych narzędzi. Zwiększa to reużywalność kodu – z jednego szablonu węzła-agenta możemy dynamicznie instancjować wielu sub-agentów o różnych specjalizacjach w danym momencie (tzw. węzły parametryzowane).

### 9. Fault Isolation / Fallback (Izolacja Błędów)
Krytyczny wzorzec chroniący stabilność przepływu (workflowu) agenta. Agenty oparte o LLM wprowadzają nowy poziom nieprzewidywalności: zwracają zły format (np. zepsuty JSON w wywołaniu funkcji), przekraczają limity przesyłu (rate-limits), ew. wzywają narzędzia, które rzucają błąd aplikacji.
W izolacji błędów (Fault isolation) buduje się jawne ścieżki zastępcze:
- **Fallback modelu**: w przypadku przekroczenia limitu na jednym API, przepływ (node) jest rutowany (przełączany) na inny, zapasowy model.
- **Self-Correction po wyłapaniu wyjątku (Exception loop)**: jeśli agent nie użył odpowiednich argumentów w narzędziu, błąd techniczny (kod usterki) jest bezpośrednio rutowany z powrotem do samego modelu z prośbą "Twój poprzedni strzał dał poniższy błąd. Zobacz go i popraw swój JSON", bez zawieszania całego systemu przed końcowym użytkownikiem.

## Powiązane pliki
- [Structured Output z LLM](structured-output-z-llm.md)
- [Komunikacja z LLM w Langchain](komunikacja-z-llm-w-langchain.md)
- [LLM Guardrails](llm-guardrails.md)
