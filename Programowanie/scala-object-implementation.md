# Scala Object Implementation

**Data:** 2023-03-03

---

**User:**

Popraw kod w Scala
case class Cat()
case class Dog()

trait Says[A]{
  def say(a: A): String
  def somethingElse(a: A): String
}
val dogSays: Says[Dog] =
  a => "Woof"
val catSays: Says[Cat] =
  a => "Meow"



---

**Assistant:**

Oto poprawiony kod w Scala:

```scala
case class Cat()
case class Dog()

trait Says[A] {
  def say(a: A): String
  def somethingElse(a: A): String
}

val dogSays: Says[Dog] = new Says[Dog] {
  override def say(a: Dog): String = "Woof"
  override def somethingElse(a: Dog): String = "Something else"
}

val catSays: Says[Cat] = new Says[Cat] {
  override def say(a: Cat): String = "Meow"
  override def somethingElse(a: Cat): String = "Something else"
}
```

W celu poprawnego zdefiniowania obiektów typu `Says`, należy dostarczyć implementację metod `say` i `somethingElse`. Dlatego, dla typów `Dog` i `Cat` powinny zostać zdefiniowane osobne obiekty `Says` z odpowiednimi implementacjami metod. W przypadku, gdybyśmy chcieli użyć wyrażenia lambda, to możemy użyć konkretnej metody zdefiniowanej w obiekcie `Says` za pomocą notacji z kropką. Przykład:
```scala
val dogSays: Says[Dog] = (a: Dog) => dogSays.say(a)
``` 
Jednak, w powyższym kodzie, obiekty `Says` zostały zdefiniowane przez klasy anonimowe, które implementują odpowiednie metody.

---

**User:**

W języku Scala w jakim celu stosuje się pojedyncze wyrażenie case zawarte np. w funkcji map?

---

**Assistant:**

Pojedyncze wyrażenie `case` w funkcji `map` w języku Scala służy do destrukturyzacji wartości w kolekcji i zastosowania do nich określonej funkcji. Jest to sposób na wygodne i czytelne mapowanie elementów kolekcji.

Przykładowo, jeśli mamy kolekcję zawierającą obiekty typu `Person` i chcemy utworzyć nową kolekcję zawierającą nazwiska osób z oryginalnej kolekcji, to możemy to zrobić za pomocą metody `map` i wykorzystując pojedyncze wyrażenie `case`:

```scala
case class Person(firstName: String, lastName: String)

val people = List(
  Person("John", "Doe"),
  Person("Jane", "Doe")
)

val lastNames = people.map {
  case Person(_, lastName) => lastName
}

println(lastNames) // prints: List(Doe, Doe)
```

W powyższym przykładzie wyrażenie `case` destrukturyzuje obiekty typu `Person` i przypisuje nazwiska do zmiennej `lastName`. Dzięki temu wewnątrz bloku wyrażeń można wykorzystać tylko tę zmienną, a pozostałe wartości będą ignorowane.

---

**User:**

podaj więcej przykładów kodu

---

**Assistant:**

Oto kilka dodatkowych przykładów użycia pojedynczego wyrażenia `case` w funkcji `map` w języku Scala:

1. Mapowanie elementów kolekcji typu `Option`:
```scala
val maybeNumbers = List(Some(1), None, Some(3))

val squaredNumbers = maybeNumbers.map {
  case Some(n) => n * n
  case None => 0
}

println(squaredNumbers) // prints: List(1, 0, 9)
```

2. Mapowanie elementów kolekcji zagnieżdżonych typów:
```scala
case class Order(id: Int, items: List[String])

val orders = List(
  Order(1, List("apple", "orange")),
  Order(2, List("banana"))
)

val orderItemCounts = orders.map {
  case Order(_, items) => items.size
}

println(orderItemCounts) // prints: List(2, 1)
```

3. Mapowanie elementów kolekcji zawierającej krotki:
```scala
val tuples = List((1, "one"), (2, "two"), (3, "three"))

val reversedTuples = tuples.map {
  case (n, s) => (s, n)
}

println(reversedTuples) // prints: List((one,1), (two,2), (three,3))
```

4. Mapowanie elementów kolekcji, której typ jest zdefiniowany za pomocą adnotacji `sealed trait` i `case class`:
```scala
sealed trait Animal
case class Dog(name: String) extends Animal
case class Cat(name: String) extends Animal

val animals = List(Dog("Fido"), Cat("Fluffy"), Dog("Rufus"))

val animalNames = animals.map {
  case Dog(name) => name
  case Cat(name) => name
}

println(animalNames) // prints: List(Fido, Fluffy, Rufus)
```

W każdym z powyższych przypadków, wyrażenie `case` służy do wyodrębnienia potrzebnych wartości z elementów kolekcji i przekazania ich do funkcji mapującej.