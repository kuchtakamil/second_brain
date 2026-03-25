# Przywracanie usuniętego pliku

**Data:** 2025-01-02

---

**User:**

Kilka commitów temu skasowałem pewien plik który teraz chcę przywrócić. Jak to zrobić?

---

**Assistant:**

Aby przywrócić plik, który został usunięty w poprzednich commitach, możesz skorzystać z poniższych kroków w Git:

1. **Znajdź commit, w którym plik istniał**  
   Użyj polecenia:
   ```bash
   git log -- <ścieżka_pliku>
   ```
   Wyświetli to historię commitów, w których plik istniał. Skopiuj identyfikator (hash) odpowiedniego commita.

2. **Przywróć plik z danego commita**  
   Aby przywrócić plik do bieżącej gałęzi, użyj:
   ```bash
   git checkout <hash_commita> -- <ścieżka_pliku>
   ```
   Ten krok przywraca plik do obecnej przestrzeni roboczej, ale nie dodaje go do indeksu.

3. **Dodaj plik do commitów**  
   Po przywróceniu pliku dodaj go do indeksu:
   ```bash
   git add <ścieżka_pliku>
   ```

4. **Stwórz commit z przywróconym plikiem**  
   Utwórz nowy commit:
   ```bash
   git commit -m "Przywrócono plik <nazwa_pliku>"
   ```

### Szybsza alternatywa:
Jeśli chcesz przywrócić cały plik tak, jak wyglądał w konkretnym commicie, użyj:
```bash
git restore --source=<hash_commita> -- <ścieżka_pliku>
```

Czy chcesz, żebym wyjaśnił któryś z tych kroków bardziej szczegółowo? 😊

---

**User:**

dostaję błąd did not match any file(s) known to git

---

**Assistant:**

Błąd `did not match any file(s) known to git` oznacza, że Git nie zna pliku, ponieważ został usunięty i nie ma go w bieżącej przestrzeni roboczej. Aby rozwiązać ten problem:

1. **Upewnij się, że plik istniał w historii repozytorium**  
   Możesz sprawdzić historię commitów dla repozytorium i znaleźć, gdzie plik istniał:
   ```bash
   git log --name-only --all | grep <nazwa_pliku>
   ```
   To polecenie przeszuka historię wszystkich commitów i wyświetli te, które zawierają nazwę pliku.

2. **Znajdź hash commita, gdzie plik istniał**  
   Gdy znajdziesz odpowiedni commit, skopiuj jego hash.

3. **Przywróć plik, korzystając z pełnej ścieżki**  
   Jeśli znasz ścieżkę pliku, użyj jej w poleceniu `git checkout` lub `git restore`:
   ```bash
   git checkout <hash_commita> -- <ścieżka_pliku>
   ```

4. **Jeśli nie znasz pełnej ścieżki pliku**  
   Możesz przeszukać repozytorium, by znaleźć nazwę pliku i jego lokalizację:
   ```bash
   git log --all -- <nazwa_pliku>
   ```
   Lub spróbuj bardziej ogólnego wyszukiwania:
   ```bash
   git log --name-only --all | grep <nazwa_pliku>
   ```

5. **Sprawdź gałęzie**  
   Jeśli plik istniał w innej gałęzi, musisz uwzględnić jej historię. Dodaj opcję `--all` do `git log`.

Czy potrzebujesz pomocy w znalezieniu ścieżki lub wykonaniu tych kroków? 😊

---

**User:**

Chcę wrócić do komitu powstałego 2 dni temu. jak to zrobić?

---

**Assistant:**

Aby wrócić do commita sprzed 2 dni, możesz wykonać następujące kroki:

### 1. **Znajdź hash commita sprzed 2 dni**
Najpierw sprawdź historię commitów, aby znaleźć odpowiedni commit:
```bash
git log --since="2 days ago"
```
To wyświetli listę commitów z ostatnich dwóch dni i starszych. Skopiuj hash interesującego Cię commita.

### 2. **Przejdź do tego commita**
- Jeśli chcesz przejść do commita i pracować w trybie "odczytu" (detached HEAD), użyj:
  ```bash
  git checkout <hash_commita>
  ```

- Jeśli chcesz zresetować gałąź do tego commita (nadpisując lokalne zmiany), użyj:
  ```bash
  git reset --hard <hash_commita>
  ```

### 3. **Jeśli chcesz utworzyć nową gałąź od tego commita**
Jeśli chcesz kontynuować pracę od tego commita w nowej gałęzi:
```bash
git checkout -b nowa_galaz <hash_commita>
```

### 4. **Wracając w historii na stałe (opcjonalne)**
Jeżeli chcesz, aby obecna gałąź wskazywała na commit sprzed dwóch dni, wykonaj:
```bash
git reset --hard <hash_commita>
```
⚠️ **Ostrzeżenie**: Użycie `--hard` spowoduje utratę niezapisanych zmian w lokalnym repozytorium.

---

Jeśli potrzebujesz pomocy w przejściu przez któryś z kroków lub w razie wątpliwości, daj znać! 😊