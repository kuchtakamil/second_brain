# AI Prompt Orchestration

**Prompt Orchestration** (orkiestracja promptów) to zaawansowany proces koordynacji wielu wywołań modeli językowych (LLM), narzędzi zewnętrznych, pamięci oraz logiki decyzyjnej w celu realizacji złożonych zadań. Zamiast wysyłać pojedyncze zapytania do modelu, orkiestrator zarządza przepływem informacji (workflow), tworząc łańcuchy, grafy lub współpracujące ze sobą systemy wieloagentowe.

## Dlaczego to jest ważne?

Pojedyncze prompty sprawdzają się w prostych zadaniach (np. "przetłumacz ten tekst"). Gdy system musi analizować dane z API, podejmować decyzje na podstawie wyników, korygować własne błędy i utrzymywać stan, proste wywołanie modelu zawodzi. Orkiestracja zapewnia:

- **Niezawodność**: Możliwość implementacji pętli weryfikacyjnych i automatycznej poprawy błędów (self-correction).
- **Radzenie sobie ze złożonością**: Rozbicie ogromnego problemu na mniejsze, wyspecjalizowane kroki (np. Planner -> Researcher -> Writer).
- **Optymalizację kosztów i czasu**: Kierowanie prostych, powtarzalnych zadań do mniejszych, szybszych modeli, a kluczowych decyzji logicznych do tych najbardziej zaawansowanych.
- **Zarządzanie stanem**: Utrzymywanie pamięci krótkotrwałej (kontekst bieżącego zadania) i długotrwałej współdzielonej między różnymi etapami działania systemu.

## Jak to działa (Kluczowe wzorce)

Nowoczesna orkiestracja opiera się na sprawdzonych wzorcach architektonicznych:

1. **Chaining (Łańcuchowanie sekwencyjne)**: Wyjście z pierwszego promptu staje się wejściem dla drugiego.
   *Przykład*: Prompt A (wydobądź kluczowe fakty z dokumentu) -> Prompt B (napisz oficjalnego e-maila na podstawie faktów z Promptu A).
2. **Routing (Dynamiczne przekierowywanie)**: Klasyfikacja wejścia i wybór odpowiedniej ścieżki wykonania lub specjalistycznego modelu. Uwaga terminologiczna: routing to **nie** to samo co orkiestrator — to jeden z wzorców, którymi orkiestrator się posługuje. Orkiestrator jest nadrzędnym koordynatorem całego przepływu (zarządza stanem, narzędziami i kolejnością kroków), a routing to konkretna decyzja „dokąd skierować to wejście" podejmowana wewnątrz tego przepływu.
   *Przykład*: Jeśli pytanie użytkownika dotyczy problemu z kodem, skieruj je do programistycznego agenta, w przeciwnym razie do ogólnego asystenta.
3. **Parallelization (Równoległość / Fan-out Fan-in)**: Uruchomienie kilku promptów lub agentów jednocześnie i późniejsza agregacja wyników. Ponieważ wywołania LLM są zwykle ograniczone czasem odpowiedzi (I/O-bound), a nie obliczeniami lokalnymi, uruchomienie ich równolegle (`asyncio.gather`, `Promise.all`) skraca łączny czas niemal do czasu najwolniejszego z nich — zamiast sumy wszystkich.
   *Przykład*: Agent Recenzent równolegle analizuje kod pod kątem bezpieczeństwa, wydajności i stylu, a następnie reduktor (reducer) łączy te 3 analizy w jeden raport.

   **Dwa warianty wzorca:**
   - **Sectioning (podział zadania)**: jeden problem dzielimy na **niezależne podzadania**, które liczą się jednocześnie, a wyniki sklejamy. Przykład wyżej (bezpieczeństwo / wydajność / styl) to właśnie sectioning. Dobre, gdy podzadania nie zależą od siebie nawzajem i każde wymaga skupionego kontekstu.
   - **Voting (głosowanie / ensemble)**: **to samo** zadanie uruchamiamy kilka razy (często z różnymi promptami lub temperaturą), a następnie wybieramy odpowiedź większością głosów lub agregujemy. Podnosi to niezawodność tam, gdzie pojedyncze wywołanie bywa zawodne — np. ocena „czy ten kod ma lukę bezpieczeństwa", gdzie wolimy kilka niezależnych opinii niż jedną.

   **Faza Fan-in (agregacja)** jest tak samo ważna jak rozproszenie. Reducer może być prosty (konkatenacja, suma, głosowanie większościowe) albo sam być wywołaniem LLM, które syntetyzuje cząstkowe wyniki w spójną całość. Tu też trzeba zaplanować obsługę **częściowych porażek** — co zrobić, gdy 1 z 3 gałęzi zwróci błąd lub timeout (pominąć, ponowić, czy przerwać całość).

   **Kompromis**: równoległość tnie czas (latencję), ale **nie** koszt — N wywołań to N razy więcej tokenów, tyle że poniesionych naraz. Warto jej używać tam, gdzie zależy nam na szybkości lub na różnorodności perspektyw, a nie po to, by oszczędzać.
4. **Stateful Cyclic Workflows (Przepływy cykliczne i stanowe)**: Wykorzystanie grafów do modelowania pętli i zależności. W przeciwieństwie do prostego łańcucha (DAG — graf acykliczny), przepływ cykliczny pozwala wrócić do wcześniejszego węzła i powtórzyć krok, dopóki warunek nie zostanie spełniony. To właśnie ten wzorzec odróżnia prawdziwego *agenta* (który iteruje aż do osiągnięcia celu) od zwykłego potoku promptów.
   *Przykład*: Agent Kodujący generuje skrypt -> Narzędzie uruchamia skrypt -> Jeśli pojawia się wyjątek, logi trafiają z powrotem do Agenta Kodującego w celu poprawy (pętla trwa do sukcesu lub limitu prób).

   **Dwa filary tego wzorca:**
   - **Stan (State)**: współdzielony obiekt przekazywany między iteracjami, gromadzący kontekst — historię prób, dotychczasowe wyniki, liczniki. Bez trwałego stanu pętla „nie pamięta", co już próbowała, i kręci się w kółko. Narzędzia takie jak LangGraph utrwalają ten stan przez **Checkpointers**, co dodatkowo umożliwia wznawianie przerwanego przepływu i wstrzymanie na akcję człowieka (Human-in-the-Loop).
   - **Cykl (Cycle) z warunkiem stopu**: krawędź warunkowa decyduje, czy wrócić do węzła, czy zakończyć. **Zawsze** trzeba zdefiniować bezpiecznik (np. `max_iterations`), inaczej błędnie działający agent wpadnie w nieskończoną pętlę, generując koszty i ryzyko zapętlenia tego samego błędu.

   **Typowe realizacje tego wzorca:**
   - **ReAct (Reason + Act)**: model na zmianę rozumuje i wywołuje narzędzia, a obserwacje z narzędzi wracają do niego w kolejnej iteracji — aż uzna, że ma odpowiedź.
   - **Reflection / Self-correction**: jeden węzeł (lub osobny agent-krytyk) ocenia wynik i odsyła go do poprawy z konkretną informacją zwrotną, podnosząc jakość bez udziału człowieka.
   - **Pętla weryfikacyjna z narzędziem**: wynik jest sprawdzany twardym narzędziem (kompilator, testy, walidator schematu, linter); porażka uruchamia kolejną iterację. To najpewniejsza forma — sygnał stopu jest deterministyczny, nie pochodzi z samooceny modelu.

## Nowoczesne narzędzia (Obecny standard)

Tradycyjne frameworki pierwszej fali (jak wczesny LangChain oparty na klasach `LLMChain` czy `AgentExecutor`) ustępują dziś miejsca architekturze opartej na grafach i zdarzeniach. Obecnie wspierane i rozwijane technologie to m.in.:

- **LangGraph**: Stanowi dzisiejszy rynkowy standard od twórców LangChain. Pozwala na budowę systemów w formie stanowych grafów. Umożliwia precyzyjną kontrolę nad cyklicznymi przepływami, pamięcią persystentną (Checkpointers) i wstrzymywaniem procesów (Human-in-the-Loop).
- **LlamaIndex Workflows**: Wprowadzone niedawno, w pełni zdarzeniowe (event-driven) podejście do orkiestracji. Zamiast budować sztywne grafy, węzły emitują i nasłuchują określonych zdarzeń (Events), co czyni architekturę asynchroniczną i wysoce skalowalną.
- **Vercel AI SDK (Core)**: Niezwykle wydajny i nowoczesny standard w ekosystemie TypeScript/React. Skupia się na programistycznej prostocie orkiestracji na styku LLM-Frontend (np. Generative UI, streamowanie wywołań narzędzi prosto do interfejsu).
- **CrewAI**: Bardzo popularny framework specjalizujący się w systemach wieloagentowych (multi-agent). Opiera się na koncepcji "Role-playing" – agenci otrzymują konkretne role, zadania (Tasks) oraz narzędzia, a orkiestrator deleguje pracę sekwencyjnie lub w sposób zorganizowany hierarchicznie.

## Przykład koncepcyjny: Orkiestracja wsparcia technicznego (LangGraph)

W poniższym pseudokodzie orkiestrator zarządza stanem zgłoszenia i decyduje (Routing), co ma się wydarzyć.

```python
from typing import TypedDict
from langgraph.graph import StateGraph, END

# Stan współdzielony między wszystkimi etapami
class State(TypedDict):
    ticket_text: str
    category: str
    draft_reply: str

def classifier_node(state: State):
    # Wywołanie LLM określające kategorię ("Billing", "Tech", "Other")
    return {"category": "Billing"}

def route_based_on_category(state: State):
    # Routing decydujący o dalszej ścieżce
    if state["category"] == "Billing":
        return "billing_agent"
    return "human_escalation"

def billing_agent_node(state: State):
    # Agent wykorzystujący narzędzia (dostęp do bazy) by sprawdzić faktury
    return {"draft_reply": "Znaleźliśmy błąd w fakturze..."}

def human_escalation_node(state: State):
    # Wymagany czynnik ludzki (Human-in-the-loop)
    return {"draft_reply": "Przekazano do konsultanta."}

# Budowa grafu orkiestracji
workflow = StateGraph(State)

workflow.add_node("classifier", classifier_node)
workflow.add_node("billing_agent", billing_agent_node)
workflow.add_node("human", human_escalation_node)

workflow.set_entry_point("classifier")

# Węzeł klasyfikatora decyduje, gdzie skierować przepływ
workflow.add_conditional_edges(
    "classifier",
    route_based_on_category,
    {
        "billing_agent": "billing_agent",
        "human_escalation": "human"
    }
)

workflow.add_edge("billing_agent", END)
workflow.add_edge("human", END)

app = workflow.compile()
```

## Powiązane

- [Multi-Agent Supervisor LangGraph](multi-agent-supervisor-langgraph.md)
