# Wykorzystanie operatorów IO.

**Data:** 2023-03-24

---

**User:**

W blibliotece Cats istnieje operator *> oraz >>. W przypadku >> wartość przekazywana jest by name. Jakie są praktyczne różnice w wykorzystaniu *> i >>. Podaj przykłady.

---

**Assistant:**

Operator `>>` i `*>` są często stosowane w bibliotece Cats, która jest biblioteką funkcyjną dla języka Scala, do operacji na monadach. 

Operator `>>` to operator sekwencjonowania, który pozwala na wykonanie dwóch operacji sekwencyjnie. Może być wykorzystywany z monadami, takimi jak `Option`, `Either`, `Try`, czy `Future`. Przykładowo, wyrażenie `a >> b` oznacza, że `a` zostanie wykonane, a następnie `b`, ale wynik `a` zostanie zignorowany. Można go wykorzystać do sekwencyjnego wykonywania kilku operacji, gdzie wynik nie jest potrzebny w kolejnych etapach.

Operator `*>` to operator sekwencjonowania, który działa podobnie do operatora `>>`, ale zwraca wynik drugiego argumentu. Przykładowo, wyrażenie `a *> b` oznacza, że `a` zostanie wykonane, a następnie `b`, ale wynik `a` zostanie zignorowany, a wynik `b` zostanie zwrócony. Można go wykorzystać, gdy chcemy zwrócić wynik drugiej operacji, ale wykonanie pierwszej jest konieczne.

Przykłady:

1. Wykorzystanie operatora `>>`:

```scala
import cats.implicits._

val maybeInt: Option[Int] = Some(10)
val maybeString: Option[String] = Some("test")

val result: Option[String] = maybeInt >> maybeString
// Wynik: Some("test")
```

W powyższym przykładzie, wynik `maybeInt` zostanie zignorowany, a `maybeString` zostanie zwrócone jako wynik.

2. Wykorzystanie operatora `*>`:

```scala
import cats.implicits._

val maybeInt: Option[Int] = Some(10)
val maybeString: Option[String] = Some("test")

val result: Option[String] = maybeInt *> maybeString
// Wynik: Some("test")
```

W powyższym przykładzie, wynik `maybeInt` zostanie zignorowany, ale `maybeString` zostanie zwrócone jako wynik. Różnica pomiędzy `>>` a `*>` polega na tym, że `>>` zwróciłby `Option[Unit]`, a `*>` zwraca `Option[String]`.