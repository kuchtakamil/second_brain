# Błąd składni w skrypcie

**Data:** 2025-06-09

---

**User:**

Mam skrypt SH napisany dla macOS. Przy próbie jego uruchomienia otrzymuję błąd wskazujący na ostatnią linię. Syntax Error Unexpected End of File.

---

**Assistant:**

Błąd `Syntax Error: Unexpected end of file` w skryptach shellowych (SH/Bash) oznacza, że parser shella spodziewał się jakiegoś zakończenia (np. `fi`, `done`, `}` itp.), ale nie znalazł go przed końcem pliku.

Najczęstsze przyczyny tego błędu:

---

### 🔁 1. **Niezamknięta struktura (if, while, case, funkcja, etc.):**

Np. masz `if`, ale nie ma `fi`:

```sh
if [ "$x" -eq 1 ]; then
  echo "x is 1"
# <- brak fi
```

Albo:

```sh
while true; do
  echo "looping"
# <- brak done
```

---

### 🧵 2. **Złe cudzysłowy (niedomknięty string):**

Np.:

```sh
echo "To jest test
```

Zostanie potraktowane jako niedokończony string — shell będzie „czekał” na zakończenie `"`, ale plik się kończy.

---

### 📝 3. **Niewidoczny znak (np. Windows CRLF zamiast Unix LF):**

Jeśli skrypt był edytowany w Notepadzie lub innym edytorze, który używa końców linii Windows (`\r\n`), Bash może mieć z tym problem. Sprawdź:

```sh
file twój_skrypt.sh
```

Jeśli zobaczysz `CRLF line terminators`, użyj:

```sh
dos2unix twój_skrypt.sh
```

---

### 📋 4. **Brak zamknięcia nawiasu `}` lub `)`**

Typowe w funkcjach lub tablicach:

```sh
myfunc() {
  echo "hello"
# <- brak zamknięcia }
```

---

Jeśli chcesz, podeślij zawartość skryptu lub jego końcowe linie (ostatnie 10–15), a wskażę konkretnie, gdzie jest błąd.