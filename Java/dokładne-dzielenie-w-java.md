# Dokładne dzielenie w Java

**Data:** 2024-02-17

---

**User:**

jak w java zapisać dzielenie 11 / 2 aby uzyskać dokładny wynik

---

**Assistant:**

W języku Java, aby uzyskać dokładny wynik dzielenia liczb, jedną z opcji jest użycie typu danych zmiennoprzecinkowego, na przykład `double` lub `BigDecimal`. Oto przykłady dla obu typów:

### Użycie typu `double`:
```java
public class Dzielenie {
    public static void main(String[] args) {
        double wynik = 11.0 / 2.0;
        System.out.println("Wynik: " + wynik);
    }
}
```

### Użycie typu `BigDecimal`:
```java
import java.math.BigDecimal;

public class Dzielenie {
    public static void main(String[] args) {
        BigDecimal liczba1 = new BigDecimal("11");
        BigDecimal liczba2 = new BigDecimal("2");
        
        BigDecimal wynik = liczba1.divide(liczba2);
        System.out.println("Wynik: " + wynik);
    }
}
```

Użycie `BigDecimal` jest szczególnie przydatne w przypadku precyzyjnych obliczeń, ale należy pamiętać, że operacje na `BigDecimal` są mniej efektywne niż na typach prymitywnych, takich jak `double`. Wybór między nimi zależy od konkretnych wymagań Twojego programu.

---

**User:**

double wynik = 11.0 / 2.0; daje 5.0 a ja chę uzyskać 5.5.
Nie chcę używać BigDecimal

---

**Assistant:**

Przepraszam za błąd. Jeśli chcesz uzyskać dokładny wynik dzielenia 11 przez 2 jako 5.5, możesz użyć jednej z poniższych opcji:

### Użycie liczby zmiennoprzecinkowej jako rezultatu:
```java
public class Dzielenie {
    public static void main(String[] args) {
        double wynik = (double) 11 / 2;
        System.out.println("Wynik: " + wynik);
    }
}
```

### Użycie rzutowania jednej z liczb na `double`:
```java
public class Dzielenie {
    public static void main(String[] args) {
        double wynik = 11 / (double) 2;
        System.out.println("Wynik: " + wynik);
    }
}
```

W obu przypadkach wynik powinien być 5.5, ponieważ jedna z liczb jest rzutowana na typ `double` przed wykonaniem dzielenia.