# Pamięć długoterminowa AI

**Data:** 2024-12-24

---

**User:**

Jestem programistą więc możesz do mnie mówić w bardziej złożony sposób.
Chciałbym stworzyć swojego asystenta AI. Jest to duży projekt ale zaczniemy od od wybranych funkcji i konceptów projektowych.
Zakładam że będę używał LLM działających lokalnie na komputerze np. Ollama.
Pierwsze co chciałbym ustalić to sposób zapewnienia pamięci długoterminowej dla agenta. Chcę mieć możliwość wczytania do pamięci długoterminowej przeczytanych przeze mnie książek a później móc rozmawiać z asystentem na ich temat. W jaki sposób mogę zapewnić taką pamięć długoterminową? Jakich technologii mogę użyć?

---

**Assistant:**

Użytkownik jest programistą i chce stworzyć swojego asystenta AI. Planuje korzystać z LLM działających lokalnie, takich jak Ollama. Chce, aby asystent miał pamięć długoterminową umożliwiającą wczytywanie treści, np. przeczytanych książek, i późniejszą rozmowę na ich temat.

---

**Assistant:**

Aby zaimplementować pamięć długoterminową dla agenta AI, możesz użyć następujących technologii i podejść:

### 1. **Baza danych dla pamięci długoterminowej**
   - **Relacyjne bazy danych**: Możesz użyć PostgreSQL lub SQLite, aby przechowywać informacje w uporządkowany sposób.
   - **NoSQL**: MongoDB lub Elasticsearch pozwolą na łatwe indeksowanie i wyszukiwanie dużych ilości tekstu.
   - **Vektoryzacja i wyszukiwanie podobieństwa**:
     - Wykorzystaj narzędzia takie jak Pinecone, Weaviate, czy Qdrant do przechowywania reprezentacji wektorowych tekstów.
     - Użyj biblioteki FAISS (Facebook AI Similarity Search) do lokalnego wyszukiwania podobieństwa.

### 2. **Vektoryzacja treści**
   - Aby móc porównywać i wyszukiwać fragmenty tekstu, przekształcaj tekst w wektory za pomocą modeli językowych takich jak Sentence Transformers, OpenAI Embeddings, czy LLaMA.
   - Możesz lokalnie trenować lub korzystać z gotowych modeli.

### 3. **Struktura pamięci długoterminowej**
   - **Podział treści**:
     - Podziel książki na małe fragmenty (np. akapity, strony).
     - W każdym fragmencie zachowaj metadane (np. tytuł książki, numer strony, temat).
   - **Wyszukiwanie kontekstowe**:
     - Gdy użytkownik zada pytanie, wyszukaj najbardziej podobne fragmenty w pamięci za pomocą wyszukiwania wektorowego.
     - Przekaż te fragmenty do lokalnego LLM jako kontekst do odpowiedzi.

### 4. **Interfejs użytkownika i interakcja**
   - **Wczytywanie książek**:
     - Wczytuj książki w formatach takich jak PDF, EPUB, czy TXT.
     - Przetwarzaj tekst, usuwając zbędne elementy (np. stopki, numery stron).
   - **API do komunikacji z bazą danych**:
     - Stwórz API, które pozwoli asystentowi szybko wyszukiwać fragmenty tekstu w bazie danych.

### 5. **Technologie**
   - **Do ekstrakcji tekstu z książek**:
     - Tesseract (OCR) dla skanów książek.
     - PyPDF2, pdfplumber dla plików PDF.
   - **Do obróbki tekstu i tokenizacji**:
     - NLTK, SpaCy lub Hugging Face Transformers.
   - **Integracja z lokalnym LLM**:
     - Ollama lub inne lokalne instancje modeli językowych.

### 6. **Dodatkowe funkcje**
   - **Uczenie się z treści**:
     - Możesz zaimplementować system podsumowywania treści przy użyciu lokalnych modeli językowych.
   - **Kategoryzacja i notatki**:
     - Dodaj funkcję organizowania fragmentów według tematów czy tagów.

Czy chciałbyś zacząć od skonfigurowania konkretnego narzędzia, np. FAISS do wyszukiwania wektorowego, czy od innego elementu?

---

**User:**

Załóżmy że będę chciał skorzystać z bazy wektorowej Qdrant. Czy obo przechowywania treści w formie embedingów w bazie wektorowej istnieje potrzeba przechowywania treści w wersji oryginalnej w bazie SQL/noSQL?

---

**Assistant:**

Użycie bazy SQL/NoSQL do przechowywania treści w wersji oryginalnej jest opcjonalne, ale może być korzystne w zależności od wymagań projektu. Oto kluczowe aspekty, które warto rozważyć:

---

### **Korzyści przechowywania treści w wersji oryginalnej:**

1. **Łatwy dostęp do pełnego tekstu:**
   - Jeśli użytkownik chce uzyskać pełny fragment tekstu jako odpowiedź, możesz pobrać go bezpośrednio z bazy SQL/NoSQL. 
   - Ułatwia to integrację, jeśli bazy wektorowe nie obsługują dobrze przechowywania dużych tekstów (co może być ograniczeniem w przypadku Qdrant).

2. **Lepsze zarządzanie danymi:**
   - Trzymanie danych w SQL/NoSQL pozwala na dodatkowe operacje, takie jak filtrowanie, grupowanie lub sortowanie, które mogą być trudniejsze do wykonania w bazie wektorowej.

3. **Metadane i powiązania:**
   - SQL/NoSQL ułatwia przechowywanie i zarządzanie metadanymi (np. tytuł, autor, numer strony, rozdział).
   - Możesz łatwo łączyć różne źródła informacji i tworzyć bardziej złożone zapytania.

4. **Backup i bezpieczeństwo:**
   - Przechowywanie treści w klasycznej bazie może być bezpieczniejsze w przypadku uszkodzenia danych w bazie wektorowej.

5. **Wersjonowanie:**
   - Możesz zarządzać wersjami tekstów, co może być przydatne w przypadku edycji lub aktualizacji treści.

---

### **Przechowywanie tylko embeddingów w Qdrant:**

Jeśli zdecydujesz się przechowywać wyłącznie embeddingi w Qdrant:
1. **Lekkość i prostota:**
   - Rozwiązanie jest prostsze w implementacji i wymaga mniej zasobów.
2. **Wystarczające dla większości przypadków użycia:**
   - Embeddingi pozwalają na wyszukiwanie podobnych treści, a oryginalny tekst można przechowywać w Qdrant jako część dokumentu (np. w polu `payload`).

---

### **Rekomendacja:**

1. **Przechowywanie obu form:**
   - Embeddingi w Qdrant dla szybkiego wyszukiwania.
   - Oryginalna treść w SQL/NoSQL dla łatwego dostępu, archiwizacji i zarządzania.

2. **Alternatywa z samym Qdrant:**
   - Możesz przechowywać embeddingi i oryginalne teksty w jednym rekordzie w Qdrant, korzystając z pola `payload`:
     ```json
     {
       "id": "123",
       "vector": [0.123, 0.456, ...],
       "payload": {
         "text": "Pełny tekst fragmentu",
         "title": "Tytuł książki",
         "author": "Autor"
       }
     }
     ```
   - To pozwala na zachowanie prostoty, ale ogranicza elastyczność w przypadku bardziej złożonych operacji.

---

Podsumowując, wybór zależy od Twoich potrzeb:
- Jeśli priorytetem jest prostota, użyj tylko Qdrant.
- Jeśli zależy Ci na wszechstronności i łatwości zarządzania, rozważ kombinację Qdrant (embeddingi) i SQL/NoSQL (pełne teksty i metadane).

---

**User:**

Popraw mnie w moim rozumowaniu jeśli się mylę.
Zakładam że podzielę treści książek na strony. Na przykładowej stronie może znaleźć się ok trzy interesujące informacje. Powiedzmy że strona zawiera informacje na temat miejsca żerowań krokodyla australijskiego oraz jego zwyczajów godowych. Gdy do bazy wektorowej zostanie wysłane zapytanie dotyczące "niebezpiecznych zwierząt w Australii" to czy baza zwróci mi akurat stronę o krokodylu?

---

**Assistant:**

Twoje rozumowanie jest poprawne, ale wymaga kilku doprecyzowań, aby dobrze zrozumieć mechanizmy wyszukiwania w bazie wektorowej. Oto szczegóły, jak działa proces i dlaczego baza powinna zwrócić odpowiednią stronę:

---

### **1. Mechanizm działania wyszukiwania wektorowego**
- Baza wektorowa, taka jak Qdrant, działa na zasadzie porównywania **embeddingów** – matematycznych reprezentacji semantycznych treści.
- Gdy dzielisz książki na strony i tworzysz embedding dla każdej strony, embedding reprezentuje całą zawartość tej strony w sposób uwzględniający semantyczne znaczenie.

---

### **2. Czy baza zwróci stronę o krokodylu?**
- Jeśli strona zawiera informacje o żerowaniu i zwyczajach godowych krokodyla australijskiego, embedding tej strony będzie zawierał semantyczne wskazówki, że strona dotyczy krokodyli i Australii. 
- Gdy użytkownik zada pytanie o "niebezpieczne zwierzęta w Australii", pytanie zostanie również przekonwertowane na embedding. 
- Baza znajdzie embeddingi najbardziej podobne do zapytania i zwróci odpowiednią stronę, **jeśli** w treści strony faktycznie jest mowa o krokodylach jako niebezpiecznych zwierzętach.

---

### **3. Co może wpłynąć na wynik?**

#### **Podział treści na strony**
- **Granularność podziału ma znaczenie**:
  - Jeśli strona zawiera zarówno informacje o krokodylach, jak i inne mniej związane z pytaniem treści (np. o lokalnym krajobrazie), embedding może być mniej precyzyjny.
  - Lepszym podejściem może być podział na mniejsze fragmenty, np. akapity, z zachowaniem metadanych o ich położeniu (strona, rozdział).

#### **Jakość embeddingów**
- Modele embeddingów powinny być wystarczająco zaawansowane, aby dobrze rozumieć semantyczne związki między pytaniem a treścią (np. Sentence Transformers lub podobne modele fine-tunowane na Twoich danych).

#### **Kontekst pytania**
- Pytanie "niebezpieczne zwierzęta w Australii" może być zbyt ogólne. Jeśli baza nie ma wyraźnych wskazówek w embeddingach, że krokodyl jest niebezpieczny, wynik może nie być trafny.

---

### **4. Jak zwiększyć precyzję wyszukiwania?**
1. **Mniejsze fragmenty**:
   - Zamiast całych stron używaj akapitów lub zdań jako jednostek indeksowanych. To zmniejsza "rozmycie" kontekstu w embeddingu.

2. **Zachowanie metadanych**:
   - Dodaj do każdego rekordu metadane opisujące treść (np. słowa kluczowe, kategorie tematyczne). W przypadku zapytań możesz dodatkowo filtrować wyniki według tych metadanych.

3. **Połączenie wyszukiwania semantycznego i klasycznego**:
   - Najpierw znajdź najbardziej podobne embeddingi w bazie wektorowej, a następnie użyj klasycznego wyszukiwania (np. słów kluczowych) do doprecyzowania wyników.

4. **Fine-tuning modelu embeddingów**:
   - Jeśli zależy Ci na maksymalnej precyzji, warto przeprowadzić fine-tuning modelu embeddingów na Twoich danych, aby lepiej rozumiał specyficzne relacje między tekstami.

---

### **Podsumowanie**
Przy odpowiednim podziale tekstu i zastosowaniu dobrych embeddingów, baza wektorowa powinna zwrócić stronę o krokodylu na zapytanie "niebezpieczne zwierzęta w Australii". Jednak precyzja będzie zależeć od:
1. Jakości podziału na fragmenty.
2. Użytego modelu embeddingów.
3. Dodatkowych mechanizmów filtrowania i wzbogacania kontekstu.

Czy chcesz, abym zaproponował konkretne podejście do podziału treści i wyboru modeli embeddingów?

---

**User:**

OK a czy problemem będzie gdy po takim zapytaniu baza wektorowa zwróci bardzo wiele fragmentów książek? Rozumiem że to może być problem bo to co zwróci baza wektorowa jest ładowane do kontekstu modelu? A może się mylę?

---

**Assistant:**

Masz rację, zbyt wiele zwróconych fragmentów może stanowić problem, zwłaszcza jeśli zamierzasz przekazać je wszystkie do kontekstu modelu. Modele językowe, takie jak LLaMA czy inne lokalne LLM, mają ograniczenie długości kontekstu (np. 2048, 4096 tokenów lub więcej w nowszych modelach). Zbyt duża liczba fragmentów może spowodować, że przekroczysz ten limit, co wpłynie na skuteczność modelu. 

---

### **1. Dlaczego zbyt wiele fragmentów jest problemem?**
- **Ograniczenia kontekstu**: Jeśli załadujesz za dużo tekstu, fragmenty mogą zostać obcięte, a model może nie mieć dostępu do kluczowych informacji.
- **Szum informacyjny**: Wprowadzenie zbyt wielu nieistotnych fragmentów może sprawić, że model "zgubi się" i nie będzie w stanie odpowiedzieć precyzyjnie na pytanie.

---

### **2. Jak ograniczyć liczbę zwracanych fragmentów?**

#### **a) Priorytetyzacja wyników**
- **Sortowanie po trafności**:
  - Qdrant zwraca wyniki posortowane według podobieństwa embeddingów. Możesz ustalić próg trafności (np. minimalny `score`), aby odrzucić mniej istotne wyniki.
- **Limit wyników**:
  - W zapytaniu do bazy ustaw limit, np. 5–10 najlepszych fragmentów.

#### **b) Grupowanie wyników**
- **Grupowanie tematyczne**:
  - Możesz grupować wyniki według tematu, aby ograniczyć liczbę fragmentów przekazywanych do modelu.
  - Przykład: Jeśli baza zwraca wiele fragmentów o krokodylach i wężach, wybierz tylko kilka z każdego tematu.

#### **c) Podsumowanie lub agregacja wyników**
- **Podsumowanie tekstów przed przekazaniem do modelu**:
  - Po otrzymaniu fragmentów możesz je automatycznie podsumować, aby zmniejszyć ilość tekstu.
  - Przykład: Użyj modelu do wygenerowania krótkiego podsumowania 5–10 fragmentów, a następnie załaduj tylko podsumowanie do kontekstu.

---

### **3. Jak efektywnie zarządzać kontekstem modelu?**

#### **a) Wybór najbardziej istotnych fragmentów**
- Zastosuj dodatkowe filtry w wynikach z bazy wektorowej, np. wybierając fragmenty najbardziej dopasowane tematycznie do pytania.

#### **b) Dynamiczne zarządzanie kontekstem**
- **Kontekst hierarchiczny**:
  - Jeśli pytanie wymaga bardziej ogólnej odpowiedzi, najpierw przekaż podsumowanie najtrafniejszych fragmentów.
  - W przypadku bardziej szczegółowego pytania możesz przeprowadzić kolejne zapytanie do bazy, aby pogłębić kontekst.

#### **c) Okno przesuwne (sliding window)**
- Podziel tekst na małe fragmenty, które mieszczą się w limicie kontekstu, i przekaż je do modelu w partiach, łącząc wyniki.

---

### **4. Przykładowe podejście: Workflow**
1. **Zapytanie do bazy wektorowej**:
   - Wyślij zapytanie i pobierz np. 10 najbardziej trafnych fragmentów.
   
2. **Filtrowanie wyników**:
   - Usuń fragmenty o niskiej trafności.
   - Ewentualnie zgrupuj wyniki według tematów.

3. **Przetwarzanie wyników**:
   - Wygeneruj podsumowanie, jeśli tekst jest zbyt długi.
   - Przeanalizuj kluczowe fragmenty i wybierz najbardziej istotne.

4. **Przekazanie do modelu**:
   - Przekaż ograniczoną liczbę fragmentów jako kontekst.

---

### **5. Czy to zawsze problem?**
Jeśli baza zwraca dużo wyników, ale są one dobrze posortowane pod względem trafności, wystarczy wybrać tylko te najbardziej istotne. Przy odpowiednim ograniczeniu liczby fragmentów nie powinno to stanowić dużego problemu.

Chcesz, żebym opracował przykładowy kod lub pseudokod dla tego workflow?