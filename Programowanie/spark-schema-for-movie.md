# Spark Schema for Movie

**Data:** 2023-12-16

---

**User:**

dla takich danych
index,id,title,type,description,release_year,age_certification,runtime,imdb_id,imdb_score,imdb_votes
0,tm84618,Taxi Driver,MOVIE,"A mentally unstable Vietnam War veteran works as a night-time taxi driver in New York City where the perceived decadence and sleaze feed his urge for violent action, attempting to save a preadolescent prostitute in the process.",1976,R,113,tt0075314,8.3,795222.0

utwórz scheme dla Spark 
StructType(
Array(
StructField(....

---

**Assistant:**

Oto struktura schematu Spark dla podanych danych:

```python
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DoubleType

# Definicja schematu
movie_schema = StructType([
    StructField("index", IntegerType(), True),
    StructField("id", StringType(), True),
    StructField("title", StringType(), True),
    StructField("type", StringType(), True),
    StructField("description", StringType(), True),
    StructField("release_year", IntegerType(), True),
    StructField("age_certification", StringType(), True),
    StructField("runtime", IntegerType(), True),
    StructField("imdb_id", StringType(), True),
    StructField("imdb_score", DoubleType(), True),
    StructField("imdb_votes", DoubleType(), True)
])

# Utworzenie pustego DataFrame z zastosowaniem zdefiniowanego schematu
empty_df = spark.createDataFrame([], schema=movie_schema)
```

Powyższy kod tworzy schemat Spark dla podanych danych, a następnie używa go do utworzenia pustego DataFrame. Możesz użyć tego schematu podczas wczytywania danych do Spark DataFrame, aby ustalić odpowiednie typy kolumn.