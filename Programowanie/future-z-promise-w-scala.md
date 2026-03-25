# Future z Promise w Scala

**Data:** 2023-03-24

---

**User:**

Dlaczego w Scala powinienem używać Future razem z Promise? Jaki i podaj przykład

---

**Assistant:**



W Scala warto stosować Future wraz z Promise, ponieważ pozwala to na asynchroniczne wykonywanie operacji, a jednocześnie zapewnia kontrolę nad wynikiem obliczeń.

Future reprezentuje obietnicę, że pewna wartość zostanie zwrócona w przyszłości, a Promise jest mechanizmem, który umożliwia ustawienie wartości, która ma zostać zwrócona w przyszłości przez Future.

Przykład użycia Future z Promise w Scala:

```scala
import scala.concurrent.{Future, Promise}
import scala.concurrent.ExecutionContext.Implicits.global

def calculateMeaningOfLife(): Future[Int] = {
  val promise = Promise[Int]()
  Future {
    val meaningOfLife = 42 // Obliczenie wartości.
    promise.success(meaningOfLife) // Ustawienie wartości w Promise.
  }
  promise.future // Zwrócenie Future powiązanego z Promise.
}

// Wywołanie funkcji calculateMeaningOfLife i przetworzenie wyniku asynchronicznie.
calculateMeaningOfLife().foreach { meaningOfLife =>
  println(s"The meaning of life is $meaningOfLife")
}
```

W tym przykładzie funkcja `calculateMeaningOfLife` zwraca Future, który zawiera obietnicę zwrócenia wartości, którą ustawia się w Promise. Asynchroniczne obliczenia wykonywane są wewnątrz Future, a kiedy obliczenia zostaną zakończone, Promise jest używany do ustawienia wyniku, który zostanie zwrócony przez Future. Następnie, w przetwarzaniu wyniku, można wykorzystać metodę `foreach`, aby wykonać pewną operację na zwróconej wartości.

---

**User:**

Dlaczego  Promise jest używany do ustawienia wyniku? Czy nie można byłoby zwrócić 42 w Future?

---

**Assistant:**

W teorii, można byłoby zwrócić 42 w Future, ale w praktyce zastosowanie Promise jest bardziej elastyczne i umożliwia bardziej zaawansowaną kontrolę nad wartością, która ma być zwrócona przez Future.

Zastosowanie Promise pozwala na oddzielenie deklaracji i ustawienia wyniku od samej implementacji obliczeń wewnątrz Future. Dzięki temu, obliczenia mogą być wykonywane asynchronicznie, a wynik może zostać ustawiony w Promise, gdy będzie już dostępny.

Ponadto, Promise umożliwia również przypisanie funkcji obsługi błędów, które mogą być wywołane w przypadku błędu w trakcie wykonywania obliczeń. To pozwala na elastyczne zarządzanie błędami i reakcję na nie w odpowiedni sposób.

Ostatecznie, użycie Promise zwiększa elastyczność i kontrolę nad wartością, która ma zostać zwrócona przez Future, co czyni kod bardziej czytelnym i łatwiejszym do utrzymania.

---

**User:**

Czym różni się 
val result = Future.traverse(0 until 10)(i => runTasks(s"task-$i", 1_000_000)(task()))
od
  val result = Future.sequence(
  for (i <- 0 until 10)
    yield runTasks(runTasks(s"task-$i", 1_000_000)(task()))
  }

---

**Assistant:**

Obie metody `Future.traverse` i `Future.sequence` służą do przetwarzania sekwencji asynchronicznych wywołań, ale różnią się w sposobie przetwarzania sekwencji.

`Future.traverse` wykonuje asynchroniczne wywołania dla każdego elementu sekwencji i zwraca Future zawierający sekwencję wyników w kolejności odpowiadającej oryginalnej sekwencji. Przykład użycia `Future.traverse` w Twoim pytaniu przetwarza sekwencję wartości typu `Int` od 0 do 9 za pomocą funkcji `runTasks` z wartością 1_000_000 i zwraca sekwencję wyników typu `TaskResult` w kolejności odpowiadającej oryginalnej sekwencji. W tym przypadku, jeśli którykolwiek z wywołań zakończy się niepowodzeniem, `Future.traverse` zakończy się z błędem, a pozostałe wywołania zostaną anulowane.

`Future.sequence` wykonuje asynchroniczne wywołania dla każdego elementu sekwencji i zwraca Future zawierający sekwencję wyników w kolejności, w jakiej wywołania zakończyły się. Przykład użycia `Future.sequence` w Twoim pytaniu przetwarza sekwencję wartości typu `Int` od 0 do 9 za pomocą funkcji `runTasks` z wartością 1_000_000 i zwraca sekwencję wyników typu `TaskResult` w kolejności, w jakiej wywołania zostały zakończone. W tym przypadku, jeśli którykolwiek z wywołań zakończy się niepowodzeniem, `Future.sequence` zakończy się z błędem, a pozostałe wywołania zostaną wykonane i zwrócone w sekwencji wyników.

Podsumowując, `Future.traverse` i `Future.sequence` różnią się sposobem przetwarzania sekwencji wyników asynchronicznych wywołań. `Future.traverse` zwraca sekwencję wyników w kolejności oryginalnej sekwencji, a `Future.sequence` w kolejności, w jakiej wywołania zostały zakończone.