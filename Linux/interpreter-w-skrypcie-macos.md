# Interpreter w skrypcie macOS

**Data:** 2025-06-09

---

**User:**

Na macOS próbuję napisać skrypt. Jaki interpreter powinien nam wskazać w pierwszej linijce?

---

**Assistant:**

Na macOS, w pierwszej linijce skryptu (tzw. *shebang*), interpreter powinien być wskazany w zależności od języka, w jakim piszesz skrypt. Oto najczęstsze przykłady:

### 1. **Bash** (domyślny shell w starszych wersjach macOS):
```bash
#!/bin/bash
```

### 2. **Zsh** (domyślny shell od macOS Catalina):
```bash
#!/bin/zsh
```

### 3. **Uniwersalny sposób — `env`** (zalecane dla przenośnych skryptów):
```bash
#!/usr/bin/env bash
```
Lub:
```bash
#!/usr/bin/env zsh
```

Ten sposób jest bardziej przenośny, ponieważ `env` znajduje interpreter w aktualnym `PATH`, więc nie polega na twardo zakodowanej ścieżce.

### 4. **Python (jeśli piszesz w Pythonie)**:
```bash
#!/usr/bin/env python3
```

### 5. **Node.js**:
```bash
#!/usr/bin/env node
```

---

Daj znać, w jakim języku piszesz, to podpowiem dokładnie.