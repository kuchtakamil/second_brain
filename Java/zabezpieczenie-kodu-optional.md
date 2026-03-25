# Zabezpieczenie kodu Optional

**Data:** 2025-02-21

---

**User:**

myString może być null. Zabezpiecz ten kod używając Optional
        String myString = getMyString();
        List<String> events = Arrays.asList(myString.split(",")).stream()
                .map(String::trim).collect(Collectors.toList());
        final List<Attribute> attrs = getAttr()
                .stream().filter(attr -> events.contains(attr.getType()))
                .collect(Collectors.toList());

---

**Assistant:**

Oto wersja kodu zabezpieczona przy użyciu `Optional`:  

```java
import java.util.*;
import java.util.stream.Collectors;

public class Main {
    public static void main(String[] args) {
        String myString = getMyString();
        
        List<String> events = Optional.ofNullable(myString)
                .map(s -> Arrays.asList(s.split(",")))
                .orElse(Collections.emptyList())
                .stream()
                .map(String::trim)
                .collect(Collectors.toList());

        List<Attribute> attrs = getAttr()
                .stream()
                .filter(attr -> events.contains(attr.getType()))
                .collect(Collectors.toList());
    }

    private static String getMyString() {
        return null; // Przykładowa metoda, może zwracać null
    }

    private static List<Attribute> getAttr() {
        return List.of(new Attribute("type1"), new Attribute("type2"));
    }

    static class Attribute {
        private final String type;

        public Attribute(String type) {
            this.type = type;
        }

        public String getType() {
            return type;
        }
    }
}
```

### Co zostało poprawione?
1. **Użycie `Optional.ofNullable(myString)`** – jeśli `myString` jest `null`, `Optional` przejdzie do `orElse(Collections.emptyList())`, zapobiegając `NullPointerException`.
2. **Zapewnienie, że `events` nie jest `null`** – jeśli `myString` jest `null`, `events` zostanie ustawione na pustą listę.
3. **Reszta kodu pozostaje niezmieniona** – `attrs` jest przetwarzane tak jak wcześniej, ale teraz mamy pewność, że `events` nigdy nie będzie `null`.

Teraz kod jest odporny na przypadek, gdy `getMyString()` zwraca `null`. 🚀