# String na Listę charów

**Data:** 2025-05-08

---

**User:**

java string - czy jest jakiś sposób aby ze string zrobić listę elementów typu char?

---

**Assistant:**

Tak, w Javie możesz bardzo łatwo przekształcić `String` na listę znaków (`List<Character>`), choć wymaga to lekkiej konwersji, ponieważ `String.toCharArray()` zwraca tablicę prymitywów `char[]`, a `List` operuje na obiektach (`Character`).

Oto kilka sposobów:

---

### 1. **Najprostszy i czytelny sposób (Java 8+)**
```java
String str = "hello";
List<Character> chars = str.chars()
                           .mapToObj(c -> (char) c)
                           .collect(Collectors.toList());
```

- `str.chars()` zwraca `IntStream`, więc trzeba go zamapować na `char` i dopiero wtedy kolekcjonować.

---

### 2. **Tradycyjny sposób z pętlą**
```java
String str = "hello";
List<Character> chars = new ArrayList<>();
for (char c : str.toCharArray()) {
    chars.add(c);
}
```

- Działa w każdej wersji Javy, ale jest nieco bardziej rozwlekły.

---

### 3. **Użycie streama ze `String.toCharArray()` (Java 8+)**
```java
String str = "hello";
List<Character> chars = IntStream.range(0, str.length())
                                 .mapToObj(str::charAt)
                                 .collect(Collectors.toList());
```

---

Wszystkie te sposoby dadzą Ci `List<Character>` zawierającą znaki ze stringa.

Czy chcesz od razu coś z tą listą zrobić – np. filtrować, sortować, itd.?

---

**User:**

str.split(" ") - jak to przerobić na listę?

---

**Assistant:**

Jeśli masz `String` i używasz `split(" ")`, to otrzymujesz tablicę `String[]`. Aby przerobić ją na `List<String>`, wystarczy użyć:

```java
String str = "Ala ma kota";
List<String> list = Arrays.asList(str.split(" "));
```

### Uwaga:
- `Arrays.asList(...)` zwraca listę *stałej długości*, więc nie można np. dodawać/usuwać z niej elementów.
- Jeśli chcesz mieć pełnoprawną, modyfikowalną listę, użyj:

```java
List<String> list = new ArrayList<>(Arrays.asList(str.split(" ")));
```

Chcesz też może splitować po dowolnej liczbie spacji lub innych separatorach?

---

**User:**

jak posortować taką. listę?

---

**Assistant:**

Aby posortować listę `List<String>` w Javie, masz kilka prostych opcji. Oto najczęstsze:

---

### 1. **Naturalne sortowanie alfabetyczne**
```java
List<String> list = new ArrayList<>(Arrays.asList("kot", "Ala", "pies"));
Collections.sort(list); // sortuje rosnąco, A-Z
```

---

### 2. **Z użyciem `List.sort()` (Java 8+)**
```java
list.sort(Comparator.naturalOrder());
```

---

### 3. **Sortowanie malejąco (Z–A)**
```java
list.sort(Comparator.reverseOrder());
```

---

### 4. **Sortowanie niestandardowe (np. po długości stringa)**
```java
list.sort(Comparator.comparingInt(String::length));
```

Albo malejąco po długości:
```java
list.sort(Comparator.comparingInt(String::length).reversed());
```

---

Jeśli chcesz, mogę też pokazać przykład sortowania z użyciem streamów. Chcesz?

---

**User:**

.toList() zwraca listę immutable, czy collect(Collectors.toList()) zwraca nie immutable?

---

**Assistant:**

Świetne pytanie — i bardzo ważne przy pracy z kolekcjami w Javie!

---

### 🔹 `List.of(...)` i `.toList()` z `Stream`a (Java 16+):
```java
List<String> list = List.of("a", "b", "c");
```

lub:

```java
List<String> list = Stream.of("a", "b", "c").toList(); // od Java 16
```

- **Zwracają listy niemodyfikowalne (immutable)**.
- Próba `add()`, `remove()` itd. rzuci `UnsupportedOperationException`.

---

### 🔹 `collect(Collectors.toList())`
```java
List<String> list = Stream.of("a", "b", "c")
                          .collect(Collectors.toList());
```

- **Zwraca modyfikowalną (`mutable`) listę.**
- Najczęściej jest to `ArrayList`.

---

### Podsumowanie:

| Sposób                                 | Mutable?     |
|---------------------------------------|--------------|
| `List.of(...)`                        | ❌ Immutable |
| `Stream.toList()` (Java 16+)         | ❌ Immutable |
| `Collectors.toList()`                | ✅ Mutable   |
| `new ArrayList<>(...)`               | ✅ Mutable   |

---

Chcesz może przykład pokazujący różnicę i wyjątek przy próbie modyfikacji?