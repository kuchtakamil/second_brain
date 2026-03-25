# Parametry by name vs by value

**Data:** 2023-08-29

---

**User:**

Scala.
def whileLoop(condition: => Boolean)(body: => Unit): Unit =
  if (condition) {
    body
    whileLoop(condition)(body)
  }

var i = 2

whileLoop (i > 0) {
  println(i)
  i -= 1
} 

Jaka jest różnica między takim użyciem condition czyli by name a gdyby była użyta by value

---

**Assistant:**

W kodzie, który dostarczyłeś, funkcja `whileLoop` została zaimplementowana w sposób umożliwiający jej wywołanie za pomocą "by-name" lub "by-value" parametrów. Oba te rodzaje parametrów pozwalają na różne zachowanie kodu w zależności od tego, jakie wyrażenie zostanie przekazane. Oto wyjaśnienie różnicy między tymi dwoma podejściami:

1. **By-name (by nazwa) parametry:**
   W przypadku by-name parametrów, wyrażenie przekazywane jako argument jest obliczane za każdym razem, gdy jest używane w ciele funkcji. Oznacza to, że wyrażenie jest opóźniane do momentu jego użycia i może być obliczane wielokrotnie, jeśli jest wykorzystywane w wielu miejscach wewnątrz ciała funkcji.

   W twoim przypadku, używasz by-name parametrów dla `condition` i `body`. To oznacza, że wyrażenie `i > 0` i `println(i); i -= 1` zostaną obliczone za każdym razem, gdy zostaną użyte w ciele funkcji. Dzięki temu w trakcie każdej iteracji pętli while wyrażenia te będą obliczane na nowo.

2. **By-value (by wartość) parametry:**
   W przypadku by-value parametrów, wyrażenie przekazywane jako argument jest obliczane tylko raz, przed wejściem do ciała funkcji. Wszystkie referencje do tego parametru wewnątrz funkcji odnoszą się do wyniku obliczonego wyrażenia.

   Gdybyś użył by-value parametrów w twoim kodzie, wyrażenie `condition` (`i > 0`) oraz `body` (`println(i); i -= 1`) byłoby obliczane tylko raz, na początku działania funkcji `whileLoop`. Wszelkie późniejsze odwołania do `condition` i `body` wewnątrz pętli while odnosiłyby się już do tych obliczonych wartości.

W skrócie, różnica między by-name a by-value polega na tym, czy wyrażenie przekazywane jako argument jest obliczane za każdym razem, gdy jest używane (by-name), czy tylko raz na początku (by-value). W twoim przykładzie, zastosowanie by-name parametrów prowadzi do obliczania wyrażeń w każdej iteracji pętli, podczas gdy zastosowanie by-value parametrów spowodowałoby obliczenie tych wyrażeń tylko raz, na samym początku.