# Obsługa Błędów w Systemie Wieloagentowym — Plan Tekstów

Plan zawiera strukturę artykułów / rozdziałów pokrywających temat obsługi błędów w architekturze multi-agent. Każda sekcja to osobny, samodzielny tekst lub rozdział do rozwinięcia.

---

## 1. Taksonomia błędów — skąd pochodzą i jak je klasyfikować

- Podział błędów według warstwy: agent, narzędzie, orkiestrator, infrastruktura, dane wejściowe użytkownika
- Błędy deterministyczne vs niedeterministyczne (LLM hallucynuje vs tool rzuca wyjątek)
- Błędy transientne (przejściowe, np. timeout sieci) vs permanentne (np. brak uprawnień)
- Błędy ciche (silent failures) — agent zwraca fałszywą odpowiedź zamiast błędu
- Kaskadowe propagowanie błędów — gdy awaria jednego agenta "zaraża" kolejne węzły w grafie

---

## 2. Błędy pochodzące z agentów (LLM-level errors)

- Halucynacje — agent produkuje faktoidy i nie sygnalizuje braku wiedzy
- Złe formatowanie odpowiedzi (zepsuty JSON, brak wymaganych pól w structured output)
- Nieskończona pętla ReAct — agent krąży w kółko nie osiągając celu (`recursion_limit`)
- Odmowa wykonania (refusal) — model odrzuca polecenie z powodu guardrails / safety
- Utrata kontekstu przy długich konwersacjach (context window overflow, utrata instrukcji systemowej)
- Dryf intencji — agent zmienia cel w trakcie wielokrokowego rozumowania
- Nieoptymalne decyzje routingowe — supervisor deleguje zadanie do niewłaściwego sub-agenta
- Niespójność między agentami — dwa agenty produkują sprzeczne wyniki i brak mechanizmu arbitrażu

---

## 3. Błędy z narzędzi (Tool-level errors)

- Wyjątki w kodzie narzędzia (RuntimeError, ValueError, itp.)
- Niepoprawne argumenty wygenerowane przez LLM (złe typy, brakujące parametry)
- Timeout narzędzia — operacja trwa za długo (np. web scraping, zapytanie do API)
- Rate limiting — zewnętrzne API odrzuca zbyt częste żądania
- Błędy autoryzacji i wygasłe tokeny (OAuth, API keys)
- Narzędzie zwraca pusty lub nieprzewidywalny wynik (np. pusta strona, 404)
- Efekty uboczne nieudanego narzędzia — częściowo wykonana operacja (np. przelew wysłany, ale potwierdzenie nie dotarło)
- Brak idempotentności — ponowienie narzędzia powoduje duplikację akcji (np. podwójna wysyłka e-maila)

---

## 4. Błędy środowiskowe i infrastrukturalne

- Awaria checkpointera / bazy stanu (SQLite locked, Postgres connection lost)
- Utrata stanu grafu — checkpoint się nie zapisał i workflow nie można wznowić
- Problemy z siecią między komponentami (message broker down, gRPC timeout)
- Brak zasobów (OOM, GPU unavailable, dysk pełny)
- Niespójność wersji — agent korzysta z innej wersji narzędzia niż oczekuje orkiestrator
- Problemy z kolejkowaniem i dostarczaniem komunikatów w systemach rozproszonych
- Cold start i opóźnienia inicjalizacji modeli
- Współbieżność — race conditions przy równoległym dostępie agentów do wspólnego stanu

---

## 5. Błędy na poziomie orkiestracji i przepływu (Orchestration-level errors)

- Deadlock — dwa agenty czekają na siebie nawzajem
- Livelock — agenty aktywnie działają, ale nie robią postępu (ciągłe przekierowywanie)
- Nieprawidłowy routing — krawędź warunkowa kieruje do nieistniejącego węzła
- Błędy w reducerach stanu — agenci równolegli produkują kolizje przy merge stanu (fan-in)
- Przekroczenie limitu rekurencji grafu (`recursion_limit` w LangGraph)
- Niespójność stanu po Human-in-the-Loop — człowiek modyfikuje stan w sposób niekompatybilny z oczekiwaniami agenta
- Brak obsługi ścieżki END — graf nie ma zdefiniowanego warunku zakończenia dla pewnych scenariuszy
- Zagubienie kontekstu przy handoff — agent przekazujący nie dołącza kluczowych informacji do następnika

---

## 6. Strategie obsługi błędów — wzorce i mechanizmy

- **Retry z backoff** — automatyczne ponawianie z wykładniczym opóźnieniem (transient errors)
- **Fallback modelu** — przełączenie na zapasowy LLM (np. GPT-4 → Claude) gdy główny jest niedostępny
- **Self-correction loop** — odesłanie komunikatu o błędzie z powrotem do agenta z prośbą o poprawę
- **Circuit breaker** — wyłączenie agenta/narzędzia po N kolejnych awariach, żeby chronić resztę systemu
- **Timeout i deadline propagation** — globalne ograniczenie czasu dla całego workflow, nie tylko pojedynczego kroku
- **Graceful degradation** — system zwraca częściowy wynik zamiast całkowitej awarii
- **Checkpoint & resume** — zapis stanu przed ryzykownymi operacjami, możliwość wznowienia od ostatniego poprawnego punktu
- **Idempotent tool design** — projektowanie narzędzi tak, by ponowienie nigdy nie powodowało duplikacji
- **Validation gates** — walidacja wyjścia agenta przed przekazaniem dalej (structured output + Pydantic)
- **Human-in-the-Loop jako fallback** — eskalacja do człowieka gdy automatyczne mechanizmy zawiodą

---

## 7. Obserwowalność i diagnostyka błędów

- Structured logging — ustrukturyzowane logi z każdego węzła grafu (input, output, czas, błędy)
- Trace ID propagation — powiązanie logów ze sobą w rozproszonym systemie (OpenTelemetry, LangSmith)
- Metryki: error rate per agent, per tool, latency p50/p95/p99, retry count
- Alerty i progi — automatyczne powiadomienia przy przekroczeniu progów błędów
- Replay & debug — możliwość odtworzenia dokładnego przebiegu grafu z checkpointów
- Audyt akcji z efektami ubocznymi — logowanie każdego wywołania narzędzia zmieniającego stan zewnętrzny
- Dashboard operacyjny — wizualizacja stanu zdrowia systemu w czasie rzeczywistym

---

## 8. Testowanie odporności na błędy

- Unit testy narzędzi — mockowanie zewnętrznych API, testowanie edge cases
- Testy integracyjne przepływu — weryfikacja ścieżek błędnych w grafie (czy fallback faktycznie działa)
- Chaos engineering — celowe wstrzykiwanie błędów (losowe timeouty, awarie narzędzi, złe odpowiedzi LLM)
- Testy regresyjne halucynacji — zestaw promptów z oczekiwanymi odpowiedziami + ewaluacja
- Load testing — jak system zachowuje się pod obciążeniem (rate limiting, kolejkowanie, współbieżność)
- Red-teaming agentów — próba złamania agenta advesarialnym inputem (prompt injection, jailbreak)
- Snapshot testing stanu — porównywanie checkpointów z oczekiwanym stanem po każdym kroku

---

## 9. Wzorce architektoniczne zwiększające odporność

- Bulkhead pattern — izolacja agentów w osobnych procesach/kontenerach (awaria jednego nie zabija systemu)
- Saga pattern — koordynacja rozproszonej transakcji z kompensacjami (rollback po częściowej awarii)
- Event sourcing — zapis każdej zmiany stanu jako zdarzenia, możliwość pełnego odtworzenia
- Dead letter queue — przechwytywanie komunikatów, których nie udało się przetworzyć, do późniejszej analizy
- Supervisor hierarchy — wielopoziomowa orkiestracja, gdzie wyższy supervisor obsługuje awarie niższego
- Watchdog / heartbeat — monitoring aktywności agentów, wykrywanie zamrożonych procesów

---

## 10. Aspekty produkcyjne i polityki błędów

- Definiowanie SLA/SLO dla systemu wieloagentowego (dopuszczalny error rate, czas odpowiedzi)
- Polityka eskalacji — kiedy błąd trafia do logów, kiedy do alertu, kiedy do człowieka
- Budżet błędów (error budget) — ile awarii system może sobie pozwolić w oknie czasowym
- Wersjonowanie promptów i narzędzi — zarządzanie zmianami bez wprowadzania regresji
- Canary deployments dla agentów — stopniowe wdrażanie nowej wersji agenta z monitoringiem
- Post-mortem i blameless culture — analiza poważnych incydentów i wyciąganie wniosków

---

## Powiązane pliki
- [Wzorce Projektowe Systemów Agentowych](wzorce-projektowe-systemow-agentowych.md)
- [Agentic Workflows i Multi-Agent Orchestration](agentic-workflows-multi-agent-orchestration.md)
- [Multi-Agent Supervisor w LangGraph](multi-agent-supervisor-langgraph.md)
- [Interrupts w LangGraph](interrupts-langgraph.md)
- [LLM Guardrails](llm-guardrails.md)
- [Narzędzia dla agentów (Tool Use)](narzedzia-dla-agentow-tool-use-langgraph.md)
