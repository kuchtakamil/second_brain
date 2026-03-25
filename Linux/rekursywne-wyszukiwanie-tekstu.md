# Rekursywne wyszukiwanie tekstu

**Data:** 2025-04-07

---

**User:**

chcę rekursywnie wyszukać w macos tekst BLACKLIST_CAT1_FURTHER_ACTION_UPLIFT we wszystkich plikach

---

**Assistant:**

Aby rekursywnie wyszukać tekst `BLACKLIST_CAT1_FURTHER_ACTION_UPLIFT` we wszystkich plikach na macOS, możesz użyć komendy `grep` w terminalu:

```bash
grep -r "BLACKLIST_CAT1_FURTHER_ACTION_UPLIFT" .
```

### Co robi ta komenda:
- `grep` — narzędzie do wyszukiwania tekstu
- `-r` — rekursywne przeszukiwanie katalogów
- `"BLACKLIST_CAT1_FURTHER_ACTION_UPLIFT"` — szukany tekst (w cudzysłowie, żeby uniknąć problemów ze znakami specjalnymi)
- `.` — aktualny katalog jako punkt startowy

### Opcjonalnie:
- Jeśli chcesz wiedzieć, które pliki zawierają ten tekst (bez samego wyniku), dodaj `-l`:
  ```bash
  grep -rl "BLACKLIST_CAT1_FURTHER_ACTION_UPLIFT" .
  ```

- Jeśli chcesz ignorować wielkość liter:
  ```bash
  grep -ril "BLACKLIST_CAT1_FURTHER_ACTION_UPLIFT" .
  ```

- Jeśli chcesz tylko pliki z konkretnym rozszerzeniem (np. `.java`):
  ```bash
  grep -rl --include="*.java" "BLACKLIST_CAT1_FURTHER_ACTION_UPLIFT" .
  ```

Daj znać, jeśli chcesz to zrobić w GUI (np. Finderem) albo przez jakąś aplikację.