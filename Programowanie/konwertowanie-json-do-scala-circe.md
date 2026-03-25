# Konwertowanie JSON do Scala - Circe

**Data:** 2023-05-09

---

**User:**

Scala i Circe. W jaki sposób w Circe mając obiekt typu JSON, utworzyć obiekt konkretnego typu w Scala?

---

**Assistant:**

Aby utworzyć obiekt konkretnego typu w Scala z obiektu typu JSON w Circe, możesz użyć mechanizmu "drukowania" (ang. "decoding") kodu JSON do struktury danych w Scala. 

Aby to zrobić, musisz najpierw zdefiniować klasę w Scala, która odzwierciedla strukturę JSON, którą chcesz zdekodować. Następnie musisz użyć mechanizmu dekodowania Circe, aby zdekodować JSON do obiektu Scala.

Na przykład, zakładając, że masz JSON o następującej postaci:

```
{
  "name": "John",
  "age": 30,
  "email": "john@example.com"
}
```

Możesz zadeklarować klasę w Scala, która reprezentuje tę strukturę JSON, na przykład:

```
case class Person(name: String, age: Int, email: String)
```

Następnie możesz zdekodować JSON do obiektu tej klasy, korzystając z mechanizmu dekodowania Circe:

```
import io.circe.parser.decode
import io.circe.generic.auto._

val json = """{
  "name": "John",
  "age": 30,
  "email": "john@example.com"
}"""

val result = decode[Person](json)
```

W ten sposób otrzymasz obiekt klasy `Person` o wartościach pól odpowiadających wartościom JSON. W przypadku powyższego przykładu, obiekt `result` będzie miał wartość:

```
Right(Person("John", 30, "john@example.com"))
```

Używając `decode` możesz też obsłużyć przypadki gdy JSON nie odpowiada strukturze twojej klasy, a w wyniku wystapi błąd dekodowania. W takim przypadku metoda `decode` zwróci błąd, który możesz obsłużyć zgodnie z wymaganiami twojego kodu.

---

**User:**

W podanym przykładzie nie ma obiektu typu JSON. Obiekt typu JSON tworzony jest np. z funkcji parse(someString). 

---

**Assistant:**

Masz rację, przepraszam za nieścisłość w mojej odpowiedzi. Aby zadeklarować obiekt typu JSON w Circe, możesz skorzystać z funkcji `parse` z pakietu `io.circe.parser`, która zamienia ciąg znaków zawierający kod JSON na obiekt `Json`. Przykładowo:

```
import io.circe.parser

val json: String = """{
  "name": "John",
  "age": 30,
  "email": "john@example.com"
}"""

val jsonParsed = parser.parse(json).getOrElse(Json.Null)
```

Następnie możesz użyć funkcji `as` na obiekcie `Json` z zadeklarowanym typem w Scala, aby przekonwertować JSON na obiekt Scala. Na przykład:

```
import io.circe.parser
import io.circe.generic.auto._

val json: String = """{
  "name": "John",
  "age": 30,
  "email": "john@example.com"
}"""

case class Person(name: String, age: Int, email: String)

val jsonParsed = parser.parse(json).getOrElse(Json.Null)

val result = jsonParsed.as[Person]
```

W ten sposób otrzymasz obiekt klasy `Person` o wartościach pól odpowiadających wartościom JSON. W przypadku powyższego przykładu, obiekt `result` będzie miał wartość:

```
Right(Person("John", 30, "john@example.com"))
```

Możesz też użyć mechanizmu dekodowania bezpośrednio na obiekcie `Json`, na przykład:

```
import io.circe.parser
import io.circe.generic.auto._
import io.circe.Json

val json: String = """{
  "name": "John",
  "age": 30,
  "email": "john@example.com"
}"""

case class Person(name: String, age: Int, email: String)

val jsonParsed = parser.parse(json).getOrElse(Json.Null)

val result = jsonParsed.as[Person]
```

W ten sposób otrzymasz obiekt klasy `Person` o wartościach pól odpowiadających wartościom JSON. W przypadku powyższego przykładu, obiekt `result` będzie miał wartość:

```
Right(Person("John", 30, "john@example.com"))
```