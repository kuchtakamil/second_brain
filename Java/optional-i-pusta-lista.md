# Optional i pusta lista

**Data:** 2025-03-14

---

**User:**

Optional<String> actionOpt = Optional.ofNullable(params.get(ACTION)).map(p -> p.get(0));
Jeśli params.get(ACTION) zwraca listę lub null to czy to jest ok?

---

**Assistant:**

Tak, ten kod jest jak najbardziej poprawny – zakładając, że `params` to np. `Map<String, List<String>>`, to linijka:

```java
Optional<String> actionOpt = Optional.ofNullable(params.get(ACTION)).map(p -> p.get(0));
```

robi dokładnie to, co prawdopodobnie chcesz osiągnąć:

- `params.get(ACTION)` może zwrócić `null` albo `List<String>`.
- `Optional.ofNullable(...)` sprawi, że jeśli `params.get(ACTION)` zwróci `null`, to `actionOpt` będzie po prostu `Optional.empty()`.
- Jeśli natomiast zwróci listę, to `.map(p -> p.get(0))` wyciąga pierwszy element tej listy i zawija go w `Optional`.

### Potencjalna pułapka:
Jeśli `params.get(ACTION)` zwróci pustą listę (`Collections.emptyList()`), to `p.get(0)` rzuci `IndexOutOfBoundsException`.

Jeśli chcesz tego uniknąć (czyli jeśli chcesz, żeby również pustą listę traktować jako `Optional.empty()`), to bezpieczniejsza wersja wyglądałaby tak:

```java
Optional<String> actionOpt = Optional.ofNullable(params.get(ACTION))
    .filter(list -> !list.isEmpty())
    .map(list -> list.get(0));
```

Wtedy:
- `null` → `Optional.empty()`
- `[]` → `Optional.empty()`
- `[someValue, ...]` → `Optional.of(someValue)`

Chcesz, żebym podpowiedział jeszcze jakąś bardziej czytelną wersję lub może z użyciem streamów?