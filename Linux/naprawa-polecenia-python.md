# Naprawa polecenia python

**Data:** 2025-07-06

---

**User:**

w ubuntu działa mi polecenie python3 ale python już nie. Używam oh my zsh, jak to naprawić?

---

**Assistant:**

Domyślnie w Ubuntu (szczególnie w wersjach nowszych niż 20.04) polecenie `python` nie wskazuje na żadną wersję Pythona, ponieważ domyślnie jest zainstalowany tylko `python3`, a `python` jako alias nie jest tworzony automatycznie.

Aby `python` działało tak samo jak `python3`, masz kilka opcji:

---

### ✅ **Najprostsze rozwiązanie: alias w `.zshrc`**

1. Otwórz swój plik `.zshrc`:
   ```bash
   nano ~/.zshrc
   ```

2. Dodaj na końcu pliku:
   ```bash
   alias python=python3
   ```

3. Zapisz i zamknij plik, potem zaktualizuj konfigurację:
   ```bash
   source ~/.zshrc
   ```

4. Sprawdź:
   ```bash
   python --version
   ```

---

### 🔧 Alternatywnie: ustaw `python` globalnie przez `update-alternatives`

Jeśli chcesz, żeby `python` działał systemowo (np. w skryptach innych użytkowników), możesz ustawić go przez `update-alternatives`:

```bash
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3 1
```

Sprawdź:
```bash
python --version
```

---

### 🧼 Uwaga

Niektóre skrypty systemowe mogą wymagać konkretnej wersji Pythona (np. `python2` lub `python3`). Ręczne ustawienie `python` na `python3` może teoretycznie wprowadzać niezgodność w bardzo starych systemach, ale w nowoczesnym Ubuntu to bezpieczne.

---

Daj znać, jeśli chcesz, żeby `python` wskazywał na inną wersję (np. z `pyenv`, Conda lub `venv`).