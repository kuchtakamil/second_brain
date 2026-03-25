# Korekta SQL i tabel

**Data:** 2023-12-27

---

**User:**

Stworzyłem takie tabele w postgresql i wypełniłem je przykładowymi danymi. Popraw jeśli gdzieś jest błąd
CREATE TABLE ministry_name(
	id SERIAL PRIMARY KEY,
  name VARCHAR(50),
);

INSERT INTO ministry_name VALUES('Ministry of War')
INSERT INTO ministry_name VALUES('Ministry of Lies')
INSERT INTO ministry_name VALUES('Ministry of Science')
INSERT INTO ministry_name VALUES('Ministry of Defence')
INSERT INTO ministry_name VALUES('Ministry of Adventure')
INSERT INTO ministry_name VALUES('Ministry of Cooking')

CREATE TABLE expense (
	id SERIAL PRIMARY KEY,
  subject VARCHAR(50),
  transaction_date date,
  amount integer,
	ministry_name_id: integer REFERENCES ministry_name(id)
);

INSERT INTO expense VALUES('Galaxy Destroyer', '16-12-5023', 500000, 1)
INSERT INTO expense VALUES('Laser Beam', '16-12-5023', 3000, 1)
INSERT INTO expense VALUES('Shield Barier', '18-12-5023', 5200, 1)
INSERT INTO expense VALUES('Cloaking System', '18-12-5023', 4000, 1)
INSERT INTO expense VALUES('Healing Drones', '18-12-5023', 500, 1)
INSERT INTO expense VALUES('Fighters Fleet', '18-12-5023', 22500, 1)
INSERT INTO expense VALUES('Destructor Canon', '19-12-5023', 19000, 1)
INSERT INTO expense VALUES('Subspace Drive', '19-12-5023', 85000, 1)
INSERT INTO expense VALUES('Communication System', '20-12-5023', 6000, 1)

---

**Assistant:**

There are a few issues in your SQL statements. Here's the corrected version:

1. In the `ministry_name` table creation, you should remove the comma at the end of the `name` column definition.
2. In the `expense` table creation, you should use a comma instead of a colon after `ministry_name_id`.

Here's the corrected SQL:

```sql
CREATE TABLE ministry_name (
	id SERIAL PRIMARY KEY,
	name VARCHAR(50)
);

INSERT INTO ministry_name (name) VALUES
  ('Ministry of War'),
  ('Ministry of Lies'),
  ('Ministry of Science'),
  ('Ministry of Defence'),
  ('Ministry of Adventure'),
  ('Ministry of Cooking');

CREATE TABLE expense (
	id SERIAL PRIMARY KEY,
	subject VARCHAR(50),
	transaction_date date,
	amount integer,
	ministry_name_id integer REFERENCES ministry_name(id)
);

INSERT INTO expense (subject, transaction_date, amount, ministry_name_id) VALUES
  ('Galaxy Destroyer', '5023-12-16', 500000, 1),
  ('Laser Beam', '5023-12-16', 3000, 1),
  ('Shield Barrier', '5023-12-18', 5200, 1),
  ('Cloaking System', '5023-12-18', 4000, 1),
  ('Healing Drones', '5023-12-18', 500, 1),
  ('Fighters Fleet', '5023-12-18', 22500, 1),
  ('Destructor Cannon', '5023-12-19', 19000, 1),
  ('Subspace Drive', '5023-12-19', 85000, 1),
  ('Communication System', '5023-12-20', 6000, 1);
```

Changes made:
- Removed the comma after `name` in the `ministry_name` table definition.
- Replaced the date format in the `transaction_date` field with the standard 'YYYY-MM-DD' format.
- Changed `ministry_name_id: integer` to `ministry_name_id integer` in the `expense` table definition.
- Corrected the `INSERT INTO` statements by specifying the columns to insert values into and using the correct date format.

---

**User:**

Teraz przy użyciu Window Functions chcę policzyć sumę wydatków dla każdego dnia. Chcę wyświetlić szukaną sumę, datę i nazwę ministerstwa

---

**Assistant:**

Aby obliczyć sumę wydatków dla każdego dnia oraz wyświetlić sumę, datę i nazwę ministerstwa, możesz użyć okienkowej funkcji (Window Function) `SUM()` razem z funkcją `OVER()`. Oto zapytanie SQL, które to realizuje:

```sql
SELECT
  e.transaction_date,
  mn.name AS ministry_name,
  SUM(e.amount) OVER(PARTITION BY e.transaction_date) AS daily_expense_total
FROM
  expense e
JOIN
  ministry_name mn ON e.ministry_name_id = mn.id
ORDER BY
  e.transaction_date;
```

W tym zapytaniu:
- Wybieramy datę transakcji (`transaction_date`) z tabeli `expense`.
- Dołączamy nazwę ministerstwa (`name`) z tabeli `ministry_name` poprzez dopasowanie `ministry_name_id`.
- Używamy funkcji `SUM(e.amount) OVER(PARTITION BY e.transaction_date)` do obliczenia sumy wydatków dla każdego dnia. `PARTITION BY` dzieli wyniki na grupy na podstawie daty transakcji, a `SUM()` oblicza sumę wydatków w ramach każdej grupy.
- Wyniki są sortowane według daty transakcji.

Dzięki temu zapytaniu otrzymasz wynik, który zawiera datę, nazwę ministerstwa oraz sumę wydatków dla każdego dnia.

---

**User:**

a czy dałoby się to zrobić przy użyciu tradycyjnego SQLa bezwindow functions?

---

**Assistant:**

Tak, możesz obliczyć sumę wydatków dla każdego dnia bez okienkowych funkcji, używając zwykłego SQL. W tym celu możesz skorzystać z grupowania (GROUP BY) i funkcji agregujących. Oto zapytanie SQL, które to realizuje:

```sql
SELECT
  e.transaction_date,
  mn.name AS ministry_name,
  SUM(e.amount) AS daily_expense_total
FROM
  expense e
JOIN
  ministry_name mn ON e.ministry_name_id = mn.id
GROUP BY
  e.transaction_date, mn.name
ORDER BY
  e.transaction_date;
```

W tym zapytaniu:

- Wybieramy datę transakcji (`transaction_date`) i nazwę ministerstwa (`name`) z tabeli `expense` i `ministry_name`.
- Używamy funkcji `SUM(e.amount)` do obliczenia sumy wydatków dla każdej grupy daty transakcji i nazwy ministerstwa.
- Wykorzystujemy klauzulę `GROUP BY` do grupowania wyników według daty transakcji i nazwy ministerstwa.
- Wyniki są sortowane według daty transakcji.

Dzięki temu zapytaniu również otrzymasz wynik, który zawiera datę, nazwę ministerstwa oraz sumę wydatków dla każdego dnia, ale bez konieczności korzystania z okienkowych funkcji.

---

**User:**

SELECT
  e.transaction_date,
  mn.name AS ministry_name,
  SUM(e.amount) OVER(PARTITION BY e.transaction_date) AS daily_expense_total
FROM
  expense e
JOIN
  ministry_name mn ON e.ministry_name_id = mn.id
ORDER BY
  e.transaction_date;

zwraca 9 wierszy a unikalnych dat jest 4. Można zmienić tak to zapytanie aby w wyniku były 4 wiersze każdy dla unkalnej daty? 

---

**Assistant:**

Aby uzyskać tylko 4 wiersze, po jednym dla każdej unikalnej daty, możesz użyć agregacji w połączeniu z podzapytaniem. Oto zaktualizowane zapytanie SQL:

```sql
SELECT
  e.transaction_date,
  mn.name AS ministry_name,
  daily_expense_total
FROM
  (SELECT
     e.transaction_date,
     mn.name AS ministry_name,
     SUM(e.amount) AS daily_expense_total
   FROM
     expense e
   JOIN
     ministry_name mn ON e.ministry_name_id = mn.id
   GROUP BY
     e.transaction_date, mn.name) AS subquery
ORDER BY
  subquery.transaction_date;
```

W tym zapytaniu:

- Tworzymy podzapytanie (`subquery`), które grupuje wydatki według daty transakcji i nazwy ministerstwa i oblicza sumę wydatków dla każdej grupy.
- Następnie, w zewnętrznym zapytaniu, wybieramy datę transakcji, nazwę ministerstwa i sumę wydatków z wyników podzapytania.
- Wyniki są sortowane według daty transakcji.

Dzięki temu zapytaniu otrzymasz tylko 4 wiersze, po jednym dla każdej unikalnej daty transakcji.

---

**User:**

Na podstawie wcześniej wprowadzonych danych do tabel ministry i expense, wymyśl jakiś przykład jak pokazać NTILE window function

---

**Assistant:**

Okej, załóżmy, że chcesz użyć funkcji NTILE w kontekście wydatków ministerstw, aby podzielić ministerstwa na grupy, które reprezentują ich wydatki w sposób równomierny. Możemy użyć funkcji NTILE do podzielenia ministerstw na trzy grupy, gdzie każda grupa ma podobną sumę wydatków. Oto przykład:

```sql
SELECT
  mn.name AS ministry_name,
  e.amount,
  NTILE(3) OVER(ORDER BY e.amount) AS expense_group
FROM
  expense e
JOIN
  ministry_name mn ON e.ministry_name_id = mn.id
ORDER BY
  e.amount;
```

W tym zapytaniu:

1. Wybieramy nazwę ministerstwa (`ministry_name`) i kwotę wydatków (`amount`) z tabeli `expense`.
2. Używamy funkcji `NTILE(3) OVER(ORDER BY e.amount)` do podzielenia ministerstw na trzy grupy w oparciu o kwoty wydatków. Funkcja `NTILE(3)` dzieli dane na trzy grupy, a `ORDER BY e.amount` określa, według czego sortować ministerstwa przed podziałem.
3. Wyniki są sortowane według kwoty wydatków.

W efekcie otrzymasz listę ministerstw wraz z ich wydatkami, podzieloną na trzy grupy w taki sposób, aby każda grupa miała podobną sumę wydatków. Grupa 1 będzie zawierać ministerstwa z najniższymi wydatkami, grupa 2 z wydatkami średnimi, a grupa 3 z najwyższymi wydatkami.

---

**User:**

Opisz co robi funkcja NTILE

---

**Assistant:**

Funkcja NTILE jest funkcją okienkową w języku SQL, która dzieli dane na równą liczbę przedziałów (kategorii) i przypisuje każdemu wierszowi wartość reprezentującą numer przedziału, do którego ten wiersz należy. Działa to na podstawie wartości w określonej kolumnie lub wyrażeniu, które jest określane wewnątrz funkcji NTILE.

Ogólna składnia funkcji NTILE wygląda następująco:

```sql
NTILE(n) OVER (ORDER BY kolumna)
```

Gdzie:
- `n` to liczba przedziałów, na które mają zostać podzielone dane.
- `ORDER BY kolumna` określa kolumnę lub wyrażenie, według którego dane są sortowane przed podziałem na przedziały.

Funkcja NTILE przydaje się w analizie danych, szczególnie w przypadku potrzeby podziału danych na grupy o podobnych rozmiarach lub wartościach. Jest często stosowana w celu tworzenia kwantyli lub percentyli, dzieląc dane na równy procent lub równą liczbę grup.

Przykład użycia funkcji NTILE:
Załóżmy, że mamy tabelę z wynikami testów studentów, a my chcemy podzielić wyniki na trzy grupy: "niskie", "średnie" i "wysokie". Możemy to zrobić przy użyciu funkcji NTILE, dzieląc wyniki na trzy przedziały. Każdy przedział będzie zawierać podobną liczbę studentów, a każdemu studentowi zostanie przypisany numer grupy na podstawie jego wyniku.

Wynik działania funkcji NTILE jest przydatny do analizy danych i zrozumienia rozkładu wartości w kolumnie lub wyrażeniu, szczególnie w kontekście porównywania, klasyfikowania lub podejmowania decyzji opartych na danych.