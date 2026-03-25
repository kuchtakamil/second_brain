# LangChain prompt przykład

**Data:** 2025-11-11

---

**User:**

Używając LangChain chcę wysłać do mojego kontat platform open ai prompt. Chcę go podzielić na system i user prompt. Podaj przykład

---

**Assistant:**

Oczywiście — oto prosty przykład, jak wysłać prompt do modelu OpenAI za pomocą **LangChain**, rozdzielając go na część *system* i *user* (czyli tak, jak robi to ChatGPT):  

```python
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# Inicjalizacja modelu (możesz ustawić np. gpt-4o-mini)
llm = ChatOpenAI(
    model="gpt-4o-mini",  # lub np. "gpt-4-turbo"
    api_key="YOUR_OPENAI_API_KEY"
)

# Definiujemy wiadomości
messages = [
    SystemMessage(content="Jesteś pomocnym asystentem, który odpowiada zwięźle i rzeczowo."),
    HumanMessage(content="Wyjaśnij w prosty sposób, jak działa model transformera.")
]

# Wysyłamy zapytanie
response = llm.invoke(messages)

# Wyświetlamy odpowiedź
print(response.content)
```

### Objaśnienie:
- `SystemMessage` – ustawia kontekst modelu (np. jego osobowość, ton, ograniczenia).
- `HumanMessage` – to faktyczna treść pytania użytkownika.
- `invoke()` – wysyła listę wiadomości do modelu (możesz też użyć `llm(messages)` w nowszych wersjach LangChain).

Jeśli chcesz dodać kolejne kroki konwersacji, możesz kontynuować listę `messages` dodając więcej `HumanMessage` i `AIMessage`.

Chcesz, żebym pokazał też przykład z **ChatPromptTemplate**, czyli zbudowaniem promptu w stylu “chain” (np. do integracji z pipeline)?

---

**User:**

ok jak używając poetry dodać zależności żeby nie było błędów w tym kodzie?

---

**Assistant:**

Aby ten kod działał poprawnie w projekcie zarządzanym przez **Poetry**, musisz zainstalować odpowiednie paczki. Wystarczy wykonać poniższe polecenia w katalogu projektu:

```bash
poetry add langchain langchain-openai
```

To zainstaluje:
- `langchain` – główną bibliotekę frameworka,
- `langchain-openai` – oficjalny pakiet integrujący LangChain z API OpenAI (nowy, zalecany zamiast starego `openai`).

---

### Dodatkowe uwagi

1. Jeśli chcesz testować kod interaktywnie (np. w notebooku Jupyter):
   ```bash
   poetry add jupyter ipykernel
   ```

2. Jeśli chcesz używać zmiennych środowiskowych (np. `OPENAI_API_KEY` z `.env`):
   ```bash
   poetry add python-dotenv
   ```
   i wtedy w kodzie możesz dodać:
   ```python
   from dotenv import load_dotenv
   load_dotenv()
   ```

---

### Minimalny `pyproject.toml`
Po dodaniu zależności, twój plik może wyglądać mniej więcej tak:

```toml
[tool.poetry]
name = "langchain-test"
version = "0.1.0"
description = "Test LangChain + OpenAI"
authors = ["Twoje Imię <twojemail@example.com>"]
python = "^3.10"

[tool.poetry.dependencies]
python = "^3.10"
langchain = "*"
langchain-openai = "*"
python-dotenv = "*"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

---

Chcesz, żebym dodał też przykład, jak ustawić `OPENAI_API_KEY` przez `.env` i użyć go w kodzie, żeby nie trzymać klucza w kodzie źródłowym?

---

**User:**

wciąż błąd dla from langchain.schema import SystemMessage, HumanMessage

---

**Assistant:**

Tak, to się zgadza — w nowszych wersjach LangChain zmieniła się struktura importów.  
W aktualnych wersjach (`langchain >= 0.2.x`) poprawny import wygląda tak:

```python
from langchain_core.messages import SystemMessage, HumanMessage
```

---

### Pełny działający przykład

```python
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# Inicjalizacja modelu
llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key="YOUR_OPENAI_API_KEY"
)

# Definicja promptu
messages = [
    SystemMessage(content="Jesteś pomocnym asystentem."),
    HumanMessage(content="Wyjaśnij prostym językiem, jak działa model transformera.")
]

# Wykonanie zapytania
response = llm.invoke(messages)

print(response.content)
```

---

### Upewnij się, że masz aktualne wersje bibliotek:

```bash
poetry add langchain-core langchain-openai
```

lub (jeśli chcesz mieć całość LangChain bez dzielenia na moduły):

```bash
poetry add langchain langchain-openai
```

---

💡 **Dlaczego zmiana?**  
W nowej architekturze LangChain podzielono projekt na mniejsze pakiety:
- `langchain-core` – zawiera podstawowe klasy (`SystemMessage`, `HumanMessage`, `ChatPromptTemplate` itp.),
- `langchain-openai` – integracja z API OpenAI.

---

Chcesz, żebym pokazał też przykład z użyciem `ChatPromptTemplate`, który łączy system i user prompt w jeden obiekt promptu (wygodne do pipeline’ów)?