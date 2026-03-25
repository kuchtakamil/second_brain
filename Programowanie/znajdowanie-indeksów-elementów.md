# Znajdowanie indeksów elementów

**Data:** 2023-08-17

---

**User:**

Scala, jak w liście znaleźć index elementów który spełnia dany predykat

---

**Assistant:**

W języku Scala, możesz użyć metody `zipWithIndex` w połączeniu z `filter` lub `collect` do znalezienia indeksów elementów, które spełniają określony predykat. Oto kilka przykładów:

```scala
val lista = List(10, 20, 30, 40, 50)

// Przykład 1: Użycie zipWithIndex i filter
val indeksy1 = lista.zipWithIndex.filter { case (element, _) => element > 25 }.map(_._2)
println(indeksy1) // Wyświetli: List(2, 3, 4)

// Przykład 2: Użycie zipWithIndex i collect
val indeksy2 = lista.zipWithIndex.collect { case (element, indeks) if element > 25 => indeks }
println(indeksy2) // Wyświetli: List(2, 3, 4)
```

Oba przykłady tworzą listę indeksów elementów, które spełniają określony predykat (w tym przypadku `element > 25`). W pierwszym przykładzie używa się `filter` do przefiltrowania par `(element, indeks)`, a następnie mapuje się je na same indeksy. W drugim przykładzie używa się `collect`, aby wybierać pary `(element, indeks)` zgodnie z warunkiem, a następnie mapuje się je na indeksy.

Możesz dostosować te przykłady do swojego konkretnego przypadku i użyć odpowiedniego predykatu w zależności od tego, jakie elementy chcesz znaleźć.

---

**User:**

Popraw
resultedPlayers.span(!_.numberedPlayer.isBot) match {case (h, _) => h}

---

**Assistant:**

Wygląda na to, że próbujesz użyć metody `span` na kolekcji `resultedPlayers`, aby podzielić elementy na dwie części - pierwszą zawierającą elementy, które nie są botami, i drugą, która nie jest wykorzystywana w tym fragmencie kodu. Następnie zwracasz pierwszą część. Twój kod jest już poprawny, ale jeśli chcesz go nieco uprościć, możesz to zrobić tak:

```scala
val nonBotPlayers = resultedPlayers.takeWhile(!_.numberedPlayer.isBot)
```

W tym przypadku, używając metody `takeWhile`, tworzysz nową kolekcję `nonBotPlayers`, która zawiera elementy aż do napotkania pierwszego elementu, który nie spełnia predykatu `!_.numberedPlayer.isBot`. To jest równoważne działaniu `span` w tym kontekście, ale może być bardziej czytelne i zwięzłe.