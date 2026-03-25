# Dodawanie list do słownika

**Data:** 2026-01-10

---

**User:**

jak w pyton mając słownik output = {} dodać do niego listę z innymi obiektami które mają property i property które są listą?

---

**Assistant:**

W Pythonie wszystko zależy od **docelowej struktury słownika** oraz od tego, **czy lista ma być wartością pod jednym kluczem**, czy **elementy listy mają być scalone z innymi danymi**. Poniżej pokazuję najczęstsze i poprawne wzorce.

---

## 1. Dodanie listy obiektów jako wartości pod kluczem

Załóżmy, że:
- `output` to słownik
- chcesz dodać klucz `"items"`
- jego wartością ma być lista obiektów (np. słowników)
- każdy obiekt ma pola, z których jedno jest listą

```python
output = {}

items = [
    {
        "id": 1,
        "name": "A",
        "tags": ["x", "y"]
    },
    {
        "id": 2,
        "name": "B",
        "tags": ["z"]
    }
]

output["items"] = items
```

Efekt:
```python
{
    "items": [
        {"id": 1, "name": "A", "tags": ["x", "y"]},
        {"id": 2, "name": "B", "tags": ["z"]}
    ]
}
```

---

## 2. Budowanie listy dynamicznie (np. w pętli)

Jeżeli lista ma być tworzona stopniowo:

```python
output = {"items": []}

for obj in source_objects:
    output["items"].append({
        "id": obj.id,
        "values": obj.values  # values jest listą
    })
```

To jest **najczęstszy i zalecany wzorzec**.

---

## 3. Obiekty klasowe → słowniki

Jeżeli masz obiekty klasowe, a nie słowniki:

```python
class Item:
    def __init__(self, id, values):
        self.id = id
        self.values = values  # lista

items = [
    Item(1, ["a", "b"]),
    Item(2, ["c"])
]

output = {
    "items": [
        {
            "id": item.id,
            "values": item.values
        }
        for item in items
    ]
}
```

---

## 4. Spłaszczanie list z obiektów (jeśli o to chodzi)

Jeżeli **property będące listą** ma zostać połączone w jedną listę w `output`:

```python
output = {"values": []}

for obj in items:
    output["values"].extend(obj.values)
```

Efekt:
```python
{"values": ["a", "b", "c"]}
```

---

## 5. Typowy błąd

Nie rób tak:

```python
output["items"] = {}
output["items"].append(...)
```

Słownik nie ma `append`. Lista – tak.

---

## Podsumowanie – wzorzec referencyjny

Jeżeli:
- `output` to słownik
- chcesz dodać **listę obiektów**
- obiekty mają pola, w tym listy

to **kanoniczne rozwiązanie** wygląda tak:

```python
output = {"items": []}

for obj in objects:
    output["items"].append({
        "property": obj.property,
        "list_property": obj.list_property
    })
```

Jeżeli chcesz, możesz doprecyzować:
- jak wygląda **dokładna struktura danych wejściowych**
- czy obiekty są słownikami czy instancjami klas
- jaki ma być **finalny JSON**

i pokażę rozwiązanie dokładnie pod ten przypadek.

---

**User:**

Mam taki json
[{
    "title": "The Art of Interruption & Managing Flow",
    "focus": "Techniques for fluid entry and dynamic control in professional or social discourse.",
    "phrases": [
        {
            "expression": "Sorry to cut you off",
            "context": "Polite interruption to address a point while it is still relevant.",
            "type": "standard_polite"
        },
        {
            "expression": "If I could just chime in here",
            "context": "Professional/group setting interruption used to add a brief comment.",
            "type": "professional"
        },
        {
            "expression": "Fill me in",
            "context": "Requesting a concise briefing or status update on a situation you missed.",
            "type": "idiomatic"
        }
    ]
},
{...}
]
i chcę przenieść wartości tak:

[
 {
        "title": "title",
        "explanation": "focus",
        "content": [
            "expression — context",
            "expression — context",
           "expression — context",
    ]
}
]

---

**Assistant:**

Poniżej masz **jednoznaczne i poprawne przekształcenie struktury JSON → JSON w Pythonie**, dokładnie według opisu.

Zakładam, że:
- wejście to **lista słowników**
- pole `phrases` jest listą obiektów
- `content` ma być listą stringów w formacie  
  `"<expression> — <context>"` (prawdziwa pauza, nie minus)

---

## Przykładowe dane wejściowe

```python
input_data = [
    {
        "title": "The Art of Interruption & Managing Flow",
        "focus": "Techniques for fluid entry and dynamic control in professional or social discourse.",
        "phrases": [
            {
                "expression": "Sorry to cut you off",
                "context": "Polite interruption to address a point while it is still relevant.",
                "type": "standard_polite"
            },
            {
                "expression": "If I could just chime in here",
                "context": "Professional/group setting interruption used to add a brief comment.",
                "type": "professional"
            },
            {
                "expression": "Fill me in",
                "context": "Requesting a concise briefing or status update on a situation you missed.",
                "type": "idiomatic"
            }
        ]
    }
]
```

---

## Transformacja (czytelna i produkcyjna)

```python
output = []

for item in input_data:
    output.append({
        "title": item["title"],
        "explanation": item["focus"],
        "content": [
            f'{p["expression"]} — {p["context"]}'
            for p in item.get("phrases", [])
        ]
    })
```

---

## Wynik

```python
[
    {
        "title": "The Art of Interruption & Managing Flow",
        "explanation": "Techniques for fluid entry and dynamic control in professional or social discourse.",
        "content": [
            "Sorry to cut you off — Polite interruption to address a point while it is still relevant.",
            "If I could just chime in here — Professional/group setting interruption used to add a brief comment.",
            "Fill me in — Requesting a concise briefing or status update on a situation you missed."
        ]
    }
]
```

---

## Wariant funkcyjny (jeżeli chcesz to wielokrotnie wykorzystywać)

```python
def transform(data: list[dict]) -> list[dict]:
    return [
        {
            "title": item["title"],
            "explanation": item["focus"],
            "content": [
                f'{p["expression"]} — {p["context"]}'
                for p in item.get("phrases", [])
            ]
        }
        for item in data
    ]
```

---

## Uwagi inżynierskie
- `item.get("phrases", [])` zabezpiecza przed brakującym kluczem
- `type` jest celowo pominięte (nie występuje w docelowej strukturze)
- wynik jest **gotowy do serializacji do JSON**

Jeżeli chcesz:
- grupować `content` po `type`
- zmienić separator
- zachować `type` w nawiasach
- generować Markdown / HTML

— daj znać, pokażę odpowiedni wariant.

---

**User:**

OK, chcę teraz wydrukować wynik w ładnej formie sformatowanego jsona 
zrobiłem print(json.dumps(output))
i wypisuje w jednej linii  w dodatku np, tak
"content": ["I'll sleep on it \u2014 Delaying a decision until the following day to allow for reflection.", "I\u2019ll give it some thought

---

**Assistant:**

To jest oczekiwane zachowanie `json.dumps()` bez dodatkowych parametrów. Musisz jawnie włączyć **ładne formatowanie** oraz **obsługę znaków Unicode**.

Użyj następującej postaci:

```python
import json

print(json.dumps(output, indent=2, ensure_ascii=False))
```

---

## Co robią te parametry

### `indent=2`
- powoduje wieloliniowe formatowanie
- ustawia wcięcia (2 spacje; możesz użyć 4, jeśli wolisz)

### `ensure_ascii=False`
- **nie ucieka znaków Unicode**
- zamiast `\u2014` zobaczysz `—`
- zamiast `\u2019` zobaczysz `’`

---

## Przykładowy wynik

```json
[
  {
    "title": "The Art of Interruption & Managing Flow",
    "explanation": "Techniques for fluid entry and dynamic control in professional or social discourse.",
    "content": [
      "I'll sleep on it — Delaying a decision until the following day to allow for reflection.",
      "I’ll give it some thought — Considering an idea before making a decision."
    ]
  }
]
```

---

## Dodatkowe opcje (jeżeli chcesz „jeszcze ładniej”)

### Sortowanie kluczy
```python
print(json.dumps(output, indent=2, ensure_ascii=False, sort_keys=True))
```

### Inne wcięcie
```python
print(json.dumps(output, indent=4, ensure_ascii=False))
```

---

## Uwaga praktyczna
Jeżeli zapisujesz do pliku:

```python
with open("output.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)
```

To **encoding="utf-8" jest obowiązkowy**, inaczej znaki typograficzne mogą się wysypać.

Jeżeli chcesz:
- format kompatybilny z Prettier / jq
- pretty-print w jednej linii na element listy
- streaming dużych JSON-ów

— powiedz, pokażę odpowiedni wariant.