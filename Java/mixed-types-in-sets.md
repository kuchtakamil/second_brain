# Mixed Types in Sets

**Data:** 2024-04-05

---

**User:**

        SortedSet<Object> s = new TreeSet<>();
        s.add("a");
        s.add("b");
        s.add("m");
        s.add("c");
        s.add(1L);

Why the last line causes exception

---

**Assistant:**

The last line `s.add(1L);` causes an exception because you're trying to add an element of a different type (`Long`) to a `SortedSet<Object>` which already contains `String` elements. 

In a `SortedSet`, the elements must be mutually comparable, meaning they must implement the `Comparable` interface or you must provide a `Comparator` during set creation. 

When you try to add a `Long` after adding `String` elements, it violates the contract of a `SortedSet` because `String` and `Long` are not mutually comparable. 

In this case, you can't mix different types in the same `SortedSet` unless they have a common superclass or if you provide a custom `Comparator` that can handle the comparison between `String` and `Long` objects.

---

**User:**

SortedSet<Object> s = new TreeSet<>();
TreeSet is a SortedSet?

---

**Assistant:**

Yes, `TreeSet` is indeed a type of `SortedSet`. In Java, `TreeSet` implements the `SortedSet` interface. 

The `SortedSet` interface extends the `Set` interface and provides a total ordering on its elements. This ordering can be either the natural ordering (if the elements implement the `Comparable` interface) or a custom ordering provided by a `Comparator`.

`TreeSet` specifically is an implementation of `SortedSet` that uses a Red-Black tree structure to maintain the elements in sorted order. This allows for efficient retrieval and insertion operations.

---

**User:**

Jaki jest ich najbliższy wspólny przodek?

---

**Assistant:**

Najbliższym wspólnym przodkiem `SortedSet` i `TreeSet` jest interfejs `Set`. Oba `SortedSet` i `TreeSet` są typami zbiorów, gdzie `TreeSet` jest konkretną implementacją `SortedSet`, która zapewnia zbiorowi uporządkowanie. Natomiast `SortedSet` jest interfejsem, który rozszerza `Set` o dodatkowe funkcje związane z zachowaniem uporządkowania elementów w zbiorze.