# Odpowiednik readObject / writeObject z Javy Jeśli chcesz kontrolować serializacj

**Data:** 9 lut 2026, 14:36:52 CET

---

**User:**

Odpowiednik readObject / writeObject z Javy
Jeśli chcesz kontrolować serializację (jak w Javie):


class User:
    def __init__(self, name, password):
        self.name = name
        self.password = password

    def __getstate__(self):
        state = self.__dict__.copy()
        del state["password"]      # nie zapisujemy hasła
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.password = None

Wyjaśnij __getstate__ i __setstate__

---

**Gemini:**

W Pythonie protokół `pickle` obsługuje customizację procesu serializacji i deserializacji poprzez metody specjalne `__getstate__` oraz `__setstate__`. Są one bezpośrednim odpowiednikiem mechanizmów `writeObject` i `readObject` znanych z interfejsu `Serializable` w Javie.

### Metoda `__getstate__`

Metoda ta jest wywoływana w momencie serializacji obiektu (funkcja `pickle.dump()` lub `pickle.dumps()`). Jej zadaniem jest przygotowanie i zwrócenie obiektu reprezentującego stan, który faktycznie ma zostać zapisany.

- **Domyślne zachowanie:** Jeśli nie zdefiniujesz tej metody, Python domyślnie pobiera zawartość słownika `self.__dict__`.
- **Zastosowanie:** Używamy jej, gdy chcemy odfiltrować dane wrażliwe (hasła, klucze API), wykluczyć obiekty nie-serializowalne (np. otwarte deskryptory plików, połączenia z bazą danych, wątki) lub zoptymalizować rozmiar wynikowego bajtostrumienia.
- **Zwracana wartość:** Najczęściej jest to słownik (`dict`), ale `pickle` akceptuje dowolny obiekt.

### Metoda `__setstate__`

Metoda ta jest wywoływana podczas deserializacji (funkcja `pickle.load()` lub `pickle.loads()`). Otrzymuje ona jako argument `state`, czyli dokładnie to, co zwróciła metoda `__getstate__`.

- **Domyślne zachowanie:** Jeśli nie istnieje, Python po prostu aktualizuje `self.__dict__` wartościami ze zdeserializowanego słownika.
- **Zastosowanie:** Pozwala na przywrócenie stanu obiektu do pełnej funkcjonalności. Można tu zainicjalizować wartości domyślne dla pominiętych pól, otworzyć nowe połączenia sieciowe lub przeliczyć wartości cache'owane, które nie były zapisywane.
- **Mechanizm działania:** Ważne jest, że podczas deserializacji z `__setstate__`, metoda `__init__` zazwyczaj **nie jest wywoływana**. Obiekt jest tworzony w stanie "surowym", a następnie wypełniany danymi.

---

### Porównanie z Java Serialization

| Cecha | Java (`Serializable`) | Python (`pickle`) |
| --- | --- | --- |
| **Metoda zapisu** | `private void writeObject(ObjectOutputStream out)` | `def __getstate__(self)` |
| **Metoda odczytu** | `private void readObject(ObjectInputStream in)` | `def __setstate__(self, state)` |
| **Modyfikator dostępu** | Prywatna (wywoływana przez refleksję) | Publiczna metoda specjalna (dunder) |
| **Dane wejściowe** | Strumień (`ObjectOutputStream`) | Obiekt stanu (zazwyczaj `dict`) |
| **Wykluczanie pól** | Słowo kluczowe `transient` | Ręczne usunięcie ze stanu w `__getstate__` |

### Zaawansowane aspekty techniczne

1. **Sloty (`__slots__`):** Jeśli klasa definiuje `__slots__`, domyślny mechanizm serializacji ulega zmianie, ponieważ nie istnieje `__dict__`. W takim przypadku `__getstate__` musi ręcznie zebrać wartości ze slotów, aby zapewnić poprawność procesu.
2. **Protokół kopiowania:** Metody te są również honorowane przez moduł `copy` (przy wykonywaniu `copy.deepcopy()`). Pozwala to na spójne zarządzanie stanem obiektu zarówno przy zapisie na dysk, jak i przy klonowaniu w pamięci.
3. **Wersjonowanie schematu:** `__setstate__` jest idealnym miejscem na obsługę **migracji danych**. Jeśli dodasz nowe pole do klasy w nowej wersji aplikacji, w `__setstate__` możesz sprawdzić, czy klucz istnieje w otrzymanym słowniku, a jeśli nie – ustawić wartość domyślną dla starych obiektów.

Czy chciałbyś, abym przygotował przykład implementujący wersjonowanie stanu obiektu przy użyciu tych metod?