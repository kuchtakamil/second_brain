# gdzie w internecie mogę sprawdzić jakie zależności ma mangum?

**Data:** 8 sty 2026, 15:41:41 CET

---

**User:**

gdzie w internecie mogę sprawdzić jakie zależności ma mangum?

---

**Gemini:**

Istnieje kilka profesjonalnych źródeł, które pozwalają na wgląd w drzewo zależności (zarówno bezpośrednich, jak i przejściowych/transitive) dla biblioteki `mangum`.

### 1. PyPI (Python Package Index)

Najbardziej oficjalne źródło. Na stronie projektu w sekcji **Dependencies** można sprawdzić, co autor zadeklarował w metadanych paczki.

- **Link:** [pypi.org/project/mangum/](https://pypi.org/project/mangum/)
- Szukaj zakładki **"Built Distribution"** i kliknij w **"Dependencies"**. PyPI odczytuje te dane z pliku `METADATA` zawartego wewnątrz dystrybucji `wheel`.

### 2. GitHub (Źródło prawdy)

Większość nowoczesnych projektów Pythonowych (w tym Mangum) definiuje zależności w pliku `pyproject.toml` (zgodnie z PEP 518/621) lub starszym `setup.py`.

- **Link:** [github.com/jordaneremieff/mangum](https://github.com/jordaneremieff/mangum)
- Szukaj sekcji `[project.dependencies]` w pliku `pyproject.toml`.
- Obecnie `mangum` bezpośrednio zależy głównie od biblioteki **`anyio`**.

### 3. Libraries.io

To agregator metadanych o bibliotekach open-source. Jest szczególnie przydatny, ponieważ wizualizuje drzewo zależności i pokazuje tzw. **Transitive Dependencies** (czyli od czego zależą biblioteki, od których zależy Mangum).

- **Link:** [libraries.io/pypi/mangum](https://www.google.com/search?q=https://libraries.io/pypi/mangum)
- Sekcja **"Dependencies"** pokaże Ci listę paczek niezbędnych do działania.

### 4. Snyk Advisor

Narzędzie zorientowane na bezpieczeństwo, które bardzo czytelnie prezentuje kondycję pakietu oraz jego zależności.

- **Link:** [snyk.io/advisor/python/mangum](https://snyk.io/advisor/python/mangum)

---

### Analiza zależności Mangum w kontekście Twojego błędu

Mangum jest adapterem ASGI i opiera się na bibliotece `anyio` do obsługi asynchroniczności. Błąd `No module named 'mangum'` w AWS Lambda mimo obecności plików w konsoli sugeruje jeden z poniższych scenariuszy technicznych:

1. **Missing Transitive Dependencies**: Mangum wymaga `anyio`, które z kolei wymaga `idna` oraz `sniffio`. Jeśli instalowałeś paczkę ręcznie (np. kopiując folder), mogłeś pominąć te sub-zależności.
2. **Namespace Collisions**: Jeśli w Twoim projekcie lub w `PYTHONPATH` znajduje się inny plik lub folder o nazwie `mangum.py` lub `mangum/`, może on przesłaniać właściwą bibliotekę.
3. **Incomplete Installation**: Jeśli używasz `pip install -t . mangum`, pip powinien pobrać wszystkie zależności. Jeśli jednak budujesz paczkę w systemie Windows i wysyłasz ją na Lambdę (Amazon Linux 2/2023), upewnij się, że nie ma tam skompilowanych plików binarnych (`.so`), które są niekompatybilne (choć akurat mangum to czysty Python).

### Sprawdzenie lokalne (CLI)

Zamiast szukać w internecie, możesz sprawdzić dokładnie to, co masz zainstalowane w swoim środowisku, z którego budujesz paczkę:

```
# Wyświetla bezpośrednie zależności i metadane
pip show mangum

# Wyświetla pełne drzewo zależności (wymaga zainstalowania pipdeptree)
pip install pipdeptree
pipdeptree -p mangum
```

Efekt działania `pipdeptree` dla `mangum` powinien wyglądać mniej więcej tak:

```
mangum==X.X.X
└── anyio [required: >=3.0,<5.0, installed: 4.x.x]
    ├── idna [required: >=2.8, installed: 3.x]
    └── sniffio [required: >=1.1, installed: 1.x.x]
```

Jeśli w Twoim ZIP-ie na Lambdzie brakuje folderów `anyio`, `idna` lub `sniffio`, import `mangum` może rzucać błędy, ponieważ inicjalizacja modułu (w `__init__.py`) wymaga tych komponentów.

Czy chcesz, abym przygotował skrypt `build.sh`, który poprawnie spakuje wszystkie te zależności do formatu akceptowanego przez AWS Lambda?