# Identyfikacja funkcji JS

**Data:** 2024-11-26

---

**User:**

czy używając chome dev tools istnieje jakaś metoda aby zidentyfikować która funkcja w javascript (i w którym pliku) jest uruchamiana po kliknięciu na rybrany Radio button?

---

**Assistant:**

Tak, przy użyciu Chrome DevTools możesz zidentyfikować, która funkcja JavaScript (i w którym pliku) jest uruchamiana po kliknięciu na radio button. Oto kroki:

---

### 1. **Użycie narzędzia "Event Listeners"**
1. Otwórz Chrome DevTools (prawy przycisk myszy -> "Zbadaj" lub `Ctrl+Shift+I`/`Cmd+Option+I`).
2. Przejdź do zakładki **Elements**.
3. Znajdź element radio button w drzewie DOM (możesz na niego kliknąć prawym przyciskiem myszy i wybrać "Inspect").
4. W prawym panelu DevTools kliknij zakładkę **Event Listeners**.
5. Znajdź zdarzenia przypisane do elementu (np. `click`, `change`). Po kliknięciu na zdarzenie zobaczysz przypisane funkcje i ich lokalizację w kodzie.

---

### 2. **Użycie "Break on Event Listener"**
1. W zakładce **Elements** znajdź swój radio button w drzewie DOM.
2. Kliknij prawym przyciskiem myszy na elemencie w DOM, a następnie wybierz **Break on** > **Attribute modifications** lub **Subtree modifications**.
3. Następnie kliknij radio button na stronie — debugger zatrzyma się w miejscu, w którym zdarzenie zostało wywołane, wskazując na powiązaną funkcję.

---

### 3. **Monitorowanie zdarzeń w zakładce "Console"**
Jeśli chcesz zobaczyć w konsoli, która funkcja jest wywoływana:
1. W zakładce **Console** możesz użyć funkcji monitorowania, np.:
   ```javascript
   monitorEvents(document.querySelector('input[type="radio"]'), 'click');
   ```
2. Po kliknięciu radio button w konsoli pojawią się informacje o zdarzeniu, w tym o pliku i linii, w której zarejestrowano funkcję.

---

### 4. **Ustawienie punktu przerwania (breakpoint) w kodzie źródłowym**
1. Przejdź do zakładki **Sources** w DevTools.
2. Znajdź plik źródłowy, w którym podejrzewasz, że funkcja jest zdefiniowana.
3. Użyj wyszukiwania (`Ctrl+Shift+F`/`Cmd+Option+F`) z frazą odpowiadającą np. `addEventListener('click',` lub podobną.
4. Ustaw breakpoint w podejrzanej funkcji, klikając na numer linii w pliku.
5. Kliknij radio button — debugger zatrzyma się w miejscu wywołania.

---

### 5. **Analiza wywołań za pomocą `debugger`**
Jeśli masz dostęp do kodu źródłowego, możesz dodać instrukcję `debugger` w podejrzanej funkcji i odświeżyć stronę. Po kliknięciu radio button, DevTools zatrzyma wykonanie w miejscu `debugger`.

---

Te metody pozwolą Ci szybko znaleźć funkcję obsługującą zdarzenie. Jeśli nadal masz problem, mogę pomóc z bardziej szczegółową analizą. 😊