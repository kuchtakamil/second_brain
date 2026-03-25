# Zaawansowane zagadnienia w Pythonie

**Data:** 2025-05-02

---

**User:**

jestem doświadczonym. programistą, od jakiegoś czasu powoli poznaję python. Potrzebuję listę zagadnień zaawansowanych które muszę poznać.

---

**Assistant:**

Świetnie, że już poznajesz Pythona – mając doświadczenie programistyczne, przeskok do zaawansowanego poziomu będzie dla Ciebie znacznie łatwiejszy. Poniżej znajdziesz listę **zaawansowanych zagadnień w Pythonie**, które warto opanować, by naprawdę dobrze czuć ten język – zarówno od strony idiomatycznej, jak i technicznej.

---

### 🔁 **Zaawansowane aspekty języka**
- **Dekoratory** – funkcje wyższego rzędu, modyfikujące zachowanie innych funkcji.
- **Generatory i iteratory** – `yield`, `__iter__`, `__next__`, lazy evaluation.
- **Funkcje jako obiekty pierwszoklasowe** – przekazywanie, zwracanie funkcji, `functools`.
- **List / dict comprehensions i generator expressions**.
- **Metaprogramowanie**:
  - `getattr`, `setattr`, `hasattr`, `__getattr__`, `__setattribute__`.
  - Tworzenie klas dynamicznie (`type`, `metaclasses`).
- **Context managers** – `with`, `__enter__`, `__exit__`, `contextlib`.

---

### 🧱 **Struktury danych i standardowa biblioteka**
- **`collections`** (`deque`, `defaultdict`, `Counter`, `namedtuple`, `ChainMap`, `UserDict`).
- **`itertools`** i **`functools`** – programowanie funkcyjne.
- **`heapq`, `bisect`, `array`** – niskopoziomowe struktury.
- **`dataclasses`** – wygodne struktury danych z domyślnymi metodami.

---

### 🧵 **Wielowątkowość i równoległość**
- **`threading`, `multiprocessing`, `concurrent.futures`**.
- **Global Interpreter Lock (GIL)** – jak działa i co to oznacza.
- **`asyncio`** – programowanie asynchroniczne i event loop.
- **`aiohttp`, `httpx`, `asyncpg`** – biblioteki async.

---

### 🧪 **Testowanie i jakość kodu**
- **`unittest`, `pytest`**, `mock`, `hypothesis`.
- **Testy parametrów, testy funkcjonalne, testy integracyjne**.
- **Linting i formatting**: `flake8`, `black`, `pylint`, `mypy`.

---

### 🧰 **Zarządzanie kodem i środowiskiem**
- **Wirtualne środowiska**: `venv`, `virtualenv`, `pipenv`, `poetry`.
- **Zarządzanie zależnościami i wersjami pakietów**.
- **Pisanie własnych paczek i publikowanie na PyPI**.

---

### 🔍 **Debugowanie i profilowanie**
- **`pdb`, `ipdb`**, debugowanie interaktywne.
- **Profilowanie**: `cProfile`, `line_profiler`, `memory_profiler`.

---

### 🛠️ **Interoperacyjność i integracje**
- **FFI / Ctypes / Cython / PyO3 (Rust)** – integracja z kodem C/C++/Rust.
- **Serializacja**: `pickle`, `json`, `marshal`.

---

### ☁️ **Zastosowania praktyczne**
- **Web development**: Flask, FastAPI, Django (zaawansowane funkcje).
- **Data engineering / ETL**: Pandas, Dask, Airflow.
- **ML/AI**: NumPy, scikit-learn, PyTorch, TensorFlow.
- **CLI / skrypty**: `argparse`, `click`, `typer`.

---

### 🧠 **Python idioms & best practices**
- Zasada EAFP vs LBYL.
- Duck typing, typowanie statyczne (PEP 484, `typing`, `mypy`).
- PEP8, idiomatyczne konstrukcje.
- Clean code w stylu pythonowym.

---

Chcesz listę w formie checklisty do odhaczania albo diagramu powiązań między tymi tematami?