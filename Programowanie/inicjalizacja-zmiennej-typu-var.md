# Inicjalizacja zmiennej typu Var.

**Data:** 2023-05-03

---

**User:**

Używając scala.js oraz Laminar, mając następujące klasy modelu
case class CarriageSpeed(updatedOn: Instant, value: Int, status: String)
case class BedTemperature(updatedOn: Instant, value: Int, status: String)
podaj w jaki sposób można zainicjalizować wartość typu Var która zawiera obiekt typu CarriageSpeed

---

**Assistant:**

Aby zainicjalizować wartość typu Var, która zawiera obiekt typu CarriageSpeed, należy użyć poniższego kodu:

```scala
import com.raquo.laminar.api.L._

val carriageSpeedVar: Var[CarriageSpeed] = Var(
  CarriageSpeed(
    updatedOn = Instant.now(),
    value = 0,
    status = "stopped"
  )
)
```

Ten kod importuje potrzebne moduły z Laminar, tworzy zmienną typu `Var` o nazwie `carriageSpeedVar`, która jest inicjalizowana obiektem `CarriageSpeed` z niezerową wartością prędkości i statusem zatrzymania. Można zmienić wartości zgodnie z wymaganiami.