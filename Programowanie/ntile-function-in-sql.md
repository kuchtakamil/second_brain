# NTILE Function in SQL

**Data:** 2023-12-27

---

**User:**

Co to jest NTILE na podstawie
https://mode.com/sql-tutorial/sql-window-functions

---

**Assistant:**

The `NTILE()` function in SQL is a window function used to distribute rows of a partition into a specified number of approximately equal groups, known as buckets. Here's an overview of how it works and its syntax:

1. **Functionality**: `NTILE()` divides the result set into a designated number of groups or buckets, which are approximately equal in size. It assigns a unique bucket number to each group, starting from one. Every row within a group is then given the bucket number corresponding to that group【20†source】【14†source】.

2. **Syntax**: The general syntax of the `NTILE()` function is `NTILE(buckets) OVER ( [PARTITION BY partition_expression, ...] ORDER BY sort_expression [ASC | DESC], ...)`. The `buckets` parameter specifies the number of buckets into which the rows are divided. This can be a literal positive integer or an expression evaluating to a positive integer. The `PARTITION BY` clause is used to distribute rows of a result set into partitions, and the `ORDER BY` clause determines the logical order of rows in each partition【14†source】【20†source】.

3. **Distribution of Rows**: If the total number of rows is not evenly divisible by the specified number of buckets, `NTILE()` creates groups of two different sizes with a difference of one row. The larger groups are placed before the smaller groups in the order specified by the `ORDER BY` clause. However, if the total number of rows is divisible by the number of buckets, the function evenly divides the rows among the buckets【14†source】【20†source】.

4. **Practical Example**: An example provided by Mode.com demonstrates the use of `NTILE()` in assigning quartiles, quintiles, and percentiles to rows. In this example, data is partitioned by a column `start_terminal` and ordered by `duration_seconds`. The `NTILE()` function is then used to divide the data into 4, 5, and 100 buckets respectively. This example highlights an important consideration: when working with small windows, the `NTILE()` function may not produce expected percentile distributions, particularly when the number of records is less than the number of buckets【8†source】.

In summary, `NTILE()` is a versatile SQL window function that can be used for a variety of purposes, such as statistical analysis, data segmentation, and creating ranked subdivisions within a dataset. The function's ability to partition data into equal or nearly equal groups based on specified criteria makes it a powerful tool for data analysis and reporting.

---

**User:**

Napisz to po polsku

---

**Assistant:**

Funkcja `NTILE()` w SQL to funkcja okienkowa służąca do podziału wierszy partycji na określoną liczbę mniej więcej równych grup, nazywanych wiaderkami (buckets). Oto przegląd jej działania i składni:

1. **Funkcjonalność**: `NTILE()` dzieli zestaw wyników na określoną liczbę grup lub wiaderek, które są mniej więcej równe pod względem wielkości. Każdej grupie przypisuje unikalny numer wiaderka, zaczynając od jedynki. Każdy wiersz w grupie otrzymuje numer wiaderka odpowiadającego tej grupie.

2. **Składnia**: Ogólna składnia funkcji `NTILE()` to `NTILE(buckets) OVER ([PARTITION BY partition_expression, ...] ORDER BY sort_expression [ASC | DESC], ...)`. Parametr `buckets` określa liczbę wiaderek, na które dzielone są wiersze. Może to być dosłowna dodatnia liczba całkowita lub wyrażenie, które ewaluuje do dodatniej liczby całkowitej. Klauzula `PARTITION BY` służy do rozdzielenia wierszy zestawu wyników na partycje, a klauzula `ORDER BY` określa logiczny porządek wierszy w każdej partycji.

3. **Rozkład wierszy**: Jeśli całkowita liczba wierszy nie dzieli się równo przez określoną liczbę wiaderek, `NTILE()` tworzy grupy o dwóch różnych rozmiarach, z różnicą jednego wiersza. Większe grupy są umieszczane przed mniejszymi w kolejności określonej przez klauzulę `ORDER BY`. Natomiast gdy całkowita liczba wierszy dzieli się przez liczbę wiaderek, funkcja równomiernie dzieli wiersze między wiaderka.

4. **Praktyczny przykład**: Przykład podany przez Mode.com pokazuje użycie `NTILE()` do przypisania kwartylów, kwintylów i percentyli do wierszy. W tym przykładzie dane są partycjonowane według kolumny `start_terminal` i uporządkowane według `duration_seconds`. Następnie funkcja `NTILE()` jest używana do podziału danych na 4, 5 i 100 wiaderek odpowiednio. Przykład ten podkreśla ważną kwestię: przy pracy z małymi oknami, funkcja `NTILE()` może nie produkować oczekiwanych dystrybucji percentylowych, szczególnie gdy liczba rekordów jest mniejsza niż liczba wiaderek.

Podsumowując, `NTILE()` to wszechstronna funkcja okienkowa SQL, którą można wykorzystać do różnych celów, takich jak analiza statystyczna, segmentacja danych oraz tworzenie rankingu podziałów w zbiorze danych. Możliwość partycjonowania danych na równe lub prawie równe grupy według określonych kryteriów sprawia, że jest to potężne narzędzie do analizy danych i raportowania.