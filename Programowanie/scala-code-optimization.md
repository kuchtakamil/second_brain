# Scala code optimization.

**Data:** 2023-05-03

---

**User:**

Czy można napisać powyższy kod w bardziej idiomatyczny dla Scala sposób
      val eitherSimValue: Either[io.circe.Error, SimValue] = decode[SimValue](event.data.toString)
      val simValue                                         = eitherSimValue match {
        case Right(value) => value
        case Left(err)    => throw new RuntimeException(err)
      }
      simValue match {
        case cs: CarriageSpeed => carriageSpeedVar.update(_ => cs)
        case bt: BedTemperature => bedTemperatureValueVar.update(_ => bt)
      }

---

**Assistant:**

Tak, powyższy kod można napisać w bardziej idiomatyczny dla Scala sposób, wykorzystując wyrażenia dla mapowania i obsługi błędów. Oto, jak mógłby wyglądać taki kod:

```
import io.circe.parser.decode
import cats.implicits._

val simValue: SimValue = decode[SimValue](event.data.toString)
  .leftMap(err => new RuntimeException(err))
  .fold(throw _, identity)

simValue match {
  case cs: CarriageSpeed => carriageSpeedVar.update(_ => cs)
  case bt: BedTemperature => bedTemperatureValueVar.update(_ => bt)
}
```

W tym nowym kodzie wykorzystano bibliotekę `cats` do uzyskania wyrażenia `leftMap`, które służy do mapowania wartości typu `Either`. W przypadku wystąpienia błędu, wyjątek jest rzucony przez metodę `fold`, w przeciwnym razie zostaje zwrócona wartość `identity`. Zamiast używać wzorca dopasowania `case Right(value) => value` i `case Left(err) => throw new RuntimeException(err)`, użyto `fold` z metodą `identity` w celu zwrócenia prawidłowej wartości i rzuconia wyjątku w przypadku błędu.

---

**User:**

a czy można to wszystko zapisać używająć for comprehension?

---

**Assistant:**

Tak, można również wykorzystać for comprehension do bardziej zwięzłego zapisu tego kodu. Oto przykład, jak to może wyglądać:

```
import io.circe.parser.decode
import cats.implicits._

val simValue: SimValue = for {
  json <- decode[Json](event.data.toString).leftMap(new RuntimeException(_))
  simValue <- json.as[SimValue].leftMap(new RuntimeException(_))
} yield simValue

simValue match {
  case cs: CarriageSpeed => carriageSpeedVar.update(_ => cs)
  case bt: BedTemperature => bedTemperatureValueVar.update(_ => bt)
}
```

W tym kodzie, użyliśmy `for comprehension` w celu odczytania wartości `SimValue` z `Json`. Najpierw, wartość `Json` jest dekodowana z wykorzystaniem metody `decode` z biblioteki `io.circe`. Jeśli wystąpi błąd dekodowania, zostanie utworzony nowy wyjątek z komunikatem błędu i rzucony. Następnie, wartość `Json` zostaje skonwertowana na `SimValue` z wykorzystaniem metody `as`. Jeśli również wystąpi błąd, zostanie utworzony nowy wyjątek z komunikatem błędu i rzucony. W przypadku poprawnej konwersji, zwrócona zostanie wartość `SimValue`.

Na końcu, używając `match`, wartość `SimValue` jest dopasowana do odpowiedniego typu i przypisana do zmiennej w zależności od tego, jaki jest jej typ.

---

**User:**

ten kod nie kompiluje się w tym miejscu json.as[SimValue].leftMap

---

**Assistant:**

Mój błąd, przepraszam za pomyłkę. W rzeczywistości, `json.as[SimValue]` zwraca wartość typu `Either[io.circe.Error, SimValue]`, więc `leftMap` nie może być użyte w tym miejscu. Można jednak użyć `left.flatMap` do obsługi błędów w for comprehension. Oto poprawiona wersja kodu:

```
import io.circe.parser.decode
import cats.implicits._

val simValue: SimValue = (for {
  json <- decode[Json](event.data.toString).leftMap(new RuntimeException(_)).toEither
  simValue <- json.as[SimValue].leftMap(new RuntimeException(_)).toEither
} yield simValue).fold(throw _, identity)

simValue match {
  case cs: CarriageSpeed => carriageSpeedVar.update(_ => cs)
  case bt: BedTemperature => bedTemperatureValueVar.update(_ => bt)
}
```

W tym nowym kodzie, wykorzystano `toEither` do konwersji wartości `Left` i `Right` na wartość typu `Either`. W przypadku wystąpienia błędu, wartość typu `Left` zostanie utworzona z wyjątkiem `RuntimeException`. Następnie, wykorzystano `flatMap` zamiast `map` do obsługi błędów w for comprehension. Na końcu, użyto `fold` z metodą `identity` w celu zwrócenia prawidłowej wartości i rzuconia wyjątku w przypadku błędu.