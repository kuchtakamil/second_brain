# Porównanie stylów Pythona

**Data:** 2025-12-21

---

**User:**

w python pisać tak
file_path_1: Union[str, Path]
czy tak
file_path_1: str | Path

---

**Assistant:**

Obie formy są poprawne, ale **nie są równoważne pod względem wersji Pythona i stylu**.

### 1. `file_path_1: Union[str, Path]`
- Poprawne od **Python 3.5+**
- Wymaga importu:
  ```python
  from typing import Union
  from pathlib import Path
  ```
- Styl „klasyczny”, nadal spotykany w bibliotekach wspierających starsze wersje Pythona
- Bardziej gadatliwe

### 2. `file_path_1: str | Path`
- Poprawne od **Python 3.10+** (PEP 604)
- Nie wymaga `typing.Union`
- Czytelniejsze i krótsze
- **Rekomendowane w nowym kodzie**, jeśli nie musisz wspierać < 3.10

### Rekomendacja praktyczna
- **Nowy projekt, Python ≥ 3.10** → używaj:
  ```python
  file_path_1: str | Path
  ```
- **Biblioteka / legacy / wsparcie starszych wersji** → użyj:
  ```python
  file_path_1: Union[str, Path]
  ```

### Dodatkowa uwaga (istotna projektowo)
Jeśli i tak wewnętrznie normalizujesz ścieżki, często lepsze jest:
```python
def foo(file_path: Path):
    ...
```
a na wejściu:
```python
file_path = Path(file_path)
```
To upraszcza API i eliminuje propagację `Union` w dalszym kodzie.

Jeżeli chcesz, mogę podać rekomendacje zgodne z mypy / pyright albo styl „library vs application”.