# Domyślna metoda equals

**Data:** 2025-06-25

---

**User:**

Java, jeśli na obiektach klas, które nie mają zaimplementowanej, bardziej przeładowanej metody equals wywoła się taką metodę equals, to jakiego rodzaju porównanie wtedy tych dwóch obiektów nastąpi?

---

**Assistant:**

W Javie, jeśli wywołasz metodę `equals` na obiektach klas, które **nie nadpisują** (`@Override`) metody `equals`, to zostanie użyta **domyślna implementacja** z klasy `Object`. 

### Co robi domyślna implementacja `equals` z klasy `Object`?

```java
public boolean equals(Object obj) {
    return (this == obj);
}
```

Czyli porównuje **referencje**, a nie zawartość obiektów. Innymi słowy:

- `a.equals(b)` będzie `true` **tylko wtedy**, gdy `a` i `b` wskazują na **ten sam obiekt** (ta sama referencja w pamięci).
- Jeśli `a` i `b` są różnymi instancjami (nawet jeśli zawierają identyczne dane), to `a.equals(b)` zwróci `false`.

### Przykład:

```java
class Person {
    String name;
    Person(String name) {
        this.name = name;
    }
}

public class Main {
    public static void main(String[] args) {
        Person p1 = new Person("Anna");
        Person p2 = new Person("Anna");

        System.out.println(p1 == p2);       // false - różne referencje
        System.out.println(p1.equals(p2));  // false - bo domyślnie ==, czyli referencje
    }
}
```

### Jeśli nadpiszesz `equals`, możesz porównywać zawartość:

```java
@Override
public boolean equals(Object o) {
    if (this == o) return true;
    if (o == null || getClass() != o.getClass()) return false;
    Person person = (Person) o;
    return Objects.equals(name, person.name);
}
```

Wtedy `p1.equals(p2)` zwróci `true`, jeśli `name` jest taki sam.

---

**Podsumowując:**  
Jeśli klasa **nie nadpisuje `equals`**, to `equals` działa jak `==`, czyli porównuje **adresy pamięci (referencje)**, nie zawartość.