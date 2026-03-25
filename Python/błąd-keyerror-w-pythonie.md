# Błąd KeyError w Pythonie

**Data:** 2026-01-12

---

**User:**

propmpt = "sdf asdf asdf ewr {title}. {explanation}"
prompt.format(title=item["title"],explanation=item["explanation"])

powyższy kod rzuca wyjątek KeyError: '\n\n"title"'

---

**Assistant:**

Przyczyna jest typowa dla `str.format()` w Pythonie.

### Co się dzieje

`str.format()` **interpretuje każdą parę `{...}` jako placeholder**.  
Błąd:

```
KeyError: '\n\n"title"'
```

oznacza, że **w samym `prompt` znajduje się dodatkowa para klamer**, której Python **nie powinien traktować jako placeholder**, ale traktuje — i próbuje znaleźć klucz o nazwie `"\n\n"title"`.

Najczęściej dzieje się to, gdy:

- w `prompt` masz **JSON**, **fragment tekstu z klamrami**, lub
- `item["explanation"]` zawiera `{` i `}`

Przykład problematycznego tekstu:

```text
{
  "title": "abc",
  "value": 123
}
```

Dla `format()` to są *placeholders*.

---

### Poprawne rozwiązania

#### ✅ 1. Ucieczka klamer (najczęściej poprawne)

Jeśli w `prompt` **celowo** masz klamry, musisz je podwoić:

```python
prompt = "Treść JSON:\n{{\n  \"title\": \"{title}\"\n}}\n{explanation}"
```

Zasada:
- `{` → `{{`
- `}` → `}}`

---

#### ✅ 2. Bezpieczne formatowanie przez `f-string` (jeśli masz kontrolę nad zmiennymi)

```python
prompt = f"sdf asdf asdf ewr {item['title']}. {item['explanation']}"
```

`f-string` **nie parsuje zawartości zmiennych**, więc jest odporny na JSON-y.

---

#### ✅ 3. Użycie `format_map` z defaultdict (obejście, nie idealne)

```python
from collections import defaultdict

prompt.format_map(defaultdict(str, title=item["title"], explanation=item["explanation"]))
```

Nie polecam jako rozwiązanie docelowe — maskuje realny problem.

---

### Rekomendacja praktyczna

Jeżeli:
- generujesz **prompty dla LLM**
- wstawiasz **JSON / YAML / kod / markdown**

➡ **NIE używaj `str.format()`**  
➡ **Użyj `f-string` albo templatingu (np. Jinja2)**

---

### TL;DR

Błąd wynika z tego, że:
- gdzieś w `prompt` (lub `explanation`) są `{}`  
- `str.format()` traktuje je jako placeholdery

Najprościej i najbezpieczniej:

```python
prompt = f"sdf asdf asdf ewr {item['title']}. {item['explanation']}"
```

Jeśli chcesz, mogę przejrzeć **konkretną treść `prompt` lub `explanation`** i wskazać dokładnie, która klamra powoduje wyjątek.

---

**User:**

w prompt w dalszej części jest wklejony przykładowy JSON więc są { i }. I to właśnie tam mam podwoić klamry?

---

**Assistant:**

Tak — **dokładnie tam**.

Każda klamra `{` i `}` w *statycznej treści prompta* (czyli np. wklejony przykładowy JSON) **musi być podwojona**, aby `str.format()` jej nie interpretował jako placeholder.

### Przykład

Masz prompt:

```python
prompt = """
Oto przykład JSON:
{
  "title": "example",
  "value": 123
}

Tytuł: {title}
Opis: {explanation}
"""
```

To **zawsze** skończy się `KeyError`.

### Poprawna wersja z podwojonymi klamrami

```python
prompt = """
Oto przykład JSON:
{{
  "title": "example",
  "value": 123
}}

Tytuł: {title}
Opis: {explanation}
"""
```

Zasada jest zero-jedynkowa:
- `{` → `{{`
- `}` → `}}`
- **tylko** `{title}` i `{explanation}` zostają pojedyncze

---

### Ważna uwaga praktyczna (szczególnie dla promptów LLM)

Jeżeli:
- często wklejasz JSON / YAML / kod
- albo budujesz prompty dynamicznie

to `str.format()` staje się **źródłem błędów i frustracji**.

#### Lepsze alternatywy

**1. f-string (najczęściej najlepsze)**

```python
prompt = f"""
Oto przykład JSON:
{json_example}

Tytuł: {item['title']}
Opis: {item['explanation']}
"""
```

**2. Jinja2 (jeśli masz rozbudowane prompty)**  
Jinja używa `{{ }}` domyślnie, ale obsługuje *raw blocks* i jest znacznie bezpieczniejsza do tekstu z kodem.

---

### Podsumowanie

- ✔ Tak, **podwajasz klamry dokładnie w tym wklejonym JSON-ie**
- ✔ Placeholdery (`{title}`) zostają bez zmian
- ⚠ Jeśli to prompty do LLM — rozważ porzucenie `str.format()`

Jeżeli chcesz, mogę zaproponować **docelowy wzorzec budowania promptów**, który nie rozsypie się przy większej liczbie przykładów JSON.

---

**User:**

nie mogę użyć f-stringa bo string jest długi, zdefioniowany wcześniej. Napisz więcej o kolejnym rozwiązaniu

---

**Assistant:**

Rozumiem ograniczenie. W takim przypadku **Jinja2 jest właściwym i skalowalnym rozwiązaniem**. Poniżej opisuję je w sposób praktyczny, z naciskiem na prompty zawierające JSON i długie, statyczne treści.

---

## Dlaczego `str.format()` jest złym narzędziem w Twoim przypadku

- Konflikt składni: `{}` występuje **naturalnie** w JSON-ie
- Brak trybu „literalnego” dla klamer
- Trudna konserwacja — każda zmiana w przykładzie JSON grozi regresją

To jest dokładnie problem, który **silniki szablonów** rozwiązują od lat.

---

## Jinja2 – rozwiązanie docelowe

### 1. Instalacja

```bash
pip install jinja2
```

---

### 2. Szablon prompta (bez uciekania klamer)

```python
PROMPT_TEMPLATE = """
You are an AI assistant.

Here is an example JSON:
{
  "title": "example",
  "value": 123
}

Now process the following input:

Title: {{ title }}
Explanation: {{ explanation }}
"""
```

**Zauważ:**
- JSON ma **pojedyncze klamry**
- Zmienne są wyraźnie odróżnione (`{{ title }}`)

---

### 3. Renderowanie prompta

```python
from jinja2 import Template

template = Template(PROMPT_TEMPLATE)
prompt = template.render(
    title=item["title"],
    explanation=item["explanation"]
)
```

---

## Kluczowa funkcja: `{% raw %}`

Jeżeli w promptcie masz **fragmenty, które mogą przypadkowo zawierać `{{ ... }}`** (np. przykłady promptów, dokumentację), możesz je całkowicie wyłączyć z parsowania.

```jinja
{% raw %}
{
  "title": "{{ not_a_variable }}",
  "value": 123
}
{% endraw %}
```

Jinja **nie dotknie** tego fragmentu.

---

## Alternatywa: zmiana delimiterów (mało znana, bardzo przydatna)

Jeżeli boisz się kolizji z `{{ }}` (np. dokumentacja Jinja, Helm, Mustache):

```python
from jinja2 import Environment

env = Environment(
    variable_start_string='<<',
    variable_end_string='>>'
)

template = env.from_string("""
Example JSON:
{
  "title": "example"
}

Title: << title >>
Explanation: << explanation >>
""")

prompt = template.render(
    title=item["title"],
    explanation=item["explanation"]
)
```

To rozwiązanie jest **bardzo cenione w systemach promptowych**.

---

## Porównanie podejść

| Podejście | Bezpieczne dla JSON | Czytelność | Skalowalność |
|--------|------------------|-----------|--------------|
| `str.format()` | ❌ | ❌ | ❌ |
| `f-string` | ✔ | ✔ | ⚠ |
| **Jinja2** | ✔✔ | ✔✔ | ✔✔ |

---

## Rekomendacja architektoniczna (LLM / AI)

Dla długich promptów:
- trzymaj je jako **pliki `.j2`**
- wersjonuj je
- testuj renderowanie osobno
- traktuj jak **kontrakt wejścia do modelu**

---

Jeżeli chcesz, mogę:
- zaproponować **strukturę katalogów** dla promptów
- pokazać **test jednostkowy** dla renderowania
- albo porównać Jinja2 z `string.Template` z stdliba

Daj znać, w którą stronę chcesz iść.

---

**User:**

ok, mam inny błąd
openai.BadRequestError: Error code: 400 - [{'error': {'code': 400, 'message': 'Value is not a struct: 

---

**Assistant:**

Ten komunikat **nie pochodzi z Pythona**, tylko bezpośrednio z **walidacji payloadu po stronie OpenAI API**.  
Kluczowa część brzmi:

> **`Value is not a struct`**

W praktyce oznacza to:

➡ API **oczekiwało obiektu (dict / JSON object)**  
➡ a dostało **string, listę albo `None`**

---

## Najczęstsza przyczyna (bardzo typowa)

Po przejściu na Jinja2 lub refaktoryzacji promptów **jeden z parametrów requestu ma zły typ**.

### Przykład błędny (Responses API / Chat Completions)

```python
client.responses.create(
    model="gpt-4.1",
    input=prompt   # ❌ prompt jest stringiem
)
```

Podczas gdy API **oczekuje struktury**, np.:

```json
{
  "input": [
    {
      "role": "user",
      "content": [{ "type": "text", "text": "..." }]
    }
  ]
}
```

---

## Poprawne formy – w zależności od API

### ✅ Responses API (zalecane)

```python
response = client.responses.create(
    model="gpt-4.1",
    input=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt}
            ]
        }
    ]
)
```

**Jeżeli podasz sam string → `Value is not a struct`**

---

### ✅ Chat Completions (starsze, ale nadal spotykane)

```python
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "user", "content": prompt}
    ]
)
```

Tu `messages` **musi być listą obiektów**, nie stringiem.

---

## Inne częste źródła tego błędu

### 1. `response_format` w złym typie

```python
response_format="json"   # ❌
```

Zamiast:

```python
response_format={"type": "json_object"}  # ✅
```

---

### 2. `tools` / `functions` przekazane jako string

```python
tools="[]"   # ❌
```

Zamiast:

```python
tools=[]     # ✅
```

---

### 3. `metadata`, `input_text`, `content` = string zamiast dict/list

Każde pole opisane w dokumentacji jako **object / struct**  
→ **musi być dict-em**, nawet jeśli ma jedno pole.

---

## Jak szybko zdiagnozować

Dodaj przed wywołaniem API:

```python
import json
print(json.dumps(payload, indent=2))
```

I sprawdź:

- czy **każdy poziom jest dict/list**, nie string
- czy **nie masz JSON-a jako stringa**

---

## Co potrzebuję, żeby wskazać dokładnie linijkę

Wklej **minimalny fragment**:
- samo wywołanie `client.responses.create(...)`
- bez kluczy API, bez danych wrażliwych

Na tej podstawie wskażę **konkretnie**, które pole powoduje `Value is not a struct` i dlaczego.

---

**User:**

Wygląda to tak
response = client.chat.completions.create(
        model="gemini-3-pro-preview",
        messages=[
            {   "role": "system",
                "content": template.render(title=item["title"],explanation=item["explanation"])
            },
            {
                "role": "user",
                "content": [{"type": "text", "text": item["content"]}]
            }
        ]
    )

i taki mam błąd
openai.BadRequestError: Error code: 400 - [{'error': {'code': 400, 'message': 'Value is not a string: 

---

**Assistant:**

Błąd jest już bardzo precyzyjny i **wynika z niespójności formatu `messages`**.

Kluczowa część:

> **`Value is not a string`**

W **Chat Completions API** pole `content` **MUSI BYĆ STRINGIEM**.  
Ty mieszasz **dwa różne formaty API**.

---

## Co dokładnie jest nie tak

Masz:

```python
messages=[
    {
        "role": "system",
        "content": template.render(...)
    },
    {
        "role": "user",
        "content": [{"type": "text", "text": item["content"]}]
    }
]
```

### Problem

- `system.content` → ✅ string (OK)
- `user.content` → ❌ **lista obiektów**

Lista `{ "type": "text", "text": ... }` jest **formatem Responses API**,  
**NIE** Chat Completions API.

Chat Completions oczekuje:

```python
"content": "plain string"
```

---

## Poprawna wersja (minimalna zmiana)

```python
response = client.chat.completions.create(
    model="gemini-3-pro-preview",
    messages=[
        {
            "role": "system",
            "content": template.render(
                title=item["title"],
                explanation=item["explanation"]
            )
        },
        {
            "role": "user",
            "content": item["content"]   # ← STRING
        }
    ]
)
```

To **rozwiąże błąd `Value is not a string`**.

---

## Dlaczego wcześniej był `Value is not a struct`

Masz w kodzie **ślad migracji między API**:

| API | `content` |
|----|---------|
| Chat Completions | `str` |
| Responses API | `[{ "type": "text", "text": "..." }]` |

Najpierw podałeś string tam, gdzie oczekiwano struct  
Teraz podałeś struct tam, gdzie oczekiwano string

Objawy są różne, **przyczyna ta sama**.

---

## Rekomendacja architektoniczna (ważne)

### ❌ Nie mieszaj API
- Chat Completions **albo**
- Responses API

### ✅ Jeśli chcesz używać bloków (`type: text`, obrazy, tool calls)

Przejdź **w całości** na Responses API:

```python
response = client.responses.create(
    model="gemini-3-pro-preview",
    input=[
        {
            "role": "system",
            "content": [
                {"type": "text", "text": system_prompt}
            ]
        },
        {
            "role": "user",
            "content": [
                {"type": "text", "text": item["content"]}
            ]
        }
    ]
)
```

---

## TL;DR

- Chat Completions → `content` **musi być stringiem**
- Ty podałeś listę obiektów
- To jest **dokładnie powód** błędu 400
- Albo:
  - uprość do stringów
  - albo przejdź w 100% na Responses API

Jeżeli chcesz, mogę:
- pomóc Ci **świadomie wybrać API**
- albo przygotować **jednolity wrapper**, żebyś nie wpadł w to ponownie