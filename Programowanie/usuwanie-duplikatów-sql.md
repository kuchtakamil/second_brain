# Usuwanie duplikatów SQL.

**Data:** 2023-08-03

---

**User:**

wyjaśnij co robi podany kod SQL i w jaki sposób. Jaką rolę pełnią tam group by?
DELETE
FROM MyDuplicateTable
WHERE ID NOT IN
(
SELECT MAX(ID)
FROM MyDuplicateTable
GROUP BY DuplicateColumn1, DuplicateColumn2, DuplicateColumn3)

---

**Assistant:**

Ten kod SQL to zapytanie DELETE, które służy do usunięcia duplikatów z tabeli o nazwie MyDuplicateTable. Duplikaty są rozpoznawane na podstawie wartości kolumn DuplicateColumn1, DuplicateColumn2 i DuplicateColumn3. W skrócie, pozostawione zostaną tylko wiersze, które mają najwyższy (najnowszy) ID wśród duplikatów o tych samych wartościach w tych trzech kolumnach.

Dokładnie:

1. Zapytanie podzapytania (subquery):
```
SELECT MAX(ID)
FROM MyDuplicateTable
GROUP BY DuplicateColumn1, DuplicateColumn2, DuplicateColumn3
```
To jest podzapytanie, które wybiera maksymalny ID dla każdego zestawu wartości w kolumnach DuplicateColumn1, DuplicateColumn2 i DuplicateColumn3. W tym przypadku wykorzystujemy funkcję agregującą MAX(ID), która zwraca największą wartość ID w każdej grupie, grupując po trzech kolumnach.

2. Główne zapytanie (main query):
```
DELETE
FROM MyDuplicateTable
WHERE ID NOT IN (...)
```
Główne zapytanie używa podzapytania, aby usunąć wiersze, których ID nie znajduje się w wynikach podzapytania. Innymi słowy, wiersze, których ID nie odpowiada maksymalnemu ID w swojej grupie, zostaną usunięte. Oznacza to, że zostanie zachowany tylko jeden wiersz dla każdego zestawu unikalnych wartości w kolumnach DuplicateColumn1, DuplicateColumn2 i DuplicateColumn3, ponieważ tylko ten wiersz będzie miał najwyższy (najnowszy) ID w grupie duplikatów.

Rola "GROUP BY" polega na grupowaniu wierszy w tabeli na podstawie określonych kolumn (w tym przypadku DuplicateColumn1, DuplicateColumn2 i DuplicateColumn3) i tworzeniu grup na podstawie ich unikalnych wartości. Następnie funkcja agregująca MAX(ID) jest używana do znalezienia maksymalnej wartości ID w każdej z tych grup. Dzięki temu możemy zidentyfikować duplikaty w tabeli na podstawie tych trzech kolumn i zachować tylko te wiersze, które mają największy (najnowszy) ID w każdej z grup. Pozostałe duplikaty są usuwane za pomocą instrukcji DELETE.