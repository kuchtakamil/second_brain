# Zależności w pyproject.toml

**Data:** 2026-01-16

---

**User:**

from google import genai
from google.genai import types
from PIL import Image

jakie zależności w pyproject toml mam dodać?

---

**Assistant:**

Dla podanego kodu:

```python
from google import genai
from google.genai import types
from PIL import Image
```

w `pyproject.toml` musisz dodać zależności odpowiadające **Google GenAI SDK** oraz **Pillow**.

### Minimalne zależności

Zakładając, że używasz standardu PEP 621:

```toml
[project]
dependencies = [
    "google-generativeai",
    "Pillow"
]
```

To wystarczy w większości przypadków.

---

### Wyjaśnienie

- **`google-generativeai`**  
  Dostarcza pakiet `google.genai` oraz `genai.types`.  
  Jest to oficjalne SDK do pracy z modelami Gemini.

- **`Pillow`**  
  Zapewnia `PIL.Image`, czyli obsługę obrazów.

---

### Opcjonalne / dobre praktyki

Jeżeli pracujesz w środowisku produkcyjnym lub chcesz uniknąć problemów z kompatybilnością, warto **spiąć wersje**:

```toml
[project]
dependencies = [
    "google-generativeai>=0.5.0,<1.0.0",
    "Pillow>=10.0.0,<11.0.0"
]
```

(Numery wersji możesz dostosować do polityki wersjonowania w projekcie).

---

### Alternatywa: Poetry

Jeśli używasz Poetry:

```bash
poetry add google-generativeai pillow
```

---

Jeżeli korzystasz z **konkretnych funkcji** (np. streaming, multimodal input, async, proxy, itp.), daj znać — wtedy sprawdzimy, czy potrzebne są dodatkowe zależności lub flagi.

---

**User:**

dodałem ręcznie w pliku, jak to teraz zainstalować?

---

**Assistant:**

To zależy od **narzędzia, którym zarządzasz środowiskiem**. Poniżej najczęstsze scenariusze — wybierz ten, którego używasz.

---

## 1. Standardowy `pip` (PEP 621 / pyproject.toml)

Jeżeli masz **Python ≥ 3.11** i `pyproject.toml` z sekcją:

```toml
[project]
dependencies = [
    "google-generativeai",
    "Pillow"
]
```

w katalogu projektu wykonaj:

```bash
pip install .
```

To:
- odczyta `pyproject.toml`
- zainstaluje zależności
- zainstaluje projekt jako pakiet (editable **nie**)

### Editable install (odpowiednik `pip install -e .`)
```bash
pip install -e .
```

---

## 2. Poetry

Jeśli masz w `pyproject.toml` sekcję:

```toml
[tool.poetry.dependencies]
python = "^3.11"
google-generativeai = "^0.5"
pillow = "^10.0"
```

uruchom:

```bash
poetry install
```

Jeżeli nie masz jeszcze virtualenv:
```bash
poetry env use python
poetry install
```

---

## 3. PDM

Jeżeli używasz **PDM**:

```bash
pdm install
```

---

## 4. Używasz tylko `pip` + venv (najczęstszy case)

Jeżeli **nie masz backendu builda** (`build-system`) i chcesz tylko zainstalować zależności:

### Krok 1: virtualenv (jeśli jeszcze nie masz)
```bash
python -m venv .venv
source .venv/bin/activate     # Linux / macOS
.venv\Scripts\activate        # Windows
```

### Krok 2: instalacja
```bash
pip install .
```

---

## 5. Szybka diagnostyka (gdy coś nie działa)

### Sprawdź, czy pip widzi zależności
```bash
pip show google-generativeai
pip show pillow
```

### Sprawdź importy
```bash
python -c "from google import genai; from PIL import Image; print('OK')"
```

---

## Najczęstsze problemy

### ❌ `ModuleNotFoundError: No module named 'google.genai'`
- zła paczka (`google` zamiast `google-generativeai`)
- stary `pip`  
  → `pip install --upgrade pip`

### ❌ `pip install .` nic nie instaluje
- brak `[project]` lub `[tool.poetry]`
- błędna składnia TOML

---

Jeżeli chcesz, wklej **swój `pyproject.toml`** (albo jego fragment), a powiem dokładnie, którą komendę wykonać i czy plik jest poprawny.