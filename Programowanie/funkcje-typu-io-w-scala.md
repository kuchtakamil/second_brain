# Funkcje typu IO w Scala.

**Data:** 2023-04-07

---

**User:**

w scala po co używamy funkcji void przy typie IO?

---

**Assistant:**

W języku Scala funkcja o typie `IO` zwykle zwraca wartość typu `IO`, który reprezentuje opóźnione obliczenie, które może potencjalnie zakończyć się efektem ubocznym, takim jak odczytanie pliku, zapisanie do bazy danych, wyświetlenie czegoś na ekranie itp.

Jeśli funkcja nie ma zwracać żadnej wartości, ale wciąż chcemy, aby wykonywała efekty uboczne, możemy zwrócić wartość typu `IO[Unit]`. Typ `Unit` w języku Scala jest typem, który reprezentuje brak wartości, podobny do typu `void` w innych językach programowania. Dlatego, zwracając wartość typu `IO[Unit]`, informujemy, że funkcja wykona efekty uboczne, ale nie będzie zwracać żadnej wartości.

Przykład użycia:

```scala
import cats.effect.IO

def printToConsole(str: String): IO[Unit] = IO(println(str))

val program: IO[Unit] = for {
  _ <- printToConsole("Hello, World!")
  _ <- printToConsole("This is an example of using IO[Unit]")
} yield ()

program.unsafeRunSync()
```

W tym przykładzie funkcja `printToConsole` zwraca wartość typu `IO[Unit]`, co oznacza, że wyświetli tekst na ekranie, ale nie zwróci żadnej wartości. Następnie, w ciele programu, używamy funkcji `printToConsole` dwukrotnie, a wynik obu wywołań przypisujemy do wartości `_`, ponieważ nas interesuje tylko wykonanie efektów ubocznych. Ostatecznie, łączymy te dwie operacje za pomocą funkcji `flatMap` i `yield` i tworzymy wartość typu `IO[Unit]`, która odpowiada całemu programowi.