# Future w Javie: Uruchamianie Zadań

**Data:** 2023-09-25

---

**User:**

Java, gdy utworzę obiekt typu Future to czy zadanie w nim zawarte odpala się natychmiast czy czeka na wywołanie get?

---

**Assistant:**

W języku Java, gdy utworzysz obiekt typu `Future`, zadanie w nim zawarte nie odpala się natychmiast. `Future` jest interfejsem do reprezentowania wyniku obliczeń asynchronicznych, które mogą być jeszcze w trakcie wykonywania lub zostały już ukończone.

Aby uruchomić zadanie asynchronicznie i uzyskać wynik, możesz użyć mechanizmu `ExecutorService`, który jest często wykorzystywany wraz z `Future`. `ExecutorService` zarządza wątkami i może uruchamiać zadania asynchronicznie. Po utworzeniu zadania i przekazaniu go do `ExecutorService`, możesz otrzymać `Future`, który będzie reprezentować wynik tego zadania.

Ostatecznie zadanie zostanie uruchomione, gdy zostanie przekazane do `ExecutorService`, ale nie musisz czekać na wynik, dopóki nie wywołasz metody `get()` na `Future`. Wywołanie `get()` zablokuje wątek, który to robi, do momentu uzyskania wyniku zadania lub zgłoszenia wyjątku, jeśli wystąpił jakiś błąd.

Jeśli chcesz uruchomić zadanie natychmiast i oczekujesz wyniku, możesz użyć metody `submit()` na `ExecutorService`, która zwraca `Future`, który można od razu użyć do oczekiwania na wynik.

Ogólnie rzecz biorąc, `Future` służy do zarządzania wynikami zadań asynchronicznych i pozwala na asynchroniczne wykonywanie zadań w tle, co nie blokuje głównego wątku programu.

---

**User:**

przykłąd z execute i submit

---

**Assistant:**

Oto przykład użycia `ExecutorService` z metodami `execute()` i `submit()` w języku Java:

```java
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

public class ExecutorExample {
    public static void main(String[] args) {
        // Tworzenie ExecutorService z pojedynczym wątkiem
        ExecutorService executorService = Executors.newSingleThreadExecutor();

        // Użycie metody execute() do uruchomienia zadania asynchronicznego
        executorService.execute(() -> {
            try {
                Thread.sleep(2000); // Symulowanie długotrwałego zadania
                System.out.println("Zadanie wykonane.");
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        });

        // Użycie metody submit() do uruchomienia zadania asynchronicznego i uzyskania Future
        Future<String> futureResult = executorService.submit(() -> {
            try {
                Thread.sleep(1000); // Symulowanie długotrwałego zadania
                return "Wynik zadania";
            } catch (InterruptedException e) {
                e.printStackTrace();
                return "Błąd";
            }
        });

        // W tym miejscu możemy kontynuować pracę w głównym wątku

        try {
            // Wywołanie get() na Future blokuje wątek i czeka na wynik
            String result = futureResult.get();
            System.out.println("Wynik: " + result);
        } catch (Exception e) {
            e.printStackTrace();
        }

        // Zamykanie ExecutorService po użyciu
        executorService.shutdown();
    }
}
```

W tym przykładzie mamy `ExecutorService` z pojedynczym wątkiem, który obsługuje dwie operacje asynchroniczne. Pierwsza używa metody `execute()` do uruchomienia zadania bez możliwości oczekiwania na wynik. Druga używa metody `submit()` do uruchomienia zadania i uzyskania `Future`, który pozwala nam później pobrać wynik zadania.

---

**User:**

czy muszę na końcu użyć awaitTermiantion?

---

**Assistant:**

Nie, nie jest konieczne używanie metody `awaitTermination()` na końcu, ale jest to dobra praktyka, jeśli chcesz upewnić się, że wszystkie zadania zostały zakończone przed zakończeniem działania programu.

Metoda `awaitTermination()` jest używana do oczekiwania na zakończenie wszystkich zadań w `ExecutorService` przed jego zamknięciem. Może być przydatna, szczególnie gdy masz zadania, które trwają długo i nie chcesz, aby program zakończył się zanim te zadania zostaną ukończone.

Oto jak użyć `awaitTermination()` w kontekście poprzedniego przykładu:

```java
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

public class ExecutorExample {
    public static void main(String[] args) {
        // Tworzenie ExecutorService z pojedynczym wątkiem
        ExecutorService executorService = Executors.newSingleThreadExecutor();

        // Użycie metody execute() do uruchomienia zadania asynchronicznego
        executorService.execute(() -> {
            try {
                Thread.sleep(2000); // Symulowanie długotrwałego zadania
                System.out.println("Zadanie 1 wykonane.");
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        });

        // Użycie metody submit() do uruchomienia zadania asynchronicznego i uzyskania Future
        Future<String> futureResult = executorService.submit(() -> {
            try {
                Thread.sleep(1000); // Symulowanie długotrwałego zadania
                return "Wynik zadania 2";
            } catch (InterruptedException e) {
                e.printStackTrace();
                return "Błąd";
            }
        });

        // Zamykanie ExecutorService po użyciu
        executorService.shutdown();

        try {
            // Oczekiwanie na zakończenie wszystkich zadań
            executorService.awaitTermination(Long.MAX_VALUE, java.util.concurrent.TimeUnit.NANOSECONDS);
            
            // Wywołanie get() na Future blokuje wątek i czeka na wynik
            String result = futureResult.get();
            System.out.println("Wynik zadania 2: " + result);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

W tym przykładzie, po zamknięciu `ExecutorService`, używamy `awaitTermination()` do oczekiwania na zakończenie wszystkich zadań przed kontynuacją programu. Jest to szczególnie przydatne w przypadku zadań, które trwają dłużej niż główny wątek programu, aby upewnić się, że program nie zakończy się przed zakończeniem tych zadań.