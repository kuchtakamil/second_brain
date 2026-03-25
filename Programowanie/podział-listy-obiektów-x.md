# Podział listy obiektów X

**Data:** 2023-05-02

---

**User:**

A extends X
oraz
B extends X
W Scala jaki jest sposób aby z jednej listy obiektów typu X, stworzyć dwie listy. Jedna lista obiektów typu A, druga obiektów typu B

---

**Assistant:**

W Scala można użyć metody `partition` na liście obiektów typu `X`, aby podzielić listę na dwie listy, jedną zawierającą obiekty typu `A`, a drugą zawierającą obiekty typu `B`. 

Oto przykład:

```scala
class X
class A extends X
class B extends X

val xList = List(new A, new B, new A, new B, new A)

val (aList, bList) = xList.partition {
  case _: A => true
  case _ => false
}

println(s"aList: $aList") // aList: List(A@44cc50b2, A@7720f2c2, A@1a2e7541)
println(s"bList: $bList") // bList: List(B@5e5ca5e, B@282ba1e, B@53f8d10f)
```

Metoda `partition` przyjmuje jako argument funkcję, która dla każdego elementu listy zwraca wartość typu `Boolean`, określającą, czy element należy do pierwszej czy drugiej listy. W powyższym przykładzie funkcja ta jest definiowana za pomocą wyrażenia `case`, które sprawdza, czy dany obiekt jest typu `A` i zwraca wartość `true`, jeśli tak jest, lub `false`, jeśli jest typu `B`. Wynikowa para list jest przypisywana do zmiennych `aList` i `bList` i może być wydrukowana do konsoli za pomocą funkcji `println`.

---

**User:**

użyj proszę funkcji groupBy

---

**Assistant:**

Oczywiście, można również użyć funkcji `groupBy` na liście obiektów typu `X`, aby podzielić ją na dwie listy, jedną zawierającą obiekty typu `A`, a drugą zawierającą obiekty typu `B`. 

Oto przykład:

```scala
class X
class A extends X
class B extends X

val xList = List(new A, new B, new A, new B, new A)

val grouped = xList.groupBy {
  case _: A => "aList"
  case _ => "bList"
}

val aList = grouped.getOrElse("aList", List.empty)
val bList = grouped.getOrElse("bList", List.empty)

println(s"aList: $aList") // aList: List(A@44cc50b2, A@7720f2c2, A@1a2e7541)
println(s"bList: $bList") // bList: List(B@5e5ca5e, B@282ba1e, B@53f8d10f)
```

Funkcja `groupBy` również przyjmuje funkcję jako argument, która dla każdego elementu listy zwraca klucz, według którego elementy zostaną pogrupowane. W powyższym przykładzie funkcja ta jest definiowana za pomocą wyrażenia `case`, które zwraca ciąg znaków "aList" dla elementów typu `A` i ciąg znaków "bList" dla elementów typu `B`. Funkcja `groupBy` zwraca mapę, w której klucze to wartości zwracane przez funkcję grupującą, a wartościami są listy elementów o tych kluczach. Aby uzyskać poszczególne listy, można użyć funkcji `getOrElse` z odpowiednimi kluczami i domyślnymi wartościami list pustych. Wynikowe listy mogą być wydrukowane do konsoli za pomocą funkcji `println`.