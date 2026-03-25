# Zalety CompletableFuture w Javie

**Data:** 2024-10-05

---

**User:**

W java dlaczego completablefuture jest lepsze od Future?

---

**Assistant:**

W Javie, `CompletableFuture` jest uważane za lepsze od klasycznego `Future` z kilku powodów, głównie ze względu na większą elastyczność, możliwości kompozycji i obsługę asynchronicznych operacji. Oto kluczowe różnice, które sprawiają, że `CompletableFuture` jest bardziej funkcjonalnym narzędziem niż `Future`:

### 1. **Możliwość ręcznego ustawiania wyniku**
   - W przypadku `Future`, wynik jest ustawiany przez wykonanie zadania w tle (np. poprzez `ExecutorService.submit()`). Nie można samodzielnie ustawić lub zmienić wyniku.
   - `CompletableFuture` pozwala na ręczne ustawienie wyniku (metody takie jak `complete()` lub `completeExceptionally()`), co daje większą kontrolę nad procesem przetwarzania.

### 2. **Kompozycja i łączenie asynchronicznych operacji**
   - `Future` nie pozwala na łatwe łączenie lub sekwencjonowanie zadań. Aby połączyć kilka zadań, trzeba napisać dodatkowy kod obsługujący takie sytuacje.
   - `CompletableFuture` oferuje różne metody do łączenia i kompozycji zadań, takie jak `thenApply()`, `thenCompose()`, `thenAccept()`, które umożliwiają łatwe przetwarzanie wyników zadań, nawet w sposób asynchroniczny. Dzięki temu można z łatwością budować złożone przepływy operacji.

### 3. **Łatwa obsługa wyjątków**
   - W `Future`, aby obsłużyć wyjątki, trzeba ręcznie sprawdzać, czy wywołanie metody `get()` rzuciło wyjątek, co nie jest intuicyjne ani wygodne.
   - `CompletableFuture` ma wbudowaną obsługę wyjątków za pomocą metod takich jak `exceptionally()`, `handle()`, czy `whenComplete()`. To pozwala na bardziej czytelny i efektywny sposób obsługi błędów w operacjach asynchronicznych.

### 4. **Nieblokująca się natura** 
   - `Future.get()` blokuje bieżący wątek do momentu zakończenia operacji. W efekcie, jeśli chcesz uzyskać wynik z `Future`, musisz czekać, aż zadanie się zakończy.
   - `CompletableFuture` pozwala na rejestrację "callbacków", które zostaną wywołane, gdy zadanie się zakończy. Nie musisz blokować wątku oczekującego na wynik, ponieważ `CompletableFuture` obsługuje zdarzenia asynchroniczne.

### 5. **Metody asynchroniczne**
   - `CompletableFuture` oferuje metody asynchroniczne, takie jak `supplyAsync()`, które automatycznie wykonują zadanie w tle na domyślnym lub dostarczonym przez użytkownika executorze, co jest znacznie bardziej zintegrowane i elastyczne niż w przypadku `Future`.

### 6. **Zadania zależne od siebie**
   - `CompletableFuture` ułatwia tworzenie zależności pomiędzy zadaniami. Metody takie jak `thenCombine()` pozwalają na uruchomienie kolejnego zadania po zakończeniu dwóch niezależnych, co jest znacznie trudniejsze do zrealizowania za pomocą samego `Future`.

### 7. **Możliwość skorzystania z API reaktywnego**
   - `CompletableFuture` pozwala na bardziej reaktywne programowanie dzięki możliwości reagowania na zakończenie operacji w sposób bardziej naturalny i funkcjonalny, co jest trudne lub niemożliwe do osiągnięcia przy użyciu `Future`.

Podsumowując, `CompletableFuture` to bardziej nowoczesna i wszechstronna wersja `Future`, oferująca znacznie więcej możliwości związanych z przetwarzaniem asynchronicznym, obsługą wyjątków oraz kompozycją zadań. W efekcie, jest to preferowana opcja do pracy z asynchronicznością w nowoczesnych aplikacjach Javy.

---

**User:**

Podaj najważniejsze metody completablefuture i krótko je opisz

---

**Assistant:**

`CompletableFuture` oferuje wiele metod do pracy z asynchronicznymi zadaniami, kompozycją operacji oraz obsługą wyjątków. Oto najważniejsze z nich z krótkim opisem:

### 1. **`supplyAsync(Supplier<U>)`**
   - Uruchamia asynchronicznie dostarczone zadanie, które zwraca wynik. Zadanie wykonywane jest na domyślnym `ForkJoinPool`u (wątkach systemowych).
   - **Przykład**: `CompletableFuture.supplyAsync(() -> "Hello")`
  
### 2. **`runAsync(Runnable)`**
   - Uruchamia asynchronicznie zadanie bez zwracania wyniku. Wykonuje tylko akcję.
   - **Przykład**: `CompletableFuture.runAsync(() -> System.out.println("Task completed"))`

### 3. **`thenApply(Function<T, U>)`**
   - Przetwarza wynik po zakończeniu asynchronicznego zadania i zwraca przekształcony wynik. Używane do modyfikowania wyniku.
   - **Przykład**: `future.thenApply(result -> result + " World")`

### 4. **`thenAccept(Consumer<T>)`**
   - Akceptuje wynik asynchronicznego zadania, ale niczego nie zwraca. Używane do uruchomienia kodu, który konsumuje wynik.
   - **Przykład**: `future.thenAccept(result -> System.out.println("Result: " + result))`

### 5. **`thenRun(Runnable)`**
   - Wykonuje podany kod, gdy poprzednie zadanie zostanie zakończone, ale nie bierze pod uwagę jego wyniku.
   - **Przykład**: `future.thenRun(() -> System.out.println("All tasks completed"))`

### 6. **`thenCombine(CompletionStage<U>, BiFunction<T,U,R>)`**
   - Łączy wynik dwóch zadań, gdy oba są zakończone, i zwraca nowy wynik na podstawie dwóch wejściowych wyników.
   - **Przykład**: `future1.thenCombine(future2, (result1, result2) -> result1 + result2)`

### 7. **`thenCompose(Function<T, CompletionStage<U>>)`**
   - Służy do łączenia asynchronicznych zadań zależnych od siebie. Umożliwia kontynuowanie przetwarzania na podstawie wyniku pierwszego zadania i zwraca nowe `CompletableFuture`.
   - **Przykład**: `future.thenCompose(result -> getAnotherFuture(result))`

### 8. **`exceptionally(Function<Throwable, T>)`**
   - Obsługuje wyjątki, które wystąpiły podczas wykonywania zadania. Pozwala na dostarczenie wartości alternatywnej w przypadku błędu.
   - **Przykład**: `future.exceptionally(ex -> "Error occurred: " + ex.getMessage())`

### 9. **`handle(BiFunction<T, Throwable, U>)`**
   - Obsługuje zarówno sukces, jak i wyjątek. Umożliwia przetwarzanie wyniku lub błędu.
   - **Przykład**: `future.handle((result, ex) -> { if (ex != null) return "Error"; else return result; })`

### 10. **`whenComplete(BiConsumer<T, Throwable>)`**
   - Wykonuje kod po zakończeniu zadania, niezależnie od tego, czy zakończyło się ono sukcesem czy wyjątkiem. Nie modyfikuje wyniku.
   - **Przykład**: `future.whenComplete((result, ex) -> { if (ex == null) System.out.println(result); else System.out.println("Error"); })`

### 11. **`complete(T value)`**
   - Ustawia wynik `CompletableFuture`, jeśli zadanie jeszcze się nie zakończyło. 
   - **Przykład**: `future.complete("Manual result")`

### 12. **`completeExceptionally(Throwable ex)`**
   - Ustawia wynik w przypadku wystąpienia wyjątku, jeśli zadanie jeszcze się nie zakończyło.
   - **Przykład**: `future.completeExceptionally(new RuntimeException("Manual failure"))`

### 13. **`allOf(CompletableFuture<?>... futures)`**
   - Zwraca nowy `CompletableFuture`, który zostanie zakończony, gdy wszystkie przekazane futures zostaną zakończone.
   - **Przykład**: `CompletableFuture.allOf(future1, future2).thenRun(() -> System.out.println("All tasks done"))`

### 14. **`anyOf(CompletableFuture<?>... futures)`**
   - Zwraca nowy `CompletableFuture`, który zostanie zakończony, gdy którekolwiek z przekazanych futures zostanie zakończone.
   - **Przykład**: `CompletableFuture.anyOf(future1, future2).thenAccept(result -> System.out.println("First result: " + result))`

### 15. **`join()`**
   - Podobnie jak `get()`, zwraca wynik zadania, ale nie rzuca wyjątków sprawdzanych. Używane, gdy wiadomo, że zadanie zakończy się sukcesem.
   - **Przykład**: `String result = future.join();`

### 16. **`get()`**
   - Blokująca metoda, która zwraca wynik `CompletableFuture` po zakończeniu zadania, ale może rzucić wyjątki.
   - **Przykład**: `String result = future.get();`

### 17. **`orTimeout(long timeout, TimeUnit unit)`**
   - Ustawia limit czasu, po którym zadanie zakończy się niepowodzeniem, jeśli nie zostanie ukończone.
   - **Przykład**: `future.orTimeout(1, TimeUnit.SECONDS)`

### 18. **`completeOnTimeout(T value, long timeout, TimeUnit unit)`**
   - Ustawia wartość domyślną, jeśli zadanie nie zakończy się w określonym czasie.
   - **Przykład**: `future.completeOnTimeout("Default Value", 1, TimeUnit.SECONDS)`

Te metody dają ogromne możliwości w zakresie zarządzania asynchronicznymi operacjami w Javie, pozwalając na budowanie bardziej złożonych przepływów programistycznych z obsługą wyjątków i kompozycją zadań.