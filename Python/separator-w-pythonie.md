# Separator w Pythonie

**Data:** 2025-12-25

---

**User:**

defs = []
    for item in data:
        for title, content in item.items():
            if title not in exclude:
                lines = [line.strip() for line in content.splitlines() if line.strip()]
                lines.extend("------")
                defs.extend(lines)

Chcę aby pojawiał się separator ------ w każdym wewnętrznym for ale wypisuje się to w takiej formie
-
-
-
-
-
-

---

**Assistant:**

Problem jest dokładnie tutaj 👇  
```python
lines.extend("------")
```

`extend()` **traktuje argument jako iterowalny** i dodaje **każdy element osobno**.  
A że string jest iterowalny znak po znaku, to Python robi to:

```python
["-", "-", "-", "-", "-", "-"]
```

stąd masz separator wypisany linia po linii jako `-`.

---

### ✅ Poprawne rozwiązanie

Jeśli chcesz dodać **jedną linię** `"------"`, użyj `append()`:

```python
lines.append("------")
```

Całość:

```python
defs = []
for item in data:
    for title, content in item.items():
        if title not in exclude:
            lines = [line.strip() for line in content.splitlines() if line.strip()]
            lines.append("------")
            defs.extend(lines)
```

---

### 🧠 Zasada na przyszłość (łatwa do zapamiętania)

- `append(x)` → dodaje **jeden element**
- `extend(iterable)` → dodaje **wiele elementów**

```python
lst.append("abc")     # ["abc"]
lst.extend("abc")     # ["a", "b", "c"]
lst.extend(["abc"])   # ["abc"]
```

---

Jeśli chcesz, mogę też pomóc:
- wstawić separator **tylko między blokami** (a nie na końcu)
- albo zrobić to bardziej „pythonicznie” jednym wyrażeniem

---

**User:**

jakie są jeszcze inne funkcje dodające do listy?

---

**Assistant:**

W Pythonie lista ma **niewiele metod do dodawania elementów**, ale każda robi coś trochę innego. Oto pełna, praktyczna mapa 🧭

---

## 🔹 Metody *bezpośrednio* dodające elementy

### 1️⃣ `append(x)`
Dodaje **jeden element** na koniec listy.

```python
lst = [1, 2]
lst.append(3)      # [1, 2, 3]
```

✔ najczęściej używana  
✔ O(1)

---

### 2️⃣ `extend(iterable)`
Dodaje **wiele elementów** z iterowalnego obiektu.

```python
lst = [1, 2]
lst.extend([3, 4])   # [1, 2, 3, 4]
lst.extend("abc")    # [1, 2, 'a', 'b', 'c']
```

✔ szybka  
⚠️ string = znaki

---

### 3️⃣ `insert(index, x)`
Wstawia element **w konkretne miejsce**.

```python
lst = [1, 2, 3]
lst.insert(1, "X")   # [1, 'X', 2, 3]
```

⚠️ kosztowne (przesuwa elementy)

---

## 🔹 Operatory i składnia języka

### 4️⃣ `+` (konkatenacja)
Tworzy **nową listę**.

```python
a = [1, 2]
b = a + [3, 4]
```

❌ nie modyfikuje oryginału  
❌ dodatkowa alokacja

---

### 5️⃣ `+=` (in-place extend)
Działa jak `extend()`.

```python
a = [1, 2]
a += [3, 4]
```

✔ czytelne  
✔ modyfikuje listę

---

## 🔹 Mniej oczywiste / specjalne przypadki

### 6️⃣ Slice assignment
Możesz „wstrzyknąć” wiele elementów w dowolnym miejscu.

```python
lst = [1, 4]
lst[1:1] = [2, 3]   # [1, 2, 3, 4]
```

💡 bardzo elastyczne  
⚠️ mało czytelne bez komentarza

---

### 7️⃣ `list.extend()` + generator
Często spotykane w „pythonicznym” kodzie:

```python
lst.extend(x * 2 for x in range(3))
# [0, 2, 4]
```

✔ bez listy tymczasowej  
✔ dobre dla dużych danych

---

## 🔹 Czego NIE MA (częste zaskoczenie)

❌ `push()` – nie istnieje  
❌ `add()` – nie istnieje  
❌ `enqueue()` – to `collections.deque`

---

## 🔹 Kiedy czego używać (ściąga)

| Chcę… | Użyj |
|----|----|
| dodać 1 element | `append()` |
| dodać wiele | `extend()` / `+=` |
| wstawić w środek | `insert()` |
| dodać iteracyjnie | `append()` w pętli |
| wydajny FIFO/LIFO | `deque.append()` |

---

Jeśli chcesz, mogę:
- porównać **wydajność** (`append` vs `extend`)
- pokazać **idiomy z list comprehensions**
- albo powiedzieć kiedy **lista to zły wybór** (i lepiej użyć `deque`, `array`, `set`)