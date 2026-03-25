# Moduły i importy w Pythonie

**Data:** 2025-06-22

---

**User:**

Załóżmy że w projekcie w Python 3 tworze swój moduł. Później chcę tego modułu używać w tym samym projekcie. Wygeneruj przykładowy kod który ilustruje poruszane tematy.
Wyjaśnij użycie __init__.py
Utwórz przykładową hierarchie pakietów, modułów i plików z wykorzystaniem __init__.py
Wyjaśnij występowanie błędu attempted relative import with no know parent package  i co trzeba zrobić żeby nie występował.

---

**Assistant:**

Świetne pytanie — poniżej znajdziesz kompletną odpowiedź wraz z przykładem kodu, strukturą katalogów oraz wyjaśnieniem najczęstszych problemów z importami w Pythonie.

---

## 🧱 Założenia

Tworzysz projekt w Pythonie 3 i chcesz:
- stworzyć **własny moduł**
- korzystać z niego w innym pliku w tym samym projekcie
- zrozumieć rolę `__init__.py`
- zrozumieć i unikać błędu `attempted relative import with no known parent package`

---

## 📁 Przykładowa struktura katalogów

```
my_project/
│
├── main.py
│
└── mypackage/
    ├── __init__.py
    ├── utils.py
    └── submodule/
        ├── __init__.py
        └── helper.py
```

---

## 📄 Zawartość plików

### `mypackage/utils.py`

```python
def greet(name):
    return f"Hello, {name}!"
```

---

### `mypackage/submodule/helper.py`

```python
# Import względny z folderu nadrzędnego
from ..utils import greet

def greet_loud(name):
    return greet(name).upper()
```

---

### `mypackage/__init__.py`

```python
# Plik może być pusty, ale może też eksponować funkcje lub pakiety
from .utils import greet
```

---

### `mypackage/submodule/__init__.py`

```python
# Może być pusty lub importować helpery
from .helper import greet_loud
```

---

### `main.py`

```python
from mypackage import greet
from mypackage.submodule import greet_loud

print(greet("Kuba"))         # Hello, Kuba!
print(greet_loud("Kuba"))    # HELLO, KUBA!
```

---

## 📦 Rola `__init__.py`

Plik `__init__.py`:
- czyni katalog pakietem (od Pythona 3.3 nie jest to wymagane, ale **zalecane**)
- pozwala kontrolować, **co jest dostępne z poziomu pakietu**
- może zawierać inicjalizację (np. ustawienia logowania, aliasy itp.)

Przykład:
```python
from .utils import greet  # dzięki temu `from mypackage import greet` działa
```

---

## ❌ Błąd: `attempted relative import with no known parent package`

### 📌 Problem

Ten błąd występuje, gdy uruchamiasz moduł **bez kontekstu pakietu**, np.:

```bash
python mypackage/submodule/helper.py
```

A w `helper.py` masz:
```python
from ..utils import greet
```

Python **nie wie**, że `mypackage` to pakiet, bo uruchamiasz plik bezpośrednio.

---

### ✅ Rozwiązania

#### 1. Uruchamiaj **z poziomu katalogu głównego**:

```bash
cd my_project
python main.py
```

Dzięki temu `mypackage` jest traktowany jako pakiet.

---

#### 2. Lub użyj `-m`, np.:

```bash
python -m mypackage.submodule.helper
```

Ale wtedy `helper.py` musi mieć np.:

```python
if __name__ == "__main__":
    print(greet_loud("Test"))
```

---

#### 3. Unikaj uruchamiania **modułów zawierających importy względne** bezpośrednio.

Jeśli musisz testować je samodzielnie, to lepiej:
- twórz skrypty testowe w katalogu `tests/`
- lub pisz testy w `unittest` / `pytest`

---

## ✍️ Podsumowanie

| Element | Rola |
|--------|------|
| `__init__.py` | definiuje pakiet, umożliwia eksport funkcji |
| `from ..utils import greet` | import względny |
| `attempted relative import with no known parent package` | wynika z uruchamiania pliku bez kontekstu pakietu |
| `python -m` | sposób na poprawne uruchamianie z kontekstem pakietu |

Chcesz, żebym przygotował też wersję z testami jednostkowymi?