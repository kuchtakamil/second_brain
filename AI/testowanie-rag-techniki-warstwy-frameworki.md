# Testowanie mechanizmu RAG — techniki, warstwy testów i sprawdzone frameworki

## Krótkie wprowadzenie

Ten dokument to materiał edukacyjny opisujący, **jak testuje się systemy RAG (Retrieval-Augmented Generation)** w praktyce inżynierskiej. Testowanie RAG nie jest jedną czynnością — to zestaw nakładających się **warstw** (od testów pojedynczych komponentów, przez testy end-to-end, po monitoring na produkcji), z których każda używa innych metryk i innych narzędzi. Celem dokumentu jest pokazanie tej mapy w sposób opisowy oraz wskazanie konkretnych, sprawdzonych w branży **frameworków** (RAGAS, TruLens, DeepEval, Arize Phoenix, LangSmith, Giskard i innych).

## Dlaczego testowanie RAG jest trudne (i dlaczego jest kluczowe)

Klasyczne testy oprogramowania zakładają determinizm: dla danego wejścia oczekujemy dokładnie jednego, znanego wyjścia (`assert result == expected`). System RAG łamie wszystkie te założenia naraz:

- **Niedeterminizm generacji** — ten sam prompt z tym samym kontekstem może dać dwie różne (i obie poprawne) odpowiedzi. Sprawdzanie przez dosłowne dopasowanie tekstu (`==`) jest bezużyteczne.
- **Dwa niezależne źródła błędów** — odpowiedź może być zła, bo (a) wyszukiwanie (*retrieval*) zwróciło zły kontekst, albo (b) model (*generation*) zignorował dobry kontekst i zhalucynował. Dobry zestaw testów musi **rozróżnić, która warstwa zawiodła**, inaczej debugowanie sprowadza się do zgadywania.
- **Brak jednej „prawdy"** — w zadaniach otwartych (*open-ended*) nie istnieje jedyna poprawna odpowiedź, tylko spektrum lepszych i gorszych.
- **Sprzężenie zmian** — podmiana modelu embeddingów, zmiana `chunk_size`, inny prompt czy nowy LLM mogą poprawić jedną metrykę, a cicho zepsuć inną. Bez testów regresji jest to niewykrywalne.

Z tych powodów w ekosystemie LLM przyjęło się podejście **eval-driven development**: zbiór ewaluacji (evals) pełni rolę, jaką w klasycznym kodzie pełni suite testów jednostkowych — jest siatką bezpieczeństwa, która pozwala iterować bez psucia tego, co już działało. Por. [[opisz-temat-llmy-a-metryki-do-ich-oceniania]] (metryki oceny LLM ogólnie) oraz [[kontrowersje-wokół-rag]] (kiedy RAG zawodzi).

---

## Mapa mentalna: dekompozycja RAG na komponenty

Żeby wiedzieć **co** testować, trzeba najpierw rozłożyć pipeline na części. Każda strzałka poniżej to osobny punkt, w którym może wkraść się błąd — i osobny punkt, który warto testować w izolacji:

```
Dokumenty → [Ingestion/Parsing] → [Chunking] → [Embedding] →
          → [Vector DB / Index] → [Retrieval top-k] → [Re-ranking] →
          → [Budowa promptu / kontekst] → [LLM Generation] → Odpowiedź
```

Z tej dekompozycji wynika naturalny podział testów na **warstwy**:

| Warstwa | Co testuje | Główne pytanie |
|---|---|---|
| **1. Retrieval** | jakość wyszukiwania (top-k, reranking) | Czy znaleźliśmy właściwe fragmenty? |
| **2. Generation** | jakość odpowiedzi przy danym kontekście | Czy model dobrze wykorzystał kontekst? |
| **3. End-to-end** | cały pipeline jako całość | Czy użytkownik dostał dobrą odpowiedź? |
| **4. Regresja / CI-CD** | stabilność w czasie | Czy zmiana czegoś nie zepsuła? |
| **5. Produkcja / online** | zachowanie na żywym ruchu | Czy działa na realnych zapytaniach? |
| **6. Odporność / adversarial** | przypadki brzegowe i ataki | Czy da się to złamać / oszukać? |

Poniżej omawiam każdą warstwę.

---

## Warstwa 1: Testy komponentu wyszukiwania (Retrieval)

To **najważniejsza i najczęściej zaniedbywana** warstwa. Reguła kciuka brzmi: *garbage in, garbage out* — jeśli retrieval zwróci zły kontekst, żaden, nawet najlepszy LLM tego nie naprawi. Dlatego retrieval testuje się **osobno**, jeszcze zanim w grę wejdzie generacja.

### Fundament: złoty zbiór (golden dataset / ground truth)

Niemal każdy sensowny test offline wymaga zbioru referencyjnego. W kontekście retrievalu jest to lista par:

> *zapytanie → identyfikatory fragmentów, które POWINNY zostać znalezione* (tzw. *relevant documents*)

Ten zbiór tworzy się ręcznie (eksperci dziedzinowi), półautomatycznie albo syntetycznie (patrz sekcja o generowaniu danych). Jakość złotego zbioru determinuje wiarygodność wszystkich metryk — to inwestycja, której nie da się obejść.

### Metryki Information Retrieval (klasyczne, deterministyczne)

Retrieval to w istocie problem *information retrieval* znany z wyszukiwarek, więc używa się sprawdzonych metryk IR. Dzielą się one na dwie grupy:

**A) Metryki nieuwzględniające kolejności (order-unaware)** — liczy się, *czy* trafny dokument jest w top-k, a nie *na której pozycji*:

- **Precision@k** — jaki odsetek z `k` zwróconych fragmentów jest faktycznie trafny. Mierzy „zanieczyszczenie" kontekstu szumem.
- **Recall@k** — jaki odsetek wszystkich istniejących trafnych fragmentów udało się znaleźć w top-k. Mierzy „kompletność".
- **Hit Rate@k** — odsetek zapytań, dla których *przynajmniej jeden* trafny fragment znalazł się w top-k. Najprostsza, intuicyjna miara „czy w ogóle trafiliśmy".
- **F1@k** — średnia harmoniczna precision i recall.

**B) Metryki uwzględniające kolejność (order-aware)** — kara za umieszczanie trafnych fragmentów nisko w rankingu. Kolejność jest krytyczna w RAG ze względu na zjawisko **„Lost in the Middle"** (model słabiej widzi środek długiego kontekstu — patrz [[pytania-rekrutacyjne-rag]]):

- **MRR (Mean Reciprocal Rank)** — uśredniona odwrotność pozycji *pierwszego* trafnego wyniku (`1/rank`). Premia za to, że właściwa rzecz jest wysoko.
- **MAP (Mean Average Precision)** — średnia z precyzji liczonej na kolejnych pozycjach trafień; uwzględnia wiele trafnych dokumentów.
- **NDCG@k (Normalized Discounted Cumulative Gain)** — najbogatsza metryka: uwzględnia zarówno pozycję, jak i **stopień** trafności (relevance grade, np. 0/1/2/3), z logarytmicznym dyskontem za niższe pozycje. Standard dla rankingów.

> **Intuicja, kiedy co:** jeśli do LLM trafia tylko top-3, najbardziej liczy się, by trafny fragment był w tej trójce i jak najwyżej → patrz MRR i NDCG. Jeśli budujemy szeroki kontekst i ważna jest kompletność → patrz Recall@k.

Te metryki liczą m.in. **LlamaIndex** (`RetrieverEvaluator` — hit rate, MRR) oraz biblioteki IR jak `ranx` czy `pytrec_eval`. Do wyboru samego modelu embeddingów i retrievera służą benchmarki **MTEB** (Massive Text Embedding Benchmark) i **BEIR** — warto na nich oprzeć decyzję, zamiast zgadywać.

### Metryki retrievalu oparte na LLM (reference-free)

Klasyczne metryki IR wymagają złotego zbioru z oznaczonymi dokumentami. Gdy go nie ma, używa się **LLM-as-a-Judge** do oceny trafności kontekstu „w locie". Najważniejsze (z frameworka **RAGAS**):

- **Context Precision** — czy *trafne* fragmenty znalazły się *wysoko* w rankingu (sygnał vs szum). Może działać z ground truth lub bez (wersja LLM-owa).
- **Context Recall** — czy cały kontekst potrzebny do udzielenia wzorcowej odpowiedzi udało się odzyskać. Wymaga ground truth (referencyjnej odpowiedzi). Odpowiada na pytanie: *czy w pobranych fragmentach w ogóle JEST odpowiedź?*
- **Context Relevance / Context Relevancy** — jaki odsetek pobranego kontekstu jest faktycznie istotny dla pytania (mierzy szum).

### Testowanie chunkingu i embeddingów w izolacji

Warto traktować **strategię chunkingu** jako osobny eksperyment: ten sam złoty zbiór przepuszcza się przez różne konfiguracje (`fixed-size` vs `semantic` vs `parent-child` / *small-to-big*, różne `chunk_size` i `overlap`) i porównuje metryki retrievalu. To czysty test A/B na poziomie komponentu, bez angażowania kosztownego LLM. Szczegóły strategii — patrz [[pytania-rekrutacyjne-rag]] oraz [[rag-tabele-czy-model-czy-preprocesor]].

---

## Warstwa 2: Testy komponentu generacji (Generation)

Tu sprawdzamy: **zakładając, że kontekst był dobry — czy model wygenerował dobrą odpowiedź?** Izolacja jest tu kluczowa: podajemy modelowi „idealny" kontekst (lub ten, który faktycznie pobrał retrieval) i oceniamy samą generację.

### Faithfulness / Groundedness (wierność, uziemienie) — najważniejsza metryka anty-halucynacyjna

**Czy każde twierdzenie w odpowiedzi da się wywieść z dostarczonego kontekstu?** To rdzeń RAG — model ma być „maszyną do czytania ze zrozumieniem", a nie konfabulować z wiedzy parametrycznej.

Typowy mechanizm pomiaru (np. w RAGAS): LLM rozkłada odpowiedź na atomowe twierdzenia (*claims*), a następnie sprawdza, ile z nich znajduje potwierdzenie w kontekście. Wynik = `twierdzenia poparte kontekstem / wszystkie twierdzenia`. Niski faithfulness = halucynacja.

### Answer Relevance (trafność odpowiedzi)

**Czy odpowiedź faktycznie odnosi się do pytania?** Mierzy gadatliwość i ucieczki od tematu. RAGAS robi to sprytnie: na podstawie wygenerowanej odpowiedzi prosi LLM o wygenerowanie pytań, na które ta odpowiedź by pasowała, i mierzy podobieństwo (cosine) tych pytań do pytania oryginalnego.

### Answer Correctness / Answer Semantic Similarity

**Czy odpowiedź jest poprawna względem wzorca (ground truth)?** Łączy zgodność faktograficzną z podobieństwem semantycznym do odpowiedzi referencyjnej. Wymaga złotego zbioru z wzorcowymi odpowiedziami.

### Detekcja halucynacji i dodatkowe kryteria

Frameworki oferują też dedykowane metryki: **Hallucination**, a także kryteria bezpieczeństwa/jakości jak **Bias**, **Toxicity** (np. w DeepEval). Tematycznie pokrewne są mechanizmy obronne na wejściu/wyjściu — patrz [[llm-guardrails]].

---

## Warstwa 3: Testy end-to-end — RAG Triad

Najpopularniejszy framework koncepcyjny do oceny całości to **RAG Triad**, spopularyzowany przez **TruLens**. Składa się z trzech sprzężonych ocen tworzących „trójkąt":

```
              Pytanie użytkownika
               /                \
   Context Relevance         Answer Relevance
   (pytanie ↔ kontekst)      (pytanie ↔ odpowiedź)
               \                /
                \              /
               Groundedness / Faithfulness
               (odpowiedź ↔ kontekst)
```

1. **Context Relevance** — czy pobrany kontekst pasuje do pytania? (diagnozuje **retrieval**)
2. **Groundedness (Faithfulness)** — czy odpowiedź jest oparta na kontekście? (diagnozuje **generację / halucynacje**)
3. **Answer Relevance** — czy odpowiedź odpowiada na pytanie? (diagnozuje **trafność końcową**)

**Diagnostyczna siła triady:** kombinacja wyników mówi, *gdzie* jest problem. Niski Context Relevance → wina retrievalu/chunkingu. Wysoki Context Relevance, ale niski Groundedness → model halucynuje mimo dobrego kontekstu. Wysokie pierwsze dwa, niski Answer Relevance → model gubi się lub jest zbyt rozwlekły. To właśnie czyni triadę tak użyteczną — nie tylko ocenia, ale wskazuje winowajcę.

RAGAS w praktyce rozszerza ten zestaw o **Context Precision/Recall**, **Answer Correctness** i **Noise Sensitivity** (odporność na nieistotne fragmenty w kontekście).

---

## Metryki — przegląd taksonomiczny

Niezależnie od warstwy, używane metryki dzielą się na cztery rodziny. (Szersze omówienie w [[opisz-temat-llmy-a-metryki-do-ich-oceniania]].)

### 1. Metryki statystyczne / leksykalne (n-gram)
**BLEU, ROUGE, METEOR, Exact Match, token-level F1.** Liczą dosłowne pokrycie n-gramów z tekstem referencyjnym. W generacji RAG **w dużej mierze przestarzałe** — ignorują semantykę (parafraza dostaje niską ocenę). Wciąż przydatne w retrievalu (exact match na ID) i w zadaniach o sztywnej formie.

### 2. Metryki semantyczne / embeddingowe
**BERTScore, MoverScore, Cosine Similarity** na embeddingach (np. Sentence-BERT). Mierzą podobieństwo *znaczenia*, nie słów. Lepsze niż leksykalne, ale czułe na jakość modelu embeddingów i czasem zbyt „pobłażliwe".

### 3. LLM-as-a-Judge (model jako sędzia) — dziś dominujący paradygmat
Silny model (np. klasy GPT-4o / Claude) ocenia wyjście wg rubryki. Warianty:
- **Single-answer scoring** — ocena w skali (np. 1–5) wg kryteriów.
- **Pairwise comparison** — która z dwóch odpowiedzi lepsza (jak w *Chatbot Arena*); idealne do testów A/B i regresji.
- **Reference-guided** — sędzia ma dostęp do wzorcowej odpowiedzi.
- **G-Eval** — sędzia generuje najpierw kroki rozumowania (Chain-of-Thought), a dopiero potem ocenę; mocno podnosi korelację z oceną człowieka. Zaimplementowane natywnie w **DeepEval**.

> **Uwaga o pułapkach sędziego LLM:** *self-enhancement bias* (faworyzowanie odpowiedzi własnego modelu), *verbosity bias* (premiowanie dłuższych odpowiedzi), *position bias* (kolejność w pairwise). Dlatego sędziego też trzeba kalibrować względem ocen ludzkich.

### 4. Reference-based vs reference-free
- **Reference-based** — wymaga wzorcowej odpowiedzi/dokumentów (Context Recall, Answer Correctness, klasyczne IR). Dokładniejsze, ale kosztowne (trzeba zbudować złoty zbiór).
- **Reference-free** — ocenia spójność wewnętrzną pytanie↔kontekst↔odpowiedź bez wzorca (Faithfulness, Answer/Context Relevance, cała triada). Tańsze i skalowalne — można je liczyć nawet na produkcji. To była główna innowacja oryginalnego RAGAS.

---

## Generowanie syntetycznych zbiorów testowych

Ręczne tworzenie złotego zbioru (setki par pytanie–odpowiedź–kontekst) jest wąskim gardłem. Sprawdzone narzędzia generują je automatycznie z bazy wiedzy:

- **RAGAS `TestsetGenerator`** — buduje graf wiedzy z dokumentów i generuje pytania o różnym poziomie złożoności (tzw. *evolutions*: proste, wymagające wnioskowania *reasoning*, łączące wiele fragmentów *multi-context*, warunkowe). Daje zróżnicowany, „trudny" zbiór, a nie tylko trywialne pytania.
- **LlamaIndex `RagDatasetGenerator` / `generate_question_context_pairs`** — generuje pary pytanie–kontekst wprost z zaindeksowanych węzłów; świetne do ewaluacji retrievalu.
- **Giskard RAGET (RAG Evaluation Toolkit)** — generuje zróżnicowane typy pytań (proste, złożone, „z rozproszeniem", podwójne) i potrafi przypisać błędy do konkretnego komponentu pipeline'u.

Złota zasada: zbiór syntetyczny **zawsze** przejrzyj wyrywkowo ludzkim okiem — generator też potrafi tworzyć bezsensowne lub niejednoznaczne pytania.

---

## Warstwa 4: Testy regresji i integracja z CI/CD (eval-driven development)

To miejsce, gdzie evals stają się prawdziwymi „testami" w sensie inżynierskim. Idea:

1. Utrzymuj wersjonowany złoty zbiór ewaluacyjny w repo.
2. Po każdej zmianie (inny prompt, model, `chunk_size`, embeddingi, reranker) uruchom pełną ewaluację.
3. Ustaw **progi (thresholds / assertions)** — np. `faithfulness > 0.85`, `context_recall > 0.9`. Spadek poniżej progu = czerwony build, dokładnie jak nieprzechodzący test jednostkowy.
4. Bramkuj merge do głównej gałęzi wynikiem ewaluacji.

Narzędzia wprost wspierające ten model:
- **DeepEval** — projektowany jako *„pytest dla LLM"*; testy pisze się jak `pytest`, integruje z CI, ma asercje na metrykach.
- **Promptfoo** — deklaratywne testy promptów/RAG w YAML, świetne do porównań i bramek w CI.
- **LangSmith** (LangChain) — datasety + evaluatory uruchamiane w pipeline.
- **MLflow** (`mlflow.evaluate`) — ewaluacja z metrykami RAG i wersjonowaniem eksperymentów (por. [[mlflow]]).

Pokrewne podejścia do testowania warstwy LLM (fuzzing, analiza latencji) opisuje [[gpt-token-latency-analytics-guardrails-fuzzing-testing]].

---

## Warstwa 5: Testy w produkcji (online evaluation, monitoring, observability)

Offline eval nigdy nie pokryje wszystkich realnych zapytań — rozkład pytań użytkowników dryfuje. Dlatego dochodzi warstwa **online**:

- **Tracing / observability** — pełne ślady każdego zapytania (pytanie → pobrane chunki → prompt → odpowiedź → latencja → koszt). Standard: **Arize Phoenix** (open source, wizualizacja embeddingów i klastrów UMAP, wykrywanie dryfu), **LangSmith**, **TruLens**, **Langfuse**.
- **Reference-free eval na żywym ruchu** — metryki triady (Faithfulness, Relevance) liczone na próbce realnych zapytań, bo nie wymagają wzorca.
- **User feedback** — sygnały kciuk w górę/dół, edycje odpowiedzi, „regeneruj" — implicytne i eksplicytne oceny jakości.
- **A/B testing** — porównanie dwóch konfiguracji pipeline'u na żywym ruchu (np. dwa rerankery), z metrykami biznesowymi i jakościowymi.
- **Detekcja dryfu** — monitorowanie rozkładu zapytań i embeddingów; nowe tematy spoza bazy wiedzy = sygnał do aktualizacji korpusu.

---

## Warstwa 6: Testy odpornościowe i adversarialne (robustness / red-teaming)

Ostatnia warstwa sprawdza zachowanie w przypadkach brzegowych i pod presją:

- **Testy negatywne** — zapytania, na które odpowiedzi *nie ma* w bazie. Poprawne zachowanie: *„Nie wiem / brak informacji w kontekście"*, a **nie** konfabulacja. To jeden z najważniejszych i najczęściej pomijanych testów.
- **Noise Sensitivity** — wstrzykiwanie nieistotnych/sprzecznych fragmentów do kontekstu i sprawdzenie, czy model się nie rozprasza (metryka w RAGAS).
- **Needle in a Haystack** — ukrycie pojedynczego faktu („igły") w bardzo długim kontekście („stogu siana") i test, czy model go znajdzie niezależnie od pozycji (diagnoza problemu „Lost in the Middle").
- **Prompt injection / jailbreak** — czy złośliwa treść w dokumentach lub zapytaniu potrafi przejąć instrukcje modelu. Dedykowane narzędzia: **Giskard** (skan podatności), **DeepTeam** (red-teaming od twórców DeepEval), **promptfoo** (moduł red-team), **Garak**.
- **Out-of-domain / robustność językowa** — parafrazy, literówki, inne języki, zapytania wieloskokowe (*multi-hop*).

---

## Przegląd sprawdzonych frameworków (zestawienie)

| Framework | Typ | Mocne strony / czym wyróżnia się w testach RAG |
|---|---|---|
| **RAGAS** | open source | Zestaw metryk RAG (Faithfulness, Context Precision/Recall, Answer Relevancy/Correctness, Noise Sensitivity); reference-free; generator syntetycznych zbiorów. De facto standard. |
| **TruLens** | open source (Snowflake) | **RAG Triad**, feedback functions, instrumentacja/tracing aplikacji. |
| **DeepEval** | open source (Confident AI) | *„Pytest dla LLM"* — testy w stylu pytest, G-Eval, integracja z CI, red-teaming (DeepTeam). |
| **Arize Phoenix** | open source | Observability + ewaluacja; wizualizacja embeddingów (UMAP), wykrywanie dryfu; online i offline. |
| **LangSmith** | komercyjny (LangChain) | Tracing, datasety, evaluatory (LLM-judge i custom), monitoring produkcyjny. |
| **Giskard** | open source | RAGET — autogeneracja testów per komponent; skan podatności (halucynacje, prompt injection). |
| **Promptfoo** | open source | Deklaratywne (YAML) testy i porównania promptów/RAG; red-teaming; idealne do CI. |
| **MLflow** | open source | `mlflow.evaluate` z metrykami RAG, wersjonowanie eksperymentów (zob. [[mlflow]]). |
| **LlamaIndex evals** | open source | Wbudowane `RetrieverEvaluator` (Hit Rate, MRR), `FaithfulnessEvaluator`, `RelevancyEvaluator`, `CorrectnessEvaluator`. |
| **Continuous Eval** (Relari) | open source | Modułowa ewaluacja pipeline'u RAG komponent po komponencie. |
| **UpTrain / Galileo / Langfuse** | open / komercyjne | Ewaluacja i obserwowalność GenAI (Galileo i Langfuse mocno produkcyjne). |

> **Benchmarki doboru komponentów (nie pipeline'u):** **MTEB** i **BEIR** do wyboru modelu embeddingów i retrievera; **MMLU/TruthfulQA/HellaSwag** do oceny samego LLM (zob. [[benchmarki-ewaluacja-koszt-skalowalnosc-ml-ai]]).

---

## Praktyczny przepływ pracy (rekomendowana kolejność)

1. **Zbuduj złoty zbiór** — ręcznie + syntetycznie (RAGAS/LlamaIndex/Giskard), przejrzyj ludzkim okiem.
2. **Najpierw napraw retrieval** — mierz Hit Rate / MRR / NDCG i Context Precision/Recall. Bez dobrego retrievalu reszta nie ma sensu.
3. **Potem testuj generację w izolacji** — Faithfulness i Answer Relevance na poprawnym kontekście.
4. **Złóż end-to-end** — RAG Triad jako dashboard diagnostyczny.
5. **Wepnij to w CI/CD** — progi/asercje (DeepEval, promptfoo), bramkuj zmiany.
6. **Wdroż monitoring produkcyjny** — tracing (Phoenix/LangSmith), reference-free eval na próbce, feedback, A/B.
7. **Cyklicznie red-teaming** — testy negatywne, noise sensitivity, prompt injection.

## Najczęstsze pułapki

- **Testowanie tylko end-to-end** — gdy całość daje zły wynik, nie wiesz, czy winny jest retrieval, czy LLM. Zawsze izoluj warstwy.
- **Ślepe zaufanie sędziemu LLM** — kalibruj wyniki LLM-judge względem próbki ocen ludzkich; uważaj na verbosity i self-enhancement bias.
- **Złoty zbiór zbyt mały lub zbyt łatwy** — same trywialne pytania zawyżają metryki; potrzebujesz pytań *multi-hop* i negatywnych.
- **Mierzenie BLEU/ROUGE na odpowiedziach generatywnych** — niereprezentatywne; przejdź na metryki semantyczne i LLM-judge.
- **Brak testów regresji** — bez progów w CI każda „drobna" zmiana promptu może cicho pogorszyć jakość.
- **Ignorowanie produkcji** — offline eval nie wychwyci dryfu rozkładu realnych zapytań.

---

## Podsumowanie

Testowanie RAG to **wielowarstwowa dyscyplina**, nie pojedyncza metryka. Trzeba osobno ocenić **retrieval** (metrykami IR: Precision/Recall/Hit Rate/MRR/NDCG oraz Context Precision/Recall), osobno **generację** (Faithfulness, Answer Relevance, Correctness), spiąć je w **RAG Triad** dla diagnostyki, a następnie ufortyfikować całość **testami regresji w CI/CD**, **monitoringiem produkcyjnym** i **testami adversarialnymi**. Na poziomie metryk dominuje dziś podejście **LLM-as-a-Judge** (zwłaszcza reference-free), wspierane metrykami semantycznymi, podczas gdy stare metryki n-gramowe (BLEU/ROUGE) zeszły na dalszy plan. W warstwie narzędziowej rynkowym standardem są **RAGAS** (metryki + generacja zbiorów), **TruLens** (triada), **DeepEval** (testy w stylu pytest + CI) oraz **Arize Phoenix / LangSmith** (observability), uzupełniane przez **Giskard** i **promptfoo** dla testów odpornościowych.

---

## Powiązane notatki

- [[pytania-rekrutacyjne-rag]] — architektura RAG, chunking, retrieval, re-ranking (kontekst dla testowanych komponentów)
- [[opisz-temat-llmy-a-metryki-do-ich-oceniania]] — metryki oceny LLM (BLEU, ROUGE, BERTScore, LLM-as-a-Judge, G-Eval)
- [[kontrowersje-wokół-rag]] — kiedy i dlaczego RAG zawodzi
- [[rag-tabele-czy-model-czy-preprocesor]] — preprocessing/ingestion (źródło błędów w warstwie 1)
- [[llm-guardrails]] — mechanizmy obronne na wejściu/wyjściu (pokrewne testom odpornościowym)
- [[gpt-token-latency-analytics-guardrails-fuzzing-testing]] — fuzzing i analiza latencji LLM
- [[benchmarki-ewaluacja-koszt-skalowalnosc-ml-ai]] — benchmarki i ewaluacja w szerszym kontekście ML/AI
- [[mlflow]] — wersjonowanie eksperymentów i ewaluacji
