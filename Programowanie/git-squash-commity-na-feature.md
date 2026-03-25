# Git Squash Commity na Feature

**Data:** 2024-01-04

---

**User:**

Jak zrobić git squash na gałęzi feature w sytuacji fdy na gałęzi mam swoje komity oraz komit merdżowy pochodzący z gałęzi master

---

**Assistant:**

Aby zrobić squash commitów na gałęzi `feature`, włączając własne commity oraz commit merge'owy z gałęzi `master`, wykonaj następujące kroki:

1. Przełącz się na gałąź `feature`:
   ```
   git checkout feature
   ```

2. Uruchom interaktywny rebase dla commitów, które chcesz złączyć. Załóżmy, że chcesz zesquashować ostatnie 4 commity:
   ```
   git rebase -i HEAD~4
   ```

3. W otwartym edytorze tekstowym zobaczysz listę commitów, które wybrałeś do rebase'a, wraz z poleceniami przed nimi. Zostaw pierwszy commit z poleceniem `pick` a resztę zmień na `squash` lub `s` (to złączy te commity z poprzednim commit'em z poleceniem `pick`). Powinno to wyglądać mniej więcej tak:
   ```
   pick 1234567 Twój pierwszy commit
   squash 89abcd8 Twój drugi commit
   squash efghijk Commit merge'owy
   squash lmnopqr Jakiś inny commit
   ```

4. Po zapisaniu i zamknięciu edytora, Git rozpocznie proces squashowania commitów. Jeśli wszystko pójdzie dobrze, zostaniesz poproszony o stworzenie nowego komunikatu commita dla złączonych commitów.

5. Po zakończeniu procesu, jeśli chcesz zaktualizować zdalną gałąź, użyj `git push` z flagą `--force`, ponieważ zmieniłaś historię commitów:
   ```
   git push origin feature --force
   ```

Pamiętaj, że używanie `git push --force` może być ryzykowne, zwłaszcza jeśli współpracujesz z innymi na tej samej gałęzi. Upewnij się, że wszyscy członkowie zespołu są świadomi zmian w historii commitów.