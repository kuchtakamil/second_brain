# Funkcje Agregujące w Analizie

**Data:** 2024-02-14

---

**User:**

Co to są funkcje agregujące

---

**Assistant:**

Funkcje agregujące to operacje matematyczne, które są używane do przetwarzania zestawu danych, aby uzyskać pojedynczą wartość reprezentującą pewną charakterystykę zbioru. Te funkcje są powszechnie stosowane w bazach danych, analizie danych i statystyce. Oto kilka przykładów funkcji agregujących:

1. **Suma (SUM):** Dodaje wszystkie wartości w zbiorze danych.
   
2. **Średnia arytmetyczna (AVG lub MEAN):** Oblicza średnią wartość zbioru danych przez podzielenie sumy przez liczbę elementów.

3. **Maksimum (MAX):** Zwraca największą wartość w zbiorze danych.

4. **Minimum (MIN):** Zwraca najmniejszą wartość w zbiorze danych.

5. **Mediana (MEDIAN):** Zwraca wartość, która dzieli zbiór danych na dwie równe części, gdzie połowa wartości jest większa, a połowa mniejsza niż mediana.

6. **Odchylenie standardowe (STDDEV):** Mierzy stopień rozproszenia danych wokół ich średniej wartości.

7. **Liczba elementów (COUNT):** Zwraca liczbę elementów w zbiorze danych.

8. **Suma kumulatywna (CUMSUM):** Oblicza sumę kumulatywną, gdzie każda wartość jest sumą poprzednich wartości w zbiorze danych.

Te funkcje agregujące są używane w różnych dziedzinach analizy danych i programowania, aby uzyskać istotne informacje na temat zbiorów danych i dokonać różnych obliczeń statystycznych.

---

**User:**

dlaczego w spark aby policzyć wiersze piszemy 
.agg(count(lit(1))
Wyjaśnij dlaczego należy użyć lit(1)

---

**Assistant:**

W Apache Spark, metoda `.agg()` jest często używana w kontekście operacji agregacji na ramkach danych (DataFrames). Aby policzyć liczbę wierszy w ramce danych, możemy użyć funkcji `count()` w połączeniu z funkcją `lit(1)`. Oto dlaczego używamy `lit(1)` w tej kontekście:

1. **count(lit(1)) vs. count(\*):**
   - `count(lit(1))`: Wyrażenie `lit(1)` tworzy kolumnę, w której każda wartość to zawsze 1. Funkcja `count()` następnie zlicza ilość niepustych wartości w tej kolumnie. Ponieważ każda wartość jest równa 1, suma tych wartości daje liczbę wierszy w ramce danych.
   - `count(\*)`: Używanie `count(\*)` oznacza, że Spark zlicza ilość niepustych wierszy w ramce danych. Jest to równoważne z użyciem `count(columnName)` dla dowolnej istniejącej kolumny (która nie ma wartości null).

2. **Efektywność:**
   - Użycie `lit(1)` jest bardziej efektywne pod względem zasobów niż używanie `*` lub konkretnej kolumny, ponieważ `lit(1)` tworzy jedną stałą kolumnę o stałej wartości dla każdego wiersza, co jest lżejsze niż sprawdzanie wartości w innych kolumnach.

Przykładowy kod wykorzystujący `count(lit(1))` wyglądałby tak:

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import count, lit

spark = SparkSession.builder.appName("example").getOrCreate()

# Załóżmy, że mamy ramkę danych df
df = spark.createDataFrame([(1, "A"), (2, "B"), (3, "C")], ["ID", "Value"])

# Używamy agg(count(lit(1))) do zliczenia liczby wierszy
row_count = df.agg(count(lit(1))).collect()[0][0]

print("Liczba wierszy w ramce danych: {}".format(row_count))
```

W tym przykładzie `count(lit(1))` jest używane do zliczenia liczby wierszy w ramce danych `df`.