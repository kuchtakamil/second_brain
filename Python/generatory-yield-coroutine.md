# Generatory, yield, yield from i coroutines w Pythonie

Generatory to funkcje ze słowem kluczowym `yield`, zwracające "leniwy" iterator. Generują elementy jeden po drugim, pamiętając swój stan (zmienne lokalne) pomiędzy wywołaniami. Pozwala to na uniknięcie ładowania całych kolekcji do pamięci.

```python
# generator function
def countdown(n):
    while n > 0:
        yield n    # zwraca wartość i wstrzymuje wykonanie funkcji do kolejnego odpytania
        n -= 1

list(countdown(5))   # [5,4,3,2,1]

# generator expression
gen = (x**2 for x in range(10))
next(gen)   # 0
next(gen)   # 1
```

## yield from

`yield from iterable` to "cukier syntaktyczny" (syntactic sugar). Zamiast pisać pętlę ręcznie w stylu `for x in iterable: yield x`, delegujesz oddawanie wartości element po elemencie bezpośrednio z przekazanego iterable.

```python
def chain(*iters):
    for it in iters:
        yield from it  # "wypakowuje" dany iterator

# list(chain([1,2], [3,4])) -> [1,2,3,4]
```

## send() – coroutine (korutyny)

Wyrażenie `yield` działa w dwie strony: może **zwracać** wartość, ale też w to samo miejsce **przyjmować** wartość wstrzykniętą z zewnątrz. Robimy to metodą `.send(wartość)`.

```python
def accumulator():
    total = 0
    while True:
        # Kod wstrzymuje działanie tutaj. 'total' jest zwracane na zewnątrz.
        # Gdy z zewnątrz wywołamy .send(jakas_wartosc), to the 'value' dostanie te dane.
        value = yield total
        total += value

acc = accumulator()
next(acc)     # KROK 1: "rozgrzanie" (priming). Generator musi dojść do pierwszego yield (total=0).
acc.send(10)  # KROK 2: wznowienie. 'value' = 10 -> total = 10 -> pętla wraca na start -> yield 10
acc.send(5)   # KROK 3: wznowienie. 'value' = 5 -> total = 15 -> pętla wraca na start -> yield 15
```

> Przed pierwszym wywołaniem `.send()` musisz zawsze uruchomić korutynę używając `next(gen)` lub `gen.send(None)`. Zanim generator zatrzyma się na instrukcji `yield`, nie jest w stanie odebrać żadnej wartości.
