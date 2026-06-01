# Co robić, gdy baza danych stopniowo zwalnia pomimo dodawania nowych indeksów?

## Krótkie podsumowanie
Dodawanie indeksów to najczęstszy pierwszy krok przy problemach z wydajnością bazy danych, ale nie jest panaceum. Jeśli mimo nowych indeksów baza (łącznie z odczytami) stopniowo zwalnia, oznacza to, że problem leży głębiej — w architekturze danych, strategii zapytań, konfiguracji serwera lub w samym wzorcu dostępu do danych. Co więcej, nadmiar indeksów sam w sobie pogarsza wydajność zapisów i zwiększa zużycie pamięci. Poniżej opisano systematyczne podejście do diagnozowania i naprawiania tego problemu.

## Dlaczego to ma znaczenie / Kiedy to stosować?
Stopniowa degradacja wydajności bazy danych to jeden z najczęstszych problemów w systemach produkcyjnych. Jeśli nie zostanie rozwiązany, prowadzi do lawinowo rosnących opóźnień (latency), timeoutów, a ostatecznie do niedostępności całego systemu. Zrozumienie przyczyn i technik naprawczych jest kluczowe zarówno przy codziennej pracy z produkcją, jak i na rozmowach rekrutacyjnych z System Design.

## Krok 1: Zrozum, dlaczego same indeksy nie wystarczą

### Indeksy to nie magia — mają koszty
*   Każdy dodatkowy indeks **spowalnia operacje zapisu** (`INSERT`, `UPDATE`, `DELETE`), bo baza musi aktualizować strukturę indeksu przy każdej zmianie wiersza.
*   Indeksy zajmują pamięć (RAM). Gdy jest ich za dużo, nie mieszczą się w buforze (np. `shared_buffers` w PostgreSQL, `innodb_buffer_pool` w MySQL) i spadają na dysk — odczyty **zamiast z RAM zaczynają trafiać na I/O dyskowe**.
*   Query planner może **wybrać niewłaściwy indeks** (lub żaden) jeśli statystyki są nieaktualne lub indeks ma niską selektywność.

### Syndrom „za dużo indeksów" (Index Bloat)
*   Nadmiarowe, pokrywające się lub nieużywane indeksy to martwy balast — zajmują pamięć, spowalniają zapisy i zaśmiecają plan zapytań.
*   W PostgreSQL: `pg_stat_user_indexes` pozwala znaleźć indeksy z `idx_scan = 0` (nigdy nieużyte).
*   W MySQL: `sys.schema_unused_indexes` pokazuje indeksy, których optimizer nie ruszał.

## Krok 2: Diagnoza — znajdź prawdziwe wąskie gardło

### 2.1. Analiza wolnych zapytań (Slow Query Log)
*   Włącz logowanie wolnych zapytań i zbierz TOP 10 najwolniejszych.
*   PostgreSQL: `pg_stat_statements` — rozszerzenie pokazujące sumaryczny czas, liczbę wywołań i średni czas każdego zapytania.
*   MySQL: `slow_query_log` + narzędzie `pt-query-digest` z Percona Toolkit.

```sql
-- PostgreSQL: TOP 10 najwolniejszych zapytań
SELECT query, calls, mean_exec_time, total_exec_time
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;
```

### 2.2. EXPLAIN ANALYZE — czytaj plan wykonania
*   Używaj `EXPLAIN ANALYZE` do każdego wolnego zapytania. Szukaj:
    *   **Seq Scan** na dużych tabelach — oznacza brak trafienia w indeks.
    *   **Nested Loop** z dużą liczbą iteracji — potencjalny problem N+1.
    *   **Sort** z `external merge` — sortowanie na dysku zamiast w pamięci (`work_mem` za niski).
    *   **Hash Join** z odrzuceniem wielu wierszy (`Rows Removed by Filter`) — zapytanie czyta za dużo danych.

```sql
EXPLAIN ANALYZE
SELECT o.id, c.name
FROM orders o
JOIN customers c ON c.id = o.customer_id
WHERE o.created_at > '2025-01-01'
  AND o.status = 'active';
```

### 2.3. Sprawdź metryki systemowe
*   **CPU:** Czy baza jest CPU-bound? Zwykle oznacza złożone zapytania lub brak indeksów.
*   **I/O dyskowe (iowait):** Wysoki `iowait` = dane nie mieszczą się w RAM i są czytane z dysku.
*   **Pamięć (RAM):** Jaki % danych jest w cache (`buffer cache hit ratio`)? Poniżej 95% to sygnał alarmowy.
*   **Połączenia:** Ile aktywnych połączeń? Zbyt wiele = contention na lockach.

```sql
-- PostgreSQL: Cache Hit Ratio (powinien być > 0.95)
SELECT
  sum(heap_blks_hit) / (sum(heap_blks_hit) + sum(heap_blks_read)) AS cache_hit_ratio
FROM pg_statio_user_tables;
```

## Krok 3: Typowe przyczyny degradacji i ich rozwiązania

### 3.1. Table Bloat (Rozdęcie tabeli)
*   **Problem:** W PostgreSQL, `UPDATE` i `DELETE` nie usuwają fizycznie wierszy — tworzą „martwe krotki" (dead tuples). Tabela rośnie, indeksy stają się fragmentaryczne, skany pochłaniają coraz więcej I/O.
*   **Rozwiązanie:**
    *   Upewnij się, że `autovacuum` działa prawidłowo i nadąża za tempem zmian.
    *   Dostosuj parametry: `autovacuum_vacuum_scale_factor`, `autovacuum_vacuum_cost_delay`.
    *   Jednorazowo: `VACUUM FULL` (blokuje tabelę!) lub `pg_repack` (online, bez locka).

```sql
-- Sprawdź liczbę martwych krotek
SELECT relname, n_dead_tup, n_live_tup,
       round(n_dead_tup::numeric / greatest(n_live_tup, 1) * 100, 2) AS dead_pct
FROM pg_stat_user_tables
ORDER BY n_dead_tup DESC
LIMIT 10;
```

### 3.2. Index Bloat (Rozdęcie indeksów)
*   **Problem:** Indeksy B-tree również się fragmentują — po wielu `UPDATE`/`DELETE` zawierają dużo pustych stron.
*   **Rozwiązanie:**
    *   `REINDEX CONCURRENTLY` (PostgreSQL 12+) — przebudowuje indeks bez blokowania tabeli.
    *   W MySQL: `ALTER TABLE ... FORCE` lub `OPTIMIZE TABLE`.

### 3.3. Brak partycjonowania (Table Partitioning)
*   **Problem:** Tabela z setkami milionów wierszy jest za duża, by jakikolwiek indeks był efektywny. Skany indeksowe na ogromnych B-tree są wolne, a `VACUUM` trwa godzinami.
*   **Rozwiązanie:**
    *   **Partycjonowanie** tabel po kluczu czasowym (np. `created_at` — partycja per miesiąc) lub logicznym (np. `tenant_id`).
    *   Pozwala na **partition pruning** — baza skanuje tylko relewanatne partycje zamiast całej tabeli.
    *   Ułatwia archiwizację: zamiast `DELETE FROM ... WHERE created_at < X` (drogie), po prostu `DROP PARTITION`.

```sql
-- PostgreSQL: Partycjonowanie po zakresie dat
CREATE TABLE orders (
    id         BIGSERIAL,
    created_at TIMESTAMPTZ NOT NULL,
    status     TEXT,
    total      NUMERIC
) PARTITION BY RANGE (created_at);

CREATE TABLE orders_2025_q1 PARTITION OF orders
    FOR VALUES FROM ('2025-01-01') TO ('2025-04-01');
```

### 3.4. Problemy z zapytaniami (Query Antipatterns)

*   **SELECT \*:** Czyta wszystkie kolumny — wymusza odczyt z tabeli nawet jeśli indeks pokrywa potrzebne dane (covering index). Zawsze wymieniaj konkretne kolumny.
*   **N+1 Query Problem:** ORM generuje N osobnych zapytań zamiast jednego `JOIN`-a. Sprawdź logi — setki niemal identycznych zapytań to klasyczny objaw.
*   **Funkcje na kolumnie w WHERE:** `WHERE YEAR(created_at) = 2025` **nie trafi w indeks** na `created_at`. Użyj zakresu: `WHERE created_at >= '2025-01-01' AND created_at < '2026-01-01'`.
*   **Implicit Type Casting:** `WHERE varchar_col = 12345` (porównanie stringa z intem) może wymusić Seq Scan.
*   **LIKE '%tekst%':** Wildcard na początku uniemożliwia użycie B-tree indeksu. Rozwiązanie: indeks GIN z `pg_trgm` (trigram) lub pełnotekstowy (Full-Text Search).

### 3.5. Niewystarczające zasoby serwera / Konfiguracja
*   **`shared_buffers` / `innodb_buffer_pool_size`:** Za mały bufor = ciągły I/O dyskowy. Reguła: ~25% RAM dla PostgreSQL, ~70-80% RAM dla dedykowanego MySQL.
*   **`work_mem` (PostgreSQL):** Za niski = sortowanie i hash join lądują na dysku. Zwiększ ostrożnie (mnoży się przez liczbę operacji * połączeń).
*   **`effective_cache_size`:** Informuje query planner ile pamięci ma do dyspozycji (nie alokuje jej fizycznie). Zbyt niska wartość sprawia, że planner unika indeksów.
*   **Connection Pooling:** Brak poolera (np. PgBouncer, ProxySQL) = setki bezpośrednich połączeń = ogromny overhead na pamięć i context switching.

### 3.6. Lock Contention i Long-Running Transactions
*   **Problem:** Długotrwałe transakcje trzymają locki, blokując inne zapytania. W PostgreSQL blokują też `VACUUM`, co prowadzi do Table Bloat.
*   **Rozwiązanie:**
    *   Monitoruj `pg_stat_activity` — szukaj zapytań w stanie `idle in transaction`.
    *   Ustaw `idle_in_transaction_session_timeout`.
    *   Przenieś ciężkie operacje analityczne na **Read Replica**.

```sql
-- Znajdź blokujące zapytania
SELECT blocked.pid AS blocked_pid,
       blocked.query AS blocked_query,
       blocking.pid AS blocking_pid,
       blocking.query AS blocking_query
FROM pg_stat_activity blocked
JOIN pg_locks bl ON bl.pid = blocked.pid
JOIN pg_locks lk ON lk.locktype = bl.locktype
  AND lk.relation = bl.relation
  AND lk.pid != bl.pid
JOIN pg_stat_activity blocking ON blocking.pid = lk.pid
WHERE NOT bl.granted;
```

## Krok 4: Strategie skalowania, gdy optymalizacja nie wystarcza

### Read Replicas
*   Kieruj odczyty (zwłaszcza ciężkie raporty) na repliki. Master obsługuje tylko zapisy.
*   Uwaga: repliki mogą mieć **replication lag** — nie nadają się do odczytów wymagających natychmiastowej spójności.

### Caching (Redis / Memcached)
*   Cachuj wyniki częstych, kosztownych zapytań. Zmniejsza liczbę trafień w bazę o rząd wielkości.
*   Wzorce: Cache-Aside, Write-Through, Write-Behind.
*   Uważaj na **cache invalidation** — „one of the two hard things in CS".

### Archiwizacja danych (Data Archival)
*   Przenieś stare dane (np. zamówienia starsze niż 2 lata) do osobnej tabeli archiwum lub cold storage (np. S3 + Athena).
*   Mniejsza tabela = szybsze indeksy, szybszy `VACUUM`, mniejszy bufor.

### Denormalizacja i Materialized Views
*   Jeśli zapytania wymagają wielu `JOIN`-ów — rozważ **Materialized View** odświeżane cyklicznie.
*   Denormalizacja (duplikacja danych) zmniejsza liczbę joinów kosztem spójności — stosuj świadomie.

```sql
-- Materialized View w PostgreSQL
CREATE MATERIALIZED VIEW mv_daily_sales AS
SELECT date_trunc('day', created_at) AS day,
       count(*) AS order_count,
       sum(total) AS revenue
FROM orders
WHERE status = 'completed'
GROUP BY 1;

-- Odświeżanie (np. cron co godzinę)
REFRESH MATERIALIZED VIEW CONCURRENTLY mv_daily_sales;
```

### Sharding (ostateczność)
*   Podział danych na wiele instancji bazy (np. po `tenant_id` lub `user_id`).
*   Ogromny wzrost złożoności operacyjnej — stosuj dopiero po wyczerpaniu pozostałych opcji.

## Podsumowanie — kolejność działań (Checklist)

| Priorytet | Akcja | Narzędzie |
|-----------|-------|-----------|
| 1 | Znajdź TOP 10 wolnych zapytań | `pg_stat_statements`, slow query log |
| 2 | Przeanalizuj plany wykonania | `EXPLAIN ANALYZE` |
| 3 | Sprawdź cache hit ratio i metryki I/O | `pg_statio_user_tables`, `iostat` |
| 4 | Usuń nieużywane / zduplikowane indeksy | `pg_stat_user_indexes` |
| 5 | Napraw table/index bloat | `VACUUM`, `REINDEX`, `pg_repack` |
| 6 | Zoptymalizuj zapytania (N+1, SELECT *, funkcje w WHERE) | Logi ORM, code review |
| 7 | Dostosuj konfigurację (bufory, work_mem, pooling) | `postgresql.conf`, PgBouncer |
| 8 | Partycjonuj duże tabele | `PARTITION BY RANGE` |
| 9 | Dodaj cache (Redis) i read replicas | Architektura aplikacji |
| 10 | Archiwizuj stare dane | Cron + cold storage |

## Powiązane pliki
*   [Kiedy stosować bazy SQL a kiedy NoSQL?](sql-vs-nosql-criteria.md)
*   [Twierdzenie CAP](cap-theorem.md)
*   [Pytania rekrutacyjne z System Design](system-design-pytania-rekrutacyjne.md)
