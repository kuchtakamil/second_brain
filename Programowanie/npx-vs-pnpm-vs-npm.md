# npx vs pnpm vs npm

**Data:** 2025-10-03

---

**User:**

Znam npm - pracowałem kiedyś z Nodejs i Angular. Ale co to jest npx i pnpm?

---

**Assistant:**

Dobre pytanie – to trzy różne narzędzia, które często się spotyka razem, ale pełnią inne role.  

### 1. **npm**
To znasz: **Node Package Manager** – standardowy menedżer paczek dla Node.js.  
- Służy do instalowania bibliotek (`npm install express`)  
- Zarządza zależnościami w `package.json`  
- Potrafi uruchamiać skrypty zdefiniowane w `package.json` (`npm run build`)  

---

### 2. **npx**
To **narzędzie dostarczane wraz z npm (od npm 5.2+)**.  
- Jego głównym celem jest **uruchamianie paczek bez konieczności ich globalnej instalacji**.  
- Przykład: zamiast instalować create-react-app globalnie:
  ```bash
  npx create-react-app my-app
  ```
  → `npx` pobierze paczkę, uruchomi ją, a potem wyrzuci, jeśli nie jest już potrzebna.  
- Jeśli paczka jest już zainstalowana lokalnie w projekcie (`node_modules`), `npx` też ją znajdzie i uruchomi.  

Można to traktować jako „odpalacz paczek” – wygodne do jednorazowych CLI.

---

### 3. **pnpm**
To alternatywa dla npm i yarn – **szybszy i bardziej wydajny menedżer paczek**.  
- Główna różnica: **pnpm używa linków symbolicznych i pojedynczego globalnego cache** dla wszystkich projektów.  
  - npm instaluje kopię każdej paczki osobno w `node_modules`.  
  - pnpm trzyma jedną wersję paczki w globalnym magazynie i robi linki → oszczędza miejsce i przyspiesza instalację.  
- Przykład użycia:
  ```bash
  pnpm install express
  pnpm run build
  ```
- Coraz częściej używany w większych projektach (np. monorepo), bo radzi sobie lepiej z dużą ilością zależności.

---

🔑 Podsumowanie:  
- **npm** – menedżer paczek.  
- **npx** – do uruchamiania paczek (lokalnych lub jednorazowych).  
- **pnpm** – alternatywny, wydajniejszy menedżer paczek.  

Chcesz, żebym zrobił Ci krótką tabelkę porównawczą npm vs npx vs pnpm, żebyś miał to w skrócie?