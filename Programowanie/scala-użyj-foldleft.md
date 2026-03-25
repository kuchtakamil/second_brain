# Scala: Użyj foldLeft

**Data:** 2023-04-26

---

**User:**

W Scala przekształć kod
msgs.length match {
          case len if len > 0 => queue.offer(msgs.last)
          case 0              => IO.unit
        }
z użyciem funkcji fold

---

**Assistant:**

Można przekształcić kod wykorzystując metodę `foldLeft`, która pozwala iterować po elementach kolekcji i wykonywać na nich operacje, akumulując w ten sposób wynik. W tym przypadku wynikiem końcowym będzie wartość typu `IO[Unit]`.

Przykładowe rozwiązanie:

```
msgs.foldLeft(IO.unit) { (acc, msg) =>
  queue.offer(msg)
}
```

W tym kodzie zamiast korzystać z instrukcji warunkowej `match` wykorzystaliśmy metodę `foldLeft`, która iteruje po elementach listy `msgs` i wywołuje na nich metodę `offer` kolejki `queue`. Jako wartość początkową akumulatora podaliśmy wartość `IO.unit`, która reprezentuje efekt uboczny nie wykonujący żadnej operacji. Dzięki temu w przypadku, gdy lista `msgs` jest pusta, nie będzie wykonywana żadna operacja na kolejce.

---

**User:**

W przykładzie który podajesz, do funkcji queue.offer przekazywane są wszystkie elementy msgs. W podanym przeze mnie kodzie do queue.offer przekazywany jest tylko ostatni element - użycie last.

---

**Assistant:**

Przepraszam za moje nieporozumienie. W takim razie, aby uzyskać taki sam efekt jak w podanym przez Ciebie kodzie, można skorzystać z metody `lastOption`, która zwraca ostatni element listy w formie `Option` lub `None`, gdy lista jest pusta. W ten sposób można sprawdzić, czy lista zawiera elementy i jeśli tak, to dodać ostatni element do kolejki.

Przykładowe rozwiązanie z użyciem funkcji `fold`:

```
msgs.fold(IO.unit) { (_, msg) =>
  msgs.lastOption match {
    case Some(lastMsg) => queue.offer(lastMsg)
    case None          => IO.unit
  }
}
```

W tym kodzie wykorzystaliśmy metodę `fold` do iteracji po elementach listy `msgs`. W przypadku, gdy lista jest pusta, zostanie zwrócona wartość `IO.unit`. W przeciwnym razie, za pomocą metody `lastOption` pobieramy ostatni element listy i jeśli istnieje, dodajemy go do kolejki za pomocą metody `offer`. W przeciwnym wypadku zwracamy wartość `IO.unit`.