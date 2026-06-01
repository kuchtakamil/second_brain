# Kiedy stosować bazy SQL a kiedy NoSQL? (Kryteria wyboru)

## Krótkie podsumowanie
Wybór między relacyjną bazą danych (SQL) a nierelacyjną (NoSQL) to jedna z najważniejszych decyzji architektonicznych w projektowaniu systemów (System Design). Bazy SQL (np. PostgreSQL, MySQL) opierają się na ustrukturyzowanych tabelach i relacjach, gwarantując spójność (ACID). Bazy NoSQL (np. MongoDB, Cassandra, Redis) oferują elastyczne modele danych (dokumenty, klucz-wartość, grafy, szerokie kolumny) i często stawiają na dostępność oraz partycjonowanie poziome (zgodnie z twierdzeniem CAP).

## Dlaczego to ma znaczenie / Kiedy to stosować?
Nieodpowiedni dobór bazy danych może prowadzić do problemów z wydajnością, trudności w skalowaniu oraz niepotrzebnych kosztów. Wymagania biznesowe, struktura danych oraz oczekiwany ruch (odczyty vs zapisy) determinują, który rodzaj bazy sprawdzi się najlepiej. Zrozumienie kryteriów wyboru pozwala zaprojektować system, który jest elastyczny i przygotowany na określony rodzaj obciążenia.

## Główne kryteria wyboru

### 1. Struktura danych i Schemat
*   **SQL:** Wybierz, gdy dane są wysoce ustrukturyzowane, a relacje między encjami są dobrze zdefiniowane i rzadko się zmieniają. Zmiana schematu (migracje) w ogromnych bazach SQL może być uciążliwa i spowalniać wprowadzanie nowych funkcji.
*   **NoSQL:** Wybierz, gdy struktura danych jest dynamiczna, szybko ewoluuje lub gdy dane są półustrukturyzowane/nieustrukturyzowane (np. logi, JSON, dane IoT, katalogi z różnorodnymi atrybutami). Brak narzuconego schematu (schema-less) pozwala na dużą elastyczność i przyspiesza development.

### 2. Skalowalność
*   **SQL (Skalowanie pionowe):** Bazy relacyjne tradycyjnie skaluje się w górę (Scale-up) — kupując lepszy serwer (więcej RAM/CPU/Dysku). Rozproszenie bazy SQL (sharding) na wiele serwerów (skalowanie poziome) jest możliwe, ale złożone architektonicznie i często pozbawia nas zalet takich jak swobodne używanie `JOIN`.
*   **NoSQL (Skalowanie poziome):** Powstały z myślą o architekturze rozproszonej (Scale-out). Pozwalają łatwo dokładać kolejne, tańsze węzły do klastra, co czyni je idealnymi przy ciągłym, nieprzerwanym przyroście danych (Big Data) i gigantycznym ruchu.

### 3. Właściwości ACID vs BASE (Spójność vs Dostępność)
*   **SQL:** Zapewnia pełną gwarancję ACID (Atomicity, Consistency, Isolation, Durability). Gwarantuje to, że po zatwierdzeniu transakcji (commit), dane są od razu spójne i weryfikowalne. Kluczowe dla systemów finansowych, ERP, księgowości, i tam gdzie nie możemy sobie pozwolić na utratę danych czy błędy w kalkulacjach.
*   **NoSQL:** Często opiera się na modelu BASE (Basically Available, Soft state, Eventual consistency). Używamy, gdy możemy zaakceptować tzw. "ostateczną spójność" (eventual consistency) – w zamian za to zyskujemy wysoką dostępność i mniejsze opóźnienia. Idealne tam, gdzie małe opóźnienie wyświetlania powiadomień lub lajków jest ważniejsze niż natychmiastowa globalna spójność.

### 4. Zapytania i Sposób dostępu do danych (Querying)
*   **SQL:** Posiada potężny język zapytań (SQL), umożliwiający skomplikowane agregacje, złączenia (`JOIN`) wielu tabel i przeprowadzanie ad-hoc analiz. Najlepsze dla złożonych transakcji biznesowych (OLTP) i generowania raportów.
*   **NoSQL:** Zapytania bywają mocno ograniczone zależą od typu bazy i użytego w niej sposobu wyszukiwania. Często konieczna jest *denormalizacja* danych w fazie zapisu (np. zapisywanie zagnieżdżonego dokumentu z danymi o autorze wewnątrz wpisu na bloga), aby zoptymalizować i maksymalnie przyspieszyć sam odczyt.

## Przykładowe silniki i ich zastosowania

### Bazy SQL
*   **Przykłady:** PostgreSQL, MySQL, Oracle, Microsoft SQL Server.
*   **Kiedy:** Złożone systemy księgowe, aplikacje bankowe, tradycyjne platformy e-commerce, CRM-y, gdzie priorytetem są transakcje wieloobiektowe.

### Bazy NoSQL
*   **Klucz-Wartość (Key-Value):** Redis, DynamoDB. 
    *   **Kiedy:** Superszybkie odczyty (często w pamięci RAM). Caching, zarządzanie sesjami użytkowników, koszyki zakupowe z wysoką rotacją, systemy rankingu (leaderboards).
*   **Dokumentowe (Document):** MongoDB, Couchbase, Firestore. 
    *   **Kiedy:** Przechowywanie danych w formacie JSON. Systemy zarządzania treścią (CMS), katalogi produktów z różnymi atrybutami, personalizacja profili użytkowników.
*   **Szerokokolumnowe (Wide-Column):** Cassandra, HBase, ScyllaDB. 
    *   **Kiedy:** Bardzo szybki zapis ogromnej ilości pomiarów z czujników (IoT), logowanie zdarzeń aplikacji, analityka telemetryczna o dużym natężeniu ruchu.
*   **Grafowe (Graph):** Neo4j, Amazon Neptune.
    *   **Kiedy:** Skupienie na skomplikowanych relacjach węzłów (nodes). Sieci społecznościowe (polecanie znajomych), systemy rekomendacji zakupowych (osoby które kupiły A, kupiły też B), wykrywanie wzorców oszustw bankowych (fraud detection).

## Powiązane pliki
*   [Pytania rekrutacyjne z System Design](system-design-pytania-rekrutacyjne.md)
*   [Pytania rekrutacyjne z Mikroserwisów](mikroserwisy-pytania-rekrutacyjne.md)
