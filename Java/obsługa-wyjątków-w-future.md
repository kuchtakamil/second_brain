# Obsługa wyjątków w Future

**Data:** 2024-10-06

---

**User:**

W Java jak wygląda obsługa wyjątków gdy używa się Future?

---

**Assistant:**

W Javie, gdy korzystasz z klasy `Future`, obsługa wyjątków jest specyficzna, ponieważ metody zwracające `Future` mogą działać asynchronicznie. Najważniejszą metodą, którą wykorzystujesz do pobrania wyniku z obiektu `Future`, jest metoda `get()`. Może ona zgłaszać wyjątki związane z problemami, które mogą wystąpić podczas wykonywania zadania w tle.

Oto podstawowe wyjątki, jakie mogą być zgłaszane w kontekście używania `Future`:

1. **`InterruptedException`** – zgłaszany, gdy wątek oczekujący na wynik (wywołujący metodę `get()`) zostaje przerwany.
2. **`ExecutionException`** – zgłaszany, gdy podczas wykonywania zadania w tle pojawił się wyjątek. W tym przypadku wyjątek, który spowodował problem, jest zawarty wewnątrz `ExecutionException` i można go uzyskać za pomocą metody `getCause()`.
3. **`TimeoutException`** – zgłaszany, gdy metoda `get(long timeout, TimeUnit unit)` nie otrzyma wyniku w określonym czasie.

### Przykład obsługi wyjątków z `Future`:

```java
import java.util.concurrent.*;

public class FutureExample {
    public static void main(String[] args) {
        ExecutorService executor = Executors.newSingleThreadExecutor();
        
        // Zadanie asynchroniczne, które zwraca wynik w przyszłości
        Future<Integer> future = executor.submit(() -> {
            // Symulacja długiego zadania
            Thread.sleep(2000);
            return 42;
        });

        try {
            // Próba pobrania wyniku z `Future`
            Integer result = future.get(); // lub future.get(5, TimeUnit.SECONDS) dla timeoutu
            System.out.println("Wynik: " + result);
        } catch (InterruptedException e) {
            System.out.println("Zadanie zostało przerwane.");
            Thread.currentThread().interrupt(); // Przywrócenie statusu przerwania wątku
        } catch (ExecutionException e) {
            System.out.println("Wystąpił błąd podczas wykonywania zadania: " + e.getCause());
        } finally {
            executor.shutdown();
        }
    }
}
```

### Opis kodu:
1. **`ExecutorService`** – Tworzy wątek do wykonania zadania w tle.
2. **`Future.submit()`** – Zleca wykonanie zadania w tle i zwraca obiekt `Future`, który reprezentuje wynik tego zadania.
3. **`future.get()`** – Pobiera wynik zadania. Jeśli zadanie napotka wyjątek podczas wykonywania, zostanie zgłoszony `ExecutionException`.
4. **Obsługa wyjątków** – Przechwytujemy `InterruptedException`, jeśli wątek zostanie przerwany, oraz `ExecutionException`, gdy zadanie zakończy się wyjątkiem.

Jeśli zależy ci na bardziej zaawansowanej obsłudze wyjątków lub lepszej integracji z programowaniem asynchronicznym, warto rozważyć użycie bardziej nowoczesnych konstrukcji, takich jak `CompletableFuture`, które oferują bardziej elastyczne API.

---

**User:**

Jak według najlepszych praktyk poprawić ten kod i obsłużyć błędy
    public Future<Integer> calculateWithRunnable(Integer input) {
        return executor.submit(() -> {
            Thread.sleep(1000);
            System.out.println(input * input);
        });
    }

---

**Assistant:**

W twoim kodzie istnieje kilka rzeczy, które można poprawić, aby lepiej obsługiwać wyjątki oraz lepiej dopasować go do koncepcji, jakie `Future` i `Callable` oferują w Javie.

Oto kluczowe problemy:

1. **Nieprawidłowe użycie `Runnable` zamiast `Callable`:** W twoim kodzie używasz `Runnable` w konstrukcji lambda, ale chcesz zwrócić wartość z tej operacji. `Runnable` nie zwraca wartości, dlatego lepiej jest użyć `Callable`, który umożliwia zwracanie wartości.

2. **Brak obsługi wyjątków:** Jeśli w środku lambdy zostanie zgłoszony wyjątek (np. `InterruptedException`), to nie będzie to poprawnie obsłużone. Należy zadbać o odpowiednią obsługę wyjątków w bloku `try-catch`.

3. **`Future` zwraca `null`:** W twojej wersji metoda zwróci obiekt `Future` typu `Integer`, ale bez wartości (będzie to `null`), ponieważ `Runnable` nie zwraca wartości. Oczekiwany typ metody (`Future<Integer>`) sugeruje, że wartością powinien być wynik obliczeń.

### Poprawiony kod z najlepszymi praktykami:

```java
import java.util.concurrent.*;

public class FutureExample {
    private final ExecutorService executor = Executors.newSingleThreadExecutor();

    public Future<Integer> calculateWithCallable(Integer input) {
        return executor.submit(() -> {
            try {
                // Symulacja opóźnienia
                Thread.sleep(1000);
                
                // Obliczenia
                int result = input * input;
                System.out.println("Wynik: " + result);
                
                // Zwracamy wynik
                return result;
            } catch (InterruptedException e) {
                // Obsługa przerwanego wątku
                System.err.println("Wątek został przerwany: " + e.getMessage());
                Thread.currentThread().interrupt(); // Przywrócenie statusu przerwania
                return null; // Opcjonalnie można tu rzucić własny wyjątek lub zwrócić wartość domyślną
            } catch (Exception e) {
                // Obsługa innych wyjątków
                System.err.println("Wystąpił błąd: " + e.getMessage());
                return null; // Możesz rzucić wyjątek lub zwrócić specjalny kod błędu
            }
        });
    }

    public void shutdownExecutor() {
        executor.shutdown();
    }

    public static void main(String[] args) throws ExecutionException, InterruptedException {
        FutureExample example = new FutureExample();
        
        Future<Integer> future = example.calculateWithCallable(5);

        try {
            // Pobieramy wynik
            Integer result = future.get();
            System.out.println("Otrzymany wynik: " + result);
        } catch (InterruptedException | ExecutionException e) {
            System.err.println("Błąd podczas pobierania wyniku: " + e.getMessage());
        } finally {
            // Zamykamy executor po zakończeniu
            example.shutdownExecutor();
        }
    }
}
```

### Kluczowe zmiany:

1. **Użycie `Callable<Integer>` zamiast `Runnable`:** Zmieniliśmy lambdę, aby zwracała wartość (`Callable` pozwala na zwracanie wartości).
   
2. **Obsługa wyjątków w lambdzie:** Dodałem blok `try-catch` wewnątrz lambdy, aby obsługiwać ewentualne wyjątki, takie jak `InterruptedException`. Ważne jest, aby ustawić flagę przerwania (`Thread.currentThread().interrupt()`), gdy wątek zostanie przerwany.

3. **Zwracanie wyniku:** Teraz metoda `calculateWithCallable` faktycznie zwraca wynik obliczeń (kwadrat liczby), a nie `null`.

4. **Zamykanie `ExecutorService`:** Dodaliśmy metodę `shutdownExecutor()`, aby po zakończeniu wykonywania zamknąć `ExecutorService`. To jest dobra praktyka, ponieważ brak zamknięcia `ExecutorService` może prowadzić do wycieków wątków.

5. **Obsługa wyjątków z `Future`:** W `main()` obsługujemy wyjątki `InterruptedException` i `ExecutionException` w przypadku problemów z pobraniem wyniku z obiektu `Future`.

### Podsumowanie:
- Zastosowanie `Callable<Integer>` pozwala na zwrócenie wyniku.
- Obsługa wyjątków w bloku `try-catch` wewnątrz lambdy zapobiega przerwaniu działania programu przez nieoczekiwane błędy.
- Dodanie zamknięcia `ExecutorService` po zakończeniu zadań to dobra praktyka zapobiegająca wyciekom zasobów.

---

**User:**

Chcę koniecznie tam użyć Runnable, popraw kod tak aby tam było Runnable

---

**Assistant:**

Rozumiem, że chcesz koniecznie użyć `Runnable`. W takim przypadku `Runnable` nie zwraca żadnej wartości, więc jedynym sposobem na ominięcie tego ograniczenia w kontekście `Future` jest zwrócenie specjalnego obiektu typu `Future<?>` lub alternatywnie zwrócenie stałej wartości, np. `null`.

Jeśli chcesz wykorzystać `Runnable`, aby przeprowadzić obliczenia bez zwracania wyniku, można to zrobić w ten sposób:

### Poprawiony kod z `Runnable`:

```java
import java.util.concurrent.*;

public class FutureExample {
    private final ExecutorService executor = Executors.newSingleThreadExecutor();

    public Future<?> calculateWithRunnable(Integer input) {
        return executor.submit(() -> {
            try {
                // Symulacja opóźnienia
                Thread.sleep(1000);
                
                // Obliczenia
                int result = input * input;
                System.out.println("Wynik: " + result);
                
            } catch (InterruptedException e) {
                // Obsługa przerwanego wątku
                System.err.println("Wątek został przerwany: " + e.getMessage());
                Thread.currentThread().interrupt(); // Przywrócenie statusu przerwania
            } catch (Exception e) {
                // Obsługa innych wyjątków
                System.err.println("Wystąpił błąd: " + e.getMessage());
            }
        });
    }

    public void shutdownExecutor() {
        executor.shutdown();
    }

    public static void main(String[] args) throws ExecutionException, InterruptedException {
        FutureExample example = new FutureExample();
        
        // Uruchamiamy zadanie z Runnable
        Future<?> future = example.calculateWithRunnable(5);

        try {
            // Oczekujemy, aż zadanie zostanie wykonane (zamiast pobierania wyniku)
            future.get();
            System.out.println("Zadanie zakończone.");
        } catch (InterruptedException | ExecutionException e) {
            System.err.println("Błąd podczas wykonywania zadania: " + e.getMessage());
        } finally {
            // Zamykamy executor po zakończeniu
            example.shutdownExecutor();
        }
    }
}
```

### Kluczowe zmiany i wyjaśnienia:

1. **Użycie `Runnable` zamiast `Callable`:** Zachowaliśmy `Runnable`, ponieważ w tym wypadku nie jest wymagane zwracanie wyniku. Zamiast tego zadanie wykonywane jest asynchronicznie, a wynik (kwadrat liczby) jest wyświetlany bezpośrednio wewnątrz lambdy.

2. **Zwracanie `Future<?>`:** Ponieważ `Runnable` nie zwraca wartości, obiekt `Future<?>` reprezentuje asynchroniczne wykonanie zadania, ale nie ma wartości zwracanej. Metoda `get()` na takim `Future` służy jedynie do oczekiwania na zakończenie zadania, bez pobierania wyniku.

3. **Obsługa wyjątków:** Tak jak poprzednio, obsługujemy wyjątki takie jak `InterruptedException` i inne, aby zapewnić stabilność kodu.

4. **Zakończenie zadania:** Zamiast pobierać wynik (ponieważ go nie ma), wywołanie `future.get()` służy jedynie do oczekiwania na zakończenie zadania. Możesz także dodać timeout, jeśli chcesz ograniczyć czas oczekiwania.

5. **Zamknięcie `ExecutorService`:** Tak jak wcześniej, po zakończeniu zadania zamykamy `ExecutorService`.

### Kiedy używać `Runnable`?

Jeżeli chcesz tylko uruchomić zadanie bez konieczności zwracania wartości, `Runnable` jest dobrym wyborem. Jeśli potrzebujesz zwracać wynik obliczeń, wtedy `Callable` będzie bardziej odpowiedni. W tym przypadku, `Runnable` działa, ale warto rozważyć, czy w przyszłych zastosowaniach nie lepsze będzie użycie `Callable`, jeśli wyniki obliczeń są ważne dla dalszego działania aplikacji.

---

**User:**

Podaj przykład z ExecutionException

---

**Assistant:**

`ExecutionException` jest zgłaszany w momencie, gdy zadanie wykonane przez `Future` kończy się wyjątkiem. Wyjątek ten jest „opakowany” w `ExecutionException`, a rzeczywisty wyjątek można uzyskać za pomocą metody `getCause()`.

Poniżej przykład, gdzie zadanie wywołane przez `Runnable` kończy się wyjątkiem (w tym przypadku dzielenie przez zero). Ten wyjątek jest przekazywany do głównego wątku poprzez `ExecutionException`.

### Przykład z `ExecutionException`:

```java
import java.util.concurrent.*;

public class ExecutionExceptionExample {
    private final ExecutorService executor = Executors.newSingleThreadExecutor();

    public Future<?> calculateWithRunnable(Integer input) {
        return executor.submit(() -> {
            try {
                // Symulacja błędu: dzielenie przez zero
                if (input == 0) {
                    throw new ArithmeticException("Dzielenie przez zero!");
                }
                
                // Obliczenia
                int result = 100 / input;
                System.out.println("Wynik: " + result);
                
            } catch (InterruptedException e) {
                // Obsługa przerwanego wątku
                System.err.println("Wątek został przerwany: " + e.getMessage());
                Thread.currentThread().interrupt(); // Przywrócenie statusu przerwania
            }
        });
    }

    public void shutdownExecutor() {
        executor.shutdown();
    }

    public static void main(String[] args) {
        ExecutionExceptionExample example = new ExecutionExceptionExample();
        
        // Uruchamiamy zadanie z Runnable z błędnym inputem (0)
        Future<?> future = example.calculateWithRunnable(0);

        try {
            // Oczekujemy na zakończenie zadania
            future.get();
            System.out.println("Zadanie zakończone pomyślnie.");
        } catch (InterruptedException e) {
            System.err.println("Zadanie zostało przerwane: " + e.getMessage());
        } catch (ExecutionException e) {
            // Obsługa wyjątków wykonania
            System.err.println("Wystąpił błąd podczas wykonywania zadania: " + e.getCause());
        } finally {
            // Zamykamy executor po zakończeniu
            example.shutdownExecutor();
        }
    }
}
```

### Wyjaśnienie:

1. **Wyjątek w zadaniu:** Jeśli `input` jest równy 0, wówczas zostanie rzucony wyjątek `ArithmeticException` z komunikatem „Dzielenie przez zero!”. W normalnych warunkach ten wyjątek zostałby zgłoszony podczas wykonywania zadania, ale ponieważ jest wykonywane asynchronicznie w osobnym wątku, zostaje przechwycony przez mechanizm obsługi `Future`.

2. **Zgłoszenie `ExecutionException`:** Wyjątek ten zostanie „opakowany” w `ExecutionException` i przekazany do wywołania `future.get()`, gdy główny wątek próbuje pobrać wynik zadania.

3. **Obsługa `ExecutionException`:** W bloku `catch`, możemy użyć `e.getCause()`, aby uzyskać oryginalny wyjątek, który spowodował błąd (w tym przypadku `ArithmeticException`).

### Wynik:

Dla wejścia `0`, program wyświetli:

```
Wystąpił błąd podczas wykonywania zadania: java.lang.ArithmeticException: Dzielenie przez zero!
```

To pokazuje, jak obsługiwać wyjątki zgłaszane podczas wykonywania asynchronicznych zadań w Javie za pomocą `Future`.