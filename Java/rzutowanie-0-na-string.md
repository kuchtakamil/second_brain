# Rzutowanie 0 na String

**Data:** 2025-06-26

---

**User:**

Java, czy rzutowanie 0 na stringa rzuci wyjątek?

---

**Assistant:**

W Javie **rzutowanie liczby `0` na `String`** w sposób bezpośredni, jak np.:

```java
String s = (String) 0;
```

**rzuci wyjątek czasu wykonania (runtime exception)** — konkretnie będzie to:

```
java.lang.ClassCastException: java.lang.Integer cannot be cast to java.lang.String
```

### Dlaczego?

- `0` jest literaleem typu `int` → zostanie automatycznie opakowany w `Integer`.
- Próbujesz rzutować `Integer` na `String` → a te typy nie są względem siebie zgodne (nie ma między nimi dziedziczenia ani implementacji interfejsu).
- To nie jest konwersja, tylko rzutowanie — czyli wymuszenie na obiekcie, by był traktowany jako inny typ,

---

**User:**

Pytałem o NUL.

---

**Assistant:**

Dziękuję za doprecyzowanie — chodziło Ci o rzutowanie **`null`** na `String` w Javie, a nie o liczbę `0`.

### Odpowiedź:
```java
String s = (String) null;
```
**Nie rzuci wyjątku.**

To przypisanie jest poprawne i zakończy się tym, że zmienna `s` po prostu będzie miała wartość `null`.

### Wyjaśnienie:
- `null` jest domyślną wartością referencyjną — można ją przypisać do każdej zmiennej typu obiektowego.
- Rzutowanie `null` na dowolny typ referencyjny (np. `String`, `List`, `Object`, `MyClass`) jest dozwolone, ponieważ `null` nie ma konkretnego typu, ale jest kompatybilny ze wszystkimi typami referencyjnymi.

### Przykład:
```java
public class Test {
    public static void main(String[] args) {
        String s = (String) null;
        System.out.println(s); // wypisze: null
    }
}
```

Nie ma żadnego wyjątku — dopiero próba **wywołania metody** na tym `s` zakończy się `NullPointerException`.