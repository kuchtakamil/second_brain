# Opisz temat LLMy a metryki do ich oceniania

**Data:** 28 gru 2025, 00:26:47 CET

---

**User:**

Opisz temat LLMy a metryki do ich oceniania

---

**Gemini:**

Ewaluacja dużych modeli językowych (LLM) jest procesem wielowymiarowym, który ewoluował od prostych porównań statystycznych do zaawansowanych systemów opartych na modelowaniu semantycznym i sędziowaniu przez inne modele AI (LLM-as-a-Judge). Ze względu na generatywny i często niedeterministyczny charakter LLM, tradycyjne metryki NLP są obecnie uznawane za niewystarczające.

---

## 1. Metryki Statystyczne (N-gram Based)

Tradycyjne metryki opierają się na dosłownym dopasowaniu tokenów (n-gramów) między tekstem wygenerowanym (*candidate*) a tekstem referencyjnym (*reference*).

- **BLEU (Bilingual Evaluation Understudy):** Skupia się na precyzji (*precision*). Oblicza frakcję n-gramów w wygenerowanym tekście, które występują w tekście referencyjnym. Stosowana głównie w tłumaczeniu maszynowym.
- **ROUGE (Recall-Oriented Understudy for Gisting Evaluation):** Koncentruje się na pełności (*recall*). Najczęściej stosowana w zadaniach streszczania tekstu (ROUGE-N, ROUGE-L).
- **METEOR:** Rozszerza BLEU o synonimy i odmiany morfologiczne, co częściowo rozwiązuje problem sztywności dopasowania n-gramów.

**Ograniczenia:** Metryki te całkowicie ignorują semantykę. Zdania o identycznym znaczeniu, ale innej strukturze leksykalnej, otrzymają niskie noty.

---

## 2. Metryki Semantyczne i Embeddingowe

Metryki te wykorzystują przestrzenie wektorowe (embeddings) do oceny podobieństwa znaczeniowego, a nie tylko tekstowego.

- **Cosine Similarity (Podobieństwo Cosinusowe):** Jedna z najpopularniejszych metryk używanych do określania geometrycznego podobieństwa między dwoma tekstami po przekształceniu ich w wektory (tzw. *embeddings*, np. przy użyciu modeli takich jak *Sentence-BERT* czy *OpenAI Embeddings*). W kontekście oceny LLM-ów najczęściej porównuje się wektor **odpowiedzi wygenerowanej przez oceniany model** (tzw. *candidate* lub *prediction*) z wektorem **odpowiedzi wzorcowej/oczekiwanej** (tzw. *reference* lub *ground truth*, napisanej np. przez człowieka w zbiorze testowym).
  - **Zasada działania:** Zamiast mierzyć bezwzględną odległość punktów w przestrzeni (jak to ma miejsce w odległości euklidesowej), metryka ta analizuje *kąt* pomiędzy dwoma wielowymiarowymi wektorami. Wartość cosinusa kąta mieści się w przedziale od -1 (całkowite przeciwieństwo semantyczne) do 1 (identyczny kierunek / znaczenie). Wektor w przestrzeni ortogonalnej (kąt 90 stopni, cosinus 0) oznacza brak związku tematycznego. W praktyce w modelach językowych wartości zazwyczaj oscylują między 0 a 1.
  - **Kluczowe zalety:** Podobieństwo cosinusowe jest w dużej mierze niewrażliwe na *wielkość* (magnitudę) wektorów, co w NLP przekłada się na odporność na różnice w długości analizowanych tekstów (np. podczas porównywania krótkiego pytania z długim dokumentem). Metryka sprawdza jedynie, czy wektory wskazują w ten sam obszar znaczeniowy.
  - **Zastosowanie w RAG:** Stanowi rdzeń systemów wyszukiwania gęstego (*dense retrieval*). Pozwala systemom wektorowym docierać do dokumentów najlepiej pasujących intencją do zapytania użytkownika, nawet kiedy słownictwo pytania i dokumentu jest zupełnie inne (brak wspólnych n-gramów/słów kluczowych).
  - **Ograniczenia:** Skuteczność tej metryki zależy w 100% od dobrego modelu generującego embeddingi (słabe embeddingi dadzą bezwartościowe podobieństwo cosinusowe). Dodatkowo, operując tylko na kącie a ignorując długość wektora, ryzykujemy utratę niektórych subtelnych różnic w częstotliwości występowania istotnych znaków czy tokenów.
- **BERTScore:** Wykorzystuje kontekstowe embeddingi z modelu BERT do mapowania tokenów między tekstem wygenerowanym a referencyjnym. Oblicza sumę podobieństw cosinusowych dla najlepiej dopasowanych par tokenów.
- **MoverScore:** Wykorzystuje odległość *Word Mover’s Distance* (WMD) w przestrzeni embeddingów, co pozwala na lepsze wychwytywanie przesunięć strukturalnych w tekście.

---

## 3. LLM-as-a-Judge (Model-based Evaluation)

Obecnie najskuteczniejsza metoda oceny jakości odpowiedzi w zadaniach *open-ended*. Silniejszy model (np. GPT-4o) ocenia wyjście słabszego modelu.

### Metodyki oceniania:

- **Pairwise Comparison:** Sędzia otrzymuje dwie odpowiedzi na to samo pytanie i musi wskazać lepszą lub ogłosić remis (stosowane w *Chatbot Arena*).
- **Single Answer Scoring:** Sędzia ocenia odpowiedź w skali 1-5 lub 1-10 na podstawie zdefiniowanych kryteriów (rubryk).
- **Reference-guided Evaluation:** Sędzia ma dostęp do poprawnej odpowiedzi i ocenia zgodność kandydata z prawdą.

### G-Eval i technika Chain-of-Thought

Zaawansowane podejście, w którym sędzia (LLM) proszony jest o wygenerowanie kroków logicznych (CoT) przed wystawieniem oceny końcowej. Pozwala to na uniknięcie "halucynacji sędziowskich" i zwiększa korelację z oceną ludzką.

---

## 4. Benchmarki Dziedzinowe

Zamiast pojedynczych metryk, stosuje się zestawy testowe (benchmarks) weryfikujące konkretne zdolności kognitywne.

| Benchmark | Domena | Co mierzy? |
| --- | --- | --- |
| **MMLU** | Wiedza ogólna | 57 zadań z zakresu nauk ścisłych, humanistycznych i społecznych. |
| **GSM8K** | Matematyka | Rozwiązywanie wieloetapowych zadań tekstowych ze szkoły podstawowej. |
| **HumanEval** | Kodowanie | Generowanie kodu w Pythonie na podstawie docstringów (metryka pass@k). |
| **HellaSwag** | Common Sense | Przewidywanie zakończenia scenariuszy z życia codziennego. |
| **TruthfulQA** | Prawdomówność | Odporność na powielanie powszechnych mitów i dezinformacji. |

---

## 5. Metryki Specjalistyczne dla Systemów RAG

W systemach *Retrieval-Augmented Generation* (RAG) ocena musi uwzględniać zarówno jakość odnalezionego kontekstu, jak i wierność odpowiedzi względem tego kontekstu.

- **Faithfulness (Wierność):** Czy odpowiedź opiera się wyłącznie na dostarczonym kontekście? (Eliminacja halucynacji).
- **Answer Relevance:** Czy odpowiedź faktycznie adresuje zapytanie użytkownika?
- **Context Precision:** Czy najbardziej istotne fragmenty dokumentów znajdują się na górze wyników wyszukiwania?

Frameworki takie jak **RAGAS** czy **TruLens** automatyzują ten proces, wykorzystując triadę ocen: *Context Relevance*, *Faithfulness* oraz *Answer Relevance*.

---

## 6. Problematyka i Wyzwania

### Data Contamination (Zanieczyszczenie danych)

Zjawisko, w którym zestawy testowe (np. pytania z MMLU) trafiają do zbioru treningowego modelu. Skutkuje to sztucznie zawyżonymi wynikami, które nie przekładają się na realne zdolności rozumowania.

### Human Preference Bias

Modele oceniane przez ludzi często promują odpowiedzi, które są:

- **Verbose (Przegadane):** Dłuższe odpowiedzi są postrzegane jako lepsze, nawet jeśli zawierają mniej konkretów.
- **Confident:** Model brzmiący pewnie, nawet jeśli się myli, otrzymuje wyższe noty.

### Self-enhancement Bias

Zjawisko, w którym model sędziujący (np. GPT-4) ma tendencję do przyznawania wyższych ocen odpowiedziom wygenerowanym przez samego siebie lub modele o podobnej architekturze.

---

Czy chcesz, abym przedstawił implementację własnego sędziego w Pythonie przy użyciu biblioteki LangChain lub RAGAS?