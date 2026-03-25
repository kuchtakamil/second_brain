# Sprawdzanie pustego stringa

**Data:** 2024-12-08

---

**User:**

jak w java sprawdzić czy string jest pusty lub jest nullem?

---

**Assistant:**

W Javie możesz sprawdzić, czy string jest pusty lub nullem, używając metody statycznej z klasy `Objects` lub kombinacji metod wbudowanych w `String`. Oto kilka podejść:

### 1. **Użycie `Objects.isNull` lub `Objects.nonNull`**
```java
import java.util.Objects;

String str = null;

// Sprawdzenie
if (Objects.isNull(str) || str.isEmpty()) {
    System.out.println("String jest pusty lub null");
}
```

### 2. **Tradycyjne podejście z `if`**
```java
String str = null;

if (str == null || str.isEmpty()) {
    System.out.println("String jest pusty lub null");
}
```

### 3. **Użycie `StringUtils` z Apache Commons Lang**
Biblioteka Apache Commons Lang oferuje wygodne metody:
```java
import org.apache.commons.lang3.StringUtils;

String str = null;

if (StringUtils.isEmpty(str)) {
    System.out.println("String jest pusty lub null");
}
```

### 4. **Użycie `StringUtils` z Spring Framework**
Jeśli używasz Springa, możesz skorzystać z `org.springframework.util.StringUtils`:
```java
import org.springframework.util.StringUtils;

String str = null;

if (!StringUtils.hasLength(str)) {
    System.out.println("String jest pusty lub null");
}
```

### 5. **Własna metoda**
Jeśli chcesz mieć bardziej elastyczną funkcję, możesz stworzyć własną metodę:
```java
public static boolean isNullOrEmpty(String str) {
    return str == null || str.isEmpty();
}

// Przykład użycia
String str = null;

if (isNullOrEmpty(str)) {
    System.out.println("String jest pusty lub null");
}
```

Wybierz rozwiązanie, które najlepiej pasuje do Twojego projektu i zależności. Jeśli używasz Springa, możesz wykorzystać jego klasy. Jeśli nie masz dodatkowych zależności, rozwiązanie standardowe (np. `if`) jest wystarczające.