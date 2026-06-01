# Działanie i różnice między `__new__`, `__init__`, `__call__` oraz `__del__`

W Pythonie tzw. *magiczne metody* (dunder methods, od *double underscore*) pozwalają na kontrolowanie podstawowych zachowań obiektów – od ich powstania, przez inicjalizację, użycie, aż po zniszczenie. Poniżej przedstawiono cztery kluczowe metody, które tworzą pewien cykl życia i użyteczności obiektu.

## 1. `__new__(cls, *args, **kwargs)` – Tworzenie (Alokacja)

Metoda `__new__` jest pierwszym krokiem w procesie tworzenia nowego obiektu. W przeciwieństwie do `__init__`, jest to metoda na poziomie klasy (choć nie wymaga dekoratora `@staticmethod`), która bierze klasę `cls` jako pierwszy argument i zwraca **nową instancję**.

- **Kiedy używamy?** Zazwyczaj jej nie nadpisujemy, chyba że dziedziczymy po typach niemutowalnych (jak `tuple` czy `str`) i chcemy zmodyfikować ich wartość przy tworzeniu, albo implementujemy wzorce projektowe, np. **Singleton**.
- **Co zwraca?** Musi zwrócić nową instancję klasy (często przez wywołanie `super().__new__(cls)`). Jeśli nie zwróci instancji danej klasy, `__init__` nie zostanie wywołane.

```python
class Singleton:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

s1 = Singleton()
s2 = Singleton()
print(s1 is s2)  # True, obie referencje wskazują na ten sam obiekt w pamięci
```

## 2. `__init__(self, *args, **kwargs)` – Inicjalizacja (Ustawienie Stanu)

Metoda `__init__` wywoływana jest automatycznie **po** `__new__`. Otrzymuje już utworzoną instancję jako `self` i służy wyłącznie do ustawienia jej początkowego stanu (przypisania atrybutów).

- **Kiedy używamy?** Praktycznie zawsze, gdy tworzymy nową klasę z jakimiś polami (stanem).
- **Co zwraca?** Nic (`None`). Próba zwrócenia czegokolwiek innego rzuci błędem `TypeError`.

```python
class Person:
    def __init__(self, name):
        # self już istnieje dzięki __new__
        self.name = name
```

### Różnica między `__new__` a `__init__`
- `__new__` **tworzy** obiekt i przydziela mu pamięć. Zwraca instancję.
- `__init__` **konfiguruje** już utworzony obiekt. Nie zwraca niczego (konkretnie `None`).

## 3. `__call__(self, *args, **kwargs)` – Wywołanie (Obiekt jako Funkcja)

Metoda `__call__` pozwala na użycie instancji klasy tak, jakby była funkcją (obiekt staje się *callable*). 

- **Kiedy używamy?** Gdy obiekt ma pełnić rolę funkcji przechowującej pewien stan (np. w dekoratorach pisanych jako klasy, fabrykach, czy modelach uczenia maszynowego).
- **Zaleta:** W przeciwieństwie do zwykłej funkcji z domknięciem (closure), obiekt klasy zachowuje swój stan w wyraźnych atrybutach, które łatwiej modyfikować, analizować czy testować.

```python
class Multiplier:
    def __init__(self, factor):
        self.factor = factor
        
    def __call__(self, value):
        return value * self.factor

times_two = Multiplier(2)
print(times_two(5))  # Wypisze: 10 (Obiekt użyty jak funkcja!)
```

## 4. `__del__(self)` – Destrukcja (Sprzątanie)

Do dopełnienia tego zestawu idealnie pasuje `__del__`, zamykając cykl życia instancji. Jest wywoływana, gdy licznik referencji obiektu spada do zera i proces *Garbage Collectora* (GC) przygotowuje go do usunięcia z pamięci.

- **Kiedy używamy?** Głównie do sprzątania niezarządzanych zasobów: zamykania otwartych plików, kończenia połączeń sieciowych czy z bazą danych (choć we współczesnym Pythonie zaleca się raczej Context Managery - protokół `__enter__` i `__exit__`).
- **Uwaga:** Nie możemy do końca przewidzieć *kiedy dokładnie* uruchomi się GC i wywoła `__del__`.

```python
class DatabaseConnection:
    def __init__(self):
        print("Otwieranie połączenia...")
        self.connected = True
        
    def __del__(self):
        print("Zamykanie połączenia i zwalnianie zasobów...")
        self.connected = False
```

## Podsumowanie cyklu życia

1. `obj = MyClass()` —> Wywołuje się `__new__`, by stworzyć obiekt.
2. Następnie (pod maską) wywołuje się `__init__`, by ustawić początkowy stan `obj`.
3. Jeśli klasa definiuje `__call__`, możemy wywołać `obj(...)`, używając jej instancji wielokrotnie, przekazując nowe argumenty i zwracając nowe wyniki, zachowując przy tym stan zdefiniowany w `__init__`.
4. Gdy tracimy ostatnią referencję do `obj`, wywołuje się `__del__`, by posprzątać przed ostatecznym zwolnieniem pamięci.

---
**Zobacz też:**
- [Garbage Collector w Pythonie](garbage-collector-w-pythonie.md)
- [Context Manager w Pythonie](context-manager-w-pythonie.md)
- [Rola metody init w Pythonie](rola-metody-init-w-pythonie.md)
