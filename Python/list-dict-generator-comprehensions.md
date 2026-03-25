# List Dict Generator Comprehensions

**Data:** 2025-05-02

---

**User:**

Opisz List / dict comprehensions i generator expressions w Python

---

**Assistant:**

W Pythonie **list comprehensions**, **dict comprehensions** i **generator expressions** to zwięzłe sposoby tworzenia kolekcji danych (list, słowników lub generatorów) na podstawie istniejących iterowalnych struktur. Umożliwiają one czytelniejsze, krótsze i często bardziej wydajne zapisy niż tradycyjne pętle `for`.

---

### 1. **List Comprehension**

To sposób tworzenia listy w jednej linijce.

**Składnia:**
```python
[expression for item in iterable if condition]
```

**Przykład:**
```python
squares = [x**2 for x in range(10)]              # [0, 1, 4, 9, 16, ..., 81]
even_squares = [x**2 for x in range(10) if x % 2 == 0]  # [0, 4, 16, 36, 64]
```

---

### 2. **Dict Comprehension**

Podobna koncepcja jak list comprehension, ale tworzy słownik.

**Składnia:**
```python
{key_expr: value_expr for item in iterable if condition}
```

**Przykład:**
```python
squares = {x: x**2 for x in range(5)}     # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}
```

---

### 3. **Generator Expression**

Podobna składnia do list comprehension, ale zamiast listy zwraca **iterator (generator)** — użyteczny, gdy chcesz oszczędzać pamięć, bo elementy są obliczane na żądanie.

**Składnia:**
```python
(expression for item in iterable if condition)
```

**Przykład:**
```python
gen = (x**2 for x in range(10))       # <generator object ...>
for val in gen:
    print(val)
```

---

### Porównanie:

| Cecha                  | List comprehension | Dict comprehension | Generator expression |
|------------------------|-------------------|---------------------|-----------------------|
| Zwracany typ           | `list`            | `dict`              | `generator`          |
| Wydajność              | szybkie           | szybkie             | bardziej pamięciooszczędne |
| Obliczenia             | natychmiastowe    | natychmiastowe      | leniwe (na żądanie)  |

---

Chcesz przykłady zagnieżdżonych comprehension albo jak ich używać w praktyce np. z plikami lub API?

---

**User:**

tak, chcę oba przykłady

---

**Assistant:**

Świetnie! Oto oba przykłady: **zagnieżdżone comprehension** oraz **praktyczne zastosowanie z plikiem i API**.

---

## 🔁 **1. Zagnieżdżone Comprehension**

Możesz używać comprehension również zagnieżdżając pętle — np. do spłaszczania listy list lub tworzenia macierzy.

### Przykład: Spłaszczanie listy list
```python
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flattened = [item for row in matrix for item in row]
# Wynik: [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

### Przykład: Macierz 3x3 z kwadratami liczb
```python
squares_matrix = [[(i * 3 + j) ** 2 for j in range(3)] for i in range(3)]
# Wynik: [[0, 1, 4], [9, 16, 25], [36, 49, 64]]
```

---

## 📁 **2. Praktyczne Zastosowanie z Plikiem i API**

### ✅ List comprehension do odczytu linii z pliku i filtrowania
Plik `dane.txt` zawiera:
```
apple
banana
avocado
cherry
apricot
```

```python
with open("dane.txt") as f:
    a_words = [line.strip() for line in f if line.startswith("a")]
# Wynik: ['apple', 'avocado', 'apricot']
```

---

### 🌐 Generator expression do przetwarzania dużych danych z API

Załóżmy, że masz dużą listę użytkowników z API i chcesz przefiltrować tylko ich adresy e-mail:

```python
import requests

response = requests.get("https://jsonplaceholder.typicode.com/users")
users = response.json()

# Generator, który przetwarza tylko potrzebne dane
emails = (user["email"] for user in users if user["email"].endswith(".org"))

for email in emails:
    print(email)
```

---

Chcesz przykład z dict comprehension użyty z JSON-em albo coś bardziej złożonego jak mapowanie danych z REST API?