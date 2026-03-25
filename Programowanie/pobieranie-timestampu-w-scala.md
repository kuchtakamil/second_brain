# Pobieranie timestampu w Scala

**Data:** 2023-08-28

---

**User:**

Scala, jak pobrać aktualny timestamp

---

**Assistant:**

W języku Scala możesz pobrać aktualny timestamp (czas w milisekundach lub sekundach) na kilka różnych sposobów. Oto przykłady:

1. **Użycie klasy `System` w Javie:**

   Scala dziedziczy wiele klas i funkcji z języka Java, więc możesz użyć klasy `System` do uzyskania aktualnego czasu w milisekundach lub sekundach.

   ```scala
   val currentTimeMillis: Long = System.currentTimeMillis()
   val currentTimeSeconds: Long = System.currentTimeMillis() / 1000
   ```

2. **Użycie biblioteki `java.time` (dostępnej w Scala od wersji 2.13):**

   Scala od wersji 2.13 ma wbudowaną obsługę biblioteki `java.time`, która oferuje bardziej nowoczesne i elastyczne API do pracy z datami i czasami.

   ```scala
   import java.time.Instant

   val instant: Instant = Instant.now()  // Aktualny czas i data
   val epochMillis: Long = instant.toEpochMilli()  // Czas w milisekundach od 1970-01-01T00:00:00Z
   val epochSeconds: Long = instant.getEpochSecond()  // Czas w sekundach od 1970-01-01T00:00:00Z
   ```

3. **Użycie `System.nanoTime()`:**

   `System.nanoTime()` zwraca czas w nanosekundach. Należy jednak pamiętać, że wartość ta jest związana z precyzją i dokładnością sprzętu, a nie z reprezentacją czasu rzeczywistego.

   ```scala
   val nanoTime: Long = System.nanoTime()
   ```

Wybór metody zależy od twoich potrzeb. Jeśli pracujesz z datami i czasami w bardziej zaawansowany sposób, użycie biblioteki `java.time` jest zdecydowanie rekomendowane. Jeśli potrzebujesz po prostu czasu w milisekundach lub sekundach od punktu odniesienia, `System.currentTimeMillis()` lub `Instant.now().toEpochMilli()` będą odpowiednie.