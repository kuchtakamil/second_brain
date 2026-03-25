# Wywołanie funkcji ze stringa

**Data:** 2025-11-06

---

**User:**

w python mam jakiś string i chcę wywołać funkcję która nazywa się tak jak ten string.

---

**Assistant:**

W Pythonie możesz wywołać funkcję o nazwie przechowywanej w stringu na kilka sposobów — zależnie od tego, gdzie ta funkcja jest zdefiniowana.  

### 🔹 Przykład 1: Funkcja w tym samym module
Jeśli funkcja jest zdefiniowana w tym samym pliku:
```python
def foo():
    print("Hello from foo!")

func_name = "foo"

globals()[func_name]()  # -> Hello from foo!
```

🔸 Wyjaśnienie:
- `globals()` zwraca słownik globalnych symboli (m.in. nazwy funkcji).
- `globals()["foo"]` zwróci obiekt funkcji `foo`.

---

### 🔹 Przykład 2: Funkcja w obiekcie lub module
Jeśli funkcja jest metodą obiektu:
```python
class MyClass:
    def bar(self):
        print("Hello from bar!")

obj = MyClass()
func_name = "bar"

getattr(obj, func_name)()  # -> Hello from bar!
```

lub jeśli to funkcja w module:
```python
import math

func_name = "sqrt"
result = getattr(math, func_name)(9)
print(result)  # -> 3.0
```

---

### 🔹 Uwaga bezpieczeństwa
Unikaj `eval(func_name + '()')` — jest to **niebezpieczne**, jeśli string pochodzi z zewnętrznego źródła.

---

Chcesz, żebym pokazał przykład, jak to zrobić dynamicznie dla funkcji zarejestrowanych np. w jakimś twoim module lub klasie (np. pluginy, komendy)?

---

**User:**

a nie można zrobić czegoś takiego?

def foo():
    print("Hello from foo!")

func_name = "foo"
if is_function(func_name):
   func_name()

---

**Assistant:**

Nie, w takiej formie to nie zadziała — `func_name` jest **stringiem**, a nie referencją do funkcji, więc `func_name()` spowoduje błąd typu:  
```
TypeError: 'str' object is not callable
```

Aby zrobić coś w tym stylu poprawnie, możesz napisać to tak:

```python
def foo():
    print("Hello from foo!")

func_name = "foo"

# sprawdzamy, czy w przestrzeni nazw istnieje taka funkcja
if func_name in globals() and callable(globals()[func_name]):
    globals()[func_name]()  # wywołanie funkcji
```

---

Jeśli chcesz, możesz sobie zdefiniować pomocniczą funkcję `is_function`, żeby Twój przykład wyglądał tak, jak chciałeś:

```python
def is_function(name):
    return name in globals() and callable(globals()[name])

def foo():
    print("Hello from foo!")

func_name = "foo"

if is_function(func_name):
    globals()[func_name]()
```

---

Alternatywnie (dla metod w klasach lub obiektach):

```python
if hasattr(obj, func_name) and callable(getattr(obj, func_name)):
    getattr(obj, func_name)()
```

Chcesz, żebym pokazał wersję działającą także z metodami klas i funkcjami z importowanych modułów w jednym?

---

**User:**

ok, a czy mogę przekazać argumenty "zbiorowo", to znaczy bez względu na to jaka wołana jest funkcja, chcę przekazać zmienną arguments
        if tool_call in globals() and callable(globals()[tool_call]):
            arguments = json.loads(tool_call.function.arguments)

---

**Assistant:**

Tak — możesz to zrobić, ale musisz wiedzieć, **w jakiej formie** masz dane w `arguments`.  
Skoro ładujesz je z JSON-a (`json.loads(...)`), to zapewne będzie to słownik (`dict`).  

Wtedy możesz przekazać argumenty **rozpakowując je** przy wywołaniu funkcji za pomocą `**` (dla argumentów nazwanych) lub `*` (dla listy pozycyjnych).

---

### 🔹 Przykład z argumentami nazwanymi (`**kwargs`)
```python
import json

def greet(name, age):
    print(f"Hello {name}, age {age}")

tool_call = "greet"
arguments = json.loads('{"name": "Alice", "age": 30}')

if tool_call in globals() and callable(globals()[tool_call]):
    globals()[tool_call](**arguments)
```
➡️ wynik:
```
Hello Alice, age 30
```

---

### 🔹 Przykład z argumentami pozycyjnymi (`*args`)
Jeśli `arguments` jest listą:
```python
import json

def add(a, b):
    print(a + b)

tool_call = "add"
arguments = json.loads('[3, 5]')

if tool_call in globals() and callable(globals()[tool_call]):
    globals()[tool_call](*arguments)
```
➡️ wynik:
```
8
```

---

### 🔹 Przykład uniwersalny
Możesz też zrobić prostą funkcję, która „spróbuje” wywołać funkcję niezależnie od tego, czy argumenty są listą czy słownikiem:

```python
def call_tool(tool_call, arguments):
    func = globals().get(tool_call)
    if not callable(func):
        raise ValueError(f"Function '{tool_call}' not found")

    if isinstance(arguments, dict):
        return func(**arguments)
    elif isinstance(arguments, list):
        return func(*arguments)
    else:
        return func(arguments)
```

Chcesz, żebym pokazał wersję, która działa również, jeśli funkcja znajduje się w module lub klasie (a nie tylko w globalnym zakresie)?

---

**User:**

  File "/tmp/ipykernel_43011/4162550598.py", line 4, in handle_tool_calls
    if tool_call in globals() and callable(globals()[tool_call]):
       ^^^^^^^^^^^^^^^^^^^^^^
TypeError: unhashable type: 'ChatCompletionMessageFunctionToolCall'

---

**Assistant:**

Dokładnie — ten błąd oznacza, że `tool_call` **nie jest stringiem**, tylko obiektem (konkretnie typu `ChatCompletionMessageFunctionToolCall`).  
Nie możesz więc używać go jako klucza w `globals()`, bo Python próbuje zrobić `globals()[tool_call]`, a obiekty tego typu nie są „hashowalne”.

---

### 🔹 Co się dzieje
Jeśli używasz API OpenAI / lokalnego modelu z funkcjami (tool calls), to `tool_call` jest **obiektem**, który ma np. pola:
```python
tool_call.function.name
tool_call.function.arguments
```

Więc zamiast:
```python
if tool_call in globals() and callable(globals()[tool_call]):
```

powinno być:
```python
tool_name = tool_call.function.name
arguments = json.loads(tool_call.function.arguments)

if tool_name in globals() and callable(globals()[tool_name]):
    globals()[tool_name](**arguments)
```

---

### 🔹 Pełny przykład

```python
import json

def greet(name):
    print(f"Hello {name}!")

# symulacja obiektu tool_call z OpenAI
class FakeToolCall:
    class Func:
        name = "greet"
        arguments = '{"name": "Alice"}'
    function = Func()

tool_call = FakeToolCall()

tool_name = tool_call.function.name
arguments = json.loads(tool_call.function.arguments)

if tool_name in globals() and callable(globals()[tool_name]):
    globals()[tool_name](**arguments)
```

➡️ Wynik:
```
Hello Alice!
```

---

Czy chcesz, żebym pokazał wersję, która automatycznie obsłuży wiele `tool_calls` (np. w pętli, jak to zwykle bywa w odpowiedzi modelu OpenAI)?

---

**User:**

Chcę zrobić funkcję z jednym parametrem ale nazwanym
def get_ticket_price(destination_city=destination_city):
ale to nie działa

---

**Assistant:**

Tak — to nie zadziała, i Python ma ku temu bardzo konkretne powody.  
W deklaracji funkcji nie możesz użyć wartości domyślnej (`destination_city=destination_city`), która **odwołuje się do parametru lub zmiennej**, która nie istnieje jeszcze w tym momencie.  

---

### 🔹 Dlaczego to nie działa
Podczas definiowania funkcji interpreter **natychmiast** próbuje obliczyć wartość domyślną.  
Czyli w tym miejscu:
```python
def get_ticket_price(destination_city=destination_city):
```
Python pyta: „a co to jest `destination_city`?”  
— ale ta zmienna **nie istnieje jeszcze** (ani jako parametr, ani w scope), więc dostajesz `NameError`.

---

### 🔹 Poprawne rozwiązania

#### 1️⃣ Po prostu zwykły parametr (bez wartości domyślnej)
Jeśli chcesz, by był wymagany:
```python
def get_ticket_price(destination_city):
    print(f"Price for {destination_city}")
```

---

#### 2️⃣ Użycie wartości domyślnej zdefiniowanej wcześniej zmiennej
Jeśli masz zmienną w zakresie globalnym lub zewnętrznym:
```python
default_city = "Warsaw"

def get_ticket_price(destination_city=default_city):
    print(f"Price for {destination_city}")
```

To działa, bo `default_city` istnieje w momencie definiowania funkcji.

---

#### 3️⃣ Ustawienie domyślnej wartości w ciele funkcji
Jeśli wartość ma być dynamiczna (np. zależna od jakiegoś stanu w momencie wywołania, nie definicji):
```python
def get_ticket_price(destination_city=None):
    if destination_city is None:
        destination_city = "Warsaw"  # ustalanie domyślnej wartości w runtime
    print(f"Price for {destination_city}")
```

---

Chcesz, żebym pokazał przykład, jak to zrobić gdy domyślna wartość ma pochodzić np. z konfiguracji lub zmiennej środowiskowej (czyli dynamicznie)?

---

**User:**

ok, pokaż jak się tworzy named params w python

---

**Assistant:**

W Pythonie *named parameters* (czyli parametry nazwane) to po prostu argumenty przekazywane do funkcji z użyciem ich nazw — Python obsługuje to natywnie.  

Możesz je tworzyć i wykorzystywać na kilka sposobów:

---

### 🔹 1. Zwykłe parametry nazwane

```python
def greet(name, age):
    print(f"Hello {name}, you are {age} years old")

# wywołanie z nazwanymi parametrami
greet(name="Alice", age=30)
```

➡️ W efekcie:
```
Hello Alice, you are 30 years old
```

To, co wyróżnia „named parameters” w Pythonie, to fakt, że możesz je przekazywać w dowolnej kolejności:
```python
greet(age=30, name="Alice")  # też działa
```

---

### 🔹 2. Parametry z wartościami domyślnymi

```python
def connect(host="localhost", port=3306):
    print(f"Connecting to {host}:{port}")

connect()                   # używa wartości domyślnych
connect(port=5432)          # tylko jeden parametr nadpisany
```

---

### 🔹 3. Wymuszenie nazwanych parametrów (`*`)

Jeśli chcesz **wymusić**, żeby użytkownik funkcji *musiał* podać parametry po nazwie, dodajesz `*`:
```python
def create_user(*, username, email):
    print(f"Creating user {username} with email {email}")
```

Teraz:
```python
create_user("alice", "a@b.com")   # ❌ błąd: TypeError
create_user(username="alice", email="a@b.com")  # ✅ działa
```

---

### 🔹 4. Dowolna liczba nazwanych parametrów (`**kwargs`)

Czasem chcesz, żeby funkcja przyjmowała *dowolne* nazwane argumenty:
```python
def debug_print(**kwargs):
    for key, value in kwargs.items():
        print(f"{key} = {value}")

debug_print(a=1, b=2, c="hello")
```

➡️ Wynik:
```
a = 1
b = 2
c = hello
```

---

### 🔹 5. Łączenie wszystkiego
```python
def example(a, b=2, *, c, d=4, **extra):
    print(a, b, c, d, extra)

example(1, c=3, e=5, f=6)
# a=1, b=2, c=3, d=4, extra={'e':5, 'f':6}
```

---

Chcesz, żebym pokazał, jak wywoływać takie funkcje dynamicznie (np. mając nazwę funkcji i dict argumentów — czyli połączenie z Twoim wcześniejszym przypadkiem)?

---

**User:**

jaka jest wymuszona kolejność rodzajów parametrów? na początku te zwykłe, nie nazwane, a później?

---

**Assistant:**

Świetne pytanie — Python ma **ściśle określoną kolejność** rodzajów parametrów w definicji funkcji.  
Kolejność **musi** być zachowana w tej kolejności (od lewej do prawej):

---

### 🔹 Kolejność parametrów w funkcji Python

```
def func(
    positional_only,          # 1. tylko pozycyjne (przed /)
    /,                        # separator (opcjonalny)
    positional_or_keyword,    # 2. pozycyjne lub nazwane
    *args,                    # 3. dowolna liczba pozycyjnych
    keyword_only,             # 4. tylko nazwane (po *)
    **kwargs                  # 5. dowolna liczba nazwanych
):
```

---

### 🔸 Przykład pokazujący wszystkie typy

```python
def example(a, b, /, c, d=4, *args, e, f=6, **kwargs):
    print(a, b, c, d, args, e, f, kwargs)
```

Wywołania:
```python
example(1, 2, 3, e=5)
# a=1, b=2, c=3, d=4, args=(), e=5, f=6, kwargs={}

example(1, 2, 3, 4, 5, e=7, f=8, g=9)
# a=1, b=2, c=3, d=4, args=(5,), e=7, f=8, kwargs={'g': 9}
```

---

### 🔸 Znaczenie separatorów `/` i `*`

- `/` → wszystko **przed** nim może być przekazane **tylko pozycyjnie**, nie nazwą.
- `*` → wszystko **po** nim musi być przekazane **nazwą** (keyword-only).

---

### 🔹 Przykład z `/`
```python
def f(a, b, /, c):
    print(a, b, c)

f(1, 2, 3)        # ✅
f(1, 2, c=3)      # ✅
f(a=1, b=2, c=3)  # ❌ TypeError: a and b are positional-only
```

---

### 🔹 Przykład z `*`
```python
def g(a, *, b):
    print(a, b)

g(1, b=2)   # ✅
g(1, 2)     # ❌ TypeError: b must be passed as keyword
```

---

Czy chcesz, żebym rozpisał to w formie małej tabeli z typami parametrów, separatorami i przykładowymi wywołaniami?

---

**User:**

czy w ogólnym ujęciu ta kolejność nie powinna wyglądać tak?
def func(
    positional_only,          # 1. tylko pozycyjne (przed /)
    /,                        # separator (opcjonalny)
    positional_or_keyword,    # 2. pozycyjne lub nazwane
    *,                        # separator opcjonalny
    *args,                    # 3. dowolna liczba pozycyjnych
    keyword_only,             # 4. tylko nazwane (po *)
    **kwargs                  # 5. dowolna liczba nazwanych
):

---

**Assistant:**

Bardzo dobre spostrzeżenie — i masz **prawie rację**, ale w Pythonie jest **drobna różnica** między `*` jako separatorem a `*args` jako parametrem.  
Nie można mieć obu w dowolnym miejscu, więc formalnie kolejność wygląda trochę inaczej.

---

### ✅ **Poprawna kolejność składniowa (pełna forma)**

```python
def func(
    positional_only,          # 1. tylko pozycyjne (przed '/')
    /,                        #    separator (opcjonalny)
    positional_or_keyword,    # 2. pozycyjne lub nazwane
    *args,                    # 3. dowolna liczba pozycyjnych (opcjonalnie)
    keyword_only,             # 4. tylko nazwane (po '*args' lub samym '*')
    **kwargs                  # 5. dowolna liczba nazwanych
):
```

---

### 🔸 Ale są dwie sytuacje:
1. **Z `*args`** – gwiazdka należy do `*args`, więc nie możesz mieć drugiej, „gołej” `*`.
   ```python
   def f(a, b, *args, c, **kwargs):
       ...
   ```

2. **Bez `*args`** – możesz dać „gołą” `*`, żeby tylko wymusić parametry nazwane.
   ```python
   def f(a, b, *, c, d):
       ...
   ```

Czyli:
- `*args` **zastępuje** separator `*`
- jeśli nie potrzebujesz `*args`, ale chcesz wymusić nazwane parametry — dajesz samo `*`

---

### 🔹 W skrócie

| Sekcja | Typ parametrów | Notacja | Przykład |
|--------|----------------|----------|-----------|
| 1 | tylko pozycyjne | `a, b, /` | `def f(a, b, /)` |
| 2 | pozycyjne lub nazwane | `c, d` | `def f(a, b, c)` |
| 3 | dowolna liczba pozycyjnych | `*args` | `def f(*args)` |
| 4 | tylko nazwane | `*, e, f` lub `*args, e, f` | `def f(*, e)` |
| 5 | dowolna liczba nazwanych | `**kwargs` | `def f(**kwargs)` |

---

Czy chcesz, żebym pokazał kilka wariantów faktycznie działających definicji (np. z / i * w różnych kombinacjach), żeby zobaczyć różnice praktycznie?

---

**User:**

a mogę mieć tak?
def f(a, b, *, c, **kwargs):

---

**Assistant:**

Tak ✅ — dokładnie taka definicja jest **poprawna** i w pełni zgodna ze składnią Pythona.  

Oznacza to:

```python
def f(a, b, *, c, **kwargs):
    print(a, b, c, kwargs)
```

Zachowuje się tak:

```python
f(1, 2, c=3, d=4, e=5)
# a=1, b=2, c=3, kwargs={'d': 4, 'e': 5}
```

---

### 🔹 Co to znaczy dokładnie
- `a`, `b` → można przekazać **pozycyjnie** albo nazwą (bo są przed `*`)  
- `*` → od tego miejsca **wszystkie kolejne parametry muszą być nazwane**
- `c` → obowiązkowy **tylko nazwany** parametr  
- `**kwargs` → przechwyci **dowolne dodatkowe nazwane argumenty**

---

### 🔹 Niepoprawne wywołanie
```python
f(1, 2, 3)          # ❌ TypeError: f() takes 2 positional arguments but 3 were given
```
bo `c` musi być podane nazwą.

---

To jest bardzo częsty i praktyczny wzorzec, np. w bibliotekach — pozwala jasno oddzielić część pozycyjną od nazwanych argumentów konfiguracyjnych.

---

**User:**

czy w tym przypadku
def f(a, b, *args, c, **kwargs):
c jest nazwane czy dowolne?

---

**Assistant:**

Świetne pytanie — w tej definicji:  

```python
def f(a, b, *args, c, **kwargs):
```

parametr `c` jest **parametrem tylko nazwanym** (*keyword-only parameter*).  

---

### 🔹 Dlaczego
Ponieważ w Pythonie **wszystkie parametry po `*args` muszą być przekazywane nazwą**.  
Gwiazdkowy argument (`*args`) „zjada” wszystkie pozycje pozycyjne, więc `c` nie ma już pozycji, którą można by mu przypisać — dlatego **musi być przekazany jako `c=...`**.

---

### 🔹 Przykład:

```python
def f(a, b, *args, c, **kwargs):
    print(a, b, args, c, kwargs)

f(1, 2, 3, 4, c=5, d=6)
```

➡️ wynik:
```
1 2 (3, 4) 5 {'d': 6}
```

---

### 🔹 A gdybyś spróbował bez nazwy:
```python
f(1, 2, 3, 4, 5)
```

➡️ dostaniesz:
```
TypeError: f() missing 1 required keyword-only argument: 'c'
```

---

### 🔹 W skrócie

| Parametr | Typ | Jak można przekazać |
|-----------|-----|----------------------|
| `a`, `b` | pozycyjny lub nazwany | `f(1, 2)` lub `f(a=1, b=2)` |
| `*args` | zbiera dodatkowe pozycyjne | `(3, 4, ...)` |
| `c` | tylko nazwany | `c=5` |
| `**kwargs` | zbiera dodatkowe nazwane | `{'d': 6, ...}` |

---

Czy chcesz, żebym pokazał jak Python rozdziela te argumenty krok po kroku przy wywołaniu, np. co dokładnie trafia do `args`, `c` i `kwargs` przy różnych wywołaniach?