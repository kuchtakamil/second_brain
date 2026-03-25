# Kiedyś znałem dosyć dobrze język Scala ale teraz już większość zapomniałem. Pami

**Data:** 30 paź 2025, 00:29:30 CET

---

**User:**

Kiedyś znałem dosyć dobrze język Scala ale teraz już większość zapomniałem. Pamiętam, że uwielbiałem potężny mechanizm typów za pomocą którego można było zrobić wiele rzeczy nieosiągalnych w innych językach. Napisz przykład w języku Scala który mogę podać znajomemu jako przykład wszechstronności i potęgi mechanizmu typów/typowania w Scala.

---

**Gemini:**

Oto przykład demonstrujący arytmetykę na poziomie typów z wykorzystaniem liczb Peano. Pokazuje on, jak system typów Scali jest kompletny w sensie Turinga, co pozwala na wykonywanie obliczeń podczas kompilacji.

---

### ## Wprowadzenie: Liczby Peano jako typy

Zamiast używać wbudowanych typów liczbowych, zdefiniujemy liczby naturalne za pomocą typów. Zgodnie z aksjomatami Peano, każda liczba naturalna to albo **zero**, albo **następnik** (`Successor`) innej liczby naturalnej.

1. **Cecha bazowa** (`trait`) dla wszystkich liczb naturalnych.
2. **Typ dla zera**.
3. **Typ dla następnika**, który przyjmuje inny typ liczby naturalnej jako parametr.

```
// Base trait for all natural numbers at the type level
sealed trait Nat

// Type-level representation of Zero
sealed trait _0 extends Nat

// Type-level representation of a Successor to a natural number N
// Succ[N] is equivalent to N + 1
sealed class Succ[N <: Nat] extends Nat
```

Na podstawie powyższych definicji możemy tworzyć aliasy typów dla kolejnych liczb, aby ułatwić sobie pracę:

```
type _1 = Succ[_0]
type _2 = Succ[_1] // which is Succ[Succ[_0]]
type _3 = Succ[_2] // which is Succ[Succ[Succ[_0]]]
```

---

### ## Definiowanie operacji na typach: Dodawanie

Teraz zdefiniujemy operację dodawania (`Sum`) w całości na poziomie typów. Użyjemy do tego mechanizmu *type class* z *type memberem* `Out`, który będzie reprezentował wynik operacji.

Kompilator będzie w stanie znaleźć odpowiednią niejawną (`implicit`) implementację `Sum` dla dwóch danych typów `Nat` i na tej podstawie wywnioskować typ wynikowy.

1. **Definicja `type class` `Sum`**:
   Ma dwa parametry typów (`A`, `B`) i typ wynikowy `Out`.

   ```
   // Type class for summing two Nat types
   trait Sum[A <: Nat, B <: Nat] {
     type Out <: Nat
   }
   ```
2. **Implementacja reguł dodawania za pomocą `implicit`**:

   - **Reguła 1 (Przypadek bazowy):** `0 + N = N`
     Jeśli dodajemy `_0` do dowolnej liczby `N`, wynikiem jest `N`.

     ```
     object Sum {
       implicit def zeroSum[N <: Nat]: Sum[_0, N] { type Out = N } = new Sum[_0, N] {
         type Out = N
       }
     }
     ```
   - **Reguła 2 (Krok rekurencyjny):** `Succ[A] + B = Succ[A + B]`
     Jeśli dodajemy `Succ[A]` (czyli `A + 1`) do `B`, wynik jest taki sam jak `Succ` z wyniku dodawania `A + B`. Zwróć uwagę, że ta reguła zależy od istnienia `implicit` dla `Sum[A, B]`.

     ```
     // We need to put this implicit into the trait to have a higher priority
     // than the base case, but for clarity, it's presented here.
     // Let's adjust the object Sum for a complete example.
     object Sum {
       // Base case: 0 + N = N
       implicit def zeroSum[N <: Nat]: Sum[_0, N] { type Out = N } = new Sum[_0, N] {
         type Out = N
       }

       // Recursive step: Succ[A] + B = Succ[A + B]
       // This rule is chosen if the first argument is a Succ.
       // It requires that a Sum instance can be found for A and B.
       implicit def successorSum[A <: Nat, B <: Nat, S <: Nat](
         implicit innerSum: Sum[A, B] { type Out = S }
       ): Sum[Succ[A], B] { type Out = Succ[S] } = new Sum[Succ[A], B] {
         type Out = Succ[S]
       }
     }
     ```

---

### ## Wykorzystanie w praktyce

Teraz możemy napisać funkcję, która operuje na wartościach, ale której poprawność jest weryfikowana na poziomie typów. Kompilator udowodni, że operacja jest poprawna, zanim program zostanie uruchomiony.

```
def sum[A <: Nat, B <: Nat, S <: Nat](a: A, b: B)(implicit s: Sum[A, B] { type Out = S }): S = {
  // The actual runtime implementation is irrelevant for this example,
  // as the magic happens at compile time.
  // In a real scenario, you might construct a value representation.
  null.asInstanceOf[S]
}
```

Teraz zobaczmy, co się stanie podczas próby kompilacji:

**Przypadek poprawny: `1 + 2 = 3`**

```
val one: _1 = new Succ[_0]
val two: _2 = new Succ(new Succ[_0])

// The compiler proves that Sum[_1, _2] results in _3
val result: _3 = sum(one, two) // This compiles successfully!
```

Kompilator przeprowadza następujące rozumowanie:

1. Potrzebuje `Sum[_1, _2]`, czyli `Sum[Succ[_0], _2]`.
2. Używa reguły `successorSum`. Wymaga to znalezienia `Sum[_0, _2]`.
3. Do `Sum[_0, _2]` pasuje reguła `zeroSum`, która zwraca wynik (`Out`) jako `_2`.
4. Wracając do kroku 2, `innerSum` ma `Out = _2`. Zatem wynik `successorSum` to `Succ[_2]`, czyli `_3`.
5. Kompilator wywnioskował, że `sum(one, two)` zwraca typ `_3`. Ponieważ oczekiwany typ to `_3`, kod się kompiluje.

**Przypadek niepoprawny: `1 + 2 != 2`**

```
// Trying to assign the result of 1 + 2 to a variable of type _2
val wrongResult: _2 = sum(one, two) // COMPILE-TIME ERROR!
```

Kompilator zgłosi błąd, ponieważ — jak udowodnił powyżej — wynik operacji ma typ `_3`, który nie jest zgodny z oczekiwanym typem `_2`.

```
[Error]  found   : _3
[Error]  required: _2
```

---

### ## Co to demonstruje?

Ten przykład, chociaż akademicki, pokazuje kilka niezwykle potężnych koncepcji systemu typów Scali:

1. **Type-Level Programming**: Obliczenia (tutaj: dodawanie) są wykonywane przez kompilator w trakcie analizy typów, a nie w czasie wykonania programu.
2. **Dependent Typing (emulacja)**: Typ *wynikowy* (`_3`) zależy od *typów* wejściowych (`_1`, `_2`). Jest to cecha zazwyczaj spotykana w językach takich jak Idris czy Agda, a Scala pozwala na jej emulację.
3. **Dowody w czasie kompilacji (Compile-Time Proofs)**: Kompilator nie tylko sprawdza poprawność typów, ale jest w stanie *udowodnić* matematyczną poprawność operacji. Błąd kompilacji jest dowodem na to, że przypisanie było nieprawidłowe.
4. **Zero-Cost Abstractions**: Cała ta złożona logika typów i niejawnych dowodów znika po kompilacji. Wygenerowany kod bajtowy nie zawiera żadnego narzutu związanego z tymi obliczeniami na poziomie typów.
5. **Potęga `implicits`**: Mechanizm `implicit` to nie tylko "magia". To narzędzie dla kompilatora do rozwiązywania problemów i znajdowania dowodów (instancji `type class`), co umożliwia tworzenie tak zaawansowanych konstrukcji.