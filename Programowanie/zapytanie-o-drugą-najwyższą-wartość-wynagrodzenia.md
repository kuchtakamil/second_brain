# Zapytanie o drugą najwyższą wartość wynagrodzenia.

**Data:** 2023-08-02

---

**User:**

Jak mogłoby wyglądać zapytanie SQL które miałoby znaleźć drugą najwyższą wartość wynagrodzenia?

---

**Assistant:**

Aby znaleźć drugą najwyższą wartość wynagrodzenia w tabeli, możemy użyć zapytania SQL z użyciem funkcji ORDER BY i LIMIT. Przyjmijmy, że tabela nazywa się "employees", a kolumna z wynagrodzeniem to "salary". Poniżej znajduje się przykładowe zapytanie:

```sql
SELECT MAX(salary) AS second_highest_salary
FROM employees
WHERE salary < (SELECT MAX(salary) FROM employees);
```

To zapytanie znajduje maksymalną wartość wynagrodzenia (czyli najwyższą) w tabeli "employees" poprzez użycie funkcji MAX(salary). Następnie, przy użyciu podzapytania, szukamy maksymalnej wartości wynagrodzenia, której wartość jest mniejsza niż najwyższa wartość wynagrodzenia w tabeli. W ten sposób otrzymamy drugą najwyższą wartość wynagrodzenia.

Wynik tego zapytania będzie zawierać jedną kolumnę o nazwie "second_highest_salary", która będzie zawierała drugą najwyższą wartość wynagrodzenia z tabeli "employees".