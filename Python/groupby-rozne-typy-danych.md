# Grupowanie (GroupBy) w Pythonie przy użyciu standardowych bibliotek

W języku Python (bez użycia bibliotek takich jak `pandas`) operację grupowania można wykonać na dowolnej strukturze iterowalnej (lista, krotka, zbiór, słownik) za pomocą dwóch głównych narzędzi ze standardowej biblioteki:
1. `itertools.groupby` - narzędzie bardziej funkcyjne, które **wymaga** wcześniejszego posortowania danych po kluczu, według którego będziemy grupować.
2. `collections.defaultdict` - podejście bardziej uniwersalne i zazwyczaj łatwiejsze w złożoności czasowej $O(N)$, ponieważ nie wymaga sortowania $O(N \log N)$.

Poniżej przedstawiono przykłady grupowania dla różnych typów struktur danych: list, zagnieżdżonych list, zbiorów oraz słowników. Omawiane techniki wykorzystują powszechne wzorce w Pythonie i świetnie sprawdzają się na rozmowach rekrutacyjnych.

## 1. Grupowanie elementow listy
Gdy mamy prostą listę, możemy grupować jej elementy np. według parzystości lub ich długości (jeśli są to stringi). Najwygodniej w tym przypadku użyć biblioteki pre-definiowanych struktur `collections`.

```python
from collections import defaultdict
from itertools import groupby

numbers = [1, 2, 3, 4, 5, 6, 7, 8]

# Approach 1: collections.defaultdict (Recommended - no sorting required)
grouped_by_parity_dict = defaultdict(list)
for num in numbers:
    # Key is '0' for even, '1' for odd
    grouped_by_parity_dict[num % 2].append(num)
    
print("Defaultdict result:", dict(grouped_by_parity_dict))
# Output: {1: [1, 3, 5, 7], 0: [2, 4, 6, 8]}

# Approach 2: itertools.groupby (Requires sorting first!)
# We sort by the same key we will group by
sorted_numbers = sorted(numbers, key=lambda x: x % 2)
grouped_by_parity_iter = {
    key: list(group) for key, group in groupby(sorted_numbers, key=lambda x: x % 2)
}

print("Itertools groupby result:", grouped_by_parity_iter)
# Output: {0: [2, 4, 6, 8], 1: [1, 3, 5, 7]}
```

## 2. Grupowanie zagnieżdżonych list (list of lists)
Przypadek niezwykle częsty gdy operujemy na danych z bazy SQL pobranych jako krotki bądź wierszach z odczytanego pliku CSV.

```python
from collections import defaultdict
from itertools import groupby

# List of lists: [id, name, department]
employees = [
    [1, "Alice", "IT"],
    [2, "Bob", "HR"],
    [3, "Charlie", "IT"],
    [4, "Dave", "Finance"],
    [5, "Eve", "HR"]
]

# Approach 1: defaultdict
grouped_employees_dict = defaultdict(list)
for emp in employees:
    department = emp[2]
    grouped_employees_dict[department].append(emp)

print("Defaultdict grouped by department:", dict(grouped_employees_dict))

# Approach 2: itertools.groupby
# Sort by department first, otherwise groupby won't aggregate non-adjacent duplicates!
employees.sort(key=lambda x: x[2]) 
grouped_employees_iter = {
    department: list(group) 
    for department, group in groupby(employees, key=lambda x: x[2])
}

print("Itertools grouped by department:", grouped_employees_iter)
```

## 3. Grupowanie zbiorów (Sets)
Zbiór (`set`) w Pythonie nie ma zdefiniowanej kolejności. Ponieważ `itertools.groupby` jest wrażliwy na ułożenie elementów obok poczucia, element taki i tak musiałby zostać posortowany na listę przed agregacją. Dlatego `defaultdict` sprawdza się tutaj idealnie - iterujemy prosto po elementach bez marnowania czasu na układanie.

```python
from collections import defaultdict

words_set = {"apple", "banana", "cherry", "avocado", "blueberry", "date"}

# Grouping by the first letter using defaultdict
grouped_words = defaultdict(set) # We can collect grouped items into sets directly!
for word in words_set:
    first_letter = word[0]
    grouped_words[first_letter].add(word)

print("Grouped set elements:", dict(grouped_words))
# Output: {'a': {'apple', 'avocado'}, 'b': {'blueberry', 'banana'}, 'c': {'cherry'}, 'd': {'date'}}
```

## 4. Grupowanie słowników (Dicts)
Zależnie od logiki biznesowej, możemy chcieć grupować strukturę po kluczach, po określonych polach wartości, a niekiedy odwracać słownik "na lewą stronę" grupując oryginalne klucze według ich pod-wartości. Operujemy wtedy na enumeracji `dict.items()`.

```python
from collections import defaultdict

# Dictionary of student initials and their final grades
students_grades = {
    "JD": "A",
    "AS": "B",
    "MW": "A",
    "KL": "C",
    "RT": "B"
}

# Grouping dictionary keys (students) by their values (grades)
students_by_grade = defaultdict(list)
for student, grade in students_grades.items():
    students_by_grade[grade].append(student)

print("Students grouped by grade:", dict(students_by_grade))
# Output: {'A': ['JD', 'MW'], 'B': ['AS', 'RT'], 'C': ['KL']}
```

## Podsumowanie i wybór

1. **`collections.defaultdict`** ⭐️ Najlepszy wybór do grupowania w locie bez użycia bibliotek analitycznych. Działa naturalnie dla każdego z iterowalnych typów (słowników, krotek, itp) i osiąga stały czas rzędu $O(N)$, ponieważ korzysta ze zoptymalizowanego mechanizmu tablicy mieszającej pod spodem. Eliminuje on też błędy `KeyError`.
2. **`itertools.groupby`** Wbudowany mechanizm funkcyjny. Główną wpadką rekrutacyjną i "haczykiem" z nim związanym jest próg wejścia jako **konieczność wcześniejszego posortowania $O(N \log N)$ danych według klucza grupowania**. Metoda ta jedynie porównuje elementy będące tuż obok siebie.

---
Związane zagadnienia:
- [Wbudowane funkcje i itertools](biblioteka-functools-python.md)
- [Struktury oparte na hashach](w-python-wymień-struktury-danych-oparte-na-technice-haszowania-zawartości-strukt.md)
