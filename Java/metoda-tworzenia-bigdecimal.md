# Metoda tworzenia BigDecimal

**Data:** 2024-10-08

---

**User:**

W java chcę zrobić metodę która zwróci Optional<BigDecimal> a jeśli nie jest to możliwe zwróci Optional empty. Popraw:

   static Optional<BigDecimal> createBigDecimal(String str) {
        return new BigDecimal(str);
    }

---

**Assistant:**

Aby poprawić metodę, która zwraca `Optional<BigDecimal>`, musisz obsłużyć wyjątek, który może być rzucony podczas tworzenia obiektu `BigDecimal`. W przypadku niepoprawnego formatu liczby, `BigDecimal` rzuci wyjątek `NumberFormatException`. Możesz go przechwycić i zwrócić `Optional.empty()` w przypadku błędu.

Oto poprawiona wersja metody:

```java
import java.math.BigDecimal;
import java.util.Optional;

static Optional<BigDecimal> createBigDecimal(String str) {
    try {
        return Optional.of(new BigDecimal(str));
    } catch (NumberFormatException e) {
        return Optional.empty();
    }
}
```

W tej wersji:
- `Optional.of(new BigDecimal(str))` zwraca wartość, jeśli `str` jest poprawną liczbą.
- Jeśli `BigDecimal` rzuci wyjątek, `catch` zwraca `Optional.empty()`.