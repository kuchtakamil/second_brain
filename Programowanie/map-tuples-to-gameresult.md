# Map tuples to GameResult

**Data:** 2023-08-17

---

**User:**

Scala 
mam val tuples: List[(String, Int, Int)]
i 
case class GameResult(position: Int, player: String, number: Int, result: Int)
Chcę zrobić
tuples.map(t => GameResult(idx, t._1, t._2, t._3))
gdzie idx to index listy tuples. Nie wiem jak zrobyć ten index

---

**Assistant:**

W języku Scala można uzyskać indeks elementu podczas iteracji po liście przy użyciu metody `zipWithIndex`. Poniżej przedstawiam, jak to zrobić w kontekście Twojego przykładu:

```scala
val tuples: List[(String, Int, Int)] = ... // Twoja lista tuples
val gameResults: List[GameResult] = tuples.zipWithIndex.map { case ((player, number, result), idx) =>
  GameResult(idx, player, number, result)
}
```

W powyższym kodzie `zipWithIndex` łączy każdy element z listy tuples ze swoim indeksem, a następnie wewnątrz funkcji `map` tworzony jest obiekt `GameResult` dla każdej pary (element, indeks).

Warto zauważyć, że w definicji `GameResult` używane są pola `position`, `player`, `number` i `result`, podczas gdy w kodzie korzystamy z `idx`, `player`, `number` i `result`. Jeśli chcesz użyć nazwy `position` zamiast `idx`, możesz zmienić wzorzec w funkcji `map` na taki:

```scala
val gameResults: List[GameResult] = tuples.zipWithIndex.map { case ((player, number, result), position) =>
  GameResult(position, player, number, result)
}
```

Obie wersje działają tak samo - wybór, który z nich użyć, zależy od Twoich preferencji co do nazewnictwa.