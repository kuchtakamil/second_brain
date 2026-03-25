# Spłaszczanie CompletableFuture

**Data:** 2024-11-27

---

**User:**

Czy w java jest szybki sposób aby z CompletableFuture<Set<CompletableFuture<Set<URI>>>> zrobić CompletableFuture<Set<URI>>?

---

**Assistant:**

Tak, w Javie można łatwo przekształcić strukturę `CompletableFuture<Set<CompletableFuture<Set<URI>>>>` na `CompletableFuture<Set<URI>>`, korzystając z funkcji pomocniczych, takich jak `CompletableFuture.allOf` oraz strumieni. Oto, jak to zrobić:

### Rozwiązanie:
```java
import java.net.URI;
import java.util.Set;
import java.util.concurrent.CompletableFuture;
import java.util.stream.Collectors;

public class CompletableFutureExample {
    public static void main(String[] args) {
        // Zakładamy, że mamy CompletableFuture<Set<CompletableFuture<Set<URI>>>>
        CompletableFuture<Set<CompletableFuture<Set<URI>>>> futureSetOfFutures = ...;

        CompletableFuture<Set<URI>> flattenedFuture = futureSetOfFutures.thenCompose(setOfFutures -> 
            CompletableFuture.allOf(
                setOfFutures.toArray(new CompletableFuture[0])
            ).thenApply(v -> 
                setOfFutures.stream()
                    .map(CompletableFuture::join) // Łączenie wewnętrznych wyników
                    .flatMap(Set::stream)         // Spłaszczenie zbiorów
                    .collect(Collectors.toSet()) // Zebranie do jednego zbioru
            )
        );

        // Obsługa wyniku
        flattenedFuture.thenAccept(flattenedSet -> 
            System.out.println("Zflattenowany zbiór: " + flattenedSet)
        );
    }
}
```

### Wyjaśnienie:
1. **`thenCompose`**:
   - Po `futureSetOfFutures` wywołujemy `thenCompose`, aby operować na wynikowym `Set<CompletableFuture<Set<URI>>>`.

2. **`CompletableFuture.allOf`**:
   - `allOf` pozwala utworzyć jeden `CompletableFuture`, który zakończy się dopiero, gdy wszystkie wewnętrzne `CompletableFuture` zakończą się.

3. **`thenApply`**:
   - Po zakończeniu wszystkich wewnętrznych `CompletableFuture`, strumieniujemy wyniki:
     - `map(CompletableFuture::join)` - pobieramy wyniki z wewnętrznych `CompletableFuture`.
     - `flatMap(Set::stream)` - spłaszczamy zagnieżdżone `Set<Set<URI>>` do `Set<URI>`.
     - `collect(Collectors.toSet())` - zbieramy wyniki do jednego zbioru.

### Efekt:
Otrzymujesz `CompletableFuture<Set<URI>>`, który zawiera wszystkie URI z wewnętrznych zbiorów po zakończeniu operacji.

---

**User:**

Czy można to też zrobić szybko w Scala? Możesz użyć innych klas jako przykład

---

**Assistant:**

Tak, w Scali można to zrobić bardzo elegancko i zwięźle dzięki wbudowanym funkcjom monadycznym w `Future` i bibliotece standardowej. W poniższym przykładzie użyjemy `Future[Set[Future[Set[URI]]]]` jako analogicznego do przykładu z Javy.

### Rozwiązanie w Scali
```scala
import scala.concurrent.{Future, ExecutionContext}
import java.net.URI
import scala.concurrent.ExecutionContext.Implicits.global

object FutureFlattenExample extends App {
  // Przykładowa struktura Future[Set[Future[Set[URI]]]]
  val futureSetOfFutures: Future[Set[Future[Set[URI]]]] = Future.successful(
    Set(
      Future.successful(Set(new URI("http://example.com"), new URI("http://example.org"))),
      Future.successful(Set(new URI("http://example.net")))
    )
  )

  // Spłaszczenie Future[Set[Future[Set[URI]]]] do Future[Set[URI]]
  val flattenedFuture: Future[Set[URI]] = for {
    setOfFutures <- futureSetOfFutures              // Rozpakowanie zewnętrznego Future
    sets <- Future.sequence(setOfFutures)          // Połączenie wszystkich Future w Set
  } yield sets.flatten                             // Spłaszczenie Set[Set[URI]] do Set[URI]

  // Obsługa wyniku
  flattenedFuture.map { flattenedSet =>
    println(s"Spłaszczony zbiór: $flattenedSet")
  }
}
```

### Wyjaśnienie
1. **`for` comprehension**:
   - Wykorzystujemy wyrażenie `for`, które jest naturalnym sposobem pracy z monadami w Scali. Wartości wewnętrzne `Future` są automatycznie rozpakowywane.

2. **`Future.sequence`**:
   - Funkcja `Future.sequence` przekształca `Set[Future[T]]` w `Future[Set[T]]`. Dzięki temu możemy czekać na zakończenie wszystkich wewnętrznych `Future`.

3. **`flatten`**:
   - Po `Future.sequence` mamy `Future[Set[Set[URI]]]`. Wywołujemy `.flatten`, aby spłaszczyć `Set[Set[URI]]` do `Set[URI]`.

### Dlaczego Scala jest bardziej zwięzła?
Scala pozwala na lepsze wykorzystanie wyrażeń monadycznych (takich jak `Future`) w postaci bardziej zwięzłej składni `for` oraz funkcji takich jak `sequence` i `flatten`. Dzięki temu kod jest bardziej czytelny i przypomina deklaratywny opis przekształcenia.

### Efekt
Po zakończeniu wszystkich operacji mamy `Future[Set[URI]]`, który zawiera spłaszczony zbiór URI.

---

**User:**

Wróćmy do Javy. Czy gdyby nie istniała funkcja CompletableFuture.allOf, używalibyśmy CompletableFuture tylko czegoś innego, to czy moglibyśmy to zrobić?

---

**Assistant:**

Tak, w Javie można osiągnąć ten sam efekt bez użycia `CompletableFuture.allOf`, choć będzie to wymagało nieco więcej pracy. Kluczem jest manualne połączenie wielu `CompletableFuture` w jeden, wykorzystując ich metody, takie jak `thenCombine`, `thenCompose`, lub pętle z ręcznym zarządzaniem kolekcjami wyników.

### Rozwiązanie bez `CompletableFuture.allOf`

Poniżej przykład, jak to zrobić, ręcznie zarządzając wynikami z `CompletableFuture`:

```java
import java.net.URI;
import java.util.HashSet;
import java.util.Set;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;

public class ManualCompletableFutureFlatten {
    public static void main(String[] args) throws ExecutionException, InterruptedException {
        // Przykładowa struktura CompletableFuture<Set<CompletableFuture<Set<URI>>>>
        CompletableFuture<Set<CompletableFuture<Set<URI>>>> futureSetOfFutures = CompletableFuture.supplyAsync(() -> {
            Set<CompletableFuture<Set<URI>>> setOfFutures = new HashSet<>();
            setOfFutures.add(CompletableFuture.supplyAsync(() -> Set.of(URI.create("http://example.com"))));
            setOfFutures.add(CompletableFuture.supplyAsync(() -> Set.of(URI.create("http://example.org"))));
            return setOfFutures;
        });

        // Spłaszczenie bez CompletableFuture.allOf
        CompletableFuture<Set<URI>> flattenedFuture = futureSetOfFutures.thenCompose(setOfFutures -> {
            CompletableFuture<Set<URI>> result = CompletableFuture.completedFuture(new HashSet<>());

            for (CompletableFuture<Set<URI>> innerFuture : setOfFutures) {
                result = result.thenCombine(innerFuture, (accumulatedSet, newSet) -> {
                    accumulatedSet.addAll(newSet); // Dodanie wyników do zbioru
                    return accumulatedSet;
                });
            }

            return result;
        });

        // Obsługa wyniku
        flattenedFuture.thenAccept(flattenedSet ->
            System.out.println("Spłaszczony zbiór: " + flattenedSet)
        ).get(); // Czekanie na wynik (tylko na potrzeby demonstracji)
    }
}
```

### Wyjaśnienie
1. **`thenCompose`**:
   - Zewnętrzny `CompletableFuture` rozpakowujemy za pomocą `thenCompose`, aby operować na wyniku typu `Set<CompletableFuture<Set<URI>>>`.

2. **Manualne iterowanie przez `Set<CompletableFuture<Set<URI>>>`**:
   - Używamy pętli, aby kolejno łączyć wyniki każdego wewnętrznego `CompletableFuture` z akumulowanym `CompletableFuture<Set<URI>>`.

3. **`thenCombine`**:
   - `thenCombine` pozwala połączyć wynik dwóch `CompletableFuture`, dodając nowy zestaw wyników do akumulowanego zbioru.

4. **`CompletableFuture.completedFuture`**:
   - Zaczynamy od pustego `Set<URI>`, które stopniowo uzupełniamy o kolejne wartości.

### Wady podejścia
- **Mniej czytelne**: Kod jest bardziej skomplikowany niż w przypadku użycia `CompletableFuture.allOf`.
- **Potencjalna złożoność**: Wymaga ręcznego zarządzania akumulacją wyników, co może być podatne na błędy w bardziej złożonych przypadkach.

### Zaletą jest:
To rozwiązanie działa niezależnie od istnienia `CompletableFuture.allOf` i daje pełną kontrolę nad logiką agregacji.

### Efekt
Tak jak poprzednio, wynik to `CompletableFuture<Set<URI>>`, które spłaszcza wszystkie zagnieżdżone wyniki.