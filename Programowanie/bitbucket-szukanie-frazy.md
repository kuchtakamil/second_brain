# Bitbucket szukanie frazy

**Data:** 2025-04-15

---

**User:**

jak w bitbucket szukać danej frazy ale tylko w podanym repo?

---

**Assistant:**

W Bitbucket możesz przeszukiwać kod w konkretnym repozytorium, ale zależnie od tego, czy używasz **Bitbucket Cloud** czy **Bitbucket Server / Data Center**, sposób może się nieco różnić:

---

### 🟦 **Bitbucket Cloud**
1. Wejdź na stronę danego repozytorium.
2. W prawym górnym rogu (nad listą plików) jest **ikonka lupy** z napisem „Search in this repository”.
3. Kliknij i wpisz interesującą Cię frazę.
4. Możesz też dodać:
   - `filename:` – jeśli chcesz szukać w konkretnym pliku.
   - `path:` – jeśli chcesz szukać tylko w danym katalogu.
   - Np. `myFunction path:src/main/java`

---

### 🟪 **Bitbucket Server / Data Center**
1. Wejdź na repozytorium.
2. Po lewej stronie kliknij „Search”.
3. Możesz szukać po:
   - Całym repo
   - Konkretnych branchach
   - Można też zawęzić wyszukiwanie dodając regexy lub frazy

Jeśli Twoja instancja Bitbucket Server ma **plugin Code Search**, możesz też używać bardziej zaawansowanych operatorów.

---

### 🔍 Alternatywa: lokalne przeszukiwanie
Jeśli repozytorium masz lokalnie, szybkie i wygodne będzie:
```bash
git grep "szukana_fraza"
```
albo:
```bash
grep -rnw . -e "szukana_fraza"
```

---

Daj znać, z której wersji Bitbucketa korzystasz (Cloud czy Server), to podam dokładniejsze info albo skróty.