# Context Manager w Pythonie

**Data:** 2025-05-03

---

**User:**

Opisz w Python askepkt:
Context managers – with, __enter__, __exit__, contextlib.

---

**Assistant:**

W Pythonie *context managers* (menedżery kontekstu) służą do zarządzania zasobami w sposób bezpieczny i czytelny — na przykład plikami, połączeniami sieciowymi, blokadami itp. Głównym zastosowaniem jest zapewnienie, że zasoby są poprawnie otwierane i zamykane, nawet jeśli wystąpi wyjątek.

## 1. Słowo kluczowe `with`

Najbardziej popularny sposób korzystania z context managerów to użycie słowa kluczowego `with`. Przykład:

```python
with open('plik.txt', 'r') as f:
    dane = f.read()
```

Tutaj `open()` zwraca obiekt, który działa jako menedżer kontekstu — `__enter__` otwiera plik, `__exit__` go zamyka automatycznie, nawet jeśli wewnątrz bloku wystąpi wyjątek.

---

## 2. Metody `__enter__` i `__exit__`

Aby stworzyć własny menedżer kontekstu, można zaimplementować metody `__enter__` i `__exit__` w klasie:

```python
class MyContextManager:
    def __enter__(self):
        print("Wchodzę do kontekstu")
        return self  # opcjonalnie jakiś zasób

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Wychodzę z kontekstu")
        if exc_type:
            print(f"Wystąpił wyjątek: {exc_val}")
        # można zwrócić True, żeby "stłumić" wyjątek
```

Użycie:

```python
with MyContextManager():
    print("W środku")
```

---

## 3. `contextlib` — uproszczenie tworzenia context managerów

Moduł `contextlib` pozwala pisać menedżery kontekstu jako funkcje, co jest prostsze i bardziej zwięzłe.

### Przykład z dekoratorem `@contextmanager`:

```python
from contextlib import contextmanager

@contextmanager
def my_context():
    print("Wchodzę do kontekstu")
    yield "zasób"
    print("Wychodzę z kontekstu")

with my_context() as val:
    print(f"W środku z wartością: {val}")
```

Zamiast `__enter__` i `__exit__`, funkcja dzieli się na część przed `yield` (setup) i po `yield` (cleanup).

---

## 4. Konkretny przykład: Mierzenie czasu wykonania

Aby lepiej zrozumieć różnicę między oboma podejściami, stworzymy ten sam menedżer kontekstu do mierzenia czasu wykonania bloku kodu na dwa sposoby: za pomocą klasy oraz generatora z dekoratorem.

### Podejście klasowe (obiektowe)

```python
import time

class TimerClass:
    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        end_time = time.time()
        print(f"Czas wykonania (klasa): {end_time - self.start_time:.4f} s")

# Użycie:
with TimerClass():
    time.sleep(0.1)
```

### Podejście z `contextlib` (funkcyjne)

```python
import time
from contextlib import contextmanager

@contextmanager
def timer_func():
    start_time = time.time()
    try:
        yield
    finally:
        end_time = time.time()
        print(f"Czas wykonania (funkcja): {end_time - start_time:.4f} s")

# Użycie:
with timer_func():
    time.sleep(0.1)
```

Oba podejścia dają ten sam rezultat. Wersja z funkcją (generatorem) jest często preferowana dla prostych menedżerów kontekstu ze względu na zwięzłość i brak konieczności tworzenia dedykowanej klasy. Należy jednak pamiętać o użyciu bloku `try...finally` w wersji z generatorem — jest to kluczowe, aby zagwarantować wykonanie kodu czyszczącego (po `yield`), nawet jeśli wewnątrz bloku `with` wystąpi wyjątek.

---

## 5. Po co zwracać wartość po `yield` (lub z `__enter__`)?

Często przy użyciu menedżerów kontekstu widzimy zapis `with ... as zmienna:`. Aby to zadziałało, menedżer musi przekazać jakiś obiekt do wnętrza bloku `with`. 
- W klasach odpowiada za to instrukcja `return` w metodzie `__enter__`.
- W funkcjach z `@contextmanager` odpowiada za to instrukcja `yield zwracany_obiekt`.

Robimy to po to, aby **kod wewnątrz bloku `with` mógł manipulować zarządzanym zasobem**. Najlepszym przykładem jest wbudowany `open()`, który zwraca uchwyt do pliku, dzięki czemu możemy z niego czytać lub do niego pisać. Jeśli nic nie zwrócimy (użyjemy gołego `yield`), blok `with` wykona się poprawnie, ale nie będziemy mieli referencji do zasobu w jego wnętrzu.

### Przykład: Zarządzanie plikiem tymczasowym

W tym przykładzie tworzymy plik, zwracamy do niego uchwyt (aby można było w nim pisać), a po wyjściu z bloku `with` zamykamy go i usuwamy z dysku.

```python
import os
from contextlib import contextmanager

@contextmanager
def temporary_file(filename):
    # Setup: Tworzymy i otwieramy plik do zapisu
    print(f"[Setup] Tworzę plik: {filename}")
    file_obj = open(filename, 'w')
    
    try:
        # Przekazujemy otwarty obiekt pliku na zewnątrz. 
        # Zostanie on przypisany do zmiennej po słowie kluczowym 'as'
        yield file_obj
    finally:
        # Cleanup: Zamykamy plik i usuwamy go z dysku
        print(f"[Cleanup] Zamykam i usuwam plik: {filename}")
        file_obj.close()
        if os.path.exists(filename):
            os.remove(filename)

# Użycie: Zmienna 'f' przechowuje obiekt przekazany przez 'yield'
with temporary_file('test_temp.txt') as f:
    f.write("Zapisuję tymczasowe dane...\n")
    print("Operacje na pliku zakończone.")
    
# Poza blokiem with pliku już nie ma (został usunięty w sekcji finally)
```

W powyższym przykładzie `yield file_obj` sprawia, że w instrukcji `with temporary_file(...) as f:` zmienna `f` staje się uchwytem do pliku. Gdybyśmy użyli samego `yield` bez żadnej wartości, pod `f` znalazłoby się `None` (domyślna wartość), a próba wywołania `f.write(...)` zakończyłaby się błędem `AttributeError`.

---

## Podsumowanie

| Element           | Opis                                                        |
|-------------------|-------------------------------------------------------------|
| `with`            | Słowo kluczowe do użycia menedżera kontekstu                |
| `__enter__`       | Wywoływane na wejściu do bloku `with`                       |
| `__exit__`        | Wywoływane przy wyjściu (nawet przy wyjątku)                |
| `contextlib`      | Moduł wspierający pisanie context managerów jako funkcji    |
| `@contextmanager` | Dekorator do tworzenia menedżera kontekstu z funkcji       |

Chcesz przykład context managera do zarządzania połączeniem do bazy, plikiem, czy może czymś innym?