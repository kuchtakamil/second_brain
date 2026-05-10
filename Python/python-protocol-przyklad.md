# Wykorzystanie `Protocol` w Pythonie (Duck Typing statyczny)

W module `typing` Pythona od wersji 3.8 pojawiła się klasa `Protocol`. Służy ona do definiowania **strukturalnego typowania subów (structural subtyping)**, co w świecie Pythona często nazywane jest statycznym *duck typingiem*.

Dzięki `Protocol` nie musimy jawnie dziedziczyć po klasie bazowej (jak ma to miejsce w przypadku użycia `abc.ABC`), aby narzędzia analizy statycznej (np. `mypy`) i samo środowisko programistyczne (IDE) rozpoznawały, że obiekt pasuje do danego interfejsu. Wystarczy, że klasa (świadomie lub nie) implementuje w swoim ciele wymagane przez protokół metody z właściwymi sygnaturami.

## Kiedy stosować `Protocol`?

1. Kiedy zależy nam na luźnym powiązaniu (loose coupling) i nie chcemy zmuszać zewnętrznych klas, nierzadko pochodzących z pakietów importowanych z zewnątrz, do dziedziczenia z naszego lokalnego interfejsu.
2. Gdy piszemy funkcję, która oczekuje obiektu implementującego określoną metodę (np. `read()`, `execute()`, `send()`), ale nie wiemy i nie interesuje nas jego dokładna ścieżka dziedziczenia w hierarchii klas.
3. W typowaniu zależności do mockowania przy wstrzykiwaniu zależności (dependency injection) – ułatwia to testy modularne, bo pozwala na zaleznosc klasy od minimalistycznego interfejsu zamiast "opasłych" klas konkretnych.

## Kompletny przykład użycia

Zbudujemy prosty system przetwarzania płatności, gdzie wykorzystamy `Protocol` dla procesora płatności. Zdefiniujemy protokół `PaymentProcessor` oraz dwie niezależne klasy, które go implementują, ale *nie* dziedziczą po nim wprost.

```python
from typing import Protocol

# 1. Definicja protokołu
class PaymentProcessor(Protocol):
    def process_payment(self, amount: float) -> bool:
        """Przetwarza płatność i zwraca True w przypadku sukcesu."""
        ...

# 2. Implementacja A (Paypal)
class PaypalProcessor:
    def __init__(self, email: str):
        self.email = email

    # Klasa ma wymaganą metodę, więc automatycznie "wpisuje się" w protokół PaymentProcessor
    def process_payment(self, amount: float) -> bool:
        print(f"Przetwarzam {amount} PLN przez PayPal ({self.email}).")
        # logika np. call do API PayPal
        return True

# 3. Implementacja B (Stripe)
class StripeProcessor:
    def __init__(self, api_key: str):
        self.api_key = api_key

    # Podobnie jak wyżej, implementuje strukturę oczekiwaną przez protokół
    def process_payment(self, amount: float) -> bool:
        print(f"Przetwarzam {amount} PLN przez Stripe API.")
        return True

# 4. Użycie protokołu jako adnotacji w zarządzającej klasie lub funkcji
class CheckoutSession:
    # Adnotacja typu wskazuje: Oczekujemy JAKIEGOKOLWIEK obiektu, który spełnia PaymentProcessor
    def __init__(self, processor: PaymentProcessor):
        self.processor = processor

    def checkout(self, total_amount: float) -> str:
        # Poniżej IDE/mypy wie, że metoda .process_payment jest w 100% poprawna i bezpieczna
        success = self.processor.process_payment(total_amount)
        if success:
            return "Płatność zakończona sukcesem."
        return "Płatność odrzucona."
```

Gdybyśmy spróbowali uruchomić narzędzie do sprawdzania typów (jak `mypy`) po zadeklarowaniu tych klas i utworzeniu zmiennej z niewłaściwym typem:

```python
class CryptoProcessor:
    def pay(self, amount: float) -> bool:
        return True

# To spowoduje zaznaczenie na czerwono w IDE i wyrzucenie błedu przez mypy,
# (ponieważ brakuje wymaganej metody `process_payment`):
# session = CheckoutSession(CryptoProcessor())
```

## Unit Testy (z użyciem `pytest` oaz statycznych "Fake Objects")

Poniżej znajduje się kilka unit testów wskazujących na elastyczność i moc płynącą z wykorzystania `Protocol`. Dzięki tak zdefiniowanej zależności klasy `CheckoutSession`, możemy w łatwy sposób wstrzykiwać do niej obiekty przeznaczone wyłącznie do testów (tzw. _Fake Objects_ lub _Spies_ / _Mocks_):

```python
import pytest
from unittest.mock import Mock

# Założenie: kod z poprzedniego bloku znajduje się w module payment_system.py
# from payment_system import CheckoutSession, PaymentProcessor, PaypalProcessor, StripeProcessor

# 1. Testowanie z faktyczną / realną implementacją (klasyczny przypadek)
def test_checkout_with_paypal():
    paypal = PaypalProcessor(email="test@example.com")
    session = CheckoutSession(processor=paypal)
    
    result = session.checkout(150.0)
    
    assert result == "Płatność zakończona sukcesem."

# 2. Utworzenie prostego Fake Object na potrzeby testu (bez używania bibliotek do mockowania)
# Bardzo promowane i popularne w projektach mocno "typujących"
class FakeFailingProcessor:
    # Klasa ma wyłącznie jedną odpowiedzialność – spełnia protokół i odrzuca płatność
    def process_payment(self, amount: float) -> bool:
        return False

def test_checkout_with_fake_processor_returning_false():
    fake_processor = FakeFailingProcessor()
    session = CheckoutSession(processor=fake_processor)
    
    result = session.checkout(999.0)
    assert result == "Płatność odrzucona."

# 3. Tworzenie Fake Spy Object (do obserwacji wewnętrznego stanu testu)
class SpyProcessor:
    def __init__(self):
        self.amounts_processed: list[float] = []
        
    def process_payment(self, amount: float) -> bool:
        self.amounts_processed.append(amount)
        return True

def test_checkout_calls_process_payment_with_correct_amount():
    spy = SpyProcessor()
    session = CheckoutSession(processor=spy)
    
    session.checkout(42.50)
    
    assert spy.amounts_processed == [42.50]

# 4. Testowanie z użyciem generatora Mock (standardowy unittest.mock)
def test_checkout_with_mocked_processor():
    # Uwaga: używająć mypy wymusza to zazwyczaj rzutowanie "cast()", 
    # mocki omijają system typów oparty bezpośrednio o Protocol.
    mock_processor = Mock()
    mock_processor.process_payment.return_value = True
    
    session = CheckoutSession(processor=mock_processor) # type: ignore
    result = session.checkout(100.0)
    
    assert result == "Płatność zakończona sukcesem."
    mock_processor.process_payment.assert_called_once_with(100.0)
```

## Podsumowanie

- Klasa biznesowa/używająca modułu (`CheckoutSession`) zupełnie nic nie wie o szczegółach wdrożenia np. `PaypalProcessor` czy wywołaniach zapytań HTTP w `StripeProcessor`. Zależy jedynie od abstrakcji (`PaymentProcessor`).
- Narzędzia takie jak `mypy` zaprotestują, jeśli przekażemy do powiązanej klasy obiekt jawnie niezgodny z wirtualnym interfejsem (czyli np. bez ujętej sygnatury `process_payment(amount: float) -> bool`).
- Uzyskujemy całą kontrolę i ścisłe typowanie kojarzące się z językami takimi jak Java czy C# ze "statycznymi interfejsami", pisząc jednocześnie bardzo czysty, uproszczony kod zgodny z duchem klasycznego pythonowskiego *duck typingu*, gdzie to właściwości obiektu (a nie nagłówek klasy i hierarchia dziedziczenia) definiują jego przydatność.

---

### Zobacz również w Second Brain
- [Dziedziczenie w Pythonie](dziedziczenie-w-pythonie.md)
- [Python - Pydantic vs Dataclasses](Pydantic_vs_Dataclasses.md)
- [Python Protocol zamiast interfejsów](python-protocol-zamiast-interfejsów.md) (związany z tematem wpis omawiający Protocol jako zastępstwo staromodnych wcięć interfejsowych w kodzie)
