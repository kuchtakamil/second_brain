# Zastosowanie foldLeft w Scala

**Data:** 2023-08-28

---

**User:**

Podaj przykładowe zastodowanie funkcji foldLeft w Scala

---

**Assistant:**

Funkcja `foldLeft` jest często używana w języku Scala do iterowania przez elementy kolekcji (np. listy, tablicy) i łączenia ich w jeden wynik poprzez zastosowanie podanej funkcji akumulującej. Oto przykład zastosowania funkcji `foldLeft`:

```scala
val numbers = List(1, 2, 3, 4, 5)

// Przykład 1: Sumowanie wszystkich liczb w liście
val sum = numbers.foldLeft(0)((acc, num) => acc + num)
println(s"Suma liczb: $sum")

// Przykład 2: Łączenie napisów w jeden długi napis
val strings = List("Hello", " ", "world", "!")
val combinedString = strings.foldLeft("")((acc, str) => acc + str)
println(s"Połączony napis: $combinedString")

// Przykład 3: Znalezienie największej liczby w liście
val maxNumber = numbers.foldLeft(Int.MinValue)((acc, num) => if (num > acc) num else acc)
println(s"Największa liczba: $maxNumber")
```

W każdym z tych przykładów, funkcja `foldLeft` przyjmuje dwa argumenty: wartość początkową akumulatora (pierwszy argument) oraz funkcję akumulującą (drugi argument). Funkcja akumulująca jest wywoływana dla każdego elementu kolekcji, przyjmując aktualną wartość akumulatora (`acc`) oraz kolejny element (`num` lub `str` w przykładach). Wynik funkcji akumulującej staje się nową wartością akumulatora dla następnego wywołania funkcji akumulującej. W ten sposób elementy kolekcji są przetwarzane sekwencyjnie, a wynik końcowy jest budowany na podstawie iteracji i zastosowania funkcji akumulującej.

---

**User:**

Podaj przykładowe zastosowanie funkcji flatMap w Scala

---

**Assistant:**

Funkcja `flatMap` w języku Scala jest często używana do transformacji i spłaszczania kolekcji, takiej jak lista zawierająca kolekcje wewnętrzne. Działa poprzez zastosowanie funkcji mapującej na każdym elemencie kolekcji i następnie "spłaszczenie" wynikowych kolekcji do pojedynczej kolekcji. Oto przykład zastosowania funkcji `flatMap`:

```scala
val listOfLists = List(List(1, 2, 3), List(4, 5, 6), List(7, 8, 9))

// Przykład 1: Spłaszczenie listy list do pojedynczej listy
val flattenedList = listOfLists.flatMap(list => list)
println(s"Spłaszczona lista: $flattenedList")

// Przykład 2: Transformacja i spłaszczenie listy napisów
val words = List("Hello", "World", "Scala", "FlatMap")
val flattenedChars = words.flatMap(word => word.toCharArray)
println(s"Spłaszczona lista znaków: $flattenedChars")
```

W przykładzie 1, `listOfLists` zawiera trzy listy z liczbami. Za pomocą `flatMap` przekształcamy każdą listę wewnętrzną w pojedynczą listę, co prowadzi do spłaszczenia całej struktury do pojedynczej listy `[1, 2, 3, 4, 5, 6, 7, 8, 9]`.

W przykładzie 2, `flatMap` jest używany do przekształcenia każdego napisu w listę jego znaków, a następnie spłaszczenia wynikowych list znaków do jednej listy znaków.

Ogólnie rzecz biorąc, `flatMap` jest przydatnym narzędziem do równoczesnego mapowania i spłaszczania kolekcji w celu uzyskania jednolitej struktury danych.