# Zatrzymanie wątku w Javie

**Data:** 2023-07-17

---

**User:**

java, w jaki sposób zatrzymać wątek?

---

**Assistant:**

W Javie istnieje kilka sposobów zatrzymania wątku. Oto trzy najczęściej stosowane metody:

1. Metoda `Thread.stop()` (przestarzała): Metoda ta była używana w starszych wersjach Javy, jednak została oznaczona jako przestarzała i nie powinna być używana. Wywołanie tej metody powoduje rzucenie wyjątku `ThreadDeath`, który można przechwycić, ale nie jest zalecane korzystanie z tej metody ze względu na potencjalne problemy z bezpieczeństwem i nieprzewidywalne skutki.

2. Metoda `Thread.interrupt()`: Metoda `interrupt()` służy do wysłania sygnału przerwania wątkowi. Wątek może sprawdzać, czy został przerwany poprzez wywołanie metody `Thread.isInterrupted()` lub sprawdzenie flagi `Thread.interrupted()`. Można to wykorzystać do zakończenia działania wątku poprzez wykonanie odpowiednich czynności kończących (np. zamknięcie zasobów, wyczyszczenie stanu itp.). Jednak samo wywołanie `interrupt()` nie kończy natychmiastowo działania wątku, tylko ustawia flagę przerwania, którą wątek musi samodzielnie obsłużyć.

3. Wykorzystanie zmiennej flagowej: Można zdefiniować zmienną typu `boolean`, która będzie pełnić rolę flagi zatrzymania. Wątek regularnie sprawdza wartość tej zmiennej i jeśli zostanie ustawiona na `true`, to wychodzi z pętli głównej lub kończy swoje działanie. Aby zatrzymać wątek, wystarczy zmienić wartość tej zmiennej na `true`.

Oto przykład użycia flagi zatrzymania wątku:

```java
public class MyRunnable implements Runnable {
    private volatile boolean isRunning = true;

    public void stopThread() {
        isRunning = false;
    }

    public void run() {
        while (isRunning) {
            // Logika wątku

            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                // Przechwytywanie wyjątku InterruptedException
            }
        }
    }
}
```

W powyższym przykładzie wątek będzie działał, dopóki flaga `isRunning` będzie miała wartość `true`. Aby zatrzymać wątek, wystarczy wywołać metodę `stopThread()` z innego wątku.

Należy pamiętać, że zawsze warto zadbać o prawidłowe zakończenie działania wątku, np. poprzez zamknięcie otwartych zasobów czy odpowiednie wyczyszczenie stanu.