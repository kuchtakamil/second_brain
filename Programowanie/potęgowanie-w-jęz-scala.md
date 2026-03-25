# Potęgowanie w jęz. Scala

**Data:** 2023-08-16

---

**User:**

Scala, jak wykonać operacje pontegowania

---

**Assistant:**

W języku Scala, jak w większości języków programowania, operacje potęgowania można wykonać za pomocą operatora `Math.pow()` lub poprzez użycie notacji operatora `**`.

1. Używając `Math.pow()`:
```scala
val podstawa = 2.0
val wykladnik = 3.0
val wynik = Math.pow(podstawa, wykladnik)
println(wynik) // Wyświetli: 8.0
```

2. Używając notacji operatora `**` (dostępna w Scala 2.11 i nowszych):
```scala
val podstawa = 2.0
val wykladnik = 3.0
val wynik = podstawa ** wykladnik
println(wynik) // Wyświetli: 8.0
```

W obu przypadkach, wartości `podstawa` i `wykladnik` można zmieniać według własnych potrzeb. Pamiętaj, że `Math.pow()` zwraca wynik w postaci wartości zmiennoprzecinkowej, więc jeśli chcesz wynik w formie całkowitej, możesz go zaokrąglić lub rzutować.

Jeśli nie masz dostępu do notacji `**` lub potrzebujesz bardziej zaawansowanych operacji matematycznych, warto także zwrócić uwagę na bibliotekę ScalaMath, która dostarcza wiele przydatnych funkcji matematycznych, w tym potęgowanie.

---

**User:**

Dlaczego Math.pow zwraca double?

---

**Assistant:**

Metoda `Math.pow()` zwraca wartość typu `double`, ponieważ operacje potęgowania mogą prowadzić do wyników zmiennoprzecinkowych (czyli z ułamkami) nawet wtedy, gdy argumenty są całkowite. Przykładowo, potęga pierwiastka kwadratowego (0.5) z liczby całkowitej może dać wynik zmiennoprzecinkowy.

Język Java (i przez to również Scala, która dziedziczy wiele cech z Javy) został zaprojektowany tak, aby zachowywać się w sposób przewidywalny i zgodny z zasadami matematyki. Dlatego też wynik operacji potęgowania, nawet jeśli argumenty są całkowite, jest zwracany jako `double`, aby uwzględnić potencjalne wyniki zmiennoprzecinkowe.

Jeśli chcesz, aby wynik operacji potęgowania był całkowitym typem, możesz dokonać zaokrąglenia wyniku lub skonwertować go na typ całkowity za pomocą rzutowania, wiedząc, że możesz utracić część wartości po przecinku.