# Wykorzystanie ABC w Pythonie (Abstract Base Classes)

Wbudowany w Pythona moduł `abc` (Abstract Base Classes) służy do tworzenia **klas abstrakcyjnych**. Klasa abstrakcyjna to struktura pełniąca rolę szablonu (interfejsu), która określa, jakie metody i właściwości muszą zostać zaimplementowane, ale sama w sobie z założenia nie jest przeznaczona do tworzenia bezpośrednich instancji.

W przeciwieństwie do tworzenia zwykłych klas z metodami rzucającymi `NotImplementedError`, użycie modułu `abc` sprawia, że Python wyrzuci błąd `TypeError` **już w momencie próby utworzenia obiektu**, jeśli klasa dziedzicząca nie zaimplementuje wszystkich wymaganych metod.

## Kiedy stosować `ABC`?

1. Kiedy chcemy zaprojektować jasny **kontrakt** (interfejs), który inne klasy z naszego systemu muszą bezwzględnie realizować.
2. Gdy mamy wspólną logikę (np. konstruktor `__init__`, czy inne nieabstrakcyjne metody pomocnicze) do uwspólnienia, ale trzon głównej operacji różni się dla każdej klasy implementującej.
3. Gdy zależy nam na ścisłej weryfikacji hierarchii dziedziczenia (`isinstance(obj, NaszeABC)`).
4. Kiedy nie chcemy korzystać z duck-typingu (jak w `typing.Protocol`), tylko wymusić jawne dziedziczenie.

## Kiedy stosować `Protocol` (statyczny Duck Typing)?

Dla porównania, z `typing.Protocol` warto skorzystać:

1. Gdy zależy nam na **luźnym powiązaniu** (loose coupling) – klasy nie muszą bezpośrednio wiedzieć o istnieniu interfejsu ani po nim dziedziczyć.
2. Gdy chcemy opisać typ dla **obiektów pochodzących z zewnętrznych pakietów**, których kod źródłowy nie może dziedziczyć po naszym `ABC`.
3. Kiedy piszemy krótkie typowania "w locie" wymagające jedynie określonych metod (np. `def read(self) -> str`), co jest bardziej w duchu tradycyjnego Pythona.

Więcej o tym w notatce: [Python Protocol (Statyczny Duck Typing)](python-protocol-przyklad.md).

## Kompletny przykład użycia

Zaprojektujemy system wysyłania powiadomień. Posiada on bazową klasyfikację `NotificationSender`, nałożoną dziedziczeniem na poszczególne rozwiązania (np. SMS, Email). 

```python
from abc import ABC, abstractmethod

# 1. Definicja klasy abstrakcyjnej
class NotificationSender(ABC):
    
    # Metoda nienależąca ściśle do interfejsu (metoda konkretna / dzielona)
    def __init__(self, recipient: str):
        self.recipient = recipient

    # Wspólna metoda pomocnicza logiki domenowej
    def log_attempt(self) -> None:
        print(f"Rozpoczynam wysyłkę do: {self.recipient}")

    # Kolejna wspólna metoda (np. podstawowa walidacja dla każdej klasy pochodnej)
    def validate_message(self, message: str) -> bool:
        if not message.strip():
            print("Błąd: Wiadomość jest pusta!")
            return False
        return True

    # 2. Definicja metody abstrakcyjnej, którą KAŻDA klasa pochodna musi nadpisać
    @abstractmethod
    def send(self, message: str) -> bool:
        """Wysyła wiadomość do zdefiniowanego odbiorcy. Zwraca True przy sukcesie."""
        pass


# 3. Pierwsza implementacja (Email)
class EmailSender(NotificationSender):
    
    # Konieczna implementacja abstrakcyjnej metody send
    def send(self, message: str) -> bool:
        # 1. Użycie dziedziczonej metody przed wysłaniem (sprawdzenie walidacji)
        if not super().validate_message(message):
            return False
            
        # 2. Użycie innej dziedziczonej metody (logowanie)
        super().log_attempt()
        
        print(f"[Email do {self.recipient}]: {message}")
        # Logika SMTP...
        return True


# 4. Druga implementacja (SMS)
class SMSSender(NotificationSender):
    
    def __init__(self, recipient: str, country_code: str = "+48"):
        # Użycie konstruktora z klasy bazowej (super)
        super().__init__(recipient)
        self.country_code = country_code
        
    def send(self, message: str) -> bool:
        if not super().validate_message(message):
            return False
            
        super().log_attempt()
        
        phone_number = f"{self.country_code}{self.recipient}"
        print(f"[SMS na {phone_number}]: {message}")
        # Logika API do bramki SMS...
        return True


# Wykorzystanie polimorfizmu na poziomie funkcji
def alert_user(sender: NotificationSender, alert_msg: str) -> None:
    # Funkcja wie, że dostaje obiekty powiązane z NotificationSender, 
    # więc na 100% mają bezpieczną metodę `.send()`
    success = sender.send(alert_msg)
    if not success:
        print("Nie udało się wysłać powiadomienia!")
```

## Próba naruszenia interfejsu (Co się stanie?)

Gdybyśmy spróbowali stworzyć instancję niedokończonej klasy:

```python
class PushSender(NotificationSender):
    # Zapomnieliśmy o implementacji `send`
    pass

# rzuci TypeError: Can't instantiate abstract class PushSender with abstract method send
# device = PushSender("device_id_123") 
```

Wyrzuca błąd od razu, szybciej chroniąc naszą aplikację przed bugami (fail-fast logic).

## Unit Testy (z użyciem `pytest`)

Do przetestowania naszych klas można wykorzystać natywny `pytest`. Ponieważ testujemy m.in. błędy rzucane przez kod strukturalny, przydatny bywa kontekst `pytest.raises`.

```python
import pytest
# Założenie: kod z powyższego przykładu jest np. w module notifications.py
# from notifications import NotificationSender, EmailSender, SMSSender, alert_user

def test_cannot_instantiate_abstract_base_class():
    with pytest.raises(TypeError) as exc_info:
        # Próba bezpośredniego zainstancjowania ABC
        sender = NotificationSender("user@example.com")
        
    assert "Can't instantiate abstract class" in str(exc_info.value)

def test_cannot_instantiate_class_without_implementing_abstract_methods():
    class BadSender(NotificationSender):
        def another_method(self):
            pass
            
    with pytest.raises(TypeError):
        # Klasa dziedziczy po ABC, ale nie posiada `send`
        sender = BadSender("xyz")

def test_email_sender_initialization_and_sending(capsys):
    # capsys to użyteczny fixture pytestu pozwalający na przechwyt printów w konsoli
    email_sender = EmailSender("test@test.com")
    
    # Test działania instancji i rezultatu 
    result = email_sender.send("Hello World")
    assert result is True
    
    # Test "efektu ubocznego"
    captured = capsys.readouterr()
    assert "[Email do test@test.com]: Hello World\n" in captured.out

def test_email_sender_validation(capsys):
    email_sender = EmailSender("test@test.com")
    
    # Próba wysłania pustej wiadomości
    result = email_sender.send("")
    assert result is False
    
    captured = capsys.readouterr()
    assert "Błąd: Wiadomość jest pusta!\n" in captured.out

def test_sms_sender_default_country_code(capsys):
    sms_sender = SMSSender("123456789")
    
    result = sms_sender.send("Alert!")
    assert result is True
    
    captured = capsys.readouterr()
    assert "[SMS na +48123456789]: Alert!\n" in captured.out

def test_polymorphism_via_alert_user(mocker):
    # Możemy też sprawdzić zachowanie polimorficzne stosując spy/mock
    mock_email = EmailSender("admin@domain.com")
    # Zastępuje naturalne wywołanie metody send i obserwuje jej parametry
    mocker.patch.object(mock_email, 'send', return_value=True)
    
    alert_user(mock_email, "System Down!")
    
    mock_email.send.assert_called_once_with("System Down!")
```

## Podsumowanie

- **Bezpieczeństwo kontraktu:** Klasa abstrakcyjna wymusza natychmiastowo poprawne zachowanie klas podrzędnych. Zapobiega rzucaniu `NotImplementedError` niespodziewanie ukrytym głęboko w kodzie klienta.
- **Wspólny stan:** ABC w Pythonie stanowi doskonały sposób na uwspólnienie logiki inicjalizującej powiązanej w `__init__` lub pomocniczych metod współdzielonych przez wszystkie podsystemy z konkretnie sprecyzowaną przymusową końcówką działania – ułatwia to zasadę DRY.
- **Różnica w stosunku do `Protocol`:** Wymaga jawnego określenia pochodzenia (jawne słowo `class Klient(KlasaAbstrakcyjna):`), co z jednej strony wprowadza mocniejsze powiązanie w systemie (tight coupling), a z drugiej czyni hierarchię oczywistą.

---

### Zobacz również w Second Brain
- [Python Protocol (Statyczny Duck Typing)](python-protocol-przyklad.md)
- [Dziedziczenie w Pythonie](dziedziczenie-w-pythonie.md)
- [Python Protocol zamiast interfejsów](python-protocol-zamiast-interfejsów.md)
- [Pydantic vs Dataclasses](Pydantic_vs_Dataclasses.md)
