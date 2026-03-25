# Cofanie ostatniego commita

**Data:** 2024-12-06

---

**User:**

git. chcę cofnąć ostatni commit czyli zrobić nowy commit który przywraca zmiany ze starego

---

**Assistant:**

Aby cofnąć ostatni commit i zrobić nowy commit, który przywraca zmiany z tego commita, możesz skorzystać z następujących kroków:

1. **Utwórz commit przywracający zmiany:**

   Użyj polecenia `git revert`:

   ```bash
   git revert HEAD
   ```

   To polecenie tworzy nowy commit, który odwraca zmiany wprowadzone w ostatnim commitcie. Git automatycznie otworzy edytor tekstu, aby umożliwić edycję wiadomości do commita. Możesz zachować domyślną wiadomość lub ją zmodyfikować.

2. **Zatwierdź zmiany:**

   Po zapisaniu wiadomości commit zostanie zapisany i odwróci zmiany z ostatniego commita.

Jeśli chcesz automatycznie zatwierdzić revert bez edytowania wiadomości commit, możesz dodać flagę `--no-edit`:

```bash
git revert HEAD --no-edit
```

To rozwiązanie pozwala zachować historię commitów w porządku i jest szczególnie przydatne, jeśli pracujesz z repozytorium współdzielonym z innymi.