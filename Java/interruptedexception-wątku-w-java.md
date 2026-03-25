# InterruptedException wątku w Java

**Data:** 2024-02-18

---

**User:**

Java, jak rzucenie InterruptedException sprawia, że wątek ma się skończyć?

---

**Assistant:**

W Javie rzucenie wyjątku `InterruptedException` nie powoduje automatycznego zakończenia wątku. Zamiast tego, rzucenie tego wyjątku sygnalizuje wątkowi, że został przerwany, i to jest odpowiedzialność programisty obsłużyć tę sytuację.

Standardowy sposób obsługi `InterruptedException` to ustawienie flagi przerwania wątku za pomocą metody `interrupt()`. Następnie, wątek może regularnie sprawdzać tę flagę, używając metody `isInterrupted()`, i zdecydować, kiedy zakończyć swoje działanie. Na przykład:

```java
public class MyRunnable implements Runnable {
    public void run() {
        try {
            // kod wątku
            while (!Thread.interrupted()) {
                // działanie wątku
            }
        } catch (InterruptedException e) {
            // Obsługa przerwania
            System.out.println("Wątek został przerwany");
        }
    }
}
```

W powyższym kodzie, wątek będzie kontynuował swoje działanie do momentu, gdy flaga przerwania zostanie ustawiona poprzez wywołanie `interrupt()`. Wówczas `Thread.interrupted()` zwróci true, a wątek może zakończyć swoje wykonanie.

Ważne jest, aby zauważyć, że nie wszystkie metody w Javie rzucają `InterruptedException`, a wiele z nich, które tak robią, jest związanych z operacjami wejścia/wyjścia (I/O) lub z operacjami, które czekają na zasoby. Ręczne zarządzanie przerwaniami wątku jest ważne w przypadku obsługi takich sytuacji.