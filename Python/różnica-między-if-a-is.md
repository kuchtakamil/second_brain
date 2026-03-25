# Różnica między if a is

**Data:** 2026-01-13

---

**User:**

czy jest różnica w python między
if my_val:
oraz
if my_val is not None:
?

---

**Assistant:**

Tak — między tymi dwoma zapisami w Pythonie istnieje **istotna różnica semantyczna**.

---

## `if my_val:`

Ten warunek sprawdza **prawdziwość (truthiness)** obiektu. Instrukcja wykona się wtedy, gdy `my_val` jest obiektem uznawanym za `True` w kontekście boolowskim.

Za `False` uznawane są m.in.:

- `None`
- `False`
- `0`, `0.0`
- `""` (pusty string)
- `[]`, `{}`, `set()`
- obiekty z `__bool__()` lub `__len__()` zwracającymi `False` / `0`

Przykład:
```python
my_val = 0
if my_val:
    print("wejdzie")
else:
    print("nie wejdzie")  # wykona się
```

---

## `if my_val is not None:`

Ten warunek sprawdza **wyłącznie**, czy zmienna **nie jest dokładnie obiektem `None`**.

Wartości takie jak `0`, `""`, `False`, `[]` **przejdą** ten warunek.

Przykład:
```python
my_val = 0
if my_val is not None:
    print("wejdzie")  # wykona się
```

---

## Kluczowa różnica w praktyce

| `my_val`      | `if my_val:` | `if my_val is not None:` |
|---------------|--------------|--------------------------|
| `None`        | ❌           | ❌                       |
| `0`           | ❌           | ✅                       |
| `""`          | ❌           | ✅                       |
| `[]`          | ❌           | ✅                       |
| `False`       | ❌           | ✅                       |
| `"text"`      | ✅           | ✅                       |

---

## Kiedy używać którego?

### Użyj `if my_val:` gdy:
- interesuje Cię, czy wartość jest „sensowna” / „niepusta”
- brak wartości, zero, pusty string i pusta kolekcja mają **to samo znaczenie**
- typowy przypadek w logice biznesowej lub walidacji wejścia

### Użyj `if my_val is not None:` gdy:
- `None` oznacza „brak wartości”
- inne wartości (np. `0`, `""`) są **poprawne i znaczące**
- często spotykane przy parametrach opcjonalnych, API, konfiguracji

Przykład idiomatyczny:
```python
def set_limit(limit: int | None):
    if limit is not None:
        apply_limit(limit)
```

---

## Ważna uwaga stylistyczna

Porównywanie do `None` **zawsze** wykonuj przez `is / is not`, nigdy przez `==`:
```python
# poprawnie
if my_val is None:

# niepoprawnie
if my_val == None:
```

---

Jeżeli chcesz, mogę też omówić:
- jak działa `__bool__` i `__len__`
- typowe bugi wynikające z `if x:` vs `if x is not None`
- różnice w kontekście `Optional` i type hintów

Wystarczy, że powiesz.

---

**User:**

co porównuje "is" a co "==" ?

---

**Assistant:**

W Pythonie `is` i `==` porównują **coś zupełnie innego**, choć często są mylone.

---

## `is` — porównanie **tożsamości obiektu**

`is` sprawdza, czy **obie zmienne wskazują dokładnie na ten sam obiekt w pamięci**.

Formalnie:
```text
id(a) == id(b)
```

Przykład:
```python
a = [1, 2, 3]
b = a
c = [1, 2, 3]

a is b      # True  (ten sam obiekt)
a is c      # False (inny obiekt)
```

Najczęstsze i poprawne użycie:
```python
if x is None:
```

Dlaczego?
- `None` jest singletonem
- w danym interpreterze istnieje **dokładnie jeden** obiekt `None`

---

## `==` — porównanie **równości wartości**

`==` sprawdza, czy obiekty są **równe logicznie**, czyli czy mają tę samą wartość / stan.

Technicznie:
- wywołuje metodę `__eq__`

Przykład:
```python
a = [1, 2, 3]
b = [1, 2, 3]

a == b      # True  (ta sama zawartość)
a is b      # False (różne obiekty)
```

Dla typów prostych:
```python
1 == 1      # True
1 is 1      # True (implementacyjny detal — nie gwarantować)
```

---

## Kluczowa tabela porównawcza

| Przypadek             | `is` | `==` |
|----------------------|------|------|
| Ten sam obiekt       | ✅   | ✅   |
| Inny obiekt, ta sama wartość | ❌ | ✅ |
| Różna wartość        | ❌   | ❌   |

---

## Dlaczego `is` **nie** zastępuje `==`?

Bo możesz mieć:
```python
a = 1000
b = 1000

a == b   # True
a is b   # False (często)
```

To, czy `a is b` zwróci `True`, zależy od:
- cache’owania obiektów (np. small integers)
- optymalizacji interpretera
- implementacji (CPython vs PyPy)

**Nie wolno** na tym polegać.

---

## Zasady praktyczne (best practices)

### Używaj `is` tylko do:
- `None`
- `True` / `False`
- sprawdzania, czy to dokładnie ten sam obiekt (np. sentinel, cache)

```python
if result is SENTINEL:
```

### Używaj `==` do:
- porównywania wartości
- liczb, stringów, kolekcji, dat, obiektów domenowych

```python
if user.role == "ADMIN":
```

---

## Częsty błąd

```python
if x == None:   # błąd stylistyczny i potencjalny logiczny
```

Dlaczego?
- `__eq__` może być przeciążone
- porównanie może dać nieoczekiwany wynik

Zawsze:
```python
if x is None:
```

---

## Jednozdaniowe podsumowanie

- `is` → **czy to ten sam obiekt**
- `==` → **czy mają tę samą wartość**

Jeśli chcesz, mogę też rozwinąć:
- jak działa interning i cache obiektów w CPythonie
- przykłady z `__eq__` i pułapki w klasach domenowych
- porównanie z `equals()` w Javie (analogia jest bardzo dobra)