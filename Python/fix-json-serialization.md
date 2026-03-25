# Fix JSON serialization

**Data:** 2025-12-20

---

**User:**

Mam taki kod

import json
from pathlib import Path

from itertools import islice
from typing import Iterator, List, TextIO

from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI


def extract_content(input_path, output_path):
    with open(input_path, "r") as f:
        data = json.load(f)

    exclude = ['category', "take"]
    defs = []
    for item in data:
        for title, content in item.items():
            if title not in exclude:
                lines = [line.strip() for line in content.splitlines() if line.strip()]
                defs.extend(lines)

    with open(output_path, "w") as f:
        f.write("\n".join(defs))

def process_content(part, output_json):
    load_dotenv()
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-3-pro-preview",
        max_tokens=None,
        timeout=None,
        max_retries=2,
        # other params...
    )

    system_prompt = """
You are given:
1. A list of English words and expressions with short definitions (**NEW_ENTRIES**).
2. A JSON array of groups (**GROUPS**) that follows the exact output schema described below.
   - GROUPS may be empty or non-empty.

Your task is to produce an updated version of GROUPS by integrating all NEW_ENTRIES.

---

### Core behavior
- If GROUPS is empty, create a complete set of highly specific groups covering all NEW_ENTRIES.
- If GROUPS is not empty, extend it by:
  - adding new expressions to existing groups where they clearly and precisely fit,
  - creating new groups when no existing group provides a sufficiently specific and accurate match.

---

### Grouping rules (strict)
1. Groups must be **highly specific and narrowly scoped**, defined by a strong unifying criterion, such as:
    - idioms built around the **same metaphor or imagery**,
    - very narrow domains (e.g. *airplane cabin service*, *non-alcoholic mixed drinks*, *cutlery hybrids*),
    - conversational phrases serving the **same pragmatic function** (e.g. interrupting politely),
    - a precise grammatical, semantic, or usage-based nuance.
2. **Do not weaken, broaden, or dilute existing groups** to accommodate new expressions.
3. **Actively prefer creating a new group** over forcing an imprecise fit into an existing one.
4. If an expression fits multiple groups, include it in **all relevant groups**.
5. A group may contain **between 3 and 15 expressions**.
6. Avoid mixing literal and figurative meanings unless the metaphor itself is the grouping criterion.
7. All expressions already present in GROUPS must remain assigned to their groups.

---

### Handling groups
- You may append new expressions to the `"content"` array of existing groups.
- You may create entirely new groups if needed.
- Preserve existing:
  - `"title"` and `"explanation"` fields (do not rewrite them unless they are factually incorrect).
- New groups must use sequential `"group_no"` values, continuing from the highest existing number.

---

### Coverage requirement
- Every expression in NEW_ENTRIES must appear in **at least one group**.
- The output must include:
  - all expressions originally present in GROUPS,
  - all expressions from NEW_ENTRIES.

---

### Output requirements (strict)
- Return **only** a valid JSON array.
- Do NOT include any text outside the JSON.
- Each group object must contain exactly:
  - `"title"`: string, short and specific group title
  - `"explanation"`: string, one-sentence explanation of the grouping criterion
  - `"content"`: array of strings (expressions only, without definitions)
- The JSON must be syntactically valid and fully parsable.

### Output structure example
[
  {
    "title": "'Cold' idioms expressing hesitation or emotional distance",
    "explanation": "Idiomatic expressions that use 'cold' metaphorically to describe reluctance or social withdrawal",
    "content": ["quit cold turkey", "get cold feet", "give someone the cold shoulder"]
  },
  {
    "title": "Verbs describing drinking methods",
    "explanation": "Specific verbs used to describe the speed or sound made when consuming liquids",
    "content": ["sip", "slurp", "gulp"]
  }
]
    """

    try:
        with open(output_json, "r") as f_r:
            groups = json.load(f_r)
    except FileNotFoundError:
        groups = "[]"

    human_prompt=f"""
**GROUPS**
{groups}

**NEW_ENTRIES**
{part}
    """

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=human_prompt)
    ]

    response = llm.invoke(messages)
    result = response.text

    with open(output_json, "w") as f_w:
        json.dump(result, f_w, ensure_ascii=False)


def part_iterator(
    file: TextIO,
    first_part: int,
    next_part: int
) -> Iterator[List[str]]:

    yield list(islice(file, first_part))

    while True:
        part = list(islice(file, next_part))
        if not part:
            break
        yield part


if __name__ == '__main__':
    chanel_name = "lovenglish_4u"
    my_file = Path(f"../scraped/{chanel_name}/result_{chanel_name}.json")
    to_categorise = Path(f"../scraped/{chanel_name}/extracted.txt")
    outputJson = Path(f"../scraped/{chanel_name}/categorized.json")

    # extract_content(my_file, to_categorise)
    # with to_categorise.open("r", encoding="utf-8") as f:
    #     line_count = sum(1 for _ in f)

    with open(to_categorise, encoding="utf-8") as f:
        for batch in part_iterator(f, 50, 200):
            process_content(batch, outputJson)

On w linii
json.dump(result, f_w, ensure_ascii=False)
produkuje json w takiej formie
"```json\n[\n  {\n    \"title\": \"Words with prefix 'over-' indicating excess or specific states\",\n 
Dlaczego? Jak to poprawić? Popraw tylko fragment kodu, nie całość

---

**Assistant:**

Problem nie jest w `json.dump`, tylko w tym, **co faktycznie zapisujesz**.

### Dlaczego tak się dzieje

`response.text` zwracane przez `ChatGoogleGenerativeAI` **nie jest obiektem JSON**, tylko **stringiem**, który zawiera:

```
```json
[
  { ... }
]
```
```

Model – mimo instrukcji – opakowuje odpowiedź w **Markdownowy code fence**.  
Ty następnie robisz:

```python
json.dump(result, f_w, ensure_ascii=False)
```

czyli:
- serializujesz **string** do JSON-a  
- więc dostajesz poprawny JSON… zawierający string, a nie tablicę obiektów

Dlatego wynik zaczyna się od:

```json
"```json\n[\n  {\n    \"title\": ...
```

---

### Minimalna poprawka (tylko fragment)

Musisz:
1. Usunąć ```json / ``` z tekstu
2. Zdeserializować string → obiekt Python
3. Dopiero wtedy zapisać go jako JSON

Zamień **tylko** ten fragment:

```python
result = response.text

with open(output_json, "w") as f_w:
    json.dump(result, f_w, ensure_ascii=False)
```

na:

```python
result = response.text.strip()

# usunięcie markdownowych code fence
if result.startswith("```"):
    result = result.removeprefix("```json").removeprefix("```")
    result = result.removesuffix("```").strip()

parsed = json.loads(result)

with open(output_json, "w", encoding="utf-8") as f_w:
    json.dump(parsed, f_w, ensure_ascii=False, indent=2)
```

---

### Dlaczego to jest poprawne rozwiązanie

- zachowujesz **walidację JSON-a** (`json.loads` natychmiast wywali błąd, jeśli model zwróci śmieci)
- zapisujesz **prawdziwą strukturę JSON**, a nie string
- nie polegasz ślepo na tym, że LLM „posłucha” instrukcji

Jeżeli chcesz, mogę pokazać wariant odporny na:
- ```JSON``` / ```json``` / brak języka
- odpowiedzi z komentarzami przed lub po JSON-ie

---

**User:**

tak pokarz

---

**Assistant:**

Poniżej masz **odporny fragment**, który:

- usuwa dowolne code fence (``` / ```json / ```JSON)
- ignoruje śmieci przed i po JSON-ie
- wyciąga **pierwszą poprawną tablicę JSON** z odpowiedzi modelu
- failuje jasno, jeżeli model zwróci coś nieparsowalnego

### Zamień tylko ten fragment

```python
result = response.text
```

oraz zapis do pliku — na poniższe:

```python
import re

raw = response.text.strip()

# 1. Usuń wszystkie markdownowe code fence
raw = re.sub(r"```(?:json|JSON)?", "", raw).strip()

# 2. Wyciągnij pierwszą tablicę JSON
match = re.search(r"\[[\s\S]*\]", raw)
if not match:
    raise ValueError("LLM response does not contain a JSON array")

json_text = match.group(0)

# 3. Parsuj JSON (twarda walidacja)
parsed = json.loads(json_text)

with open(output_json, "w", encoding="utf-8") as f_w:
    json.dump(parsed, f_w, ensure_ascii=False, indent=2)
```

---

### Co to rozwiązuje (konkretnie)

✔ ```json … ```  
✔ ``` … ```  
✔ tekst przed JSON-em (np. „Here is the result:”)  
✔ tekst po JSON-ie  
✔ przypadkowe nowe linie i spacje  
✔ gwarancja, że na dysku masz **array**, nie string

---

### Uwaga architektoniczna (ważna przy batchach)

Ponieważ robisz:

```python
for batch in part_iterator(...):
    process_content(batch, outputJson)
```

to:
- **każdy batch nadpisuje cały plik**
- jeśli LLM raz się wywali → tracisz poprzedni stan

Jeśli chcesz, w kolejnym kroku mogę:
- pokazać **bezpieczny merge** grup batch → batch
- albo wersję z **append + atomic write**
- albo walidację schematu (np. `jsonschema`)

Daj znać.

---

**User:**

Przy wykonaniu tego kodu dostałem taki błąd
Retrying langchain_google_genai.chat_models._chat_with_retry.<locals>._chat_with_retry in 2.0 seconds as it raised DeadlineExceeded: 504 Deadline Exceeded.
Co oznacza? czy dalej mam czekać na odpowiedź z modelu? Jak wyłączyć ten timeout?

---

**Assistant:**

### Co oznacza ten błąd

```
DeadlineExceeded: 504 Deadline Exceeded
```

To **nie jest timeout po Twojej stronie**, tylko **timeout po stronie Google API (serwerowy)**.

Znaczenie praktyczne:
- żądanie **dotarło do modelu**
- model **nie zdążył wygenerować odpowiedzi w limicie narzuconym przez backend**
- backend **przerwał request** i zwrócił 504
- LangChain **automatycznie retryuje** (stąd komunikat „Retrying … in 2.0 seconds”)

**Czekanie nic nie da** — to żądanie zostało już definitywnie przerwane.

---

### Dlaczego to się dzieje w Twoim przypadku

Masz kilka czynników ryzyka naraz:

1. **Bardzo długi prompt systemowy**
2. **Rosnący `GROUPS` JSON** (każdy batch zwiększa payload)
3. **Brak limitu `max_tokens`**
4. Model `gemini-3-pro-preview` (wolniejszy, cięższy)
5. Operacja wymagająca **pełnego przemyślenia i restrukturyzacji JSON-a**

To klasyczny przypadek:
> *request jest poprawny, ale zbyt ciężki obliczeniowo*

---

### Czy da się „wyłączyć timeout”?

**Nie.**  
Timeout 504 jest **twardym limitem infrastruktury Google**. Parametr:

```python
timeout=None
```

oznacza tylko:
- brak timeoutu **po stronie klienta**
- **nie wpływa** na timeout serwera

Tego limitu **nie da się wyłączyć**.

---

### Co możesz zrobić (konkretne i skuteczne)

#### 1. Ogranicz `max_tokens` (najważniejsze)

Dodaj **konkretny limit**, np.:

```python
llm = ChatGoogleGenerativeAI(
    model="gemini-3-pro-preview",
    max_tokens=2048,
    timeout=120,
    max_retries=2,
)
```

Bez tego model może próbować generować bardzo długą odpowiedź → timeout.

---

#### 2. Zmniejsz payload GROUPS (architektonicznie kluczowe)

Obecnie:
- przy każdym batchu wysyłasz **cały narastający JSON**
- po kilku iteracjach prompt staje się ogromny

Lepsze podejście:
- wysyłaj tylko **nowe grupy + ich skrócony opis**
- albo sharduj GROUPS (np. per litera / domena)

Jeśli chcesz, mogę zaproponować **konkretny schemat shardingowy**.

---

#### 3. Zmniejsz batch NEW_ENTRIES

Masz:

```python
first_part = 50
next_part = 200
```

Dla Gemini to dużo przy takim zadaniu. Bezpieczniej:

```python
first_part = 30
next_part = 50
```

---

#### 4. Zmień model (jeśli możesz)

Jeżeli nie potrzebujesz aż takiej jakości reasoningowej:

```python
model="gemini-1.5-pro"
```

albo nawet:
```python
model="gemini-1.5-flash"
```

Flash **radykalnie** zmniejsza liczbę 504 przy takich pipeline’ach.

---

### Jak poprawnie obsłużyć ten błąd w kodzie

Nie licz na retry LangChaina — lepiej kontrolować to samemu:

```python
from google.api_core.exceptions import DeadlineExceeded

try:
    response = llm.invoke(messages)
except DeadlineExceeded:
    # zapisz batch do retry / zmniejsz payload / loguj
    raise RuntimeError("Gemini timeout — payload too large or model overloaded")
```

---

### Podsumowanie wprost

- ❌ **Nie, nie ma sensu czekać**
- ❌ **Nie da się wyłączyć tego timeoutu**
- ✔ **To limit serwerowy Google**
- ✔ **Rozwiązanie: mniejsze batch’e, mniejszy JSON, limit `max_tokens`**
- ✔ **Problem będzie narastał wraz z kolejnymi iteracjami**

Jeżeli chcesz, w kolejnym kroku mogę:
- przeprojektować ten pipeline tak, żeby **nigdy nie wysyłać całego GROUPS**
- albo zaproponować **dwufazowe grupowanie (local + merge)**  
To jest dokładnie ten typ problemu, który później zabija stabilność LLM-owych ETL-i.