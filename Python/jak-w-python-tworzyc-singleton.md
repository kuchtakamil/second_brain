# Jak w Pythonie tworzyć Singleton?

Singleton to wzorzec projektowy, który gwarantuje, że dana klasa ma tylko jedną instancję, oraz zapewnia globalny punkt dostępu do tej instancji.

## Dlaczego to jest ważne i kiedy się przydaje?

Warto używać Singletona, gdy:
- Potrzebujemy dokładnie jednego obiektu koordynującego działania w całym systemie (np. zarządzanie połączeniem z bazą danych, konfiguracja aplikacji, system logowania).
- Tworzenie obiektu jest kosztowne (np. odczyt ciężkich plików z dysku, nawiązywanie połączeń sieciowych) i chcemy to zrobić zaledwie raz, przy pierwszym odwołaniu.

## Jak to działa w praktyce?

W Pythonie istnieje kilka sposobów na implementację tego wzorca, od najprostszych po bardziej zaawansowane.

### 1. Wykorzystanie modułu (najbardziej "Pythonic" sposób)

W Pythonie moduły (`.py`) są importowane tylko w jednym egzemplarzu. Wszystkie kolejne importy w tym samym procesie używają tego samego obiektu w pamięci. Jest to najczęstszy i w 90% przypadków najlepszy sposób na Singleton.

```python
# plik: database.py
class Database:
    def __init__(self):
        self.connection = "Połączono z PostgreSQL"

# Tworzymy instancję od razu w module
db_instance = Database()
```

Użycie w innym pliku:
```python
from database import db_instance

print(db_instance.connection)
```

### 2. Nadpisanie metody `__new__`

Metoda magiczna `__new__` odpowiada za fizyczne tworzenie obiektu. Możemy w niej sprawdzić, czy instancja już istnieje, i jeśli tak, po prostu zwrócić tę już utworzoną, zamiast tworzyć nową.

```python
class SingletonNew:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # Tworzymy nowy obiekt tylko jeśli instancji jeszcze brakuje
            cls._instance = super().__new__(cls)
        return cls._instance

s1 = SingletonNew()
s2 = SingletonNew()

print(s1 is s2)  # Zwróci: True
```
*Uwaga:* Przy tym podejściu metoda `__init__` i tak zostanie wywołana przy każdym "tworzeniu" instancji wywołując `SingletonNew()`. Trzeba zachować ostrożność, by nie nadpisywać niechcący stanu obiektu.

### 3. Użycie Metaklasy (Metaclass)

Metaklasy definiują sposób tworzenia samych klas (klas dla klas). To bardzo czyste, w pełni obiektowe rozwiązanie, ponieważ pozwala ominąć problem z wielokrotnym wywoływaniem `__init__`.

```python
class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        # Sprawdzamy, czy klasa znajduje się już w słowniku instancji
        if cls not in cls._instances:
            # Tworzymy instancję używając super() tylko za pierwszym razem
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Database(metaclass=SingletonMeta):
    def __init__(self):
        print("Trwa Inicjalizacja bazy danych...")

db1 = Database()  # Wypisze: Trwa Inicjalizacja bazy danych...
db2 = Database()  # Nic nie wypisze! __init__ ominięty

print(db1 is db2)  # Zwróci: True
```

### 4. Użycie Dekoratora

Możemy również napisać prosty dekorator, który zamyka instancję w tzw. domknięciu (closure) i zwraca ją za każdym razem.

```python
def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance

@singleton
class Logger:
    def __init__(self):
        print("Tworzę loggera")

log1 = Logger()
log2 = Logger()

print(log1 is log2)  # Zwróci: True
```

### Różnica między `super().__new__(cls)` a `super(SingletonMeta, cls).__call__(...)`

Podczas implementacji Singletona można natknąć się na dwa podobne zapisy, które służą do instancjonowania obiektu, ale mają zupełnie inne konsekwencje dla metody `__init__`:

1. **`cls._instance = super().__new__(cls)`** (używane w metodzie `__new__` zwykłej klasy – Sposób 2)
Służy jedynie do alokacji pamięci dla nowego obiektu. Kłopot w tym, że po zwróceniu instancji przez `__new__`, Python **zawsze automatycznie wywołuje `__init__`** na tym obiekcie. Jeśli obiekt Singletona już istniał i został zwrócony z pamięci, jego stan zostanie nadpisany przez ponowne wykonanie inicjalizatora `__init__`.

2. **`cls._instances[cls] = super().__call__(*args, **kwargs)`** (używane w metodzie `__call__` metaklasy – Sposób 3)
Przechwytuje moment nałożenia nawiasów na klasę (np. `Database()`). Metoda `__call__` z poziomu metaklasy (czyli domyślne zachowanie `type.__call__`) robi pod spodem dwie rzeczy na raz: najpierw odpala `__new__`, a zaraz potem `__init__` utworzonego obiektu. Zatrzymując ten proces w naszej metaklasie i zwracając gotową instancję ze słownika, całkowicie omijamy wywołanie `type.__call__`. Dzięki temu **Python nie uruchomi ponownie ani `__new__`, ani `__init__`** dla pobranej z pamięci instancji.

### Różnica między `super().__new__(cls)` a `super(SingletonNew, cls).__new__(cls)`

Są to dwa zapisy robiące **dokładnie to samo**, ale pochodzące z różnych etapów rozwoju języka Python:

- **`super(SingletonNew, cls).__new__(cls)`** to starszy sposób wywołania (wymagany przed wydaniem Pythona 3). Konieczne było wtedy jawne przekazywanie do funkcji `super()` klasy bieżącej oraz pierwszego argumentu funkcji, aby jednoznacznie ustalić punkt startowy do wyszukiwania po drzewie dziedziczenia (Method Resolution Order).
- **`super().__new__(cls)`** to uproszczony, nowszy zapis, obecny w Pythonie 3. Kompilator pod maską automatycznie "chwyta" z kontekstu domyślne argumenty (nazwę klasy w której jest się aktualnie znajduje oraz pierwszy argument metody - `self` lub `cls`). Taki kod jest czytelniejszy oraz pozwala uniknąć błędów w razie zmiany nazwy klasy (nie musisz poprawiać wszystkich wywołań wewnątrz w starym stylu rzutowania).

W nowoczesnym Pythonie standardem jest stosowanie krótszej, pustej formy `super()`.

## Podsumowanie

Dla prostych rozwiązań najlepsze w Pythonie jest zostawienie obiektu jako **modułu** (sposób nr 1). Jeśli jednak potrzebujemy dziedziczenia po klasach bazowych albo rozbudowanej formy klasycznej - użycie **metaklasy** (sposób nr 3) jest najbardziej kompletnym i bezpiecznym rozwiązaniem w języku Python.
