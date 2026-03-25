# Strukturyzowane wyjście (Structured Output) i szablony Jinja2 w LangChain / LangGraph

W kontekście budowania nowoczesnych, przewidywalnych aplikacji opartych na LLM (oraz złożonych agentów w LangGraph), bardzo często zachodzi potrzeba, aby model zwracał dane w ściśle określonym formacie (np. obiekty JSON, słowniki, modele Pydantic), a nie jako luźny tekst.

Służy do tego proces nazywany strukturyzacją wyjścia (Structured Output).

## Co robi `self._llm.with_structured_output`?

*(Uwaga: w kodzie czasem używany jest w nazewnictwie skrót myślowy `with_structured` od metody `with_structured_output`, która jest standardowym interfejsem LangChain).*

Metoda `.with_structured_output(schema)` to wbudowana w klasy modeli czatowych LangChain (np. `ChatOpenAI`, `ChatAnthropic`) potężna metoda narzędziowa. Reprezentuje ona "owrapowanie" (wrapper) podstawowego wywołania LLMa tak, aby **wymusić na nim wygenerowanie odpowiedzi jednoznacznie zgodnej z zadanym schematem**.

Zamiast polegać na tak zwanym *Prompt Engineeringu* polegającym na krzyczeniu na model ("ZWRÓĆ TYLKO PRAWIDŁOWY JSON BEZ ZNACZNIKÓW MARKDOWN!"), metoda ta "pod maską" wykorzystuje natywne możliwości providerów AI (np. **Tool Calling / Function Calling** w OpenAI czy wbudowany **JSON Mode**).

Zwracany z modelu obiekt nie jest klasycznym obiektem `AIMessage` ze zmienną `.content` zawierającą tekst, ale **gotowym zinstancjonowanym obiektem w Pythonie** (np. obiektem Pydantic lub słownikiem typu TypedDict).

## Jak otrzymywane są ustrukturyzowane odpowiedzi? (Krok po kroku)

Proces działania ustrukturyzowanego wyjścia składa się z czterech etapów:

1. **Definicja schematu**: Programista definiuje strukturę oczekiwanych danych. Najczęściej używa się do tego biblioteki **Pydantic** ze względu na ścisłą walidację typów, ale wspierane są też słowniki (np. `TypedDict`) lub surowe schematy JSON.
2. **Bindowanie (Wiązanie)**: Metoda `llm.with_structured_output(Schemat)` w tle analizuje podaną klasę Pydantic i konwertuje ją na tzw. schemat funkcji (OpenAI Function Schema) zrozumiały dla dostawcy LLM.
3. **Wywołanie (Invoke)**: Po stronie serwera AI model połączony jest z tym schematem – API niejako "wymusza" na nim użycie dostarczonego strukturalnie "narzędzia" do zbudowania odpowiedzi.
4. **Parsowanie i Walidacja (LangChain SDK)**: Model zwraca odpowiedź (zazwyczaj string JSON arg w ToolCall). LangChain przechwytuje go, weryfikuje poprawność zdefiniowanego schematu (np. czy wszystkie wymagane pola istnieją i zgadzają się ich typy), a następnie parsuje z powrotem do zdefiniowanego przez programistę schematu Pydantic. Zwraca bezpieczny obiekt w locie.

### Przykład w kodzie

```python
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

# 1. Zdefiniowanie pożądanego schematu odpowiedzi
class UserProfile(BaseModel):
    name: str = Field(description="Pełne imię i nazwisko użytkownika")
    age: int = Field(description="Wiek użytkownika (całkowity)")
    interests: list[str] = Field(description="Lista zainteresowań")

class Agent:
    def __init__(self):
        # Inicjalizacja standardowego modelu
        base_llm = ChatOpenAI(model="gpt-4o", temperature=0)
        
        # 2. Wymuszenie Outputu - powstaje nowy, "zbindowany" obiekt na bazie llm
        self._llm = base_llm.with_structured_output(UserProfile)

    def extract_info(self, text: str) -> UserProfile:
        # 3 i 4. Wywołanie i Automatyczne Parsowanie. 
        # Zwracany typ to gotowy UserProfile!
        response = self._llm.invoke(text)
        return response

agent = Agent()
result = agent.extract_info("Nazywam się Anna Nowak, mam 28 lat i uwielbiam nurkować oraz czytać Sci-Fi.")

print(result.name)       # "Anna Nowak"
print(type(result))      # <class '__main__.UserProfile'>
```

---

## Wykorzystanie szablonów plików `.md.j2`

Pliki z rozszerzeniem `.md.j2` to tzw. **Szablony Jinja2 osadzone w składni Markdown**. Służą one do dynamicznego budowania złożonych promptów, oddzielając "tekst instrukcji" od "kodu analitycznego" w Pythonie (Separation of Concerns).

### Dlaczego używa się `md.j2`?

1. **Clean Code i Utrzymanie**: Prompty systemowe bywają bardzo długie, mogą pisać je analitycy biznesowi. Trzymanie 200 linijek tekstu bezpośrednio w kodzie Pythona zaciemnia architekturę (szczególnie w LangGraph).
2. **Składnia Jinja2**: Podobnie jak w szablonach HTML, pozwala na dynamiczne zarządzanie danymi z poziomu samego pliku z promptem. Umożliwia pisanie wewnątrz pliku instrukcji warunkowych (`{% if condition %}`), stosowanie pętli (`{% for item in items %}`) oraz zastępowanie zmiennych (`{{ context }}`).
3. **Podświetlanie składni**: Plik pozostaje plikiem Markdown, więc IDE i edytory podświetlają poprawnie nagłówki, pogrubienia oraz bloki kodu, co znacząco ułatwia pracę nad ulepszaniem promptów.

### Jak współgrają `md.j2` i `with_structured_output` w aplikacjach LangGraph?

Oto najczęstszy wzorzec projektowy w solidnych agentach:

* Używa się **`.md.j2`** do *skonfigurowania* środowiska w jakim model operuje (kontekst, regulamin operacyjny tzn. system prompt).
* Używa się **`with_structured_output`** do *wyciągnięcia* z modelu pewności odnośnie struktury decyzyjnej/wiedzy.

### Kompletny Zarys Wykorzystania

**Plik `/prompts/extraction_agent.md.j2`**

```markdown
# System Instruction
You are an expert Data Extractor bot working in a secure environment.

## Current Context
The total amount of memory available is: {{ memory_limit }} MB.

## History Logs:
{% if recent_errors %}
Be specifically careful about these recent errors:
{% for error in recent_errors %}
- {{ error }}
{% endfor %}
{% else %}
There are no recent errors recorded.
{% endif %}

## Instructions
Analyze the following user input and provide precisely the extracted User Profile.
If any data is missing, make a logical guess or set to null/0.

User Input: {{ user_input }}
```

**Plik `graph_node.py` (Z użyciem obydwu mechanizmów)**

```python
import jinja2
from langchain_core.messages import SystemMessage

class ExtractionNode:
    def __init__(self, llm_model):
        # Opakowanie modelem LLM wymuszającego strukturę outputu
        self._llm = llm_model.with_structured_output(UserProfile)
        
        # Konfiguracja środowiska szablonów (załaduj szablony z katalogu /prompts)
        self.jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader("prompts/"))
        self.template = self.jinja_env.get_template("extraction_agent.md.j2")

    def process_node(self, state: dict):
        # 1. Renderowanie pliku md.j2 z dynamicznymi danymi ze state (LangGraph state)
        rendered_prompt = self.template.render(
            memory_limit=state.get("memory", 1024),
            recent_errors=state.get("errors", []),
            user_input=state.get("current_message", "")
        )
        
        messages = [SystemMessage(content=rendered_prompt)]
        
        # 2. Zastosowanie Ustrukturyzowanego LLMa
        # LLM na wejściu dostaje pięknie sformatowanego Markdowna,
        # a na wyjściu MUSI zwrócić obiekt UserProfile ze względu na .with_structured_output
        structured_result: UserProfile = self._llm.invoke(messages)
        
        # 3. Zwrócenie nowego elementu do stanu grafu
        return {"extracted_profile": structured_result}
```

### Podsumowanie

1. **`md.j2`** zajmuje się **Wejściem (Inputem)** dla Modelu. Pilnuje by długie ciągi tekstowe wygenerowane z instrukcji warunkowych były przemyślane i zarządzalne.
2. **`with_structured_output`** zajmuje się **Wyjściem (Outputem)** z modelu. Daje gwarancję dla programisty Pythona, że program nie musi radzić sobie z Regexami do wyszukania JSON-a, tylko od razu na wyjściu z metody `invoke` otrzymuje sprawdzony, gotowy obiekt.
