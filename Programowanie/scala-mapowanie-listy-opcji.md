# Scala: Mapowanie Listy Opcji.

**Data:** 2023-02-19

---

**User:**

co jest nie tak w tym kodzie Scala
  val l: List[Option[Int]] = List(Option(1), Option(5))
  println(l.map(v =>v + 2))

---

**Assistant:**

Kod Scala zawiera błąd kompilacji. 

Wartością typu `v` w wyrażeniu `v + 2` jest wartość typu `Option[Int]`, więc próba dodania liczby całkowitej do opcji jest niepoprawna i powoduje błąd kompilacji.

Aby poprawić ten kod, można użyć metody `map` na liście `List[Option[Int]]`, a następnie zmapować wartości `Option` do odpowiednich wartości całkowitych i dodać 2 do każdej z nich, na przykład:

```
val l: List[Option[Int]] = List(Option(1), Option(5))
println(l.map(opt => opt.map(_ + 2)))
```

Metoda `map` jest używana do zastosowania funkcji do każdej wartości w liście, a `opt.map` jest używana do zastosowania funkcji do wartości `Option`. Używamy `_ + 2`, aby dodać 2 do wartości całkowitej wewnątrz każdej wartości `Option`. Ostatecznie, zwracamy listę, która zawiera wartości `Option` zawierające odpowiednio zmodyfikowane wartości całkowite.

---

**User:**

Super. A co jest nie tak tutaj?
  val l: List[Option[Int]] = List(Option(1), Option(null), Option(3), Option(null), Option(5))
  println(l.map(opt => opt.map(_ + 2)))

---

**Assistant:**

Ten kod również może powodować błąd w czasie działania, zależnie od sposobu, w jaki jest obsługiwana wartość `null`. 

Jeśli wartość `null` jest niedopuszczalna w kontekście aplikacji, wówczas taki kod powinien być zmodyfikowany tak, aby uniknąć przetwarzania wartości `null`. W tym przypadku, zamiast używać typu `Option[Int]`, należy użyć typu `Option[Option[Int]]`, aby oddzielić wartości `null` od wartości całkowitych:

```
val l: List[Option[Option[Int]]] = List(Option(Option(1)), Option(None), Option(Option(3)), Option(None), Option(Option(5)))
println(l.flatten.map(_.map(_ + 2)))
```

W powyższym kodzie, używamy typu `Option[Option[Int]]`, aby wskazać, że wartości `null` są obecne w liście. Następnie używamy `flatten`, aby usunąć wewnętrzną warstwę `Option`, dzięki czemu otrzymujemy listę `List[Option[Int]]`. Ostatecznie, używamy `map`, aby dodać 2 do każdej wartości całkowitej, ale tylko dla wartości `Option[Int]`, które nie są `None`.

W przeciwnym razie, jeśli wartość `null` jest dopuszczalna, wówczas taki kod może działać poprawnie, ale wartości `null` będą przetwarzane jako wartości `None`. W tym przypadku, można użyć tego samego kodu, jak w poprzednim przykładzie, ponieważ wtedy wartości `null` zostaną automatycznie zamienione na `None`.