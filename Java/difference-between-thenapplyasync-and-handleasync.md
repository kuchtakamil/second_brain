# Difference between thenApplyAsync and handleAsync

**Data:** 2024-06-20

---

**User:**

podaj różnice między thenApplyAsync a handleAsync 

---

**Assistant:**

W bibliotekach Java związanych z programowaniem współbieżnym, takich jak `CompletableFuture`, metody `thenApplyAsync` i `handleAsync` są używane do przetwarzania wyników asynchronicznych. Oto główne różnice między nimi:

1. **Cel**:
   - **thenApplyAsync**: Używane do przekształcania wyniku operacji asynchronicznej. Przyjmuje funkcję, która przetwarza wynik poprzedniego etapu i zwraca nowy wynik.
   - **handleAsync**: Używane do przetwarzania zarówno wyniku operacji asynchronicznej, jak i wyjątków. Przyjmuje funkcję, która przetwarza zarówno wynik, jak i wyjątek, i zwraca nowy wynik.

2. **Sygnatura metody**:
   - **thenApplyAsync**: 
     ```java
     public <U> CompletableFuture<U> thenApplyAsync(Function<? super T,? extends U> fn)
     ```
   - **handleAsync**:
     ```java
     public <U> CompletableFuture<U> handleAsync(BiFunction<? super T, Throwable, ? extends U> fn)
     ```

3. **Obsługa wyjątków**:
   - **thenApplyAsync**: Nie obsługuje wyjątków. Jeśli w poprzednim etapie wystąpi wyjątek, `thenApplyAsync` nie zostanie wywołane.
   - **handleAsync**: Obsługuje zarówno wynik, jak i wyjątki. Zawsze zostanie wywołane, niezależnie od tego, czy poprzedni etap zakończył się sukcesem, czy wyjątkiem.

4. **Przykłady**:
   - **thenApplyAsync**:
     ```java
     CompletableFuture.supplyAsync(() -> "Hello")
                      .thenApplyAsync(result -> result + " World")
                      .thenAcceptAsync(System.out::println);
     ```
     W tym przykładzie `thenApplyAsync` przekształca wynik "Hello" na "Hello World".

   - **handleAsync**:
     ```java
     CompletableFuture.supplyAsync(() -> {
         if (true) throw new RuntimeException("Error");
         return "Hello";
     }).handleAsync((result, ex) -> {
         if (ex != null) {
             return "Error occurred: " + ex.getMessage();
         } else {
             return result + " World";
         }
     }).thenAcceptAsync(System.out::println);
     ```
     W tym przykładzie `handleAsync` obsługuje wyjątek i zwraca odpowiedni komunikat.

5. **Wykonanie asynchroniczne**:
   - Obie metody (`thenApplyAsync` i `handleAsync`) wykonują podane funkcje asynchronicznie, używając domyślnego `ForkJoinPool.commonPool()` lub dostarczonego `Executor`.

W skrócie:
- Używaj `thenApplyAsync`, gdy chcesz przekształcić wynik asynchronicznej operacji.
- Używaj `handleAsync`, gdy chcesz obsłużyć zarówno wynik, jak i wyjątki, które mogą wystąpić podczas asynchronicznej operacji.