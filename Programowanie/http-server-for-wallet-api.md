# HTTP server for wallet API.

**Data:** 2023-04-20

---

**User:**

import cats.effect.{ExitCode, IO, IOApp}
import com.comcast.ip4s._
import org.http4s.{HttpApp, HttpRoutes}
import org.http4s.ember.server.EmberServerBuilder
import org.http4s.server.middleware.ErrorHandling
import org.http4s.server.websocket.WebSocketBuilder2
import org.http4s.dsl.io._
import org.http4s.implicits._

import scala.concurrent.ExecutionContext

// Complete all TODOs below according to their description.

object Protocol {
  // TODO Define ADT representing `Transaction`. It should have the following fields:
  //  * `playerId` — the id of a player, which initiated the transaction;
  //  * `deltaAmount` — the delta amount, can be either positive (for credits) or negative (for debits).
  //  `Transaction` should be representable with the following JSON:
  //  {
  //    "playerId": "player12345",
  //    "deltaAmount": 12.34
  //  }

  // TODO Define ADT representing `Balance`. It should have the following fields:
  //  * `playerId` — the id of a player, which the balance belongs to;
  //  * `balanceAmount` — the current balance amount;
  //  * `updatedAt` — the timestamp the balance has been last updated at.
  //  `Balance` should be representable with the following JSON:
  //  {
  //    "playerId": "player12345",
  //    "balanceAmount": 123.45,
  //    "updatedAt": "2021-11-02T20:12:44.697Z"
  //  }
}

object ProtocolFormat {
  // TODO Implement JSON encoders and decoders for ADTs that are defined in `Protocol`.
}

object WalletServer extends IOApp {

  private[bootcamp] def httpApp: IO[WebSocketBuilder2[IO] => HttpApp[IO]] =
    IO.pure { wsb =>
      ErrorHandling {
        HttpRoutes.of[IO] {
          case POST -> Root / "transaction" =>
            // TODO Implement HTTP POST route that accepts `Transaction`, encoded as JSON in the request body.
            //  If the request is valid, HTTP status 202 Accepted should be returned with an empty body. The
            //  received `Transaction` should be processed by adding its delta amount to the current balance
            //  of the player and streaming the updated balance via "/balance" route. If the request is
            //  invalid for any reason, HTTP status 400 Bad Request should be returned with an empty body.
            ???

          case GET -> Root / "balance" =>
            // TODO Implement WebSocket route that streams updated `Balance` instances to all clients upon
            //  each valid `Transaction`, received via "/transaction" HTTP POST route.
            ???
        }.orNotFound
      }
    }

  override def run(args: List[String]): IO[ExitCode] =
    httpApp.flatMap {
      EmberServerBuilder
        .default[IO]
        .withHost(ipv4"127.0.0.1")
        .withPort(port"9001")
        .withHttpWebSocketApp(_)
        .build
        .useForever
    }
}

---

**Assistant:**

The code provided is an incomplete skeleton of an HTTP server that implements a wallet API. The server allows clients to submit transactions that adjust player balances and to receive updates to the current balances of all players in real-time via websockets.

Below are the TODOs that need to be completed:

```scala
object Protocol {
  sealed trait Transaction
  // Define ADT representing `Transaction`. It should have the following fields:
  //  * `playerId` — the id of a player, which initiated the transaction;
  //  * `deltaAmount` — the delta amount, can be either positive (for credits) or negative (for debits).
  //  `Transaction` should be representable with the following JSON:
  //  {
  //    "playerId": "player12345",
  //    "deltaAmount": 12.34
  //  }
  final case class Credit(playerId: String, deltaAmount: Double) extends Transaction
  final case class Debit(playerId: String, deltaAmount: Double) extends Transaction

  final case class Balance(playerId: String, balanceAmount: Double, updatedAt: String)
  // TODO Define ADT representing `Balance`. It should have the following fields:
  //  * `playerId` — the id of a player, which the balance belongs to;
  //  * `balanceAmount` — the current balance amount;
  //  * `updatedAt` — the timestamp the balance has been last updated at.
  //  `Balance` should be representable with the following JSON:
  //  {
  //    "playerId": "player12345",
  //    "balanceAmount": 123.45,
  //    "updatedAt": "2021-11-02T20:12:44.697Z"
  //  }
}

object ProtocolFormat {
  import io.circe.{Encoder, Decoder}
  import io.circe.generic.semiauto._

  // TODO Implement JSON encoders and decoders for ADTs that are defined in `Protocol`.
  implicit val transactionEncoder: Encoder[Protocol.Transaction] = Encoder.instance {
    case Protocol.Credit(playerId, deltaAmount) => 
      Encoder.forProduct2("playerId", "deltaAmount")(c => (c.playerId, c.deltaAmount))(Credit.unapply)
    case Protocol.Debit(playerId, deltaAmount) => 
      Encoder.forProduct2("playerId", "deltaAmount")(d => (d.playerId, d.deltaAmount))(Debit.unapply)
  }

  implicit val transactionDecoder: Decoder[Protocol.Transaction] = Decoder.instance { cursor =>
    for {
      playerId <- cursor.downField("playerId").as[String]
      deltaAmount <- cursor.downField("deltaAmount").as[Double]
      transaction <- cursor.get[Option[String]]("type").flatMap {
        case Some("credit") => Right(Credit(playerId, deltaAmount))
        case Some("debit") => Right(Debit(playerId, deltaAmount))
        case Some(other) => Left(DecodingFailure(s"Invalid transaction type: $other", cursor.history))
        case None => Left(DecodingFailure(s"Missing transaction type", cursor.history))
      }
    } yield transaction
  }

  implicit val balanceEncoder: Encoder[Protocol.Balance] = deriveEncoder
  implicit val balanceDecoder: Decoder[Protocol.Balance] = deriveDecoder
}

object WalletServer extends IOApp {

  private[bootcamp] def httpApp: IO[WebSocketBuilder2[IO] => HttpApp[IO]] =
    IO.pure { wsb =>
      ErrorHandling {
        HttpRoutes.of[IO] {
          case req @ POST -> Root / "transaction" =>
            req.as

---

**User:**

dokończ WalletServer 

---

**Assistant:**

Sure, I can help you complete the `WalletServer` implementation. Here's the updated code with the TODOs completed:

```scala
import java.time.Instant

import cats.effect.{ExitCode, IO, IOApp}
import com.comcast.ip4s._
import io.circe.{Decoder, Encoder}
import io.circe.generic.semiauto.{deriveDecoder, deriveEncoder}
import org.http4s.{HttpApp, HttpRoutes}
import org.http4s.circe.{jsonEncoderOf, jsonOf}
import org.http4s.ember.server.EmberServerBuilder
import org.http4s.server.middleware.ErrorHandling
import org.http4s.server.websocket.WebSocketBuilder2
import org.http4s.dsl.io._
import org.http4s.implicits._
import org.http4s.websocket.WebSocketFrame
import fs2.concurrent.Queue

import scala.concurrent.ExecutionContext

// Define ADT representing `Transaction`
case class Transaction(playerId: String, deltaAmount: BigDecimal)
object Transaction {
  implicit val decoder: Decoder[Transaction] = deriveDecoder[Transaction]
  implicit val encoder: Encoder[Transaction] = deriveEncoder[Transaction]
}

// Define ADT representing `Balance`
case class Balance(playerId: String, balanceAmount: BigDecimal, updatedAt: Instant)
object Balance {
  implicit val decoder: Decoder[Balance] = deriveDecoder[Balance]
  implicit val encoder: Encoder[Balance] = deriveEncoder[Balance]
}

object WalletServer extends IOApp {

  private[bootcamp] def httpApp: IO[WebSocketBuilder2[IO] => HttpApp[IO]] = {
    val transactionQueue = Queue.unbounded[IO, Transaction]

   

---

**User:**

Napisz ponownie wyłącznie obiekt WalletServer 

---

**Assistant:**

Oczywiście, oto pełny kod obiektu `WalletServer` z wykonanymi TODO:

```scala
import java.time.Instant

import cats.effect.{ExitCode, IO, IOApp}
import com.comcast.ip4s._
import io.circe.{Decoder, Encoder}
import io.circe.generic.semiauto.{deriveDecoder, deriveEncoder}
import org.http4s.{HttpApp, HttpRoutes}
import org.http4s.circe.{jsonEncoderOf, jsonOf}
import org.http4s.ember.server.EmberServerBuilder
import org.http4s.server.middleware.ErrorHandling
import org.http4s.server.websocket.WebSocketBuilder2
import org.http4s.dsl.io._
import org.http4s.implicits._
import org.http4s.websocket.WebSocketFrame
import fs2.concurrent.Queue

import scala.concurrent.ExecutionContext

object WalletServer extends IOApp {

  // Define ADT representing `Transaction`
  case class Transaction(playerId: String, deltaAmount: BigDecimal)
  object Transaction {
    implicit val decoder: Decoder[Transaction] = deriveDecoder[Transaction]
    implicit val encoder: Encoder[Transaction] = deriveEncoder[Transaction]
  }

  // Define ADT representing `Balance`
  case class Balance(playerId: String, balanceAmount: BigDecimal, updatedAt: Instant)
  object Balance {
    implicit val decoder: Decoder[Balance] = deriveDecoder[Balance]
    implicit val encoder: Encoder[Balance] = deriveEncoder[Balance]
  }

  private[bootcamp] def httpApp: IO[WebSocketBuilder2[IO] => HttpApp[IO]] = {
    val transactionQueue = Queue.unbounded[IO, Transaction]

    IO.pure { wsb =>
      ErrorHandling {
        HttpRoutes.of[IO] {
          case req @ POST -> Root / "transaction" =>
            // Decode the incoming transaction from the request body
            val decoded: IO[Either[String, Transaction]] = req.as[Transaction].attempt.map {
              case Right(transaction) => Right(transaction)
              case Left(e) => Left(e.getMessage)
            }

            decoded.flatMap {
              case Right(transaction) =>
                // Enqueue the transaction for processing and respond with HTTP status 202 Accepted
                transactionQueue.enqueue1(transaction) *> Accepted()
              case Left(errorMsg) =>
                // Respond with HTTP status 400 Bad Request if the request is invalid
                BadRequest(errorMsg)
            }

          case GET -> Root / "balance" =>
            val balanceStream = transactionQueue.dequeue.scan(Balance("player12345", BigDecimal(0), Instant.now)) {
              case (balance, Transaction(playerId, deltaAmount)) =>
                // Calculate the new balance
                val newBalanceAmount = balance.balanceAmount + deltaAmount
                val newUpdatedAt = Instant.now
                Balance(playerId, newBalanceAmount, newUpdatedAt)
            }

            // Encode the stream of balance updates as a stream of WebSocket frames and return it as the HTTP response
            val balanceWebSocketStream = balanceStream.map(balance => WebSocketFrame.Text(balance.asJson.noSpaces))
            wsb.copy(onNonWebSocketRequest = httpApp => httpApp.orNotFound.map(_.asRight[WebSocketBuilder2[IO]]))
              .build(balanceWebSocketStream)
        }.orNotFound
      }
    }
  }

  override def run(args: List[String]): IO[ExitCode] =
    httpApp.flatMap {
      EmberServerBuilder
        .default[IO]
        .withHost(ipv4"127.0.0.1")
        .withPort(port"9001")
        .withHttpWebSocketApp(_)
        .build
        .useForever
    }
}
``` 

W kodzie zostały dodane dwie kl