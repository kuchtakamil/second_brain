# Przekształcenie daty w Scala.

**Data:** 2023-05-10

---

**User:**

W jaki sposób w Scala przekształcić datę o następującym formacie 2023-05-10T15:10:08.882658045Z do formatu dytelnego dla człowieka?

---

**Assistant:**

W języku Scala można przekształcić datę o formacie "2023-05-10T15:10:08.882658045Z" do formatu czytelnego dla człowieka za pomocą klasy `java.time.LocalDateTime` oraz metody `java.time.format.DateTimeFormatter`. Oto przykładowy kod, który wykonuje to przekształcenie:

```scala
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter

val inputDate = "2023-05-10T15:10:08.882658045Z"

val inputFormatter = DateTimeFormatter.ISO_INSTANT
val outputFormatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")

val dateTime = LocalDateTime.parse(inputDate, inputFormatter)
val formattedDate = dateTime.format(outputFormatter)

println(formattedDate)
```

W powyższym kodzie najpierw definiujemy wejściową datę jako łańcuch znaków (`inputDate`). Następnie tworzymy obiekty formaterów dla wejścia (`inputFormatter`) i wyjścia (`outputFormatter`). `DateTimeFormatter.ISO_INSTANT` jest gotowym formaterem, który obsługuje format ISO 8601, a `DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")` definiuje format wyjściowy jako "RRRR-MM-dd HH:mm:ss".

Następnie używamy `LocalDateTime.parse` do przekształcenia wejściowego łańcucha znaków na obiekt `LocalDateTime`. Na koniec używamy metody `format` obiektu `LocalDateTime`, aby sformatować datę do czytelnego formatu i przypisujemy wynik do zmiennej `formattedDate`. W przykładzie wyświetlamy sformatowaną datę za pomocą `println(formattedDate)`.