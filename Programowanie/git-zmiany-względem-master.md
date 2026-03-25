# Git zmiany względem master

**Data:** 2025-03-14

---

**User:**

Chcę uruchomić polecenie git takie aby w jego rezultacie wyświetlone były pliki które zostały zmienione na bieżącej gałęzi względem gałęzi master. Lista wyświetlonych plików ma być taka sama gdy jest wyświetlana podczas przeglądania pull requestu w bitbucket.

---

**Assistant:**

Aby uzyskać listę plików zmienionych na bieżącej gałęzi względem `master`, tak jak widzisz to w **Bitbucket Pull Request (PR)**, możesz użyć polecenia:

```bash
git diff --name-status origin/master...
```

Lub, alternatywnie:

```bash
git diff --name-status origin/master...HEAD
```

### Co to robi:
- `--name-status` — pokazuje typ zmiany (`A` - added, `M` - modified, `D` - deleted) oraz ścieżkę pliku.
- `origin/master...` — porównuje **merge-base** (`common ancestor`) gałęzi `origin/master` i `HEAD`, czyli dokładnie tak, jak robi to Bitbucket przy tworzeniu PR (czyli od miejsca rozgałęzienia, a nie ostatniego commita na `master`).

Jeśli chcesz tylko same nazwy plików (bez typu zmian), możesz użyć:
```bash
git diff --name-only origin/master...
```

### Przykład wyniku:
```
M       src/com/example/MyClass.java
A       src/com/example/NewClass.java
D       src/com/example/OldClass.java
```

---

### Uwaga:
Upewnij się, że masz aktualne dane o `origin/master`:
```bash
git fetch origin
```

---

Jeśli chciałbyś coś bardziej doprecyzowanego (np. tylko zmienione pliki bez usuniętych/dodanych, albo z pełną ścieżką względną od repozytorium głównego), daj znać — dopasuję polecenie pod Twój scenariusz.

Chcesz, żeby to też obejmowało rename’y i kopie (`R`, `C`) tak jak Bitbucket?

---

**User:**

czy grybym chciał uruchomić to samo w python to czy to polecenie jest ok?|
subprocess.check_output(['git', '-C', repo_path, 'diff', '--name-status', 'master...'], encoding='utf-8')

---

**Assistant:**

Jesteś bardzo blisko — prawie dobrze, ale jest jedna mała rzecz do poprawy.

Twoje polecenie:

```python
subprocess.check_output(['git', '-C', repo_path, 'diff', '--name-status', 'master...'], encoding='utf-8')
```

działa, ale **lepiej byłoby sprecyzować**, że chodzi o `master...HEAD` lub `origin/master...HEAD`, żeby wynik był **taki sam jak w Bitbucket PR** (czyli od **common ancestor** do aktualnej gałęzi).

### ✅ Poprawiona wersja:
```python
import subprocess

output = subprocess.check_output(
    ['git', '-C', repo_path, 'diff', '--name-status', 'origin/master...HEAD'],
    encoding='utf-8'
)
print(output)
```

lub jeśli nie korzystasz z `origin`, tylko z lokalnej referencji:
```python
output = subprocess.check_output(
    ['git', '-C', repo_path, 'diff', '--name-status', 'master...HEAD'],
    encoding='utf-8'
)
```

### 🔍 Różnica między `master...` a `master..HEAD`
- `master...HEAD` (trzy kropki) → **od wspólnego przodka do HEAD** → dokładnie tak jak PR.
- `master..HEAD` (dwie kropki) → **od commitów na HEAD, które nie są na masterze**, ale niekoniecznie od wspólnego przodka.

### 📌 Jeśli zależy Ci na tym, co Bitbucket PR widzi — używaj `master...HEAD`.

---

Dodatkowo możesz sobie sparsować wynik do listy plików:
```python
changed_files = [line.split('\t')[1] for line in output.strip().split('\n') if line]
```

Chcesz, żebym zrobił Ci gotową funkcję `get_changed_files(repo_path)`?

---

**User:**

chciałbym użyć tej wersji
git diff --name-only origin/master...

---

**Assistant:**

Super, wtedy Twoje wywołanie w Pythonie będzie wyglądać tak:

```python
import subprocess

def get_changed_files(repo_path):
    output = subprocess.check_output(
        ['git', '-C', repo_path, 'diff', '--name-only', 'origin/master...'],
        encoding='utf-8'
    )
    files = output.strip().split('\n') if output else []
    return files
```

### ✅ Co robi ten kod:
- `--name-only` — zwraca tylko ścieżki plików, bez informacji o typie zmiany (czy `M`, `A`, `D` itd.).
- `origin/master...` — porównanie od wspólnego przodka `origin/master` do aktualnej gałęzi (`HEAD`).
- `.strip().split('\n')` — konwertuje wynik do listy plików.

### 📌 Uwaga: Upewnij się, że wcześniej zrobiłeś:
```bash
git fetch origin
```
albo dodaj to w Pythonie, np. jako dodatkowy krok przed `diffem`:
```python
subprocess.run(['git', '-C', repo_path, 'fetch', 'origin'])
```

### Finalna wersja z `fetch`:

```python
import subprocess

def get_changed_files(repo_path):
    subprocess.run(['git', '-C', repo_path, 'fetch', 'origin'], check=True)
    output = subprocess.check_output(
        ['git', '-C', repo_path, 'diff', '--name-only', 'origin/master...'],
        encoding='utf-8'
    )
    return output.strip().split('\n') if output else []
```

Daj znać, jeśli chcesz też zwracać tylko pliki `.java`, `.xml` itd., albo od razu pełne ścieżki z repo. Chętnie dorzucę :)

---

**User:**

co oznacza -C

---

**Assistant:**

Świetne pytanie!

Opcja `-C` w poleceniu `git` oznacza:

> **"change directory before running the git command"**

czyli po prostu: **"uruchom to polecenie w tym katalogu (repozytorium)"**.

### Przykład:
```bash
git -C /ścieżka/do/repo diff --name-only origin/master...
```

to dokładnie to samo co:
```bash
cd /ścieżka/do/repo
git diff --name-only origin/master...
```
…ale możesz to zrobić **w jednym poleceniu**, bez zmieniania aktualnego katalogu roboczego Twojego skryptu.

### Dlaczego to jest przydatne w Pythonie?
Bo możesz uruchamiać git na różnych repozytoriach bez zmieniania katalogu skryptu głównego.

---

📌 **Podsumowując:**
- `-C /some/path` → mówi `git`, żeby działał **tak jakby był uruchomiony w tym katalogu**.
- Idealne do skryptów automatyzujących różne repozytoria.

Chcesz przykład, jak przetwarzać wiele repo w pętli w Pythonie z użyciem `-C`?