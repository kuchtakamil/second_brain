# Uruchamianie Pythona bez venv

**Data:** 2025-03-14

---

**User:**

oglądam filmy instruktażowe jak uruchamiać pliki python w vs code. Mówią żeby utworzyć virtual env a potem instalować potrzebne biblioteki. Czy mogę nie tworzyć venv tylko zainstalować paczkę termcolor globalnie i uruchomić w vs code korzystając z Run -> Start Debugging?

---

**Assistant:**

Tak, możesz jak najbardziej **nie tworzyć `venv`** i po prostu zainstalować paczkę **`termcolor`** **globalnie**, np. przez:
```bash
pip install termcolor
```
…i wtedy normalnie uruchamiać swój skrypt w **VS Code** przez `Run → Start Debugging` albo `F5`. To zadziała, **o ile VS Code używa tego samego Pythona**, do którego zainstalowałeś paczkę (czyli globalnego interpretera).

---

### Ale po co właściwie `venv`?
`venv` (wirtualne środowisko) **nie jest obowiązkowe**, ale:

- pomaga trzymać zależności oddzielnie dla każdego projektu,
- unikasz konfliktów wersji bibliotek między projektami,
- łatwiej potem komuś przekazać projekt (`requirements.txt` → `pip install -r requirements.txt`).

W projektach produkcyjnych albo zespołowych jest to **standard**.

---

### Jak sprawdzić, którego Pythona używa VS Code?
1. Kliknij w prawym dolnym rogu na **interpreter Pythona** (np. `Python 3.11.5`).
2. Zobacz, czy to ten sam Python, do którego zainstalowałeś `termcolor` (`which python` na Linux/Mac lub `where python` na Windows pokaże ścieżkę).
3. Jeśli nie — możesz wybrać interpreter ręcznie w Command Palette (`Ctrl+Shift+P` → "Python: Select Interpreter").

---

### Podsumowując:
✅ Możesz zainstalować globalnie `termcolor` i odpalać bez `venv`.  
✅ Będzie działać w VS Code.  
💡 Ale przy większych projektach warto jednak rozważyć `venv` — w dłuższej perspektywie ułatwia życie.

Chcesz, żebym pokazał Ci krok po kroku jak to zrobić z `venv` lub jak ustawić interpreter w VS Code?

---

**User:**

Okazało się że vs code używa innego pythona a inny jest zainstalowany globalnie. Ten którego używa vscode znajduje się w ~/homebrew/bin/python3
Jak zainstalować termcolor dla tej instancji python?

---

**Assistant:**

Świetnie, że to wychwyciłeś — to bardzo częsty przypadek, zwłaszcza jak masz Pythona zainstalowanego np. przez **Homebrew** na macOS/Linux.

Jeśli **VS Code używa Pythona z `~/homebrew/bin/python3`**, to musisz zainstalować `termcolor` **dla tego konkretnego Pythona**, czyli:

```bash
~/homebrew/bin/python3 -m pip install termcolor
```

To mówi wprost: „Użyj **tego konkretnego Pythona** i jego `pip` do instalacji”.

---

### Jak to sprawdzić?
Jeśli chcesz się upewnić, że instalujesz do tej samej wersji, którą widzi VS Code, możesz zrobić:
```bash
~/homebrew/bin/python3 -m pip list
```
Powinno tam potem pojawić się `termcolor`.

---

### Alternatywnie (opcjonalnie):
Możesz też zainstalować `pip` globalnie powiązane z tym Pythona, jeśli go jeszcze nie ma:
```bash
~/homebrew/bin/python3 -m ensurepip --upgrade
```

---

### Jeśli chcesz ustawić to też w terminalu jako domyślny Python:
Jeśli używasz np. `zsh` lub `bash`, możesz dodać alias:
```bash
alias python3=~/homebrew/bin/python3
alias pip3="~/homebrew/bin/python3 -m pip"
```
(np. w `.zshrc` albo `.bashrc`)

---

Daj znać, jeśli chcesz żebym Ci pokazał też jak ustawić to środowisko na stałe w VS Code albo jak utworzyć `venv` na tym konkretnym interpreterze.