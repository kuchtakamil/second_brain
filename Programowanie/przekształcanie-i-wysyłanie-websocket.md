# Przekształcanie i Wysyłanie WebSocket

**Data:** 2023-08-20

---

**User:**

Scala
Chcę odebrać komunikat websocket przekształcić (tutaj dodać " dada"do string)  i go odesłać w odpowiedzi. Popraw kod 
    def routes(ws: WebSocketBuilder2[F]): HttpRoutes[F] =
      HttpRoutes.of[F] { case GET -> Root / "ws" =>
        val receive: Pipe[F, WebSocketFrame, Unit] =
          _.collect { case WebSocketFrame.Text(message, _) =>
            val result = message + " dada"
      }

---

**Assistant:**

Oczywiście, poprawiony kod wyglądać będzie następująco:

```scala
import cats.effect.Sync
import fs2.Pipe
import org.http4s.HttpRoutes
import org.http4s.dsl.Http4sDsl
import org.http4s.server.websocket.WebSocketBuilder2
import org.http4s.websocket.WebSocketFrame

class MyRoutes[F[_]: Sync] extends Http4sDsl[F] {
  def routes(ws: WebSocketBuilder2[F]): HttpRoutes[F] =
    HttpRoutes.of[F] { case GET -> Root / "ws" =>
      val receive: Pipe[F, WebSocketFrame, Unit] =
        _.collect { case WebSocketFrame.Text(message, _) =>
          val result = message + " dada"
          // Tutaj możesz coś zrobić z przekształconym "result", np. przesłać dalej przez WebSocket
        }
      
      ws.build(receive = receive, send = _.map(_ => ???)) // Warto zaimplementować logikę wysyłania "result" przez WebSocket
    }
}
```

Kod został poprawiony o następujące rzeczy:
1. Dodano importy brakujących klas i typów, takich jak `Http4sDsl`, `WebSocketBuilder2`, `WebSocketFrame`, itp.
2. Wykorzystano konstruktor `ws.build` aby zbudować WebSocket przy użyciu funkcji odbierającej `receive` oraz przekształcającej `send`.
3. W miejscu `send` powinieneś zaimplementować logikę wysyłania przekształconego komunikatu przez WebSocket.

Upewnij się, że w miejscu `???` w linii `ws.build(receive = receive, send = _.map(_ => ???))` umieścisz odpowiednią logikę wysyłania przekształconego komunikatu przez WebSocket.

---

**User:**

ale w jaki sposób wysłać ten result?

---

**Assistant:**

Przepraszam za zamieszanie. Oczywiście, chętnie Ci pomogę. Aby wysłać przetworzony komunikat przez WebSocket, musisz skonfigurować funkcję `send` w `ws.build`. Oto poprawiony kod z dodaną logiką wysyłania przetworzonego komunikatu:

```scala
import cats.effect.Sync
import fs2.Pipe
import org.http4s.HttpRoutes
import org.http4s.dsl.Http4sDsl
import org.http4s.server.websocket.WebSocketBuilder2
import org.http4s.websocket.WebSocketFrame

class MyRoutes[F[_]: Sync] extends Http4sDsl[F] {
  def routes(ws: WebSocketBuilder2[F]): HttpRoutes[F] =
    HttpRoutes.of[F] { case GET -> Root / "ws" =>
      val receive: Pipe[F, WebSocketFrame, Unit] =
        _.collect { case WebSocketFrame.Text(message, _) =>
          val result = message + " dada"
          result
        }
      
      ws.build(receive = receive, send = _.map(result => WebSocketFrame.Text(result)))
    }
}
```

W tej linii: `ws.build(receive = receive, send = _.map(result => WebSocketFrame.Text(result)))` wykorzystujemy funkcję `send`, która transformuje przetworzony komunikat `result` do obiektu `WebSocketFrame.Text(result)` i przesyła go przez WebSocket.

Podczas wywoływania funkcji `ws.build`, funkcja `send` przyjmuje każdy element strumienia `result` i mapuje go na odpowiedni obiekt `WebSocketFrame`. W tym przypadku, przetworzony komunikat jest mapowany na `WebSocketFrame.Text(result)`, który jest następnie przesyłany przez WebSocket.