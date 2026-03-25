# Przeszukiwanie katalogu Linux

**Data:** 2025-12-23

---

**User:**

chcę w linux przeszukać katalog /home/llm i znaleźć prisma.schema

---

**Assistant:**

Aby w Linuksie przeszukać katalog **/home/llm** i znaleźć plik **prisma.schema**, użyj jednego z poniższych poleceń (w zależności od potrzeby).

**Najprościej i najbezpieczniej (rekurencyjnie):**
```bash
find /home/llm -type f -name "prisma.schema"
```

**Jeśli nie masz uprawnień do części katalogów i chcesz ukryć błędy:**
```bash
find /home/llm -type f -name "prisma.schema" 2>/dev/null
```

**Jeżeli nie masz pewności co do wielkości liter (case-insensitive):**
```bash
find /home/llm -type f -iname "prisma.schema"
```

**Jeśli interesują Cię wszystkie pliki `.schema` zawierające „prisma” w nazwie:**
```bash
find /home/llm -type f -iname "*prisma*.schema"
```

Jeżeli chcesz dodatkowo **przeszukać zawartość plików** (np. znaleźć katalog projektu, który używa Prisma), daj znać — wtedy zaproponuję `grep` lub kombinację `find | xargs`.