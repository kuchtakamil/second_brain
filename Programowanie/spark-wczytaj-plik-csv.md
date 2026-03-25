# Spark: Wczytaj plik CSV

**Data:** 2023-12-16

---

**User:**

Mam plik csv z danymi, w Scali utworzoną case class (o nazwie Movie) z odpowiednimi typami danych  dla kolumn z pliku csv. Jak w spark teraz wczytać ten plik tak aby uzyskać Dataset[Movie]

---

**Assistant:**

Aby wczytać plik CSV i utworzyć `Dataset[Movie]` w Apache Spark z użyciem języka Scala, możesz skorzystać z `spark.read` i `as` do konwersji DataFrame na Dataset. Przyjmując, że twoja case class Movie wygląda mniej więcej tak:

```scala
case class Movie(id: Int, title: String, genre: String, releaseYear: Int)
```

Możesz użyć poniższego kodu:

```scala
import org.apache.spark.sql.{SparkSession, Encoders}

// Inicjalizacja SparkSession
val spark = SparkSession.builder().appName("MovieDatasetExample").getOrCreate()

// Ścieżka do pliku CSV
val filePath = "/ścieżka/do/twojego/pliku.csv"

// Wczytanie pliku CSV do DataFrame
val movieDF = spark.read
  .option("header", "true") // Jeśli plik CSV ma nagłówek
  .csv(filePath)

// Definicja schemy dla Dataset
val movieSchema = Encoders.product[Movie].schema

// Konwersja DataFrame na Dataset[Movie]
val movieDataset = movieDF.as[Movie](movieSchema)

// Wyświetlenie kilku rekordów z Dataset
movieDataset.show()
```

Upewnij się, że dostosujesz nazwy kolumn w pliku CSV oraz odpowiednie typy danych w case class Movie, aby pasowały do twojego przypadku. Pamiętaj także o poprawnym ustawieniu opcji "header" w zależności od tego, czy twój plik CSV zawiera nagłówek czy nie.

Utworzenie SparkSession jest kluczowe, ponieważ zapewnia dostęp do funkcji Spark. W przykładzie zakłada się, że Spark jest dostępny w trybie lokalnym. Jeśli pracujesz na klastrze Spark, dostosuj ustawienia sesji zgodnie z wymaganiami klastra.

---

**User:**

dostaję błąd Cannot resolve symbol as

---

**Assistant:**

Przepraszam za zamieszanie. Błąd "Cannot resolve symbol as" sugeruje, że kod nie rozpoznaje metody `as`. Możliwe przyczyny to nieprawidłowe importy lub brak odpowiednich bibliotek. Upewnij się, że dodajesz poprawne zależności do projektu. 

Dodaj poniższe importy, które są istotne dla tego kodu:

```scala
import org.apache.spark.sql.{SparkSession, Encoders}
```

Jeśli nadal występuje problem, sprawdź, czy masz odpowiednie zależności w swoim projekcie. W pliku `build.sbt` (lub inny plik konfiguracyjny, w zależności od tego, jak jesteś skonfigurowany), dodaj coś w stylu:

```scala
libraryDependencies += "org.apache.spark" %% "spark-sql" % "2.4.8"
```

Zwróć uwagę, że liczba wersji (`2.4.8`) może być różna w zależności od wersji Spark, którą używasz.

Po wprowadzeniu tych poprawek, kod powinien działać poprawnie.

---

**User:**

to nie to, nadal mam blad

---

**Assistant:**

Przepraszam za wcześniejsze zamieszanie. Wydaje się, że problem może wynikać z tego, że klasa `Encoders` nie jest importowana w sposób właściwy. Upewnij się, że dodajesz import dla `Encoders` z `org.apache.spark.sql`:

```scala
import org.apache.spark.sql.{SparkSession, Encoders}
```

Ponadto, sprawdź, czy twoje zależności Spark są prawidłowo skonfigurowane. W pliku `build.sbt` (lub innym pliku konfiguracyjnym), upewnij się, że dodajesz zależność do modułu `spark-sql`:

```scala
libraryDependencies += "org.apache.spark" %% "spark-sql" % "2.4.8"
```

Zaktualizuj wersję Spark (`2.4.8`) zgodnie z wersją, którą używasz. Po dodaniu tych importów i zależności, powinieneś być w stanie użyć metody `as` bez problemów. Jeśli problem nadal występuje, proszę dostarczyć więcej informacji na temat błędu, abyśmy mogli pomóc w jego rozwiązaniu.

---

**User:**

powtarzasz w kółko to samo, mówię że nie w tym jest problem

---

**Assistant:**

Przepraszam za wszelkie zamieszanie. Jeśli nadal napotykasz problem z użyciem metody `as` w celu konwersji DataFrame na Dataset, możemy spróbować alternatywnego podejścia. Zamiast używać metody `as`, możemy użyć konstruktora case class bezpośrednio w DataFrame.

Oto jak to można zrobić:

```scala
import org.apache.spark.sql.{SparkSession, Row}
import org.apache.spark.sql.types._

// Inicjalizacja SparkSession
val spark = SparkSession.builder().appName("MovieDatasetExample").getOrCreate()

// Ścieżka do pliku CSV
val filePath = "/ścieżka/do/twojego/pliku.csv"

// Wczytanie pliku CSV do DataFrame
val movieDF = spark.read
  .option("header", "true") // Jeśli plik CSV ma nagłówek
  .csv(filePath)

// Definicja schemy dla DataFrame
val movieSchema = StructType(Seq(
  StructField("id", IntegerType, nullable = false),
  StructField("title", StringType, nullable = false),
  StructField("genre", StringType, nullable = false),
  StructField("releaseYear", IntegerType, nullable = false)
))

// Konwersja DataFrame na Dataset[Movie]
val movieDataset = movieDF
  .flatMap { case Row(id: Int, title: String, genre: String, releaseYear: Int) =>
    Some(Movie(id, title, genre, releaseYear))
  }(Encoders.product[Movie])

// Wyświetlenie kilku rekordów z Dataset
movieDataset.show()
```

W tym przypadku używamy metody `flatMap` do konwersji DataFrame na Dataset, a następnie definiujemy schemę ręcznie. Sprawdź, czy to podejście działa dla Twojego przypadku. Jeśli nadal masz problemy, proszę podać więcej informacji na temat błędu, abyśmy mogli lepiej zdiagnozować problem.