# Zliczanie słów w kodzie

**Data:** 2023-09-12

---

**User:**

Uzupełnij ______

****** Result for Image/Page 1 ******
class WordCounter {	
ConcurrentHashMap<String, LongAdder> wordToCounter = new	
ConcurrentHashMap<>();	
void add(String word) {	
wordToCounter. ______(word, key -> new	
LongAdder ()).increment ();
}}

---

**Assistant:**

Oto uzupełnienie brakującej części kodu:

```java
wordToCounter.computeIfAbsent(word, key -> new LongAdder()).increment();
```

Powyższy kod używa metody `computeIfAbsent` z klasy `ConcurrentHashMap`, aby dodać nowy rekord do mapy, jeśli klucz `word` nie istnieje, lub zaktualizować istniejący rekord, inkrementując go o 1, jeśli klucz już istnieje. W ten sposób możesz zliczać wystąpienia różnych słów w mapie `wordToCounter`.

---

**User:**

private static final Zoneld GMT_ZONE = ZoneId.of ("'GMT");
public ZonedDateTime convertToZonedDateTime(LocalDateTime
localDateTime) {
return ZonedDateTime.____(localDateTime, GMT_ZONE);
}

---

**Assistant:**

Aby uzupełnić brakującą część kodu, użyj metody `of` z klasy `ZonedDateTime`. Oto poprawiony kod:

```java
return ZonedDateTime.of(localDateTime, GMT_ZONE);
```

W powyższym kodzie `ZonedDateTime.of()` jest używane do przekształcenia obiektu `LocalDateTime` na `ZonedDateTime` przy użyciu strefy czasowej `GMT_ZONE`.

---

**User:**

Map<String, Boolean> userTypeToEditPermission() {
return Stream.of(UserType._______)
._____(_____(Enum::name, UserType::hasEditPermission));
}
enum UserType {
ADMIN(true), MODERATOR(true), DEVELOPER(false);


private final boolean editPermission;
UserType(boolean editPermission) {
this.editPermission = editPermission;
}
public boolean hasEditPermission() {
return editPermission;
}
}

---

**Assistant:**

Aby uzupełnić brakujące części kodu, użyj metod strumieni Java Stream w celu utworzenia mapy `userTypeToEditPermission`. Oto poprawiony kod:

```java
import java.util.Map;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public Map<String, Boolean> userTypeToEditPermission() {
    return Stream.of(UserType.values())
            .collect(Collectors.toMap(Enum::name, UserType::hasEditPermission));
}

enum UserType {
    ADMIN(true), MODERATOR(true), DEVELOPER(false);

    private final boolean editPermission;

    UserType(boolean editPermission) {
        this.editPermission = editPermission;
    }

    public boolean hasEditPermission() {
        return editPermission;
    }
}
```

W powyższym kodzie `Stream.of(UserType.values())` tworzy strumień z wszystkimi wartościami enumeracji `UserType`, a następnie `Collectors.toMap()` zbiera te wartości do mapy, używając nazwy enum jako klucza i metody `hasEditPermission()` jako wartości boolean.

---

**User:**

class PrintingRunnable implements Runnable {
ThreadLocal<Double> value = new _________<>();
@Override
public void run() {
value.set(Math.random());
System.out.println(value.get());
Thread childThread = new Thread(() ->
System.out.println(value.get()));
childThread.start();
}
}

---

**Assistant:**

Aby uzupełnić brakującą część kodu, użyj konstruktora klasy `ThreadLocal`. Oto poprawiony kod:

```java
class PrintingRunnable implements Runnable {
    ThreadLocal<Double> value = ThreadLocal.withInitial(() -> 0.0);

    @Override
    public void run() {
        value.set(Math.random());
        System.out.println(value.get());
        Thread childThread = new Thread(() -> System.out.println(value.get()));
        childThread.start();
    }
}
```

W powyższym kodzie używamy `ThreadLocal.withInitial(() -> 0.0)` do zainicjowania `ThreadLocal` z początkową wartością 0.0. Dzięki temu każdy wątek będzie miał swoją kopię zmiennej `value`, zainicjowaną wartością 0.0.

---

**User:**

ma być z new 
ThreadLocal<Double> value = new _________<>();

---

**Assistant:**

Jeśli chcesz utworzyć nowy obiekt `ThreadLocal` z użyciem konstruktora, możesz to zrobić tak:

```java
ThreadLocal<Double> value = new ThreadLocal<>();
```

W powyższym kodzie tworzymy nowy obiekt `ThreadLocal` typu `Double` za pomocą konstruktora domyślnego. Pamiętaj jednak, że początkowa wartość w tym przypadku będzie `null`, więc będziesz musiał ją ustawić później w kodzie.

---

**User:**

As an employee at the local grocery shop, you want to find out which products have a lower than average price. Please complete the query to return the correct dataset:
SELECT * FROM products
WHERE price ________(SELECT AVG(price) FROM products);

---

**Assistant:**

To zapytanie SQL ma na celu znalezienie produktów, których cena jest niższa niż średnia cena wszystkich produktów. Aby uzupełnić brakującą część zapytania, użyj operatora `<`. Oto poprawne zapytanie:

```sql
SELECT * FROM products
WHERE price < (SELECT AVG(price) FROM products);
```

W powyższym zapytaniu `<` porównuje cenę każdego produktu z wynikiem podzapytania, które oblicza średnią cenę (`AVG(price)`) wszystkich produktów. Produkty, których cena jest niższa niż średnia cena, zostaną zwrócone jako wynik zapytania.

---

**User:**

podaj więcej przykładów użycia computeIfAbsent

---

**Assistant:**

`computeIfAbsent` to przydatna metoda w Javie, która pozwala na bezpieczne dodawanie wartości do mapy, jeśli klucz nie istnieje, lub aktualizowanie wartości, jeśli klucz już istnieje. Oto kilka przykładów użycia `computeIfAbsent`:

1. Dodawanie wartości do mapy, jeśli klucz nie istnieje:

```java
Map<String, Integer> map = new HashMap<>();
map.computeIfAbsent("key1", key -> 42);
```

Jeśli klucz "key1" nie istnieje w mapie, zostanie dodany z wartością 42.

2. Aktualizowanie wartości w mapie, jeśli klucz już istnieje:

```java
Map<String, List<String>> map = new HashMap<>();
map.computeIfAbsent("fruits", key -> new ArrayList<>()).add("apple");
map.computeIfAbsent("fruits", key -> new ArrayList<>()).add("banana");
```

W tym przypadku najpierw tworzymy pustą listę dla klucza "fruits", a następnie dodajemy do niej "apple" i "banana". Ponieważ klucz "fruits" istnieje już w mapie, metoda `computeIfAbsent` nie tworzy nowej listy, ale aktualizuje istniejącą.

3. Zastosowanie `computeIfAbsent` z mapą zawierającą obiekty z niestandardowymi typami:

```java
Map<String, Set<Integer>> map = new HashMap<>();
map.computeIfAbsent("even", key -> new HashSet<>()).add(2);
map.computeIfAbsent("even", key -> new HashSet<>()).add(4);
map.computeIfAbsent("odd", key -> new HashSet<>()).add(3);
```

W tym przykładzie tworzymy mapę, która zawiera zestawy liczb całkowitych. Metoda `computeIfAbsent` jest używana do dodawania liczb do odpowiednich zestawów na podstawie klucza. Jeśli zestaw nie istnieje, zostanie utworzony.

`computeIfAbsent` jest przydatną metodą do manipulowania mapami, zwłaszcza gdy chcesz uniknąć problemów związanych z NullPointerException, gdy próbujesz dodać lub aktualizować wartości w mapie.

---

**User:**

przykłady computeIfPresent

---

**Assistant:**

`computeIfPresent` to metoda, która pozwala na aktualizację wartości w mapie tylko wtedy, gdy klucz już istnieje w mapie. Oto kilka przykładów użycia `computeIfPresent`:

1. Aktualizowanie wartości w mapie na podstawie klucza:

```java
Map<String, Integer> map = new HashMap<>();
map.put("key1", 42);
map.computeIfPresent("key1", (key, value) -> value + 1);
```

W tym przykładzie, jeśli klucz "key1" istnieje w mapie, jego wartość zostanie zaktualizowana o 1.

2. Usuwanie wartości z mapy na podstawie klucza, jeśli wartość spełnia warunek:

```java
Map<String, Integer> map = new HashMap<>();
map.put("key1", 42);
map.computeIfPresent("key1", (key, value) -> {
    if (value > 40) {
        return null; // Usunięcie wartości z mapy
    } else {
        return value; // Pozostawienie wartości bez zmian
    }
});
```

W tym przypadku, jeśli wartość klucza "key1" jest większa niż 40, zostanie ona usunięta z mapy.

3. Aktualizacja wartości w mapie przy użyciu obliczeń na podstawie aktualnej wartości:

```java
Map<String, Double> prices = new HashMap<>();
prices.put("apple", 1.0);
prices.computeIfPresent("apple", (key, currentValue) -> currentValue * 1.1);
```

W tym przykładzie wartość klucza "apple" zostanie pomnożona przez 1.1, co jest przykładem aktualizacji wartości w mapie na podstawie jej aktualnej wartości.

`computeIfPresent` jest używane, gdy chcemy dokonać zmiany w mapie tylko w przypadku, gdy klucz już istnieje. Jeśli klucz nie istnieje, metoda `computeIfPresent` nie wprowadza żadnych zmian w mapie.