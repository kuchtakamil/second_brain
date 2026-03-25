# Deep understanding of production ML best practice

**Data:** 5 lut 2026, 17:28:34 CET

---

**User:**

W ofercie pracy jest wymaganie.   Deep understanding of production ML best practices (training/serving skew, offline/online parity, reproducibility, data quality, monitoring/observability) .      Jakie tematy powinienem zgłębić żeby się do rozmowy przygotować?

---

**Gemini:**

Aby przygotować się do rozmowy kwalifikacyjnej opartej na tych wymaganiach, należy zgłębić techniczne aspekty architektury systemów ML oraz cyklu życia modelu (MLOps). Poniżej znajduje się zestawienie kluczowych obszarów wraz z konkretnymi koncepcjami i narzędziami.

---

## 1. Training/Serving Skew & Offline/Online Parity

Ten obszar dotyczy różnic między zachowaniem modelu podczas trenowania a jego działaniem na produkcji.

- **Feature Engineering Consistency:** Zrozumienie, jak zapobiegać duplikacji logiki w Pythonie (do treningu) i np. w C++/Java/SQL (do serwowania). Rozwiązaniem jest stosowanie **Feature Stores** (np. Feast, Tecton), które zapewniają jeden punkt prawdy dla cech.
- **Data Leakage (Leakage od strony czasu):** Metody walidacji krzyżowej opartej na czasie (**Time-series split**), aby uniknąć używania danych z "przyszłości" podczas treningu.
- **Schema Validation:** Implementacja rygorystycznych kontraktów danych (np. Protobuf, Pydantic) w celu zapewnienia, że wejście modelu produkcyjnego jest identyczne ze strukturą danych treningowych.
- **Point-in-time Correctness:** Zdolność do odtworzenia stanu bazy danych dokładnie z momentu, w którym wystąpiło dane zdarzenie historyczne.

## 2. Reproducibility

Zdolność do powtórzenia eksperymentu i uzyskania identycznych wyników jest fundamentem profesjonalnego ML.

- **Artifact Management:** Przechowywanie nie tylko wag modelu, ale także hiperparametrów, wersji kodu i konkretnego snapshotu danych (narzędzia: **MLflow**, **DVC**, **Weights & Biases**).
- **Environment Isolation:** Wykorzystanie **Docker** do konteneryzacji całego stacku oraz definiowanie precyzyjnych zależności (np. `poetry.lock`, `conda-lock`).
- **Deterministic Operations:** Znajomość flag deterministycznych w bibliotekach takich jak PyTorch czy TensorFlow (np. `torch.use_deterministic_algorithms(True)`) oraz zarządzanie ziarnem losowości (**seed**) we wszystkich modułach (numpy, random, cuda).
- **Code Versioning:** Wykorzystanie Git do tagowania konkretnych wydań modeli (Model Registry).

## 3. Data Quality

W systemach produkcyjnych jakość danych jest ważniejsza niż architektura samego modelu.

- **Data Profiling & Testing:** Automatyczne sprawdzanie statystyk danych wejściowych. Narzędzia takie jak **Great Expectations**, **Pandera** czy **TFX Data Validation**.
- **Distribution Shift:** Zrozumienie, kiedy dane produkcyjne zaczynają odbiegać od treningowych.
- **Data Lineage:** Śledzenie pochodzenia danych (narzędzia: **OpenLineage**, **Amundsen**) – skąd dane pochodzą, jakie transformacje przeszły i które modele z nich korzystają.
- **Unit Tests for Data:** Pisanie testów jednostkowych sprawdzających np. zakresy wartości (age > 0), brakujące nulle czy unikalność kluczy.

## 4. Monitoring & Observability

Monitoring ML wykracza poza standardowe metryki IT (CPU/RAM).

- **Model Drift Monitoring:**
  - **Data Drift:** Zmiana rozkładu cech wejściowych ($P(X)$). Metody: test Kołmogorowa-Smirnowa, Population Stability Index (PSI).
  - **Concept Drift:** Zmiana relacji między cechami a celem ($P(Y|X)$). Sygnał, że model wymaga retrainingu.
- **Performance Decay:** Śledzenie metryk biznesowych i ML-owych (Precision, Recall, F1, RMSE) w czasie rzeczywistym.
- **Model Explainability (XAI) w produkcji:** Generowanie snapshotów **SHAP** lub **LIME** dla predykcji produkcyjnych w celu debugowania błędnych decyzji modelu.
- **System Health:** Latency (p95, p99), throughput, error rates (4xx, 5xx). Integracja z **Prometheus** i **Grafana**.

---

## Zaawansowane wzorce projektowe (Deep Dive)

| Temat                         | Opis techniczny                                                                                                               |
| ----------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| **Shadow Deployment**         | Równoległe uruchomienie nowego modelu na produkcji bez zwracania jego wyników do klienta (porównywanie z modelem "Champion"). |
| **Canary Releases**           | Stopniowe przekierowywanie ruchu (np. 5% użytkowników) do nowej wersji modelu.                                                |
| **Continuous Training (CT)**  | Automatyzacja potoku (pipeline), która wyzwala trening modelu po wykryciu dryfu danych lub pojawieniu się nowych etykiet.     |
| **Online Inference vs Batch** | Kiedy stosować API (REST/gRPC), a kiedy przetwarzanie wsadowe (Spark/Flink) pod kątem kosztów i opóźnień.                     |

### Przykład kodu: Walidacja danych (Pandera)

Warto znać paradygmat definiowania schematów dla danych produkcyjnych:

```
import pandera as pa
from pandera.typing import Series

class ModelInputSchema(pa.SchemaModel):
    user_age: Series[int] = pa.Field(ge=18, le=120)
    transaction_amount: Series[float] = pa.Field(gt=0)
    user_country: Series[str] = pa.Field(isin=["PL", "US", "DE"])

    @pa.check("transaction_amount")
    def check_outliers(cls, amount: Series[float]) -> Series[bool]:
        return amount < 1_000_000

# Usage in production pipeline
def predict(data):
    validated_data = ModelInputSchema.validate(data)
    # proceed to inference
```

Czy chciałbyś, abym przygotował listę pytań rekrutacyjnych, które mogą paść w kontekście konkretnie Monitoring/Observability?