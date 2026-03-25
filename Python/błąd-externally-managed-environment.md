# Błąd externally-managed-environment

**Data:** 2025-11-16

---

**User:**

w cursor.sh mam otwarty sheet z jupyter notebook, chcę uruchomić komórkę z !pip install...., mam wybrany .venv  i dostaję błąd
error: externally-managed-environment

---

**Assistant:**

Błąd `externally-managed-environment` oznacza, że próbujesz instalować pakiety w środowisku, które **blokuje instalacje przez pip**, zwykle dlatego, że:

- jest to **systemowe Python** (np. zainstalowany przez apt na Linuxie), **albo**
- środowisko zostało stworzone przy użyciu `python -m venv` w Pythonie 3.12+ *bez włączonego trybu opt-out*.

Od Pythona 3.12 pip domyślnie odmawia instalacji pakietów, jeśli środowisko jest oznaczone jako „externally managed”.

### ✔ Jak to naprawić  
Opcje działania:

---

## **1. Najprostsze: utworzyć nowe venv zgodne z pip**
Zamiast:  
```bash
python3 -m venv .venv
```

Utwórz:  
```bash
python3 -m venv --upgrade-deps .venv
```

albo (pewniejsze):  
```bash
python3 -m venv --without-pip .venv
pip install --upgrade pip
```

Potem aktywuj środowisko w Cursorze i użyj `!pip install ...` w notebooku.

---

## **2. Drugie wyjście: użyj `--break-system-packages`**
Jeśli musisz korzystać z obecnego środowiska:

W komórce Jupyter:
```python
!pip install --break-system-packages nazwa_pakietu
```

Ale to **obejście**, nie idealne do pracy długoterminowej.

---

## **3. Sprawdź, czy Jupyter na pewno używa twojego .venv**
Często Jupyter odpala się na innym interpreterze niż ten otwarty w środowisku.

Uruchom w komórce:
```python
import sys
print(sys.executable)
```

Jeśli nie wskazuje na `.venv/bin/python`, to kernel Jupyter jest zły.

Wtedy dodaj kernel do Jupytera:

W terminalu w .venv:
```bash
python -m ipykernel install --user --name myvenv --display-name "Python (.venv)"
```

Wybierz go potem jako kernel notebooka.

---

## Jeśli chcesz, mogę przeanalizować dokładnie:
- jak utworzyłeś `.venv`,
- jaki masz system,
- co zwraca `sys.executable`.

Dzięki temu podam 100% pewne rozwiązanie dla twojego przypadku.