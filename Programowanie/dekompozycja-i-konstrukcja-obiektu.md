# Dekompozycja i konstrukcja obiektu.

**Data:** 2023-08-17

---

**User:**

Scala

      .map { case (resultedPlayer, position) =>
        GameResult(
          position,
          resultedPlayer.numberedPlayer.playerNo,
          resultedPlayer.numberedPlayer.number,
          resultedPlayer.result,
        )
      }

Czy możliwe jest zamiast obiektu resultedPlayer po case, użyć mechanizmu który rozbije obiekt resultedPlayer na skłądowe i używać później tych składowych zamiast ciągle odwoływać się do resultedPlayer?

---

**Assistant:**

Tak, w języku Scala istnieje możliwość rozbicia obiektu na jego składowe za pomocą mechanizmu pattern matchingu i wykorzystania tzw. "extractorów" (klas, które posiadają metodę `unapply`, wykorzystywaną do dekonstrukcji obiektu). Możesz to zastosować w swoim przykładzie, aby uniknąć ciągłego odwoływania się do `resultedPlayer`.

Zakładając, że `resultedPlayer` to obiekt z odpowiednimi składowymi, możesz to zrobić w ten sposób:

```scala
.map { case (resultedPlayer, position) =>
  val playerNo = resultedPlayer.numberedPlayer.playerNo
  val number = resultedPlayer.numberedPlayer.number
  val result = resultedPlayer.result

  GameResult(
    position,
    playerNo,
    number,
    result
  )
}
```

Jeśli chcesz użyć mechanizmu pattern matchingu, aby zdekomponować `resultedPlayer` w jednym miejscu, możesz to zrobić w następujący sposób:

```scala
.map { case (resultedPlayer, position) =>
  val NumberedPlayer(playerNo, number) = resultedPlayer.numberedPlayer
  val result = resultedPlayer.result

  GameResult(
    position,
    playerNo,
    number,
    result
  )
}
```

W tym przypadku zakłada się, że istnieje odpowiednio zdefiniowana klasa `NumberedPlayer` z mechanizmem extractorów (`unapply`). Dzięki temu dekompozycja `resultedPlayer.numberedPlayer` na składowe `playerNo` i `number` zostanie wykonana automatycznie.