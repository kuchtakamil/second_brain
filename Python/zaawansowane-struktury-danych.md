# Zaawansowane struktury danych w Pythonie (poza list, dict, set)

Python oferuje znacznie więcej wbudowanych struktur danych niż tylko podstawowe `list`, `dict`, `set` czy `tuple`. Większość z nich znajduje się w module `collections` lub jako osobne moduły (np. `heapq`, `array`, `bisect`). Korzystanie z nich pozwala na pisanie bardziej wydajnego i czytelnego kodu, ponieważ są zoptymalizowane pod kątem konkretnych zadań.

## Kiedy stosować zaawansowane struktury?

- Gdy potrzebujesz szybkiego dodawania/usuwania elementów z obu stron kolekcji (np. kolejki, bufory).
- Gdy potrzebujesz utrzymać elementy w posortowanym porządku i szybko pobierać najmniejszy element (kolejki priorytetowe).
- Gdy zależy Ci na pamięci lub specyficznym zachowaniu domyślnym słownika.
- Kiedy chcesz grupować lub zliczać elementy w elegancki sposób.

---

## 1. `deque` (Double-Ended Queue) - moduł `collections`

`deque` to kolejka dwukierunkowa. Można myśleć o niej jak o liście, ale zoptymalizowanej pod kątem szybkiego dodawania i usuwania elementów **z obu końców** (złożoność czasowa $\mathcal{O}(1)$).

### Czym różni się od zwykłej listy?
W zwykłej liście (`list`) wstawianie lub usuwanie z końca (metody `append()` i `pop()`) jest szybkie ($\mathcal{O}(1)$). Jednak wstawianie lub usuwanie z początku listy (`insert(0, val)` lub `pop(0)`) wymaga przesunięcia wszystkich pozostałych elementów w pamięci, co daje złożoność $\mathcal{O}(N)$. W przypadku `deque` operacje te zawsze trwają $\mathcal{O}(1)$.
Z kolei dostęp do elementów w środku (np. `lista[50]`) jest szybszy w zwykłej liście (stały czas $\mathcal{O}(1)$) niż w `deque` ($\mathcal{O}(N)$).

### Jak `deque` działa pod spodem?
W implementacji referencyjnej Pythona (CPython) lista to **ciągła tablica wskaźników** w pamięci. Z tego powodu dodanie czegoś na początek wymaga przesunięcia całego bloku w prawo. 

Z kolei `deque` jest zaimplementowane jako **podwójnie kierunkowa lista bloków (tzw. chunków)**. 
- Każdy taki blok (węzeł listy kierunkowej) to tablica o stałym rozmiarze (zazwyczaj mieści 64 wskaźniki na obiekty).
- Kiedy robisz `appendleft()`, Python sprawdza pierwszy (najbardziej wysunięty na lewo) blok.
- Jeśli jest w nim miejsce, po prostu wpisuje tam nowy element.
- Jeśli blok jest pełny, Python alokuje w pamięci nowy blok (dla kolejnych 64 elementów), dowiązuje go na początek jako nowy "lewy koniec" (dzięki wskaźnikom podwójnie kierunkowej listy) i umieszcza w nim nowy element.
Dzięki tej architekturze (lista powiązanych ze sobą tablic o stałym rozmiarze) nigdy nie ma potrzeby kopiowania i przesuwania wszystkich elementów w pamięci. Dlatego dodawanie i usuwanie na krańcach jest zawsze niezwykle szybkie $\mathcal{O}(1)$.

### Przykład użycia

```python
from collections import deque

# Inicjalizacja
d = deque(['b', 'c', 'd'])

# Szybkie dodawanie na końce O(1)
d.append('e')      # dodaje na prawo
d.appendleft('a')  # dodaje na lewo

print(d)  # deque(['a', 'b', 'c', 'd', 'e'])

# Szybkie usuwanie z końców O(1)
right_item = d.pop()
left_item = d.popleft()

print(d)  # deque(['b', 'c', 'd'])

# Można też określić maksymalną długość (starsze elementy są usuwane automatycznie)
fixed_d = deque(maxlen=3)
fixed_d.extend([1, 2, 3])
fixed_d.append(4)
print(fixed_d) # deque([2, 3, 4], maxlen=3)
```

---

## 2. `heapq` (Kopiec binarny / Kolejka priorytetowa)

Moduł `heapq` nie dostarcza nowej struktury danych w postaci obiektu, ale zbiór algorytmów (funkcji) działających na zwykłej liście, aby zachowywała się jak **kopiec min-heap** (gdzie najmniejszy element jest zawsze pod indeksem 0).

### Dlaczego warto?
Jeśli musisz często znajdować i wyciągać najmniejszy (lub największy) element z dynamicznie zmieniającej się kolekcji, sortowanie całej listy ($\mathcal{O}(N \log N)$) po każdym dodaniu jest nieefektywne. Wstawienie do kopca lub pobranie minimum kosztuje zaledwie $\mathcal{O}(\log N)$.

### Przykład użycia

```python
import heapq

data = [5, 1, 9, 3, 7]
heapq.heapify(data)  # Transformacja zwykłej listy w kopiec w czasie O(N)
print(data)          # [1, 3, 9, 5, 7] - zauważ, że data[0] to najmniejszy element

# Wstawienie elementu O(log N)
heapq.heappush(data, 2)

# Pobranie najmniejszego elementu O(log N)
smallest = heapq.heappop(data)
print(smallest)  # 1
```

---

## 3. Inne ważne struktury z `collections`

Chociaż nie zawsze całkowicie zmieniają one to, co robi np. lista czy słownik, dodają ogromną użyteczność.

### `Counter` (Multizbiór)
Rozszerzenie słownika zoptymalizowane do zliczania elementów. Zamiast pisać pętle iterujące i zwiększające licznik, `Counter` robi to w jednej linijce.
Więcej szczegółów: [Counter w Pythonie](python-counter-multizbiór.md).

```python
from collections import Counter

word_counts = Counter("abracadabra")
print(word_counts)                # Counter({'a': 5, 'r': 2, 'b': 2, 'c': 1, 'd': 1})
print(word_counts.most_common(2)) # [('a', 5), ('r', 2)]
```

### `defaultdict`
Słownik, który nie rzuca `KeyError` gdy odwołamy się do nieistniejącego klucza, ale automatycznie inicjalizuje go domyślną wartością (np. listą, zerem).
Więcej: [Wyjaśnienie defaultdict](wyjaśnienie-defaultdict-w-pythonie.md).

```python
from collections import defaultdict

# Automatycznie tworzy pustą listę dla nowego klucza
grupy = defaultdict(list)
grupy['owoce'].append('jabłko') 
```

### `namedtuple`
Szybka alternatywa dla prostych klas (przechowujących tylko dane). Tworzy "krotkę z nazwanymi polami", dzięki czemu zamiast `osoba[0]` możesz napisać `osoba.imie`. Zajmuje tyle samo pamięci co zwykła krotka (jest bardzo oszczędna) i jest niemutowalna.

```python
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])
p = Point(10, 20)
print(p.x) # 10
```

### `ChainMap`
Służy do logicznego łączenia wielu słowników (bez ich fizycznego kopiowania) w jeden widok, w którym odbywa się wyszukiwanie.
Więcej: [ChainMap w Pythonie](chainmap-w-python.md).

---

## 4. Dodatkowe moduły

### `array` (tablice typowane)
Podczas gdy Pythonowe listy mogą przechowywać elementy różnych typów, co może pochłaniać dużo pamięci, moduł `array` dostarcza tablice przechowujące wyłącznie dane jednego, konkretnego typu (np. tylko liczby całkowite lub tylko floaty, podobnie jak w C). Są one znacznie bardziej oszczędne pamięciowo przy wielkich zbiorach liczbowych niż `list`.

```python
import array
# 'i' oznacza signed integer
arr = array.array('i', [1, 2, 3, 4, 5]) 
```

### `bisect`
Podobnie jak `heapq`, to moduł działający na listach. Służy do utrzymywania posortowanej listy poprzez wykorzystanie wyszukiwania binarnego ($\mathcal{O}(\log N)$) do znajdowania odpowiedniego miejsca wstawienia nowego elementu, bez konieczności ponownego sortowania całości.
