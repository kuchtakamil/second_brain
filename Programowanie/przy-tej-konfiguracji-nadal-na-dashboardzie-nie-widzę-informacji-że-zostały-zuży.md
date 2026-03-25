# Przy tej konfiguracji nadal na dashboardzie nie widzę informacji że zostały zuży

**Data:** 24 gru 2025, 17:04:03 CET

---

**User:**

Przy tej konfiguracji nadal na dashboardzie nie widzę informacji że zostały zużyte jakieś tokeny i requesty.
Używam ChatGoogleGenerativeAI.
Gdy dla testów użyłem parametru base_url="http://localhost:4000" requesty wisiały.

---

**Gemini:**

Problem z `ChatGoogleGenerativeAI` (z biblioteki `langchain-google-genai`) wynika z faktu, że pod spodem korzysta ona z oficjalnego SDK Google (`google-generativeai`), które ignoruje standardowe zmienne środowiskowe takie jak `GOOGLE_API_BASE`. Ponadto, SDK Google używa specyficznego protokołu (często gRPC lub REST ze specyficznym mapowaniem ścieżek), który różni się od standardu OpenAI, na którym bazuje domyślnie LiteLLM Proxy.

Oto jak poprawnie skonfigurować to połączenie, aby uniknąć "wiszenia" requestów i zapewnić monitoring tokenów.

### 1. Dlaczego requesty "wiszą"?

Jeśli podajesz `base_url="http://localhost:4000"`, biblioteka próbuje wysłać zapytanie w formacie Google do endpointu, który LiteLLM interpretuje jako OpenAI-compatible. Następuje niedopasowanie ścieżek (np. `/v1beta/...` vs `/v1/chat/completions`).

### 2. Rozwiązanie: Użycie `ChatOpenAI` jako klienta dla Gemini

Najskuteczniejszym sposobem na monitorowanie Gemini przez LiteLLM w LangChain jest wykorzystanie klasy `ChatOpenAI`. LiteLLM został zaprojektowany tak, aby przyjmować ujednolicony format OpenAI i tłumaczyć go na format Google.

**Przykład w Python:**

```
from langchain_openai import ChatOpenAI

# LiteLLM przetłumaczy format OpenAI na Gemini dzięki prefiksowi gemini/
llm = ChatOpenAI(
    model="gemini/gemini-1.5-pro", # Prefiks jest kluczowy dla routingu w LiteLLM
    api_key="sk-whatever",         # Klucz może być dowolny, LiteLLM użyje tego z config.yaml
    base_url="http://localhost:4000/v1",
    temperature=0
)

response = llm.invoke("Test request")
print(response.content)
```

### 3. Poprawka w `config.yaml` dla Gemini

Upewnij się, że w konfiguracji LiteLLM masz poprawnie zdefiniowane mapowanie, aby proxy wiedziało, jak obsłużyć zapytanie przychodzące z prefiksem `gemini/`.

```
model_list:
  - model_name: "gemini/*"
    litellm_params:
      model: "gemini/*" # Dynamiczne przekazanie modelu do Google AI Studio
      api_key: "os.environ/GEMINI_API_KEY"

general_settings:
  database_url: "postgresql://litellm_user:password@localhost:5432/litellm_db"
  master_key: "sk-admin-1234"
```

### 4. Wymuszenie logowania tokenów (Streaming)

Jeśli używasz streamingu, LiteLLM czasem może mieć problem z raportowaniem tokenów, jeśli dostawca (Google) nie przesyła ich w ostatnim chunku. Dodaj poniższe ustawienie w `config.yaml`:

```
litellm_settings:
  stream_response_with_usage_batch: true
  include_usage_with_streaming: true
```

### 5. Diagnostyka "Wiszących" połączeń

Jeśli nadal masz problem z połączeniem, wykonaj test diagnostyczny za pomocą `curl`, aby wykluczyć błąd w kodzie Python:

```
curl --location 'http://localhost:4000/v1/chat/completions' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer sk-admin-1234' \
--data '{
    "model": "gemini/gemini-1.5-flash",
    "messages": [
        {"role": "user", "content": "Hello, this is a test"}
    ]
}'
```

**Jeśli `curl` zadziała, a LangChain nie:**

1. Sprawdź, czy w środowisku, w którym uruchamiasz LangChain, nie ma ustawionych zmiennych `http_proxy` lub `https_proxy`, które mogłyby kierować ruch poza `localhost`.
2. Upewnij się, że używasz `ChatOpenAI` zamiast `ChatGoogleGenerativeAI`. Ta druga klasa jest zbyt sztywno powiązana z endpointami Google i próba jej "oszukania" przez `base_url` często kończy się timeoutem.

### 6. Podgląd logów w czasie rzeczywistym

Uruchom monitoring logów i sprawdź, co dzieje się w momencie wysyłania requestu:

```
journalctl -u litellm -f -n 100
```

Szukaj komunikatów:

- `POST /v1/chat/completions HTTP/1.1` – czy request w ogóle dociera?
- `litellm.main:DEBUG: self.model_prices_and_context_window` – czy LiteLLM rozpoznał model i wie, jak policzyć tokeny?

Jeśli w logach widzisz `404 Not Found` lub `401 Unauthorized`, oznacza to błąd w routingu wewnątrz `config.yaml` lub brak klucza API do Google w zmiennych środowiskowych serwisu.