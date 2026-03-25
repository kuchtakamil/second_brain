# Git Tag wyjaśnienie

**Data:** 2025-01-14

---

**User:**

Co to jest Git Tag?

---

**Assistant:**

Git Tag to mechanizm w systemie kontroli wersji Git, który pozwala oznaczać konkretne punkty w historii projektu jako ważne. Tag jest często używany do oznaczania wydań oprogramowania (np. wersji `v1.0.0`, `v2.1.3`), dzięki czemu można łatwo odnaleźć kod, który odpowiada danej wersji.

### Rodzaje tagów
1. **Tagi lekkie (lightweight tags)**  
   - Są jak wskaźnik na określony commit.  
   - Nie zawierają dodatkowych metadanych, takich jak autor, data ani wiadomość.
   - Tworzy się je w prosty sposób:
     ```bash
     git tag nazwa-tagu
     ```

2. **Tagi z adnotacją (annotated tags)**  
   - Zawierają metadane, takie jak autor, data, wiadomość czy podpis kryptograficzny.  
   - Są bardziej trwałe i preferowane, gdy tag ma pełnić rolę trwałego oznaczenia.  
   - Tworzy się je poleceniem:
     ```bash
     git tag -a nazwa-tagu -m "Opis tagu"
     ```

### Przykłady użycia
1. **Tworzenie tagu:**
   ```bash
   git tag -a v1.0.0 -m "Pierwsze wydanie projektu"
   ```

2. **Przeglądanie istniejących tagów:**
   ```bash
   git tag
   ```

3. **Pobieranie informacji o konkretnym tagu:**
   ```bash
   git show v1.0.0
   ```

4. **Wysyłanie tagów na zdalne repozytorium:**
   - Wysyłanie konkretnego tagu:
     ```bash
     git push origin v1.0.0
     ```
   - Wysyłanie wszystkich tagów:
     ```bash
     git push origin --tags
     ```

5. **Usuwanie tagu:**
   - Lokalnie:
     ```bash
     git tag -d nazwa-tagu
     ```
   - Ze zdalnego repozytorium:
     ```bash
     git push origin --delete tag nazwa-tagu
     ```

### Zalety korzystania z tagów
- Ułatwiają wersjonowanie i zarządzanie wydaniami.
- Pomagają w szybkim powrocie do określonych punktów w historii projektu.
- Są niezależne od branchy, dzięki czemu zawsze wskazują na ten sam commit.