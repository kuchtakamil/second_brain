# Sealed class w Javie

**Data:** 2025-10-03

---

**User:**

Zademonstruj jak działa Sealed class w Javie 17

---

**Assistant:**

W Javie 17 wprowadzono **sealed classes** i **sealed interfaces**, które pozwalają kontrolować **kto może dziedziczyć** po danej klasie lub implementować dany interfejs.  

Dzięki temu można ograniczyć hierarchię dziedziczenia do jasno określonego zestawu klas.  

---

### Przykład:

```java
// Klasa sealed - tylko wybrane klasy mogą po niej dziedziczyć
public sealed class Shape
    permits Circle, Rectangle, Square {

    // wspólne metody
    public abstract double area();
}

// Klasa final - nie można po niej dalej dziedziczyć
public final class Circle extends Shape {
    private final double radius;

    public Circle(double radius) {
        this.radius = radius;
    }

    @Override
    public double area() {
        return Math.PI * radius * radius;
    }
}

// Klasa sealed – można rozszerzać, ale tylko przez dozwolone klasy
public sealed class Rectangle extends Shape
    permits FilledRectangle, TransparentRectangle {

    protected final double width;
    protected final double height;

    public Rectangle(double width, double height) {
        this.width = width;
        this.height = height;
    }

    @Override
    public double area() {
        return width * height;
    }
}

// Klasa non-sealed – pozwala na dalsze dziedziczenie bez ograniczeń
public non-sealed class Square extends Shape {
    private final double side;

    public Square(double side) {
        this.side = side;
    }

    @Override
    public double area() {
        return side * side;
    }
}

// Przykład rozszerzeń Rectangle
public final class FilledRectangle extends Rectangle {
    public FilledRectangle(double w, double h) {
        super(w, h);
    }
}

public final class TransparentRectangle extends Rectangle {
    public TransparentRectangle(double w, double h) {
        super(w, h);
    }
}
```

---

### Zasady
1. **sealed** – klasa/interfejs określa dokładnie, kto może po nim dziedziczyć (lista `permits`).
2. Klasy potomne muszą być jedną z trzech rzeczy:
   - **final** – nie można ich dalej rozszerzać.
   - **sealed** – mogą być dalej dziedziczone, ale tylko przez określone klasy.
   - **non-sealed** – otwierają hierarchię i pozwalają na dalsze dziedziczenie bez ograniczeń.
3. Słowo kluczowe `permits` można pominąć, jeśli klasy znajdują się w tym samym pliku źródłowym.

---

### Użycie w `switch` (pattern matching)

Ponieważ hierarchia jest **zamknięta**, kompilator wie, że rozpatrzył wszystkie przypadki:

```java
public static String describeShape(Shape shape) {
    return switch (shape) {
        case Circle c -> "Koło o polu " + c.area();
        case Rectangle r -> "Prostokąt o polu " + r.area();
        case Square s -> "Kwadrat o polu " + s.area();
    };
}
```

Tutaj **nie potrzeba** domyślnego `default`, bo `Shape` jest sealed i kompilator wie, że uwzględniliśmy wszystkie możliwe typy.  

---

Chcesz, żebym przygotował dla Ciebie **krótki projekt Maven/Gradle** z tym przykładem, który możesz od razu uruchomić?