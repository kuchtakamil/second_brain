# Scala mapN

**Data:** 2023-03-27

---

**User:**

W Scala podaj przykłady użycia funkcji mapN

---

**Assistant:**

Funkcja mapN jest dostępna w bibliotece Cats w języku Scala i pozwala zastosować funkcję na kombinacji wartości z kilku kontekstów.

Przykład użycia funkcji mapN:

```scala
import cats.implicits._

val a = Option(1)
val b = Option(2)
val c = Option(3)

val result = (a, b, c).mapN((x, y, z) => x + y + z)

println(result) // Output: Some(6)
```

W powyższym przykładzie zastosowano funkcję mapN na trójce wartości typu Option. W funkcji mapN, podano lambdę, która przyjmuje trzy argumenty (x, y, z) i zwraca ich sumę. W wyniku zastosowania funkcji mapN na wartościach a, b i c, otrzymujemy wynik Some(6), ponieważ wartości a, b i c zawierają po jednej wartości i funkcja lambda zostanie zastosowana na tych wartościach.

Można również zastosować funkcję mapN na kontenerach zawierających więcej niż jedną wartość, np. na listach:

```scala
import cats.implicits._

val list1 = List(1, 2, 3)
val list2 = List(10, 20, 30)

val result = (list1, list2).mapN((x, y) => x * y)

println(result) // Output: List(10, 40, 90)
```

W tym przykładzie, zastosowano funkcję mapN na dwóch listach. Funkcja