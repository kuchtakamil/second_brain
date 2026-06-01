# Czym jest `__slots__` w Pythonie?

## Krótkie podsumowanie

`__slots__` to specjalny atrybut w języku Python, który pozwala na statyczne zadeklarowanie zmiennych (atrybutów) instancji danej klasy. Użycie `__slots__` zapobiega tworzeniu się domyślnego słownika `__dict__` dla każdego nowo utworzonego obiektu. Dzięki temu program oszczędza znaczną ilość pamięci RAM i może nieznacznie przyspieszyć odczyt oraz zapis atrybutów obiektu.

## Kiedy to ma znaczenie?

- **Optymalizacja pamięci:** Użycie `__slots__` jest najbardziej widoczne, gdy tworzysz miliony małych obiektów tej samej klasy (np. węzły w drzewie binarnym, rzędy wczytane z ogromnej bazy danych, współrzędne cząsteczek w symulacji). Różnica w pamięci może być kilkukrotna.
- **Zabezpieczenie przed literówkami:** `__slots__` w pewnym sensie "blokuje" strukturę obiektu. Oznacza to, że nie można do niego dynamicznie dodawać nowych atrybutów. Jeśli programista popełni literówkę podczas przypisywania (np. napisze `self.nme = ...` zamiast `self.name = ...`), Python natychmiast wyrzuci błąd, co w normalnych klasach zostałoby po prostu zignorowane (utworzyłaby się nowa zmienna w słowniku `__dict__`).

## Jak to działa?

Domyślnie każdy obiekt w Pythonie przechowuje swoje wewnętrzne atrybuty w dynamicznym słowniku dostępnym jako atrybut `__dict__`. Słowniki w Pythonie są wysoce zoptymalizowane pod kątem szybkości działania (to tablice z haszowaniem), ale zajmują bardzo dużo pamięci z powodu swojego początkowego rozmiaru oraz konieczności obsługi potencjalnych kolizji kluczy.

Kiedy w klasie definiujemy `__slots__`, Python zamiast tworzyć ciężki słownik, rezerwuje stałą i znacznie mniejszą ilość pamięci w postaci struktury przypominającej zwykłą tablicę (array) w języku C.

### Przykład w kodzie

```python
import sys

# Klasa bez użycia slots (standardowe zachowanie)
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Klasa wykorzystująca slots
class PointSlots:
    # Deklarujemy atrybuty, które ta klasa będzie obsługiwać.
    # Używamy do tego krotki lub listy stringów.
    __slots__ = ('x', 'y')
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Tworzenie instancji
p1 = Point(1, 2)
p2 = PointSlots(1, 2)

# Dynamiczne dodawanie atrybutów
p1.z = 3  # Działa bez problemu - trafia do słownika p1.__dict__

try:
    p2.z = 3  # Rzuca błąd! Atrybut 'z' nie jest wpisany w __slots__
except AttributeError as e:
    print(f"Błąd: {e}")  # Wypisze błąd o braku atrybutu 'z'

# Wymiar pamięciowy domyślnego słownika
print(f"Rozmiar p1.__dict__: {sys.getsizeof(p1.__dict__)} bajtów")
# p2 w ogóle nie posiada atrybutu __dict__!
```

## Czego Python NIE tworzy, gdy używamy `__slots__`?

Kiedy klasa definiuje atrybut `__slots__`, Python optymalizuje alokację pamięci dla obiektów, pomijając tworzenie ukrytych struktur danych, które normalnie towarzyszą każdej instancji. Konkretnie nie są tworzone:

1. **Słownik atrybutów (`__dict__`)**: 
   - Standardowo każda instancja posiada własny słownik `__dict__` przechowujący jej zmienne (dzięki czemu możemy dodawać atrybuty w locie).
   - Przy użyciu `__slots__` słownik ten **nie powstaje**. Pamięć alokowana jest statycznie (jak w tablicy) tylko na zmienne wymienione w deklaracji. Z powodu braku `__dict__` przypisywanie nowych, niezadeklarowanych atrybutów kończy się błędem `AttributeError`. (Można to obejść, dodając `'__dict__'` do listy slotów, ale to drastycznie zmniejsza zysk pamięciowy).

2. **Wskaźnik słabych referencji (`__weakref__`)**:
   - Domyślnie obiekty w Pythonie wspierają tworzenie tzw. słabych referencji (przydatnych np. w mechanizmach cachowania).
   - Instancje z użyciem `__slots__` **nie tworzą** pod spodem wskaźnika `__weakref__`, aby maksymalnie zminimalizować zużycie pamięci. Jeśli Twoja klasa ze slotami musi obsługiwać słabe referencje (często wymagają tego zewnętrzne biblioteki), musisz dodać `'__weakref__'` explicite do listy atrybutów w `__slots__`.

## Ograniczenia i Pułapki (Gotchas)

Przed użyciem `__slots__` warto znać kilka ograniczeń, przez które mechanizm ten nie jest używany "wszędzie jako domyślny":

1. **Dziedziczenie (największa pułapka!):** 
   - Jeśli klasa dziedziczy po klasie, która **nie ma** `__slots__`, zysk z pamięci przepada (Python i tak utworzy `__dict__` dla potomka). 
   - Jeśli dziedziczysz po klasie, która **ma** `__slots__`, klasa potomna również musi pusto zadeklarować `__slots__ = ()`, jeśli nie dodaje nowych atrybutów. W innym razie utworzy się w niej pusty słownik.
2. **Wielodziedziczenie:** Klasa nie może dziedziczyć po więcej niż jednej klasie z niepustą definicją `__slots__`. Doprowadzi to do wyrzucenia `TypeError` podczas inicjalizacji struktury dziedziczenia.
3. **Brak słabych referencji (`weakref`):** Instancje klas z samymi "czystymi" slotami nie mogą stać się celem referencji generowanych przez moduł `weakref`. Jeśli jest to potrzebne dla bibliotek trzecich, musisz dodać `'__weakref__'` do listy `__slots__`.
4. **Wsparcie dla Dataclass:** Jeśli używasz klas danych (`@dataclass`), od wersji Pythona 3.10 dodanie slotów to kwestia przekazania jednego parametru: `@dataclass(slots=True)`. Python wygeneruje odpowiednie definicje sam pod spodem.
