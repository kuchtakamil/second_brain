# `patch()` jako Context Manager i `pytest.mark.asyncio` — Anatomia Testu Asynchronicznego

Poniższy dokument szczegółowo rozkłada na czynniki pierwsze fragment testu jednostkowego, który łączy w sobie dwie potężne techniki: **mockowanie za pomocą `patch()` w trybie context managera** oraz **testowanie kodu asynchronicznego z użyciem `pytest.mark.asyncio`**. Obydwa mechanizmy pełnią komplementarne, ale zasadniczo różne role.

---

## Analizowany Fragment Testu

```python
@pytest.mark.asyncio
async def test_full_info_maps_all_fields():
    tool = YahooFinanceTool()
    with patch("dd.tools.yahoo_finance.yf.Ticker", return_value=_make_mock(_FULL_INFO)):
        metrics = await tool.execute(ticker="AAPL")

    assert isinstance(metrics, FinancialMetrics)
    assert metrics.market_cap == 3_000_000_000_000
    assert metrics.pe_ratio == pytest.approx(29.5)
    assert metrics.revenue_ttm == 400_000_000_000
```

Oraz testowany kod produkcyjny:

```python
class YahooFinanceTool:
    async def execute(self, *, ticker: str) -> FinancialMetrics:
        return await asyncio.to_thread(self._fetch, ticker.upper().strip())
```

---

## 1. `pytest.mark.asyncio` — Uruchamianie Korutyn w Testach

### Co to jest?

`pytest.mark.asyncio` to **dekorator (marker)** dostarczany przez wtyczkę [`pytest-asyncio`](https://github.com/pytest-dev/pytest-asyncio). Jego jedyne, ale kluczowe zadanie to: **pozwolić pytest'owi uruchomić funkcję testową zadeklarowaną jako `async def`**.

### Dlaczego jest potrzebny?

Bez tego markera pytest nie wie, co zrobić z korutyną. Standardowy runner pytest oczekuje **zwykłych, synchronicznych funkcji**. Gdy napotka `async def`, bez dodatkowej konfiguracji po prostu ją zignoruje lub wyrzuci błąd.

Oto co dzieje się pod spodem:

```text
BEZ @pytest.mark.asyncio:
  pytest widzi async def test_...()
  → wywołuje ją jak normalną funkcję
  → dostaje obiekt coroutine (nie wynik!)
  → test "przechodzi" bez wykonania kodu (cichy fałszywy sukces!)

Z @pytest.mark.asyncio:
  pytest-asyncio przechwytuje test
  → tworzy pętlę zdarzeń (event loop)
  → uruchamia korutynę: asyncio.run(test_full_info_maps_all_fields())
  → czeka na zakończenie wszystkich await'ów
  → raportuje wynik testu
```

> [!CAUTION]
> Bez markera `@pytest.mark.asyncio` test asynchroniczny **nie zostanie faktycznie wykonany**. Pytest potraktuje zwrócony obiekt korutyny jako „truthy" i test przejdzie — nawet jeśli zawiera błędy logiczne. To jeden z najniebezpieczniejszych cichych błędów w testach Pythona.

### Mechanizm działania krok po kroku

1. **Wtyczka `pytest-asyncio`** rejestruje się jako plugin w pytest.
2. Gdy pytest napotyka marker `@pytest.mark.asyncio`, deleguje uruchomienie testu do specjalnego runnera.
3. Runner tworzy **nową pętlę zdarzeń** (`asyncio.EventLoop`) dla każdego testu (domyślny tryb `function`).
4. Korutyna testowa jest uruchamiana wewnątrz tej pętli za pomocą `loop.run_until_complete()`.
5. Wszelkie `await` wewnątrz testu (np. `await tool.execute(...)`) są prawidłowo obsługiwane.
6. Po zakończeniu testu pętla jest zamykana.

### Kiedy jest potrzebny?

Zawsze, gdy testujesz kod, który używa `async`/`await`. W naszym przypadku:

```python
async def execute(self, *, ticker: str) -> FinancialMetrics:
    return await asyncio.to_thread(self._fetch, ticker.upper().strip())
```

Metoda `execute` jest **korutyną** (`async def`), więc aby ją wywołać w teście, musimy użyć `await` — a to wymaga, by sam test też był `async def` + miał marker `@pytest.mark.asyncio`.

### Tryby konfiguracji (`mode`)

Wtyczka `pytest-asyncio` oferuje różne tryby wykrywania testów asynchronicznych:

| Tryb | Opis |
|:---|:---|
| `mode = "strict"` (domyślny) | Wymaga jawnego markera `@pytest.mark.asyncio` na każdym teście async |
| `mode = "auto"` | Automatycznie wykrywa i uruchamia wszystkie `async def test_*` bez markera |

Konfiguracja w `pyproject.toml`:

```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
```

> [!TIP]
> Jeśli w projekcie jest dużo testów asynchronicznych, tryb `auto` eliminuje konieczność powtarzania dekoratora nad każdą funkcją. Jednak tryb `strict` jest bezpieczniejszy — zmusza do jawnego oznaczania, co jest async.

---

## 2. `patch()` — Podmiana Obiektu na Czas Testu

### Co to jest?

`patch()` to funkcja z wbudowanej biblioteki `unittest.mock`, która **tymczasowo podmienia obiekt** (klasę, funkcję, zmienną) pod podanym adresem w przestrzeni nazw Pythona. Po zakończeniu bloku `with` (lub dekoratora) **automatycznie przywraca oryginalny obiekt**.

### Jak działa w naszym przykładzie?

```python
with patch("dd.tools.yahoo_finance.yf.Ticker", return_value=_make_mock(_FULL_INFO)):
    metrics = await tool.execute(ticker="AAPL")
```

Rozbijmy ten zapis na elementy:

#### A. Ścieżka `"dd.tools.yahoo_finance.yf.Ticker"`

To **ścieżka kropkowa** (dotted path) wskazująca, **gdzie** w przestrzeni nazw Pythona znajduje się obiekt do podmienienia:

```text
dd.tools.yahoo_finance    ← moduł (plik dd/tools/yahoo_finance.py)
         .yf              ← obiekt 'yf' w tym module (zaimportowana biblioteka yfinance)
            .Ticker       ← klasa Ticker w obiekcie yf
```

To oznacza, że gdzieś w pliku `dd/tools/yahoo_finance.py` istnieje import w stylu:

```python
import yfinance as yf
```

A kod produkcyjny wywołuje `yf.Ticker("AAPL")`, aby utworzyć obiekt reprezentujący akcję.

> [!IMPORTANT]
> **Złota zasada mockowania** (Where to Patch): Patchujemy `yf.Ticker` **w module, który go używa** (`dd.tools.yahoo_finance`), a nie w oryginalnej bibliotece `yfinance`. Dlaczego? Bo Python tworzy **lokalną referencję** `yf` w przestrzeni nazw modułu `dd.tools.yahoo_finance`. Patch musi celować w tę lokalną referencję.

#### B. Argument `return_value=_make_mock(_FULL_INFO)`

Ten parametr definiuje, **co zostanie zwrócone**, gdy kod produkcyjny wywoła `yf.Ticker("AAPL")`:

```text
Normalny przebieg (bez mocka):
  yf.Ticker("AAPL")  →  prawdziwy obiekt Ticker  →  łączy się z Yahoo Finance API

Z mockiem:
  yf.Ticker("AAPL")  →  _make_mock(_FULL_INFO)  →  sztuczny obiekt z przygotowanymi danymi
```

Funkcja `_make_mock(_FULL_INFO)` to **fabryka mocka** — tworzy obiekt, który udaje prawdziwy obiekt `Ticker` z atrybutem `.info` zawierającym słownik `_FULL_INFO` z kontrolowanymi danymi testowymi (market_cap, pe_ratio itp.).

#### C. Context Manager (`with ... :`)

Użycie `patch()` jako context managera oznacza:

```python
# PRZED blokiem with:
# yf.Ticker w module dd.tools.yahoo_finance → prawdziwa klasa z yfinance

with patch("dd.tools.yahoo_finance.yf.Ticker", return_value=_make_mock(_FULL_INFO)):
    # WEWNĄTRZ bloku:
    # yf.Ticker → MagicMock, który przy wywołaniu zwraca _make_mock(_FULL_INFO)
    metrics = await tool.execute(ticker="AAPL")

# PO bloku with:
# yf.Ticker → znowu prawdziwa klasa (mock jest automatycznie "odpięty")
```

> [!TIP]
> Użycie `patch()` jako context managera (`with`) jest preferowane nad dekoratorem `@patch(...)`, bo:
> 1. **Precyzyjnie ogranicza zakres** — mock działa tylko tam, gdzie jest potrzebny
> 2. **Nie zaśmieca sygnatury** — nie dodaje dodatkowych parametrów do `def test_...(...)`
> 3. **Łatwiej się czyta** — widać dokładnie, który fragment kodu jest objęty mockiem

#### D. Wiele mocków naraz — czy `with` daje radę?

Tak — i to na trzy sposoby. Wyobraźmy sobie, że `_fetch` oprócz `yf.Ticker` wywołuje jeszcze `yf.download`:

**Sposób 1 — Zagnieżdżone `with` (działa wszędzie):**

```python
async def test_multiple_patches_nested():
    tool = YahooFinanceTool()
    with patch("dd.tools.yahoo_finance.yf.Ticker", return_value=mock_ticker):
        with patch("dd.tools.yahoo_finance.yf.download", return_value=mock_df):
            metrics = await tool.execute(ticker="AAPL")

    assert metrics.market_cap == 3_000_000_000_000
```

Czytelne przy 2 mockach, ale przy 4–5 wcięcia rosną w piramidę.

**Sposób 2 — `ExitStack` z `contextlib` (elegancko przy wielu mockach):**

```python
from contextlib import ExitStack

async def test_multiple_patches_exitstack():
    tool = YahooFinanceTool()
    with ExitStack() as stack:
        mock_ticker_cls = stack.enter_context(
            patch("dd.tools.yahoo_finance.yf.Ticker", return_value=mock_ticker)
        )
        mock_download = stack.enter_context(
            patch("dd.tools.yahoo_finance.yf.download", return_value=mock_df)
        )
        metrics = await tool.execute(ticker="AAPL")

    assert metrics.market_cap == 3_000_000_000_000
```

`ExitStack` zarządza wieloma context managerami bez zagnieżdżania. Każdy `enter_context()` rejestruje kolejnego patcha, a po wyjściu z bloku `with` wszystkie są automatycznie odwracane — w kolejności odwrotnej do rejestracji (LIFO).

**Sposób 3 — Nawiasy w `with` (Python ≥ 3.10, najczytelniejszy):**

```python
async def test_multiple_patches_parenthesized():
    tool = YahooFinanceTool()
    with (
        patch("dd.tools.yahoo_finance.yf.Ticker", return_value=mock_ticker) as mock_t,
        patch("dd.tools.yahoo_finance.yf.download", return_value=mock_df) as mock_d,
    ):
        metrics = await tool.execute(ticker="AAPL")

    assert metrics.market_cap == 3_000_000_000_000
```

Od Pythona 3.10 można grupować wiele context managerów w nawiasach — płasko, bez zagnieżdżania, z opcjonalnym `as` do przechwycenia referencji do mocka.

> [!NOTE]
> **Który sposób wybrać?**
>
> | Sposób | Kiedy stosować |
> |:---|:---|
> | Zagnieżdżone `with` | 2 mocki, projekt na Python < 3.10 |
> | `ExitStack` | 3+ mocków, dynamiczna liczba mocków, Python < 3.10 |
> | Nawiasy `with (...)` | Zawsze gdy Python ≥ 3.10 — najczytelniejsza forma |

---

## 3. Pełny Przebieg Testu — Krok Po Kroku

Poniższy diagram ilustruje dokładny przepływ wykonania testu:

```text
1. pytest uruchamia test
   ↓
2. @pytest.mark.asyncio → pytest-asyncio tworzy event loop
   ↓
3. tool = YahooFinanceTool()  → tworzy instancję testowanej klasy
   ↓
4. patch("dd.tools.yahoo_finance.yf.Ticker", ...)
   → Python znajduje obiekt yf.Ticker w module dd.tools.yahoo_finance
   → zapamiętuje oryginalną referencję
   → podmienia ją na MagicMock z return_value=_make_mock(_FULL_INFO)
   ↓
5. await tool.execute(ticker="AAPL")
   → execute() jest korutyną, więc event loop ją scheduluje
   → wewnętrznie: asyncio.to_thread(self._fetch, "AAPL")
   → _fetch() wywołuje yf.Ticker("AAPL")
   → ALE yf.Ticker to teraz mock!
   → mock zwraca _make_mock(_FULL_INFO) zamiast łączyć się z API
   → _fetch() odczytuje dane z mocka i buduje obiekt FinancialMetrics
   → zwraca FinancialMetrics do testu
   ↓
6. with-block kończy się
   → patch przywraca oryginalny yf.Ticker
   ↓
7. Asercje (POZA blokiem with — mock już nie jest potrzebny):
   → isinstance(metrics, FinancialMetrics) → True
   → metrics.market_cap == 3_000_000_000_000 → True
   → metrics.pe_ratio == pytest.approx(29.5) → True (z tolerancją)
   → metrics.revenue_ttm == 400_000_000_000 → True
   ↓
8. Test przechodzi ✅
```

---

## 4. Dlaczego `pytest.approx(29.5)`?

Wyrażenie `pytest.approx(29.5)` to **porównanie z tolerancją** dla liczb zmiennoprzecinkowych. W arytmetyce komputerowej `float` nie jest dokładny:

```python
>>> 0.1 + 0.2 == 0.3
False  # 0.30000000000000004 != 0.3

>>> 0.1 + 0.2 == pytest.approx(0.3)
True   # porównanie z domyślną tolerancją 1e-6
```

W naszym teście `pe_ratio` (wskaźnik cena/zysk) jest liczbą `float`, więc bezpośrednie porównanie `==` mogłoby zawieść z powodu drobnych błędów zaokrągleń. `pytest.approx()` rozwiązuje ten problem.

---

## 5. Rola `asyncio.to_thread()` w Kodzie Produkcyjnym

```python
async def execute(self, *, ticker: str) -> FinancialMetrics:
    return await asyncio.to_thread(self._fetch, ticker.upper().strip())
```

Metoda `_fetch` jest **synchroniczna** (prawdopodobnie wywołuje `yf.Ticker(...).info`, co jest blokującym zapytaniem HTTP). Gdyby wywołać ją bezpośrednio w korutynie, zablokowałaby pętlę zdarzeń.

`asyncio.to_thread()` rozwiązuje ten problem:

```text
Pętla zdarzeń (event loop) — wątek główny
  ↓
  await asyncio.to_thread(self._fetch, "AAPL")
    → przenosi _fetch do osobnego wątku z puli ThreadPoolExecutor
    → pętla zdarzeń jest wolna i może obsługiwać inne korutyny
    → gdy _fetch zakończy się, wynik wraca do korutyny
```

> [!NOTE]
> Wzorzec `asyncio.to_thread(synchroniczna_funkcja)` jest standardowym sposobem na integrację blokujących bibliotek (jak `yfinance`, `requests`, operacje na plikach) z kodem asynchronicznym bez blokowania event loopa.

---

## 6. Podsumowanie Mechanizmów

| Mechanizm | Rola w teście | Dlaczego jest potrzebny |
|:---|:---|:---|
| `@pytest.mark.asyncio` | Uruchomienie `async def` testu w pętli zdarzeń | Bez niego test nie zostanie wykonany (cichy fałszywy sukces) |
| `patch("dd.tools...yf.Ticker", ...)` | Podmiana klasy `Ticker` na mock | Izolacja od prawdziwego API Yahoo Finance |
| `return_value=_make_mock(...)` | Definicja co zwróci sfałszowany `Ticker(...)` | Kontrola danych wejściowych testu |
| `with ... :` (context manager) | Ograniczenie zakresu mocka | Automatyczne przywrócenie oryginału po bloku |
| `await tool.execute(...)` | Wywołanie testowanej korutyny | Testowanie asynchronicznej logiki biznesowej |
| `pytest.approx(29.5)` | Porównanie float z tolerancją | Uniknięcie fałszywych niepowodzeń z powodu zaokrągleń |
| `asyncio.to_thread()` | Uruchomienie blokującego kodu w osobnym wątku | Ochrona event loopa przed blokadą |

---

## Przydatne Powiązania

- Kompleksowy przewodnik po technikach mockowania: [Mockowanie i Monkeypatching w PyTest](PyTest_Mockowanie.md)
- Pełny przykład testu z MagicMock i wzorcem Arrange-Act-Assert: [Pełny Przykład Testu z Mockowaniem](pelny-przyklad-testu-z-mockowaniem-magicmock.md)
- Cheatsheet z asyncio: [Asyncio Cheatsheet](asyncio-cheatsheet.md)
- Szczegółowy przewodnik po async/await: [Async i Await w Pythonie](async-await-w-pythonie.md)
