# Quarkus CompletionStage Asynchroniczne Akcje

**Data:** 2023-12-28

---

**User:**

W Java, Quarkus, mam metodę która uruchamia w sposób asynchroniczny akcję i zwraca CompletionStage. Chcę aby po zakończeniu tej asynchronicznej akcji wywołać kolejną inną akcją. Jak to zrobić

---

**Assistant:**

W Javie, korzystając z Quarkus i asynchronicznych operacji, możesz wykorzystać `CompletionStage` do łańcuchowania działań. Gdy masz metodę, która zwraca `CompletionStage`, możesz użyć metody `thenCompose` lub `thenAccept` do wykonania kolejnej akcji po zakończeniu pierwszej. Oto przykładowy sposób, w jaki możesz to zrobić:

1. **Użyj `thenCompose` dla Asynchronicznych Ciągów Akcji**: Jeśli chcesz, aby kolejna akcja była również asynchroniczna i zwracała `CompletionStage`, możesz użyć `thenCompose`. Metoda `thenCompose` pozwala na łańcuchowanie kolejnej asynchronicznej operacji, która zostanie rozpoczęta po zakończeniu poprzedniej.

   ```java
   public CompletionStage<ResultType> pierwszaAkcja() {
       // logika asynchroniczna
   }

   public CompletionStage<AnotherResultType> drugaAkcja(ResultType result) {
       // kolejna logika asynchroniczna
   }

   public void uruchomAkcje() {
       pierwszaAkcja()
           .thenCompose(this::drugaAkcja)
           .thenAccept(finalResult -> {
               // Obsługa ostatecznego wyniku
           });
   }
   ```

2. **Użyj `thenAccept` dla Prostych Ciągów Akcji**: Jeśli druga akcja jest prostą operacją (np. wydrukiem lub zapisem), która nie wymaga zwracania `CompletionStage`, możesz użyć `thenAccept`. Metoda `thenAccept` pozwala na wykonanie operacji, która przyjmuje wynik poprzedniej operacji, ale nie zwraca nowego `CompletionStage`.

   ```java
   public CompletionStage<ResultType> pierwszaAkcja() {
       // logika asynchroniczna
   }

   public void drugaAkcja(ResultType result) {
       // Prosta operacja, np. wydruk
   }

   public void uruchomAkcje() {
       pierwszaAkcja()
           .thenAccept(this::drugaAkcja);
   }
   ```

W obu przypadkach, metody `thenCompose` i `thenAccept` są używane do łańcuchowania operacji, gdzie druga akcja rozpoczyna się po zakończeniu pierwszej. Ważne jest, aby pamiętać, że te operacje są wykonywane asynchronicznie, co oznacza, że kod poza tymi łańcuchami może być wykonany przed ich zakończeniem.

---

**User:**

W Quarkus przy pomocy 
@Inject
Event<MyEvent> appEvent

appEvent.fireAsync(new MyNewEvent())
wysyłam MyNewEvent
Chciałbym po tym jak to zadanie się wykona i przyjdzie potwierdzenie, że praca się zakończyła, chciałbym wysłać następny event

---

**Assistant:**

W Quarkus, gdy używasz asynchronicznego modelu eventowego z `Event<MyEvent>.fireAsync(...)`, możesz zastosować mechanizm `CompletionStage`, aby wykonać pewne działania po zakończeniu asynchronicznej operacji. Aby wysłać następny event po otrzymaniu potwierdzenia zakończenia pierwszego, możesz łańcuchować operacje używając metod dostępnych w `CompletionStage`.

Oto przykład, jak możesz to zrobić:

1. **Wysyłanie Pierwszego Eventu**: Rozpocznij od wysłania pierwszego asynchronicznego eventu przy użyciu `fireAsync`.

   ```java
   @Inject
   Event<MyEvent> appEvent;

   public CompletionStage<Void> wyslijPierwszyEvent() {
       MyNewEvent pierwszyEvent = new MyNewEvent();
       return appEvent.fireAsync(pierwszyEvent);
   }
   ```

2. **Łańcuchowanie Następnego Eventu po Zakończeniu**: Użyj metody `thenRun` lub `thenAccept` na `CompletionStage`, aby wysłać kolejny event po zakończeniu pierwszego.

   ```java
   public void wyslijNastepnyEventPoZakonczeniu() {
       wyslijPierwszyEvent()
           .thenRun(() -> {
               MyNextEvent nastepnyEvent = new MyNextEvent();
               appEvent.fireAsync(nastepnyEvent);
           });
   }
   ```

W tym przykładzie, metoda `thenRun` jest używana do wykonania kodu po zakończeniu asynchronicznej operacji wysłania pierwszego eventu. Wewnątrz `thenRun`, możesz umieścić logikę do wysłania następnego eventu.

Jeśli potrzebujesz przekazać wynik pierwszego eventu do drugiego, możesz zamiast tego użyć `thenAccept`, które przyjmuje wynik pierwszego eventu jako argument:

```java
wyslijPierwszyEvent()
    .thenAccept(result -> {
        // Możesz tutaj przetworzyć wynik pierwszego eventu, jeśli jest potrzebny
        MyNextEvent nastepnyEvent = new MyNextEvent();
        appEvent.fireAsync(nastepnyEvent);
    });
```

Upewnij się, że obsługujesz również potencjalne wyjątki i błędy, które mogą wystąpić podczas przetwarzania asynchronicznego.

---

**User:**

Quarkus, czy w przypadku appEvent.fireAsync(...) CompletionStage jest zwracany od razu po wysłaniu eventu, czy gdy obserwatorzy odbiorą event, czy gdy obserwatorzy odbiorą event i wykonają swoją pracę?

---

**Assistant:**

W Quarkus, kiedy używasz `appEvent.fireAsync(...)`, `CompletionStage` jest zwracany nie w momencie wysłania eventu, ale po jego przetworzeniu przez wszystkich obserwatorów (listeners). Oznacza to, że `CompletionStage` zwrócony przez `fireAsync` zostanie zakończony (completed), gdy wszyscy obserwatorzy, którzy nasłuchują na ten event, wykonają swoją pracę.

W praktyce wygląda to tak:

1. **Wysyłanie Eventu**: Gdy wywołujesz `fireAsync(...)`, event jest umieszczany w kolejce do asynchronicznego przetworzenia.

2. **Przetwarzanie przez Obserwatorów**: Obserwatorzy, którzy są zainteresowani tym eventem (tj. mają metody oznaczone adnotacją `@ObservesAsync` odpowiadające typowi eventu), będą przetwarzać event w sposób asynchroniczny.

3. **Zakończenie `CompletionStage`**: `CompletionStage` zwrócony przez `fireAsync(...)` zostanie zakończony, gdy wszyscy obserwatorzy zakończą przetwarzanie eventu. Oznacza to, że operacje zdefiniowane w metodach takich jak `thenAccept`, `thenRun`, czy `thenCompose` zostaną wykonane po zakończeniu pracy wszystkich obserwatorów.

Przykład:

```java
appEvent.fireAsync(new MyEvent())
    .thenRun(() -> System.out.println("Wszyscy obserwatorzy zakończyli przetwarzanie eventu."));
```

W tym przykładzie, tekst zostanie wydrukowany dopiero po tym, jak wszyscy obserwatorzy zakończą przetwarzanie eventu `MyEvent`.

Jest to użyteczne w scenariuszach, gdzie chcesz mieć pewność, że pewne operacje (np. wysłanie odpowiedzi do użytkownika, zapisanie stanu aplikacji) zostaną wykonane dopiero po całkowitym przetworzeniu eventu przez wszystkie zainteresowane komponenty aplikacji.