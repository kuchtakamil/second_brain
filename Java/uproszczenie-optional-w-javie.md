# Uproszczenie Optional w Javie

**Data:** 2025-03-03

---

**User:**

Mam taki kod 
Optional<MyDto> dto =
                Optional.ofNullable(selectedParam).flatMap(chosen ->  myAction(chosen));

Jednak wiem że "selectedParam" nigdy nie będzie nullem. Jest stringiem. jak to poprawić

---

**Assistant:**

Jeśli masz pewność, że `selectedParam` nigdy nie będzie `null`, możesz uprościć kod i uniknąć `Optional.ofNullable`, który jest zbędny w tym przypadku. Możesz użyć `Optional.of`, ponieważ `selectedParam` jest gwarantowanie nie-`null`:  

```java
Optional<MyDto> dto = Optional.of(selectedParam).flatMap(this::myAction);
```

Ewentualnie, jeśli `myAction` zwraca `Optional<MyDto>`, ale nie chcesz używać `Optional` na wejściu, możesz po prostu wywołać metodę bez `Optional`:  

```java
Optional<MyDto> dto = myAction(selectedParam);
```

To jest najczystsze rozwiązanie, jeśli `myAction` już zwraca `Optional`.

---

**User:**

OK, czyli jest to trochę na siłę używanie Optional tylko po to by móc wywołać flatMap, prawda?

---

**Assistant:**

Dokładnie! To jest właśnie „na siłę” używanie `Optional` tam, gdzie nie jest to potrzebne.  

`Optional` jest użyteczny, gdy chcesz elegancko obsłużyć możliwość `null`, ale jeśli masz gwarancję, że `selectedParam` nigdy nie będzie `null`, to tworzenie `Optional` tylko po to, by użyć `flatMap`, jest zbędnym narzutem.  

W tym przypadku wystarczy po prostu:  

```java
Optional<MyDto> dto = myAction(selectedParam);
```

To jest bardziej czytelne i efektywne.