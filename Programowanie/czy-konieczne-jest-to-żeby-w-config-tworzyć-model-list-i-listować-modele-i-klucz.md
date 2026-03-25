# czy konieczne jest to żeby w config tworzyć model_list i listować modele i klucz

**Data:** 22 gru 2025, 18:33:20 CET

---

**User:**

czy konieczne jest to żeby w config tworzyć model_list i listować modele i klucze do nich z których chcę korzystać? może da się to ustawić tak żeby przechwytywał zapytania do wszystkich llm?

---

**Gemini:**

Nie jest to bezwzględnie konieczne, ale stopień automatyzacji zależy od tego, jak bardzo chcesz ingerować w konfigurację sieciową systemu oraz czy zależy Ci na automatycznym wyliczaniu kosztów w USD (co wymaga mapowania modelu do cennika).

Możesz podejść do tego problemu na trzy sposoby, od najbardziej elastycznego po najbardziej "przezroczysty".

### 1. LiteLLM w trybie Dynamic Model Passthrough

W tym trybie nie musisz listować każdego modelu w `config.yaml`. LiteLLM może działać jako "przekaźnik", który przyjmuje dowolną nazwę modelu od klienta i próbuje ją dopasować do dostawcy na podstawie prefiksu.

Jeśli włączysz odpowiednie flagi, LiteLLM wyśle zapytanie do dostawcy, używając klucza przekazanego bezpośrednio przez Twoją aplikację (Client-side keys) lub klucza nadrzędnego.

**Konfiguracja `config.yaml` dla dynamicznego wykrywania:**

```
general_settings:
  allow_user_managed_keys: true # Pozwala aplikacji wysyłać własny klucz API w nagłówku
  drop_params: true            # Usuwa parametry nieobsługiwane przez dany model

litellm_settings:
  set_verbose: false
```

**Wywołanie z poziomu aplikacji (Python):**

```
import openai

client = openai.OpenAI(
    api_key="your-actual-provider-key", # Klucz przekazywany przez proxy do dostawcy
    base_url="http://localhost:4000"
)

# Możesz użyć dowolnego modelu, nawet jeśli nie ma go w config.yaml
# LiteLLM użyje prefiksu (np. "anthropic/") do rozpoznania routingu
response = client.chat.completions.create(
    model="anthropic/claude-3-5-sonnet-20240620",
    messages=[{"role": "user", "content": "Hello"}]
)
```

### 2. Przechwytywanie globalne (Transparent Proxy / DNS Spoofing)

Jeśli nie chcesz zmieniać `base_url` w kodzie każdej aplikacji, możesz wymusić na poziomie systemu operacyjnego, aby zapytania do np. `api.openai.com` trafiały do Twojego serwisu LiteLLM.

**Krok 1: Przekierowanie ruchu w `/etc/hosts`**
Możesz przekierować domeny dostawców na `localhost`:

```
127.0.0.1 api.openai.com
127.0.0.1 api.anthropic.com
```

**Krok 2: SSL Termination**
To jest najtrudniejsza część. Ponieważ API komunikują się przez HTTPS, LiteLLM musiałby posiadać certyfikaty SSL dla tych domen, a Twój system musi ufać Twojemu lokalnemu CA (Certificate Authority). Bez tego biblioteki (jak `openai-python`) rzucą błąd `SSL: CERTIFICATE_VERIFY_FAILED`.

To rozwiązanie jest zazwyczaj implementowane przy użyciu narzędzi typu **mitmproxy** lub profesjonalnych API Gateways (np. Kong, Tyk), ale dla celów zliczania tokenów w developmentcie jest to często "overkill".

### 3. Zbieranie danych bez listowania modeli (Wildcard Mapping)

Możesz skonfigurować LiteLLM tak, aby obsługiwał "wszystko od danego dostawcy" za pomocą jednego wpisu, co eliminuje potrzebę dodawania każdego nowego modelu z osobna.

```
model_list:
  - model_name: "openai/*" # Wildcard dla wszystkich modeli OpenAI
    litellm_params:
      model: "openai/*"
      api_key: "os.environ/OPENAI_API_KEY"
  - model_name: "anthropic/*"
    litellm_params:
      model: "anthropic/*"
      api_key: "os.environ/ANTHROPIC_API_KEY"
```

### Kluczowe wyzwania przy braku definicji modeli:

- **Zliczanie kosztów:** LiteLLM posiada wewnętrzną bazę danych `model_prices_and_context_window.json`. Jeśli użyjesz modelu, którego nie ma na liście (i nie jest on rozpoznany przez wildcard), narzędzie zliczy tokeny (na podstawie odpowiedzi z API), ale może nie być w stanie przypisać im wartości dolarowej, dopóki nie zdefiniujesz stawki.
- **Tokenizacja:** Różne modele używają różnych algorytmów (np. GPT-4o używa `o200k_base`, starsze `cl100k_base`). Jeśli LiteLLM nie wie, co to za model, może mieć problem z dokładnym przeliczeniem tokenów *przed* wysłaniem zapytania (tzw. pre-call estimation), choć po otrzymaniu odpowiedzi z API (która zazwyczaj zawiera pole `usage`) dane będą poprawne.

### Rekomendacja techniczna

Zamiast pełnej interceptacji sieciowej (która psuje weryfikację certyfikatów SSL), najlepiej zastosować **LiteLLM z wildcardami** (Punkt 3) oraz ustawić zmienną środowiskową w systemie:
`export OPENAI_BASE_URL="http://localhost:4000/v1"`

Większość nowoczesnych bibliotek (OpenAI SDK, LangChain, LlamaIndex) automatycznie sprawdza tę zmienną środowiskową i kieruje ruch do Twojego lokalnego serwisu bez zmiany ani jednej linii kodu w aplikacji.

Czy chcesz, abym przygotował skrypt bashowy, który zautomatyzuje konfigurację tych zmiennych środowiskowych i certyfikatów dla serwisu systemd?