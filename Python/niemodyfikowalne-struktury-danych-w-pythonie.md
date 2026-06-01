# Niemodyfikowalne (Immutable) struktury danych w Pythonie

## Podsumowanie

W Pythonie **niemodyfikowalne (immutable) struktury danych** to takie, których stan ani zawartość nie mogą zostać zmienione po ich utworzeniu w pamięci. Każda próba modyfikacji takiego obiektu (np. dodanie elementu, zmiana znaku w napisie) nie modyfikuje oryginalnego obiektu, lecz w rzeczywistości tworzy **nowy obiekt w pamięci** o nowym adresie ID.

Do wbudowanych typów immutable należą m.in. liczby (`int`, `float`), napisy (`str`), krotki (`tuple`), zamrożone zbiory (`frozenset`) oraz sekwencje bajtów (`bytes`). Standardowa biblioteka Pythona dostarcza także bardziej zaawansowane narzędzia, takie jak `MappingProxyType`, `NamedTuple` czy mrożone klasy danych (`@dataclass(frozen=True)`).

---

## Dlaczego to ważne? Zalety niemodyfikowalności

Stosowanie struktur immutable niesie za sobą ogromne zalety architektoniczne i wydajnościowe:

1. **Haszowalność (Hashability)**: Tylko obiekty o niezmiennej zawartości mogą generować stabilny skrót (*hash*) za pomocą funkcji `hash()`. Dzięki temu mogą służyć jako **klucze w słownikach (`dict`)** oraz jako **elementy zbiorów (`set`)**.
2. **Bezpieczeństwo wątkowe (Thread Safety)**: Obiekty immutable są naturalnie odporne na wyścigi (race conditions). Ponieważ żaden wątek nie może zmodyfikować ich stanu, mogą być bezpiecznie współdzielone pomiędzy procesami/wątkami bez konieczności stosowania blokad (locks).
3. **Optymalizacje pamięciowe (Memory Interning & Caching)**: CPython stosuje zaawansowane techniki współdzielenia pamięci dla obiektów immutable, takie jak *string interning* czy buforowanie małych liczb całkowitych (od -5 do 256), co drastycznie ogranicza narzut pamięciowy.
4. **Brak niepożądanych efektów ubocznych (Side Effects)**: Przekazywanie obiektów immutable do funkcji daje gwarancję, że funkcja ta nie zmodyfikuje wewnątrz naszej struktury danych.

---

## Przegląd struktur immutable w Pythonie

### 1. Typy podstawowe (Skalary)

Wszystkie typy reprezentujące pojedyncze wartości są w Pythonie niemodyfikowalne.

* **`int`, `float`, `complex`, `bool`**: Próba przypisania nowej wartości (np. `x += 1`) alokuje nową liczbę pod innym adresem w pamięci.
* **`str` (Napisy)**: Ciągi znaków w Pythonie są zawsze immutable. Każda operacja taka jak `.upper()`, `.replace()` czy konkatenacja zwraca nowy obiekt `str`.
* **`bytes`**: Immutable odpowiednik zmiennej tablicy bajtów `bytearray`.

```python
# Przykład dla typu int
x = 10
print(id(x))  # Zwraca adres w pamięci, np. 140733560731248

x += 1
print(id(x))  # Zwraca ZUPEŁNIE INNY adres w pamięci! Stary obiekt 10 pozostaje bez zmian.

# Przykład dla typu str
text = "python"
# text[0] = "P"  # Błąd! TypeError: 'str' object does not support item assignment
```

### 2. Wbudowane kolekcje i sekwencje

#### Krotka (`tuple`)
Krotka to uporządkowana sekwencja elementów. Jest immutable, co oznacza, że po jej stworzeniu nie możemy zmienić liczby jej elementów ani podmienić referencji do nich.

```python
my_tuple = (1, 2, 3)
# my_tuple[0] = 99  # Błąd! TypeError: 'tuple' object does not support item assignment
```
> [!WARNING]
> **Pułapka "pozornej niezmienności"**: Krotka jest immutable pod kątem *referencji*, które przechowuje. Jeśli jednak krotka zawiera obiekt mutowalny (np. listę), zawartość tej listy MOŻNA zmodyfikować! Szczegóły znajdziesz w sekcji o pułapkach poniżej.

#### Zamrożony zbiór (`frozenset`)
Podczas gdy standardowy `set` jest mutowalny, `frozenset` to jego niemodyfikowalna wersja. Ponieważ jest immutable, jest w pełni haszowalny i może być umieszczany jako element innego zbioru lub klucz w słowniku.

```python
frozen = frozenset([1, 2, 3])
# frozen.add(4)  # Błąd! AttributeError: 'frozenset' object has no attribute 'add'
```

#### Sekwencja liczb (`range`)
Obiekt zwracany przez `range()` reprezentuje niezmienną, leniwą sekwencję liczb całkowitych. Nie generuje wszystkich elementów w pamięci na raz, lecz oblicza je w locie i nie pozwala na ich modyfikację.

---

### 3. Zaawansowane struktury z biblioteki standardowej

#### `NamedTuple` (`collections` / `typing`)
Umożliwia tworzenie krotek z nazwanymi polami, co poprawia czytelność kodu. Zachowuje pełną niezmienność standardowych krotek.

```python
from typing import NamedTuple

class Point(NamedTuple):
    x: int
    y: int

p = Point(10, 20)
# p.x = 15  # Błąd! AttributeError: can't set attribute
```

#### Frozen Dataclasses (`dataclasses`)
Klasy danych (wprowadzone w Pythonie 3.7) można łatwo przekształcić w struktury immutable przez ustawienie parametru `frozen=True`. Python wygeneruje wtedy metody blokujące modyfikację pól oraz automatycznie zaimplementuje odpowiednie metody `__hash__`.

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class User:
    username: str
    email: str

u = User("kamil", "kamil@example.com")
# u.username = "nowy"  # Błąd! FrozenInstanceError: cannot assign to field 'username'
```

##### Czy wewnętrzne metody mrożonej klasy mogą modyfikować jej pola?

W standardowy sposób — **nie**. Jeśli zdefiniujesz metodę wewnątrz mrożonej klasy danych i spróbujesz w niej zmodyfikować pole za pomocą standardowego przypisania:

```python
@dataclass(frozen=True)
class User:
    username: str
    email: str

    def update_email(self, new_email: str):
        # Ta linia spowoduje błąd podczas wywołania metody!
        self.email = new_email  
```

Wywołanie `u.update_email("nowy@example.com")` zakończy się wyjątkiem `dataclasses.FrozenInstanceError` (będącym podklasą `AttributeError`). Dzieje się tak, ponieważ parametr `frozen=True` generuje metody `__setattr__` i `__delattr__` na poziomie całej klasy, które bezwarunkowo blokują wszelkie przypisania i usunięcia atrybutów. Mechanizm ten nie odróżnia, czy modyfikacja pochodzi z zewnątrz, czy z wnętrza samej klasy.

##### Sposoby na ominięcie blokady (Obejścia)

Chociaż modyfikowanie stanu mrożonego obiektu jest wbrew idei immutability i uważane za antywzorzec, istnieją techniczne sposoby na obejście tego ograniczenia:

1. **Użycie `object.__setattr__`**:
   Ponieważ mechanizm `frozen` opiera się na przeciążeniu metody `__setattr__` danej klasy, można go ominąć, odwołując się bezpośrednio do implementacji z klasy bazowej `object`:
   ```python
   @dataclass(frozen=True)
   class User:
       username: str
       email: str

       def force_update_email(self, new_email: str):
           # Obejście blokady poprzez bezpośrednie wywołanie metody z klasy 'object'
           object.__setattr__(self, "email", new_email)
   ```
   *Uwaga*: Jest to dokładnie ta sama technika, którą mechanizm `dataclasses` wykorzystuje wewnętrznie podczas metody `__init__` do przypisania początkowych wartości pól.

2. **Modyfikacja pól będących obiektami mutowalnymi**:
   Podobnie jak w przypadku krotek, jeśli polem mrożonej klasy danych jest obiekt mutowalny (np. lista lub słownik), metody klasy mogą modyfikować stan tego obiektu w miejscu. Sama referencja do obiektu (która jest zapisana w polu) pozostaje bez zmian:
   ```python
   from dataclasses import dataclass, field
   from typing import List

   @dataclass(frozen=True)
   class User:
       username: str
       tags: List[str] = field(default_factory=list)

       def add_tag(self, tag: str):
           # Działa! Sama lista jest mutowalna, modyfikujemy jej zawartość
           self.tags.append(tag) 
   ```

#### `MappingProxyType` (`types`)
Pozwala na stworzenie **tylko do odczytu (read-only)** wrapper'a na zwykły słownik. Zmiana za pośrednictwem proxy jest niemożliwa, natomiast jeśli oryginalny słownik ulegnie zmianie, proxy odzwierciedli tę modyfikację. Jest to idealny wzorzec do wystawiania wewnętrznych stanów klas na zewnątrz bez ryzyka ich przypadkowej modyfikacji.

```python
from types import MappingProxyType

original_data = {"host": "localhost", "port": 8000}
read_only_proxy = MappingProxyType(original_data)

# read_only_proxy["port"] = 9000  # Błąd! TypeError: 'mappingproxy' object does not support item assignment

# Zmiana oryginalnego słownika jest widoczna w proxy:
original_data["port"] = 9000
print(read_only_proxy["port"])  # Output: 9000
```

---

## Pułapki i detale implementacyjne (Gotchas)

### 1. Krotka z mutowalnymi elementami
Mimo że krotka jest niemutowalna, nie gwarantuje to głębokiej niezmienności (*deep immutability*), jeśli umieścimy w niej zmienne obiekty (np. listy).

```python
bad_tuple = (1, 2, [3, 4])
# Zmiana referencji w krotce jest zablokowana:
# bad_tuple[2] = [5, 6]  # TypeError

# Modyfikacja wewnątrz mutowalnego elementu krotki działa bez problemu!
bad_tuple[2].append(5)
print(bad_tuple)  # Output: (1, 2, [3, 4, 5])
```
*Skutek uboczny*: Ponieważ element krotki uległ zmianie, taka krotka traci swoją haszowalność. Wywołanie `hash(bad_tuple)` rzuci błąd `TypeError: unhashable type: 'list'`.

### 2. Narzut wydajnościowy przy częstych zmianach
Ponieważ każda zmiana obiektu immutable tworzy nowy obiekt w pamięci, częste modyfikacje (np. budowanie długiego stringu w pętli przez dodawanie znaków) mogą drastiwnie spowolnić program.

```python
# NIEPOLECANE (nieoptymalne - tworzy tysiące obiektów str w pamięci):
result = ""
for i in range(10000):
    result += str(i)

# REKOMENDOWANE (szybkie - buduje listę i łączy na koniec):
result = "".join(str(i) for i in range(10000))
```

### 3. CPython String Interning
Aby oszczędzać pamięć i przyspieszyć porównywanie napisów, CPython automatycznie optymalizuje przechowywanie niektórych stringów (składających się np. tylko z liter, cyfr i podkreśleń) poprzez mechanizm *internowania*. Sprawia to, że dwa identyczne stringi w kodzie mogą wskazywać na dokładnie ten sam adres w pamięci.

```python
a = "hello_world"
b = "hello_world"
print(a is b)  # True (ten sam obiekt w pamięci dzięki internowaniu)

c = "hello world!"  # Zawiera spację i wykrzyknik - CPython nie internuje automatycznie
d = "hello world!"
print(c is d)  # False (dwa różne obiekty, choć mają tę samą wartość)
```

---

## Zobacz również

* [Dlaczego lista nie może być kluczem w słowniku?](dlaczego-lista-nie-moze-byc-kluczem-w-slowniku.md)
* [Krotki vs listy - pamięć i wydajność](krotki-vs-listy-pamiec-i-wydajnosc.md)
* [Struktury oparte na haszowaniu](struktury-oparte-na-hashowaniu.md)
* [Typy danych w Pythonie i zużycie pamięci](typy-danych-w-python-i-zuzycie-pamieci.md)
