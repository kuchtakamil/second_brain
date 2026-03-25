# Walidacja wartości dla case'ów w Scala.

**Data:** 2023-04-30

---

**User:**

W Scala wyekstraktuj funkcję będącą wspólną częścią dla obu caseów

    simValue match {
      case CarriageSpeed(updatedOn, value) =>
        val validValueRange = validRanges.carriageSpeed.validValueRange
        if (validValueRange.min < simValue.value && simValue.value < validValueRange.max)
          IO.delay{ model.consumer.CarriageSpeed(updatedOn, value, "valid") }
        else
          IO.delay{ model.consumer.CarriageSpeed(updatedOn, value, "invalid") }

      case BedTemperature(updatedOn, value) =>
        val validValueRange = validRanges.bedTemperature.validValueRange
        if (validValueRange.min < simValue.value && simValue.value < validValueRange.max)
          IO.delay {
            model.consumer.BedTemperature(updatedOn, value, "valid")
          }
        else
          IO.delay {
            model.consumer.BedTemperature(updatedOn, value, "invalid")
          }
      }

---

**Assistant:**

Można wyekstraktować funkcję walidującą wartość, która jest wspólna dla obu case'ów:

```scala
def validateValue[T <: SimValue](simValue: T, validRange: ValidRange, consumerFn: (LocalDateTime, Double, String) => Unit) = {
  if (validRange.min < simValue.value && simValue.value < validRange.max)
    IO.delay{ consumerFn(simValue.updatedOn, simValue.value, "valid") }
  else
    IO.delay{ consumerFn(simValue.updatedOn, simValue.value, "invalid") }
}
```

Można ją wykorzystać w oryginalnym kodzie w ten sposób:

```scala
simValue match {
  case carriageSpeed: CarriageSpeed =>
    val validValueRange = validRanges.carriageSpeed.validValueRange
    validateValue(carriageSpeed, validValueRange, model.consumer.CarriageSpeed)

  case bedTemperature: BedTemperature =>
    val validValueRange = validRanges.bedTemperature.validValueRange
    validateValue(bedTemperature, validValueRange, model.consumer.BedTemperature)
}
```

---

**User:**

przekształć następującą funkcję def na postać funkcji val
  def validateValue[T <: SimValue](simValue: T, validRange: ValidValueRange, consumerFn: (Instant, Int, String) => ClassifiedValue): IO[ClassifiedValue] = {
    if (validRange.min < simValue.value && simValue.value < validRange.max)
      IO.delay{ consumerFn(simValue.updatedOn, simValue.value, "valid") }
    else
      IO.delay{ consumerFn(simValue.updatedOn, simValue.value, "invalid") }
  }

---

**Assistant:**

Można przekształcić funkcję `validateValue` na postać funkcji `val` w ten sposób:

```scala
val validateValue = (simValue: SimValue, validRange: ValidValueRange, consumerFn: (Instant, Int, String) => ClassifiedValue) => {
  if (validRange.min < simValue.value && simValue.value < validRange.max)
    IO.delay{ consumerFn(simValue.updatedOn, simValue.value, "valid") }
  else
    IO.delay{ consumerFn(simValue.updatedOn, simValue.value, "invalid") }
}: IO[ClassifiedValue]
```

W takiej postaci funkcję `validateValue` można wywołać w podobny sposób jak w oryginalnej funkcji, np.:

```scala
val result = validateValue(carriageSpeed, validValueRange, model.consumer.CarriageSpeed).unsafeRunSync()
``` 

Wynik wywołania funkcji zwraca `IO[ClassifiedValue]`, więc można użyć metody `unsafeRunSync()` w celu uzyskania wartości typu `ClassifiedValue`.