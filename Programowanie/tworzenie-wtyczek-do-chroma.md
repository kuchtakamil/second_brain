# Tworzenie wtyczek do Chroma

**Data:** 2024-08-25

---

**User:**

Chciałbym napisać wtyczkę do Chroma. W jakich językach mogę to zrobić?

---

**Assistant:**

Aby napisać wtyczkę do przeglądarki Chrome, musisz użyć kilku kluczowych technologii:

1. **HTML** - do tworzenia interfejsu użytkownika wtyczki, takich jak popupy, strony opcji, czy panele w narzędziach deweloperskich.

2. **CSS** - do stylizacji interfejsu wtyczki.

3. **JavaScript** - to główny język używany do logiki działania wtyczki, obsługi zdarzeń, komunikacji z przeglądarką oraz manipulacji DOM.

4. **JSON** - używany do definiowania manifestu wtyczki (`manifest.json`), który zawiera wszystkie kluczowe informacje o wtyczce, takie jak nazwa, wersja, uprawnienia i pliki składające się na wtyczkę.

5. **WebAssembly** (opcjonalnie) - jeśli wtyczka wymaga bardziej zaawansowanych obliczeń, można użyć WebAssembly do uruchamiania kodu napisanego w językach takich jak C, C++, Rust, czy innych, które mogą być skompilowane do WebAssembly.

Do stworzenia wtyczki potrzebne są przynajmniej podstawowe umiejętności w HTML, CSS i JavaScript. JSON jest również konieczny do skonfigurowania manifestu. WebAssembly jest opcjonalne i wymaga bardziej zaawansowanej wiedzy.

---

**User:**

Czy tworząc taką wtyczkę mogę obejść się bez używania JavaScript, a użyć jedynie WebAssembly, czyli Rasta?

---

**Assistant:**

W teorii, można zbudować wtyczkę Chrome bez użycia JavaScriptu, opierając się wyłącznie na WebAssembly (i w tym przypadku na języku Rust). Jednakże, w praktyce nie jest to takie proste i ma pewne ograniczenia:

1. **Ładowanie WebAssembly**: Aby załadować i uruchomić moduł WebAssembly w przeglądarce, nadal potrzebujesz pewnej ilości kodu JavaScript. WebAssembly nie jest w stanie samodzielnie załadować się do przeglądarki; potrzebuje „bootstrapu” w JavaScript, który go załaduje i uruchomi.

2. **Interakcje z DOM**: WebAssembly jest bardzo wydajny, ale jego możliwości interakcji z DOM są ograniczone. Większość interakcji z DOM, takich jak manipulacja elementami na stronie czy obsługa zdarzeń, odbywa się przez JavaScript. Chociaż istnieją narzędzia i biblioteki, które pozwalają na bardziej bezpośrednią komunikację między WebAssembly a DOM, to JavaScript pozostaje głównym środkiem do tego celu.

3. **API przeglądarki**: Większość API przeglądarki, które są dostępne w kontekście wtyczki (np. API do komunikacji z treścią strony, zarządzania zakładkami, historii, itp.), jest dostępnych tylko poprzez JavaScript. WebAssembly sam w sobie nie ma bezpośredniego dostępu do tych API.

4. **Kod startowy**: Nawet jeśli główna logika wtyczki jest napisana w Rust i uruchamiana jako WebAssembly, nadal potrzebujesz trochę kodu JavaScript, aby rozpocząć działanie wtyczki, załadować moduł WebAssembly i przekazać do niego kontrolę.

**Podsumowując**: Możliwe jest napisanie większości logiki w Rust i uruchomienie jej jako WebAssembly, ale nie obejdziesz się całkowicie bez JavaScriptu. Będziesz potrzebował przynajmniej małej ilości kodu JavaScript do ładowania i interakcji z WebAssembly oraz do obsługi niektórych funkcji wtyczki, takich jak interakcja z DOM czy API przeglądarki.

---

**User:**

Czy zamiast JavaScripta można użyć TypeScripta?

---

**Assistant:**

Tak, zamiast JavaScriptu możesz użyć TypeScriptu do tworzenia wtyczki do przeglądarki Chrome. TypeScript jest nadzbiorem JavaScriptu, który dodaje statyczne typowanie oraz inne funkcje, takie jak interfejsy, klasy czy moduły, co ułatwia pisanie bardziej złożonych i mniej podatnych na błędy aplikacji.

Aby użyć TypeScriptu w swojej wtyczce, musisz:

1. **Zainstalować TypeScript**: Upewnij się, że masz zainstalowany TypeScript i skonfigurowane środowisko do jego kompilacji. Możesz to zrobić za pomocą npm:
   ```bash
   npm install -g typescript
   ```

2. **Skonfigurować plik `tsconfig.json`**: Utwórz plik konfiguracyjny TypeScriptu (`tsconfig.json`) w katalogu projektu. Przykładowy plik może wyglądać tak:
   ```json
   {
     "compilerOptions": {
       "target": "es6",
       "module": "commonjs",
       "outDir": "./dist",
       "strict": true,
       "esModuleInterop": true
     },
     "include": ["src/**/*.ts"],
     "exclude": ["node_modules"]
   }
   ```
   W tym przykładzie kod TypeScript jest kompilowany do kodu ES6 i umieszczany w katalogu `./dist`.

3. **Kompilacja TypeScriptu do JavaScriptu**: TypeScript musi zostać skompilowany do JavaScriptu, zanim będzie mógł być użyty w przeglądarce. Możesz to zrobić, uruchamiając:
   ```bash
   tsc
   ```
   Kompilator przetworzy wszystkie pliki `.ts` i wygeneruje odpowiadające im pliki `.js`.

4. **Włączanie skompilowanych plików JavaScript**: Po skompilowaniu TypeScriptu do JavaScriptu, używasz tych plików JavaScript w swojej wtyczce, tak jakby były napisane w czystym JavaScripcie.

**Przykład struktury projektu:**
```
my-extension/
│
├── src/
│   ├── background.ts
│   ├── content_script.ts
│   └── popup.ts
│
├── dist/
│   ├── background.js
│   ├── content_script.js
│   └── popup.js
│
├── manifest.json
└── tsconfig.json
```

W powyższej strukturze, `src/` zawiera pliki TypeScript (`.ts`), a `dist/` zawiera skompilowane pliki JavaScript (`.js`), które są w rzeczywistości używane w wtyczce.

**Podsumowanie**: TypeScript to świetna opcja, która może poprawić jakość i czytelność kodu Twojej wtyczki. Końcowy kod wciąż będzie JavaScriptem, ale pisany będzie w bardziej bezpiecznym i nowoczesnym środowisku TypeScriptu.