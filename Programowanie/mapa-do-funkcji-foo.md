# Mapa do funkcji "foo"

**Data:** 2023-08-16

---

**User:**

Scala, chcę każda para klucz - wartość z mapy został przekazana do funkcji foo(k: Int, v: Int)

---

**Assistant:**

Oczywiście! Jeśli chcesz przekazać każdą parę klucz-wartość z mapy do funkcji `foo`, możesz użyć pętli `foreach` na mapie i wywołać funkcję dla każdej pary. Oto przykład w języku Scala:

```scala
def foo(k: Int, v: Int): Unit = {
  println(s"Key: $k, Value: $v")
}

val map = Map(1 -> 10, 2 -> 20, 3 -> 30)

map.foreach { case (key, value) =>
  foo(key, value)
}
```

W tym przykładzie definiujemy funkcję `foo`, która przyjmuje dwa argumenty typu `Int`. Następnie tworzymy mapę `map`, która zawiera kilka par klucz-wartość. W pętli `foreach` iterujemy przez każdą parę klucz-wartość z mapy i wywołujemy funkcję `foo`, przekazując odpowiednie argumenty.

Wynik działania tego kodu będzie wyglądać mniej więcej tak:

```
Key: 1, Value: 10
Key: 2, Value: 20
Key: 3, Value: 30
```

Możesz dostosować funkcję `foo` oraz mapę do swoich potrzeb.