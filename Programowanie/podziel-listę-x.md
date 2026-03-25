# Podziel listę X

**Data:** 2023-05-01

---

**User:**

A extends X
oraz
B extends X
W Scala jaki jest sposób aby z jednej listy obiektów typu X, stworzyć dwie listy. Jedna lista obiektów typu A, druga obiektów typu B

---

**Assistant:**

W Scala można użyć funkcji `partition` z biblioteki standardowej, która rozdzieli elementy listy na dwie oddzielne listy na podstawie warunku określonego przez funkcję predykatu. 

Aby użyć funkcji `partition` w tym przypadku, należy określić predykat, który będzie sprawdzał, czy dany element jest typu A czy B. Można to zrobić na przykład w następujący sposób:

```scala
val listX: List[X] = ???
val (listA, listB) = listX.partition {
  case _: A => true
  case _: B => false
}
```

W powyższym kodzie wykorzystywana jest metoda `partition` na liście `listX`, która zwraca parę list zawierających elementy spełniające odpowiednio warunek zwracający wartość `true` i `false`. W predykacie wykorzystywane jest dopasowanie wzorców (`case`) do typu każdego elementu z listy `listX`. Elementy typu `A` zwracają wartość `true`, natomiast elementy typu `B` zwracają wartość `false`. Następnie wynik funkcji `partition` jest przypisywany do dwóch zmiennych `listA` i `listB`, które zawierają odpowiednio elementy typu `A` i `B`.

---

**User:**

A co gdybym chciał rozdzielić na trzy klasy dla 
A extends X
oraz
B extends X
oraz 
C extends X

---

**Assistant:**

Aby rozdzielić listę obiektów typu `X` na trzy oddzielne listy obiektów typu `A`, `B` i `C`, można wykorzystać metodę `foldLeft` w połączeniu z wzorcem `match`. Metoda `foldLeft` umożliwia iterowanie po elementach listy i zbieranie wyników w zmiennej akumulatorze. W tym przypadku będziemy korzystać z trzech zmiennych akumulatorów, które będą przechowywać kolejno elementy typu `A`, `B` i `C`. 

```scala
val listX: List[X] = ???
val (listA, listB, listC) = listX.foldLeft((List.empty[A], List.empty[B], List.empty[C])) {
  case ((accA, accB, accC), elem) => elem match {
    case a: A => (a :: accA, accB, accC)
    case b: B => (accA, b :: accB, accC)
    case c: C => (accA, accB, c :: accC)
    case _ => (accA, accB, accC)
  }
}
```

W powyższym kodzie metoda `foldLeft` jest wywoływana na liście `listX`, zaczynając od pustych list `List.empty[A]`, `List.empty[B]` i `List.empty[C]`. W każdym kroku iteracji metoda `foldLeft` przetwarza jeden element z listy `listX` i aktualizuje zm