# Scala: Alternatywne zapisy.

**Data:** 2023-08-17

---

**User:**

Scala, jak można to napisać lepiej
val value: List[Int] = numbersForPlayers.map(num => constructGameResult(num))

---

**Assistant:**

Oczywiście, mogę pomóc! Poniżej znajdziesz alternatywne sposoby zapisu tego fragmentu kodu w języku Scala:

1. Z użyciem notacji funkcyjnej:
```scala
val value: List[Int] = numbersForPlayers.map(constructGameResult)
```

2. Z użyciem funkcji anonimowej w notacji skróconej:
```scala
val value: List[Int] = numbersForPlayers.map(constructGameResult(_))
```

3. Używając notacji underscore w przypadku jednoargumentowej funkcji:
```scala
val value: List[Int] = numbersForPlayers.map(constructGameResult)
```

4. Z użyciem for comprehensions (złożenia for):
```scala
val value: List[Int] = for {
  num <- numbersForPlayers
} yield constructGameResult(num)
```

5. Używając metod `collect`:
```scala
val value: List[Int] = numbersForPlayers.collect {
  case num => constructGameResult(num)
}
```

Każdy z tych zapisów jest równie poprawny i spełnia to samo zadanie. Wybierz ten, który według Ciebie jest najbardziej czytelny i zrozumiały dla Ciebie oraz innych programistów pracujących nad kodem.