# Circe: implicitny dekoder Simulacji

**Data:** 2023-03-30

---

**User:**

Napraw błąd could not find implicit value for evidence parameter of type io.circe.Decoder[Generator.Simulator]

w poniższym kodzie
 
object Generator extends App {
  import io.circe.generic.JsonCodec
  @JsonCodec case class ConfigPayload(possibleRange: ValueRange, validRange: ValueRange, everyNSec: Int, avgDelta: Int)
  @JsonCodec case class ValueRange(from: Int, to: Int)
  @JsonCodec case class Simulator(carriageSpeed: ConfigPayload, bedTemp: ConfigPayload)
  val jsonString = Source.fromResource("config.json").getLines().mkString

  val result: Either[circe.Error, Simulator] = decode[Simulator](jsonString)
  result match {
    case Right(res) => println(res)
    case Left(_) => println("jeblo")
  }
}

---

**Assistant:**

Błąd "could not find implicit value for evidence parameter of type io.circe.Decoder[Generator.Simulator]" oznacza, że brakuje implicit dekodera (Decoder) dla typu Generator.Simulator. Aby rozwiązać ten problem, należy dodać implicit dekoder dla tego typu. Można to zrobić na kilka sposobów, na przykład:

1. Dodać implicit dekoder ręcznie:

```
implicit val simulatorDecoder: Decoder[Generator.Simulator] = deriveDecoder[Generator.Simulator]
```

2. Dodać implicit dekoder za pomocą macro:

```
object Generator extends App {
  import io.circe.generic.auto._
  import io.circe.parser.decode
  import io.circe.syntax._

  @JsonCodec case class ConfigPayload(possibleRange: ValueRange, validRange: ValueRange, everyNSec: Int, avgDelta: Int)
  @JsonCodec case class ValueRange(from: Int, to: Int)
  @JsonCodec case class Simulator(carriageSpeed: ConfigPayload, bedTemp: ConfigPayload)

  val jsonString = Source.fromResource("config.json").getLines().mkString

  val result = decode[Simulator](jsonString)
  result match {
    case Right(res) => println(res)
    case Left(_) => println("jeblo")
  }
}
```

3. Dodać implicit dekoder za pomocą implicit w klasie case:

```
object Generator extends App {
  import io.circe.generic.JsonCodec
  @JsonCodec case class ConfigPayload(possibleRange: ValueRange, validRange: ValueRange, everyNSec: Int, avgDelta: Int)
  @JsonCodec case class ValueRange(from: Int, to: Int)
  @JsonCodec case class Simulator(carriageSpeed: ConfigPayload, bedTemp: ConfigPayload)
  object Simulator {
    implicit val decoder: Decoder[Simulator] = deriveDecoder[Simulator]
  }

  val jsonString = Source.fromResource("config.json").getLines().mkString

  val result = decode[Simulator](jsonString)
  result match {
    case Right(res) => println(res)
    case Left(_) => println("jeblo")
  }
}
```

Każda z tych metod pozwoli na uzyskanie implicit dekodera dla typu Generator.Simulator i powinna rozwiązać problem.