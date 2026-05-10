# Python `@runtime_checkable` z pakietu `typing`

## Czym jest `@runtime_checkable`?

Dekorator `@runtime_checkable` pochodzący z modułu `typing` sprawia, że zdefiniowane przez nas protokoły (dziedziczące po `Protocol`) zyskują możliwość sprawdzania ich zgodności w czasie działania programu (runtime) za pomocą standardowych wbudowanych funkcji `isinstance()` oraz `issubclass()`.

## Dlaczego jest to ważne i kiedy się przydaje?

Standardowo interfejsy oparte na `Protocol` służą w Pythonie do realizowania strukturalnego typowania systemów, czyli statycznego *duck typingu*, ale tylko w sposób analizowany przez narzędzia zewnętrze typu `mypy`. Gdy uruchomisz interpreter i spróbujesz wykonać operację `isinstance(obiekt, JakisProtokol)` na czystym protokole, Python rzuci błędem `TypeError`.

Dekorator `@runtime_checkable` omija to ograniczenie. Przydaje się w następujących sytuacjach:
1. **Dynamiczne sterowanie przepływem programu**: Gdy funkcja może uwarunkować swoje działanie na podstawie tego, jakie metody implementuje dany obiekt w czasie jego przypisywania/ładowania. Przydatne dla instrukcji sterujących (np. zagnieżdżonego `match-case` lub bloków if typu `if isinstance(...)`).
2. **Sanity checks / walidacja runtime**: Jeżeli korzystasz z zewnętrznych obiektów np. pochodzących z integracji z zewnętrznym API, i chcesz mieć 100% pewność na etapie ładowania obiektu do silnika bez czekania na ew. wstrzyknięcie wyjątku `AttributeError` głębiej w kodzie.

## Jak to działa (przykłady)?

Dekorator modyfikuje protokół w ten sposób, że w czasie wykonywania kodu `isinstance()` sprawdza dostępność (obecność) metody lub atrybutów zdefiniowanych w ciele `Protocol`.

**Uwaga**: Mechanizm sprawdza *wyłącznie* obecność wymienionych w protokole atrybutów/metod w strukturze obiektu. **Nie sprawdza** ich sygnatur typów zwrotnych, czy deklaracji przyjmowanych parametrów (tym wciąż zajmuje się wyłącznie narzędzie do statycznej konfiguracji `mypy`).

### Przykład kodu:

```python
from typing import Protocol, runtime_checkable

# 1. Deklaracja protokołu z użyciem dekoratora
@runtime_checkable
class SupportsClose(Protocol):
    def close(self) -> None:
        ...

# 2. Implementacja zgodna w pełni z wymogami protokołu
class Resource:
    def close(self) -> None:
        print("Zamykanie zasobu systemowego...")

# 3. Implementacja niekompletna (brak metody close)
class Dummy:
    pass

r = Resource()
d = Dummy()

# Weryfikacja w locie za pomocą isinstance()
print(isinstance(r, SupportsClose))  # Zwróci: True
print(isinstance(d, SupportsClose))  # Zwróci: False

# Weryfikacja definicji klasy w locie za pomocą issubclass()
print(issubclass(Resource, SupportsClose))  # Zwróci: True
print(issubclass(Dummy, SupportsClose))     # Zwróci: False
```

Bez użycia dekoratora `@runtime_checkable`, powyższe zapytania zwróciłyby wyjątek `TypeError: Instance and class checks can only be used with @runtime_checkable protocols`.

## Zobacz również
- [Przykład użycia Protocol](python-protocol-przyklad.md)
- [Python Protocol zamiast interfejsów](python-protocol-zamiast-interfejsów.md)
