# Zlicz wystąpienia elementu

**Data:** 2023-08-16

---

**User:**

Scala, zlicz ile razy dany element występuje w liście

---

**Assistant:**

Oczywiście! W języku Scala możesz zliczyć ile razy dany element występuje w liście za pomocą różnych podejść. Oto kilka sposobów:

1. Użycie metody `count`:

```scala
val lista = List(1, 2, 3, 1, 4, 1, 5)
val element = 1
val iloscWystapien = lista.count(_ == element)
println(s"Element $element występuje $iloscWystapien razy w liście.")
```

2. Użycie funkcji `foldLeft`:

```scala
val lista = List(1, 2, 3, 1, 4, 1, 5)
val element = 1
val iloscWystapien = lista.foldLeft(0)((acc, el) => if (el == element) acc + 1 else acc)
println(s"Element $element występuje $iloscWystapien razy w liście.")
```

3. Użycie funkcji `groupBy` i mapowania wyników:

```scala
val lista = List(1, 2, 3, 1, 4, 1, 5)
val element = 1
val grupowane = lista.groupBy(identity)
val iloscWystapien = grupowane.getOrElse(element, Nil).size
println(s"Element $element występuje $iloscWystapien razy w liście.")
```

4. Użycie rekurencji:

```scala
def zliczWystapienia(lista: List[Int], element: Int): Int = {
  lista match {
    case Nil => 0
    case head :: tail => (if (head == element) 1 else 0) + zliczWystapienia(tail, element)
  }
}

val lista = List(1, 2, 3, 1, 4, 1, 5)
val element = 1
val iloscWystapien = zliczWystapienia(lista, element)
println(s"Element $element występuje $iloscWystapien razy w liście.")
```

Każda z tych metod osiąga ten sam rezultat, ale może mieć różnice w wydajności i czytelności kodu. Wybierz tę, która najlepiej odpowiada twoim preferencjom i wymaganiom projektu.

---

**User:**

Scala, zlicz ile razy każdy element występuje w liście

---

**Assistant:**

Oczywiście! Możesz zliczyć, ile razy każdy element występuje w liście w języku Scala za pomocą różnych podejść. Oto kilka sposobów:

1. Użycie metody `groupBy` i mapowania wyników:

```scala
val lista = List(1, 2, 3, 1, 4, 1, 5)
val grupowane = lista.groupBy(identity)
val wystapienia = grupowane.mapValues(_.size)
println(s"Wystąpienia poszczególnych elementów: $wystapienia")
```

2. Użycie pętli `for`:

```scala
val lista = List(1, 2, 3, 1, 4, 1, 5)
val wystapienia = scala.collection.mutable.Map.empty[Int, Int].withDefaultValue(0)

for (element <- lista) {
  wystapienia(element) += 1
}

println(s"Wystąpienia poszczególnych elementów: $wystapienia")
```

3. Użycie funkcji `foldLeft`:

```scala
val lista = List(1, 2, 3, 1, 4, 1, 5)
val wystapienia = lista.foldLeft(Map.empty[Int, Int].withDefaultValue(0)) { (acc, element) =>
  acc.updated(element, acc(element) + 1)
}

println(s"Wystąpienia poszczególnych elementów: $wystapienia")
```

4. Użycie rekurencji:

```scala
def zliczWystapienia(lista: List[Int], wynik: Map[Int, Int]): Map[Int, Int] = {
  lista match {
    case Nil => wynik
    case head :: tail =>
      val aktualnyWynik = wynik.updated(head, wynik(head) + 1)
      zliczWystapienia(tail, aktualnyWynik)
  }
}

val lista = List(1, 2, 3, 1, 4, 1, 5)
val wystapienia = zliczWystapienia(lista, Map.empty.withDefaultValue(0))
println(s"Wystąpienia poszczególnych elementów: $wystapienia")
```

Każda z tych metod pozwala zliczyć wystąpienia każdego elementu w liście. Wybierz tę, która najlepiej pasuje do twoich preferencji i wymagań projektu.