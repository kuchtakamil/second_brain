# Java: Użycie funkcji groupingBy

**Data:** 2023-09-10

---

**User:**

Java, podaj przykłady użycia funkcji groupingBy

---

**Assistant:**

Funkcja `groupingBy` jest często używana w języku Java w połączeniu z kolekcjami, zwłaszcza w kontekście strumieni (Streams) i operacji na strumieniach, takich jak `Collectors.groupingBy`. Pozwala ona grupować elementy na podstawie określonego kryterium lub klucza. Oto kilka przykładów użycia funkcji `groupingBy`:

1. Grupowanie liczb całkowitych po parzystości:

```java
List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);

Map<Boolean, List<Integer>> evenOddGroups = numbers.stream()
    .collect(Collectors.groupingBy(n -> n % 2 == 0));

System.out.println("Parzyste: " + evenOddGroups.get(true));
System.out.println("Nieparzyste: " + evenOddGroups.get(false));
```

2. Grupowanie osób według wieku:

```java
class Person {
    private String name;
    private int age;

    // konstruktor, gettery, settery
}

List<Person> people = Arrays.asList(
    new Person("Anna", 25),
    new Person("Jan", 30),
    new Person("Karolina", 25),
    new Person("Piotr", 35),
    new Person("Maria", 30)
);

Map<Integer, List<Person>> peopleByAge = people.stream()
    .collect(Collectors.groupingBy(Person::getAge));

peopleByAge.forEach((age, group) -> {
    System.out.println("Wiek " + age + ": " + group);
});
```

3. Grupowanie słów po długości:

```java
List<String> words = Arrays.asList("kot", "pies", "auto", "rower", "dom", "drzewo");

Map<Integer, List<String>> wordsByLength = words.stream()
    .collect(Collectors.groupingBy(String::length));

wordsByLength.forEach((length, group) -> {
    System.out.println("Długość " + length + ": " + group);
});
```

4. Grupowanie obiektów po dowolnym kryterium:

```java
class Product {
    private String category;
    private String name;

    // konstruktor, gettery, settery
}

List<Product> products = Arrays.asList(
    new Product("Elektronika", "Telewizor"),
    new Product("Kuchnia", "Mikrofalówka"),
    new Product("Elektronika", "Smartfon"),
    new Product("Kuchnia", "Lodówka"),
    new Product("Elektronika", "Laptop")
);

Map<String, List<Product>> productsByCategory = products.stream()
    .collect(Collectors.groupingBy(Product::getCategory));

productsByCategory.forEach((category, group) -> {
    System.out.println("Kategoria " + category + ": " + group);
});
```

Te przykłady pokazują różne przypadki użycia funkcji `groupingBy` w języku Java do grupowania elementów w kolekcjach na podstawie różnych kryteriów.

---

**User:**

Podaj bardziej skomplikowany przykład, możesz użyć również innych funkcji

---

**Assistant:**

Oto bardziej skomplikowany przykład, który wykorzystuje funkcję `groupingBy` w połączeniu z innymi funkcjami, takimi jak `summingInt` i `mapping`. Przyjmijmy, że mamy listę zamówień i chcemy zgrupować je po kategorii produktu, a następnie obliczyć łączną kwotę zamówień w każdej kategorii:

```java
import java.util.*;
import java.util.stream.Collectors;

class Order {
    private String productName;
    private String category;
    private double price;

    public Order(String productName, String category, double price) {
        this.productName = productName;
        this.category = category;
        this.price = price;
    }

    public String getCategory() {
        return category;
    }

    public double getPrice() {
        return price;
    }

    // Pozostałe gettery i settery
}

public class GroupingExample {
    public static void main(String[] args) {
        List<Order> orders = Arrays.asList(
            new Order("Telewizor", "Elektronika", 1200.0),
            new Order("Smartfon", "Elektronika", 800.0),
            new Order("Lodówka", "AGD", 1500.0),
            new Order("Mikrofalówka", "AGD", 300.0),
            new Order("Buty", "Moda", 100.0),
            new Order("Koszula", "Moda", 50.0)
        );

        // Grupowanie zamówień po kategorii produktu i obliczenie sumy zamówień w każdej kategorii
        Map<String, Double> totalAmountByCategory = orders.stream()
            .collect(Collectors.groupingBy(
                Order::getCategory,
                Collectors.summingDouble(Order::getPrice)
            ));

        totalAmountByCategory.forEach((category, totalAmount) -> {
            System.out.println("Kategoria: " + category + ", Suma zamówień: " + totalAmount);
        });
    }
}
```

W tym przykładzie używamy `groupingBy` do grupowania zamówień po kategorii produktu. Następnie używamy `summingDouble` wewnątrz `groupingBy`, aby obliczyć łączną kwotę zamówień w każdej kategorii. Wynik jest mapą, gdzie kluczem jest kategoria, a wartością jest suma zamówień w danej kategorii.

---

**User:**

kolejny proszę

---

**Assistant:**

Oto bardziej skomplikowany przykład, który wykorzystuje funkcję `groupingBy` w połączeniu z innymi funkcjami i operacjami na strumieniach. W przykładzie tym będziemy mieli listę studentów i ich ocen w różnych przedmiotach, a następnie zgrupujemy studentów według ocen w przedmiotach i obliczymy średnią ocenę dla każdego studenta w każdym przedmiocie:

```java
import java.util.*;
import java.util.stream.Collectors;

class Student {
    private String name;
    private Map<String, Integer> grades;

    public Student(String name, Map<String, Integer> grades) {
        this.name = name;
        this.grades = grades;
    }

    public String getName() {
        return name;
    }

    public Map<String, Integer> getGrades() {
        return grades;
    }

    // Pozostałe gettery i settery
}

public class GroupingExample {
    public static void main(String[] args) {
        List<Student> students = Arrays.asList(
            new Student("Anna", Map.of("Matematyka", 90, "Fizyka", 85, "Chemia", 92)),
            new Student("Jan", Map.of("Matematyka", 78, "Fizyka", 88, "Chemia", 95)),
            new Student("Karolina", Map.of("Matematyka", 85, "Fizyka", 92, "Chemia", 87)),
            new Student("Piotr", Map.of("Matematyka", 88, "Fizyka", 76, "Chemia", 90))
        );

        // Grupowanie studentów według ocen w przedmiotach i obliczenie średniej oceny dla każdego studenta w każdym przedmiocie
        Map<String, Map<String, Double>> averageGradesByStudentAndSubject = students.stream()
            .collect(Collectors.groupingBy(
                Student::getName,
                Collectors.toMap(
                    Map.Entry::getKey,
                    entry -> entry.getValue().values().stream()
                        .mapToDouble(Integer::doubleValue)
                        .average()
                        .orElse(0.0)
                )
            ));

        averageGradesByStudentAndSubject.forEach((student, gradesBySubject) -> {
            System.out.println("Student: " + student);
            gradesBySubject.forEach((subject, averageGrade) -> {
                System.out.println("  Przedmiot: " + subject + ", Średnia ocena: " + averageGrade);
            });
        });
    }
}
```

W tym przykładzie używamy `groupingBy` do grupowania studentów według ich imion. Następnie używamy `toMap` wewnątrz `groupingBy`, aby utworzyć mapę ocen dla każdego studenta, gdzie klucz to przedmiot, a wartość to średnia ocena. Ostatecznie otrzymujemy mapę, w której kluczem jest imię studenta, a wartością jest mapa przedmiotów i ich średnich ocen.

---

**User:**

Napisz przykład użycia Stream.of

---

**Assistant:**

`Stream.of` jest używane do tworzenia strumienia z określonych elementów. Możesz przekazać dowolną ilość argumentów do `Stream.of`, a te elementy zostaną przekształcone w strumień. Oto przykład użycia `Stream.of`:

```java
import java.util.stream.Stream;

public class StreamOfExample {
    public static void main(String[] args) {
        // Tworzenie strumienia z kilku elementów
        Stream<String> stringStream = Stream.of("jabłko", "banan", "gruszka", "śliwka");

        // Wyświetlanie elementów strumienia
        stringStream.forEach(System.out::println);

        // Tworzenie strumienia z liczb całkowitych
        Stream<Integer> integerStream = Stream.of(1, 2, 3, 4, 5);

        // Wyświetlanie elementów strumienia
        integerStream.forEach(System.out::println);

        // Tworzenie strumienia z obiektów niestandardowych
        Stream<Person> personStream = Stream.of(
            new Person("Anna", 25),
            new Person("Jan", 30),
            new Person("Karolina", 25),
            new Person("Piotr", 35)
        );

        // Wyświetlanie elementów strumienia
        personStream.forEach(person -> System.out.println(person.getName() + " - " + person.getAge()));
    }
}

class Person {
    private String name;
    private int age;

    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    public String getName() {
        return name;
    }

    public int getAge() {
        return age;
    }
}
```

W powyższym przykładzie używamy `Stream.of` do utworzenia trzech różnych strumieni: strumienia ciągów znaków (String), strumienia liczb całkowitych (Integer) oraz strumienia obiektów niestandardowych (Person). Następnie używamy `forEach`, aby wyświetlić elementy każdego z tych strumieni.

---

**User:**

Podaj przykład zastosowania IntStream

---

**Assistant:**

`IntStream` jest specjalnym rodzajem strumienia w Javie, który zawiera elementy typu `int`. Jest używany do przetwarzania danych numerycznych w bardziej wydajny sposób niż ogólny `Stream` zawierający obiekty. Oto przykład zastosowania `IntStream` do generowania i przetwarzania liczb całkowitych:

```java
import java.util.Arrays;
import java.util.IntSummaryStatistics;
import java.util.stream.IntStream;

public class IntStreamExample {
    public static void main(String[] args) {
        // Tworzenie IntStream z tablicy liczb całkowitych
        int[] numbers = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
        IntStream intStream = Arrays.stream(numbers);

        // Wyświetlanie wszystkich liczb w strumieniu
        intStream.forEach(System.out::println);

        // Tworzenie IntStream za pomocą range
        IntStream.range(1, 6)
            .forEach(System.out::println);

        // Przykład operacji mapToInt
        int sum = Arrays.stream(numbers)
            .mapToInt(x -> x * 2)
            .sum();
        System.out.println("Suma podwójnych liczb: " + sum);

        // Przykład operacji filter
        IntStream evenNumbers = Arrays.stream(numbers)
            .filter(x -> x % 2 == 0);
        evenNumbers.forEach(System.out::println);

        // Przykład operacji statistics
        IntSummaryStatistics stats = Arrays.stream(numbers)
            .summaryStatistics();
        System.out.println("Statystyki: " +
            "średnia=" + stats.getAverage() +
            ", suma=" + stats.getSum() +
            ", maksimum=" + stats.getMax() +
            ", minimum=" + stats.getMin()
        );
    }
}
```

W tym przykładzie używamy `IntStream` do przetwarzania liczb całkowitych. Pokazujemy, jak utworzyć `IntStream` z tablicy, generować liczby w określonym zakresie za pomocą `range`, przekształcać elementy strumienia za pomocą `mapToInt`, filtrować elementy za pomocą `filter` oraz uzyskiwać statystyki liczbowe za pomocą `summaryStatistics`. `IntStream` jest przydatny, gdy pracujesz z dużą ilością danych numerycznych, ponieważ umożliwia bardziej wydajne operacje na liczbach całkowitych.

---

**User:**

Podaj przykład użycia Collectors.groupingBy(Function.identity())
Podaj przykładowe dane wejściowe i wyjściowe

---

**Assistant:**

`Collectors.groupingBy(Function.identity())` jest używane do grupowania elementów strumienia na podstawie ich własnych wartości, czyli utworzenia grupy dla każdego unikalnego elementu w strumieniu. Oto przykład użycia z przykładowymi danymi wejściowymi i wyjściowymi:

Załóżmy, że mamy listę owoców, i chcemy je zgrupować na podstawie ich nazw:

```java
import java.util.*;
import java.util.stream.Collectors;

public class GroupingByIdentityExample {
    public static void main(String[] args) {
        List<String> fruits = Arrays.asList("jabłko", "banan", "gruszka", "banan", "jabłko", "śliwka", "jabłko");

        Map<String, List<String>> groupedFruits = fruits.stream()
            .collect(Collectors.groupingBy(Function.identity()));

        groupedFruits.forEach((fruit, occurrences) -> {
            System.out.println("Owoc: " + fruit + ", Liczba wystąpień: " + occurrences.size());
        });
    }
}
```

W tym przykładzie mamy listę owoców, w której pojawiają się powtórzenia. Korzystając z `Collectors.groupingBy(Function.identity())`, grupujemy te owoce na podstawie ich własnych nazw. Wynik jest mapą, gdzie kluczem jest nazwa owocu, a wartością jest lista tych owoców. Dla powyższego przykładu dane wyjściowe mogą wyglądać tak:

```
Owoc: jabłko, Liczba wystąpień: 3
Owoc: banan, Liczba wystąpień: 2
Owoc: gruszka, Liczba wystąpień: 1
Owoc: śliwka, Liczba wystąpień: 1
```

Jak widać, `Collectors.groupingBy(Function.identity())` pomaga w grupowaniu elementów na podstawie ich własnych wartości i tworzeniu listy elementów w każdej grupie.