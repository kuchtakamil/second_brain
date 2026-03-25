# Builder Pattern in Java

**Data:** 2024-02-22

---

**User:**

Podaj przykład wzorca Builder w Java

---

**Assistant:**

Wzorzec Builder to wzorzec projektowy, który pozwala na konstrukcję złożonych obiektów krok po kroku. Oto prosty przykład implementacji wzorca Builder w języku Java:

```java
// Klasa reprezentująca złożony obiekt, który chcemy skonstruować
class Product {
    private String part1;
    private String part2;

    public void setPart1(String part1) {
        this.part1 = part1;
    }

    public void setPart2(String part2) {
        this.part2 = part2;
    }

    @Override
    public String toString() {
        return "Product [part1=" + part1 + ", part2=" + part2 + "]";
    }
}

// Interfejs Buildera
interface Builder {
    void buildPart1(String part1);
    void buildPart2(String part2);
    Product getResult();
}

// Konkretna implementacja Buildera
class ConcreteBuilder implements Builder {
    private Product product = new Product();

    @Override
    public void buildPart1(String part1) {
        product.setPart1(part1);
    }

    @Override
    public void buildPart2(String part2) {
        product.setPart2(part2);
    }

    @Override
    public Product getResult() {
        return product;
    }
}

// Dyrektor - kontroluje proces konstrukcji
class Director {
    private Builder builder;

    public Director(Builder builder) {
        this.builder = builder;
    }

    public void construct() {
        builder.buildPart1("Part 1");
        builder.buildPart2("Part 2");
    }
}

// Przykładowe użycie wzorca Builder
public class BuilderExample {
    public static void main(String[] args) {
        Builder builder = new ConcreteBuilder();
        Director director = new Director(builder);

        director.construct();
        Product product = builder.getResult();

        System.out.println("Zbudowany produkt: " + product);
    }
}
```

W tym przykładzie mamy klasę `Product`, która reprezentuje złożony obiekt, interfejs `Builder` oraz jego konkretną implementację `ConcreteBuilder`. Klasa `Director` kontroluje proces konstrukcji obiektu za pomocą Buildera. W przykładowym użyciu, obiekt `Product` jest konstruowany przy użyciu `ConcreteBuilder`, a następnie wyświetlamy wynikową strukturę obiektu.

---

**User:**

A taki przykład gdzie wykorzystana jest wersja z return this;

---

**Assistant:**

Oczywiście, możemy dostosować przykład tak, aby korzystać z konstrukcji "return this" w metodach budujących. Oto zmodyfikowany przykład:

```java
// Klasa reprezentująca złożony obiekt, który chcemy skonstruować
class Product {
    private String part1;
    private String part2;

    public Product() {
        // Konstruktor domyślny
    }

    public void setPart1(String part1) {
        this.part1 = part1;
    }

    public void setPart2(String part2) {
        this.part2 = part2;
    }

    @Override
    public String toString() {
        return "Product [part1=" + part1 + ", part2=" + part2 + "]";
    }
}

// Interfejs Buildera z metodami zwracającymi this
interface Builder {
    Builder buildPart1(String part1);
    Builder buildPart2(String part2);
    Product getResult();
}

// Konkretna implementacja Buildera
class ConcreteBuilder implements Builder {
    private Product product = new Product();

    @Override
    public Builder buildPart1(String part1) {
        product.setPart1(part1);
        return this;
    }

    @Override
    public Builder buildPart2(String part2) {
        product.setPart2(part2);
        return this;
    }

    @Override
    public Product getResult() {
        return product;
    }
}

// Dyrektor - kontroluje proces konstrukcji
class Director {
    private Builder builder;

    public Director(Builder builder) {
        this.builder = builder;
    }

    public void construct() {
        builder.buildPart1("Part 1").buildPart2("Part 2");
    }
}

// Przykładowe użycie wzorca Builder z return this
public class BuilderExample {
    public static void main(String[] args) {
        Builder builder = new ConcreteBuilder();
        Director director = new Director(builder);

        director.construct();
        Product product = builder.getResult();

        System.out.println("Zbudowany produkt: " + product);
    }
}
```

W tym przykładzie metody `buildPart1` i `buildPart2` z interfejsu `Builder` zwracają obiekt typu `Builder` (czyli `this`). Dzięki temu można łańcuchowo wywoływać te metody podczas konstrukcji obiektu.