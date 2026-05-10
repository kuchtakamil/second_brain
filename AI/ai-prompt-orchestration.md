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
2. **Routing (Dynamiczne przekierowywanie)**: Klasyfikacja wejścia i wybór odpowiedniej ścieżki wykonania lub specjalistycznego modelu.
   *Przykład*: Jeśli pytanie użytkownika dotyczy problemu z kodem, skieruj je do programistycznego agenta, w przeciwnym razie do ogólnego asystenta.
3. **Parallelization (Równoległość / Fan-out Fan-in)**: Uruchomienie kilku promptów lub agentów jednocześnie i późniejsza agregacja wyników.
   *Przykład*: Agent Recenzent równolegle analizuje kod pod kątem bezpieczeństwa, wydajności i stylu, a następnie reduktor (reducer) łączy te 3 analizy w jeden raport.
4. **Stateful Cyclic Workflows (Przepływy cykliczne i stanowe)**: Wykorzystanie grafów do modelowania pętli i zależności.
   *Przykład*: Agent Kodujący generuje skrypt -> Narzędzie uruchamia skrypt -> Jeśli pojawia się wyjątek, logi trafiają z powrotem do Agenta Kodującego w celu poprawy (pętla trwa do sukcesu lub limitu prób).

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
