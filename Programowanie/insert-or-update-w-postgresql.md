# Insert or update w PostgreSQL

**Data:** 2025-11-06

---

**User:**

PostgreSQL, w przypadku wywołania INSERT z istniejącym już kluczem głównym, poleci wyjątek. A czy można wywołać coś w stylu INSERT OR UPDATE?

---

**Assistant:**

Tak, w PostgreSQL można to zrobić – służy do tego składnia:  

```sql
INSERT INTO tabela (kolumna1, kolumna2, ...)
VALUES (wartość1, wartość2, ...)
ON CONFLICT (klucz) 
DO UPDATE SET kolumna2 = EXCLUDED.kolumna2, kolumna3 = EXCLUDED.kolumna3;
```

Działa to tak:  
- Jeśli rekord o takim kluczu (np. `PRIMARY KEY` lub `UNIQUE`) **nie istnieje**, zostanie wstawiony.  
- Jeśli **istnieje konflikt** (czyli np. taki klucz już jest), wtedy wykona się część po `DO UPDATE`.

Przykład:
```sql
INSERT INTO users (id, name, email)
VALUES (1, 'Jan', 'jan@example.com')
ON CONFLICT (id)
DO UPDATE SET 
  name = EXCLUDED.name,
  email = EXCLUDED.email;
```

Warto wiedzieć:
- `EXCLUDED` to alias reprezentujący wartości, które próbowano wstawić.
- Można też pominąć aktualizację i np. nic nie robić:
  ```sql
  ON CONFLICT (id) DO NOTHING;
  ```
- Konflikt można definiować po konkretnym unikalnym kluczu, np. `ON CONFLICT (email)`.

Dla pełnej kontroli, czasami stosuje się też warunek:
```sql
ON CONFLICT (id)
DO UPDATE SET 
  name = EXCLUDED.name
WHERE users.name IS DISTINCT FROM EXCLUDED.name;
```
— żeby aktualizować tylko wtedy, gdy dane się rzeczywiście różnią.

Czy chcesz przykład takiego „upserta” w Javie (np. z JDBC lub JPA)?