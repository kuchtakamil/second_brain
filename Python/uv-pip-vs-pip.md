# Uv pip vs pip

**Data:** 2025-04-21

---

**User:**

dlaczego w poleceniach uv pip list lub uv pip show mcp obok uv trzeba używąć pip skoro uv to osobny menadżer zależności podobno lepszy niż uv

---

**Assistant:**

Świetne pytanie — faktycznie może to wyglądać trochę myląco na pierwszy rzut oka.

### TL;DR:
`uv pip list` i `uv pip show` to sposób na wywołanie *kompatybilnych z pip* poleceń przez `uv`, który *symuluje pip*, żeby zapewnić zgodność. To nie jest użycie prawdziwego `pip`, tylko jego "emulacja" w ramach `uv`.

---

### Szczegóły:

#### 1. **`uv` stara się być drop-in replacement dla `pip` i `virtualenv`**
`uv` to narzędzie, które obsługuje zarządzanie środowiskiem oraz zależnościami. Ma swój własny szybki resolver i build system (napisany w Rust), ale jednocześnie:

- **obsługuje polecenia kompatybilne z `pip`**, żeby użytkownicy mogli się łatwo przesiąść
- dlatego dodano "namespace" `uv pip`, żeby np. `uv pip install` czy `uv pip list` działały znajomo

#### 2. **`uv pip` ≠ `pip`**
Mimo że piszesz `uv pip`, to:

- *nie używasz Pythona + pip*
- tylko wywołujesz *kompatybilny interfejs pipowy zaimplementowany przez `uv`*

Tak więc:
```bash
uv pip list
```
znaczy: "wykonaj `list` tak, jakby to było `pip list`, ale z użyciem szybkiego, natywnego mechanizmu `uv`".

#### 3. **Dlaczego nie po prostu `uv list`?**
Bo `uv` na razie nie ma pełnego, własnego interfejsu CLI dla każdego polecenia pip. Niektóre komendy są tylko w `uv pip`, żeby zachować znajomy styl. W przyszłości mogą to spłaszczyć.

---

### Bonus: `uv pip` jako alias

Możesz to sobie też wyobrazić tak:

```bash
uv pip list  ≈  "uruchom 'list' w trybie zgodnym z pip-em, ale przez uv"
```

---

Jeśli chcesz zobaczyć „natywne” komendy `uv`, które nie są „pod-pipem”, to np.:

```bash
uv venv         # tworzy środowisko
uv sync         # instaluje zależności z pyproject.toml
uv pip install  # też działa — ale tylko dla kompatybilności
```

---

Chcesz, mogę pokazać ci różnice np. między `uv pip install` a `uv sync` albo rozrysować, jak wygląda ich architektura pod spodem.