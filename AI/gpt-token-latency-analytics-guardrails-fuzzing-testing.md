# Analityka, Guardraile i Testowanie LLM w Produkcji

Poniższy materiał został przygotowany pod kątem **rozmowy rekrutacyjnej (Job Interview)** na stanowiska związane z AI Engineeringiem, MLOps, LLMOps oraz architekturą systemów AI. Skupia się na produkcyjnych aspektach wdrażania modeli językowych, takich jak bezpieczeństwo, koszty, optymalizacja oraz observability.

---

## 1. GPT-Token & Latency Analytics (Analityka Tokenów i Opóźnień)

### Co to jest?
Zbieranie metryk dotyczących działania modelu w czasie rzeczywistym. Najważniejsze wskaźniki to:
- **Token Analytics:** Zużycie tokenów na wejściu (Prompt Tokens) i wyjściu (Completion Tokens).
- **Latency (Opóźnienia):** 
  - **TTFT (Time To First Token):** Czas od wysłania zapytania do otrzymania pierwszego tokena (kluczowe przy streamingu).
  - **TPOT (Time Per Output Token):** Czas generowania pojedynczego tokena.
  - **Total Latency:** Całkowity czas odpowiedzi.

### Dlaczego to ważne (Wartość biznesowa)?
LLM-y są kosztowne, a ich koszty rosną liniowo z liczbą tokenów. Z kolei opóźnienia drastycznie wpływają na User Experience (UX). Użytkownik nie poczeka 10 sekund na odpowiedź, dlatego stosuje się strumieniowanie (streaming) i śledzi TTFT.

### Jak o tym mówić na rozmowie?
> *"Na produkcji zawsze wdrażam narzędzia do LLM Observability, takie jak **Langfuse**, **LangSmith** czy **Datadog**. Analiza TTFT pozwala mi dobrać odpowiednią strategię streamingu, a śledzenie tokenów ułatwia wychwycenie nieoptymalnie długich promptów w cyklu [RAG](pytania-rekrutacyjne-rag.md). Traktuję to jako podstawę AI FinOps."*

---

## 2. Budget Guardrails (Strażnicy Budżetu)

### Co to jest?
Zabezpieczenia finansowe i infrastrukturalne nałożone na API wywołujące modele LLM. Mogą przyjmować formę hard capów (odcięcie usługi po przekroczeniu X dolarów) lub rate limitingu (Token Bucket per `user_id` / `tenant_id`).

### Nowoczesne Frameworki i Narzędzia
Do implementacji strażników budżetu wykorzystuje się najczęściej wyspecjalizowane bramki API (AI API Gateways), np.:
- **LiteLLM** – bardzo popularne proxy open-source. Unifikuje API wielu dostawców i pozwala na przypisywanie sztywnych limitów kosztowych (`spend limits`) dla konkretnych projektów, użytkowników lub kluczy API.
- **Portkey** – zaawansowany gateway ułatwiający precyzyjne zarządzanie budżetem, routing zapytań (np. fallback na tańszy model) oraz observability.
- **Helicone / Pezzo** – platformy Observability połączone z funkcjonalnością Gatewaya, idealne do śledzenia wydatków i nakładania limitów zapytań.

### Dlaczego to ważne (Wartość biznesowa)?
Chroni firmę przed **Denial of Wallet (DoW)** – atakiem lub po prostu błędem (np. zapętlenie się agenta w [systemie wieloagentowym](obsluga-bledow-system-wieloagentowy.md)), który może wygenerować ogromne rachunki u dostawcy chmury/API (np. OpenAI, Anthropic).

### Jak o tym mówić na rozmowie?
> *"Aplikacje oparte na LLM są podatne na pętle (infinite loops) agentów oraz ataki typu DoW. Rozwiązuję to poprzez **Budget Guardrails** implementowane na poziomie API Gateway. Agreguję zużycie tokenów i przeliczam je na dolary na poziomie najemcy (tenant_id), stosując progi alarmowe oraz twarde odcięcia (circuit breakers), by uniknąć 'bill shocka'."*

---

## 3. Guardrails (Bariery Ochronne)

### Co to jest?
Semantyczne i deterministyczne filtry (Input/Output Guardrails), które walidują to, co wchodzi do modelu i co z niego wychodzi. 

**Tak, w praktyce jest to dodatkowa warstwa (często proxy) pośrednicząca między użytkownikiem a głównym modelem LLM.** Architektura ta składa się najczęściej z:
1. **Reguł deterministycznych** – bardzo szybkie sprawdzanie (np. wyrażenia regularne / Regex) pod kątem słów zakazanych, formatowania (np. wymuszanie JSON-a) czy wycieku PII (np. numerów PESEL).
2. **Kontrolujących modeli AI (LLM-as-a-Judge / Evaluators)** – mniejsze, wyspecjalizowane i tańsze w odpytaniu modele (np. Llama Guard, małe modele typu Cross-Encoder). Ich jedynym zadaniem jest ocena intencji. Przed wysłaniem zapytania do głównego modelu sprawdzają: *Czy prompt wejściowy nie jest próbą Jailbreaku?*. Po wygenerowaniu odpowiedzi przez główny model weryfikują: *Czy odpowiedź jest na temat (Topical Guardrail), nie jest toksyczna i nie halucynuje?* Dopiero po akceptacji strażnika odpowiedź trafia do użytkownika.

### Dlaczego to ważne (Wartość biznesowa)?
LLM-y to "czarne skrzynki", które potrafią generować toksyczne treści, ujawniać dane wrażliwe (PII) lub po prostu halucynować, zwracając błędny format (np. zamiast JSON-a). Guardrails zapewniają, że aplikacja jest bezpieczna dla marki i zgodna z prawem.

### Jak o tym mówić na rozmowie?
> *"Oprócz zwykłego promptowania stosuję frameworki takie jak **NeMo Guardrails**, **Guardrails AI** czy **Llama Guard**. Implementuję wielowarstwową ochronę: od prostych Regexów na numer PESEL (PII leakage), po małe modele ewaluacyjne (np. Cross-Encodery), które sprawdzają, czy odpowiedź nie zbacza z tematu (Topical Guardrails) i czy jest bezpieczna. Więcej o ich implementacji przeczytasz w [LLM Guardrails](llm-guardrails.md)."*

---

## 4. Prompt Fuzzing

### Co to jest?
Adaptacja klasycznego fuzzingu z cyberbezpieczeństwa na potrzeby AI. Polega na automatycznym wstrzykiwaniu tysięcy losowych, zmutowanych lub specjalnie spreparowanych promptów (edge cases), by "złamać" system i znaleźć luki (np. podatność na Prompt Injection).

### Dlaczego to ważne (Wartość biznesowa)?
Tradycyjne testy jednostkowe nie sprawdzają się przy niedeterministycznych modelach LLM. Fuzzing pozwala na stres-testy aplikacji przed jej wdrożeniem na produkcję.

### Jak o tym mówić na rozmowie?
> *"Ręczne testowanie LLM to za mało. W pipeline'ach CI/CD dołączam **Prompt Fuzzing** używając narzędzi typu **Promptfoo** lub **Giskard**. Automatycznie generuję setki scenariuszy ataku, by zweryfikować, na ile mój system [RAG](pytania-rekrutacyjne-rag.md) jest odporny na przełamanie (Jailbreaks) i czy nie ujawni wewnętrznego promptu systemowego."*

---

## 5. Adversarial & Bias Testing (Testowanie Adwersarzowe i Uprzedzeń)

### Co to jest?
- **Adversarial Testing (Red Teaming):** Celowe, wyrafinowane ataki (np. role-playing typu *DAN - Do Anything Now*, ukrywanie komend w innych językach czy base64), by zmusić model do ominięcia wbudowanych zasad bezpieczeństwa.
- **Bias Testing:** Zautomatyzowane sprawdzanie, czy model nie faworyzuje konkretnych płci, ras, grup wiekowych, czy religijnych.

### Dlaczego to ważne (Wartość biznesowa)?
Regulacje prawne, w tym nadchodzący **EU AI Act**, nakładają surowe kary za dyskryminujące algorytmy. Błędy w tych obszarach niszczą reputację firmy w kilka minut.

### Jak o tym mówić na rozmowie?
> *"Przed wydaniem modelu na produkcję przeprowadzam sesje **Red Teamingu**. Zamiast po prostu ufać modelowi, atakuję go metodami adwersarzowymi. Dodatkowo, regularnie ewaluuję dataset i outputy pod kątem **biasu**, stosując metryki fairness. Dbałość o bezpieczeństwo i zgodność z regulacjami (Compliance/Governance) to dla mnie równie ważny aspekt co sama celność odpowiedzi."*

---

## 6. Alignment & Feedback (RLHF / RLAIF)

### Co to jest?
Techniki "dostrajania" zachowania modelu, aby jego odpowiedzi były zgodne (aligned) z oczekiwaniami, wartościami i intencjami użytkownika (tzw. zasada HHH: Helpful, Honest, Harmless).
- **RLHF (Reinforcement Learning from Human Feedback):** Trenowanie modelu z wykorzystaniem ocen wystawianych przez ludzi (np. kciuk w górę / w dół), na podstawie których model uczy się optymalizować swoje odpowiedzi (Reward Model).
- **RLAIF (Reinforcement Learning from AI Feedback):** Nowsze, wysoce skalowalne podejście, w którym rolę "człowieka oceniającego" przejmuje inny, potężniejszy model AI (tzw. LLM-as-a-Judge, oceniający np. output z mniejszego modelu).

### Dlaczego to ważne (Wartość biznesowa)?
Podstawowe (base) modele są surowe i mogą zachowywać się nieprzewidywalnie. Alignment pozwala na spersonalizowanie zachowania modelu pod specyfikę branży (np. asystent medyczny musi być formalny i ostrożny). Ponadto, wbudowany w aplikację system zbierania feedbacku pozwala na ciągłe udoskonalanie produktu w czasie (budowanie tzw. Data Flywheel).

### Jak o tym mówić na rozmowie?
> *"Aby zbudować produkt AI klasy premium, wdrażam mechanizmy zbierania ciągłego feedbacku (explicit/implicit) od użytkowników. Taki strumień danych służy mi jako sygnał do **RLHF** lub nowszego **DPO (Direct Preference Optimization)**, by iteracyjnie 'doszlifować' model. W środowiskach, gdzie adnotatorzy są zbyt drodzy, stawiam na **RLAIF**, automatyzując ocenę poprzez silne modele-sędziów, co radykalnie obniża koszty i czas budowania własnych modeli."*

---

## 7. Synthetic Data Generation (Generowanie Danych Syntetycznych)

### Co to jest?
Wykorzystywanie potężnych modeli (Frontier Models) do tworzenia ogromnych, wysokiej jakości zbiorów danych treningowych (par zapytanie-odpowiedź, scenariuszy konwersacyjnych, krawędziowych przypadków), które następnie służą do fine-tuningu mniejszych modeli lub testowania systemów RAG.

### Dlaczego to ważne (Wartość biznesowa)?
Największym wąskim gardłem w MLOps jest brak "czystych", zróżnicowanych i zlabelowanych danych. Dane syntetyczne rozwiązują ten problem: są nieporównywalnie tańsze, błyskawiczne w wygenerowaniu, a co najważniejsze – z założenia pozbawione są danych wrażliwych (PII), co całkowicie eliminuje ryzyka prawno-prywatnościowe.

### Jak o tym mówić na rozmowie?
> *"Aby zredukować koszty inferencji (Inference Costs) bez utraty jakości, często stosuję technikę **Synthetic Data Generation**. Używam dużych modeli (jak GPT-4o czy Claude 3.5 Sonnet) do wygenerowania tysięcy wysokiej jakości przykładów treningowych na bazie firmowych dokumentów. Na tak spreparowanym, syntetycznym zbiorze przeprowadzam Fine-Tuning małego i taniego modelu (np. z rodziny Llama). Dzięki takiej destylacji wiedzy uzyskuję własny model, który działa lokalnie, kosztuje ułamek centa i dorównuje gigantom na wąskim wycinku zadań."*

---

## Słowo kluczowe na podsumowanie
Podczas rozmowy użyj pojęcia **LLM Observability & Security Pipeline**. Wdrożenie LLM-a na produkcję to nie tylko wrzucenie klucza API do LangChaina, ale zbudowanie wokół niego ekosystemu analitycznego (Telemetry), ochronnego (Guardrails) oraz testowego (DevSecOps dla AI / Red Teaming).
