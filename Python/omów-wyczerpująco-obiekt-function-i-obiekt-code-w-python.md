# Obiekt `function` i obiekt `code` w Pythonie

## Krótkie podsumowanie
W Pythonie **funkcje są obiektami pierwszej klasy** (first-class objects), co oznacza, że można je przypisywać do zmiennych, przekazywać jako argumenty i zwracać z innych funkcji. Kiedy definiujesz funkcję wykorzystując słowo kluczowe `def` lub stworzysz `lambda`, Python tak naprawdę ewaluuje to powołując do życia **obiekt funkcji** (`function object`).

Sam obiekt funkcji przechowuje "kontekst" i metadane wywołania (np. domyślne argumenty, domknięcia/closures, przestrzeń nazw modułu), ale **nie zawiera** samego kodu wykonywalnego. Skompilowany kod (instrukcje bajtowe, bytecode) jest trzymany w osobnym bycie: **obiekcie kodu** (`code object`), który jest przypisany do obiektu funkcji pod atrybutem `__code__`.

## Dlaczego to jest ważne / kiedy się przydaje?
Zrozumienie podziału na `function object` i `code object` to krok niezbędny do zostania świadomym programistą Pythona.
* **Metaprogramowanie i dekoratory:** Mając dostęp do atrybutów funkcji, można dynamicznie wyciągać nazwy argumentów, podmieniać je, budować zaawansowane dekoratory lub cache'ować wyniki.
* **Inspekcja kodu (introspection):** Moduły takie jak `inspect` mocno opierają się na analizie obiektów funkcji i kodu, by tworzyć debuggery, profilery czy systemy wstrzykiwania zależności (Dependency Injection – np. w frameworku FastAPI czy Pytest).
* **Zarządzanie pamięcią i optymalizacja:** Ponieważ kod wykonywalny (`code object`) jest ściśle niezmienny (immutable) i wolny od otoczenia, interpreter może bezpiecznie współdzielić ten sam `code object` między wieloma różnymi obiektami funkcji — na przykład w pętlach tworzących domknięcia (closures).

## Jak to działa w praktyce?

### 1. Obiekt Funkcji (`Function Object`)
Obiekt funkcji reprezentuje powiązaną całość w środowisku runtime i posiada cały szereg atrybutów "dunder" (od *double underscore*). Najważniejsze z nich to m.in.:
* `__name__`: Nazwa funkcji.
* `__doc__`: Docstring (dokumentacja) funkcji.
* `__defaults__`: Krotka z domyślnymi wartościami argumentów pozycyjnych.
* `__kwdefaults__`: Słownik domyślnych wartości argumentów przekazywanych po słowie kluczowym (keyword-only).
* `__closure__`: Zmienne z zewnętrznego zasięgu, z których funkcja korzysta (jeśli to closure).
* `__globals__`: Słownik wskazujący na globalną przestrzeń nazw (modułu), w którym funkcja została zdefiniowana.
* `__code__`: Referencja do skompilowanego **obiektu kodu**.

**Przykład inspekcji obiektu funkcji:**
```python
def my_function(a, b=10, *, c=20):
    """A standard sample function."""
    x = a + b + c
    return x

print(my_function.__name__)        # my_function
print(my_function.__doc__)         # A standard sample function.
print(my_function.__defaults__)    # (10,)
print(my_function.__kwdefaults__)  # {'c': 20}
```

### 2. Obiekt Kodu (`Code Object`)
Podczas wczytywania i parsowania pliku w Pythonie, kompilator tworzy `types.CodeType` dla ciał funkcji. Takowy kod jest surowy, **niezmienny (immutable)** i nie zwraca uwagi na globalne środowisko czy domyślne atrybuty. Znajdziesz w nim wszystko co potrzebne CPythonowi do odpalenia logiki, m.in.:

Najważniejsze atrybuty obiektu `code`:
* `co_code`: Skompilowane instrukcje kodu bajtowego (bytecode) w formie surowej.
* `co_consts`: Krotka stałych (np. integerów, stringów deklarowanych w ciele, m.in. sam docstring).
* `co_varnames`: Krotka zawierająca nazwy zmiennych używanych i argumentów lokalnych.
* `co_argcount`: Liczba docelowych argumentów pozycyjnych.
* `co_nlocals`: Obliczona w kompilacji całkowita liczba zmiennych lokalnych.
* `co_filename`, `co_firstlineno`: Informacja skąd pochodzi kod, niezbędna dla generowania tzw. tracebacków przy błędach.

**Zajrzenie do obiektu kodu dla powyższej funkcji:**
```python
code_obj = my_function.__code__

print(code_obj.co_argcount)    # 2  (because 'a' and 'b' are positional arguments)
print(code_obj.co_varnames)    # ('a', 'b', 'c', 'x')
print(code_obj.co_consts)      # (None, 'A standard sample function.')
print(code_obj.co_filename)    # <stdin> or appropriate path to .py script
```

### 3. Różnica: Funkcja a Kod
Najlepsza metafora pomagająca zrozumieć ich podział:
- **Obiekt kodu** to sam *suchy przepis kulinarny* (np. „dodaj łyżkę soli i zagotuj”). Jest statyczny, sam w sobie nic nie zdziała i nie wie nic o kuchni dookoła. 
- **Obiekt funkcji** to związanie tego konkretnego *przepisu* z wyposażoną, pełną składników *kuchnią* w restauracji (dostęp do `__globals__`, domyślne parametry z lodówki zachowane w `__defaults__` itp.).

Modułowa architektura języka pozwala na to, abyśmy przy użyciu modułu `types` utworzyli nową funkcję programistycznie (runtime), recyklingując sam bytecode i podsuwając własne środowisko.

**Bawimy się Pythonem - własnoręczne przypięcie kodu nowej kuchni:**
```python
import types

def contextless_function():
    return verify_explosion()

# Namespace with different logic
globals_1 = {"verify_explosion": lambda: "BOOM!"}
globals_2 = {"verify_explosion": lambda: "Silence..."}

# Manually instantiating new function objects sharing THE SAME code object
new_f1 = types.FunctionType(contextless_function.__code__, globals_1, name="new_f1")
new_f2 = types.FunctionType(contextless_function.__code__, globals_2, name="new_f2")

print(new_f1()) # -> BOOM!
print(new_f2()) # -> Silence...
```

## Moduł wspierający: `dis`
Aby faktycznie zajrzeć "pod maskę" do samego bajtkodu i zobaczyć reprezentację z wnętrza `co_code`, deweloperzy na ogół używają standardowej biblioteki `dis` (*disassembler*):
```python
import dis
dis.dis(my_function)
```
Pozwala to prześledzić stos dokładnie rozbity na m.in. operatory `LOAD_FAST`, `BINARY_ADD` oraz `RETURN_VALUE`.

Zobacz też:
- [[funkcje-jako-obiekty.md]]
- [[zaawansowane-zagadnienia-w-pythonie.md]]
- [[dekoratory-w-pythonie.md]]
