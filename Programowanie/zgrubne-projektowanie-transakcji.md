# Zgrubne projektowanie transakcji

**Data:** 2025-01-14

---

**User:**

Jesteś na job interview na stanowisko senior java developer.
Zostałeś zapytany o zgrubne zaprojektowanie systemu transakcji rozproszonych. 

---

**Assistant:**

Projektowanie systemu transakcji rozproszonych jest wyzwaniem, które wymaga uwzględnienia takich aspektów jak integralność danych, odporność na błędy i wydajność. Oto zarys, jak można podejść do tego problemu:

---

### 1. **Zrozumienie wymagań**
Najpierw trzeba zrozumieć wymagania biznesowe i techniczne:
- **Cechy transakcji:** ACID (Atomicity, Consistency, Isolation, Durability) czy BASE (Basic Availability, Soft state, Eventual consistency)?
- **Rozproszony charakter:** Ilu uczestników będzie w systemie? Jakie operacje muszą być zsynchronizowane?
- **Odporność na błędy:** Czy system musi obsługiwać scenariusze awarii sieci, serwerów lub komponentów?

---

### 2. **Wybór wzorca**
Dwa główne wzorce transakcji rozproszonych:
1. **Dwufazowy commit (2PC):**
   - Pierwsza faza: Uczestnicy przygotowują transakcję i zgłaszają gotowość.
   - Druga faza: Koordynator decyduje o zatwierdzeniu lub odrzuceniu transakcji.
   - **Zalety:** Silna spójność.
   - **Wady:** Może blokować uczestników i jest mniej odporny na awarie.

2. **Sagi:**
   - Sekwencja lokalnych transakcji, gdzie każda ma operację kompensującą.
   - **Zalety:** Wysoka skalowalność i elastyczność.
   - **Wady:** Trudniejsze zarządzanie spójnością i ryzyko długotrwałych transakcji.

---

### 3. **Komponenty systemu**
- **Koordynator transakcji:**
  Zarządza cyklem życia transakcji, np. poprzez 2PC lub Sagi.
- **Uczestnicy transakcji:**
  Komponenty (bazy danych, usługi), które wykonują lokalne operacje.
- **Mechanizmy komunikacji:**
  Message broker (np. Kafka, RabbitMQ) do wymiany komunikatów.
- **Logger:**
  Mechanizm do śledzenia stanu transakcji (np. dziennik w przypadku odtwarzania stanu po awarii).

---

### 4. **Obsługa awarii**
- **Retry logic:** Uczestnicy muszą być w stanie powtórzyć operacje.
- **Idempotencja:** Operacje muszą być odporne na wielokrotne wykonanie.
- **Timeouts i deadlocki:** Należy unikać nieskończonych blokad.

---

### 5. **Technologie**
- **Baza danych:** Może być relacyjna (PostgreSQL) lub nierelacyjna (Cassandra) w zależności od wymagań.
- **Frameworki:** Spring Boot + Spring Transaction Management dla 2PC, Axon Framework lub orchestratory dla Sag.
- **Integracja:** Narzędzia takie jak gRPC lub REST dla komunikacji.

---

### Przykład
Załóżmy, że projektujemy system rezerwacji podróży:
1. **Usługi:** Rezerwacja lotu, hotelu i samochodu.
2. **Wzorzec:** Używamy Sag, gdzie każda usługa ma operację kompensującą (np. anulowanie rezerwacji).
3. **Koordynacja:** Dedykowany koordynator wywołuje operacje sekwencyjnie i monitoruje ich status.

---

### Wyzwania i optymalizacje
- **Sieciowość:** Minimalizacja opóźnień.
- **Spójność vs dostępność:** Zbalansowanie w zależności od wymagań.
- **Monitoring i alerty:** Narzędzia takie jak Prometheus lub Elastic Stack.

---

Czy chcesz, żebym omówił konkretny aspekt bardziej szczegółowo?