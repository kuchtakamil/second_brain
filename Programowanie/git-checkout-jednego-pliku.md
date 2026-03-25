# Git checkout jednego pliku

**Data:** 2026-01-30

---

**User:**

czy istnieje w git wygodne polecenie do checkoutowania jednego pliku? np. coś jak git add -i czyli interfejs w CLI

---

**Assistant:**

Krótka odpowiedź: **nie ma w Gitcie wbudowanego, „ładnego” interaktywnego CLI dokładnie na wzór `git add -i` do checkoutowania pojedynczych plików**, ale są **bardzo sensowne substytuty**, w zależności od tego *co dokładnie chcesz zrobić*.

Poniżej precyzyjnie rozbijam temat.

---

## 1. Klasyczne checkout jednego pliku (bez interakcji)

Jeśli wiesz *który plik*:

```bash
git checkout -- path/to/file
```

albo (nowszy, zalecany wariant):

```bash
git restore path/to/file
```

Z konkretnego commita / brancha:

```bash
git restore --source=HEAD~1 path/to/file
git checkout HEAD~1 -- path/to/file
```

---

## 2. Interaktywne cofanie zmian — **git restore -p** (najbliżej `git add -i`)

Jeśli chodzi Ci o **interaktywne cofanie zmian w pliku / hunki**, to to jest **najlepsza odpowiedź**:

```bash
git restore -p
```

Działa analogicznie do:

```bash
git add -p
```

Możesz:
- wybierać pliki
- wybierać hunki
- częściowo cofać zmiany

To **często rozwiązuje realny problem**, dla którego ludzie pytają o „checkout jednego pliku”.

---

## 3. Interfejs pół-interaktywny: git checkout -p (starsze gity)

W starszych wersjach:

```bash
git checkout -p
```

Działa podobnie do `restore -p`, ale:
- jest **deprecated mentalnie**
- `git restore` jest czytelniejszy semantycznie

---

## 4. Pełny TUI / interaktywny CLI (nie wbudowane)

Git **nie ma** wbudowanego TUI do checkoutowania plików jak `add -i`, ale popularne narzędzia robią to świetnie:

### 🔹 lazygit (mocno polecany)
```bash
lazygit
```

- checkout / restore plików
- staging / unstaging
- cofanie hunks
- wszystko z klawiatury

Dla kogoś z Twoim doświadczeniem → **ogromny boost produktywności**.

---

### 🔹 tig
```bash
tig status
```

- tryb tekstowy
- wybór plików / commitów
- mniej „discoverable” niż lazygit

---

## 5. git add -i + revert logic (hack)

Czasem używa się:

```bash
git add -i
# wybierasz reverse
```

Ale to:
- działa tylko na staging area
- jest bardziej obejściem niż rozwiązaniem

---

## TL;DR — co wybrać

| Cel | Najlepsze polecenie |
|----|----|
| Cofnąć cały plik | `git restore file` |
| Cofnąć zmiany interaktywnie | `git restore -p` |
| Interaktywny workflow TUI | `lazygit` |
| Checkout z commita | `git restore --source=<commit> file` |

Jeśli chcesz, mogę:
- rozpisać **konkretny workflow** (np. „mam 10 plików zmienionych, chcę cofnąć 3”)
- albo porównać `restore` vs `checkout` od strony **wewnętrznego modelu Git** (index / HEAD / working tree).