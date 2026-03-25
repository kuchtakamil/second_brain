# Wyjaśnij czym jest w Python self.__dict__

**Data:** 9 lut 2026, 16:33:02 CET

---

**User:**

Wyjaśnij czym jest w Python self.__dict__

---

**Gemini:**

W języku Python atrybut `self.__dict__` jest słownikiem służącym do przechowywania przestrzeni nazw instancji obiektu. Każdy obiekt (z wyjątkiem tych korzystających z mechanizmu `__slots__`) posiada ten atrybut, który mapuje nazwy atrybutów instancji na ich aktualne wartości.

---

### Mechanizm działania i struktura

Kiedy przypisujesz wartość do atrybutu obiektu za pomocą `self.attribute = value`, Python wewnętrznie wykonuje operację wpisania klucza do słownika `__dict__`. Jest to fundamentalny element implementacji modelu obiektowego w Pythonie, oparty na dynamicznym dostępie do danych.

- **Klucze:** Stringi reprezentujące nazwy atrybutów instancji.
- **Wartości:** Referencje do obiektów przypisanych do tych atrybutów.

### Praktyczne zastosowania techniczne

#### 1. Dynamiczna inspekcja i modyfikacja

Dzięki `self.__dict__` możesz w czasie rzeczywistym sprawdzać stan obiektu lub masowo modyfikować jego atrybuty. Jest to często wykorzystywane w systemach ORM lub podczas serializacji danych (np. konwersja obiektu na format JSON).

```
class AdvancedComponent:
    def __init__(self, **kwargs):
        # Masowe przypisanie argumentów keyword do instancji
        self.__dict__.update(kwargs)

    def get_state(self):
        return self.__dict__.copy()

component = AdvancedComponent(id=101, status="active", logic_level=5)
print(component.status)  # Wynik: active
```

#### 2. Metaprogramowanie i Proxy

`__dict__` pozwala na manipulację atrybutami, które nie zostały jawnie zdefiniowane w kodzie klasy, co jest kluczowe przy tworzeniu dekoratorów klasowych lub wzorców typu *Adapter*.

### Relacja z `getattr()` i `setattr()`

Funkcje wbudowane `getattr(obj, 'name')` oraz `setattr(obj, 'name', value)` w większości przypadków operują właśnie na słowniku `__dict__`. Wywołanie `obj.x` inicjuje następujący łańcuch poszukiwań:

1. Sprawdzenie, czy `x` istnieje w `obj.__dict__`.
2. Jeśli nie, przeszukanie `__dict__` klasy, a następnie klas nadrzędnych (zgodnie z MRO).
3. Wywołanie metody `__getattr__`, jeśli została zdefiniowana.

---

### Wydajność i `__slots__`

Choć `__dict__` zapewnia ogromną elastyczność (możliwość dodawania atrybutów "w locie"), wiąże się to z pewnym narzutem pamięciowym. W systemach, gdzie tworzone są miliony małych obiektów, stosuje się `__slots__`.

- **Z `__dict__`**: Obiekt jest dynamiczny, słownik zajmuje dodatkową pamięć na hashowanie kluczy.
- **Z `__slots__`**: Atrybuty są przechowywane w stałej strukturze (tablicy), a `__dict__` nie jest tworzony, co drastycznie redukuje zużycie RAM, ale blokuje możliwość dynamicznego dodawania nowych atrybutów spoza listy.

### Różnica między `__dict__` instancji a klasy

Warto odróżnić `self.__dict__` od `ClassName.__dict__`:

- **`self.__dict__`**: Zawiera dane specyficzne dla konkretnego obiektu (instancji).
- **`ClassName.__dict__`**: Zawiera metody, zmienne klasowe (static fields) oraz deskryptory. Jest obiektem typu `mappingproxy` (tylko do odczytu bezpośredniego), co zapewnia integralność definicji klasy.

Czy chciałbyś, abym przygotował przykład implementacji customowego serializatora, który wykorzystuje `__dict__` do filtrowania prywatnych atrybutów?