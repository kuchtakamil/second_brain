# Pattern Matching w Javie 17

**Data:** 2025-10-03

---

**User:**

Zademonstruj jak działa Pattern Matching w Javie 17

---

**Assistant:**

W Javie 17 **Pattern Matching** pojawia się w kilku miejscach, przede wszystkim:  

1. **Pattern Matching dla `instanceof`** (stało się standardem od Javy 16, w 17 też jest dostępne).  
2. **Pattern Matching dla `switch`** (w Javie 17 jako *preview feature* – wymaga włączenia flag kompilatora `--enable-preview`).  

---

### 1. Pattern Matching dla `instanceof`
Zamiast pisać kod w stylu:  

```java
Object obj = "Hello Java 17!";

if (obj instanceof String) {
    String s = (String) obj; // konieczny był rzut
    System.out.println(s.toUpperCase());
}
```

można teraz uprościć go do:  

```java
Object obj = "Hello Java 17!";

if (obj instanceof String s) { // od razu tworzy zmienną s
    System.out.println(s.toUpperCase());
}
```

✔️ Dzięki temu unikamy powtarzania rzutowania.  

---

### 2. Pattern Matching dla `switch` (preview w Javie 17)
Pozwala stosować dopasowanie typów w `switch`.  
Przykład:

```java
public class PatternMatchingSwitch {
    public static void main(String[] args) {
        System.out.println(formatter(123));
        System.out.println(formatter("tekst"));
        System.out.println(formatter(3.14));
    }

    static String formatter(Object obj) {
        return switch (obj) {
            case Integer i -> String.format("Liczba całkowita: %d", i);
            case String s -> String.format("Napis o długości %d", s.length());
            case Double d -> String.format("Liczba zmiennoprzecinkowa: %.2f", d);
            case null -> "To jest null!";
            default -> obj.toString();
        };
    }
}
```

Dzięki temu `switch` potrafi rozróżniać **typy**, nie tylko wartości.  

⚠️ Aby to uruchomić w Javie 17, trzeba kompilować i uruchamiać z flagą:  
```
javac --enable-preview --release 17 PatternMatchingSwitch.java
java --enable-preview PatternMatchingSwitch
```

---

Chcesz, żebym przygotował dla Ciebie **pełny przykład projektu Maven/Gradle**, w którym można to od razu uruchomić i zobaczyć w praktyce?

---

**User:**

czy coś zmieniło się w tym temacie w następnych nowszych wersjach java?

---

**Assistant:**

Tak, sporo się zmieniało po Javie 17, bo pattern matching to jedna z głównych ewolucji języka. Chronologicznie wyglądało to tak:  

---

### **Java 17 (LTS)**  
- **Pattern Matching for `instanceof`** – finalna funkcjonalność.  
- **Pattern Matching for `switch`** – *preview feature*.  

---

### **Java 18**  
- Nic istotnego w pattern matching (głównie zmiany w API / incubatorach).  

---

### **Java 19**  
- **Pattern Matching for `switch`** – *2nd preview*.  
- **Record Patterns** – *preview feature* (pierwsza wersja).  
  - Możesz rozkładać rekordy bezpośrednio w warunku:  

  ```java
  record Point(int x, int y) {}

  static String print(Object obj) {
      return switch (obj) {
          case Point(int x, int y) -> "Point: (" + x + ", " + y + ")";
          default -> obj.toString();
      };
  }
  ```

---

### **Java 20**  
- **Pattern Matching for `switch`** – *3rd preview* (poprawki).  
- **Record Patterns** – *2nd preview*.  

---

### **Java 21 (LTS)**  
- **Pattern Matching for `switch`** – **finalna funkcjonalność** (weszło na stałe).  
- **Record Patterns** – **finalna funkcjonalność**.  
- Dodano możliwość łączenia obu w `switch`.  

  Przykład:  

  ```java
  sealed interface Shape permits Circle, Rectangle {}
  record Circle(double r) implements Shape {}
  record Rectangle(double w, double h) implements Shape {}

  static String describe(Shape s) {
      return switch (s) {
          case Circle(double r) -> "Koło o promieniu " + r;
          case Rectangle(double w, double h) -> "Prostokąt " + w + "x" + h;
      };
  }
  ```

---

### **Java 22 i 23**  
- Rozwój tzw. **Unnamed Patterns & Variables** (ułatwienia typu `_` w miejscach, gdzie zmienna jest zbędna).  
- W `switch` można pisać np.:  

  ```java
  case Rectangle(_, int h) -> "Prostokąt o wysokości " + h;
  ```

---

✅ **Podsumowanie**:  
- Od Javy 17 → tylko `instanceof` i *preview switch*.  
- Od Javy 21 → `switch` + `record patterns` są już **stabilne** i można ich używać w produkcji.  
- W nowszych wersjach (22, 23) trwają już tylko kosmetyczne usprawnienia.  

---

Chcesz, żebym zrobił tabelę porównującą **które wersje Javy wprowadziły które elementy pattern matchingu** (tak, żeby było to w jednym miejscu klarowne)?