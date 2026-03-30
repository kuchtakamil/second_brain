# Catastrophic Cancellation — utrata precyzji przy odejmowaniu bliskich liczb

## Czym jest ten problem?

Gdy obliczamy `f(x) = √(1 + x) − 1` dla bardzo małych wartości `x` (np. `x = 1e-15`), wynik jest **znacząco niedokładny**. Dotyczy to **każdego** języka korzystającego z arytmetyki zmiennoprzecinkowej IEEE 754 — a więc zarówno Javy, jak i Pythona, C, JavaScriptu itd.

```python
import math

x = 1e-15

# Wynik niedokładny — catastrophic cancellation
bad = math.sqrt(1 + x) - 1
print(f"Zły wynik:  {bad}")    # 4.440892098500626e-16

# Wynik dokładny — po przekształceniu algebraicznym
good = x / (math.sqrt(1 + x) + 1)
print(f"Dobry wynik: {good}")  # 4.999999999999999e-16
```

**Oczekiwany (dobry) wynik:** `≈ 4.999999999999999875e-16`

## Dlaczego pojawia się błąd?

### Krok po kroku — jak komputer liczy `√(1 + x) − 1`

1. **Reprezentacja `x`** — liczba `1e-15` jest dokładnie reprezentowalna w `float64`.

2. **Obliczenie `1 + x`** — tu Python (i każdy inny język z IEEE 754) musi zapisać wynik w 64-bitowym `float`:

   ```
   1 + 0.000000000000001 = 1.000000000000001
   ```

   `float64` ma ~15-16 cyfr znaczących. Wynik `1.000000000000001` **mieści się** w tej precyzji, ale `x` „traci" na znaczeniu — staje się najmniej znaczącymi bitami dużej liczby `1`.

3. **Obliczenie `√(1.000000000000001)`** — wynik to coś bardzo bliskiego `1`:

   ```
   ≈ 1.0000000000000005
   ```

4. **Odejmowanie `1.0000000000000005 − 1`** — i tu następuje **catastrophic cancellation**:
   - Obie liczby mają identyczne bity na wszystkich pozycjach poza ostatnimi 1-2 bitami.
   - Odejmowanie „zżera" wszystkie wspólne cyfry znaczące.
   - Zostają nam tylko **1-2 bity** faktycznej informacji, reszta to **szum zaokrągleń**.

### Ale dlaczego te 1-2 bity nie reprezentują poprawnej wartości?

To świetne pytanie. Intuicja podpowiada: „skoro odejmowanie daje mały wynik, to czemu ten mały wynik nie jest po prostu prawidłowy?" Odpowiedź: **błąd nie powstaje w momencie odejmowania — on już tam był, tylko odejmowanie go odsłania.**

Implementacja `float` **nie jest** wadliwa. Każda pojedyncza operacja IEEE 754 daje najlepszy możliwy wynik z zaokrągleniem do najbliższej reprezentowalnej wartości. Problem polega na **narastaniu błędu zaokrąglenia w poprzednich krokach**, który potem zostaje „obnażony" przez odejmowanie:

1. **Krok `1 + x`** — dodajemy `1e-15` do `1`. Wynik musi zmieścić się w 52 bitach mantysy. Liczba `1` zajmuje praktycznie całą mantysę, więc `x` musi zostać „wciśnięte" w ostatnie bity. Tu traci się już kilka bitów precyzji `x` (bo `x` jest o 15 rzędów wielkości mniejsze od `1`).

2. **Krok `√(...)`** — pierwiastek jest obliczany poprawnie, ale działa na **już zaokrąglonym** wyniku `1 + x`. Błąd z kroku 1 propaguje się dalej.

3. **Krok `... − 1`** — i tu następuje „odsłonięcie". Gdy obie liczby miały postać `1.00000000000000??`, te wspólne cyfry `1.00000000000000` się **znoszą**, i jedyne co zostaje to `??` — ale te `??` zawierają w sobie **błąd zaokrąglenia z kroków 1 i 2**, nie prawdziwą wartość `x/2`.

```
Prawdziwa wartość:   1.0000000000000004999...
Po zaokrągleniu:     1.0000000000000004441...  (najbliższy float64)
                                       ^^^
                           te bity już zawierają błąd zaokrąglenia

Po odjęciu 1:        0.0000000000000004441...
                     ↑ wynik składa się GŁÓWNIE z błędu zaokrąglenia
```

**Analogia:** wyobraź sobie, że mierzysz wzrost dwóch osób linijką z dokładnością do 1 cm. Jedna ma 180 cm, druga 181 cm. Różnica to „1 cm" — ale błąd pomiaru też wynosi ±1 cm! Wynik `1 cm` jest więc **całkowicie zdominowany przez błąd pomiaru**, mimo że linijka sama w sobie działa poprawnie.

> [!IMPORTANT]
> `float` nie jest „zepsuty". Każda operacja z osobna jest maksymalnie dokładna. Problem w tym, że odejmowanie bliskich liczb **wzmacnia** względny błąd zaokrąglenia z poprzednich operacji — zamienia mały błąd bezwzględny w ogromny błąd względny.

### Analogia z liczbami dziesiętnymi

Wyobraź sobie, że masz kalkulator z precyzją 5 cyfr znaczących:

```
  1.0000   (5 cyfr znaczących)
- 0.99997  (5 cyfr znaczących)
= 0.00003  (1 cyfra znacząca!)
```

Obie liczby wejściowe miały 5 cyfr precyzji, ale wynik ma tylko **1 cyfrę znaczącą**. To właśnie jest **catastrophic cancellation** — katastrofalna utrata cyfr znaczących przy odejmowaniu dwóch bliskich sobie liczb.

## Rozwiązanie — przekształcenie algebraiczne

### Trik z „mnożeniem przez sprzężenie"

Mnożymy i dzielimy wyrażenie przez **sprzężenie** (`√(1+x) + 1`):

```
f(x) = √(1+x) − 1

     = (√(1+x) − 1) × (√(1+x) + 1)
       ─────────────────────────────
              (√(1+x) + 1)

     =  (1+x) − 1
       ───────────
       √(1+x) + 1

     =     x
       ───────────
       √(1+x) + 1
```

Wykorzystaliśmy tu wzór skróconego mnożenia **(a − b)(a + b) = a² − b²**:

```
(√(1+x))² − 1² = (1+x) − 1 = x
```

### Dlaczego nowa postać jest dokładna?

W nowej postaci `f(x) = x / (√(1+x) + 1)`:

| Operacja | Dokładność |
|---|---|
| `x` | Dokładna wartość wejściowa — żadna utrata precyzji |
| `√(1+x)` | Obliczone z pełną precyzją `float64` (~15 cyfr) |
| `√(1+x) + 1` | **Dodawanie** dwóch liczb bliskich `1` — żadne odejmowanie, żadna utrata cyfr |
| `x / (√(1+x) + 1)` | Dzielenie — zachowuje pełną precyzję |

**Kluczowa różnica:** zamieniliśmy **odejmowanie bliskich liczb** (destrukcyjne) na **dodawanie** i **dzielenie** (bezpieczne operacje).

## Czy ten problem dotyczy Pythona?

**Tak, absolutnie.** Python używa dokładnie tego samego standardu IEEE 754 double-precision (64-bit) co Java, C, JavaScript i większość innych języków. Pod spodem typ `float` w Pythonie to C `double`.

```python
import sys
print(sys.float_info)
# sys.float_info(max=1.7976931348623157e+308, ..., dig=15, ...)
#                                                    ^^^^^^
#                                          ~15 cyfr znaczących
```

### Porównanie Python vs Java

```python
# Python
import math
x = 1e-15
print(math.sqrt(1 + x) - 1)         # 4.440892098500626e-16  ← ZŁY
print(x / (math.sqrt(1 + x) + 1))   # 4.999999999999999e-16  ← DOBRY
```

```java
// Java — identyczne wyniki!
double x = 1e-15;
System.out.println(Math.sqrt(1 + x) - 1);          // 4.440892098500626E-16
System.out.println(x / (Math.sqrt(1 + x) + 1));    // 4.999999999999999E-16
```

**Wyniki są identyczne**, bo oba języki korzystają z tego samego sprzętu (FPU procesora) i standardu IEEE 754.

## Alternatywa — typy danych odporne na catastrophic cancellation

Zarówno Python, jak i Java oferują typy, które **nie korzystają z IEEE 754 float** i mogą obliczać z dowolną precyzją. Dzięki nim nie trzeba przekształcać wzorów:

### Python — `decimal.Decimal`

```python
from decimal import Decimal, getcontext

getcontext().prec = 50  # 50 cyfr znaczących (zamiast ~15 we float)

x = Decimal('1e-15')
result = (1 + x).sqrt() - 1
print(result)
# 4.9999999999999998750000000000000006250000000000000E-16  ← DOKŁADNY
```

Rozwiązanie z codewars:

```python
from decimal import Decimal

def f (x):
    return float(Decimal.sqrt(1 + Decimal(x))-1)
```

> [!NOTE]
> Kluczowe: `Decimal('1e-15')` — przekazujemy string, nie float!
> Gdybyśmy napisali `Decimal(1e-15)`, Python najpierw utworzyłby niedokładny `float`, a potem skonwertował go na `Decimal` — i błąd byłby już „wpieczony".

### Python — `fractions.Fraction`

```python
from fractions import Fraction
import math

x = Fraction(1, 10**15)  # dokładnie 1/1000000000000000
result = float((1 + x)) ** 0.5 - 1  # tu i tak tracimy precyzję przy konwersji na float
```

`Fraction` przechowuje ułamki **dokładnie** jako parę licznik/mianownik, ale nie ma wbudowanej metody `sqrt()`. Nadaje się więc do operacji algebraicznych (dodawanie, mnożenie, dzielenie), ale nie do pierwiastków — tu lepszy jest `Decimal`.

### Java — `BigDecimal`

```java
import java.math.BigDecimal;
import java.math.MathContext;

MathContext mc = new MathContext(50); // 50 cyfr znaczących
BigDecimal x = new BigDecimal("1e-15");
BigDecimal one = BigDecimal.ONE;

BigDecimal result = one.add(x).sqrt(mc).subtract(one);
System.out.println(result);
// 4.9999999999999998750000000000000006250000000000000E-16
```

> [!NOTE]
> Tak samo jak w Pythonie — kluczowe jest `new BigDecimal("1e-15")` (string), nie `new BigDecimal(1e-15)` (double).

### Porównanie — kiedy co stosować?

| Cecha | `float` / `double` | `Decimal` / `BigDecimal` |
| --- | --- | --- |
| Precyzja | ~15 cyfr (stała) | Dowolna (konfigurowalna) |
| Szybkość | **Bardzo szybki** (sprzętowy FPU) | 10-100× wolniejszy (software) |
| Pamięć | 8 bajtów | Dziesiątki–setki bajtów |
| Catastrophic cancellation | **Tak** — trzeba przekształcać wzory | **Nie** — wystarczy zwiększyć precyzję |
| Zastosowanie | Obliczenia naukowe, grafika, ML | Finanse, obliczenia wymagające dokładności |

> [!TIP]
> W praktyce: w 99% przypadków używa się `float`/`double` + przekształceń algebraicznych, bo są **wielokrotnie szybsze**. `Decimal`/`BigDecimal` stosuje się tam, gdzie liczy się **dokładność co do cyfry** (np. systemy bankowe), a szybkość jest drugorzędna.

## Podsumowanie

| Aspekt | `√(1+x) − 1` | `x / (√(1+x) + 1)` |
|---|---|---|
| Operacja krytyczna | **Odejmowanie** bliskich liczb | **Dodawanie** + dzielenie |
| Utrata precyzji | Tak — catastrophic cancellation | Nie |
| Wynik dla `x = 1e-15` | `4.44e-16` (błędny) | `5.00e-16` (poprawny) |
| Dotyczy Pythona? | **Tak** | — |
| Dotyczy Javy? | **Tak** | — |

> [!TIP]
> Zawsze gdy widzisz wyrażenie typu `a − b`, gdzie `a ≈ b`, szukaj przekształcenia algebraicznego, które eliminuje odejmowanie. Typowe techniki to:
>
> - Mnożenie przez **sprzężenie** (conjugate multiplication)
> - Rozwinięcie w **szereg Taylora** (np. `√(1+x) ≈ 1 + x/2` dla małych `x`)
> - Użycie funkcji bibliotecznych jak `math.log1p(x)` zamiast `math.log(1 + x)` lub `math.expm1(x)` zamiast `math.exp(x) - 1`

## Powiązane pliki

- [Python interview cheatsheet](python-interview-cheatsheet.md)
- [Typy danych w Python i zużycie pamięci](typy-danych-w-python-i-zuzycie-pamieci.md)
- [Ograniczenia typów liczbowych](ograniczenia-typów-liczbowych.md)
