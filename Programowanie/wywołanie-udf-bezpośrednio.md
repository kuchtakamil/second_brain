# Wywołanie UDF bezpośrednio.

**Data:** 2024-03-17

---

**User:**

W Spark mam zdefiniowany UDF przy pomocy klasy. Czy jest możliwość wywołania tej funkcji inaczej niż przez call_udf i podając w string nazwę tej funkcji?

---

**Assistant:**

Tak, istnieje możliwość wywołania zdefiniowanej funkcji UDF (User Defined Function) w Spark'u inaczej niż poprzez `call_udf` i podając nazwę funkcji jako string. Można to zrobić poprzez wykorzystanie metod z klasy `pyspark.sql.functions`, które są wbudowane w Spark SQL. Aby osiągnąć to, należy zarejestrować funkcję zdefiniowaną przez użytkownika za pomocą metody `register` obiektu `pyspark.sql.functions.udf`.

Oto przykład, jak to zrobić:

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import IntegerType

# Inicjalizacja sesji Spark
spark = SparkSession.builder \
    .appName("UDF Example") \
    .getOrCreate()

# Przykładowa funkcja UDF zdefiniowana jako klasa
class MyUDF:
    @staticmethod
    @udf(returnType=IntegerType())
    def square(x):
        return x * x

# Rejestracja funkcji UDF
spark.udf.register("square_udf", MyUDF.square)

# Tworzenie ramki danych
data = [(1,), (2,), (3,), (4,), (5,)]
df = spark.createDataFrame(data, ["value"])

# Wywołanie funkcji UDF
result = df.select(MyUDF.square("value").alias("squared_value"))
result.show()
```

W tym przykładzie, funkcja UDF `square` jest zarejestrowana pod nazwą "square_udf" za pomocą `spark.udf.register()`. Następnie jest wywoływana bezpośrednio używając jej jako atrybutu `MyUDF.square("value")` w metodzie `select` na ramce danych `df`.