# Scala Unit Tests

**Data:** 2023-08-18

---

**User:**

Scala, wygeneruj unit testy dla kodu
trait GameLogic[F[_]] {
  def generateNumbersForPlayers(playerNumber: Int): F[List[PlayerWithNumber]]
  def sortResults(numbersForPlayers: List[PlayerWithNumber]): List[GameResult]
}
object GameLogic {
  val upperLimit = 999999
  def make[F[_]: Async]: GameLogic[F] = new GameLogic[F] {
    def generateNumbersForPlayers(playerNumber: Int): F[List[PlayerWithNumber]] = for {
      playerNumbers <- generateRandomNumbers(playerNumber - 1, upperLimit)
      botNumber     <- generateRandomNumber(upperLimit)
    } yield {
      val players = (0 until playerNumber - 1).toList.map { index =>
        PlayerWithNumber(index.toString, false, playerNumbers(index))
      }
      PlayerWithNumber(playerNumber.toString, true, botNumber) :: players
    }
    def sortResults(numbersForPlayers: List[PlayerWithNumber]): List[GameResult] = {
      val resultedPlayers: List[PlayerWithResult] = numbersForPlayers
        .map { numberedPlayer =>
          PlayerWithResult(numberedPlayer, parseNumberToResult(numberedPlayer.number))
        }
        .sortBy(_.result)

      resultedPlayers
        .takeWhile(!_.playerWithNumber.isBot)
        .zipWithIndex
        .map { case (resultedPlayer, position) =>
          GameResult(
            position,
            resultedPlayer.playerWithNumber.playerNo,
            resultedPlayer.playerWithNumber.number,
            resultedPlayer.result,
          )
        }
    }
    private def parseNumberToResult(result: Int): Int = {
      result.toString.toList
        .foldLeft(Map.empty[Char, Int].withDefaultValue(0)) { (acc, element) =>
          acc.updated(element, acc(element) + 1)
        }
        .foldLeft(0)((sum, entry) => sum + formula(entry._1, entry._2))
    }
    private def generateRandomNumber(upperLimit: Int): F[Int] =
      Async[F].delay {
        scala.util.Random.nextInt(upperLimit)
      }
    private def generateRandomNumbers(count: Int, upperLimit: Int): F[List[Int]] =
      Async[F].delay {
        List.fill(count)(scala.util.Random.nextInt(upperLimit))
      }
    private def formula(times: Int, digit: Int): Int =
      Math.pow(10, (times - 1) * digit).intValue
  }
}

---

**Assistant:**

Sure, here are some unit tests for the provided Scala code using popular testing frameworks like ScalaTest and Cats Effect:

```scala
import cats.effect.{IO, Sync}
import org.scalatest.flatspec.AnyFlatSpec
import org.scalatest.matchers.should.Matchers
import org.scalatest.concurrent.ScalaFutures
import org.scalatest.time.SpanSugar._

class GameLogicSpec extends AnyFlatSpec with Matchers with ScalaFutures {
  import cats.effect.unsafe.implicits.global // Implicitly needed for running IO

  behavior of "GameLogic"

  it should "generate numbers for players" in {
    val logic = GameLogic.make[IO]
    val result = logic.generateNumbersForPlayers(3).unsafeRunSync()

    result.length shouldBe 3
  }

  it should "sort results correctly" in {
    val logic = GameLogic.make[IO]
    val playerNumbers = List(
      PlayerWithNumber("1", false, 123),
      PlayerWithNumber("2", false, 456),
      PlayerWithNumber("3", true, 789)
    )

    val results = logic.sortResults(playerNumbers)

    results should have length 2
    results.headOption.foreach(_.position shouldBe 0)
    results.lastOption.foreach(_.position shouldBe 1)
  }

  it should "parse number to result" in {
    val logic = GameLogic.make[IO]
    val result = logic.parseNumberToResult(123)

    result shouldBe 102
  }

  it should "generate random number" in {
    val logic = GameLogic.make[IO]
    val result = logic.generateRandomNumber(100).unsafeRunSync()

    result should (be >= 0 and be < 100)
  }

  it should "generate random numbers" in {
    val logic = GameLogic.make[IO]
    val result = logic.generateRandomNumbers(5, 100).unsafeRunSync()

    result.length shouldBe 5
    result.foreach(num => num should (be >= 0 and be < 100))
  }
}
```

This example uses ScalaTest for test organization and assertion, and Cats Effect's `IO` for managing the asynchronous code. Make sure you have the necessary dependencies in your build configuration to use ScalaTest and Cats Effect. The tests cover various aspects of your `GameLogic` trait, including generating numbers, sorting results, parsing numbers to results, and generating random numbers.

Note: Depending on the versions of the libraries you're using, you might need to adjust the import statements or make minor modifications to the code.

---

**User:**

Co robi / oznacza linijka behavior of "GameLogic"

---

**Assistant:**

Linijka `behavior of "GameLogic"` jest częścią kodu testów jednostkowych napisanych przy użyciu frameworka do testowania o nazwie ScalaTest. Ta linijka definiuje opis zachowania testów dla konkretnej części kodu lub klasy, w tym przypadku dla klasy `GameLogic`.

W kontekście testowania w ScalaTest, metoda `behavior of` jest używana do tworzenia grupy testów, które koncentrują się na określonym zachowaniu. Możesz myśleć o tym jako o sposobie grupowania testów, które sprawdzają różne aspekty zachowania danej klasy lub komponentu.

Na przykład, w powyższym teście, używając `behavior of "GameLogic"`, tworzysz grupę testów, które będą dotyczyć zachowania klasy `GameLogic`. Wewnątrz tej grupy, poszczególne testy (zawarte w blokach `it should ...`) sprawdzają konkretne aspekty zachowania tej klasy, takie jak generowanie liczb, sortowanie wyników, parsowanie liczb na wyniki, generowanie losowych liczb itp.

Ogólnie rzecz biorąc, `behavior of` pomaga w organizacji i opisie testów, co może ułatwić zrozumienie, co dokładnie jest testowane w ramach danej klasy lub komponentu.