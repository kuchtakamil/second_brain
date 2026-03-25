# Currying w Pythonie

**Data:** 2026-02-09

---

**User:**

Python i curring

---

**Assistant:**

Pewnie chodzi Ci o **currying w Pythonie** (często mylone pisownią jako *curring*).

To pojęcie z programowania funkcyjnego i w Pythonie jest **bardzo użyteczne**, szczególnie gdy budujesz API, pipeline’y, dekoratory albo funkcje wyższego rzędu.

---

## 🧠 Co to jest currying?

**Currying** to przekształcenie funkcji:

```
f(a, b, c)  →  f(a)(b)(c)
```

Czyli funkcja, która przyjmuje wiele argumentów naraz, zostaje zamieniona na serię funkcji przyjmujących po jednym argumencie.

---

## 🔹 Klasyczny przykład

### Bez currying

```python
def add(a, b):
    return a + b

add(2, 3)  # 5
```

### Z currying

```python
def add(a):
    def inner(b):
        return a + b
    return inner

add(2)(3)  # 5
```

`add(2)` zwraca nową funkcję, która "pamięta" `a = 2`.

To jest **closure** — fundament currying w Pythonie.

---

## 🔹 Dlaczego to ma sens w realnym kodzie?

Wyobraź sobie, że często robisz:

```python
send_request(url, timeout, headers, payload)
```

I w wielu miejscach `timeout` i `headers` są takie same.

Z currying:

```python
def send_request(timeout, headers):
    def with_url(url):
        def with_payload(payload):
            # faktyczna logika
            ...
        return with_payload
    return with_url
```

Teraz:

```python
api_call = send_request(5, {"Auth": "token"})
api_call("/users")({"name": "John"})
```

---

## 🔥 Pythonowe, praktyczne currying (czyli to co się naprawdę używa)

W Pythonie rzadko pisze się ręcznie takie zagnieżdżone funkcje. Używa się:

### ✅ `functools.partial` — „pythonowe currying”

To nie jest czyste currying matematyczne, ale w praktyce daje 95% korzyści.

```python
from functools import partial

def add(a, b):
    return a + b

add_2 = partial(add, 2)

add_2(3)  # 5
```

Tu powstaje funkcja, gdzie pierwszy argument jest już ustawiony.

---

## 🔹 Currying vs Partial — ważna różnica

| Cecha | Currying | `partial` |
|-------|----------|-----------|
| Argumenty po jednym | ✅ | ❌ |
| Pythonowe | ❌ | ✅ |
| Czytelne | ❌ | ✅ |
| Produkcyjnie używane | rzadko | bardzo często |

W Pythonie **prawie zawsze używa się `partial` zamiast prawdziwego currying**.

---

## 🔹 Przykład z realnego życia (np. map/filter)

Bez currying:

```python
def greater_than(x, y):
    return x > y

list(filter(lambda n: greater_than(n, 10), nums))
```

Z `partial`:

```python
gt_10 = partial(greater_than, y=10)
list(filter(gt_10, nums))
```

Bardziej deklaratywnie.

---

## 🔹 Automatyczne currying dekoratorem (dla ciekawych)

Możesz zrobić funkcję, która **automatycznie curry-uje dowolną funkcję**:

```python
def curry(func):
    def curried(*args):
        if len(args) >= func.__code__.co_argcount:
            return func(*args)
        return lambda *more: curried(*(args + more))
    return curried
```

Użycie:

```python
@curry
def add(a, b, c):
    return a + b + c

add(1)(2)(3)  # 6
add(1, 2)(3)  # 6
```

---

## 🧩 Dlaczego to jest potężne przy LLM / pipeline / clean architecture

Currying pozwala budować **konfigurowalne funkcje**:

```python
def llm_call(model, temperature, prompt):
    ...

gpt4 = partial(llm_call, "gpt-4", 0.2)
gpt4("Explain currying")
```

Masz funkcje „wyspecjalizowane konfiguracyjnie”, bez klas, bez DI, bez boilerplate.

To jest bardzo funkcyjne i bardzo eleganckie.

---

## 🧠 Mental model

Currying to:

> „funkcja, która produkuje coraz bardziej wyspecjalizowane funkcje”

To jest dokładnie to, co robisz w:
- builderach
- konfiguratorach
- middleware
- dekoratorach
- pipeline’ach

Tylko w wersji funkcyjnej.

---

## TL;DR

W Pythonie:

- Currying = koncept
- `functools.partial` = praktyczne narzędzie
- Closures = mechanizm
- Użyteczne do budowy konfigurowalnych funkcji i pipeline’ów

Jeśli chcesz, mogę pokazać **bardzo realny przykład currying w stylu „LLM assistant pipeline”**, gdzie to daje ogromną czystość kodu.