# Pattern Matching with Traits

**Data:** 2023-08-22

---

**User:**

Scala, dla takich klas
  case class GeneralWebSocketMsg(message_type: String)
  case class WebSocketResult(results: List[GameResult]) extends GeneralWebSocketMsg("response.results")
mam błąd
case class WebSocketResult has case ancestor com.onairentertainment.game.model.Model.GeneralWebSocketMsg, but case-to-case inheritance is prohibited. To overcome this limitation, use extractors to pattern match on non-leaf nodes.
  case class WebSocketResult(results: List[GameResult]) extends GeneralWebSocketMsg("response.results")


---

**Assistant:**

Wygląda na to, że napotkałeś na błąd związany z dziedziczeniem przypadków w języku Scala. Błąd ten występuje, gdy próbujesz dziedziczyć jedną przypadłość od drugiej za pomocą klasy potomnej. Przypadki do przypadków dziedziczyć nie mogą ze względu na pewne ograniczenia.

W Twoim przypadku chcesz, aby `WebSocketResult` dziedziczył po `GeneralWebSocketMsg`, co jest niemożliwe w przypadku klas przypadków. Jednakże można to osiągnąć, stosując wzorce wydobywające (ang. extractors) do dopasowywania wzorców na węzłach nie-końcowych. Wzorce wydobywające to specjalne obiekty, które pozwalają na dopasowywanie do wartości i przypisanie do nich wartości.

Oto jak można to poprawić, wykorzystując wzorce wydobywające:

```scala
trait GeneralWebSocketMsg {
  def message_type: String
}

case class WebSocketResult(results: List[GameResult]) extends GeneralWebSocketMsg {
  override def message_type: String = "response.results"
}

object GeneralWebSocketMsg {
  def unapply(arg: GeneralWebSocketMsg): Option[String] = Some(arg.message_type)
}
```

W tym przykładzie, zamiast dziedziczenia, używamy traitu `GeneralWebSocketMsg`, który definiuje jedynie pole `message_type`. W klasie `WebSocketResult` implementujemy ten trait i dostarczamy konkretne wartości dla tego pola. Dodatkowo, tworzymy obiekt towarzyszący `GeneralWebSocketMsg`, który definiuje wzorzec wydobywający `unapply`. To pozwala nam na dopasowywanie do obiektów, które implementują trait `GeneralWebSocketMsg`.

Następnie możesz użyć wzorca wydobywającego w następujący sposób:

```scala
val msg: GeneralWebSocketMsg = WebSocketResult(List(GameResult(...)))
msg match {
  case GeneralWebSocketMsg("response.results") =>
    println("Matched WebSocketResult with message type 'response.results'")
  case _ =>
    println("Did not match")
}
```

Ten kod powinien działać poprawnie i umożliwiać Ci uzyskanie oczekiwanych wyników związanych z dziedziczeniem przypadków w Scala.

---

**User:**

Dlaczego taka hierarchia
  case class GeneralWebSocketMsg(message_type: String)
  case class WebSocketResult(results: List[GameResult]) extends GeneralWebSocketMsg("response.results")

gdy jest parsowana przez circe, zwraca json bez message_type:response.results

---

**Assistant:**

Problem, który napotkałeś, może wynikać z faktu, że klasa `GeneralWebSocketMsg` jest przypadkiem klasy, a circe (biblioteka do przetwarzania JSON w języku Scala) obsługuje konwersje JSON dla klas, które nie są przypadkami.

Kiedy tworzysz instancję klasy `WebSocketResult`, przekazujesz argument `"response.results"` do konstruktora klasy nadrzędnej `GeneralWebSocketMsg`. Jednakże circe nie będzie w stanie poprawnie przekształcić tej struktury w JSON, ponieważ pola z klasy nadrzędnej nie są w pełni obsługiwane przez circe dla przypadków klas.

Aby to naprawić, możesz użyć wzorca, który zapewni poprawne zachowanie podczas konwersji JSON. Oto przykład, jak możesz to zrobić:

```scala
import io.circe._
import io.circe.syntax._
import io.circe.generic.semiauto._

sealed trait GeneralWebSocketMsg {
  def message_type: String
}

object GeneralWebSocketMsg {
  implicit val encoder: Encoder[GeneralWebSocketMsg] = deriveEncoder
  implicit val decoder: Decoder[GeneralWebSocketMsg] = deriveDecoder
}

case class WebSocketResult(results: List[GameResult]) extends GeneralWebSocketMsg {
  override def message_type: String = "response.results"
}

case class GameResult(...)  // Definicja GameResult

object WebSocketResult {
  implicit val encoder: Encoder[WebSocketResult] = deriveEncoder
  implicit val decoder: Decoder[WebSocketResult] = deriveDecoder
}
```

W tym przykładzie używamy circe do automatycznego generowania enkoderów (encoder) i dekoderów (decoder) dla klas `GeneralWebSocketMsg` i `WebSocketResult`. Dzięki temu circe będzie w stanie poprawnie przekształcić instancje tych klas w JSON i z powrotem.

Pamiętaj, że circe używa implicit conversions do automatycznego wykrywania enkoderów i dekoderów dla Twoich klas, dlatego konieczne może być umieszczenie ich w zakresie odpowiednich obiektów towarzyszących lub dostarczenie ich ręcznie, jeśli jest to konieczne.