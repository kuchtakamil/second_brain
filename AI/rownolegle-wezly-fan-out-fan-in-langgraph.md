# Równoległe węzły (Fan-out / Fan-in) w LangGraph

## Krótki opis

LangGraph (≥ 1.0) umożliwia **równoległe uruchamianie wielu węzłów** w ramach jednego kroku obliczeniowego (superstep). Dwa kluczowe wzorce:

- **Fan-out** — jeden węzeł rozgałęzia przepływ do wielu węzłów wykonywanych jednocześnie.
- **Fan-in** — wiele równoległych węzłów łączy swoje wyniki w jednym węźle agregującym.

Równoległość wymaga **reducerów** — funkcji definiujących sposób łączenia wyników z wielu węzłów zapisujących do tego samego klucza stanu. Bez reducera próba zapisu do tego samego klucza z wielu równoległych węzłów kończy się błędem `InvalidUpdateError`.

## Dlaczego to ważne / Kiedy stosować?

- **Skrócenie czasu odpowiedzi** — zamiast wywoływać agentów sekwencyjnie, uruchamiamy ich równolegle (np. 2 agenty po 3s = 3s zamiast 6s).
- **Multi-perspektywa** — jedno zapytanie analizowane z wielu punktów widzenia (emocjonalny + logiczny, techniczny + biznesowy) daje bogatszą odpowiedź.
- **Map-Reduce** — przetwarzanie wielu elementów tym samym węzłem równolegle (np. streszczanie 10 dokumentów jednocześnie).
- **Separacja logiki** — każdy agent ma własny system prompt i opcjonalnie własne narzędzia, a synthesizer scala wyniki w spójną odpowiedź.

---

## Mechanizm działania: Supersteps

LangGraph opiera się na modelu obliczeniowym zainspirowanym [Pregel](https://research.google/pubs/pregel-a-system-for-large-scale-graph-processing/). Wykonanie grafu składa się z serii **superstepów**:

1. W ramach jednego superstepu wszystkie aktywne węzły uruchamiają się **równolegle**.
2. Graf **czeka** na zakończenie wszystkich węzłów w superstepie.
3. Wyniki z węzłów są **łączone** za pomocą reducerów i zapisywane do stanu.
4. Następny superstep rozpoczyna kolejne węzły wyznaczone przez krawędzie.

```
Superstep 1: classifier
Superstep 2: therapist + logical  ← równoległe
Superstep 3: synthesizer
```

---

## Dwa sposoby fan-out

### 1. Statyczny fan-out (`add_edge`)

Znany w czasie budowania grafu. Dodajemy wiele krawędzi z jednego węzła:

```python
builder.add_edge("classifier", "therapist")
builder.add_edge("classifier", "logical")
```

LangGraph automatycznie uruchomi `therapist` i `logical` w tym samym superstepie.

**Fan-in** — oba węzły prowadzą do tego samego węzła docelowego:

```python
builder.add_edge("therapist", "synthesizer")
builder.add_edge("logical", "synthesizer")
```

`synthesizer` uruchomi się dopiero po zakończeniu obu gałęzi.

### 2. Dynamiczny fan-out (`Send`)

Liczba i wybór równoległych węzłów ustalany **w runtime** na podstawie stanu. Używamy `Send` z `langgraph.types`:

```python
from langgraph.types import Send

def fan_out_to_agents(state: State):
    """Warunkowa krawędź zwracająca listę Send — uruchomi węzły równolegle."""
    return [
        Send("therapist", state),
        Send("logical", state),
    ]

builder.add_conditional_edges("classifier", fan_out_to_agents)
```

Każdy obiekt `Send(node_name, payload)` tworzy niezależne wywołanie węzła z podanym stanem. Pozwala to na:
- dynamiczne wybieranie, które węzły uruchomić
- przekazywanie różnych danych do każdego węzła
- skalowanie do dowolnej liczby gałęzi

---

## Reducery — agregacja wyników z równoległych węzłów

### Problem

Gdy dwa węzły równolegle zwracają aktualizację tego samego klucza stanu, LangGraph nie wie, który wynik zachować. Domyślny reducer **nadpisuje** wartość — przy równoległych zapisach to błąd.

### Rozwiązanie: `Annotated` z funkcją reducera

```python
import operator
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[list, add_messages]      # reducer dla wiadomości
    responses: Annotated[list, operator.add]      # reducer: konkatenacja list
```

| Reducer | Zachowanie | Zastosowanie |
|---|---|---|
| `operator.add` | Konkatenuje listy: `[A] + [B] = [A, B]` | Zbieranie wyników z równoległych węzłów |
| `add_messages` | Inteligentne łączenie wiadomości (deduplikacja po ID) | Klucz `messages` w agentach konwersacyjnych |
| Własna funkcja | Dowolna logika: np. `max`, `merge dict`, walidacja | Niestandardowe scenariusze |

### Własna funkcja reducera

```python
def merge_dicts(existing: dict, new: dict) -> dict:
    """Reducer łączący słowniki — nowe klucze nadpisują stare."""
    return {**existing, **new}

class State(TypedDict):
    metadata: Annotated[dict, merge_dicts]
```

### Kluczowa zasada

Jeśli klucz stanu jest zapisywany przez **więcej niż jeden równoległy węzeł**, **musi** mieć reducer. W przeciwnym razie: `InvalidUpdateError`.

---

## Pełny scenariusz: classifier → [therapist, logical] → synthesizer

### Wzorzec grafu

```
START → classifier → therapist   ──┐
                   → logical     ──┤ (równolegle, superstep 2)
                                   └→ synthesizer → END
```

### Implementacja

```python
import operator
from typing import Annotated, Literal
from typing_extensions import TypedDict
from pydantic import BaseModel, Field

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

# ============================================================
# 1. STAN Z WŁASNYM REDUCEREM
# ============================================================

class State(TypedDict):
    messages: Annotated[list, add_messages]
    responses: Annotated[list, operator.add]  # agreguje odpowiedzi z obu agentów

# ============================================================
# 2. MODEL
# ============================================================

llm = ChatOpenAI(model="gpt-4o")

# ============================================================
# 3. CLASSIFIER — klasyfikuje intencję (nie routuje, bo oba agenty
#    zawsze odpowiadają równolegle)
# ============================================================

def classifier_node(state: State):
    """Przygotowuje kontekst klasyfikacji — tutaj przepuszcza wiadomość dalej.
    W złożonym scenariuszu można dodać preprocessing (wykrywanie języka,
    ekstrakcja słów kluczowych itp.)."""
    return {"messages": state["messages"]}

# ============================================================
# 4. TERAPEUTA — empatyczna odpowiedź
# ============================================================

def therapist_node(state: State):
    """Agent empatyczny — odpowiada z perspektywy emocjonalnej."""
    response = llm.invoke([
        SystemMessage(
            content="Jesteś empatycznym psychologiem. Odpowiadaj ciepło, "
                    "z troską i zrozumieniem. Skup się na emocjach i wsparciu. "
                    "Odpowiedź sformułuj w 2-3 zdaniach."
        )
    ] + state["messages"])
    return {"responses": [{"agent": "therapist", "content": response.content}]}

# ============================================================
# 5. AGENT LOGICZNY — analityczna odpowiedź
# ============================================================

def logical_node(state: State):
    """Agent analityczny — odpowiada z perspektywy logicznej i faktograficznej."""
    response = llm.invoke([
        SystemMessage(
            content="Jesteś precyzyjnym analitykiem. Odpowiadaj rzeczowo, "
                    "z faktami i konkretnymi poradami. "
                    "Odpowiedź sformułuj w 2-3 zdaniach."
        )
    ] + state["messages"])
    return {"responses": [{"agent": "logical", "content": response.content}]}

# ============================================================
# 6. SYNTHESIZER — scala odpowiedzi obu agentów
# ============================================================

def synthesizer_node(state: State):
    """Scala odpowiedzi z obu agentów w jedną spójną odpowiedź."""
    responses_text = "\n\n".join(
        f"[{r['agent']}]: {r['content']}" for r in state["responses"]
    )
    response = llm.invoke([
        SystemMessage(
            content="Masz odpowiedzi dwóch ekspertów na pytanie użytkownika. "
                    "Połącz je w jedną spójną, zbalansowaną odpowiedź, "
                    "uwzględniając zarówno perspektywę emocjonalną, "
                    "jak i logiczną. Nie cytuj ekspertów z nazwy."
        ),
        HumanMessage(content=responses_text)
    ])
    return {"messages": [response]}

# ============================================================
# 7. BUDOWA GRAFU
# ============================================================

builder = StateGraph(State)

# Dodaj węzły
builder.add_node("classifier", classifier_node)
builder.add_node("therapist", therapist_node)
builder.add_node("logical", logical_node)
builder.add_node("synthesizer", synthesizer_node)

# Krawędzie
builder.add_edge(START, "classifier")

# Fan-out: classifier → [therapist, logical] (równolegle)
builder.add_edge("classifier", "therapist")
builder.add_edge("classifier", "logical")

# Fan-in: [therapist, logical] → synthesizer
builder.add_edge("therapist", "synthesizer")
builder.add_edge("logical", "synthesizer")

builder.add_edge("synthesizer", END)

# Kompilacja
app = builder.compile()
```

### Uruchomienie

```python
result = app.invoke({
    "messages": [HumanMessage(content="Czuję się przytłoczony pracą i nie wiem jak to ogarnąć.")],
    "responses": []
})

print(result["messages"][-1].content)
# → Zbalansowana odpowiedź łącząca empatię z konkretnymi radami
```

### Przepływ danych krok po kroku

```
1. HumanMessage → classifier
   Stan: messages=[HumanMessage], responses=[]

2. classifier → [therapist, logical]  ← SUPERSTEP (równoległe)
   therapist zwraca: {"responses": [{"agent": "therapist", "content": "..."}]}
   logical   zwraca: {"responses": [{"agent": "logical",   "content": "..."}]}
   
   Reducer operator.add łączy: responses = [therapist_resp, logical_resp]

3. synthesizer ← odbiera stan z pełną listą responses
   Generuje scalony AIMessage → dopisuje do messages

4. END
```

---

## Dynamiczny fan-out z `Send` — wariant z wyborem agentów w runtime

Gdy nie zawsze chcemy uruchamiać obu agentów, używamy `Send`:

```python
from langgraph.types import Send

def dynamic_fan_out(state: State):
    """Dynamicznie decyduje, które agenty uruchomić."""
    agents = []
    
    # Logika decyzyjna — np. na podstawie klasyfikacji
    user_msg = state["messages"][-1].content.lower()
    
    # Zawsze uruchom logicznego
    agents.append(Send("logical", state))
    
    # Terapeutę tylko gdy wykryto emocje
    emotional_keywords = ["czuję", "smutek", "stres", "lęk", "samotny"]
    if any(kw in user_msg for kw in emotional_keywords):
        agents.append(Send("therapist", state))
    
    return agents

# Zastąp statyczne krawędzie fan-out:
builder.add_conditional_edges("classifier", dynamic_fan_out)
```

---

## Map-Reduce: ten sam węzeł, wiele instancji

`Send` pozwala uruchomić **ten sam węzeł wielokrotnie** z różnymi danymi — klasyczny wzorzec Map-Reduce:

```python
from langgraph.types import Send

class OverallState(TypedDict):
    subjects: list[str]
    summaries: Annotated[list[str], operator.add]

def generate_summary(state: dict):
    """Generuje streszczenie jednego tematu."""
    subject = state["subject"]
    response = llm.invoke([
        HumanMessage(content=f"Napisz streszczenie na temat: {subject}")
    ])
    return {"summaries": [response.content]}

def map_subjects(state: OverallState):
    """Fan-out: dla każdego tematu uruchom osobny węzeł."""
    return [Send("generate_summary", {"subject": s}) for s in state["subjects"]]

builder = StateGraph(OverallState)
builder.add_node("generate_summary", generate_summary)
builder.add_conditional_edges(START, map_subjects)
builder.add_edge("generate_summary", END)

graph = builder.compile()

result = graph.invoke({
    "subjects": ["Python", "Rust", "Go"],
    "summaries": []
})
# result["summaries"] → [streszczenie_python, streszczenie_rust, streszczenie_go]
```

---

## Kontrola współbieżności

Przy wielu równoległych wywołaniach LLM warto ograniczyć współbieżność, by nie przekroczyć limitów API:

```python
result = app.invoke(
    {"messages": [HumanMessage(content="...")]},
    config={"max_concurrency": 3}  # maks. 3 węzły jednocześnie
)
```

---

## Najczęstsze pułapki

1. **Brak reducera przy równoległym zapisie** — dwa węzły piszą do tego samego klucza bez reducera → `InvalidUpdateError`. Zawsze używaj `Annotated[list, operator.add]` lub innego reducera.

2. **Nadpisywanie wartości skalarnych** — `Annotated[str, ...]` nie ma sensu z `operator.add` (skleja stringi). Dla skalarów używaj listy z reducerem i agreguj w synthesizer.

3. **Inicjalizacja stanu** — klucze z reducerem wymagają wartości początkowej przy `invoke`. Dla `operator.add` podaj pustą listę: `{"responses": []}`.

4. **Niedeterministyczna kolejność** — wyniki z równoległych węzłów mogą trafiać do listy w dowolnej kolejności. Jeśli kolejność ma znaczenie, dodaj timestamp lub indeks w danych i sortuj w synthesizer.

5. **Brak fan-in** — zapomnienie o krawędziach z gałęzi do węzła agregującego powoduje, że graf kończy się przedwcześnie lub synthesizer nie otrzymuje wszystkich wyników.

---

## Podsumowanie wzorców

| Wzorzec | Mechanizm | Kiedy użyć |
|---|---|---|
| **Statyczny fan-out** | `add_edge` z jednego węzła do wielu | Stała, znana liczba gałęzi |
| **Dynamiczny fan-out** | `Send` w `add_conditional_edges` | Liczba/wybór gałęzi zależy od danych |
| **Map-Reduce** | `Send` do tego samego węzła wielokrotnie | Przetwarzanie listy elementów tym samym kodem |
| **Fan-in** | `add_edge` z wielu węzłów do jednego + reducer | Zawsze potrzebny przy fan-out |

---

## Powiązane pliki

- [Narzędzia dla agentów (Tool Use)](narzedzia-dla-agentow-tool-use-langgraph.md)
- [Wzorce Multi-Agentowe (Subagents, Handoffs, Skills, Router)](langchain-multi-agent-patterns.md)
- [Wzorce projektowe systemów agentowych](wzorce-projektowe-systemow-agentowych.md)
- [Pamięć i Persistence — Checkpointers](pamiec-i-persistence-checkpointers-langgraph.md)
- [Create Agent vs ReAct Agent](create-agent-vs-react-agent.md)
