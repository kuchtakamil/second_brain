# `with_structured_output()` vs `PydanticOutputParser`

**Nie — `with_structured_output()` NIE używa `PydanticOutputParser`.**

To dwa różne mechanizmy strukturyzowania odpowiedzi z LLM.

## `PydanticOutputParser` (stare podejście)

- Działa **post-hoc**: bierze schemat Pydantic → generuje instrukcje formatu (`get_format_instructions()`) → wstrzykuje je do promptu → po wywołaniu LLM parsuje string odpowiedzi i waliduje.
- Model nie wie nic o schemie poza tym, co dostanie w tekście promptu. Łatwo o malformed JSON.

```python
from langchain_core.output_parsers import PydanticOutputParser

parser = PydanticOutputParser(pydantic_object=Movie)
prompt = PromptTemplate(
    template="Answer the user query.\n{format_instructions}\n{query}",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)
chain = prompt | llm | parser
result = chain.invoke({"query": "Inception"})
```

## `with_structured_output()` (nowoczesne podejście)

Wg dokumentacji LangChain, używa jednej z trzech metod **natywnych dla providera**, bez parsowania stringa:

1. **`function_calling` / tool calling** — wymusza tool call zgodny ze schematem (najczęstsze, np. OpenAI, Anthropic).
2. **`json_schema`** — natywny tryb providera (np. OpenAI Structured Outputs, gwarantowana zgodność).
3. **`json_mode`** — model zwraca poprawny JSON, ale schema musi być w promptie.

Cytat z docs LangChain:
> "The `json_schema` method uses dedicated provider features, while `function_calling` derives output by forcing a tool call that follows the schema."

```python
from pydantic import BaseModel, Field

class Movie(BaseModel):
    title: str = Field(description="The title of the movie")
    year: int = Field(description="The year the movie was released")

model_with_structure = llm.with_structured_output(Movie)
response = model_with_structure.invoke("Provide details about Inception")
# Movie(title="Inception", year=2010)
```

## Praktyczna różnica

| Aspekt | `PydanticOutputParser` | `with_structured_output()` |
|---|---|---|
| Mechanizm | Parsowanie stringa odpowiedzi | Natywne tool calling / JSON schema providera |
| Format instructions w prompcie | **Wymagane** | Niepotrzebne |
| Niezawodność | Może się wysypać na malformed JSON | Provider gwarantuje zgodność ze schemą |
| Pipeline | `prompt \| llm \| parser` | `llm.with_structured_output(Model).invoke(...)` |
| Wsparcie providera | Wszystkie LLM (działa z czystym tekstem) | Wymaga wsparcia tool calling / JSON mode |

## Podsumowanie

Wewnętrznie nowsze API `with_structured_output()` używa **tool calling / JSON schema** providera, a nie `PydanticOutputParser`. Są to dwa niezależne mechanizmy — `with_structured_output()` jest preferowane, gdy provider je wspiera.

---

## Czym dokładnie jest Function Calling (Tool Calling)?

*Function Calling* (często nazywane *Tool Calling*, w LangChain silnik zaszyty m.in. pod użyciem funkcji `with_structured_output`) to wbudowany w nowoczesne modele (takie jak GPT-4, Claude 3, Gemini) mechanizm, który pozwala LLM-om połączyć się z zewnętrznym systemem czy bazą danych. Co kluczowe: **sam LLM nie wykonuje żadnego kodu**. On po prostu informuje Cię o tym, jaką wewnętrzną funkcję aplikacji należy wywołać i z jakimi parametrami.

Oto jak ten proces wygląda krok po kroku w typowym scenariuszu (np. pobrania pogody przez bota):

1. **Przekazanie schematu:** Wraz z promptem od użytkownika przesyłasz do modelu definicję dostępnych dla niego "narzędzi" (najczęściej na bazie **JSON Schema**). Definicja zawiera nazwę funkcji, jej ogólny cel i strukturę argumentów w formie słownika JSON.
2. **Generowanie argumentów (Decyzja LLMa):** LLM podczas analizy zapytania decyduje, że do podania precyzyjnej odpowiedzi musi użyć przygotowanego przez Ciebie narzędzia (np. `get_weather_in_city`). Generowanie tradycyjnego tekstu zostaje powstrzymane na rzecz zwrócenia specjalnego metadanych ze strony API w obiekcie (tzw. `tool_calls`). W tym obiekcie model podaje wybraną zarejestrowaną nazwę narzędzia oraz uformowany, bezbłędny **ciąg znaków jako JSON**, reprezentujący argumenty dla tej funkcji przygotowane i wydedukowane z konwersacji (np. `{"city": "Kraków"}`).
3. **Parsowanie i wykonanie w aplikacji:** Ten wejściowy JSON jako sygnał do interwencji ląduje z powrotem w Twoim kodzie w Python / Node.js. Jeśli masz zdefiniowaną połączoną funkcję wedle specyfikacji dla danego wejścia – wtedy po swojej stronie bezpiecznie ją wykonujesz (strzelasz na podany obiekt np. API pogodowego). Informacje te jako wynik następnie "zwracasz" i przekazujesz z powrotem dla LLMa jako wiadomość w typie `tool_response`, a LLM po jego odczytaniu redaguje już w oparciu o prawdziwe środowisko kompletną wiadomość do użytkownika.

### Dlaczego tego mechanizmu LLM używamy w `.with_structured_output()`?

Skoro model decyduje o "wygenerowaniu zapotrzebowania na narzędzie" po to, by Twoja aplikacja zrealizowała funkcję, to w jaki sposób używamy tego mechanizmu do czegoś tak prozaicznego, jak wymuszenie zwrócenia samej konkretnej struktury danych Pydantic dla rezerwanta czy analizy CV z tekstu?

Otóż dlatego, że współczesne LLMy (szczególnie począwszy od modelu `gpt-3.5-turbo-0613` firmy OpenAI) na etapie ich douczania przez dostawców po zakończeniu standardowego treningu zostały potężnie "zoptymalizowane" przez techniki takie jak fine-tuning by **perfekcyjnie trzymać się i formatować konwencję składni schematu argumentów Tool Calling jako nieugięty format JSON**.

Programiści uzyskali w ten sposób niespotykaną wcześniej gwarancję i pewność zmuszania i zamykania "odpowiedzi" w stałe formaty, co wykorzystali do bardzo chytrego wykorzystania. Sposób stosowania w LangChain nazywany "ToolStrategy" (czyli użycia parsowanego wyjścia Tool Callingu do wyciągnięcia modelu np. Pydantic z klasy) to nic innego jak pożyteczny programistyczny "hack":

1. Definiujesz całkowicie "fałszywe" narzędzie w którym **samą strukturą argumentów bazowych parametru** do spreparowania przez LLM jest w całości Twoja klasa z danymi `Pydantic`, którą byś chciał od modelu uzyskać, nadając jej trafną nazwę akcji (np. `extract_filmInformation`). To kluczowy element objaśnienia — ciało funkcji wykonującej prawdziwą logikę do odpalenia w systemie nigdy się nie urzeczywistnia — istnieje jedynie fasadowy kontrakt przesłany dla modelu!
2. Zamiast dawać modelowi decyzyjność, czy po przeczytaniu pliku PDF z recenzją uważa za słuszne to narzędzie aktywować, Ty **twardo narzucasz na niego wywołanie tej konkretnej spreparowanej funkcji asystującej** (np. poprzez specjalną flagę w zapytaniu API ustawianą na `tool_choice: "required"`). Właśnie to w sercu mechaniki wykonuje funkcja LangChain pod fasadą nazwy podsystemu `with_structured_output`.
3. Model LLM, postawiony przed oknem z wymuszonym zadaniem narzędziowym wstrzykuje i od razu dedukuje na wyjście jedyny cudowny, w 100% poprawny technicznie i składniowo uformatowany parametr JSON na wejście spodziewając się jego odpalenia. Po zwróceniu zmuszonych narzędzi — urywa proces generowania.
4. Twój system, widząc na horyzoncie odpowiedź zwrotną API ze zdarzeniem wywołania narzuconego narzędzia w locie tylko **rozpakowuje ten argumentowy bezbłędny JSON bez żadnych obróbek stringów**, po czym bez wahania przekluwa te informacje nakładając na parametry wejściowe mapowania Twojej klasy. Pomija jakiekolwiek odbicia czy powrotne logiki zwracające do LLMa odpowiedzi funkcji — jedynym Twoim celem było posłużenie się rygorem parsowanego pod schematy narządzia tekstu formatującego jako solidniejszej powłoki niż wadliwy starego typu kod `PydanticOutputParser` walczący z naturalnie zwracanym plain textem i nie domykanymi cudzysłowami JSON modelów nie wspierających Callingu.

Podsumowując, funkcja zadeklarowana tutaj przed obliczem *Function Calling* okazuje się być w ostatecznym znaczeniu wyłącznie **nieaktywnym protokołem rygoru Twojej wejściowej paczki danych** wykorzystywanym na rzecz niezrównanej precyzji w formowaniu ostatecznego rezultatu typu danych jaki otrzymasz dla integracji w ekosystemie backendu.

Oczywiście rozwój i badania nad precyzyjnością nie stoją w miejscu, więc to wysoce efektywne podejście dostaje w obecnym czasie ogromną przebudowę — od połowy 2024 giganci tacy jak OpenAI i inni, wspólnie wypuszczają odseparowane nowe tryby natywne do uzyskiwania obiektów (sławne **Strict Structured Outputs** czy pola w stylach `json_schema`). Bazują one w całości np. o potężny mechanizm tak zwanego *"Constrained Decoding"* ("Dekodowania Uwarunkowanego") polegającego na ślepym fizycznym ograniczaniu lub obcinaniu możliwości wybierania danego zniekształconego słowa lub wylosowania złego kolejnego znaku przez silnik "zgadujący" jeszcze zanim ten faktycznie je na świat zrealizuje — co potrafi gwarantować wręcz absolutnie idealną 100% składniowo pewność i natywnie wypełniony poprawny format.

Z tego jednak względu po dziś dzień sztandarowy filar, jakim stał się od 2023 r mechanizm ustrukturyzowania przez wymuszony Tool Calling pozostaje silnikiem kluczowym w niemal całej globalnej przestrzeni sztucznej inteligencji. Ma niebotyczne oparcie przez gigantów sceny AI jako nadal główna i powszechna opcja (fallback w klasach `ToolStrategy`), i najpewniej jeszcze bardzo długo będzie standardowym sposobem od pytań o zwykły kod parsujący bez problemów natywnych formatów modeli niszowych.

---

## FAQ

### Czy `function_calling` oznacza wywołanie mojej funkcji, która zwraca JSON?

**Nie.** Nie chodzi o to, że Twoja funkcja "programistycznie zwraca JSON". Mechanizm jest taki:

1. Deklarujesz schemę (Pydantic / JSON Schema) — to jest **definicja tool'a, bez ciała**. Sama funkcja nigdy nie jest wywoływana przez LangChain ani LLM.
2. LangChain wysyła tę schemę do API providera jako definicję tool'a.
3. Provider zmusza model do wyemitowania **`tool_call`** z argumentami zgodnymi ze schemą (`tool_choice` ustawione na ten konkretny tool).
4. Provider gwarantuje, że JSON argumentów jest składniowo poprawny (a w trybie `strict` — także semantycznie zgodny ze schemą).
5. LangChain bierze już sparsowane argumenty (dict) i instancjonuje Twój `BaseModel`.

Innymi słowy: to **API providera** wymusza poprawny JSON na poziomie protokołu — nie żaden kod Python wykonywany lokalnie. "Function" w "function calling" to tylko **kontrakt schemy**, nie wywoływany kod.

### Czy Anthropic i Gemini też mają natywny structured output?

**Tak — oba.** Wg dokumentacji LangChain:

> "Some model providers support structured output natively through their APIs (e.g. OpenAI, xAI (Grok), Gemini, Anthropic (Claude))."

Każdy provider implementuje to nieco inaczej, ale `with_structured_output()` ujednolica API:

| Provider              | Natywny mechanizm                                                                                     |
| --------------------- | ----------------------------------------------------------------------------------------------------- |
| **OpenAI**            | Structured Outputs (`response_format={"type": "json_schema", "strict": true}`) + tool calling         |
| **Anthropic (Claude)**| Tool use — wymuszenie `tool_choice` z konkretnym narzędziem; Claude generuje JSON zgodny ze schemą    |
| **Google Gemini**     | `response_mime_type="application/json"` + `response_schema` (Pydantic / JSON Schema / proto)          |
| **xAI (Grok)**        | Structured Outputs w stylu OpenAI                                                                     |

Dla wszystkich tych providerów `with_structured_output(Model)` "po prostu działa" — LangChain pod spodem wybiera odpowiednią natywną metodę. Jeśli model nie ma natywnego wsparcia, LangChain spada na `ToolStrategy` (artificial tool calling) jako fallback.

### Praktyczna konsekwencja

W LangChain 1.0:

- `ProviderStrategy` — używany domyślnie, gdy provider wspiera natywny structured output (najbardziej niezawodny).
- `ToolStrategy` — fallback, używa "sztucznego" tool calling, gdy nie ma natywnego wsparcia.

Wybór jest automatyczny po przekazaniu schemy do `response_format=` lub `with_structured_output()`.
