# Liczba plików PNG w Linuxie

**Data:** 2026-02-12

---

**User:**

linux jak zliczyć liczbę plików png

---

**Assistant:**

Najprościej i poprawnie (z uwzględnieniem podkatalogów):

```bash
find . -type f -iname '*.png' | wc -l
```

**Wyjaśnienie techniczne:**
- `find .` — rekurencyjnie od bieżącego katalogu
- `-type f` — tylko pliki (bez katalogów, linków itp.)
- `-iname` — case-insensitive (`.png`, `.PNG`, `.Png` itd.)
- `wc -l` — zlicza wiersze = liczbę plików

---

### Jeśli chcesz tylko w bieżącym katalogu (bez podkatalogów)

```bash
find . -maxdepth 1 -type f -iname '*.png' | wc -l
```

---

### Jeśli masz bardzo dużo plików (wydajniej, bez potoków)

```bash
find . -type f -iname '*.png' -printf '.' | wc -c
```

Tu `wc` zlicza znaki, nie linie — szybciej przy milionach plików.

---

### Jeśli chcesz policzyć osobno w każdym katalogu

```bash
find . -type f -iname '*.png' -exec dirname {} \; | sort | uniq -c
```

Dostaniesz liczbę PNG per katalog.