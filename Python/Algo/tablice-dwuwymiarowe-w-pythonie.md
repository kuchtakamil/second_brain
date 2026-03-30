# Tablice dwuwymiarowe (2D Arrays) w Pythonie

W wielu obiekto-zorientowanych językach programowania (np. C++, Java, C#) tablica dwuwymiarowa (macierz) to wbudowana struktura o stałym rozmiarze. W Pythonie **nie ma wbudowanego typu tablicy 2D**, a programiści zazwyczaj używają innych, natywnych struktur lub zewnętrznych bibliotek.

Na klasycznych rozmowach rekrutacyjnych (job interviews) w ramach zadań algorytmicznych (typu LeetCode, HackerRank), rolę tablicy dwuwymiarowej pełni **lista list** (ang. *list of lists*). Zewnętrzne biblioteki takie jak `NumPy` rzadko są dozwolone na ogólnych interview algorytmicznych, chyba że stanowisko jest stricte związane z Data Science.

---

## 1. Tworzenie tablicy 2D — Lista list

Najprostszym i najbardziej idiomatycznym (tzw. *Pythonic*) sposobem na reprezentację macierzy w czystym Pythonie jest lista, w której każdy element to inna lista (reprezentująca wiersz).

### Poprawna inicjalizacja (List Comprehension)

Aby zainicjować tablicę 2D (np. planszę do gry lub mapę) o rozmiarach `rows` na `cols`, wypełnioną zerami, należy użyć *list comprehension*.

```python
rows, cols = 3, 4

# Poprawne utworzenie tablicy 3x4 wypełnionej zerami
matrix = [[0] * cols for _ in range(rows)]

# Zmiana jednego elementu
matrix[0][0] = 1

for row in matrix:
    print(row)
    
# Wynik:
# [1, 0, 0, 0]
# [0, 0, 0, 0]
# [0, 0, 0, 0]
```

Dzięki `for _ in range(rows)` każdy wiersz jest **nowym, oddzielnym obiektem** w pamięci.

### Błędna inicjalizacja (Pułapka Shallow Copy!)

Jednym z najczęstszych błędów kandydatów, wynikającym z braku znajomości pamięci w Pythonie, jest powielenie listy w ten sposób:

```python
rows, cols = 3, 4

# BŁĄD! Tworzy tablicę z 3 referencjami do TEJ SAMEJ listy-wiersza!
bad_matrix = [[0] * cols] * rows

bad_matrix[0][0] = 1

for row in bad_matrix:
    print(row)
    
# Wynik (zmiana w jednym miejscu nadpisała wartości we wszystkich wierszach):
# [1, 0, 0, 0]
# [1, 0, 0, 0]
# [1, 0, 0, 0]
```

**Dlaczego to błąd?** Operator `*` powiela powiązania (referencje) do obiektu, a nie sam obiekt. Mamy tutaj trzy wskaźniki na tę samą wewnętrzną listę.

---

## 2. Płaska struktura (1D udające 2D)

Opcjonalnym podejściem (często stosowanym w systemach wbudowanych bądź C/C++, czasem spotykanym opcjonalnie w rozwiązaniach ze względu na lepsze *"cache locality"*) jest stworzenie jednowymiarowej listy i matematyczne obliczanie indeksów.

```python
rows, cols = 3, 4

# Tworzenie pojedynczej listy 1D o rozmiarze rows * cols
flat_matrix = [0] * (rows * cols)

# Dostęp do elementu pod (row, col) używając wzoru matematycznego:
target_row, target_col = 1, 2
flat_matrix[target_row * cols + target_col] = 5
```

---

## 3. Iteracja po elementach (Przechodzenie)

W zadaniach algorytmicznych na macierzach często musimy przeglądać każdy element.

### Podejście klasyczne (potrzebne indeksy `i`, `j`)

```python
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

# Gdy zależy nam na współrzędnych poszczególnych elementów:
for i in range(len(matrix)):
    for j in range(len(matrix[i])):
        if matrix[i][j] == 5:
            print(f"Znaleziono element w rzędzie {i}, kolumnie {j}")
```

### Z użyciem `enumerate`

Odpowiednik, który jest bardziej elegancki w Pythonie i powszechnie punktowany za czytelność.

```python
for r_idx, row in enumerate(matrix):
    for c_idx, val in enumerate(row):
        if val == 5:
            print(f"Znaleziono {val} na pozycji [{r_idx}][{c_idx}]")
```

---

## 4. Opcja Data Science: `NumPy`

Jeśli treść zadania rekrutacyjnego dopuszcza zewnętrzne biblioteki (lub stanowisko wiąże się stricte z analizą danych/ML), używamy biblioteki `NumPy`. Zapewnia ona rzeczywistą macierz 2D, przechowywaną jako ciągły blok pamięci zapisany w C, co daje kolosalne korzyści w szybkości obliczeń.

```python
import numpy as np

# Inicjalizacja prawdziwej macierzy 2D (tutaj 3x4)
np_matrix = np.zeros((3, 4), dtype=int)
np_matrix[0, 0] = 5

print(np_matrix.shape) # Zwróci tuplę (3, 4)
```

---

## Powiązane tematy

- [Zrozumienie Shallow and Deep Copy](../deep-copy-vs-shallow-copy.md)
- [List Comprehensions w Pythonie](../list-dict-generator-comprehensions.md)
- [Python Wycieki i zarządzanie pamięcią](../python-wycieki-pamieci.md)
