# Konstruktor w Scali.

**Data:** 2023-04-04

---

**User:**

W Scala podaj przykład użycia konstruktora

---

**Assistant:**

W języku Scala konstruktor jest definiowany w ciele klasy, a jego nazwa jest zawsze "this". Konstruktor może przyjmować parametry, które są wykorzystywane do inicjalizacji pól klasy. Poniżej przedstawiam przykład klasy z konstruktorem:

```scala
class Person(firstName: String, lastName: String) {
  println(s"Creating person $firstName $lastName")
  
  def fullName: String = s"$firstName $lastName"
}
```

W tym przykładzie definiujemy klasę `Person`, która przyjmuje dwa parametry typu `String` w konstruktorze - `firstName` oraz `lastName`. Następnie wewnątrz konstruktora wyświetlamy informację o tworzeniu nowego obiektu klasy `Person` z użyciem podanych parametrów. 

Dodatkowo klasa `Person` posiada metodę `fullName`, która zwraca pełne imię i nazwisko osoby, sklejając wartości `firstName` i `lastName`. 

Możemy utworzyć nowy obiekt klasy `Person` z użyciem konstruktora, podając wartości dla obu parametrów:

```scala
val person = new Person("Jan", "Kowalski")
println(person.fullName)
```

W wyniku wykonania powyższego kodu na konsoli zostanie wyświetlony napis "Creating person Jan Kowalski", a następnie "Jan Kowalski", ponieważ zostanie utworzony nowy obiekt klasy `Person` i wywołana zostanie jego metoda `fullName`.

---

**User:**

Rozszerz przykład z klasą Person w której w konstruktorze z podanego lastName odcinamy dwa ostatnie znaki

---

**Assistant:**

Oto przykład klasy `Person`, w której w konstruktorze z podanego `lastName` odcinamy dwa ostatnie znaki:

```scala
class Person(firstName: String, lastName: String) {
  private val shortLastName: String = lastName.dropRight(2)
  println(s"Creating person $firstName $shortLastName")
  
  def fullName: String = s"$firstName $shortLastName"
}
```

W tym przykładzie dodaliśmy nowe pole klasy `shortLastName`, które przechowuje wartość pola `lastName` bez dwóch ostatnich znaków. Wykorzystaliśmy metodę `dropRight(n: Int)`, która zwraca nowy łańcuch znaków bez ostatnich `n` znaków.

Następnie wewnątrz konstruktora wyświetlamy informację o tworzeniu nowego obiektu klasy `Person` z użyciem podanych parametrów, ale wykorzystując pole `shortLastName` zamiast `lastName`.

Metoda `fullName` została zmodyfikowana tak, aby zwracać imię oraz `shortLastName`.

Możemy utworzyć nowy obiekt klasy `Person` z użyciem zmodyfikowanego konstruktora, podając wartości dla obu parametrów:

```scala
val person = new Person("Jan", "Kowalski")
println(person.fullName)
```

W wyniku wykonania powyższego kodu na konsoli zostanie wyświetlony napis "Creating person Jan Kowal", a następnie "Jan Kowal", ponieważ zostanie utworzony nowy obiekt klasy `Person` i wywołana zostanie jego metoda `fullName`.