# Projektowanie memory management oraz session handling dla agentów AI

Zarządzanie pamięcią (Memory Management) i obsługa sesji (Session Handling) to kluczowe elementy w architekturze zaawansowanych systemów opartych o agentów AI (np. budowanych w oparciu o LangGraph czy LangChain). Decydują one o tym, jak agent przechowuje kontekst rozmowy w krótkim i długim czasie, co bezpośrednio wpływa na jego użyteczność, koszt (zużycie tokenów) i spójność działania.

## Dlaczego jest to ważne?

1. **Limit tokenów (Context Window)**: Modele LLM mają ograniczoną pojemność kontekstu, którą mogą przetworzyć na raz. Bez efektywnego zarządzania pamięcią długa rozmowa doprowadzi do błędu lub znacznego spowolnienia oraz wzrostu kosztów.
2. **Zachowanie stanu**: Agenty rozwiązujące skomplikowane problemy (np. [Multi-Agent Supervisor](multi-agent-supervisor-langgraph.md)) potrzebują śledzić swój postęp krok po kroku oraz wiedzieć, na jakim etapie znajduje się wykonanie zadania.
3. **Personalizacja (Long-Term Memory)**: Zdolność do przypomnienia sobie faktów o użytkowniku z poprzednich sesji, oddalonych w czasie o dni lub tygodnie, znacząco podnosi odczucia z użytkowania (UX).

## Session Handling (Pamięć Krótkoterminowa)

Obsługa sesji skupia się na bieżącym przebiegu konwersacji (tzw. _Short-Term Memory_). To w tym obszarze działają mechanizmy takie jak przekazywanie historii czatu wraz z bieżącym zapytaniem.

### Jak to działa?

W nowoczesnych rozwiązaniach agentowych, takich jak LangGraph, używa się **Checkpointerów** (np. `SqliteSaver`, `PostgresSaver`), które na bieżąco zapisują stan całego grafu pod konkretnym `thread_id` (identyfikatorem sesji). Umożliwia to m.in. pauzowanie agenta, czekanie na interakcję człowieka, i wznawianie pracy od tego samego miejsca.

```python
from langgraph.checkpoint.sqlite import SqliteSaver

# Inicjalizacja checkpointera do śledzenia sesji
memory = SqliteSaver.from_conn_string(":memory:")

# Uruchomienie agenta w kontekście konkretnego wątku (sesji)
config = {"configurable": {"thread_id": "sesja_123"}}
response = graph.invoke(input_state, config=config)
```

Warto zapoznać się z plikami powiązanymi: [Persistence i Checkpointers w LangGraph](persistence-sqlite-postgres-langgraph.md) oraz [Chat History](chat-history-langchain-langgraph.md).

## Memory Management (Pamięć Długoterminowa)

Pamięć długoterminowa (_Long-Term Memory_) to zapisywanie i odzyskiwanie informacji z odległej przeszłości. Zamiast wrzucać do promptu całą historię interakcji użytkownika (co jest nieoptymalne), agent ekstrahuje kluczowe fakty i zapisuje je na zewnątrz, najczęściej w **wektorowej bazie danych** lub w grafie wiedzy.

### Wzorce zarządzania pamięcią długoterminową:

1. **Windowing / Truncation**: Ucinanie starszych wiadomości w bieżącej sesji, zachowując w kontekście tylko $N$ ostatnich interakcji.
2. **Summarization**: Gdy bufor wiadomości staje się zbyt duży, dedykowany krok w procesie (lub mniejszy, tańszy LLM) generuje podsumowanie dotychczasowej rozmowy. Zmniejsza to liczbę tokenów, ale może powodować gubienie drobnych detali.
3. **RAG (Retrieval-Augmented Generation)**: Wyciągnięte informacje, fakty i dokumenty zapisywane są jako wektory (np. w Qdrant, Pinecone). Przy nowym zapytaniu system wyszukuje semantycznie powiązane wpisy i wstrzykuje je do promptu. Zobacz: [Baza Wektorowa vs LLM](baza-wektorowa-vs-llm.md).
4. **Ekstrakcja encji (Entity Memory)**: Specjalistyczne mechanizmy lub gotowe usługi (np. Mem0, Zep) służące do wyciągania z konwersacji twardych faktów (np. "Użytkownik lubi kolor niebieski", "Użytkownik programuje w Pythonie od 10 lat") i strukturyzowania ich jako globalny profil użytkownika.

### Przykładowy przepływ z hybrydową pamięcią:

1. Użytkownik wysyła wiadomość.
2. System pobiera `thread_id` (Session Handling) dla wybranego wątku z bazy relacyjnej.
3. System wyszukuje w bazie wektorowej (Long-Term Memory) powiązane fakty o użytkowniku.
4. Agent otrzymuje prompt składający się z: *Instrukcji systemowej* + *Wyciągniętych historycznych faktów* + *Ostatnich N wiadomości z bieżącej sesji* + *Bieżącego zapytania*.

## Podsumowanie

Dobrze zaprojektowany system agentowy używa hybrydowego podejścia:
- **Checkpointerów / relacyjnych baz danych** (dla sesji, pamięci roboczej i śledzenia stanu kroków w grafie),
- **Bazy wektorowej / grafów wiedzy** (dla trwałego zachowywania istotnych faktów i dokumentów między sesjami),
- **Mechanizmów optymalizacji kontekstu** (Summary, Windowing) w celu rygorystycznej kontroli kosztów zużycia tokenów LLM.

Więcej na ten temat znajdziesz w dokumencie: [Pamięć i Persistence Checkpointers LangGraph](pamiec-i-persistence-checkpointers-langgraph.md) oraz [Pamięć długoterminowa AI](pamięć-długoterminowa-ai.md).
