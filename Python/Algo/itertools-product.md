# Itertools Product

Funkcja `itertools.product()` z modułu `itertools` w Pythonie służy do obliczania **iloczynu kartezjańskiego** (cartesian product) z podanych obiektów iterowalnych (np. list, krotek, stringów). Zastępuje ona w zwięzły sposób wielokrotnie zagnieżdżone pętle `for`.

Wartość `product(A, B)` zwraca dokładnie taki sam rezultat jak popularne w Pythonie wyrażenie: `((x, y) for x in A for y in B)`.

## Do czego służy?
- **Tworzenie kombinacji:** Generuje wszystkie możliwe kombinacje elementów z wielu kolekcji.
- **Zwiększanie czytelności:** Spłaszcza zagnieżdżone pętle w jeden, czytelny strumień i eliminuje wcięcia kodu.
- **Optymalizacja pamięciowa:** `product()` jest "leniwy" (lazy evaluation). Generuje kolejne krotki (ang. *tuples*) w locie poprzez obiekt iteratora, zamiast od razu ładować wszystkie elementy do pamięci.

## Jak to działa?

Standardowe zagnieżdżone pętle dla wygenerowania iloczynu:
```python
list_a = [1, 2]
list_b = [3, 4]

# Nested loop approach
result = []
for item_a in list_a:
    for item_b in list_b:
        result.append((item_a, item_b))

print(result) 
# Output: [(1, 3), (1, 4), (2, 3), (2, 4)]
```

Oto jak wygląda to przy użyciu `itertools.product()`:
```python
from itertools import product

list_a = [1, 2]
list_b = [3, 4]

# Using itertools.product returns an iterator
cartesian_product = product(list_a, list_b)

# Convert the iterator to a list to print
print(list(cartesian_product))
# Output: [(1, 3), (1, 4), (2, 3), (2, 4)]
```

### Parametr `repeat`
Możemy użyć argumentu `repeat`, aby obliczyć iloczyn kartezjański obiektu z samym sobą.
```python
from itertools import product

# product(A, repeat=2) is computationally equivalent to product(A, A)
repeated_product = product([1, 2, 3], repeat=2)

print(list(repeated_product))
# Output: [(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (3, 3)]
```

### Rozpakowywanie zagnieżdżonych list (`*args`)
Jeśli posiadamy listę zawierającą w sobie podlisty (np. reprezentację macierzy) możemy użyć operatora `*` by rozpakować jej zawartość bezpośrednio do funkcji `product()`:
```python
from itertools import product

arrays = [[1, 2], [3, 4]]

# Using the * operator unspools the inner lists as individual arguments
unpacked_product = product(*arrays)

print(list(unpacked_product))
# Output: [(1, 3), (1, 4), (2, 3), (2, 4)]
```

## Przykładowa implementacja
**Kontekst zadania:** Mając dwie listy $A$ i $B$, Twoim celem jest obliczenie ich iloczynu kartezjańskiego. Elementy przychodzą z wejścia standardowego (jako ciągi liczb oddzielonych spacją), a każdy element iloczynu docelowo ma zostać wyświetlony, oddzielony jedną spacją w ostatecznym wyjściu: np. `(1, 3) (1, 4) (2, 3) (2, 4)`.

```python
from itertools import product

def solve_cartesian_product() -> None:
    # Read space-separated strings, convert them directly into integers,
    # and form lists using the input() function.
    list_a = list(map(int, input().split()))
    list_b = list(map(int, input().split()))
    
    # Calculate cartesian product iterator
    result = product(list_a, list_b)
    
    # Using the * unpacking operator unwraps the resulting 
    # tuples straight into the arguments of the print() function. 
    # This automatically formats the output with single spacing between pairs.
    print(*result)

if __name__ == '__main__':
    solve_cartesian_product()
```
Dzięki użyciu gwiazdki `print(*result)` zawartość generatora/krotek iterowanych w ramach `result` jest przekazywana do funkcji print jako kolejne argumenty, które drukują się rozdzielone domyślnym separatorem (spacją).

## Jak to działa pod maską? (Czysty Python)

Oryginalna implementacja `itertools.product` jest napisana w zoptymalizowanym języku C, ale jej zachowanie można wiernie odtworzyć w czystym Pythonie. Pozwala to dobrze zrozumieć, w jaki sposób pod spodem obsługiwana jest iteracja po wielu pulach argumentów na raz:

```python
def pure_python_product(*args, repeat=1):
    # Tworzymy listę pul ze wszystkich obiektów iterowalnych
    pools = [tuple(pool) for pool in args] * repeat
    
    # Inicjalizujemy wynik macierzą składającą się z jednej pustej listy
    result = [[]]
    
    # Dla każdej kolejnej puli mnożymy dotychczasowy wynik
    for pool in pools:
        result = [x + [y] for x in result for y in pool]
        
    # Na samym końcu zamieniamy pule wartości na niemodyfikowalne krotki
    for prod in result:
        yield tuple(prod)

# Przykład użycia pokazujący działanie z rozpakowywaniem macierzy
B = [[1, 2, 3], [3, 4, 5], [7, 8]]

# *B rozpakowuje macierz jako 3 oddzielne argumenty:
# pure_python_product([1, 2, 3], [3, 4, 5], [7, 8])
print(list(pure_python_product(*B)))
# Output: [(1, 3, 7), (1, 3, 8), (1, 4, 7), (1, 4, 8), (1, 5, 7), (1, 5, 8), (2, 3, 7), (2, 3, 8), (2, 4, 7), (2, 4, 8), (2, 5, 7), (2, 5, 8), (3, 3, 7), (3, 3, 8), (3, 4, 7), (3, 4, 8), (3, 5, 7), (3, 5, 8)]
```

Kod ten bardzo dobrze obrazuje, że przy pomocy zagnieżdżonych list (tzw. `list comprehension`) funkcja "przeżuwa" stopniowo wszystkie kombinacje elementów, a na koniec zwraca kolejne pasujące krotki przez wyrażenie odroczone `yield`. Dlatego też, tak łatwo jest jej obsłużyć rozpakowywanie list operatorami `*`.
