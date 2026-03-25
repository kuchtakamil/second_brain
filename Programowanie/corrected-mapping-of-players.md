# Corrected Mapping of Players

**Data:** 2023-08-17

---

**User:**

Scala
  case class NumberedPlayer(playerNo: Int, isBot: Boolean, number: Int)
  case class ResultedPlayer(numberedPlayer: NumberedPlayer, result: Int)

val numbersForPlayers: List[NumberedPlayer]
popraw
numbersForPlayers.map { case (_, isBot, number) => ResultedPlayer(constructGameResult(number)) }

---

**Assistant:**

It looks like you're trying to map a list of `NumberedPlayer` instances to a list of `ResultedPlayer` instances in Scala. There are a couple of issues in your code snippet. I'll help you correct them.

First, let's address the issues:

1. You are trying to pattern match on a `NumberedPlayer` instance using a tuple-like syntax. Instead, you should use the pattern matching syntax for a case class.

2. The `constructGameResult` function is missing, and it seems you want to use the `number` field from `NumberedPlayer` as an argument to this function. You need to provide the implementation of `constructGameResult` or replace it with your actual game result calculation logic.

Here's the corrected version of your code:

```scala
case class NumberedPlayer(playerNo: Int, isBot: Boolean, number: Int)
case class ResultedPlayer(numberedPlayer: NumberedPlayer, result: Int)

// Define the constructGameResult function or replace it with your actual logic
def constructGameResult(number: Int): Int = {
  // Your game result calculation logic here
  // For demonstration, let's just return a dummy result
  number * 2
}

val numbersForPlayers: List[NumberedPlayer] = List(
  NumberedPlayer(1, false, 10),
  NumberedPlayer(2, true, 20),
  NumberedPlayer(3, false, 30)
)

val resultedPlayers: List[ResultedPlayer] = numbersForPlayers.map { numberedPlayer =>
  val result = constructGameResult(numberedPlayer.number)
  ResultedPlayer(numberedPlayer, result)
}

// Print the resultedPlayers list for demonstration
resultedPlayers.foreach(println)
```

In this corrected code, I've provided a dummy implementation for the `constructGameResult` function to demonstrate the mapping. You should replace it with your actual game result calculation logic. The `map` function is now correctly using the `NumberedPlayer` instance to create a `ResultedPlayer` instance with the calculated result.