# Nauka React z hookami

**Data:** 2025-09-25

---

**User:**

Chcę nauczyć się podstaw React. Narzędzie AI napisało mi żebym nauczył się z aktualnego kursu a nie starego. "Unikaj starych tutoriali opartych o komponenty klasowe – skup się wyłącznie na hakach." Czy to prawda?

---

**Assistant:**

Tak, to prawda – ale z małym zastrzeżeniem.  

W React od wersji **16.8 (2019)** wprowadzono **hooki (hooks)** i od tego momentu nowoczesny sposób pisania komponentów to **funkcje + hooki**, a nie **klasy**.  
Większość aktualnych bibliotek, kursów i dokumentacji zakłada użycie hooków (`useState`, `useEffect`, `useContext`, itp.), a nie klas.  

Dlatego:
- **Ucząc się Reacta od zera** – zdecydowanie lepiej skupić się na hookach i komponencie funkcyjnym, bo to jest *teraźniejszość i przyszłość* Reacta.  
- **Klasy** nadal istnieją w kodzie wielu starszych projektów i warto wiedzieć, że są, ale **nie trzeba się ich uczyć na początku**. Możesz je poznać później, jeśli trafisz do projektu, który ich używa.  

Podsumowując:  
👉 Do nauki Reacta wybieraj materiały, które pokazują **komponenty funkcyjne + hooki**.  
👉 Klasy traktuj jako ciekawostkę lub wiedzę uzupełniającą – na start nie są potrzebne.  

Chcesz żebym przygotował Ci mini-ścieżkę nauki React (od podstaw do pierwszej małej aplikacji) w oparciu o hooki?

---

**User:**

czy taka agenta kursu spełnia ten pożądany warunek?
React Introduction
00:06:02 | Setup & Installation
00:08:08 | React Template Walkthrough
00:13:31 | JSX
00:16:22 | Components
00:19:56 | Movie Card Component
00:29:15 | Conditional Rendering
00:32:43 | Home Page & .map()
00:40:00 | State
00:48:11 | Page Routing
00:56:41 | CSS Styling
01:01:00 | Calling APIS
01:07:25 | useEffect
01:16:54 | Searching for Movies
01:20:14 | Contexts

---

**Assistant:**

Tak, ta agenda wygląda na nowoczesną i spełnia warunek „uczyć się na hookach, nie na klasach”.  

Dlaczego:  
- **State** – w kursach opartych na klasach zwykle byłoby `this.state` i `this.setState`. Tutaj prawie na pewno używane jest `useState`.  
- **useEffect** – to typowy hook do efektów ubocznych, czyli zdecydowanie nowoczesne podejście.  
- **Contexts** – też w formie hooków (`useContext`).  
- Brak punktów typu „class components”, „lifecycle methods” (`componentDidMount`, `componentWillUnmount` itd.), co sugeruje, że autor uczy od razu nowego stylu.  

Czyli możesz spokojnie przerobić ten kurs – to jest właśnie to, czego chcesz się nauczyć.  

Chcesz żebym Ci wskazał, na co szczególnie zwracać uwagę w trakcie tego kursu, żeby faktycznie utrwalić nowoczesne podejście?