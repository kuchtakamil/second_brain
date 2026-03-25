# Błąd z asJson. (Error with asJson.)

**Data:** 2023-04-12

---

**User:**

W Scala napraw błąd związany z  asJson

    private def createObj(deviceType: String, newVal: Int): SimValue = deviceType match {
        case ConfigDomain.bedTemp => BedTemperature(Instant.now(), newVal)
        case ConfigDomain.carriageSpeed => CarriageSpeed(Instant.now(), newVal)
        case _ => CarriageSpeed(Instant.now(), newVal)
    }

val obj = createObj(deviceType, newVal)
val str = obj.asJson

---

**Assistant:**

The `asJson` method is not a built-in method in Scala, so it's possible that this method is part of a third-party library you are using in your project. However, assuming that you are using the Circe library to convert your `obj` instance to a JSON string, here's an example of how to use the `asJson` method correctly:

1. First, make sure you have added the necessary dependencies to your `build.sbt` file:

```
libraryDependencies ++= Seq(
  "io.circe" %% "circe-core" % "0.14.1",
  "io.circe" %% "circe-generic" % "0.14.1",
  "io.circe" %% "circe-parser" % "0.14.1"
)
```

2. Import the necessary Circe classes at the top of your file:

```
import io.circe._
import io.circe.syntax._
```

3. Use the `asJson` method to convert your `obj` instance to a JSON string:

```
val obj = createObj(deviceType, newVal)
val str = obj.asJson.noSpaces
```

In this example, `noSpaces` is used to remove all whitespace from the resulting JSON string. If you want the JSON string to be more human-readable, you can use the `spaces2` method instead:

```
val str = obj.asJson.spaces2
```

This will use two spaces to indent each level of the JSON hierarchy.