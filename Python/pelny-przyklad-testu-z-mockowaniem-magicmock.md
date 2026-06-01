# Pełny Przykład Testu z Mockowaniem przy Użyciu `MagicMock`

Mockowanie (tworzenie atrap obiektów) to kluczowa technika w testach jednostkowych. Pozwala ona odizolować testowany kod od jego rzeczywistych zależności (np. baz danych, zewnętrznych API czy serwisów wysyłających e-maile). 

W Pythonie najpotężniejszym i najczęściej stosowanym narzędziem do tego celu jest **`MagicMock`** (z wbudowanej biblioteki `unittest.mock`).

---

## Czym jest `MagicMock` i kiedy go stosować?

`MagicMock` to podklasa standardowego `Mocka`, która posiada domyślnie zaimplementowane wszystkie metody magiczne (tzw. *dunder methods*, np. `__len__`, `__str__`, `__iter__`, `__enter__`). 

> [!TIP]
> **Złota zasada wyboru:** Zawsze używaj `MagicMock` zamiast zwykłego `Mock`. Dzięki temu unikniesz błędów typu `TypeError` w kodzie produkcyjnym, który próbuje np. sprawdzić długość obiektu, użyć go jako menedżera kontekstu (`with`) lub po nim iterować.

Stosujemy go, gdy:
- Chcemy przetestować logikę biznesową danej funkcji/klasy, ale nie chcemy wykonywać rzeczywistych operacji wejścia/wyjścia (I/O).
- Chcemy zasymulować rzadkie lub trudne do wywołania sytuacje (np. awaria sieci, brak środków na karcie płatniczej).
- Chcemy zweryfikować, czy nasza metoda wywołała inne zależności w odpowiedni sposób i z właściwymi parametrami.

---

## Scenariusz Biznesowy do Testu

Zaimplementujemy system obsługi zamówień sklepowych. Nasza klasa `OrderService` współpracuje z dwoma zewnętrznymi systemami (zależnościami):
1. **`PaymentGateway`** (Bramka Płatnicza) – metoda `.charge(card_token, amount)` obciąża kartę klienta. Może rzucić wyjątek `PaymentError`, gdy transakcja zostanie odrzucona.
2. **`EmailService`** (Serwis E-mail) – metoda `.send_confirmation(email, order_id)` wysyła e-mail do klienta.

### Logika Biznesowa (`order_service.py`):
1. Sprawdza, czy kwota zamówienia jest większa od zera.
2. Wywołuje bramkę płatniczą `PaymentGateway.charge`.
3. Jeśli płatność się powiedzie, rejestruje zamówienie i zleca `EmailService.send_confirmation` wysyłkę e-maila.
4. Jeśli płatność rzuci wyjątek `PaymentError`, system powinien przechwycić ten błąd, anulować proces zamówienia i przekazać informację dalej (np. rzucić lokalny wyjątek `OrderProcessingError`), **nie** wysyłając e-maila.

---

## 1. Kod Produkcyjny (`order_service.py`)

Zastosujemy tutaj technikę **Dependency Injection (Wstrzykiwanie Zależności)**, co sprawia, że kod jest niezwykle łatwy w testowaniu i nie wymaga skomplikowanego patchowania globalnych przestrzeni nazw.

```python
# order_service.py
from typing import Protocol

# Definiujemy interfejsy (Protokoły) dla naszych zależności
class PaymentGateway(Protocol):
    def charge(self, card_token: str, amount: float) -> bool:
        ...

class EmailService(Protocol):
    def send_confirmation(self, email: str, order_id: str) -> None:
        ...

# Niestandardowe wyjątki dla czytelnej obsługi błędów
class PaymentError(Exception):
    """Wyjątek rzucany bezpośrednio przez bramkę płatności."""
    pass

class OrderProcessingError(Exception):
    """Lokalny wyjątek aplikacji przy nieudanym procesie zamówienia."""
    pass


class OrderService:
    def __init__(self, payment_gateway: PaymentGateway, email_service: EmailService):
        self.payment_gateway = payment_gateway
        self.email_service = email_service

    def process_order(self, order_id: str, email: str, card_token: str, amount: float) -> str:
        if amount <= 0:
            raise ValueError("Kwota zamówienia musi być większa od zera.")

        try:
            # Próba obciążenia karty klienta
            self.payment_gateway.charge(card_token=card_token, amount=amount)
        except PaymentError as e:
            # W przypadku błędu płatności, nie wysyłamy maila i rzucamy wyjątek domenowy
            raise OrderProcessingError(f"Płatność nie powiodła się: {e}") from e

        # Jeśli płatność przeszła pomyślnie, wysyłamy potwierdzenie e-mail
        self.email_service.send_confirmation(email=email, order_id=order_id)
        
        return f"Order-{order_id}-Processed"
```

---

## 2. Kod Testowy (`test_order_service.py`)

Napiszemy pełny zestaw testów z użyciem frameworka `pytest` oraz `unittest.mock.MagicMock`. Przetestujemy trzy scenariusze:
1. **Scenariusz Sukcesu** – Płatność przechodzi pomyślnie, e-mail zostaje wysłany z poprawnymi argumentami.
2. **Scenariusz Błędu Płatności** – Płatność rzuca wyjątek `PaymentError`, e-mail **nie** zostaje wysłany, a nasza metoda rzuca `OrderProcessingError`.
3. **Scenariusz Błędnych Danych** – Próba przekazania kwoty `<=` 0 kończy się natychmiastowym błędem `ValueError` bez wywoływania jakichkolwiek mocków.

```python
# test_order_service.py
import pytest
from unittest.mock import MagicMock
from order_service import (
    OrderService,
    PaymentError,
    OrderProcessingError,
    PaymentGateway,
    EmailService
)

@pytest.fixture
def mock_payment_gateway() -> MagicMock:
    """Fixture tworzący MagicMock dla bramki płatności."""
    return MagicMock(spec=PaymentGateway)

@pytest.fixture
def mock_email_service() -> MagicMock:
    """Fixture tworzący MagicMock dla serwisu e-mail."""
    return MagicMock(spec=EmailService)

@pytest.fixture
def order_service(mock_payment_gateway: MagicMock, mock_email_service: MagicMock) -> OrderService:
    """Fixture inicjalizujący testowany OrderService z wstrzykniętymi mockami."""
    return OrderService(
        payment_gateway=mock_payment_gateway,
        email_service=mock_email_service
    )


def test_process_order_success(order_service, mock_payment_gateway, mock_email_service):
    """
    TEST 1: Scenariusz sukcesu.
    Sprawdza, czy po udanej płatności zamówienie jest procesowane,
    a e-mail z potwierdzeniem zostaje wysłany z poprawnymi danymi.
    """
    # 1. Konfiguracja mocków (ARRANGE)
    # Domyślnie MagicMock dla metody charge zwróci True przy wywołaniu
    mock_payment_gateway.charge.return_value = True

    # 2. Wywołanie testowanej metody (ACT)
    result = order_service.process_order(
        order_id="1001",
        email="klient@example.com",
        card_token="tok_visa_123",
        amount=250.50
    )

    # 3. Weryfikacja wyników i wywołań (ASSERT)
    # A. Sprawdzenie wartości zwracanej przez testowaną metodę
    assert result == "Order-1001-Processed"

    # B. Weryfikacja czy bramka płatności została wywołana dokładnie raz z poprawnymi argumentami
    mock_payment_gateway.charge.assert_called_once_with(
        card_token="tok_visa_123",
        amount=250.50
    )

    # C. Weryfikacja czy serwis e-mail wysłał potwierdzenie dokładnie raz z poprawnymi danymi
    mock_email_service.send_confirmation.assert_called_once_with(
        email="klient@example.com",
        order_id="1001"
    )


def test_process_order_payment_failure(order_service, mock_payment_gateway, mock_email_service):
    """
    TEST 2: Scenariusz błędu płatności (wykorzystanie side_effect).
    Sprawdza, czy w przypadku błędu bramki płatności OrderService rzuca
    wyjątek OrderProcessingError oraz czy wysyłka e-maila zostaje zablokowana.
    """
    # 1. Konfiguracja mocków (ARRANGE)
    # Używamy side_effect, aby wywołanie metody charge rzuciło określony wyjątek
    mock_payment_gateway.charge.side_effect = PaymentError("Brak środków na karcie.")

    # 2. Wywołanie i weryfikacja rzucenia wyjątku (ACT & ASSERT)
    with pytest.raises(OrderProcessingError) as exc_info:
        order_service.process_order(
            order_id="1002",
            email="klient@example.com",
            card_token="tok_declined_999",
            amount=99.99
        )

    # Weryfikacja czy wiadomość błędu jest poprawna i zawiera powód z bramki
    assert "Płatność nie powiodła się: Brak środków na karcie." in str(exc_info.value)

    # 3. Weryfikacja zachowania zależności (ASSERT)
    # A. Bramka płatności musiała zostać wywołana
    mock_payment_gateway.charge.assert_called_once_with(
        card_token="tok_declined_999",
        amount=99.99
    )

    # B. KLUCZOWE: Serwis e-mail NIE MÓGŁ zostać wywołany (transakcja nieudana)
    mock_email_service.send_confirmation.assert_not_called()


def test_process_order_invalid_amount(order_service, mock_payment_gateway, mock_email_service):
    """
    TEST 3: Walidacja danych wejściowych.
    Sprawdza, czy przy ujemnej kwocie natychmiast rzucany jest ValueError
    bez uruchamiania jakichkolwiek zewnętrznych zależności.
    """
    # ACT & ASSERT
    with pytest.raises(ValueError, match="Kwota zamówienia musi być większa od zera"):
        order_service.process_order(
            order_id="1003",
            email="klient@example.com",
            card_token="tok_any",
            amount=-50.0
        )

    # Ponieważ walidacja nie przeszła, mocki nie mogły być w ogóle dotknięte
    mock_payment_gateway.charge.assert_not_called()
    mock_email_service.send_confirmation.assert_not_called()
```

---

## Analiza Działania Mockowania w Przykładzie

W powyższym teście użyliśmy kilku najważniejszych mechanizmów `MagicMock`:

| Mechanizm | Użycie w kodzie | Wyjaśnienie |
| :--- | :--- | :--- |
| **`return_value`** | `mock.charge.return_value = True` | Definiuje, co ma zostać zwrócone, gdy dana metoda mocka zostanie wywołana. |
| **`side_effect`** | `mock.charge.side_effect = PaymentError(...)` | Pozwala zdefiniować dynamiczne zachowanie. Gdy przypiszemy do niego wyjątek, mock go **rzuci**. Gdy przypiszemy listę, mock przy kolejnych wywołaniach będzie zwracał kolejne elementy z listy. |
| **`spec`** | `MagicMock(spec=PaymentGateway)` | Zabezpiecza mocka przed odpytywaniem o metody, które nie istnieją w oryginalnej klasie/interfejsie `PaymentGateway` (zapobiega to "cichym" literówkom w testach). |
| **`assert_called_once_with`** | `mock.method.assert_called_once_with(...)` | Asercja weryfikująca, czy metoda mocka została wywołana **dokładnie raz** i z **konkretnymi argumentami**. |
| **`assert_not_called`** | `mock.method.assert_not_called()` | Asercja sprawdzająca, czy metoda **nigdy** nie została wywołana podczas trwania testu. |

---

## Przydatne Powiązania

- Jeśli chcesz dowiedzieć się więcej o mockowaniu modułów przy użyciu fixture `mocker` z `pytest-mock` oraz o patchowaniu lokalnych referencji bez stosowania Dependency Injection, przeczytaj główny artykuł:
  [Mockowanie i Monkeypatching w PyTest](PyTest_Mockowanie.md)
