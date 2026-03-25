# Serializacja w Pythonie

**Data:** 2026-02-09

---

**User:**

Czy w Python jest koncept Serializable jak w Java?

---

**Assistant:**

Krótko: **nie**.  
W Pythonie **nie istnieje odpowiednik interfejsu `Serializable` z Javy**.

Ale…

Python ma **wbudowany mechanizm serializacji obiektów**, który działa zupełnie inaczej niż w Javie i w praktyce jest **bardziej elastyczny**.

---

## Java – przypomnienie modelu

W Javie:

```java
class User implements Serializable {
    private String name;
}
```

- klasa *musi* zadeklarować `implements Serializable`
- JVM używa refleksji + metadanych klasy
- serializacja jest częścią specyfikacji języka
- brak `implements` → wyjątek w runtime

To jest **opt-in przez interfejs**.

---

## Python – model jest odwrotny

W Pythonie:

> **Każdy obiekt jest serializowalny, dopóki jego zawartość jest serializowalna.**

Nie ma żadnego interfejsu.  
Nie ma żadnej deklaracji.  
Nie ma żadnego „implements”.

Jest moduł standardowy:

```python
import pickle
```

---

## Podstawowa serializacja

```python
import pickle

class User:
    def __init__(self, name):
        self.name = name

u = User("Jan")

data = pickle.dumps(u)      # serializacja do bajtów
u2 = pickle.loads(data)     # deserializacja
```

Działa. Bez żadnych adnotacji. Bez interfejsu.

---

## Kiedy obiekt NIE jest serializowalny?

Gdy zawiera rzeczy, których nie da się odtworzyć:

- otwarte pliki
- połączenia sieciowe
- lambdy
- wątki
- referencje do C-extension bez wsparcia pickla

Wtedy dostaniesz:

```
TypeError: cannot pickle ...
```

---

## Odpowiednik `readObject` / `writeObject` z Javy

Jeśli chcesz kontrolować serializację (jak w Javie):

```python
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
```

To jest **pełny odpowiednik** customowej serializacji w Javie.

---

## Dlaczego Python nie ma `Serializable`?

Bo Python:

> nie serializuje klasy na podstawie deklaracji, tylko na podstawie **stanu obiektu (`__dict__`)**

To jest fundamentalna różnica filozofii:

| Java | Python |
|-----|-------|
| serializacja klasy | serializacja instancji |
| interfejs | brak interfejsu |
| opt-in | domyślnie działa |
| statyczny model | dynamiczny model |

---

## Bardzo ważne (praktyczne)

`pickle` to nie jest odpowiednik JSON.

To jest **pełna serializacja grafu obiektów Pythona**:

- zachowuje referencje
- zachowuje typy
- działa dla złożonych struktur
- używane wewnętrznie przez multiprocessing, caching, ML, itd.

---

## Jeśli chcesz „javowe” zachowanie (kontrolowane DTO)

W Pythonie w takich sytuacjach **nie używa się pickle**, tylko:

- `dataclasses` + `json`
- `pydantic`
- własne `to_dict()` / `from_dict()`

Bo `pickle` jest do:
> zapisz stan obiektu Pythona i odtwórz go w Pythonie

a nie do:
> wymiany danych między systemami

---

## TL;DR dla programisty Javy

`pickle` = Java `Serializable` + `ObjectOutputStream` + refleksja  
ale:

> **bez `implements Serializable`**

I z możliwością nadpisania procesu przez `__getstate__` / `__setstate__`.

---

## Jedno zdanie, które ustawia mindset

W Javie pytasz:  
> „czy ta klasa jest serializowalna?”

W Pythonie pytasz:  
> „czy stan tego obiektu da się zapisać?”