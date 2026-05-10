# Cardinality Sorting

## Podsumowanie

Zadanie "Cardinality Sorting" (sortowanie po kardynalności binarnej) polega na posortowaniu tablicy liczb dziesiętnych na podstawie dwóch kryteriów (od najważniejszego do najmniej ważnego):
1. **Rosnąca kardynalność binarna**: liczba jedynek (tzw. _bitów zapalonych_) w reprezentacji binarnej danej liczby.
2. **Rosnąca wartość dziesiętna**: jeśli dwie liczby mają taką samą ilość jedynek w systemie binarnym, to mniejsza liczba dziesiętna powinna w posortowanej tablicy znaleźć się wcześniej.

## Jak to działa?

Dla każdej z liczb obliczamy ilość jedynek po konwersji do postaci binarnej. Na przykład, dla liczby `10` (system dziesiętny) jej reprezentacja binarna to `1010`, co oznacza, że zawiera ona dokładnie dwie jedynki. Jej kardynalność wynosi zatem 2.

Rozpatrując przykład z zadania, mając wejściową tablicę `[1, 2, 3, 4]`, przeliczamy każdą wartość:
- `1` jest reprezentowane jako `1` (1 jedynka)
- `2` jest reprezentowane jako `10` (1 jedynka)
- `3` jest reprezentowane jako `11` (2 jedynki)
- `4` jest reprezentowane jako `100` (1 jedynka)

Poszczególne poziomy kardynalności dla tablicy to 1, 1, 2, 1. Grupując liczby według ilości jedynek i następnie sortując mniejsze wartości dziesiętne pośród remisów (kardynalność = 1), otrzymujemy pożądaną, posortowaną tablicę: `[1, 2, 4, 3]`.

## Rozwiązanie w Pythonie

W Pythonie możemy w bardzo prosty i idiomatyczny sposób zrealizować to zadanie, korzystając z wbudowanej funkcji `sorted()`, która jako opcjonalny argument `key` może przyjmować funkcję lambda zwracającą krotkę (ang. `tuple`). Python domyślnie wspiera sortowanie według zawartości krotek — system ocenia pierwszy element jako główne kryterium, a w przypadku takich samych wartości rozstrzyga remisy porządkując sekwencję wedle kolejnych elementów w krotce.

Począwszy od Pythona 3.10 dostępna jest wbudowana i wysoce wydajna metoda typu `int` nosząca nazwę `bit_count()`, która zwraca liczbę jedynek w reprezentacji binarnej:

```python
def cardinalitySort(nums: list[int]) -> list[int]:
    """
    Sorts a list of integers primarily by their binary cardinality (number of 1s in binary representation),
    and secondarily by their decimal value.
    """
    # bit_count() returns the number of ones in the binary representation of an integer.
    # The lambda function creates a tuple: (cardinality, actual number)
    return sorted(nums, key=lambda x: (x.bit_count(), x))

# Example usage:
nums = [1, 2, 3, 4]
print(cardinalitySort(nums))
# Expected Output: [1, 2, 4, 3]
```

Dla starszych środowisk (Python 3.9 lub niżej) możemy zastąpić wywołanie metody `x.bit_count()` poleceniem zliczającym odpowiednie znaki w ciągu teksowym (string) po konwersji do reprezentacji binarnej za pomocą `bin()`. Alternatywa jest odrobinę mniej zoptymalizowana, lecz zachowuje kompletną zgodność zadaniową i logiczną:

```python
def cardinalitySort(nums: list[int]) -> list[int]:
    return sorted(nums, key=lambda x: (bin(x).count('1'), x))
```

### Rozwiązanie z użyciem `collections.Counter`

W przypadku, gdybyśmy nie dotarli jeszcze do metod takich jak `bit_count()` lub `str.count()`, albo jeśli specyfika zadania zabrania korzystania z nich dla sprawdzenia wiedzy kandydata, dobrą alternatywą będzie sięgnięcie po klasę `Counter` z modułu `collections`. 

Konstruktor klasy `Counter` po otrzymaniu sekwencji (w tym przypadku ciągu znaków z naszej konwersji binarnej) zlicza jego znaki, tworząc strukturę podobną do słownika. Ponieważ zapytanie domyślnego obiektu `Counter` o podany klucz bezpiecznie zwraca 0 w wypadku braku danego znaku, rozwiązanie to działa znakomicie w każdych warunkach:

```python
from collections import Counter

def cardinalitySort(nums: list[int]) -> list[int]:
    # Counter zlicza wystąpienia znaków z wyniku bin() np: Counter({'1': 2, '0': 1, 'b': 1}).
    # Odwołujemy się po ilości jedynek odpytując słownik kluczem '1'.
    return sorted(nums, key=lambda x: (Counter(bin(x))['1'], x))
```

### Podejście Obiektowe (Własna klasa i `__lt__`)

Jeżeli chcielibyśmy rozwiązać to zadanie w sposób w pełni zorientowany obiektowo (OOP), możemy stworzyć lokalną klasę reprezentującą liczby z przypisaną do nich kardynalnością zapisaną w atrybutach. 

Aby wbudowane metody sortujące w Pythonie wiedziały, w jaki sposób porównywać i wymieniać miejscami ze sobą nasze obiekty, zaimplementujemy tzw. _dunder method_ (metodę magiczną) `__lt__` (skrót od _less than_ – „mniejsze niż”). Dzięki temu zdefiniujemy precyzyjną, własną logikę sortowania.

```python
class BinaryNumber:
    def __init__(self, decimal_val: int):
        self.value = decimal_val
        # Wyliczamy kardynalność od razu w momencie tworzenia instancji
        self.cardinality = decimal_val.bit_count() # LUB: bin(decimal_val).count('1')
        
    def __lt__(self, other: 'BinaryNumber') -> bool:
        # 1. Główne kryterium: rosnąca kardynalność binarna
        if self.cardinality != other.cardinality:
            return self.cardinality < other.cardinality
        
        # 2. Kryterium pomocnicze: mniejsza wartość dziesiętna w przypadku remisów
        return self.value < other.value

def cardinalitySort(nums: list[int]) -> list[int]:
    # Konwertujemy wszystkie inty na obiekty naszej nowej klasy
    binary_objects = [BinaryNumber(num) for num in nums]
    
    # Sortujemy listę obiektów – Python automatycznie pod spodem użyje naszej metody __lt__
    binary_objects.sort()
    
    # Przechodzimy po posortowanych już obiektach, zwracając listę ich wartości
    return [obj.value for obj in binary_objects]
```

## Różne warianty zliczania: Zera w `bin()` oraz znaki w `hex()`

W wielu innych zadaniach z algorytmiki możesz spotkać się z koniecznością zliczenia innej grupy znaków – na przykład zer lub liter pochodzących z systemu heksadecymalnego. W obu z tych wariantów trzeba **uważać na prefiksy** wbudowane w natywne funkcje!

### Liczenie zer ('0') w reprezentacji binarnej
Pamiętaj, że funkcja `bin(num)` dodaje do wyniku specyfikator formatu na samym początku stringa. Na przykład dla dwójki `bin(2)` zwraca ciąg `"0b10"`.
Jeżeli użylibyśmy polecenia `bin(num).count('0')` zapominając o tym zachowaniu, wliczylibyśmy do wyniku powtarzające się, fałszywe zero zlokalizowane z przodu, które jest wyłącznie wskaźnikiem układu `0b` we wbudowanym konwerterze.

Rozwiązaniem tego probemu jest odcięcie dwóch pierwszych znaków poprzez zjawisko o nazwie *slicing* (`[2:]`):

```python
def count_zeros(num: int) -> int:
    # Ucinamy prefiks '0b' przed rozpoczęciem liczenia
    binary_str = bin(num)[2:]
    return binary_str.count('0')

# Uproszczone użycie w locie z funkcją sortowania we wbudowanej lambdzie:
sorted_nums = sorted(nums, key=lambda x: bin(x)[2:].count('0'))
```

### Liczenie liter ('c') w ujęciu szesnastkowym (Hex)
Podobny układ obowiązuje funkcję `hex(num)`, konwertującą liczby na system heksadecymalny. Poprzedza ona wyjście identyfikatorem `0x`. Przykładowo dla 12 wywołanie `hex(12)` zwróci `"0xc"`.

Choć dla znaku `'c'` w teorii nie rodzi to wymiernych błędów matematycznych (w `"0x"` nie ma żadnego "c"), wciąż zaleca się dbanie o czysty i niezależny od konwertera ciąg, z uwagi na potencjalne ryzyko i błędy przy zliczaniu `x` i `0`.

Zamiast standardowego ucina *slice'm*, w tym wypadku doskonale sprawdza się użycie sprytnego wariantu natywnego formatowania f-string:

```python
def count_hex_c(num: int) -> int:
    # Formatowanie :x wymusza małe litery heksadecymalne
    # wbudowane bez żadnych prefiksów formatowania, np. "c" zamiast "0xc"
    return f"{num:x}".count('c')

# LUB - dla standardowego ucinania w locie:
sorted_nums = sorted(nums, key=lambda x: hex(x)[2:].count('c'))
```

### Liczenie wystąpień ('5') w systemie ósemkowym (Octal)
Sytuacja z układem ósemkowym wymaga podobnego podejścia co systemy zaprezentowane wcześniej. Natywna funkcja `oct(num)` wyznacza reprezentację, ale zwraca ją opatuloną przedrostkiem `0o` (reprezentującym zero i małą literę 'o').
Przykładowo polecenie `oct(13)` wygeneruje łańcuch znaków `"0o15"`.

Chociaż szukanie samej piątki w prefiksie `"0o"` nam nie straszne, to w dobie skalowania czy ryzyka zapytań o zera (albo o literę 'o') – najlepszą praktyką pozostaje obróbka stringa na czysty tekst układu liczbowego. Z pomocą znów mogą przyjść metody *slicingu* lub *f-string*:

```python
def count_oct_5(num: int) -> int:
    # Odcięcie identyfikatora '0o' znakiem slicingu [2:]
    oct_str = oct(num)[2:]
    return oct_str.count('5')

# Alternatywa: nowsze formatowanie f-string niezawierające prefiksu
def count_oct_5_format(num: int) -> int:
    # Specyfikator :o konwertuje do ukłądu ósemkowego bez dodatku '0o' na przodzie
    return f"{num:o}".count('5')
```
