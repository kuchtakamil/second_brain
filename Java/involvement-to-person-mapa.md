# Involvement to Person mapa

**Data:** 2025-05-30

---

**User:**

W Java Mam 
List<Involvement> inv i z tej listy chcę utworzyć mapę Involvement -> Person
Obiekt Person można pobrać z inv przy pomocy inv.getPerson()

---

**Assistant:**

Możesz łatwo przekształcić listę `List<Involvement>` do mapy `Map<Involvement, Person>` w Javie przy użyciu strumieni (Java 8+):

```java
Map<Involvement, Person> map = inv.stream()
    .collect(Collectors.toMap(
        Function.identity(),           // klucz: sam obiekt Involvement
        Involvement::getPerson         // wartość: wynik metody getPerson()
    ));
```

### Co robi ten kod:
- `inv.stream()` — tworzy strumień z listy `inv`.
- `Collectors.toMap(...)` — zbiera elementy do mapy.
  - `Function.identity()` — oznacza, że kluczem ma być dany obiekt `Involvement`.
  - `Involvement::getPerson` — wartość to wynik wywołania `getPerson()` na tym obiekcie.

### Uwaga:
Jeśli lista może zawierać duplikaty (czyli np. różne obiekty `Involvement` uważane za równe przez `equals`), a chcesz je obsłużyć, możesz dodać trzeci argument do `toMap`, np.:

```java
Collectors.toMap(
    Function.identity(),
    Involvement::getPerson,
    (existing, replacement) -> existing // albo replacement, zależnie od potrzeb
)
```

Daj znać, jeśli chcesz odwrotną mapę (`Person -> List<Involvement>`) albo coś bardziej customowego.

---

**User:**

ok a teraz chcę mieć mapę Involvement Id do Person Id

---

**Assistant:**

W takim razie chcesz stworzyć mapę `Long -> Long`, gdzie:

- klucz to `involvement.getId()`  
- wartość to `involvement.getPerson().getId()`

Możesz to zrobić tak:

```java
Map<Long, Long> map = inv.stream()
    .collect(Collectors.toMap(
        Involvement::getId,
        i -> i.getPerson().getId()
    ));
```

### Wyjaśnienie:
- `Involvement::getId` – klucz mapy, czyli ID obiektu `Involvement`
- `i -> i.getPerson().getId()` – wartość mapy, czyli ID powiązanego obiektu `Person`

Jeśli istnieje ryzyko, że któryś `getPerson()` może zwrócić `null`, warto zabezpieczyć się np. tak:

```java
Map<Long, Long> map = inv.stream()
    .filter(i -> i.getPerson() != null)
    .collect(Collectors.toMap(
        Involvement::getId,
        i -> i.getPerson().getId()
    ));
```

Daj znać, jeśli chcesz też coś zrobić z tymi ID później – np. filtrować, grupować itp.

---

**User:**

co gdy aby zdobyć id involvement trzeba zawołać inv.getDetails().getId()

---

**Assistant:**

W takim przypadku wystarczy zmienić sposób pobierania klucza w `toMap`. Załóżmy, że `getDetails()` zwraca obiekt, który ma metodę `getId()` (np. `Long`). Wtedy kod będzie wyglądał tak:

```java
Map<Long, Long> map = inv.stream()
    .filter(i -> i.getDetails() != null && i.getPerson() != null)
    .collect(Collectors.toMap(
        i -> i.getDetails().getId(),    // klucz: ID z details
        i -> i.getPerson().getId()      // wartość: ID osoby
    ));
```

### Wyjaśnienie zabezpieczeń:
- `.filter(i -> i.getDetails() != null && i.getPerson() != null)` – zapobiega `NullPointerException` w przypadku, gdy `getDetails()` lub `getPerson()` zwróci `null`.

Jeśli chcesz też zabezpieczyć się przed `null` w samym `getId()`, możesz dopisać dodatkowe warunki, np.:

```java
.filter(i -> i.getDetails() != null && i.getDetails().getId() != null &&
             i.getPerson() != null && i.getPerson().getId() != null)
```

Chcesz, żeby mapowanie ignorowało duplikaty, czy zgłaszało błąd w razie kolizji ID? Jeśli ignorować – można dodać trzeci argument:

```java
.collect(Collectors.toMap(
    i -> i.getDetails().getId(),
    i -> i.getPerson().getId(),
    (existing, replacement) -> existing // lub replacement
));
```