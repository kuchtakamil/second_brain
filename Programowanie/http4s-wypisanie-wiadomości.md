# http4s: wypisanie wiadomości

**Data:** 2023-05-05

---

**User:**

Wykorzystując http4s przekształć kod tak aby przy przyjmowaniu wiadomości, była ona jedynie wypisywana na ekran przy użyciu println
  private def httpApp(topic: Topic[IO, String], websocketEndpoint: String)(wsb: WebSocketBuilder2[IO]): HttpApp[IO] =
    HttpRoutes
      .of[IO] { case GET -> Root / "simvalue" =>
        wsb.build(
          receive = topic.publish.compose[Stream[IO, WebSocketFrame]](_.collect {
            case WebSocketFrame.Text(message, _) => message
          }),
          send = topic.subscribe(maxQueued = 10).map(WebSocketFrame.Text(_)),
        )
      }
      .orNotFound

---

**Assistant:**

Aby wypisać przychodzące wiadomości na ekranie przy użyciu `println`, możemy zmodyfikować ten kod w następujący sposób:

```scala
private def httpApp(topic: Topic[IO, String], websocketEndpoint: String)(wsb: WebSocketBuilder2[IO]): HttpApp[IO] =
  HttpRoutes
    .of[IO] { case GET -> Root / "simvalue" =>
      wsb.build(
        receive = topic.publish.compose[Stream[IO, WebSocketFrame]](_.collect {
          case WebSocketFrame.Text(message, _) => message
        }).evalMap(message => IO(println(message))), // wypisanie wiadomości przy użyciu println
        send = topic.subscribe(maxQueued = 10).map(WebSocketFrame.Text(_)),
      )
    }
    .orNotFound
```

Zmiany w tym kodzie to dodanie metody `evalMap` do strumienia otrzymywanych wiadomości, która wywołuje efekt uboczny, w tym przypadku wypisanie wiadomości przy użyciu `println`.

---

**User:**

Powyższy kod przy odbieraniu wiadomości, zwraca taką samą wiadomość. Działa jak echo. Przekształć ten kod tak aby zupełnie nic się nie działo przy odbieraniu wiadomości
  private def httpApp(topic: Topic[IO, String], websocketEndpoint: String)(wsb: WebSocketBuilder2[IO]): HttpApp[IO] =
    HttpRoutes
      .of[IO] { case GET -> Root / "simvalue" =>
        wsb.build(
          receive = topic.publish.compose[Stream[IO, WebSocketFrame]](_.collect {
            case WebSocketFrame.Text(message, _) => message
          }),
          send = topic.subscribe(maxQueued = 10).map(WebSocketFrame.Text(_)),
        )
      }
      .orNotFound

---

**Assistant:**

Aby nic nie działo się przy odbieraniu wiadomości, możemy usunąć przekształcenie strumienia odbieranych wiadomości, które jest wykonywane w wywołaniu `topic.publish.compose[Stream[IO, WebSocketFrame]](_.collect { case WebSocketFrame.Text(message, _) => message })`. Możemy po prostu przekazać strumień otrzymywanych wiadomości bez żadnych zmian. Ostatecznie, kod może wyglądać następująco:

```scala
private def httpApp(topic: Topic[IO, String], websocketEndpoint: String)(wsb: WebSocketBuilder2[IO]): HttpApp[IO] =
  HttpRoutes
    .of[IO] { case GET -> Root / "simvalue" =>
      wsb.build(
        receive = topic.publish,
        send = topic.subscribe(maxQueued = 10).map(WebSocketFrame.Text(_)),
      )
    }
    .orNotFound
```

W tym kodzie `topic.publish` jest bezpośrednio przekazywany jako strumień otrzymywanych wiadomości. Zwracany strumień otrzymywanych wiadomości będzie zawierał `WebSocketFrame` z różnymi typami wiadomości, w tym `Text`, `Binary`, `Close`, `Ping`, `Pong` i inne. Z drugiej strony, `topic.subscribe(maxQueued = 10).map(WebSocketFrame.Text(_))` nadal zwraca strumień `WebSocketFrame` z wiadomościami tekstowymi, które są publikowane przez `Topic`.