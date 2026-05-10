# Simple Agent (create_agent) vs ReAct Agent (create_react_agent)

Krótkie podsumowanie dwóch podejść do tworzenia agentów w ekosystemie LangChain/LangGraph. Główne różnice sprowadzają się do obecności (lub braku) pętli wykonawczej, co drastycznie zmienia możliwości i przeznaczenie modelu.

## Dlaczego to jest ważne?

Zrozumienie, kiedy używamy pętli (ReAct), a kiedy odpalamy model tylko na raz, jest kluczowe w projektowaniu systemów AI. Rzutuje to na koszt, czas odpowiedzi (latency) i zdolność agenta do "myślenia", pozyskiwania informacji oraz korygowania swoich błędów.

## Różnice w podejściach

### 1. Simple Agent / Tool Calling Chain (tworzony zazwyczaj przez podstawowe funkcje jak np. `create_agent`)
Przepływ (flow): `Query -> LLM -> Tool (Act) -> Output`

- LLM działa tu jednorazowo. Otrzymuje zapytanie użytkownika, decyduje się wywołać konkretne narzędzie jako odpowiedź, a system uruchamia to narzędzie i zwraca jego surowy wynik użytkownikowi. Nie ma zapętlonego kroku "Observe", w którym model czytałby wynik z narzędzia.
- W starszym ekosystemie LangChain narzędzia takie jak np. `create_openai_tools_agent` generują tak naprawdę sam mechanizm (Runnable), który działa na zasadzie przepływu łańcuchowego. Zakończy on swoje działanie po wygenerowaniu żądania wywołania narzędzia. Aby uzyskać z niego pętlę, konieczne było przekazanie takiego "agenta" do `AgentExecutor`, który implementował w sobie mechanizm zapętlania.

### 2. ReAct Agent (`create_react_agent` np. z LangGraph)
Przepływ (flow): `Query -> LLM -> Tool (Act) -> Observe (powrót do LLM) -> [opcjonalnie kolejne iteracje] -> Answer`

- Ten flow od razu implementuje na poziomie silnika pętlę **ReAct** (Reasoning and Acting).
- Oznacza to, że LLM decyduje o uruchomieniu narzędzia, system je wykonuje, a następnie zwraca pobrany wynik *z powrotem* do tego samego LLM-a. Model czyta wynik, wyciąga z niego wnioski i w kolejnym ruchu decyduje co dalej: czy wywołać inne potrzebne narzędzie, czy przygotować i sformułować dla użytkownika odpowiedź w języku naturalnym.

---

## Odpowiedzi na Twoje pytania

> **"Skoro w flow simple agent (Tool Act) idzie od razu do Answer (output), to znaczy że tutaj LLM nie dostaje wyniku z działania toola?"**

**Tak, dokładnie tak to wygląda.** W tym uproszczonym, liniowym przepływie (chain bez pętli) proces wygląda przeważnie tak: 
1. Wysyłasz np. zapytanie "Jaka jest pogoda w Krakowie?".
2. LLM stwierdza "muszę wywołać funkcję od pogody" i na wyjściu generuje z ustruktruryzowanego schematu JSON z argumentami (tzw. wywołanie `tool_call`). Zakończył w tym miejscu swoje zadanie.
3. Twój system aplikacyjny odbiera tego JSON-a, odpala kod w środowisku Python (np. uderza w API z pogodą), API odpowiada odczytem `{"temp": 15}`.
4. Twój system (albo LangChainowy Chain) wypluwa wynik z narzędzia. Ostatecznym rezultatem całego flow jest surowe: `{"temp": 15}`.

> **"Czy ten flow w ogóle jest poprawny?"**

**Jak najbardziej.** Wymieniony wzorzec z zadowoleniem jest używany z sukcesem i nazywa się go najczęściej jako *"Tool Calling Flow"*, *Data Extraction* albo *Router*.
Używa się go z myślą o systemach, gdzie zależy nam aby po prostu wyciągnąć ze świata lub API ukryte dane w konkretnej, silnie narzuconej strukturze i obsłużyć to w kodzie własnym (np. aplikacją), bez straty tokenów i opóźnienia na ładne ubierane tego w słowa. Przykład to system asystenta zarządzania domem inteligentnym – użytkownik rzuca "wyłącz w końcu to światło w salonie!". LLM dokonuje transkrypcji z polskiego na intencję `turn_off(light_id=12)`, system de facto gasi prąd i flow dobiega końca. Dzięki węższemu zakresowi ten przepływ jest tańszy, znacznie szybszy na środowiskach i w 100% użyteczny.

> **"Czy taki agent nie mógłby korzystać np. z toola pobierającego temperaturę w Krakowie i po przeczytaniu tej wartości opakować ją w jakieś zdanie i wysłać użytkownikowi?"**

**Nie, po prostu z racji tego, że skończyło mu się wykonanie, nie mógłby w tym jedynym przebiegu (liniowym flow).** 
Żeby spełnić to, o czym myślałeś na samym początku, potrzebujesz przynajmniej jednorazowej iteracji — wynik, czyli wyciągnięte przykładowe `15°C`, absolutnie na dnie mechaniki po wyciągnięciu musi zostać dołączony jako "Observation" z powrotem do prompta asystenta i wywołać nowe API LLM-a! Model otrzymuje nowy kontekst z poprzednim wynikiem i po lekturze generuje wyjście normalną prozą, dopisując wynik z odpowiedzi z narzędzia jako "Aktualnie w Krakowie notuje się równo 15 stopni (Celsjusza).".

Taka nawrotka nazywa się właśnie wzorcem **ReAct Agent** (dlatego `create_react_agent` zapewnia ten uśmiechnięty loop by default). Kiedy podpinasz wywoływanie narzędzi bez zapętlania i z chęcią uzyskania wypowiedzi z LLMa, wymagałoby to zaprogramowania w swoim kodzie wywoływania drugiej intencji prosto pod drugiem strzałem API z wynikiem Tool-a do LLMa pod koniec. 

## Zobacz również (Powiązane Tagi)
- [Wzorce projektowe systemów agentowych](wzorce-projektowe-systemow-agentowych.md)
- [Strukturyzowane wyjście LLM](langchain-structured-output-jinja2.md)
