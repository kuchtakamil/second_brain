# Python Counter Multizbiór

**Data:** 2026-02-09

---

**User:**

Jak w Python działa Counter - multizbiór?

---

**Assistant:**

`collections.Counter` w Pythonie to **implementacja multizbioru (bag / multiset)** zrealizowana jako wyspecjalizowany słownik:  

> klucz = element  
> wartość = liczba wystąpień

Formalnie: `Counter` dziedziczy po `dict`.

---

## Podstawowa idea

```python
from collections import Counter

c = Counter(['a', 'b', 'a', 'c', 'a', 'b'])
print(c)
```

Wynik:

```
Counter({'a': 3, 'b': 2, 'c': 1})
```

To jest dokładnie multizbiór:
```
{ a, a, a, b, b, c }
```

---

## Tworzenie

### Z sekwencji
```python
Counter("banana")
# {'a': 3, 'n': 2, 'b': 1}
```

### Ze słownika (już jako multizbiór)
```python
Counter({'a': 4, 'b': 2})
```

### Pusty
```python
Counter()
```

---

## Dostęp jak w dict — ale z ważną różnicą

```python
c = Counter("abc")

c['a']   # 1
c['z']   # 0  <-- NIE KeyError
```

To jest kluczowe: **brak elementu = 0**, co ma sens dla multizbioru.

---

## Aktualizacja (zliczanie)

```python
c.update("aab")
# dodaje wystąpienia
```

Możesz też odejmować:

```python
c.subtract("ab")
```

---

## Operacje multizbiorowe (najciekawsze)

To jest miejsce, gdzie `Counter` przestaje być zwykłym słownikiem.

Załóżmy:

```python
c1 = Counter(a=3, b=1)
c2 = Counter(a=1, b=2)
```

### Suma multizbiorów (⊎)

```python
c1 + c2
# {'a': 4, 'b': 3}
```

### Różnica multizbiorów

```python
c1 - c2
# {'a': 2}
```

Elementy z wynikiem ≤ 0 są usuwane.

### Część wspólna (minimum)

```python
c1 & c2
# {'a': 1, 'b': 1}
```

Czyli: `min(count)`.

### Suma w sensie zbiorowym (maximum)

```python
c1 | c2
# {'a': 3, 'b': 2}
```

Czyli: `max(count)`.

To są **dokładnie operacje na multizbiorach z teorii mnogości**.

---

## Najczęstsze operacje praktyczne

### Najczęstsze elementy

```python
Counter("banana").most_common(2)
# [('a', 3), ('n', 2)]
```

### Rozwinięcie z powrotem do sekwencji

```python
list(Counter(a=2, b=1).elements())
# ['a', 'a', 'b']
```

### Suma wszystkich elementów

```python
sum(c.values())
```

---

## Zachowanie przy wartościach ujemnych i zerowych

`Counter` **pozwala** na wartości ≤ 0:

```python
c = Counter(a=1)
c['a'] -= 3
print(c)      # {'a': -2}
```

Ale:

- operacje `+`, `-`, `&`, `|` **ignorują** elementy ≤ 0
- `elements()` je ignoruje

Możesz wyczyścić takie wpisy:

```python
+c
```

To jest mało znany trick:

```python
c = Counter(a=2, b=-1, c=0)
print(+c)   # {'a': 2}
```

Unary plus = „usuń niepozytywne”.

---

## Dlaczego to jest potężne (i niedoceniane)

`Counter` to:

- histogram
- multizbiór
- licznik
- bardzo szybka struktura do porównań „co się zmieniło między zbiorami”

Przykład z realnego życia:

```python
before = Counter(tokens_before)
after  = Counter(tokens_after)

added   = after - before
removed = before - after
```

Albo porównywanie plików, logów, eventów, stanów systemu, etc.

---

## Złożoność

Ponieważ to dict:

- dostęp: **O(1)**
- operacje `+ - & |`: **O(n)** po liczbie kluczy

---

## Mentalny model

Myśl nie:

> „słownik z intami”

Tylko:

> „algebra multizbiorów za darmo w standardowej bibliotece”

I dlatego `Counter` jest jednym z najbardziej niedocenianych narzędzi w Pythonie.

---

**User:**

z tego Counter({3: 2, 5: 1, 1: 0, 2: 0, 4: 0, 6: 0})
chcę uzyskać listę tylko tych które wartośc mają != 0

---

**Assistant:**

Najprościej (i idiomatycznie dla `Counter`):

```python
from collections import Counter

c = Counter({3: 2, 5: 1, 1: 0, 2: 0, 4: 0, 6: 0})

result = list((+c).keys())
print(result)  # [3, 5]
```

### Dlaczego to działa

Unary `+` na `Counter`:

> usuwa wszystkie elementy, których licznik ≤ 0

Czyli:

```python
+c
# Counter({3: 2, 5: 1})
```

---

### Alternatywa „po słownikowemu”

```python
result = [k for k, v in c.items() if v != 0]
```

Ale dla `Counter` wersja z `+c` jest:
- czytelniejsza semantycznie (operacja multizbiorowa),
- szybsza,
- idiomatyczna dla tej struktury.

---

### Jeśli chcesz od razu elementy powtórzone wg liczności

```python
list((+c).elements())
# [3, 3, 5]
```

---

**User:**

nie bardzo rozumiem (+c)? + zostawia wszystkie elementy większe większe od 0? jakie są jeszcze inne operatory?

---

**Assistant:**

Tak.  
W `Counter` operator unarny `+` ma **specjalne znaczenie**, które nie istnieje dla zwykłego `dict`.

## `+c` — co dokładnie robi

```python
+c
```

oznacza:

> zwróć nowy `Counter` zawierający **tylko te elementy, których licznik > 0**

Czyli to jest w praktyce:

```python
Counter({k: v for k, v in c.items() if v > 0})
```

Przykład:

```python
from collections import Counter

c = Counter({3: 2, 5: 1, 1: 0, 2: -4})

print(+c)
# Counter({3: 2, 5: 1})
```

---

## `-c` — mało znany odpowiednik

Analogicznie istnieje:

```python
-c
```

To oznacza:

> zwróć tylko te elementy, których licznik < 0, ale jako wartości dodatnie

```python
c = Counter({3: 2, 5: -3, 1: 0})

print(-c)
# Counter({5: 3})
```

Bo: `abs(ujemnych)`.

To jest czysta algebra multizbiorów.

---

## Operatory, które `Counter` przeciąża

Załóżmy:

```python
c1 = Counter(a=3, b=1)
c2 = Counter(a=1, b=2)
```

### `+` — suma liczności

```python
c1 + c2
# {'a': 4, 'b': 3}
```

### `-` — różnica liczności (ucina ≤0)

```python
c1 - c2
# {'a': 2}
```

### `&` — część wspólna (minimum)

```python
c1 & c2
# {'a': 1, 'b': 1}
```

### `|` — suma zbiorowa (maximum)

```python
c1 | c2
# {'a': 3, 'b': 2}
```

To są **operatory multizbiorów z teorii mnogości**.

---

## Operatory unarne (mało znane)

| Operator | Znaczenie |
|---|---|
| `+c` | usuń elementy z count ≤ 0 |
| `-c` | zostaw tylko elementy z count < 0 (zrób dodatnie) |

To są specjalne metody: `__pos__` i `__neg__` w implementacji.

---

## Dlaczego to istnieje?

Bo `Counter` może mieć wartości ujemne i zera, a operacje multizbiorowe **ignorują** takie elementy.  
`+c` to szybki sposób „przywrócenia poprawnego multizbioru”.

---

## Intuicja

Myśl o `Counter` jak o obiekcie algebry:

- `+` / `-` / `&` / `|` → operacje na multizbiorach
- `+c` → normalizacja do poprawnego multizbioru
- `-c` → „co jest na minusie”

To nie jest przypadek — to zaprojektowane bardzo świadomie.