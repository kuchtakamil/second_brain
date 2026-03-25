# SQL: GROUP BY COUNT

**Data:** 2024-02-20

---

**User:**

Napisz przykład SQL z zastosowaniem group by i count

---

**Assistant:**

Oczywiście! Poniżej znajdziesz przykład zastosowania klauzuli `GROUP BY` i funkcji agregującej `COUNT` w zapytaniu SQL. Przyjmijmy, że mamy tabelę o nazwie `Orders`, która zawiera informacje o zamówieniach, a chcemy policzyć ilość zamówień dla każdego klienta:

```sql
SELECT CustomerID, COUNT(OrderID) as NumberOfOrders
FROM Orders
GROUP BY CustomerID;
```

W tym zapytaniu używamy klauzuli `GROUP BY` do grupowania wyników według wartości w kolumnie `CustomerID`. Następnie funkcja agregująca `COUNT` oblicza liczbę zamówień dla każdego unikalnego klienta. Wynikiem będzie tabela, w której każdy wiersz przedstawia `CustomerID` oraz odpowiadającą mu ilość zamówień (`NumberOfOrders`).