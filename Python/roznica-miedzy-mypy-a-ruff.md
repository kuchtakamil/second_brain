# Różnica między mypy a ruff w Pythonie

**Data:** 2026-05-20

---

## Szybkie podsumowanie (TL;DR)

**mypy** oraz **ruff** to dwa fundamentalne narzędzia w nowoczesnym ekosystemie Pythona służące do statycznej analizy kodu. Choć oba pomagają pisać bezbłędny kod, rozwiązują **zupełnie inne problemy**:

*   **mypy** to **Type Checker** (analizator typów). Sprawdza poprawność logiki typów danych (np. czy nie próbujesz przekazać tekstu `str` tam, gdzie funkcja wymaga liczby `int`). Interesuje go, *co* kod robi ze strukturami danych w świetle adnotacji typów (PEP 484).
*   **ruff** to **Linter i Formatter** (narzędzie do stylu i jakości). Sprawdza styl kodu, zgodność z PEP 8, usuwa nieużywane importy, formatuje pliki (zastępuje `black`, `flake8`, `isort`) oraz wyłapuje oczywiste błędy składniowe lub antywzorce (np. brakujący `await`, zmienne nadpisujące wbudowane funkcje).

> [!TIP]
> **Krótka metafora:**
> * **mypy** jest jak inżynier sprawdzający, czy rury w projekcie budynku mają odpowiednią przepustowość i czy woda nie popłynie tam, gdzie powinien płynąć gaz (analiza logiczna danych).
> * **ruff** jest jak architekt dbający o to, by ściany były proste, pomalowane na właściwy kolor, a w pokojach nie leżały zbędne śmieci (estetyka, standardy i porządek).

---

## 1. Czym jest i co robi mypy?

**mypy** to pionierskie i najpopularniejsze narzędzie do sprawdzania typów (static type checking) w Pythonie. Analizuje kod przed jego uruchomieniem, bazując na adnotacjach typów (tzw. *type hints*).

### Przykład problemu dla mypy

Wyobraź sobie następujący kod:

```python
def pomnoz_tekst(tekst: str, razy: int) -> str:
    return tekst * razy

# Kod jest syntaktycznie poprawny, Python go uruchomi!
wynik = pomnoz_tekst(10, "super") 
```

Dla standardowego interpretera Pythona ten kod jest poprawny w fazie parsowania. Wywoła jednak błąd w czasie wykonywania (*runtime*), ponieważ nie można pomnożyć `10 * "super"`.

**Co robi mypy:**
Gdy uruchomisz `mypy skrypt.py`, narzędzie natychmiast zgłosi błąd:
```text
skrypt.py:5: error: Argument 1 to "pomnoz_tekst" has incompatible type "int"; expected "str"
skrypt.py:5: error: Argument 2 to "pomnoz_tekst" has incompatible type "str"; expected "int"
```
Mypy wykonuje głęboką analizę przepływu danych. Wie, jak typy przechodzą przez funkcje, klasy, generyki (`TypeVar`), unie (`Union` / `|`) oraz słowniki (`TypedDict`).

---

## 2. Czym jest i co robi ruff?

**ruff** to niezwykle szybkie (napisane w języku Rust) narzędzie typu "wszystko w jednym" do lintowania i formatowania kodu. Zostało stworzone, by zastąpić cały zestaw starszych narzędzi takich jak:
*   `flake8` (szukanie błędów stylu i jakości kodu)
*   `black` (automatyczne formatowanie kodu)
*   `isort` (sortowanie importów)
*   `bandit` (analiza bezpieczeństwa)
*   `pydocstyle` (sprawdzanie docstringów)

### Przykład problemu dla ruff

Spójrz na poniższy kod:

```python
import os  # ruff: nieużywany import!
import sys

def oblicz(a,b): # ruff: brak spacji po przecinku, brak spacji wokół operatorów
    Zmienna = a+b # ruff: zmienna powinna być pisana snake_case
    return a

async def pobierz_dane():
    import asyncio
    asyncio.sleep(1) # ruff: brak 'await' przy wywołaniu coroutine!
```

**Co robi ruff:**
Ruff błyskawicznie (często poniżej 10 milisekund) przeanalizuje plik i zgłosi:
1. Nieużywany import `os` (kod błędu: `F401`).
2. Niewłaściwy styl nazewnictwa zmiennej `Zmienna` (kod błędu: `N806`).
3. Brak słowa kluczowego `await` przed asynchronicznym sleepem (kod błędu: `RUF006`).
4. Dodatkowo, jeśli uruchomisz `ruff format`, automatycznie poprawi formatowanie kodu (doda odpowiednie spacje, przeniesie importy i ułoży je alfabetycznie).

---

## 3. Bezpośrednie porównanie (Tabela)

| Cecha | mypy | ruff |
| :--- | :--- | :--- |
| **Główna rola** | Sprawdzanie poprawności typów (Type Checker). | Sprawdzanie stylu, jakości kodu (Linter) oraz formatowanie (Formatter). |
| **Język napisania** | Python | Rust (dzięki temu jest 10x-100x szybszy od tradycyjnych linterów). |
| **Głębokość analizy** | **Głęboka.** Śledzi zależności, klasy, dziedziczenie, interfejsy i generyki w całym projekcie. | **Płaska.** Sprawdza reguły składniowe i wzorce linia po linii (lub plik po pliku). |
| **Wpływ na styl kodu** | Ignoruje spacje, wcięcia, cudzysłowy i nieużywane zmienne. | W pełni formatuje pliki, sortuje importy, pilnuje PEP 8. |
| **Przykładowy komunikat** | `incompatible type "str"; expected "int"` | `F401: 'os' imported but unused` |

---

## 4. Dlaczego ruff nie zastępuje mypy (i na odwrót)?

Ruff posiada zestaw reguł sprawdzających typowanie (np. zestaw reguł `ANN` wymuszający pisanie adnotacji typów). Może to rodzić błędne przekonanie, że ruff potrafi zastąpić mypy.

Nic bardziej mylnego! **Ruff potrafi sprawdzić jedynie strukturę zapisu**, np.:
*   Czy dodałeś adnotację typu do argumentu funkcji (np. czy napisałeś `: int`)?
*   Czy nie używasz przestarzałych zapisów typowania (np. zaleca używanie `list[int]` zamiast `List[int]` z modułu `typing`).

Ruff **nie potrafi jednak przeanalizować logicznej spójności tych typów**. Nie wie, czy obiekt klasy `A` przekazany do funkcji faktycznie spełnia wymagania protokołu `B`. Do tego niezbędny jest pełnoprawny type checker, taki jak **mypy** (lub **pyright**).

Z drugiej strony, mypy w ogóle nie interesuje się tym, czy Twój kod ma ładne wcięcia, czy importy są posortowane alfabetycznie i czy nie zapomniałeś usunąć zmiennej, której nigdzie nie używasz.

---

## 5. Jak używać ich razem w projekcie?

W nowoczesnych projektach standardem jest uruchamianie obu tych narzędzi w potoku CI/CD (np. GitHub Actions) oraz w edytorze kodu. Najwygodniej skonfigurować je wspólnie w pliku `pyproject.toml` w głównym katalogu projektu:

```toml
[tool.ruff]
line-length = 88
target-version = "py310"

[tool.ruff.lint]
# Wybór zestawów reguł (np. Pyflakes, Pycodestyle, isort, itp.)
select = ["E", "F", "I", "N", "UP", "ASYNC", "RUF"]
ignore = []

[tool.mypy]
python_version = "3.10"
warn_unused_configs = true
disallow_untyped_defs = true  # Wymagaj typowania we wszystkich funkcjach
strict_equality = true
ignore_missing_imports = true
```

Deweloperzy najczęściej:
1. Uruchamiają `ruff check --fix` oraz `ruff format`, aby automatycznie oczyścić kod ze zbędnych importów i poprawić formatowanie.
2. Następnie uruchamiają `mypy .`, aby upewnić się, że cała logika typowania w systemie jest w 100% spójna.

---

## Powiązane materiały

* [Typowanie w Pythonie](typowanie-w-pythonie.md) – Wprowadzenie do type hintów.
* [Typing Ignore Comments](Typing_Ignore_Comments.md) – Jak ignorować błędy sprawdzania typów oraz linterów.
