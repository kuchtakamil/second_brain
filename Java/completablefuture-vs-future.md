# CompletableFuture vs Future

**Data:** 2024-11-24

---

**User:**

W Java jakie zalety ma CompletableFuture nad Future oraz odwrotnie

---

**Assistant:**

W Javie zarówno `CompletableFuture`, jak i `Future` służą do obsługi programowania asynchronicznego, ale różnią się funkcjonalnością i zakresem zastosowania. Poniżej przedstawiono ich zalety i ograniczenia:

---

### **Zalety `CompletableFuture` nad `Future`:**

1. **Łatwiejsza obsługa zadań asynchronicznych:**
   - `CompletableFuture` pozwala na łączenie i przetwarzanie zadań asynchronicznych przy użyciu metod takich jak `.thenApply()`, `.thenAccept()`, `.thenCompose()`, czy `.thenCombine()`.
   - Umożliwia pisanie bardziej czytelnego i deklaratywnego kodu.

2. **Możliwość ręcznego ustawiania wyniku:**
   - `CompletableFuture` pozwala programiście ręcznie ustawić wynik lub błąd (metody `.complete()` i `.completeExceptionally()`), co jest przydatne np. w testach lub specyficznych scenariuszach.

3. **Brak blokowania podczas oczekiwania na wynik:**
   - W przypadku `Future`, aby uzyskać wynik, musisz wywołać `.get()`, co blokuje bieżący wątek. W `CompletableFuture` możesz zarejestrować callbacki i pracować dalej.

4. **Wsparcie dla potoków i kombinacji:**
   - `CompletableFuture` umożliwia łatwe łączenie wielu zadań asynchronicznych w potoki (pipeline), np. poprzez metody `.thenCombine()` (łącz zadania), `.applyToEither()` (wybierz pierwszy zakończony).

5. **Obsługa wyjątków:**
   - `CompletableFuture` ma wbudowane mechanizmy do obsługi wyjątków, np. `.exceptionally()` lub `.handle()`, co pozwala na bardziej elegancką obsługę błędów.

6. **Asynchroniczność z różnymi executorami:**
   - Metody takie jak `.thenApplyAsync()` pozwalają na wykonywanie operacji w osobnym executorze, podczas gdy `Future` tego nie wspiera.

7. **Strumieniowe API:**
   - `CompletableFuture` dobrze współpracuje z API Stream, co pozwala na łatwe przetwarzanie kolekcji w sposób asynchroniczny.

---

### **Zalety `Future` nad `CompletableFuture`:**

1. **Prostota:**
   - `Future` jest prostszy i bardziej intuicyjny, co może być zaletą w przypadku prostych, jednorazowych zadań asynchronicznych.

2. **Mniejsze zużycie pamięci:**
   - `Future` ma mniejszy narzut pamięci i procesora, ponieważ nie obsługuje callbacków ani bardziej zaawansowanych funkcji.

3. **Stabilność i zgodność wstecz:**
   - `Future` istnieje od Javy 5 i może być używany w starszych projektach, gdzie `CompletableFuture` (dostępny od Javy 8) może być nieosiągalny.

4. **Prosta implementacja dla ExecutorService:**
   - Przy standardowym korzystaniu z `ExecutorService`, metoda `.submit()` zwraca obiekt `Future`, co może być wystarczające w prostych przypadkach.

---

### **Kiedy wybrać który?**

- **Użyj `CompletableFuture`, gdy:**
  - Musisz wykonywać złożone przetwarzanie asynchroniczne z zależnościami między zadaniami.
  - Chcesz uniknąć blokowania wątków.
  - Potrzebujesz zaawansowanej obsługi wyjątków i callbacków.
  - Pracujesz z nowoczesnymi API i architekturą.

- **Użyj `Future`, gdy:**
  - Twój przypadek użycia jest prosty (np. jedno zadanie i prosty wynik).
  - Chcesz ograniczyć narzut pamięci i mocy obliczeniowej.
  - Pracujesz ze starszym kodem lub zależnościami. 

W większości nowoczesnych projektów preferuje się `CompletableFuture` ze względu na jego elastyczność i możliwości. Jednak `Future` nadal może być przydatny w prostych, jednowątkowych aplikacjach.