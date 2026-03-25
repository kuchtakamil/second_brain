# napisz czym jest __slots__

**Data:** 9 lut 2026, 16:42:17 CET

---

**User:**

napisz czym jest __slots__

---

**Gemini:**

Mechanizm `__slots__` w Pythonie służy do jawnego definiowania listy atrybutów, jakie mogą posiadać instancje danej klasy. Jego głównym celem jest optymalizacja zużycia pamięci oraz przyspieszenie dostępu do atrybutów poprzez wyeliminowanie domyślnego słownika instancji `__dict__`.

---

### Mechanizm działania

Domyślnie każda instancja klasy w Pythonie posiada dynamiczny słownik `__dict__`. Pozwala on na dodawanie dowolnych atrybutów w czasie wykonywania programu, ale wiąże się z dużym narzutem pamięciowym (hash table overhead).

Definiując `__slots__`, informujesz interpretera: "Ta klasa będzie posiadać tylko te konkretne atrybuty". Python rezerwuje wtedy stałą ilość miejsca dla każdego obiektu w strukturze przypominającej tablicę, zamiast tworzyć słownik dla każdej instancji.

```
class Point:
    __slots__ = ('x', 'y')  # Rezerwacja miejsca tylko dla x oraz y

    def __init__(self, x, y):
        self.x = x
        self.y = y
```

### Kluczowe korzyści techniczne

#### 1. Drastyczna oszczędność pamięci

W przypadku aplikacji operujących na milionach małych obiektów (np. punkty w przestrzeni, rekordy bazy danych w pamięci), użycie `__slots__` może zredukować zużycie RAM o **40-70%**. Wynika to z faktu, że instancja nie musi przechowywać wskaźnika do słownika ani samego słownika z jego wewnętrzną strukturą tablicy mieszającej.

#### 2. Szybszy dostęp do atrybutów

Dostęp do atrybutów zdefiniowanych w `__slots__` jest mierzalnie szybszy niż w przypadku `__dict__`. Python używa niskopoziomowych deskryptorów do bezpośredniego mapowania nazwy atrybutu na konkretne przesunięcie (offset) w strukturze obiektu.

#### 3. Restrykcyjność (Side Effect)

Próba przypisania atrybutu spoza listy zdefiniowanej w `__slots__` zakończy się błędem `AttributeError`. Zapobiega to literówkom i przypadkowemu tworzeniu nowych atrybutów.

```
p = Point(1, 2)
p.z = 10  # AttributeError: 'Point' object has no attribute 'z'
```

---

### Zaawansowane aspekty i ograniczenia

- **Dziedziczenie:** `__slots__` nie są automatycznie dziedziczone w sposób, który blokuje `__dict__` w podklasach. Jeśli klasa bazowa ma `__slots__`, a klasa pochodna nie ma zdefiniowanego `__slots__`, instancje klasy pochodnej i tak będą miały słownik `__dict__`. Aby utrzymać oszczędność pamięci, każda klasa w hierarchii musi definiować `__slots__`.
- **Brak `__weakref__`:** Domyślnie obiekty ze `__slots__` nie wspierają słabych referencji (`weakref`). Jeśli ich potrzebujesz, musisz dodać `'__weakref__'` do krotki `__slots__`.
- **Wielodziedziczenie:** Łączenie wielu klas bazowych z niepustymi `__slots__` jest problematyczne i często prowadzi do `TypeError`, chyba że wszystkie klasy (poza jedną) mają puste `__slots__`.
- **Deskryptory:** `__slots__` są implementowane na poziomie klasy jako deskryptory danych. Oznacza to, że na poziomie klasy nazwy te istnieją, ale przechowują logikę dostępu do pól instancji.

### Porównanie struktur danych

| Cecha | Standardowa klasa (`__dict__`) | Klasa z `__slots__` |
| --- | --- | --- |
| **Alokacja pamięci** | Dynamiczna (Słownik) | Statyczna (Struktura stałego rozmiaru) |
| **Możliwość dodawania pól** | Tak (dowolne) | Nie (tylko zdefiniowane) |
| **Szybkość dostępu** | Standardowa | Wyższa (bezpośredni offset) |
| **Zastosowanie** | Ogólne, elastyczne modele | Optymalizacja wysokowydajna |

Czy chciałbyś zobaczyć test porównawczy (benchmark) zużycia pamięci i czasu dostępu dla klasy ze `__slots__` i bez nich?