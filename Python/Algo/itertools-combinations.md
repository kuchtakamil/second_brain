# Itertools Combinations

Funkcja `itertools.combinations()` z modułu `itertools` w Pythonie służy do generowania wszystkich możliwych **kombinacji** (podzbiorów o określonej wielkości $r$) elementów z wybranego obiektu iterowalnego (np. listy czy stringa). Kombinacje takie są emitowane w porządku leksykograficznym – na podstawie ich indeksowych pozycji z wejścia. W związku z tym, jeżeli wyjściowa kolekcja na wejściu jest uprzednio posortowana, to krotki zwrotne też będą uporządkowane.

Jest niezwykle użytecznym narzędziem przy zastępowaniu wielu zagnieżdżonych pętli generujących kombinacje bez powtórzeń w kontekście tych samych indeksów bazowych.

## Do czego służy?
- **Tworzenie niezależnych zbiorów podrzędnych:** Idealnie sprawuje się, kiedy interesuje nas znalezienie powiązań między unikalnymi elementami, gdzie wewnątrz krotki element $A$ z elementem $B$ nie mają znaczenia na jakiej są pozycji - dąży tak abyśmy odzyskali $n! / r! / (n-r)!$ elementów wyjściowych.. 
- **Zwiększanie czytelności:** Pozwala na generowanie kombinacji w jednej prostej linijce wewnątrz kodu, a nie obciążającej wielowarstwowo.
- **Optymalizacja pamięciowa:** Podobnie jak inni przedstawiciele rodziny z biblioteki `itertools`, w tym używany do silnych wyliczeń wektorowych iloczyn kartezjański, tak i model ewaluacji przy funcjonalności kombinacji jest tzw. leniwy (lazy evaluation).

## Jak to działa?

Standardowe znalezienie k-krotności ciągu manualnie jest utemperowane do statycznych wielkości ze względu na używanie klasycznych zagnieżdżeń:

```python
from itertools import combinations

# Usage for generating pairs
string_val = '12345'
print(list(combinations(string_val, 2)))
# Output: [('1', '2'), ('1', '3'), ('1', '4'), ('1', '5'), ('2', '3'), ('2', '4'), ('2', '5'), ('3', '4'), ('3', '5'), ('4', '5')]

# Usage with duplicate elements
array_val = [1, 1, 3, 3, 3]
print(list(combinations(array_val, 4)))
# Output: [(1, 1, 3, 3), (1, 1, 3, 3), (1, 1, 3, 3), (1, 3, 3, 3), (1, 3, 3, 3)]
```

## Przykładowa implementacja

**Kontekst zadania:** Mając dany ciąg znaków $S$ i liczbę całkowitą $k$, Twoim zadaniem jest wydrukowanie wszystkich możliwych kombinacji znaków o wielkościi (rzędu) aż do $k$ włącznie. Kombinacje w odpowiednich rzędach długości mają powinnny być generowane w stabilnej i poprawnej kolejności leksykograficznej.

**Dane wejściowe:** Dla wejścia składającego się z dwóch wartości oddzielonych spacją, czyli np. `HACK 2`. 

Aby osiągnąć poprawny rezultat pamiętajmy o pre-sortowaniu ciągu docelowego aby wynik został sformatowany, zgodnie z zasadnością modułu, tak by wyliczał wszystkie litery zaczynając od litery A (zgodnie z `ACHK`).
 
```python
from itertools import combinations

def solve_combinations() -> None:
    # Read the input values correctly and map size constraint
    input_str, input_k = input().split()
    k = int(input_k)
    
    # Sort string structurally as combinations iterates by position
    sorted_s = sorted(input_str)
    
    # Iterate progressively for sub-combinations length 1, 2, ..., k
    for r in range(1, k + 1):
        for combo in combinations(sorted_s, r):
            # Join characters into single string representation
            print("".join(combo))

if __name__ == '__main__':
    solve_combinations()
```

Dla danych wejściowych `HACK 2`, rozwiązanie wyprodukuje następujący output:
```text
A
C
H
K
AC
AH
AK
CH
CK
HK
```

Dla każdej nowej domeny długości, użyliśmy tutaj nowej powłoki ze standardowego wariantu i wymuszaliśmy przełożenie literału na natywny format `"".join` by usunąć formatowanie odrębnych elementów krotki (np. `('A', 'C') -> AC`).

## Co, jeśli kolejność wyjściowa ma znaczenie? (Permutacje)

Jeśli potrzebujesz uwzględnić kolejność elementów, co oznacza, że zbiory takie jak `AC` oraz `CA` są traktowane jako dwa całkowicie unikalne przypadki, powinieneś użyć pokrewnej funkcji z tej samej rodziny — mianowicie `itertools.permutations()`.

Permutacje zwracają wszystkie możliwe uporządkowania generowanego zestawu wartości bez wielokrotnego powielania tych samych indeksów bazowych. Odznaczają się tym, że ewaluują obiekty również bazując na ich kolejności ułożenia:

```python
from itertools import permutations

# Generating pairs where specific order is distinguished
string_val = 'AC'
print(list(permutations(string_val, 2)))
# Output: [('A', 'C'), ('C', 'A')]
```

W analogicznym zadaniu, w którym do metody wpadłby zbiór `HACK`, po wywołaniu iteracji dla `r=2` z funkcją `permutations`, algorytm wyemitowałby oddzielnie jako unikalne trafienia, np. zarówno pary w wektorach ułożonych wg ciągu początkowego `AH`, jak i powiązane odwrócone pary `HA`.

## Powiązane tematy
- [Itertools Product](itertools-product.md) - do iloczynu kartezjańskiego (cartesian product).
