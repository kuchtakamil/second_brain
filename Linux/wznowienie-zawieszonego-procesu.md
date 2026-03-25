# Wznowienie zawieszonego procesu

**Data:** 2025-10-07

---

**User:**

przez przypadek nacisnąłem ctrl + z, jak powrócić do zawieszonego porgramu?

---

**Assistant:**

Jeśli w terminalu (np. bash, zsh) nacisnąłeś **Ctrl + Z**, to **zawiesiłeś** (ang. *suspended*) działający proces — ale go **nie zakończyłeś**.  
Można go łatwo wznowić na dwa sposoby:

---

### 🔹 1. Wznowienie w **tym samym terminalu** (na pierwszym planie)
Wpisz:
```bash
fg
```
To polecenie (*foreground*) przywróci ostatnio zawieszony proces do działania na pierwszym planie.

Jeśli masz więcej niż jeden zawieszony proces, możesz wybrać konkretny numer zadania:
```bash
fg %1
```
lub
```bash
jobs
```
aby zobaczyć listę wszystkich zawieszonych procesów i ich numery.

---

### 🔹 2. Wznowienie w tle (proces będzie działał dalej, ale nie zajmie terminala)
Wpisz:
```bash
bg
```
To polecenie (*background*) uruchomi zawieszony proces w tle.

---

### 🔹 Przykład
```bash
$ python myscript.py
^Z
[1]+  Zatrzymany          python myscript.py
$ fg
```
➡ skrypt wraca do działania.

---

Jeśli przypadkiem zamknąłeś terminal, to niestety procesu nie da się już wznowić — trzeba go uruchomić ponownie.

---

Czy chcesz, żebym wyjaśnił, jak przywrócić proces, jeśli to się stało w **Eclipse** albo innym **IDE**, a nie w terminalu?