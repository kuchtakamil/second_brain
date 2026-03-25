# Python Protocol zamiast interfejsów

**Data:** 2026-02-09

---

**User:**

Zamiast tworzenia interfejsów jak w Java, w python można użyć Protocol. Wyjaśnij jakto się robi i podaj pełny przykład

---

**Assistant:**

W Pythonie **nie definiujesz interfejsów nominalnie** (jak `interface` w Javie), tylko możesz użyć **strukturalnego typowania** (*structural typing / duck typing z kontrolą przez type checker*).

Do tego służy `typing.Protocol`.

To jest mechanizm wprowadzony w **PEP 544**.

Różnica fundamentalna:

| Java | Python + Protocol |
|---|---|
| Klasa **musi** zadeklarować `implements` | Klasa **nie musi wiedzieć**, że spełnia „interfejs” |
| Typowanie nominalne | Typowanie strukturalne |
| Sprawdzane przez kompilator | Sprawdzane przez type checker (mypy, pyright, pylance) |
| Relacja jawna | Relacja wynikająca ze struktury metod |

Jeśli coś **ma odpowiednie metody i sygnatury**, to **jest traktowane jako ten typ**.

---

## 1. Najpierw: jak wygląda interfejs w Javie

```java
public interface PaymentProcessor {
    void pay(double amount);
}
```

Klasa musi jawnie:

```java
public class StripeProcessor implements PaymentProcessor {
    public void pay(double amount) {
        ...
    }
}
```

---

## 2. Odpowiednik w Pythonie — `Protocol`

```python
from typing import Protocol

class PaymentProcessor(Protocol):
    def pay(self, amount: float) -> None:
        ...
```

To NIE jest klasa bazowa.
To NIE jest ABC.
To jest **kontrakt strukturalny**.

### Co się dzieje "pod maską"? (Rola techniczna `Protocol`)

Sam fakt dopisania `(Protocol)` jako klasy bazowej pełni dwie zupełnie różne funkcje:

**1. Dla narzędzi statycznych (mypy, pyright, Twoje IDE):**
Jest to znacznik (flaga), która mówi analizatorowi kodu: *"Nie traktuj tej klasy jak zwykłego rodzica z drzewa dziedziczenia. Przełącz się na typowanie strukturalne"*. Kiedy type checker widzi, że argument funkcji wymaga typu `PaymentProcessor`, zaczyna analizować podstawiany obiekt (np. `StripeProcessor`) i sprawdza wyłącznie, czy posiada on opisane w protokole metody o takich samych nazwach i sygnaturach (w tym przypadku `pay(float) -> None`). Analizator **całkowicie pomija sprawdzanie dziedziczenia**.

**2. W czasie działania programu (runtime):**
Klasa `typing.Protocol` jest specjalnie przygotowaną pustą klasą bazową, która w runtime nie robi praktycznie nic. Nie modyfikuje w żaden sposób Twoich klas, nie generuje dodatkowego kodu i nie wprowadza narzutu wydajnościowego.  
Istotna "magia" dzieje się dopiero, gdy dodasz dekorator `@runtime_checkable` (zobacz punkt 11) – wtedy metaklasa współpracująca z klasą `Protocol` nadpisuje wbudowane funkcje Pythona: `__instancecheck__` oraz `__subclasscheck__`. Dzięki temu wywołanie w runtime funkcji `isinstance(obj, PaymentProcessor)` nie sprawdza drzewa klas (MRO), ale "pod maską" w locie sprawdza (np. przez `hasattr`), czy przekazany obiekt posiada wymagane metody.

---

## 3. Implementacja — bez dziedziczenia

```python
class StripeProcessor:
    def pay(self, amount: float) -> None:
        print(f"Stripe paid {amount}")
```

Ta klasa **nie wie**, że implementuje `PaymentProcessor`.

A jednak type checker uzna ją za zgodną.

---

## 4. Użycie

```python
def process_payment(processor: PaymentProcessor) -> None:
    processor.pay(100.0)
```

I teraz:

```python
stripe = StripeProcessor()
process_payment(stripe)  # OK
```

Dlaczego OK?

Bo `StripeProcessor` **ma metodę `pay(float) -> None`**.

---

## 5. Co jeśli sygnatura się nie zgadza?

```python
class BadProcessor:
    def pay(self, amount: int) -> None:
        ...
```

`mypy` / `pyright`:

> error: Argument 1 to "process_payment" has incompatible type "BadProcessor"

Mimo że Python w runtime to wykona.
Błąd jest **na etapie statycznej analizy**.

---

## 6. Pełny przykład z kilkoma implementacjami

```python
from typing import Protocol


class PaymentProcessor(Protocol):
    def pay(self, amount: float) -> None:
        ...


class StripeProcessor:
    def pay(self, amount: float) -> None:
        print(f"Stripe paid {amount}")


class PaypalProcessor:
    def pay(self, amount: float) -> None:
        print(f"Paypal paid {amount}")


class MockProcessor:
    def pay(self, amount: float) -> None:
        print(f"Mock paid {amount}")


def checkout(processor: PaymentProcessor) -> None:
    processor.pay(42.0)


def main():
    stripe = StripeProcessor()
    paypal = PaypalProcessor()
    mock = MockProcessor()

    checkout(stripe)
    checkout(paypal)
    checkout(mock)


if __name__ == "__main__":
    main()
```

Żadna klasa **nie dziedziczy** po `PaymentProcessor`.

A jednak wszystko jest typowo poprawne.

---

## 7. Protocol może mieć też atrybuty

```python
class Named(Protocol):
    name: str

def greet(entity: Named) -> None:
    print(f"Hello {entity.name}")
```

Implementacja:

```python
class User:
    def __init__(self, name: str):
        self.name = name

greet(User("Alice"))  # OK
```

---

## 8. Protocol vs ABC (Abstract Base Class)

To jest kluczowe.

### ABC (jak Java)

```python
from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    @abstractmethod
    def pay(self, amount: float) -> None:
        pass
```

Wymaga dziedziczenia:

```python
class StripeProcessor(PaymentProcessor):
```

### Protocol

Nie wymaga.

To ogromna różnica przy:

- testach
- mockach
- kodzie legacy
- third-party bibliotekach
- refaktorach

---

## 9. Protocol + generics

Możesz mieć generyczne interfejsy.

```python
from typing import Protocol, TypeVar

T = TypeVar("T")

class Repository(Protocol[T]):
    def get(self, id: int) -> T:
        ...
```

Implementacja:

```python
class UserRepo:
    def get(self, id: int) -> str:
        return "user"
```

Użycie:

```python
def load(repo: Repository[str]) -> None:
    user = repo.get(1)
```

---

## 10. Najważniejsza rzecz mentalnie (dla kogoś z Javy)

W Javie:

> "Ta klasa implementuje interfejs"

W Pythonie z Protocol:

> "Ta klasa **pasuje do interfejsu**"

To jest *dopasowanie przez strukturę*, nie przez deklarację.

To jest dużo bliższe temu jak faktycznie działa duck typing, ale z kontrolą typu.

---

## 11. Runtime check (opcjonalnie)

Domyślnie Protocol działa tylko dla type checkerów.

Jeśli chcesz sprawdzać w runtime:

```python
from typing import runtime_checkable

@runtime_checkable
class PaymentProcessor(Protocol):
    def pay(self, amount: float) -> None:
        ...
```

Wtedy:

```python
isinstance(stripe, PaymentProcessor)  # True
```

---

## Kiedy używać Protocol zamiast ABC?

Używaj `Protocol`, gdy:

- robisz DI
- piszesz testy / mocki
- integrujesz z obcymi klasami
- robisz refaktory
- budujesz API biblioteki
- chcesz prawdziwy duck typing + typowanie

Używaj `ABC`, gdy:

- chcesz wymusić dziedziczenie
- chcesz współdzielić implementację
- chcesz mieć kontrolę runtime

---

## TL;DR

`Protocol` to **pythonowy odpowiednik interfejsów**, ale:

- strukturalny, nie nominalny
- bez dziedziczenia
- idealny do DI i testów
- bliższy duck typingowi
- weryfikowany przez mypy/pyright

To jest jedna z najbardziej niedocenianych rzeczy w typowanym Pythonie.
