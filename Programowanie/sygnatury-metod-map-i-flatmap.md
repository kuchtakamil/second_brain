# Sygnatury metod map i flatMap

**Data:** 2023-08-29

---

**User:**

Scala, podaj sygnatury metod map i flatMap

---

**Assistant:**

Oczywiście, oto sygnatury metod `map` i `flatMap` w języku programowania Scala:

1. Metoda `map`:
```scala
def map[B](f: A => B): Option[B]
```
Metoda `map` jest dostępna w klasie `Option` i służy do transformowania wartości wewnątrz instancji `Option`. Przyjmuje funkcję `f` jako argument, która przekształca wartość wewnątrz `Option[A]` na wartość typu `B` i zwraca nową instancję `Option[B]`. Jeśli oryginalne `Option` było puste (`None`), to wynikowe `Option` również będzie puste.

2. Metoda `flatMap`:
```scala
def flatMap[B](f: A => Option[B]): Option[B]
```
Metoda `flatMap` również jest dostępna w klasie `Option`. Podobnie jak `map`, przyjmuje funkcję `f` jako argument, ale ta funkcja zwraca już wartość opakowaną w `Option[B]`. Metoda `flatMap` wyłuskuje wartość z istniejącego `Option[A]`, przekazuje ją do funkcji `f`, która zwraca `Option[B]`, a następnie spłaszcza wynik do pojedynczego `Option[B]`. Jeśli oryginalne `Option` było puste, to wynikowe `Option` również będzie puste.

Obie te metody są często używane w kontekście monadycznych struktur danych takich jak `Option`, gdzie reprezentują obliczenia, które mogą się zakończyć wartością lub nie zawierać żadnej wartości (wartość pustą).