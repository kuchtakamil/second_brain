# Testy rozwiązywania problemów

**Data:** 2025-05-11

---

**User:**

czy są jakieś znane testy sprawdzające umiejętność tzw Problem solving?

---

**Assistant:**

Tak, istnieje wiele znanych testów i platform służących do sprawdzania i rozwijania umiejętności **problem solving** — zarówno ogólnych, jak i technicznych (np. programistycznych). Oto podział na kilka kategorii:

---

### 🧠 **Testy ogólne (logiczne myślenie, analityka, rozwiązywanie problemów):**

1. **Raven's Progressive Matrices**  
   - Klasyczny test na inteligencję płynną (rozpoznawanie wzorców, logiczne myślenie bez wiedzy językowej).
   - Używany często w testach IQ i rekrutacjach.

2. **SHL / Talent Q / Cubiks / Kenexa**  
   - Profesjonalne testy stosowane w rekrutacjach. Obejmują różne aspekty: rozumowanie logiczne, werbalne, numeryczne i abstrakcyjne.
   - Często używane przez duże firmy i korporacje.

3. **Numerical & Logical Reasoning Tests (np. JobTestPrep, PracticeAptitudeTests)**  
   - Symulują typowe zadania sprawdzające umiejętność szybkiego analizowania informacji i podejmowania decyzji.

---

### 👨‍💻 **Dla programistów (algorytmy, myślenie analityczne, rozwiązywanie zadań kodowych):**

1. **LeetCode / HackerRank / CodeSignal / Codewars / Codility**  
   - Zadania oparte na problem solvingu (algorytmy, struktury danych). 
   - Szczególnie LeetCode i CodeSignal mają dedykowane działy „problem solving”.

2. **Advent of Code / Project Euler**  
   - Matematyczno-logiczne łamigłówki, często z elementami kodowania.
   - Świetne do nauki i rozwijania kreatywnego podejścia do rozwiązywania problemów.

3. **Google Foobar**  
   - Ukryty rekrutacyjny test Google’a dla programistów (zaproszenia często przychodzą po wpisaniu odpowiednich fraz w Google).
   - Zadania są trudne i skupione na myśleniu algorytmicznym.

---

### 🧩 **Zabawa i rozwój (logiczne łamigłówki, zadania intelektualne):**

1. **Brilliant.org**  
   - Interaktywne kursy i zadania z matematyki, informatyki i logiki.
   - Duży nacisk na rozumienie problemu, a nie tylko wynik.

2. **Lumosity / Peak**  
   - Gry rozwijające pamięć, koncentrację, szybkość myślenia i elastyczność poznawczą.

---

Czy interesuje Cię bardziej wersja ogólna (np. do ćwiczenia logiki), czy raczej techniczna (np. dla programisty)?

---

**User:**

Chciałbym znaleźć sposób na testowanie umiejętności Problem solving dla inżynierów oprogramowania. Jednak nie chcę żeby to był zwykły test programowania, live coding, algorytmy itp. Bardziej interesuje mnie czy testowana osoba posiada umiejętności kojarzenia faktów, szukania i znajdywania zależności, przeszukiwania bazy kodu itp

---

**Assistant:**

Użytkownik szuka sposobu na testowanie umiejętności problem solving u inżynierów oprogramowania, ale nie poprzez klasyczne testy programistyczne czy algorytmy. Interesuje go testowanie zdolności do kojarzenia faktów, znajdowania zależności i przeszukiwania bazy kodu.

---

**Assistant:**

Świetnie — to podejście znacznie lepiej odzwierciedla codzienną pracę inżyniera oprogramowania niż typowe testy algorytmiczne. Skoro zależy Ci na sprawdzaniu **praktycznego problem solvingu**, a nie „competitive programming”, warto podejść do tego bardziej realistycznie. Oto kilka pomysłów i form testów, które możesz wykorzystać:

---

### 🔍 **1. Zadanie eksploracyjne w dużej bazie kodu**
**Cel:** Sprawdzenie umiejętności czytania kodu, rozumienia zależności i lokalizowania problemów.  
**Forma:**
- Dostarcz kandydata/pracownika zanonimizowaną bazą kodu (np. open-source lub mock project).
- Zadaj pytania typu:
  - „W jaki sposób działa funkcja X?”
  - „Co się stanie, jeśli zmienimy zachowanie endpointu Y?”
  - „Gdzie znajduje się kod odpowiedzialny za zachowanie Z?”
- Alternatywnie: „Ten system ma błąd polegający na… Znajdź źródło problemu.”

👉 *Symuluje debugging, rozpoznawanie wzorców i orientację w złożonym środowisku.*

---

### 🧠 **2. Scenariusze z niepełną informacją (case study)**
**Cel:** Sprawdzenie kojarzenia faktów i zadawania właściwych pytań.  
**Forma:**
- Podajesz opis sytuacji, np. „Użytkownicy skarżą się, że system X czasami zwraca błędne dane.”
- Kandydat musi:
  - Zidentyfikować możliwe przyczyny.
  - Zadać pytania lub zaproponować eksperymenty / logi do sprawdzenia.
  - Opisać, jak by diagnozował i naprawił problem.

👉 *Sprawdza analityczne myślenie, priorytetyzację i metodykę dochodzenia do źródła problemu.*

---

### 🧭 **3. Zadanie typu “System Navigation Quest”**
**Cel:** Ocena zdolności odnajdywania się w dużych systemach.  
**Forma:**
- Dostajesz złożoną dokumentację/API (np. Swagger, README + kilka modułów).
- Pytania:
  - „Który endpoint odpowiada za X?”
  - „Gdzie znajduje się konfiguracja dla komponentu Y?”
  - „Czy ten komponent może działać bez zależności Z?”

👉 *Weryfikuje orientację, umiejętność szybkiego ogarniania systemu oraz wyciągania logicznych wniosków.*

---

### 🔧 **4. Realistyczne zadanie maintenance / debug / refactor**
**Cel:** Pokazanie codziennego problem solvingu bez pisania od zera.  
**Forma:**
- Dajesz fragment istniejącego kodu z bugiem, nieczytelną logiką lub niepełną funkcją.
- Zadajesz pytanie: „Zrób refaktoryzację tak, by…”, „Napraw błąd X” albo „Wydłuż funkcję o obsługę przypadku Y”.

---

### 📘 **5. Test umiejętności wyszukiwania informacji**
**Cel:** Ocena, jak dobrze ktoś wykorzystuje narzędzia (kod, dokumentację, Stack Overflow, itp.).  
**Forma:**
- Dajesz problem, którego rozwiązanie jest „wiedzą powszechną” (ale nie trywialną) lub wymaga szukania przykładów.
- Obserwujesz sposób dochodzenia do odpowiedzi — czy wie, czego i gdzie szukać, czy zadaje właściwe pytania.

---

### 💡 Jak to wdrożyć?
- Możesz stworzyć mini sandbox w GitHub Codespaces, repl.it albo jako repo z instrukcją.
- Jeśli chcesz zautomatyzować: rozważ stworzenie własnego assessment tool (np. w oparciu o Jupyter Notebook, VSCode Dev Containers albo lokalne IDE + testy manualne).
- Wersję "papierową" da się zrobić w Notion / Google Docs jako rozmowę techniczną lub warsztat.

---

Jeśli chcesz, mogę pomóc Ci przygotować konkretny przykład takiego testu — np. mini case study z kodem lub scenariusz do analizy. Chciałbyś coś w tym stylu?