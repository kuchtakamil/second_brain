# Java: Pytania Rekrutacyjne (Senior)

Lista pytań na rozmowę kwalifikacyjną z zakresu **języka Java** na poziomie Senior. Pytania dotyczą wyłącznie samego języka i platformy — bez frameworków (Spring, Hibernate itp.). Pogrupowane tematycznie.

---

## 1. Model obiektowy i system typów

### 1. Czym jest kontrakt między `equals()` a `hashCode()`? Co się stanie, jeśli go złamiemy?

Kontrakt między `equals()` a `hashCode()` opiera się na dwóch głównych zasadach:
1. Jeśli dwa obiekty są równe według metody `equals(Object)`, to wywołanie metody `hashCode()` na każdym z nich **musi** zwrócić taką samą wartość całkowitą.
2. Jeśli dwa obiekty mają ten sam `hashCode()`, **nie muszą** być one równe według `equals()` (dochodzi wtedy do tzw. kolizji).

**Złamanie kontraktu:**
Jeśli nadpiszemy `equals()`, a zapomnimy o `hashCode()` (lub napiszemy go błędnie), aplikacja skompiluje się poprawnie, ale obiekty będą działać nieprzewidywalnie w kolekcjach bazujących na haszowaniu (takich jak `HashMap`, `HashSet`, `Hashtable`).
Na przykład, jeśli dodasz obiekt do `HashSet`, a następnie spróbujesz sprawdzić, czy tam jest (metodą `contains()`), `HashSet` może zwrócić `false`, mimo że obiekt logicznie taki sam istnieje w secie. Dzieje się tak, ponieważ `HashSet` najpierw szuka obiektu we właściwym koszyku (buckecie) na podstawie wartości `hashCode()`. Jeśli `hashCode` jest inny, szuka w złym miejscu i nawet nie wywołuje `equals()`.

---

### 2. Dlaczego `String` jest niemutowalny (immutable)? Jakie to ma konsekwencje dla bezpieczeństwa, wydajności i wielowątkowości?

Niemutowalność klasy `String` w Javie to kluczowa decyzja projektowa, polegająca na tym, że po utworzeniu obiektu `String` nie da się zmienić jego wartości (zawsze powstaje nowy obiekt).

**Konsekwencje:**
- **Bezpieczeństwo:** `String` jest często używany jako parametr do operacji krytycznych (np. ścieżki do plików, loginy, hasła, URL-e, hasła w połączeniach z bazą danych). Gdyby był mutowalny, kod wywołujący API mógłby zmienić wartość łańcucha znaków po tym, jak API zweryfikowało bezpieczeństwo operacji, co prowadziłoby do poważnych luk (Time-of-check to time-of-use - TOCTOU).
- **Wielowątkowość (Thread-safety):** Ponieważ stan obiektu `String` nigdy się nie zmienia po inicjalizacji, jest on automatycznie bezpieczny dla wątków (thread-safe). Można go bezpiecznie udostępniać i współdzielić między wieloma wątkami bez jakiejkolwiek synchronizacji.
- **Wydajność (String Pool):** Niemutowalność umożliwia istnienie mechanizmu String Pool (puli stringów). JVM może przechowywać w pamięci tylko jedną kopię danego literału znakowego i współdzielić ją, co znacząco oszczędza pamięć.
- **Hashowanie:** Ponieważ wartość `String` się nie zmienia, jego `hashCode` może być obliczony raz (i zbuforowany/zcacheowany). Sprawia to, że `String` jest niezwykle szybkim i idealnym kluczem w strukturach takich jak `HashMap`.

---

### 3. Czym różni się `String`, `StringBuilder` i `StringBuffer`? Kiedy użyjesz którego?

| Cecha | `String` | `StringBuilder` | `StringBuffer` |
|---|---|---|---|
| Mutowalność | Niemutowalny | Mutowalny | Mutowalny |
| Thread-safety | Tak (z racji niemutowalności) | Nie | Tak (metody synchronizowane) |
| Wydajność | Najwolniejszy przy licznych modyfikacjach | Najszybszy | Wolniejszy niż `StringBuilder` |

**Kiedy użyć:**
- **`String`:** Gdy wartość się nie zmienia lub modyfikacji jest bardzo mało (zwykłe użycie literałów).
- **`StringBuilder`:** Gdy budujesz lub modyfikujesz ciąg znaków w obrębie jednego wątku (np. wewnątrz metody lub pętli). Jest to najczęstszy wybór do składania stringów w kodzie, z powodu najwyższej wydajności.
- **`StringBuffer`:** Gdy musisz współdzielić bufor modyfikowanego łańcucha znaków pomiędzy wieloma wątkami. W praktyce bardzo rzadko stosowany w nowoczesnym kodzie.

---

### 4. Jak działa String Pool i jakie ma znaczenie dla porównywania stringów (`==` vs `equals()`)?

**String Pool (Pula Stringów)** to wydzielony obszar w stercie (Heap) pamięci JVM, służący do przechowywania literałów tekstowych. Kiedy w kodzie tworzymy literał np. `String s = "Hello";`, JVM sprawdza, czy "Hello" już istnieje w puli. Jeśli tak, zwraca do niego referencję. Jeśli nie, tworzy nowy obiekt w puli.

**Tworzenie przez operator `new`:**
Użycie `String s = new String("Hello");` omija (częściowo) ten mechanizm. Gwarantuje stworzenie **nowego** obiektu na stercie (poza pulą stringów), nawet jeśli "Hello" w puli już jest.

**Znaczenie dla porównywania:**
- `==` sprawdza tożsamość referencji (czy obie zmienne wskazują na ten sam obiekt w pamięci).
- `equals()` sprawdza logiczną wartość ciągu znaków.

```java
String s1 = "Java";
String s2 = "Java";
String s3 = new String("Java");

System.out.println(s1 == s2); // true - ta sama referencja z puli
System.out.println(s1 == s3); // false - s3 to inny obiekt na stercie
System.out.println(s1.equals(s3)); // true - wartości są te same
```
*Dobrą praktyką jest używanie `equals()` do porównywania wartości `String`.* Metoda `intern()` wywołana na obiekcie string dodaje go do puli (jeśli go nie było) i zwraca z niej referencję.

---

### 5. Czym są klasy `sealed` (Java 17) i jaki problem rozwiązują?

Klasy i interfejsy **sealed** (opieczętowane) dają kontrolę nad dziedziczeniem. Pozwalają autorowi klasy/interfejsu precyzyjnie określić, które inne klasy mają prawo z niej dziedziczyć (lub implementować).

Rozwiązuje to problem między pełnym otwarciem na dziedziczenie (zwykła klasa), a całkowitym zakazem dziedziczenia (klasa `final`).

**Składnia:**
```java
public abstract sealed class Shape permits Circle, Rectangle, Square { ... }

// Subklasy muszą być zadeklarowane jako final, non-sealed albo same być sealed.
public final class Circle extends Shape { ... }
public non-sealed class Square extends Shape { ... } // Pozwala na dalsze dziedziczenie
```

**Zastosowanie:**
Szczególnie przydatne w Domain-Driven Design (DDD) oraz pattern matchingu. Jeśli kompilator wie (dzięki `sealed`), że `Shape` może być tylko `Circle`, `Rectangle` lub `Square`, wyrażenie `switch` może być w pełni wyczerpujące bez konieczności dodawania bloku `default`.

---

### 6. Czym jest `record` (Java 16) i jakie są jego ograniczenia w porównaniu z klasycznym POJO?

**`record`** to nowy, zwięzły typ klasy, który służy jako transparentny nośnik niemutowalnych danych. Generuje automatycznie boilerplate code: konstruktor canonical (wymagający wszystkich argumentów), gettery (bez przedrostka `get`, np. `point.x()`), `equals()`, `hashCode()` i `toString()`.

```java
public record Point(int x, int y) { }
```

**Ograniczenia względem klasycznego POJO:**
- Klasa rekordu jest domyślnie (i musi pozostać) `final` — nie można z niej dziedziczyć, ani ona nie może dziedziczyć z innej klasy (choć może implementować interfejsy).
- Wszystkie pola stanu (deklarowane w nagłówku) są `private final`.
- Nie można dodawać innych niestatycznych pól instancyjnych poza tymi w nagłówku rekordu.

Mimo to rekordy wspierają niestandardowe walidacje (tzw. kompaktowe konstruktory), oraz mogą posiadać dodatkowe metody, a także metody statyczne.

---

### 7. Jakie są różnice między klasą abstrakcyjną a interfejsem? Kiedy wybrać jedno, a kiedy drugie?

Od Javy 8 (gdzie pojawiły się metody `default` w interfejsach) ta granica się zaciera, jednak fundamenty pozostają:

| Cecha | Interfejs | Klasa abstrakcyjna |
|---|---|---|
| Dziedziczenie | Klasa może implementować **wiele** interfejsów | Klasa może dziedziczyć tylko po **jednej** klasie |
| Stan obiektu (pola) | Pola są wyłącznie `public static final` (stałe). Brak możliwości posiadania zmiennych instancyjnych. | Może posiadać pola (np. `private`, `protected`) trzymające stan obiektu. |
| Konstruktor | Interfejsy **nie** mają konstruktorów. | Klasy abstrakcyjne mogą mieć konstruktory (wywoływane przez super()). |
| Widoczność metod | Tradycyjnie `public` (od Javy 9 można użyć `private` jako helperów dla default). | Pełen wachlarz widoczności: `public`, `protected`, `private`. |

**Kiedy użyć czego:**
- **Interfejs:** Gdy chcesz zdefiniować kontrakt lub pewną „zdolność” (np. `Comparable`, `Runnable`), którą mogą implementować całkowicie niespokrewnione klasy. Od tego powinieneś zaczynać projektowanie API.
- **Klasa abstrakcyjna:** Gdy masz powiązane klasy i chcesz wydzielić im silną wspólną tożsamość bazową, zawierającą **wspólny stan** lub wspólną logikę, korzystającą z tego stanu. Oraz gdy chcesz udostępnić wspólny kod nielokalnie przez metody `protected`.

---

### 8. Czym są metody domyślne (`default`) w interfejsach i jakie problemy mogą powodować (diamond problem)?

**Metody domyślne** (oznaczone słowem kluczowym `default`) zostały wprowadzone w Javie 8 po to, aby umożliwić rozszerzanie interfejsów o nowe metody bez psucia istniejących klas (wsteczna kompatybilność). Pozwalają na implementację logiki metody wewnątrz interfejsu.

```java
public interface Vehicle {
    void start();
    default void honk() {
        System.out.println("Beep!");
    }
}
```

**Problem diamentu (Diamond problem):**
Zjawisko to pojawia się, kiedy klasa implementuje dwa interfejsy, a oba dostarczają domyślną implementację metody o identycznej sygnaturze.

```java
interface A { default void hello() { System.out.println("A"); } }
interface B { default void hello() { System.out.println("B"); } }

class C implements A, B { } // Błąd kompilacji!
```
Kompilator Javy nie podejmuje decyzji sam, aby uniknąć niejednoznaczności. Zmusza programistę do nadpisania metody i zdefiniowania własnego zachowania (np. wywołania jednej z wersji przez `A.super.hello()`).

---

### 9. Jak działa wielodziedziczenie interfejsów z metodami domyślnymi? Jak Java rozwiązuje konflikty?

W Javie zasady rozwiązywania konfliktów z metodami `default` oparte są na "zasadzie najbardziej specyficznej implementacji" i trzech prostych regułach:
1. **Klasy wygrywają z interfejsami:** Jeśli metoda jest zdefiniowana w klasie (lub klasie nadrzędnej), zawsze nadpisuje implementacje `default` z jakiegokolwiek interfejsu.
2. **Bardziej wyspecjalizowany interfejs wygrywa:** Jeśli interfejs B dziedziczy po interfejsie A i oba dostarczają defaultową metodę o tej samej sygnaturze, metoda z interfejsu B zostanie użyta, bo jest "bliżej" (jest bardziej specyficzna).
3. **Zmuszenie do rozwiązania ręcznego:** Jeśli ani reguła 1, ani 2 nie ma zastosowania (klasa implementuje dwa interfejsy rodzeństwa A i B bez wspólnego potomka, z których każdy ma taką samą metodę `default`), kompilator zwróci błąd, wymagając wyraźnego przesłonięcia i rozwikłania, zwykle poprzez składnię `InterfaceName.super.methodName()`.

---

### 10. Czym jest pattern matching for `instanceof` (Java 16) i jak upraszcza kod?

Przed Javą 16, jeśli chcieliśmy sprawdzić typ obiektu i użyć go jako tego typu, musieliśmy dokonać jawnego rzutowania:
```java
if (obj instanceof String) {
    String s = (String) obj;
    System.out.println(s.length());
}
```

Pattern matching dla `instanceof` eliminuje ten nadmiarowy boilerplate, pozwalając zdefiniować i jednocześnie wyekstrahować zmienną wiążącą (binding variable):
```java
if (obj instanceof String s) {
    System.out.println(s.length());
}
```
Zmienna `s` jest w zasięgu od razu tam, gdzie test `instanceof` zwrócił `true` (tzw. flow typing). Obejmuje to nawet warunki logiczne: `if (obj instanceof String s && s.length() > 5)`. Zmienna `s` ma typ `String` z pominięciem jawnego rzutowania.

---

### 11. Czym jest `switch` z pattern matching (Java 21) i jakie nowe możliwości daje w porównaniu z klasycznym `switch`?

Java 21 ostatecznie ustabilizowała pattern matching dla operatora `switch`. Klasyczny `switch` potrafił działać tylko na wąskim zestawie typów: `int`, `String`, oraz `enum`.

Z nowym `switch` możemy operować na **każdym** typie obiektowym. Zamiast porównywać do konkretnej wartości, sprawdzamy dopasowanie do wzorców:
```java
String formatInfo(Object obj) {
    return switch (obj) {
        case Integer i -> String.format("int %d", i);
        case Long l    -> String.format("long %d", l);
        case String s  -> String.format("String of length %d", s.length());
        case null      -> "To jest null"; // Nowość: łapanie null w switchu!
        default        -> obj.toString();
    };
}
```

Daje to takie możliwości jak:
- Testowanie typów zmiennych w gałęziach `case`.
- Klauzule strażnicze (guard clauses) np. `case String s when s.length() > 5 -> ...`.
- Bezpieczniejsze, w pełni kontrolowane przez kompilator zachowanie, w połączeniu z klasami `sealed` i systemem typów zmuszającym do wyczerpującej (exhaustive) konstrukcji bez defaulta.

---

### 12. Czym są typy wyliczeniowe (`enum`) w Javie i czym różnią się od prostych stałych? Jakie zaawansowane zastosowania znasz?

W Javie `enum` nie jest prostą etykietą numeryczną jak w języku C. Jest to **pełnoprawna klasa** będąca częścią mechanizmu typu wyliczeniowego dostarczanego przez język. Przez to kompilator zapobiega przypisywaniu niewłaściwych wartości.

**Różnice względem np. statycznych pól String/int:**
- Type-safety (bezpieczeństwo typów).
- Posiada wbudowane metody `values()`, `name()`, `ordinal()`.
- Obiekty typu `enum` są singletonami w obrębie wirtualnej maszyny na wyliczenie (JVM to gwarantuje).
- Można go bezpiecznie i wydajnie serializować.

**Zaawansowane zastosowania:**
1. **Pola i konstruktory:** Enuma można potraktować jak klasę - możemy przypisywać poszczególnym wpisom unikalne wartości:
   ```java
   public enum Status {
       SUCCESS(200), ERROR(500);
       private int code;
       Status(int code) { this.code = code; }
   }
   ```
2. **Implementacja Singletonu:** Rekomendowany przez Joshuę Blocha sposób na singleton w Javie to użycie `enum`, bo jest z definicji serializable-safe oraz uniemożliwia wielokrotną inicjalizację poprzez refleksję: `public enum MySingleton { INSTANCE; }`.
3. **Implementacja wzorca Strategy:** Typ wyliczeniowy może implementować dany interfejs, a każda konkretna stała może zawierać unikalne zachowanie poprzez implementację metody abstrakcyjnej (często połączone z lambdami i konstruktorami enuma).

---

## 2. Generics

### 13. Czym jest type erasure i jakie ma konsekwencje w runtime?

**Type erasure** (wymazywanie typów) to mechanizm wprowadzony w Javie 5, który umożliwia stosowanie typów generycznych przy jednoczesnym zachowaniu wstecznej kompatybilności ze starszymi wersjami Javy. Kompilator Javy weryfikuje poprawność typów podczas kompilacji, a następnie **usuwa (wymazuje)** informacje o nich z wygenerowanego kodu bajtowego (bytecode).

**Jak działa:**
- Parametry typów niezwiązane (np. `<T>`) są zastępowane typem `Object`.
- Parametry typów ograniczone (np. `<T extends Number>`) są zastępowane ich ograniczeniem (tutaj: `Number`).
- Kompilator automatycznie wstawia rzutowania w miejscach, gdzie wyciągamy obiekty z generycznej kolekcji/klasy.

**Konsekwencje w runtime:**
- **Brak informacji o typie w runtime:** Maszyna wirtualna nie wie, z jakim typem generycznym utworzono instancję obiektu. `new ArrayList<String>()` oraz `new ArrayList<Integer>()` w trakcie działania programu to ta sama klasa: `ArrayList`.
- Nie można używać operatora `instanceof` z parametrami typów: `if (obj instanceof List<String>)` jest błędem kompilacji (zamiast tego używa się wildcard: `List<?>`).
- Nie można użyć typu parametru do łapania wyjątków `catch (T e)`.
- Metody o tej samej sygnaturze po wymazaniu typów (np. `void print(List<String> list)` oraz `void print(List<Integer> list)`) nie mogą istnieć obok siebie w jednej klasie (tzw. name clash).

---

### 14. Jaka jest różnica między `<? extends T>` a `<? super T>` (zasada PECS — Producer Extends, Consumer Super)?

Zasada **PECS** (Producer Extends, Consumer Super) pomaga zrozumieć kiedy stosować górne (extends) i dolne (super) ograniczenia dla typów wildcard (tzw. użycie wariancji):

- **`<? extends T>` (Covariance - Górne Ograniczenie):**
  - Akceptuje listę obiektów typu `T` lub **dowolnej klasy dziedziczącej** po `T`.
  - **Producer (Producent):** Używamy tego, gdy kolekcja *produkuje* dane do odczytu (czyli pobieramy elementy).
  - Gwarancja: na pewno odczytasz stamtąd co najmniej obiekt typu `T`.
  - Ograniczenie: **nie można dodawać elementów** do takiej kolekcji (z wyjątkiem wartości `null`), ponieważ kompilator nie potrafi określić bezpiecznego konkretnego podtypu kolekcji.
  
- **`<? super T>` (Contravariance - Dolne Ograniczenie):**
  - Akceptuje listę obiektów typu `T` lub **dowolnej nadklasy** typu `T` (aż do `Object`).
  - **Consumer (Konsument):** Używamy tego, gdy kolekcja ma *konsumować* (przyjmować/zapisać) dane.
  - Gwarancja: do tej kolekcji możemy zawsze bezpiecznie dodać obiekty typu `T` (oraz klas po nim dziedziczących).
  - Ograniczenie: przy odczycie typ zwracanych wartości to bezpiecznie jedynie `Object` (tracimy ścisłe typowanie przy wyciąganiu danych), ponieważ nie wiemy, jaki konkretnie jest to bazowy typ.

---

### 15. Czym są ograniczenia wielokrotne (bounded type parameters), np. `<T extends Comparable<T> & Serializable>`?

W Javie parametr typu można ograniczyć za pomocą więcej niż jednej klasy/interfejsu używając operatora `&` (intersection types). Pozwala to na nałożenie wielu wymagań na typ `T` jednocześnie.

**Zasady:**
- Klasa bazowa (jeśli jest wymagana) musi zawsze być na **pierwszym** miejscu przed znakiem `&`.
- Po pierwszej klasie mogą następować **tylko** interfejsy (dowolna ich liczba).
- Jeśli typ zostanie użyty w metodzie/klasie deklarującej to ograniczenie, kod kompiluje się z gwarancją, że dany typ ma dostęp do wszystkich metod reprezentowanych zarówno przez pierwszą klasę, jak i wszystkie wymienione interfejsy.

**Konsekwencja po wymazaniu (erasure):**
Podczas Type Erasure, kompilator zastępuje parametr `T` **najbardziej lewym** ograniczeniem. Dlatego kolejność deklaracji ma istotne znaczenie dla wydajności lub rozmiaru kodu (wstawiane castingi do pozostałych typów), stąd `Comparable` w powyższym przypadku zostanie typem wewnątrz wygenerowanego bytecode'u.

---

### 16. Dlaczego nie można tworzyć instancji typu generycznego (`new T()`) ani tablic generycznych (`new T[]`)?

Ograniczenie to bezpośrednio wynika ze zjawiska **Type Erasure**. 

1. **`new T()`:**
Maszyna Wirtualna Javy w trakcie działania programu potrzebuje znać dokładny typ obiektu, który instancjuje (potrzebuje wywołać dany konstruktor). Skoro parametr `T` w runtime zostaje wymazany np. do `Object`, wykonanie instrukcji `new T()` faktycznie oznaczałoby próbę zrobienia `new Object()`, a to całkowicie zrujnowałoby gwarancje typowania i cel pisania generycznego kodu. Ponadto `T` mogłoby nie posiadać konstruktora domyślnego. Obejście: należy przekazać obiekt `Class<T>` do metody (np. `clazz.getDeclaredConstructor().newInstance()`).

2. **`new T[]`:**
Tablice w Javie przechowują informacje o swoim typie w runtime (są ko-wariantne z natury - tzw. *reified* types). Oznacza to, że wiedzą jakiego typu elementami są i rzucą `ArrayStoreException`, jeśli spróbujesz wstawić nieprawidłowy obiekt. Tablica o typie generycznym `T[]` po wymazaniu byłaby po prostu tablicą `Object[]`. Ponieważ jednak runtime wymaga faktycznego, dokładnego typu tablicy do poprawnego weryfikowania operacji na jej pamięci, nie możemy utworzyć bezpiecznej tablicy typu `T`. Najlepiej zamiast tablic używać list generycznych (`List<T>`).

---

### 17. Czym jest raw type i dlaczego jego użycie jest niebezpieczne?

**Raw type** (typ surowy) to użycie generycznej klasy lub interfejsu (takiego jak `List` czy `HashMap`) bez określania jej parametrów typu (np. po prostu `List` zamiast `List<String>`).

Jest on pozostawiony w Javie **wyłącznie** dla celów kompatybilności wstecznej z kodem napisanym przed Javą 5, która nie posiadała obsługi typów generycznych.

**Dlaczego to niebezpieczne:**
1. **Utrata gwarancji typu w czasie kompilacji (Type-Safety):** Zmienna surowego typu pozwala na dodanie do niej obiektu absolutnie jakiejkolwiek klasy. Nie dostaniesz w zamian ostrzeżenia (błędu) podczas kompilacji.
```java
List rawList = new ArrayList();
rawList.add("String");
rawList.add(42); // Kompilator na to pozwala!
```
2. **Ryzyko w czasie wykonania (ClassCastException):** Kiedy później w kodzie będziemy próbowali np. założyć, że w kolekcji są `Stringi`, rzutowanie zakończy się błędem `ClassCastException` psując aplikację. Z generykami unikamy rzutowania ręcznego, a pomyłki wyłapywane są już na etapie kompilatora.
3. Wyłącza mechanizm generyków także w metodach tej klasy.

---

### 18. Jak działa wildcard capture i kiedy kompilator wymaga helper method?

**Wildcard capture** to proces, w którym kompilator wnioskuje specyficzny, chociaż anonimowy, typ pod widocznym symbolem `?` (wildcard). Kiedy przekazujesz argument `List<?>` do metody, kompilator wie, że to zbiór "jakiegoś" konkretnego typu, ale nie potrafi połączyć tego faktu między różnymi operacjami w obrębie metody.

**Przykład błędu kompilacji:**
```java
void reverse(List<?> list) {
    // błąd: nie można dodać Object do listy niewiadomego typu
    Object tmp = list.get(0); 
    list.set(0, list.get(1)); 
    list.set(1, tmp); 
}
```
Kompilator nie wie, że typ zwracany z `list.get()` to ten sam typ, co przyjmowany przez `list.set()`. 

**Helper method:**
Kompilator wymaga, byś napisał sparametryzowaną (z named typem `T`) metodę pomocniczą (często ukrytą z modyfikatorem `private`). Przez nazwanie tego `T` na wywołaniu z `<?>`, kompilator "łapie" ("captures") typ do zmiennej.
```java
void reverse(List<?> list) { reverseHelper(list); }

// Helper method pozwala powiązać zmienną T
private <T> void reverseHelper(List<T> list) {
    T tmp = list.get(0);
    list.set(0, list.get(1));
    list.set(1, tmp);
}
```

---

### 19. Czym jest recursive type bound (np. `<T extends Comparable<T>>`) i gdzie go spotykamy?

**Rekursywne ograniczenie typu** to technika deklarowania parametrów typu, gdzie ograniczenie odnosi się do samego deklarowanego parametru.

Przykład: `<T extends Comparable<T>>`
Zapis ten oznacza: "Typ `T` musi być typem klasy, która może być porównywalna sama z sobą (lub z swoimi własnymi instancjami)".
Dzięki temu kompilator Javy wie, że na pewno obiekt klasy typu `T` przekazany jako argument do metody `compareTo` będzie oczekiwał innego obiektu dokładnie tego samego typu `T` (unikamy w ten sposób niebezpiecznego porównywania Jabłka do Pomarańczy).

**Gdzie go spotykamy:**
Najczęściej występuje przy metodach i operacjach sortujących (np. w standardowej bibliotece API np. `Collections.max()`, `Collections.sort()`). Widać to bardzo silnie we wzorcach projektowych używających fluent interfaces (tzw. `Builder` w strukturze dziedziczenia hierarchicznego), np:
```java
public abstract class AbstractBuilder<B extends AbstractBuilder<B>> {
    public B withValue(String val) {
        // ... logic ...
        return (B) this; 
    }
}
```
Dzięki temu po zbudowaniu podklasy, zwrócona wartość nie będzie traciła typu docelowego i będziemy mogli łańcuchować metody dalej.

---

### 20. Jak typy generyczne wpływają na mostkowanie metod (bridge methods) w bytecode?

Pojawienie się tzw. **Bridge Methods (Metod mostkujących)** w wygenerowanym kodzie bytecode to zjawisko, które kompilator wprowadza, by chronić zasady **polimorfizmu i nadpisywania** w obliczu działania **Type Erasure**.

Załóżmy, że mamy generyczny interfejs i klaskę konkretną:
```java
public interface Node<T> {
    void setData(T data);
}

public class MyNode implements Node<Integer> {
    public void setData(Integer data) { ... }
}
```

Po kompilacji (Type Erasure) interfejs `Node` będzie wyglądał tak: `void setData(Object data);`. Natomiast nasza podklasa ma metodę `void setData(Integer data);`.
Wygenerowana metoda w podklasie fizycznie **nie przesłania** metody w interfejsie (ponieważ `Object` vs `Integer` to różne sygnatury metod z punktu widzenia JVM). Rozbija to mechanizm polimorfizmu Javy.

Dlatego w klasie `MyNode` kompilator automatycznie dopisuje, potajemnie ukrytą tzw. **bridge method**:
```java
// Zobaczysz to jedynie przez analizę kodu bytecode (lub zrzut jclasslib)
public void setData(Object data) { // To jest wygenerowana metoda mostkowa
    setData((Integer) data); // Rzutowanie i wywołanie prawdziwej metody
}
```
Metoda mostkująca ma identyczną zamazaną (erased) sygnaturę jak ta z klasy bazowej, a jej jedynym celem jest bezpieczne zrzutowanie argumentu na silnie-typowany parametr w metodzie właściwej, po czym delegacja wywołania, chroniąc w ten sposób dziedziczenie wewnątrz JVM.

---

## 3. Kolekcje i struktury danych

21. Opisz hierarchię interfejsów kolekcji w Javie (`Collection`, `List`, `Set`, `Queue`, `Deque`, `Map`).
22. Jak działa wewnętrznie `HashMap`? Opisz mechanizm haszowania, buckety, tree-ification (Java 8+) i rehashing.
23. Czym różni się `HashMap` od `LinkedHashMap`, `TreeMap` i `ConcurrentHashMap`?
24. Jak zaimplementowany jest `HashSet` pod spodem?
25. Jakie są różnice między `ArrayList` a `LinkedList`? Kiedy `LinkedList` faktycznie ma przewagę?
26. Czym jest `ArrayDeque` i dlaczego jest preferowany nad `Stack` i `LinkedList` jako kolejka/stos?
27. Jakie są różnice między `Comparable` a `Comparator`? Kiedy użyjesz którego?
28. Czym jest fail-fast iterator a czym fail-safe (weakly consistent)? Podaj przykłady kolekcji.
29. Czym jest `EnumSet` i `EnumMap` i jakie mają optymalizacje w porównaniu z ogólnymi implementacjami?
30. Jak działa `PriorityQueue`? Na jakiej strukturze danych jest oparta?
31. Czym jest `Collections.unmodifiableList()` vs `List.of()` vs `List.copyOf()`? Jakie są różnice w gwarancjach niemodyfikowalności?
32. Jak działa `IdentityHashMap` i kiedy jest przydatna?

---

## 4. Wielowątkowość i współbieżność

33. Czym jest Java Memory Model (JMM) i co gwarantuje relacja **happens-before**?
34. Czym jest `volatile` i jakie gwarancje daje? Czego **nie** gwarantuje?
35. Czym jest `synchronized` — na poziomie metody i bloku? Jak działa monitor obiektu?
36. Jakie są różnice między `ReentrantLock` a `synchronized`? Kiedy warto użyć `ReentrantLock`?
37. Czym jest deadlock, livelock i starvation? Jak im zapobiegać?
38. Opisz framework `Executor` / `ExecutorService` / `ThreadPoolExecutor`. Jak dobrać wielkość puli wątków?
39. Czym jest `CompletableFuture` i jakie operacje oferuje (thenApply, thenCompose, allOf, anyOf, exceptionally)?
40. Czym są klasy z pakietu `java.util.concurrent.atomic` (np. `AtomicInteger`, `AtomicReference`)? Na czym opiera się ich działanie (CAS)?
41. Czym jest `CountDownLatch`, `CyclicBarrier`, `Semaphore` i `Phaser`? Opisz różnice i zastosowania.
42. Czym jest `ReadWriteLock` i `StampedLock`? Kiedy stosować optymistyczne czytanie?
43. Czym są kolekcje współbieżne (`ConcurrentHashMap`, `CopyOnWriteArrayList`, `BlockingQueue`) i czym różnią się od synchronizowanych wrapperów?
44. Jak działa `ForkJoinPool` i algorytm **work-stealing**?
45. Czym są wirtualne wątki (virtual threads) w Java 21 (Project Loom)? Jak zmieniają model współbieżności?
46. Czym jest `ThreadLocal` i jakie problemy może powodować (memory leaks, zwłaszcza w kontekście puli wątków)?
47. Czym jest problem **false sharing** i jak go unikać?

---

## 5. Strumienie (Streams) i programowanie funkcyjne

48. Czym jest `Stream` API i czym różni się strumień od kolekcji?
49. Jakie są różnice między operacjami pośrednimi (intermediate) a terminalnymi (terminal)?
50. Czym jest lazy evaluation w kontekście strumieni? Jak wpływa na wydajność?
51. Czym jest `Optional` i jakie są dobre praktyki jego stosowania? Kiedy **nie** należy go używać?
52. Jakie są różnice między `map()`, `flatMap()` i `peek()` w strumieniach?
53. Jak działają `Collector`y? Czym jest `Collectors.groupingBy()`, `partitioningBy()`, `toMap()`, `reducing()`?
54. Jak napisać własny kolektor (`Collector.of()`)? Jakie wymagania musi spełniać?
55. Czym jest `Stream.parallel()` i kiedy naprawdę daje korzyść wydajnościową? Jakie są ryzyka?
56. Jakie są różnice między `reduce()` a `collect()` w strumieniach?
57. Czym jest interfejs funkcyjny (`@FunctionalInterface`)? Jakie podstawowe interfejsy funkcyjne dostarcza Java (`Function`, `Predicate`, `Consumer`, `Supplier`, `BiFunction`, `UnaryOperator`)?
58. Jak działają referencje do metod (method references) i jakie są ich rodzaje?
59. Czym jest effectively final i dlaczego lambdy wymagają tego od zmiennych lokalnych?

---

## 6. JVM, pamięć i Garbage Collection

60. Opisz model pamięci JVM: heap, stack, metaspace (wcześniej PermGen), code cache.
61. Jak działa Garbage Collector w Javie? Opisz podejście generacyjne (Young Generation, Old Generation).
62. Jakie są główne algorytmy GC w nowoczesnej Javie (G1, ZGC, Shenandoah)? Czym się różnią?
63. Czym jest Stop-The-World (STW) pause i jak nowoczesne GC ją minimalizują?
64. Jakie są rodzaje referencji w Javie (`Strong`, `Weak`, `Soft`, `Phantom`)? Kiedy używać których?
65. Czym jest memory leak w Javie i jakie są typowe przyczyny mimo istnienia GC?
66. Jak zdiagnozować wyciek pamięci (heap dump, MAT, jmap, jcmd)?
67. Czym jest `OutOfMemoryError` i jakie są jego warianty (heap space, metaspace, GC overhead, native)?
68. Jak działają flagi JVM do strojenia pamięci (`-Xms`, `-Xmx`, `-XX:MaxMetaspaceSize`, `-XX:+UseG1GC`)?
69. Czym jest JIT (Just-In-Time) compilation? Czym różni się C1 od C2 compilera? Co to jest tiered compilation?
70. Jak działa class loading w Javie? Opisz hierarchię class loaderów i delegację.
71. Czym jest GraalVM i kompilacja Ahead-of-Time (AOT)? Jakie daje korzyści i ograniczenia?

---

## 7. Wyjątki i obsługa błędów

72. Czym są checked exceptions i unchecked exceptions? Jaka jest hierarchia wyjątków w Javie?
73. Dlaczego checked exceptions są kontrowersyjne? Jakie są argumenty za i przeciw?
74. Czym jest `try-with-resources` i interfejs `AutoCloseable`? Jak działa suppressed exception?
75. Jakie są dobre praktyki obsługi wyjątków (kiedy łapać, kiedy propagować, kiedy opakowywać)?
76. Czym jest `Error` vs `Exception`? Kiedy (jeśli w ogóle) łapiemy `Error`?
77. Jaki jest koszt rzucania wyjątków w Javie? Czym jest `fillInStackTrace()` i kiedy warto go nadpisać?

---

## 8. Moduły i system modułów (JPMS)

78. Czym jest Java Platform Module System (JPMS, Project Jigsaw)? Jaki problem rozwiązuje?
79. Czym jest `module-info.java` i jakie dyrektywy zawiera (`requires`, `exports`, `opens`, `uses`, `provides`)?
80. Czym różni się `exports` od `opens`? Jak to wpływa na refleksję?
81. Jakie są konsekwencje modularyzacji dla bibliotek korzystających z refleksji i internal API (`sun.misc.Unsafe`)?
82. Czym jest classpath vs module path? Jak działa unnamed module i automatic module?

---

## 9. Refleksja, adnotacje i metaprogramowanie

83. Czym jest refleksja w Javie i jakie są jej zastosowania? Jakie niesie ryzyka (wydajność, bezpieczeństwo)?
84. Jak działa `java.lang.reflect.Proxy` (dynamic proxy)? Do czego służy i jakie ma ograniczenia?
85. Czym są adnotacje? Jak stworzyć własną adnotację i przetworzyć ją w runtime (`RetentionPolicy.RUNTIME`)?
86. Czym jest annotation processing (`javax.annotation.processing`) i jak działa w compile-time?
87. Czym jest `MethodHandle` i `VarHandle`? Jak się mają do refleksji i jakie dają korzyści?
88. Czym jest `invokedynamic` i jak jest wykorzystywane wewnętrznie (np. przez lambdy, konkatenację stringów)?

---

## 10. I/O, NIO i serializacja

89. Czym różni się klasyczne I/O (`java.io`) od NIO (`java.nio`)? Czym jest non-blocking I/O?
90. Jak działają `Channel`, `Buffer` i `Selector` w NIO?
91. Czym jest `Path` i `Files` API (NIO.2)? Jakie operacje oferuje w porównaniu ze starym `File`?
92. Czym jest serializacja w Javie (`Serializable`)? Jakie ma problemy i ryzyka bezpieczeństwa?
93. Dlaczego wbudowana serializacja Javy jest odradzana? Jakie są alternatywy?
94. Czym jest `transient` i `serialVersionUID`? Co się stanie, jeśli zmienimy klasę, a nie zaktualizujemy `serialVersionUID`?

---

## 11. Zarządzanie datą i czasem (java.time)

95. Czym różni się `LocalDateTime` od `ZonedDateTime` i `OffsetDateTime`? Kiedy używać którego?
96. Czym jest `Instant` i jak reprezentuje czas w Javie?
97. Dlaczego stare API (`java.util.Date`, `Calendar`) jest problematyczne i jak migrować na `java.time`?
98. Jak działa `Duration` vs `Period`? Czym się różnią?
99. Jakie są pułapki w pracy ze strefami czasowymi i czasem letnim (DST)?

---

## 12. Nowości w Javie (Java 11–21+)

100. Czym jest `var` (local variable type inference) w Java 10? Jakie są ograniczenia i dobre praktyki?
101. Jakie nowe metody pojawiły się w API `String` w nowszych wersjach Javy (np. `isBlank()`, `strip()`, `lines()`, `repeat()`, `indent()`)?
102. Czym są text blocks (Java 15) i jak działają?
103. Czym są `switch` expressions (Java 14)? Jak działają z `yield`?
104. Czym jest `Stream.toList()` (Java 16) i czym różni się od `Collectors.toList()`?
105. Czym są sequenced collections (Java 21)? Jakie interfejsy dodają (`SequencedCollection`, `SequencedSet`, `SequencedMap`)?
106. Czym jest scoped values (preview) i jak ma zastąpić `ThreadLocal` w kontekście wirtualnych wątków?
107. Czym jest structured concurrency (preview) i jaki problem rozwiązuje?

---

## 13. Dobre praktyki i wzorce projektowe

108. Czym jest zasada niemodyfikowalności (immutability) i jak tworzyć obiekty niemutowalne w Javie?
109. Jak poprawnie zaimplementować wzorzec Singleton w Javie (enum singleton, double-checked locking, holder class)?
110. Czym jest wzorzec Builder i kiedy go stosować? Porównaj implementację ręczną z Lombok `@Builder`.
111. Czym jest wzorzec Strategy implementowany za pomocą interfejsów funkcyjnych?
112. Jak poprawnie zaimplementować `clone()` vs copy constructor vs static factory method?
113. Czym jest defensive copying i kiedy jest konieczne?
114. Jak działa kontrakt `Comparable` i kiedy własna implementacja może być niebezpieczna?
115. Czym jest NullPointerException i jakie strategie stosować, aby go unikać (Optional, @Nullable, fail-fast)?

---

## Powiązane materiały

- [Pytania Rekrutacyjne — Spring 3.0](pytania-rekrutacyjne-spring-3-0.md)
- [Mikroserwisy: Pytania Rekrutacyjne](../SystemDesign/mikroserwisy-pytania-rekrutacyjne.md)
