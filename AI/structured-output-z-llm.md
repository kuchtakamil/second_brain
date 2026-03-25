# Structured Output z LLM

## Podsumowanie (Co to jest?)
**Structured Output** (Ustrukturyzowane wyjście) to technika zmuszania i gwarantowania, że duży model językowy (LLM) zwróci odpowiedź w ściśle określonym, maszynowo czytelnym formacie (najczęściej JSON), zamiast luźnego tekstu naturalnego. Oznacza to, że aplikacja kliencka może bezpiecznie parsować wynik działania modelu i mapować go bezpośrednio na obiekty w kodzie (np. klasy `Pydantic` w Pythonie lub interfejsy w TypeScript) bez obawy o błędy składniowe czy halucynacje kluczy w strukturze danych.

## Dlaczego się stosuje? (Zastosowanie i Znaczenie)
Standardowo LLM generuje tekst w taki sposób, w jaki "rozmawia" z człowiekiem (np. `"Oto twój wynik w formacie JSON:\n```json\n...\n```"`). Dla oprogramowania parsowanie takich odpowiedzi za pomocą wyrażeń regularnych czy wyciągania fragmentów tekstu jest niezwykle kruche, zawodne i podatne na błędy (np. ucięty JSON, dodatkowe komentarze modelu, złe typy danych). Structured Output jest krytycznym elementem budowy produkcyjnych aplikacji opartych o sztuczną inteligencję (tzw. AI Agents). 

Główne zastosowania:
1. **Ekstrakcja danych (Data Extraction):** Przekształcanie nieustrukturyzowanego tekstu (np. artykułu, maila, CV) w ustrukturyzowaną reprezentację (np. wyciągnięcie imienia, nazwiska i doświadczenia kandydata do bazy danych).
2. **AI Agents (Narzędzia i Funkcje - Tool Calling):** Gdy Agent decyduje się na wywołanie zewnętrznej funkcji (API), musi wygenerować precyzyjny JSON odpowiadający argumentom tejże funkcji.
3. **Podejmowanie decyzji (Routing):** Zmuszenie modelu do kategoryzacji zapytania użytkownika lub zwrócenia określonej wartości wyliczeniowej (Enum), co umożliwia twarde sterowanie logiką biznesową aplikacji na podstawie tekstu wejściowego.
4. **Validacja i Typowanie:** Ograniczenie halucynacji poprzez zawężenie przestrzeni wyjściowej modelu - ograniczony model "nie ma wyjścia" i musi podać wartości odpowiedniego typu (np. liczba zamiast tekstu).

## Jak to działa i Przykłady Technologii

Techniki wymuszania struktury można podzielić na dwie główne kategorie:
1. **Podejścia oparte na promptingu i walidacji (np. LangChain, zwykły `JSON mode`, weryfikacja z ponowieniem - Auto Retry):** Model jest po prostu instruowany w prompcie systemowym, aby zwrócił JSON, a aplikacja aplikuje walidację Pydantic i ewentualnie odrzuca lub prosi model o naprawę odpowiedzi (Self-Correction).
2. **Gwarantowane parsowanie na poziomie generacji (np. rygorystyczne OpenAI Structured Outputs, Outlines, Instructor):** Zastosowanie tzw. wymuszonego schematu (Constrained Decoding / logits masking). Prawdopodobieństwa tokenów niezgodnych z wyciętym schematem są sztucznie zerowane w trakcie fazy generacji silnika. Model uczy się wewnętrznie gramatyki podanego JSON Schema, co daje 100% gwarancję poprawnego formatu struktury, a nie tylko jego uprawdopodobnienie.

### 1. OpenAI Structured Outputs (API Natywne, Strict Mode)
W sierpniu 2024 OpenAI wprowadziło funkcję `strict: true` dla strukturyzowanych wyjść.

```python
from pydantic import BaseModel
from openai import OpenAI

client = OpenAI()

class MathReasoning(BaseModel):
    step_by_step: list[str]
    final_answer: float

# Użycie parametru response_format parsującego strukturę klas do JSON Schema modelu
response = client.beta.chat.completions.parse(
    model="gpt-4o-2024-08-06",
    messages=[
        {"role": "system", "content": "Jesteś pomocnym matematykiem."},
        {"role": "user", "content": "Ile to jest 8x12?"}
    ],
    response_format=MathReasoning,
)

math_response = response.choices[0].message.parsed
print(math_response.final_answer) # Gwarantowany typ float (96.0)
```

### 2. Instructor (Biblioteka Python)
`Instructor` to jedna z najpopularniejszych bibliotek dla deweloperów AI do strukturyzowania outputu. Opakowuje ona klientów LLM (OpenAI, Anthropic, Gemini, Groq) ujednolicając interfejs i umożliwia bezpośrednie zwracanie obiektów Pydantic. Obsługuje zaawansowane mechanizmy Retries (ponowienia), łatwą walidację pod predykty i zgrabne wstrzykiwanie logiki wyciągania struktury.

```python
import instructor
from pydantic import BaseModel
from openai import OpenAI

# Oklejenie standardowego klienta OpenAI przez bibliotekę Instructor
client = instructor.from_openai(OpenAI())

class UserDetail(BaseModel):
    name: str
    age: int

# Zwracana jest od razu zwalidowana instancja Pydantic
user = client.chat.completions.create(
    model="gpt-4o-mini",
    response_model=UserDetail, # Instructor obsługuje bezpośrednio klasę
    messages=[
        {"role": "user", "content": "Wyciągnij dane: Jan Kowalski ma 30 lat"}
    ]
)

print(user.name) # "Jan Kowalski"
print(user.age)  # 30
```

### 3. Outlines (dla lokalnych modeli open-source)
Gdy używamy lokalnych modeli odpalanych ze swoich serwerów, `Outlines` oferuje najwyższą wydajność dla gwarantowanego strukturyzowania dzięki sterowaniu wyborem tokenów zdefiniowanych stanami (Guided Generation). Model zmuszony jest generować w formacie JSON lub określonego wyrażenia regularnego (Regex), eliminując poleganie na API chmurowym.

```python
import outlines
from pydantic import BaseModel

model = outlines.models.transformers("mistralai/Mistral-7B-Instruct-v0.2")

class Character(BaseModel):
    name: str
    class_type: str
    hp: int

# Outlines przebudowuje potok w sposób "wymuszony" na podstawie klasy Pydantic
generator = outlines.generate.json(model, Character)
character = generator("Opisz potężnego maga ognia z gry RPG.")

print(character) # Zawsze zwróci oczekiwany obiekt bez marginesu błędu
```

### 4. LangChain (z nowoczesnym `with_structured_output`)
LangChain w nowszych iteracjach (wersje 0.1 i 0.2+) zmodernizował swój ekosystem, wprowadzając ujednoliconą metodę `.with_structured_output()`, która automatycznie pod maską wybiera najlepszą strategię zgodną z dostawcą modelu.

```python
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

llm = ChatOpenAI(model="gpt-4o")

class Joke(BaseModel):
    setup: str = Field(description="Pytanie przygotowujące żart")
    punchline: str = Field(description="Puenta żartu")

# Przybicie struktury Pydantic do łańcucha konwersacji (Chain)
structured_llm = llm.with_structured_output(Joke)

joke = structured_llm.invoke("Odpowiedz sucharem o programistach.")
print(joke.setup)
print(joke.punchline)
```

## Podsumowanie i Ewolucja Technik 
- **Zwykły JSON Mode:** LLM po prostu wie (i jest odpowiednio strojony), że ma zwrócić JSON. Nie ma jednak twardego sprawdzania schematu. Czasami się myli w szczegółach.
- **Tool Calling (Function Calling):** Pierwotna "obejściowa" metoda ustrukturyzowania odpowiedzi polegająca na nakłonieniu modelu do generacji JSON-a wywołującego sztuczną funkcję definiującą dane wyjściowe.
- **Constrained Decoding (Strict Mode / Structured Outputs):** Obecny złoty standard inżynierii AI. Głęboka integracja wymuszania schematu struktury w trakcie procesu generowania kolejnych prawdopodobieństw tokenów przez model. Gwarantuje niemal 100% poprawność parsowania.

## Powiązane pliki (Zobacz również)
- [Komunikacja z LLM w LangChain](./komunikacja-z-llm-w-langchain.md)
- [LangChain - structured output i Jinja2](./langchain-structured-output-jinja2.md)
- [LLM Guardrails](./llm-guardrails.md)
