# Propozycje technologii frontendowej

**Data:** 2025-07-25

---

**User:**

Chcę zrobić małą aplikację którą wdroże na moim RaspberryPi. 
Aplikacja składa się z części backend i bardzo prostej frontend.

Backend: bardzo prosta aplikacja w Rust która wywołuje deepl API. 
To dokumentacja do tego API.
https://developers.deepl.com/api-reference/document
Wywołania w dwóch trybach: Translate text oraz Improve text.

Frontend: źródłem danych wejściowych dla backendu jest frontend. Składa się z jednej strony na których są dwa pola tekstowy (pierwsze podpisane Translate text, drugie Improve text)
Pod każdym polem jest miejsce na której wyświetla się rezyltat zapytania API z backendu.

Nie wiem jakiej technologii tutaj użyć. Do backendu chcę użyć Rust bo chcę się uczyć tej technologii. Zaproponuj technologię dla frontendu. 

---

**Assistant:**

Oto propozycje technologii frontendowej dobrze współgrającej z backendem w Rust uruchamianym na Raspberry Pi (bardzo prostym API do DeepL):

---

## 🔧 1. Frontend w Rust + WebAssembly (np. Yew, Dioxus, Seed)

### **Yew**  
- Popularny frontendowy framework w Rust, kompilowany do WebAssembly, oparty na podejściu podobnym do React (komponenty, stan, hooki) citeturn0search13turn0search12.  
- Nada się do napisania dwóch pól tekstowych forms i wyświetlania wyniku poacyk API.  
- Dostajesz pełne bezpieczeństwo typów i brak „każania się” JavaScriptem — całość w jednym języku.

### **Dioxus / Seed**  
- **Dioxus**: pełen stos (web i desktop) – można użyć go jako SPA dla prostego UI w Rust citeturn0search10turn0search11.  
- **Seed**: lekki Elm-like framework, szybki, minimalistyczny citeturn0search12turn0search11.

**Zalety**: całość w Rust, jedna baza kodu.  
**Wady**: wymaga kompilacji do WASM, trochę konfiguracji (wasm-pack lub trunk).

---

## 🌐 2. Frontend w HTML/CSS/JS + prosty JavaScript (clean, minimal)

- Napisać statyczny plik HTML z dwoma `textarea` i JavaScriptem, który robi fetch do endpointów backendu.  
- Przykład minimalistyczny, działa na każdej przeglądarce, nie wymaga dużych narzędzi.  
- Backend w Rust może służyć statyczny plik oraz obsługiwać `/translate` i `/improve` endpoints.

**Zalety**: bardzo szybki setup, minimalne wymagania.  
**Wady**: mniej struktur i typów, bardziej ręczne zarządzanie stanem.

---

## ⚙️ 3. WebView / desktop jako UI (WebUI, Tauri) – opcjonalnie

- **WebUI** – Rustowa biblioteka uruchamiająca lokalną przeglądarkę jako GUI, niskie zasoby citeturn0search3  
- **Tauri** – używa HTML/CSS/JS jako UI w WebView, z backendem w Rust — działa też na Raspberry Pi (ARM64) po cross-kompilacji citeturn0search6turn0search24.

To bardziej do app desktopowej, ale jeśli podłączysz wyświetlacz do Raspberry Pi – to realna opcja.

---

## ✅ Podsumowanie rekomendacji

| Option | Kod w Rust? | Prosty setup? | Zasoby | Rekomendacja |
|--------|-------------|----------------|--------|--------------|
| **Yew / Dioxus / Seed** | ✅ | umiarkowany | średnie | idealne jeśli chcesz frontend w Rust |
| **Klasyczny JS (HTML + fetch)** | ❌ | bardzo prosty | minimalne | najlepszy kompromis prostoty i funkcjonalności |
| **Tauri / WebUI** | ✅ | bardziej skomplikowany (cross-kompilacja) | średnie | użyteczne jeśli chcesz lokalne GUI na Pi z ekranem |

---

### 🛠️ Przykładowy workflow

1. **Backend**: aplikacja w Rust (np. z użyciem Actix‑Web, Rocket lub Axum), która obsługuje HTTP POSTy pod `/translate` i `/improve`, wykonując wywołania DeepL API (w oparciu o dokumentację oficialną) citeturn0search15turn0search9.  
2. **Frontend**:  
   - W Yew: komponent z dwoma `textarea`, po submicie `fetch("/translate", …)` i pokazanie odpowiedzi JSON.  
   - W klasycznym JS: prosty `index.html + main.js`, fetch do backendu, wynik w `div`.  
3. **Deploy**: skompiluj backend dla ARM (albo cross‑compile), wrzuć na Raspberry Pi i uruchom jako serwer HTTP. Podaj adres IP Pi lub `localhost`.

---

Jeśli chcesz kontynuować, mogę pomóc:
- z przykładowym kodem w Yew lub Seed,
- prostym HTML/JS front-endem,
- lub z konfiguracją cross-kompilacji i deploymentem (np. przy Tauri/WebUI).

Daj znać, co Ci bardziej odpowiada i chcesz zobaczyć dalej.

---

**User:**

który z tych frameworków Yew / Dioxus / Seed jest najczęściej używany komercyjnie?

---

**Assistant:**

Jeśli chodzi o **komercyjne wykorzystanie** spośród frameworków Rust‑WASM (Yew, Dioxus, Seed) — najczęściej spotykanym w realnych projektach (szczególnie produkcyjnych, wewnętrznych lub start‑upowych) jest **Yew**.

---

## 📌 Główne wnioski:

### 🔹 **Yew**
- Najdłużej istniejący i **najbardziej dojrzały** framework do frontendu w Rust, wzorowany na React, z komponentową architekturą i bogatym ekosystemem narzędzi (Trunk, wasm-pack itd.) citeturn0search1turn0search3turn0search9.
- Według statystyk branżowych Yew jest **ok. 1,1× bardziej popularny niż Dioxus** pod względem liczby stron korzystających z tego frameworka citeturn0search0.
- Programiści na Reddit często wskazują, że Yew to pierwsze narzędzie do rozważenia, **najbardziej zbliżone do produkcyjnych wymagań**, używane w rzeczywistych aplikacjach – np. wewnętrznych dashboardach firmowych, aplikacjach jak Uber‑like itp. citeturn0reddit21turn0reddit13.

### 🔹 **Dioxus**
- Rozwijany jako **bardziej dewelopersko przyjazny (DX)** framework, wspiera wiele platform: web, desktop (Tauri), mobile i więcej citeturn0search4turn0search1turn0search5.
- Ma szybko rosnące zainteresowanie oraz aktywną społeczność, lecz wciąż **nieco mniej szeroko używany komercyjnie niż Yew** citeturn0search0turn0search4.

### 🔹 **Seed**
- Bardziej **lekki, Elm‑style framework**, używany przez freelancerów i małe projekty, z relatywnie mniejszym ekosystemem niż Yew i Dioxus citeturn0search10turn0search7.
- Mniejsza społeczność i ograniczone ślady zastosowań komercyjnych citeturn0search10turn0reddit13turn0search7.

---

## Podsumowanie:

| Framework | Dojrzałość ●●●●● | Popularność komercyjna | Użycie w projektach real low-level |
|-----------|------------------|-------------------------|------------------------------------|
| **Yew**   | ⭐⭐⭐⭐⭐          | Największa              | Tak, istnieją realne wdrożenia     |
| **Dioxus**| ⭐⭐⭐⭐☆          | Rosnąca szybko, mniej niż Yew | Coraz więcej eksperymentów         |
| **Seed**  | ⭐⭐⭐☆☆          | Najmniej komercyjna     | Przeważnie hobbystyczne projekty   |

---

### ✅ Wniosek:
Jeśli Twoim celem jest **najbardziej sprawdzona i szeroko stosowana (również komercyjnie) opcja**, to **Yew** jest obecnie najczęściej używanym wyborem w firmach.  
Dioxus to świetna alternatywa, szczególnie gdy zależy Ci na lepszej ergonomii deweloperskiej i wsparciu wielu platform. Seed natomiast sprawdzi się w małych, prostych projektach, ale ma mniejszy zasięg w środowisku komercyjnym.

---

Jeśli chcesz, mogę przygotować przykładowy kod frontendu w Yew (dwa textarea + fetch do API). Daj znać.

---

**User:**

Napisz po angielsku polecenie wykonania takiego projektu dla narzędzia AI. Backend w Rust, frontend w Yew.

---

**Assistant:**

Here’s an example prompt you can give to an AI code‑generation tool to spin up your project (Rust backend calling DeepL API, and Yew frontend):

---

**AI tool prompt (in English):**

```
Create a full‑stack project in Rust with the following structure:
- A backend Rust service using a web framework of your choice (e.g. Actix Web or Axum), exposing two HTTP endpoints:
    • POST /translate — accepts JSON with “text” and optional target language, calls DeepL API Translate endpoint
    • POST /improve — accepts JSON with “text”, uses DeepL Improve (edit) API
  Backend should forward the request, parse DeepL response, and return JSON result.

- A frontend SPA written in Rust using Yew + WebAssembly:
    • Display a page with two labeled textareas ("Translate text" and "Improve text")
    • Below each textarea show a button that triggers a fetch() call to the corresponding backend endpoint
    • Display the translated or improved text response beneath each field in a result area

- Use Trunk or wasm-pack for building and serving the Yew frontend.

- Optionally bundle into a Rust workspace (“common”, “backend”, “frontend”) so they compile together.

Generate project files (Cargo.toml, Rust source, index.html, frontend code) with minimal additional UI; focus on functionality and API integration.

Also include instructions to compile backend for Raspberry Pi (ARM target) and run locally, plus how to serve static frontend files via the backend or separate serve command.

```

---

This prompt is inspired by real‑world tutorials for combining Yew frontends with Rust backends (so you get the right structure and tooling) citeturn0search2turn0search8turn0search4turn0search16.

Would you like me to refine it further, or generate actual sample code from this?

---

**User:**

Actix Web or Axum - which one is more popular?

---

**Assistant:**

Here’s a refined answer based on recent web data:

---

## 🔍 Popularity: Actix Web vs. Axum

### **Actix Web**
- Historically the most **popular and mature** Rust web framework, renowned for performance, rich ecosystem, and proven use in production environments citeturn0search5turn0search2.
- Preferred for performance-sensitive, enterprise-grade services and has substantial documentation and extensions citeturn0search5turn0search4.

### **Axum**
- Rapidly gaining adoption thanks to its **clean API**, deep integration into the **Tokio + Hyper + Tower ecosystem**, and strong developer experience citeturn0search0turn0search2turn0search3.
- Widely recommended by developers seeking maintainability, modular middleware, and safer long‑term support from the Tokio team citeturn0reddit8turn0reddit13turn0reddit6.

---

## 👥 Community & Usage Insights (from Reddit)

- A top community post estimates **Axum has around 29 million monthly downloads vs ~16 million for Actix-web**, though some of Axum’s figure is driven indirectly by its use in other tools like gRPC libraries citeturn0reddit6.
- Many users report preferring Axum for **ease of use, better documentation, and simpler middleware support**, especially for new projects citeturn0reddit8turn0reddit13turn0reddit7.
- Others still rely on Actix for its **high performance and long track record in production**, especially in larger, performance-critical systems citeturn0reddit7turn0reddit16.

---

## 📊 Summary

| Framework    | Ecosystem & Integration       | Performance       | Developer Experience     | Popularity in Production     |
|--------------|-------------------------------|-------------------|---------------------------|------------------------------|
| **Actix Web**| Own ecosystem; less tied to Tokio/Tower | Often top-performer | Mature but more boilerplate | Longstanding, widely used     |
| **Axum**     | Full Tokio/Hyper/Tower support | Very fast, near Actix | Ergonomic, modular, macro-free | Rapidly growing, now dominant|

---

## ✅ Final Takeaway

- **Historically**, **Actix Web** has been the safest, most battle-tested choice in production—especially where raw performance matters.
- **Currently**, **Axum** is often considered the **more popular and modern choice**, offering superior developer ergonomics, growing community, and stronger alignment with the broader Tokio ecosystem.
- In 2025, many in the community consider **Axum the go-to default** for new Rust web APIs, while Actix still holds strong for performance-critical or existing systems citeturn0reddit6turn0reddit7turn0reddit13turn0reddit8.

---

Would you like help scaffolding an Axum-based backend or comparing sample code for Actix vs Axum?