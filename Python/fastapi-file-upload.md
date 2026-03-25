# FastAPI File Upload

**Data:** 2025-07-09

---

**User:**

def upload_documents(files: List[UploadFile] = File(...)):
co to oznacza 
= File(...)

---

**Assistant:**

Wyrażenie `= File(...)` w kontekście FastAPI oznacza, że dany parametr funkcji (`files` w tym przypadku) powinien być traktowany jako plik przesyłany w żądaniu HTTP typu multipart/form-data.

Szczegóły:

```python
from fastapi import File, UploadFile
from typing import List

def upload_documents(files: List[UploadFile] = File(...)):
```

### Co oznacza `= File(...)`?

- `File(...)` to funkcja pomocnicza FastAPI, która:
  - oznacza, że wartość tego parametru ma pochodzić z przesłanego pliku (czyli z formularza).
  - `...` (trzy kropki) oznacza, że parametr jest **wymagany** (to odpowiednik `required=True`).
  
### Co robi cały zapis?

- `files: List[UploadFile]` — FastAPI spodziewa się **listy plików** przesłanych przez użytkownika.
- `= File(...)` — mówi FastAPI, że pliki mają być pobierane z żądania typu multipart/form-data.

### Przykład użycia

Użytkownik może przesłać wiele plików poprzez formularz HTML lub narzędzie takie jak Postman, a FastAPI automatycznie przekształci je na listę obiektów `UploadFile`.

### Alternatywa

Jeśli nie użyjesz `File(...)`, FastAPI nie będzie wiedzieć, że chodzi o pliki z formularza, więc nie zmapuje ich poprawnie.

---

Jeśli potrzebujesz przykładu całego endpointa z takim uploadem — mogę podesłać.

---

**User:**

"Jeśli nie użyjesz File(...), FastAPI nie będzie wiedzieć, że chodzi o pliki z formularza, więc nie zmapuje ich poprawnie."
ale dlaczego skoro już jest napisane że ma być to lista UploadFile?

---

**Assistant:**

To bardzo dobre pytanie — i kluczowe dla zrozumienia działania FastAPI.

### Dlaczego sama adnotacja `List[UploadFile]` nie wystarcza?

W FastAPI (i ogólnie w Pydanticu), adnotacje typu takie jak `List[UploadFile]` mówią **jaki typ danych** spodziewany jest w danym parametrze. **Nie mówią natomiast skąd te dane mają pochodzić** (czy z query, body, plików, itp.).

### FastAPI musi wiedzieć **skąd** pobrać dane

FastAPI interpretuje parametry funkcji na podstawie:

- typu danych (`int`, `str`, `UploadFile`, `List[UploadFile]`),
- miejsca ich występowania w definicji funkcji (czy są w `*args`, czy mają domyślne wartości),
- oraz **funkcji pomocniczych**, takich jak `Query`, `Body`, `File`, `Form`, itp.

To właśnie te funkcje (`File`, `Form`, itd.) mówią FastAPI **jak wyciągnąć dane z żądania HTTP**.

#### Przykład:

```python
# Błędne — FastAPI nie wie, że to mają być pliki z formularza multipart
def upload(files: List[UploadFile]):
    ...
```

Tutaj FastAPI przyjmie, że `files` pochodzi z **query params** (bo nie ma `File(...)`, `Body(...)` ani `Form(...)`), co oczywiście nie zadziała — nie da się przesłać plików przez query.

#### Poprawnie:

```python
def upload(files: List[UploadFile] = File(...)):
    ...
```

Tutaj `File(...)` mówi: „ten parametr pochodzi z formularza typu `multipart/form-data` i jest wymagany”.

### Podsumowując

- `List[UploadFile]` → mówi **co** to za dane (lista plików),
- `File(...)` → mówi **skąd** te dane pobrać (z formularza multipart).

Obie informacje są potrzebne FastAPI do poprawnego działania.

---

**User:**

czy znak = powinno się tu traktować jak operator przypisania?

---

**Assistant:**

Tak, znak `=` w tym kontekście **formalnie jest operatorem przypisania**, ale jego znaczenie w definicji funkcji w Pythonie jest trochę inne niż przy zwykłym przypisaniu.

### W definicji funkcji `=` oznacza **wartość domyślną parametru**

Przykład ogólny:

```python
def foo(x=10):
    ...
```

Tutaj `x` ma domyślną wartość `10`, jeśli nie zostanie przekazana przy wywołaniu funkcji.

---

### W FastAPI:

```python
def upload_documents(files: List[UploadFile] = File(...)):
```

Tutaj `= File(...)` ustawia domyślną wartość parametru `files` na wynik wywołania funkcji `File(...)`. Ale to **nie jest** domyślna wartość w sensie "jeśli nie podano, to wstaw tę wartość" — tylko:

- `File(...)` jest obiektem specjalnym, który zawiera **metadane** potrzebne FastAPI (np. że to ma być multipart, typ pliku, wymagany lub nie, itd.),
- a `=` jest nadal standardowym przypisaniem domyślnej wartości w definicji funkcji — tylko ta wartość to właśnie `File(...)`.

---

### Czyli:

- **Tak**, to `=` jest formalnie operatorem przypisania domyślnej wartości parametru funkcji.
- **Ale** w FastAPI ta "wartość domyślna" (np. `File(...)`, `Body(...)`, `Query(...)`) służy do określenia **źródła i sposobu przetwarzania** danego parametru przez framework — nie do faktycznego ustawienia domyślnej wartości jak `x=5`.

Dla porównania:

```python
def example(id: int = 1):            # domyślna wartość 1
def example(id: int = Query(1)):     # domyślna wartość 1 z query string
def example(file: UploadFile = File(...)):  # wymagany plik z formularza
```