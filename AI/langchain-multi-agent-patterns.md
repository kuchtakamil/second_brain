# Wzorce Multi-Agentowe w LangChain (Subagents, Handoffs, Skills, Router)

Wraz z rozwojem ekosystemu LangChain (i w szczególności wyłonieniem się frameworka **LangGraph**), popularnością zaczęły cieszyć się zaawansowane wzorce projektowe dla systemów typu multi-agent. Wzorce takie jak **Subagents**, **Handoffs**, **Skills** oraz **Router** pozwalają na budowanie złożonych, wysoce zorganizowanych i przewidywalnych systemów AI, które działają niezawodnie w skali produkcyjnej poprzez rozdzielenie odpowiedzialności pomiędzy różne, specjalizowane komponenty.

## Dlaczego to ma znaczenie?

Pojedynczy potężny agent LLM może się zgubić, zacząć "halucynować" lub zgubić sens zadania, gdy dostarczymy mu kilkanaście narzędzi (tools) i sprzecznych czy też bardzo skomplikowanych instrukcji w jednym dużym prompcie. Wdrażanie systemów opartych na jednym agencie sprawdza się tyko przy powierzchownych i prostych zadaniach.

Złożone procesy biznesowe wymagają dekompozycji i specjalizacji poszczególnych "pracowników AI" (agentów), co daje nam:
- Lepszą precyzję i kontrolę na poziomie konkretnej dziedziny (każdy subagent ma własny, krótki prompt systemowy).
- Ograniczenie i specjalizację kontekstu (tzw. context window), dzięki czemu wysyłamy modelowi tylko te informacje i funkcje, których potrzebuje do wąskiego zadania.
- Znacznie łatwiejsze testowanie, niezależny rozwój (np. inny zasób dla Supportu, inny dla Analizy Danych) i stabilniejsze procesy dla całej aplikacji zbudowanej wokół AI.

## Jak to działa (Kluczowe koncepcje)

Budując zaawansowany wieloagentowy system w najnowszym LangChain/LangGraph, zazwyczaj operujemy poniższymi koncepcjami:

### 1. Skills (Umiejętności)
**Skills** to po prostu dedykowane narzędzia (najczęściej instancje obiektów `Tool`), w które wyposażamy agentów. Jeden "skil" (np. przeszukiwanie internetu, sprawdzenie rachunku klienta) to zwykła pythonowa funkcja posiadająca własny docstring (używany potem przez AI przy podjęciu decyzji, jak takiego skilla użyć). 

```python
from langchain_core.tools import tool

@tool
def check_order_status(order_id: str) -> str:
    """Zwraca status zamówienia po jego unikalnym numerze ID."""
    return "Status: Wysłano"
```

### 2. Subagents (Pod-agenci / Specjaliści)
**Subagent** to niezależny agent posiadający wąską specjalizację, własny węższy polecenia zachowania (System Prompt) i przypisany mu ograniczony zbiór *Skills*. Subagent wykonuje w systemie jedno specjalistyczne zadanie podlegające wyższemu nadzorowi. Na przykład: `BillingAgent` albo `TechSupportAgent`. 

W grafowej architekturze LangGraph subagent jest wdrażany jako oddzielny wierzchołek (Node) w ogólnym przepływie stanu sieci (`StateGraph`). 

### 3. Router (Koordynator / Dyspozytor)
**Router** w architekturze agentowej działa jak recepcjonista lub warunkowy drogowskaz w LangGraph. Jego bezpośrednim obowiązkiem nie jest odpowiadać na pytanie użytkownika. Ma on na celu odczytanie intencji i wybranie najlepszego subagenta do jej obsłużenia.
Osiąga się to wymuszając odpowiedni format danych – w najnowszych mechanizmach stosując tzw. *Structured Output* (wymuszenie by model zwrócił obiekt Pydantic lub enum), za pomocą którego przepływ programu przechodzi do wskazanego pod-agenta.

```python
from typing import Literal
from pydantic import BaseModel, Field

class RouterOutput(BaseModel):
    next_action: Literal["billing_agent", "support_agent", "human"] = Field(
        description="Zdecyduj, gdzie przekierować klienta."
    )
```

### 4. Handoffs (Przekazanie kontroli)
**Handoffs** to zaawansowany wzorzec pozwalający jednemu agentowi w trakcie swojej pracy zorientować się, że sprawa nie dotyczy jego kompetencji, po czym przekazać ("oddać") komunikację i kontrolę do innego agenta. O ile *Router* działa zazwyczaj przed podjęciem działań, **Handoff** jest mechanizmem reagującym na rozwój zdarzeń. 

W systemie opartym o LLM implementuje się to dając modelowi fikcyjne narzędzie "Skill" o nazwie np. `transfer_to_support`. Model może wywołać to narzędzie, a system obsługujący jego wyjście zorientuje się, że musi przenieść cały dotychczasowy stan kontekstu rozmowy jako wejście do nowego wierzchołka operacyjnego (Node). W najnowszym LangGraph używa się do tego celu specjalnych wyjątków lub obiektów, m.in. obiektu `Command`.

```python
# Przykład nowoczesnego wzorca Handoff w LangGraph z użyciem Command
from langgraph.types import Command

def frontend_dev_agent(state: dict):
    # Agent frontendowy decyduje, że zadanie wymaga zmian w API
    # i ręcznie oddaje sterowanie innemu węzłowi w grafie
    return Command(
        goto="backend_dev_agent",
        update={"messages": [("ai", "Przekazuję proces ekspertowi ds. backendu.")]}
    )
```

## Architektura w Praktyce

Kompozycja tych elementów przeważnie opiera się na wytycznych zwanych **Supervisor Framework** (ang. sieć z elementem nadrzędnym). Workflow takiego układu to:
1. Zewnętrzne polecenie wchodzi początkowo do elementu decyzyjnego (**Routera** albo Supervisory Agenta).
2. Oparty o logikę LangGraph, agent główny ewaluuje, jakiego eksperta wezwać i decyduje o delegacji do specyficznego **Subagenta**.
3. **Subagent** rozpoczyna pętlę ReAct rozwiązując problem użytkownika z pomocą dostarczonych do niego wąskich narzędzi (**Skills**).
4. Gdy ten domyka sprawę lub brakuje mu uprawnień do innego zadania, wykonuje **Handoff**, cofając odpowiedź do Routera lub kierując prosto do innej jednostki.

Architektura ta, ze względu na rygor grafowy wymuszony przez LangGraph (w kontekście LangChain w wersjach nowoczesnych tj. 0.2 / 0.3+), oferuje doskonałą skalowalność potężnych asystentów AI. 

## Powiązane materiały
- [Wzorce projektowe systemów agentowych](wzorce-projektowe-systemow-agentowych.md)
- [Komunikacja z LLM w Langchain](komunikacja-z-llm-w-langchain.md)
- [Create Agent vs ReAct Agent](create-agent-vs-react-agent.md)
