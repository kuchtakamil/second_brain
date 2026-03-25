# Poprawa polecenia find

**Data:** 2024-11-28

---

**User:**

popraw find / --name=application.properties

---

**Assistant:**

A more accurate and commonly used form of the command is:

```bash
find / -name application.properties 2>/dev/null
```

### Explanation:
1. **`find`**: The command to search for files.
2. **`/`**: The root directory, indicating that the search will span the entire filesystem.
3. **`-name application.properties`**: Specifies the name of the file to search for.
4. **`2>/dev/null`**: Redirects error messages (like "Permission denied") to `/dev/null`, effectively silencing them.

This ensures the output contains only the paths of files named `application.properties`, without clutter from errors.

---

**User:**

a jak przeszukać wszystkie pliki zeby znaleźć tekst ss-my-refupg

---

**Assistant:**

Aby przeszukać wszystkie pliki w systemie i znaleźć tekst `ss-my-refupg`, możesz użyć narzędzia `grep`. Oto poprawne polecenie:

```bash
grep -rnw '/' -e 'ss-my-refupg' 2>/dev/null
```

### Wyjaśnienie:
1. **`grep`**: Komenda do wyszukiwania tekstu w plikach.
2. **`-r`**: Rekurencyjne przeszukiwanie katalogów.
3. **`-n`**: Wyświetlanie numerów linii, w których znaleziono dopasowanie.
4. **`-w`**: Wyszukiwanie całego słowa (jeśli `ss-my-refupg` jest częścią większego słowa, usuń tę flagę).
5. **`'/'`**: Wskazuje katalog główny jako punkt startowy wyszukiwania.
6. **`-e 'ss-my-refupg'`**: Wskazuje tekst do wyszukania.
7. **`2>/dev/null`**: Ukrywa błędy (np. "Permission denied") dla katalogów, do których nie masz dostępu.

### Jeśli chcesz zobaczyć tylko ścieżki do plików zawierających tekst:
Użyj flagi `-l` (bez wyświetlania zawartości i numerów linii):
```bash
grep -rl '/' -e 'ss-my-refupg' 2>/dev/null
```

### Uwaga:
- Możesz uruchomić polecenie z uprawnieniami superużytkownika (sudo), aby uzyskać dostęp do chronionych katalogów:
  ```bash
  sudo grep -rnw '/' -e 'ss-my-refupg'
  ```