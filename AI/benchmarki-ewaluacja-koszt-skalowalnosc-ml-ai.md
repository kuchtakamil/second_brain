# Benchmarki modeli ML/AI oraz ewaluacja jakości, kosztu i skalowalności

## Krótkie podsumowanie
**Ewaluacja i benchmarkowanie modeli ML/AI** to usystematyzowany proces mierzenia wydajności modelu pod kątem dokładności (jakości), zużycia zasobów (kosztów) oraz zachowania serwowanego rozwiązania przy zmiennym obciążeniu (skalowalności). W erze wdrożeń komercyjnych (zwłaszcza LLM) ocena samego "Accuracy" to za mało – liczy się balans między jakością wyników, opóźnieniami (latencją) a kosztami utrzymania infrastruktury i wywołań API.

## Dlaczego jest to ważne (i kiedy ma zastosowanie)?
- **Optymalizacja kosztów operacyjnych (FinOps w AI):** Modele językowe (np. GPT-4, Llama) oraz duże modele dyfuzyjne potrafią być bardzo kosztowne na etapie inferencji (zarówno w API, jak i self-hosted). Wybór odpowiedniego modelu pozwala kontrolować koszty.
- **Zapobieganie regresji jakościowej:** Po wyuczeniu rzadszego wariantu (fine-tuning) musimy sprawdzić, czy model się poprawił w docelowej domenie, unikając jednocześnie problemu *catastrophic forgetting*.
- **Weryfikacja umów SLA (Service Level Agreement):** Gwarantowanie użytkownikom końcowym stałego poziomu usług oznacza, że system musi odpowiadać w danym, przewidywalnym czasie (niskie opóźnienia), co wymusza monitorowanie skalowalności.
- **Wybór technologii (Trade-off):** Pozwala podjąć świadomą inżynierską decyzję, analizując tzw. pareto-front (np. zmniejszamy jakość o 2%, ale tniemy koszty hostingu o 60% przechodząc na mniejszy model).

## Jak to działa (Kluczowe płaszczyzny oceny)

### 1. Ewaluacja Jakości (Quality)
Mierzenie, jak trafne, wiarygodne i sensowne są predykcje i generacje modelu.
- **Metryki zadań klasycznych / NLP:** F1-Score, ROUGE, BLEU, BERTScore.
- **Popularne Benchmarki:** MMLU (ogólna wiedza wielozadaniowa), HumanEval (pisanie kodu), GSM8k (matematyka).
- **RAG (Retrieval-Augmented Generation):** Frameworki takie jak RAGAS mierzące zjawiska takie jak *Faithfulness* (czy odp. opiera się tylko na kontekście) oraz *Answer Relevance*.
- **LLM-as-a-Judge:** Mechanizm zautomatyzowanej oceny, gdzie potężniejszy, zaufany model (np. GPT-4o, Claude 3.5 Sonnet) ocenia wygenerowany tekst na podstawie przygotowanego schematu ocen (rubric). Zastępuje lub optymalizuje drogą i czasochłonną ocenę ludzką raterów (RLHF/Human-in-the-loop).

### 2. Ocena Kosztu (Cost)
Monitorowanie kosztów bezpośrednich wynikających z ewaluacji punktów końcowych.
- **Dla modeli via API (SaaS):** Przeliczanie kosztów na $ / 1M tokenów wejściowych (Prompt) i wyjściowych (Completion). Testowanie technik ich redukcji, np. poprzez **Prompt Caching** czy użycie mniejszych modeli w rolach pomocniczych (tzw. LLM Routing).
- **Dla własnego hostowania (Self-Hosted):** Koszt instancji oblażonej w chmurze (Total Cost of Ownership - TCO). Utylizacja zasobów GPU (np. % użycia SM, Memory Bandwidth), koszt prądu. Skupienie na tym, ile kosztuje nas serwowanie predykcji na pojedynczego użytkownika miesięcznie.

### 3. Skalowalność i Wydajność (Scalability & Performance)
Mierzenie reakcji środowiska produkcyjnego pod ciężarem jednoczesnych requestów.
- **Latency (Opóźnienie):**
  - **TTFT (Time To First Token):** Czas po jakim silnik zwraca pierwszy token (kluczowe do doświadczenia w aplikacjach w trybie *streaming*).
  - **TPOT (Time Per Output Token):** Szybkość generacji każdego kolejnego tokenu.
- **Throughput (Przepustowość):** Liczba wygenerowanych tokenów (lub ukończonych zaptań) na sekundę na poziomie całego serwera.
- **Konkurencja sprzętowa i wirtualna:** Zastosowanie serwerów takich jak vLLM, TensorRT-LLM, korzystających z alokacji pamięci na żądanie (PagedAttention), celem obsługi *Continuous Batchingu*.

---

## Lista pytań na Job Interview

1. Jakie metryki wybrałbyś/wybrałabyś do oceny systemu RAG, który musi odpowiadać na pytania użytkowników na podstawie dokumentacji prawnej organizacji?
2. Wyobraź sobie, że używamy w produkcji modelu przez API generującego w pewnym momencie ogromne koszty obsługi ze względu na ciągłe wysyłanie olbrzymiego kontekstu. Jakie kroki inżynieryjne podejmiesz, aby zmniejszyć koszty bez drastycznego spadku jakości odpowiedzi?
3. Czym różni się metryka TTFT (Time To First Token) od TPOT (Time Per Output Token)? W jakich produktach i use-case'ach dany wskaźnik będzie miał największe znaczenie z perspektywy UX?
4. Co oznacza koncepcja "LLM-as-a-Judge"? Jakie widzisz jej największe zalety, a jakie są ryzyka związane z jej poleganiem w pełni na modelu referencyjnym?
5. Twoim zadaniem jest hostowanie modelu LLM self-hosted. Jakimi narzędziami zmierzysz jego skalowalność pod obciążeniem i jakich "wąskich gardeł" sprzętowych (bottlenecks) byś się spodziewał/a przy stukrotnym wzroście ruchu?
6. W jaki sposób mierzysz utylizację infrastruktury procesorów GPU podczas obsługi wielu żądań w czasie rzeczywistym? Pokaż, dlaczego statyczny batch size to często zły u pomysł i jak to rozwiązuje PagedAttention/Continuous Batching.
7. Opowiedz o problemie "Catastrophic Forgetting" w kontekście optymalizacji modeli. Jak dobrze poprowadzona ewaluacja i tzw. "golden sets" pomagają uniknąć wgrywania wadliwego modelu na produkcję?
8. W jaki sposób zidentyfikować najbardziej optymalny kompromis (trade-off) pomiędzy ilością parametrów modelu (np. 8B vs 70B), a oczekiwaną dokładnością w bardzo specyficznym środowisku domenowym? 

---

## Powiązane tematy
- [[opisz-temat-llmy-a-metryki-do-ich-oceniania|LLMy a metryki do ich oceniania (Cosine Similarity, itp.)]]
- [[repozytorium-datasetow-oraz-wersjonowanie-danych|Repozytorium datasetów oraz wersjonowanie danych]]
