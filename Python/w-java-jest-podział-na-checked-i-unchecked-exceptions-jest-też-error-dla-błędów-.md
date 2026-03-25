# W Java jest podział na checked i unchecked exceptions. Jest też Error dla błędów

**Data:** 3 sty 2026, 18:58:49 CET

---

**User:**

W Java jest podział na checked i unchecked exceptions. Jest też Error dla błędów w VM. Czy istnieje jakiśpodział wyjątków w Python?

---

**Gemini:**

W Pythonie nie istnieje ścisły podział na **checked** i **unchecked exceptions**, który jest charakterystyczny dla Javy. Wszystkie wyjątki w Pythonie są traktowane tak, jak `RuntimeException` w Javie – czyli są "unchecked". Kompilator (lub interpreter) nie wymusza na programiście deklarowania wyjątków w sygnaturze funkcji (`throws`) ani ich bezpośredniej obsługi.

Mimo braku wymuszenia syntaktycznego, Python posiada bardzo wyraźną hierarchię klas, która dzieli błędy na kilka kategorii logicznych.

---

### Hierarchia BaseException vs Exception

Kluczowy podział w Pythonie przebiega na poziomie klasy bazowej. Wszystkie wyjątki muszą dziedziczyć po `BaseException`, ale większość z nich dziedziczy po `Exception`.

#### 1. BaseException

Jest to klasa nadrzędna dla wszystkich wyjątków. Bezpośrednio z niej (omijając klasę `Exception`) dziedziczą wyjątki, które zazwyczaj nie powinny być przechwytywane przez standardowe bloki `try...except Exception:`:

- **`SystemExit`**: Wywoływany przez funkcję `sys.exit()`. Jeśli go przechwycisz, uniemożliwisz zamknięcie programu.
- **`KeyboardInterrupt`**: Wywoływany, gdy użytkownik naciśnie `Ctrl+C`. Przechwytywanie go w sekcji `Exception` mogłoby uniemożliwić przerwanie zapętlonego skryptu.
- **`GeneratorExit`**: Wywoływany, gdy generator lub korutyna są zamykane.

#### 2. Exception

To baza dla prawie wszystkich błędów związanych z logiką aplikacji. Zaleca się, aby instrukcje `except Exception:` przechwytywały właśnie tę klasę, co pozwala uniknąć przypadkowego zablokowania sygnałów systemowych wspomnianych wyżej.

---

### Podział funkcjonalny i techniczny

Choć Python nie ma słowa kluczowego `Error` w sensie VM-level fatal error (jak `OutOfMemoryError` w Javie), posiada klasy odpowiadające tym stanom:

| Kategoria | Przykład | Opis |
| --- | --- | --- |
| **Błędy krytyczne (VM/System)** | `MemoryError`, `SystemError` | Odpowiedniki Java `Error`. Sygnalizują poważne problemy wewnętrzne interpretera lub brak zasobów. |
| **Błędy składniowe** | `SyntaxError`, `IndentationError` | Występują podczas parsowania kodu, zanim jeszcze zostanie on wykonany. |
| **Błędy logiczne** | `ValueError`, `TypeError`, `KeyError` | Standardowe błędy runtime wynikające z błędnej logiki aplikacji. |
| **Błędy zasobów** | `OSError`, `FileNotFoundError` | Błędy wejścia/wyjścia, interakcja z systemem operacyjnym. |

---

### Zaawansowane mechanizmy: Exception Chaining

Python obsługuje tzw. **Exception Chaining** (łańcuchowanie wyjątków), co pozwala na śledzenie przyczyny błędu (causality). Służy do tego atrybut `__cause__` oraz składnia `raise ... from`.

```
def process_data(data):
    try:
        return data['id']
    except KeyError as e:
        raise ValueError("Invalid data format") from e

# W tym przypadku pierwotny KeyError jest przechowywany w __cause__
# i zostanie wyświetlony w tracebacku jako bezpośrednia przyczyna.
```

Można również użyć `raise ... from None`, aby celowo ukryć kontekst poprzedniego wyjątku, co jest przydatne w czystych interfejsach API.

---

### Exception Groups (Python 3.11+)

Wprowadzona w Pythonie 3.11 klasa `ExceptionGroup` pozwala na rzucanie wielu wyjątków jednocześnie. Jest to szczególnie istotne w programowaniu asynchronicznym (`asyncio`), gdzie kilka zadań może zawieść w tym samym czasie.

Do ich obsługi wprowadzono nową składnię `except*`:

```
try:
    raise ExceptionGroup(
        "Multiple errors",
        [ValueError("Invalid value"), TypeError("Invalid type")]
    )
except* ValueError as eg:
    print(f"Handled ValueErrors: {eg.exceptions}")
except* TypeError as eg:
    print(f"Handled TypeErrors: {eg.exceptions}")
```

---

### Obiekty Traceback i Inspekcja

Każdy wyjątek w Pythonie posiada atrybut `__traceback__`. W zaawansowanych systemach debugowania lub frameworkach (np. Sentry, Pytest), można manipulować tym obiektem za pomocą modułu `inspect` lub `traceback`, aby wyodrębnić stan stosu w momencie wystąpienia błędu.

Wyjątki są obiektami pierwszej klasy, co oznacza, że można je przekazywać jako argumenty, przechowywać w strukturach danych i dynamicznie modyfikować ich stan przed ponownym rzuceniem.

Czy chciałbyś, abym przygotował przykład implementacji customowego systemu obsługi błędów z wykorzystaniem asynchronicznych grup wyjątków?