# Type-Safe Equals in Scala

**Data:** 2023-03-05

---

**User:**

In Scala language
  object EqualsTask {
    // TODO Design a typesafe equals so I can do a === b, but it won't compile if a and b are of different types
    // Define the typeclass (think of a method signature)
    // Keep in mind that `a method b` is `a.method(b)`
  }

---

**Assistant:**



In order to design a type-safe equals method in Scala that uses a typeclass to ensure that two objects are of the same type, you can define a trait with a type parameter and an associated method that performs the equality check. Here is an example implementation:

```
trait TypeEquals[A] {
  def typeEquals(a: A, b: A): Boolean
}
```

This trait takes a type parameter `A` and defines a method `typeEquals` that takes two objects of type `A` and returns a Boolean indicating whether they are equal. Now we can define an implicit instance of this trait for any type `A`:

```
object TypeEquals {
  implicit def typeEqualsInstance[A]: TypeEquals[A] = new TypeEquals[A] {
    def typeEquals(a: A, b: A): Boolean = a == b
  }
}
```

This implicit instance simply checks whether the two objects are equal using the `==` operator. Now we can define a new infix operator `===` that takes two objects of the same type `A` and uses the `typeEquals` method to check their equality:

```
object EqualsTask {
  import TypeEquals._
  implicit class TypeSafeEquals[A](a: A) {
    def ===(b: A)(implicit ev: TypeEquals[A]): Boolean = ev.typeEquals(a, b)
  }
}
```

This code defines an implicit class `TypeSafeEquals` that takes an object `a` of type `A` and defines a new infix operator `===` that takes another object `b` of type `A`. The `===` operator requires an implicit instance of the `TypeEquals` trait for type `A`, which ensures that the two objects are of the same type. Finally, the `===` operator calls the `typeEquals` method on the implicit instance to perform the equality check.

With this implementation, you can use the `===` operator to safely compare two objects of the same type:

```
val x: Int = 1
val y: Int = 2
val z: String = "hello"

x === y // true
x === z // compilation error: Cannot prove that TypeEquals[Int] <:< TypeEquals[String]
```

---

**User:**

  object Foldable {

    trait Semigroup[A] {
      def combine(x: A, y: A): A
    }

    trait Monoid[A] extends Semigroup[A] {
      def empty: A
    }

    trait Foldable[F[_]] {
      def foldLeft[A, B](as: F[A])(z: B)(f: (B, A) => B): B
      def foldRight[A, B](as: F[A])(z: B)(f: (A, B) => B): B
      def foldMap[A, B](as: F[A])(f: A => B)(implicit monoid: Monoid[B]): B
    }

    implicit val optionFoldable: Foldable[Option] = ??? // TODO Implement Foldable instance for Option

    implicit val listFoldable: Foldable[List] = ??? // TODO Implement Foldable instance for List

    sealed trait Tree[A]
    object Tree {
      final case class Leaf[A](value: A) extends Tree[A]
      final case class Branch[A](left: Tree[A], right: Tree[A]) extends Tree[A]
    }

    implicit val treeFoldable: Foldable[Tree] = ??? // TODO Implement Foldable instance for Tree
  }

---

**Assistant:**

To implement the `Foldable` typeclass for `Option`, `List`, and `Tree` in Scala, you can define implicit instances of the `Foldable` trait for each type, and implement the three required methods `foldLeft`, `foldRight`, and `foldMap`. Here's how you can implement this:

```
object Foldable {

  trait Semigroup[A] {
    def combine(x: A, y: A): A
  }

  trait Monoid[A] extends Semigroup[A] {
    def empty: A
  }

  trait Foldable[F[_]] {
    def foldLeft[A, B](as: F[A])(z: B)(f: (B, A) => B): B
    def foldRight[A, B](as: F[A])(z: B)(f: (A, B) => B): B
    def foldMap[A, B](as: F[A])(f: A => B)(implicit monoid: Monoid[B]): B
  }

  implicit val optionFoldable: Foldable[Option] = new Foldable[Option] {
    def foldLeft[A, B](as: Option[A])(z: B)(f: (B, A) => B): B =
      as match {
        case Some(a) => f(z, a)
        case None => z
      }

    def foldRight[A, B](as: Option[A])(z: B)(f: (A, B) => B): B =
      as match {
        case Some(a) => f(a, z)
        case None => z
      }

    def foldMap[A, B](as: Option[A])(f: A => B)(implicit monoid: Monoid[B]): B =
      as match {
        case Some(a) => f(a)
        case None => monoid.empty
      }
  }

  implicit val listFoldable: Foldable[List] = new Foldable[List] {
    def foldLeft[A, B](as: List[A])(z: B)(f: (B, A) => B): B =
      as.foldLeft(z)(f)

    def foldRight[A, B](as: List[A])(z: B)(f: (A, B) => B): B =
      as.foldRight(z)(f)

    def foldMap[A, B](as: List[A])(f: A => B)(implicit monoid: Monoid[B]): B =
      as.foldLeft(monoid.empty)((acc, a) => monoid.combine(acc, f(a)))
  }

  implicit val treeFoldable: Foldable[Tree] = new Foldable[Tree] {
    def foldLeft[A, B](as: Tree[A])(z: B)(f: (B, A) => B): B =
      as match {
        case Leaf(a) => f(z, a)
        case Branch(left, right) =>
          val z1 = foldLeft(left)(z)(f)
          foldLeft(right)(z1)(f)
      }

    def foldRight[A, B](as: Tree[A])(z: B)(f: (A, B) => B): B =
      as match {
        case Leaf(a) => f(a, z)
        case Branch(left, right) =>
          val z1 = foldRight(right)(z)(f)
          foldRight(left)(z1)(f)
      }

    def foldMap[A, B](as: Tree[A])(f: A => B)(implicit monoid: Monoid[B]): B =
      as match {
        case Leaf(a) => f(a)
        case Branch(left, right) =>
          val l = foldMap(left)(f)


---

**User:**

  object ApplicativeTask {

    trait Semigroupal[F[_]] {
      def product[A, B](fa: F[A], fb: F[B]): F[(A, B)]
    }

    trait Functor[F[_]] {
      def map[A, B](fa: F[A])(f: A => B): F[B]
    }

    trait Apply[F[_]] extends Functor[F] with Semigroupal[F] {

      def ap[A, B](fab: F[A => B])(fa: F[A]): F[B] // "ap" here stands for "apply" but it's better to avoid using it

      override def product[A, B](fa: F[A], fb: F[B]): F[(A, B)] = ??? // TODO Implement using `ap` and `map`

      def map2[A, B, Z](fa: F[A], fb: F[B])(f: (A, B) => Z): F[Z] = ??? // TODO Implement using `map` and `product`
    }

    trait Applicative[F[_]] extends Apply[F] {
      def pure[A](a: A): F[A]
    }

    // TODO Implement Applicative instantce for Option
    implicit val optionApplicative: Applicative[Option] = ??? // Keep in mind that Option has flatMap

    // TODO Implement traverse using `map2`
    def traverse[F[_]: Applicative, A, B](as: List[A])(f: A => F[B]): F[List[B]] = ???

    // TODO Implement sequence (ideally using already defined things)
    def sequence[F[_]: Applicative, A](fas: List[F[A]]): F[List[A]] = ???
  }

---

**Assistant:**

Here's one possible implementation for the missing parts in `ApplicativeTask`:

```scala
object ApplicativeTask {

  trait Semigroupal[F[_]] {
    def product[A, B](fa: F[A], fb: F[B]): F[(A, B)]
  }

  trait Functor[F[_]] {
    def map[A, B](fa: F[A])(f: A => B): F[B]
  }

  trait Apply[F[_]] extends Functor[F] with Semigroupal[F] {

    def ap[A, B](fab: F[A => B])(fa: F[A]): F[B]

    override def product[A, B](fa: F[A], fb: F[B]): F[(A, B)] =
      ap(map(fa)(a => (b: B) => (a, b)))(fb)

    def map2[A, B, Z](fa: F[A], fb: F[B])(f: (A, B) => Z): F[Z] =
      map(product(fa, fb))(f.tupled)
  }

  trait Applicative[F[_]] extends Apply[F] {
    def pure[A](a: A): F[A]
  }

  implicit val optionApplicative: Applicative[Option] = new Applicative[Option] {
    def pure[A](a: A): Option[A] = Some(a)

    def ap[A, B](fab: Option[A => B])(fa: Option[A]): Option[B] = (fab, fa) match {
      case (Some(f), Some(a)) => Some(f(a))
      case _                  => None
    }
  }

  def traverse[F[_]: Applicative, A, B](as: List[A])(f: A => F[B]): F[List[B]] =
    as.foldRight(Applicative[F].pure(List.empty[B])) { (a, acc) =>
      Applicative[F].map2(f(a), acc)(_ :: _)
    }

  def sequence[F[_]: Applicative, A](fas: List[F[A]]): F[List[A]] =
    traverse(fas)(identity)
}
```

---

**User:**

what with map?
    implicit val optionApplicative: Applicative[Option] = new Applicative[Option] {
      def pure[A](a: A): Option[A] = Some(a)

      def ap[A, B](fab: Option[A => B])(fa: Option[A]): Option[B] = (fab, fa) match {
        case (Some(f), Some(a)) => Some(f(a))
        case _ => None
      }

      override def map[A, B](fa: Option[A])(f: A => B): Option[B] = ???
    }

---

**Assistant:**

The `map` function in the `Applicative` trait extends the `Functor` trait, which means that it provides the same `map` operation as the `Functor`. In the case of `Option`, the `map` operation is simply applied to the underlying value of the `Option`, if it exists. So, you can implement the `map` operation for `Option` like this:

```scala
  implicit val optionApplicative: Applicative[Option] = new Applicative[Option] {
    def pure[A](a: A): Option[A] = Some(a)

    def ap[A, B](fab: Option[A => B])(fa: Option[A]): Option[B] = (fab, fa) match {
      case (Some(f), Some(a)) => Some(f(a))
      case _ => None
    }

    override def map[A, B](fa: Option[A])(f: A => B): Option[B] = fa.map(f)
  }
```

Here, `map` is simply defined as the `map` operation on the `Option` type, which applies the function `f` to the underlying value of the `Option`, if it exists, and returns a new `Option` with the transformed value.