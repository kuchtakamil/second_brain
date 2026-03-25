# --- System Prompt --- **Role:** Senior Technical Documentation Engineer & Conten

**Data:** 18 gru 2025, 15:36:59 CET

---

**User:**

--- System Prompt ---
**Role:** Senior Technical Documentation Engineer & Content Architect.

**Task:** Technical Content Distillation (Information Density Optimization).

**Contextual Anchor:** The input text belongs to the broader topic: "{{CHAPTER_CONTEXT}}". Use this context to maintain terminological consistency and ensure high technical precision.

**Mandatory Structural Constraints:**
1. **Preserve Headers:** You must retain all original Markdown headers (e.g., `###`, `####`) exactly as they appear in the source.
2. **Title Integrity:** Do not translate, rename, or shorten any header titles. They must remain 1:1 identical to the input.
3. **Sequential Logic:** Maintain the exact order of sections as presented in the source text.
4. **Code Blocks:** All code snippets, CLI commands, and configuration examples must be preserved in their entirety, using English for comments and variable names.

**Extraction Logic (Signal vs. Noise):**
- **KEEP (The Signal):**
    - Formal definitions and technical specifications.
    - Architectural patterns, logic flows, and state transitions.
    - Trade-off analyses (pros/cons) and performance metrics (latency, throughput, complexity).
    - API signatures, parameters, and data structures.
    - Best practices, anti-patterns, direct technical recommendations and security constraints.
- **REMOVE (The Noise):**
    - Motivational framing, anecdotes, and personal stories.
    - Metaphors, analogies, and "educational fluff".
    - Meta-commentary (e.g., "In this section, we will explore...", "As we saw earlier...").
    - Rhetorical questions and repetitive introductory transitions.
    - Historical context that does not impact current implementation.
    - Author's personal opinions or "flavor" text that does not contribute to technical mastery.

**Output Requirements:**
- Target a high "Information-to-Word" ratio.
- Use technical, precise language.
- Where appropriate, convert descriptive paragraphs into dense bullet points or tables to increase readability, provided no technical nuance is lost.
- **NO summary, NO introduction, NO concluding remarks.** Output only the processed Markdown.

**Execution Directive:** The output should read like a high-end technical reference manual or documentation. If the original text is 10 pages of "chatty" book content, the output should be as many pages as necessary to contain 100% of the facts, but 0% of the filler.
--- End System Prompt --- 

--- User prompt ---
## Monitorowanie pod kątem sukcesu i identyfikowanie niepowodzeń  
Przypomnij sobie nasz przykładowy stary system konferencyjny omówiony we wprowadzeniu i zastanów się, jak podejść do tematu monitorowania w pojedynczej aplikacji. Pojedyncza usługa ma jeden plik dziennika zdarzeń przeznaczony do śledzenia żądań i przetwarzany przez aplikację. Jest tylko jedna aplikacja, którą trzeba sprawdzić, aby monitorować stan procesu na serwerze. Podział rozwiązania na wiele usług, np. usługę uczestnika, prowadzi do zwiększenia stopnia złożoności operacyjnej. Im więcej przeskoków między usługami, tym większe niebezpieczeństwo potencjalnego niepowodzenia, a ręczne szukanie źródła problemu staje się znacznie trudniejsze.  
### Trzy filary monitorowania  
Architektura bazująca na API charakteryzuje się luźnym powiązaniem komponentów. Bez odpowiedniej obsługi technicznej trudno jest uzasadnić jej stosowanie i rozwiązywać ewentualne problemy. Monitorowanie zapewnia przejrzystość w systemie oraz pozwala w pełni zrozumieć, co się w nim dzieje. Monitorowanie można najlepiej opisać za pomocą trzech filarów, operacyjnego minimum wymaganego do uzasadnienia zastosowania architektury rozproszonej.  
Wskaźnik to pomiar przechwytywany w regularnych odstępach czasu i przedstawiający ważny element dla ogólnego stanu platformy. Wskaźniki mogą znajdować się na różnych poziomach platformy, zaś swoboda w zakresie ich struktury oznacza, że platforma może określać, które z nich są ważne do przechwycenia. Na przykład platforma Javy może zdecydować o przechwytywaniu poziomu wykorzystania procesora, bieżącej wielkości sterty i długości przerwy w działaniu mechanizmu usuwania nieużytków itd.
Dziennik zdarzeń to dokładne dane otrzymane w wyniku przetwarzania danego komponentu. Jakość dziennika zdarzeń jest często ściśle związana z aplikacją bądź komponentem infrastruktury, na podstawie którego dziennik został wygenerowany. Format dziennika zdarzeń ma duży wpływ na użyteczność wyszukiwania i przetwarzania zarejestrowanych danych. Strukturalne rejestrowanie danych ułatwia wyszukiwanie i pobieranie istotniejszych danych. W systemie rozproszonym same dzienniki zdarzeń zwykle nie wystarczają, będą lepiej wykorzystane w połączeniu z kontekstem zapewnianym przez wskaźniki i ślady.
Śledzenie ma duże znaczenie podczas przejścia do architektury rozproszonej, pozwala na śledzenie poszczególnych żądań wykonywanych przez wszystkie komponenty współpracujące z architekturą. Na przykład jeśli żądanie zakończy się niepowodzeniem, śledzenie pozwoli na szybkie zlokalizowanie konkretnego komponentu architektury, który uległ awarii. Śledzenie odbywa się przez dodanie unikatowego nagłówka maksymalnie jak najbliżej źródła żądania. Ten nagłówek będzie propagowany we wszystkich kolejnych operacjach przetwarzania danego żądania. Jeżeli kontekst żądania przejdzie do innego typu infrastruktury (np. kolejki), wówczas unikatowy nagłówek zostanie zarejestrowany w kopercie wiadomości.
Więcej szczegółowych informacji na ten temat znajdziesz w napisanej przez Cindy Sridharan i wydanej przez O’Reilly książce Distributed Systems Observability (https://www.oreilly.com/library/view/distributed-systems-observability/9781492033431/).  
Nie wystarczy zaimplementować na platformie tych trzech filarów monitorowania. W dalszej części rozdziału wyjaśnimy, jak te filary można wykorzystać podczas pracy z infrastrukturą używaną na platformie API.  
Projekt OpenTelemetry (https://opentelemetry.io/) okaże się najlepszym rozwiązaniem pomagającym w rozpoczęciu pracy z trzema wymienionymi filarami monitorowania. Dostarcza on otwartego standardu w Cloud Native Computing Foundation (CNCF), co chroni przed zamknięciem w rozwiązaniu własnościowym producenta i maksymalnie ułatwia jak najszerszą zgodność. Podczas gdy standardy wskaźników i śledzenia powstały już jakiś czas temu i są stabilne, rejestrowanie danych jest nieco trudniejszym do rozwiązania problemem (ze względu na ogromną ilość różnych potencjalnych emiterów danych). Na szczęście również z tym można sobie poradzić dzięki wykorzystaniu projektu OpenTelemetry.  
### Ważne wskaźniki dla API  
Określenie, które wskaźniki są ważne na platformie API, to kluczowa decyzja pomagająca we wczesnym wykrywaniu awarii, a nawet być może pozwalająca im zapobiec. Wprawdzie można sprawdzać i pobierać szeroką gamę różnych wskaźników, ale dostępność części z nich zależy także od platformy. Wskaźniki RED (ang. rate, error, duration) są najczęściej wymieniane jako jedno z podejść w zakresie monitorowania architektury usługi bazującej na ruchu sieciowym. Zaletą tych wskaźników jest to, że zapewniają dobre informacje o aktualnej sytuacji — szybkość (ang. rate) wskazuje liczbę żądań na sekundę przetwarzanych przez usługę (to inaczej przepustowość), jakie błędy (ang. errors) są zwracane i jaka jest długość (ang. duration) bądź opóźnienie poszczególnych żądań. W świecie inżynierii niezawodności (ang. site reliability engineering, SRE) te wskaźniki pomagają w ustaleniu tzw. czterech złotych sygnałów (https://sre.google/sre-book/monitoring-distributed-systems/#xref_monitoring_golden-signals) — opóźnienia, ruchu sieciowego, błędów i nasycenia.
Prawdopodobnie największą wadą wskaźników RED i czterech złotych sygnałów jest łatwość, z jaką można zastosować reguły i przeoczyć szerszy kontekst systemu, czyli go nie zrozumieć. Na przykład: czy każdy błąd w API został spowodowany przez usługę w łańcuchu żądania? W przypadku API kontekst błędów jest naprawdę ważny — np. błąd o kodzie stanu w zakresie 5xx jest istotny, ponieważ wskazuje na niepowodzenie, którego źródłem jest komponent infrastruktury bądź usługa. Z kolei błąd o kodzie stanu w zakresie 4xx nie jest błędem usługi, a bardziej błędem po stronie klienta, ale czy to oznacza, że można go po prostu zignorować? Seria błędów o kodzie stanu 403 może wskazywać, że ktoś próbuje uzyskać dostęp do danych, do których nie ma upoważnienia. To tylko jeden z przykładów pokazujących, dlaczego kontekst ma znaczenie krytyczne. W celu ustalenia, które wskaźniki są ważne, trzeba mieć wiedzę o API wykraczającą poza wskaźniki RED.
Ważne wskaźniki powinny być powiązane z systemem ostrzegania, aby w ten sposób zapewnić Ci możliwość zajęcia się istniejącymi (lub nadchodzącymi) problemami. Należy zachować ostrożność podczas definiowania ostrzeżeń, aby uniknąć fałszywych alarmów. Na przykład jeśli ostrzeżenie jest generowane w przypadku małej aktywności lub jej braku, w przypadku banku może się pojawić w trakcie świąt bądź w weekendy. Rozwiązaniem może być zdefiniowanie tego rodzaju ostrzeżeń jedynie dla godzin pracy organizacji bądź powiązanie np. z bieżącą liczbą logowań do witryny internetowej organizacji.
W naszym przykładowym systemie konferencyjnym wymienione tutaj wskaźniki mogą być uznane za bardzo ważne do przechwycenia:  
Liczba żądań na minutę wykonywanych przez uczestników.
Wartość SLO dla uczestników to średnie opóźnienie podczas udzielania odpowiedzi. Jeżeli to opóźnienie zacznie wyraźnie odstawać, to może być wczesny sygnał wskazujący na problem.
Wartość 401 w systemie CFP może wskazywać na włamanie do producenta bądź kradzież tokena.
Pomiar dostępności i czasu działania usługi uczestnika.
Poziom użycia pamięci i procesora przez aplikacje.
Całkowita liczba uczestników w systemie.  
### Odczytywanie sygnałów  
Dotychczas omówiliśmy temat monitorowania i wyjaśniliśmy, dlaczego ma ono tak duże znaczenie. Ponadto przedstawiliśmy przeznaczenie poszczególnych filarów monitorowania. Pokrótce omówiliśmy wybrane z kluczowych wskaźników dla API, a także ostrzegliśmy, że implementacja tylko jednego wskaźnika bądź wskaźników bez kontekstu jest niewystarczająca. Przewinęła się również idea przechwytywania wskaźników z uruchomionych aplikacji, np. w trakcie działania mechanizmu równoważenia obciążenia. Wydłużenie czasu działania tego mechanizmu może być wczesnym symptomem zbliżającej się awarii aplikacji. Mechanizm usuwania nieużytków zwykle działa po wstrzymaniu aplikacji, co z kolei przekłada się na opóźnienie w obsłudze żądań, a to z kolei wpływa na ogólne opóźnienie. Wczesne wychwycenie jest tutaj odpowiednikiem zwrócenia uwagi na dziwne odgłosy wydawane przez silnik — wciąż działa, ale zdecydowanie coś jest nie tak.
W celu odczytywania sygnałów pomocne będzie zdefiniowanie oczekiwań i przygotowanie wartości bazowych, a następnie przeprowadzanie pomiarów z uwzględnieniem tego zakresu i ostrzeganie, gdy wartość będzie poza nim — to pomoże w wychwytywaniu nieprawidłowości. Następnym krokiem będzie obserwowanie rzeczywistego wskaźnika dotyczącego opóźnienia w działaniu API, co można uznać za odpowiednik sprawdzenia, czy w samochodzie świeci się kontrolka silnika. Im wcześniej udaje się odczytywać sygnały potencjalnych problemów, tym mniejsze prawdopodobieństwo, że dotkną one użytkownika. Jeżeli odczyty zostaną zignorowane, aplikacja ostatecznie ulegnie awarii i zespół będzie musiał zająć się jej naprawą.
Zrozumienie oprogramowania i powiązania z kluczowymi wskaźnikami pomaga w przygotowaniu dopracowanej platformy operacyjnej, na której będzie można wcześnie wychwytywać potencjalne problemy i je usuwać. W architekturze rozproszonej awaria jest nieunikniona, zaś po jej wystąpieniu ślady to pierwsza rzecz do sprawdzenia w celu zawężenia przyczyny problemu. Mieliśmy okazję przekonać się, że wyszukiwanie problemu bez dostępu do narzędzi monitorowania i śledzenia może zabierać godziny, w trakcie których programiści zamieniają się w detektywów przeglądających dzienniki zdarzeń w poszukiwaniu jakichkolwiek wskazówek dotyczących problemu. Kolejnym ważnym aspektem jest ustalenie, jak szybko zespół jest w stanie reagować na różne zdarzenia. Jeżeli pierwsza awaria nie pozwoli na żaden ruch sieciowy do API, wówczas będzie to sytuacja wysoce stresująca (i prawdopodobnie będzie miała ogromny wpływ na działalność biznesową organizacji).

--- End User Prompt ---

---

**Gemini:**

## Monitorowanie pod kątem sukcesu i identyfikowanie niepowodzeń

- **Złożoność operacyjna:** Przejście z aplikacji monolitycznej na architekturę rozproszoną (np. mikrousługi) zwiększa liczbę punktów potencjalnej awarii oraz utrudnia manualną identyfikację źródła błędów.
- **Wielokrotne przeskoki (hops):** Każda dodatkowa komunikacja międzyusługowa podnosi ryzyko niepowodzenia i wymaga zautomatyzowanych systemów śledzenia przepływu żądań.

### Trzy filary monitorowania

Fundamentem obserwowalności (observability) systemów rozproszonych są trzy kategorie danych:

| Filar | Definicja i charakterystyka | Przykład / Implementacja |
| --- | --- | --- |
| **Wskaźniki (Metrics)** | Pomiary przechwytywane w regularnych odstępach czasu, reprezentujące stan platformy. | Wykorzystanie CPU, wielkość sterty (heap size), czas trwania Garbage Collection (GC). |
| **Dzienniki zdarzeń (Logs)** | Strukturalne dane generowane podczas przetwarzania przez komponent. | Zapisy zdarzeń w formacie JSON dla ułatwienia indeksowania i przeszukiwania. |
| **Śledzenie (Tracing)** | Rejestracja ścieżki pojedynczego żądania przez wszystkie komponenty systemu. | Unikatowy nagłówek (Correlation ID) wstrzykiwany u źródła i propagowany w nagłówkach HTTP lub kopertach wiadomości (np. kolejki). |

- **Standardyzacja:** Projekt **OpenTelemetry (CNCF)** stanowi otwarty standard dla metryk, śladów i logów, eliminując ryzyko vendor lock-in i zapewniając interoperacyjność między różnymi emiterami danych.

### Ważne wskaźniki dla API

Skuteczne monitorowanie API opiera się na analizie ruchu sieciowego i wydajności usług:

- **Metryki RED:**
  - **Rate (Szybkość):** Liczba żądań na sekundę (przepustowość).
  - **Errors (Błędy):** Częstotliwość występowania niepowodzeń.
  - **Duration (Czas trwania):** Opóźnienie (latency) poszczególnych żądań.
- **Cztery złote sygnały (SRE):** Opóźnienie, ruch, błędy i nasycenie (saturation).
- **Analiza kontekstowa kodów stanu:**
  - **5xx:** Błędy infrastruktury lub usług (krytyczne dla stabilności).
  - **4xx:** Błędy klienta; serie błędów (np. 403 Forbidden) mogą sygnalizować próby nieautoryzowanego dostępu.
- **Systemy ostrzegania (Alerting):**
  - Definiowanie wartości bazowych i progów alarmowych.
  - Korelacja alertów z kontekstem biznesowym (np. godziny pracy vs święta) w celu redukcji fałszywych alarmów.

**Kluczowe wskaźniki operacyjne (przykład):**

- Liczba żądań na minutę.
- Średnie opóźnienie odpowiedzi w relacji do **SLO (Service Level Objective)**.
- Anomalie w kodach 401 (sygnalizacja potencjalnej kradzieży tokenów).
- Dostępność i uptime usług.
- Użycie zasobów (RAM/CPU) przez instancje aplikacji.

### Odczytywanie sygnałów

- **Wczesne wykrywanie:** Monitorowanie metryk infrastrukturalnych, takich jak narzut mechanizmu równoważenia obciążenia (load balancer) lub wydłużenie pauz GC, pozwala na identyfikację nadchodzących awarii przed ich wystąpieniem u użytkownika końcowego.
- **Wartości bazowe (Baselines):** Ustalenie normatywnych zakresów pracy systemu umożliwia wykrywanie anomalii poprzez systemy monitorowania.
- **Izolacja przyczyn (Root Cause Analysis):** W architekturze rozproszonej ślady (traces) są podstawowym narzędziem do szybkiego zawężania obszaru awarii, skracając czas od wykrycia do naprawy błędu.
- **Reakcja operacyjna:** Szybkość reakcji na sygnały z monitoringu bezpośrednio determinuje wpływ awarii na ciągłość biznesową organizacji.

Chciałbyś, abym przygotował przykładową konfigurację OpenTelemetry dla usługi w wybranym języku programowania (np. Java, Python, Go)?