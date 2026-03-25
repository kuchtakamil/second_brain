# Domyślny argument listy

**Data:** 2025-05-10

---

**User:**

[obraz niedostępny: file-service://file-8nA9jbKJ1MBVhcb6cVaZEc]

Dlaczego jeśli nie poda się swojej listy w drugim parametrze, to przy każdym wywołaniu funkcji append_to_list argumenty dodawane są do tej samej listy? Przecież to nie jest klasa że jest gdzieś zdefiniowana jedna lista do której można dodwać? Wydawałoby się że default [] w argumentach metody będzie tworzył zawsze nową listę

---

**Assistant:**

Świetne pytanie — to jedno z klasycznych „pułapek” w Pythonie, które zaskakują nawet doświadczonych programistów.

Problemem jest to, że **domyślne argumenty funkcji są obliczane tylko raz, w momencie definiowania funkcji**, a nie przy każdym jej wywołaniu.

### Co się dzieje dokładnie:

W tej funkcji:

```python
def append_to_list(elements: Iterable[T], target: list[T] = []) -> list[T]:
```

ten `target=[]` **jest tworzony tylko raz**, kiedy interpreter przechodzi przez definicję funkcji. Każde kolejne wywołanie funkcji, które nie poda `target`, **używa tego samego obiektu listy**.

Dlatego w tym przypadku:

```python
print(append_to_list([1, 2]))
print(append_to_list([3, 4]))
```

obie operacje wykonują `extend` na **tej samej liście**, co skutkuje rosnącą listą przy każdym kolejnym wywołaniu.

---

### Jak to poprawić:

Najbezpieczniejszy sposób to użycie `None` jako wartości domyślnej i utworzenie nowej listy wewnątrz funkcji:

```python
def append_to_list(elements: Iterable[T], target: list[T] = None) -> list[T]:
    if target is None:
        target = []
    target.extend(elements)
    return target
```

Dzięki temu nowa lista jest tworzona **za każdym razem**, gdy `target` nie zostanie podany.

Chcesz, żebym pokazał wynik działania obu wersji funkcji dla porównania?