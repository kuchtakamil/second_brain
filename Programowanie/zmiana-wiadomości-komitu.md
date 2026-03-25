# Zmiana wiadomości komitu

**Data:** 2024-11-04

---

**User:**

Jak zmodyfikować przed ostatnią wiadomość w komicie GIT.

---

**Assistant:**

Aby zmodyfikować przedostatnią wiadomość w komicie w GIT, musisz wykonać poniższe kroki:

1. Użyj polecenia `git rebase -i HEAD~2`:
   ```bash
   git rebase -i HEAD~2
   ```

2. W edytorze tekstu, który się otworzy, zobaczysz listę dwóch ostatnich komitów. Zmień `pick` przy przedostatnim komicie na `reword`.

   Przykład:
   ```plaintext
   reword abc1234 Przedostatni komit
   pick def5678 Ostatni komit
   ```

3. Zapisz i zamknij edytor. Następnie pojawi się edytor, w którym możesz zmienić wiadomość przedostatniego komitu. Wprowadź nową wiadomość, zapisz i zamknij edytor.

4. Po zakończeniu zmiany wiadomości, zakończ rebasing:
   ```bash
   git rebase --continue
   ```

5. Jeśli wcześniej wypchnąłeś już te komity do zdalnego repozytorium, musisz wymusić aktualizację, używając `git push --force`:
   ```bash
   git push --force
   ```

To wszystko! W ten sposób możesz edytować przedostatnią wiadomość w komicie GIT.