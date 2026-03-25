# Skasowanie ostatniego komita

**Data:** 2025-02-27

---

**User:**

chcę skasować ostatni kommit który zrobiłem w git

---

**Assistant:**

Jeśli chcesz usunąć ostatni commit w Git, masz kilka opcji w zależności od tego, czy commit został już wypchnięty do zdalnego repozytorium.

### 1. **Jeśli commit NIE został jeszcze wypchnięty**  
Możesz po prostu zresetować go do poprzedniego stanu:

- **Zachowując zmiany w plikach jako niezatwierdzone (`unstaged`)**:  
  ```sh
  git reset --soft HEAD~1
  ```
  To usunie commit, ale pozostawi zmiany w plikach.

- **Usuwając commit i zmiany całkowicie**:  
  ```sh
  git reset --hard HEAD~1
  ```
  Uwaga! To usunie zmiany i nie będzie można ich odzyskać, chyba że użyjesz reflog.

### 2. **Jeśli commit został już wypchnięty**  
Musisz usunąć commit lokalnie i wymusić zmianę na zdalnym repozytorium:

```sh
git reset --hard HEAD~1
git push --force
```
⚠️ **Ostrzeżenie**: `git push --force` może spowodować problemy dla innych osób pracujących nad repozytorium, jeśli już pobrali ten commit.

Czy chcesz go usunąć całkowicie, czy tylko cofnąć i poprawić?