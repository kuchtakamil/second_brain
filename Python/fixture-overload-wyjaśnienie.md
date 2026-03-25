# Fixture overload wyjaśnienie

**Data:** 2025-07-14

---

**User:**

W załączonym poniżej kodzie, dwie wersje fixture nie mają implementacji. Nawet nie odwołują się w żaden sposób do trzeciej wersji która implementację ma. Jak w takim razie mogą działać pierwsze dwie wersję metody fixture ?

@overload
def fixture(
    fixture_function: Callable[..., object],
    *,
    scope: _ScopeName | Callable[[str, Config], _ScopeName] = ...,
    params: Iterable[object] | None = ...,
    autouse: bool = ...,
    ids: Sequence[object | None] | Callable[[Any], object | None] | None = ...,
    name: str | None = ...,
) -> FixtureFunctionDefinition: ...


@overload
def fixture(
    fixture_function: None = ...,
    *,
    scope: _ScopeName | Callable[[str, Config], _ScopeName] = ...,
    params: Iterable[object] | None = ...,
    autouse: bool = ...,
    ids: Sequence[object | None] | Callable[[Any], object | None] | None = ...,
    name: str | None = None,
) -> FixtureFunctionMarker: ...


def fixture(
    fixture_function: FixtureFunction | None = None,
    *,
    scope: _ScopeName | Callable[[str, Config], _ScopeName] = "function",
    params: Iterable[object] | None = None,
    autouse: bool = False,
    ids: Sequence[object | None] | Callable[[Any], object | None] | None = None,
    name: str | None = None,
) -> FixtureFunctionMarker | FixtureFunctionDefinition:
    
    fixture_marker = FixtureFunctionMarker(
        scope=scope,
        params=tuple(params) if params is not None else None,
        autouse=autouse,
        ids=None if ids is None else ids if callable(ids) else tuple(ids),
        name=name,
        _ispytest=True,
    )

    # Direct decoration.
    if fixture_function:
        return fixture_marker(fixture_function)

    return fixture_marker

---

**Assistant:**

Dwie wersje oznaczone jako `@overload` w Twoim przykładzie to **tylko deklaracje typów** dla narzędzi typu checker (`mypy`, `pyright` itd.). Nie mają one żadnej implementacji i **nie są wykonywane w czasie działania programu**. One służą **jedynie do podpowiedzi typów** oraz lepszego sprawdzania zgodności sygnatury w edytorze lub narzędziu typu static analysis.

Główna implementacja tej funkcji to:

```python
def fixture(
    fixture_function: FixtureFunction | None = None,
    *,
    scope: _ScopeName | Callable[[str, Config], _ScopeName] = "function",
    params: Iterable[object] | None = None,
    autouse: bool = False,
    ids: Sequence[object | None] | Callable[[Any], object | None] | None = None,
    name: str | None = None,
) -> FixtureFunctionMarker | FixtureFunctionDefinition:
    ...
```

Ta implementacja odpowiada za logikę działania.

---

### Jak to działa?

Python (a konkretnie `typing.overload`) pozwala deklarować wiele wersji funkcji o różnych sygnaturach – ale **tylko jedna implementacja faktycznie istnieje**.

Przykład uproszczony:

```python
from typing import overload, Union

@overload
def func(x: int) -> int: ...
@overload
def func(x: str) -> str: ...

def func(x: Union[int, str]) -> Union[int, str]:
    return x
```

Tutaj `func` ma dwie wersje typowe (`int -> int`, `str -> str`), ale implementację tylko jedną.

---

### W Twoim przykładzie

```python
@overload
def fixture(fixture_function: Callable[..., object], *, ...) -> FixtureFunctionDefinition: ...
```

to wersja dla dekoratora używanego jako:

```python
@fixture
def my_fixture():
    ...
```

czyli dekorator bez parametrów — przekazujemy od razu funkcję.

Druga wersja:

```python
@overload
def fixture(fixture_function: None = ..., *, ...) -> FixtureFunctionMarker: ...
```

jest dla sytuacji, gdzie dekorator przyjmuje parametry:

```python
@fixture(scope="session", autouse=True)
def my_fixture():
    ...
```

I faktyczna implementacja rozróżnia te przypadki:

```python
if fixture_function:
    return fixture_marker(fixture_function)
return fixture_marker
```

Czyli:
- jeśli `fixture_function` jest podane → zwraca gotowy obiekt dekorujący funkcję (natychmiast),
- jeśli nie → zwraca dekorator (marker), który dopiero potem udekoruje funkcję (przy wywołaniu go na funkcji).

---

### Podsumowując:

- Dekorowane wersje `@overload` są tylko **dla checkera typów**, nigdy nie są wykonywane.
- Jedyna działająca implementacja to ta ostatnia (`def fixture(...)`).
- `@overload` umożliwia lepsze typowanie i intellisense, np. rozróżnianie:
  - `@fixture` vs `@fixture(...)`

Jeśli chcesz, mogę pokazać też minimalny działający przykład z takim zachowaniem.

---

**User:**

Nie rozumiem, przecież oba mają parametr fixture_function
@overload
def fixture(
    fixture_function:

---

**Assistant:**

Racja — oba `@overload` mają parametr `fixture_function`, więc pytanie jest bardzo zasadne.

Wyjaśnijmy to dokładnie, krok po kroku:

---

## 🔍 Obie wersje mają `fixture_function`, ale różnie użyte

### 1️⃣ Pierwsze `@overload`

```python
@overload
def fixture(
    fixture_function: Callable[..., object],
    *,
    ...
) -> FixtureFunctionDefinition: ...
```

Tu `fixture_function` jest **wymagane** i oznacza, że użytkownik używa dekoratora **bez nawiasów**:

```python
@fixture
def my_fixture():
    ...
```

Czyli funkcja `my_fixture` jest przekazana jako pierwszy (i jedyny) argument do `fixture(...)`.

---

### 2️⃣ Drugie `@overload`

```python
@overload
def fixture(
    fixture_function: None = ...,
    *,
    ...
) -> FixtureFunctionMarker: ...
```

Tu `fixture_function` ma wartość domyślną `None`, czyli **nie jest przekazywane przez użytkownika**, i użytkownik wywołuje:

```python
@fixture(scope="session", autouse=True)
def my_fixture():
    ...
```

W tym wypadku `fixture()` zwraca dekorator, który potem zostanie wywołany na `my_fixture`.

---

## ✅ Implementacja to rozróżnia

Zobacz, co robi implementacja:

```python
def fixture(fixture_function: FixtureFunction | None = None, *, ...) -> ...:
    fixture_marker = FixtureFunctionMarker(...)

    if fixture_function:
        return fixture_marker(fixture_function)

    return fixture_marker
```

### Czyli:

- jeśli `fixture_function` zostało przekazane i jest nie-None (pierwszy overload), to od razu dekoruje funkcję i zwraca `FixtureFunctionDefinition`.
- jeśli nie zostało przekazane (drugi overload), to zwraca dekorator (`FixtureFunctionMarker`), który potem zostanie użyty na funkcji.

---

## 🔄 Różnice sprowadzają się do sposobu użycia:

| Wywołanie użytkownika                 | `fixture_function`        | Zastosowany `@overload`         |
|--------------------------------------|---------------------------|----------------------------------|
| `@fixture`                           | funkcja                   | 1: `fixture_function: Callable` |
| `@fixture(...)`                      | `None`                    | 2: `fixture_function: None = ...`|

---

## 📌 Dlaczego oba mają `fixture_function`, mimo że jedno `None`?

Bo Python nie pozwala na zupełnie inne sygnatury, jeśli chcemy typować dekorator zarówno:
- jako **funkcję przyjmującą funkcję** (dekorator bez parametrów),
- jak i jako **funkcję przyjmującą parametry i zwracającą dekorator**.

Musisz w obu przypadkach mieć formalnie taki sam podpis funkcji, więc `fixture_function` jest zawsze obecne — tylko jego wartość (czy to `None`, czy `Callable`) jest rozróżniana.

---

Jeśli chcesz, mogę też pokazać minimalny przykład reprodukujący ten mechanizm w prostym dekoratorze.