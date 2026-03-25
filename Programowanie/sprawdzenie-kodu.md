# Sprawdzenie kodu

**Data:** 2025-11-23

---

**User:**

sprawdź czy kod jej poprawny
def make_it_easier(read_path: Path, write_path: Path):
    llm = ChatOpenAI(model="gpt-5-mini")

    # transcript_dict = {}
    with open(read_path, "r", encoding="utf-8") as f_read:
        transcript_dict = json.load(f_read)

    result_dict = {}
    with open(write_path, "w", encoding="utf-8") as f_write:
        counter = 0
        for key, val in transcript_dict.items():
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=val)
            ]
            response = llm.invoke(messages)
            result_dict[key] = response
            counter = counter + 1
            if (counter % 10) == 0:
                json.dump(result_dict, f_write, ensure_ascii=False, indent=2)

        json.dump(result_dict, f_write, ensure_ascii=False, indent=2)

---

**Assistant:**

Kod ma kilka problemów i pułapek, które mogą spowodować błędy lub niepoprawne działanie. Poniżej konkretne uwagi:

---

## ❗ Problemy

### 1. **`response` nie jest serializowalny do JSON**
`llm.invoke()` zwraca zwykle obiekt typu `AIMessage` lub podobny, a nie czysty tekst.  
`json.dump()` wyrzuci błąd:  
```
TypeError: Object of type AIMessage is not JSON serializable
```

Musisz użyć `response.content`.

### 2. **Pisanie do pliku w trakcie iteracji usuwa poprzednią zawartość**
Plik jest otwarty w trybie `"w"` — każde `json.dump()` nadpisuje plik od początku.

Najprościej zapisywać całość **po pętli**, albo użyć `"r+"` i ręcznie przesuwać wskaźnik.

### 3. **`result_dict` jest dumpowane dwa razy**
Pierwszy dump co 10 elementów, drugi na końcu.  
Jeśli pętla zatrzyma się po dumpie, a później wystąpi błąd – stracisz dane.

### 4. **Brakuje importów**
Potrzebujesz: `json`, `Path`, `ChatOpenAI`, `SystemMessage`, `HumanMessage`.

### 5. **`system_prompt` musi być wcześniej zdefiniowany**

---

## ✔️ Poprawiona wersja (bez zmian logiki, tylko poprawki)

```python
import json
from pathlib import Path
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

def make_it_easier(read_path: Path, write_path: Path):
    llm = ChatOpenAI(model="gpt-5-mini")

    with open(read_path, "r", encoding="utf-8") as f_read:
        transcript_dict = json.load(f_read)

    result_dict = {}
    counter = 0

    for key, val in transcript_dict.items():
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=val)
        ]
        response = llm.invoke(messages)
        result_dict[key] = response.content
        counter += 1

    with open(write_path, "w", encoding="utf-8") as f_write:
        json.dump(result_dict, f_write, ensure_ascii=False, indent=2)
```

---

## Jeśli chcesz *zrzucać co 10 rekordów*, trzeba użyć innej strategii
Np.:

- trzymać zapisany JSON w pamięci i nadpisywać cały plik
- albo dopisywać liniowo w formacie JSONL (najbezpieczniejsze)

Mogę przygotować poprawną wersję z **inkrementalnym zapisem**, jeśli tego potrzebujesz.

---

**User:**

tak chce robić backup co 10, do tego samego, jednego pliku

---

**Assistant:**

Poniżej masz wersję, która:

- zapisuje **co 10 rekordów**,
- nie traci wcześniejszych danych,
- **nadpisuje cały plik** za każdym razem,
- zawsze zapisuje poprawny JSON,
- obsługuje `response.content`.

To najbezpieczniejsza metoda, jeśli koniecznie musi być jeden plik, a nie JSONL.

---

## ✔️ Wersja z poprawnym backupem co 10 elementów

```python
import json
from pathlib import Path
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

def make_it_easier(read_path: Path, write_path: Path):
    llm = ChatOpenAI(model="gpt-5-mini")

    with open(read_path, "r", encoding="utf-8") as f_read:
        transcript_dict = json.load(f_read)

    result_dict = {}
    counter = 0

    for key, val in transcript_dict.items():
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=val)
        ]
        response = llm.invoke(messages)
        result_dict[key] = response.content
        counter += 1

        # backup co 10
        if counter % 10 == 0:
            with open(write_path, "w", encoding="utf-8") as f_write:
                json.dump(result_dict, f_write, ensure_ascii=False, indent=2)

    # finalny zapis po zakończeniu
    with open(write_path, "w", encoding="utf-8") as f_write:
        json.dump(result_dict, f_write, ensure_ascii=False, indent=2)
```

---

## Dlaczego ta wersja działa poprawnie?

- **Nie zapisuje do tego samego uchwytu pliku w środku pętli**, więc nie zostaje śmieci po poprzednich dumpach.
- **Zawsze nadpisuje cały plik** – masz gwarancję, że zawartość jest spójna.
- Jeśli program padnie między backupami, tracisz maksymalnie 9 rekordów.
- `AIMessage` jest zamieniony na `response.content`.

---

Jeśli chcesz, mogę przygotować alternatywę z:

- JSONL (bezpieczniejsze),
- lockiem na plik,
- obsługą wznawiania po przerwaniu,
- logowaniem czasu operacji.

---

**User:**

czy mogę podać ścieżkę do pliku który jeszcze nie istnieje jeśli chodzi o write_path?

---

**Assistant:**

Tak, możesz — Python utworzy **plik, jeśli go nie ma**, ale tylko pod warunkiem, że **katalog nadrzędny istnieje**.

### ✔️ Działa
Jeśli `write_path` wskazuje na plik, np.:

```
/home/user/output/result.json
```

a katalog `/home/user/output` istnieje, to:

```python
with open(write_path, "w", encoding="utf-8") as f:
    ...
```

**utworzy nowy plik** `result.json`.

### ❗ Nie działa
Jeśli katalog nie istnieje, np.:

```
/home/user/output_new/result.json
```

a `output_new` nie ma — wtedy dostaniesz:

```
FileNotFoundError: [Errno 2] No such file or directory
```

### ✔️ Jak upewnić się, że katalog istnieje?
Możesz to zrobić przed otwarciem pliku:

```python
write_path.parent.mkdir(parents=True, exist_ok=True)
```

Przykład:

```python
write_path.parent.mkdir(parents=True, exist_ok=True)

with open(write_path, "w", encoding="utf-8") as f_write:
    json.dump(result_dict, f_write, ensure_ascii=False, indent=2)
```

Jeśli chcesz, mogę też przygotować funkcję, która sama ogarnia tworzenie brakujących katalogów.

---

**User:**

W przypadku gdy chciałbym użyć Gemini API a nie OpenAI API czego zamiast
from langchain_openai import ChatOpenAI
powinienem użyć

---

**Assistant:**

W przypadku używania **Gemini API (Google)** zamiast OpenAI, w LangChain używasz:

```python
from langchain_google_genai import ChatGoogleGenerativeAI
```

To jest bezpośredni odpowiednik `ChatOpenAI`, tylko dla modeli Gemini.

### Minimalny przykład

```python
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    api_key="...jeśli nie masz w ENV..."
)

response = llm.invoke("Hello")
print(response.content)
```

### Wersja do twojego kodu

Zastępujesz:

```python
from langchain_openai import ChatOpenAI
```

przez:

```python
from langchain_google_genai import ChatGoogleGenerativeAI
```

i tworzysz obiekt:

```python
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")
```

Jeśli chcesz, mogę przygotować pełną wersję twojej funkcji działającą z Gemini.