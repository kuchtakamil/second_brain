# Split tekstu w Pythonie

**Data:** 2025-12-19

---

**User:**

jak w python zrobić split lini tekstu po \n lub \n\n

---

**Assistant:**

W Pythonie masz kilka poprawnych opcji – wybór zależy od tego, **czy chcesz traktować `\n\n` inaczej niż pojedyncze `\n`**, czy po prostu rozbić tekst na logiczne linie / bloki.

---

## 1. Split po **jednym lub wielu znakach nowej linii** (najczęstszy przypadek)

Jeżeli **nie interesuje Cię różnica między `\n` a `\n\n`**:

```python
lines = text.splitlines()
```

**Zalety:**
- Obsługuje `\n`, `\r\n`, `\r`
- Ignoruje puste linie na końcu
- Czytelne i idiomatyczne

Jeżeli chcesz **zachować puste linie**:

```python
lines = text.splitlines(keepends=False)
```

---

## 2. Split na **bloki oddzielone pustą linią (`\n\n`)**

Jeżeli chcesz np. **akapitów**:

```python
blocks = text.split("\n\n")
```

Uwaga: jeżeli w tekście mogą występować `\n\n\n`, dostaniesz puste elementy.

Lepsza wersja:

```python
blocks = [b for b in text.split("\n\n") if b.strip()]
```

---

## 3. Split po **`\n` LUB `\n\n`** z użyciem regexa

Jeżeli chcesz mieć **jednoznaczną regułę: jeden lub więcej znaków nowej linii**:

```python
import re

parts = re.split(r"\n+", text)
```

To jest najbliższe literalnie temu, o co pytasz.

---

## 4. Najbardziej „pythonowa” i odporna wersja (rekomendowana)

Jeżeli Twoim celem są **logiczne linie tekstu**, a nie dokładna liczba `\n`:

```python
parts = [line for line in text.splitlines() if line.strip()]
```

Usuwa:
- puste linie
- wielokrotne `\n`
- różne zakończenia linii

---

## Rekomendacja praktyczna

| Cel | Rozwiązanie |
|----|------------|
| Linie tekstu | `splitlines()` |
| Akapity | `re.split(r"\n\s*\n", text)` |
| Jeden lub więcej `\n` | `re.split(r"\n+", text)` |

Jeżeli chcesz, mogę dobrać rozwiązanie dokładnie pod Twój przypadek (np. parsowanie logów, Markdown, LLM input, itp.).

---

**User:**

jak mogę zrobić 
lines = content.splitlines().map(str.strip)

---

**Assistant:**

W Pythonie **nie ma metody `map` na liście** (to częsty skrót myślowy z JS / Stream API w Javie). Masz kilka poprawnych i idiomatycznych odpowiedników.

---

## 1. Najbardziej pythonowa wersja (list comprehension)

```python
lines = [line.strip() for line in content.splitlines()]
```

To jest **rekomendowane** rozwiązanie:
- czytelne
- szybkie
- standard w ekosystemie

---

## 2. Z użyciem wbudowanego `map`

```python
lines = list(map(str.strip, content.splitlines()))
```

Poprawne, ale:
- mniej czytelne
- trudniejsze do debugowania
- rzadziej spotykane w realnym kodzie

---

## 3. Strip + filtrowanie pustych linii (częsty przypadek)

Jeżeli chcesz jednocześnie:
- usunąć białe znaki
- pozbyć się pustych linii

```python
lines = [line.strip() for line in content.splitlines() if line.strip()]
```

---

## 4. Odpowiednik „streamowy” (jeśli chcesz lazy evaluation)

```python
lines = (line.strip() for line in content.splitlines())
```

Zwraca generator, nie listę.

---

## 5. Dlaczego `content.splitlines().map(...)` nie działa?

- `splitlines()` → `list[str]`
- `list` **nie ma metody `map`**
- `map` w Pythonie jest **funkcją globalną**, nie metodą obiektu

To jest istotna różnica względem:
- Java Streams
- JavaScript Array.prototype.map

---

### TL;DR

Chcesz tego:

```python
lines = [line.strip() for line in content.splitlines()]
```

Jeżeli przetwarzasz duże pliki albo dane pod LLM (co u Ciebie jest bardzo prawdopodobne), generator z pkt 4 bywa lepszym wyborem.

---

**User:**

lines = [line.strip() for line in content.splitlines() if line.strip()]
results.append(lines)

takie rozwiązanie dodaje listę i w results mam listę list. Jak dodać tylko elementy z listy lines?

---

**Assistant:**

Masz **dwie poprawne opcje**, w zależności od tego, czy chcesz **rozszerzyć listę `results` elementami**, czy zachować inne zachowanie strukturalne.

---

## 1. Poprawne rozwiązanie: `extend` (to dokładnie to, czego chcesz)

```python
lines = [line.strip() for line in content.splitlines() if line.strip()]
results.extend(lines)
```

Efekt:
```python
results == ["linia1", "linia2", "linia3", ...]
```

Zamiast:
```python
[["linia1", "linia2"], ["linia3"]]
```

To jest **idiomatyczne i czytelne**.

---

## 2. Równoważne rozwiązanie z operatorem `+=`

```python
results += lines
```

Działa identycznie jak `extend`, ale:
- trochę mniej czytelne semantycznie
- łatwiej o błąd, jeżeli `results` nie jest listą

---

## 3. Czego NIE robić (częsty błąd)

```python
results.append(lines)  # ❌
```

Bo `append`:
- zawsze dodaje **jeden element**
- nie „rozpakowuje” listy

---

## 4. Alternatywa funkcyjna (jeżeli przetwarzasz wiele bloków)

Jeżeli robisz to w pętli i chcesz mieć to w jednej linijce:

```python
results = [
    line.strip()
    for content in contents
    for line in content.splitlines()
    if line.strip()
]
```

---

### TL;DR

Zamień:

```python
results.append(lines)
```

na:

```python
results.extend(lines)
```

To jest dokładny odpowiednik semantyczny tego, czego oczekujesz.