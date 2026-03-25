# Transformacja Either w Scala

**Data:** 2023-04-20

---

**User:**

W Scala przy użyciu funkcji traverse z cats jak z List[Either[String, Int]] zrobić Either[String, List[Int]]

---

**Assistant:**

Można użyć funkcji `traverse` z biblioteki Cats, która pozwala na transformację struktury składającej się z wartości będących monadami, na monadę składającą się z wartości.

Aby przeprowadzić transformację z `List[Either[String, Int]]` na `Either[String, List[Int]]`, należy wykorzystać `traverse` w kontekście `Either`. Przykład implementacji może wyglądać następująco:

```scala
import cats.implicits._

val myList: List[Either[String, Int]] = List(Right(1), Right(2), Left("Error"))

val result: Either[String, List[Int]] = myList.traverse {
  case Right(i) => Right(i)
  case Left(s) => Left(s)
}
```

W powyższym przykładzie wykorzystana jest metoda `traverse`, która przyjmuje jako argument funkcję, która transformuje elementy listy. W przypadku, gdy element jest typu `Right`, to zostanie on zwrócony bez zmian. Natomiast w przypadku `Left`, zostanie zwrócony błąd.

Po wykonaniu tej transformacji otrzymamy monadę `Either[String, List[Int]]`, która będzie zawierać listę wszystkich wartości `Right` lub pierwszy napotkany błąd `Left`.