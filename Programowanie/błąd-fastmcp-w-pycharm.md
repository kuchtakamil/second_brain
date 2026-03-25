# Błąd FastMCP w PyCharm

**Data:** 2025-04-21

---

**User:**

w pycharm otworzyłem folder, wywołałem uv init. 
później uv add mcp[cli]
i z prostego kodu który używa 
from mcp.server.fastmcp import FastMCP
mam bład Unresolved reference 'FastMCP' 

---

**Assistant:**

Błąd `Unresolved reference 'FastMCP'` w PyCharm oznacza, że IDE nie potrafi znaleźć tej klasy lub symbolu w zainstalowanych paczkach lub strukturze kodu. Zakładając, że paczka `mcp[cli]` została poprawnie zainstalowana przez `uv`, oto kilka kroków, które możesz przejść, by rozwiązać problem:

---

### 🔍 Krok 1: Sprawdź, czy paczka jest faktycznie zainstalowana
W terminalu w katalogu projektu uruchom:

```bash
uv pip list | grep mcp
```

Albo po prostu:
```bash
uv pip show mcp
```

To pokaże, czy paczka `mcp` jest zainstalowana i skąd ją ładuje.

---

### 🔍 Krok 2: Sprawdź strukturę paczki
Zobacz, czy w folderze `site-packages` paczki `mcp` jest rzeczywiście ścieżka:

```
mcp/server/fastmcp.py
```

Możesz to sprawdzić np.:

```bash
uv pip show mcp
```

To pokaże lokalizację paczki, np.:

```
Location: /home/user/.venv/lib/python3.11/site-packages
```

Potem możesz wejść w ten katalog i sprawdzić, czy rzeczywiście istnieje `mcp/server/fastmcp.py` i czy zawiera klasę `FastMCP`.

---

### 🔧 Krok 3: Dodaj interpreter uv do PyCharm
PyCharm domyślnie nie wie o `uv`. Musisz ustawić interpreter tak, by używał środowiska `uv`.

Możliwości:
1. `uv` bazuje na `uv venv`, które tworzy środowisko w `.venv` – jeśli tak, ustaw je jako interpreter.
2. Jeśli używasz `uv` z `sys` Pythona – stwórz plik `pyproject.toml`, wtedy `uv` zainstaluje zależności do globalnego cache i PyCharm może nie widzieć ich.

💡 Najlepiej zainicjować środowisko:

```bash
uv venv .venv
source .venv/bin/activate
uv pip install mcp[cli]
```

A potem w PyCharm:
**File > Settings > Project > Python Interpreter > Add > Existing environment** i wskaż `.venv/bin/python`.

---

### 💡 Dodatkowe podpowiedzi
- Spróbuj w PyCharm kliknąć PPM na folderze głównym projektu i zaznacz `Mark Directory as > Sources Root`.
- Czasem trzeba zrestartować PyCharm lub zrobić `Invalidate Caches / Restart`.

---

Jeśli chcesz, podeślij fragment `pyproject.toml` i struktury katalogu albo nazwę konkretnej biblioteki `mcp`, jeśli jest dostępna w PyPI – to pomoże zawęzić problem.

---

**User:**

Nie ma katalogu mcp w site-packages.
Polecenie uv pip show mcp
Name: mcp
Version: 1.6.0
Location: /home/kamil/ai/MCPServer/.venv/lib/python3.10/site-packages
więc mcp zostało zainstalowane w wirtualnym środowisku.

Nie wiem czy dobrze, ale zrobiłem teraz 
source .venv/bin/activate
uv pip install mcp[cli]
idostałem błąd
zsh: no matches found: mcp[cli]

---

**Assistant:**

Świetnie, że podałeś więcej szczegółów — wygląda na to, że jesteś blisko 💡

---

### 🔧 Co się dzieje z `zsh: no matches found: mcp[cli]`?

Ten błąd pochodzi od **Zsh**, a nie od `pip` — Zsh **interpretuje nawiasy kwadratowe jako wzorce (globbing)**. Musisz je albo:

- **Ująć w cudzysłów:**

```bash
uv pip install 'mcp[cli]'
```

albo

```bash
uv pip install "mcp[cli]"
```

To rozwiąże problem z błędem `zsh: no matches found`.

---

### 📁 Brak katalogu `mcp` w `site-packages`

To wskazuje, że:

1. albo paczka `mcp` nie zawiera faktycznego kodu (np. tylko metadane),
2. albo kod jest ukryty głębiej (np. nazwa katalogu może się różnić — np. `mcpserver`, `mcp_core`, etc.),
3. albo `mcp` nie instaluje plików Pythona tylko np. skrypt CLI.

---

### 🔍 Sprawdź, co zawiera paczka

W terminalu w `.venv`:

```bash
cd /home/kamil/ai/MCPServer/.venv/lib/python3.10/site-packages
ls -l | grep mcp
```

lub

```bash
find . -iname '*fastmcp*'
```

To pozwoli znaleźć, gdzie naprawdę znajduje się `FastMCP` — być może `mcp` to tylko alias.

---

### 🧪 Alternatywnie – sprawdź to z poziomu Pythona

Odpal interpreter:

```bash
.venv/bin/python
```

I spróbuj:

```python
import mcp
print(mcp.__file__)
```

lub

```python
from mcp.server.fastmcp import FastMCP
```

Zobacz, czy Python to ładuje — jeśli tak, to problem leży tylko w PyCharm.

---

### ⚙️ Na koniec – upewnij się, że PyCharm widzi `.venv`

1. W PyCharm:
   - **File > Settings > Project > Python Interpreter**
   - Kliknij zębatkę > Add...
   - Wybierz: **Existing environment**
   - Wskaż: `.venv/bin/python`

2. Zrestartuj PyCharm lub użyj opcji **Invalidate Caches / Restart**.

---

Jak chcesz, możesz też wrzucić:
- zawartość katalogu `site-packages/mcp*`,
- albo zawartość `pyproject.toml` z tą zależnością.

Wtedy mogę zerknąć, co dokładnie instaluje paczka `mcp[cli]` i jak powinno się do niej odwoływać.