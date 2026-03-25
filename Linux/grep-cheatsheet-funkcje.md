# Grep cheatsheet funkcje

**Data:** 2025-07-30

---

**User:**

Przygotuj mi cheatsheet z grep. Takie najbardziej przydatne i najczęściej używane funkcje jak --include --exclude rodzajów plików lub ścieżek, -C -A -B i inne

---

**Assistant:**

Oto **cheatsheet dla `grep`** z najczęściej używanymi i przydatnymi opcjami:

---

## 🔍 Podstawowe użycie
```bash
grep "wzorzec" plik
```
Szukaj tekstu "wzorzec" w pliku `plik`.

---

## 🧠 Często używane opcje

### 📂 Przeszukiwanie rekurencyjne
```bash
grep -r "wzorzec" katalog/
```
Rekurencyjne przeszukiwanie katalogu.

```bash
grep -r --include="*.java" "wzorzec" .
```
Tylko pliki z rozszerzeniem `.java`.

```bash
grep -r --exclude="*.log" "wzorzec" .
```
Pominięcie plików `.log`.

```bash
grep -r --include="*.{java,xml}" "wzorzec" .
```
Wiele rozszerzeń — pliki `.java` i `.xml`.

---

## 📄 Wykluczanie/uwzględnianie plików/ścieżek

```bash
grep -r --exclude-dir={.git,target,node_modules} "TODO" .
```
Pominięcie katalogów `.git`, `target`, `node_modules`.

```bash
grep -r --include="*.py" --exclude-dir="venv" "def " .
```
Szukaj tylko w `.py`, pomijając `venv`.

---

## 🔍 Dopasowania kontekstu

```bash
grep -C 3 "Exception" logfile.log
```
3 linie **przed i po** dopasowaniu.

```bash
grep -A 2 "Exception" logfile.log
```
2 linie **po** dopasowaniu.

```bash
grep -B 4 "Exception" logfile.log
```
4 linie **przed** dopasowaniem.

---

## 🧵 Inne przydatne opcje

| Opcja         | Opis                                                  |
|---------------|--------------------------------------------------------|
| `-i`          | Ignoruj wielkość liter (`case-insensitive`)           |
| `-n`          | Pokaż numery linii                                     |
| `-H`          | Zawsze pokaż nazwę pliku (przydatne przy wielu plikach) |
| `-l`          | Wypisz **tylko nazwy plików** zawierających dopasowanie |
| `-L`          | Wypisz **nazwy plików bez** dopasowania                |
| `-v`          | Odwrócenie — pokaż linie **niepasujące**              |
| `-E`          | Rozszerzone regex (np. `|`, `+`, `?`, `()` bez `\`)    |
| `-F`          | Wyszukiwanie **dosłowne**, bez interpretacji regex     |
| `-q`          | Tryb **cichy**, tylko kod wyjścia                      |
| `-c`          | Liczba dopasowań (tylko liczba, nie zawartość linii)  |
| `--color=auto`| Pokoloruj dopasowania                                  |

---

## 🧪 Przykłady praktyczne

### Szukaj tylko w plikach `.java`, ignoruj katalog `target`
```bash
grep -r --include="*.java" --exclude-dir="target" "MyService" .
```

### Znajdź wystąpienia z kontekstem w logach
```bash
grep -C 5 "ERROR" /var/log/app.log
```

### Znajdź pliki **niezawierające** frazy
```bash
grep -rL "spring.jpa" .
```

### Szukaj wielu fraz (regex z `-E`)
```bash
grep -E "WARN|ERROR|FATAL" logfile.log
```

---

Jeśli chcesz, mogę też przygotować wersję w PDF lub gotową do wrzucenia na wewnętrznego wiki.

---

**User:**

ok ale napisz to wszystko w jednym bloku textu markdown tak żebym mógł to wydrukować

---

**Assistant:**

Oczywiście — poniżej masz kompletny **`grep` cheatsheet** w jednym bloku Markdown, gotowy do wydruku lub wrzucenia do wiki:

````markdown
# 🧾 `grep` Cheatsheet

## 🔍 Podstawowe użycie

```bash
grep "wzorzec" plik
```
Szukaj tekstu "wzorzec" w pliku `plik`.

---

## 📂 Przeszukiwanie rekurencyjne

```bash
grep -r "wzorzec" katalog/
```
Rekurencyjne przeszukiwanie katalogu.

```bash
grep -r --include="*.java" "wzorzec" .
```
Tylko pliki z rozszerzeniem `.java`.

```bash
grep -r --exclude="*.log" "wzorzec" .
```
Pominięcie plików `.log`.

```bash
grep -r --include="*.{java,xml}" "wzorzec" .
```
Wiele rozszerzeń — pliki `.java` i `.xml`.

---

## 📄 Wykluczanie/uwzględnianie plików/ścieżek

```bash
grep -r --exclude-dir={.git,target,node_modules} "TODO" .
```
Pominięcie katalogów `.git`, `target`, `node_modules`.

```bash
grep -r --include="*.py" --exclude-dir="venv" "def " .
```
Szukaj tylko w `.py`, pomijając `venv`.

---

## 🔍 Dopasowania kontekstu

```bash
grep -C 3 "Exception" logfile.log
```
3 linie **przed i po** dopasowaniu.

```bash
grep -A 2 "Exception" logfile.log
```
2 linie **po** dopasowaniu.

```bash
grep -B 4 "Exception" logfile.log
```
4 linie **przed** dopasowaniem.

---

## 🧵 Inne przydatne opcje

| Opcja         | Opis                                                  |
|---------------|--------------------------------------------------------|
| `-i`          | Ignoruj wielkość liter (`case-insensitive`)           |
| `-n`          | Pokaż numery linii                                     |
| `-H`          | Zawsze pokaż nazwę pliku                               |
| `-l`          | Tylko nazwy plików zawierających dopasowanie          |
| `-L`          | Tylko pliki **bez** dopasowania                        |
| `-v`          | Odwrócenie — pokaż linie **niepasujące**              |
| `-E`          | Rozszerzone regex (np. `|`, `+`, `?`, `()` bez `\`)    |
| `-F`          | Dosłowne wyszukiwanie (bez regex)                      |
| `-q`          | Tryb **cichy**, tylko kod wyjścia                      |
| `-c`          | Liczba dopasowań                                       |
| `--color=auto`| Pokoloruj dopasowania                                  |

---

## 🧪 Przykłady praktyczne

### Szukaj tylko w plikach `.java`, ignoruj katalog `target`

```bash
grep -r --include="*.java" --exclude-dir="target" "MyService" .
```

### Znajdź wystąpienia z kontekstem w logach

```bash
grep -C 5 "ERROR" /var/log/app.log
```

### Znajdź pliki **niezawierające** frazy

```bash
grep -rL "spring.jpa" .
```

### Szukaj wielu fraz (regex z `-E`)

```bash
grep -E "WARN|ERROR|FATAL" logfile.log
```

---

## 🧰 Wskazówki

- Używaj `--color=auto` aby łatwo dostrzegać dopasowania.
- `-F` działa szybciej, gdy nie potrzebujesz regexów.
- `-l` i `-L` są przydatne do szybkiej identyfikacji plików z (lub bez) dopasowań.

````

Jeśli chcesz, mogę też wygenerować z tego PDF lub plik `.md`.

---

**User:**

wygeneruj prosze pdf

---

**Assistant:**

Gotowe — oto Twój cheatsheet `grep` w formacie PDF (bez znaków specjalnych i polskich liter, by uniknąć błędów kodowania):

📄 [Pobierz grep_cheatsheet_ascii.pdf](sandbox:/mnt/data/grep_cheatsheet_ascii.pdf)