# Projektowanie memory management oraz session handling dla agentów AI

Projektowanie systemów pamięci (memory management) oraz obsługi sesji (session handling) to jeden z najważniejszych aspektów budowy zaawansowanych agentów AI (np. z wykorzystaniem LangGraph, LangChain czy LlamaIndex). Odpowiada za to, w jaki sposób agent zapamiętuje kontekst krótko- i długoterminowy, co bezpośrednio wpływa na jakość odpowiedzi, optymalizację kosztów (zużycie tokenów) i spójność konwersacji.

## Dlaczego jest to ważne?

- **Ograniczenia Context Window**: LLMy mają limitowaną liczbę tokenów, którą mogą przetworzyć na raz. Wrzucanie całej historii rozmowy szybko wyczerpuje ten limit i zwiększa koszty.
- **Ciągłość działania**: Złożone zadania mogą trwać długo i wymagać wielu kroków. Agent musi wiedzieć, na jakim etapie się znajduje i nie powtarzać tych samych akcji.
- **Personalizacja**: Pamiętanie preferencji użytkownika z poprzednich sesji znacząco poprawia UX.

## Session Handling (Pamięć Krótkoterminowa - Short-Term Memory)

Obsługa sesji skupia się na bieżącym przebiegu konwersacji. Odpowiada za przechowywanie stanu w obrębie jednego, aktywnego wątku.

### Jak to działa w praktyce?

Wykorzystuje się tzw. **Checkpointery**, które na każdym etapie działania agenta zapisują jego aktualny stan pod konkretnym identyfikatorem sesji (`thread_id`). W architekturze np. LangGraph pozwala to na tzw. przerywanie działania (interrupts) i oczekiwanie na interakcję człowieka (Human-in-the-Loop).

**Przykład:**
```python
from langgraph.checkpoint.sqlite import SqliteSaver

# Inicjalizacja mechanizmu zapisującego stan sesji
memory = SqliteSaver.from_conn_string("checkpoints.db")

# Przekazanie ID sesji do agenta
config = {"configurable": {"thread_id": "user_session_998"}}
response = graph.invoke(input_data, config=config)
```

**Powiązane tematy:**
- [Persistence i Checkpointers w LangGraph](persistence-sqlite-postgres-langgraph.md)
- [Interrupts w LangGraph](interrupts-langgraph.md)

## Memory Management (Pamięć Długoterminowa - Long-Term Memory)

Pamięć długoterminowa rozwiązuje problem zachowania informacji pomiędzy niezależnymi sesjami, po tym jak stara sesja została zamknięta lub jej historia stała się zbyt długa do utrzymania w kontekście.

### Wzorce projektowe pamięci:

1. **Windowing (Okno przesuwne)**:
   Agent ma dostęp tylko do $N$ ostatnich wiadomości z historii. Rozwiązanie tanie i proste, ale powoduje całkowitą utratę starszego kontekstu.

2. **Summarization (Podsumowywanie historii)**:
   Gdy konwersacja przekracza określony limit tokenów, tańszy model językowy (lub główny w tle) generuje zwięzłe podsumowanie dotychczasowej wymiany zdań. Wrzucane jest ono na początek kolejnych promptów, zachowując esencję rozmowy przy minimalnym narzucie tokenów.

3. **Wektorowa Baza Danych (RAG)**:
   Starsze rozmowy, wyekstrahowane fakty i istotne dane użytkownika poddawane są procesowi embeddingu i zapisywane w bazach wektorowych (np. Qdrant, Pinecone). Kiedy użytkownik zadaje pytanie, agent pobiera tylko semantycznie dopasowane fragmenty ze swojej "pamięci" i dołącza je do promptu.
   Zobacz: [Baza Wektorowa vs LLM](baza-wektorowa-vs-llm.md)

4. **Entity Memory (Pamięć faktów / encji)**:
   System aktywnie wychwytuje twarde fakty o użytkowniku podczas rozmowy (np. "Jest wegetarianinem", "Ma psa o imieniu Burek"). Fakty te są zapisywane w zewnętrznej bazie i automatycznie wstrzykiwane do kontekstu (instrukcji systemowej) w każdej nowej sesji, by profilować agenta. W systemach rozproszonych można do tego wykorzystać narzędzia typu Mem0.

## Podsumowanie - Architektura Hybrydowa

Produkcyjni agenci łączą wszystkie powyższe podejścia:
- **Relacyjne/NoSQL bazy danych** jako Checkpointery (zarządzanie bieżącym stanem i sesją).
- **Bazy wektorowe** jako długoterminowy magazyn wiedzy i dokumentów.
- **Mechanizmy okienkowania i podsumowywania** do optymalizacji kosztów bieżącego zapytania.

Zobacz również: [Pamięć długoterminowa AI](pamięć-długoterminowa-ai.md).
