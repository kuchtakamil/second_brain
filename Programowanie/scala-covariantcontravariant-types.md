# Scala Covariant/Contravariant Types.

**Data:** 2023-03-03

---

**User:**

Wytłumacz pojęcia Covariant i Contravariant w języku Scala.

---

**Assistant:**



Covariant i Contravariant są pojęciami związanymi z dziedziczeniem typów w języku Scala.

Covariant oznacza, że dany typ A jest podtypem typu B, jeśli B jest supertypem A. W języku Scala oznacza to, że deklaracja typu A musi zawierać operator "+" przed typem, a deklaracja typu B musi zawierać operator "+", ale nie może zawierać operatora "-". Przykład:

```scala
class A[+T]
class B
class C extends B

val a: A[B] = new A[C] // poprawne, ponieważ A jest covariant
```

W powyższym przykładzie, klasa A jest covariant, ponieważ posiada operator "+". Z tego powodu, deklaracja `val a: A[B]` może wskazywać na instancję typu A[C], ponieważ C jest podtypem B.

Contravariant oznacza, że dany typ A jest podtypem typu B, jeśli B jest podtypem A. W języku Scala oznacza to, że deklaracja typu A musi zawierać operator "-", a deklaracja typu B musi zawierać operator "-", ale nie może zawierać operatora "+". Przykład:

```scala
class A[-T]
class B
class C extends B

val a: A[C] = new A[B] // poprawne, ponieważ A jest contravariant
```

W powyższym przykładzie, klasa A jest contravariant, ponieważ posiada operator "-". Z tego powodu, deklaracja `val a: A[C]` może wskazywać na instancję typu A[B], ponieważ B jest podtypem C.

Podsumowując, covariant i contravariant to dwa pojęcia związane z dziedziczeniem typów w języku Scala. Covariant oznacza, że typ można traktować jako bardziej szczegółowy, a contravariant jako bardziej ogólny.