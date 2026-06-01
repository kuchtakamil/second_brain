# Wyjaśnienie defaultdict w Pythonie

**Data:** 2025-12-03

---

**User:**

Na przykładach wyjaśnij defaultdict w Python

---

**Assistant:**

`defaultdict` pochodzi z modułu `collections` i działa jak zwykły słownik, ale jeśli odwołasz się do nieistniejącego klucza, automatycznie tworzy dla niego wartość domyślną. Dzięki temu nie trzeba sprawdzać, czy klucz istnieje.

---

## Podstawowy przykład

```python
from collections import defaultdict

d = defaultdict(int)  # int() zwraca 0
d['a'] += 1
d['b'] += 5

print(d)   # defaultdict(<class 'int'>, {'a': 1, 'b': 5})
print(d['c'])  # 0 – klucz nie istniał, został utworzony z wartością 0
```

Tutaj `defaultdict(int)` tworzy nowe klucze z wartością `0`.

---

## Własne wartości domyślne (np. 5 lub ["2"])

Konstruktor `defaultdict` przyjmuje jako pierwszy argument **dowolny obiekt wywoływalny (callable)**, czyli funkcję (lub klasę), która nie przyjmuje żadnych argumentów i zwraca wartość, którą chcemy ustawić jako domyślną.

Gdy przekazujemy `int`, Python pod spodem wywołuje `int()`, co daje `0`. Gdy przekazujemy `list`, wywołuje `list()`, co daje pustą listę `[]`.

Jeśli chcemy ustawić inną domyślną wartość, np. liczbę `5` albo listę z początkowym elementem `["2"]`, najprościej jest użyć **funkcji anonimowej (lambda)**.

### Przykład 1: Domyślna wartość `5` (zamiast `0`)

```python
from collections import defaultdict

# lambda nie przyjmuje argumentów i zawsze zwraca 5
d = defaultdict(lambda: 5)

d['a'] += 1     # klucz 'a' nie istniał -> powstaje d['a'] = 5, a potem 5 + 1 = 6
print(d['a'])   # 6
print(d['b'])   # 5 (klucz nie istniał, więc dostał wartość domyślną 5)
```

### Przykład 2: Domyślna lista z początkowym elementem `["2"]` (zamiast pstej listy `[]`)

```python
from collections import defaultdict

# lambda za każdym razem tworzy nową listę z elementem "2"
grouped = defaultdict(lambda: ["2"])

grouped['a'].append("3")  # do domyślnej listy ['2'] dodajemy '3'
print(grouped['a'])       # ['2', '3']
print(grouped['b'])       # ['2'] (klucz nie istniał, pobrał nową domyślną listę)
```

> [!IMPORTANT]
> **Dlaczego musimy użyć `lambda: ["2"]`, a nie po prostu przekazać listę `["2"]`?**
>
> `defaultdict` oczekuje **obiektu wywoływalnego (funkcji)**, a nie gotowej wartości. Musi mieć możliwość *wywołania* tej funkcji za każdym razem, gdy napotka nowy klucz, aby stworzyć **nowy, niezależny obiekt w pamięci**.
> 
> Gdybyśmy mogli przekazać po prostu listę (np. `defaultdict(["2"])`), to każdy nowy klucz wskazywałby na **tę samą listę w pamięci**. Zmiana listy pod jednym kluczem modyfikowałaby dane pod wszystkimi innymi kluczami! Funkcja lambda (lub standardowa funkcja zdefiniowana przez `def`) gwarantuje, że przy każdym nowym kluczu wywoływana jest instrukcja zwracająca nową, świeżą instancję obiektu.

---

## Jako lista wartości pod jednym kluczem

Częsty przypadek: grupowanie elementów.

```python
from collections import defaultdict

grouped = defaultdict(list)

items = [('A', 1), ('A', 2), ('B', 3)]

for key, value in items:
    grouped[key].append(value)

print(grouped)  
# defaultdict(<class 'list'>, {'A': [1, 2], 'B': [3]})
```

Bez `defaultdict` musiałbyś sprawdzać, czy lista istnieje.

---

## Tworzenie zagnieżdżonych struktur

Możesz zdefiniować zagnieżdżone słowniki bez pilnowania kluczy:

```python
from collections import defaultdict

nested = defaultdict(lambda: defaultdict(int))

nested['users']['count'] += 1
nested['users']['active'] += 2

print(nested)
# defaultdict(<lambda>, {'users': defaultdict(<class 'int'>, {'count': 1, 'active': 2})})
```

---

## Porównanie ze zwykłym dict

Zwykły `dict`:

```python
d = {}
d['x'] += 1   # błąd: KeyError
```

`defaultdict`:

```python
from collections import defaultdict
d = defaultdict(int)
d['x'] += 1   # działa, bo tworzy x = 0, a potem zwiększa do 1
```

---

## Metoda setdefault() w zwykłym dict a defaultdict

Tak, metoda `setdefault()` wbudowana w zwykły słownik (`dict`) i klasa `defaultdict` **służą do rozwiązywania dokładnie tego samego problemu** – bezpiecznego inicjalizowania wartości pod nieistniejącym kluczem. Różnią się jednak sposobem działania, wygodą i wydajnością.

### Jak działa `dict.setdefault()`?

Metoda `setdefault(key, default)` na zwykłym słowniku działa w następujący sposób:
1. Jeśli `key` **istnieje** w słowniku – zwraca przypisaną mu wartość.
2. Jeśli `key` **nie istnieje** – dodaje go do słownika z wartością `default` i zwraca tę wartość.

### Porównanie w kodzie: grupowanie

Oba poniższe podejścia dadzą identyczny rezultat:

**1. Użycie `defaultdict`:**
```python
from collections import defaultdict
grouped = defaultdict(list)

grouped['A'].append(1)  # Domyślna lista tworzy się automatycznie
```

**2. Użycie zwykłego `dict` z `setdefault`:**
```python
grouped = {}

# Jeśli 'A' nie istnieje, tworzy listę [], a potem dodaje do niej 1
grouped.setdefault('A', []).append(1)
```

---

### Kluczowe różnice

| Cecha | `defaultdict` | `dict.setdefault()` |
| :--- | :--- | :--- |
| **Gdzie definiujemy wartość domyślną?** | Jednorazowo, przy tworzeniu całego słownika. | Przy każdym pobieraniu/modyfikacji elementu. |
| **Wymóg importu** | Tak (`from collections import defaultdict`). | Nie, działa na każdym standardowym `dict`. |
| **Wydajność w pętli** | **Wyższa** – fabryka jest wywoływana tylko wtedy, gdy klucz faktycznie nie istnieje. | **Niższa** – domyślny obiekt jest tworzony w pamięci przy każdym wywołaniu, nawet gdy klucz już istnieje! |
| **Czytelność kodu** | Znakomita przy powtarzających się operacjach (np. w pętlach). | Może prowadzić do mniej czytelnych, "przeładowanych" linii kodu. |

### Dlaczego `setdefault` może być nieoptymalne?

Spójrzmy na ten fragment:
```python
d = {}
# ... (słownik ma już tysiące elementów)
d.setdefault('istniejacy_klucz', [1, 2, 3, 4, 5])
```
Nawet jeśli `'istniejacy_klucz'` istnieje w słowniku i `setdefault` po prostu go zwróci, Python **i tak najpierw utworzy nową listę `[1, 2, 3, 4, 5]` w pamięci**, aby móc przekazać ją jako argument do metody `setdefault()`. Dopiero potem ta lista zostanie odrzucona i usunięta z pamięci przez Garbage Collector. 

W przypadku `defaultdict` przekazujesz referencję do fabryki (np. `list` lub `lambda`), która jest wywoływana **wyłącznie wtedy, gdy klucz rzeczywiście nie istnieje**.

### Kiedy używać czego?
- Wybierz `defaultdict`, gdy tworzysz nowy słownik od zera i wiesz, że będziesz wielokrotnie dodawać do niego elementy pod nieznanymi kluczami (np. przy grupowaniu danych czy zliczaniu).
- Wybierz `.setdefault()`, gdy pracujesz na już istniejącym, standardowym słowniku (którego nie chcesz lub nie możesz konwertować) i musisz jednorazowo zabezpieczyć pobranie/dodanie jakiejś wartości domyślnej.

---

Jeśli chcesz, mogę pokazać jeszcze przykłady z użyciem `set`, z liczeniem częstotliwości albo bardziej praktyczne zastosowania.