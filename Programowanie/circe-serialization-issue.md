# Circe Serialization Issue

**Data:** 2023-08-22

---

**User:**

Dlaczego taka hierarchia
  class GeneralWebSocketMsg(message_type: String)
  case class WebSocketResult(results: List[GameResult]) extends GeneralWebSocketMsg("response.results")

gdy jest parsowana przez circe, zwraca json bez message_type:response.results

---

**Assistant:**

To, co opisałeś, wygląda na kod napisany w języku Scala, który korzysta z biblioteki Circe do serializacji i deserializacji danych JSON. Obejmuje to definicję klasy `GeneralWebSocketMsg` oraz przypadku klasy `WebSocketResult`, które dziedziczą po niej.

Przyjrzyjmy się kodowi, który podałeś:

```scala
class GeneralWebSocketMsg(message_type: String)
case class WebSocketResult(results: List[GameResult]) extends GeneralWebSocketMsg("response.results")
```

W tym kodzie jest tworzona hierarchia klas dziedziczących po sobie. `GeneralWebSocketMsg` jest klasą bazową, która ma jedno pole konstruktora `message_type` typu String. Klasa `WebSocketResult` dziedziczy po `GeneralWebSocketMsg` i jest przypadkiem klasy, który zawiera listę `results` typu `List[GameResult]`.

Problem, który opisałeś, dotyczy prawdopodobnie procesu serializacji do formatu JSON za pomocą biblioteki Circe. Wygląda na to, że chciałbyś, aby w wynikowym JSONie była zawarta wartość pola `message_type` zdefiniowanego w klasie `GeneralWebSocketMsg`. Jednak domyślnie Circe nie serializuje prywatnych pól konstruktorów do JSONu.

Możesz to rozwiązać na kilka sposobów:

1. **Ustaw pole jako `val` lub `var`**: Zamiast definiować pole `message_type` jako argument konstruktora, możesz zrobić je polem klasy `GeneralWebSocketMsg`. To spowoduje, że pole będzie dostępne jako publiczne i Circe będzie je serializować.

   ```scala
   class GeneralWebSocketMsg(val message_type: String)
   case class WebSocketResult(results: List[GameResult]) extends GeneralWebSocketMsg("response.results")
   ```

2. **Użyj adnotacji `@JsonKey`**: Jeśli nie chcesz zmieniać dostępu do pola `message_type`, możesz skorzystać z adnotacji `@JsonKey` z Circe. Dzięki temu możesz określić, jakie pole JSONa odpowiada danemu polu klasy.

   ```scala
   import io.circe.{Json, KeyEncoder}
   import io.circe.generic.semiauto._

   class GeneralWebSocketMsg(message_type: String)
   object GeneralWebSocketMsg {
     implicit val keyEncoder: KeyEncoder[GeneralWebSocketMsg] = deriveKeyEncoder
   }

   case class WebSocketResult(results: List[GameResult]) extends GeneralWebSocketMsg("response.results")
   ```

3. **Niestandardowa serializacja**: Możesz również napisać niestandardowy serializer w Circe dla klasy `GeneralWebSocketMsg`, jeśli chcesz mieć pełną kontrolę nad procesem serializacji.

Ostatecznie wybór zależy od Twoich preferencji i ogólnego projektu, nad którym pracujesz.

---

**User:**

Podaj przykład rozwiązania nr 2

---

**Assistant:**

Oczywiście, poniżej znajdziesz przykład wykorzystania adnotacji `@JsonKey` z biblioteką Circe, aby skonfigurować niestandardową serializację dla pola `message_type` w klasie `GeneralWebSocketMsg`.

```scala
import io.circe._
import io.circe.syntax._
import io.circe.generic.semiauto._

class GeneralWebSocketMsg(@JsonKey("message_type") val messageType: String)

object GeneralWebSocketMsg {
  implicit val encoder: Encoder[GeneralWebSocketMsg] = deriveEncoder
}

case class GameResult(name: String) // Przykład klasy GameResult

case class WebSocketResult(results: List[GameResult]) extends GeneralWebSocketMsg("response.results")

object WebSocketResult {
  implicit val encoder: Encoder[WebSocketResult] = deriveEncoder
}

object CirceExample extends App {
  val gameResults = List(GameResult("Result 1"), GameResult("Result 2"))
  val webSocketResult = WebSocketResult(gameResults)

  println(webSocketResult.asJson)
}
```

W tym przykładzie korzystamy z adnotacji `@JsonKey("message_type")` nad polem `messageType` w klasie `GeneralWebSocketMsg`. Dzięki temu przy serializacji Circe użyje nazwy "message_type" w JSONie.

Pamiętaj, że powyższy kod jest tylko ilustracją sposobu wykorzystania adnotacji `@JsonKey` w Circe. W rzeczywistych projektach konfiguracja może być bardziej złożona, w zależności od potrzeb i struktury danych.