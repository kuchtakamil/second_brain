# Problem z Ctrl+V w terminalu

**Data:** 2025-07-07

---

**User:**

W ubuntu gdy wciskam Ctrl + V zamiast wklejenia tekstu w schowku wkleja się również ^[200~

---

**Assistant:**

Wklejanie ciągu znaków `^[200~` zamiast zawartości schowka oznacza, że Twój terminal (lub środowisko, w którym pracujesz) interpretuje skrót `Ctrl+V` w nietypowy sposób — często jest to związane z trybem **bracketed paste mode** lub **specyfiką emulatora terminala**.

### Możliwe przyczyny i rozwiązania:

#### 1. **Bracketed Paste Mode**
Niektóre aplikacje terminalowe (np. Vim, Bash, IPython) wspierają tzw. *bracketed paste mode*, który otacza wklejany tekst sekwencjami:
- `\e[200~` (rozpoczęcie wklejania)
- `\e[201~` (zakończenie wklejania)

`\e` (escape) jest czasem pokazywane jako `^[`.

Jeśli widzisz `^[200~`, to prawdopodobnie Twój terminal **nie obsługuje tego trybu poprawnie**, albo aplikacja, z której korzystasz, **źle to interpretuje**.

##### ➤ Rozwiązanie:
Wyłącz bracketed paste mode (o ile nie jest potrzebny). W `bash` możesz spróbować:
```bash
bind 'set enable-bracketed-paste off'
```

Jeśli używasz `readline`, dodaj to do `~/.inputrc`:
```bash
set enable-bracketed-paste off
```
Potem wyloguj się i zaloguj ponownie lub zrestartuj terminal.

#### 2. **Ctrl+V jako dosłowne wprowadzenie znaku (w terminalu)**
W niektórych konfiguracjach terminala `Ctrl+V` działa jako polecenie "wstaw dosłownie" — a nie jako "wklej". To zachowanie pochodzi z `readline`.

##### ➤ Rozwiązanie:
Spróbuj użyć:
- **Shift+Insert** – klasyczne wklejanie w terminalu X11
- **Prawy klik > Wklej**
- **Ctrl+Shift+V** – standardowy skrót "wklej" w wielu emulatorach terminala (np. GNOME Terminal, Tilix)

#### 3. **Nietypowy emulator terminala lub konfiguracja**
Upewnij się, jakiego emulatora terminala używasz (np. GNOME Terminal, Terminator, xterm, tmux, screen itp.), i czy nie jest tam przypisany niestandardowy skrót do `Ctrl+V`.

##### ➤ Rozwiązanie:
- Sprawdź ustawienia skrótów klawiszowych w emulatorze terminala
- Jeśli używasz `tmux`, może być potrzebna modyfikacja `.tmux.conf`

---

### Podsumowanie
Najprawdopodobniej masz włączony tryb bracketed paste mode, a terminal go źle interpretuje lub nie obsługuje poprawnie. Możesz spróbować:

1. `bind 'set enable-bracketed-paste off'`
2. Wklejać za pomocą `Ctrl+Shift+V` lub `Shift+Insert`
3. Sprawdzić, czy masz aktywnego `tmux` lub `screen`, które mogą przechwytywać `Ctrl+V`.

Jeśli chcesz — możesz podać, w jakim terminalu pracujesz i co dokładnie robisz, to podam dokładniejsze instrukcje.

---

**User:**

chciałbym użyć bind 'set enable-bracketed-paste off' ale używam oh my zsh, czy to problem?

---

**Assistant:**

Użycie `bind 'set enable-bracketed-paste off'` dotyczy **readline**, a więc **bash**, a nie `zsh` — dlatego ten sposób **nie zadziała w `zsh`**, niezależnie od tego, czy używasz Oh My Zsh, czy nie.

### Co zamiast tego w `zsh`?

W `zsh` tryb *bracketed paste* również istnieje, ale jego obsługa jest inna — bazuje na *ZLE* (Zsh Line Editor), a nie `readline`.

#### ➤ Aby wyłączyć bracketed paste w `zsh`, możesz dodać do pliku `~/.zshrc`:

```zsh
unset zle_bracketed_paste
```

**lub**, jeśli masz Oh My Zsh, spróbuj też:

```zsh
zle -D bracketed-paste
```

Potem zrestartuj terminal **lub wykonaj**:
```zsh
source ~/.zshrc
```

---

### Co jeszcze warto wiedzieć

Oh My Zsh może mieć pluginy, które manipulują `zle` i mogą z powrotem aktywować `bracketed paste`, np. `vi-mode`, `paste`, `zsh-users/zsh-syntax-highlighting` itp.

Jeśli po wyłączeniu nadal masz problem, sprawdź, czy masz włączone któreś z tych pluginów w `~/.zshrc`:

```zsh
plugins=(... paste ...)
```

Spróbuj usunąć `paste` z listy pluginów i ponownie załaduj `zsh`.

---

Daj znać, jeśli chcesz, mogę pomóc przeanalizować Twoje `.zshrc` lub podać sposób na debugowanie tego dalej.