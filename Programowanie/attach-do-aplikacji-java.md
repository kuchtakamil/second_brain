# Attach do aplikacji Java

**Data:** 2025-09-19

---

**User:**

Korzystam z Coursor AI bazującym na VS Code. W konsoli w linux mam uruchomioną aplikację java w trybie debug która nasłuchuje na port 5005. Jak teraz w VS Code mam zrobić attach do tej aplikacji

---

**Assistant:**

Aby podpiąć się z **VS Code** (a właściwie Coursor AI, który bazuje na VS Code) do działającej aplikacji Javy uruchomionej w trybie debug (`-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=5005`), musisz skonfigurować `launch.json`.  

Kroki:  

1. Upewnij się, że masz zainstalowane rozszerzenie **Debugger for Java** (wchodzi w skład pakietu *Extension Pack for Java*).  

2. W VS Code otwórz:  
   - `Ctrl+Shift+P` → wpisz **"Debug: Open launch.json"**.  

3. W pliku `launch.json` dodaj konfigurację typu `attach`, np.:  

   ```json
   {
     "version": "0.2.0",
     "configurations": [
       {
         "type": "java",
         "name": "Attach to Remote Java",
         "request": "attach",
         "hostName": "localhost",
         "port": 5005
       }
     ]
   }
   ```

4. Zapisz plik, a następnie wybierz w panelu debugowania (po lewej stronie) konfigurację **Attach to Remote Java** i uruchom ją (`F5`).  

Wtedy VS Code połączy się z twoją aplikacją działającą w trybie debug i będziesz mógł normalnie korzystać z breakpointów.  

Chcesz, żebym Ci pokazał też minimalny przykład uruchomienia aplikacji Javy z włączonym debugiem (np. `mvn spring-boot:run` albo `java -jar ...` z odpowiednimi flagami), żeby mieć pełny obraz od końca do końca?