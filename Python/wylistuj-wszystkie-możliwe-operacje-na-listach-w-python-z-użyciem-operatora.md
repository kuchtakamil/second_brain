# Wylistuj wszystkie możliwe operacje na listach w Python z użyciem operatora :

**Data:** 4 lut 2026, 00:24:19 CET

---

**User:**

Wylistuj wszystkie możliwe operacje na listach w Python z użyciem operatora :

---

**Gemini:**

W języku Python operator `:` (dwukropek) służy do wykonywania operacji **slicingu** (wycinania), co pozwala na dostęp do fragmentów list, kopiowanie ich oraz modyfikację. Składnia bazowa to `list[start:stop:step]`.

### Podstawowe wycinanie (Slicing)

- **`list[start:stop]`**: Zwraca nową listę zawierającą elementy od indeksu `start` do `stop - 1`.
- **`list[start:]`**: Zwraca elementy od indeksu `start` aż do końca listy.
- **`list[:stop]`**: Zwraca elementy od początku listy do indeksu `stop - 1`.
- **`list[:]`**: Tworzy **płytką kopię** (shallow copy) całej listy. Jest to często wykorzystywane, aby uniknąć mutowania oryginału podczas operacji.

### Slicing z krokiem (Stride)

- **`list[start:stop:step]`**: Wybiera elementy od `start` do `stop - 1` z zachowaniem odstępu o wartości `step`.
- **`list[::step]`**: Przechodzi przez całą listę z określonym krokiem (np. `list[::2]` zwraca co drugi element).
- **`list[::-1]`**: Odwraca listę (reverse). Krok ujemny powoduje iterację od końca do początku.

---

### Zaawansowane operacje modyfikacji (In-place)

Operator `:` może być używany po lewej stronie operatora przypisania `=`, co pozwala na bezpośrednią manipulację strukturą listy bez zmiany jej referencji w pamięci.

| Operacja | Kod | Opis techniczny |
| --- | --- | --- |
| **Zastępowanie fragmentu** | `L[1:3] = [10, 20]` | Zamienia elementy na wskazanych indeksach. Długość nowej sekwencji nie musi być równa długości wycinka. |
| **Wstawianie elementów** | `L[1:1] = [5, 6]` | Wstawia nową sekwencję w określone miejsce bez usuwania istniejących elementów (indeks `stop` równy `start`). |
| **Usuwanie fragmentu** | `L[1:3] = []` | Usuwa elementy z zakresu poprzez przypisanie pustej listy (alternatywa dla `del L[1:3]`). |
| **Czyszczenie listy** | `L[:] = []` | Usuwa wszystkie elementy, zachowując ten sam obiekt listy w pamięci. |
| **Nadpisywanie całości** | `L[:] = [1, 2, 3]` | Podmienia całą zawartość listy, co jest przydatne, gdy inne zmienne współdzielą referencję do `L`. |

---

### Techniczne aspekty implementacji

Slicing w Pythonie wywołuje pod spodem metodę magiczną `__getitem__` (dla odczytu) lub `__setitem__` (dla zapisu), przekazując do nich obiekt klasy `slice`.

```
# Przykład użycia obiektu slice zamiast składni z dwukropkiem
s = slice(1, 5, 2)
my_list[s]  # Równoważne my_list[1:5:2]
```

Warto zauważyć, że slicing przy odczycie zawsze tworzy **nowy obiekt**. Jeśli lista zawiera obiekty mutowalne, kopiowane są tylko ich referencje. W przypadku **Extended Slicing** (kiedy `step != 1`) przy przypisywaniu wartości (`L[::2] = [...]`), długość wstawianej sekwencji musi dokładnie odpowiadać liczbie wybranych slotów, w przeciwnym razie interpreter zgłosi `ValueError`.

Chciałbyś, abym przygotował przykłady implementacji zaawansowanych algorytmów (np. in-place quicksort) z wykorzystaniem operacji na wycinkach?