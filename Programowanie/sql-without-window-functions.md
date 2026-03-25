# SQL without Window Functions

**Data:** 2023-12-30

---

**User:**

Przepisz zapytanie w SQL bez window functions

SELECT 
	*,
	MAX(amount) OVER() AS max_amount,
	MIN(amount) OVER() AS min_amount
FROM expense;

---

**Assistant:**

To rewrite the given SQL query without using window functions, you can use a subquery to calculate the maximum and minimum amounts. Here's the revised query:

```sql
SELECT 
    e.*,
    (SELECT MAX(amount) FROM expense) AS max_amount,
    (SELECT MIN(amount) FROM expense) AS min_amount
FROM expense e;
```

In this query:
- The subqueries `(SELECT MAX(amount) FROM expense)` and `(SELECT MIN(amount) FROM expense)` calculate the maximum and minimum amounts, respectively, from the entire `expense` table.
- These values are then selected alongside all columns (`e.*`) from each row in the `expense` table.
- The alias `e` is used for the `expense` table for clarity, though it's not strictly necessary.