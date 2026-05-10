# Middlewares w LangChain (wersje >= 1.0)

## Zwięzłe podsumowanie
**Middleware** (oprogramowanie pośredniczące) w ekosystemie LangChain (zwłaszcza w kontekście zaawansowanych architektur agentowych) to mechanizm pozwalający na precyzyjną, wielokrotnego użytku kontrolę nad pętlą wykonania agenta lub przepływem danych. Działa na zasadzie określonych "haków" (hooks), które przechwytują wywołania na poszczególnych etapach cyklu życia – np. tuż przed wywołaniem modelu, przed uruchomieniem narzędzia, bądź zaraz po otrzymaniu odpowiedzi. Pozwala to na modyfikację zachowania bez ingerencji w główny, biznesowy kod agenta.

## Dlaczego to ma znaczenie / Kiedy się to stosuje?
Tworzenie produkcyjnych agentów AI wiąże się z koniecznością obsługi tzw. aspektów przekrojowych (cross-cutting concerns), co często "zanieczyszcza" główną logikę. Middleware mityguje ten problem, ponieważ gwarantuje:
1. **Separację ról (Decoupling):** Aspekty takie jak infrastrukturalne logowanie, telemetria, zliczanie tokenów czy limity uruchomień są wydzielone poza główną pętlę rozumowania agenta.
2. **Bezpieczeństwo i Zgodność (Compliance):** Możliwość bezproblemowego zastosowania filtrów PII (danych wrażliwych), ukrywających dane zanim te dotrą do zewnętrznego API modelu LLM.
3. **Zarządzanie stanem i okna kontekstowe:** Możliwość analizy stanu (np. dynamicznego ucinania historii pamięci lub stosowania mechanizmów kompresji/podsumowywania), zanim wyczerpany zostanie limit tokenów.
4. **Human-in-the-Loop (HITL):** Zatrzymywanie wykonywania (wstrzymanie pętli wewnętrznej) przed odpaleniem przez model wrażliwego, niosącego skutki uboczne narzędzia celem zatwierdzenia przez człowieka.
5. **Niezawodność (Reliability):** Rozszerzone mechanizmy ponawiania żądań (retry) przy błędach parsowania struktury czy odpowiedzi z serwera.

## Jak to działa (Koncepcje i zastosowanie)

Architektura middleware opiera się na umieszczaniu nasłuchiwaczy (lub podklas `AgentMiddleware`) wokół agenta, interweniując m.in. zdefiniowanymi metodami (hookami):

*   `before_agent`: Uruchamiany raz podczas startu iteracji agenta (np. celem walidacji struktury danych wejściowych).
*   `before_model`: Metoda inicjowana bezpośrednio przed requestem do LLM (idealna do wstrzykiwania ukrytych promptów w konkretnym etapie, lub cenzurowania).
*   `modify_model_request`: Parametryzacja samego requesta – np. ukrycie konkretnych narzędzi gdy stan aplikacji zabrania na ich użycie na tym etapie.
*   `wrap_model_call`: Oplata właściwy request asynchroniczny, w naturalny sposób adaptuje mechanizmy cache i fallback.
*   `wrap_tool_call`: Oplata wywołanie narzędzi zdefiniowanych przez użytkownika (HITL, śledzenie czasu trwania).
*   `after_model` / `after_agent`: Uruchamiane do zewaluowania efektów (np. auto-poprawianie parsera kiedy wygeneruje "uszkodzony" wynik).

### Predefiniowane Middleware'y
Biblioteka dostarcza gotowych, powtarzalnych adapterów rozwiązujących trywialne problemy na etapie przechodzenia z wersji PoC na Produkcję:
*   `PIIMiddleware` – Zabezpiecza prywatność danych.
*   `ModelCallLimitMiddleware` oraz `ToolCallLimitMiddleware` – Kluczowa bramka zatrzymująca tzw. nieskończone pętle halucynacji narzędziowych.
*   `HumanInTheLoopMiddleware` – Wstrzymanie dla ludzkiej kontroli i aprobaty.
*   `SummarizationMiddleware` – Zapobieganie błędom _Max Context Window_.

### Przykład gotowego Middleware (Human-in-the-Loop)

Poniższy kod przedstawia wbudowany w LangChain komponent `HumanInTheLoopMiddleware`:

```python
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langgraph.checkpoint.memory import InMemorySaver

def read_email_tool(email_id: str) -> str:
    """Mock function to read an email by its ID."""
    return f"Email content for ID: {email_id}"

def send_email_tool(recipient: str, subject: str, body: str) -> str:
    """Mock function to send an email."""
    return f"Email sent to {recipient} with subject '{subject}'"

agent = create_agent(
    model="gpt-4o",
    tools=[read_email_tool, send_email_tool],
    checkpointer=InMemorySaver(),
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={
                "send_email_tool": {
                    "allowed_decisions": ["approve", "edit", "reject"],
                },
                "read_email_tool": False,
            }
        ),
    ],
)
```

**Gdzie tutaj są zdefiniowane hooki (`before_model`, `after_model` itp.)?**
W powyższym przykładzie powiązań z konkretnym etapem **nie widać**. Wynika to z faktu, że używamy gotowej, wbudowanej klasy (`HumanInTheLoopMiddleware`). Kod określający moment ingerencji w pętlę agenta (w tym przypadku logicznie zlokalizowany na etapie `wrap_tool_call`, z uwagi na wstrzymywanie wywoływań konkretnych narzędzi) jest ukryty **w implementacji tej klasy w bibliotece LangChain**. Jako programista dostarczasz do niej jedynie predykaty konfiguracyjne (jak `interrupt_on`).

**Jak określa się KIEDY człowiek musi interweniować?**
Kluczowe w zrozumieniu `HumanInTheLoopMiddleware` jest to, że nie określasz przerw na podstawie kolejności (np. po 4 przebiegach pętli). Zamiast tego reagujesz **zawsze w momencie próby wywołania sklasyfikowanego narzędzia (Tool)**. 

Zatem jeśli ustawisz w jego konfiguracji `interrupt_on={"send_email_tool": ...}` oznacza to w logicznym ujęciu procedury: *"Zrób kroki 1, 2, 3 samodzielnie używając bezpiecznych narzędzi czy wymiany informacji... ALE GDY w końcu dojdziesz do wniosku, że dla zrealizowania mojego zadania celowe jest uruchomienie tego niebezpiecznego narzędzia (`send_email_tool`), zapisz i zamroź swój stan, a następnie poproś mnie o zgodę."*

**Pełny przepływ w kodzie (Wstrzymanie i Wznowienie):**
Kiedy model używa toola `send_email_tool`, middleware zgłasza żądanie Interrupt, a checkpointer zrzuca ten stan do pamięci podręcznej (np. `InMemorySaver`). Skrypt (pętla) kończy strumieniowanie i serwer zostaje zwolniony. Kiedy użytkownik dokona akceptacji w interfejsie przeglądarki, powracamy do skryptu i wysyłamy modelowi instrukcję wznawiającą podając poprzednie kody wątku:

```python
from langgraph.types import Command

# 1. Startujemy nową sesję (dzięki temu checkpointer wie, jak powiązać kroki w obrębie zadania)
thread_config = {"configurable": {"thread_id": "sesja_raportowania_1"}}

print("--- URUCHAMIAMY AGENTA ---")
# Agent rusza - robi kroki 1, 2, 3 (np. czytając wiadomości z ID używając read_email_tool) bez ingerencji programu...
for chunk in agent.stream(
    {"messages": [("user", "Przeczytaj emaile i jeśli to konieczne użyj toola by wysłać odpowiedź.")]}, 
    config=thread_config
):
    print("Log aktywności Agenta:", chunk)

# 2. Powyższa pętla zostaje porzucona, gdy middleware napotka na swoim etapie chronione 
# narzędzie `send_email_tool` i wymusi przerwanie wykonania (Interrupt).
# Pobieramy stan z checkpointera:
state = agent.get_state(thread_config)

if state.next:
    # W state.next znajduje się informacja, że algorytm jest uziemiony z powodu interwencji
    print(f"\\n[!] AGENT ZATRZYMANY: Czeka na interwencję. Zatrzymano przed: {state.next}")
    
    # 3. INTERWENCJA CZŁOWIEKA (Użytkownik np. po kilku godzinach loguje się do systemu webowego,
    # aktywuje odpowiedni endpoint API przekazując mu: "approve" dla danej sesji).
    user_action = "approve" 
    
    # 4. WZNAWIAMY SESJĘ AGENTA
    print("\\n--- WZNAWIAMY PRACĘ (RESUME) ---")
    
    # W strumieniu jako argument początkowy podajemy dedykowaną komendę `Command(resume=...)` 
    # WSKAZUJĄC tę samą konfigurację thread_config co początkowo, 
    # aby LangChain wiedział wczorajszą historię zadania.
    for chunk in agent.stream(
        Command(resume={"action": user_action}), 
        config=thread_config
    ):
        print("Log zakończenia pracy:", chunk)
```

Jeśli chcesz samodzielnie wskazać, że Twoja logika ma reagować precyzyjnie na etapie `before_model` lub `after_model`, powinieneś stworzyć autorską logikę poprzez dziedziczenie (co ilustruje przykład poniżej):

### Przykład kodu własnego (Custom Middleware)

Poniżej można zauważyć jak wygląda wysoce modularna konfiguracja implementacji:

```python
from my_agent_framework import create_agent, AgentMiddleware
from my_agent_framework.middlewares import PIIMiddleware, ModelCallLimitMiddleware

# 1. Definicja własnego, niestandardowego Middleware
class AuditLoggingMiddleware(AgentMiddleware):
    def before_model(self, state, request):
        print(f"[AUDIT] Wysyłam zapytanie do LLM. Ilość wiaddomości: {len(request.messages)}")
        # Mamy możliwość modyfikacji requesta modyfikując ten obiekt
        return request
        
    def after_model(self, state, response):
        print(f"[AUDIT] Otrzymano odpowiedź, zużyto tokenów: {response.token_usage}")
        return response

# 2. Definicja agenta bazującego na warstwach middleware
agent = create_agent(
    model="gpt-4",
    tools=[search_tool, database_update_tool],
    middlewares=[
        # Kolejność zazwyczaj ma polegać na strukturze cebuli (od najniższej do najwyższej warstwy)
        PIIMiddleware(sensitive_fields=["pesel", "credit_card"]), 
        ModelCallLimitMiddleware(max_iterations=5),
        AuditLoggingMiddleware()
    ]
)

# Podczas działania agenta wszystkie pośredniczące instrukcje wykonają się bezszelestnie, 
# a kod biznesowy będzie "czysty".
response = agent.invoke({"input": "Zapłać rachunek Janka z użyciem karty X."})
```

Alternatywne implementacje nowszego ekosystemu w rdzeniu (LangGraph oraz uogólnione LCEL) osiągają analogiczne procesy poprzez konfigurację dedykowanych węzłów nadzorujących stan (w *StateGraphs*) i wykorzystanie np. wbudowanych metod interceptorów takich jak `.with_listeners()`, `.with_fallbacks()` lub zdarzeń (callbacks system) w starszej iteracji łańcuchów.

## Zobacz powiązane
- [Komponenty ekosystemu Langchain](komponenty-ekosystemu-langchain.md)
- [Komunikacja z LLM w Langchain](komunikacja-z-llm-w-langchain.md)
- [Wzorce projektowe systemów agentowych](wzorce-projektowe-systemow-agentowych.md)
