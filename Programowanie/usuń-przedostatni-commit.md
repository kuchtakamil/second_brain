# Usuń przedostatni commit

**Data:** 2025-08-21

---

**User:**

Jak w got usunąć przedostatni commit

---

**Assistant:**

W **Git** możesz usunąć przedostatni commit na kilka sposobów – zależnie od tego, czy commit został już wypchnięty na zdalne repozytorium, czy tylko istnieje lokalnie.  

### 1. Jeśli commit jest tylko lokalnie  
Możesz użyć interaktywnego rebase:  
```bash
git rebase -i HEAD~2
```

- Otworzy się lista dwóch ostatnich commitów (ostatni i przedostatni).  
- Zmień `pick` przy przedostatnim commicie na `drop` (lub po prostu usuń tę linię).  
- Zapisz i zamknij edytor.  

Git zreorganizuje historię, usuwając ten commit.  

---

### 2. Jeśli commit jest już wypchnięty (np. na `origin/main`)  
- Nadal możesz użyć `git rebase -i HEAD~2`, ale po tym musisz wymusić wypchnięcie zmian:  
  ```bash
  git push origin +branch_name
  ```
- **Uwaga**: to nadpisuje historię w repozytorium zdalnym. Jeżeli ktoś inny pracuje na tej gałęzi, może to spowodować konflikty.  

---

### 3. Alternatywa – odwrócenie zmian bez usuwania commita  
Jeśli nie chcesz przepisywać historii, a jedynie „cofnąć” efekty przedostatniego commita, możesz użyć:  
```bash
git revert <commit_hash>
```
To doda nowy commit odwracający zmiany.  

---

Chcesz, żebym podał Ci przykład dokładnej sekwencji komend dla **konkretnej sytuacji** – np. gdy commit jest już na `origin/main`, czy gdy masz go tylko lokalnie?