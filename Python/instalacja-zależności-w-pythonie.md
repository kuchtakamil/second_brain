# Instalacja zależności w Pythonie

**Data:** 2025-11-24

---

**User:**

po tym jak do pyproject.toml dodan nową zależność to jaką komendę muszę uruchomić aby się ściągnęła?

---

**Assistant:**

To zależy od narzędzia, którego używasz do zarządzania projektem Python.

### **Jeśli używasz *Poetry*** (najczęstsze przy pyproject.toml)
Po dodaniu zależności ręcznie w `pyproject.toml`:
```
poetry install
```
lub żeby zaktualizować środowisko:
```
poetry update
```

### **Jeśli używasz *Pip + pyproject.toml* (bez Poetry)**
Sam `pip` **nie pobierze automatycznie zależności tylko dlatego, że pojawiły się w pyproject.toml**. Musi istnieć backend typu `hatchling`/`setuptools` itp., a instalacja wygląda wtedy tak:
```
pip install .
```
lub w trybie developerskim:
```
pip install -e .
```

### **Jeśli używasz PDM**
```
pdm install
```

Jeśli podasz, z czego korzystasz (Poetry, PDM, Hatch, pip), dopasuję dokładnie.

---

**User:**

w przypadku poetry gdy dodaję zależność i zawsze chcę żeby była latest to jak to wpisać?

---

**Assistant:**

W Poetry najprostszy sposób to **nie podawać wersji**, wtedy Poetry pobierze najnowszą dostępną:

```
poetry add numpy
```

W `pyproject.toml` zapisze się to jako coś w stylu:
```toml
numpy = "^2.1.0"
```
(czyli aktualna najnowsza wersja z automatycznym dopuszczeniem kolejnych minor/patch)

Jeśli chcesz *zawsze* brać absolutnie najnowszą możliwą wersję (nawet gdy wyjdzie major), ustaw:

### **1. Szeroki zakres:**
```toml
numpy = "*"
```
lub dodając przez komendę:
```
poetry add numpy@*
```

### **2. Lub bezpośrednio z PyPI, wymuszając brak pinowania:**
```
poetry add "numpy@latest"
```

To spowoduje, że Poetry nie zawęzi wersji i będzie instalować najświeższą przy `poetry update`.

Jeśli chcesz, mogę pokazać dokładnie jak to wygląda dla konkretnej biblioteki.

---

**User:**

chcę wpisać bezpośrednio w pliku. MOgę tak?
google-genai = latest

---

**Assistant:**

Nie, taki zapis **nie zadziała**:

```toml
google-genai = latest
```

`latest` nie jest poprawną wartością w `pyproject.toml`.

### Jak można to zrobić poprawnie?

#### **1. Najprościej – pozwolić na dowolną wersję**
```toml
google-genai = "*"
```
To oznacza: instaluj zawsze najnowszą wersję dostępną na PyPI.

#### **2. Możesz też szeroko dopuścić wersje semver, np.:**
```toml
google-genai = ">=0"
```
Efekt jest taki sam – zawsze najnowsza.

### Podsumowanie
W pliku **nie istnieje słowo kluczowe `latest`**. Jeśli chcesz najnowszą wersję, użyj `*` lub `>=0`.

Jeśli chcesz, mogę sprawdzić czy dana biblioteka ma jakieś specyficzne wymagania wersji.