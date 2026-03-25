# Scala.js i biblioteki

**Data:** 2023-05-07

---

**User:**

Czy tworząc projekt w Scala.js mogę korzystać z dowolnych dependencji dla Scala?

---

**Assistant:**

Tak, podczas tworzenia projektu w Scala.js możesz korzystać z większości bibliotek i zależności dla języka Scala. Scala.js udostępnia tzw. "interop" z kodem napisanym w języku JavaScript, co umożliwia wykorzystanie większości popularnych bibliotek JavaScript w Twoim projekcie. Jednak nie wszystkie biblioteki będą działać poprawnie lub będą dostępne w wersji przeznaczonej dla platformy JavaScript, ponieważ niektóre zależności wymagają dostępu do funkcji specyficznych dla platformy JVM, które nie są dostępne w JavaScript. 

Przed dodaniem zależności do Twojego projektu w Scala.js, zaleca się sprawdzenie, czy biblioteka działa poprawnie w środowisku Scala.js lub czy nie ma innych zależności, które wymagają dostępu do funkcjonalności specyficznych dla JVM. Możesz także skorzystać z repozytoriów bibliotek przeznaczonych specjalnie dla Scala.js, które zawierają wersje bibliotek, które są w pełni kompatybilne z tą platformą.

---

**User:**

Co to za repozytorium?

---

**Assistant:**

Istnieje kilka repozytoriów bibliotek przeznaczonych specjalnie dla Scala.js, które zawierają wersje bibliotek, które są w pełni kompatybilne z tą platformą. Oto niektóre z tych repozytoriów:

1. Scala.js Community Build - repozytorium zawierające popularne biblioteki z ekosystemu Scala, które są w pełni kompatybilne z platformą Scala.js.

2. scalajs-bundler - narzędzie umożliwiające łatwe dodawanie zależności do projektu Scala.js i ich pakowanie w jednym pliku JavaScript.

3. scalajs-react - biblioteka umożliwiająca tworzenie interfejsów użytkownika w React za pomocą języka Scala i Scala.js.

4. scalajs-jquery - biblioteka umożliwiająca korzystanie z biblioteki jQuery w projekcie Scala.js.

5. scalajs-angular - biblioteka umożliwiająca tworzenie aplikacji webowych w Angular za pomocą języka Scala i Scala.js.

Te repozytoria zawierają wiele popularnych bibliotek i narzędzi, które są w pełni kompatybilne z platformą Scala.js i mogą być używane bezpośrednio w Twoim projekcie.

---

**User:**

możesz podać linki dla wszystkich wymienionych?

---

**Assistant:**

Oto linki do repozytoriów, o których wspomniałem wcześniej:

1. Scala.js Community Build: https://github.com/scala-js/scala-js-community-build
2. scalajs-bundler: https://github.com/scalacenter/scalajs-bundler
3. scalajs-react: https://github.com/japgolly/scalajs-react
4. scalajs-jquery: https://github.com/scalajs-io/scalajs-jquery
5. scalajs-angular: https://github.com/greencatsoft/scalajs-angular

Mam nadzieję, że będą one dla Ciebie pomocne!

---

**User:**

Czy możesz podać sposób, przykład jak sparsować string przy pomocy circe w Scala.js? Nie w Scala tylko Scala.js, to ważne.

---

**Assistant:**

Oczywiście, poniżej przedstawiam przykład parsowania stringa JSON przy użyciu biblioteki Circe w projekcie Scala.js:

1. Najpierw musisz dodać bibliotekę Circe do pliku build.sbt projektu Scala.js. Dodaj następującą zależność do sekcji "libraryDependencies":

```scala
libraryDependencies += "io.circe" %%% "circe-core" % "0.14.1"
libraryDependencies += "io.circe" %%% "circe-parser" % "0.14.1"
```

2. Następnie możesz napisać kod, który sparsuje string JSON. Oto przykład:

```scala
import io.circe._
import io.circe.parser._

val jsonString = "{\"name\":\"John\", \"age\":30}"

val parsedJson = parse(jsonString) match {
  case Left(error) => println("Error: " + error); Json.Null
  case Right(json) => json
}

val name = parsedJson.hcursor.get[String]("name")
val age = parsedJson.hcursor.get[Int]("age")

println("Name: " + name)
println("Age: " + age)
```

W powyższym kodzie parsujemy string JSON zawierający nazwę i wiek osoby. Funkcja `parse` zwraca obiekt JSON lub błąd, jeśli wystąpił problem podczas parsowania. Następnie możemy użyć kursora, aby otrzymać wartości pól "name" i "age" z obiektu JSON.

3. Uruchom projekt Scala.js, a następnie sprawdź wyniki w konsoli.

Mam nadzieję, że ten przykład będzie dla Ciebie pomocny!