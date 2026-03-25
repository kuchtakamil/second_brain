# Wyszukiwanie binarne w Scala.

**Data:** 2023-02-26

---

**User:**

W Scala napisz wyszukiwanie binarne w wersji iteracyjnej a później w wesji rekurencyjnej nieogonowej

---

**Assistant:**

Wyszukiwanie binarne to algorytm wyszukiwania elementu w posortowanej tablicy lub liście. Algorytm ten działa w czasie logarytmicznym, co oznacza, że czas jego działania rośnie wolniej niż liniowo wraz z ilością elementów do przeszukania.

Wersja iteracyjna wyszukiwania binarnego w języku Scala:

```scala
def binarySearch(arr: Array[Int], x: Int): Int = {
  var left = 0
  var right = arr.length - 1
  
  while (left <= right) {
    val mid = left + (right - left) / 2
    
    if (arr(mid) == x) {
      return mid
    } else if (arr(mid) < x) {
      left = mid + 1
    } else {
      right = mid - 1
    }
  }
  
  return -1
}
```

Wersja rekurencyjna nieogonowa wyszukiwania binarnego w języku Scala:

```scala
def binarySearchRecursive(arr: Array[Int], x: Int, left: Int, right: Int): Int = {
  if (left > right) {
    return -1
  }
  
  val mid = left + (right - left) / 2
  
  if (arr(mid) == x) {
    return mid
  } else if (arr(mid) < x) {
    return binarySearchRecursive(arr, x, mid + 1, right)
  } else {
    return binarySearchRecursive(arr, x, left, mid - 1)
  }
}
```

W obu przypadkach algorytm działa w czasie logarytmicznym względem ilości elementów w tablicy. W wersji rekurencyjnej algorytm korzysta z wywołań rekurencyjnych, co może wpłynąć na wydajność w przypadku dużej ilości wywołań.

---

**User:**

wyjaśnij sposób wyznaczania środkowego elementu
val mid = left + (right - left) / 2

---

**Assistant:**

Wyszukiwanie binarne polega na podziale posortowanej tablicy lub listy na dwie połowy, a następnie porównaniu wartości środkowego elementu z wartością poszukiwaną. Jeśli wartość środkowego elementu jest mniejsza niż poszukiwana, to poszukiwana wartość musi znajdować się w górnej połowie tablicy lub listy, w przeciwnym przypadku musi znajdować się w dolnej połowie. W ten sposób algorytm działa rekurencyjnie, dzieląc tablicę na coraz mniejsze połowy, aż zostanie znaleziony poszukiwany element lub dojdzie się do końca tablicy.

Wyznaczanie środkowego elementu polega na obliczeniu średniej wartości indeksów pierwszego i ostatniego elementu danego przedziału, a następnie zaokrągleniu jej w dół do najbliższej liczby całkowitej, gdyż wynik musi być liczbą całkowitą. W języku Scala, w celu zaokrąglenia w dół, stosuje się operator dzielenia całkowitego `/` zamiast zwykłego operatora dzielenia `/`, który zwraca wartość zmiennoprzecinkową. Ostatecznie, obliczona wartość środkowego indeksu to `(left + right) / 2`. 

Jednakże, aby uniknąć problemów związanych z przepełnieniem (np. w przypadku bardzo dużych wartości `left` i `right`), warto wykonać to działanie w następujący sposób:

```scala
val mid = left + (right - left) / 2
```

W tej wersji obliczenia, zamiast sumować `left` i `right` i dzielić przez 2, odjęcie `left` od `right` daje nam połowę odległości między nimi, a następnie dodanie `left` zwraca nam indeks środkowego elementu. To pozwala na uniknięcie problemów związanych z przepełnieniem, a wynik jest taki sam jak w przypadku zwykłego dzielenia.

---

**User:**

Napisz algorytm w wersji regurencyjnej ogonowej.

---

**Assistant:**

Wersja rekurencyjna ogonowa wyszukiwania binarnego polega na wykorzystaniu akumulatora, który przechowuje indeks poszukiwanego elementu, wraz z granicami przedziału, w którym jest on wyszukiwany. W każdym wywołaniu rekurencyjnym aktualizowane są granice przedziału i wartość akumulatora, w zależności od wyniku porównania wartości środkowego elementu z poszukiwaną wartością.

```scala
def binarySearchTailRecursive(arr: Array[Int], x: Int): Int = {
  def search(left: Int, right: Int, acc: Int): Int = {
    if (left > right) {
      -1
    } else {
      val mid = left + (right - left) / 2
      
      if (arr(mid) == x) {
        acc + mid - left
      } else if (arr(mid) < x) {
        search(mid + 1, right, acc + mid - left + 1)
      } else {
        search(left, mid - 1, acc)
      }
    }
  }
  
  search(0, arr.length - 1, 0)
}
```

W tej wersji algorytmu, zamiast zwracać indeks poszukiwanego elementu, zwracana jest jego pozycja w posortowanej tablicy, czyli wartość `acc + mid - left`, gdzie `acc` to wartość akumulatora z poprzedniego wywołania, a `mid` i `left` to indeks środkowego i lewego elementu przedziału, na którym działa rekurencyjnie algorytm. Wartość `acc + mid - left` pozwala na przeliczenie indeksu na pozycję w posortowanej tablicy.

Wersja rekurencyjna ogonowa może być bardziej wydajna niż wersja rekurencyjna nieogonowa, ponieważ w niej unikamy rekurencyjnych wywołań i stosu wywołań, co pozwala na zmniejszenie zużycia pamięci.

---

**User:**

napisz inną wersję rekurencyjnej ogonowej

---

**Assistant:**

Oto inna wersja algorytmu wyszukiwania binarnego w wersji rekurencyjnej ogonowej w języku Scala:

```scala
def binarySearchTailRecursive(arr: Array[Int], x: Int): Int = {
  def search(left: Int, right: Int, acc: Int): Int = {
    if (left <= right) {
      val mid = left + (right - left) / 2
      arr(mid) match {
        case m if m == x => acc + mid - left
        case m if m < x => search(mid + 1, right, acc + mid - left + 1)
        case _ => search(left, mid - 1, acc)
      }
    } else {
      -1
    }
  }
  search(0, arr.length - 1, 0)
}
```

W tej wersji, funkcja wyszukiwania `search` jest wciąż wywoływana rekurencyjnie, ale jest ona zaimplementowana w sposób ogonowy, ponieważ żadne wywołania rekurencyjne nie następują po zwróceniu wartości z funkcji. Zamiast tego, każde wywołanie rekurencyjne jest zwracane bezpośrednio przez wywołanie `search`, a wynik jest przekazywany jako argument akumulatora.

Funkcja `search` działa analogicznie do wersji iteracyjnej i rekurencyjnej nieogonowej. W każdym wywołaniu rekurencyjnym sprawdzane jest, czy lewy indeks nie przekroczył prawego indeksu, a następnie wyznaczany jest środkowy indeks. Następnie porównywana jest wartość środkowego elementu z wartością `x`. Jeśli są równe, to funkcja zwraca sumę akumulatora i różnicy między środkowym a lewym indeksem, co jest równoważne z zwróceniem indeksu poszukiwanego elementu. Jeśli wartość środkowego elementu jest mniejsza od `x`, to funkcja wykonuje wywołanie rekurencyjne na przedziale od `mid + 1` do `right`, z zaktualizowanym akumulatorem, który dodaje liczbę elementów między lewym indeksem a środkowym indeksem plus jeden, czyli `mid - left + 1`. Jeśli wartość środkowego elementu jest większa niż `x`, to funkcja wykonuje wywołanie rekurencyjne na przedziale od `left` do `mid - 1` z niezmienionym akumulatorem. Jeśli lewy indeks przekroczy prawy indeks, to funkcja zwraca `-1`, co oznacza, że element nie został znaleziony.

Funkcja `binarySearchTailRecursive` zwraca wynik wywołania funkcji `search` z wartościami granic przedziału i akumulatorem początkowym, którym jest `0`.