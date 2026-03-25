# Wzorzec Projektowy: Registry (Rejestr) w Pythonie

## Wprowadzenie

Wzorzec Registry (Rejestr) to niezwykle przydatny wzorzec projektowy (często klasyfikowany jako wariacja fabryki lub wzorzec kreacyjny), który służy do przechowywania globalnego i scentralizowanego spisu obiektów, klas lub funkcji. W Pythonie jest on bardzo popularny i najczęściej realizowany za pomocą słowników (`dict`) w połączeniu z **dekoratorami**.

Wzorzec ten jest idealny do tworzenia systemów wtyczek (plugins), systemów *factory* (fabryk), routingów webowych (jak np. w we frameworkach Flask, czy FastAPI), analizatorów danych, modyfikatorów tekstu czy systemów zdarzeń (event handlers). Pozwala na rejestrowanie komponentów podczas ładowania modułów bez konieczności modyfikowania centralnego rdzenia kodu (silnika aplikacji).

## Główne zalety

- **Zgodność z Open/Closed Principle (Zasada otwarte-zamknięte):** Możesz dodawać nowe funkcjonalności (np. nowe typy powiadomień) poprzez dodanie nowego modułu lub pliku, bez modyfikowania kodu zarządzającego/uruchamiającego te powiadomienia.
- **Decoupling (Luźne powiązanie):** Komponenty nie muszą nic o sobie nawzajem wiedzieć. Wiedzą tylko o centralnym rejestrze.
- **Deklaratywność:** Użycie dekoratorów sprawia, że blisko kodu konkretnej klasy/funkcji znajduje się intencja jej ponownego użycia (*"zarejestruj to jako wtyczkę X"*).

## Jak to działa?

1. Tworzymy centralny obiekt (zazwyczaj słownik - np. w atrybucie klasy, lub jako globalną instancję), który służy jako rejestr.
2. Tworzymy mechanizm (najczęściej dekorator parametryzowany), który dodaje element do rejestru, przypisując mu określony klucz (np. nazwę (`str`), typ, czy Enum).
3. Reszta aplikacji, gdy potrzebuje użyć tej logiki, jedynie zgłasza do rejestru prośbę: "Daj mi funkcję/klasę zapisaną pod kluczem X", na podstawie czego może dokonać instancjonowania obiektu, bądź wykonania funkcji.

---

## Kompletny przykład: System przetwarzania powiadomień

Poniższy przykład demonstruje implementację wzorca Registry do zarządzania różnymi typami powiadomień (Email, SMS, Push, itd.).

Zbudujemy architekturę, w której dodanie nowego typu powiadomienia (np. `Slack`) nie wymaga żadnej modyfikacji głównej klasy wysyłającej!

```python
from typing import Callable, Dict, Any

# ==========================================
# DEFINICJA TYPÓW I GŁÓWNA KLASA REJESTRU
# ==========================================

# Typ domniemany dla funkcji obsługującej powiadomienie.
# Przyjmuje treść wiadomości i dodatkowy kontekst, zwraca bool (sukces/porażka)
NotificationHandler = Callable[[str, Dict[str, Any]], bool]

class NotificationRegistry:
    """Centralny rejestr dla obsługi powiadomień w naszej aplikacji."""
    
    def __init__(self):
        # Nasz wewnętrzny rejestr mapujący nazwy na funkcje powiadamiające
        self._handlers: Dict[str, NotificationHandler] = {}

    def register(self, name: str) -> Callable:
        """
        Dekorator służący do rejestrowania nowych handlerów powiadomień.
        
        :param name: Nazwa (klucz) pod jaką handler ma być zarejestrowany.
        """
        def decorator(func: NotificationHandler) -> NotificationHandler:
            if name in self._handlers:
                raise ValueError(f"⚠️ Uwaga: Handler dla '{name}' jest już zarejestrowany!")
            
            # Zapis funkcji w słowniku
            self._handlers[name] = func
            print(f"✅ Zarejestrowano pomyślnie kanał: '{name}' -> func: {func.__name__}")
            
            return func
        return decorator

    def get_handler(self, name: str) -> NotificationHandler:
        """Pobiera handler (funkcję) z rejestru na podstawie nazwy."""
        handler = self._handlers.get(name)
        if not handler:
            raise ValueError(f"❌ Nie znaleziono zdefiniowanego handlera dla: '{name}'")
        return handler
        
    def dispatch(self, name: str, message: str, context: Dict[str, Any] = None) -> bool:
        """Fasada: Odnajduje odpowiedni handler i automatycznie go wykonuje."""
        if context is None:
            context = {}
            
        print(f"\n[Dispatcher] Próba wysłania przez kanał '{name}'...")
        try:
            handler = self.get_handler(name)
            return handler(message, context)
        except ValueError as e:
            print(e)
            return False

# ==========================================
# 1. TWORZYMY INSTANCJĘ REJESTRU
# ==========================================
notifier = NotificationRegistry()

# ==========================================
# 2. REJESTRUJEMY KANAŁY ZA POMOCĄ DEKORATORA
# ==========================================

@notifier.register("email")
def send_email(message: str, context: Dict[str, Any]) -> bool:
    email_address = context.get("email", "nieznany@adres.pl")
    print(f"📧 WYSYŁANIE EMAIL to {email_address}: {message}")
    # Tu logika łączenia z SMTP...
    return True

@notifier.register("sms")
def send_sms(message: str, context: Dict[str, Any]) -> bool:
    phone = context.get("phone_number", "brak numeru")
    print(f"📱 WYSYŁANIE SMS do {phone}: {message}")
    # Tu logika łączenia z Twilio/Bramką SMS...
    return True

@notifier.register("push")
def send_push(message: str, context: Dict[str, Any]) -> bool:
    device_id = context.get("device_id", "unknown_device")
    print(f"🔔 WYSYŁANIE PUSH do urządzenia [{device_id}]: {message}")
    # Tu logika integracji z Firebase Cloud Messaging...
    return True

# ROZSZERZALNOŚĆ W PRAKTYCE:
# Jeśli po 3 miesiącach szef mówi "Dodajmy wsparcie dla Slacka",
# my dodajemy tylko poniższe linie kodu. Nie dotykamy `NotificationRegistry` 
# ani żadnego logiki `if/elif` która zwykle decyduje co wysłać!

@notifier.register("slack")
def send_to_slack(message: str, context: Dict[str, Any]) -> bool:
    channel = context.get("channel", "#general")
    print(f"💬 WYSYŁANIE SLACK na kanał {channel}: {message}")
    # Tu logika Slack API...
    return True

# ==========================================
# 3. UŻYCIE (Wywołanie abstrakcyjne w rdzeniu aplikacji)
# ==========================================

if __name__ == "__main__":
    print("-" * 40)
    
    # Symulacja zdarzeń w aplikacji. Aplikacja decyduje użyć jakiegoś kanału dynamicznie
    notifier.dispatch("email", "Witaj w naszym nowym systemie!", {"email": "jan@kowalski.pl"})
    notifier.dispatch("sms", "Zalogowano do serwisu. Typowy kod SMS to: 12345", {"phone_number": "+48 123 456 789"})
    notifier.dispatch("slack", "Błąd bazy danych na gałęzi produkcyjnej!", {"channel": "#alerts"})
    
    # Próba użycia nieistniejącego handlera
    notifier.dispatch("fax", "Proszę wydrukować ten ważny dokument PDF.")
```

## Alternatywny scenariusz: Zastosowanie na klasach

Wzorzec ten możemy spotkać w zaawansowanych systemach ORM, w walidatorach (jak np. w Pydantic, gdzie wykorzystuje się pewną jego wariację) czy systemach wtyczkowych klasyfikujących klasy do uruchomienia. Rejestrujemy tutaj instrukcję w postaci `klasy`, nie od razu ją powołując do życia (tzw. leniwe ładowanie / instancjonowanie podczas parsowania):

```python
class ComponentRegistry:
    # Używamy statycznego słownika bez powoływania instancji samego rejestru
    _registry = {}

    @classmethod
    def register(cls, name):
        def inner_wrapper(wrapped_class):
            cls._registry[name] = wrapped_class
            return wrapped_class
        return inner_wrapper
        
    @classmethod
    def get_instance_for(cls, name, *args, **kwargs):
        """Metoda pełniąca formę prostej fabryki kreacyjnej."""
        if name not in cls._registry:
            raise ValueError(f"Brak komponentu: {name}")
        
        # Pobieramy klasę z rejestru i ZWRACAMY JEJ NOWĄ INSTANCJĘ wywołując typ
        component_class = cls._registry[name]
        return component_class(*args, **kwargs)

@ComponentRegistry.register('user_model')
class User:
    def __init__(self, username):
        self.username = username
        
    def __repr__(self):
        return f"User(username='{self.username}')"

# Powołanie instancji z użyciem rejestru-fabryki w jednym:
obiekt_usera = ComponentRegistry.get_instance_for('user_model', username='admin123')
print(obiekt_usera) # User(username='admin123')
```

## Bonus: Wbudowany `singledispatch`

Python posiada świetne wbudowane narzędzie wspierające specyficzną wersję Rejestru dla przeciążania funkcji na podstawie typów (`functools.singledispatch`). Pozwala ono dynamicznie wybierać konkretną implementację funkcji w zależności od przekazanego typu pierwszej zmiennej do funkcji nadrzędnej. Pod spodem korzysta z bardzo wyrafinowanego i szybkiego mechanizmu w stylu *registry*.

---

## Zaawansowany przykład: Rejestr wielowymiarowy z Auto-Discovery (Lazy Loading)

W dużych projektach (np. systemach RAG, architekturach opartych o pluginy, systemach modułowych) często pojawia się potrzeba rejestrowania komponentów z podziałem na różne domeny i interfejsy – na przykład inne klasy dla przetwarzania tekstu (`Chunker`), inne dla wektoryzatorów (`Embedder`).

Poniższy przykład rozbudowuje podstawowy wzorzec, stosując dwuwymiarowe grupowanie wtyczek oraz wpierając tzw. automatyczne odkrywanie (ang. *Auto-Discovery*).

### Kod implementacji (Oparty na typowaniu i `pkgutil`)

```python
"""Plugin registry — maps (interface, name) pairs to concrete classes."""

from __future__ import annotations

import importlib
import logging
import pkgutil
from typing import Any, TypeVar

logger = logging.getLogger(__name__)

# Rejestr dwuwymiarowy: { nazwa_interfejsu: { nazwa_implementacji: klasa } }
_REGISTRY: dict[str, dict[str, type]] = {}

T = TypeVar("T")

def register(interface: str, name: str):
    """
    Dekorator klasy, który zapisuje klasę w `_REGISTRY[interface][name]`.
    Zwraca oryginalną klasę bez zmian, przez co bardzo dobrze współpracuje z analizatorami typów (np. mypy).
    """
    def decorator(cls: type[T]) -> type[T]:
        # setdefault automatycznie tworzy pusty słownik dla nowego interfejsu
        _REGISTRY.setdefault(interface, {})[name] = cls
        return cls
    return decorator

def create(interface: str, name: str, **kwargs: Any) -> Any:
    """
    Wzorzec fabryki wbudowany z rejestrem:
    Instancjonuje i zwraca zarejestrowaną klasę, podając `kwargs` jako argumenty jej konstruktora.
    """
    try:
        cls = _REGISTRY[interface][name]
    except KeyError:
        available = list(_REGISTRY.get(interface, {}).keys())
        raise KeyError(
            f"No implementation '{name}' registered for interface '{interface}'. "
            f"Available: {available}"
        ) from None
    return cls(**kwargs)

def list_implementations(interface: str) -> list[str]:
    """Zwraca listę zarejestrowanych implementacji dla konkretnego interfejsu."""
    return list(_REGISTRY.get(interface, {}).keys())

def import_all_implementations() -> None:
    """
    Kluczowy element oparty o dynamiczny import (Lazy Loading).
    Wymusza zaimportowanie wszystkich podpakietów, co spowoduje wywołanie rejestrujących dekoratorów.
    Lokalnie można to obsłużyć iterując po `pkgutil.iter_modules`.
    """
    _import_subpackages("ai_book_rag")
    
def _import_subpackages(package_name: str) -> None:
    # Wewnętrzna metoda do poszukiwania modułów, np. przy użyciu pkgutil lub path
    pass
```

### Zastosowanie (Cykl Życia)

Deweloper definiuje nową klasę w jakimkolwiek pliku wewnątrz pakietu.

```python
from my_app.core.registry import register
from my_app.core.interfaces import Chunker

@register("chunker", "fixed_size")
class FixedSizeChunker(Chunker):
    def __init__(self, max_tokens: int):
        self.max_tokens = max_tokens
```

Przy starcie aplikacji ładujemy wtyczki (Auto-Discovery) i możemy ich używać:

```python
from my_app.core.registry import create, import_all_implementations

# Krok 1: Wczytanie wszystkich plików aplikacji (co wywoła dekoratory @register)
import_all_implementations()

# Krok 2: Powołanie klasy do życia przez nasz rejestr-fabrykę
moj_chunker = create("chunker", "fixed_size", max_tokens=512)
```

### Analiza tego podejścia i kluczowe korzyści

1. **Rejestr Dwuwymiarowy (Multi-dimensional Registry):** Zamiast płaskiego słownika mapującego jedną nazwę na klasę, mamy tutaj zagnieżdżony słownik: `dict[str, dict[str, type]]`. Pozwala to na organizowanie pluginów "tematycznie" – unikamy kolizji nazw. Słowo `fixed_size` mogłoby mieć zupełnie inny sens w kontekście interfejsu, np. `parser` i inny w `chunker`.

2. **Przezroczysty dekorator (Transparent Decorator) & Type Hinting:** Dzięki użyciu bloku generycznego `T = TypeVar("T")`, dekorator `@register` sygnalizuje np. Mypy'emu, że przetwarza zmienną i zwraca ją dokładnie w tym samym kształcie `type[T]`. Chronimy tym sposobem informacje typowania wokół oryginalnej klasy – w wielu źle zaprojektowanych generycznych dekoratorach traci się wsparcie autouzupełniania u klas.

3. **Rozbudowana Fabryka (`create`) z lepszymi logami:** Metoda ta służy jako punkt wejścia i wzorzec metody wytwórczej (Factory Pattern). Rejestr nie tylko zwraca referencję do typu (co by wymuszało ręczne wywoływanie nawiasów przez użytkownika), ale też natychmiastowo przekazuje argumenty pozycyjne lub parametry kluczowe `**kwargs`. Jeśli nazwa nie istnieje, funkcja łapie wyjątkowo dokładnie błąd i elegancko listuje użytkownikowi, **jakie nazwy dla tego konkretnego interfejsu aktualnie były zarejestrowane**.

4. **Leniwe Ładowanie z Auto-Discovery (Dynamiczne importy):**
   W klasycznym rejestrze występuje tzw. *"Problem martwego kodu"*. Jeśli główny plik aplikacji (`config.py` albo `main.py`) **jawnie nie zaimportuje pliku** `moj_parser.py`, to kod z definicją dekoratora nigdy nie zostanie przetworzony przez interpreter i klasa do rejestru nie trafi! To zabija ideę luźnego powiązania.
   Dzięki stworzeniu spoiwa w postaci `import_all_implementations()`, jesteśmy w stanie uruchomić potężny mechanizm (tzw. *Auto-Discovery* często oparty na `pkgutil.walk_packages`). Narzędzie takie przy uruchomieniu aplikacji przelatuje po naszych katalogach i sztucznie wywołuje polecenia *import*, co bez żadnej dalszej interakcji z naszej strony odpala wszystkie dekoratory `@register` w projekcie i ładuje zależności tam gdzie ich miejsce. Jest to rozwiązanie klasy enterprise.
