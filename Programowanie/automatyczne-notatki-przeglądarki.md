# Automatyczne notatki przeglądarki

**Data:** 2024-08-21

---

**User:**

Chciałbym stworzyć narzędzie które pozwoli mi automatyzować notatki sporządzane na podstawie oglądania stron internetowych. Przeglądam np. strony sklepu z perfumami, przeglądam wiele stron z poszczególnymi perfumami na których jest nazwa perfumy, pojemność flakonu i cena. Chciałbym stworzyć notatki w postaci
v_nazwa_perfumy - v_pojemność ml - v_cena zł
Mogę w jakiś sposób wskazać narzędziu które elementy ze strony mają być częścią takiej notatki. Po takim wskazaniu, chcę nacisnąć jakiś skrót klawiszowy a notatka ma być dodana np. do Obsydia lub Notion.
Zaproponuj stos technologiczny w którym to narzędzie może zostać wykonane.

---

**Assistant:**

Aby stworzyć narzędzie do automatyzacji tworzenia notatek na podstawie przeglądania stron internetowych, które pozwalałoby na łatwe wyciąganie informacji (takich jak nazwa perfum, pojemność flakonu i cena) i dodawanie ich do aplikacji takich jak Obsidian czy Notion, możesz skorzystać z poniższego stosu technologicznego:

### 1. **Przeglądarka i rozszerzenie przeglądarki**
   - **Technologia:** JavaScript (ES6+), HTML, CSS
   - **Narzędzie:** Rozszerzenie przeglądarki (np. Chrome, Firefox)
   - **Opis:** Rozszerzenie przeglądarki pozwoli użytkownikowi na interakcję z zawartością strony internetowej. Umożliwi ono wskazanie elementów, które mają być wyciągnięte (np. poprzez kliknięcie na elementy strony lub zaznaczenie ich). Po wybraniu elementów, użytkownik mógłby nacisnąć zdefiniowany skrót klawiszowy, który uruchomi skrypt zbierający dane i przetwarzający je w odpowiedni format.

### 2. **Scripting i ekstrakcja danych**
   - **Technologia:** JavaScript (do ekstrakcji danych)
   - **Narzędzie:** DOM API (Document Object Model API) + XPath lub `querySelector` do selekcji elementów na stronie
   - **Opis:** Skrypt w JavaScript będzie odpowiedzialny za pobranie wskazanych elementów z DOM (struktury strony). Może korzystać z XPath lub CSS Selectors, aby dokładnie wybrać te elementy (nazwa, pojemność, cena). Skrypt ten powinien również przetworzyć dane w wymaganym formacie (np. `v_nazwa_perfumy - v_pojemność ml - v_cena zł`).

### 3. **Integracja z notatnikiem**
   - **Technologia:** REST API (dla Notion) lub obsługa plików Markdown (dla Obsidian)
   - **Narzędzie:**
     - **Notion:** Notion API - pozwala na programatyczne dodawanie notatek do bazy danych lub określonej strony w Notion.
     - **Obsidian:** Zapisywanie danych do pliku Markdown w lokalnym systemie plików.
   - **Opis:** W przypadku Notion, rozszerzenie przeglądarki może wysyłać dane bezpośrednio do API Notion, gdzie będą one automatycznie dodawane do określonego miejsca w Notion. W przypadku Obsidian, dane mogą być zapisywane lokalnie jako plik `.md`, który Obsidian będzie mógł automatycznie przetworzyć.

### 4. **Backend (opcjonalnie)**
   - **Technologia:** Node.js, Express.js (opcjonalnie)
   - **Opis:** Backend może być używany do dodatkowego przetwarzania danych, obsługi autoryzacji do API Notion lub jako miejsce do przechowywania konfiguracji użytkownika (np. szablony notatek). Może też służyć jako pośrednik między przeglądarką a aplikacjami zewnętrznymi.

### 5. **Interfejs użytkownika**
   - **Technologia:** HTML, CSS, JavaScript
   - **Opis:** Interfejs użytkownika rozszerzenia przeglądarki powinien być prosty i intuicyjny, umożliwiając łatwe wskazanie elementów na stronie oraz podgląd zebranych danych przed wysłaniem ich do wybranej aplikacji.

### 6. **Zarządzanie skrótami klawiszowymi**
   - **Technologia:** JavaScript + przeglądarka (API skrótów klawiszowych)
   - **Opis:** Możesz użyć przeglądarkowego API do przypisania skrótu klawiszowego, który uruchomi proces zbierania danych i tworzenia notatki.

### 7. **Użytkowanie**
   - **Opis:** Po zainstalowaniu rozszerzenia, użytkownik odwiedza stronę z perfumami, wybiera odpowiednie elementy (nazwa, pojemność, cena) na stronie, a następnie za pomocą skrótu klawiszowego zapisuje te dane w formacie notatki do Obsidian lub Notion.

### Podsumowanie:
- **Frontend:** Rozszerzenie przeglądarki napisane w HTML/CSS/JS
- **Backend:** Opcjonalny, napisany w Node.js (jeśli potrzeba dodatkowej logiki lub przetwarzania)
- **Integracja:** Notion API lub zapis plików Markdown dla Obsidian
- **Interfejs użytkownika:** Prosty GUI umożliwiający interakcję z treścią strony
- **Automatyzacja:** Skróty klawiszowe do szybkiego zbierania danych

Zastosowanie tego stosu technologicznego pozwoli na stworzenie efektywnego narzędzia do automatyzacji tworzenia notatek z treści internetowych.

---

**User:**

A czy możliwe jest stworzenie aplikacji w Rust która będzie działać i po zminimalizowaniu i otwarciu przeglądarki będzie przechwytywać dane  tekstowe do zapisania?

---

**Assistant:**

Tak, możliwe jest stworzenie aplikacji w Rust, która działałaby w tle (nawet po zminimalizowaniu) i przechwytywałaby dane tekstowe z przeglądarki do późniejszego zapisania. Taka aplikacja mogłaby działać jako tzw. "headless" (czyli bez interfejsu graficznego) lub jako aplikacja z minimalnym GUI, która pozwala na łatwe zarządzanie jej działaniem. Poniżej znajdziesz opis technologii i kroków, które mogłyby być użyte do stworzenia takiego narzędzia.

### 1. **Rust jako język główny**
   - **Język:** Rust
   - **Opis:** Rust jest świetnym wyborem do pisania aplikacji działających w tle ze względu na swoją wydajność, bezpieczeństwo pamięci oraz możliwość bezpośredniego operowania na niskim poziomie. Pozwoli to na efektywne przechwytywanie danych tekstowych bez dużego obciążenia systemu.

### 2. **Przechwytywanie danych z przeglądarki**
   - **Biblioteki:** 
     - **`wry` lub `tauri`:** Umożliwia tworzenie aplikacji desktopowych z możliwością interakcji z treścią przeglądarki (np. poprzez WebView). Może być użyte, jeśli aplikacja ma posiadać GUI.
     - **`inputbot` lub `enigo`:** Biblioteki do zarządzania wejściami użytkownika (przechwytywanie skrótów klawiszowych, kliknięć).
     - **`reqwest` lub `ureq`:** Do wysyłania żądań HTTP, jeżeli chciałbyś komunikować się z API (np. Notion).
   - **Opis:** Aplikacja mogłaby działać w tle i nasłuchiwać na określone skróty klawiszowe. Po wykryciu skrótu, mogłaby przechwytywać zawartość schowka systemowego (clipboard), w którym użytkownik mógłby wcześniej umieścić dane skopiowane z przeglądarki. 

### 3. **Zarządzanie skrótami klawiszowymi**
   - **Biblioteka:** `inputbot`, `enigo`
   - **Opis:** Umożliwia nasłuchiwanie na globalne skróty klawiszowe, które użytkownik może skonfigurować, aby wywołać określone akcje, takie jak zapisanie danych do pliku lub wysłanie ich do aplikacji.

### 4. **Zarządzanie schowkiem systemowym**
   - **Biblioteka:** `arboard` lub `copypasta`
   - **Opis:** Pozwala na dostęp do schowka systemowego, z którego można pobierać tekst (np. po skopiowaniu tekstu z przeglądarki). Aplikacja mogłaby przechwytywać zawartość schowka w momencie wykrycia skrótu klawiszowego.

### 5. **Zapis do pliku lub integracja z API**
   - **Zapis do pliku:** Aplikacja może zapisywać dane bezpośrednio do pliku na dysku (np. pliku Markdown w przypadku Obsidian) przy użyciu standardowych funkcji zapisu do plików w Rust.
   - **Integracja z API:** Można użyć `reqwest` lub `ureq` do komunikacji z API Notion, gdzie dane byłyby automatycznie dodawane do odpowiedniego miejsca w aplikacji.

### 6. **Działanie w tle**
   - **Biblioteka:** `systemd` (Linux), `winapi` (Windows), `launchd` (macOS)
   - **Opis:** Aplikacja może być skonfigurowana do działania jako usługa systemowa lub aplikacja w trayu (dla GUI), co pozwala na jej minimalizację lub uruchamianie bez okna. Dzięki temu użytkownik może kontynuować pracę, a aplikacja będzie działać w tle.

### 7. **Ewentualne GUI**
   - **Biblioteka:** `Tauri`, `egui` lub `iced`
   - **Opis:** Jeśli chcesz, aby aplikacja miała proste GUI do zarządzania konfiguracją lub podglądu zebranych danych, możesz użyć jednej z tych bibliotek do stworzenia minimalistycznego interfejsu.

### 8. **Użytkowanie**
   - Aplikacja działa w tle, czeka na aktywację skrótu klawiszowego.
   - Użytkownik kopiuje tekst z przeglądarki (np. nazwę perfum, pojemność, cenę).
   - Po naciśnięciu określonego skrótu klawiszowego aplikacja przechwytuje zawartość schowka, przetwarza ją i zapisuje do pliku lub wysyła do Notion.

### Podsumowanie:
- **Główna aplikacja:** Rust
- **Przechwytywanie skrótów:** `inputbot`, `enigo`
- **Przechwytywanie schowka:** `arboard`, `copypasta`
- **Zapis danych:** Do pliku lub poprzez API (np. `reqwest`)
- **Działanie w tle:** Usługa systemowa lub aplikacja trayowa
- **Ewentualne GUI:** `Tauri`, `egui`, `iced`

Taki stos technologiczny pozwoli Ci stworzyć lekką i wydajną aplikację w Rust, która będzie działać w tle i automatyzować proces tworzenia notatek na podstawie przeglądanych stron.