# Metryki AI przy Accuracy i Threshold dla RAG

## Czym jest ten dokument

Dokument wyjaśnia dwa fundamentalne pojęcia w ewaluacji systemów RAG (Retrieval-Augmented Generation): **Accuracy** (dokładność / wynik metryki) oraz **Threshold** (próg akceptacji). Omówione jest ich znaczenie, wzajemna relacja, sposób konfiguracji i praktyczne zastosowanie w pipeline'ach CI/CD.

---

## Definicje

### Accuracy (Score) — wynik metryki

**Accuracy** w kontekście ewaluacji RAG **nie jest jedną, konkretną metryką** — to termin parasol (*umbrella term*) opisujący **liczbowy wynik (score)**, jaki dana metryka przypisuje konkretnemu przypadkowi testowemu. Każda metryka (np. `Faithfulness`, `AnswerRelevancy`, `ContextualPrecision`) zwraca wynik w przedziale **0.0 – 1.0**, gdzie:

- **0.0** — najgorsza jakość (np. odpowiedź całkowicie nieoparta na kontekście),
- **1.0** — idealna jakość (np. 100% twierdzeń w odpowiedzi potwierdzonych kontekstem).

Score jest **obliczany automatycznie** przez framework ewaluacyjny (DeepEval, RAGAS, TruLens) na podstawie algorytmu przypisanego do metryki — najczęściej z użyciem podejścia **LLM-as-a-Judge** lub metryk embeddingowych.

> **Intuicja:** Score to „ocena na sprawdzianie" — wynik, jaki system RAG uzyskał w danym teście.

### Threshold — próg akceptacji

**Threshold** to **parametr konfiguracyjny** definiujący **minimalny akceptowalny wynik** (score) dla danej metryki. Pełni rolę **bramki jakościowej (quality gate)**:

- Jeśli `score >= threshold` → metryka **przeszła** (PASS ✅),
- Jeśli `score < threshold` → metryka **nie przeszła** (FAIL ❌).

Threshold ustawia inżynier na podstawie wymagań projektu. Domyślna wartość w DeepEval wynosi **0.5**, ale w praktyce dobiera się ją indywidualnie per metryka.

> **Intuicja:** Threshold to „próg zdawalności egzaminu" — minimalna nota, od której wynik traktujemy jako akceptowalny.

---

## Relacja Score ↔ Threshold — wizualizacja

```
Score metryki:  0.0 ─────────── 0.5 ─────────── 1.0
                │                │                │
                │   ❌ FAIL      │   ✅ PASS       │
                │                │                │
                └────────────────┘────────────────┘
                          ▲
                     Threshold = 0.5
                   (domyślna wartość)
```

Przesunięcie thresholdu w prawo (`0.7`, `0.9`) **podwyższa wymagania** — więcej przypadków testowych nie przejdzie. Przesunięcie w lewo (`0.3`) **obniża wymagania** — akceptujemy niższą jakość.

---

## Które metryki RAG mają Score i Threshold

Poniższa tabela pokazuje najważniejsze metryki stosowane w ewaluacji RAG, ich domyślne progi i rekomendowane wartości produkcyjne:

| Metryka | Co mierzy | Domyślny threshold | Zalecany threshold (produkcja) |
|---|---|---|---|
| **Faithfulness** | Czy odpowiedź opiera się na kontekście (anty-halucynacja) | 0.5 | **0.85 – 0.95** |
| **Answer Relevancy** | Czy odpowiedź odnosi się do pytania | 0.5 | 0.7 – 0.8 |
| **Contextual Precision** | Czy trafne fragmenty są wysoko w rankingu | 0.5 | 0.7 – 0.85 |
| **Contextual Recall** | Czy odzyskano wszystkie potrzebne fragmenty | 0.5 | 0.8 – 0.9 |
| **Contextual Relevancy** | Jaki % kontekstu jest istotny (sygnał vs szum) | 0.5 | 0.6 – 0.8 |
| **Answer Correctness** | Zgodność z wzorcową odpowiedzią (ground truth) | 0.5 | 0.7 – 0.85 |
| **Hallucination** | Wykrywanie halucynacji (odwrotność Faithfulness) | 0.5 | 0.1 – 0.2 (tu **niższy** = lepszy) |

> **Uwaga:** Dla metryki **Hallucination** logika jest odwrócona — wysoki score oznacza więcej halucynacji, więc threshold ustawia się nisko jako *maksimum* dopuszczalne.

---

## Przykład w kodzie — DeepEval

DeepEval to framework projektowany jako *„pytest dla LLM"*, który natywnie wspiera koncepcję threshold:

```python
from deepeval import assert_test
from deepeval.metrics import (
    FaithfulnessMetric,
    AnswerRelevancyMetric,
    ContextualRecallMetric,
)
from deepeval.test_case import LLMTestCase

# 1. Definicja metryk z RÓŻNYMI thresholdami
faithfulness = FaithfulnessMetric(threshold=0.9)      # surowy próg — halucynacje niedopuszczalne
relevancy    = AnswerRelevancyMetric(threshold=0.7)    # łagodniejszy próg
recall       = ContextualRecallMetric(threshold=0.85)  # retrieval musi być solidny

# 2. Przypadek testowy
test_case = LLMTestCase(
    input="Jaka jest polityka zwrotów?",
    actual_output="Produkty można zwracać w ciągu 14 dni od zakupu.",
    expected_output="Zwroty są możliwe do 14 dni.",
    retrieval_context=[
        "Polityka zwrotów: klient ma prawo zwrócić produkt w ciągu 14 dni."
    ],
)

# 3. Asercja — test przejdzie TYLKO gdy WSZYSTKIE metryki >= ich threshold
assert_test(test_case, [faithfulness, relevancy, recall])
```

### Co się dzieje pod spodem

Dla każdej metryki framework:
1. **Oblicza score** (0.0 – 1.0) — np. faithfulness = 0.95
2. **Porównuje z threshold** — 0.95 >= 0.9 → ✅ PASS
3. **Agreguje wyniki** — test przechodzi tylko gdy **wszystkie** metryki zdały

```
faithfulness:  score=0.95  threshold=0.9  → ✅ PASS
relevancy:     score=0.82  threshold=0.7  → ✅ PASS
recall:        score=0.78  threshold=0.85 → ❌ FAIL  ← retrieval za słaby!

Wynik testu: ❌ FAIL (recall poniżej progu)
```

---

## Strict Mode — tryb binarny

DeepEval oferuje dodatkowy tryb `strict_mode=True`, który **ignoruje threshold** i wymaga idealnego wyniku:

```python
faithfulness = FaithfulnessMetric(threshold=0.9, strict_mode=True)
# W strict mode: score musi być dokładnie 1.0, inaczej FAIL
# Threshold 0.9 jest ignorowany
```

Przydatne w scenariuszach zero-tolerance (np. systemy medyczne, prawne), gdzie **każda** halucynacja jest niedopuszczalna.

---

## Integracja z CI/CD — threshold jako bramka jakości

Główna wartość koncepcji threshold objawia się w automatyzacji:

```yaml
# Przykład: GitHub Actions
name: RAG Quality Gate
on: [push, pull_request]

jobs:
  eval:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run RAG evaluations
        run: deepeval test run tests/test_rag.py
      # Jeśli jakikolwiek score < threshold → build FAILS
      # Merge do main zablokowany
```

**Przepływ pracy:**

```
Zmiana promptu / modelu / chunkingu
        ↓
  Uruchom eval suite
        ↓
  Oblicz score per metryka
        ↓
  Score >= Threshold?  ──── Tak ──→ ✅ Merge dozwolony
        │
       Nie
        ↓
  ❌ Build FAIL → Napraw regresję
```

---

## Najczęstsze błędy przy ustawianiu thresholdów

| Błąd | Dlaczego jest problemem | Rozwiązanie |
|---|---|---|
| **Jeden threshold dla wszystkich metryk** | Faithfulness wymaga surowszego progu niż Answer Relevancy | Ustawiaj threshold per metryka |
| **Threshold = 0.5 na produkcji** | Domyślna wartość jest za niska — 50% jakości to za mało | Wyznacz baseline, następnie ustaw próg 10–15% powyżej |
| **Threshold bez baseline'u** | Arbitralny próg (np. 0.9) może być nieosiągalny lub za niski | Najpierw uruchom evals, poznaj rozkład wyników, potem ustaw próg |
| **Brak recalibracji** | Rozkład zapytań dryftuje w czasie | Cyklicznie weryfikuj thresholdy na produkcyjnych danych |
| **Ignorowanie rozróżnienia retrieval vs generation** | Nie wiesz, co naprawić | Ustawiaj osobne thresholdy dla metryk retrievalu i generacji |

---

## Podsumowanie

| Pojęcie | Czym jest | Analogia |
|---|---|---|
| **Score (Accuracy)** | Liczbowy wynik metryki (0.0 – 1.0) obliczany automatycznie | Ocena na egzaminie |
| **Threshold** | Minimalny akceptowalny score, ustawiany przez inżyniera | Próg zdawalności egzaminu |
| **PASS / FAIL** | Wynik porównania: `score >= threshold` | Zdał / nie zdał |

Razem tworzą system **eval-driven development**: metryki mierzą jakość RAG, a thresholdy automatyzują decyzję „czy to jest wystarczająco dobre, żeby wdrożyć". Bez thresholdów metryki są jedynie informatywne — z thresholdami stają się **bramkami jakości** w pipeline CI/CD.

---

## Powiązane notatki

- [Testowanie RAG — techniki, warstwy testów i frameworki](testowanie-rag-techniki-warstwy-frameworki.md) — pełna mapa testowania RAG, warstwy ewaluacji
- [LLMy a metryki do ich oceniania](opisz-temat-llmy-a-metryki-do-ich-oceniania.md) — metryki oceny LLM (BLEU, ROUGE, BERTScore, LLM-as-a-Judge)
- [Pytania rekrutacyjne RAG](pytania-rekrutacyjne-rag.md) — architektura RAG, chunking, retrieval
- [Kontrowersje wokół RAG](kontrowersje-wokół-rag.md) — kiedy i dlaczego RAG zawodzi
- [Benchmarki, ewaluacja, koszt, skalowalność ML/AI](benchmarki-ewaluacja-koszt-skalowalnosc-ml-ai.md) — benchmarki i ewaluacja w szerszym kontekście
