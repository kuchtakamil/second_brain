# Błąd przy imporcie względnym

**Data:** 2025-04-06

---

**User:**

Kiedy w python pojawia się błąd: attempted relative import with no known parent package

---

**Assistant:**

Błąd `attempted relative import with no known parent package` w Pythonie pojawia się, gdy próbujesz użyć **relatywnego importu** (np. `from . import module`) w pliku, który **nie został uruchomiony jako część pakietu**.

### Kiedy dokładnie się to dzieje?

Typowo, gdy:
- Odpalasz skrypt **bezpośrednio**, np. `python some_module.py`
- A w tym pliku próbujesz wykonać import w formie:
  ```python
  from . import something  # względny import
  ```

Python nie wie wtedy, co jest „rodzicem” danego modułu (czyli jego pakietem), więc wyrzuca ten błąd.

---

### Jak to naprawić?

Masz kilka opcji:

#### ✅ 1. Uruchom jako pakiet (poprzez `-m`)
Jeśli masz strukturę:

```
project/
├── package/
│   ├── __init__.py
│   ├── module1.py
│   └── module2.py  # tu jest `from . import module1`
```

Zamiast:
```bash
python package/module2.py  # ❌
```

Uruchom:
```bash
python -m package.module2  # ✅
```

#### ✅ 2. Użyj absolutnego importu
Zamiast:
```python
from . import module1
```

Zrób:
```python
from package import module1
```

Ale wtedy cały projekt musi być w katalogu widocznym dla Pythona (np. dodanym do `PYTHONPATH`).

#### ✅ 3. Przemyśl strukturę, jeśli to tylko skrypt
Jeśli to tylko prosty skrypt i nie potrzebujesz pakietów, po prostu nie używaj relatywnych importów – zamień na zwykłe importy lub przekształć pliki w skrypt bez pakietów.

---

### TL;DR

- **Błąd**: używasz `from . import something` w pliku uruchamianym bezpośrednio.
- **Naprawa**: uruchamiaj przez `python -m`, albo używaj pełnych (absolutnych) importów.

Chcesz, żebym rzucił okiem na jakąś konkretną strukturę katalogów, w której ten błąd się pojawia?

---

**User:**

A co kiedy ten błąd jest wynikiem próby importowania w __init__.py ?

---

**Assistant:**

Świetne pytanie — `__init__.py` ma trochę wyjątkowe zasady, ale **błąd `attempted relative import with no known parent package` nadal może się w nim pojawić**, jeśli:

- **Uruchamiasz moduł bezpośrednio**, a nie jako część pakietu,
- Lub Twój projekt **nie jest poprawnie zorganizowany jako pakiet**, z punktu widzenia Pythona.

---

### 🔎 Przykład problemu

Struktura katalogów:

```
project/
├── mypackage/
│   ├── __init__.py  # <- tutaj: from . import module1
│   └── module1.py
└── main.py
```

W `__init__.py` masz:

```python
from . import module1
```

I odpalasz `main.py` w taki sposób:

```bash
python main.py
```

Wtedy Python widzi tylko `main.py` jako **główny moduł** i nie traktuje `mypackage` jako **pełnoprawnego pakietu**, więc `__init__.py` nie ma „znanego pakietu nadrzędnego”.

---

### ✅ Jak to poprawnie zrobić?

#### ✅ 1. Uruchom z kontekstu wyższego katalogu, jako pakiet:
Przejdź do katalogu `project/` i odpal:

```bash
python -m mypackage
```

Lub, jeśli masz `main.py` i chcesz używać `mypackage`, to:

```bash
# main.py
import mypackage  # to odpali __init__.py poprawnie
```

i uruchamiaj:

```bash
python -m main  # jeśli main.py jest w module, lub po prostu: python main.py
```

Ale ważne, żeby `mypackage` był w `PYTHONPATH` albo w tym samym katalogu co `main.py`.

---

### ✅ 2. Alternatywa: nie używaj relatywnych importów w `__init__.py`

Jeśli w `__init__.py` masz:

```python
from . import module1  # ❌
```

Zamień na:

```python
import mypackage.module1  # ✅
```

Tylko wtedy `mypackage` musi być w ścieżce (np. przez `PYTHONPATH` albo jeśli jesteś w katalogu nadrzędnym).

---

### TL;DR

- `__init__.py` też podlega zasadom pakietów — jak uruchamiasz coś "na skróty", Python może nie wiedzieć, że to pakiet.
- **Nie uruchamiaj plików zagnieżdżonych z poziomu nich samych**, tylko z wyższej perspektywy (`python -m pakiet.moduł`)
- Możesz też zmienić relatywne importy na absolutne, jeśli to pasuje do stylu Twojego projektu.

Chcesz, żebym rzucił okiem na Twój `__init__.py` albo strukturę projektu, żeby dać konkretną poradę?