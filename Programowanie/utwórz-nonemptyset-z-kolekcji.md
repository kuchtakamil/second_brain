# Utwórz NonEmptySet z kolekcji.

**Data:** 2023-05-01

---

**User:**

W jaki sposób utworzyć cats.NonEmptySet na podstawie kolekcji Set lub List lub Array

---

**Assistant:**

W języku Scala, aby utworzyć cats.NonEmptySet na podstawie istniejącej kolekcji typu Set, List lub Array, możesz skorzystać z następujących metod:

1. Dla kolekcji Set:

```scala
import cats.data.NonEmptySet

val mySet = Set(1, 2, 3, 4, 5)
val myNonEmptySet = NonEmptySet.fromSet(mySet).get
```

Metoda `NonEmptySet.fromSet` utworzy obiekt `NonEmptySet` na podstawie istniejącego zbioru `Set`. Metoda zwraca `Option`, ponieważ `Set` może być pusty i wtedy nie można utworzyć `NonEmptySet`. Wywołanie `.get` na wyniku tej metody spowoduje rzucenie wyjątku, jeśli `Set` jest pusty.

2. Dla kolekcji List:

```scala
import cats.data.NonEmptySet

val myList = List(1, 2, 3, 4, 5)
val myNonEmptySet = NonEmptySet.fromList(myList).get
```

Metoda `NonEmptySet.fromList` utworzy obiekt `NonEmptySet` na podstawie istniejącej listy `List`. Metoda zwraca `Option`, ponieważ `List` może być pusta i wtedy nie można utworzyć `NonEmptySet`. Wywołanie `.get` na wyniku tej metody spowoduje rzucenie wyjątku, jeśli `List` jest pusta.

3. Dla kolekcji Array:

```scala
import cats.data.NonEmptySet

val myArray = Array(1, 2, 3, 4, 5)
val myNonEmptySet = NonEmptySet.fromSet(myArray.toSet).get
```

Podobnie jak w przypadku `Set`, możesz skonwertować tablicę na zbiór za pomocą metody `toSet`, a następnie użyć metody `NonEmptySet.fromSet`, aby utworzyć obiekt `NonEmptySet`. Możesz również wykorzystać metodę `NonEmptySet.fromIterable`, która działa dla dowolnej kolekcji, ale może wymagać dodatkowej konwersji typów.

---

**User:**

fromSet przyjmuje SortedSet a nie Set. Jak więc zrrobić SrortedSet z Set a później NonEmptySet?

---

**Assistant:**

Tak, masz rację, metoda `fromSet` zdefiniowana w klasie `NonEmptySet` przyjmuje `SortedSet`, a nie `Set`.

Aby utworzyć `SortedSet` na podstawie istniejącego `Set`, możesz użyć metody `sorted` dostępnej na `Set`, która zwraca `SortedSet` posortowany w naturalnym porządku elementów:

```scala
import cats.data.NonEmptySet

val mySet = Set(1, 2, 3, 4, 5)
val mySortedSet = mySet.toSeq.sorted.to(Set)
val myNonEmptySet = NonEmptySet.fromSet(mySortedSet).get
```

Najpierw konwertujemy `Set` na sekwencję (`Seq`) za pomocą metody `toSeq`, a następnie sortujemy tę sekwencję przy użyciu metody `sorted`. Następnie konwertujemy posortowaną sekwencję na `Set` za pomocą metody `to(Set)`, aby otrzymać `SortedSet`. Na końcu wykorzystujemy metodę `fromSet` klasy `NonEmptySet`, aby utworzyć obiekt `NonEmptySet`.

Pamiętaj, że metoda `fromSet` zwraca `Option[NonEmptySet[A]]`, więc zalecam użycie metody `.get` tylko wtedy, gdy jesteś pewny, że zbiór wejściowy nie jest pusty. W przeciwnym razie lepiej jest obsłużyć ten przypadek w bezpieczny sposób, na przykład używając `Option.fold`.

---

**User:**

A jak zrobić SortedSet z Array?

---

**Assistant:**

Aby utworzyć `SortedSet` na podstawie istniejącej tablicy `Array`, możesz użyć metody `sorted` dostępnej na `Array`, która zwraca `Array` posortowany w naturalnym porządku elementów, a następnie skonwertować go na `SortedSet`:

```scala
import scala.collection.immutable.SortedSet
import scala.math.Ordering.Implicits._

val myArray = Array(1, 3, 2, 5, 4)
val mySortedSet = SortedSet(myArray.sorted: _*)
```

Najpierw sortujemy tablicę za pomocą metody `sorted` i następnie wywołujemy konstruktor `SortedSet`, który przyjmuje sekwencję elementów jako argument. Aby przekonwertować posortowaną tablicę na sekwencję elementów, musimy dodać `:_*` do końca tablicy, co powoduje rozwinięcie tablicy do sekwencji.

Ponieważ `SortedSet` jest podtypem `Set`, możesz następnie użyć metody `NonEmptySet.fromSet`, aby utworzyć obiekt `NonEmptySet`:

```scala
import cats.data.NonEmptySet

val myNonEmptySet = NonEmptySet.fromSet(mySortedSet).get
```

Ponownie, pamiętaj, że metoda `fromSet` zwraca `Option[NonEmptySet[A]]`, więc zalecam użycie metody `.get` tylko wtedy, gdy jesteś pewny, że zbiór wejściowy nie jest pusty.

---

**User:**

Jak przekształcić tą linijkę
    val deviceTypes: NonEmptySet[Nothing] =
      NonEmptySet.fromSet(args(0).split(",").toSet.map(_.trim).toSeq.sorted.to(Set)).get

aby uzyskać rezultat typu NonEmptySet[String] 

---

**Assistant:**

Aby uzyskać wynik typu `NonEmptySet[String]` zamiast `NonEmptySet[Nothing]`, musisz zmienić typ argumentu wejściowego do metody `fromSet` z `Set[Nothing]` na `Set[String]`. Możesz to zrobić poprzez zastosowanie metody `map` na wyniku metody `split`, która zamieni wszystkie elementy na typ `String`:

```scala
val deviceTypes: NonEmptySet[String] =
  NonEmptySet.fromSet(args(0).split(",").map(_.trim).toSet)(Ordering[String]).get
```

Tutaj używamy konstruktora `Ordering[String]`, aby dostarczyć porządek elementów do utworzenia `NonEmptySet`. Dzięki temu, gdy zostanie utworzony `NonEmptySet`, elementy będą już posortowane w naturalnym porządku typu `String`.

Zauważ, że można również pominąć konwersję na `Seq`, a po prostu utworzyć `SortedSet` z użyciem `toSet`:

```scala
val deviceTypes: NonEmptySet[String] =
  NonEmptySet.fromSet(args(0).split(",").map(_.trim).toSet)(Ordering[String]).get
```

---

**User:**

Podany kod nie działa i wyrzuca 
found   : [B >: String]scala.collection.immutable.Set[B]
 required: scala.collection.immutable.SortedSet[?]

---

**Assistant:**

Przepraszam za poprzednią odpowiedź, wygląda na to, że popełniłem błąd. Aby uzyskać `SortedSet` z `Set`, należy utworzyć instancję `SortedSet` z zastosowaniem dostarczonego `Ordering`. Można to zrobić na przykład w ten sposób:

```scala
import scala.collection.immutable.SortedSet
import scala.math.Ordering.Implicits._

val set = Set("b", "c", "a")
val sortedSet = SortedSet.empty[String] ++ set
```

W powyższym przykładzie tworzymy pusty `SortedSet` typu `String`, a następnie dodajemy do niego wszystkie elementy z istniejącego zbioru `set`. Konwersja z `Set` na `SortedSet` następuje wtedy, gdy używamy operatora `++` między `SortedSet` a `Set`.

Aby utworzyć `NonEmptySet` z `SortedSet`, możesz użyć metody `fromSet` tak samo, jak w poprzedniej odpowiedzi:

```scala
import cats.data.NonEmptySet

val nonEmptySet = NonEmptySet.fromSet(sortedSet).get
```

Ten kod utworzy `NonEmptySet` z `SortedSet` o elementach typu `String`. Pamiętaj, że ponieważ metoda `fromSet` zwraca `Option[NonEmptySet[A]]`, należy zawsze sprawdzić, czy wynik nie jest pusty przed użyciem metody `.get`.