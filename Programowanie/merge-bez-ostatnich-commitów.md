# Merge bez ostatnich commitów

**Data:** 2025-02-12

---

**User:**

Git, czy da się zmerdżować branch A do branch B ale w ten sposób aby w merdżu nie uczestniczyły dwa ostatnie commity z branch A?

---

**Assistant:**

Tak, można to zrobić na kilka sposobów, zależnie od tego, jak bardzo chcesz zmodyfikować historię. Oto kilka metod:

### 1. **Cherry-pick bez dwóch ostatnich commitów**  
Jeśli chcesz zmergować branch A do B, ale bez dwóch ostatnich commitów, możesz to zrobić ręcznie poprzez `cherry-pick`:
```sh
git checkout B
git cherry-pick <commit1> <commit2> <commit3> ...
```
Gdzie `<commitX>` to identyfikatory commitów z `A`, które chcesz przenieść na `B`, pomijając dwa ostatnie.

Aby łatwo znaleźć commit, do którego chcesz się cofnąć:
```sh
git log A --oneline
```
Załóżmy, że ostatnie dwa commity mają identyfikatory `abc123` i `def456`, a chcesz przenieść wszystko sprzed `def456`. Możesz użyć:
```sh
git cherry-pick A~2
```
To przeniesie wszystko do przedostatniego commit-a.

---

### 2. **Tymczasowy branch i merge bez dwóch ostatnich commitów**  
Jeśli chcesz wykorzystać merge zamiast cherry-pick, możesz utworzyć tymczasowy branch i go zmergować:
```sh
git checkout A
git checkout -b A-temp
git reset --hard A~2  # Cofamy branch o dwa commity
git checkout B
git merge A-temp
```
To spowoduje, że branch `B` dostanie wszystkie zmiany z `A` oprócz dwóch ostatnich commitów.

---

### 3. **Merge z `--no-commit` i ręczne usunięcie ostatnich commitów**  
Jeśli chcesz wykonać merge i usunąć te commity ręcznie:
```sh
git checkout B
git merge --no-commit A
git reset HEAD~2  # Usunięcie ostatnich dwóch commitów z merge
git commit -m "Merge A into B without last 2 commits"
```
Tutaj `--no-commit` powoduje, że Git nie zapisuje zmian automatycznie, a `git reset HEAD~2` usuwa ostatnie dwa commity przed finalnym commitowaniem.

---

### Podsumowanie  
- Jeśli chcesz wybrać konkretne commity → `cherry-pick`
- Jeśli chcesz zmergować, ale bez dwóch ostatnich commitów → tymczasowy branch i `reset --hard`
- Jeśli chcesz kontrolować merge przed commitowaniem → `--no-commit` i `reset HEAD~2`

Które podejście najlepiej pasuje do Twojego przypadku? 🚀