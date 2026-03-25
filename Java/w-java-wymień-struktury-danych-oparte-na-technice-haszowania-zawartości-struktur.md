# W Java wymień struktury danych oparte na technice haszowania zawartości struktur

**Data:** 19 lip 2025, 16:12:54 CET

---

**User:**

W Java wymień struktury danych oparte na technice haszowania zawartości struktury.

---

**Gemini:**

W Javie, podstawowymi strukturami danych opartymi na technice haszowania są implementacje interfejsów `Map` i `Set` z pakietu `java.util`. Kluczowe klasy to:

---

### `java.util.HashMap`

`HashMap` jest implementacją interfejsu `Map`, która przechowuje dane w formie par klucz-wartość. Jest to najczęściej używana implementacja mapy oparta na haszowaniu.

- **Zasada działania:**
  - Kiedy para klucz-wartość jest dodawana do `HashMap`, obliczany jest kod skrótu (`hash code`) dla klucza za pomocą jego metody `hashCode()`.
  - Wynikowy hash jest następnie używany do określenia "kubka" (ang. *bucket*), czyli indeksu w wewnętrznej tablicy (`Node<K,V>[] table`), gdzie ma być przechowywany obiekt `Node` zawierający klucz i wartość.
  - W przypadku, gdy dwa różne klucze wygenerują ten sam indeks (kolizja), obiekty `Node` są przechowywane w tym samym kubku w postaci listy połączonej (linked list) lub, gdy liczba elementów w kubku przekroczy pewien próg (`TREEIFY_THRESHOLD`), w postaci zbalansowanego drzewa czerwono-czarnego (dla poprawy wydajności z $O(n)$ do $O(\log n)$ w najgorszym przypadku).
- **Kluczowe cechy:**
  - **Złożoność czasowa:** Średnia złożoność operacji `put`, `get` i `remove` wynosi $O(1)$, pod warunkiem, że funkcja haszująca jest dobrze zaimplementowana i rozprasza elementy równomiernie.
  - **Klucze i wartości:** Pozwala na przechowywanie jednego klucza `null` i wielu wartości `null`.
  - **Kolejność:** Nie gwarantuje zachowania kolejności wstawiania elementów.

```
import java.util.HashMap;
import java.util.Map;

public class HashMapExample {
    public static void main(String[] args) {
        Map<String, Integer> userAge = new HashMap<>();
        userAge.put("Alice", 30);
        userAge.put("Bob", 25);
        userAge.put(null, 35); // Allows one null key

        Integer ageOfAlice = userAge.get("Alice");
        System.out.println("Age of Alice: " + ageOfAlice);
    }
}
```

---

### `java.util.HashSet`

`HashSet` jest implementacją interfejsu `Set`, która służy do przechowywania unikalnych elementów.

- **Zasada działania:**
  - `HashSet` wewnętrznie wykorzystuje instancję `HashMap` do przechowywania swoich elementów.
  - Elementy dodawane do `HashSet` stają się kluczami w pod spodem leżącej `HashMap`, a dla wszystkich wartości używana jest stała, współdzielona wartość `PRESENT` (obiekt `Object`).
  - Mechanizm haszowania i obsługi kolizji jest identyczny jak w `HashMap`. Unikalność jest zapewniona przez naturę kluczy w mapie.
- **Kluczowe cechy:**
  - **Złożoność czasowa:** Średnia złożoność operacji `add`, `remove` i `contains` wynosi $O(1)$.
  - **Wartości:** Pozwala na przechowywanie jednego elementu `null`.
  - **Kolejność:** Nie gwarantuje zachowania kolejności wstawiania elementów.

```
import java.util.HashSet;
import java.util.Set;

public class HashSetExample {
    public static void main(String[] args) {
        Set<String> uniqueNames = new HashSet<>();
        uniqueNames.add("Charlie");
        uniqueNames.add("David");
        boolean isAdded = uniqueNames.add("Charlie"); // Returns false, as "Charlie" already exists

        System.out.println("Set contains 'David': " + uniqueNames.contains("David"));
        System.out.println("Was 'Charlie' added again? " + isAdded);
    }
}
```

---

### `java.util.LinkedHashMap`

`LinkedHashMap` jest podklasą `HashMap`, która dodatkowo zachowuje kolejność wstawiania elementów.

- **Zasada działania:**
  - Działa na tej samej zasadzie co `HashMap` (tablica haszująca i obsługa kolizji), ale utrzymuje dodatkowo dwukierunkową listę połączoną, która przechodzi przez wszystkie jej wpisy.
  - Ta lista definiuje porządek iteracji, który jest domyślnie kolejnością wstawiania kluczy do mapy (ang. *insertion-order*).
- **Kluczowe cechy:**
  - **Złożoność czasowa:** Złożoność operacji jest taka sama jak w `HashMap`, $O(1)$ dla `put`, `get`, `remove`, ale z nieco większym narzutem stałym z powodu zarządzania listą połączoną.
  - **Kolejność:** Iteracja po elementach odbywa się w kolejności ich wstawienia.
  - **Tryb dostępu:** Może być skonfigurowana do pracy w trybie kolejności dostępu (ang. *access-order*), gdzie element ostatnio użyty (przez `get` lub `put`) jest przesuwany na koniec listy. Jest to przydatne do implementacji pamięci podręcznej (cache) typu LRU (Least Recently Used).

```
import java.util.LinkedHashMap;
import java.util.Map;

public class LinkedHashMapExample {
    public static void main(String[] args) {
        Map<Integer, String> insertionOrderMap = new LinkedHashMap<>();
        insertionOrderMap.put(3, "Three");
        insertionOrderMap.put(1, "One");
        insertionOrderMap.put(2, "Two");

        // Iteration will be in the order of insertion: 3, 1, 2
        insertionOrderMap.forEach((key, value) -> System.out.println(key + ": " + value));
    }
}
```

---

### `java.util.LinkedHashSet`

`LinkedHashSet` jest podklasą `HashSet`, która zachowuje kolejność wstawiania unikalnych elementów.

- **Zasada działania:**
  - Podobnie jak `HashSet` jest oparty na `HashMap`, tak `LinkedHashSet` jest oparty na `LinkedHashMap`.
  - Zachowuje unikalność elementów, a jednocześnie pamięta kolejność ich dodawania dzięki wewnętrznej strukturze `LinkedHashMap`.
- **Kluczowe cechy:**
  - **Złożoność czasowa:** Identyczna jak w `HashSet` ($O(1)$ dla podstawowych operacji), z minimalnie większym narzutem.
  - **Kolejność:** Iteracja odbywa się w kolejności wstawiania elementów.

```
import java.util.LinkedHashSet;
import java.util.Set;

public class LinkedHashSetExample {
    public static void main(String[] args) {
        Set<String> orderedUniqueNames = new LinkedHashSet<>();
        orderedUniqueNames.add("Zebra");
        orderedUniqueNames.add("Apple");
        orderedUniqueNames.add("Monkey");

        // Iteration will be in the order of insertion: Zebra, Apple, Monkey
        orderedUniqueNames.forEach(System.out::println);
    }
}
```

---

### `java.util.concurrent.ConcurrentHashMap`

Jest to implementacja interfejsu `ConcurrentMap`, zaprojektowana do użytku w środowiskach wielowątkowych.

- **Zasada działania:**
  - Używa zaawansowanych technik haszowania i blokowania, aby zapewnić bezpieczeństwo wątkowe przy minimalnym wpływie na wydajność.
  - Zamiast blokować całą strukturę na czas modyfikacji, `ConcurrentHashMap` dzieli wewnętrzną tablicę na segmenty (lub w nowszych wersjach Javy używa blokad na poziomie pojedynczych kubków). To pozwala wielu wątkom na jednoczesny dostęp i modyfikację różnych części mapy.
  - Operacje odczytu (`get`) są zazwyczaj nieblokujące i mogą odbywać się równolegle z operacjami zapisu.
- **Kluczowe cechy:**
  - **Bezpieczeństwo wątkowe:** Zapewnia bezpieczny dostęp z wielu wątków bez potrzeby zewnętrznej synchronizacji.
  - **Wydajność:** Oferuje znacznie lepszą skalowalność niż `Collections.synchronizedMap(new HashMap<>())` w aplikacjach o wysokiej współbieżności.
  - **Klucze i wartości:** Nie pozwala na przechowywanie kluczy ani wartości `null`.

```
import java.util.concurrent.ConcurrentHashMap;
import java.util.Map;

public class ConcurrentHashMapExample {
    public static void main(String[] args) {
        Map<String, Integer> concurrentMap = new ConcurrentHashMap<>();

        // Multiple threads can safely perform operations on this map
        Runnable task = () -> {
            for (int i = 0; i < 1000; i++) {
                concurrentMap.put(Thread.currentThread().getName() + i, i);
            }
        };

        Thread t1 = new Thread(task);
        Thread t2 = new Thread(task);
        t1.start();
        t2.start();

        // Wait for threads to finish (simplified)
        try {
            t1.join();
            t2.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        
        System.out.println("Map size: " + concurrentMap.size());
    }
}
```