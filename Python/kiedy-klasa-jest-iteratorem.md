# Kiedy klasa w Pythonie pozwala na iterację (for ... in ...)?

Aby na instancji klasy można było wywołać pętlę `for element in obiekt:`, obiekt ten musi być **Iterable** (iterowalny). To, czy obiekt pozwala na iterację, w Pythonie ustala się na podstawie **protokołu iteracji** (czyli określonych metod magicznych), a nie na podstawie dziedziczenia.

## Protokół iteracji - co musi mieć klasa?

Klasa jest **Iterable** (pozwala na użycie w pętli `for`), jeśli zaimplementuje **przynajmniej jedną** z poniższych metod magicznych:

1. `__iter__(self)` - to jest główne i zalecane podejście. Metoda ta powinna zwracać obiekt **Iteratora** (czyli obiekt posiadający metodę `__next__()`). Najprościej to osiągnąć stosując wewnątrz niej słowo kluczowe `yield` (co czyni ją generatorem).
2. `__getitem__(self, index)` - to podejście historyczne (tzw. "fallback"). Jeśli klasa nie ma metody `__iter__`, ale pozwala na indeksowanie od 0 wzwyż (np. `obiekt[0]`, `obiekt[1]`), pętla `for` poradzi sobie iterując po indeksach, aż klasa zgłosi błąd `IndexError`.

### Przykład najprostszej iterowalnej klasy

```python
class MojaKolekcja:
    def __init__(self):
        self.dane = [1, 2, 3]

    def __iter__(self):
        # Najbardziej "pythonowy" sposób to zwrócenie generatora z użyciem yield
        for element in self.dane:
            yield element * 10

kolekcja = MojaKolekcja()

# Skoro klasa ma __iter__, pętla for na niej zadziała:
for x in kolekcja:
    print(x)  # Wynik: 10, 20, 30
```

Więcej wzorców projektowych dotyczących pisania własnych klas iterowalnych (oraz pełne iteratory z wbudowanym `__next__`) znajdziesz w [Iterable Class in Python](iterable-class-in-python.md).

## Iterable vs Iterator

Aby w pełni zrozumieć działanie pętli `for`, należy rozróżnić te dwa, powiązane ze sobą pojęcia:

- **Iterable (Obiekt iterowalny)**: Np. lista, set, Twoja klasa z `__iter__`. Możesz wywołać na nim wbudowaną funkcję `iter(obiekt)`, a ona zwróci Ci *Iterator*. Pętla `for` robi to automatycznie pod spodem (wywołując `iter(obiekt)` przed rozpoczęciem pętli).
- **Iterator**: Obiekt, który "wie" na jakim etapie iteracji się znajduje. Posiada metodę `__next__()`. Zwraca kolejny element przy wywołaniu wbudowanej funkcji `next(iterator)`, a gdy elementy się skończą, wyrzuca wyjątek `StopIteration` (co dla pętli `for` jest cichym sygnałem do zakończenia iteracji).

> [!NOTE]
> **Zasada kciuka:** Każdy Iterator jest jednocześnie Iterable (ponieważ iteratory ze względu na specyfikację protokołu muszą mieć metodę `__iter__` zwracającą samych siebie), ale nie każdy Iterable jest Iteratorem (lista jest Iterable, ale *sama w sobie* nie jest Iteratorem, tylko tworzy odrębny obiekt Iteratora).

## Skąd wiedzieć, czy obiekt jest Iteratorem/Iterable?

Python promuje filozofię **Duck Typing** (jeśli coś kwacze jak kaczka, to traktujemy to jak kaczkę), więc zamiast sprawdzać po klasie bazowej, sprawdzamy "czy dany obiekt obsługuje odpowiednie metody".

### Sposób 1: Najprostszy ("Lepsze prosić o wybaczenie niż o pozwolenie" - EAFP)

Najbardziej pythonicznym sposobem sprawdzenia, czy obiekt pozwala na iterację, jest po prostu spróbowanie wywołania na nim funkcji `iter()` wewnątrz bloku try-except:

```python
def czy_jest_iterable(obiekt):
    try:
        iter(obiekt)
        return True
    except TypeError:
        return False

# Przykłady:
print(czy_jest_iterable([1, 2, 3])) # True
print(czy_jest_iterable(100))       # False, bo rzuciłoby TypeError
```

### Sposób 2: Korzystając z modułu `collections.abc`

Możemy też elegancko i formalnie sprawdzić, czy obiekt spełnia protokół Iterable za pomocą funkcji `isinstance`, korzystając z modułu z klasami abstrakcyjnymi:

```python
from collections.abc import Iterable, Iterator

dane = [1, 2, 3]
iterator_danych = iter(dane)

# Czy lista pozwala na for...in... ?
print(isinstance(dane, Iterable))  # True

# Czy lista SAMA W SOBIE jest iteratorem?
print(isinstance(dane, Iterator))  # False!

# Czy iterator_danych to iterator?
print(isinstance(iterator_danych, Iterator)) # True
```

## Podsumowanie

- Możesz wywołać `for ... in ...` na obiekcie (na przykład Twojej własnej klasie), jeśli jest ona **Iterable**.
- Aby klasa stała się Iterable, powinna implementować metodę `__iter__(self)`, która musi z kolei zwracać iterator (co można uprościć słowem kluczowym `yield`). Alternatywnie działa starszy mechanizm w postaci metody `__getitem__(self, index)`.
- Aby sprawdzić, czy jakikolwiek obiekt można iterować, wywołaj na nim funkcję wbudowaną `iter(obiekt)` (przykład podejścia EAFP) lub użyj wbudowanych typów ABC z paczki `collections.abc` przy pomocy `isinstance()`.

## Powiązane tematy
- [Yield w Pythonie](yield-w-pythonie.md)
- [Generatory w Pythonie](generatory-yield-coroutine.md)
- [Jak zaprojektować iterowalną klasę z różnymi wzorcami](iterable-class-in-python.md)
