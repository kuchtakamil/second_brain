---
tags: [ai-agents, interview, langchain, langgraph]
date: 2026-06-06
---
# Pytania rekrutacyjne — AI Agents

Zestaw pytań na rozmowę kwalifikacyjną dotyczącą **agentów AI**. Pytania są pogrupowane w podrozdziały — od fundamentów, przez rozumowanie, narzędzia, pamięć i systemy wieloagentowe, aż po produkcję, bezpieczeństwo i ewaluację. Szczegóły frameworkowe ograniczone są wyłącznie do **LangChain** i **LangGraph** (osobne podrozdziały 7 i 8).

W obrębie każdego podrozdziału pytania ułożone są z grubsza od podstawowych (junior/mid) do pogłębionych (senior / trade-offy / system design).

## Spis treści

- [1. Fundamenty — czym jest agent](#1-fundamenty--czym-jest-agent)
- [2. Rozumowanie i planowanie (reasoning & planning)](#2-rozumowanie-i-planowanie-reasoning--planning)
- [3. Narzędzia i tool use](#3-narzędzia-i-tool-use)
- [4. Pamięć i stan (memory & state)](#4-pamięć-i-stan-memory--state)
- [5. Systemy wieloagentowe i orkiestracja](#5-systemy-wieloagentowe-i-orkiestracja)
- [6. Kontekst, RAG i context engineering w agentach](#6-kontekst-rag-i-context-engineering-w-agentach)
- [7. LangChain (framework)](#7-langchain-framework)
- [8. LangGraph (framework)](#8-langgraph-framework)
- [9. Human-in-the-loop i sterowanie przebiegiem](#9-human-in-the-loop-i-sterowanie-przebiegiem)
- [10. Produkcja: observability, koszt, latencja, streaming](#10-produkcja-observability-koszt-latencja-streaming)
- [11. Bezpieczeństwo i guardrails](#11-bezpieczeństwo-i-guardrails)
- [12. Ewaluacja i testowanie agentów](#12-ewaluacja-i-testowanie-agentów)
- [13. Pytania scenariuszowe / system design](#13-pytania-scenariuszowe--system-design)
- [14. Pytania pogłębiające (senior / trade-offy)](#14-pytania-pogłębiające-senior--trade-offy)

---

## 1. Fundamenty — czym jest agent

**1. Czym jest agent AI? Jak zdefiniowałbyś go w jednym zdaniu, odróżniając od „zwykłego" wywołania LLM?**

Agent AI to system, w którym **LLM steruje przebiegiem działania w pętli** — sam decyduje, jakie kroki podjąć i jakich narzędzi użyć, aby osiągnąć cel, obserwując wyniki swoich akcji i korygując kolejne decyzje, zamiast jedynie wygenerować jedną odpowiedź na podstawie jednego wejścia.

Kluczowa różnica względem „zwykłego" wywołania LLM:

- **Zwykłe wywołanie LLM**: `wejście → model → wyjście`. Jeden strzał (lub łańcuch z góry ustalonych strzałów). Model nie wpływa na to, co się stanie dalej.
- **Agent**: `cel → [model decyduje → akcja → obserwacja]* → wynik`. To **model w czasie wykonania decyduje**, ile kroków zrobić, jakie narzędzia wywołać i kiedy skończyć.

Skrótowo: agent = **LLM + narzędzia + pętla sterująca + pamięć/stan**, gdzie to model kontroluje pętlę.

---

**2. Na czym polega różnica między workflow a agentem? Kiedy świadomie wybierasz jedno, a kiedy drugie?**

- **Workflow** — ścieżki sterowania są **zakodowane przez programistę**. LLM bywa wykorzystany w poszczególnych krokach (klasyfikacja, ekstrakcja, generacja), ale o tym, *który krok wykona się następny*, decyduje kod (if/else, router, sekwencja). Przewidywalny, łatwy do testowania, tańszy, niższa latencja.
- **Agent** — to **LLM dynamicznie decyduje** o kolejnych krokach i użyciu narzędzi w pętli, aż uzna zadanie za zakończone. Elastyczny, radzi sobie z otwartymi/nieprzewidywalnymi zadaniami, ale droższy, wolniejszy i mniej przewidywalny.

Reguła praktyczna (zgodna z podejściem Anthropic „Building Effective Agents”): **zaczynaj od najprostszego rozwiązania**, sięgaj po agenta dopiero, gdy prostsze (pojedynczy prompt, RAG, ustalony workflow) nie wystarcza.

- **Wybierz workflow**, gdy: kroki są znane z góry, zależy Ci na powtarzalności/audytowalności, zadanie ma wąską, ustabilizowaną ścieżkę, koszt i latencja są krytyczne.
- **Wybierz agenta**, gdy: liczba i kolejność kroków zależy od danych wejściowych, przestrzeń możliwych ścieżek jest duża/otwarta, a wartość elastyczności przewyższa koszt nieprzewidywalności (np. eksploracyjny research, debugowanie, obsługa zróżnicowanych zgłoszeń).

---

**3. Opisz pętlę agentową (sense → think → act → observe). Co jest „obserwacją", a co „akcją"?**

Pętla to cykl powtarzany aż do osiągnięcia celu lub limitu:

1. **Sense** — agent „odbiera" stan: prompt użytkownika, dotychczasowa historia, wynik poprzedniego kroku.
2. **Think (reason)** — LLM rozumuje: co już wie, czego brakuje, jaki ma być następny krok.
3. **Act** — **akcja** = decyzja modelu, która wpływa na świat lub pozyskuje dane: zwykle **wywołanie narzędzia** (zapytanie do bazy, wyszukiwanie, wywołanie API, uruchomienie kodu) albo wygenerowanie finalnej odpowiedzi.
4. **Observe** — **obserwacja** = **wynik akcji wracający do kontekstu**: zwrócone dane z narzędzia, kod błędu, treść dokumentu, odpowiedź API. Staje się wejściem do następnego „think".

Czyli: **akcja** to to, co agent *robi* (najczęściej tool call), a **obserwacja** to *informacja zwrotna* o skutku tej akcji, którą agent wciela z powrotem do swojego rozumowania. Pętla kończy się, gdy model uzna, że ma wszystko, by zwrócić wynik (albo gdy zadziała guard: limit kroków/tokenów/czasu).

---

**4. Z jakich komponentów składa się typowy agent?**

- **Model (LLM)** — „mózg": rozumuje, planuje, wybiera narzędzia i decyduje o zakończeniu. Dobór modelu (i ewentualny routing) wpływa na jakość, koszt i latencję.
- **Narzędzia (tools)** — interfejs do świata zewnętrznego: API, bazy, wyszukiwarka, wykonywanie kodu, RAG. Definiowane przez nazwę, opis i schemat argumentów (de facto część promptu).
- **Pamięć i stan** — pamięć krótkoterminowa (kontekst/historia bieżącej sesji, stan przebiegu) i długoterminowa (trwała wiedza między sesjami, np. baza wektorowa). Por. [[memory-management-i-session-handling]].
- **Pętla sterująca (orchestration loop)** — mechanizm wykonujący cykl think→act→observe, zarządzający warunkiem stopu, limitami, obsługą błędów. W LangGraph realizowana jako graf węzłów.
- **Prompt / instrukcje (system prompt)** — definiuje rolę, cel, ograniczenia, dostępne narzędzia, format wyjścia, kryteria zakończenia.

(Opcjonalnie: guardrails, observability/tracing, human-in-the-loop, persystencja/checkpointing.)

---

**5. Czym jest wzorzec ReAct (Reasoning + Acting)? Jak przeplata rozumowanie z działaniem?**

**ReAct** to wzorzec, w którym model **przeplata jawne rozumowanie z akcjami** w pętli, zamiast najpierw zaplanować wszystko, a potem ślepo wykonać. Schemat kroku:

```
Thought:      (rozumowanie — co wiem, czego potrzebuję, co zrobić dalej)
Action:       (wywołanie narzędzia + argumenty)
Observation:  (wynik narzędzia wrócony do kontekstu)
... powtarzaj ...
Thought:      mam już wszystko
Final Answer: (odpowiedź)
```

Siła ReAct: rozumowanie **opiera się na świeżych obserwacjach** — model adaptuje się do tego, co realnie zwróciło narzędzie (np. inaczej zareaguje, gdy wyszukiwanie nic nie znalazło). To ogranicza halucynacje (decyzje są zakotwiczone w danych) i daje czytelny ślad rozumowania. Wada: każdy krok to osobne wywołanie LLM → koszt i latencja rosną; jawne „Thought" zużywa tokeny. Por. plan-and-execute (sekcja 2) jako alternatywa, gdy plan da się ustalić z góry.

---

**6. Co decyduje o zakończeniu pętli? Jak rozpoznać i obsłużyć „niekończącą się" pętlę?**

**Naturalne zakończenie**: model przestaje wołać narzędzia i zwraca finalną odpowiedź (w tool-callingu — brak `tool_calls` w odpowiedzi, sama treść). To model „decyduje", że cel osiągnięty.

Ponieważ na tym nie można polegać w 100%, dokłada się **twarde warunki stopu (guardraile)**:

- **max liczba kroków/iteracji** (recursion limit),
- **budżet tokenów** i **timeout** całego przebiegu,
- **wykrywanie powtórzeń** — ten sam tool call z tymi samymi argumentami N razy z rzędu, oscylacja A→B→A→B,
- **warunek na poziomie stanu/grafu** (conditional edge w LangGraph kierujący do END).

Diagnostyka „nieskończonej pętli": tracing/observability pokazujący powtarzające się akcje, brak postępu (te same obserwacje), brak zmiany stanu. Przyczyny zwykle: narzędzie ciągle zwraca błąd a model uparcie ponawia, źle zdefiniowany warunek stopu, mglisty cel, zła obsługa pustego wyniku.

Obsługa: po przekroczeniu limitu — **kontrolowane przerwanie** z czytelnym komunikatem/fallbackiem (a nie cichy zawis), ewentualnie eskalacja do człowieka (HITL), oraz wstrzyknięcie do kontekstu informacji „zostało N kroków", by skłonić model do domknięcia.

---

**7. Jaką rolę pełni prompt systemowy / instrukcje? Co zwykle musi się w nim znaleźć?**

System prompt to **konstytucja agenta** — definiuje jego stałe zachowanie niezależnie od konkretnego zapytania. Steruje tym, jak agent rozumuje, kiedy sięga po narzędzia i kiedy kończy. Zwykle zawiera:

- **Rolę i cel** — kim jest agent, jaki problem ma rozwiązać i w jakim zakresie.
- **Dostępne narzędzia i zasady ich użycia** — kiedy których używać, kiedy *nie* używać.
- **Ograniczenia i polityki** — czego nie wolno, granice uprawnień, kiedy eskalować do człowieka, wymóg potwierdzeń przed akcjami nieodwracalnymi.
- **Format wyjścia** — struktura odpowiedzi (np. structured output), język, ton.
- **Kryteria zakończenia** — co znaczy „zadanie wykonane".
- **Sposób radzenia sobie z niepewnością/błędami** — np. „jeśli brak danych, dopytaj / zwróć błąd, nie zmyślaj".

Dobry system prompt jest konkretny i testowalny; mglisty prompt = nieprzewidywalny agent. Powinien być **wersjonowany** (zmiana promptu potrafi cicho zmienić zachowanie na produkcji).

---

**8. Czym różni się autonomia od niezawodności? Dlaczego więcej autonomii często = mniej przewidywalności?**

- **Autonomia** — jak dużo decyzji agent podejmuje sam, bez sztywnych szyn i bez człowieka (ile narzędzi, jak swobodne ścieżki, ile kroków).
- **Niezawodność** — jak konsekwentnie i poprawnie agent realizuje zadanie (powtarzalność wyniku, brak katastrofalnych błędów, przewidywalny koszt).

Napięcie: każda decyzja oddana modelowi to dodatkowy **punkt niedeterminizmu**. Im więcej swobodnych decyzji w łańcuchu, tym **mnoży się** przestrzeń możliwych trajektorii i rośnie szansa, że któraś pójdzie źle (błędny tool call, dryf od celu). Mniej szyn = większa elastyczność, ale trudniejsze testowanie, audyt i kontrola kosztu.

Wniosek inżynierski: autonomię dawkuje się **tam, gdzie naprawdę potrzeba elastyczności**, a resztę „zabija się" deterministycznym kodem, guardrailami i punktami kontrolnymi (HITL). To temat rozwinięty w sekcji 14 („budżet zaufania").

---

**9. Jakie zadania nadają się dla agenta, a jakie lepiej rozwiązać deterministycznym kodem / prostym łańcuchem?**

**Dla agenta** (gdy ścieżka nie jest znana z góry):

- zadania o **zmiennej liczbie i kolejności kroków** zależnej od danych (research wieloźródłowy, debugowanie, eksploracja),
- duża/otwarta przestrzeń możliwych ścieżek, gdzie zakodowanie wszystkich gałęzi byłoby niewykonalne,
- konieczność adaptacji do wyników pośrednich (np. „jeśli wyszukiwanie puste, spróbuj inaczej"),
- gdzie wartość elastyczności > koszt nieprzewidywalności.

**Deterministyczny kod / prosty łańcuch** (gdy ścieżka jest znana):

- ustalony, powtarzalny proces (ETL, walidacja, formatowanie, klasyfikacja → routing),
- wymóg pełnej przewidywalności, audytowalności, niskiej latencji i kosztu,
- operacje wrażliwe/nieodwracalne, gdzie nie chcesz, by „decydował" model,
- proste „jeden prompt wystarczy" — wtedy nie buduj agenta w ogóle.

Zasada: **nie używaj agenta, bo modny** — używaj, bo deterministyczne rozwiązanie nie radzi sobie z różnorodnością wejść.

---

**10. Single-agent vs multi-agent? Dlaczego nie zawsze warto od razu sięgać po wiele agentów?**

- **Single-agent** — jeden LLM z zestawem narzędzi w jednej pętli.
- **Multi-agent** — kilku wyspecjalizowanych agentów (np. supervisor + workerzy), współpracujących przez handoff/wspólny stan/wiadomości. Por. [[multi-agent-supervisor-langgraph]], [[wzorce-projektowe-systemow-agentowych]].

Po multi-agent sięga się, gdy: zadanie naturalnie dzieli się na **rozłączne specjalizacje**, jeden kontekst staje się przeładowany (za dużo narzędzi/instrukcji), albo trzeba **równoległości** (np. wielu researcherów naraz).

Dlaczego **nie od razu**:

- **Wzrost złożoności i kosztu** — więcej wywołań LLM, więcej rund komunikacji = więcej tokenów i latencji.
- **Nowe tryby porażki** — handoffy gubiące kontekst, agenci zapętlający się w „rozmowie", konflikty/sprzeczne wyniki, trudniejszy debug i tracing.
- Często **single-agent z dobrze dobranymi narzędziami** rozwiązuje problem prościej i taniej.

Reguła: zacznij od single-agent; dziel na wielu agentów dopiero, gdy pojawi się konkretny ból (przeładowany kontekst, potrzeba równoległości, wyraźnie rozłączne role). Przeinżynierowany multi-agent to klasyczny anty-wzorzec (sekcja 14).

---

**11. Jakie są główne tryby porażki agentów?**

- **Halucynacja kroków / faktów** — model wymyśla nieistniejące narzędzia, pola, dane albo „udaje", że coś wykonał. Przeciwdziałanie: zakotwiczenie w obserwacjach (ReAct/RAG), walidacja, structured output.
- **Błędne użycie narzędzia** — złe narzędzie, złe lub niezwalidowane argumenty, zła interpretacja wyniku. Przeciwdziałanie: dobre opisy/schematy narzędzi, walidacja (np. Pydantic), mniej narzędzi naraz.
- **Zapętlenie (loop)** — powtarzanie tej samej akcji bez postępu, oscylacja, ponawianie błędnego wywołania. Przeciwdziałanie: limity kroków/tokenów/czasu, wykrywanie powtórzeń.
- **Dryf od celu (goal drift)** — w długim, wieloetapowym zadaniu agent „gubi" pierwotny cel, rozprasza się na poboczne wątki. Przeciwdziałanie: przypominanie celu w kontekście, dekompozycja, planner/executor, checkpoints.
- **Context rot / zatrucie kontekstu** — narastający, zaszumiony lub sprzeczny kontekst pogarsza decyzje (por. sekcja 6).
- **Kaskada błędów** — pomyłka we wczesnym kroku propaguje się i narasta w kolejnych.
- **Podatność na prompt injection** — zwłaszcza przy narzędziach i pobieranych treściach (por. sekcja 11).

Większość z nich adresuje się **guardrailami, limitami, walidacją, observability i HITL** — agent „samonaprawiający się" bez tych zabezpieczeń maskuje błędy, zamiast je usuwać.

## 2. Rozumowanie i planowanie (reasoning & planning)

**1. Czym jest Chain-of-Thought i jak wiąże się z jakością decyzji agenta?**

**Chain-of-Thought (CoT)** to skłonienie modelu, by **przed odpowiedzią wypisał pośrednie kroki rozumowania** („pomyśl krok po kroku"). Zamiast strzelać od razu wynikiem, model rozkłada problem na etapy.

Związek z jakością decyzji agenta:

- Daje modelowi „przestrzeń obliczeniową" — więcej tokenów na rozumowanie zwykle = lepsze decyzje w zadaniach wymagających wieloetapowego myślenia (matematyka, logika, wybór narzędzia).
- W agentach CoT to fundament każdego „Thought" w ReAct — uzasadnienie, *dlaczego* agent wybiera daną akcję.
- Daje **czytelny ślad** do debugowania (widać, gdzie rozumowanie się załamało).

Pułapki: CoT zużywa tokeny (koszt/latencja), bywa **post-hoc racjonalizacją** (model „uzasadnia" decyzję podjętą z innych powodów — ślad ≠ realna przyczyna), a wydłużone rozumowanie potrafi też skumulować błąd.

---

**2. ReAct vs plan-and-execute — zalety i wady.**

- **ReAct** — przeplata rozumowanie z akcjami; planuje „krok po kroku" reagując na obserwacje.
  - *Zalety*: adaptacyjny, zakotwiczony w świeżych wynikach, dobry przy nieprzewidywalnych ścieżkach.
  - *Wady*: każdy krok = wywołanie LLM (koszt/latencja), brak globalnego oglądu → ryzyko krótkowzroczności i dryfu w długich zadaniach.
- **Plan-and-execute** — najpierw **pełny plan** (lista kroków), potem wykonanie, często z tańszym modelem/kodem na etapie egzekucji.
  - *Zalety*: globalna spójność, mniej wywołań „dużego" modelu, łatwiej zrównoleglić i audytować plan, taniej.
  - *Wady*: plan ułożony „na ślepo" może się rozjechać z rzeczywistością → wymaga **replanningu**; sztywniejszy przy zmiennych warunkach.

W praktyce hybryda: planner tworzy szkielet, executor działa w stylu ReAct na podzadaniach, a przy odchyleniach uruchamiany jest replanning.

---

**3. Co to jest reflection / self-critique?**

To wzorzec, w którym agent **ocenia własny wynik i poprawia go w kolejnej iteracji** — osobny krok (lub osobna „persona"/agent-krytyk) sprawdza odpowiedź względem kryteriów (poprawność, kompletność, zgodność z wymaganiami) i zwraca uwagi, na podstawie których następuje poprawa.

Warianty: self-refine (ten sam model krytykuje i poprawia), generator+krytyk jako dwie role, reflection oparta o **sygnał zewnętrzny** (wynik testów, błąd kompilatora, walidacja schematu) — to najmocniejsza forma, bo krytyka jest obiektywna.

Pułapki: model bywa **zbyt pewny** i nie wyłapuje własnych błędów (samo „przejrzyj jeszcze raz" daje ograniczony zysk); każda runda to koszt; bez twardego sygnału reflection może „kręcić się w kółko". Zawsze ograniczaj liczbę iteracji.

---

**4. Planner vs executor — po co rozdzielać?**

- **Planner** — rozkłada cel na plan/podzadania, ustala kolejność i zależności (zwykle silniejszy model, rzadziej wywoływany).
- **Executor** — realizuje pojedyncze kroki: wywołuje narzędzia, generuje wynik (może być tańszy model lub wręcz deterministyczny kod).

Korzyści z rozdzielenia:

- **Klarowność i kontrola** — plan jest jawnym, audytowalnym artefaktem (można go zatwierdzić, zob. HITL).
- **Koszt** — drogie rozumowanie tylko w planowaniu, tania egzekucja w pętli.
- **Równoległość** — niezależne kroki planu można puścić jednocześnie.
- **Replanning** — gdy egzekucja się rozjedzie, wracasz do plannera, nie przebudowując wszystkiego.

Por. rozróżnienie orkiestrator vs planner: [[orkiestrator-vs-planner-w-architekturze-wieloagentowej]].

---

**5. Jak dekomponować złożone zadanie? Ryzyka zbyt drobnej / zbyt grubej dekompozycji.**

Dobra dekompozycja: podzadania **rozłączne, samowystarczalne** (mają wszystko, co potrzebne do wykonania), z jasnym kryterium „done" i jawnymi zależnościami (co można równolegle, co sekwencyjnie).

- **Zbyt gruba** (kroki za duże) — pojedynczy krok wciąż jest „mini-problemem", model się gubi, trudno zlokalizować błąd, mała szansa na równoległość.
- **Zbyt drobna** (kroki za małe) — eksplozja liczby wywołań LLM (koszt/latencja), narzut koordynacji, gubienie kontekstu między mikro-krokami, ryzyko dryfu i kaskady błędów.

Sztuka polega na trafieniu w „granulację", przy której każdy krok jest jednoznaczny i tani do zweryfikowania, a ich liczba pozostaje rozsądna.

---

**6. Co zrobić, gdy plan okazuje się błędny w trakcie? Jak realizuje się replanning?**

**Replanning** = wykrycie, że dotychczasowy plan przestał pasować do rzeczywistości, i wygenerowanie nowego (lub korekta istniejącego) na bazie zebranych obserwacji.

Wyzwalacze: krok zwrócił błąd/pusty wynik, obserwacje przeczą założeniom planu, pojawiły się nowe informacje, przekroczono budżet kroków dla podzadania.

Realizacja:
- pętla planner→executor z **krawędzią warunkową** wracającą do plannera, gdy executor sygnalizuje odchylenie (w LangGraph naturalnie jako conditional edge),
- planner dostaje **dotychczasowy postęp + powód niepowodzenia**, nie zaczyna od zera,
- **limit liczby replanów**, by uniknąć zapętlenia,
- przy poważnych odchyleniach — eskalacja do człowieka (HITL).

---

**7. Jak ograniczyć liczbę kroków/iteracji, nie psując jakości?**

- **Twarde limity**: max kroków (recursion limit), budżet tokenów, timeout — z kontrolowanym fallbackiem po przekroczeniu.
- **Lepsze narzędzia zamiast więcej kroków** — narzędzie zwracające bogatszy, gotowy wynik skraca pętlę (np. jedno zapytanie zamiast pięciu drobnych).
- **Plan-and-execute / batching** — zamiast wielu rund ReAct, zaplanuj i wykonaj hurtem; równoległe tool calls zamiast sekwencyjnych.
- **Dobór modelu** — silniejszy model często potrzebuje mniej kroków; routing słabszego do prostych kroków.
- **Wyraźne kryterium zakończenia** w promptcie + przypominanie „ile kroków zostało".
- **Caching** powtarzalnych wyników.

Klucz: limity to siatka bezpieczeństwa, a realną redukcję kroków daje **lepszy design narzędzi i promptu**, nie samo ucięcie pętli.

---

**8. Rozumowanie jawne vs modele „reasoning" z ukrytym łańcuchem myśli — co to zmienia w designie?**

- **Jawne rozumowanie** — model wypisuje kroki w wyjściu (klasyczny CoT/ReAct). Masz pełny wgląd i kontrolę nad śladem, ale tokeny rozumowania są w kontekście (koszt, ryzyko, że agent „działa" na własnych spekulacjach).
- **Modele reasoning** (z wbudowanym, ukrytym łańcuchem myśli) — robią rozumowanie „wewnętrznie" przed odpowiedzią; często lepsze w trudnych zadaniach „za jednym wywołaniem".

Co to zmienia:
- Mniejsza potrzeba ręcznego CoT-promptowania i wieloetapowych pętli „tylko po to, by model pomyślał".
- **Mniejsza widoczność** rozumowania → trudniejszy debug i guardrailing łańcucha myśli; bazujesz na wyniku, nie na śladzie.
- Inny profil kosztu/latencji (reasoning tokens) — model reasoning bywa droższy/wolniejszy na krok, ale potrafi zastąpić kilka kroków.
- Projektowo: część „myślenia" przenosisz do modelu zamiast budować ją jako jawne kroki grafu — prostszy graf, mniej kontroli.

---

**9. Czym jest Tree-of-Thoughts i kiedy w ogóle warto?**

**Tree-of-Thoughts (ToT)** uogólnia CoT: zamiast jednej liniowej ścieżki rozumowania, model **rozgałęzia się na wiele kandydujących kroków**, ocenia je i przeszukuje drzewo (BFS/DFS, z heurystyką), porzucając słabe gałęzie i wracając (backtracking) w lepsze.

Kiedy warto: zadania z **dużą przestrzenią rozwiązań i możliwością oceny częściowych stanów**, gdzie pojedyncza ścieżka łatwo wpada w ślepą uliczkę (łamigłówki, planowanie, gry, trudne dowody).

Kiedy *nie*: zdecydowana większość zadań produkcyjnych. ToT jest **bardzo drogi i wolny** (mnoży wywołania LLM o rzędy wielkości) i wymaga sensownej funkcji oceny. W praktyce rzadko opłacalny — najpierw ReAct/plan-and-execute + reflection.

---

**10. Jak zapobiegać dryfowi od celu w długich zadaniach?**

- **Trzymaj cel „na wierzchu"** — powtarzaj pierwotny cel/kryteria sukcesu w kontekście każdego kroku (nie pozwól mu wypaść z okna).
- **Dekompozycja + checklista** — jawna lista podzadań i odhaczanie postępu; planner/executor utrzymuje strukturę.
- **Stan/scratchpad** — utrwalony plan i dotychczasowe ustalenia w stanie (a nie tylko w rosnącej historii czatu).
- **Streszczanie** starszej historii zamiast jej narastania (przeciw context rot).
- **Punkty kontrolne** — okresowa weryfikacja „czy to wciąż służy celowi?" (self-critique) lub HITL.
- **Limity kroków** wymuszające domknięcie, nim agent się rozproszy.

## 3. Narzędzia i tool use

**1. Czym jest tool use / function calling? Jak model „decyduje" o wywołaniu narzędzia i argumentach?**

**Tool use (function calling)** to mechanizm, w którym modelowi udostępnia się **definicje narzędzi** (nazwa, opis, schemat argumentów w JSON Schema), a model — zamiast zwykłego tekstu — może zwrócić **ustrukturyzowane żądanie wywołania** narzędzia z konkretnymi argumentami. Aplikacja wykonuje narzędzie i **oddaje wynik z powrotem** do modelu jako kolejną wiadomość, po czym model kontynuuje.

„Decyzja" modelu nie jest magią: model został wytrenowany, by na podstawie **opisów narzędzi + bieżącego kontekstu** ocenić, czy któreś narzędzie pasuje do potrzeby, i wygenerować argumenty zgodne ze schematem. To wciąż predykcja tokenów — stąd jakość opisów i schematów wprost przekłada się na trafność. (W LangChain: `bind_tools`; por. [[narzedzia-dla-agentow-tool-use-langgraph]].)

---

**2. Jak zaprojektować dobry interfejs narzędzia?**

- **Nazwa** — czytelna, czasownikowa, jednoznaczna (`search_orders`, nie `do_stuff`).
- **Opis** — co robi, **kiedy używać i kiedy NIE**, jakie ma efekty uboczne, co zwraca. To najważniejszy element (zob. pyt. 3).
- **Schemat argumentów** — typy, pola wymagane vs opcjonalne, enumy zamiast wolnego tekstu tam, gdzie się da, opisy per-pole, sensowne wartości domyślne, walidacje (zakresy, formaty).
- **Granularność** — narzędzie powinno robić jedną rzecz dobrze; unikaj „kombajnów" z trybami sterowanymi flagą.
- **Zwracany wynik** — zwięzły, ustrukturyzowany, z czytelnym sygnałem błędu (a nie surowy zrzut 10k tokenów).
- **Odporność na pomyłki** — projektuj tak, by łatwą do popełnienia pomyłką nie dało się zrobić szkody (least privilege, zob. sekcja 11).

---

**3. Dlaczego opis narzędzia i parametrów to de facto część promptu?**

Bo model **nie widzi implementacji** — widzi wyłącznie nazwę, opis i schemat. To one trafiają do kontekstu i na ich podstawie model decyduje, czy i jak wywołać narzędzie. Opis narzędzia jest więc fragmentem instrukcji, tyle że „przyklejonym" do narzędzia.

Konsekwencje: doprecyzowanie opisu (kiedy używać, jednostki, formaty, przykłady, co oznaczają pola) potrafi **drastycznie poprawić trafność** wywołań — częściej niż zmiana modelu. Mglisty opis → model wywołuje złe narzędzie, myli argumenty, używa narzędzia poza intencją. Traktuj opisy narzędzi jak prompt: testuj, iteruj, wersjonuj.

---

**4. Jak walidować argumenty wygenerowane przez model? Gdzie wchodzi schemat (Pydantic)?**

Zasada: **nigdy nie ufaj argumentom z modelu** — to dane z granicy systemu. Dwie warstwy:

1. **Schematowa** — model generuje argumenty zgodne z JSON Schema, ale to nie gwarantuje sensowności. Przed wykonaniem parsuj/waliduj przez **Pydantic** (typy, pola wymagane, zakresy, formaty, enumy, walidatory niestandardowe). Niepoprawne → **odrzuć i oddaj modelowi czytelny błąd walidacji**, by poprawił argumenty (zamiast wykonywać).
2. **Biznesowa/uprawnieniowa** — czy wartości są dozwolone w tym kontekście (np. id należy do użytkownika, kwota w limicie, akcja w allowliście). To poza modelem, w kodzie narzędzia.

Pydantic służy tu jako kontrakt: definiuje schemat *podawany modelowi* i jednocześnie *waliduje* zwrócone argumenty — jedna definicja, dwie role.

---

**5. Jak obsłużyć błąd wykonania narzędzia? Oddać modelowi, ponowić, czy przerwać?**

Zależy od **rodzaju błędu**:

- **Błąd „naprawialny przez model"** (złe argumenty, walidacja, 404, niejednoznaczne zapytanie) → **oddaj błąd modelowi** jako obserwację, by skorygował kolejny krok. To często najlepsze.
- **Błąd przejściowy** (timeout, 5xx, rate limit) → **retry z backoffem**, idealnie z jitterem, z **twardym limitem prób**.
- **Błąd krytyczny/nieodwracalny lub brak uprawnień** → **przerwij** i zwróć kontrolowany komunikat / fallback / eskalacja do człowieka.

Unikanie pętli ponawiania: licznik prób per narzędzie, wykrywanie powtarzalnego identycznego wywołania, globalny limit kroków/budżet, oraz „nie oddawaj w nieskończoność tego samego błędu" — po N próbach zmień strategię lub przerwij. Por. [[obsluga-bledow-system-wieloagentowy]].

---

**6. Co robić, gdy narzędzi jest bardzo dużo (100+)?**

Problem: wszystkie definicje narzędzi siedzą w kontekście (koszt + szum), a model przy dziesiątkach podobnych narzędzi częściej wybiera złe (spadek trafności). Stąd zasada: **udostępniaj modelowi tylko narzędzia istotne dla danego kroku**.

Techniki:
- **Routing/selekcja narzędzi** — wstępny krok (klasyfikator lub retrieval po opisach narzędzi, „tool RAG") wybiera podzbiór 5–15 kandydatów, które dopiero trafiają do modelu.
- **Grupowanie/namespacing** — narzędzia pod „fasadą" (np. jedno narzędzie `database` z pod-operacjami), hierarchiczny wybór.
- **Multi-agent z wąskimi rolami** — każdy agent ma mały, spójny zestaw narzędzi (zob. sekcja 5).
- **Czytelne, rozróżnialne opisy** — by model nie mylił podobnych narzędzi.

---

**7. Jak zapewnić idempotentność i bezpieczeństwo narzędzi ze skutkami ubocznymi?**

Dla narzędzi mutujących (zapis do bazy, płatność, mail):

- **Idempotency key** — każda operacja z kluczem; powtórzone wywołanie z tym samym kluczem nie wykonuje akcji drugi raz (krytyczne, bo agent bywa ponawiany/retry’owany).
- **Walidacja + autoryzacja** przed wykonaniem (sekcja 11, least privilege).
- **HITL / approval gate** dla akcji nieodwracalnych (płatność, wysyłka, usunięcie) — zob. sekcja 9.
- **Potwierdzenia i podsumowanie** efektu zwracane modelowi, by wiedział, że akcja się powiodła (i nie powtarzał).
- **Dry-run / sandbox** tam, gdzie możliwe; transakcyjność i możliwość rollbacku.
- **Limity** (np. maks. kwota, maks. liczba maili) jako twarde bezpieczniki.

---

**8. Read-only vs narzędzia mutujące stan — wpływ na guardrails i HITL.**

- **Read-only** (wyszukiwanie, odczyt, RAG) — błąd modelu jest tani i odwracalny; można dawać dużą swobodę, minimalny HITL.
- **Mutujące stan** (zapis, płatność, usunięcie, wysyłka) — błąd bywa nieodwracalny i kosztowny; wymagają najmocniejszych zabezpieczeń.

Implikacje: rozdziel oba typy w architekturze, stosuj **least privilege**, **approval gate / HITL** głównie na akcjach mutujących, dokładną walidację argumentów, idempotentność, audyt/logowanie. Dobra heurystyka: „czytanie" może iść autonomicznie, „pisanie/działanie w świecie" przechodzi przez bramki kontroli — to wprost „budżet zaufania" z sekcji 14.

---

**9. Jak testować, że model wywołuje właściwe narzędzie z właściwymi argumentami?**

- **Asercje na wywołaniu, nie na finalnym tekście** — dla zestawu wejść sprawdzaj: czy wybrano właściwe narzędzie, czy argumenty są poprawne (dokładnie lub po kluczowych polach).
- **Mockowanie narzędzi** — podstaw atrapy zwracające ustalone wyniki; testujesz *decyzję* modelu w izolacji od realnych side-effectów.
- **Dataset przypadków** (wejście → oczekiwane narzędzie + argumenty), w tym przypadki brzegowe i „nie wywołuj żadnego narzędzia".
- **Walidacja schematu** — czy argumenty zawsze przechodzą Pydantic.
- **Ocena trajektorii** (sekcja 12) — przy wielokroku liczy się też kolejność i liczba wywołań.
- Ze względu na niedeterminizm: powtórzenia/progi (np. „≥9/10 trafień"), a realne porażki produkcyjne zamieniaj w nowe testy regresji.

---

**10. Czym jest MCP (Model Context Protocol) i jaki problem rozwiązuje?**

**MCP** to **otwarty standard (protokół) podłączania narzędzi, danych i zasobów do agentów/LLM** — „USB-C dla narzędzi AI". Zamiast pisać dla każdej aplikacji własną, niekompatybilną integrację narzędzi, definiujesz **serwer MCP** wystawiający narzędzia/zasoby/prompty w ustandaryzowany sposób, a dowolny **klient MCP** (np. agent) może je odkryć i wywołać.

Problem, który rozwiązuje: **kombinatoryczna eksplozja integracji M×N** (M aplikacji × N narzędzi) sprowadzona do **M+N** dzięki wspólnemu protokołowi; reużywalność, interoperacyjność i oddzielenie dostawcy narzędzia od konsumenta. Por. [[mcp-ai-engineer-interview]].

---

**11. Jak realizować równoległe wywołania narzędzi i kiedy to ma sens?**

Współczesne modele potrafią w jednej odpowiedzi zwrócić **wiele tool calls naraz** (parallel tool calling); runtime wykonuje je równolegle i oddaje komplet wyników. Można też zrównoleglać po stronie grafu (fan-out/fan-in, zob. [[rownolegle-wezly-fan-out-fan-in-langgraph]]).

**Ma sens**, gdy wywołania są **niezależne** (nie potrzebują nawzajem swoich wyników): np. pobranie pogody dla 3 miast, przeszukanie kilku źródeł jednocześnie. Skraca latencję.

**Nie ma sensu / jest błędem**, gdy istnieje **zależność** (wynik A jest argumentem B) — wtedy sekwencja jest konieczna. Uwaga też na: kolejność efektów ubocznych, limity rate, koszt równoległych zapytań i trudniejszą obsługę częściowych porażek (część calli padła). Reguła: **równolegle to, co niezależne; sekwencyjnie to, co zależne**.

## 4. Pamięć i stan (memory & state)

**1. Pamięć krótkoterminowa vs długoterminowa.**

- **Krótkoterminowa** — kontekst **bieżącej sesji**: prompt, historia rozmowy, wyniki narzędzi, stan przebiegu. Żyje w oknie kontekstu modelu, znika (lub jest streszczana) po sesji. Ograniczona rozmiarem kontekstu.
- **Długoterminowa** — wiedza **trwała między sesjami**: preferencje użytkownika, fakty, wcześniejsze ustalenia. Przechowywana poza modelem (baza wektorowa, dokumentowa, relacyjna) i **selektywnie pobierana** do kontekstu, gdy potrzebna.

Skrótowo: krótkoterminowa = „to, co teraz w głowie"; długoterminowa = „to, co zapisane na dysku i przywoływane na żądanie".

---

**2. Stan vs pamięć — co gdzie trzymać?**

- **Stan (state) przebiegu** — robocza struktura *bieżącego* wykonania: aktualny plan, dotychczasowe kroki, wyniki pośrednie, licznik iteracji, flagi kontrolne. Efemeryczny dla danego threadu/uruchomienia (w LangGraph: obiekt `State` z reducerami).
- **Pamięć (memory)** — informacja, która ma **przetrwać** poza bieżący przebieg: historia rozmów do przywołania, profil użytkownika, zgromadzona wiedza.

Reguła: w **stanie** — to, czym steruje pętla *teraz*; w **pamięci trwałej** — to, co chcesz odzyskać *później/w innej sesji*. Granica bywa płynna: checkpointing potrafi utrwalić stan (zob. pyt. 8), ale rolą jest tam wznawianie, nie „wiedza".

---

**3. Historia przekraczająca okno kontekstu — trimming, summarization, retrieval.**

- **Trimming** — odcinanie najstarszych wiadomości (sliding window), zwykle z zachowaniem system promptu i kilku ostatnich tur. Proste i tanie, ale **bezpowrotnie gubi** starszy kontekst.
- **Summarization** — streszczanie starszej historii do zwięzłego podsumowania, które zostaje w kontekście zamiast surowych wiadomości. Zachowuje sens, kosztuje dodatkowe wywołanie LLM i ryzykuje utratę detali.
- **Selektywne pobieranie (retrieval)** — całą historię trzymasz poza kontekstem (np. baza wektorowa) i dociągasz **tylko fragmenty istotne** dla bieżącego pytania. Skaluje się najlepiej, ale zależy od jakości retrievalu.

W praktyce **hybryda**: system prompt + kilka ostatnich tur (raw) + podsumowanie środka + doszukane istotne fragmenty z przeszłości.

---

**4. Czym jest context window i jakie są skutki jego przepełnienia?**

**Context window** to maksymalna liczba tokenów (wejście + wyjście), jaką model „widzi" w jednym wywołaniu — system prompt, historia, pobrane dokumenty, opisy narzędzi i odpowiedź muszą się w nim zmieścić.

Skutki przepełnienia / nadmiernego zapełnienia:
- **Twarde** — przekroczenie limitu = błąd albo wymuszone ucięcie (model traci początek/koniec, czasem „gubi" instrukcje systemowe).
- **Miękkie (degradacja jakości)** — nawet w granicach limitu długi, zaszumiony kontekst pogarsza decyzje: **„Lost in the Middle"** (model słabiej korzysta z informacji w środku), **context rot** (narastający szum/sprzeczności), wyższy koszt i latencja.

Stąd waga **context engineering** (sekcja 6): wkładać tylko to, co potrzebne, i pilnować budżetu okna.

---

**5. Pamięć epizodyczna vs semantyczna vs proceduralna.**

Analogia do pamięci ludzkiej (por. [[pamięć-długoterminowa-ai]]):

- **Epizodyczna** — konkretne *zdarzenia/interakcje* z przeszłości („w poprzedniej sesji user prosił o X"). Realizacja: zapis przebiegów/rozmów + retrieval, często few-shot z przeszłych epizodów.
- **Semantyczna** — *fakty i wiedza* oderwane od konkretnego zdarzenia („user jest wegetarianinem", „firma działa w UE"). Realizacja: baza faktów/profil, baza wektorowa lub graf wiedzy.
- **Proceduralna** — *jak coś robić*: utrwalone instrukcje, reguły, wyuczone procedury (często w system prompcie lub jako narzędzia/playbooki). „Mięśniowa pamięć" agenta.

Projektowo: rozdziel te typy, bo mają różny cykl życia i sposób pobierania — fakty aktualizujesz, epizody archiwizujesz i przeszukujesz, procedury wersjonujesz.

---

**6. Pamięć długoterminowa na bazie wektorowej — jak i jakie pułapki?**

Jak: informacje (fakty, fragmenty rozmów) są **embeddowane** i zapisywane w bazie wektorowej z metadanymi (user_id, timestamp, typ); przy potrzebie robisz **wyszukiwanie po podobieństwie** i wstrzykujesz najtrafniejsze do kontekstu. Zapis bywa wyzwalany regułą lub osobnym krokiem „co warto zapamiętać".

Pułapki:
- **Nieaktualne wspomnienia** — stary fakt zostaje, mimo że się zmienił („mieszka w Krakowie" po przeprowadzce). Trzeba wersjonować/aktualizować i ważyć świeżością.
- **Sprzeczne fakty** — baza zwraca dwie wykluczające się informacje; potrzebny mechanizm rozstrzygania (najnowszy wygrywa, źródło, jawna reconciliacja).
- **Retrieval nie po znaczeniu** — semantyczne podobieństwo ≠ trafność; ryzyko dociągnięcia mylących fragmentów.
- **Prywatność/izolacja** — twarde filtrowanie po user_id, by nie wyciekła pamięć innego użytkownika.
- **Rozrost i szum** — bez „zapominania" baza puchnie i pogarsza trafność.

---

**7. Wiele równoległych sesji/użytkowników — jak nie pomieszać?**

- **Klucz izolacji** — każda konwersacja pod własnym identyfikatorem (np. `thread_id`), każdy użytkownik pod `user_id`; pamięć i stan **partycjonowane** po tych kluczach.
- **Twarde filtrowanie** przy odczycie pamięci długoterminowej (zawsze `where user_id = ...`), by nie wyciekł kontekst innej osoby.
- **Bezstanowość warstwy aplikacji** — stan trzymany w store/checkpointerze po `thread_id`, nie w zmiennych globalnych/procesie (bezpieczne przy współbieżności i skalowaniu poziomym).
- **Rozdział „per-thread" (historia danej rozmowy) od „per-user" (wiedza o użytkowniku wspólna dla jego sesji).**

W LangGraph realizuje to `thread_id` + checkpointer (izolacja stanu wątków). Por. [[memory-management-i-session-handling]], [[projektowanie-memory-management-oraz-session-handling-dla-agentow-ai]].

---

**8. Persistence / checkpointing — co to i po co?**

**Checkpointing** to **zapisywanie snapshotu stanu agenta** (po każdym kroku/węźle) do trwałego backendu, dzięki czemu przebieg nie żyje tylko w pamięci procesu.

Po co:
- **Wznawianie (resume)** — po awarii, restarcie procesu czy przerwaniu (HITL) agent kontynuuje od ostatniego checkpointu, nie od zera.
- **Human-in-the-loop** — graf można wstrzymać (interrupt), poczekać na decyzję człowieka i wznowić z zachowanym stanem (zob. sekcja 9, [[interrupts-langgraph]]).
- **Time-travel / debug** — cofnięcie do wcześniejszego checkpointu, podejrzenie/edycja stanu, „odtworzenie" trajektorii i puszczenie alternatywnej ścieżki.
- **Odporność na awarie** i długo żyjące, wielosesyjne konwersacje.

W LangGraph: checkpointery z backendem in-memory/SQLite/Postgres (zob. [[checkpointers-langgraph]], [[persistence-sqlite-postgres-langgraph]]).

---

**9. Mechanizm „zapominania" / aktualizacji nieaktualnych informacji.**

- **Aktualizacja zamiast dopisywania** — gdy fakt się zmienia, **nadpisz/zwersjonuj** wpis (upsert po kluczu encji), zamiast dokładać sprzeczny obok.
- **Metadane czasu i źródła** — timestamp, źródło, „ważność do"; przy konflikcie wygrywa **najnowszy/najbardziej wiarygodny**.
- **TTL / decay** — wygaszanie lub obniżanie wagi starych, nieużywanych wspomnień; archiwizacja zamiast trzymania wszystkiego w aktywnym indeksie.
- **Reconciliacja** — okresowy (lub wyzwalany) krok wykrywający i scalający sprzeczne fakty, ewentualnie z potwierdzeniem od użytkownika.
- **Jawne „zapomnij to"** — operacja usunięcia na żądanie (także ze względów prywatności / RODO).
- **Walidacja przy odczycie** — przy konflikcie nie wstrzykuj obu wersji do kontekstu (źródło halucynacji), tylko rozstrzygnij przed użyciem.

## 5. Systemy wieloagentowe i orkiestracja

**1. Kiedy warto przejść z jednego agenta na system wieloagentowy? Jakie problemy to rozwiązuje, a jakie tworzy?**

Przechodzisz, gdy pojawia się **konkretny ból single-agenta**, a nie „bo brzmi dojrzalej":

- **Przeładowany kontekst** — jeden agent ma za dużo narzędzi i instrukcji naraz, trafność wyboru narzędzia spada → rozbij na agentów z wąskimi zestawami.
- **Rozłączne specjalizacje** — zadanie naturalnie dzieli się na role (research / kodowanie / weryfikacja), z których każda chce innego promptu, narzędzi, a czasem innego modelu.
- **Równoległość** — np. kilku researcherów przeszukujących źródła jednocześnie skraca czas (fan-out).
- **Izolacja błędów** — porażka jednego workera nie wywraca całości.

**Rozwiązuje**: czytelniejszy podział odpowiedzialności, mniejsze i lepiej testowalne konteksty, skalowanie przez specjalizację.

**Tworzy**: wzrost kosztu i latencji (więcej wywołań LLM, rundy komunikacji), gubienie kontekstu w handoffach, nowe tryby porażki (agenci zapętleni w „rozmowie", sprzeczne wyniki), trudniejszy debug/tracing, ryzyko przeinżynierowania. Reguła: zacznij od single-agent, dziel dopiero pod realny ból (por. sekcja 1, pyt. 10 i sekcja 14).

---

**2. Opisz wzorzec supervisor / orchestrator — jeden agent koordynujący pracę wyspecjalizowanych agentów.**

**Supervisor** to centralny agent-koordynator, który nie wykonuje zadania merytorycznego sam, tylko **decyduje, którego workera (sub-agenta) uruchomić** dla danego podzadania, przekazuje mu potrzebny kontekst, odbiera wynik i decyduje o kolejnym kroku — aż uzna cel za osiągnięty.

- Workerzy są wyspecjalizowani (własny prompt, wąski zestaw narzędzi, czasem własny model) i zwykle nie znają się nawzajem — komunikują się przez supervisora.
- W LangGraph realizuje się to jako węzeł-supervisor z krawędziami warunkowymi kierującymi do podgrafów-workerów i z powrotem (por. [[multi-agent-supervisor-langgraph]], [[agentic-workflows-multi-agent-orchestration]]).

Zalety: czytelna, gwiazdista topologia (łatwy routing i kontrola), prosty audyt „kto co robił", łatwo dołożyć workera. Wady: supervisor to wąskie gardło i pojedynczy punkt decyzyjny; każdy hop przez niego to dodatkowe wywołanie LLM (koszt/latencja).

---

**3. Czym różni się orkiestrator od plannera w architekturze wieloagentowej?**

To dwie różne funkcje, czasem mylone, bo bywają w jednym komponencie (por. [[orkiestrator-vs-planner-w-architekturze-wieloagentowej]]):

- **Planner** — *co* trzeba zrobić: rozkłada cel na plan/podzadania, ustala kolejność i zależności. Produkuje **plan** jako artefakt (myślenie).
- **Orkiestrator** — *kto i kiedy* to wykona: w czasie wykonania routuje podzadania do właściwych agentów/narzędzi, zarządza przepływem, stanem, równoległością, błędami i warunkiem stopu (egzekucja/dyrygowanie).

Skrótowo: planner układa partyturę, orkiestrator nią dyryguje. W prostych systemach jeden agent robi oba; w większych rozdziela się je (planner = silny model, rzadko; orkiestrator = lekka logika sterująca, często deterministyczna).

---

**4. Porównaj topologie: hierarchiczną, sieciową/swarm i sekwencyjny pipeline. Kiedy która?**

(Por. [[langchain-multi-agent-patterns]], [[wzorce-projektowe-systemow-agentowych]].)

- **Hierarchiczna (supervisor → workerzy)** — koordynator deleguje do specjalistów. Najlepsza, gdy zadanie dzieli się na rozłączne role i chcesz centralnej kontroli/audytu. Skaluje się dobrze, łatwy routing; ale supervisor to wąskie gardło.
- **Sieciowa / swarm (peer-to-peer)** — agenci przekazują kontrolę bezpośrednio sobie (handoff bez centrali). Elastyczna przy dynamicznej współpracy bez sztywnej hierarchii; ale trudna do kontroli, podatna na zapętlenia i trudny debug — rzadko potrzebna.
- **Sekwencyjny pipeline** — agenci/etapy w ustalonej kolejności (wyjście jednego = wejście następnego), np. ekstrakcja → analiza → raport. Najprostszy, przewidywalny, łatwy do testowania; ale sztywny — to w praktyce workflow, nie „prawdziwy" multi-agent.

Reguła: zacznij od pipeline'u, gdy ścieżka znana; hierarchia, gdy potrzebna dynamiczna delegacja z kontrolą; swarm tylko gdy współpraca jest z natury nieprzewidywalna i naprawdę nie da się jej zhierarchizować.

---

**5. Jak agenci powinni się komunikować — współdzielony stan, przekazywanie wiadomości czy handoff? Kompromisy.**

Trzy modele (często łączone):

- **Współdzielony stan (shared state / blackboard)** — agenci czytają i piszą do wspólnej struktury stanu. Zaleta: pełna widoczność, brak duplikacji kontekstu. Wada: ryzyko „context bleed" (agent widzi nieistotne dla niego dane), konflikty zapisu, gorsza izolacja.
- **Przekazywanie wiadomości (message passing)** — agenci wymieniają jawne komunikaty. Czytelny ślad „kto co powiedział", dobre dla luźno powiązanych ról; ale rosnąca historia czatu między agentami puchnie i szumi.
- **Handoff** — jeden agent przekazuje kontrolę (i wybrany kontekst) drugiemu. Czyste przekazanie odpowiedzialności; ale trzeba świadomie zdecydować, *co* przekazać (pyt. 6).

Kompromis: shared state jest wygodny w LangGraph (jeden `State`), ale przekazuj sub-agentowi **wycinek** istotny dla niego, nie cały stan — inaczej tracisz korzyść ze specjalizacji i rozdmuchujesz kontekst.

---

**6. Czym jest handoff między agentami i jak przekazać kontekst, by odbiorca miał to, czego potrzebuje (a nie wszystko)?**

**Handoff** to przekazanie kontroli (i danych) od jednego agenta do drugiego — odbiorca przejmuje zadanie od miejsca, w którym nadawca skończył.

Klucz: **nie przekazuj całej historii**. Pełny zrzut kontekstu rozdmuchuje okno, szumi i niweczy specjalizację. Zamiast tego przekaż **skondensowany ładunek zadania**:

- jasno sformułowane podzadanie i kryterium „done",
- tylko istotne fakty/wyniki dotychczasowe (wyciąg, nie transkrypt),
- ewentualne ograniczenia i format oczekiwanego wyniku.

Realizacja: nadawca (lub supervisor) tworzy **strukturalne podsumowanie** dla odbiorcy; w LangGraph przekazujesz wybrany wycinek stanu, a nie całą listę wiadomości. Dobry handoff to „brief", a nie „cała teczka". Złe handoffy (gubiące lub przeładowane kontekstem) to główny tryb porażki multi-agentów.

---

**7. Jak rozłożyć role i odpowiedzialności między agentów, żeby uniknąć nakładania się kompetencji i konfliktów?**

- **Rozłączność (single responsibility)** — każdy agent ma jeden, jasno opisany zakres; brak dwóch agentów uprawnionych do tej samej decyzji/akcji.
- **Wąski zestaw narzędzi per rola** — narzędzia przypisane do roli, nie współdzielone „wszystko dla wszystkich" (mniejszy kontekst, mniej pomyłek, łatwiejszy audyt).
- **Jeden właściciel decyzji** — dla każdej decyzji/zapisu jasno wskazany agent odpowiedzialny (unikasz sytuacji „obaj myśleli, że zrobi drugi" albo sprzecznych zapisów).
- **Jawne kontrakty wejścia/wyjścia** między rolami (structured output), by granice były egzekwowalne.
- **Centralna koordynacja** (supervisor) zamiast swobodnej peer-to-peer, gdy ryzyko konfliktu jest realne.

Heurystyka: projektuj role jak mikroserwisy — wysoka kohezja, niskie sprzężenie, jasne API między nimi.

---

**8. Jak obsługiwać błędy w systemie wieloagentowym — propagacja, izolacja, retry, fallback?**

(Por. [[obsluga-bledow-system-wieloagentowy]].)

- **Izolacja** — błąd workera nie powinien wywracać całego systemu; supervisor łapie porażkę sub-agenta i decyduje, co dalej (granica błędu wokół każdego agenta).
- **Retry** — przejściowe błędy (timeout, 5xx) ponawiane z backoffem i twardym limitem prób, najlepiej na poziomie konkretnego workera/narzędzia.
- **Propagacja vs pochłonięcie** — błąd „naprawialny" oddaj agentowi/supervisorowi jako obserwację do korekty; błąd krytyczny propaguj w górę do kontrolowanego zakończenia, nie ukrywaj go.
- **Fallback** — alternatywna ścieżka: inny worker, prostszy tryb, degradacja funkcji, w ostateczności eskalacja do człowieka (HITL).
- **Brak cichego maskowania** — self-healing bez limitów i logowania ukrywa błędy zamiast je usuwać (anty-wzorzec, sekcja 14). Wszystko z observability/tracingiem, by dało się wskazać, który agent zawiódł.

---

**9. Jak kontrolować koszt i latencję, które rosną z liczbą agentów i rund komunikacji?**

- **Minimalizuj liczbę hopów** — każda runda przez supervisora i każdy handoff to wywołanie LLM; nie mnóż agentów ponad realną potrzebę.
- **Routing modeli / kaskadowanie** — tańszy/mniejszy model do prostych workerów i rutynowych decyzji, silny tylko tam, gdzie trzeba (por. [[wyjasnij-teraz-model-routing-kaskadowanie-modeli]]).
- **Równoległość** — niezależne podzadania puszczaj jednocześnie (fan-out/fan-in), by latencja nie była sumą, lecz maksimum (por. [[rownolegle-wezly-fan-out-fan-in-langgraph]]).
- **Chudy kontekst w handoffach** — przekazuj wyciąg, nie transkrypt (mniej tokenów na każdą rundę).
- **Prompt caching** powtarzalnych fragmentów (system prompty workerów).
- **Twarde limity** — budżet kroków/tokenów/rund na cały system, nie tylko na agenta.
- **Deterministyczny kod zamiast agenta** tam, gdzie decyzja nie wymaga LLM (np. routing po regule).

---

**10. Jak zapobiec sytuacji, w której dwóch agentów „zapętla się" w nieproduktywnej rozmowie albo wzajemnie się blokuje?**

- **Limit rund komunikacji** między agentami (i globalny recursion limit całego grafu) z kontrolowanym przerwaniem.
- **Wykrywanie braku postępu** — te same wiadomości/wyniki powtarzane, brak zmiany stanu → przerwij lub eskaluj.
- **Centralny arbiter (supervisor)** zamiast swobodnej peer-to-peer dyskusji — to supervisor decyduje o zakończeniu, agenci nie „negocjują" w nieskończoność.
- **Jasne kryterium „done"** dla każdej interakcji i jawny warunek stopu (kto i kiedy kończy wątek).
- **Unikanie cykli zależności** w topologii (A czeka na B, B na A) — projektuj graf bez zakleszczeń, z timeoutami.
- **Tracing**, by zobaczyć oscylację i zamienić ją w guard/test regresyjny.

---

**11. Jak zaprojektować mechanizm konsensusu / rozstrzygania sporów, gdy agenci dają sprzeczne wyniki?**

- **Wyznaczony arbiter** — supervisor lub osobny agent-sędzia rozstrzyga na podstawie kryteriów (najczęstsza i najprostsza opcja).
- **Głosowanie / majority vote** — przy kilku niezależnych wynikach bierzesz dominujący (dobre, gdy odpowiedzi są porównywalne i dyskretne).
- **Reguła pierwszeństwa** — jawna hierarchia źródeł/ról (np. wynik zweryfikowany narzędziem > wynik wygenerowany), „najświeższy/najbardziej wiarygodny wygrywa".
- **Sygnał zewnętrzny jako rozjemca** — gdy się da, rozstrzygaj obiektywnie (uruchom test, zweryfikuj w bazie), nie kolejnym promptem.
- **Krok reconciliacji** — agent łączy/uzgadnia sprzeczne wyniki, jawnie zaznaczając rozbieżność.
- **Eskalacja do człowieka** (HITL), gdy stawka wysoka, a automatyczne rozstrzygnięcie niepewne.

Ważne: nie wstrzykuj obu sprzecznych wyników dalej bez rozstrzygnięcia — to źródło halucynacji (analogicznie do sprzecznych faktów w pamięci, sekcja 4).

## 6. Kontekst, RAG i context engineering w agentach

**1. Czym jest context engineering i dlaczego bywa ważniejsze od wyboru samego modelu?**

**Context engineering** to dyscyplina **świadomego doboru i organizacji tego, co trafia do okna kontekstu** w danym kroku — instrukcji, historii, pobranych dokumentów, opisów narzędzi, wyników pośrednich — tak, by model miał *dokładnie* to, czego potrzebuje, i nic ponadto (por. [[czy-znasz-termin-context-engineering-w-ai]]).

Dlaczego bywa ważniejsze od wyboru modelu: model operuje wyłącznie na tym, co dostanie w kontekście. Nawet najlepszy model podejmie złą decyzję na złym/zaszumionym/niekompletnym kontekście, a słabszy z dobrze przygotowanym kontekstem często go pobije. W praktyce więcej zysku daje doszlifowanie *co* i *jak* wkładamy do okna (lepszy retrieval, lepsze opisy narzędzi, zwięzła historia) niż podmiana modelu na większy. To także bezpośrednio steruje kosztem i latencją (tokeny) oraz jakością (Lost in the Middle, context rot).

---

**2. Jak agent powinien decydować, jaki kontekst pobrać do danego kroku (a nie wrzucać wszystkiego naraz)?**

Zasada: **just-in-time, nie just-in-case** — dociągaj kontekst pod konkretną potrzebę kroku, nie „na zapas".

- **Retrieval sterowany zapytaniem** — pobieraj fragmenty istotne dla bieżącego podzadania (semantycznie + filtry po metadanych), a nie cały korpus.
- **Agent jako decydent** — to model (agentic RAG, pyt. 3) decyduje, *czy* w ogóle szukać i *czego*, formułując zapytanie zamiast dostawać wszystko z góry.
- **Pamięć selektywnie** — z długoterminowej przywołuj tylko trafne wpisy (po `user_id`, świeżości, podobieństwie).
- **Narzędzia selektywnie** — tylko podzbiór istotny dla kroku (tool routing, sekcja 3).
- **Streszczaj, nie wklejaj** — zamiast surowych transkryptów wstrzykuj wyciągi.

Cel: maksymalizować „signal-to-noise" w oknie; każdy zbędny token to koszt i ryzyko rozproszenia uwagi modelu.

---

**3. Jak łączysz RAG z agentem? Czym różni się „RAG jako pojedynczy krok" od agentic RAG?**

- **RAG jako pojedynczy krok (klasyczny)** — stały pipeline: `pytanie → retrieve → wstrzyknij → generuj`. Wyszukiwanie zawsze się dzieje, raz, niezależnie od tego, czy jest potrzebne. Proste, tanie, przewidywalne — dobre dla wąskich Q&A.
- **Agentic RAG** — retrieval jest **narzędziem**, a agent **sam decyduje** w pętli: czy w ogóle szukać, czego, w którym źródle, czy doszukać jeszcze raz po słabych wynikach, jak przeformułować zapytanie, kiedy ma dość, by odpowiedzieć. Może łączyć wiele źródeł i iterować.

Różnica: klasyczny RAG to *workflow* (ścieżka zakodowana), agentic RAG to *agent* (model steruje retrievalem). Agentic radzi sobie z pytaniami wieloźródłowymi i takimi, które wymagają kilku rund wyszukiwania, ale jest droższy i mniej przewidywalny. Wybór jak w sekcji 1: prosty RAG, dopóki wystarcza; agentic, gdy zapytania wymagają decyzji o tym, *czego* szukać.

---

**4. Jak radzić sobie ze zjawiskiem „Lost in the Middle" przy długim kontekście agenta?**

„Lost in the Middle" = model najlepiej wykorzystuje informacje na **początku i końcu** kontekstu, a słabiej te w środku długiego okna. Przeciwdziałanie:

- **Krótszy, gęstszy kontekst** — nie wrzucaj wszystkiego; mniej, ale trafniej (context engineering).
- **Pozycjonowanie** — najważniejsze informacje (instrukcje, kluczowe dokumenty) na początku lub na końcu, nie zatopione w środku.
- **Re-ranking** — po retrievalu układaj fragmenty wg trafności i ograniczaj ich liczbę (top-k), zamiast wrzucać dziesiątki.
- **Streszczanie/kompresja** zamiast surowych, długich fragmentów.
- **Dekompozycja** — rozbij zadanie na mniejsze kroki z węższym kontekstem każdy, zamiast jednego mega-promptu.

Zjawisko bezpośrednio łączy się z context window i jego degradacją (sekcja 4, pyt. 4).

---

**5. Czym jest context rot / zatrucie kontekstu w długiej sesji i jak temu przeciwdziałać?**

**Context rot** to stopniowa **degradacja jakości decyzji w miarę narastania kontekstu** w długiej sesji: okno zapełnia się starymi, nieistotnymi, powtarzalnymi lub **sprzecznymi** informacjami (w tym błędnymi wynikami i halucynacjami z wcześniejszych kroków), które zaszumiają i mylą model — zwłaszcza gdy agent zaczyna „działać na własnych spekulacjach".

Przeciwdziałanie:

- **Streszczanie** starszej historii zamiast jej kumulowania (sekcja 4, pyt. 3).
- **Trimming** nieistotnych tur i wyników narzędzi.
- **Świeży, czysty kontekst per podzadanie** — handoffy z wyciągiem, a nie z całym transkryptem; w multi-agent każdy worker dostaje czysty brief.
- **Rozstrzyganie sprzeczności** przed wstrzyknięciem (nie zostawiaj dwóch wykluczających się faktów w oknie).
- **Trzymanie celu „na wierzchu"** (przeciw dryfowi, sekcja 2).
- **Limity długości sesji** / resetowanie z przeniesieniem trwałych ustaleń do pamięci.

---

**6. Jak realizować structured output, żeby wyniki agenta były maszynowo przetwarzalne i walidowalne?**

(Por. [[structured-output-z-llm]], [[with_structured_output_vs_pydantic_parser]].)

- **Zdefiniuj schemat** (Pydantic / JSON Schema) jako kontrakt wyjścia — typy, pola wymagane, enumy, zakresy.
- **Wymuś go na modelu** — przez natywny structured output / function calling dostawcy (model zwraca dane zgodne ze schematem), nie przez „proszę o JSON" w prompcie. W LangChain: `with_structured_output` (pyt. 7.5).
- **Waliduj po stronie kodu** — parsuj przez Pydantic; niepoprawne odrzuć i ewentualnie oddaj modelowi błąd do korekty (retry na walidacji).
- **Schemat = granica systemu** — structured output to miejsce, gdzie niedeterministyczne wyjście LLM staje się deterministycznym, walidowalnym artefaktem do dalszego przetwarzania.

To kluczowe dla agentów, bo wyniki jednego kroku/agenta zasilają następne — muszą być parsowalne, nie „prozą".

---

**7. Jaką rolę pełni prompt orchestration w sterowaniu wieloma krokami/promptami agenta?**

(Por. [[ai-prompt-orchestration]], [[w-temacie-llm-integration-orchestration-czym-jest-prompt-orchistration]].)

**Prompt orchestration** to warstwa **koordynująca wiele wywołań/promptów** w jeden spójny przepływ: komponuje kroki, przekazuje wyjście jednego jako wejście kolejnego, zarządza szablonami promptów, warunkowym rozgałęzianiem, równoległością i ponawianiem.

Rola w agencie:

- **Sekwencjonowanie i routing** — który prompt/krok wykonać następnie (w workflow zakodowane, w agencie częściowo delegowane modelowi).
- **Wstrzykiwanie kontekstu** — składanie właściwych danych (retrieval, historia, wynik poprzedniego kroku) do każdego promptu.
- **Spójność i wersjonowanie** — szablony zamiast sklejania stringów; łatwiej testować i wersjonować (sekcja 10).
- **Granica między „kodem sterującym" a „myśleniem modelu"** — orchestration trzyma deterministyczny szkielet, w który wpięte są wywołania LLM.

W LangChain/LangGraph rolę tę pełnią LCEL (kompozycja łańcuchów) i graf (kompozycja kroków agenta).

---

**8. Jak budżetować okno kontekstu między: instrukcje, historię, pobrane dokumenty i opisy narzędzi?**

Traktuj okno jak **ograniczony budżet tokenów** i świadomie alokuj, z marginesem na odpowiedź modelu:

- **Instrukcje (system prompt)** — zwykle stałe i nienaruszalne; trzymaj zwięzłe, ale nie przycinaj (to konstytucja agenta).
- **Opisy narzędzi** — tylko podzbiór istotny dla kroku (tool routing); przy 100+ narzędziach to one zżerają okno (sekcja 3, pyt. 6).
- **Pobrane dokumenty (RAG)** — najtwardziej ograniczaj: top-k + re-ranking, krótkie trafne fragmenty zamiast całych dokumentów; to zwykle największy i najbardziej elastyczny składnik.
- **Historia** — kilka ostatnich tur raw + streszczenie środka + doszukane istotne fragmenty (hybryda z sekcji 4).

Reguła praktyczna: priorytet ma to, co **niezbędne dla bieżącej decyzji**; rezerwuj zapas na wyjście; monitoruj realne zużycie tokenów (observability) i dynamicznie tnij najmniej istotny składnik (zwykle dokumenty/historię), zanim przekroczysz limit. Mniej i trafniej > więcej (Lost in the Middle, context rot).

## 7. LangChain (framework)

**1. Z jakich głównych komponentów składa się ekosystem LangChain i za co odpowiadają?**

(Por. [[komponenty-ekosystemu-langchain]].)

- **Modele (chat models / LLMs)** — ujednolicony interfejs do różnych dostawców (OpenAI, Anthropic…), w tym `bind_tools` i structured output.
- **Prompty (prompt templates)** — szablony z parametrami zamiast sklejania stringów.
- **Output parsers / structured output** — zamiana wyjścia LLM na ustrukturyzowane, walidowalne dane.
- **Narzędzia (tools)** i tool calling — definiowanie i wywoływanie funkcji przez model.
- **Retrievery / vector stores / embeddings / document loaders / splitters** — warstwa RAG.
- **Pamięć / chat history** — zarządzanie historią konwersacji.
- **LCEL** — język kompozycji tych elementów w łańcuchy (pyt. 2).

Wokół biblioteki: **LangGraph** (orkiestracja agentów jako graf), **LangSmith** (observability/tracing/eval), integracje (`langchain-*`). Skrótowo: LangChain dostarcza **klocki + spoiwo** do budowy aplikacji LLM, niezależnie od dostawcy.

---

**2. Czym jest LCEL (LangChain Expression Language) i jaki problem rozwiązuje?**

**LCEL** to deklaratywny sposób **komponowania komponentów w łańcuch** operatorem `|` (pipe), gdzie każdy element jest `Runnable` (wspólny interfejs `invoke`/`stream`/`batch`): `prompt | model | parser`.

Problem, który rozwiązuje: zamiast ręcznie spinać wywołania w imperatywnym kodzie, dostajesz jednolity, kompozycyjny interfejs, który **za darmo** daje:

- **streaming, batching i async** — bez dopisywania ich osobno dla każdego kroku,
- **równoległość** (`RunnableParallel`) i przekazywanie/mapowanie danych (`RunnablePassthrough`),
- **spójne tracing/observability** (każdy Runnable widoczny w LangSmith),
- łatwą podmianę i ponowne użycie fragmentów łańcucha.

Skrótowo: LCEL standaryzuje „jak składać kroki" i odejmuje boilerplate wokół wykonywania.

---

**3. Jak w LangChain reprezentuje się wiadomości (System/Human/AI/Tool) i po co rozróżnia się te typy?**

(Por. [[komunikacja-z-llm-w-langchain]].)

LangChain modeluje rozmowę jako **listę typowanych wiadomości**:

- **SystemMessage** — instrukcje/rola agenta (konstytucja, sekcja 1).
- **HumanMessage** — wejście użytkownika.
- **AIMessage** — odpowiedź modelu; może zawierać `tool_calls` (żądania wywołania narzędzi) zamiast/obok treści.
- **ToolMessage** — wynik wykonania narzędzia, powiązany z konkretnym `tool_call_id`, oddawany modelowi jako obserwacja.

Po co rozróżnienie: API czatowe wymagają **ról**, by model wiedział, kto mówi i jak traktować dany fragment (inną wagę ma instrukcja systemowa, inną wejście użytkownika, inną wynik narzędzia). Rozdzielenie `AIMessage.tool_calls` od `ToolMessage` to właśnie mechanika pętli tool use (akcja vs obserwacja). Typowanie pozwala też frameworkowi poprawnie serializować i odtwarzać historię.

---

**4. Jak działa tool calling w LangChain — jak definiuje się narzędzie i jak model je wywołuje?**

(Por. [[narzedzia-dla-agentow-tool-use-langgraph]].)

- **Definicja** — najczęściej dekorator `@tool` na funkcji (nazwa, docstring jako opis, type hints / schemat Pydantic jako argumenty) lub `StructuredTool`. Z tego LangChain generuje schemat narzędzia podawany modelowi.
- **Podpięcie** — `model.bind_tools([...])` dołącza definicje narzędzi do wywołań modelu (trafiają do kontekstu jako dostępne funkcje).
- **Wywołanie** — model zwraca `AIMessage` z `tool_calls` (nazwa + argumenty zgodne ze schematem). To **nie** wykonuje narzędzia — to dopiero *żądanie*.
- **Wykonanie** — aplikacja (lub gotowy `ToolNode` w LangGraph) uruchamia funkcję z argumentami, opakowuje wynik w `ToolMessage` i oddaje modelowi, który kontynuuje.

Czyli LangChain spina: schemat z funkcji → `bind_tools` → odczyt `tool_calls` → wykonanie → `ToolMessage`. Walidacja argumentów przez Pydantic jak w sekcji 3.

---

**5. Jak realizuje się structured output w LangChain (`with_structured_output`) i czym różni się od ręcznego parsera Pydantic?**

(Por. [[with_structured_output_vs_pydantic_parser]], [[langchain-structured-output-jinja2]].)

- **`with_structured_output(Schema)`** — owija model tak, że zwraca od razu **zwalidowany obiekt** zgodny ze schematem (Pydantic/TypedDict). Pod spodem używa **natywnego mechanizmu dostawcy** (function calling / JSON mode / constrained decoding), więc model jest *zmuszony* do zgodnej struktury — nie trzeba prosić o JSON w prompcie.
- **Ręczny parser Pydantic** (np. `PydanticOutputParser`) — wstrzykuje instrukcje formatu do promptu, model generuje **tekst**, a parser próbuje go sparsować *po fakcie*. Działa też z modelami bez natywnego structured output, ale jest kruchy: model może zwrócić niezgodny tekst → błąd parsowania, trzeba retry/fixing parser.

Różnica praktyczna: `with_structured_output` jest pewniejsze i prostsze, gdy dostawca to wspiera (wymuszenie na poziomie API); ręczny parser to fallback dla modeli/sytuacji bez wsparcia natywnego, kosztem niezawodności. Por. structured output jako granica systemu (sekcja 6, pyt. 6).

---

**6. Czym są middleware w LangChain i do czego służą?**

(Por. [[langchain-middlewares]].)

**Middleware** to mechanizm wpinania **logiki przed/po wywołaniu modelu (lub wokół kroków agenta)** — analogicznie do middleware w webie. Pozwala przechwytywać i modyfikować przepływ bez przepisywania rdzenia agenta.

Typowe zastosowania:

- **przed modelem** — przycinanie/streszczanie historii (zarządzanie oknem), wstrzykiwanie kontekstu, guardrails wejściowe, modyfikacja promptu/narzędzi,
- **po modelu** — guardrails wyjściowe, walidacja/filtrowanie, logowanie, redagowanie danych wrażliwych,
- **wokół** — retry, fallback, pomiar kosztu/latencji.

Wartość: **przekrojowe funkcje** (cross-cutting concerns) w jednym, reużywalnym miejscu, zamiast rozsiewać je po kodzie agenta — czytelniej i łatwiej testować. To naturalne miejsce na część guardraili z sekcji 11.

---

**7. Jak LangChain obsługuje historię czatu i zarządzanie sesją?**

(Por. [[chat-history-langchain-langgraph]].)

- **Historia jako lista wiadomości** (`ChatMessageHistory`) — przechowuje tury rozmowy, dołączane do kolejnych wywołań jako kontekst.
- **Per-sesja po kluczu** — historia partycjonowana po `session_id` (analogicznie do `thread_id`), z backendem trwałym (in-memory, Redis, baza) — izolacja sesji jak w sekcji 4, pyt. 7.
- **Zarządzanie oknem** — trimming/summarization, by historia nie przekroczyła kontekstu (sekcja 4, pyt. 3).

Kierunek frameworka: nowsze podejście przenosi zarządzanie historią i sesją do **LangGraph (stan + checkpointer + `thread_id`)**, które robi to trwale i z możliwością wznawiania — starsze konstrukcje typu `RunnableWithMessageHistory` to lżejszy wariant dla prostych łańcuchów. Skrótowo: prosty czat → chat history w LangChain; agent z trwałym, wznawialnym stanem → checkpointer w LangGraph.

---

**8. Różnica między prebudowanym agentem (`create_agent` / ReAct agent) a budową własnego grafu? Kiedy wystarcza gotowiec?**

(Por. [[create-agent-vs-react-agent]].)

- **Prebudowany agent** (`create_agent` / prebuilt ReAct w LangGraph) — gotowa pętla model↔narzędzia: podajesz model, narzędzia, (prompt, checkpointer) i dostajesz działającego agenta ReAct. Mało kodu, szybki start, sprawdzone domyślne zachowanie.
- **Własny graf (LangGraph)** — sam definiujesz węzły, krawędzie, stan i warunki — pełna kontrola nad przepływem.

**Gotowiec wystarcza**, gdy: klasyczna pętla ReAct (jeden agent + narzędzia) realizuje zadanie, nie potrzebujesz nietypowego routingu, wielu wyspecjalizowanych etapów, HITL w konkretnym miejscu, równoległych gałęzi czy własnej obsługi błędów per węzeł.

**Własny graf**, gdy: potrzebujesz rozgałęzień warunkowych, planner/executor, multi-agent (supervisor → podgrafy), interruptów w wybranych punktach, fan-out/fan-in, customowych fallbacków — czyli gdy logika sterowania wykracza poza prostą pętlę (płynne przejście do sekcji 8 i pyt. 10).

---

**9. Jak w LangChain podejść do streamingu odpowiedzi i zdarzeń pośrednich?**

- **`.stream()` / `.astream()`** — strumieniuje wynik łańcucha/agenta przyrostowo (tokeny finalnej odpowiedzi) — lepsze odczucie latencji w UI.
- **`.astream_events()`** — strumień **zdarzeń pośrednich** całego grafu/łańcucha: start/koniec kroku, wywołania narzędzi, tokeny modelu, wyniki retrievera — pozwala pokazać użytkownikowi „co agent teraz robi" (myśli, woła narzędzie), nie tylko końcowy tekst.
- Dzięki LCEL streaming działa **jednolicie** dla całego łańcucha bez dopisywania go per krok.

Po co zdarzenia pośrednie: w wielokrokowym agencie finalny token przychodzi późno — streaming kroków pośrednich utrzymuje zaangażowanie i daje wgląd/transparentność (rozwinięte w sekcji 10, pyt. 6; w LangGraph tryby `values`/`updates`/`messages`, sekcja 8 pyt. 11).

---

**10. Gdzie kończą się możliwości „prostego" LangChain, a zaczyna potrzeba LangGraph?**

„Prosty" LangChain (LCEL) świetnie obsługuje **łańcuchy o przepływie zasadniczo liniowym/acyklicznym** (DAG): prompt → model → parser, RAG jako sekwencja, równoległe gałęzie łączone na końcu. Brakuje mu naturalnego modelu **cykli, trwałego stanu i sterowania w czasie wykonania**.

**LangGraph staje się potrzebny**, gdy pojawia się:

- **pętla agentowa z dynamicznym warunkiem stopu** (model↔narzędzia, iteracje) — cykl, nie DAG,
- **stan współdzielony** ewoluujący między krokami (z reducerami),
- **persystencja/checkpointing** i wznawianie (resume, długie sesje),
- **human-in-the-loop / interrupty** w wybranych punktach,
- **rozgałęzienia warunkowe, multi-agent, fan-out/fan-in, fallbacki per węzeł**.

Skrótowo: **LCEL = kompozycja kroków (przepływ danych)**; **LangGraph = orkiestracja stanowej, cyklicznej maszyny (przepływ sterowania)**. Gdy potrzebujesz pętli, stanu i kontroli przebiegu — przechodzisz na graf (cała sekcja 8).

## 8. LangGraph (framework)

**1. Dlaczego LangGraph modeluje agenta jako graf (węzły + krawędzie + stan)? Co to daje w porównaniu z liniowym łańcuchem?**

Agent to z natury **stanowa maszyna z cyklami i rozgałęzieniami**, a nie liniowy potok. Graf oddaje to wprost:

- **Węzły** — jednostki pracy (wywołanie modelu, narzędzia, krok logiki), każdy czyta i aktualizuje wspólny stan.
- **Krawędzie** (zwykłe i warunkowe) — sterowanie: co dalej, w tym **pętle** (model↔narzędzia) i **rozgałęzienia** (routing).
- **Stan** — współdzielona struktura niosąca kontekst między krokami.

Czego nie daje liniowy łańcuch (LCEL/DAG): naturalnych **cykli** z dynamicznym warunkiem stopu, **trwałego stanu**, **przerwań/wznawiania** i sterowania zależnego od wyniku w czasie wykonania. Graf daje to wszystko plus czytelność (topologia jest jawna), checkpointing per krok, HITL w wybranych węzłach i równoległość. Skrótowo: łańcuch modeluje *przepływ danych*, graf — *przepływ sterowania* stanowego agenta (por. sekcja 7, pyt. 10).

---

**2. Czym jest State w LangGraph i jak działają reducery?**

**State** to **współdzielona, typowana struktura** (zwykle `TypedDict`/Pydantic) przekazywana przez węzły grafu — nośnik kontekstu całego przebiegu (wiadomości, plan, wyniki pośrednie, flagi). Każdy węzeł dostaje aktualny stan i zwraca **aktualizację** (zwykle częściową).

**Reducer** to funkcja określająca, **jak scalić zwróconą aktualizację z dotychczasowym stanem** dla danego pola:

- domyślnie wartość **nadpisuje** poprzednią,
- dla pola `messages` używa się reducera **`add_messages`**, który **dołącza** nowe wiadomości do listy (zamiast ją nadpisać) — i obsługuje deduplikację/aktualizację po `id`.

Dzięki reducerom węzeł nie musi znać całej historii — zwraca tylko swój wkład, a framework wie, jak go wpiąć. To także klucz do bezpiecznego **łączenia wyników równoległych węzłów** (pyt. 10): reducer definiuje regułę scalania współbieżnych aktualizacji tego samego pola.

---

**3. Czym różnią się krawędzie zwykłe od warunkowych? Jak realizują rozgałęzienia i pętle?**

- **Krawędź zwykła (`add_edge`)** — **bezwarunkowe** przejście: po węźle A zawsze idzie B. Modeluje stałą sekwencję.
- **Krawędź warunkowa (`add_conditional_edges`)** — po węźle uruchamiana jest **funkcja routingu**, która na podstawie *stanu* zwraca nazwę następnego węzła (lub `END`). Modeluje decyzję w czasie wykonania.

Jak dają rozgałęzienia i pętle:

- **Rozgałęzienie** — funkcja warunkowa kieruje do różnych węzłów zależnie od stanu (np. „jeśli model poprosił o narzędzie → węzeł narzędzi, w przeciwnym razie → END").
- **Pętla** — krawędź (zwykła lub warunkowa) **wraca do wcześniejszego węzła** (np. z węzła narzędzi z powrotem do modelu), tworząc cykl powtarzany aż warunek skieruje do `END`.

To właśnie krawędzie warunkowe odróżniają graf od liniowego łańcucha i realizują warunek stopu pętli agentowej (pyt. 4).

---

**4. Jak w LangGraph buduje się pętlę agentową (węzeł modelu ↔ węzeł narzędzi) i jak ustala warunek zakończenia?**

Kanoniczny wzorzec ReAct jako graf:

1. **Węzeł `agent` (model)** — wywołuje LLM z `bind_tools`; wynik (`AIMessage`) trafia do stanu (`messages`).
2. **Krawędź warunkowa** po węźle modelu — funkcja sprawdza ostatnią `AIMessage`:
   - **są `tool_calls`** → kieruj do węzła narzędzi,
   - **brak `tool_calls`** (sama treść) → kieruj do `END`.
3. **Węzeł `tools` (`ToolNode`)** — wykonuje żądane narzędzia, wyniki jako `ToolMessage` dopisuje do `messages`.
4. **Krawędź zwykła `tools → agent`** — wynik wraca do modelu; pętla się zamyka.

**Warunek zakończenia**: naturalnie — gdy model przestaje wołać narzędzia (brak `tool_calls`) → `END`. Twardo — **`recursion_limit`** (maks. kroków) chroni przed nieskończoną pętlą, plus własne guardy (budżet/timeout, wykrywanie powtórzeń) z sekcji 1, pyt. 6. Gotowy `create_react_agent` buduje dokładnie ten graf (sekcja 7, pyt. 8).

---

**5. Czym są checkpointery w LangGraph i jaką rolę pełnią w persystencji stanu?**

(Por. [[checkpointers-langgraph]], [[pamiec-i-persistence-checkpointers-langgraph]].)

**Checkpointer** to **warstwa persystencji stanu grafu**: komponent, który zapisuje **migawkę (checkpoint) stanu po każdym superkroku** wykonania i potrafi ją później odczytać oraz wylistować. Podpinasz go raz, przy kompilacji grafu (`graph.compile(checkpointer=...)`), i od tej pory każde wywołanie grafu z danym `thread_id` automatycznie utrwala kolejne migawki — stan przestaje żyć wyłącznie w pamięci procesu. Bez checkpointera graf jest **bezstanowy** (każde wywołanie zaczyna od zera); z checkpointerem staje się **stanową, wznawialną maszyną**.

**Czym jest „superkrok"**: jeden tik wykonania grafu — zbiór węzłów, które ruszyły równolegle w tej samej rundzie. Checkpoint powstaje **po każdym takim tiku**, więc długi przebieg to ciąg checkpointów (uporządkowana historia stanu threadu), a nie pojedynczy zapis na końcu.

Rola:

- **Persystencja i wznawianie (resume)** — po awarii/restarcie/przerwaniu przebieg kontynuuje od ostatniej migawki, nie od początku.
- **Pamięć konwersacji** — historia per `thread_id` trwa między wywołaniami (wielotura, wielosesja).
- **Human-in-the-loop** — interrupt zapisuje stan; po decyzji człowieka graf wznawia od punktu przerwania (pyt. 8–9).
- **Time-travel / debug** — pełna historia checkpointów pozwala cofnąć się i wznowić z dowolnego punktu, także po edycji stanu (pyt. 13).

### Jak fizycznie przechowywany jest stan

Checkpointer **serializuje** stan (domyślnie przez `JsonPlusSerializer`, który radzi sobie nie tylko z JSON-em, ale i z obiektami LangChain — `messages`, Pydantic, datetime itp.; obiekty nieserializowalne wprost idą jako bezpieczny fallback) i zapisuje go do wybranego backendu:

- **InMemorySaver** — słownik w pamięci procesu (ulotne),
- **SqliteSaver** — wiersze w pliku/bazie SQLite,
- **PostgresSaver** — tabele w Postgresie (`checkpointer.setup()` zakłada schemat przy pierwszym użyciu).

Zapis jest **partycjonowany** po kluczach z `config`: `thread_id` (konwersacja), `checkpoint_ns` (przestrzeń nazw — m.in. dla podgrafów) oraz `checkpoint_id` (konkretna migawka). Dzięki temu jeden backend trzyma równolegle wiele niezależnych threadów (izolacja z pyt. 6), a w obrębie threadu — całą oś czasu migawek.

### Czy istnieje schema danych — stała czy definiowalna

Trzeba rozdzielić dwie „schemy":

1. **Schemat samego checkpointu (koperty) — STAŁY**, narzucony przez LangGraph. Każda migawka to obiekt `Checkpoint` o ustalonych polach:
   - `v` — wersja formatu checkpointu,
   - `id` — identyfikator migawki (monotoniczny, sortowalny w czasie),
   - `ts` — znacznik czasu (ISO 8601),
   - `channel_values` — **właściwa zawartość Twojego stanu** (wartości „kanałów", czyli pól State),
   - `channel_versions` — wersja każdego kanału (która migawka ostatnio go zmieniła),
   - `versions_seen` — które wersje kanałów dany węzeł już „widział" (to steruje tym, co uruchomić w kolejnym superkroku, i zapewnia poprawne wznawianie).

   Obok checkpointu zapisywane są też **metadane** (`CheckpointMetadata`: m.in. `source` — skąd zapis: `input`/`loop`/`update`, `step` — numer kroku, `parents` — powiązania z rodzicami) oraz **pending writes** (zapisy oczekujące — kluczowe, by po awarii w połowie superkroku nie zgubić częściowych wyników). Tego kształtu nie zmieniasz — jest kontraktem między grafem a checkpointerem.

2. **Schemat Twojego stanu (zawartość `channel_values`) — DEFINIOWALNY przez Ciebie**. To Ty deklarujesz `State` (np. `TypedDict`/Pydantic z `messages`, `plan`, własnymi polami i reducerami). Checkpointer jest **agnostyczny** wobec tej struktury — pakuje dowolne zadeklarowane przez Ciebie pola do `channel_values`. Czyli: koperta zawsze taka sama, list w środku — wedle Twojego `State`.

Odczyt zwraca **`CheckpointTuple`**: `config` + `checkpoint` + `metadata` + `parent_config` (wskazanie poprzedniej migawki, tworzące łańcuch historii) + ewentualne `pending_writes`.

### Przykładowa treść zapisu

Minimalny przykład bezpośredniego użycia interfejsu (zwykle robi to graf automatycznie — `put(config, checkpoint, metadata, new_versions)`):

```python
from langgraph.checkpoint.memory import InMemorySaver

write_config = {"configurable": {"thread_id": "1", "checkpoint_ns": ""}}
checkpointer = InMemorySaver()

checkpoint = {
    "v": 4,
    "ts": "2024-07-31T20:14:19.804150+00:00",
    "id": "1ef4f797-8335-6428-8001-8a1503f9b875",
    "channel_values": {            # <- TU jest Twój State (wg własnej schemy)
        "my_key": "meow",
        "node": "node"
    },
    "channel_versions": {          # wersja każdego kanału
        "__start__": 2,
        "my_key": 3,
        "start:node": 3,
        "node": 3
    },
    "versions_seen": {             # co który węzeł już widział (sterowanie pętlą)
        "__input__": {},
        "__start__": {"__start__": 1},
        "node": {"start:node": 2}
    }
}

checkpointer.put(write_config, checkpoint, {}, {})   # zapis migawki
checkpointer.get({"configurable": {"thread_id": "1"}})  # odczyt najnowszej
list(checkpointer.list({"configurable": {"thread_id": "1"}}))  # cała historia
```

Dla realnego agenta `channel_values` zwykle zawiera m.in. zserializowaną listę `messages` (System/Human/AI z `tool_calls`/Tool), aktualny plan i flagi — wszystko zgodnie z zadeklarowanym `State`. Backendowo (SQLite/Postgres) ląduje to jako wiersz z kluczem `(thread_id, checkpoint_ns, checkpoint_id)` i zserializowanym blobem checkpointu + osobno metadane i pending writes.

Checkpointer to fundament wszystkich „stanowych" funkcji LangGraph (persistence z sekcji 4, pyt. 8), a `parent_config` łączący migawki w łańcuch jest tym, co umożliwia time-travel (pyt. 13).

---

**6. Jak działają thready i `thread_id`? Jak izolują stan różnych konwersacji?**

**Thread** to pojedyncza, izolowana sekwencja przebiegu (np. jedna konwersacja). Identyfikuje go **`thread_id`**, podawany w konfiguracji wywołania (`config={"configurable": {"thread_id": ...}}`).

Jak izoluje: checkpointer **partycjonuje zapisany stan po `thread_id`** — każdy thread ma własną, niezależną historię checkpointów. Wywołanie z danym `thread_id` wczytuje *tylko* stan tego threadu; inne konwersacje są niewidoczne. To realizuje izolację sesji z sekcji 4, pyt. 7:

- **per-thread** = stan/historia konkretnej rozmowy,
- **per-user** = wiedza wspólna dla użytkownika (osobny store długoterminowy, filtrowany po `user_id`).

Dzięki temu warstwa aplikacji jest **bezstanowa** i skaluje się poziomo: stan trzyma checkpointer po `thread_id`, nie proces.

---

**7. Jakie są opcje backendu persystencji (in-memory, SQLite, Postgres) i jak wybrać?**

(Por. [[persistence-sqlite-postgres-langgraph]].)

- **InMemorySaver** — stan w pamięci procesu. Zero konfiguracji, najszybszy; **znika po restarcie** i nie działa między procesami. Do **prototypów, testów, demo**.
- **SqliteSaver** — trwałość w pliku SQLite. Przeżywa restart, zero serwera; jeden plik/lokalny dysk, słaba współbieżność i brak skalowania poziomego. Do **aplikacji lokalnych, pojedynczego procesu, dev**.
- **PostgresSaver** — trwałość w Postgresie. Współbieżność, wiele instancji, skalowanie poziome, kopie zapasowe; wymaga serwera DB. **Standard produkcyjny**.

Wybór: zaczynaj od in-memory w czasie budowy; SQLite dla lokalnych/jednoprocesowych wdrożeń; **Postgres na produkcję** wielodostępową/skalowalną. Interfejs jest wspólny, więc backend podmieniasz bez zmiany logiki grafu.

---

**8. Czym jest interrupt w LangGraph i jak realizuje wstrzymanie grafu w celu uzyskania danych/decyzji od człowieka?**

(Por. [[interrupts-langgraph]], [[human-in-the-loop-interrupt-langgraph]].)

**Interrupt** to mechanizm **wstrzymania wykonania grafu w określonym punkcie** i oddania kontroli na zewnątrz, do czasu aż człowiek dostarczy decyzję/dane. Dwa warianty:

- **dynamiczny** — funkcja `interrupt()` wywołana wewnątrz węzła; pauzuje przebieg, wystawia ładunek (np. „zatwierdź tę akcję?") i czeka,
- **statyczny** — `interrupt_before` / `interrupt_after` na wskazanych węzłach przy kompilacji.

Jak działa technicznie: w momencie interruptu **stan jest zapisany w checkpointerze** (dlatego HITL wymaga checkpointera), a wywołanie zwraca kontrolę. Później wznawiasz przekazując decyzję — w nowych API przez **`Command(resume=...)`** — i graf kontynuuje **od miejsca przerwania**, z zachowanym stanem, bez powtarzania wykonanej pracy. To podstawa approval gate i HITL (pyt. 9, sekcja 9).

---

**9. Jak działa human-in-the-loop w LangGraph (zatwierdzanie akcji, edycja stanu, wznowienie po przerwaniu)?**

Na bazie interruptów + checkpointera (pyt. 8) realizuje się typowe wzorce HITL:

- **Zatwierdzenie (approve/reject)** — przed wrażliwą akcją węzeł wywołuje `interrupt` z propozycją; człowiek akceptuje lub odrzuca, graf wznawiany `Command(resume=...)` wykonuje akcję albo wybiera inną ścieżkę (approval gate, sekcja 9 i 11).
- **Edycja stanu** — w trakcie pauzy można **zmodyfikować zapisany stan** (`update_state`/`Command(update=...)`): poprawić argumenty narzędzia, skorygować plan, dopisać brakującą informację — i dopiero wznowić.
- **Wybór/uzupełnienie** — agent pyta człowieka o brakujące dane lub o wybór wariantu i wznawia z dostarczoną wartością.
- **Wznowienie** — dzięki checkpointowi przebieg kontynuuje **od punktu przerwania** ze spójnym stanem; nie zaczyna od zera i nie powtarza już wykonanych kroków.

To bezpośrednia realizacja sterowania przebiegiem z sekcji 9.

---

**10. Jak realizuje się równoległe węzły (fan-out / fan-in) i jak łączy się ich wyniki?**

(Por. [[rownolegle-wezly-fan-out-fan-in-langgraph]].)

- **Fan-out** — z jednego węzła prowadzisz **wiele krawędzi do kilku węzłów naraz** (lub dynamicznie przez **`Send`**, np. po jednym węźle na element listy). Węzły wykonują się **równolegle** w tym samym superkroku.
- **Fan-in** — krawędzie z równoległych węzłów **zbiegają się** do wspólnego węzła następnego, który rusza, gdy wszystkie gałęzie się zakończą (synchronizacja superkroku).

**Łączenie wyników**: przez **reducery na stanie** (pyt. 2). Gdy kilka równoległych węzłów zapisuje to samo pole, reducer (np. `add_messages` lub własny, np. konkatenacja list) **deterministycznie scala** współbieżne aktualizacje, zamiast pozwolić im się nadpisać. `Send` pozwala przekazać każdej gałęzi własny wycinek danych wejściowych.

Sens: skraca latencję przy **niezależnych** podzadaniach (sekcja 3, pyt. 11; sekcja 5 research równoległy). Uwaga na koszt równoległych wywołań i obsługę częściowych porażek gałęzi.

---

**11. Jakie tryby streamingu udostępnia LangGraph (`values`, `updates`, `messages`) i kiedy którego użyć?**

(Por. [[streaming-langgraph]].)

- **`values`** — po każdym kroku emituje **pełny, aktualny stan** grafu. Użyj, gdy chcesz na bieżąco widzieć cały bieżący stan (np. UI pokazujące kompletny snapshot). Więcej danych w strumieniu.
- **`updates`** — emituje **tylko różnice** zwrócone przez węzeł (co dany węzeł zmienił). Użyj do śledzenia **postępu krok po kroku** („który węzeł właśnie zadziałał i co dodał") — lekkie, idealne do logowania/tracingu progresu.
- **`messages`** — strumień **tokenów LLM** (z metadanymi wiadomości) w miarę generowania. Użyj do **streamingu odpowiedzi token-po-tokenie** w UI czatu.

Tryby można **łączyć**. Reguła: `messages` dla płynnego tekstu do użytkownika, `updates` dla „co agent teraz robi", `values` gdy potrzebny pełny stan. To realizacja streamingu zdarzeń pośrednich z sekcji 7 pyt. 9 i sekcji 10 pyt. 6.

---

**12. Jak zbudować system wieloagentowy w LangGraph — supervisor jako węzeł kierujący do podgrafów-agentów?**

(Por. [[multi-agent-supervisor-langgraph]], [[agentic-workflows-multi-agent-orchestration]].)

Wzorzec supervisor (sekcja 5, pyt. 2) mapuje się na graf tak:

- **Każdy worker** to osobny agent — własny graf — wpięty jako **węzeł/podgraf** (np. własny `create_react_agent` z wąskim zestawem narzędzi).
- **Węzeł supervisor** to węzeł modelu, który decyduje, którego workera uruchomić; jego decyzja zwykle przez **structured output / tool call** (np. „następny: researcher").
- **Krawędź warunkowa** po supervisorze routuje do wybranego workera; **krawędzie zwykłe `worker → supervisor`** zwracają kontrolę po wykonaniu. Pętla trwa, aż supervisor skieruje do `END`.
- **Współdzielony stan** (z reducerem na `messages`) niesie kontekst; do workerów przekazuj **wycinek**/brief, nie cały stan (handoff, sekcja 5 pyt. 6).
- Gotowce: `langgraph-supervisor` (oraz wzorzec **handoff przez `Command(goto=...)`** dla topologii swarm).

Całość zyskuje checkpointing, HITL i streaming „za darmo" z grafu. Alternatywnie topologia hierarchiczna (supervisor supervisorów) dla większej skali.

---

**13. Czym jest time-travel / wznawianie z checkpointu i jak wykorzystać je w debugowaniu agenta?**

**Time-travel** to możliwość **cofnięcia się do dowolnego wcześniejszego checkpointu** przebiegu i wznowienia od niego — bo checkpointer trzyma **całą historię** snapshotów stanu threadu (`get_state_history`).

Zastosowania w debugowaniu:

- **Inspekcja** — obejrzyj stan dokładnie w kroku, w którym agent „zrobił coś dziwnego" (sekcja 10, pyt. 2), zamiast zgadywać z logów.
- **Replay** — odtwórz przebieg od wybranego checkpointu, by zreprodukować błąd.
- **What-if / forking** — **zmodyfikuj stan** w punkcie cofnięcia (np. popraw argument narzędzia, plan) i puść **alternatywną trajektorię**, nie powtarzając całości — szybkie testowanie hipotez „co, gdyby tu poszło inaczej".
- **Naprawa po awarii** — wznowienie od ostatniego dobrego checkpointu.

To czyni niedeterministycznego agenta **inspekcjonowalnym i częściowo odtwarzalnym** (replay z sekcji 14, pyt. 5) — kluczowe, bo bez tego debug wielokroku jest bardzo trudny.

---

**14. Jak w LangGraph obsłużyć błędy w węźle i zaprojektować ścieżkę fallback?**

(Por. [[obsluga-bledow-system-wieloagentowy]].)

- **Retry na poziomie węzła** — `RetryPolicy` przy dodawaniu węzła ponawia kroki z błędami przejściowymi (backoff, limit prób) — głównie dla wywołań sieci/narzędzi (sekcja 3, pyt. 5).
- **Błąd jako stan + krawędź warunkowa** — łap wyjątek w węźle, zapisz sygnał błędu do stanu, a **funkcja routingu** kieruje do węzła fallback / naprawczego / `END` zamiast wywalać przebieg. To czyni błąd **częścią przepływu sterowania**.
- **`ToolNode` i błędy narzędzi** — domyślnie potrafi zwrócić błąd jako `ToolMessage` z powrotem do modelu (błąd „naprawialny przez model", sekcja 3).
- **Ścieżki fallback** — alternatywny węzeł (prostszy model, inny worker, degradacja funkcji) albo **interrupt → eskalacja do człowieka** (HITL) przy błędach krytycznych.
- **Checkpointing** — po naprawie/decyzji wznów od ostatniego dobrego stanu, nie od zera.
- **Bez cichego maskowania** — loguj i traceuj (observability), zamieniaj realne porażki w testy regresji (sekcja 12).

## 9. Human-in-the-loop i sterowanie przebiegiem

**1. Po co stosuje się human-in-the-loop (HITL) w agentach? Jakie typy interwencji wyróżniasz (zatwierdzenie, edycja, wybór, przerwanie)?**

HITL to **wplecenie człowieka w pętlę decyzyjną agenta** w wybranych punktach — po to, by przy akcjach ryzykownych, nieodwracalnych lub niepewnych decyzję podejmował (lub zatwierdzał) człowiek, zamiast w pełni autonomicznego, niedeterministycznego modelu. To bezpośrednie narzędzie zarządzania „budżetem zaufania" (sekcja 14): tam, gdzie koszt błędu jest wysoki, dokładasz punkt kontrolny.

Typy interwencji:

- **Zatwierdzenie (approve/reject)** — agent proponuje akcję, człowiek akceptuje lub odrzuca, zanim cokolwiek się wykona (approval gate, pyt. 4).
- **Edycja (edit)** — człowiek **modyfikuje** wynik/stan agenta przed kontynuacją: poprawia argumenty narzędzia, koryguje plan, prostuje fakt.
- **Wybór (select)** — agent przedstawia kilka wariantów lub pyta o brakującą informację, człowiek wybiera/uzupełnia.
- **Przerwanie (interrupt/abort)** — człowiek zatrzymuje przebieg, który zmierza w złą stronę (zapętlenie, dryf).

W LangGraph realizuje to mechanizm interruptów + checkpointer (sekcja 8, pyt. 8–9; [[interrupts-langgraph]], [[human-in-the-loop-interrupt-langgraph]]).

---

**2. Które akcje agenta powinny bezwarunkowo wymagać akceptacji człowieka, a które mogą iść automatycznie?**

Kryterium to **odwracalność i stawka błędu** (a nie „ważność"):

- **Wymagają akceptacji**: akcje **nieodwracalne lub kosztowne** — płatności i transfery, wysyłka komunikacji na zewnątrz (mail, post), usuwanie/nadpisywanie danych, operacje destrukcyjne na bazie produkcyjnej (`DELETE`/`DROP`), zmiany uprawnień, akcje przekraczające ustalone limity (kwota, wolumen), wszystko o skutkach regulacyjnych/prawnych.
- **Mogą iść automatycznie**: akcje **read-only i odwracalne** — wyszukiwanie, odczyt, RAG, generowanie szkiców, operacje w sandboxie/dry-run, zapisy do brudnopisu z łatwym rollbackiem.

Dobra heurystyka (sekcja 3, pyt. 8): „czytanie" płynie autonomicznie, „pisanie/działanie w świecie" przechodzi przez bramkę. Próg jest **konfigurowalny i progowy** — np. zwrot < X zł automatycznie, powyżej do akceptacji — i powinien zacieśniać się wraz z ryzykiem domeny, a luzować wraz z dojrzewaniem zaufania do systemu (pyt. 6).

---

**3. Jak technicznie wstrzymać agenta w połowie pracy i wznowić go po decyzji człowieka, nie tracąc stanu?**

Fundamentem jest **persystencja stanu (checkpointer)** — bez niej „pauza" oznaczałaby utratę kontekstu. Mechanika (LangGraph, sekcja 8 pyt. 8):

1. W punkcie kontrolnym węzeł wywołuje **`interrupt()`** (dynamicznie) albo graf jest skompilowany z **`interrupt_before/after`** na wskazanym węźle.
2. W tym momencie **stan zostaje zapisany w checkpointerze** pod `thread_id`, a sterowanie wraca na zewnątrz — z ładunkiem dla człowieka (np. „zatwierdź tę akcję").
3. Proces może swobodnie zakończyć życie — decyzja człowieka może przyjść za sekundę albo za godzinę; stan czeka w trwałym backendzie.
4. Wznowienie: kolejne wywołanie grafu z tym samym `thread_id` i **`Command(resume=...)`** (lub `Command(update=...)` przy edycji stanu) — graf kontynuuje **od punktu przerwania**, bez powtarzania już wykonanej pracy.

Klucz: to nie blokujący „sleep" w procesie, lecz **zatrzymanie + utrwalenie + późniejsze podjęcie** — dlatego skaluje się i przeżywa restart (sekcja 8, pyt. 6–7).

---

**4. Jak zaprojektować approval gate przed akcjami nieodwracalnymi (płatność, wysyłka, usunięcie danych)?**

Approval gate to **węzeł-bramka tuż przed wykonaniem** wrażliwej akcji:

- **Rozdziel decyzję od wykonania** — model najpierw *proponuje* akcję (np. zwraca strukturalny `tool_call` z argumentami), a osobny węzeł zatrzymuje przebieg (`interrupt`) **zanim** narzędzie się uruchomi. Model nigdy nie wykonuje wrażliwej akcji „przy okazji".
- **Pokaż człowiekowi konkret** — dokładnie jaka akcja, z jakimi argumentami, jaki przewidywany skutek (np. „przelew 4 200 zł na konto X"), a nie mglisty komunikat.
- **Trzy ścieżki po decyzji** — *approve* (wykonaj z zatwierdzonymi argumentami), *edit* (człowiek poprawia argumenty, potem wykonaj), *reject* (pomiń/wybierz alternatywę, oddaj modelowi info).
- **Idempotentność + autoryzacja** — bramka łączy się z idempotency key i walidacją uprawnień (sekcja 3, pyt. 7), by zatwierdzona akcja wykonała się dokładnie raz.
- **Audyt** — zapisz, kto, co i kiedy zatwierdził (ślad do governance, sekcja 11).
- **Progi i allowlista** — drobne/bezpieczne akcje przepuszczaj automatycznie, bramkuj tylko powyżej progu, żeby nie utopić człowieka w klikaniu (pyt. 6).

---

**5. Jak zbierać feedback od człowieka tak, by realnie poprawiał kolejne przebiegi (a nie tylko blokował)?**

Sama bramka *blokuje* — żeby feedback *poprawiał*, trzeba go **utrwalać i zawracać do systemu**:

- **Zapisuj sygnał, nie tylko decyzję** — nie tylko „approve/reject", ale *dlaczego* (poprawiony argument, powód odrzucenia, korekta planu). To dane treningowe/ewaluacyjne, nie jednorazowy klik.
- **Edycje jako etykiety** — gdy człowiek poprawia argument narzędzia czy plan, różnica (przed→po) to gotowy przykład „jak powinno być" — materiał na few-shot, fine-tuning lub regułę.
- **Pętla do ewaluacji** — odrzucenia i korekty zamieniaj w **przypadki testowe/regresyjne** (sekcja 12, pyt. 9), żeby ten sam błąd nie wrócił.
- **Pamięć długoterminowa** — powracające preferencje („zawsze pytaj przed wysyłką do klienta") utrwalaj w pamięci/profilu (sekcja 4), by agent nie wymagał tej samej interwencji za każdym razem.
- **Aktualizacja promptu/guardraili** — systematyczne wzorce odrzuceń → zmiana system promptu lub guardraila, wersjonowana (sekcja 10, pyt. 8).

Cel: każda interwencja człowieka ma **podnosić autonomię na przyszłość** (mniej takich samych pytań), a nie tylko gasić bieżący pożar.

---

**6. Jak pogodzić autonomię agenta z wymogiem kontroli — gdzie ustawić punkty kontrolne, by nie zabić użyteczności?**

To problem **kalibracji**, nie zero-jedynkowy. Zbyt wiele bramek = agent bezużyteczny (człowiek robi wszystko ręcznie); zbyt mało = ryzyko katastrofy. Zasady:

- **Punkty kontrolne na granicach nieodwracalności** — bramkuj tam, gdzie skutek jest trwały/kosztowny (pisanie do świata), przepuszczaj swobodnie odczyt i kroki odwracalne (pyt. 2).
- **Progi zamiast bramek na wszystkim** — interwencja wyzwalana **warunkiem** (kwota > X, akcja spoza allowlisty, niska pewność modelu, wykryta anomalia), a nie przy każdym kroku.
- **Eskalacja przy niepewności** — gdy agent „nie jest pewien" (niska confidence, sprzeczne dane, przekroczony budżet replanów) — pytaj; gdy pewny i w bezpiecznym zakresie — działaj.
- **Budżet zaufania rośnie z dojrzałością** (sekcja 14, pyt. 7) — start z ciasną kontrolą, a w miarę jak metryki produkcyjne (success rate, brak incydentów) potwierdzają niezawodność, **stopniowo luzuj** progi i przesuwaj akcje z „wymaga akceptacji" do „automatyczne".
- **Tania kontrola** — projektuj interwencje tak, by były szybkie dla człowieka (jasny kontekst, batch zatwierdzeń, sensowne domyślne), inaczej kontrola staje się wąskim gardłem.

Złota zasada: **autonomia tam, gdzie tanio o pomyłkę; kontrola tam, gdzie drogo** — i przesuwaj tę granicę danymi, nie przeczuciem.

## 10. Produkcja: observability, koszt, latencja, streaming

**1. Jak zapewnić observability / tracing agenta — co dokładnie logujesz w każdym kroku (prompt, decyzja, wywołanie narzędzia, koszt, latencja)?**

Agent jest **niedeterministyczny i wielokrokowy**, więc bez śladu nie da się ani debugować, ani optymalizować, ani ewaluować. Observability opiera się na **tracingu hierarchicznym**: jeden przebieg (trace) = drzewo span-ów (krok agenta → wywołanie modelu → wywołanie narzędzia). Narzędzia: LangSmith (natywnie do LangChain/LangGraph), OpenTelemetry/inne.

W każdym kroku logujesz:

- **Wejście modelu** — pełny prompt *po złożeniu* (system + historia + kontekst RAG + opisy narzędzi), bo to on realnie steruje decyzją; oraz wersja promptu/konfiguracji (pyt. 8).
- **Decyzję modelu** — surowe wyjście: treść i/lub `tool_calls` (które narzędzie, jakie argumenty), ewentualny ślad rozumowania.
- **Wywołanie narzędzia** — nazwa, argumenty, wynik (lub błąd), czas wykonania.
- **Koszt** — tokeny wejścia/wyjścia per wywołanie i zsumowane na przebieg, użyty model.
- **Latencja** — czas per krok i całego przebiegu (do znajdowania wąskich gardeł).
- **Metadane korelujące** — `thread_id`, `user_id`, `run_id`, znacznik czasu, wynik końcowy/status.

Dane wrażliwe **maskuj/redaguj w logach** (sekcja 11, pyt. 5). Dobry trace pozwala odtworzyć *dokładnie* to, co widział i zrobił model na każdym kroku.

---

**2. Jak debugować agenta, który „zrobił coś dziwnego" trzy kroki temu? Jakie artefakty są do tego potrzebne?**

Problem: skutek widać późno, a przyczyna jest kilka kroków wstecz. Potrzebujesz **pełnego, krokowego śladu + utrwalonego stanu**:

- **Trace całego przebiegu** (pyt. 1) — przejdź wstecz do kroku, w którym pojawiło się odchylenie, i zobacz **dokładny prompt i wyjście** w tamtym momencie (nie zgaduj z logów aplikacyjnych).
- **Historia checkpointów (time-travel)** — w LangGraph `get_state_history` daje **stan w każdym kroku**; możesz obejrzeć stan w feralnym punkcie, a nawet **wznowić z modyfikacją** („what-if", sekcja 8 pyt. 13).
- **Zlokalizuj warstwę** (sekcja 12, pyt. 7) — czy zawiódł retrieval (zły kontekst), wybór narzędzia, argumenty, czy generacja na poprawnym kontekście.
- **Replay** — odtwórz przebieg od checkpointu, by deterministycznie zreprodukować (na ile się da przy niedeterminizmie, sekcja 14 pyt. 5).

Artefakty niezbędne: krokowy trace (prompt+decyzja+narzędzie), snapshoty stanu per krok, wersje promptu/modelu, korelujące id. Bez nich debug wielokroku to wróżenie.

---

**3. Jak kontrolować i optymalizować koszt agenta (liczba tokenów, liczba kroków, cache promptów, dobór modelu na krok)?**

Koszt agenta ≈ Σ (tokeny × cena modelu) po wszystkich krokach — rośnie z **liczbą kroków** i **rozmiarem kontekstu** każdego. Dźwignie:

- **Mniej tokenów w kontekście** — context engineering (sekcja 6): tylko istotny kontekst, top-k + re-ranking RAG, streszczanie historii, podzbiór narzędzi (tool routing). To zwykle największa dźwignia.
- **Mniej kroków** — lepsze narzędzia (bogatszy wynik za jeden call), plan-and-execute zamiast wielu rund ReAct, równoległe tool calls, jasny warunek stopu (sekcja 2, pyt. 7).
- **Prompt caching** — cache'uj stały prefix (system prompt, opisy narzędzi, stały kontekst), który powtarza się w każdym kroku — duża oszczędność w pętlach.
- **Dobór modelu na krok / kaskadowanie** — tani/mniejszy model do prostych kroków i rutynowych decyzji, silny tylko gdzie trzeba (pyt. 5).
- **Caching wyników** — powtarzalne zapytania/retrieval.
- **Budżety i monitoring** — twardy limit tokenów na przebieg (pyt. 7) + alerty na koszt per przebieg/użytkownika (wyłapują zapętlenia, sekcja 13 pyt. 3).

---

**4. Jak ograniczać latencję wielokrokowego agenta (streaming, równoległość, mniejsze modele do prostych kroków)?**

Latencja wielokroku to **suma kroków sekwencyjnych** — każdy to round-trip do LLM. Redukcja:

- **Równoległość** — niezależne podzadania/tool calls puszczaj jednocześnie (fan-out/fan-in, sekcja 8 pyt. 10), by latencja była *maksimum*, a nie *sumą*.
- **Mniejsze/szybsze modele do prostych kroków** — routing (pyt. 5); duży model tylko do trudnego rozumowania.
- **Mniej kroków** — jak w koszcie (pyt. 3): lepsze narzędzia, plan-and-execute, batching.
- **Streaming** — nie zmniejsza latencji całkowitej, ale **drastycznie poprawia odczuwaną**: użytkownik widzi postęp i tokeny od razu (pyt. 6), zamiast czekać na finalny wynik.
- **Krótszy kontekst** — mniej tokenów wejścia = szybszy prefill (a context engineering pomaga i tu).
- **Caching** (prompt cache, wyniki) — pomija powtarzalną pracę.
- **Time-to-first-token vs total** — mierz oba; dla UX czatu liczy się TTFT, dla zadań batch — całość.

---

**5. Czym jest model routing / kaskadowanie modeli i jak zastosować je w agencie, by nie używać największego modelu do każdego kroku?**

(Por. [[wyjasnij-teraz-model-routing-kaskadowanie-modeli]].)

- **Model routing** — wybór modelu **per zadanie/krok** zależnie od jego trudności: klasyfikacja czy prosta ekstrakcja → mały, tani model; trudne rozumowanie/planowanie → duży. Decyduje router (reguła, klasyfikator trudności, typ węzła).
- **Kaskadowanie (cascade)** — próbujesz **najpierw tańszym** modelem, a **eskalujesz do droższego tylko, gdy tani zawiedzie** (niska pewność, nieudana walidacja, odrzucenie przez weryfikator). Płacisz za duży model jedynie w trudnych przypadkach.

Zastosowanie w agencie: różne węzły grafu = różne modele (planner = silny, executor/router/klasyfikator = tani); kaskada na krokach, gdzie da się tanio zweryfikować wynik. Efekt: znaczna redukcja kosztu i latencji przy zachowaniu jakości tam, gdzie naprawdę potrzebna. To wprost realizacja „nie używaj największego modelu do każdego kroku" (sekcja 5, pyt. 9).

---

**6. Po co streamować zdarzenia pośrednie (nie tylko finalny token) i jak to wpływa na UX agenta?**

W wielokrokowym agencie finalna odpowiedź przychodzi **późno** (kilka rund modelu + narzędzia). Gdyby UI milczał do końca, użytkownik widziałby długie „zawieszenie". Streaming zdarzeń pośrednich (sekcja 7 pyt. 9; tryby `values`/`updates`/`messages`, sekcja 8 pyt. 11) pokazuje **co agent robi w trakcie**:

- „Szukam w bazie wiedzy…", „Wywołuję narzędzie X…", „Analizuję wyniki…" — postęp krok po kroku (`updates`),
- streaming tokenów finalnej odpowiedzi (`messages`) — tekst pojawia się płynnie.

Wpływ na UX:

- **Niższa latencja odczuwana** — postęp utrzymuje zaangażowanie, mimo że całkowity czas się nie zmienił (pyt. 4).
- **Transparentność i zaufanie** — widać *dlaczego* to trwa i co się dzieje (mniej „czarnej skrzynki").
- **Wczesne wykrywanie błędu** — użytkownik (lub operator) widzi, że agent poszedł w złą stronę, i może przerwać, nie czekając do końca (HITL, sekcja 9).

---

**7. Jak zaprojektować limity (max kroków, timeout, budżet tokenów) i co robić po ich przekroczeniu?**

Limity to **siatka bezpieczeństwa** przeciw zapętleniu, dryfowi i przepalaniu kosztu (sekcja 1, pyt. 6). Warstwy:

- **Max kroków/iteracji** — `recursion_limit` w LangGraph; chroni przed nieskończoną pętlą.
- **Budżet tokenów** — na przebieg (i ewentualnie per użytkownik/dzień); wyłapuje rozdęty kontekst i pętle.
- **Timeout** — całego przebiegu i pojedynczych wywołań narzędzi (zewnętrzne API potrafi wisieć).
- **Wykrywanie braku postępu** — ten sam tool call/argumenty N razy, brak zmiany stanu (sekcja 1).

Co po przekroczeniu — **kontrolowane domknięcie, nie cichy zawis ani twardy crash**:

- zwróć **częściowy wynik + jasny komunikat** („nie udało się dokończyć w limicie X"),
- **fallback** (prostsza ścieżka, mniejszy zakres) lub **eskalacja do człowieka** (HITL),
- **zaloguj i otraceuj** zdarzenie jako sygnał do analizy (czemu przekroczył?) i ewentualny przypadek regresyjny,
- miękko: wstrzyknij do kontekstu „zostało N kroków", by skłonić model do domknięcia, *zanim* twardy limit utnie.

Limit to bezpiecznik — realną redukcję kroków daje lepszy design narzędzi i promptu (sekcja 2, pyt. 7).

---

**8. Jak wersjonować prompty i konfigurację agenta, żeby zmiana nie psuła cicho zachowania na produkcji?**

Prompt to **kod produkcyjny** — drobna zmiana sformułowania potrafi cicho zmienić zachowanie agenta na całej populacji ruchu. Dlatego:

- **Prompty i konfiguracja pod kontrolą wersji** — w repo/rejestrze promptów, z historią zmian i identyfikatorem wersji (nie „magiczne stringi" rozsiane po kodzie).
- **Loguj wersję przy każdym przebiegu** (pyt. 1) — żeby po incydencie wiedzieć, *który* prompt/model był aktywny.
- **Wersjonuj też model i jego parametry** — `model_id`, temperatura, wersja narzędzi/schematów (zmiana modelu przez dostawcę to też „zmiana", pyt. 9).
- **Ewaluacja przed wdrożeniem** — każdą zmianę promptu przepuść przez **zestaw ewaluacyjny/regresyjny** (sekcja 12), by zobaczyć wpływ na metryki, zanim trafi na produkcję — to chroni przed „cichym" pogorszeniem.
- **Stopniowy rollout + A/B** — canary/procent ruchu na nową wersję, porównanie metryk, łatwy rollback.
- **Rozdziel prompt od kodu** — by zmiana treści nie wymagała redeployu i była audytowalna osobno.

Zasada: **żadna zmiana zachowania bez wersji i bez pomiaru** — inaczej regresje są niewidzialne aż do incydentu.

---

**9. Jak wykrywać dryf zachowania agenta w czasie (zmiana modelu po stronie dostawcy, dryf rozkładu zapytań)?**

(Por. [[Dryf_w_LLM]].)

Dwa źródła dryfu:

- **Dryf modelu** — dostawca aktualizuje model „pod tym samym aliasem", więc to samo wejście zaczyna dawać inne wyjście (zachowanie zmienia się bez Twojej zmiany kodu).
- **Dryf rozkładu zapytań** — zmienia się to, *o co* pytają użytkownicy (nowe tematy, inny język, inne przypadki brzegowe), więc agent trafia poza to, na czym był strojony/testowany.

Wykrywanie:

- **Stały zestaw „kanarkowy"** — pula reprezentatywnych zapytań puszczana regularnie; nagła zmiana metryk (success rate, liczba kroków, koszt, format wyjścia) sygnalizuje dryf modelu.
- **Monitoring metryk produkcyjnych w czasie** — success rate, latencja, koszt/przebieg, odsetek interwencji człowieka, odsetek błędów narzędzi; trendy i skokowe zmiany.
- **Online eval / próbkowanie trajektorii** — LLM-as-a-Judge lub ludzka ocena na próbce produkcyjnego ruchu (sekcja 12, pyt. 8).
- **Monitoring wejścia** — rozkład tematów/długości/języka zapytań; pojawienie się nowych klastrów = dryf rozkładu.
- **Przypinanie wersji modelu** — gdzie możliwe, używaj **konkretnej, datowanej wersji** zamiast „latest", a aktualizację traktuj jak zmianę wymagającą re-ewaluacji (pyt. 8).
- **Pętla zwrotna** — wykryte regresje → nowe przypadki testowe (sekcja 12, pyt. 9).

## 11. Bezpieczeństwo i guardrails

**1. Czym jest prompt injection i dlaczego agenci z narzędziami są na nie szczególnie wrażliwi?**

**Prompt injection** to atak, w którym **wrogie instrukcje przemycone w danych wejściowych** nadpisują/zmieniają intencję system promptu — model traktuje je jako polecenia („zignoruj poprzednie instrukcje i zrób X"). Źródłem problemu jest brak twardej granicy między *instrukcją* a *danymi*: dla LLM jedno i drugie to ten sam strumień tokenów.

Dlaczego agenci z narzędziami są szczególnie wrażliwi:

- **Injection zamienia się w akcję** — w zwykłym chatbocie najgorszy skutek to „brzydka odpowiedź"; agent z narzędziami może na skutek wstrzykniętej instrukcji **wykonać realną akcję** (wysłać dane, usunąć rekord, dokonać płatności).
- **Powierzchnia ataku rośnie z narzędziami** — każde narzędzie zwracające treść z zewnątrz (web, dokumenty, maile, wyniki API) to kanał wstrzyknięcia (indirect injection, pyt. 2).
- **Łańcuch zaufania** — wynik jednego narzędzia trafia do kontekstu i wpływa na kolejne decyzje; zatruty wynik propaguje się.
- **Uprawnienia** — agent często działa z realnymi uprawnieniami (dostęp do bazy, API), więc przejęcie sterowania jest groźne.

Stąd: injection traktuje się jak **niezaufane dane** i broni warstwowo (least privilege, guardrails, HITL na akcjach) — nie da się go „wyłączyć" samym promptem.

---

**2. Na czym polega indirect prompt injection (złośliwe instrukcje ukryte w pobranym dokumencie/stronie/treści narzędzia)?**

To wariant, w którym atakujący **nie pisze bezpośrednio do agenta**, lecz **umieszcza wrogie instrukcje w treści, którą agent dopiero pobierze**: stronie WWW, dokumencie w bazie wiedzy (RAG), mailu, komentarzu, wyniku API, repozytorium. Gdy agent wciągnie tę treść do kontekstu jako „dane", model może potraktować ukryte polecenie jak instrukcję — np. „prześlij zawartość bazy na adres X" ukryte białym tekstem na stronie.

Dlaczego groźne i trudne:

- **Atak przez zaufany kanał** — treść wygląda jak zwykłe dane do przetworzenia; użytkownik niczego nie wpisał.
- **Skala** — wystarczy zatruć źródło, z którego korzysta wielu agentów (jedna strona, jeden dokument).
- **Łączy się z eksfiltracją** (pyt. 9) — typowy ładunek to „wyślij sekrety/dane na zewnętrzny endpoint".

Obrona: traktuj **całą pobraną treść jako niezaufaną**, oddzielaj ją wyraźnie od instrukcji (delimitery, „to są dane, nie polecenia"), guardrails na treści wejściowej, least privilege narzędzi, **HITL na akcjach wychodzących**, oraz ograniczenie, *gdzie* agent może wysyłać dane (allowlista domen/endpointów). Sam prompt nie wystarczy — to obrona warstwowa.

---

**3. Czym są guardrails wejściowe i wyjściowe i gdzie w architekturze agenta je umieszczasz?**

(Por. [[llm-guardrails]].)

**Guardrails** to **deterministyczne (lub osobny-model) kontrole wokół wywołań LLM**, niezależne od „dobrej woli" modelu — bo na samym promptcie nie można polegać.

- **Wejściowe (input guardrails)** — na granicy *przed* modelem: filtrowanie/oznaczanie niezaufanej treści, detekcja prompt injection, walidacja i sanizacja wejścia, blokada zakazanych tematów, oddzielenie danych od instrukcji.
- **Wyjściowe (output guardrails)** — *po* modelu, *przed* skutkiem: walidacja structured output (schemat, sekcja 6), filtr danych wrażliwych/PII w odpowiedzi, blokada niedozwolonych akcji, sprawdzenie, czy `tool_call` mieści się w allowliście i limitach, moderacja treści.

Gdzie w architekturze:

- naturalnie jako **middleware** (sekcja 7, pyt. 6) — przed/po modelu, reużywalnie,
- jako **węzły grafu** w LangGraph (węzeł-walidator, węzeł-bramka) z krawędzią warunkową do odrzucenia/poprawy,
- szczególnie **wokół narzędzi mutujących** (walidacja argumentów + autoryzacja przed wykonaniem, sekcja 3 pyt. 4/7).

Zasada: guardrails są **poza modelem** i deterministyczne tam, gdzie się da — model może je próbować obejść, kod nie.

---

**4. Jak zrealizować zasadę least privilege dla narzędzi agenta (zakres uprawnień, sandbox, allowlista akcji)?**

**Least privilege** = agent (i każde narzędzie) ma **dokładnie tyle uprawnień, ile potrzeba do zadania — i ani trochę więcej**. To najważniejsza linia obrony, bo ogranicza *skutek* udanego ataku/pomyłki, niezależnie od tego, czy model dał się oszukać.

- **Wąski zakres uprawnień** — narzędzia z minimalnym dostępem: read-only tam, gdzie wystarczy odczyt; konto bazodanowe tylko do potrzebnych tabel/operacji (osobne role dla read i write).
- **Allowlista akcji** — agent może wykonać tylko akcje z jawnej, zamkniętej listy; wszystko spoza = odrzucone (lepsze niż blacklista, której nie da się domknąć).
- **Sandbox** — wykonywanie kodu/narzędzi ryzykownych w izolowanym środowisku (kontener, ograniczone sieć/FS), z limitami zasobów.
- **Parametryzacja zamiast swobody** — narzędzia o **ograniczonych, walidowanych parametrach** (enumy, zakresy), nie „wykonaj dowolny SQL/shell". Zamiast `run_query(sql)` → `get_orders(user_id, status)`.
- **Limity twarde** — maks. kwota, maks. liczba rekordów, rate limit — jako bezpieczniki na skutek.
- **Rozdział uprawnień per rola** (multi-agent) — worker ma tylko narzędzia swojej roli (sekcja 5).

Cel: zaprojektować tak, by **łatwą do popełnienia pomyłką (lub udanym injection) nie dało się wyrządzić dużej szkody** (sekcja 3, pyt. 2).

---

**5. Jak chronić dane wrażliwe i sekrety w przepływie agenta (maskowanie w logach, brak sekretów w promptcie)?**

Agent przepuszcza przez siebie prompty, konteksty, logi i wywołania narzędzi — sekrety i PII mogą wyciec na wielu etapach:

- **Sekrety poza promptem i poza modelem** — klucze API/hasła trzymaj w **secret managerze / zmiennych środowiskowych**; narzędzie pobiera je samo przy wykonaniu, **nie wstrzykuj ich do kontekstu** (inaczej trafiają do logów, do dostawcy modelu, i mogą wyciec przez injection). Model powinien wywoływać narzędzie, nie *znać* poświadczeń.
- **Maskowanie/redakcja w logach i trace** — PII i sekrety filtruj **zanim** trafią do observability (sekcja 10, pyt. 1); loguj zredagowane wersje.
- **Minimalizacja danych w kontekście** — wstrzykuj tylko niezbędne pola (nie cały rekord klienta); pseudonimizacja/tokenizacja, gdzie się da.
- **Guardrails wyjściowe na PII** (pyt. 3) — wykrywaj i blokuj wyciek danych wrażliwych w odpowiedzi/akcji.
- **Izolacja per użytkownik** — twarde filtrowanie pamięci po `user_id` (sekcja 4, pyt. 7), by nie wyciekł kontekst innej osoby.
- **Świadomość granicy dostawcy** — wszystko w kontekście idzie do zewnętrznego API modelu; traktuj to jak wysyłkę danych na zewnątrz (retencja, zgodność, RODO).

---

**6. Jak zapobiec wykonaniu przez agenta destrukcyjnej akcji (np. `DROP TABLE`, masowe usunięcie)? Rola HITL i piaskownicy.**

Obrona **warstwowa** — nie polegaj na jednym mechanizmie:

- **Least privilege (pierwsza linia)** — agent po prostu **nie ma uprawnień** do destrukcji: konto bez `DROP`/`DELETE` na masową skalę, brak takiego narzędzia w zestawie (pyt. 4). Najlepsza ochrona: niemożliwe ≫ zabronione.
- **Parametryzacja zamiast surowego SQL/shell** — narzędzia o wąskim kontrakcie zamiast „wykonaj dowolne zapytanie"; jeśli surowy SQL konieczny — parser/allowlista operacji, zakaz DDL i bezwarunkowych `DELETE/UPDATE`, wymuszony `WHERE`/limit.
- **HITL / approval gate (druga linia)** — akcje destrukcyjne/nieodwracalne **bezwarunkowo przez bramkę** (sekcja 9, pyt. 4): człowiek widzi dokładnie, co i na ilu rekordach, zanim się wykona.
- **Sandbox / dry-run** — najpierw wykonanie próbne (ile rekordów dotknie?), transakcja z możliwością rollbacku, środowisko izolowane do operacji ryzykownych.
- **Limity i bezpieczniki** — maks. liczba rekordów na operację, blokada operacji bez warunku, soft-delete zamiast hard-delete.
- **Audyt** — log każdej akcji mutującej (kto/co/kiedy/zatwierdził).

HITL i piaskownica to **ostatnie szczeble** — ważne, ale najpierw zadbaj, żeby agent w ogóle *nie mógł* zrobić nieodwracalnej szkody.

---

**7. Jak podejść do kontroli dostępu i governance, gdy agent działa w imieniu różnych użytkowników o różnych uprawnieniach?**

(Por. [[bezpieczenstwo-danych-kontrola-dostepu-governance-ai]].)

Kluczowa zasada: **agent działa z uprawnieniami użytkownika, w imieniu którego pracuje — nie własnymi, „nadludzkimi"**. Inaczej staje się obejściem kontroli dostępu (confused deputy).

- **Propagacja tożsamości i uprawnień** — przekazuj kontekst autoryzacyjny użytkownika (token/rola) aż do warstwy narzędzi; narzędzie **egzekwuje uprawnienia tego użytkownika** przy każdym wywołaniu, a nie ufa, że „agent wie najlepiej".
- **Autoryzacja po stronie zasobu, nie modelu** — sprawdzenie „czy wolno" robisz w kodzie narzędzia/bazy (np. RLS, filtr `WHERE user_id`), nie w prompcie. Model może dać się oszukać; warstwa danych nie.
- **Izolacja danych per użytkownik/tenant** — twarde filtrowanie pamięci, kontekstu i wyników po `user_id`/`tenant_id` (sekcja 4, pyt. 7); brak „przecieku" między użytkownikami.
- **Najmniejszy wspólny mianownik** — agent nie może *eskalować* uprawnień; jeśli user nie ma dostępu do zasobu, agent też nie.
- **Governance** — audyt (kto, w czyim imieniu, co zrobił), polityki retencji/zgodności (RODO), jasne reguły, jakie dane wolno przetwarzać i wysyłać do modelu (pyt. 5), oraz przegląd uprawnień agenta.

---

**8. Jak testować odporność agenta na ataki (red-teaming, jailbreak, próby przejęcia narzędzi)?**

Bezpieczeństwa nie da się „dodać na końcu" — testuje się je **adwersarialnie**:

- **Red-teaming** — celowe, systematyczne próby złamania agenta: zestaw scenariuszy ataku (prompt injection bezpośredni i indirect, jailbreaki, próby wymuszenia destrukcyjnej akcji, eksfiltracji, eskalacji uprawnień). Prowadzony ręcznie i **automatycznie** (generatory ataków, w tym LLM atakujący LLM).
- **Indirect injection w realnych kanałach** — podstaw zatrute dokumenty/strony/maile do źródeł RAG i narzędzi i sprawdź, czy agent wykona ukryte polecenie (pyt. 2).
- **Próby przejęcia narzędzi** — czy da się skłonić agenta do wywołania narzędzia poza intencją, z wrogimi argumentami, do destrukcji lub wysyłki danych na zewnątrz.
- **Testy uprawnień / izolacji** — czy agent użytkownika A potrafi dosięgnąć danych B (cross-tenant), czy da się eskalować uprawnienia (pyt. 7).
- **Suite regresyjny bezpieczeństwa w CI** — udane ataki zamieniaj w **stałe testy regresji** (sekcja 12, pyt. 9), uruchamiane przy każdej zmianie promptu/modelu (sekcja 10, pyt. 8), bo zmiana modelu może otworzyć starą dziurę.
- **Metryka** — odsetek odpartych ataków, a porażki traktuj jak krytyczne błędy (protokół: zatrzymaj, napraw, zrotuj ewentualnie wyciekłe sekrety).

---

**9. Jak ograniczać eksfiltrację danych przez narzędzia agenta (np. wysłanie poufnych danych na zewnętrzny endpoint)?**

Eksfiltracja to typowy *cel* prompt injection (pyt. 1–2): skłonić agenta, by wysłał wrażliwe dane na kontrolowany przez atakującego endpoint. Obrona skupia się na **kanałach wyjścia**:

- **Allowlista miejsc docelowych** — narzędzia sieciowe (HTTP, mail) mogą komunikować się tylko z **jawnie dozwolonymi domenami/endpointami**; arbitralny URL = blokada. To ucina „wyślij na adres X" z injection.
- **Brak narzędzia „wyślij gdziekolwiek"** — żadnego generycznego `http_request(url, body)`; zamiast tego wąskie, parametryzowane narzędzia do konkretnych, zaufanych integracji (least privilege, pyt. 4).
- **Guardrails wyjściowe + DLP** — skanuj treść wychodzącą pod kątem PII/sekretów/poufnych wzorców i blokuj zanim wyjdzie (pyt. 3, 5).
- **HITL na akcjach wychodzących** — wysyłka danych na zewnątrz przez approval gate, zwłaszcza poza zaufany krąg (sekcja 9).
- **Minimalizacja danych w kontekście** — czego agent nie ma w kontekście, tego nie wyśle; nie wstrzykuj sekretów (pyt. 5).
- **Izolacja sieci / egress filtering** — środowisko wykonawcze agenta z ograniczonym ruchem wychodzącym (sandbox), tak by nawet przejęte narzędzie nie miało dokąd wysłać.
- **Audyt i alerty** — monitoruj nietypowe wolumeny/adresy wyjścia (sygnał trwającej eksfiltracji).

## 12. Ewaluacja i testowanie agentów

**1. Dlaczego ewaluacja agentów jest trudniejsza niż ewaluacja pojedynczego promptu?**

Pojedynczy prompt to `wejście → wyjście`, które można porównać z odpowiedzią wzorcową. Agent łamie wszystkie założenia takiej ewaluacji:

- **Niedeterminizm** — ten sam input daje różne trajektorie i różne wyjścia. Pojedynczy przebieg niewiele mówi; trzeba mierzyć rozkład (wiele powtórzeń), nie pojedynczy wynik.
- **Wieloetapowość** — porażka może tkwić w dowolnym z wielu kroków (planowanie, retrieval, wybór narzędzia, argumenty, generacja). Sukces końcowy nie znaczy, że droga była poprawna, a poprawna droga nie gwarantuje sukcesu (kaskada błędów).
- **Problem wyroczni (oracle problem)** — często nie istnieje jedna „poprawna" odpowiedź ani jedna dozwolona ścieżka; wiele dróg prowadzi do celu, a ocena otwartej odpowiedzi jest sama w sobie trudna.
- **Koszt i flakiness** — każdy przebieg to wiele wywołań LLM i realnych narzędzi (zewnętrzne API bywają niestabilne), więc duży zestaw ewaluacyjny jest drogi i kruchy.

---

**2. Jak ocenić trajektorię agenta, a nie tylko końcową odpowiedź?**

**Trajektoria** = sekwencja kroków: jakie narzędzia, w jakiej kolejności, z jakimi argumentami, ile ich było. Sposoby oceny:

- **Dopasowanie do referencyjnej trajektorii** — exact match (kruche), albo łagodniej: czy wystąpił wymagany podzbiór narzędzi (in-order / any-order), bez zbędnych kroków.
- **LLM-as-a-Judge nad ścieżką** — ocena, czy kolejność i decyzje były rozsądne.
- **Metryki ilościowe** — liczba kroków, koszt, latencja, liczba ponowień.

**Kiedy liczy się tylko wynik**: zadania z jednoznacznym, weryfikowalnym celem (kod przechodzi testy, poprawna liczba, poprawny rekord) i gdzie droga jest obojętna.

**Kiedy liczy się droga**: gdy są **skutki uboczne** (agent po drodze nie powinien skasować danych), gdy ważny jest koszt/latencja/bezpieczeństwo, gdy wynik trudno ocenić automatycznie, ale ścieżkę da się zmierzyć, oraz dla audytowalności.

---

**3. Jak zbudować zestaw ewaluacyjny dla agenta?**

- **Reprezentatywne zadania** — typowe + brzegowe + adversarialne + przypadki „nie rób nic / odmów / dopytaj".
- **Dla każdego przypadku**: input, oczekiwany wynik (lub rubryka/kryteria, gdy brak jednej odpowiedzi), wymagane/dozwolone narzędzia lub trajektorie, jasne kryterium sukcesu.
- **Źródła**: realne logi produkcyjne (golden set), dane syntetyczne, przypadki wyciągnięte z bugów.
- **Warstwowanie**: unit (pojedyncza decyzja / wywołanie narzędzia), integracja (podgraf), e2e (cały agent).
- **Mockowanie narzędzi** dla determinizmu i izolacji od side-effectów.
- **Wersjonuj dataset jak kod** — to żywy artefakt rosnący wraz z produktem.

---

**4. Co mierzysz i jak to ważyć?**

- **Task success rate** — nadrzędna metryka jakości (czy cel osiągnięty).
- **Poprawność użycia narzędzi** — właściwe narzędzie + poprawne argumenty.
- **Efektywność** — liczba kroków, tokeny/koszt, latencja.
- **Jakość wyjścia** — rubryki / LLM-judge dla odpowiedzi otwartych.
- **Bezpieczeństwo** — czy nie złamał guardraila, czy nie wykonał akcji poza uprawnieniami.

Ważenie zależy od produktu: zwykle **success rate jako bramka** (próg minimalny), a koszt / liczba kroków / latencja jako kryteria wtórne (optymalizacja Pareto). W jednym kontekście priorytetem jest poprawność za każdą cenę, w innym — niska latencja i koszt. Klucz: ustalić metryki *przed* optymalizacją, by nie „dostrajać pod wykres".

---

**5. Jak działa LLM-as-a-Judge i jakie ma pułapki?**

LLM ocenia wyjście lub trajektorię według rubryki — w trybie **scoring** (ocena bezwzględna) lub **pairwise** (A vs B). Tani, skalowalny zamiennik oceny ludzkiej dla odpowiedzi otwartych, których nie da się porównać exact-matchem.

Pułapki:
- **Bias na długość** — preferuje dłuższe/rozwlekłe odpowiedzi.
- **Self-enhancement** — faworyzuje styl/wyniki własnego modelu.
- **Position bias** (w pairwise) — preferuje pierwszą/drugą pozycję.
- **Brak kalibracji i niespójność**, podatność na **prompt injection** w ocenianym tekście.

Mitygacje: precyzyjna rubryka z przykładami, **pairwise zamiast bezwzględnego**, randomizacja kolejności, CoT przy ocenie, mocniejszy model jako sędzia, kalibracja względem ocen ludzkich, traktowanie wyników jako **trendów**, nie absolutów.

---

**6. Jak robić testy regresji w CI mimo niedeterminizmu?**

- **`temperature=0` / seed** tam, gdzie to możliwe — redukuje (nie usuwa) zmienność.
- **Asercje na właściwościach, nie na exact string** — czy wywołał narzędzie X, czy wynik zawiera wymagany fakt, czy przeszedł schemat (Pydantic).
- **Progi statystyczne** — N powtórzeń, wymagaj np. ≥9/10 sukcesów; śledź **metryki agregowane** między buildami zamiast binarnego pass/fail z jednego runu.
- **Mockowanie LLM/narzędzi** (record-replay) dla szybkich, deterministycznych testów na każdym PR.
- **Oddziel poziomy**: szybkie deterministyczne testy przy każdym PR vs pełny, kosztowny eval suite (nocny / przed releasem) z alertem na spadek metryki względem baseline.

---

**7. Jak izolować, która warstwa zawiodła?**

- **Tracing per krok** (np. LangSmith) — wejście/wyjście każdego węzła w trajektorii.
- **Dekompozycja ewaluacji** — osobno mierz retrieval (precision/recall kontekstu), wybór narzędzia, planowanie, generację.
- **Ablacje** — podstaw *idealny* kontekst: jeśli wyjście robi się dobre, winny był retrieval; podstaw idealny plan, by odizolować executor itd.
- **Testy komponentowe** obok end-to-end, plus logowanie argumentów i obserwacji do precyzyjnego wskazania miejsca załamania.

---

**8. Jak monitorować jakość agenta na produkcji?**

- **Online eval** — próbkowanie trajektorii z ruchu i ocena (LLM-judge / ludzie) na próbce.
- **Sygnały użytkownika** — kciuk góra/dół, retry, porzucenie, eskalacja, ponowne otwarcie ticketu.
- **Metryki operacyjne** — latencja, koszt/tokeny na sesję, liczba kroków, rate błędów narzędzi, trafienia guardraili, częstość osiągania limitów kroków.
- **Alerty na dryf/anomalie**, dashboardy, pełne logi trajektorii do analizy post-hoc, guardraile pełniące rolę monitorów (ile razy zablokowały).

---

**9. Jak zamienić realne porażki produkcyjne w nowe przypadki testowe?**

Domknięta pętla **prod → dataset → eval → fix**:

1. Z tracingu wyodrębnij input + kontekst incydentu, **zanonimizuj** dane.
2. Dodaj jako nowy przypadek do zestawu ewaluacyjnego z opisanym oczekiwanym (poprawnym) zachowaniem — to test **regresji**.
3. Zreprodukuj → napraw → upewnij się, że nowy test by błąd złapał → wpnij do CI.
4. **Klasteryzuj** podobne porażki, by łapać całe *klasy* błędów, nie pojedyncze przypadki.

Z czasem golden set rośnie z realnych braków i staje się najcenniejszym aktywem ewaluacyjnym.

## 13. Pytania scenariuszowe / system design

**1. Zaprojektuj agenta do obsługi klienta (RAG + ticketing + eskalacja).**

- **Komponenty**: LLM, system prompt (rola, ton, polityki, kiedy eskalować), **RAG** nad wiedzą firmową (baza wektorowa + retrieval z cytowaniami), pamięć i observability.
- **Narzędzia**: `search_knowledge` (read-only RAG), `get_customer` / `get_order` (read), `create_ticket` / `update_ticket` (mutujące), `escalate_to_human`.
- **Guardrails**: walidacja argumentów (Pydantic) + autoryzacja (ticket tylko danego klienta — least privilege), filtr PII, ograniczenie zakresu (out-of-scope → uprzejma odmowa), **grounding z cytatami** by ograniczyć halucynacje, zakaz zmyślania polityk firmowych.
- **HITL**: approval gate przed akcjami nieodwracalnymi/wrażliwymi (zwroty, zmiana zamówienia); **eskalacja** przy niskiej pewności, frustracji użytkownika, braku odpowiedzi w bazie, tematach drażliwych.
- **Pamięć/stan**: per-thread historia rozmowy, per-user profil; checkpointing dla wznawiania.
- **Produkcja**: limity kroków, fallback „przekazuję do konsultanta", tracing i metryki (rozwiązywalność, eskalacje).

---

**2. Zaprojektuj system wieloagentowy do researchu (planner + równolegli searcherzy + synthesizer).**

- **Topologia**: planner/supervisor rozkłada pytanie na podtematy → **fan-out** do N worker-researcherów działających **równolegle** (każdy ze swoim narzędziem wyszukiwania) → **fan-in** → synthesizer scala wyniki.
- **Komunikacja**: przez wspólny stan / supervisora. Każdy worker dostaje **wąski, izolowany kontekst** (tylko swój podtemat) i zwraca **ustrukturyzowane findings + źródła** — nie znają się nawzajem.
- **Łączenie**: synthesizer dedupliKuje, rozwiązuje sprzeczności (ważenie wiarygodności źródeł, najnowsze wygrywa) i buduje spójną odpowiedź z bibliografią/cytatami.
- **LangGraph**: fan-out/fan-in przez Send API, reducer agregujący wyniki workerów (por. [[rownolegle-wezly-fan-out-fan-in-langgraph]], [[multi-agent-supervisor-langgraph]]).
- **Trade-offy**: równoległość skraca czas, ale ↑ koszt; limituj liczbę workerów i głębokość; obsłuż **częściowe porażki** (worker padł → syntezuj z resztą); replanning, gdy wyniki słabe.

---

**3. Agent zapętla się i przepala tokeny na produkcji — diagnoza i zabezpieczenia.**

**Diagnoza** (z tracingu): szukaj powtarzających się identycznych tool calls, oscylacji A→B→A→B, braku zmiany stanu / postępu (te same obserwacje), narastania kontekstu. Sprawdź typowe przyczyny: narzędzie wciąż zwraca błąd, a model uparcie ponawia; wadliwy warunek stopu; mglisty cel; zła obsługa pustego wyniku.

**Zabezpieczenia**:
- **Twarde limity**: max kroków (recursion limit), budżet tokenów, timeout — z **kontrolowanym fallbackiem**, nie cichym zawisem.
- **Wykrywanie powtórzeń** — ten sam call N razy → przerwij / zmień strategię.
- **Lepszy warunek stopu** (conditional edge → END), licznik prób per narzędzie + backoff.
- Wstrzyknięcie „zostało N kroków" by skłonić do domknięcia, eskalacja HITL, **alerty kosztowe** na produkcji.
- Długoterminowo: lepsze opisy narzędzi, jaśniejszy cel, poprawna obsługa pustych wyników.

---

**4. Zaprojektuj „coding assistant" (czyta repo, uruchamia testy, proponuje poprawki) — gdzie approval gate i sandbox?**

- **Narzędzia**: `read_file` / `search_code` (read-only), `run_tests` (w sandboxie), `apply_patch` (mutujące).
- **Sandbox**: uruchamianie kodu i testów w **izolowanym, efemerycznym środowisku** (kontener) bez dostępu do sekretów, sieci i produkcji; twarde limity czasu i zasobów. To pozwala dać autonomię na uruchamianie testów (skutki ograniczone do piaskownicy).
- **Approval gate**: przed **zapisem do repo / commitem / pushem** — człowiek zatwierdza diff. Czytanie i odpalanie testów idzie autonomicznie (read-only / sandbox), pisanie do repo za bramką.
- **Pętla**: czytaj → hipoteza → patch w sandboxie → testy (twardy, **zewnętrzny sygnał** do self-critique) → iteruj do zielonych → przedstaw diff do akceptacji.
- **Guardrails**: limit iteracji, zakaz edycji plików wrażliwych (CI, sekrety) bez zgody, weryfikacja, że testy **realnie** przeszły (nie „udawane" zielone).

---

**5. Agent na produkcyjnej bazie — uprawnienia, walidacja zapytań, punkty kontrolne.**

- **Uprawnienia**: dedykowane konto z **least privilege**; domyślnie **read-only replica**; zapisy wyłącznie przez wąskie, sparametryzowane operacje / procedury składowane, nigdy surowy SQL z modelu. Brak DROP/DELETE bez bramki. Row-level security / filtr po tenant/user.
- **Walidacja zapytań**: allowlista operacji i tabel; **tylko zapytania parametryzowane** (anty-SQL-injection); parsowanie/statyczna analiza generowanego SQL; limit zwracanych wierszy; read-only transaction dla odczytów; `EXPLAIN` / dry-run; timeouty zapytań.
- **Punkty kontrolne**: HITL/approval przed mutacjami (zwłaszcza masowymi i DDL); transakcje z **rollbackiem**; **idempotency keys**; audyt i logowanie każdej operacji; twarde limity (max zmienionych wierszy). Wzorzec docelowy: agent **proponuje** zmianę, a wykonuje ją człowiek lub deterministyczny kod.

---

**6. Zaprojektuj asystenta zadań pamiętającego preferencje między sesjami.**

- **Pamięć długoterminowa**: store (wektorowy/dokumentowy) z faktami i preferencjami, embeddowane i **partycjonowane per `user_id`**, selektywnie pobierane do kontekstu. Rozdziel pamięć **semantyczną** (preferencje/fakty), **epizodyczną** (historia interakcji) i **proceduralną** (utrwalone instrukcje).
- **Prywatność**: twardy filtr `where user_id = ...` przy każdym odczycie (izolacja), szyfrowanie, operacja „zapomnij to" (RODO), minimalizacja zapisywanych danych, zgoda użytkownika.
- **Aktualizacja nieaktualnych faktów**: **upsert po kluczu encji** (nadpisuj, nie dokładaj sprzecznego obok), metadane timestamp/źródło (najnowszy/najbardziej wiarygodny wygrywa), TTL/decay, okresowa reconciliacja sprzeczności, **walidacja przy odczycie** (nie wstrzykuj dwóch sprzecznych wersji do kontekstu).
- Rozdział per-thread vs per-user; checkpointing dla wznawiania. Por. [[memory-management-i-session-handling]], [[pamięć-długoterminowa-ai]].

---

**7. Migracja sztywnego workflow na agenta (lub odwrotnie) — ocena i stopniowe wdrożenie.**

**Ocena zasadności**: czy ścieżka jest znana z góry i stabilna → zostań przy workflow. Czy liczba/kolejność kroków zależy od danych, a przestrzeń jest otwarta → agent. Zważ krytyczność kosztu/latencji/audytu przeciwko wartości elastyczności.

- Sygnały „workflow za sztywny": eksplozja gałęzi if/else, ciągłe dokładanie wyjątków, nieobsłużone warianty wejść.
- Sygnały „agent to przesada": proces deterministyczny, wymóg pełnej powtarzalności → migracja w drugą stronę (zamień rozumowanie na kod).

**Stopniowo**: zacznij od **hybrydy** — szkielet workflow z agentowym węzłem tylko tam, gdzie jest zmienność. Mierz na golden secie (success / koszt / latencja) względem baseline. Użyj **shadow mode** (agent działa obok, bez skutków), potem **canary** / feature flag. Rozszerzaj autonomię tam, gdzie się sprawdza; zostaw deterministyczny kod tam, gdzie wystarcza.

---

**8. Agent odporny na awarię zewnętrznego narzędzia/API w połowie zadania.**

- **Retry z exponential backoff + jitter** i twardym limitem prób — dla błędów przejściowych (timeout, 5xx, rate limit).
- **Fallback** — alternatywne narzędzie/źródło, cache, tryb degradacji albo graceful „nie udało się, oto co mam".
- **Wznowienie z checkpointu** — stan utrwalany po każdym kroku, więc po awarii/restarcie agent kontynuuje od ostatniego checkpointu, nie od zera (por. [[checkpointers-langgraph]]).
- **Idempotency keys** — krytyczne, by retry/resume nie powtórzył skutków ubocznych operacji mutujących.
- **Circuit breaker** dla wciąż padającego API, timeouty, HITL przy trwałej awarii akcji krytycznej, obsługa **częściowych wyników** przy równoległości. Por. [[obsluga-bledow-system-wieloagentowy]].

## 14. Pytania pogłębiające (senior / trade-offy)

**1. „Więcej autonomii = lepiej" — dlaczego to fałsz? Gdzie granica elastyczności vs przewidywalności?**

Każda decyzja oddana modelowi to dodatkowy **punkt niedeterminizmu**. Im więcej swobodnych decyzji w łańcuchu, tym **wykładniczo** rośnie przestrzeń możliwych trajektorii, a z nią szansa, że któraś pójdzie źle — plus rośnie koszt i trudność testowania/audytu. Autonomia nie jest wartością samą w sobie; jest narzędziem na **różnorodność wejść**.

**Granica**: elastyczność opłaca się tam, gdzie wartość obsłużenia nieprzewidywalnych wejść przewyższa koszt nieprzewidywalności (research, eksploracja). Gdzie ścieżka jest znana — deterministyczny kod jest tańszy, szybszy i pewniejszy. Przy operacjach **nieodwracalnych/wrażliwych** przewidywalność wygrywa zawsze. Inżynierska reguła: **dawkuj autonomię tylko tam, gdzie naprawdę potrzeba**, a resztę „zabij" deterministycznym kodem, guardrailami i HITL.

---

**2. Jak pogodzić niedeterminizm generatora z wymogiem deterministycznych, wersjonowanych artefaktów?**

Klucz to **rozdzielenie faz**: generowanie (niedeterministyczne, kreatywne) ≠ wykonywanie utrwalonego artefaktu (deterministyczne, wersjonowane). Agent **raz** generuje wynik (np. zestaw testów, plan, konfigurację); ten wynik jest następnie **zreviewowany, zatwierdzony i zamrożony jako kod**, a odtąd uruchamiany deterministycznie — bez ponownego wołania modelu.

- Człowiek lub bramka zatwierdza artefakt przed utrwaleniem; agent **proponuje**, system **wersjonuje**.
- W samej egzekucji: `temperature=0`, seed, **record-replay** nagranych odpowiedzi.
- Sedno: niedeterminizm jest dopuszczalny **przy tworzeniu**, niedopuszczalny **przy odtwarzaniu** utrwalonego. Granica = moment zatwierdzenia artefaktu.

---

**3. Kiedy zamieniasz rozumowanie LLM na deterministyczny kod? Co zostaje „w modelu", a co „w kodzie"?**

- **W kodzie**: kroki znane, deterministyczne, weryfikowalne, wrażliwe lub powtarzalne — walidacja, parsowanie, routing po jasnych regułach, obliczenia, formatowanie, transakcje. Tańsze, szybsze, testowalne, pewne.
- **W modelu**: rozumienie języka naturalnego, niejednoznaczność, otwarta przestrzeń decyzji, ekstrakcja/generacja, adaptacja do nieprzewidywalnych wejść.

**Decyzja**: jeśli da się napisać poprawną regułę, a wejście jest ustrukturyzowane → kod. Jeśli reguła musiałaby się rozgałęziać w nieskończoność albo wymaga prawdziwego „rozumienia" → model. Zasada przewodnia: maksymalnie dużo **deterministycznego rusztowania**, LLM tylko tam, gdzie naprawdę go potrzeba.

---

**4. Anty-wzorce w budowie agentów.**

- **Przeinżynierowany multi-agent** tam, gdzie wystarczy single-agent (koszt, latencja, gubienie kontekstu w handoffach).
- **Za dużo narzędzi** w jednym kontekście → spadek trafności wyboru.
- **Brak limitów** (kroków/tokenów/czasu) → zapętlenia i przepalanie budżetu.
- **Ślepa wiara w self-healing / self-critique** bez twardego, zewnętrznego sygnału → maskowanie błędów zamiast ich usuwania.
- **Agent „do wszystkiego"** bez wąskiej roli, mgliste prompty i opisy narzędzi, brak observability, brak walidacji argumentów, autonomia na akcjach nieodwracalnych bez HITL, brak ewaluacji/regresji, **niewersjonowane prompty** (cicha zmiana zachowania na produkcji).

---

**5. Jak zapewnić odtwarzalność (replay) mimo niedeterminizmu modelu?**

**Utrwalaj**: wszystkie wejścia/wyjścia LLM (prompty, odpowiedzi, tool calls), obserwacje z narzędzi, **stan po każdym kroku** (checkpointing), wersje promptu/modelu/kodu, seedy i parametry. Replay realizuj jako **record-replay** — odtworzenie z nagranych odpowiedzi, a nie ponowne wołanie modelu.

**Nie utrwalaj** (lub ostrożnie): sekrety, dane wrażliwe (anonimizacja), efemeryczne zasoby. Dodatkowo: **idempotency**, by replay nie powtarzał skutków ubocznych, time-travel z checkpointów (LangGraph) i wersjonowanie wszystkiego, co wpływa na zachowanie (prompt to też kod).

---

**6. Single-agent + dużo narzędzi vs multi-agent + wąskie role — kompromisy.**

- **Single + dużo narzędzi**: prościej, taniej (mniej wywołań i hopów), łatwiejszy debug. Ale skaluje się źle z liczbą narzędzi — przeładowany kontekst, spadek trafności wyboru, jeden przerośnięty prompt.
- **Multi + wąskie role**: każdy kontekst mały i trafny, specjalizacja, równoległość, izolacja błędów. Ale ↑ koszt i latencja (rundy komunikacji), gubienie kontekstu w handoffach, trudniejszy tracing, ryzyko przeinżynierowania.

**Co skaluje się lepiej**: pod względem liczby/różnorodności narzędzi i specjalizacji — multi-agent; pod względem kosztu, latencji i prostoty — single-agent. Reguła: zacznij od single-agent, dziel dopiero pod realny ból (przeładowany kontekst, potrzeba równoległości, rozłączne role).

---

**7. „Budżet zaufania" — które decyzje agent podejmuje sam i jak to ewoluuje?**

Metafora: agent ma **budżet** decyzji, które może podjąć samodzielnie; im większy potencjalny koszt i nieodwracalność błędu, tym mniejsza dozwolona autonomia.

- **Read-only / odwracalne / tanie** → autonomicznie.
- **Mutujące / nieodwracalne / kosztowne / wrażliwe** (płatność, usunięcie, prod) → HITL / approval gate.

**Ewolucja**: budżet **rośnie wraz z dojrzałością** — gdy ewaluacja i observability pokażą wysoki success rate i niski rate błędów na danej *klasie* akcji, stopniowo zdejmujesz bramki (canary → pełna autonomia). **Maleje** po incydencie. Powinien być kalibrowany **danymi, nie przeczuciem**, i ustalany per typ akcji, a nie globalnie.

---

**8. Jedna rzecz, która najczęściej decyduje o sukcesie agenta w produkcji.**

Najmocniejsza pojedyncza odpowiedź: **jakość kontekstu dostarczanego modelowi** (context engineering) — właściwe informacje, narzędzia z dobrymi opisami i czysty, niezaszumiony kontekst. Nawet najlepszy model decyduje **tylko na podstawie tego, co widzi**; większość porażek to „garbage in".

Szersza, równoważna formuła: **dyscyplina inżynierska wokół modelu** — guardrails, limity, walidacja, ewaluacja/observability, HITL — czyli traktowanie agenta jak system produkcyjny, nie demo. Uzasadnienie: modele są wymienne i wciąż się poprawiają; o tym, czy produkt działa, decyduje **obudowa wokół modelu** (kontekst + zabezpieczenia + pętla ewaluacji), bo to ona, a nie sam model, odróżnia działający system od efektownego dema.

---

## Powiązane notatki

- [[create-agent-vs-react-agent]] — gotowy agent vs własny graf (LangChain/LangGraph)
- [[narzedzia-dla-agentow-tool-use-langgraph]] — tool use dla agentów
- [[multi-agent-supervisor-langgraph]] — wzorzec supervisor
- [[langchain-multi-agent-patterns]] — wzorce wieloagentowe w LangChain
- [[wzorce-projektowe-systemow-agentowych]] — wzorce projektowe systemów agentowych
- [[orkiestrator-vs-planner-w-architekturze-wieloagentowej]] — orkiestrator vs planner
- [[agentic-workflows-multi-agent-orchestration]] — orkiestracja workflowów agentowych
- [[obsluga-bledow-system-wieloagentowy]] — obsługa błędów w systemie wieloagentowym
- [[zadanie-rekrutacyjne-system-wieloagentowy]] — przykładowe zadanie rekrutacyjne
- [[checkpointers-langgraph]] / [[pamiec-i-persistence-checkpointers-langgraph]] / [[persistence-sqlite-postgres-langgraph]] — persystencja stanu
- [[interrupts-langgraph]] / [[human-in-the-loop-interrupt-langgraph]] — przerwania i HITL
- [[rownolegle-wezly-fan-out-fan-in-langgraph]] — równoległe węzły
- [[streaming-langgraph]] — streaming w LangGraph
- [[komponenty-ekosystemu-langchain]] / [[komunikacja-z-llm-w-langchain]] / [[langchain-middlewares]] / [[chat-history-langchain-langgraph]] — komponenty LangChain
- [[memory-management-i-session-handling]] / [[projektowanie-memory-management-oraz-session-handling-dla-agentow-ai]] / [[pamięć-długoterminowa-ai]] — pamięć i sesje
- [[structured-output-z-llm]] / [[with_structured_output_vs_pydantic_parser]] — structured output
- [[ai-prompt-orchestration]] — orkiestracja promptów
- [[mcp-ai-engineer-interview]] — Model Context Protocol
- [[llm-guardrails]] / [[bezpieczenstwo-danych-kontrola-dostepu-governance-ai]] — guardrails i governance
- [[czy-znasz-termin-context-engineering-w-ai]] — context engineering
