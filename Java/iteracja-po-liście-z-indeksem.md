# Iteracja po liście z indeksem

**Data:** 2025-05-03

---

**User:**

W java iteruję po np. liście. Czy mogę w for mieć dostęp również do indexu?

---

**Assistant:**

Tak, w Javie masz kilka sposobów, żeby iterować po liście z dostępem do indeksu:

### 1. Klasyczna pętla `for` z indeksem
Najprostszy i najbardziej bezpośredni sposób:

```java
List<String> lista = List.of("A", "B", "C");

for (int i = 0; i < lista.size(); i++) {
    String element = lista.get(i);
    System.out.println("Index: " + i + ", Element: " + element);
}
```

### 2. Strumień z `IntStream`
Jeśli wolisz styl funkcyjny:

```java
import java.util.stream.IntStream;

List<String> lista = List.of("A", "B", "C");

IntStream.range(0, lista.size())
         .forEach(i -> System.out.println("Index: " + i + ", Element: " + lista.get(i)));
```

### 3. `ListIterator` (mniej popularne do tego celu)
Daje dostęp do indeksu, ale rzadziej używany do prostych iteracji:

```java
List<String> lista = List.of("A", "B", "C");
ListIterator<String> iterator = lista.listIterator();

while (iterator.hasNext()) {
    int index = iterator.nextIndex();
    String element = iterator.next();
    System.out.println("Index: " + index + ", Element: " + element);
}
```

Czy chcesz też przykład z użyciem `for-each`, ale z ręcznym liczeniem indeksu?

---

**User:**

a w 
for (String elem : lista)
nie da się tego zrobić?

---

**Assistant:**

W pętli `for (String elem : lista)` — czyli tzw. "enhanced for loop" — **nie masz bezpośredniego dostępu do indeksu**. Jest to celowy zabieg w Javie: ta składnia została zaprojektowana, by uprościć iterację, gdy indeks nie jest potrzebny.

### Jeśli mimo to chcesz indeks, masz 2 opcje:

#### 1. Licznik zewnętrzny (niezgrabne, ale działa):

```java
int index = 0;
for (String elem : lista) {
    System.out.println("Index: " + index + ", Element: " + elem);
    index++;
}
```

#### 2. Przesiadka na klasycznego `for` lub `IntStream`, jak wcześniej wspomniano:

```java
for (int i = 0; i < lista.size(); i++) {
    System.out.println("Index: " + i + ", Element: " + lista.get(i));
}
```

`for-each` to dobry wybór, gdy **nie interesuje Cię indeks** i chcesz tylko przejść po elementach. Jeśli potrzebujesz indeksu — wybierz inne podejście.

Chcesz, żebym pokazał analogiczne rozwiązanie np. dla `Map`?