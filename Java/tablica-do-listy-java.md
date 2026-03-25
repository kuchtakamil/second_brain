# Tablica do listy Java.

**Data:** 2023-08-05

---

**User:**

Java, jak z takiej tablicy
Integer[] sourceArray = { 0, 1, 2, 3, 4, 5 };
zrobić listę?

---

**Assistant:**

Aby przekształcić tablicę `Integer[]` w listę w języku Java, możesz skorzystać z metody `Arrays.asList()` z pakietu `java.util`. Oto jak to zrobić:

```java
import java.util.Arrays;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        Integer[] sourceArray = { 0, 1, 2, 3, 4, 5 };
        
        // Konwersja tablicy na listę
        List<Integer> listFromArray = Arrays.asList(sourceArray);
        
        // Wyświetlenie listy
        System.out.println(listFromArray);
    }
}
```

Metoda `Arrays.asList()` zamienia przekazaną tablicę na listę, ale zwraca specjalny rodzaj listy, który jest zagnieżdżoną klasą wewnętrzną. Dlatego jeśli zależy ci na zmiennej typu `List`, nie musisz niczego zmieniać. Jednak jeśli musisz wykonywać operacje modyfikujące listę, możesz utworzyć nową listę typu ArrayList:

```java
import java.util.Arrays;
import java.util.List;
import java.util.ArrayList;

public class Main {
    public static void main(String[] args) {
        Integer[] sourceArray = { 0, 1, 2, 3, 4, 5 };
        
        // Konwersja tablicy na listę typu ArrayList
        List<Integer> listFromArray = new ArrayList<>(Arrays.asList(sourceArray));
        
        // Wyświetlenie listy
        System.out.println(listFromArray);
    }
}
```

W tym przypadku `Arrays.asList()` służy jako tymczasowa lista do zainicjowania nowej listy typu `ArrayList`, która pozwala na zmiany w liście.

---

**User:**

a z takiej 
int[] sourceArray = { 0, 1, 2, 3, 4, 5 };

---

**Assistant:**

Aby przekształcić tablicę `int[]` w listę w języku Java, możesz użyć pętli i ręcznie dodać elementy do listy. Możesz też skorzystać z klasy `Arrays` z pakietu `java.util`, aby przekształcić tablicę w listę obiektów typu `Integer`, a następnie utworzyć listę typu `List<Integer>`.

Metoda 1: Za pomocą pętli

```java
import java.util.ArrayList;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        int[] sourceArray = { 0, 1, 2, 3, 4, 5 };

        // Konwersja tablicy na listę typu ArrayList
        List<Integer> listFromArray = new ArrayList<>();
        for (int num : sourceArray) {
            listFromArray.add(num);
        }

        // Wyświetlenie listy
        System.out.println(listFromArray);
    }
}
```

Metoda 2: Używając klasy `Arrays`

```java
import java.util.Arrays;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        int[] sourceArray = { 0, 1, 2, 3, 4, 5 };

        // Konwersja tablicy na listę typu List<Integer>
        Integer[] boxedArray = Arrays.stream(sourceArray).boxed().toArray(Integer[]::new);
        List<Integer> listFromArray = Arrays.asList(boxedArray);

        // Wyświetlenie listy
        System.out.println(listFromArray);
    }
}
```

W powyższym kodzie `Arrays.stream(sourceArray)` zamienia tablicę `int[]` na strumień liczb całkowitych, a następnie `boxed()` przekształca każdą liczbę całkowitą w obiekt typu `Integer`. Na końcu używamy `toArray(Integer[]::new)` do przekształcenia strumienia w tablicę obiektów `Integer[]`. Następnie używamy `Arrays.asList()` do przekształcenia tej tablicy w listę typu `List<Integer>`.