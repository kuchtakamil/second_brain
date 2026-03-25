# TypeVar w Pythonie: Zrozumienie Typów Generycznych

`TypeVar` (z modułu `typing`) to podstawowe narzędzie w Pythonie do tworzenia **typów generycznych** (generics). Pozwala ono na określenie, że funkcja, klasa lub struktura danych może działać na różnych typach, zachowując przy tym informacje o konkretnym typie używanym w danym wywołaniu.

## 1. Dlaczego potrzebujemy TypeVar?

Załóżmy, że chcemy napisać funkcję, która zwraca pierwszy element z listy:

```python
def get_first(items: list):
    return items[0]
```

Jeśli podamy listę intów (`[1, 2, 3]`), funkcja zwróci inta. Jeśli podamy listę stringów (`["a", "b"]`), zwróci stringa. Niestety, narzędzia do statycznej analizy typów (np. `mypy` lub podpowiedzi w IDE) potraktują wartość zwracaną jako niezdefiniowaną typowo wartość `Any`, gubiąc informację o konkretnym zaserwowanym typie.

Dzięki `TypeVar` możemy powiedzieć Mypy i IDE: *"Ta funkcja przyjmuje listę elementów typu T i zwraca pojedynczy element tego samego typu T"*.

## 2. Podstawowe użycie

```python
from typing import TypeVar, List

# Deklaracja zmiennej typowej (Type variable)
T = TypeVar('T')

def get_first(items: List[T]) -> T:
    return items[0]

# Mypy i Twoje IDE "wiedzą", że to wróci int
first_num = get_first([1, 2, 3]) 

# Tutaj z kolei zostanie wywnioskowany typ str
first_str = get_first(["Ala", "ma", "kota"]) 
```

W powyższym przykładzie `T` jest "zmienną typową". Gdy wywołujemy `get_first([1, 2, 3])`, `T` jest ujednolicane/wiązane z typem `int`. W związku z tym interpreter wie, że funkcja bez wątpienia wypluwa `int`.

## 3. Zastosowanie w Klasach (`Generic`)

Często `TypeVar` używa się w połączeniu z klasą bazową `Generic` do tworzenia własnych bazowych klas i generycznych struktur danych (np. własna ulepszona wersja listy, kolejki albo cache).

```python
from typing import TypeVar, Generic

T = TypeVar('T')

class Box(Generic[T]):
    def __init__(self, item: T):
        self.item = item
        
    def get_item(self) -> T:
        return self.item

# Typ "Box" określany jest precyzyjnie podczas jego tworzenia
int_box = Box[int](123)
str_box = Box[str]("Hello")

# Mypy zgłosi błąd, jeśli spróbujemy:
# bad_box = Box[int]("tekst") 
```

## 4. Ograniczanie Typów (Type Constraints)

Czasami chcemy, aby zmienna generyczna mogła przyjmować **tylko** konkretnie wymienione typy (np. żeby nie przekazano nam typu string do funkcji matematycznej). Możemy to zrobić, podając dozwolone typy zaraz po nazwie przypisywanej `TypeVar`.

```python
from typing import TypeVar

# T_Num może być tylko intem lub floatem
T_Num = TypeVar('T_Num', int, float)

def double_value(val: T_Num) -> T_Num:
    return val * 2

print(double_value(10))      # OK, zwraca int (20)
print(double_value(3.14))    # OK, zwraca float (6.28)
# double_value("tekst")      # Błąd sprawdzenia typów (Mypy) - str jest niedozwolony
```

Rozwiązuje to problem niechcianych operacji np. na znakach, ale należy pamiętać, że definiujemy tu całkowicie ściśle określoną listę dozwolonych typów.

## 5. Granice Typów (Type Boundaries - parametr `bound`)

Czym innym są ścisłe ograniczenia (Constraints), a czym innym wyznaczenie **górnej granicy (Bound)**. Parametr `bound` informuje, że przypisywany typ musi być **określoną klasą lub ewentualnie dowolną jej podklasą**.

```python
from typing import TypeVar

class Animal:
    def speak(self) -> str:
        return "..."

class Dog(Animal):
    def speak(self) -> str:
        return "Woof!"

class Cat(Animal):
    def speak(self) -> str:
        return "Meow!"

# T_Animal musi być klasą Animal LUB CZYMKOLWIEK, CO DZIEDZICZY po Animal!
T_Animal = TypeVar('T_Animal', bound=Animal)

def make_animal_speak(animal: T_Animal) -> T_Animal:
    print(animal.speak())
    return animal  # Zwraca nam dokładnie ten sam typ animala, jaki wszedł

dog = Dog()
# Typy się zgadzają: podajemy "Dog", odzyskujemy zmienną oznaczaną jako "Dog"
same_dog = make_animal_speak(dog) 
```

🤔 **Dlaczego nie napisać po prostu `def make_animal_speak(animal: Animal) -> Animal:`?**
Dlatego, że gdybyśmy tak napisali, zwracany wynik to zawsze byłaby ogólna klasa `Animal`. Jeśli przesłalibyśmy `Dog`, system uwidziałby wynik jako `Animal`, przez co stracilibyśmy dostęp do specyficznych psich metod (np. `dog.fetch_stick()`).
Dzięki zdefiniowaniu `TypeVar(bound=Animal)` – typ jest dynamiczny, ale z gwarancją bazy! Wrzucony `Dog` generuje na wyjściu instancję `Dog`.

## 6. Kowariancja (`covariant`) i Kontrawariancja (`contravariant`)

To najbardziej zaawansowane tematy, na co dzień rzadziej wykorzystywane jako "czysty Python". Domyślnie zmienne typu `TypeVar` są **inwariantne** (niezmienne / sztywne). Oznacza to, że np. `List[Dog]` **nie jest** uznawana odgórnie za poprawny przekaźnik jako `List[Animal]`.
Dlaczego? Lista zwierząt to nie jest technicznie rzecz biorąc lista psów. Do ogólnej listy zwierząt moglibyśmy chcieć próbować za chwilę dorzucić kota (`list.append(Cat())`), a jeżeli oryginalnie była to lista przyjmująca `Dog`, to rozsadzilibyśmy tożsamość naszej struktury typów!

Kowariancja i Kontrawariancja naprawiają tę lukę dla sytuacji typu interfejsy z odczytem/zapisem:

- `covariant=True`: Pozwala używać klas pochodnych w miejscu klasy bazowej ("Producent" - jedynie odczytujemy. Np. odczytywanie "Zwierzęta" z Psa nam nic nie zepsuje).
- `contravariant=True`: "Konsument" (Zapisywanie).

```python
# Tak definiuje się takie zaawansowane relacje typów
T_Co = TypeVar('T_Co', covariant=True)
T_Contra = TypeVar('T_Contra', contravariant=True)
```

## 7. Przełom: Nowa składnia w Pythonie 3.12 (PEP 695)

Warto wiedzieć, że w Pythonie 3.12 wywrócono nieco ten system (na plus!), wprowadzając bardzo odchudzoną, nowoczesną natywną składnię do typów generycznych znanych z C#, Typescriptu i C++. Oznacza to de facto **nie używanie** już ręcznych instrukcji `TypeVar` z racji istnienia dedykowanych symboli!

**Przed 3.12:**

```python
from typing import TypeVar

T = TypeVar('T')

def get_first(items: list[T]) -> T:
    return items[0]
```

**Python 3.12+ (Zupełnie bez wsparcia klasy modułu `typing`!):**

```python
def get_first[T](items: list[T]) -> T:
    return items[0]
```

W przypadku klas, a także `constraints` oraz bazy (`bound` z punktu 5), kod wygląda niesamowicie elegancko:

```python
class Box[T]:  # Już nie ma Generic[T]! 
    def __init__(self, item: T):
        self.item = item

# Z ograniczeniem "bound":
def make_speak[T: Animal](animal: T) -> T:
    print(animal.speak())
    return animal

# Z ograniczeniami "constraints":
def double_val[T: (int, float)](val: T) -> T:
    return val * 2
```

Mimo drastycznego ułatwienia w Python 3.12 standardowy mechanizm `TypeVar` jest kluczowy do zrozumienia, ponieważ występuje na porządku dziennym starszych aplikacji, w bibliotekach o szerokim wsparciu (np. zachowujących kompatybilność od Python 3.8 wzwyż) i jest głównym sercem całego silnika generyków na jakim oparty jest backend typingów w języku Python.
