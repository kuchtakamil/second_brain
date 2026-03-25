# Global vs Nonlocal w Pythonie

**Data:** 2025-12-25

---

**User:**

python - wyjaśnij global i nonlocal

---

**Assistant:**

Jasne — krótko, konkretnie, z przykładami 👍  

W Pythonie **`global`** i **`nonlocal`** mówią interpreterowi, **z którego zakresu (scope)** ma pochodzić zmienna, gdy **chcesz ją modyfikować**, a nie tylko odczytać.

---

## 1️⃣ `global`

### Do czego służy?
Pozwala **modyfikować zmienną zdefiniowaną na poziomie modułu (globalnym)** wewnątrz funkcji.

Bez `global` Python uzna zmienną za **lokalną**.

### Przykład
```python
counter = 0  # zmienna globalna

def increment():
    global counter
    counter += 1

increment()
print(counter)  # 1
```

### Co się stanie bez `global`?
```python
counter = 0

def increment():
    counter += 1  # ❌ UnboundLocalError

increment()
```

➡️ Python widzi przypisanie `counter += 1` i zakłada, że `counter` jest lokalna,
ale nie ma jej jeszcze przypisanej.

### Kiedy używać?
- rzadko
- raczej w małych skryptach
- **nie** w kodzie produkcyjnym (trudne testowanie, ukryte zależności)

---

## 2️⃣ `nonlocal`

### Do czego służy?
Pozwala **modyfikować zmienną z najbliższego zewnętrznego zakresu funkcji**
(czyli **nie globalnego**, tylko np. funkcji-rodzica).

Dotyczy **funkcji zagnieżdżonych**.

### Przykład
```python
def outer():
    x = 10

    def inner():
        nonlocal x
        x += 5

    inner()
    print(x)

outer()  # 15
```

### Bez `nonlocal`:
```python
def outer():
    x = 10

    def inner():
        x += 5  # ❌ UnboundLocalError

    inner()
```

➡️ Analogiczny problem jak przy `global`, tylko zakres inny.

---

## 3️⃣ `global` vs `nonlocal` — porównanie

| Cecha | `global` | `nonlocal` |
|-----|--------|-----------|
| Zakres | moduł (plik) | najbliższa funkcja zewnętrzna |
| Działa w | funkcjach | funkcjach zagnieżdżonych |
| Typowe użycie | rzadkie | closures, dekoratory |
| Dobra praktyka | ❌ raczej unikać | ✅ sensowne w closure |

---

## 4️⃣ Mentalny model (ważne)

Python szuka zmiennych w kolejności (**LEGB**):

1. **L**ocal – bieżąca funkcja
2. **E**nclosing – funkcja zewnętrzna
3. **G**lobal – moduł
4. **B**uilt-ins – `len`, `print`, itd.

- `global` → „bierz z **G**”
- `nonlocal` → „bierz z **E**”

---

## 5️⃣ Dobra praktyka (pro tip)

Zamiast `global`:
```python
def increment(counter):
    return counter + 1
```

Zamiast `nonlocal` czasem lepiej:
- obiekt (mutowalny)
- klasa
- `dataclass`

```python
def outer():
    state = {"x": 10}

    def inner():
        state["x"] += 5

    inner()
    print(state["x"])
```

---

Jeśli chcesz, mogę:
- pokazać **realny przykład z dekoratorem**
- porównać to z **Javą (closures / effectively final)**
- albo rozrysować **LEGB krok po kroku na przykładzie**