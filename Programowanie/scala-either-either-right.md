# Scala Either Either Right

**Data:** 2023-08-21

---

**User:**

Scala, 
generatePlayersWithNumbers zwraca Either[String, F[List[PlayerWithNumber]]]

unit test
  it should "generate numbers for players" in {
    val result = logic.generatePlayersWithNumbers(3)

    result.length shouldEqual 3
  }
jak sprawdzić wersję Right?

---

**Assistant:**

Wydaje się, że w twoim pytaniu występują pewne niejasności i błędy związane z kodem i testem, dlatego postaram się je rozwiązać, dostosowując do ogólnego kontekstu. Oto poprawione wyjaśnienia:

1. Wersja `Right` zwykle odnosi się do monady `Either`, która jest używana do reprezentowania wartości, które mogą mieć jedno z dwóch możliwych typów: `Left` lub `Right`. W twoim przypadku, `Either[String, F[List[PlayerWithNumber]]]` oznacza, że wartość może być typu `Left` (jeśli wystąpił błąd i trzeba zwrócić komunikat typu `String`) lub typu `Right` (jeśli operacja zakończyła się sukcesem i masz listę graczy z numerami). 

2. W celu przetestowania wersji `Right` możesz użyć funkcji pomocniczej, która sprawdza, czy wynik jest typu `Right` i przeprowadza dalsze asercje na wynikach. Oto przykład, jak to można zrobić w teście:

```scala
import scala.util._

// Przykładowa implementacja logic.generatePlayersWithNumbers
object logic {
  case class PlayerWithNumber(name: String, number: Int)
  type F[A] = List[A]

  def generatePlayersWithNumbers(count: Int): Either[String, F[PlayerWithNumber]] = {
    if (count < 0) Left("Invalid count")
    else Right(List.tabulate(count)(i => PlayerWithNumber(s"Player $i", i + 1)))
  }
}

// Testy
class LogicSpec extends org.scalatest.flatspec.AnyFlatSpec with org.scalatest.matchers.should.Matchers {
  import logic._

  it should "generate numbers for players" in {
    val result = generatePlayersWithNumbers(3)

    result match {
      case Right(players) =>
        players.length shouldEqual 3
        // Dalsze asercje dotyczące graczy, jeśli potrzebne
      case Left(error) =>
        fail(s"Unexpected Left result: $error")
    }
  }
}
```

W tym przykładzie, jeśli wynik jest typu `Right`, to wykonywane są dalsze asercje na gracze. Jeśli wynik jest typu `Left`, test zakończy się niepowodzeniem i wypisze komunikat otrzymany w `Left`.