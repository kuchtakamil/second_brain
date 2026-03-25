# Git log grep problem

**Data:** 2025-04-15

---

**User:**

chcę wykonać git log a później | grep jakaswartość ale to chyba nie działa

---

**Assistant:**

Masz rację, w niektórych przypadkach `git log | grep jakaswartość` nie zadziała tak, jak się spodziewasz — szczególnie jeśli `git log` domyślnie otwiera się w pagerze (`less`), który "blokuje" przekazywanie wyjścia dalej do `grep`.

### 🔧 Rozwiązania

#### 1. Wyłącz pagera `less`:
Dodaj flagę `--no-pager`:
```bash
git --no-pager log | grep jakaswartość
```

#### 2. Ustaw pager na `cat` tymczasowo:
```bash
GIT_PAGER=cat git log | grep jakaswartość
```

#### 3. Użyj `--pretty` do uproszczenia outputu:
Często chcesz filtrować tylko po commit message, autorze itp.:
```bash
git log --pretty=oneline | grep jakaswartość
```
lub:
```bash
git log --pretty=format:"%h %an %s" | grep jakaswartość
```

### 📝 Przykład:
```bash
git --no-pager log --pretty=format:"%h %s" | grep bugfix
```

Daj znać, co konkretnie chcesz wyszukać — message, autora, hash, plik? Mogę dopasować lepszą komendę.