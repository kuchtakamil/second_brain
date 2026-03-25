# czy itemgetter jest używane wyłącznie przy sortowaniu? jeśli nie, podaj inny prz

**Data:** 8 gru 2025, 00:33:18 CET

---

**User:**

czy itemgetter jest używane wyłącznie przy sortowaniu? jeśli nie, podaj inny przykład

---

**Gemini:**

Nie, `operator.itemgetter` nie służy wyłącznie do sortowania. Jest to **funkcja wyższego rzędu** (higher-order function), która zwraca obiekt wywoływalny (callable). Jej zadaniem jest pobranie elementu (lub elementów) z przekazanego jej obiektu przy użyciu metody `__getitem__` (czyli standardowego operatora nawiasów kwadratowych `[]`).

Można jej używać wszędzie tam, gdzie oczekiwana jest funkcja pobierająca dane z obiektu.

Oto trzy zaawansowane przykłady zastosowania `itemgetter` poza sortowaniem:

### 1. Ekstrakcja danych (Mapowanie)

`itemgetter` jest bardzo wydajny przy wyciąganiu konkretnych pól z listy słowników lub krotek, szczególnie w połączeniu z funkcją `map()`. Jest to szybsza alternatywa dla pętli `for` lub `list comprehension` w przypadku prostego pobierania wartości.

```
from operator import itemgetter

data = [
    {"id": 1, "name": "Alice", "role": "Admin"},
    {"id": 2, "name": "Bob", "role": "User"},
    {"id": 3, "name": "Charlie", "role": "User"}
]

# Extract only the 'name' field from each dictionary
names_iterator = map(itemgetter('name'), data)
names_list = list(names_iterator)

print(f"Extracted names: {names_list}")
# Output: Extracted names: ['Alice', 'Bob', 'Charlie']
```

### 2. Grupowanie danych (`itertools.groupby`)

To jedno z najważniejszych zastosowań w przetwarzaniu danych. Aby zgrupować dane (np. Twoje pliki JSON) według kategorii, funkcja `itertools.groupby` wymaga klucza, według którego nastąpi podział. `itemgetter` jest tutaj standardowym rozwiązaniem.

*Uwaga: `groupby` wymaga, aby dane były wcześniej posortowane według tego samego klucza.*

```
from operator import itemgetter
from itertools import groupby

data = [
    {"item": "Kleenex", "category": "Doctor"},
    {"item": "Scalpel", "category": "Doctor"},
    {"item": "Beer", "category": "Restaurant"},
    {"item": "Burger", "category": "Restaurant"}
]

# Grouping by 'category'
# itemgetter('category') is passed as the key function
grouper = groupby(data, key=itemgetter('category'))

print("--- Grouping Results ---")
for key, group in grouper:
    items = list(group)
    print(f"Category: {key}, Count: {len(items)}")
    
# Output:
# Category: Doctor, Count: 2
# Category: Restaurant, Count: 2
```

### 3. Pobieranie wielu wartości jednocześnie (Transformacja struktury)

Jeśli przekażesz do `itemgetter` więcej niż jeden argument, zwróci on funkcję, która wyciąga te wartości i zwraca je jako krotkę (`tuple`). Jest to niezwykle przydatne przy konwersji listy słowników na listę krotek (np. w celu zapisu do bazy danych SQL lub pliku CSV bez nagłówków).

```
from operator import itemgetter

record = {"id": 101, "name": "Tablet", "price": 299.99, "stock": 50, "archived": False}

# Define a getter that extracts specific fields in a specific order
# effectively filtering and reordering the data
fields_extractor = itemgetter('id', 'name', 'price')

# Apply to the record
tuple_row = fields_extractor(record)

print(f"Row for DB: {tuple_row}")
print(f"Type: {type(tuple_row)}")

# Output:
# Row for DB: (101, 'Tablet', 299.99)
# Type: <class 'tuple'>
```

### Dlaczego warto używać `itemgetter` zamiast `lambda`?

Choć `lambda x: x['key']` robi to samo, `itemgetter` ma przewagę techniczną:

1. **Wydajność:** Jest zaimplementowany w języku C, co eliminuje narzut związany z interpretacją kodu Pythona (bytecode overhead) przy każdym wywołaniu funkcji. Przy milionach rekordów różnica jest zauważalna.
2. **Serializacja (Pickling):** Obiekty `itemgetter` można łatwo serializować (pickle), co jest kluczowe w obliczeniach wieloprocesorowych (`multiprocessing`), gdzie funkcje lambda często powodują błędy.

Would you like to see a performance benchmark comparing `itemgetter` vs `lambda`?