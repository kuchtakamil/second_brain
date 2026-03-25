# Reprezentacja liczb w Python

**Data:** 2026-02-09

---

**User:**

Reprezentacja liczb int / float w Python. Jak to jest technicznie rozwiązane? Czy są ograniczenia na wielkość int / float jak w java?

---

**Assistant:**

Bardzo dobre pytanie — Python i Java **fundamentalnie różnią się** w reprezentacji liczb całkowitych. I to jest jedna z rzeczy, które często zaskakują ludzi przy przejściu z Javy.

Odpowiedź w skrócie:

| Typ | Java | Python |
|---|---|---|
| `int` | 32-bit, stały zakres | **dowolna precyzja (big integer)** |
| `long` | 64-bit, stały zakres | niepotrzebny |
| `float` | 32-bit IEEE-754 | brak odpowiednika |
| `double` | 64-bit IEEE-754 | **`float` w Pythonie = `double` z Javy** |

A teraz technicznie, jak to jest zrobione pod maską.

---

## 🔢 `int` w Pythonie — arbitralna precyzja (bigint)

Python **nie ma** typu odpowiadającego Java `int`/`long`.

Każdy `int` w Pythonie to obiekt typu:

```
PyLongObject
```

czyli **dynamiczny big integer**.

### Struktura w C (CPython)

Uproszczona definicja:

```c
typedef struct {
    PyObject_VAR_HEAD
    digit ob_digit[1];
} PyLongObject;
```

Kluczowe elementy:

- liczba zapisana jest jako **tablica "cyfr"**
- każda „cyfra” to **30 bitów** (na 64-bitowej platformie)
- reprezentacja w systemie **base 2³⁰**

Czyli liczba:

```
n = d0 + d1·2³⁰ + d2·2⁶⁰ + ...
```

To jest dokładnie klasyczny **big integer**, jak `BigInteger` w Javie.

### Co to oznacza w praktyce?

```python
x = 10**1000000
```

To jest legalne. Python po prostu zaalokuje pamięć.

Ograniczenie: **RAM**, nie zakres typu.

### Koszt operacji

Operacje nie są O(1) jak w Javie:

| Operacja | Złożoność |
|---|---|
| dodawanie | O(n) |
| mnożenie | O(n log n) (Karatsuba / FFT dla dużych) |

Dla małych liczb jest bardzo szybkie, dla ogromnych robi się drogo.

---

## 💾 Optymalizacja: small integer cache

CPython cache’uje liczby:

```
[-5, 256]
```

Czyli:

```python
a = 10
b = 10
a is b  # True
```

To nie dzieje się dla większych liczb.

---

## 🌊 `float` w Pythonie

Tutaj odwrotnie niż z `int`.

Pythonowy:

```python
float
```

to **C `double`** czyli:

```
IEEE-754 64-bit
```

identycznie jak Java `double`.

### Struktura

W CPython:

```c
typedef struct {
    PyObject_HEAD
    double ob_fval;
} PyFloatObject;
```

### Ograniczenia

Takie same jak w Javie:

- ~15–17 cyfr precyzji
- `NaN`, `inf`
- błędy zaokrągleń

```python
0.1 + 0.2 == 0.3  # False
```

---

## ❗ Python NIE ma odpowiednika Java `float` (32-bit)

Jeśli chcesz 32-bit float, musisz użyć:

```python
import numpy as np
np.float32
```

---

## 🧠 Dlaczego Python tak to zrobił?

Bo Python od początku był projektowany jako język:

> „matematycznie poprawny zanim będzie szybki”

Guido świadomie uznał, że overflow w `int` to błąd projektowy języka.

W Pythonie to **niemożliwe**:

```python
2**1000000000   # działa
```

---

## 🆚 Porównanie do Javy (ważne mentalnie)

W Javie:

```java
int a = Integer.MAX_VALUE;
a++;  // overflow
```

W Pythonie:

```python
a = 2**31 - 1
a += 1  # po prostu większa liczba
```

Python robi to, co w Javie musiałbyś zrobić przez:

```java
BigInteger
```

ale **zawsze**.

---

## 🐍 Konsekwencje wydajnościowe (ważne dla programisty Javy)

To jest kluczowe:

Python `int` **nie jest prymitywem**.

To jest:
- obiekt
- alokacja
- tablica cyfr
- GC

Dlatego operacje arytmetyczne są wolniejsze niż w Javie.

Jeśli robisz obliczenia numeryczne → używasz **numpy**, bo tam masz prawdziwe C-owe prymitywy.

---

## 🧮 Precyzyjna arytmetyka zmiennoprzecinkowa

Python ma w standardzie coś, czego Java nie daje tak wygodnie:

```python
from decimal import Decimal
```

To jest odpowiednik `BigDecimal` z Javy.

---

## 📌 Podsumowanie różnic

| Cecha | Java `int` | Python `int` |
|---|---|---|
| zakres | stały | nieograniczony |
| overflow | tak | nie |
| prymityw | tak | nie |
| szybkość | bardzo szybkie | wolniejsze |
| implementacja | 32 bity | BigInteger |

| Cecha | Java `double` | Python `float` |
|---|---|---|
| IEEE-754 | tak | tak |
| precyzja | ~16 cyfr | ~16 cyfr |
| overflow | inf | inf |

---

## Najważniejsza mentalna zmiana dla Ciebie jako Java developera

W Pythonie:

> **`int` = `BigInteger`**
>
> **`float` = `double`**

I to wyjaśnia 90% „dziwnych” rzeczy, które potem obserwujesz w wydajności i zachowaniu kodu.

---

**User:**

czyli jaki jest zakres liczb we float?

---

**Assistant:**

Pythonowy `float` to dokładnie **IEEE-754 double precision (64-bit)** — to samo co `double` w Javie i C.

Czyli zakres i właściwości są **identyczne**.

---

## 📏 Zakres wartości (wartości skończone)

IEEE-754 double ma:

- 1 bit znaku
- 11 bitów wykładnika
- 52 bity mantysy (53 bity precyzji z ukrytym bitem)

### Maksymalna wartość

```
≈ 1.7976931348623157 × 10^308
```

W Pythonie:

```python
import sys
sys.float_info.max
# 1.7976931348623157e+308
```

---

### Najmniejsza dodatnia liczba znormalizowana

```
≈ 2.2250738585072014 × 10^-308
```

```python
sys.float_info.min
# 2.2250738585072014e-308
```

To jest **min normal** (exponent != 0).

---

### Najmniejsza dodatnia liczba (subnormal / denormal)

```
≈ 4.9406564584124654 × 10^-324
```

Poniżej tego masz już **0.0**.

---

## 🧮 Precyzja

Masz **53 bity precyzji**, co daje:

```
~15–17 cyfr dziesiętnych
```

```python
sys.float_info.dig
# 15
```

To znaczy: każda liczba >15 cyfr zaczyna tracić precyzję.

---

## ⚠️ Co się dzieje poza zakresem?

### Za duża liczba

```python
1e309
# inf
```

### Za mała liczba

```python
1e-400
# 0.0
```

---

## 🧪 Masz też standardowe specjalne wartości

```python
float('inf')
float('-inf')
float('nan')
```

I działają dokładnie jak w Javie.

---

## 🔍 Pełna specyfikacja z Pythona

```python
import sys
sys.float_info
```

Daje:

| parametr | wartość |
|---|---|
| max | 1.7976931348623157e+308 |
| min | 2.2250738585072014e-308 |
| epsilon | 2.220446049250313e-16 |
| dig | 15 |
| mant_dig | 53 |

`epsilon` to najmniejsza różnica, którą da się odróżnić od 1.0:

```python
1.0 + sys.float_info.epsilon != 1.0
```

---

## 📌 Najważniejsze liczby do zapamiętania

| Cecha | Wartość |
|---|---|
| max | ~1.8e308 |
| min normal | ~2.2e-308 |
| min subnormal | ~5e-324 |
| precyzja | 15–17 cyfr |
| bity mantysy | 53 |

---

Czyli odpowiedź wprost:

> Zakres `float` w Pythonie jest **~10⁻³²⁴ do ~10³⁰⁸** z precyzją ~16 cyfr — identycznie jak `double` w Javie.