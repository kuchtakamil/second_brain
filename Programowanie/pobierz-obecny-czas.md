# Pobierz obecny czas

**Data:** 2023-05-10

---

**User:**

Jak w Scala pobrać obecny czas i datę w formacie czytelnym dla człowieka?

---

**Assistant:**

W języku Scala możesz pobrać obecny czas i datę w formacie czytelnym dla człowieka przy użyciu klasy `java.time.LocalDateTime` oraz formatu daty dostępnego w klasie `java.time.format.DateTimeFormatter`. Oto przykładowy kod:

```scala
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter

val obecnyCzas = LocalDateTime.now()
val formatter = DateTimeFormatter.ofPattern("dd-MM-yyyy HH:mm:ss")
val formatowanaData = obecnyCzas.format(formatter)

println(formatowanaData)
```

Ten kod tworzy obiekt `LocalDateTime` reprezentujący obecny czas. Następnie definiujemy `DateTimeFormatter` z określonym formatem daty i czasu, w tym przypadku "dd-MM-yyyy HH:mm:ss". Wartość `obecnyCzas` jest formatowana przy użyciu tego formattera i zapisywana w zmiennej `formatowanaData`. Na koniec drukujemy sformatowaną datę i czas przy użyciu `println(formatowanaData)`.

Po uruchomieniu tego kodu otrzymasz wynikowy obecny czas i datę w formacie "dd-MM-yyyy HH:mm:ss", na przykład "10-05-2023 15:30:45". Możesz zmienić format daty, korzystając z różnych wzorców dostępnych w klasie `DateTimeFormatter`, aby dostosować wynik do swoich preferencji.