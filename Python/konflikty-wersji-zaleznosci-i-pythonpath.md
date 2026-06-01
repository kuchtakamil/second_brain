# Konflikty wersji zależności w Pythonie i mechanizm `sys.path`

## Krótkie podsumowanie

W Pythonie — w odróżnieniu od Javy — **nie ma wbudowanego mechanizmu ładowania wielu wersji tej samej biblioteki jednocześnie**. Gdy dwie zależności projektu wymagają różnych wersji tej samej trzeciej biblioteki, menedżer pakietów (pip, Poetry, uv) musi rozwiązać ten konflikt i zainstalować **dokładnie jedną wersję**. Jeśli nie jest to możliwe — instalacja kończy się błędem. Ten dokument wyjaśnia, jak działa rozwiązywanie konfliktów, co finalnie ląduje na ścieżce wyszukiwania modułów (`sys.path`) oraz czym `sys.path` jest w porównaniu do javowego `CLASSPATH`.

---

## Odpowiednik javowego `CLASSPATH` w Pythonie

W Javie `CLASSPATH` to lista ścieżek, w których JVM szuka klas do załadowania. W Pythonie odpowiednikiem jest **`sys.path`** — lista katalogów, w których interpreter szuka modułów podczas instrukcji `import`.

### `sys.path` — czym jest?

```python
import sys
print(sys.path)
```

Wynik to lista katalogów, np.:

```python
[
    '',                                          # bieżący katalog
    '/usr/lib/python3.12',                       # stdlib
    '/usr/lib/python3.12/lib-dynload',           # rozszerzenia C
    '/home/user/project/.venv/lib/python3.12/site-packages',  # zainstalowane pakiety
]
```

### Skąd `sys.path` bierze swoje wartości?

| Źródło | Opis |
|--------|------|
| **Bieżący katalog** (`''`) | Zawsze dodawany jako pierwszy element |
| **Zmienna środowiskowa `PYTHONPATH`** | Dodatkowe katalogi, oddzielone dwukropkiem (Linux) lub średnikiem (Windows) |
| **Standardowa biblioteka** | Automatycznie dodawana na podstawie lokalizacji interpretera |
| **`site-packages`** | Katalog, do którego `pip` instaluje paczki — ustalany przez moduł `site` |
| **Pliki `.pth`** | Specjalne pliki tekstowe w `site-packages`, które mogą dodawać kolejne ścieżki |

### `PYTHONPATH` vs `sys.path`

`PYTHONPATH` to **zmienna środowiskowa**, która pozwala *ręcznie* dodać katalogi do `sys.path`. To jeden ze sposobów wpływania na `sys.path`, ale nie jedyny. W praktyce:

```bash
# Ustawienie PYTHONPATH
export PYTHONPATH="/home/user/my_libs:/home/user/other_libs"
python my_script.py
```

Wartości z `PYTHONPATH` trafiają do `sys.path` zaraz po bieżącym katalogu, ale **przed** standardową biblioteką i `site-packages`.

### Porównanie z Javą

| Cecha | Java (`CLASSPATH`) | Python (`sys.path`) |
|-------|-------------------|---------------------|
| **Co przechowuje** | Ścieżki do klas i plików `.jar` | Ścieżki do katalogów z modułami `.py` |
| **Zmienna środowiskowa** | `CLASSPATH` | `PYTHONPATH` (wpływa na `sys.path`) |
| **Obiekt w runtime** | `ClassLoader` | `sys.path` (lista stringów) |
| **Wiele wersji tej samej biblioteki** | Możliwe (osobne ClassLoadery) | ❌ Niemożliwe natywnie |
| **Modyfikowalny w trakcie działania** | Tak (custom ClassLoader) | Tak (`sys.path.append(...)`) |

---

## Jak Python rozwiązuje konflikty wersji zależności?

### Scenariusz problemu

Załóżmy taką sytuację:

```
Twój projekt
├── wymaga: biblioteka-A >= 1.0
└── wymaga: biblioteka-B >= 2.0

biblioteka-A
└── wymaga: requests >= 2.28, < 2.30

biblioteka-B
└── wymaga: requests >= 2.31
```

Biblioteka A wymaga `requests` w wersji `>=2.28, <2.30`, a biblioteka B wymaga `requests >= 2.31`. Te zakresy **nie mają części wspólnej** — to jest właśnie konflikt wersji.

### Co robi `pip`?

`pip` stosuje **prostą strategię** — domyślnie instaluje pakiety po kolei i **nie sprawdza globalnej spójności** aż do końca:

1. Instaluje `biblioteka-A` → instaluje `requests==2.29.0`
2. Instaluje `biblioteka-B` → **nadpisuje** `requests` na `requests==2.31.0`
3. Na końcu w `site-packages` jest **jedna wersja**: `requests==2.31.0`
4. `pip check` zgłosi ostrzeżenie o niekompatybilności

```bash
$ pip check
biblioteka-a 1.0 has requirement requests<2.30,>=2.28, but you have requests 2.31.0.
```

**Kluczowy wniosek:** `pip` może zainstalować niekompatybilne wersje bez błędu! To programista musi sprawdzić spójność (`pip check`).

> **Uwaga:** Nowsze wersje `pip` (od 2020) mają wbudowany *dependency resolver*, który **próbuje** znaleźć wspólną wersję. Jeśli nie znajdzie — zgłasza błąd `ResolutionImpossible`.

### Co robią nowocześniejsze narzędzia (Poetry, uv, PDM)?

Te narzędzia mają **pełny resolver zależności** (podobny do tego w npm lub Cargo), który:

1. Buduje **graf zależności** — zbiera wymagania wersji ze wszystkich pakietów
2. Szuka **wspólnej wersji**, która spełnia wszystkie ograniczenia jednocześnie
3. Jeśli wspólna wersja istnieje → instaluje ją
4. Jeśli wspólna wersja **nie istnieje** → **rzuca błąd** i nie instaluje niczego

```bash
# Przykładowy błąd z Poetry:
SolverProblemError

Because biblioteka-a (1.0) depends on requests (>=2.28, <2.30)
  and biblioteka-b (2.0) depends on requests (>=2.31),
  biblioteka-a (1.0) is incompatible with biblioteka-b (2.0).

So, because my-project depends on both biblioteka-a (>=1.0) and biblioteka-b (>=2.0),
  version solving failed.
```

### Reguła: dokładnie jedna wersja w `site-packages`

Niezależnie od narzędzia, w Pythonie obowiązuje **żelazna reguła**:

```
W danym środowisku (venv) może być zainstalowana
DOKŁADNIE JEDNA WERSJA każdej biblioteki.
```

W katalogu `site-packages` pojawia się jeden katalog:

```
site-packages/
├── requests/
│   ├── __init__.py     # <- to jest TA JEDNA zainstalowana wersja
│   ├── api.py
│   └── ...
├── requests-2.31.0.dist-info/
│   ├── METADATA
│   └── ...
```

Gdy robisz `import requests`, Python przeszukuje `sys.path`, trafia do `site-packages` i ładuje **tę jedną wersję**. Nie ma mechanizmu, który by pozwolił załadować `requests 2.29` dla biblioteki A i `requests 2.31` dla biblioteki B.

---

## Jak sobie z tym radzić w praktyce?

### 1. Znalezienie wspólnej wersji

Najczęściej rozwiązaniem jest **doprecyzowanie** lub **poluzowanie** ograniczeń wersji:

```toml
# pyproject.toml — wymuszenie konkretnej wersji, która pasuje obu stronom
[tool.poetry.dependencies]
requests = ">=2.28, <2.32"
```

### 2. Aktualizacja zależności

Często jedna z bibliotek ma nowszą wersję, która poluźnia wymagania:

```bash
poetry update biblioteka-a
# lub
pip install --upgrade biblioteka-a
```

### 3. Izolacja środowisk (wirtualne środowiska)

Jeśli zależności nie da się pogodzić w jednym projekcie, rozważ **podział na mikroserwisy** lub osobne środowiska:

```bash
# Środowisko 1 — dla biblioteki A
python -m venv .venv-a
source .venv-a/bin/activate
pip install biblioteka-a

# Środowisko 2 — dla biblioteki B  
python -m venv .venv-b
source .venv-b/bin/activate
pip install biblioteka-b
```

### 4. Java-style? Nie w Pythonie

W Javie można użyć osobnych `ClassLoaderów`, aby załadować dwie wersje tej samej klasy w jednym procesie (np. w OSGi, Tomcat). W Pythonie **nie ma takiego natywnego mechanizmu**. Istnieją hacki (np. ręczne manipulowanie `sys.modules` i `importlib`), ale w praktyce nikt ich nie stosuje w produkcji.

---

## Podsumowanie

| Aspekt | Python | Java |
|--------|--------|------|
| **Ścieżka wyszukiwania** | `sys.path` (lista katalogów) | `CLASSPATH` |
| **Zmienna środowiskowa** | `PYTHONPATH` | `CLASSPATH` |
| **Katalog z pakietami** | `site-packages` | `.jar` / katalogi z `.class` |
| **Wiele wersji tej samej lib** | ❌ Niemożliwe | ✅ Możliwe (ClassLoader) |
| **Rozwiązywanie konfliktów** | Resolver (pip/Poetry/uv) szuka jednej wspólnej wersji | Maven/Gradle — strategia „nearest wins" |
| **Gdy brak wspólnej wersji** | Błąd instalacji lub niespójność | Potencjalnie `NoSuchMethodError` w runtime |

## Powiązane pliki

- [Instalacja zależności w Pythonie](instalacja-zależności-w-pythonie.md)
- [Moduły i importy w Pythonie](moduły-i-importy-w-pythonie.md)
- [Import vs from import](import-vs-from-import.md)
- [Inicjalizacja projektu Python (pip, uv, poetry)](jak-przy-użyciu-pip-uv-poetry-zainicjować-nowy-projekt-python.md)
