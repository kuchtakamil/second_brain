# Spark SQL Window Function

**Data:** 2024-02-14

---

**User:**

To jest kod Spark dla przykładowej operacji wykorzystującej funkcje okienkowe.
val window = Window.partitionBy($"release_year".as("year")).orderBy($"imdb_score")
    movieDf2.withColumn("scoreRank", row_number().over(window))
      .filter($"scoreRank" === 1)
      .sort($"imdb_score")

Jak wyglądałby mniej więcej SQL dla takiej operacji?

---

**Assistant:**

Oto przykładowe zapytanie SQL, które realizuje podobną operację z użyciem funkcji okienkowych:

```sql
SELECT *
FROM (
    SELECT
        *,
        ROW_NUMBER() OVER (PARTITION BY release_year ORDER BY imdb_score) AS scoreRank
    FROM movieTable
) AS rankedMovies
WHERE scoreRank = 1
ORDER BY imdb_score;
```

Powyższe zapytanie SQL wykorzystuje funkcję `ROW_NUMBER()` do przypisywania rangi każdemu rekordowi w ramach partycji zdefiniowanej przez `PARTITION BY release_year`. Następnie zewnętrzne zapytanie wybiera te rekordy, które mają `scoreRank` równy 1 (czyli najwyższą rangę w każdej partycji) i sortuje wyniki według `imdb_score`. 

Warto zauważyć, że `movieTable` to przykładowa nazwa tabeli, a zapytanie powinno zostać dostosowane do faktycznej struktury bazy danych i nazw kolumn.