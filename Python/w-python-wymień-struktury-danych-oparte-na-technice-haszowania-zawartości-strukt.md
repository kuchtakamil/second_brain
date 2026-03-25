# W Python wymień struktury danych oparte na technice haszowania zawartości strukt

**Data:** 19 lip 2025, 16:13:43 CET

---

**User:**

W Python wymień struktury danych oparte na technice haszowania zawartości struktury.

---

**Gemini:**

W Pythonie, podstawowymi strukturami danych, które opierają się na technice haszowania, są **`dict`** (słownik) oraz **`set`** (zbiór) i jego niemutowalna wersja **`frozenset`**.

---

### `dict` (Słownik)

Słowniki w Pythonie to dynamiczne tablice asocjacyjne, które mapują klucze na wartości. Wewnętrznie są zaimplementowane jako **tablica haszująca** (hash table).

- **Klucze**: Klucze w słowniku muszą być obiektami haszowalnymi, co oznacza, że muszą mieć zaimplementowaną metodę `__hash__()`, która zwraca liczbę całkowitą (hash), oraz metodę `__eq__()` do porównywania obiektów. Wartość hasha jest używana do szybkiego określenia "wiadra" (bucket) w tablicy, w którym powinien być przechowywany dany element.
- **Działanie**:
  1. Gdy dodajesz parę klucz-wartość, Python oblicza hash klucza za pomocą `hash(key)`.
  2. Wynikowy hash jest używany do wyliczenia indeksu w wewnętrznej tablicy.
  3. Para (klucz, wartość) jest przechowywana pod tym indeksem.
- **Kolizje**: Jeśli dwa różne klucze mają ten sam hash (kolizja), Python stosuje techniki rozwiązywania kolizji, takie jak *open addressing*, aby znaleźć kolejne wolne miejsce w tablicy dla nowego elementu.
- **Złożoność obliczeniowa**: Dzięki haszowaniu, operacje takie jak dodawanie, usuwanie i dostęp do elementu mają średnią złożoność czasową **O(1)**. W najgorszym przypadku (wiele kolizji) może to być O(n).

```
# Klucze (stringi, liczby, krotki) są haszowalne
my_dict = {
    "name": "John",
    42: "answer",
    (1, 2): "coordinates"
}

# Klucze (listy, słowniki) nie są haszowalne, ponieważ są mutowalne
# Poniższy kod spowoduje błąd TypeError: unhashable type: 'list'
# invalid_dict = {
#     ["a", "b"]: "value"
# }
```

---

### `set` (Zbiór)

Zbiory to nieuporządkowane kolekcje unikalnych, haszowalnych elementów. Podobnie jak słowniki, są one zaimplementowane przy użyciu **tablicy haszującej**.

- **Elementy**: Każdy element w zbiorze musi być haszowalny. Zbiór można traktować jako słownik, w którym interesują nas tylko klucze, a wartości są pomijane.
- **Działanie**:
  1. Podczas dodawania elementu do zbioru, obliczany jest jego hash.
  2. Hash determinuje pozycję elementu w tablicy haszującej.
  3. Dzięki temu mechanizmowi, sprawdzenie przynależności elementu do zbioru (`element in my_set`) jest operacją o średniej złożoności **O(1)**.
- **Unikalność**: Tablica haszująca naturalnie wymusza unikalność elementów. Jeśli próbuje się dodać element, którego hash (i wartość po porównaniu przez `__eq__`) już istnieje, operacja jest ignorowana.

```
my_set = {1, "apple", 3.14, (1, 2)}

# Dodawanie duplikatu nie zmienia zbioru
my_set.add(1)
print(my_set)  # Wynik: {1, 3.14, 'apple', (1, 2)}

# Sprawdzenie przynależności jest bardzo szybkie
is_present = "apple" in my_set  # True
```

---

### `frozenset` (Niezmienny zbiór)

`frozenset` to niemutowalna wersja `set`. Działa na tej samej zasadzie haszowania co `set`, ale po utworzeniu nie można go modyfikować (dodawać ani usuwać elementów).

- **Haszowalność**: Ponieważ `frozenset` jest niemutowalny i jego zawartość jest stała, sam obiekt `frozenset` jest **haszowalny**. Oznacza to, że `frozenset` może być używany jako klucz w słowniku lub jako element w innym zbiorze.

```
frozen = frozenset([1, 2, 3])

# frozenset może być kluczem w słowniku
dict_with_frozenset_key = {frozen: "a set of numbers"}

# Zwykły set nie może być kluczem, bo jest mutowalny
# Poniższy kod spowoduje błąd TypeError: unhashable type: 'set'
# invalid_dict_key = {{1, 2, 3}: "value"}
```