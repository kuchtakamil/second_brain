# Typowanie w Pythonie

**Data:** 2025-05-10

---

**User:**

Jak to jest z typami w Python? Np. my_range: range = range(10)
Trzeba, należy je podawać? Które, wszystkie?

---

**Assistant:**

W Pythonie podawanie typów (tzw. **type hints**) nie jest obowiązkowe – Python pozostaje językiem dynamicznie typowanym. Jednak od wersji 3.5 wprowadzono możliwość podawania typów jako **adnotacji**, które:

- **nie wpływają** na wykonanie programu,
- **pomagają IDE** i narzędziom takim jak `mypy`, `pyright`, `pylance`,
- **poprawiają czytelność i dokumentację kodu**.

### Przykład, który podałeś:

```python
my_range: range = range(10)
```

To jest jak najbardziej poprawna adnotacja – mówi czytelnikowi i narzędziom, że `my_range` ma typ `range`.

---

### Czy trzeba je podawać?

- **Nie trzeba.** Kod bez adnotacji działa normalnie.
- **Należy je podawać tam, gdzie to pomaga**:
  - przy **argumentach i zwracanych wartościach funkcji**,
  - przy publicznych API, klasach, bibliotekach,
  - w większych projektach, gdzie czytelność i analiza statyczna mają znaczenie.

---

### Przykład typowania funkcji:

```python
def add(a: int, b: int) -> int:
    return a + b
```

To pomaga np. `mypy` wykryć błędy typu:

```python
add("hello", 5)  # mypy powie: Argument 1 to str, expected int
```

---

### Typować wszystkie zmienne?

Nie, typowanie **wszystkich zmiennych lokalnych** jest zwykle zbędne. Typuj je tylko wtedy, gdy:

- IDE lub `mypy` nie potrafi poprawnie wywnioskować typu,
- chcesz coś szczególnie zaznaczyć dla czytelnika (np. że coś jest `Optional[int]` albo `Callable`).

---

### Podsumowanie – **co typować**:

| Co                         | Typować?         | Dlaczego?                              |
|---------------------------|------------------|----------------------------------------|
| Parametry funkcji         | ✅ warto         | jasność, analiza statyczna             |
| Typ zwracany z funkcji    | ✅ warto         | jasność, analiza statyczna             |
| Zmienne lokalne           | ❌ niekoniecznie | Python dobrze je inferuje              |
| Atrybuty klas             | ✅ warto         | lepsze wsparcie IDE i refaktoryzacji   |
| Zmienne globalne/module-level | 🟡 opcjonalnie  | przydatne, jeśli ważne w API           |

Chcesz przykład typowania bardziej złożonej funkcji lub klasy?