# Ignorowanie statycznej analizy typów (`# type: ignore`)

W Pythonie – zwłaszcza podczas korzystania z narzędzi do statycznej analizy kodu takich jak `mypy`, `pyright`, czy serwerów językowych (np. Pylance w VS Code) – używamy adnotacji typów (tzw. "type hints"). Czasami jednak pojawiają się sytuacje, w których narzędzie zgłasza błąd typowania, chociaż jesteśmy pewni, że kod w czasie wykonania zadziała prawidłowo, lub z jakiegoś powodu nie jesteśmy w stanie (lub nie chcemy) danego przypadku poprawnie otypować.

Do wyciszania takich zgłoszeń służy specjalny komentarz: `# type: ignore`.

## Główne zastosowanie

Podstawową i najbardziej ogólną formą jest po prostu:

```python
x: int = "napis"  # type: ignore
```

Ten komentarz wycisza **wszystkie** błędy analizatora typów występujące dokładnie w tej jednej linii. Praktyka ta jednak jest niezalecana. Nazywa się ją "ślepym ignorowaniem" (*blanket ignore*). Powoduje to pewne ryzyko – w przyszłości może pojawić się w tej samej linijce inny, prawdziwy błąd, który nas pominie.

## Precyzyjne wyciszanie: `# type: ignore[kod-błędu]`

Dobrą i nowoczesną praktyką z analizatorami (zwłaszcza z najbardziej popularnym – `mypy`) jest ignorowanie konkretnych rodzajów błędów. Robimy to umieszczając kod (lub kody) błędu w nawiasach kwadratowych.

Przykład z treści Twojego pytania: **`# type: ignore[call-arg]`**

Poniżej znajdziesz omówienie najważniejszych kodów błędów obok `call-arg`:

### 1. `[call-arg]` – Zły argument wywołania

Pojawia się, gdy funkcja otrzymuje argumenty, z którymi nie wie co zrobić – wzywana jest z niewłaściwą liczbą argumentów, nieznanymi argumentami kluczowymi (kwargs) itp.

```python
def greet(name: str) -> None:
    print(f"Hello, {name}!")

# Przekazujemy argument kluczowy 'age', którego funkcja nie przyjmuje
greet("Alicja", age=30)  # type: ignore[call-arg]
```

### 2. `[arg-type]` – Zły typ argumentu

Pojawia się, gdy podajemy do funkcji argument w złym typie (niezgodnym z jej deklaracją).

```python
def process_number(x: int) -> int:
    return x * 2

result = process_number("10")  # type: ignore[arg-type]
```

### 3. `[assignment]` – Nieprawidłowe przypisanie

Wskazuje, że próbujesz przypisać wartość nowego typu do zmiennej, która została zadeklarowana dla innego typu.

```python
age: int = 25
age = "dwadzieścia pięć"  # type: ignore[assignment]
```

### 4. `[return-value]` – Nieprawidłowa wartość zwracana

Funkcja obiecuje zwrócić konkretny typ, a zwraca coś zupełnie innego.

```python
def fetch_data() -> dict[str, str]:
    return ["jakas", "lista"]  # type: ignore[return-value]
```

### 5. `[import]` i `[import-untyped]` – Typy z importów

Jeśli importujesz zewnętrzną bibliotekę (np. starszą i bez dodanych type hints / pliku `py.typed`), analizator zasugeruje błąd. W nowych wersjach `mypy` kod błędu rozdzielono, by było jasne, że brakuje typów z zewnętrznego modułu.

```python
import some_legacy_module  # type: ignore[import-untyped]
```

### 6. `[union-attr]` – Brak atrybutu (Związany np. z Optional)

Bywa frustrujący. Wyskakuje, gdy zmienna może mieć kilka typów na raz (np. Unia `int | None` czyli w starszym zapisie `Optional[int]`). Narzędzie nie pozwoli wykonać metody, o ile *wszystkie* typy w Unii jej nie posiadają.

```python
def get_user_name(user_id: int) -> str | None:
    return None if user_id == 0 else "Admin"

name = get_user_name(1)
# name jest `str | None`. Jeśli to None, wywołanie .upper() rzuci błędem AttributeError.
print(name.upper())  # type: ignore[union-attr]
```

*(Zazwyczaj zamiast ignore, lepiej jest w takim przypadku użyć bloku `if name is not None:`)*

### 7. `[attr-defined]` – Niezdefiniowany atrybut

Występuje odwołanie do pola (atrybutu/metody) obiektu/klasy, którego ten nie posiada (według analizatora).

```python
class Car:
    pass

my_car = Car()
# Python pozwala dynamicznie dodać właściwość, ale mypy o tym nie wie.
my_car.color = "Red"  # type: ignore[attr-defined]
```

## Podsumowanie i Kiedy używać

W pierwszej kolejności zawsze powinniśmy dążyć do rozwiązania samego problemu, a nie jego zignorowania. Możemy do tego używać lepszych rzutowań np. `typing.cast()` wykorzeniania pomyłek lub stosowania asercji typu `assert something is not None`.

Po `# type: ignore[...]` należy sięgać w kilku scenariuszach:

1. Analizator statyczny z racji swojej struktury "nie rozumie" w 100% dynamiki Pythona (np. użycia takich funkcji jak `getattr`, `setattr`, metaklas czy sztuczek z wykorzystaniem wstrzykiwania kodu "w locie" - *monkey patching*).
2. Korzystamy z bibliotek zewnętrznych o zamkniętym kodzie bez wprowadzonych adnotacji typu (tzw. zjawisko untyped dependencies).
3. Kod jest na tyle skomplikowany by go opisać sygnaturą (szczególnie `Generics`), że koszt napisania poprawnych reguł przyćmiewa zysk płynący ze sprawdzania typu.

Jeśli Twoim analizatorem jest **`mypy`**, przydatną opcją jest wymuszanie w narzędziu informowania o typach błędów - w konfiguracji `mypy.ini` (lub `pyproject.toml`) ustawiając opcję `show_error_codes = True`. Dzięki temu kompilacyjnemu outputowi natychmiast dowiesz się, jakiej nazwy (np. `[call-arg]`) trzeba użyć.

## Ignorowanie reguł Lintera: `# noqa`

Poza wyciszaniem błędów typowania (`# type: ignore`), w Pythonie często spotkasz się z wyciszaniem ostrzeżeń ze strony **linterów kodu** (narzędzi sprawdzających styl kodu i potencjalne błędy, takich jak `flake8`, `ruff`, czy `pylint`).

Służy do tego komentarz `# noqa`, co jest skrótem od *"No Quality Assurance"*. Podobnie jak w przypadku typów, dobrą praktyką jest podawanie konkretnego kodu błędu.

### `# noqa: F401` – Nieużywany import

Rodzina błędów zaczynających się na literę `F` dotyczy najczęściej narzędzi takich jak `flake8` lub `ruff`. Kod **F401** dosłownie oznacza błąd: *"Module imported but unused"* (Moduł zaimportowany, ale nieużyty).

Zazwyczaj linter nakazuje usunięcie martwych importów dla czystości kodu. Są jednak miejsca, gdzie robimy to celowo, przede wszystkim w plikach `__init__.py`. Stosuje się tam tzw. *re-eksportowanie* – importujemy coś z podrzędnego pliku tylko po to, by wystawić to na zewnątrz pakietu. Ponieważ w samym `__init__.py` nie wywołujemy zaimportowanej funkcji, linter zgłosi F401.

Aby poinformować linter, że jest to zjawisko celowe i oczekiwane, używamy tego komentarza:

```python
# zawartość pliku my_package/__init__.py

from .core import main_function  # noqa: F401
from .utils import my_helper     # noqa: F401
```

### Inne popularne kody `# noqa` do linterów

* `# noqa: E501` – Ignorowanie limitu długości linii (np. 88 znaków). Bardzo przydatne, gdy w kodzie mamy bardzo długi string lub link URL, którego po prostu nie da się estetycznie lub logicznie przełamać na dwie linijki.
* `# noqa: E402` – Ignorowanie reguły *"Module level import not at top of file"*. Przydaje się, gdy przed importami musimy skonfigurować jakieś rzeczy na poziomie skryptu, np. dodać ścieżkę do `sys.path`.
