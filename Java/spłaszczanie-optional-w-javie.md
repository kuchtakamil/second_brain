# Spłaszczanie Optional w Javie.

**Data:** 2023-06-13

---

**User:**

W java w jaki sposób mogę spłaszczyć Optional<Optional<Object>>

---

**Assistant:**

Aby spłaszczyć `Optional<Optional<Object>>` w języku Java, możesz skorzystać z metody `flatMap` dostępnej w klasie `Optional`. Metoda `flatMap` pozwala na mapowanie zawartości `Optional` i jednocześnie spłaszcza wynik do jednego `Optional`.

W przypadku `Optional<Optional<Object>>`, możesz zastosować `flatMap` dwa razy. Pierwsze wywołanie `flatMap` użyjemy do spłaszczenia zewnętrznego `Optional`, a drugie do spłaszczenia wewnętrznego `Optional`. Następnie możemy użyć `Optional<Object>` w celu uzyskania końcowego wyniku.

Oto przykład kodu ilustrujący ten proces:

```java
Optional<Optional<Object>> optionalOptional = ... ; // Twój Optional<Optional<Object>>

Optional<Object> flattenedOptional = optionalOptional.flatMap(Optional::stream) // Spłaszczenie zewnętrznego Optional
                                                   .flatMap(Optional::stream) // Spłaszczenie wewnętrznego Optional
                                                   .findFirst(); // Zwraca Optional<Object>

if (flattenedOptional.isPresent()) {
    Object result = flattenedOptional.get();
    // Wykonaj operacje na wyniku
} else {
    // Obsłuż przypadek, gdy wynik jest nieobecny
}
```

W powyższym kodzie `flatMap(Optional::stream)` używamy do spłaszczenia `Optional` do `Stream`, a następnie `findFirst()` do otrzymania końcowego `Optional<Object>`. Możesz dostosować operacje na wyniku do swoich potrzeb.

Pamiętaj, że `Optional<Optional<Object>>` jest często uważane za kod o złej praktyce, i warto unikać takiej konstrukcji. W przypadku, gdy masz kontrolę nad kodem, lepiej jest unikać umieszczania `Optional` wewnątrz `Optional`, jeśli to możliwe.

---

**User:**

Mam funkcję
public Optional<Sth> validate(Sth obj);

oraz listę
List<Sth> sths = createList()
Teraz chciałbym z
sths.stream().map(s -> validate(s))
uzyskać Optional<Sth>

---

**Assistant:**

Jeśli chcesz uzyskać `Optional<Sth>` poprzez mapowanie każdego elementu listy `sths` za pomocą funkcji `validate` i spłaszczenie wynikowych `Optional`, możesz zastosować metodę `flatMap` dwukrotnie.

Oto przykład kodu:

```java
List<Sth> sths = createList();
Optional<Sth> optionalSth = sths.stream()
        .map(this::validate)
        .flatMap(Function.identity())
        .findFirst();

if (optionalSth.isPresent()) {
    Sth result = optionalSth.get();
    // Wykonaj operacje na wyniku
} else {
    // Obsłuż przypadek, gdy wynik jest nieobecny
}
```

W tym kodzie, `map(this::validate)` mapuje każdy element listy `sths` za pomocą funkcji `validate`, co daje `Stream<Optional<Sth>>`. Następnie, `flatMap(Function.identity())` spłaszcza ten strumień `Optional` do jednego strumienia `Optional<Sth>`. Na koniec używamy `findFirst()`, aby uzyskać pierwszy wynik, jeśli istnieje.

Pamiętaj, że jeśli lista `sths` jest pusta lub żaden element nie przechodzi walidacji, wynikowy `Optional<Sth>` będzie pusty (nieobecny). Należy to uwzględnić i obsłużyć odpowiednio w kodzie.

---

**User:**

fragment .flatMap(Function.identity()) jest podświetlany przez kompilator

---

**Assistant:**

Przepraszam za zamieszanie. Wydaje się, że mój poprzedni fragment kodu jest niepoprawny. Musiałem popełnić błąd. 

Jeśli chcesz zastosować `flatMap` dla `Optional`, konieczne jest użycie metody `Optional.flatMap()` z odpowiednią funkcją, która zwraca `Optional`. Funkcja ta będzie odpowiedzialna za spłaszczenie `Optional<Optional<Sth>>` do `Optional<Sth>`. 

Oto poprawiony fragment kodu:

```java
List<Sth> sths = createList();
Optional<Sth> optionalSth = sths.stream()
        .map(this::validate)
        .flatMap(Optional::flatMap) // Spłaszczenie Optional<Optional<Sth>> do Optional<Sth>
        .findFirst();

if (optionalSth.isPresent()) {
    Sth result = optionalSth.get();
    // Wykonaj operacje na wyniku
} else {
    // Obsłuż przypadek, gdy wynik jest nieobecny
}
```

W tym kodzie, `.flatMap(Optional::flatMap)` jest wywoływane na strumieniu `Optional<Optional<Sth>>` i spłaszcza go do `Optional<Sth>`.

Przepraszam za zamieszanie i dziękuję za zwrócenie uwagi na ten błąd.

---

**User:**

Dalej coś jest nie tak. 

Próbuję zrobić tak
Optional<Sth> optionalSth = sths.stream()
        .flatMap(this::validate)
        .findFirst();
ale też nie działa. dlaczego?

---

**Assistant:**

Przepraszam za zamieszanie. Wyrażenie `.flatMap(this::validate)` nie będzie działać w tym przypadku, ponieważ metoda `flatMap()` oczekuje, że przekazana funkcja zwróci strumień, a nie `Optional`. 

Aby poprawnie zastosować `validate()` na każdym elemencie listy `sths` i uzyskać `Optional<Sth>` jako wynik, można użyć `.map()` zamiast `.flatMap()`. Następnie można zastosować `.filter(Optional::isPresent)` w celu usunięcia ewentualnych pustych `Optional` i na końcu wywołać `.map(Optional::get)` w celu pobrania wartości `Sth` z `Optional<Sth>`.

Oto poprawiona wersja kodu:

```java
List<Sth> sths = createList();
Optional<Sth> optionalSth = sths.stream()
        .map(this::validate)
        .filter(Optional::isPresent)
        .map(Optional::get)
        .findFirst();

if (optionalSth.isPresent()) {
    Sth result = optionalSth.get();
    // Wykonaj operacje na wyniku
} else {
    // Obsłuż przypadek, gdy wynik jest nieobecny
}
```

Teraz każdy element z listy `sths` jest mapowany za pomocą metody `validate()`, a następnie filtrowany przy użyciu `.filter(Optional::isPresent)`, aby pozbyć się ewentualnych pustych `Optional`. Następnie używamy `.map(Optional::get)`, aby pobrać wartość `Sth` z `Optional<Sth>`. Na koniec, `findFirst()` zwraca pierwsze wystąpienie, jeśli istnieje.

Przepraszam za zamieszanie wcześniej i mam nadzieję, że ta poprawiona wersja spełnia Twoje wymagania.