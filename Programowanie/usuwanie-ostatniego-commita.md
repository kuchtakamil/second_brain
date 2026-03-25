# Usuwanie ostatniego commita

**Data:** 2025-02-12

---

**User:**

jak usunąć ostatni commit w git

---

**Assistant:**

To usunięcie ostatniego commita w Git można zrobić na kilka sposobów, w zależności od tego, czy commit został już wypchnięty do zdalnego repozytorium, oraz czy chcesz zachować zmiany w plikach.

---

### 1. **Jeśli commit nie został jeszcze wypchnięty:**
#### a) Usunięcie commita, ale zachowanie zmian w plikach:
```sh
git reset --soft HEAD~1
```
- Usuwa commit, ale zachowuje zmiany w staging area.
- Możesz ponownie zrobić commit lub zmodyfikować zmiany.

#### b) Usunięcie commita i unstaging zmian:
```sh
git reset --mixed HEAD~1
```
- Commit zostanie usunięty, ale pliki pozostaną w katalogu roboczym, jakby nigdy nie były dodane do commita.

#### c) Usunięcie commita i całkowite usunięcie zmian:
```sh
git reset --hard HEAD~1
```
- Commit zostanie usunięty i wszystkie zmiany zostaną utracone.

---

### 2. **Jeśli commit został już wypchnięty do zdalnego repozytorium:**
#### a) Usunięcie commita lokalnie i nadpisanie historii w zdalnym repo:
```sh
git reset --hard HEAD~1
git push --force
```
- **Uwaga:** To nadpisze historię repozytorium i może spowodować problemy dla innych programistów.
- Używaj ostrożnie, szczególnie w zespołach.

#### b) Jeśli commit został już wypchnięty, ale chcesz go cofnąć elegancko:
```sh
git revert HEAD
git push
```
- Tworzy nowy commit cofający zmiany z ostatniego commita.
- Jest bezpieczniejszy niż `reset --hard`, szczególnie w zespołach.

Która opcja ci pasuje? 😊