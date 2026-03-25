# Zmienna lokalna w lambdach

**Data:** 2024-10-30

---

**User:**

Dlaczego w Java zmienne lokalne używane w wyrażeniach lambda muszą być ostateczne lub faktycznie ostateczne? Podaj przykład w którym gdy zmienna nie byłaby final, stałoby się coś złego.

---

**Assistant:**

W Javie zmienne lokalne używane w wyrażeniach lambda muszą być "ostateczne" (ang. *final*) lub *faktycznie ostateczne* (ang. *effectively final*), czyli ich wartość nie może się zmieniać po przypisaniu. Wymóg ten ma na celu zagwarantowanie, że lambda zachowa się w sposób przewidywalny, a także zapewnia bezpieczeństwo współbieżności.

Wyrażenia lambda są często używane w kontekście wielowątkowym, gdzie mogłoby dojść do nieoczekiwanych rezultatów, jeśli zmienna lokalna mogłaby się zmieniać. Gdyby lambdy mogły odczytywać i modyfikować zmienne, wprowadzałoby to ryzyko wyścigu danych (*race condition*) – zmiana wartości w jednym wątku mogłaby nie być widoczna dla innych wątków lub mogłaby zostać nadpisana.

### Przykład wyścigu danych

Załóżmy, że wątek główny tworzy lambda wyrażenie, które próbuje modyfikować zmienną lokalną:

```java
public class Example {
    public static void main(String[] args) {
        int counter = 0;

        Runnable task = () -> {
            for (int i = 0; i < 1000; i++) {
                counter++; // Kompilator nie pozwoli na to, bo counter nie jest "faktycznie ostateczny"
            }
        };

        Thread t1 = new Thread(task);
        Thread t2 = new Thread(task);

        t1.start();
        t2.start();
    }
}
```

W tym przypadku kompilator zgłosi błąd, ponieważ zmienna `counter` nie jest ostateczna. Pozwolenie na taką operację mogłoby prowadzić do wyścigu danych, ponieważ oba wątki mogą jednocześnie próbować zwiększyć wartość `counter`. W rezultacie ostateczna wartość mogłaby być niższa niż 2000 (co może zaskoczyć programistę), ponieważ operacje odczytu i zapisu mogą się przeplatać w nieprzewidywalny sposób.

### Rozwiązanie z użyciem zmiennej ostatecznej

Aby uniknąć wyścigu danych, można wykorzystać zmienną, która jest faktycznie ostateczna lub odpowiedni mechanizm synchronizacji:

```java
import java.util.concurrent.atomic.AtomicInteger;

public class Example {
    public static void main(String[] args) {
        AtomicInteger counter = new AtomicInteger(0);

        Runnable task = () -> {
            for (int i = 0; i < 1000; i++) {
                counter.incrementAndGet();
            }
        };

        Thread t1 = new Thread(task);
        Thread t2 = new Thread(task);

        t1.start();
        t2.start();
    }
}
```

W tym kodzie `counter` jest zmienną ostateczną, ale jest obiektem `AtomicInteger`, co pozwala na bezpieczną modyfikację wartości w sposób atomowy bez ryzyka wyścigu danych.

---

**User:**

A czy niewłaściwym zachowaniem będącym częściowo ominięciem problemu jest sytuacja w której mam kolekcję np. listę do której w wyrażeniu lambda dodajemy oraz z której usuwamy elementy?

---

**Assistant:**

Tak, używanie kolekcji (np. listy) wewnątrz wyrażenia lambda bez odpowiednich zabezpieczeń również może prowadzić do niewłaściwego zachowania, szczególnie w środowisku wielowątkowym. Mimo że kompilator nie wymaga, aby kolekcje używane w lambdach były ostateczne, wciąż istnieje ryzyko wyścigu danych i niespójności w przypadku modyfikacji kolekcji przez wiele wątków.

### Przykład problematycznego zachowania

Załóżmy, że mamy `ArrayList`, do której dodajemy i z której usuwamy elementy w dwóch różnych wątkach. Brak synchronizacji może prowadzić do niespójnych wyników, ponieważ `ArrayList` nie jest bezpieczny dla wątków równoległych:

```java
import java.util.ArrayList;
import java.util.List;

public class Example {
    public static void main(String[] args) {
        List<Integer> list = new ArrayList<>();

        Runnable addTask = () -> {
            for (int i = 0; i < 1000; i++) {
                list.add(i);
            }
        };

        Runnable removeTask = () -> {
            for (int i = 0; i < 1000; i++) {
                if (!list.isEmpty()) {
                    list.remove(0);
                }
            }
        };

        Thread t1 = new Thread(addTask);
        Thread t2 = new Thread(removeTask);

        t1.start();
        t2.start();
    }
}
```

W powyższym przykładzie wątki `t1` i `t2` równocześnie dodają i usuwają elementy z `list`, co prowadzi do niespójności, a w niektórych przypadkach może nawet skutkować `IndexOutOfBoundsException`. Dzieje się tak, ponieważ wątki nie synchronizują dostępu do `listy`, co powoduje problemy, gdy np. jeden wątek sprawdza rozmiar listy, a drugi w tym samym czasie ją modyfikuje.

### Rozwiązanie problemu

Aby zapobiec takim problemom, można użyć wątkowo bezpiecznej kolekcji, np. `CopyOnWriteArrayList`, `Collections.synchronizedList(new ArrayList<>())`, lub synchronizować dostęp do `ArrayList`:

```java
import java.util.Collections;
import java.util.List;
import java.util.ArrayList;

public class Example {
    public static void main(String[] args) {
        List<Integer> list = Collections.synchronizedList(new ArrayList<>());

        Runnable addTask = () -> {
            for (int i = 0; i < 1000; i++) {
                list.add(i);
            }
        };

        Runnable removeTask = () -> {
            for (int i = 0; i < 1000; i++) {
                synchronized (list) {
                    if (!list.isEmpty()) {
                        list.remove(0);
                    }
                }
            }
        };

        Thread t1 = new Thread(addTask);
        Thread t2 = new Thread(removeTask);

        t1.start();
        t2.start();
    }
}
```

Użycie `Collections.synchronizedList` lub ręczne synchronizowanie bloków kodu chroni `list` przed równoczesnym dostępem z wielu wątków, co zapobiega wyścigom danych i potencjalnym wyjątkom.