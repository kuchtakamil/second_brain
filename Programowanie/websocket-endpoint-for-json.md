# WebSocket Endpoint for JSON

**Data:** 2023-08-19

---

**User:**

Scala, EmberServerBuilder,
Chcę utworzyć endpoint websocket który może odebrać json np.
{
  "message_type": "request.play",
  "players": 3
}
i wywłać gameAction.generateGameResultForPlayers(3)
Uzupełnij
  def make[F[_]: Async](gameAction: GameAction[F]): WebSocket[F] = new WebSocket[F] {
    override def runWebSocketServer: Resource[F, Server] =
      EmberServerBuilder
        .default[F]
        .withHost(ipv4"127.0.0.1")
        .withPort(port"8080")
        .withHttpWebSocketApp(httpApp)
        .build

    private def httpApp()(wsb: WebSocketBuilder2[F]): HttpApp[F] =
      HttpRoutes
        .of[F] { case POST -> Root / "simvalue" =>
          wsb.build(
            receive = ???,
            send = ???,
          )
        }
        .orNotFound
  }

---

**Assistant:**

Certainly, I'll help you complete the code for creating a WebSocket endpoint that can receive a JSON payload and trigger the `gameAction.generateGameResultForPlayers` method. In the code you provided, you'll need to fill in the missing parts for handling WebSocket communication.

Here's how you can do it:

```scala
import cats.effect._
import org.http4s._
import org.http4s.dsl.Http4sDsl
import org.http4s.server.Server
import org.http4s.server.blaze.BlazeServerBuilder
import org.http4s.server.websocket.WebSocketBuilder2
import org.http4s.implicits._
import org.http4s.dsl.io._

case class GameAction[F[_]](generateGameResultForPlayers: Int => F[Unit])

object WebSocketServer {
  def make[F[_]: Async](gameAction: GameAction[F]): WebSocket[F] = new WebSocket[F] {
    override def runWebSocketServer: Resource[F, Server] =
      BlazeServerBuilder[F]
        .bindHttp(8080, "127.0.0.1")
        .withHttpWebSocketApp(httpApp(gameAction))
        .resource

    private def httpApp(gameAction: GameAction[F]): HttpApp[F] = {
      val dsl = new Http4sDsl[F]{}
      import dsl._
      
      HttpRoutes.of[F] {
        case req @ POST -> Root / "simvalue" =>
          WebSocketBuilder2[F].build(
            receive = { (ws: WebSocket[F], msg: String, close: F[Unit]) =>
              // Parse the incoming JSON message and extract relevant data
              val messageType = ??? // Parse messageType from the JSON
              val players = ??? // Parse players from the JSON

              if (messageType == "request.play") {
                gameAction.generateGameResultForPlayers(players).unsafeToFuture() // Trigger the game action
                // You can send a response back if needed
                ws.send("Game result generation initiated.").unsafeToFuture()
              } else {
                // Handle other message types if needed
                ws.send("Unknown message type.").unsafeToFuture()
              }
            },
            send = { (ws: WebSocket[F], msg: String) =>
              // Handle sending data to the client if needed
              // For example, ws.send("Response message").unsafeToFuture()
            },
          )
      }.orNotFound
    }
  }
}
```

Please note that you need to replace the placeholders (`???`) in the code with actual JSON parsing and handling logic. Additionally, remember to add error handling and other necessary components based on your application requirements. The provided code assumes you have a `GameAction` class with a method `generateGameResultForPlayers`.

---

**User:**

Scala, EmberServerBuilder,
Chcę utworzyć endpoint websocket który może odebrać json np.
{
  "message_type": "request.play",
  "players": 3
}
i wywłać gameAction.generateGameResultForPlayers(3). Funkcja ta zwraca również pewien obiekt, który można przekształcić do JSON i należy go wysłać w odpowiedzi.
Uzupełnij
  def make[F[_]: Async](gameAction: GameAction[F]): WebSocket[F] = new WebSocket[F] {
    override def runWebSocketServer: Resource[F, Server] =
      EmberServerBuilder
        .default[F]
        .withHost(ipv4"127.0.0.1")
        .withPort(port"8080")
        .withHttpWebSocketApp(httpApp)
        .build

    private def httpApp()(wsb: WebSocketBuilder2[F]): HttpApp[F] =
      HttpRoutes
        .of[F] { case POST -> Root / "simvalue" =>
          wsb.build(
            receive = ???,
            send = ???,
          )
        }
        .orNotFound
  }

---

**Assistant:**

Certainly, I'll help you complete the code to create a WebSocket endpoint that can receive a JSON payload, trigger the `gameAction.generateGameResultForPlayers` method, and send the resulting JSON object as a response. Here's how you can achieve this:

```scala
import cats.effect._
import org.http4s._
import org.http4s.dsl.Http4sDsl
import org.http4s.server.Server
import org.http4s.server.blaze.BlazeServerBuilder
import org.http4s.server.websocket.WebSocketBuilder2
import org.http4s.implicits._
import org.http4s.circe.CirceEntityEncoder._
import io.circe.syntax._

case class GameAction[F[_]](generateGameResultForPlayers: Int => F[GameResult])

case class GameResult(message: String)

object WebSocketServer {
  def make[F[_]: Async](gameAction: GameAction[F]): WebSocket[F] = new WebSocket[F] {
    override def runWebSocketServer: Resource[F, Server] =
      BlazeServerBuilder[F]
        .bindHttp(8080, "127.0.0.1")
        .withHttpWebSocketApp(httpApp(gameAction))
        .resource

    private def httpApp(gameAction: GameAction[F]): HttpApp[F] = {
      val dsl = new Http4sDsl[F]{}
      import dsl._
      
      HttpRoutes.of[F] {
        case req @ POST -> Root / "simvalue" =>
          wsb.build(
            receive = { (ws: WebSocket[F], msg: String, close: F[Unit]) =>
              // Parse the incoming JSON message and extract relevant data
              val json = io.circe.parser.parse(msg).getOrElse(Json.Null)
              val messageType = json.hcursor.downField("message_type").as[String].getOrElse("")
              val players = json.hcursor.downField("players").as[Int].getOrElse(0)

              if (messageType == "request.play") {
                for {
                  _ <- gameAction.generateGameResultForPlayers(players)
                  responseJson = GameResult("Game result generated").asJson
                  _ <- ws.send(responseJson.noSpaces)
                } yield ()
              } else {
                // Handle other message types if needed
                ws.send("Unknown message type").unsafeToFuture()
              }
            },
            send = { (ws: WebSocket[F], msg: String) =>
              // Handle sending data to the client if needed
              // For example, ws.send("Response message").unsafeToFuture()
            }
          )
      }.orNotFound
    }
  }
}
```

Please note that in the above code, I've used the `Circe` library for JSON parsing and encoding. Also, I've assumed that the `GameResult` class represents the result of the game action and can be encoded into JSON. Make sure to adjust the types and logic as per your application's specific requirements.