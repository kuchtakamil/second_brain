# Udostępnianie IDE online

**Data:** 2025-05-12

---

**User:**

W czasie interview chciałbym kandydatowi na software engineera udostępnić przygotowane środowisko. O ile utworzenie i udostępnienie przykładowego projektu w którym kandydat miałby znaleźć bug, nie jest dużym problemem, o tyle nie wiem jak rozwiązać problem jak udostępnić IDE kandydatowi. Idealnym rozwiązaniem byłoby mieć intellij lub vscode w wersji przeglądarkowej online, przynajmniej w uproszczonej wersji.

---

**Assistant:**

To bardzo ciekawe podejście do interview — bardziej praktyczne i bliskie realiom pracy. Istnieje kilka sposobów, aby udostępnić kandydatowi środowisko programistyczne przez przeglądarkę. Oto sprawdzone i sensowne opcje:

---

### 🔧 **1. GitHub Codespaces (dla VS Code)**
- **Opis**: To pełnoprawne środowisko VS Code w chmurze, z dostępem do terminala, debuggera, itd.
- **Zalety**: 
  - Bazuje na Dockerze, więc łatwo przygotować z góry środowisko.
  - Kandydat nie musi nic instalować.
  - Integracja z GitHub.
- **Wymagania**: Kandydat musi mieć konto na GitHubie. Dla organizacji komercyjnych GitHub Codespaces wymaga planu płatnego.

📌 **Alternatywa**: [https://github.com/features/codespaces](https://github.com/features/codespaces)

---

### ☁️ **2. Gitpod**
- **Opis**: Kolejna przeglądarkowa wersja VS Code. Automatycznie konfiguruje środowisko na podstawie `.gitpod.yml`.
- **Zalety**: 
  - Obsługuje wiele języków, również Javę.
  - Łatwo udostępnić repozytorium z gotowym projektem.
  - Działa również z prywatnymi repozytoriami (po autoryzacji).
- **Minusy**: Darmowy plan ma limity czasowe (np. 50h miesięcznie).

📌 [https://gitpod.io](https://gitpod.io)

---

### 🔍 **3. CodeSandbox (bardziej do frontendów, Node.js)**
- **Opis**: Świetne do frontendu lub lekkiego Node.js, nieco mniej przydatne przy dużych projektach Java.
- **Zalety**: Szybko się uruchamia, świetne UX.
- **Minusy**: Brak wsparcia dla pełnego backendu Javy.

---

### 🚀 **4. Coder (open-source self-hosted IDE z VS Code)**
- **Opis**: Możesz samodzielnie hostować środowisko z VS Code przez przeglądarkę, np. na maszynie EC2, GCP, czy VPS.
- **Zalety**: Masz pełną kontrolę, możesz mieć dowolne pluginy, JDK itd.
- **Minusy**: Musisz zarządzać dostępem i zasobami (np. VPN, konta tymczasowe).

📌 [https://coder.com](https://coder.com)

---

### 🧠 **5. JetBrains Projector lub JetBrains Gateway z IntelliJ IDEA**
- **Opis**: Udostępnienie IntelliJ przez przeglądarkę (Projector) lub klienta zdalnego (Gateway).
- **Zalety**: Masz „prawdziwe IntelliJ”, nawet z pluginami.
- **Minusy**: Konfiguracja jest bardziej złożona, wymaga dobrej maszyny po stronie serwera.

📌 [https://github.com/JetBrains/projector-server](https://github.com/JetBrains/projector-server)

---

### 🔐 **Organizacja testu**
- Zakładasz środowisko z gotowym projektem (np. mikroserwis z bugiem).
- Tworzysz tymczasowe konto lub link dostępu.
- Kandydat loguje się i pracuje jak w realnym IDE.
- Możesz dołożyć `readme.md` z instrukcją co sprawdzić / jak uruchomić testy.

---

Chcesz środowisko bardziej pod Javę (np. Spring Boot), czy raczej ogólne — np. do debugowania błędów w różnych językach?