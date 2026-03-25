# szukam narzędzia które mogłoby monitorować i zliczać wykorzystane tokeny wysyłan

**Data:** 22 gru 2025, 15:53:31 CET

---

**User:**

szukam narzędzia które mogłoby monitorować i zliczać wykorzystane tokeny wysyłane i odbierane poprzez różne API których używam do komunikacji z różnymi modelami

---

**Gemini:**

Wybór odpowiedniego narzędzia do monitorowania zużycia tokenów zależy od Twojej architektury (czy chcesz używać zewnętrznego proxy, czy biblioteki wewnątrz kodu) oraz skali projektu. Poniżej przedstawiam zestawienie najbardziej zaawansowanych rozwiązań, które wspierają wiele modeli (OpenAI, Anthropic, Google, Azure, AWS Bedrock i inne) oraz umożliwiają precyzyjne zliczanie kosztów.

### 1. LiteLLM (Proxy & Python Library)

Jest to obecnie najpopularniejszy standard "pomiędzy" Twoją aplikacją a wieloma dostawcami API. LiteLLM działa jako uniwersalny translator.

- **Model:** Proxy lub biblioteka SDK.
- **Zalety:** \* Obsługuje ponad 100 dostawców LLM.
  - Automatycznie mapuje odpowiedzi różnych API na ujednolicony format OpenAI (w tym obiekt `usage`).
  - Posiada wbudowany serwer proxy, który loguje zużycie do baz SQL (PostgreSQL), Redis lub narzędzi observability.
  - **Cost Tracking:** Pozwala na definiowanie budżetów na poziomie klucza API lub użytkownika.

**Przykład konfiguracji LiteLLM Proxy (`config.yaml`):**

```
model_list:
  - model_name: gpt-4
    litellm_params:
      model: openai/gpt-4
      api_key: os.environ/OPENAI_API_KEY
  - model_name: claude-3
    litellm_params:
      model: anthropic/claude-3-opus-20240229
      api_key: os.environ/ANTHROPIC_API_KEY

general_settings:
  master_key: sk-1234
  database_url: postgresql://user:password@localhost:5432/litellm
```

### 2. Helicone (AI Gateway)

Helicone to dedykowane rozwiązanie typu **Gateway**, które skupia się na observability i monitorowaniu kosztów bez konieczności dużej modyfikacji kodu.

- **Model:** Proxy (wymiana `baseURL`).
- **Funkcje:**
  - **Zliczanie tokenów w czasie rzeczywistym:** Automatycznie parsuje odpowiedzi i wyciąga dane o tokenach.
  - **Caching:** Możliwość cachowania odpowiedzi, co redukuje koszty tokenów przy powtarzalnych zapytaniach.
  - **Retries & Fallbacks:** Automatyczne przełączanie na inny model przy błędach, przy zachowaniu ciągłości monitoringu.
- **Implementacja:** Zmieniasz tylko `base_url` w swoim kliencie API na adres serwera Helicone.

### 3. Langfuse (Open-Source Observability)

Jeśli szukasz narzędzia do pełnego cyklu życia aplikacji (nie tylko liczenia tokenów, ale i śledzenia całych śladów/trace'ów), Langfuse jest najlepszym wyborem open-source.

- **Model:** SDK / Integration.
- **Kluczowe cechy:**
  - **Detailed Cost Tracking:** Importuje cenniki modeli i na bieżąco oblicza koszt każdego zapytania w USD.
  - **Tracing:** Pozwala zobaczyć, ile tokenów zużył konkretny "step" w złożonym agencie lub łańcuchu RAG.
  - **OpenTelemetry:** Pełne wsparcie dla standardów OTel.

### 4. Portkey (Enterprise AI Gateway)

Narzędzie klasy enterprise, które kładzie duży nacisk na zarządzanie limitami (Rate Limiting) i budżetami.

- **Model:** AI Gateway.
- **Zaawansowane funkcje:**
  - **Virtual Keys:** Możesz tworzyć wirtualne klucze dla różnych zespołów/klientów z przypisanymi limitami tokenów.
  - **Logowanie:** Eksport danych o zużyciu do hurtowni danych (BigQuery, Snowflake).
  - **Unified API:** Podobnie jak LiteLLM, oferuje jeden endpoint dla wszystkich modeli.

---

### Porównanie techniczne

| Cecha | LiteLLM | Helicone | Langfuse | Portkey |
| --- | --- | --- | --- | --- |
| **Typ** | Library / Proxy | Gateway | Observability Platform | Gateway |
| **Self-hosting** | Tak (Docker) | Tak | Tak (Docker) | Nie (Cloud-first) |
| **Główny focus** | Interoperacyjność | Monitoring & Caching | Tracing & Evals | Control & Governance |
| **Obsługa wielu API** | Ekstremalnie szeroka | Bardzo szeroka | Przez SDK/Integracje | Bardzo szeroka |

---

### Implementacja własna (Advanced: OpenTelemetry)

Jeśli budujesz infrastrukturę korporacyjną, najlepszym podejściem jest wykorzystanie standardu **OpenTelemetry (OTEL)** z rozszerzeniami dla GenAI. Pozwala to na wysyłanie metryk o tokenach do narzędzi takich jak Datadog, Grafana czy New Relic.

Możesz użyć biblioteki `openlit` (Open Source), która automatycznie instrumentuje najpopularniejsze SDK:

```
import openlit

# Automatyczna instrumentacja dla OpenAI, Anthropic, Bedrock itp.
openlit.init(
    otlp_endpoint="http://localhost:4318", # Twój kolektor OTel
    collect_metrics=True
)

# Twoje standardowe wywołania API
from openai import OpenAI
client = OpenAI()

response = client.chat.completions.create(
  model="gpt-4",
  messages=[{"role": "user", "content": "Analyze this code."}]
)
# Dane o tokenach (usage.input_tokens, usage.output_tokens) 
# zostaną automatycznie wysłane jako metryki OTel.
```

### Na co zwrócić uwagę (Problemy techniczne)

1. **Różnice w tokenizacji:** Pamiętaj, że modele od różnych dostawców używają różnych tokenizerów (np. OpenAI używa `tiktoken`/`cl100k_base`, Anthropic ma własny model). Narzędzia typu Gateway (Helicone, LiteLLM) same dbają o to, by raportować poprawne liczby, pobierając je z metadanych odpowiedzi API.
2. **Streaming:** Monitorowanie tokenów przy streamingu (`stream=True`) jest trudniejsze, ponieważ API często nie zwraca obiektu `usage` w ostatnim fragmencie (chunk). LiteLLM i Helicone rozwiązują to poprzez symulację tokenizacji lub wymuszanie parametru `include_usage` tam, gdzie jest to wspierane.
3. **Metadata:** Zawsze taguj swoje zapytania (np. `user_id`, `project_id`). Większość wymienionych narzędzi pozwala na przekazywanie metadanych w nagłówkach lub ciele zapytania, co umożliwia późniejsze filtrowanie kosztów.

Czy chciałbyś, abym przygotował konkretny przykład wdrożenia LiteLLM Proxy w Twojej infrastrukturze (np. przy użyciu Dockera)?