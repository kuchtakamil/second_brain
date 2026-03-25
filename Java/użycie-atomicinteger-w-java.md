# Użycie AtomicInteger w Java

**Data:** 2023-09-25

---

**User:**

Przykład użycia AtomicInteger

---

**Assistant:**

`AtomicInteger` jest często używany w wielowątkowych aplikacjach do kontrolowania dostępu do współdzielonych zasobów, takich jak liczniki, w sposób bezpieczny pod względem wątkowym. Oto przykład użycia `AtomicInteger`:

```java
import java.util.concurrent.atomic.AtomicInteger;

public class AtomicIntegerExample {
    public static void main(String[] args) {
        // Tworzenie obiektu AtomicInteger z początkową wartością 0
        AtomicInteger atomicInteger = new AtomicInteger(0);

        // Inkrementacja wartości w wielu wątkach
        Runnable incrementTask = () -> {
            for (int i = 0; i < 1000; i++) {
                atomicInteger.incrementAndGet();
            }
        };

        // Tworzenie i uruchamianie wielu wątków
        Thread thread1 = new Thread(incrementTask);
        Thread thread2 = new Thread(incrementTask);
        Thread thread3 = new Thread(incrementTask);

        thread1.start();
        thread2.start();
        thread3.start();

        // Oczekiwanie na zakończenie wszystkich wątków
        try {
            thread1.join();
            thread2.join();
            thread3.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        // Wyświetlenie wyniku
        System.out.println("Wartość końcowa: " + atomicInteger.get());
    }
}
```

W tym przykładzie tworzymy `AtomicInteger` o początkowej wartości 0. Następnie uruchamiamy trzy wątki, które inkrementują tę wartość łącznie 3000 razy (każdy wątek 1000 razy) przy użyciu metody `incrementAndGet()`. Dzięki temu, że `AtomicInteger` gwarantuje atomowość operacji inkrementacji, nie ma potrzeby synchronizacji i unikamy problemów związanych z równoczesnym dostępem wielu wątków do tej samej zmiennej.

Na końcu programu wyświetlamy wartość końcową `AtomicInteger`, która powinna wynosić 3000.