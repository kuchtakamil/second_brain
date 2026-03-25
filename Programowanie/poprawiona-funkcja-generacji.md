# Poprawiona funkcja generacji.

**Data:** 2023-08-21

---

**User:**

Scala, popraw
    def generatePlayersWithNumbers(playerNumber: Int): Either[String, F[List[PlayerWithNumber]]] = playerNumber match {
      case _ > 0 => Right(randomFor(playerNumber))
      case _     => Left("Number of players has to be positive")
    }

---

**Assistant:**

Oczywiście, oto poprawiona wersja kodu:

```scala
import cats.data.EitherT
import cats.effect.Sync
import cats.syntax.all._

def generatePlayersWithNumbers[F[_]: Sync](playerNumber: Int): F[Either[String, List[PlayerWithNumber]]] = {
  if (playerNumber > 0)
    randomFor(playerNumber).map(Right.apply)
  else
    Sync[F].pure(Left("Number of players has to be positive"))
}
```

W poprawionej wersji dokonałem następujących zmian:

1. Importowałem klasę `cats.effect.Sync` i składnię `cats.syntax.all._`, ponieważ używamy klas z biblioteki Cats.
2. Zmieniłem typ zwracany przez funkcję na `F[Either[String, List[PlayerWithNumber]]]`, gdzie `F[_]` to abstrakcyjny efekt, który można wybrać, na przykład `IO`, jeśli korzystasz z biblioteki Cats Effect.
3. Zastosowałem konstrukcję `if`/`else` zamiast `match`, ponieważ jest to bardziej zwięzły sposób obsługi warunków.
4. Użyłem `Sync[F].pure` do opakowania wyniku w efekt `F`, co jest ważne w kontekście obsługi efektów w asynchronicznych operacjach.

Upewnij się, że dostosowujesz importy i kontekst efektów do swojego projektu, w zależności od używanych bibliotek i kontekstu, w jakim pracujesz.

---

**User:**

chcę użyć patter matching i sprawdzić w pierwszym case czy matchowana liczba jest większa od 0

---

**Assistant:**

Oczywiście, jeśli chcesz użyć pattern matching i sprawdzić, czy liczba jest większa od 0, możesz to zrobić w następujący sposób:

```scala
import cats.data.EitherT
import cats.effect.Sync
import cats.syntax.all._

def generatePlayersWithNumbers[F[_]: Sync](playerNumber: Int): F[Either[String, List[PlayerWithNumber]]] = {
  playerNumber match {
    case n if n > 0 => randomFor(n).map(Right.apply)
    case _ => Sync[F].pure(Left("Number of players has to be positive"))
  }
}
```

W tym przypadku używamy pattern matchingu w pierwszym przypadku (`case n if n > 0`) w celu wykonania warunkowej akcji w zależności od tego, czy liczba `playerNumber` jest większa od 0.