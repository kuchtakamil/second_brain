# Dodanie pakietu do requirements

**Data:** 2025-12-17

---

**User:**

w python robię from langchain_text_splitters import MarkdownHeaderTextSplitter
Jak mam się rowiedzieć co mam dodać w pliku requirements.txt?

---

**Assistant:**

W Pythonie **`requirements.txt` zawsze zawiera nazwy pakietów z PyPI**, a **nie nazwy modułów/importów**, więc nie wynika on 1-do-1 z instrukcji `import`.

W Twoim przypadku:

```python
from langchain_text_splitters import MarkdownHeaderTextSplitter
```

oznacza, że musisz dodać do `requirements.txt` **pakiet**, który dostarcza moduł `langchain_text_splitters`.

### Co dokładnie dodać

```text
langchain-text-splitters
```

Opcjonalnie (rekomendowane w projektach produkcyjnych) z wersją:

```text
langchain-text-splitters==0.0.1
```

lub zakres:

```text
langchain-text-splitters>=0.0.1,<1.0.0
```

---

### Jak samodzielnie to ustalić (uniwersalna metoda)

#### 1. Sprawdź dokumentację / PyPI
Najpewniejsza droga:
- Szukasz w PyPI nazwy modułu → zwykle jest identyczna lub bardzo podobna  
- W tym przypadku:  
  `langchain_text_splitters` → `langchain-text-splitters`

#### 2. Sprawdź lokalnie, z jakiego pakietu pochodzi moduł
Jeśli masz już środowisko:

```bash
pip show langchain-text-splitters
```

albo:

```bash
pip list | grep langchain
```

#### 3. Z poziomu Pythona
Możesz sprawdzić, gdzie fizycznie leży moduł:

```python
import langchain_text_splitters
print(langchain_text_splitters.__file__)
```

To pokaże ścieżkę w `site-packages`, z której łatwo dojść do nazwy pakietu.

---

### Uwaga specyficzna dla LangChain (ważne)
LangChain **rozbił się na wiele mniejszych pakietów**, więc:
- dawniej wystarczało `langchain`
- obecnie **każdy komponent ma osobny pakiet**

Dlatego **nie dodawaj już automatycznie `langchain`**, tylko dokładnie te moduły, których używasz.

---

Jeżeli chcesz, mogę:
- przeanalizować cały Twój plik z importami i wygenerować kompletne `requirements.txt`
- zaproponować minimalny zestaw zależności pod projekt z LangChain + lokalne LLM (Ollama)