# jaka zmienna systemowa powinna być ustawiona dla gemini?

**Data:** 24 gru 2025, 16:27:36 CET

---

**User:**

jaka zmienna systemowa powinna być ustawiona dla gemini?

---

**Gemini:**

Dla modeli Google Gemini sprawa jest nieco bardziej złożona niż w przypadku OpenAI, ponieważ Google korzysta z dwóch różnych ścieżek dostępu (Google AI SDK oraz Vertex AI na platformie GCP).

Większość nowoczesnych bibliotek (takich jak LangChain, LlamaIndex czy nowsze wrappery SDK), które mają współpracować z proxy takim jak LiteLLM, respektuje następujące zmienne:

### 1. Podstawowa zmienna dla Google AI SDK

Najczęściej stosowaną zmienną dla standardowych modeli Gemini (tych używających klucza API z Google AI Studio) jest:

- **`GOOGLE_API_BASE`**

W Twoim pliku `/etc/profile.d/llm_proxy.sh` powinieneś dodać:

```
export GOOGLE_API_BASE="http://localhost:4000"
```

### 2. Alternatywna zmienna (często używana w środowisku Python)

Niektóre biblioteki szukają specyficznego prefiksu "Gemini":

- **`GEMINI_API_BASE`**

Dla pełnej kompatybilności warto ustawić obie:

```
export GEMINI_API_BASE="http://localhost:4000"
```

---

### Jak zaktualizować Twoją konfigurację?

Aby dołączyć Gemini do mechanizmu automatycznego przechwytywania, wykonaj poniższe kroki:

#### Krok 1: Edycja profilu systemowego

Otwórz plik:

```
sudo nano /etc/profile.d/llm_proxy.sh
```

Zaktualizuj go do poniższej postaci:

```
export OPENAI_BASE_URL="http://localhost:4000/v1"
export ANTHROPIC_BASE_URL="http://localhost:4000"
export GOOGLE_API_BASE="http://localhost:4000"
export GEMINI_API_BASE="http://localhost:4000"
```

#### Krok 2: Odświeżenie sesji

Pamiętaj, aby przeładować zmienne w bieżącej konsoli:

```
source /etc/profile.d/llm_proxy.sh
```

---

### Uwagi techniczne dotyczące Gemini

1. **Format ścieżki:** O ile OpenAI niemal zawsze wymaga `/v1` na końcu adresu, o tyle implementacja Google w LiteLLM często oczekuje "czystego" adresu hosta (`http://localhost:4000`). LiteLLM sam zajmie się translacją ścieżek na format `/v1beta/models/...`, którego wymaga Google.
2. **Vertex AI (Enterprise):** Jeśli używasz Gemini poprzez **Google Cloud Vertex AI** (zamiast kluczy z AI Studio), zmienne te mogą nie zadziałać automatycznie, ponieważ Vertex AI korzysta z gRPC lub specyficznych endpointów regionalnych. W takim przypadku musiałbyś ustawić:
   - `VERTEX_API_BASE="http://localhost:4000"`
3. **Biblioteka `google-generativeai`:** Oficjalna biblioteka Pythona od Google (`google.generativeai`) jest dość oporna na zmiany `base_url` przez zmienne środowiskowe. Jeśli zauważysz, że zapytania z tej konkretnej biblioteki omijają proxy, będziesz musiał w kodzie jawnie skonfigurować klienta:

   ```
   import google.generativeai as genai
   genai.configure(api_key="your_key", client_options={"api_endpoint": "localhost:4000"})
   ```

**Następny krok:** Czy chcesz, abym sprawdził w dokumentacji LiteLLM, jak dokładnie skonfigurować "Wildcard" w `config.yaml` dla Vertex AI, jeśli planujesz korzystać z wersji Enterprise?