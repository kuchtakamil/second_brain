# Vavr flatMap vs map

**Data:** 2024-11-24

---

**User:**

Wklejam kod Java
import io.vavr.collection.HashSet;  // we use functional library 'vavr' ...
import io.vavr.collection.Set;      // ... for sets and linked lists.
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;
import java.util.*;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.TimeUnit;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.select.Elements;


public class Crawler {
  private final HttpClient httpClient =
      HttpClient.newBuilder()
          .version(HttpClient.Version.HTTP_1_1)
          .followRedirects(HttpClient.Redirect.NORMAL)
          .build();

  public Crawler() {}

  // Only place/method where we call 'Jsoup' library.
  // Alternatively, we could have used a regex expression.
  private Set<String> extractLinks(String htmlDoc) {
    Document doc = Jsoup.parse(htmlDoc);
    Elements elements = doc.select("a[href]");
    return HashSet.ofAll(elements).map(element -> element.attr("abs:href"));
  }

  // Given the set of Uris obtained from the method above,
  // we parse it and filter undesirable ones
  private Set<URI> parseURI(Set<String> strUris) {
    return strUris // this is a 'vavr' set. But don't let distract you
        .flatMap( // flatMap is a very useful ( does not exist on standard Java sets)
            uriStr -> {
              try {
                URI uri = URI.create(uriStr);
                // Below, the last two parameters set to null are the 'queryString` and 'fragment'
                return HashSet.of(
                    new URI(uri.getScheme(), uri.getAuthority(), uri.getPath(), null, null));
              } catch (Exception e) {
                return HashSet.empty(); // don't fail parsing the others if one URI fails parsing
              }
            })
        .filter(uri -> Objects.equals(uri.getScheme(), "https"))
        .filter(uri -> uri.getHost() != null && !uri.getHost().isBlank())
        .filter(uri -> uri.getPath().endsWith(".html") || !uri.getPath().contains("."));
  }
}

Użyty został tu Set z biblioteki vavr. Na obiekcie tego setu wykonywana jest funkcja flatMap. Dlaczego zgodnie z komentarzem nie wystarczyłaby tutaj funkcja map?

---

**Assistant:**

W tym kodzie użycie metody `flatMap` w kontekście `Set` z biblioteki Vavr ma kluczowe znaczenie. Główna różnica między `map` a `flatMap` polega na tym, że:

- **`map`**: Przekształca każdy element kolekcji na inny element. Wynikiem operacji jest kolekcja tej samej struktury, w której każdy element odpowiada dokładnie jednemu elementowi wejściowemu.
- **`flatMap`**: Przekształca każdy element kolekcji na kolekcję (lub strumień elementów), a następnie „spłaszcza” wynik w jedną kolekcję.

### Dlaczego `flatMap` zamiast `map`?

W metodzie `parseURI`, dla każdego łańcucha znaków (String) reprezentującego URI, funkcja `flatMap`:

1. **Tworzy nowy URI przy użyciu `URI.create` oraz `new URI`.**
   - W wyniku przekształcenia pojedynczego ciągu znaków może powstać:
     - Pojedynczy poprawny URI, jeśli wszystko pójdzie zgodnie z planem.
     - Pusty zbiór (`HashSet.empty()`), jeśli parsowanie zakończy się błędem.
   - **Metoda `flatMap` umożliwia operację, w której jeden element wejściowy może prowadzić do 0, 1, lub więcej elementów w wyniku.**

2. **Obsługuje błędy bez przerywania przetwarzania.**
   - Jeśli parsowanie jednego URI zakończy się wyjątkiem, `flatMap` zwraca pusty zbiór (`HashSet.empty()`), co oznacza, że ten URI jest pomijany.
   - `map` nie pozwoliłby łatwo „pominąć” elementu, ponieważ zawsze musi zwrócić dokładnie jeden element.

3. **Zwraca płaski wynik zamiast kolekcji kolekcji.**
   - `flatMap` łączy wynik z różnych elementów wejściowych w jedną płaską kolekcję (w tym przypadku `Set`).
   - Gdyby użyto `map`, wynikiem byłby zbiór zagnieżdżonych kolekcji (`Set<Set<URI>>`), co nie jest pożądane w tym przypadku.

### Co by się stało, gdyby użyto `map`?

Gdyby zamiast `flatMap` zastosowano `map`, wynik metody `parseURI` byłby strukturą `Set<HashSet<URI>>`. W takim przypadku:

- Musiałbyś dodatkowo spłaszczyć wynik na `Set<URI>`, co wymagałoby dodatkowych operacji.
- Utrudnione byłoby ignorowanie błędów parsowania, ponieważ metoda `map` wymaga, aby zawsze zwracać wynik dla każdego elementu wejściowego.

### Podsumowanie

Użycie `flatMap` jest tutaj konieczne, ponieważ:

- Pozwala na przekształcenie jednego elementu w zero, jeden lub więcej elementów.
- Automatycznie spłaszcza wynik w jedną kolekcję.
- Ułatwia obsługę błędów, umożliwiając zwracanie pustego zbioru dla nieprawidłowych URI. 

Dlatego `map` byłoby niewystarczające w tym przypadku.

---

**User:**

a czy nie dałoby się zrobić tego tak z funkcją map?
map(uriStr -> { 
              try {
                return URI.create(uriStr);
              } catch (Exception e) {
                return URI.empty(); 
              }
....

---

**Assistant:**

Twój pomysł z użyciem `map` nie jest wystarczający w tym przypadku, ponieważ metoda `map` **zawsze musi zwracać dokładnie jeden element dla każdego elementu wejściowego**. Jednak metoda `parseURI` wymaga operacji, w której:

1. Jeden element wejściowy (`uriStr`) może zostać przekształcony w:
   - Pusty zbiór (`HashSet.empty()`), gdy URI jest niepoprawne.
   - Jeden poprawny URI, jeśli parsowanie się powiedzie.
   - **Więcej niż jeden URI**, jeśli są generowane różne warianty URI.

Jeśli spróbujesz wymusić to za pomocą `map`, napotkasz problem: `map` oczekuje jednego wyniku dla każdego wejścia. Twój przykład:

```java
map(uriStr -> { 
    try {
        return URI.create(uriStr);
    } catch (Exception e) {
        return URI.empty(); 
    }
})
```

ma dwa problemy:

1. **`URI.empty()` nie istnieje w standardowej klasie `URI`.**
   W Javie nie ma metody `empty()` dla klasy `URI`. Musiałbyś zwracać coś innego, np. `null` lub specjalną wartość URI, co wprowadziłoby dodatkową złożoność przy filtrowaniu wyników.

2. **Nie rozwiązuje problemu zwracania wielu elementów.**
   `map` zwraca dokładnie jeden wynik dla każdego elementu wejściowego. Jeśli chcesz, aby niektóre wejścia dawały więcej niż jeden wynik (np. różne warianty URI), musiałbyś ręcznie scalać wyniki w dalszych krokach, co jest niewygodne i nieefektywne.

### Dlaczego `flatMap` jest odpowiednie?
Dzięki `flatMap`, dla każdego `uriStr` możesz zwrócić:

- `HashSet.empty()`, jeśli parsowanie się nie powiedzie.
- `HashSet.of(uri)` w przypadku poprawnego URI.
- `HashSet.of(...)` z wieloma URI, jeśli zajdzie taka potrzeba.

Przykład z `flatMap` w Twoim kodzie:

```java
.flatMap(uriStr -> {
    try {
        URI uri = URI.create(uriStr);
        return HashSet.of(new URI(uri.getScheme(), uri.getAuthority(), uri.getPath(), null, null));
    } catch (Exception e) {
        return HashSet.empty();
    }
})
```

- Każdy `uriStr` może zostać przekształcony w 0, 1 lub wiele URI.
- Wynik jest automatycznie spłaszczany do jednej kolekcji typu `Set`.

### Czy `map` mogłoby działać?
W teorii można by próbować użyć `map`, ale wymagałoby to dodatkowego kroku spłaszczania wyniku (np. `flatMap` później lub ręczne przetwarzanie):

```java
Set<HashSet<URI>> nestedSet = strUris.map(uriStr -> {
    try {
        URI uri = URI.create(uriStr);
        return HashSet.of(new URI(uri.getScheme(), uri.getAuthority(), uri.getPath(), null, null));
    } catch (Exception e) {
        return HashSet.empty();
    }
});

// Spłaszczenie (ręcznie lub za pomocą `flatMap` później):
Set<URI> flatSet = nestedSet.flatMap(set -> set);
```

Jednak jest to bardziej skomplikowane, mniej czytelne i wprowadza niepotrzebne zagnieżdżenie danych. Dlatego `flatMap` od razu w miejscu jest naturalnym i lepszym wyborem w tym przypadku.