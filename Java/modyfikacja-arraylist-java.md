# Modyfikacja ArrayList - Java

**Data:** 2023-07-13

---

**User:**

java czy przy ArrayList wypełnionej 13 elementami, gdy chcę dodać element pod indexem 4, to tworzy się nowy obiekt ArrayList odpowiednio zmodyfikowany, czy modyfikowany jest stary obiekt?

---

**Assistant:**

W przypadku klasy `ArrayList` w języku Java, gdy dodajesz element pod określonym indeksem, nie tworzy się nowy obiekt `ArrayList`. Zamiast tego modyfikowany jest istniejący obiekt. 

Jeśli masz `ArrayList` wypełnioną 13 elementami i chcesz dodać element pod indeksem 4, istniejące elementy zostaną przesunięte o jeden indeks w górę, aby zrobić miejsce dla nowego elementu. Operacja ta jest wykonywana na tym samym obiekcie `ArrayList`, a nie na nowym obiekcie.

Oto przykładowy kod, który ilustruje to działanie:

```java
import java.util.ArrayList;

public class ArrayListExample {
    public static void main(String[] args) {
        ArrayList<String> lista = new ArrayList<>();
        lista.add("Element 1");
        lista.add("Element 2");
        lista.add("Element 3");
        lista.add("Element 4");
        lista.add("Element 5");
        lista.add("Element 6");
        lista.add("Element 7");
        lista.add("Element 8");
        lista.add("Element 9");
        lista.add("Element 10");
        lista.add("Element 11");
        lista.add("Element 12");
        lista.add("Element 13");

        System.out.println("Przed dodaniem: " + lista);

        lista.add(4, "Nowy element");

        System.out.println("Po dodaniu: " + lista);
    }
}
```

Wyjście z powyższego kodu będzie następujące:

```
Przed dodaniem: [Element 1, Element 2, Element 3, Element 4, Element 5, Element 6, Element 7, Element 8, Element 9, Element 10, Element 11, Element 12, Element 13]
Po dodaniu: [Element 1, Element 2, Element 3, Element 4, Nowy element, Element 5, Element 6, Element 7, Element 8, Element 9, Element 10, Element 11, Element 12, Element 13]
```

Widzisz, że po dodaniu elementu "Nowy element" pod indeksem 4, oryginalna lista została zmodyfikowana i zawiera ten nowy element.