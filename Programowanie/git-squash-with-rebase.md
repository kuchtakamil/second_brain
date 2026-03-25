# Git Squash with Rebase

**Data:** 2024-01-04

---

**User:**

Jak zrobić git squash przy pomocy git rebase i


---

**Assistant:**

Aby wykonać operację `git squash` za pomocą `git rebase`, wykonaj następujące kroki:

1. **Rozpocznij Rebase**: Użyj `git rebase -i` z nazwą gałęzi, na którą chcesz rebase (np. `main`), lub podaj liczbę commitów, które chcesz squashować, używając notacji HEAD~n, gdzie n to liczba commitów. Przykład: `git rebase -i HEAD~3`.

2. **Wybór Commitów do Squashowania**: W otwartym edytorze tekstu zobaczysz listę commitów, które zostaną przeniesione. Domyślnie będą one oznaczone jako `pick`. Aby squashować commity, zmień słowo `pick` na `squash` (lub skrótowo `s`) dla każdego commitu, który chcesz połączyć. Zostaw `pick` przy pierwszym commicie z serii.

3. **Rebase Commits**: Po dokonaniu zmian zapisz i zamknij edytor. Git rozpocznie proces rebasingu i squashowania wybranych commitów.

4. **Edycja Wiadomości Commita**: Jeśli wykonałeś squash kilku commitów, Git otworzy edytor tekstu, aby umożliwić Ci edycję wiadomości dla nowego, połączonego commita. Zredaguj wiadomość i zapisz zmiany.

5. **Zakończenie Rebase**: Po zakończeniu edycji wiadomości commita, Git dokończy proces rebase. Jeśli napotkasz konflikty, będziesz musiał je rozwiązać, a następnie kontynuować rebase za pomocą `git rebase --continue`.

6. **Aktualizacja Gałęzi Zdalnej**: Jeśli wcześniejsze commity zostały już wysłane do zdalnego repozytorium, będziesz musiał użyć `git push --force` (lub `git push --force-with-lease` dla większego bezpieczeństwa), aby zaktualizować historię na zdalnym repozytorium.

Pamiętaj, że squashowanie commitów i użycie `git push --force` może wprowadzić zamieszanie w historii gałęzi, zwłaszcza jeśli pracujesz w zespole. Zawsze komunikuj się ze swoim zespołem przed wykonaniem takich operacji.