# Obiekt na JSON i odwrotnie

**Data:** 2025-06-17

---

**User:**

[obraz niedostępny: file-service://file-1RfQZoDt4eeEBcf5EFXtfP]

Na zdjęciu jest fragment kodu, który ze stringa involvement.json tworzy obiekt involvement. A jak używając takiego samego mapera z obiektu involvement stworzyć string?

---

**Assistant:**

Aby przy użyciu tego samego `ObjectMapper` przekształcić obiekt `Involvement` z powrotem do JSON-a (czyli `String`a), użyj metody `writeValueAsString()`:

### Przykład:
```java
public static String toJson(Involvement involvement) throws IOException {
    com.fasterxml.jackson.databind.ObjectMapper mapper = new com.fasterxml.jackson.databind.ObjectMapper();
    mapper.registerModule(new JavaTimeModule());
    mapper.registerModule(new Jdk8Module());

    return mapper.writeValueAsString(involvement);
}
```

### Co się tu dzieje:
- Tworzysz `ObjectMapper`, rejestrujesz te same moduły co przy deserializacji (`JavaTimeModule`, `Jdk8Module`), żeby obsłużyć np. `Optional` i `java.time.*`.
- Następnie zamieniasz obiekt na JSON-owego `Stringa`.

Jeśli chcesz uniknąć wielokrotnego tworzenia `ObjectMappera` (co jest kosztowne), można go zdefiniować jako `static final` i reużywać w obu metodach.

Chcesz, żebym przerobił ten fragment z obrazka na pełną klasę z metodą `fromJson()` i `toJson()`?

---

**User:**

Rozszerz. Co miałeś na myśli, jeśli chcesz uniknąć wielokrotnego tworzenia ObjectMapper'a, można zdefiniować jako StaticFinal. Co znaczy StaticFinal? Czy masz na myśli blok kodu?

---

**Assistant:**

Świetne pytanie!

Nie miałem na myśli **bloku kodu**, tylko **pole klasowe** oznaczone jako `static final`, czyli **stałą współdzieloną przez wszystkie instancje klasy**, tworzoną tylko raz.

---

### 🔁 Co się dzieje obecnie w Twoim kodzie?

W każdej metodzie tworzysz nową instancję `ObjectMapper`:
```java
ObjectMapper mapper = new ObjectMapper();
mapper.registerModule(...);
```
To oznacza, że za każdym razem, kiedy wołasz tę metodę, tworzony jest nowy obiekt `mapper`, co niepotrzebnie obciąża pamięć i CPU (bo `ObjectMapper` to ciężki obiekt).

---

### ✅ Co można zrobić lepiej?

Zdefiniować jedną instancję `ObjectMapper` jako `static final`, czyli:
- **`static`** – należy do klasy, nie do instancji
- **`final`** – nie można jej przypisać ponownie po inicjalizacji
- Dzięki temu `ObjectMapper` będzie tworzony tylko raz i używany wielokrotnie.

---

### 📦 Przykład klasy narzędziowej

```java
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import com.fasterxml.jackson.datatype.jdk8.Jdk8Module;

import java.io.IOException;

public class InvolvementJsonUtil {

    private static final ObjectMapper mapper = new ObjectMapper();

    static {
        mapper.registerModule(new JavaTimeModule());
        mapper.registerModule(new Jdk8Module());
    }

    public static Involvement fromJson(String json) throws IOException {
        return mapper.readValue(json, Involvement.class);
    }

    public static String toJson(Involvement involvement) throws IOException {
        return mapper.writeValueAsString(involvement);
    }
}
```

---

### 🔍 Co zyskujesz?

- Nie tworzysz niepotrzebnie wielu obiektów `ObjectMapper`.
- Kod jest bardziej DRY (Don't Repeat Yourself).
- Łatwiejsze do testowania i utrzymania.

---

Jeśli chcesz, mogę też dodać test jednostkowy lub pokazać, jak taki mapper ustawić globalnie w Springu – daj znać!

---

**User:**

Metoda toJson wrzuca IOException. Teraz wywołuje tę metodę toJson w innym miejscu jako metodReference. Zostaje błąd UnhandledException, pomimo że to wywołanie znajduje się w bloku tryCatch i wszystkie wyjątki są obsługiwane.

---

**Assistant:**

Dzięki za konkret – już tłumaczę, co się dzieje.

### 🔍 Problem:
Wywołujesz metodę `toJson` jako **method reference** (czyli np. `InvolvementJsonUtil::toJson`) w kontekście jakiegoś streama, mapy albo innego miejsca, które **nie pozwala na rzucanie checked exceptions (jak `IOException`)**.

Przykład:
```java
List<Involvement> list = ...
List<String> jsonList = list.stream()
    .map(InvolvementJsonUtil::toJson)  // ❌ IOException
    .collect(Collectors.toList());
```

Tu nawet jeśli **cały stream jest w `try-catch`**, to i tak **kompilator zgłasza błąd**, bo `map()` nie pozwala na funkcje rzucające `checked exceptions`.

---

### ✅ Rozwiązania

#### ✅ Opcja 1: "Owinąć" metodę w lambdę z `try-catch`

Zamiast method reference:

```java
.map(involvement -> {
    try {
        return InvolvementJsonUtil.toJson(involvement);
    } catch (IOException e) {
        throw new RuntimeException("Serialization failed", e);
    }
})
```

To zamienia `IOException` na `RuntimeException`, którą możesz później przechwycić globalnie – albo pozwolić jej "polecieć".

---

#### ✅ Opcja 2: Zmienić `toJson` tak, by NIE rzucało `IOException`

Jackson tylko **rzuca IOException, bo musi**, ale w praktyce `writeValueAsString` **rzuca ją bardzo rzadko**.

Możesz opakować wyjątek w środku metody:

```java
public static String toJson(Involvement involvement) {
    try {
        return mapper.writeValueAsString(involvement);
    } catch (IOException e) {
        throw new RuntimeException("JSON serialization failed", e);
    }
}
```

I teraz możesz swobodnie robić:
```java
.map(InvolvementJsonUtil::toJson)
```

---

#### ✅ Opcja 3: Użyć biblioteki, która obsługuje wyjątki w streamach

Np. [Vavr](https://www.vavr.io/) lub [FunctionalJava] – ale to już inna bajka i nie zawsze warto dodawać zależność tylko dla tego.

---

Chcesz, żebym Ci to pokazał na jakimś konkretnym przykładzie ze streamem lub kolekcją?

---

**User:**

Jaki jest powód tego że java nie pozwala w streamach rzucać checked exception?

---

**Assistant:**

Świetne pytanie — i w pełni zasadne. To nie jest kwestia tego, że **Java "nie pozwala"**, tylko bardziej: **interfejsy funkcyjne w `java.util.function` nie deklarują żadnych checked exceptions**.

---

## 💡 TL;DR:
> Java Streams nie wspierają `checked exceptions` w lambdach/metodach, bo interfejsy jak `Function`, `Consumer`, `Supplier` nie deklarują, że mogą je rzucać. A Java nie ma łatwego mechanizmu propagacji `checked exceptions` przez lambdy.

---

## 🔍 Szczegóły:

### 1. **Lambda to implementacja interfejsu funkcyjnego**
Na przykład:
```java
list.stream()
    .map(someMethod) // musi pasować do Function<T, R>
```

A `Function<T, R>` wygląda tak:
```java
@FunctionalInterface
public interface Function<T, R> {
    R apply(T t);
}
```

➡️ **Nie ma w nim `throws Exception`** — czyli lambda/method reference **nie może deklarować `throws IOException` ani innego checked exception**.

---

### 2. **Java nie pozwala "wrzucić" wyjątku do lambdy bez zadeklarowania go**
Gdyby `Function<T, R>` wyglądał tak:
```java
R apply(T t) throws Exception;
```

... to cały stream musiałby teraz też propagować `throws Exception`. To byłoby bardzo niewygodne i mało czytelne — a czasem wymagałoby przeładowania dziesiątek interfejsów funkcyjnych.

---

### 3. **JDK zachowało prostotę kosztem elastyczności**
Twórcy Javy **świadomie** uprościli ten obszar:
- Nie chcieli przeciążać każdej wersji interfejsu (`Function`, `BiFunction`, `Supplier`, itd.) wersjami z `throws`.
- W zamian zostawili to użytkownikom — możesz sam zrobić własne interfejsy funkcyjne, np. `ThrowingFunction<T, R, E extends Exception>`.

---

## 🛠 Jak to się zwykle obchodzi?

1. ✅ Owijanie w `try-catch` w lambdzie, jak pokazałem wcześniej.
2. ✅ Tworzenie własnych interfejsów funkcyjnych (np. `FunctionWithException<T, R>`).
3. ✅ Używanie bibliotek typu Vavr, które to obsługują.
4. ✅ Zamiana `checked` na `unchecked exception` (rzadsze, ale działa).

---

## 📌 Przykład własnego interfejsu:
```java
@FunctionalInterface
public interface ThrowingFunction<T, R> {
    R apply(T t) throws Exception;
}
```

I helper:
```java
public static <T, R> Function<T, R> wrap(ThrowingFunction<T, R> f) {
    return t -> {
        try {
            return f.apply(t);
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    };
}
```

Użycie:
```java
.map(wrap(InvolvementJsonUtil::toJson))
```

---

Jeśli chcesz, mogę Ci przygotować taką klasę `ThrowingFunction` z helperem gotową do wrzucenia do projektu.

---

**User:**

Zrób to

---

**Assistant:**

Pewnie! Oto gotowy zestaw klas, który pozwala Ci używać method references lub lambd rzucających checked exceptions (np. `IOException`) w streamach.

---

## ✅ 1. Interfejs `ThrowingFunction`

```java
@FunctionalInterface
public interface ThrowingFunction<T, R> {
    R apply(T t) throws Exception;
}
```

---

## ✅ 2. Klasa narzędziowa `FunctionUtils`

```java
import java.util.function.Function;

public class FunctionUtils {

    public static <T, R> Function<T, R> wrap(ThrowingFunction<T, R> throwingFunction) {
        return t -> {
            try {
                return throwingFunction.apply(t);
            } catch (Exception e) {
                throw new RuntimeException(e);
            }
        };
    }
}
```

---

## ✅ 3. Użycie w praktyce

Załóżmy, że masz metodę:

```java
public static String toJson(Involvement involvement) throws IOException {
    return mapper.writeValueAsString(involvement);
}
```

A teraz możesz użyć jej **bez `try-catch`** tak:

```java
List<Involvement> list = ...
List<String> jsonList = list.stream()
    .map(FunctionUtils.wrap(InvolvementJsonUtil::toJson))
    .collect(Collectors.toList());
```

---

## ✅ Bonus – własne wersje `Consumer`, `Supplier`, `Runnable` (jeśli potrzebujesz)

Jeśli chcesz, mogę rozszerzyć ten helper o:
- `ThrowingConsumer`
- `ThrowingSupplier`
- `ThrowingRunnable`
Z analogicznym mechanizmem `wrap`.

Chcesz taki zestaw do pełnej obsługi `checked exceptions` w stylu FP?

---

**User:**

Wracamy do poprzedniego tematu. Teraz ze stringu mam zrobić List of Involvement. Jak to zrobić, może tak mapper.readValue(invsJson, List.class)

---

**Assistant:**

Świetnie, że wracamy! I bardzo dobre pytanie — ale niestety `mapper.readValue(invsJson, List.class)` nie wystarczy, bo **Java straci informacje o typie generycznym (`Involvement`) w czasie działania**. W efekcie będziesz miał listę `LinkedHashMap` zamiast listy `Involvement`.

---

## ✅ Poprawny sposób: użycie `TypeReference`

Musisz użyć `new TypeReference<>()`, żeby zachować informację o typach generycznych:

```java
import com.fasterxml.jackson.core.type.TypeReference;

// ...

List<Involvement> involvementList = mapper.readValue(invsJson, new TypeReference<List<Involvement>>() {});
```

To wszystko — `ObjectMapper` wtedy wie, że ma sparsować **listę obiektów typu `Involvement`**, a nie tylko listę czegokolwiek (`List<?>`).

---

## 📦 Dla pełności: wersja w metodzie util

Możesz dodać to jako metodę do klasy `InvolvementJsonUtil`:

```java
public static List<Involvement> listFromJson(String json) {
    try {
        return mapper.readValue(json, new TypeReference<List<Involvement>>() {});
    } catch (IOException e) {
        throw new RuntimeException("Failed to parse JSON list", e);
    }
}
```

Użycie:
```java
List<Involvement> list = InvolvementJsonUtil.listFromJson(jsonString);
```

---

Jeśli chcesz też wersję `toJson(List<Involvement>)` — czyli odwrotną — też mogę ją dodać.