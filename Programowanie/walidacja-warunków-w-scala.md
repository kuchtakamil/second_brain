# Walidacja warunków w Scala

**Data:** 2023-08-21

---

**User:**

Jaka jest najlepsza metoda sprawdzania warunków początkowych w Scala. Np. sprawdzanie czy przekazana liczba jako parametr funkcji nie jest ujemna

---

**Assistant:**

W języku Scala istnieje wiele sposobów sprawdzania warunków początkowych, takich jak sprawdzanie czy przekazana liczba jako parametr funkcji nie jest ujemna. Oto kilka sposobów, które możesz zastosować:

1. **Instrukcja `require`**:
   Instrukcja `require` pochodzi z pakietu `scala.Predef` i służy do sprawdzania warunków początkowych. Jeśli warunek jest niespełniony, zostanie zgłoszony wyjątek `IllegalArgumentException`. Przykład:

   ```scala
   def doSomething(number: Int): Unit = {
       require(number >= 0, "Number must be non-negative")
       // reszta kodu
   }
   ```

2. **Instrukcja `assert`**:
   Instrukcja `assert` jest również dostępna w pakiecie `scala.Predef` i służy do sprawdzania warunków w trakcie debugowania. Jeśli warunek jest niespełniony, zostanie zgłoszony wyjątek `AssertionError`. Jednak zazwyczaj nie jest zalecana do walidacji warunków w kodzie produkcyjnym.

   ```scala
   def doSomething(number: Int): Unit = {
       assert(number >= 0, "Number must be non-negative")
       // reszta kodu
   }
   ```

3. **Option lub Either**:
   Jeśli chcesz obsłużyć warunki początkowe w bardziej funkcyjny sposób, możesz użyć typu `Option` lub `Either`. Przykład z użyciem `Option`:

   ```scala
   def doSomething(number: Int): Option[Unit] = {
       if (number >= 0) Some(()) else None
   }
   ```

   Przykład z użyciem `Either`:

   ```scala
   def doSomething(number: Int): Either[String, Unit] = {
       if (number >= 0) Right(()) else Left("Number must be non-negative")
   }
   ```

4. **Pattern Matching**:
   Możesz również zastosować wzorzec dopasowania do warunków początkowych wewnątrz funkcji. To pozwala na bardziej zaawansowaną obsługę różnych przypadków.

   ```scala
   def doSomething(number: Int): Unit = number match {
       case n if n >= 0 => // reszta kodu
       case _ => throw new IllegalArgumentException("Number must be non-negative")
   }
   ```

5. **Walidacja przy użyciu typów**:
   Innym podejściem może być użycie typów, które samodzielnie gwarantują pewne warunki. Przykładowo, możesz zdefiniować własny typ dla nieujemnych liczb:

   ```scala
   case class NonNegativeInt(value: Int) {
       require(value >= 0, "Value must be non-negative")
   }
   
   def doSomething(number: NonNegativeInt): Unit = {
       // reszta kodu
   }
   ```

Którą metodę wybierzesz, zależy od kontekstu i preferencji. Warto również rozważyć, który sposób będzie najlepiej odpowiadać strukturze i wymaganiom twojego projektu.