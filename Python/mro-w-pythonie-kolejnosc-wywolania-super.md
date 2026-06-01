# MRO w Pythonie i kolejność wywołań `super()`

## Przykład

```python
class A:
    def process(self):
        print("A")


class B(A):
    def process(self):
        print("B")
        super().process()


class C(A):
    def process(self):
        print("C")


class D(B, C):
    def process(self):
        print("D")
        super().process()


D().process()
```

## Co się wypisze?

Program wypisze:

```text
D
B
C
```

Nie wypisze się `A`.

## Dlaczego taka kolejność?

Klasa `D` dziedziczy po dwóch klasach:

```python
class D(B, C):
```

To oznacza, że Python musi ustalić jedną liniową kolejność przeszukiwania klas. Ta kolejność nazywa się **MRO**, czyli **Method Resolution Order**.

Dla tego przykładu MRO wygląda tak:

```python
print(D.__mro__)
```

Wynik:

```text
(<class '__main__.D'>, <class '__main__.B'>, <class '__main__.C'>, <class '__main__.A'>, <class 'object'>)
```

Czyli w uproszczeniu:

```text
D -> B -> C -> A -> object
```

## Krok po kroku

Wywołanie:

```python
D().process()
```

zaczyna się od metody `process` z klasy `D`, bo obiekt jest instancją klasy `D`.

### 1. `D.process`

```python
class D(B, C):
    def process(self):
        print("D")
        super().process()
```

Najpierw wypisuje:

```text
D
```

Potem wykonuje:

```python
super().process()
```

W klasie `D` wywołanie `super()` nie oznacza po prostu "weź pierwszego rodzica z definicji klasy i koniec". Oznacza raczej:

> przejdź do następnej klasy w MRO po klasie `D`.

MRO dla `D` to:

```text
D -> B -> C -> A -> object
```

Następna klasa po `D` to `B`, więc Python wywołuje:

```python
B.process(self)
```

### 2. `B.process`

```python
class B(A):
    def process(self):
        print("B")
        super().process()
```

Metoda z klasy `B` wypisuje:

```text
B
```

Potem wykonuje:

```python
super().process()
```

I tutaj jest najważniejszy moment.

Ponieważ cały czas pracujemy na obiekcie klasy `D`, Python nadal używa MRO klasy `D`, a nie tylko dziedziczenia klasy `B`.

MRO nadal jest takie:

```text
D -> B -> C -> A -> object
```

Metoda działa teraz w kontekście klasy `B`, więc `super()` szuka następnej klasy po `B`.

Następna klasa po `B` to `C`, a nie `A`.

Dlatego Python wywołuje:

```python
C.process(self)
```

### 3. `C.process`

```python
class C(A):
    def process(self):
        print("C")
```

Metoda z klasy `C` wypisuje:

```text
C
```

I na tym koniec, ponieważ `C.process` nie wywołuje:

```python
super().process()
```

Dlatego Python nie przechodzi dalej do klasy `A`.

Gdyby `C.process` wyglądało tak:

```python
class C(A):
    def process(self):
        print("C")
        super().process()
```

wtedy wynik byłby:

```text
D
B
C
A
```

## Ważna intuicja

`super()` w Pythonie nie znaczy dokładnie "wywołaj metodę klasy rodzica".

Lepsza intuicja:

> `super()` wywołuje następną implementację metody zgodnie z MRO aktualnego obiektu.

W tym przykładzie obiektem jest instancja `D`, więc `super()` podąża po kolejności:

```text
D -> B -> C -> A -> object
```

To dlatego `super()` w klasie `B` przechodzi do `C`, mimo że `B` bezpośrednio dziedziczy po `A`.

## Czym jest MRO?

**MRO**, czyli **Method Resolution Order**, to kolejność, w jakiej Python szuka metod i atrybutów w klasach.

Python używa MRO szczególnie przy:

- dziedziczeniu wielokrotnym,
- metodach o tej samej nazwie w wielu klasach,
- używaniu `super()`.

Dla każdej klasy można sprawdzić MRO tak:

```python
print(D.__mro__)
```

albo tak:

```python
print(D.mro())
```

## Jak Python ustala MRO?

Python używa algorytmu **C3 linearization**.

Nie trzeba znać go na pamięć, ale warto zapamiętać jego główne zasady:

1. Klasa sama jest pierwsza w swoim MRO.
2. Kolejność rodziców z definicji klasy jest ważna.
3. Klasy bazowe nie powinny pojawiać się przed klasami, które po nich dziedziczą.
4. Kolejność musi być spójna w całej hierarchii.

Dla:

```python
class D(B, C):
```

Python bierze pod uwagę:

```text
MRO(B) = B -> A -> object
MRO(C) = C -> A -> object
rodzice D = B -> C
```

Po scaleniu tych kolejności powstaje:

```text
D -> B -> C -> A -> object
```

`A` jest dopiero po `C`, ponieważ `D(B, C)` mówi, że `B` ma być przed `C`, a jednocześnie `C` jako klasa bardziej szczegółowa ma być przed swoim rodzicem `A`.

## Najważniejszy wniosek

Wynik:

```text
D
B
C
```

wynika z dwóch rzeczy:

1. MRO klasy `D` to:

```text
D -> B -> C -> A -> object
```

2. Klasa `C` nie wywołuje `super().process()`, więc łańcuch kończy się na `C` i nie dochodzi do `A`.

