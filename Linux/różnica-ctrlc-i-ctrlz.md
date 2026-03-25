# Różnica Ctrl+C i Ctrl+Z

**Data:** 2025-07-04

---

**User:**

W linux jaka jest różnica między Ctrl + C a Ctrl + Z ?

---

**Assistant:**

W systemach Linux (i ogólnie Unixowych) skróty klawiszowe `Ctrl + C` i `Ctrl + Z` służą do kontrolowania procesów uruchomionych w terminalu, ale mają różne znaczenia:

---

### `Ctrl + C`
- **Działanie:** Wysyła do procesu sygnał `SIGINT` (ang. *interrupt*).
- **Efekt:** **Natychmiast przerywa (zabija)** aktualnie działający proces w terminalu.
- **Typowe użycie:** Gdy chcesz zatrzymać program, który się zawiesił, zapętlił albo po prostu chcesz go zakończyć ręcznie.

---

### `Ctrl + Z`
- **Działanie:** Wysyła do procesu sygnał `SIGTSTP` (ang. *terminal stop*).
- **Efekt:** **Wstrzymuje (pauzuje)** proces i przenosi go do tła, w stan *stopped*.
- **Typowe użycie:** Gdy chcesz tymczasowo wstrzymać działanie procesu, np. edytor tekstu `vim`, żeby wrócić później.
- **Wznowienie procesu:**
  - `fg` – przywraca proces na pierwszy plan (foreground).
  - `bg` – wznawia proces w tle (background).

---

### Przykład:
Załóżmy, że uruchamiasz program `yes` (który wypisuje nieskończenie `"y"`):
- `yes`
- `Ctrl + C` → program się natychmiast kończy.
- `Ctrl + Z` → program zostaje wstrzymany; możesz to sprawdzić komendą `jobs`.

---

Jeśli chcesz, mogę też wyjaśnić różnice między `fg`, `bg`, `jobs`, `kill` i innymi poleceniami do zarządzania procesami w terminalu.