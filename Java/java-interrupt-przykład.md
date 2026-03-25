# Java interrupt() przykład

**Data:** 2023-09-25

---

**User:**

Java, przykład użycia interrupt()

---

**Assistant:**

Metoda `interrupt()` w języku Java służy do przerywania wątków. Głównym jej celem jest powiadomienie wątku, że powinien zakończyć swoje działanie. Niemniej jednak, `interrupt()` nie przerywa wątku natychmiastowo. To jest bardziej subtelny sposób kończenia wątku niż brutalne zabicie go. To oznacza, że wątek może zakończyć się w miarę możliwości w sposób kontrolowany.

Oto przykład użycia metody `interrupt()`:

```java
public class Main {
    public static void main(String[] args) {
        Thread myThread = new MyThread();
        myThread.start();

        // Czekamy kilka sekund
        try {
            Thread.sleep(2000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        // Przerywamy wątek
        myThread.interrupt();
    }
}

class MyThread extends Thread {
    @Override
    public void run() {
        while (!Thread.currentThread().isInterrupted()) {
            System.out.println("Wątek działa...");
            try {
                Thread.sleep(500);
            } catch (InterruptedException e) {
                // Przechwytujemy wyjątek InterruptedException, który zostanie zgłoszony,
                // jeśli wątek zostanie przerwany podczas snu.
                System.out.println("Wątek został przerwany podczas snu.");
                // Wątek nie zostanie zakończony automatycznie po przerwaniu, więc możemy
                // dokończyć czyszczenie lub inne operacje i zakończyć go ręcznie.
                return;
            }
        }
        System.out.println("Wątek został przerwany.");
    }
}
```

W tym przykładzie tworzymy własny wątek `MyThread`, który jest dziedziczony z klasy `Thread`. Wewnątrz metody `run()` wątek ciągle sprawdza, czy nie został przerwany za pomocą `Thread.currentThread().isInterrupted()`. Jeśli zostanie wywołana metoda `interrupt()`, wątek zostanie przerwany, a wyjątek `InterruptedException` zostanie zgłoszony, co umożliwia wątkowi zakończenie swojego działania w kontrolowany sposób.

Warto zauważyć, że przerwanie wątku nie gwarantuje, że zostanie on zakończony natychmiast. Wątek może zakończyć się, gdy jest gotowy, ale może również obsłużyć przerwanie w bardziej specyficzny sposób, w zależności od implementacji.

---

**User:**

czy użycie isInterrupted jest konieczne?

---

**Assistant:**

Użycie `isInterrupted()` w warunku pętli sprawdzającej przerwanie wątku nie jest konieczne, ale jest to dobra praktyka, która pozwala na bardziej kontrolowane i czytelne zarządzanie przerwaniami wątku. Możesz także użyć metody `interrupted()` zamiast `isInterrupted()`, która jest metodą statyczną.

Oto dwie główne metody, które można użyć do sprawdzania przerwania wątku:

1. `isInterrupted()`: Jest to metoda niestatyczna dostępna na obiekcie wątku. Sprawdza, czy wątek został przerwany. Możesz ją używać wewnątrz pętli lub w innym miejscu wątku, aby zdecydować, czy należy przerwać działanie.

```java
while (!Thread.currentThread().isInterrupted()) {
    // Działanie wątku
}
```

2. `Thread.interrupted()`: Jest to metoda statyczna, która sprawdza, czy wątek został przerwany i jednocześnie resetuje status przerwania. Działa na wątku, na którym jest wywoływana, i resetuje jego flagę przerwania.

```java
while (!Thread.interrupted()) {
    // Działanie wątku
}
```

Używanie tych metod daje kontrolę nad zachowaniem wątku w przypadku przerwania. Możesz zdecydować, jakie akcje należy podjąć po wykryciu przerwania, na przykład zakończyć wątek, zakończyć go po zakończeniu obecnej operacji lub zignorować przerwanie, jeśli to odpowiednie.

Nie jest to absolutnie konieczne, aby korzystać z tych metod, ale ułatwiają one bardziej kontrolowane i bezpieczne zarządzanie wątkami w przypadku przerwań.