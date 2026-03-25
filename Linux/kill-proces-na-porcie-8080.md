# Kill proces na porcie 8080

**Data:** 2025-10-12

---

**User:**

jak w linux zrobić kill dla procesu który słucha na porcie 8080

---

**Assistant:**

Aby zabić proces, który nasłuchuje na porcie **8080** w Linuxie, możesz wykonać to w jednym poleceniu:  

```bash
sudo kill -9 $(sudo lsof -t -i:8080)
```

### Wyjaśnienie:
- `lsof -t -i:8080` – zwraca **PID** procesu, który używa portu 8080  
  - `-i:8080` → filtruje po porcie  
  - `-t` → wypisuje tylko PID (bez zbędnych informacji)  
- `kill -9` → wymusza zakończenie procesu  
- `sudo` może być potrzebne, jeśli proces należy do innego użytkownika

---

Alternatywnie możesz to zrobić krok po kroku:

1. Znajdź PID procesu:
   ```bash
   sudo lsof -i:8080
   ```
   lub:
   ```bash
   sudo netstat -tulpn | grep :8080
   ```
2. Zobacz PID w kolumnie **PID/Program name**.
3. Zabij proces:
   ```bash
   sudo kill -9 <PID>
   ```

---

💡 Jeśli chcesz zabić tylko „grzecznie” (spróbować zamknąć proces poprawnie), użyj:
```bash
sudo kill $(sudo lsof -t -i:8080)
```
Bez `-9` — daje procesowi szansę na posprzątanie po sobie.