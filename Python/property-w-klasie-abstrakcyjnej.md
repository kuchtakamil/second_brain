# Dlaczego property w klasie abstrakcyjnej (@property i @abstractmethod)

## Krótkie podsumowanie
Zastosowanie kombinacji dekoratorów `@property` oraz `@abstractmethod` w klasach abstrakcyjnych (dziedziczących po `ABC` z modułu `abc`) służy do **wymuszenia** na klasach potomnych (dziedziczących) zdefiniowania konkretnych atrybutów (takich jak `name` czy `embedding_dim`). 

## Dlaczego jest to ważne / Kiedy ma zastosowanie?
Gdybyśmy w klasie bazowej utworzyli po prostu zwykłe pola (np. przypisali je w konstruktorze `__init__` do wartości takich jak `None` czy `0`), to w Pythonie nie mielibyśmy wbudowanego, ścisłego mechanizmu do wymuszenia, by klasa dziedzicząca podawała dla nich swoje wartości.

Użycie takiego zapisu:
```python
from abc import ABC, abstractmethod

class BaseEmbedder(ABC):
    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def embedding_dim(self):
        pass
```
gwarantuje nam, że **nie uda się** utworzyć instancji klasy potomnej, jeśli programista zapomni zdefiniować te pola. Od razu przy próbie utworzenia obiektu zostanie wyrzucony jasny błąd (wyjątek): `TypeError: Can't instantiate abstract class with abstract methods`.

## Jak to działa w praktyce? (Przykłady)

Gdy kontrakt nakłada na nas konieczność implementacji `@abstractmethod` za pomocą `@property`, klasa bazowa informuje: *„Potomku, musisz dostarczyć pole lub właściwość `name` oraz `embedding_dim`”*.

Klasa potomna może go spełnić na dwa sposoby:

### Sposób 1: Zdefiniowanie jako zwykły atrybut klasy (najprostsze)
Od Pythona 3.3+, aby zrealizować abstrakcyjne `property`, wystarczy zadeklarować zwykłe pole (atrybut klasy).
```python
class MyEmbedder(BaseEmbedder):
    name = "my_custom_embedder"
    embedding_dim = 128

# Tworzenie obiektu zadziała bez błędów!
embedder = MyEmbedder()
```

### Sposób 2: Zaimplementowanie z użyciem własnego @property (kiedy np. wymiar jest dynamiczny)
```python
class DynamicEmbedder(BaseEmbedder):
    def __init__(self, dim):
        self._dim = dim

    @property
    def name(self):
        return "dynamic_embedder"

    @property
    def embedding_dim(self):
        return self._dim

# Również działa bez błędów i realizuje interfejs!
embedder = DynamicEmbedder(256)
```

### Dlaczego i kiedy warto stosować Sposób 2 (@property) zamiast Sposobu 1?
Skoro Sposób 1 (zwykłe atrybuty klasy) jest najprostszy i najkrótszy, to dlaczego w ogóle używać Sposobu 2? Wynika to z przewag, jakie dają dekoratory `@property` i obiektowe podejście do programowania:

1. **Dynamiczne wartości (obliczane "w locie"):** 
   Bardzo często np. wymiar embeddingu (`embedding_dim`) nie jest "sztywną" stałą znaną w momencie pisania kodu. Może zależeć od parametrów z jakimi zainicjalizowano model (w `__init__`), rozmiaru pliku wczytanego z dysku, lub konkretnego wariantu modelu. `@property` pozwala zwracać zmienną instancji (np. zapisaną jako `self._dim`) lub obliczyć ją w danej chwili. Sposób 1 działa świetnie tylko dla prostych i sztywnych "stałych" wartości.

2. **Ochrona przed nadpisaniem (Read-only):** 
   Kiedy definiujesz atrybut za pomocą samego odczytu w `@property` (czyli bez definiowania tzw. `@name.setter`), pole to zyskuje automatyczną ochronę przed modyfikacją.
   - **Sposób 1**: Programista korzystający z Twojego API może w innej części pliku przypadkowo wpisać `embedder.embedding_dim = -500`. Zmieni na stałe wymiar, po czym cała późniejsza faza uczenia/wnioskowania wybuchnie w niewyjaśnionych okolicznościach.
   - **Sposób 2**: Kod `embedder.embedding_dim = -500` od razu w rzuci jasny, zabezpieczający wyjątek: `AttributeError: can't set attribute`. Jest to świetna realizacja zasady "bezpiecznie zamkniętej architektury" (hermetyzacja).

3. **Leniwe Ładowanie (Lazy Loading):**
   Gdyby atrybut `name` wymagał wykonania kosztownego zapytania sieciowego do zewnętrznego API, możesz zaprogramować to wewnątrz `@property`. Informacja zostałaby pobrana (i ew. zbuforowana w zmiennej prywatnej) dopiero w momencie, w którym inny kod po raz pierwszy będzie chciał odczytać wartość `embedder.name`.

### Co by było, gdyby zastosowano zwykłe pola bez dekoratorów?
Gdybyśmy zamiast dekoratorów stworzyli zwykłe pola:
```python
class BaseEmbedder(ABC):
    def __init__(self):
        self.name = None
        self.embedding_dim = 0
```
Następnie programista stworzyłby nową klasę dziedziczącą, ale zapomniałby nadpisać wartości w jej inicjalizatorze `__init__`:
```python
class BadEmbedder(BaseEmbedder):
    pass # zapomniałem ustawić self.name i self.embedding_dim

# Program nie zaprotestuje! Obiekt zostanie stworzony pomyślnie.
bad_embedder = BadEmbedder()
```
Obiekt zostałby utworzony be problemu, ale błąd wyszedłby na jaw o wiele później, gdzieś głęboko w kodzie (np. podczas macierzowego mnożenia z fałszywym rozmiarem 0 lub próbą dostępu do modelu pod niewłaściwą nazwą `None`). Właśnie dlatego, aby chronić się przed ludzkimi pomyłkami na poziomie wejścia, wdrażany jest jawny kontrakt poprzez połączenie `@property` i `@abstractmethod`.
