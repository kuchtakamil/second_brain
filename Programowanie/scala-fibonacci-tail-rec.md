# Scala Fibonacci Tail Rec.

**Data:** 2023-08-28

---

**User:**

Scala, ciąg fibonnaciego w wersji tail rec

---

**Assistant:**

Oczywiście! Oto przykład implementacji ciągu Fibonacciego w języku Scala przy użyciu rekurencji ogonowej (tail recursion):

```scala
object Fibonacci {
  def fibonacci(n: Int): Long = {
    @annotation.tailrec
    def fibHelper(n: Int, a: Long, b: Long): Long = n match {
      case 0 => a
      case _ => fibHelper(n - 1, b, a + b)
    }

    fibHelper(n, 0, 1)
  }

  def main(args: Array[String]): Unit = {
    val n = 10
    println(s"Fibonacci($n) = ${fibonacci(n)}")
  }
}
```

W tej implementacji, funkcja `fibonacci` wywołuje funkcję pomocniczą `fibHelper`, która przyjmuje trzy argumenty: `n` (pozostała ilość kroków), `a` (wartość Fibonacciego dla `n-2`) i `b` (wartość Fibonacciego dla `n-1`). Funkcja `fibHelper` jest zdefiniowana jako rekurencja ogonowa, ponieważ wywołuje samą siebie w ostatnim kroku bez dodatkowych operacji po powrocie z rekursji. Dzięki temu nie ma narastającego stosu wywołań rekurencyjnych, co pomaga uniknąć potencjalnego przepełnienia stosu w przypadku dużych wartości `n`.

W przykładzie powyżej obliczana jest wartość Fibonacciego dla `n = 10`. Możesz zmienić wartość `n` w zależności od swoich potrzeb, aby obliczyć wartość Fibonacciego dla innych liczb.

---

**User:**

A w wersji z użyciem foldLeft?

---

**Assistant:**

Oczywiście! Możesz również zaimplementować ciąg Fibonacciego przy użyciu funkcji `foldLeft` w języku Scala. Oto jak to można zrobić:

```scala
object Fibonacci {
  def fibonacci(n: Int): Long = {
    if (n <= 0) 0
    else {
      val (_, result) = (2 to n).foldLeft((0L, 1L)) {
        case ((a, b), _) => (b, a + b)
      }
      result
    }
  }

  def main(args: Array[String]): Unit = {
    val n = 10
    println(s"Fibonacci($n) = ${fibonacci(n)}")
  }
}
```

W tej implementacji użyto funkcji `foldLeft`, która działa na sekwencjach (takich jak zakres liczb) i akumuluje wynik iteracji. Pierwsza para liczb `(0L, 1L)` reprezentuje dwa początkowe elementy ciągu Fibonacciego. Następnie `foldLeft` iteruje od 2 do `n`, przy czym w każdym kroku aktualizuje parę liczb na `(b, a + b)` - `b` jest nowym elementem, a `a + b` jest nowym następnikiem.

Podobnie jak w poprzedniej implementacji, możesz zmienić wartość `n` w zależności od swoich potrzeb, aby obliczyć wartość Fibonacciego dla innych liczb.

---

**User:**

Scala, funkcja zip (z dwóch list tworzy jedną listę tupli)

---

**Assistant:**

W języku Scala funkcja `zip` pozwala na połączenie dwóch list w jedną listę tupli, gdzie elementy o tych samych indeksach w obu listach są zestawiane w pary. Oto przykład użycia funkcji `zip`:

```scala
object ZipExample {
  def main(args: Array[String]): Unit = {
    val list1 = List(1, 2, 3, 4, 5)
    val list2 = List("one", "two", "three", "four", "five")

    val zipped: List[(Int, String)] = list1.zip(list2)

    zipped.foreach { case (num, word) =>
      println(s"$num - $word")
    }
  }
}
```

W tym przykładzie, `list1` zawiera liczby, a `list2` zawiera odpowiadające im napisy. Funkcja `zip` jest używana, aby stworzyć listę tupli `zipped`, gdzie każda tupla zawiera parę liczba-napis odpowiadającą sobie elementom z `list1` i `list2`.

Następnie, korzystając z `foreach`, iterujemy po liście tupli `zipped` i wypisujemy połączone wartości na konsolę.

Pamiętaj, że funkcja `zip` działa tylko wtedy, gdy obie listy mają taką samą długość. Jeśli jedna lista jest dłuższa niż druga, to nadmiarowe elementy zostaną pominięte.

---

**User:**

napisz swoją implementację, nie używaj gotowej

---

**Assistant:**

Oczywiście! Oto przykład prostego własnego zaimplementowania funkcji `zip`:

```scala
object CustomZip {
  def customZip[A, B](list1: List[A], list2: List[B]): List[(A, B)] = {
    def zipRec[A, B](list1: List[A], list2: List[B], acc: List[(A, B)]): List[(A, B)] = {
      (list1, list2) match {
        case (Nil, _) | (_, Nil) => acc.reverse
        case (head1 :: tail1, head2 :: tail2) =>
          val newAcc = (head1, head2) :: acc
          zipRec(tail1, tail2, newAcc)
      }
    }

    zipRec(list1, list2, Nil)
  }

  def main(args: Array[String]): Unit = {
    val list1 = List(1, 2, 3, 4, 5)
    val list2 = List("one", "two", "three", "four", "five")

    val zipped: List[(Int, String)] = customZip(list1, list2)

    zipped.foreach { case (num, word) =>
      println(s"$num - $word")
    }
  }
}
```

W powyższym kodzie zdefiniowałem funkcję `customZip`, która przyjmuje dwie listy i zwraca złączoną listę tupli. Wewnętrzna funkcja pomocnicza `zipRec` działa rekurencyjnie, porównując głowy obu list i łącząc je w tuplę, a następnie rekurencyjnie przetwarzając ogony obu list.

Pamiętaj, że w implementacji tej pominięto kilka kwestii związanych z obsługą różnych przypadków (np. list różnych długości), które mogą być obecne w gotowej funkcji `zip` w standardowej bibliotece Scalii.

---

**User:**

teraz przy pomocy foldLeft - jeśli to możliwe

---

**Assistant:**

Oczywiście, można również zaimplementować funkcję `zip` przy użyciu `foldLeft`. Oto przykład:

```scala
object CustomZipWithFoldLeft {
  def customZip[A, B](list1: List[A], list2: List[B]): List[(A, B)] = {
    list1.foldLeft((list2, List.empty[(A, B)])) {
      case ((Nil, acc), _) | (_, acc) => (Nil, acc.reverse)
      case (head2 :: tail2, acc) => (tail2, (list1.head, head2) :: acc)
    }._2
  }

  def main(args: Array[String]): Unit = {
    val list1 = List(1, 2, 3, 4, 5)
    val list2 = List("one", "two", "three", "four", "five")

    val zipped: List[(Int, String)] = customZip(list1, list2)

    zipped.foreach { case (num, word) =>
      println(s"$num - $word")
    }
  }
}
```

W tej implementacji użyłem funkcji `foldLeft`, która iteruje przez elementy listy `list1`, jednocześnie przetwarzając listę `list2` i budując listę wynikową w odwrotnej kolejności (stąd `acc.reverse`).

W każdym kroku folda aktualizujemy parę `(list2, List.empty[(A, B)])`, gdzie `list2` to ogon listy `list2`, a drugi element to akumulator, który jest listą tupli. W przypadku, gdy `list2` się wyczerpie lub lista `list1` będzie miała więcej elementów, kończymy proces foldowania i zwracamy odwrócony akumulator, czyli listę wynikową.

Pamiętaj, że jak w poprzednich implementacjach, ta implementacja nie obsługuje przypadków, w których listy mają różne długości. Gotowa funkcja `zip` w standardowej bibliotece Scalii prawidłowo obsługuje takie przypadki.