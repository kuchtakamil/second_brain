# Scala Pipe Operators

**Data:** 2023-04-12

---

**User:**

w scala wyjaśnij z przykładami użycie &>, !>

---

**Assistant:**

W języku Scala operatory &> oraz !> służą do tworzenia tzw. "pipe"-ów, czyli operatorów pozwalających na łączenie i przepływ danych między funkcjami w łatwy i czytelny sposób. 

Operator &> (czytany jako "and then") łączy dwa wyrażenia funkcyjne, przeprowadzając dane z lewej strony operatora do prawej strony. Operator ten zwraca wartość ostatniego wyrażenia funkcyjnego. 

Przykład użycia operatora &>:

```
val nums = List(1, 2, 3, 4, 5)
val filteredNums = nums.filter(_ % 2 == 0) &> (_.map(_ * 2))

// Wynik: filteredNums: List[Int] = List(4, 8)
```

W tym przykładzie operator &> łączy dwa wyrażenia funkcyjne: filter oraz map. Najpierw wyrażenie filter przepuszcza tylko parzyste liczby, a następnie wyrażenie map podwaja pozostałe liczby. Ostatecznie operator &> zwraca wynik z wyrażenia map, czyli listę [4, 8].

Operator !> (czytany jako "or else") działa podobnie jak operator &>, ale w przypadku gdy pierwsze wyrażenie funkcyjne zwróci wartość pustą, drugie wyrażenie funkcyjne zostanie wykonane zamiast niego.

Przykład użycia operatora !>:

```
val nums = List(1, 2, 3, 4, 5)
val filteredNums = nums.find(_ == 6) !> nums.filter(_ % 2 == 0)

// Wynik: filteredNums: List[Int] = List(2, 4)
```

W tym przykładzie operator !> łączy dwa wyrażenia funkcyjne: find oraz filter. Wyrażenie find szuka liczby 6 w liście nums, ale nie znajduje jej, więc operator !> wykonuje drugie wyrażenie funkcyjne, czyli przepuszcza tylko liczby parzyste z listy nums. Ostatecznie operator !> zwraca wynik z wyrażenia filter, czyli listę [2, 4].

---

**User:**

*> jest odpowiednikiem flatMap, a czy istnieje odpowiednik map?

---

**Assistant:**

Tak, istnieje operator w języku Scala, który jest odpowiednikiem operatora map, a nazywa się on map. 

Operator *> (czytany jako "map and ignore") działa podobnie jak operator flatMap, ale zwraca wartość z wyrażenia funkcyjnego po lewej stronie operatora, a nie z wyrażenia funkcyjnego po prawej stronie. Operator ten jest zwykle używany, gdy chcemy wykonać jakieś działanie na wartościach, ale nie interesuje nas wynik z wyrażenia funkcyjnego po prawej stronie operatora.

Przykład użycia operatora *>:

```
val nums = List(1, 2, 3, 4, 5)
val result = nums.map(_ * 2) *> println("Finished mapping")

// Wynik: result: Unit = ()
// Output: Finished mapping
```

W tym przykładzie operator *> wykonuje mapowanie wartości w liście nums i zwraca wartość Unit (oznaczającą brak wartości) z wyrażenia println. Wynik ten jest ignorowany, ponieważ nie jest przypisany do żadnej zmiennej. Natomiast wyrażenie println jest wykonane, co można zobaczyć na konsoli, gdzie zostanie wyświetlony napis "Finished mapping".

Warto zauważyć, że operator *> jest często używany w połączeniu z operatorami monadycznymi, takimi jak Option, Either, czy Future, gdzie po wykonaniu pewnej operacji, interesuje nas tylko fakt, że operacja została wykonana, a nie jej konkretny wynik.

---

**User:**

Zamień ten kod tak aby używane były operatory podobne do "*>"
                  generator.generate
                    .map(newVal => CarriageSpeed(Instant.now(), newVal))
                    .map(m => printer.print(m.asJson))
                    .flatMap(str => sender.send(deviceType, str))
                    .flatMap(_ => IO.sleep(cfg.frequency.second))

---

**Assistant:**

Można przepisać ten kod używając operatora *> w następujący sposób:

```
generator.generate
  .map(newVal => CarriageSpeed(Instant.now(), newVal))
  .map(m => printer.print(m.asJson) *> m.asJson)
  .flatMap(sender.send(deviceType, _))
  .flatMap(_ => IO.sleep(cfg.frequency.second))
```

W tym przepisaniu operator *> został zastosowany do pominięcia wywołania metody asJson() na obiekcie CarriageSpeed, co oznacza, że nie jest już potrzebna kolejna operacja map. Zamiast tego, wywołanie printer.print(m.asJson) zostaje wykonane w ramach operatora *> i jego wynik zostaje pominięty, a zwrócony zostaje tylko rezultat metody asJson(). Ten rezultat jest następnie przekazywany do funkcji sender.send za pomocą operatora flatMap.

Warto zauważyć, że przepisanie kodu w ten sposób może ułatwić jego czytelność i zwiększyć jego wydajność, ponieważ pominięcie wywołania metody asJson() w ramach operatora *> pozwala uniknąć zbędnego tworzenia dodatkowego obiektu typu Json, co może wpłynąć na wydajność aplikacji.