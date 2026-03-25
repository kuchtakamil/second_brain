# Użycie Lombok @Builder

**Data:** 2024-12-02

---

**User:**

Żeby używając Lombok użyć adnotacji @Builder jakich innych adnotacji jeszcze trzeba lub powinno się użyć?

---

**Assistant:**

Aby skutecznie używać adnotacji **@Builder** w Lombok, możesz rozważyć użycie dodatkowych adnotacji, w zależności od potrzeb Twojego projektu. Poniżej znajdziesz listę adnotacji, które mogą być przydatne:

### 1. **@Builder** w podstawowym zastosowaniu
Jeśli używasz tylko **@Builder**, Lombok wygeneruje builder oraz konstruktor dla wszystkich pól w Twojej klasie. Minimalny przykład wygląda tak:

```java
import lombok.Builder;

@Builder
public class Person {
    private String name;
    private int age;
}
```

### 2. **@AllArgsConstructor** / **@NoArgsConstructor**
Jeśli chcesz mieć również inne konstruktory, możesz użyć:
- **@AllArgsConstructor** - generuje konstruktor z wszystkimi polami.
- **@NoArgsConstructor** - generuje konstruktor bez argumentów (przydatne, np. do serializacji).

Przykład:
```java
import lombok.Builder;
import lombok.AllArgsConstructor;
import lombok.NoArgsConstructor;

@Builder
@AllArgsConstructor
@NoArgsConstructor
public class Person {
    private String name;
    private int age;
}
```

### 3. **@Getter** / **@Setter**
Jeśli chcesz mieć dostęp do pól klasy (np. w sposób niezmienny lub umożliwiający zmianę wartości), możesz użyć **@Getter** i **@Setter**:

```java
import lombok.Builder;
import lombok.Getter;

@Builder
@Getter
public class Person {
    private String name;
    private int age;
}
```

### 4. **@ToString**
Jeśli chcesz, aby Twoja klasa miała zdefiniowaną metodę `toString`, możesz użyć **@ToString**. Lombok automatycznie wygeneruje reprezentację tekstową dla wszystkich pól.

```java
import lombok.Builder;
import lombok.ToString;

@Builder
@ToString
public class Person {
    private String name;
    private int age;
}
```

### 5. **@EqualsAndHashCode**
Jeśli chcesz, aby Twoja klasa implementowała sensowne metody `equals` i `hashCode`, użyj **@EqualsAndHashCode**:

```java
import lombok.Builder;
import lombok.EqualsAndHashCode;

@Builder
@EqualsAndHashCode
public class Person {
    private String name;
    private int age;
}
```

### 6. **@Value** (dla klas niezmiennych)
Jeśli Twoja klasa ma być niezmienna (immutable), możesz użyć **@Value**, która automatycznie włącza **@Builder**. W tym przypadku wszystkie pola będą finalne, a klasa będzie niemutowalna:

```java
import lombok.Value;

@Value
@Builder
public class Person {
    String name;
    int age;
}
```

### Podsumowanie
Minimalne wymaganie to sama adnotacja **@Builder**, ale w praktyce często łączy się ją z:
- **@AllArgsConstructor** (lub innymi konstruktorami),
- **@Getter**, **@Setter**,
- **@ToString**, **@EqualsAndHashCode**,
- **@Value** (dla niezmiennych klas).

Wybór zależy od potrzeb Twojego projektu i tego, jakie funkcjonalności chcesz zautomatyzować za pomocą Lomboka.

---

**User:**

Co robi adnotacja Data?

---

**Assistant:**

Adnotacja **`@Data`** w Lombok to kompleksowa adnotacja, która automatycznie generuje zestaw standardowych metod dla klasy. Dzięki niej możesz szybko stworzyć klasę danych z minimalnym kodem.

### Funkcje generowane przez `@Data`
1. **Gettery dla wszystkich pól**  
   Generuje metody `getX()` dla każdego pola w klasie.

2. **Settery dla wszystkich pól**  
   Generuje metody `setX()` dla każdego pola (chyba że pole jest oznaczone jako `final`).

3. **`toString()`**
   Generuje metodę `toString()`, która zwraca tekstową reprezentację obiektu, zawierającą wartości wszystkich pól.

4. **`equals()` i `hashCode()`**
   Generuje metody `equals()` i `hashCode()`, które porównują obiekty na podstawie wartości ich pól.

5. **Konstruktor z wszystkimi polami wymaganymi**  
   Generuje konstruktor z argumentami dla wszystkich pól `final` (lub wszystkich, jeśli klasa nie ma pól `final`).

### Minimalny przykład użycia `@Data`
```java
import lombok.Data;

@Data
public class Person {
    private String name;
    private int age;
}
```

### Co zostanie wygenerowane?
Lombok wygeneruje następujący kod:

```java
public class Person {
    private String name;
    private int age;

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getAge() {
        return age;
    }

    public void setAge(int age) {
        this.age = age;
    }

    @Override
    public String toString() {
        return "Person(name=" + this.name + ", age=" + this.age + ")";
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Person person = (Person) o;
        return age == person.age && Objects.equals(name, person.name);
    }

    @Override
    public int hashCode() {
        return Objects.hash(name, age);
    }
}
```

### Główne zastosowania `@Data`
- Użycie w klasach, które reprezentują dane (np. DTO, modele, encje).
- Gdy chcesz szybko wygenerować standardowe metody dla klasy i nie musisz kontrolować ich szczegółów.

### Ograniczenia i uwagi
1. **Nie dla dużych klas:**  
   Jeśli masz bardzo wiele pól, metody takie jak `toString()` mogą być nieefektywne lub trudne do odczytania.

2. **Bezpieczeństwo:**  
   Automatyczne generowanie setterów dla wszystkich pól może prowadzić do problemów z mutowalnością. Jeśli klasa powinna być niemutowalna, rozważ użycie **`@Value`** zamiast **`@Data`**.

3. **Kontrola nad metodami:**  
   Jeśli potrzebujesz specyficznej logiki w getterach/setterach, musisz ręcznie napisać te metody, ponieważ Lombok ich wtedy nie wygeneruje.

Adnotacja **`@Data`** jest szybkim i wygodnym rozwiązaniem, ale zawsze warto dokładnie przemyśleć, czy jej użycie jest odpowiednie w danym kontekście.