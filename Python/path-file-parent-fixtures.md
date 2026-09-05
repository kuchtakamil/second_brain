---
tags: [claude-code]
date: 2026-06-05
---

# `Path(__file__).parent` — katalog skryptu i odporne ścieżki

Linijka z testu:

```python
from pathlib import Path

_FIXTURES = Path(__file__).parent / "fixtures"
```

tworzy stałą wskazującą na katalog `fixtures/` leżący **obok pliku testowego** — niezależnie od tego, z którego katalogu uruchomisz `pytest`. To jeden z najczęstszych idiomów w testach i skryptach.

---

## Rozbiór linijki

| Fragment | Co to jest | Wynik (przykład) |
|---|---|---|
| `__file__` | string ze ścieżką do **bieżącego pliku `.py`** | `/home/kamil/proj/tests/test_api.py` |
| `Path(__file__)` | opakowanie tego stringa w obiekt `Path` | `Path('/home/kamil/proj/tests/test_api.py')` |
| `.parent` | **katalog**, w którym ten plik leży (usuwa nazwę pliku) | `Path('/home/kamil/proj/tests')` |
| `/ "fixtures"` | operator `/` na `Path` = łączenie ścieżek (zamiast `os.path.join`) | `Path('/home/kamil/proj/tests/fixtures')` |

Czytaj to jako: „katalog tego pliku, a w nim podkatalog `fixtures`".

---

## Po co to — problem, który rozwiązuje

Ścieżki **względne** (`"fixtures/dane.json"`, `open("config.yaml")`) są liczone od **bieżącego katalogu roboczego** (CWD), a nie od miejsca, gdzie leży skrypt. CWD zależy od tego, **skąd** uruchomisz program:

```text
proj/
├── tests/
│   ├── test_api.py
│   └── fixtures/
│       └── sample.json
```

```python
# ŹLE — działa tylko gdy CWD == katalog testu
path = "fixtures/sample.json"

# pytest z /proj        -> szuka /proj/fixtures/sample.json        ❌
# pytest z /proj/tests  -> szuka /proj/tests/fixtures/sample.json  ✅
# z IDE / CI / crona     -> losowo ❌
```

```python
# DOBRZE — zawsze względem pliku, niezależnie od CWD
_FIXTURES = Path(__file__).parent / "fixtures"
path = _FIXTURES / "sample.json"   # zawsze /proj/tests/fixtures/sample.json ✅
```

`__file__` jest „przyklejony" do pliku, więc ścieżka jest **stabilna**: ten sam wynik z terminala, z IDE, z `cron`, z CI, z innego katalogu.

---

## `.parent` i wchodzenie w górę drzewa

`.parent` to jeden poziom w górę. Da się je łączyć albo użyć `.parents[n]`:

```python
here = Path(__file__)                 # .../proj/tests/test_api.py

here.parent                           # .../proj/tests        (katalog pliku)
here.parent.parent                    # .../proj              (root projektu)
here.parents[0]                       # .../proj/tests        (= .parent)
here.parents[1]                       # .../proj
here.parents[2]                       # .../  (jeszcze wyżej)
```

Typowy „namierz root projektu i zbuduj ścieżki względem niego":

```python
PROJECT_ROOT = Path(__file__).resolve().parents[1]   # dwa poziomy w górę
DATA_DIR     = PROJECT_ROOT / "data"
CONFIG       = PROJECT_ROOT / "config" / "settings.yaml"
```

---

## Operator `/` zamiast `os.path.join`

Na obiektach `Path` operator `/` skleja segmenty, niezależnie od systemu (na Windows da `\`, na Linux `/`):

```python
base = Path("/home/kamil/proj")

base / "data" / "out.json"        # Path('/home/kamil/proj/data/out.json')

# stary styl — to samo, brzydziej:
import os
os.path.join("/home/kamil/proj", "data", "out.json")
```

Pierwszy argument musi być `Path` (nie string), żeby `/` zadziałał jako łączenie ścieżek. Dlatego `Path(__file__).parent / "x"`, a nie `__file__ / "x"`.

---

## Częste zastosowania (gdzie to spotkasz)

```python
# 1. Fixtures / dane testowe obok testu
_FIXTURES = Path(__file__).parent / "fixtures"
data = (_FIXTURES / "sample.json").read_text()

# 2. Plik danych dostarczany razem z modułem (szablon, słownik, CSV)
TEMPLATE = Path(__file__).parent / "templates" / "email.html"

# 3. Wczytanie pliku tekstowego leżącego obok skryptu
words = (Path(__file__).parent / "stopwords.txt").read_text().splitlines()

# 4. Domyślny config względem pakietu, nie CWD
DEFAULT_CONFIG = Path(__file__).parent / "config.yaml"

# 5. Katalog na wyniki w roocie projektu (z utworzeniem, jeśli brak)
OUT = Path(__file__).resolve().parents[1] / "output"
OUT.mkdir(parents=True, exist_ok=True)
(OUT / "result.json").write_text(payload)

# 6. .env tuż obok punktu wejścia aplikacji
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / ".env")
```

---

## Pułapki i dobre praktyki

- **`.resolve()` dla pewności.** `__file__` bywa **względny** (zależnie od sposobu uruchomienia). `Path(__file__).resolve()` zamienia go na ścieżkę absolutną i upraszcza `..`/symlinki. W praktyce: `Path(__file__).resolve().parent`.

- **`__file__` nie istnieje wszędzie.** W interaktywnym REPL-u oraz w niektórych „zamrożonych" buildach (PyInstaller) `__file__` może nie być zdefiniowany albo wskazywać gdzie indziej. W zwykłych plikach `.py` jest zawsze.

- **Dla danych spakowanych w bibliotekę** (instalowanych przez `pip`, ewentualnie z ZIP/wheel) bardziej poprawne niż `Path(__file__).parent` jest `importlib.resources`:

  ```python
  from importlib.resources import files
  cfg = files("mojpakiet").joinpath("config.yaml").read_text()
  ```

  `Path(__file__).parent` zakłada, że pliki leżą na zwykłym dysku obok modułu — dla projektów/skryptów/testów to w zupełności wystarcza i jest najczytelniejsze.

- **Stała na górze modułu, nie liczenie w kółko.** Policz raz (`_FIXTURES = ...`) i używaj — czytelniej i taniej.

---

## TL;DR

| Chcesz... | Użyj |
|---|---|
| katalog tego pliku | `Path(__file__).parent` |
| katalog pliku, na pewno absolutny | `Path(__file__).resolve().parent` |
| root projektu N poziomów wyżej | `Path(__file__).resolve().parents[N]` |
| podpiąć podkatalog/plik | `... / "podkatalog" / "plik.ext"` |
| dane spakowane w pip-pakiet | `importlib.resources.files("pkg")` |

Sedno: **`Path(__file__).parent` przyczepia ścieżkę do pliku zamiast do katalogu roboczego** — dzięki temu testy i skrypty działają tak samo, skądkolwiek je odpalisz.

---

Powiązane: [[zamiana-placeholdera-w-pythonie]] · [[patch-i-pytest-mark-asyncio-w-testach]] · [[moduły-i-importy-w-pythonie]] · [[load-env-variables-in-python]]