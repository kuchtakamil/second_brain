# Dlaczego lista nie może być kluczem w słowniku?

## Podsumowanie

W Pythonie **lista nie może być kluczem w słowniku, ponieważ jest typem mutowalnym (zmiennym)**. Słowniki opierają się na tablicach mieszających (hash tables), co wymaga, aby każdy klucz był **haszowalny (hashable)** – czyli jego wartość skrótu (hash) nie mogła ulec zmianie przez cały czas życia obiektu.

## Dlaczego jest to ważne?

Słowniki w Pythonie oferują niezwykle szybki dostęp do elementów (złożoność $O(1)$) właśnie dzięki wewnętrznemu wykorzystaniu tablic mieszających. 
Kiedy dodajesz nową parę klucz-wartość, Python na podstawie klucza wylicza unikalny *hash* i używa go do określenia miejsca w pamięci, w którym ma zostać zapisana wartość.

Jeśli klucz mógłby zostać zmodyfikowany (np. przez dodanie nowego elementu do listy po tym, jak stała się kluczem), jego nowo wyliczony *hash* również by się zmienił. W efekcie słownik "zgubiłby" miejsce, w którym pierwotnie zapisał wartość – przy próbie wyszukania zaktualizowanej listy otrzymalibyśmy inny *hash*, wskazujący na zupełnie inne, puste miejsce w pamięci. Z tego powodu Python prewencyjnie blokuje możliwość używania obiektów zmiennych jako kluczy, rzucając od razu wyjątek `TypeError: unhashable type: 'list'`.

## Kryteria, jakie musi spełniać klucz w słowniku

Aby obiekt mógł być kluczem w słowniku, musi spełniać dwa główne warunki implementacyjne, które czynią go haszowalnym:

1. **Posiadać metodę `__hash__()`**: Obiekt musi zwracać stałą, numeryczną wartość skrótu (hash), która nie ulega zmianie w trakcie całego cyklu życia obiektu.
2. **Posiadać metodę `__eq__()`**: Obiekty muszą dać się ze sobą porównać. Jeśli dwa obiekty są sobie równe (`a == b`), to ich wartości zwracane przez `hash()` również muszą być sobie bezwzględnie równe (`hash(a) == hash(b)`).

Zasady co do typów wbudowanych:
- **Typy niemutowalne (immutable) SĄ haszowalne**: `int`, `float`, `str`, `bool`, `frozenset`. Mogą być kluczami.
- **Krotki (tuple)** są haszowalne **tylko wtedy**, gdy zawierają w sobie wyłącznie elementy, które same również są haszowalne (np. `(1, 2, "a")`). Krotka zawierająca mutowalną listę, np. `(1, 2, [3, 4])`, nie jest haszowalna i nie może posłużyć jako klucz!
- **Typy mutowalne (mutable) NIE SĄ haszowalne**: `list`, `dict`, `set`. Nie mają (właściwie zaimplementowanej) metody `__hash__`.

## Jak to działa w praktyce (Przykłady)

### Próba użycia listy jako klucza (Błąd)

```python
my_dict = {}
my_list = [1, 2, 3]

# Próba przypisania wartości pod kluczem będącym listą
my_dict[my_list] = "Wartość powiązana z listą"
# Zakończy się błędem: TypeError: unhashable type: 'list'
```

### Obejście: Użycie krotki (tuple) jako klucza złożonego

Jeśli architektura wymaga klucza złożonego z wielu elementów kolekcji, po prostu użyj krotki zamiast listy, która ze swej natury jest niemutowalna i haszowalna.

```python
my_dict = {}
my_tuple = (1, 2, 3)

# Działa bez problemu, ponieważ krotka nie zmieni już swojego stanu
my_dict[my_tuple] = "Wartość powiązana z krotką"
print(my_dict[my_tuple])  # Output: Wartość powiązana z krotką
```

### Obiekty własnych klas jako klucze

Obiekty niestandardowych (zdefiniowanych przez użytkownika) klas domyślnie **są haszowalne**, a ich wartość skrótu opiera się na tożsamości obiektu w pamięci (`id()`). Oznacza to, że z marszu mogą służyć jako klucze w słowniku.

Jeśli jednak zdecydujesz się nadpisać metodę `__eq__()` w swojej klasie (np. aby obiekty były uznawane za równe, gdy mają takie same wartości atrybutów, a nie tylko gdy są tym samym obiektem w pamięci), Python automatycznie usuwa domyślną implementację `__hash__()` i instancje tej klasy stają się niehaszowalne. 

Aby ponownie mogły pełnić rolę kluczy, musisz jawnie zaimplementować własną metodę `__hash__()`. Dobrą praktyką jest w niej wyliczenie hasha na podstawie krotki (tuple) składającej się z tych samych atrybutów, które są wykorzystywane w `__eq__()`.

```python
class MyKey:
    def __init__(self, key_id, name):
        self.key_id = key_id
        self.name = name

    def __eq__(self, other):
        if not isinstance(other, MyKey):
            return NotImplemented
        # Obiekty są równe, gdy ich id i name są identyczne
        return self.key_id == other.key_id and self.name == other.name

    def __hash__(self):
        # Zwracamy hash krotki zawierającej pola decydujące o równości
        return hash((self.key_id, self.name))

# Dzięki __eq__ i __hash__ obiekty o tych samych wartościach są traktowane jak ten sam klucz
k1 = MyKey(1, "Dokument")
k2 = MyKey(1, "Dokument")

my_dict = {k1: "Znalazłem!"}
print(my_dict[k2])  # Output: Znalazłem!
```

> [!WARNING]
> **Uwaga na mutowalność własnych obiektów!** 
> Jeśli wartości pól (np. `self.name`) branych pod uwagę podczas wyliczania `__hash__()` zostaną zmienione *po* umieszczeniu obiektu jako klucza w słowniku, nowa wartość hasza nie będzie pasować do tej przypisanej podczas dodawania. Słownik zgubi wtedy taki klucz (nie odzyskasz dostępu do przypisanej mu wartości). Dlatego do `__hash__` powinno się wykorzystywać wyłącznie atrybuty niezmienne przez całe życie obiektu.

## Zobacz również
- [Struktury danych oparte na haszowaniu](w-python-wymień-struktury-danych-oparte-na-technice-haszowania-zawartości-strukt.md)
- [Krotki vs listy - pamięć i wydajność](krotki-vs-listy-pamiec-i-wydajnosc.md)
