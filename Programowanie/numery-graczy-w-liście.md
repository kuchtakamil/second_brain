# Numery graczy w liście

**Data:** 2023-08-17

---

**User:**

Scala
    List.fill(30) {
      NumberedPlayer(1, false)
    } 
Zamiast 1 w NumberedPlayer, chcę mieć kolejny numer odpowiadający indeksowi w liście

---

**Assistant:**

Oczywiście, możesz to zrobić w następujący sposób w języku Scala:

```scala
case class NumberedPlayer(number: Int, flag: Boolean)

val playerList = List.fill(30) { index =>
  NumberedPlayer(index + 1, false)
}
```

W tym przykładzie używamy funkcji `List.fill`, aby utworzyć listę zawierającą 30 elementów. Wewnątrz bloku `{}` przekazujemy funkcję anonimową `index => NumberedPlayer(index + 1, false)`, która przyjmuje indeks i tworzy instancję `NumberedPlayer`, gdzie numer jest równy `index + 1`.

Teraz `playerList` zawiera listę 30 elementów `NumberedPlayer` o numerach od 1 do 30.

---

**User:**

    List.fill(30) { index =>
      NumberedPlayer(index, false)
    }
zwraca Int => NumberedPlayer

---

**Assistant:**

Przepraszam za zamieszanie. Wygląda na to, że wersja Scala, którą używasz, nie obsługuje automatycznego dostarczania indeksu do funkcji `List.fill` w ten sposób. W takim przypadku możesz użyć tradycyjnej pętli `for` lub funkcji `map`, aby osiągnąć zamierzony rezultat. Oto przykład z użyciem pętli `for`:

```scala
case class NumberedPlayer(number: Int, flag: Boolean)

val playerList = (0 until 30).map { index =>
  NumberedPlayer(index + 1, false)
}.toList
```

Lub przykład z użyciem funkcji `map`:

```scala
case class NumberedPlayer(number: Int, flag: Boolean)

val playerList = (0 until 30).toList.map { index =>
  NumberedPlayer(index + 1, false)
}
```

Oba te przykłady tworzą listę zawierającą 30 elementów `NumberedPlayer` o numerach od 1 do 30.