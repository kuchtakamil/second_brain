# Przykład curring w Pythonie

**Data:** 2025-05-10

---

**User:**

[obraz niedostępny: file-service://file-BNksxaHyjG9r8ducyXZH92]

oto przykład curring w python 


---

**Assistant:**

Tak, dokładnie – to jest przykład **currying**u (dokładniej: częściowej aplikacji funkcji) w Pythonie.

Oto co ten kod robi:

```python
def multiply_setup(a: float):
    def multiply(b: float) -> float:
        return a * b
    return multiply
```

Czyli:

- `multiply_setup` to funkcja, która przyjmuje jeden argument `a` i **zwraca nową funkcję** `multiply`, która przyjmuje `b`.
- Funkcja `multiply` "pamięta" wartość `a` z zewnętrznego scope'u – to tzw. **zamknięcie (closure)**.
- Dzięki temu możesz zrobić coś takiego:

```python
times3 = multiply_setup(3.0)
print(times3(4.0))  # Wypisze 12.0
```

To podejście jest podobne do `functools.partial`, ale daje więcej kontroli, np. możesz dodać logikę do wewnętrznej funkcji.

Czy chcesz, żebym pokazał podobny przykład z użyciem `functools.partial` albo jak napisać to bardziej funkcyjnie?

---

**User:**

czy to prawda że multiply_setup musi mieć tylko jeden parametr?

---

**Assistant:**

Nie, to **nie jest prawda**, że `multiply_setup` **musi** mieć tylko jeden parametr.

To, że w przykładzie ma **jeden parametr (`a`)**, wynika z chęci uproszczenia przykładu currying'u, gdzie funkcje przyjmują **kolejno po jednym argumencie** – to klasyczny styl currying'u, znany np. z Haskella.

Ale **możesz zdefiniować `multiply_setup` z wieloma parametrami**, np.:

```python
def multiply_setup(a: float, factor: float):
    def multiply(b: float) -> float:
        return (a * b) * factor
    return multiply
```

Lub nawet przekazać wszystkie parametry od razu:

```python
def multiply(a: float, b: float, factor: float) -> float:
    return (a * b) * factor
```

Ale wtedy to **nie będzie już currying**, tylko zwykła funkcja.

Currying oznacza przekształcenie funkcji wieloargumentowej w ciąg funkcji jednoargumentowych, np.:

```python
def curried_multiply(a: float):
    def with_b(b: float):
        def with_factor(factor: float):
            return (a * b) * factor
        return with_factor
    return with_b
```

Czy chcesz, żebym pokazał, jak taki wieloargumentowy currying można zrobić automatycznie w Pythonie?

---

**User:**

ok, w takim razie może multiply musi mieć jeden parametr?

---

**Assistant:**

Dobre pytanie — i tutaj odpowiedź również brzmi: **nie, `multiply` nie musi mieć tylko jednego parametru**.

W przykładzie:

```python
def multiply_setup(a: float):
    def multiply(b: float) -> float:
        return a * b
    return multiply
```

`multiply` przyjmuje jeden parametr, ponieważ to pasuje do idei „krokowego” przekazywania parametrów (currying). Ale **technicznie** możesz zdefiniować `multiply` tak, by przyjmował więcej parametrów:

```python
def multiply_setup(a: float):
    def multiply(b: float, c: float) -> float:
        return a * b * c
    return multiply
```

I wtedy użycie wygląda tak:

```python
f = multiply_setup(2)
result = f(3, 4)  # => 2 * 3 * 4 = 24
```

Tyle że w tym momencie to już **nie jest „czysty” currying**, tylko po prostu zwracanie funkcji z dostępem do zmiennej `a`.

Podsumowując:
- `multiply` *nie musi* mieć jednego parametru — to zależy od tego, co chcesz osiągnąć.
- Jednoargumentowe funkcje w tym kontekście ułatwiają styl curry.
- Ale Python nie wymusza liczby parametrów w żaden sposób.

Czy chcesz, żebym pokazał, jak można zrobić „pełny currying” automatycznie dla dowolnej funkcji w Pythonie?