# Poprawa kodu Java

**Data:** 2025-03-03

---

**User:**

popraw 
                    Optional.ofNullable(selectedInvolvementIdsAttr.getValue().split(","))
                    .orElse(Collections.emptyList())
                    .stream()
                    .map(String::trim).collect(Collectors.toSet());

---

**Assistant:**

Kod, który podałeś, może generować wyjątek `NullPointerException`, jeśli `getValue()` zwróci `null`. `Optional.ofNullable(...).orElse(...)` nie działa tutaj poprawnie, ponieważ `split(",")` zostanie wywołane na `null`, co spowoduje błąd.  

Poprawiona wersja:  

```java
Set<String> involvementIds = Optional.ofNullable(selectedInvolvementIdsAttr.getValue())
        .map(value -> value.split(","))
        .map(Arrays::asList)
        .orElse(Collections.emptyList())
        .stream()
        .map(String::trim)
        .collect(Collectors.toSet());
```

Poprawki:  
1. `getValue()` jest sprawdzane pod kątem `null` przed wywołaniem `split(",")`.
2. `split(",")` zwraca tablicę, którą zamieniamy na listę za pomocą `Arrays.asList(...)`, aby uniknąć problemów z `orElse(Collections.emptyList())`.
3. Następnie konwersja do `Set<String>` pozostaje bez zmian.

Dzięki temu unikamy `NullPointerException` i kod jest bardziej czytelny. 🚀