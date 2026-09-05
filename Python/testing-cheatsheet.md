# Testing Cheatsheet

Zwięzły cheatsheet obejmujący `pytest`, `unittest` i `unittest.mock`. Patrząc na tę stronę powinieneś być w stanie napisać i zmockować większość typowych testów.

---

## 1. Pierwszy test w pytest

```python
# test_math.py
def test_add():
    assert 1 + 1 == 2

def test_exception():
    with pytest.raises(ValueError, match="invalid"):
        int("abc")  # rzuca ValueError
```

```bash
pytest                     # uruchom wszystkie testy
pytest test_math.py        # jeden plik
pytest -k "add"            # testy pasujące do nazwy
pytest -x                  # stop po pierwszym upadku
pytest -v                  # verbose
```

## 2. Asercje w pytest

```python
assert result == expected
assert result != bad_value
assert value > 0
assert item in collection
assert isinstance(obj, MyClass)

# porównanie float z tolerancją
assert result == pytest.approx(3.14, abs=0.01)

# sprawdzenie wyjątku
with pytest.raises(KeyError):
    d = {}
    d["missing"]
```

## 3. Fixtures

Fixture = funkcja dostarczająca dane / zasoby do testu.

```python
import pytest

@pytest.fixture
def sample_user():
    return {"name": "Jan", "age": 30}

def test_user_name(sample_user):          # pytest wstrzyknie fixture
    assert sample_user["name"] == "Jan"
```

| Scope | Kiedy tworzone | Przykład użycia |
|:---|:---|:---|
| `function` (domyślny) | Przed **każdym** testem | lekkie obiekty |
| `class` | Raz na **klasę** testów | współdzielony stan |
| `module` | Raz na **plik** | połączenie DB |
| `session` | Raz na **cały run** | ciężki setup |

```python
@pytest.fixture(scope="module")
def db_connection():
    conn = create_connection()
    yield conn                # yield = teardown po testach
    conn.close()
```

## 4. Parametrize

Uruchom ten sam test z różnymi danymi:

```python
@pytest.mark.parametrize("input,expected", [
    ("hello", 5),
    ("", 0),
    ("abc", 3),
])
def test_len(input, expected):
    assert len(input) == expected
```

## 5. Markery

```python
@pytest.mark.slow
def test_heavy():
    ...

@pytest.mark.skip(reason="WIP")
def test_not_ready():
    ...

@pytest.mark.skipif(sys.platform == "win32", reason="Linux only")
def test_linux_only():
    ...
```

```bash
pytest -m slow              # uruchom tylko testy z markerem "slow"
pytest -m "not slow"        # pomiń testy slow
```

## 6. unittest — podstawy

```python
import unittest

class TestMath(unittest.TestCase):
    def setUp(self):                       # przed KAŻDYM testem
        self.data = [1, 2, 3]

    def tearDown(self):                    # po KAŻDYM teście
        self.data = None

    def test_sum(self):
        self.assertEqual(sum(self.data), 6)

    def test_contains(self):
        self.assertIn(2, self.data)

if __name__ == "__main__":
    unittest.main()
```

| Metoda | Sprawdza |
|:---|:---|
| `assertEqual(a, b)` | `a == b` |
| `assertNotEqual(a, b)` | `a != b` |
| `assertTrue(x)` | `bool(x) is True` |
| `assertFalse(x)` | `bool(x) is False` |
| `assertIs(a, b)` | `a is b` |
| `assertIn(a, b)` | `a in b` |
| `assertIsInstance(a, cls)` | `isinstance(a, cls)` |
| `assertRaises(Exc)` | podnosi `Exc` |

## 7. unittest.mock — Mock i MagicMock

```python
from unittest.mock import Mock, MagicMock

# Mock — pusty obiekt, który rejestruje wywołania
mock = Mock()
mock.some_method(1, 2, key="val")
mock.some_method.assert_called_once_with(1, 2, key="val")

# MagicMock — Mock + magic methods (__len__, __getitem__, ...)
m = MagicMock()
m.__len__.return_value = 5
assert len(m) == 5
```

| Atrybut / metoda | Opis |
|:---|:---|
| `mock.return_value` | wartość zwracana przy wywołaniu |
| `mock.side_effect` | funkcja/wyjątek/lista wyników |
| `mock.call_count` | ile razy wywołano |
| `mock.call_args` | ostatnie argumenty |
| `mock.assert_called()` | czy wywołano (min. raz) |
| `mock.assert_called_once()` | czy wywołano dokładnie raz |
| `mock.assert_not_called()` | czy nie wywołano |
| `mock.reset_mock()` | resetuje stan |

```python
# side_effect — różne wyniki dla kolejnych wywołań
mock = Mock(side_effect=[1, 2, ValueError("boom")])
mock()  # → 1
mock()  # → 2
mock()  # → raises ValueError

# side_effect jako funkcja
mock = Mock(side_effect=lambda x: x * 2)
assert mock(3) == 6
```

## 8. patch — podmiana obiektów w testach

`patch` zamienia obiekt na Mock **na czas testu** i przywraca oryginał po zakończeniu.

**Kluczowa zasada**: patchujesz tam, gdzie obiekt jest **importowany**, nie tam, gdzie jest **zdefiniowany**.

```python
from unittest.mock import patch

# Jako dekorator
@patch("myapp.services.requests.get")
def test_fetch(mock_get):
    mock_get.return_value.json.return_value = {"id": 1}
    result = fetch_user(1)
    assert result["id"] == 1
    mock_get.assert_called_once()

# Jako context manager
def test_fetch_v2():
    with patch("myapp.services.requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        result = fetch_user(1)
        assert result is not None

# patch.object — patch konkretnego atrybutu obiektu
with patch.object(MyService, "call_api", return_value=42):
    assert MyService().call_api() == 42
```

## 9. Mockowanie typowych scenariuszy

```python
# --- mockowanie metody klasy ---
class UserRepo:
    def get_by_id(self, user_id: int):
        ...  # prawdziwe zapytanie do DB

@patch.object(UserRepo, "get_by_id", return_value={"name": "Jan"})
def test_get_user(mock_method):
    repo = UserRepo()
    assert repo.get_by_id(1)["name"] == "Jan"

# --- mockowanie zmiennej środowiskowej ---
@patch.dict("os.environ", {"API_KEY": "test-key-123"})
def test_env():
    import os
    assert os.environ["API_KEY"] == "test-key-123"

# --- mockowanie open() ---
from unittest.mock import mock_open

@patch("builtins.open", mock_open(read_data="file content"))
def test_read_file():
    with open("any_file.txt") as f:
        assert f.read() == "file content"

# --- mockowanie datetime.now ---
@patch("myapp.utils.datetime")
def test_time(mock_dt):
    mock_dt.now.return_value = datetime(2025, 1, 1, 12, 0)
    assert get_current_hour() == 12
```

## 10. conftest.py

Współdzielone fixture — pytest **automatycznie** importuje `conftest.py` z danego katalogu.

```python
# conftest.py
import pytest

@pytest.fixture
def api_client():
    return TestClient(app)

@pytest.fixture(autouse=True)     # automatycznie dla KAŻDEGO testu
def reset_db():
    db.clear()
    yield
    db.clear()
```

## 11. Testowanie wyjątków (pytest vs unittest)

```python
# pytest
def test_division_by_zero():
    with pytest.raises(ZeroDivisionError):
        1 / 0

# unittest
class TestDiv(unittest.TestCase):
    def test_division_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            1 / 0
```

## 12. Struktura projektu testowego

```
myproject/
├── src/
│   └── myapp/
│       ├── __init__.py
│       ├── services.py
│       └── utils.py
├── tests/
│   ├── conftest.py          # wspólne fixtures
│   ├── test_services.py
│   └── test_utils.py
├── pyproject.toml
└── pytest.ini               # lub sekcja [tool.pytest] w pyproject.toml
```

```ini
# pytest.ini
[pytest]
testpaths = tests
addopts = -v --tb=short
markers =
    slow: marks tests as slow
```

---

## Powiązane pliki

- [PyTest: Przykłady i Scenariusze Testowania](PyTest_%20Przykłady%20i%20Scenariusze%20Testowania.md)
- [PyTest: Mockowanie](PyTest_Mockowanie.md)
- [Fixture overload — wyjaśnienie](fixture-overload-wyjaśnienie.md)
- [Patch i pytest.mark.asyncio w testach](patch-i-pytest-mark-asyncio-w-testach.md)
- [Pełny przykład testu z mockowaniem MagicMock](pelny-przyklad-testu-z-mockowaniem-magicmock.md)
