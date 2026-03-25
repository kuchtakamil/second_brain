# CopyOnWriteArrayList w aplikacji wielowątkowej

**Data:** 2024-02-18

---

**User:**

Jak przykład użycia CopyOnWriteArrayList w aplikacji wielowątkowej

---

**Assistant:**

`CopyOnWriteArrayList` to klasa w Java, która implementuje interfejs `List` i zapewnia bezpieczne operacje na wielu wątkach poprzez kopiowanie listy podczas każdej modyfikacji. Jest to przydatne, gdy lista jest często odczytywana, a zmiany są stosunkowo rzadkie.

Poniżej znajdziesz prosty przykład użycia `CopyOnWriteArrayList` w aplikacji wielowątkowej:

```java
import java.util.Iterator;
import java.util.concurrent.CopyOnWriteArrayList;

public class WielowatkowaAplikacja {

    public static void main(String[] args) {
        // Tworzymy listę wątkową
        CopyOnWriteArrayList<String> lista = new CopyOnWriteArrayList<>();

        // Dodajemy dane do listy
        lista.add("Element 1");
        lista.add("Element 2");
        lista.add("Element 3");

        // Tworzymy i uruchamiamy wątki, które będą modyfikować listę
        Thread watekDodawania = new Thread(new DodawanieElementow(lista));
        Thread watekUsuwanie = new Thread(new UsuwanieElementow(lista));

        watekDodawania.start();
        watekUsuwanie.start();

        // Czekamy na zakończenie wątków
        try {
            watekDodawania.join();
            watekUsuwanie.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        // Wyświetlamy zawartość listy po zakończeniu wątków
        System.out.println("Zawartość listy po zakończeniu wątków:");
        for (String element : lista) {
            System.out.println(element);
        }
    }

    static class DodawanieElementow implements Runnable {
        private CopyOnWriteArrayList<String> lista;

        public DodawanieElementow(CopyOnWriteArrayList<String> lista) {
            this.lista = lista;
        }

        @Override
        public void run() {
            // Dodajemy nowy element do listy
            lista.add("Nowy element dodany przez wątek dodawania");
        }
    }

    static class UsuwanieElementow implements Runnable {
        private CopyOnWriteArrayList<String> lista;

        public UsuwanieElementow(CopyOnWriteArrayList<String> lista) {
            this.lista = lista;
        }

        @Override
        public void run() {
            // Usuwamy istniejący element z listy
            Iterator<String> iterator = lista.iterator();
            while (iterator.hasNext()) {
                String element = iterator.next();
                if (element.equals("Element 2")) {
                    iterator.remove();
                    System.out.println("Element 2 usunięty przez wątek usuwania");
                }
            }
        }
    }
}
```

W tym przykładzie tworzymy `CopyOnWriteArrayList` i dodajemy do niej kilka elementów. Następnie uruchamiamy dwa wątki (`watekDodawania` i `watekUsuwanie`), które modyfikują listę. Dzięki mechanizmowi kopiowania, operacje te są wykonywane bezpiecznie, bez konieczności stosowania blokad. Po zakończeniu wątków, możemy wyświetlić zawartość listy i zobaczyć, że wszystkie zmiany zostały uwzględnione.

---

**User:**

Because of the copying mechanism, the remove() operation on the returned Iterator is not permitted – resulting with UnsupportedOperationException:

---

**Assistant:**

You're correct, and I appreciate your observation. I apologize for the oversight in the example. Indeed, the `remove()` operation on the iterator obtained from `CopyOnWriteArrayList` is not supported, and attempting to use it will result in an `UnsupportedOperationException`. This is because the `CopyOnWriteArrayList` is designed to be immutable during iteration to ensure thread safety.

Let me provide a corrected version of the `UsuwanieElementow` class:

```java
static class UsuwanieElementow implements Runnable {
    private CopyOnWriteArrayList<String> lista;

    public UsuwanieElementow(CopyOnWriteArrayList<String> lista) {
        this.lista = lista;
    }

    @Override
    public void run() {
        // Usuwamy istniejący element z listy
        for (String element : lista) {
            if (element.equals("Element 2")) {
                // Removing elements directly from the list is supported
                lista.remove(element);
                System.out.println("Element 2 usunięty przez wątek usuwania");
            }
        }
    }
}
```

In this corrected version, we are using the `remove(Object o)` method directly on the `CopyOnWriteArrayList` instead of attempting to use the iterator's `remove()` method. This modification ensures compatibility with the design of `CopyOnWriteArrayList`, and it won't throw an `UnsupportedOperationException`. I appreciate your understanding, and thank you for bringing this to my attention.

---

**User:**

Przerób ten przykład aby używał executorów

---

**Assistant:**

Certainly! You can modify the example to use `ExecutorService` and `Future` to manage the execution of threads. Here's an updated version of the example using `ExecutorService`:

```java
import java.util.concurrent.*;

public class WielowatkowaAplikacja {

    public static void main(String[] args) {
        // Tworzymy listę wątkową
        CopyOnWriteArrayList<String> lista = new CopyOnWriteArrayList<>();

        // Dodajemy dane do listy
        lista.add("Element 1");
        lista.add("Element 2");
        lista.add("Element 3");

        // Tworzymy ExecutorService z dwoma wątkami
        ExecutorService executorService = Executors.newFixedThreadPool(2);

        // Uruchamiamy wątki, które będą modyfikować listę
        Future<?> futureDodawania = executorService.submit(new DodawanieElementow(lista));
        Future<?> futureUsuwanie = executorService.submit(new UsuwanieElementow(lista));

        // Oczekujemy na zakończenie wątków
        try {
            futureDodawania.get();
            futureUsuwanie.get();
        } catch (InterruptedException | ExecutionException e) {
            e.printStackTrace();
        }

        // Wyświetlamy zawartość listy po zakończeniu wątków
        System.out.println("Zawartość listy po zakończeniu wątków:");
        for (String element : lista) {
            System.out.println(element);
        }

        // Zamykamy ExecutorService
        executorService.shutdown();
    }

    static class DodawanieElementow implements Runnable {
        private CopyOnWriteArrayList<String> lista;

        public DodawanieElementow(CopyOnWriteArrayList<String> lista) {
            this.lista = lista;
        }

        @Override
        public void run() {
            // Dodajemy nowy element do listy
            lista.add("Nowy element dodany przez wątek dodawania");
        }
    }

    static class UsuwanieElementow implements Runnable {
        private CopyOnWriteArrayList<String> lista;

        public UsuwanieElementow(CopyOnWriteArrayList<String> lista) {
            this.lista = lista;
        }

        @Override
        public void run() {
            // Usuwamy istniejący element z listy
            for (String element : lista) {
                if (element.equals("Element 2")) {
                    // Removing elements directly from the list is supported
                    lista.remove(element);
                    System.out.println("Element 2 usunięty przez wątek usuwania");
                }
            }
        }
    }
}
```

In this version, I've replaced the manual thread creation and starting with an `ExecutorService`. The `submit` method is used to submit `Runnable` tasks, and `Future` objects are used to wait for the tasks to complete. The `ExecutorService` is then shut down to release its resources.