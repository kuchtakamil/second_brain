# Dekoratory `@lru_cache` i `@cache` w Pythonie

Dekoratory `@lru_cache` oraz `@cache` to bardzo przydatne narzędzia z wbudowanej biblioteki `functools`. Służą one do optymalizacji działania programu poprzez **memoizację** – czyli zapamiętywanie wyników wykonania funkcji dla zadanych argumentów, tak aby przy kolejnym wywołaniu z tymi samymi argumentami nie trzeba było obliczać ich od nowa.

## Dlaczego i kiedy ich używać?

- **Przyspieszanie rekurencji:** Przy klasycznych, naiwnych implementacjach algorytmów rekurencyjnych (np. ciąg Fibonacciego).
- **Złożone obliczenia:** Jeżeli wykonujesz czasochłonną operację matematyczną lub przetwarzanie danych dla powtarzających się parametrów wejściowych.
- **Zapytania do bazy danych / API (I/O):** Jeśli ciągle fetchujesz te same, rzadko zmieniające się informacje.
- **Wymagania dla argumentów:** Pamiętaj, że argumenty przekazywane do udekorowanej funkcji muszą być mutowalne (tzw. "hashable" - np. int, string, tuple), ponieważ są używane jako klucze w słowniku przechowującym cache.

## Jak działają? (Na przykładzie ciągu Fibonacciego)

### Sytuacja bez stosowania cache (Problem)

Klasyczne, naiwne wyliczanie elementów ciągu Fibonacciego:

```python
def fib(n):
    if n < 2: 
        return n
    return fib(n-1) + fib(n-2)

print(fib(35)) # Wyliczy się, ale potrwa to kilka sekund...
print(fib(50)) # Prawdopodobnie zawiesi na długo program
```

**Co by było, gdyby się ich nie użyło?**
W powyższym kodzie dla `fib(5)` program oblicza `fib(4)` i `fib(3)`. Jednak do obliczenia `fib(4)` musi znów obliczyć `fib(3)` i `fib(2)`. Jak widać `fib(3)` obliczane jest **kilkukrotnie**. Prowadzi to do wykładniczej złożoności czasowej $\mathcal{O}(2^n)$, co przy wyższych wartościach `n` błyskawicznie "zabije" czas procesora i pamięć.

### Ratunek 1: Dekorator `@lru_cache`

Lekarstwem na to jest `lru_cache` (ang. _Least Recently Used_ cache). 

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def fib(n):
    if n < 2: 
        return n
    return fib(n-1) + fib(n-2)

print(fib(50)) # Wynik pojawia się NATYCHMIAST
```

**Co on robi?** 
1. `maxsize=128` oznacza, że dekorator zapamięta w pamięci do **128 ostatnich wywołań** funkcji i ich wyników. 
2. Metoda _Least Recently Used_ oznacza, że jeśli cache zostanie zapełniony, najstarsze, najrzadziej używane wyniki wywołań są wyrzucane z pamięci, by zrobić miejsce nowym.
3. Znacząco obniża to złożoność czasową (z $\mathcal{O}(2^n)$ do praktycznie liniowej za pierwszym wyliczeniem i $\mathcal{O}(1)$ za każdym powtórnym).

### Ratunek 2: Dekorator `@cache`

Od wersji **Python 3.9** dodano nową, minimalistyczną odmianę — `@cache`.

```python
from functools import cache

@cache
def fib(n):
    if n < 2: 
        return n
    return fib(n-1) + fib(n-2)
```

**Co on robi?**
`@cache` to dokładnie to samo co podanie parametru `@lru_cache(maxsize=None)`. Oznacza to, że **rozmiar słownika na wyniki jest nieograniczony** (będzie rósł w nieskończoność w miarę pojawiania się nowych wyników).

**Zalety i Kiedy stosować:**
- Jest o ułamek szybszy od `@lru_cache`, gdyż nie musi implementować wewnętrznej logiki eksmisyjnej "wyrzucania" nadmiaru rekordów (_Least Recently Used_).
- Używaj go tylko wtedy, gdy masz pewność, że zbiór unikalnych argumentów danej funkcji (kluczy cache'a) jest mały, a funkcja kończy działanie stosunkowo szybko lub Twój serwer dysponuje potężną ilością RAM'u, w przeciwnym razie **narażasz się na wycieki pamięci (Memory Leaks)**. W większości realnych scenariuszy backendowych, ustawienie górnego limitu (`maxsize`) przez `lru_cache` jest bezpieczniejszym wyjściem.

## Przydatne funkcje wbudowane

Przed zdefiniowaną jako `@lru_cache` funkcją masz dostęp do specjalnych, wbudowanych metod narzędziowych:

- `fib.cache_info()` - Podaje statystyki pracy mechanizmu cache, takie jak `hits`, `misses`, `maxsize` i `currsize`.
- `fib.cache_clear()` - Ręcznie zwalnia wszystkie zapamiętane wartości z wewnętrznego cache, wymuszając by kolejne wywołania funkcji były znowu przeliczane od nowa.

## Powiązane materiały

- [Biblioteka functools](biblioteka-functools-python.md)
- [Dekoratory w Pythonie](dekoratory-w-pythonie.md)
