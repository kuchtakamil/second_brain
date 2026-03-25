# Zip Lists with Indices

**Data:** 2023-08-17

---

**User:**

Scala, chciałbym zrobić na dwóch listach zip czyli l1.zip(l2) a jako trzeci element tupli dołożyć index

---

**Assistant:**

Oczywiście! Możesz to osiągnąć w języku Scala, korzystając z funkcji `zipWithIndex`. Oto przykład, który pokazuje, jak to zrobić:

```scala
val l1 = List("a", "b", "c")
val l2 = List(1, 2, 3)

val zippedWithIndex = l1.zip(l2).zipWithIndex.map { case ((a, b), idx) => (a, b, idx) }

zippedWithIndex.foreach(println)
```

W tym przykładzie tworzymy dwie listy: `l1` i `l2`. Następnie używamy metody `zip` do stworzenia listy krotek zawierających elementy z obu list. Na końcu używamy `zipWithIndex`, aby dołączyć indeks do każdej krotki. W rezultacie otrzymujemy listę trójek (element1, element2, indeks), którą możemy wydrukować lub przetwarzać dalej.