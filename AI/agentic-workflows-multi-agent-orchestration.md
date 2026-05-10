# Aspekty techniczne: Agentic Workflows i Multi-Agent Orchestration

Ten dokument wyjaśnia kluczowe zagadnienia techniczne, koncepcje oraz wzorce, które należy poznać, aby skutecznie budować systemy oparte na jednym agencie (Agentic Workflows) oraz orkiestrować współpracę wielu agentów (Multi-Agent Orchestration).

## 1. Agentic Workflows (Jak działa agent)

Wzorzec pojedynczego agenta opiera się na tym, że model językowy (LLM) steruje przebiegiem aplikacji: analizuje wejście, decyduje o kolejnych krokach, używa narzędzi i zwraca wynik. Aby to osiągnąć w środowisku produkcyjnym, należy opanować następujące aspekty:

### A. Pętla ReAct (Reasoning and Acting)
Zrozumienie, w jaki sposób agent łączy "myślenie" z "działaniem".
* **Koncepcja:** Agent otrzymuje prompt, generuje myśli (Thought), wybiera narzędzie (Action), wykonuje je, otrzymuje wynik (Observation) i kontynuuje pętlę.
* **Technikalia:** Implementacja tej pętli, radzenie sobie z sytuacjami, gdy agent utknie w nieskończonej pętli (ustawianie `recursion_limit`).
* **Powiązane:** [Create Agent vs ReAct Agent](create-agent-vs-react-agent.md)

### B. Wykorzystanie narzędzi (Tool Calling / Function Calling)
To fundament każdego agenta pozwalający na interakcję ze światem zewnętrznym.
* **Koncepcja:** Wiązanie (binding) schematów narzędzi z modelem LLM.
* **Technikalia:** Oznaczanie funkcji za pomocą dekoratorów (np. `@tool`), parsowanie argumentów zwracanych przez model (JSON Schema), obsługa błędów narzędzi (gdy model wygeneruje nieprawidłowe argumenty).
* **Powiązane:** [Narzędzia dla agentów (Tool Use)](narzedzia-dla-agentow-tool-use-langgraph.md)

### C. Zarządzanie stanem i Checkpointing (Persistence)
Agent musi pamiętać kontekst rozmowy i kroki, które już wykonał.
* **Koncepcja:** Pamięć krótkoterminowa i długoterminowa.
* **Technikalia:** Konfiguracja checkpointerów (np. SQLite, Postgres w LangGraph), zapisywanie stanu po każdym przejściu węzła (node), zarządzanie `thread_id` dla wielu równoległych konwersacji.
* **Powiązane:** [Pamięć i Persistence Checkpointers](pamiec-i-persistence-checkpointers-langgraph.md)

### D. Human-in-the-Loop (HITL)
Możliwość wstrzymania działania agenta w celu uzyskania akceptacji od człowieka (np. przed wykonaniem krytycznej akcji jak wysłanie przelewu).
* **Koncepcja:** Przerwania statyczne przed/po wykonaniu węzła oraz przerwania dynamiczne wewnątrz funkcji.
* **Technikalia:** Wykorzystywanie funkcji `interrupt()` do zawieszenia stanu, modyfikowanie stanu w locie przez człowieka i wznawianie grafu przy użyciu obiektu `Command(resume=...)`.
* **Powiązane:** [Interrupts w LangGraph](interrupts-langgraph.md)

### E. Ustrukturyzowane wyjście (Structured Outputs)
* **Koncepcja:** Zmuszenie agenta, aby na końcu swojego działania zwrócił wynik w przewidywalnym formacie.
* **Technikalia:** Użycie Pydantic do zdefiniowania schematu, metoda `with_structured_output`, ew. wykorzystanie parserów wyjścia (Output Parsers).
* **Powiązane:** [Structured Output z LLM](structured-output-z-llm.md)

---

## 2. Multi-Agent Orchestration (Jak wiele agentów współpracuje)

Gdy zadanie jest zbyt skomplikowane dla jednego agenta, dzielimy je na mniejszych specjalistów. Wymaga to jednak orkiestracji, aby agenci skutecznie komunikowali się i nie nadpisywali swoich wyników.

### A. Routing i Krawędzie Warunkowe (Conditional Edges)
* **Koncepcja:** Decydowanie, "co ma się wykonać dalej" na podstawie wyniku poprzedniego agenta.
* **Technikalia:** Budowanie grafów skierowanych (np. w LangGraph). Implementacja funkcji decyzyjnych w krawędziach warunkowych, które czytają aktualny stan i decydują o następnym węźle docelowym.

### B. Wzorzec Supervisor
* **Koncepcja:** Centralny agent-zarządca deleguje zadania do agentów-pracowników (Workers), ale to on zawsze podejmuje ostateczną decyzję o zakończeniu pracy.
* **Technikalia:** Zdefiniowanie grafu, gdzie Supervisor wymusza powrót z workerów do siebie. Nauka, jak instruować Supervisora, jakimi narzędziami są agenci podrzędni.
* **Powiązane:** [Multi-Agent Supervisor w LangGraph](multi-agent-supervisor-langgraph.md)

### C. Zrównoleglenie zadań (Fan-out / Fan-in)
* **Koncepcja:** Wykonywanie wielu zadań przez różnych agentów jednocześnie (np. agent tłumaczący na francuski i agent tłumaczący na niemiecki działają w tym samym czasie).
* **Technikalia:** Mapowanie po liście (API `Send` w LangGraph), uruchamianie równoległych węzłów i pisanie własnych reducerów, które łączą wyniki w jeden spójny stan grafu.
* **Powiązane:** [Równoległe Węzły (Fan-out / Fan-in)](rownolegle-wezly-fan-out-fan-in-langgraph.md)

### D. Przekazywanie kontroli (Handoffs)
* **Koncepcja:** Agent bezpośrednio przekazuje pałeczkę innemu agentowi (np. agent wsparcia przekazuje rozmowę do agenta działu rozliczeń).
* **Technikalia:** W nowoczesnych frameworkach robi się to m.in. za pomocą ustrukturyzowanych narzędzi lub obiektów takich jak `Command(goto="billing_agent")`, gdzie aktualizuje się stan i natychmiast wywołuje odpowiedni węzeł.

### E. Współdzielony vs Lokalny Stan (Shared vs Local State)
* **Koncepcja:** Zrozumienie, do jakich informacji poszczególni agenci powinni mieć dostęp.
* **Technikalia:** Definiowanie głównych kanałów wiadomości (np. globalna tablica wyników dla całego zespołu) i kanałów prywatnych (np. "brudnopis" (scratchpad), z którego korzysta tylko jeden agent i nie udostępnia go innym).

---

## Podsumowanie i od czego zacząć
1. Rozpocznij od nauki **Tool Calling**, jako że to podstawa sprawczości (agency) LLMów.
2. Skonstruuj własnego agenta **ReAct**, aby zrozumieć, jak model przetwarza zapytania iteracyjnie.
3. Gdy natrafisz na ograniczenia jednego modelu (np. zapominanie kontekstu), przejdź do budowy architektury **Supervisor** i zapoznaj się z **zarządzaniem stanem (Checkpointers)** w frameworkach takich jak LangGraph.
