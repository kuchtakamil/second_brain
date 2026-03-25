# Czy w Pythonie istnieje refleksja (jak w Java)?

## Podsumowanie
Tak, w Pythonie istnieje pojęcie refleksji, a także ściśle z nią powiązanej introskopii (ang. *introspection*). W odróżnieniu od Javy, gdzie refleksja wymaga korzystania z dedykowanego API (`java.lang.reflect`) i rygorystycznego obiecania kontroli typów w czasie wykonania, w Pythonie jest ona naturalną, wbudowaną częścią języka, ponieważ Python jest językiem w pełni dynamicznym, w którym "wszystko jest obiektem".

## Dlaczego jest to ważne / Kiedy ma to zastosowanie?
- **Tworzenie frameworków i bibliotek:** ORM-y (np. SQLAlchemy), frameworki webowe (Django, FastAPI), mechanizmy wstrzykiwania zależności (Dependency Injection) polegają na analizie dostarczonych klas lub funkcji w czasie działania w celu wygenerowania logiki bazodanowej czy routingów.
- **Serializacja/Deserializacja:** Automatyczne konwertowanie typów obiektów do takich struktur jak JSON/XML i z powrotem.
- **Metaprogramowanie:** Dynamiczne tworzenie klas (za pomocą fabryk lub metaklas), a także modyfikowanie zachowań istniejących obiektów "w locie" (np. za pomocą dekoratorów).
- **Debugowanie i testowanie:** Automatyczne odnajdywanie i uruchamianie metod testowych w klasach (tak operują ramy testowe takie jak `pytest` czy `unittest`).

## Jak to działa (z przykładami)

W Pythonie refleksja (modyfikacja i dynamiczny dostęp) oraz introskopia (badanie obiektów programu w trakcie jego trwania) są realizowane głównie przy użyciu wbudowanych funkcji oraz modułu standardowego `inspect`.

### 1. Introskopia: Badanie obiektów

Możesz w każdej chwili sprawdzić typ obiektu, jego metody, atrybuty czy odczytać treść dokumentacji.

```python
class Person:
    """Klasa reprezentująca osobę"""
    def __init__(self, name: str):
        self.name = name
        
    def greet(self):
        return f"Hi, I am {self.name}"

john = Person("John")

# Sprawdzanie typu obiektu (podobnie do getClass() w Javie)
print(type(john))                  # Zwróci: <class '__main__.Person'>
print(isinstance(john, Person))    # Zwróci: True

# Listowanie zawartości - atrybutów i metod obiektu (jak java.lang.Class.getMethods())
print(dir(john))                   # Zwraca listę wszystkich elementów (m.in. 'name', 'greet', '__init__', ...)
```

### 2. Refleksja: Dynamiczny dostęp do atrybutów i ich modyfikacja

Funkcje `getattr`, `setattr`, `hasattr` i `delattr` pozwalają operować na polach i metodach na podstawie ich nazw zapisanych w zmiennej (jako string).

```python
# Sprawdzanie, czy obiekt posiada dany atrybut/metodę
if hasattr(john, "name"):
    # Pobieranie wartości relfeksyjnie (odpowiednik Field.get() w Javie)
    value = getattr(john, "name")
    print(value)                   # "John"

# Dynamiczne wskazanie i wywołanie metody (odpowiednik Method.invoke() w Javie)
method = getattr(john, "greet")
print(method())                    # "Hi, I am John"

# Dynamiczne ustawienie nowej wartości / dodanie nowego przypisanego pola (czego Java w prosty sposób nie pozwala)
setattr(john, "surname", "Smith")
print(john.surname)                # "Smith"
```

### 3. Moduł `inspect`

Moduł `inspect` to jeszcze potężniejsze narzędzie, które daje dostęp do głębokich i szczegółowych informacji m.in. o kodzie źródłowym, sygnaturach, argumentach funkcji czy wręcz stosie wywołań.

```python
import inspect

# Pobranie samego filtra dla wszystkich metod należących do danej klasy
methods = inspect.getmembers(Person, predicate=inspect.isfunction)
for name, method in methods:
    print(f"Metoda: {name}")

# Sprawdzenie sygnatury (argumentów wraz z np. Types Hints i wartościami domyślnymi) metody
signature = inspect.signature(Person.__init__)
print(f"Argumenty konstruktora: {signature}") # Zwróci: (self, name: str)
```

### 4. Słownik obiektu (`__dict__`)

Wnętrze dużej większości wbudowanych w Pythonie obiektów to w rzeczywistości zwykłe słowniki (czyli java.util.HashMap). Standardowe atrybuty (dane obiektu, a nie same funkcje) są więc przechowywane w magicznym atrybucie `__dict__`.

```python
print(john.__dict__)  # Wynik: {'name': 'John', 'surname': 'Smith'}

# Ponieważ jest to zwykły modyfikowalny słownik obiektowy, można przypisać nową daną na instancji z jego poziomu!
john.__dict__['age'] = 30
print(john.age)      # 30
```

## Podobieństwa i różnice względem Javy
| Cecha | Java (`java.lang.reflect`) | Python |
|-------|-----------------------------|--------|
| **Podejście do refleksji** | Wymagane użycie dedykowanego wbudowanego API. Często postrzegane przez developerów jako "hackowanie" silnika i z ogromnym kosztem wydajnościowym uderzenia do runtime'u. | Naturalne dla języka narzędzie (wbudowane funkcje). Różnica wydajnościowa jest mniejsza i użycie tego jest codziennością. |
| **Dostęp do klas i metod** | Zdobywamy definicję poprzez specjalny reifikowany obiekt `Class<T>` (np. `String.class`). | Klasy, definicje z metodami są traktowane równie traktowane jak zwykłe obiekty (jako tzw. *"first-class citizens"*). |
| **Modyfikacja "w locie"** | Dość trudna lub nieskończenie skomplikowana w czasie produkcji albo bez bibliotek podmieniających kod bajtowy JVM (np. *CGLib*, *ByteBuddy*, *ASM*). | Banalnie prosta w trakcie wykonywanego pliku (tzw. zjawisko *Monkey Patching*). Kodowi Pythona uścińniętym i "skompilowanym" można swobodnie dodawać, manipulować czy zamieniać przypisaną metodę w klasie nawet na jej obiekcie! |
