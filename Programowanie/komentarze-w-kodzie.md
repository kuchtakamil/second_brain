# Komentarze w kodzie

**Data:** 2025-09-12

---

**User:**

w projekcie ze szkolenia z lang graph mam fragment kodu
from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END
from langgraph.graph import MessagesState
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition

# Node
def tool_calling_llm(state: MessagesState):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

# Build graph
builder = StateGraph(MessagesState)
builder.add_node("tool_calling_llm", tool_calling_llm)
builder.add_node("tools", ToolNode([multiply]))
builder.add_edge(START, "tool_calling_llm")
builder.add_conditional_edges(
    "tool_calling_llm",
    # If the latest message (result) from assistant is a tool call -> tools_condition routes to tools
    # If the latest message (result) from assistant is a not a tool call -> tools_condition routes to END
    tools_condition,
)
builder.add_edge("tools", END)
graph = builder.compile()

# View
display(Image(graph.get_graph().draw_mermaid_png()))

czy te komentarze 
If the latest message (result) from assistant is a tool call -> tools_condition routes to tools
również mają znaczenie dla działąnia aplikacji?

---

**Assistant:**

Nie – te komentarze **nie mają żadnego wpływu na działanie aplikacji**.  

Python ignoruje komentarze (wszystko po `#` w danej linii). W Twoim przykładzie:  

```python
# If the latest message (result) from assistant is a tool call -> tools_condition routes to tools
# If the latest message (result) from assistant is a not a tool call -> tools_condition routes to END
```

to tylko opis tego, co robi przekazana funkcja `tools_condition` w `builder.add_conditional_edges(...)`.  
Logika działania jest wyłącznie w kodzie – w tym przypadku w funkcji `tools_condition` oraz w konfiguracji krawędzi grafu.  

Komentarze służą wyłącznie dla czytelności i dokumentacji kodu. Możesz je usunąć albo zmienić, a aplikacja zadziała tak samo.  

Chcesz, żebym Ci dokładnie wyjaśnił, jak działa `tools_condition` w tym przykładzie?