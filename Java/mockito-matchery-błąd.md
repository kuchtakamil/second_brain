# Mockito matchery błąd

**Data:** 2025-05-06

---

**User:**

dostawałem błąd 
Invalid use of argument matchers!
3 matchers expected, 2 recorded:
-> at 
-> at 

This exception may occur if matchers are combined with raw values:
    //incorrect:
    someMethod(anyObject(), "raw String");
When using matchers, all arguments have to be provided by matchers.
For example:
    //correct:
    someMethod(anyObject(), eq("String by matcher"));

w sytuacji miałem
verify(operations, never()).checks(anyString(), Optional.empty());

---

**Assistant:**

Ten błąd jest typowy dla Mockito i oznacza, że **używasz mieszanki matcherów (`anyString()`) i surowych wartości (`Optional.empty()`) w jednym wywołaniu**, co Mockito traktuje jako nieprawidłowe.

Dokładnie, w tym wierszu:

```java
verify(operations, never()).checks(anyString(), Optional.empty());
```

- `anyString()` to matcher,
- `Optional.empty()` to surowa wartość.

Mockito **wymaga**, aby **wszystkie argumenty były matcherami**, jeśli używasz chociaż jednego matchera.

### ✅ Poprawna wersja:
Użyj `eq(...)` do opakowania surowej wartości:

```java
verify(operations, never()).checks(anyString(), eq(Optional.empty()));
```

Matcher `eq(...)` mówi Mockito, że ta konkretna wartość powinna być porównywana jako matcher.

---

Chcesz, żebym sprawdził inne przypadki w Twoim teście pod tym kątem?