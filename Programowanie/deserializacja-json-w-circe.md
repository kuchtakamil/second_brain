# Deserializacja JSON w Circe.

**Data:** 2023-03-29

---

**User:**

W Scala przy pomocy Circe napisz kod wczytujący plik config.json i deserializujący go do klas

case class ConfigPayload(possibleRange: ValueRange, validRange: ValueRange, everyNSec: Int, avgDelta: Int)
case class ValueRange(from: Int, to: Int)
case class Simulator(carriageSpeed: ConfigPayload, bedTemp: ConfigPayload)

---

**Assistant:**

Oto przykładowy kod w języku Scala, który wykorzystuje bibliotekę Circe do wczytania pliku JSON i deserializacji go do klas.

```scala
import io.circe.parser.decode
import io.circe.generic.auto._

import scala.io.Source

// Odczytanie pliku JSON jako String
val jsonString = Source.fromResource("config.json").getLines().mkString

// Deserializacja JSON do klasy Simulator
val result = decode[Simulator](jsonString)

// Obsługa wyniku
result match {
  case Right(simulator) => println(simulator)
  case Left(error) => println(s"Error: $error")
}
```

Przyjmujemy, że plik `config.json` znajduje się w katalogu `resources` w projekcie. Następnie używamy metody `decode` z biblioteki Circe, która deserializuje JSON do klasy `Simulator`. Dekodowanie jest automatyczne dzięki adnotacji `@JsonCodec` nad klasami `ConfigPayload` i `ValueRange`.

W przypadku poprawnego deserializowania, otrzymujemy instancję klasy `Simulator`, którą można wykorzystać w dalszej części programu. W przeciwnym wypadku, wypisujemy informację o błędzie.