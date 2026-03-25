# Konwersja Either na Option.

**Data:** 2023-05-03

---

**User:**

W scala  mając obiekt Either[Error, MyObj], używając fold lub reduce utwórz obiekt klasy Option[MyObj] a w przypadku błędu zwróć None

---

**Assistant:**

Aby utworzyć obiekt klasy `Option[MyObj]` z obiektu `Either[Error, MyObj]` i zwrócić `None` w przypadku błędu, można użyć metody `fold` lub `reduceLeft` wraz z blokiem funkcji anonimowej.

Przykład z użyciem metody `fold`:
```scala
val eitherObj: Either[Error, MyObj] = // obiekt Either zawierający błąd lub wartość MyObj
val optionObj: Option[MyObj] = eitherObj.fold(_ => None, Some(_))
```
W powyższym przykładzie, jeśli `eitherObj` zawiera błąd, `fold` wywoła pierwszy blok anonimowy `_ => None`, który zwróci `None`. W przeciwnym przypadku, `fold` wywoła drugi blok anonimowy `Some(_)` z wartością `MyObj`, który utworzy obiekt klasy `Some` zawierający wartość `MyObj`.

Przykład z użyciem metody `reduceLeft`:
```scala
val eitherObj: Either[Error, MyObj] = // obiekt Either zawierający błąd lub wartość MyObj
val optionObj: Option[MyObj] = eitherObj.reduceLeft((acc, obj) => obj match {
  case Right(myObj) => Some(myObj)
  case _ => None
})
```
W tym przypadku, `reduceLeft` zwróci wartość `Either[Error, MyObj]` jako obiekt `MyObj`, jeśli nie zawiera błędu, a w przeciwnym przypadku zwróci `None`. Zastosowano instrukcję warunkową `match` z obudowaniem `Right` dla wartości `MyObj`, która zwróci `Some(myObj)`, lub `None` dla wszystkich innych przypadków.