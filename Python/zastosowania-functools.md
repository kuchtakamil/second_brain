# Zastosowania modułu `functools` (poza cache)

Moduł `functools` w Pythonie to potężny zestaw narzędzi do programowania funkcyjnego oraz tworzenia i modyfikowania funkcji wyższego rzędu (funkcji, które działają na innych funkcjach lub je zwracają).

Poniżej znajduje się zestawienie najważniejszych funkcji tego modułu wraz z krótkim opisem i przykładami (z pominięciem ogólnych mechanizmów pamięci podręcznej, takich jak `@lru_cache` czy `@cache`).

---

## 1. `functools.partial` i `functools.partialmethod`
Zwraca nową funkcję (tzw. funkcję częściową), która zachowuje się jak funkcja pierwotna, ale ma z góry zdefiniowane (zamrożone) wartości niektórych argumentów. Zmniejsza to liczbę argumentów wymaganych do wywołania funkcji. `partialmethod` działa analogicznie, ale jest przeznaczona dla metod w klasach.

```python
from functools import partial

def multiply(x, y):
    return x * y

# Tworzymy nową funkcję, która zawsze mnoży pierwszy argument przez 2
double = partial(multiply, 2)

print(double(4))  # Wynik: 8
```

## 2. `functools.wraps`
Jest to dekorator używany wewnątrz własnych dekoratorów. Jego głównym zadaniem jest skopiowanie metadanych (np. nazwy funkcji `__name__`, docstringa `__doc__`, adnotacji) z oryginalnej dekorowanej funkcji do funkcji opakowującej (wrappera). Bez tego zabiegu, dekorowana funkcja miałaby nazwę i dokumentację domyślnego wewnętrznego wrappera, zacierając swoje właściwe przeznaczenie.

```python
from functools import wraps

def moj_dekorator(funkcja):
    @wraps(funkcja)
    def wrapper(*args, **kwargs):
        print("Wywołanie dekoratora")
        return funkcja(*args, **kwargs)
    return wrapper

@moj_dekorator
def powitanie():
    """To jest docstring funkcji powitanie."""
    print("Cześć!")

print(powitanie.__name__)  # Wypisze: powitanie, a nie 'wrapper'
print(powitanie.__doc__)   # Wypisze: To jest docstring funkcji powitanie.
```

## 3. `functools.reduce`
Zastosowuje podaną funkcję do dwóch argumentów po kolei dla wszystkich elementów z sekwencji (od lewej do prawej), redukując w ten sposób sekwencję do pojedynczej wartości końcowej. Często używana z wyrażeniami `lambda`.

```python
from functools import reduce

liczby = [1, 2, 3, 4, 5]
# Operacja: (((1+2)+3)+4)+5
suma = reduce(lambda x, y: x + y, liczby)

print(suma)  # Wynik: 15
```

## 4. `functools.singledispatch` i `functools.singledispatchmethod`
Pozwalają na stworzenie tzw. **funkcji generycznej**, czyli takiej, która ma różne implementacje w zależności od typu pierwszego przekazanego do niej argumentu. Stanowi to wygodną, "pythonową" alternatywę dla długiego łańcucha instrukcji `if isinstance(arg, type): ...`. Obiekt `singledispatchmethod` jest odpowiednikiem dla metod w klasach.

```python
from functools import singledispatch

@singledispatch
def przetworz_dane(dane):
    print("Domyślne przetwarzanie dla nierozpoznanego typu")

@przetworz_dane.register(int)
def _(dane):
    print(f"Przetwarzam liczbę całkowitą: {dane}")

@przetworz_dane.register(list)
def _(dane):
    print(f"Przetwarzam listę o długości {len(dane)}")

przetworz_dane("tekst")  # Domyślne
przetworz_dane(42)       # Int
przetworz_dane([1, 2])   # List
```

## 5. `functools.total_ordering`
Dekorator dla klas, który automatyzuje implementację relacyjną. Wystarczy zdefiniować metodę `__eq__` (sprawdzającą równość) oraz jedną z pozostałych funkcji porównujących (np. `__lt__` używające `<`), a dekorator sam wygeneruje wektor wszystkich brakujących operatorów (`<=`, `>`, `>=`).

```python
from functools import total_ordering

@total_ordering
class Student:
    def __init__(self, ocena):
        self.ocena = ocena

    def __eq__(self, other):
        return self.ocena == other.ocena

    def __lt__(self, other):
        return self.ocena < other.ocena

s1 = Student(3)
s2 = Student(5)

print(s1 < s2)  # Ręcznie zdefiniowane: True
print(s1 > s2)  # Wygenerowane automatycznie przez dekorator: False
```

## 6. `functools.cmp_to_key`
Służy do konwersji starszych funkcji porównującej "2-argumentowych" (w starym stylu z Pythona 2 - przyjmującej dwa argumenty i zwracającej liczbę ujemną, zero lub dodatnią) w klucz sortowania (tzw. _key function_), pożądany np. w funkcjach `sorted()`, `min()` czy `max()` w środowiskach modernizowanych do Pythona 3.

```python
from functools import cmp_to_key

def porownaj_dlugosc(str1, str2):
    return len(str1) - len(str2)

slowa = ["jabłko", "kiwi", "banan"]
posortowane = sorted(slowa, key=cmp_to_key(porownaj_dlugosc))

print(posortowane)  # Wynik: ['kiwi', 'banan', 'jabłko']
```

## 7. `functools.cached_property`
Dekorator dla metody klasy, który traktuje ją jako właściwość (podobnie jak `@property`), po czym wyliczony w niej wynik zapisuje i natychmiast cache'uje w instancji klasy jako statyczna wartość przy pierwszym wywołaniu. Kolejne próby dostępu odczytują bez zwłoki uprzednio wyznaczoną wartość pomijając kod metody, co znakomicie przydaje się przy leniwym _(ang. lazy)_ ewaluowaniu procesów kosztownych obliczeniowo.

```python
from functools import cached_property

class DataProcessor:
    @cached_property
    def cost_intensive_data(self):
        print("Przeprowadzam skomplikowane obliczenia...")
        return sum(range(1000000))

processor = DataProcessor()
print(processor.cost_intensive_data) # Uruchomi obliczenia i zapisze na instancji
print(processor.cost_intensive_data) # Momentalnie weźmie z buforu bez podpinania kodu
```
