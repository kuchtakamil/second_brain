# Python globalne zmienne

**Data:** 2025-08-28

---

**User:**

Python i zmienne globalne. Dlaczego w niektórych funkcja widzę słowo global przy wybranych zmiennych.

---

**Assistant:**

W Pythonie słowo kluczowe **`global`** jest używane w funkcji wtedy, gdy chcesz **modyfikować zmienną zdefiniowaną w globalnym zakresie** (poza funkcją).  

Bez tego dopisku Python domyślnie uzna, że każda przypisana w funkcji zmienna jest **lokalna**.

### Przykład bez `global`:
```python
x = 10

def foo():
    x = 5   # to nie zmienia globalnego x, tylko tworzy nową zmienną lokalną
    print("Wewnątrz:", x)

foo()
print("Na zewnątrz:", x)
```

Wynik:
```
Wewnątrz: 5
Na zewnątrz: 10
```

Tutaj globalne `x` pozostało bez zmian, bo wewnątrz funkcji powstała **nowa lokalna zmienna** o tej samej nazwie.

---

### Przykład z `global`:
```python
x = 10

def foo():
    global x
    x = 5   # teraz zmieniamy globalne x
    print("Wewnątrz:", x)

foo()
print("Na zewnątrz:", x)
```

Wynik:
```
Wewnątrz: 5
Na zewnątrz: 5
```

Tutaj dzięki `global` faktycznie nadpisaliśmy zmienną globalną `x`.

---

### Podsumowanie
- **Bez `global`**: przypisanie wewnątrz funkcji tworzy **lokalną zmienną**.  
- **Z `global`**: przypisanie działa na **zmienną globalną**.  
- Do samego **odczytu** zmiennej globalnej `global` nie jest potrzebne:
  ```python
  x = 42
  def foo():
      print(x)  # działa, bo tylko czytamy
  foo()
  ```

---

Chcesz, żebym pokazał Ci też różnicę między `global` a `nonlocal` (które działa podobnie, ale w zagnieżdżonych funkcjach)?

---

**User:**

tak, pokaż

---

**Assistant:**

Super 👍 to teraz różnica między **`global`** a **`nonlocal`**.  

### 1. `global` – działa na zmienną w **zakresie globalnym** (cały moduł).
Pokazywałem to wcześniej, ale przypomnę w prostym przykładzie:

```python
x = 10

def foo():
    global x
    x = 20   # zmienia globalne x

foo()
print(x)  # 20
```

---

### 2. `nonlocal` – działa na zmienną z **otaczającej funkcji** (nie globalną!).
Jest używane, gdy mamy funkcje zagnieżdżone:

```python
def outer():
    x = 10
    def inner():
        nonlocal x
        x = 20   # zmienia x z funkcji outer, a nie tworzy nowe
    inner()
    print("outer:", x)

outer()
```

Wynik:
```
outer: 20
```

---

### 3. Co by się stało bez `nonlocal`?
```python
def outer():
    x = 10
    def inner():
        x = 20   # to jest lokalne x, nie rusza outer.x
    inner()
    print("outer:", x)

outer()
```

Wynik:
```
outer: 10
```

Bo bez `nonlocal` Python traktuje przypisanie jako stworzenie **nowej zmiennej lokalnej** w `inner()`.

---

### Podsumowanie
- **`global`** → odwołuje się do zmiennych na poziomie modułu.  
- **`nonlocal`** → odwołuje się do zmiennych z funkcji otaczającej (pośredni zakres).  
- Bez nich → przypisanie zawsze tworzy nową zmienną **lokalną**.

---

Chcesz, żebym przygotował mały schemat (rysunek zakresów zmiennych w Pythonie: lokalny, nonlocal, globalny, built-in)?