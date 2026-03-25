# Błąd typu w kodzie

**Data:** 2023-08-22

---

**User:**

Scala, poniższy
            val receive: Pipe[F, WebSocketFrame, Unit] = _.evalMap {
              case WebSocketFrame.Text(message, _) =>
                Async[F].delay {
                  val json        = io.circe.parser.parse(message).getOrElse(Json.Null)
                  val messageType = json.hcursor.downField("message_type").as[String].getOrElse("")
                  val players     = json.hcursor.downField("players").as[Int].getOrElse(0)

                  if (messageType == "request.play") {
                    for {
                      gameResults <- gameAction.generateGameResultForPlayers(players)
                      responseJson = Printer.noSpaces.print(gameResults.asJson)
                      _           <- topic.publish1(responseJson)
                    } yield ()
                  }
                }

              case _ => Async[F].delay(println("Unknown"))
            }

 kod generuje błąd
type mismatch;
 found   : org.http4s.websocket.WebSocketFrame => F[_ >: Unit]
 required: org.http4s.websocket.WebSocketFrame => F[Any]
            val receive: Pipe[F, WebSocketFrame, Unit] = _.evalMap {

odpowiedz po polsku

---

**Assistant:**

Ten błąd wynika z niezgodności typów w wyrażeniu `evalMap`, które zostało użyte w kontekście definiowania wartości `receive`. Wygląda na to, że istnieje niezgodność pomiędzy oczekiwanym typem a rzeczywistym typem zwracanym przez blok funkcji wewnątrz `evalMap`.

Właściwa sygnatura dla `evalMap` jest taka:

```scala
def evalMap[A, B](f: A => F[B]): Pipe[F, A, B]
```

Oznacza to, że funkcja `f` (czyli blok kodu w tym przypadku) powinna przyjmować argument typu `A` (w tym przypadku `WebSocketFrame`) i zwracać wartość typu `F[B]` (gdzie `B` to rzeczywisty typ, który chcemy zwrócić). Jednak w kodzie, który dostarczyłeś, blok kodu wewnątrz `evalMap` zwraca typ `F[Unit]`.

Właściwe rozwiązanie zależy od tego, co dokładnie chcesz osiągnąć, ale jeśli chcesz zwrócić typ `F[Unit]`, musisz dostosować typy w deklaracji `receive` w ten sposób:

```scala
val receive: Pipe[F, WebSocketFrame, Unit] = _.evalMap {
  case WebSocketFrame.Text(message, _) =>
    Async[F].delay {
      val json        = io.circe.parser.parse(message).getOrElse(Json.Null)
      val messageType = json.hcursor.downField("message_type").as[String].getOrElse("")
      val players     = json.hcursor.downField("players").as[Int].getOrElse(0)

      if (messageType == "request.play") {
        for {
          gameResults <- gameAction.generateGameResultForPlayers(players)
          responseJson = Printer.noSpaces.print(gameResults.asJson)
          _           <- topic.publish1(responseJson)
        } yield ()
      } else {
        // Tutaj możesz również zwrócić jakąś wartość typu F[Unit] w przypadku innego messageType
        Async[F].unit
      }
    }

  case _ => Async[F].delay(println("Unknown"))
}
```

Ważne jest, aby upewnić się, że typ zwracany przez blok kodu wewnątrz `evalMap` jest zgodny z oczekiwanym typem zwracanym przez `evalMap`, tj. `F[Unit]` w tym przypadku.