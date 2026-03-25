# Wielka vs mała litera: `Dict`/`List` a `dict`/`list` w Pythonie

W Pythonie często można spotkać dwa sposoby zapisu podstawowych kolekcji: używające wielkich liter (np. `List`, `Dict`, `Set`, `Tuple` importowane z modułu `typing`) oraz małych (np. `list`, `dict`, `set`, `tuple`, które są typami wbudowanymi). 

Różnica między nimi polega na przeznaczeniu tych obiektów oraz, co najważniejsze, na **wersji Pythona**, w której pisany jest kod.

## Kiedy stosuje się które z nich?

1. **Mała litera (`list`, `dict`, `set`, `tuple`)**
   - **Tworzenie obiektów:** Od samego początku Pythona małych liter używa się do tworzenia rzeczywistych instancji obiektów w pamięci lub rzutowania typów (np. `my_list = list()`, `my_list = []`).
   - **Adnotacje typów (Python 3.9+):** W nowszym Pythonie wbudowane kolekcje zaczęły wspierać generyczność (dzięki PEP 585). Oznacza to, że używa się ich również do określania i podpowiadania typów, precyzując zawartość w nawiasie kwadratowym: `my_list: list[int] = [1, 2, 3]`.

2. **Wielka litera (`List`, `Dict`, `Set`, `Tuple` z modułu `typing`)**
   - **Adnotacje typów (Python < 3.9):** W starszych wersjach Pythona wbudowane klasy (`list`, `dict` itd.) nie potrafiły same określać "typu zawartości". Wykonanie `list[int]` rzucało błąd `TypeError`, ponieważ klasa wbudowana nie przyjmowała parametrów z użyciem indeksatora. Z tego powodu dodano moduł `typing`, w którym umieszczono zastępcze typy z wielkiej litery służące **wyłącznie** do analizy statycznej i adnotacji typu.
   - **Zakazane tworzenie obiektów:** Nigdy nie należy inicjować za ich pomocą obiektów w czasie wykonania (np. `my_list = List()`). Jest to błędne!

## Jak to wygląda w kodzie?

### Kod z długim stażem (Python 3.8 i starsze)

Trzeba było wyraźnie oddzielać warstwę adnotacji (importy z `typing`) od warstwy wykonawczej (wbudowane typy małą literą).

```python
from typing import List, Dict, Tuple

# Wielkie litery w adnotacjach, bo list[str] rzuciłoby wyjątek w locie
def process_data(users: List[str], config: Dict[str, int]) -> Tuple[str, ...]:
    # Małe litery w kodzie wywoływanym:
    new_users = list(users)
    return tuple(new_users)
```

### Nowy kod (Python 3.9+) - Preferowany styl

**Zaleca się zrezygnować z wielkich liter w 100%.** Wbudowane typy pisane małymi literami pełnią funkcję zarówno kreatora obiektów, jak i adnotacji. Można zapomnieć o ciągłym importowaniu ich z `typing`.

```python
# Bez zbędnych importów! Tylko małe litery do wszystkiego:
def process_data(users: list[str], config: dict[str, int]) -> tuple[str, ...]:
    return tuple(users)
```

## Wyjątek dla starszego kodu ("magiczny" import)

Jeżeli Twój projekt wymusza użycie starszej wersji środowiska, np. Python 3.7 lub 3.8, ale mimo to chcesz korzystać z czystej i spójnej składni dla typów (`list[int]`), możesz zaimportować specjalną funkcję, która wyłącza wykonywanie adnotacji typów podczas działania aplikacji:

```python
from __future__ import annotations

# Działa nawet w Python 3.7+ pomimo używania małych liter!
def process_data(users: list[str], config: dict[str, int]) -> tuple[str, ...]:
    return tuple(users)
```

## Pełna lista typów wbudowanych pisanych małą literą

W ramach uzupełnienia, poniżej znajduje się kompletne i wyczerpujące zestawienie wszystkich wbudowanych typów w Pythonie. Dzielą się one na dwie podgrupy — kolekcje, które zyskały możliwość bycia generycznymi, oraz podstawowe typy skalarne.

### 1. Kolekcje generyczne (od Pythona 3.9 - weszły zamiast typów z `typing`)
Zastąpiły one całkowicie wielkie litery z klasycznego modułu `typing`. Dodatkowo, obiekty te można indeksować (używając `[]`), by zawęzić adnotację zawartości.

- `list` (zastępuje `typing.List`) — dynamiczna tablica (np. `list[int]`)
- `dict` (zastępuje `typing.Dict`) — słownik / mapa (np. `dict[str, float]`)
- `set` (zastępuje `typing.Set`) — unikalny zbiór (np. `set[str]`)
- `tuple` (zastępuje `typing.Tuple`) — krotka, również ze zmienną długością (np. `tuple[int, str, bool]` lub `tuple[int, ...]`)
- `frozenset` (zastępuje `typing.FrozenSet`) — niemutowalny zbiór (np. `frozenset[int]`)
- `type` (zastępuje `typing.Type`) — służy do oznaczania "klasy obiektu" (np. `type[MyClass]`)

### 2. Typy proste (skalarne i z góry ustalone struktury binarne)
Typy niemutowalne/mutowalne na niższym poziomie, od początku używane małymi literami. Nie mogą być parametryzowane w nawiasach kwadratowych tak jak generyki:

- `int` — reprezentacja liczb całkowitych
- `float` — liczby zmiennoprzecinkowe
- `str` — ciągi znaków (ciągi tekstowe)
- `bool` — typ logiczny (`True` lub `False`)
- `complex` — liczby zespolone
- `bytes` — stała tablica bajtów / sekwencja oktetów
- `bytearray` — zmienna mutowalna do operacji binarnych nad bajtami
- `memoryview` — bezpośredni widok z buforowaną pamięcią
- `object` — główny "rodzic" typów z wierzchołka dziedziczenia

## Podsumowanie

- Od Pythona 3.9 korzystanie z dużych liter w wbudowanych kolekcjach (`List`, `Dict`, `Set` itp. z modułu `typing`) zostało **oficjalnie uznane za przestarzałe (deprecated)**.
- Dobrym nawykiem oraz nowym idiomem Pythona jest dzisiaj pisanie wszystkiego za pomocą małych liter — tzn. `list`, `dict` i innych.
- Klasy pisane z dużej litery dotyczyły niegdyś **tylko i wyłącznie podpowiadania typów**, podczas gdy te samoistnie pisane z małej litery od zawsze służyły rzutowaniu i inicjalizowaniu wbudowanych klas kolekcji Pythona.

## Powiązane pliki i koncepcje

- [typowanie-w-pythonie](typowanie-w-pythonie.md)
- [deprecated-typing-w-pythonie](deprecated-typing-w-pythonie.md)
- [własne-typy-w-pythonie](własne-typy-w-pythonie.md)
