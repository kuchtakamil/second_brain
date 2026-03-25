# Dekodowanie JSON w Circe.

**Data:** 2023-03-12

---

**User:**

Wykorzystując język Scala i biblioteke Circe, jak rozwiązać problem polegający na tym że nazwy pół json różnią się od tych zawartych w modelu danych przez co nie może dojść do prawidłowego dekodowania. Nie można zmieniać nazw pól w pliku z danymi ani nazw pól w modelu danych.

---

**Assistant:**

Aby rozwiązać problem, można użyć adnotacji w Circe, które pozwalają na określenie niestandardowych nazw pól dla dekodowania i kodowania. Można to zrobić poprzez użycie adnotacji `@JsonKey` w modelu danych.

Na przykład, zakładając, że mamy następujący plik JSON:

```json
{
  "first_name": "John",
  "last_name": "Doe",
  "age": 30
}
```

A następnie chcemy zdekodować go na następujący model danych:

```scala
case class Person(firstName: String, lastName: String, age: Int)
```

Jednak nazwy pól w pliku JSON różnią się od tych w modelu danych. Aby zdekodować ten plik JSON, można dodać adnotacje `@JsonKey` w modelu danych, aby określić niestandardowe nazwy pól.

```scala
import io.circe.Decoder
import io.circe.generic.semiauto.deriveDecoder
import io.circe.generic.extras._

@ConfiguredJsonCodec
case class Person(
  @JsonKey("first_name") firstName: String,
  @JsonKey("last_name") lastName: String,
  age: Int
)

object Person {
  implicit val decoder: Decoder[Person] = deriveConfiguredDecoder[Person]
}
```

W powyższym przykładzie użyto adnotacji `@JsonKey` do określenia, że pole `firstName` w modelu danych ma zostać zdekodowane z pola `first_name` w pliku JSON, a pole `lastName` z pola `last_name`.

Następnie, przy użyciu funkcji `decode` z obiektu `io.circe.parser`, można zdekodować plik JSON do modelu danych:

```scala
import io.circe.parser.decode

val jsonStr = """{"first_name":"John","last_name":"Doe","age":30}"""
val result = decode[Person](jsonStr)

result match {
  case Right(person) => println(person)
  case Left(error) => println(s"Error decoding JSON: $error")
}
```

Wynik działania powyższego kodu powinien wyświetlić:

```
Person(John,Doe,30)
```

W ten sposób można zdekodować plik JSON, który ma niestandardowe nazwy pól, do modelu danych, który ma standardowe nazwy pól.