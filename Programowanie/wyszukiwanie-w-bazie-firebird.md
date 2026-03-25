# Wyszukiwanie w bazie Firebird

**Data:** 2025-03-15

---

**User:**

W starej bazie danych Firebird chciałbym znaleźć pewien wyraz jednak nie wiem w której tabeli i w której kolumnie znajduje się ten wyraz. Czy mogę go jakoś znaleźć?

---

**Assistant:**

Tak, da się to zrobić, choć Firebird nie udostępnia gotowego narzędzia do przeszukiwania wszystkich tabel i kolumn naraz jak np. niektóre GUI do baz danych (np. w SQL Server Management Studio można robić "Full Database Search").

Musisz napisać skrypt SQL lub procedurę, która przeiteruje przez wszystkie kolumny tekstowe we wszystkich tabelach i będzie sprawdzać, czy szukany wyraz się tam znajduje. To trochę uciążliwe, ale wykonalne.

### 🔍 Oto jak możesz to zrobić krok po kroku:

#### 1. **Znajdź wszystkie kolumny typu tekstowego**
Użyj zapytania do systemowej tabeli `RDB$RELATION_FIELDS`, żeby znaleźć wszystkie kolumny typu `VARCHAR`, `CHAR`, `BLOB SUB_TYPE 1` (czyli tekstowe blob-y).

```sql
SELECT
    rf.RDB$RELATION_NAME AS TABLE_NAME,
    rf.RDB$FIELD_NAME AS COLUMN_NAME,
    f.RDB$FIELD_TYPE,
    f.RDB$FIELD_SUB_TYPE
FROM
    RDB$RELATION_FIELDS rf
JOIN
    RDB$FIELDS f ON rf.RDB$FIELD_SOURCE = f.RDB$FIELD_NAME
WHERE
    (f.RDB$FIELD_TYPE = 14 OR f.RDB$FIELD_TYPE = 37 OR (f.RDB$FIELD_TYPE = 261 AND f.RDB$FIELD_SUB_TYPE = 1))
    AND rf.RDB$SYSTEM_FLAG = 0
ORDER BY 1, 2;
```

#### 2. **Na podstawie tego wygeneruj zapytania `SELECT` dla każdej tabeli i kolumny**
Wynikiem będzie lista typu:

```sql
SELECT * FROM TABLE_NAME WHERE COLUMN_NAME LIKE '%szukany_wyraz%';
```

Możesz to zautomatyzować skryptem, który wygeneruje te zapytania.

#### 3. **(Opcjonalnie) Półautomatyczna pomoc:**
Jeśli korzystasz z jakiegoś GUI (np. IBExpert, FlameRobin, DBeaver), możesz:

- Skopiować wynik z punktu 1 do Excela.
- Zbudować tam kolumnę generującą zapytania SQL `SELECT * FROM ... WHERE ... LIKE '%...'`.
- Wykonać te zapytania ręcznie lub wsadowo.

#### 4. **(Alternatywa) Prosty generator w SQL (dla kopiowania i uruchamiania później)**

```sql
SELECT
    'SELECT * FROM ' || TRIM(rf.RDB$RELATION_NAME) || ' WHERE ' || TRIM(rf.RDB$FIELD_NAME) || ' LIKE ''%szukany_wyraz%'';'
FROM
    RDB$RELATION_FIELDS rf
JOIN
    RDB$FIELDS f ON rf.RDB$FIELD_SOURCE = f.RDB$FIELD_NAME
WHERE
    (f.RDB$FIELD_TYPE = 14 OR f.RDB$FIELD_TYPE = 37 OR (f.RDB$FIELD_TYPE = 261 AND f.RDB$FIELD_SUB_TYPE = 1))
    AND rf.RDB$SYSTEM_FLAG = 0;
```

Wynik możesz sobie przekleić do pliku .sql i odpalać jedno po drugim.

---

Jeśli chcesz, mogę przygotować pełny skrypt w PL/SQL Firebird, który automatycznie przeiteruje po tych kolumnach i wypisze tabele, w których znalazł dopasowanie — daj znać, a przygotuję taką procedurę.

Chcesz taką wersję automatyczną?

---

**User:**

Total execution time: 0.057s
Starting transaction...
Error: *** IBPP::LogicException ***
Context: Transaction::AttachDatabase
Message: Can't attach a null Database.

---

**Assistant:**

Dzięki za informację — ten błąd:

```
*** IBPP::LogicException ***
Context: Transaction::AttachDatabase
Message: Can't attach a null Database.
```

oznacza, że klient (np. IBExpert, FlameRobin lub inne narzędzie korzystające z biblioteki IBPP) próbuje rozpocząć transakcję, ale **nie jest połączony z żadną bazą danych**.

### ✅ Co możesz zrobić:

#### 1. **Sprawdź, czy jesteś połączony z bazą danych**
Upewnij się, że przed wykonaniem zapytania połączenie z bazą Firebird zostało nawiązane. Jeśli używasz GUI:
- W **IBExpert** – sprawdź, czy Twoja baza danych jest **oznaczona jako połączona (zielona ikonka)**.
- W **FlameRobin** – kliknij bazę w drzewku i upewnij się, że nie pokazuje komunikatu typu "Not connected".

#### 2. **Spróbuj połączyć się ponownie**
- Odłącz i podłącz bazę jeszcze raz.
- Sprawdź, czy ścieżka do bazy jest poprawna (lokalna `.fdb`, czy zdalna `hostname:/path/to/db.fdb`).
- Sprawdź, czy Firebird Server działa na odpowiednim porcie (domyślnie 3050).

#### 3. **Jeśli robisz to z jakiegoś skryptu/CLI**:
Upewnij się, że:
- Wcześniej zadeklarowałeś połączenie (`connect '...' user '...' password '...'`)
- Przykład z `isql`:
```sql
CONNECT 'localhost:/path/to/your_database.fdb' USER 'SYSDBA' PASSWORD 'masterkey';
```

---

Jeśli podasz mi:
- Z jakiego narzędzia korzystasz (IBExpert, isql, FlameRobin, DBeaver itd.)
- Jak dokładnie próbujesz uruchomić to zapytanie (czy masz otwarte połączenie do bazy?)

— to mogę precyzyjnie powiedzieć, gdzie leży problem i jak go rozwiązać krok po kroku.

Chcesz, żebym przygotował Ci cały gotowy skrypt .sql, który możesz wkleić po połączeniu z bazą?

---

**User:**

czy takie zapytanie SELECT * FROM LISTA_OPERACJI WHERE KASJER LIKE '%kantor%'; jest case sensitive?

---

**Assistant:**

Świetne pytanie!

W Firebird **`LIKE` jest domyślnie case-sensitive**, czyli:

```sql
SELECT * FROM LISTA_OPERACJI WHERE KASJER LIKE '%kantor%';
```

— **zwróci tylko wiersze, gdzie `KASJER` zawiera dokładnie `kantor` (małe litery)**.

Czyli:
- `kantor123` – znajdzie ✅  
- `KANTOR123` – **nie znajdzie** ❌  
- `KaNtOr123` – **nie znajdzie** ❌

---

### 🔍 Jak zrobić case-insensitive `LIKE` w Firebird?

#### ✅ **Opcja 1: `COLLATE` z porównaniem bez rozróżniania wielkości liter**
Jeśli kolumna `KASJER` została utworzona z odpowiednim **collation**, np. `UNICODE_CI` (`CI = case-insensitive`), to możesz po prostu:

```sql
SELECT * FROM LISTA_OPERACJI WHERE KASJER COLLATE UNICODE_CI LIKE '%kantor%';
```

lub (jeśli masz kolumnę w `WIN1250`, `ISO8859_2`, itp.):
```sql
SELECT * FROM LISTA_OPERACJI WHERE KASJER COLLATE PXW_POL_CI LIKE '%kantor%';
```

> Musisz tylko upewnić się, że `COLLATE UNICODE_CI` jest kompatybilny z charsetem Twojej kolumny.

#### ✅ **Opcja 2: Porównanie po `LOWER()` lub `UPPER()`**
Najczęstsze obejście, gdy nie chcesz się przejmować collation:

```sql
SELECT * FROM LISTA_OPERACJI WHERE LOWER(KASJER) LIKE '%kantor%';
```

albo:
```sql
SELECT * FROM LISTA_OPERACJI WHERE UPPER(KASJER) LIKE '%KANTOR%';
```

Ten sposób działa niezależnie od collate, ale uwaga – **może spowolnić zapytanie**, jeśli masz duże dane i nie masz indeksu na `LOWER(KASJER)`.

---

Chcesz, żebym przygotował Ci prostą funkcję case-insensitive `LIKE`, którą można łatwo ponownie używać? Albo sprawdził, jaki masz charset/collation w tabeli `LISTA_OPERACJI`?