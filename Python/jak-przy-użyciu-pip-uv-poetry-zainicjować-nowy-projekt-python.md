# Jak przy użyciu pip, uv, poetry zainicjować nowy projekt python?

**Data:** 17 gru 2025, 22:09:11 CET

---

**User:**

Jak przy użyciu pip, uv, poetry zainicjować nowy projekt python?

---

**Gemini:**

Poniżej znajduje się szczegółowe zestawienie inicjalizacji projektu dla trzech różnych podejść: natywnego (`pip` + `venv`), nowoczesnego i wydajnego (`uv`) oraz nastawionego na kompleksowe zarządzanie cyklem życia aplikacji (`poetry`).

---

## 1. Podejście natywne: `pip` + `venv`

`pip` sam w sobie jest menedżerem pakietów, a nie menedżerem projektów. Nie posiada komendy `init` tworzącej strukturę katalogów. Inicjalizacja projektu w tym ekosystemie jest procesem manualnym ("manual bootstrapping").

To podejście daje pełną kontrolę, ale nie oferuje mechanizmu *dependency locking* (chyba że użyjesz `pip-tools`) ani zarządzania metadanymi projektu (chyba że ręcznie utworzysz `pyproject.toml`).

### Proces inicjalizacji

1. **Utworzenie struktury katalogów:**
   Tworzysz katalog i wchodzisz do niego.

   ```
   mkdir my-project
   cd my-project
   ```
2. **Inicjalizacja środowiska wirtualnego (PEP 405):**
   Zaleca się tworzenie venv wewnątrz katalogu projektu (zazwyczaj jako `.venv`).

   ```
   python3 -m venv .venv
   ```
3. **Aktywacja środowiska:**

   - Linux/macOS:

     ```
     source .venv/bin/activate
     ```
   - Windows (PowerShell):

     ```
     .venv\Scripts\Activate.ps1
     ```
4. **Instalacja pakietów i zamrożenie stanu:**
   Po zainstalowaniu pakietów musisz ręcznie wygenerować plik `requirements.txt`.

   ```
   pip install numpy pandas
   pip freeze > requirements.txt
   ```

**Charakterystyka techniczna:**

- **Plik konfiguracyjny:** Brak domyślnego (opcjonalnie ręczny `pyproject.toml` lub `setup.py`).
- **Resolution Strategy:** `pip` posiada resolver, ale brak pliku *lock* oznacza, że `requirements.txt` bez przypiętych sum kontrolnych (hashes) nie gwarantuje w 100% powtarzalnych buildów.

---

## 2. Podejście nowoczesne (High-Performance): `uv`

`uv` to napisany w Rust, niezwykle szybki następca `pip` i `pip-tools`. Od nowszych wersji `uv` działa jako kompleksowy menedżer projektów (podobnie jak Cargo w Rust), obsługując zarządzanie wersjami Pythona, środowiskami wirtualnymi i zależnościami w jednym.

Jest zgodny ze standardami PEP 517, PEP 518 oraz PEP 621 (metadane w `pyproject.toml`).

### Proces inicjalizacji

`uv` posiada dedykowaną komendę `init`, która tworzy scaffold projektu.

1. **Inicjalizacja projektu:**

   ```
   # Initializes a new project in the current directory or creates a new one
   uv init my-project
   cd my-project
   ```

   Stworzy to plik `pyproject.toml`, `.python-version` oraz prosty plik `hello.py`.
2. **Dodawanie zależności:**
   `uv` automatycznie tworzy środowisko wirtualne (jeśli nie istnieje), aktualizuje `pyproject.toml` i generuje plik blokady `uv.lock`.

   ```
   uv add fastapi uvicorn
   ```
3. **Uruchamianie:**
   Nie musisz ręcznie aktywować venv. `uv run` wykonuje komendę w kontekście venv projektu.

   ```
   uv run hello.py
   ```

**Charakterystyka techniczna:**

- **Szybkość:** Wykorzystuje globalny cache i linkowanie plików (reflinks) na systemach plików obsługujących CoW (Copy-on-Write), co sprawia, że tworzenie venv jest niemal natychmiastowe.
- **Lockfile:** `uv.lock` (uniwersalny, cross-platform).
- **Python Management:** `uv` potrafi sam pobrać i zainstalować wymaganą wersję Pythona (np. `uv python install 3.12`).

---

## 3. Podejście deklaratywne: `poetry`

`poetry` to dojrzałe narzędzie, które kładzie ogromny nacisk na deterministyczne zarządzanie zależnościami i pakietowanie (packaging). Jest idealne, jeśli planujesz publikować bibliotekę na PyPI lub potrzebujesz rygorystycznego *dependency resolution*.

### Proces inicjalizacji

1. **Utworzenie nowego projektu (Scaffold):**
   Tworzy pełną strukturę katalogów (z testami, README, itp.).

   ```
   poetry new my-project
   cd my-project
   ```

   *Alternatywa:* Jeśli masz już katalog, użyj `poetry init`, co uruchomi interaktywny kreator konfiguracji `pyproject.toml`.
2. **Dodawanie zależności:**
   Po dodaniu biblioteki Poetry rozwiązuje graf zależności i zapisuje dokładne wersje w `poetry.lock`.

   ```
   poetry add django
   ```
3. **Zarządzanie środowiskiem:**
   Poetry zarządza venvami automatycznie (domyślnie w katalogu cache systemu, ale można to zmienić na in-project).

   ```
   # Spawns a shell within the virtual environment
   poetry shell

   # Or run a command directly
   poetry run python main.py
   ```

**Charakterystyka techniczna:**

- **Resolver:** Bardzo dokładny, ale bywa wolniejszy niż `uv` przy skomplikowanych grafach zależności.
- **Build System:** Działa jako backend budowania (build backend), co oznacza, że sam `poetry` jest używany do budowania plików `.whl` i `.tar.gz`.

---

## Porównanie techniczne (Summary)

| Cecha | `pip` (+ venv) | `uv` | `poetry` |
| --- | --- | --- | --- |
| **Typ** | Package Installer | Project & Package Manager | Dependency & Package Manager |
| **Plik konfiguracyjny** | Brak (standardowo) | `pyproject.toml` (PEP 621) | `pyproject.toml` (własna sekcja + PEP 621) |
| **Lockfile** | Brak (tylko `requirements.txt`) | `uv.lock` | `poetry.lock` |
| **Venv Management** | Manualne | Automatyczne | Automatyczne |
| **Dependency Resolution** | Podstawowe | Zaawansowane (bardzo szybkie) | Zaawansowane (dokładne) |
| **Język implementacji** | Python | Rust | Python |
| **Zastosowanie** | Proste skrypty, serwery legacy | Nowoczesne projekty, CI/CD, monorepo | Biblioteki, złożone aplikacje |

### Rekomendacja

Dla nowych projektów w 2025 roku standardem staje się **`uv`** ze względu na wydajność i zgodność ze standardami, wypierając powoli `poetry` w projektach aplikacyjnych, podczas gdy `poetry` wciąż pozostaje silnym graczem w ekosystemie tworzenia bibliotek (packaging).

Chcesz, abym przygotował przykładowy plik konfiguracyjny `pyproject.toml` zoptymalizowany pod konkretne narzędzie (uv lub poetry) dla projektu webowego?