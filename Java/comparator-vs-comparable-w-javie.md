# Comparator vs Comparable w Javie

**Data:** 2024-10-08

---

**User:**

Java, czym różni się Compatator od Comparable? Podaj przykład użycia obu.

---

**Assistant:**

W Javie zarówno `Comparator`, jak i `Comparable` są interfejsami służącymi do porównywania obiektów, jednak różnią się swoim zastosowaniem i sposobem działania.

### Różnice:

1. **Comparable**:
   - Jest używany, gdy chcemy narzucić **naturalny porządek** sortowania obiektów.
   - Klasa implementująca `Comparable` musi nadpisać metodę `compareTo()`.
   - Można zaimplementować tylko jeden sposób porównywania, który jest częścią samej klasy.
   - Interfejs ten znajduje się w pakiecie `java.lang`.
   
   **Sygnatura metody**: 
   ```java
   int compareTo(T obj);
   ```

2. **Comparator**:
   - Jest używany, gdy chcemy zdefiniować **alternatywne porządki** sortowania obiektów.
   - `Comparator` można zaimplementować w osobnej klasie, niezależnie od klasy obiektu, który ma być porównywany.
   - Możemy mieć wiele różnych `Comparatorów` dla jednej klasy.
   - Interfejs ten znajduje się w pakiecie `java.util`.
   
   **Sygnatura metody**: 
   ```java
   int compare(T obj1, T obj2);
   ```

### Przykłady:

1. **Comparable**:

```java
class Product implements Comparable<Product> {
    private String name;
    private double price;

    public Product(String name, double price) {
        this.name = name;
        this.price = price;
    }

    // Implementacja metody compareTo
    @Override
    public int compareTo(Product other) {
        // Naturalny porządek sortowania - według ceny
        return Double.compare(this.price, other.price);
    }

    @Override
    public String toString() {
        return name + ": " + price;
    }
}

public class Main {
    public static void main(String[] args) {
        List<Product> products = new ArrayList<>();
        products.add(new Product("Laptop", 1200.00));
        products.add(new Product("Phone", 800.00));
        products.add(new Product("Tablet", 500.00));

        Collections.sort(products);

        System.out.println("Sortowanie według ceny (Comparable):");
        for (Product p : products) {
            System.out.println(p);
        }
    }
}
```

W tym przypadku klasa `Product` implementuje interfejs `Comparable`, a sortowanie odbywa się według naturalnego porządku (ceny).

2. **Comparator**:

```java
import java.util.Comparator;

class Product {
    private String name;
    private double price;

    public Product(String name, double price) {
        this.name = name;
        this.price = price;
    }

    public String getName() {
        return name;
    }

    public double getPrice() {
        return price;
    }

    @Override
    public String toString() {
        return name + ": " + price;
    }
}

// Implementacja Comparatora do sortowania według nazwy
class ProductNameComparator implements Comparator<Product> {
    @Override
    public int compare(Product p1, Product p2) {
        return p1.getName().compareTo(p2.getName());
    }
}

public class Main {
    public static void main(String[] args) {
        List<Product> products = new ArrayList<>();
        products.add(new Product("Laptop", 1200.00));
        products.add(new Product("Phone", 800.00));
        products.add(new Product("Tablet", 500.00));

        // Sortowanie za pomocą Comparatora
        Collections.sort(products, new ProductNameComparator());

        System.out.println("Sortowanie według nazwy (Comparator):");
        for (Product p : products) {
            System.out.println(p);
        }
    }
}
```

W tym przykładzie używamy `Comparatora` do sortowania produktów według nazwy, co jest alternatywnym porządkiem sortowania w porównaniu do naturalnego porządku według ceny.

### Podsumowanie:
- **Comparable** określa naturalny porządek sortowania wewnątrz klasy, a **Comparator** pozwala definiować zewnętrzne sposoby porównywania obiektów.