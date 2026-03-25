# Java Immutable List

**Data:** 2024-02-19

---

**User:**

java, podaj przykład użycia list typu immutable

---

**Assistant:**

W Javie, typy immutable są zazwyczaj reprezentowane przez klasy, których stan nie może być modyfikowany po utworzeniu obiektu. Jednym z przykładów jest klasa `java.util.List` z pakietu Java Collections Framework. Należy jednak zauważyć, że sama klasa `List` nie jest immutable, ale możemy użyć odpowiednich metod do stworzenia niemodyfikowalnej kopii listy.

Oto przykład użycia niemodyfikowalnej listy w Javie:

```java
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class ImmutableListExample {

    public static void main(String[] args) {
        // Tworzymy listę
        List<String> mutableList = new ArrayList<>();
        mutableList.add("Element 1");
        mutableList.add("Element 2");
        mutableList.add("Element 3");

        // Tworzymy niemodyfikowalną kopię listy
        List<String> immutableList = Collections.unmodifiableList(new ArrayList<>(mutableList));

        // Próba modyfikacji niemodyfikowalnej listy spowoduje wyjątek UnsupportedOperationException
        // immutableList.add("Nowy element"); // To spowoduje wyjątek

        // Wyświetlamy zawartość niemodyfikowalnej listy
        System.out.println("Immutable List:");
        for (String element : immutableList) {
            System.out.println(element);
        }
    }
}
```

W tym przykładzie używamy `Collections.unmodifiableList()` do utworzenia niemodyfikowalnej kopii listy. Próba modyfikacji tej niemodyfikowalnej listy za pomocą operacji takich jak `add()` spowoduje wyjątek `UnsupportedOperationException`.

---

**User:**

czym różni się synchronizedCollection od unmodifiableCollection

---

**Assistant:**

`Collections.synchronizedCollection` i `Collections.unmodifiableCollection` to dwie różne metody w klasie `Collections` z Java Collections Framework, które służą do manipulacji kolekcjami. Oto różnice między nimi:

1. **Synchronized Collection (`Collections.synchronizedCollection`):**
   - `Collections.synchronizedCollection` zwraca kolekcję, która jest synchronizowana (thread-safe).
   - Oznacza to, że operacje na kolekcji są automatycznie synchronizowane, co zapewnia bezpieczeństwo wielowątkowe.
   - Synchronizacja osiągana jest poprzez synchronizowanie dostępu do wszystkich metod kolekcji.
   - Jest to przydatne w sytuacjach, gdzie wiele wątków może jednocześnie modyfikować kolekcję.

```java
List<String> synchronizedList = Collections.synchronizedList(new ArrayList<>());
```

2. **Unmodifiable Collection (`Collections.unmodifiableCollection`):**
   - `Collections.unmodifiableCollection` zwraca kolekcję, która nie może być modyfikowana (immutable).
   - Oznacza to, że po utworzeniu takiej kolekcji nie można dodawać, usuwać ani modyfikować jej elementów.
   - Jest to przydatne w sytuacjach, gdzie chcemy zapewnić, że kolekcja pozostanie stała i niepodzielna.

```java
List<String> unmodifiableList = Collections.unmodifiableList(new ArrayList<>());
```

Podsumowując, główna różnica między nimi polega na tym, czy kolekcja jest synchronizowana (thread-safe) w przypadku `synchronizedCollection`, czy tez niemodyfikowalna (immutable) w przypadku `unmodifiableCollection`. Wybór między nimi zależy od konkretnych wymagań dotyczących wielowątkowości i niemodyfikowalności w danym przypadku użycia.