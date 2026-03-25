# Dodawanie elementów do listy.

**Data:** 2023-08-17

---

**User:**

Scala jak do listy dodać element na koniec

---

**Assistant:**

Aby dodać element na koniec listy w języku Scala, możesz użyć dwóch różnych podejść: mutable (zmiennej) i immutable (niemiennej) listy.

### Mutable (Zmienna) Lista:
```scala
import scala.collection.mutable.ListBuffer

// Tworzenie pustej mutable listy
val mutableList = ListBuffer[Int]()

// Dodawanie elementów na koniec mutable listy
mutableList += 1
mutableList += 2
mutableList += 3

// Lub użyj metody append
mutableList.append(4)
```

### Immutable (Niemienne) Lista:
```scala
// Tworzenie niemiennej listy
val immutableList = List(1, 2, 3)

// Dodawanie elementów do niemiennej listy - tworzy nową listę
val newImmutableList = immutableList :+ 4
```

W przypadku niemiennej listy, operacja `:+` tworzy nową listę zawierającą dodany element, pozostawiając oryginalną listę bez zmian. Dlatego wartość `newImmutableList` będzie zawierać elementy z oryginalnej listy oraz dodany nowy element.

Zmienna lista (mutable ListBuffer) pozwala na modyfikację listy w miejscu, a niemienne listy (immutable List) tworzą nową listę z każdą operacją dodawania, zachowując oryginalną listę nietkniętą. Wybór pomiędzy tymi dwoma rodzajami zależy od wymagań Twojego programu i preferencji w stosunku do niemienności (immutable) danych.