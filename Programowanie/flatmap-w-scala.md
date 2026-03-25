# flatMap w Scala

**Data:** 2023-04-08

---

**User:**

W jakich celach w Scala jest używana funkcja flatMap

---

**Assistant:**

Funkcja `flatMap` w języku Scala jest często wykorzystywana w kontekście programowania funkcyjnego i monad. Głównym celem tej funkcji jest połączenie dwóch operacji - mapowania i spłaszczania - w jedną.

`flatMap` pozwala na aplikowanie funkcji do wartości znajdujących się wewnątrz kontenera (np. w liście czy w Option) oraz łączenie wielu kontenerów w jeden. Dzięki temu można łatwo łączyć i łańcuchować operacje na wartościach znajdujących się w kontenerach, co ułatwia pracę z danymi.

Przykład użycia funkcji `flatMap` może wyglądać następująco:

```scala
val listaLiczb = List(1, 2, 3, 4, 5)

val wynik = listaLiczb.flatMap(x => List(x, x * 2))

println(wynik)
// wynik: List(1, 2, 2, 4, 3, 6, 4, 8, 5, 10)
```

W powyższym przykładzie funkcja `flatMap` została wykorzystana do złączenia dwóch list. Dzięki temu, że funkcja zwraca nową listę, można ją łączyć z innymi operacjami, takimi jak `filter` czy `map`.