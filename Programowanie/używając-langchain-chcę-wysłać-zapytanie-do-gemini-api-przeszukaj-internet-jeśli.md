# Używając LangChain chcę wysłać zapytanie do Gemini API. Przeszukaj internet jeśl

**Data:** 26 lis 2025, 12:46:05 CET

---

**User:**

Używając LangChain chcę wysłać zapytanie do Gemini API. Przeszukaj internet jeśli konieczne żeby przedstawić najbardziej aktualny sposób jak to zrobić.

---

**Gemini:**

Aby profesjonalnie zintegrować LangChain z Gemini API (Google Generative AI) w 2025 roku, należy korzystać z dedykowanego pakietu partnerskiego `langchain-google-genai`. Jest to najbardziej aktualne i wspierane rozwiązanie, zastępujące starsze wrappery `ChatVertexAI` (dla Google Cloud) czy ogólne implementacje HTTP.

Poniżej przedstawiam kompletny, techniczny przewodnik obejmujący instalację, podstawowe użycie, konfigurację bezpieczeństwa (Safety Settings), obsługę multimodalną (obraz + tekst) oraz streaming.

### 1. Instalacja i Konfiguracja Środowiska

Wymagane są pakiety `langchain-google-genai` oraz `langchain-core`.

```
pip install -U langchain-google-genai langchain-core pillow
```

Przed rozpoczęciem upewnij się, że posiadasz klucz API z Google AI Studio.

```
import getpass
import os

# Securely set the API key if not already in environment variables
if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google API Key: ")
```

### 2. Inicjalizacja Modelu i Proste Wywołanie

Podstawową klasą jest `ChatGoogleGenerativeAI`. Obecne standardy zalecają modele z serii `gemini-1.5-pro` (dla złożonego rozumowania) lub `gemini-1.5-flash` (dla szybkości i niskich kosztów).

```
from langchain_google_genai import ChatGoogleGenerativeAI

# Initialize the model
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0.7,
    max_retries=2,
    # verbose=True # Uncomment for debugging
)

# Direct invocation
response = llm.invoke("Explain the concept of recursion in programming concisely.")
print(f"Content: {response.content}")
print(f"Usage Metadata: {response.response_metadata.get('usage_metadata')}")
```

### 3. Zaawansowana Implementacja (LCEL Chains & System Prompts)

W produkcyjnych aplikacjach LangChain rzadko wywołuje się model bezpośrednio. Należy używać **LangChain Expression Language (LCEL)**, łącząc `ChatPromptTemplate` z modelem i parserem wyjścia.

```
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. Define a structured prompt with system instructions
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a senior software architect specializing in distributed systems. Answer technically."),
    ("human", "{question}")
])

# 2. Define the output parser
output_parser = StrOutputParser()

# 3. Create the Chain using LCEL (pipe syntax)
chain = prompt | llm | output_parser

# 4. Invoke the chain
result = chain.invoke({"question": "What are the trade-offs between CAP theorem components?"})
print(result)
```

### 4. Konfiguracja Ustawień Bezpieczeństwa (Safety Settings)

Gemini posiada wbudowane filtry treści. W zastosowaniach biznesowych często konieczne jest jawne nadpisanie domyślnych ustawień (np. aby zezwolić na przetwarzanie treści medycznych lub prawnych, które mogą być błędnie oflagowane).

```
from langchain_google_genai import ChatGoogleGenerativeAI, HarmBlockThreshold, HarmCategory

# Define specific safety settings to override defaults
safety_settings = {
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH,
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}

llm_safe = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    safety_settings=safety_settings
)

response = llm_safe.invoke("Describe a fictional battle scene in a fantasy novel.")
print(response.content)
```

### 5. Obsługa Multimodalna (Wizja)

Gemini natywnie obsługuje obrazy. W LangChain przekazujemy je jako listę treści w `HumanMessage`.

```
import base64
import requests
from langchain_core.messages import HumanMessage

# Helper to encode image from URL
def encode_image(image_url):
    return base64.b64encode(requests.get(image_url).content).decode('utf-8')

image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
image_data = encode_image(image_url)

# Construct a multimodal message
message = HumanMessage(
    content=[
        {"type": "text", "text": "Analyze this image. What is the weather like and what mood does it convey?"},
        {
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}
        }
    ]
)

# Invoke model with vision input
vision_llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash") # Flash is excellent for vision tasks
vision_response = vision_llm.invoke([message])
print(vision_response.content)
```

### 6. Streaming (Strumieniowanie Odpowiedzi)

Dla poprawy UX (User Experience) przy długich generacjach, użyj metody `.stream()`.

```
print("Streaming response: ", end="", flush=True)

for chunk in llm.stream("Write a boilerplate Python script for a REST API using FastAPI."):
    print(chunk.content, end="", flush=True)
```

### Kluczowe uwagi techniczne:

- **Wersjonowanie:** Używaj modelu `gemini-1.5-...`. Starsze modele `gemini-pro` (1.0) mają mniejsze okno kontekstowe i gorsze zdolności rozumowania.
- **Batching:** `ChatGoogleGenerativeAI` obsługuje asynchroniczne wywołania (`abatch`, `ainvoke`), co jest kluczowe przy przetwarzaniu dużej ilości danych równolegle.
- **Function Calling:** Jeśli potrzebujesz strukturalnych danych (JSON), użyj metody `.with_structured_output(PydanticModel)` dostępnej w najnowszych wersjach LangChain dla Gemini.

Czy chcesz, abym przedstawił przykład użycia Gemini z własnymi narzędziami (Tool Calling) w LangChain?

... [Multimodal AI with LangChain (Full Python Code Included)](https://www.youtube.com/watch?v=I3UaV7u4JBA) ...

Wybrane wideo zawiera praktyczny tutorial implementacji multimodalnej (tekst + obraz) przy użyciu LangChain, co bezpośrednio uzupełnia sekcję nr 5 mojej odpowiedzi.