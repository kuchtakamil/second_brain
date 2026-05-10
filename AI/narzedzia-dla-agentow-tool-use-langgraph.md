# Narzędzia dla agentów (Tool Use) w LangGraph

## Krótki opis

Agenty LLM z natury potrafią jedynie generować tekst. Aby mogły **działać w świecie zewnętrznym** — wyszukiwać w internecie, wykonywać obliczenia, odpytywać bazy danych czy odczytywać czas systemowy — potrzebują **narzędzi (tools)**. LangGraph (≥ 1.0) dostarcza kompletny system integracji narzędzi oparty na trzech filarach:

1. **Dekorator `@tool`** — zamienia zwykłą funkcję Pythona w obiekt `Tool` ze schematem zrozumiałym dla LLM.
2. **`model.bind_tools(tools)`** — informuje model o dostępnych narzędziach, pozwalając mu generować strukturalne wywołania (`tool_calls`) zamiast zwykłego tekstu.
3. **`ToolNode`** — wbudowany węzeł LangGraph, który automatycznie wykonuje narzędzia wywoływane przez model i zwraca wyniki jako `ToolMessage`.

Te trzy elementy razem tworzą **pętlę ReAct** (Reasoning and Acting): agent analizuje problem → wywołuje narzędzie → obserwuje wynik → kontynuuje rozumowanie, aż uzna, że ma wystarczająco informacji, by odpowiedzieć użytkownikowi.

## Dlaczego to ważne / Kiedy stosować?

- **Agent bez narzędzi to chatbot** — może jedynie generować tekst na podstawie wiedzy wytrenowanej w modelu. Narzędzia przekształcają go w system zdolny do interakcji ze światem.
- **Aktualność danych** — LLM nie zna informacji spoza okna treningowego. Narzędzie `search_web` daje mu dostęp do bieżących danych.
- **Deterministyczne obliczenia** — LLM jest statystyczny i popełnia błędy arytmetyczne. Dedykowane narzędzie `calculate` daje dokładne wyniki.
- **Integracja z systemami zewnętrznymi** — odpytywanie baz danych, API, systemów plików, serwisów pogodowych, kalendarzy itp.
- **Wzorzec ReAct** — umożliwia agentowi iteracyjne rozwiązywanie złożonych problemów wymagających wielu kroków i wielu źródeł informacji.

---

## Kluczowe koncepty

### 1. Dekorator `@tool` — tworzenie narzędzi

Dekorator `@tool` z pakietu `langchain_core.tools` zamienia funkcję Pythona w obiekt `Tool`. Model używa **docstringu** funkcji, aby zrozumieć, kiedy i jak narzędzia użyć, a **type hints** argumentów, aby wygenerować poprawne wywołanie ze strukturalnymi parametrami (JSON Schema).

```python
from langchain_core.tools import tool

@tool
def search_web(query: str) -> str:
    """Wyszukaj informacje w internecie na zadany temat.

    Args:
        query: Zapytanie do wyszukiwarki internetowej.
    """
    # W produkcji: integracja z Tavily, SerpAPI, Google Search API itp.
    return f"Wyniki wyszukiwania dla: {query} ..."

@tool
def calculate(expression: str) -> str:
    """Oblicz wyrażenie matematyczne i zwróć wynik.

    Args:
        expression: Wyrażenie matematyczne do obliczenia, np. '2 + 2 * 3'.
    """
    try:
        result = eval(expression)  # W produkcji użyj bezpiecznego parsera (sympy, numexpr)
        return str(result)
    except Exception as e:
        return f"Błąd obliczania: {e}"

@tool
def get_current_time() -> str:
    """Zwróć aktualną datę i godzinę w strefie czasowej serwera."""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
```

**Co dokładnie robi `@tool`?**

| Aspekt | Działanie |
|---|---|
| **Nazwa** | Pobiera z `function.__name__` (np. `search_web`) |
| **Opis** | Pobiera z docstringu — model czyta go, by zdecydować, kiedy narzędzia użyć |
| **Schemat argumentów** | Generuje JSON Schema na podstawie type hints (np. `query: str`) |
| **Walidacja** | Automatycznie waliduje typy argumentów przychodzących od modelu |
| **Wartość zwrotna** | Konwertuje wynik na `str` i opakowuje w `ToolMessage` |

> **Uwaga:** Docstring jest kluczowy — to jedyna informacja, jaką model widzi o narzędziu. Niejasny lub brakujący docstring spowoduje, że model nie będzie wiedział, kiedy narzędzia użyć.

### 2. `model.bind_tools()` — podpięcie narzędzi do modelu

Metoda `bind_tools()` informuje model LLM o dostępnym zestawie narzędzi. Od tego momentu model może, zamiast generować tekst, zwrócić strukturalne żądanie wywołania narzędzia (`tool_calls`) w odpowiedzi.

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o")

tools = [search_web, calculate, get_current_time]
llm_with_tools = llm.bind_tools(tools)
```

**Co dzieje się „pod maską"?**

1. LangChain pobiera JSON Schema każdego narzędzia (nazwa, opis, parametry).
2. Przekazuje je do modelu w formacie natywnym dla danego providera (OpenAI function calling, Anthropic tool use itp.).
3. Model w odpowiedzi może zwrócić `AIMessage` z atrybutem `tool_calls` — listą słowników zawierających nazwę narzędzia, argumenty i ID wywołania.

```python
# Przykład odpowiedzi modelu z tool_call
msg = llm_with_tools.invoke("Ile to jest 15 * 37?")
print(msg.tool_calls)
# [{'name': 'calculate', 'args': {'expression': '15 * 37'}, 'id': 'call_abc123'}]
print(msg.content)
# '' ← model nie generuje tekstu, bo zdecydował się użyć narzędzia
```

> **Ważne:** `bind_tools()` nie wykonuje narzędzi — jedynie daje modelowi **wiedzę o ich istnieniu**. Wykonaniem zajmuje się `ToolNode`.

### 3. `ToolNode` — wbudowany węzeł wykonujący narzędzia

`ToolNode` z `langgraph.prebuilt` to gotowy komponent LangGraph, który:
1. Odczytuje `tool_calls` z ostatniej wiadomości `AIMessage` w stanie.
2. Wywołuje odpowiednią funkcję Pythona z podanymi argumentami.
3. Zwraca wyniki jako obiekty `ToolMessage` dopisywane do historii wiadomości.

```python
from langgraph.prebuilt import ToolNode

tool_node = ToolNode(tools)
```

Alternatywnie można zbudować `tool_node` ręcznie, co daje pełną kontrolę nad obsługą błędów i formatowaniem wyników:

```python
from langchain_core.messages import ToolMessage

def custom_tool_node(state: dict):
    """Ręczna implementacja węzła narzędziowego."""
    results = []
    tools_by_name = {t.name: t for t in tools}

    for tool_call in state["messages"][-1].tool_calls:
        tool = tools_by_name[tool_call["name"]]
        observation = tool.invoke(tool_call["args"])
        results.append(
            ToolMessage(
                content=str(observation),
                tool_call_id=tool_call["id"]
            )
        )
    return {"messages": results}
```

### 4. `tools_condition` — warunkowe routowanie

`tools_condition` z `langgraph.prebuilt` to gotowa funkcja warunkowa, która sprawdza, czy ostatnia wiadomość AI zawiera `tool_calls`. Zwraca nazwę następnego węzła:
- `"tools"` → jeśli model chce wywołać narzędzie.
- `END` → jeśli model wygenerował finalną odpowiedź.

```python
from langgraph.prebuilt import tools_condition
```

Można też napisać ją ręcznie (co jest częstsze w bardziej złożonych grafach):

```python
from langgraph.graph import END

def should_continue(state: dict):
    """Sprawdź, czy model chce wywołać narzędzie."""
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tool_node"
    return END
```

### 5. Pętla ReAct — wzorzec agent → tools → agent

Pętla ReAct to centralny wzorzec integracji narzędzi z agentem. Składa się z cyklicznego przepływu:

```
┌─────────────┐
│             │
│   agent     │──── tool_calls? ──── NIE ──── END (odpowiedź)
│  (LLM call) │
│             │
└──────┬──────┘
       │ TAK
       ▼
┌─────────────┐
│  tool_node  │
│ (wykonanie  │
│  narzędzi)  │
└──────┬──────┘
       │ ToolMessage
       └──────────── z powrotem do agent
```

**Cykl:**
1. **Reasoning** — model analizuje wiadomości (w tym wyniki poprzednich narzędzi) i decyduje: odpowiedzieć użytkownikowi, czy wywołać narzędzie?
2. **Acting** — jeśli `tool_calls` istnieją, graf kieruje przepływ do `ToolNode`, który wykonuje funkcje.
3. **Observation** — wyniki narzędzi (`ToolMessage`) są dopisywane do stanu i przepływ wraca do agenta.
4. **Repeat** — agent ponownie analizuje sytuację. Może wywołać kolejne narzędzie lub zakończyć odpowiedzią.

Pętla trwa, dopóki model nie uzna, że zebrał wystarczająco informacji i wygeneruje finalną odpowiedź bez `tool_calls`.

---

## Krok po kroku: prosty agent z narzędziami

### Krok 1 — Definicja narzędzi

```python
from langchain_core.tools import tool
from datetime import datetime

@tool
def search_web(query: str) -> str:
    """Wyszukaj informacje w internecie na zadany temat.

    Args:
        query: Zapytanie do wyszukiwarki.
    """
    # Symulacja — w produkcji użyj prawdziwego API
    return f"Wyniki dla '{query}': Python 3.12 został wydany we wrześniu 2023."

@tool
def calculate(expression: str) -> str:
    """Oblicz wyrażenie matematyczne.

    Args:
        expression: Wyrażenie do obliczenia, np. '2 + 2'.
    """
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Błąd: {e}"

@tool
def get_current_time() -> str:
    """Zwróć aktualną datę i godzinę."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

tools = [search_web, calculate, get_current_time]
```

### Krok 2 — Konfiguracja modelu z narzędziami

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o")
llm_with_tools = llm.bind_tools(tools)
```

### Krok 3 — Definicja stanu i węzłów

```python
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import SystemMessage

class State(TypedDict):
    messages: Annotated[list, add_messages]

def agent_node(state: State):
    """Węzeł agenta — wywołuje LLM z narzędziami."""
    system_prompt = SystemMessage(
        content="Jesteś pomocnym asystentem. Używaj dostępnych narzędzi, "
                "gdy potrzebujesz aktualnych informacji, obliczeń lub czasu."
    )
    response = llm_with_tools.invoke(
        [system_prompt] + state["messages"]
    )
    return {"messages": [response]}
```

### Krok 4 — Budowa grafu z pętlą ReAct

```python
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode

# Węzeł narzędziowy
tool_node = ToolNode(tools)

# Funkcja routowania
def should_continue(state: State):
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return END

# Budowa grafu
builder = StateGraph(State)
builder.add_node("agent", agent_node)
builder.add_node("tools", tool_node)

# Krawędzie
builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", should_continue, ["tools", END])
builder.add_edge("tools", "agent")  # ← pętla ReAct

# Kompilacja
app = builder.compile()
```

### Krok 5 — Uruchomienie agenta

```python
from langchain_core.messages import HumanMessage

# Pytanie wymagające narzędzia calculate
result = app.invoke({
    "messages": [HumanMessage(content="Ile to jest 1547 * 382?")]
})
for msg in result["messages"]:
    print(f"{msg.type}: {msg.content}")

# human: Ile to jest 1547 * 382?
# ai:                                  ← (pusta treść — model wybrał tool_call)
# tool: 590954                         ← (wynik z calculate)
# ai: 1547 × 382 = 590 954            ← (finalna odpowiedź)
```

```python
# Pytanie wymagające narzędzia get_current_time
result = app.invoke({
    "messages": [HumanMessage(content="Która jest teraz godzina?")]
})
print(result["messages"][-1].content)
# → "Aktualny czas to 2026-04-28 10:05:32."
```

```python
# Pytanie niewymagające narzędzi
result = app.invoke({
    "messages": [HumanMessage(content="Co to jest Python?")]
})
print(result["messages"][-1].content)
# → "Python to język programowania..." (model odpowiada bez użycia narzędzi)
```

---

## Zaawansowany przykład: Router + Agent z narzędziami

Poniższy przykład implementuje pełny wzorzec z routerem (klasyfikatorem), który kieruje zapytanie do odpowiedniego specjalisty. Agent logiczny (z narzędziami) pracuje w pętli ReAct, natomiast terapeuta odpowiada bez narzędzi.

**Wzorzec grafu:**

```
START → classifier → router → logical_agent → (tool_call?) → tool_node → logical_agent → END
                             → therapist → END
```

### Pełna implementacja

```python
from typing import Annotated, Literal
from typing_extensions import TypedDict
from pydantic import BaseModel, Field

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from datetime import datetime

# ============================================================
# 1. NARZĘDZIA
# ============================================================

@tool
def search_web(query: str) -> str:
    """Wyszukaj informacje w internecie.

    Args:
        query: Zapytanie do wyszukiwarki internetowej.
    """
    return f"Wyniki dla '{query}': Znaleziono 3 artykuły naukowe na ten temat."

@tool
def calculate(expression: str) -> str:
    """Oblicz wyrażenie matematyczne.

    Args:
        expression: Wyrażenie matematyczne, np. '(12 + 8) * 3'.
    """
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Błąd obliczania: {e}"

@tool
def get_current_time() -> str:
    """Zwróć aktualną datę i godzinę."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

tools = [search_web, calculate, get_current_time]

# ============================================================
# 2. MODEL
# ============================================================

llm = ChatOpenAI(model="gpt-4o")
llm_with_tools = llm.bind_tools(tools)

# ============================================================
# 3. STAN GRAFU
# ============================================================

class State(TypedDict):
    messages: Annotated[list, add_messages]
    route: str  # "logical" lub "therapist"

# ============================================================
# 4. KLASYFIKATOR (Router)
# ============================================================

class RouteDecision(BaseModel):
    """Decyzja routera o kierunku przekierowania."""
    next: Literal["logical", "therapist"] = Field(
        description="'logical' dla pytań logicznych, analitycznych, "
                    "faktograficznych. 'therapist' dla problemów emocjonalnych."
    )

router_llm = llm.with_structured_output(RouteDecision)

def classifier_node(state: State):
    """Klasyfikator — decyduje, czy pytanie wymaga agenta logicznego, czy terapeuty."""
    decision = router_llm.invoke([
        SystemMessage(
            content="Klasyfikuj intencję użytkownika. Użyj 'logical' "
                    "dla pytań wymagających faktów, obliczeń, wyszukiwania. "
                    "Użyj 'therapist' dla problemów emocjonalnych i wsparcia."
        ),
        state["messages"][-1]
    ])
    return {"route": decision.next}

def route_after_classifier(state: State):
    """Funkcja warunkowa — kieruje przepływ do logical_agent lub therapist."""
    return state["route"]

# ============================================================
# 5. AGENT LOGICZNY (z pętlą ReAct)
# ============================================================

def logical_agent_node(state: State):
    """Agent logiczny — używa narzędzi do odpowiedzi na pytania analityczne."""
    response = llm_with_tools.invoke([
        SystemMessage(
            content="Jesteś precyzyjnym asystentem analitycznym. "
                    "Używaj dostępnych narzędzi (wyszukiwarka, kalkulator, czas), "
                    "aby dostarczyć dokładne odpowiedzi. "
                    "Nie zgaduj — jeśli nie wiesz, wyszukaj."
        )
    ] + state["messages"])
    return {"messages": [response]}

def should_use_tools(state: State):
    """Warunkowa krawędź: agent chce narzędzia → tool_node, inaczej → END."""
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tool_node"
    return END

# ============================================================
# 6. TERAPEUTA (bez narzędzi)
# ============================================================

def therapist_node(state: State):
    """Terapeuta — empatyczna odpowiedź bez narzędzi."""
    response = llm.invoke([
        SystemMessage(
            content="Jesteś empatycznym psychologiem. Odpowiadaj ciepło "
                    "i wspierająco. Nie używasz narzędzi — polegasz na "
                    "empatii i wiedzy terapeutycznej."
        )
    ] + state["messages"])
    return {"messages": [response]}

# ============================================================
# 7. BUDOWA GRAFU
# ============================================================

tool_node = ToolNode(tools)

builder = StateGraph(State)

# Dodaj węzły
builder.add_node("classifier", classifier_node)
builder.add_node("logical_agent", logical_agent_node)
builder.add_node("tool_node", tool_node)
builder.add_node("therapist", therapist_node)

# Krawędzie
builder.add_edge(START, "classifier")

builder.add_conditional_edges(
    "classifier",
    route_after_classifier,
    {"logical": "logical_agent", "therapist": "therapist"}
)

builder.add_conditional_edges(
    "logical_agent",
    should_use_tools,
    ["tool_node", END]
)

builder.add_edge("tool_node", "logical_agent")  # pętla ReAct
builder.add_edge("therapist", END)

# Kompilacja
app = builder.compile()
```

### Testowanie

```python
# === Test 1: Pytanie logiczne wymagające kalkulatora ===
result = app.invoke({
    "messages": [HumanMessage(content="Ile to jest 2^10 + 3^5?")]
})
print(result["messages"][-1].content)
# → "2^10 + 3^5 = 1024 + 243 = 1267"

# === Test 2: Pytanie wymagające wyszukiwania ===
result = app.invoke({
    "messages": [HumanMessage(content="Jaka jest populacja Tokio?")]
})
print(result["messages"][-1].content)
# → "Według wyszukiwania... populacja Tokio wynosi ok. 14 mln."

# === Test 3: Pytanie emocjonalne → terapeuta (bez narzędzi) ===
result = app.invoke({
    "messages": [HumanMessage(content="Czuję się bardzo samotny ostatnio.")]
})
print(result["messages"][-1].content)
# → "Rozumiem, że to trudne uczucie. Samotność..."
```

---

## `ToolNode` vs ręczny `tool_node` — kiedy co wybrać?

| Cecha | `ToolNode` (prebuilt) | Ręczny `tool_node` |
|---|---|---|
| **Prostota** | ✅ Jedna linia kodu | ❌ Wymaga napisania pętli |
| **Obsługa błędów** | ✅ Wbudowana (`handle_tool_errors=True`) | ✅ Pełna kontrola |
| **Formatowanie wyników** | Standardowe `ToolMessage` | Dowolne — można filtrować, transformować |
| **Logowanie / metryki** | Wymaga hooków | ✅ Bezpośredni dostęp |
| **Zastosowanie** | Prototypy, standardowe agenty | Produkcja z niestandardowymi wymaganiami |

```python
# ToolNode z obsługą błędów
tool_node = ToolNode(tools, handle_tool_errors=True)
# Jeśli narzędzie rzuci wyjątek, ToolNode zwróci ToolMessage
# z treścią błędu zamiast przerywać cały graf.
```

---

## Wielokrotne wywołania narzędzi w jednym kroku

Model może w jednej odpowiedzi zażądać wywołania **wielu narzędzi jednocześnie** (parallel tool calls). Zarówno `ToolNode`, jak i ręczna implementacja obsługują to automatycznie:

```python
# Model może zwrócić:
# msg.tool_calls = [
#     {'name': 'calculate', 'args': {'expression': '15 * 37'}, 'id': 'call_1'},
#     {'name': 'get_current_time', 'args': {}, 'id': 'call_2'}
# ]
# ToolNode wykona OBA narzędzia i zwróci dwa ToolMessage.
```

---

## Najczęstsze pułapki

1. **Brakujący lub niejasny docstring** — model nie wie, kiedy użyć narzędzia. Docstring to jedyny opis, jaki model widzi. Zawsze opisuj: co narzędzie robi, jakie argumenty przyjmuje i kiedy powinno być użyte.

2. **Brak `bind_tools()` przed użyciem w grafie** — jeśli model nie zna narzędzi, nigdy nie wygeneruje `tool_calls`. Agent będzie działał jak zwykły chatbot.

3. **Niezamknięta pętla ReAct** — zapomnienie o krawędzi `tool_node → agent` powoduje, że wyniki narzędzi „giną" i agent nie widzi odpowiedzi z narzędzia.

4. **Niebezpieczne narzędzia bez walidacji** — np. `eval()` w `calculate` pozwala na wykonanie dowolnego kodu Pythona. Na produkcji używaj bezpiecznych parserów (`numexpr`, `sympy`).

5. **Brak limitu iteracji pętli** — agent może wpaść w nieskończoną pętlę tool calls. Warto ustawić `recursion_limit` przy kompilacji:
   ```python
   app = builder.compile()
   result = app.invoke(
       {"messages": [HumanMessage(content="...")]},
       config={"recursion_limit": 25}  # domyślnie 25
   )
   ```

6. **Zbyt wiele narzędzi** — model z dziesiątkami narzędzi gubi się w wyborze. Preferuj specjalizowanych agentów z 3–5 narzędziami każdy (wzorzec multi-agent z routerem).

---

## `create_react_agent` — skrót dla prostych przypadków

LangGraph oferuje gotową fabrykę `create_react_agent`, która automatycznie buduje pełny graf ReAct (agent + tool_node + routing) w jednej linii:

```python
from langgraph.prebuilt import create_react_agent

agent = create_react_agent(llm, tools)
result = agent.invoke({
    "messages": [HumanMessage(content="Ile to jest 15 * 37?")]
})
```

| Kiedy użyć `create_react_agent` | Kiedy budować graf ręcznie |
|---|---|
| Proste prototypy | Wieloagentowe systemy z routerem |
| Jeden agent z kilkoma narzędziami | Niestandardowa logika routowania |
| Szybkie testy | Dodatkowe węzły (walidacja, logging) |
| Brak potrzeby custom stanu | Rozszerzony stan z dodatkowymi polami |

---

## Podsumowanie przepływu danych

```
1. HumanMessage("Ile to jest 15 * 37?")
                    │
                    ▼
2. agent_node: llm_with_tools.invoke([...messages...])
   → AIMessage(tool_calls=[{name: "calculate", args: {expression: "15*37"}}])
                    │
                    ▼
3. should_continue: tool_calls? TAK → "tool_node"
                    │
                    ▼
4. tool_node: calculate("15*37") → "555"
   → ToolMessage(content="555", tool_call_id="call_xyz")
                    │
                    ▼
5. agent_node: llm_with_tools.invoke([...messages + ToolMessage...])
   → AIMessage(content="15 × 37 = 555")
                    │
                    ▼
6. should_continue: tool_calls? NIE → END
```

---

## Powiązane pliki

- [Wzorce Multi-Agentowe (Subagents, Handoffs, Skills, Router)](langchain-multi-agent-patterns.md)
- [Wzorce projektowe systemów agentowych](wzorce-projektowe-systemow-agentowych.md)
- [Pamięć i Persistence — Checkpointers](pamiec-i-persistence-checkpointers-langgraph.md)
- [Create Agent vs ReAct Agent](create-agent-vs-react-agent.md)
- [Komunikacja z LLM w LangChain](komunikacja-z-llm-w-langchain.md)
- [Structured Output z LLM](structured-output-z-llm.md)
