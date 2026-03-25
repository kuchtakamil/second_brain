# Wyjaśnienie: `=`, `==` oraz `is` w Pythonie

W Pythonie operatory przypisania i porównania odgrywają kluczową rolę. Zrozumienie różnicy między nimi, a w szczególności między `==` i `is`, pozwala uniknąć wielu trudnych do wykrycia błędów i nieporozumień.

## 1. Operator `=` (Przypisanie)

Służy do przypisawania wartości, a dokładniej dowiązania nazwy do obiektu w pamięci. Zmienna w Pythonie jest jedynie referencją (etykietą) naklejoną na obiekt.

```python
a = [1, 2, 3] # Tworzy obiekt listy i przypisuje mu etykietę 'a'
b = a         # Etykieta 'b' wskazuje na ten sam obiekt co 'a'
```

## 2. Operator `==` (Równość wartości)

Sprawdza, czy **wartości** dwóch obiektów są takie same. Porównuje to co reprezentują te obiekty. W tle Python wywołuje "magiczną" metodę `__eq__()` danego obiektu.

```python
a = [1, 2, 3]
b = [1, 2, 3]

print(a == b)  # True, ponieważ zawartość list jest identyczna
```

## 3. Operator `is` (Tożsamość / Identyczność)

Sprawdza, czy dwie zmienne wskazują na **ten sam obiekt w pamięci** (porównuje ich wewnętrzne identyfikatory, które można sprawdzić za pomocą funkcji `id()`). 

```python
a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(a is b)  # False, ponieważ utworzono dwa osobne obiekty list w pamięci
print(a is c)  # True, ponieważ 'c' i 'a' wskazują na dokładnie ten sam obiekt
```

---

## Porównanie Pythona z Javą

Porównanie tych operatorów z językiem Java doskonale obrazuje różnicę w podejściach obu języków. W Javie odpowiedniki zachowują się odwrotnie!

| Akcja | Python | Java |
|---|---|---|
| **Porównanie wartości** (np. czy dwa odrębne stringi mają ten sam tekst) | `==` <br> (np. `text1 == text2`) | `.equals()` <br> (np. `text1.equals(text2)`) |
| **Porównanie tożsamości w pamięci** (czy dwie etykiety wskazują na ten sam obiekt) | `is` <br> (np. `obj1 is obj2`) | `==` <br> (dla obiektów, np. `obj1 == obj2`) |

### Przykład - wartości vs tożsamość

**Python:**
```python
s1 = "witaj"
s2 = "".join(["wi", "taj"]) # Wymuszamy stworzenie nowego stringa dla pewności

print(s1 == s2) # True - mają taką samą wartość testową
print(s1 is s2) # False - to dwa różne obiekty w pamięci (zależne od interned strings)
```

**Java:**
```java
String s1 = new String("witaj");
String s2 = new String("witaj");

System.out.println(s1.equals(s2)); // true - tekst reprezentuje te same znaki
System.out.println(s1 == s2);      // false - to dwie różne instancje klasy String w nowym miejscu sterty (heap)
```

## Ważne niuanse
Istnieje mechanizm w Pythonie zwany **cachingiem małych obiektów (interning)**.
Python trzyma w pamięci tylko jedną kopię małych liczb całkowitych (od -5 do 256) oraz niektórych krótkich napisów. Dlatego porównanie dla małych wbudowanych typów przez `is` może niespodziewanie ukazać wartość `True`:
```python
x = 256
y = 256
print(x is y) # True (mechanizm internowania, to jest ten sam mały obiekt Integer u podstaw!)

x = 1000
y = 1000
print(x is y) # False (zmienne poza zakresem buforowania, dwa nowe obiekty)
```

## Podsumowanie - Jak korzystać na co dzień?

- Używaj `=` wyłącznie do przypisywania zmiennych i parametrów.
- Używaj `==` we wszystkich sytuacjach, gdzie intencją jest sprawdzenie zbieżności i równości danych powiązanych z jakimś obiektem (najczęstszy przypadek!).
- Używaj `is` kiedy bezwzględnie chcesz sprawdzić, czy masz do czynienia z tą samą instancją. Sprawdzanie tożsamości **jest szczególnie zalecane jako tzw. idiom w Pythonie przy porównaniach do singletonów, np. `None`, `True` lub `False`:**
  - Pisz: `if zmienna is None:`
  - Unikaj: `if zmienna == None:`
