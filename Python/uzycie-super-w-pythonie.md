# Użycie super() w Pythonie

Funkcja `super()` w Pythonie zwraca obiekt proxy (tymczasowy obiekt klasy nadrzędnej), który pozwala na wywoływanie metod klasy bazowej (lub klas bazowych w przypadku wielokrotnego dziedziczenia). Najczęściej używana jest do wywoływania konstruktora klasy nadrzędnej (`__init__`) lub rozszerzania zachowania dziedziczonych metod.

## Dlaczego jest to ważne?

- **Unikanie wpisywania nazwy klasy bazowej (Hardcoding):** Zamiast jawnie wymieniać nazwę klasy rodzica, co utrudnia późniejsze refaktoryzacje (np. zmianę klasy bazowej), używamy `super()`.
- **Wielokrotne dziedziczenie i MRO (Method Resolution Order):** W przypadku dziedziczenia wielokrotnego, `super()` gwarantuje, że każda metoda z klas nadrzędnych zostanie wywołana dokładnie raz i w odpowiedniej kolejności, zgodnie z algorytmem MRO.

## Jak to działa?

W Pythonie 3 użycie `super()` zostało znacznie uproszczone i nie wymaga przekazywania argumentów wewnątrz definicji klasy (wywołanie bezparametrowe).

```python
class Parent:
    def __init__(self, name):
        self.name = name
        print(f"Inicjalizacja Parent: {self.name}")

    def greet(self):
        print(f"Witaj, jestem {self.name}")

class Child(Parent):
    def __init__(self, name, age):
        # Wywołanie konstruktora klasy bazowej
        super().__init__(name)
        self.age = age
        print(f"Inicjalizacja Child: {self.age}")

    def greet(self):
        # Rozszerzenie metody klasy bazowej
        super().greet()
        print(f"Mam {self.age} lat.")

c = Child("Jan", 10)
c.greet()
```

## Czy super() musi być w pierwszej linii jak w Javie?

**Nie.** W przeciwieństwie do Javy, gdzie wywołanie `super()` w konstruktorze **musi** być absolutnie pierwszą instrukcją, w Pythonie `super()` jest po prostu zwykłym wywołaniem funkcji zwracającym obiekt.

Możesz wywołać `super().__init__(...)` w dowolnym miejscu konstruktora (lub innej metody): na początku, w środku, a nawet na samym końcu, w zależności od tego, kiedy potrzebujesz zainicjalizować stan z klasy bazowej.

```python
class AnotherChild(Parent):
    def __init__(self, name, extra_info):
        # Najpierw inicjalizujemy własny stan
        self.extra_info = extra_info
        print(f"Najpierw robię swoje rzeczy: {self.extra_info}")
        
        # Dopiero później wywołujemy konstruktor bazowy
        super().__init__(name)
```

Warto jednak pamiętać o dobrej praktyce: jeśli do zainicjalizowania własnego stanu (w klasie pochodnej) potrzebujesz atrybutów zdefiniowanych w klasie bazowej, `super().__init__()` powinieneś wywołać wcześniej. Jeśli nie ma takich zależności, kolejność zależy wyłącznie od logiki Twojego programu.

## Powiązane tematy
- [Dziedziczenie w Pythonie](dziedziczenie-w-pythonie.md)
