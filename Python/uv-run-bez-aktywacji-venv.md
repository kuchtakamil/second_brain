# uv run — bez ręcznej aktywacji środowiska

**Data:** 2026-04-11

---

## TL;DR

`uv run` automatycznie wykrywa i używa wirtualnego środowiska projektu — nie musisz go wcześniej aktywować poleceniem `source .venv/bin/activate`.

---

## Jak to działa?

### 1. `uv run` działa jak „launcher"

Zamiast uruchamiać skrypt bezpośrednio przez interpreter systemowy (`python script.py`), `uv run` wykonuje kilka rzeczy za Ciebie:

1. **Odnajduje środowisko** — szuka katalogu `.venv` w bieżącym folderze lub w katalogach nadrzędnych (tzw. *workspace root*)
2. **Ustawia `PATH` i zmienne środowiskowe** tak, jak gdybyś aktywował venv ręcznie
3. **Wywołuje interpreter z `.venv`** — nie systemowego Pythona

```bash
# To samo co: source .venv/bin/activate && python script.py
uv run python script.py
```

### 2. Ukryta aktywacja

Aktywacja środowiska wirtualnego to w istocie tylko kilka zmian w zmiennych środowiskowych:

| Zmienna | Po `activate` | Co robi `uv run` |
|---|---|---|
| `PATH` | Dodaje `.venv/bin` na początku | Też to robi, ale tymczasowo |
| `VIRTUAL_ENV` | Ustawia ścieżkę do `.venv` | Ustawia przed uruchomieniem |
| `PYTHONPATH` | Może być modyfikowany | Zarządzane przez `uv` |

`uv run` robi to samo, ale tylko **na czas jednego wywołania** — nie zmienia Twojej bieżącej sesji terminala.

### 3. Automatyczny wybór środowiska

`uv` szuka środowiska w tej kolejności:

1. `.venv` w bieżącym katalogu
2. `.venv` w katalogu nadrzędnym (przydatne w monorepo)
3. Środowisko wskazane przez zmienną `VIRTUAL_ENV` (jeśli ustawiona)
4. Jeśli nic nie znajdzie — może stworzyć nowe `.venv` i zainstalować zależności z `pyproject.toml`

---

## Przykład

```
mój-projekt/
├── .venv/              ← tutaj jest środowisko
├── pyproject.toml
└── skrypt.py
```

```bash
# Bez uv — musisz aktywować
source .venv/bin/activate
python skrypt.py

# Z uv — jedno polecenie
uv run skrypt.py
```

Wynik jest identyczny, ale `uv run` nie "zaśmieca" sesji terminala — po zakończeniu skryptu `PATH` wraca do poprzedniego stanu.

---

## Dlaczego to lepsze?

| Cecha | `source activate` + `python` | `uv run` |
|---|---|---|
| Wymaga aktywacji | ✅ Tak | ❌ Nie |
| Brudzi sesję terminala | ✅ Tak | ❌ Nie |
| Działa w skryptach CI/CD | ⚠️ Trzeba pamiętać | ✅ Automatycznie |
| Przenośność | ⚠️ Ścieżki absolutne | ✅ Relatywne, bazuje na `.venv` |
| Może auto-instalować zależności | ❌ Nie | ✅ Tak (z `--with`) |

---

## Bonus: `uv run --with`

Możesz jednorazowo dodać pakiet bez instalowania go na stałe:

```bash
uv run --with rich python skrypt.py
```

`rich` będzie dostępny tylko podczas tego jednego uruchomienia.

---

## Powiązane pliki

- [uv-pip-vs-pip.md](uv-pip-vs-pip.md) — różnica między `uv pip` a zwykłym `pip`
- [jak-przy-użyciu-pip-uv-poetry-zainicjować-nowy-projekt-python.md](jak-przy-użyciu-pip-uv-poetry-zainicjować-nowy-projekt-python.md) — inicjalizacja projektu z `uv`
- [python-venv-creation.md](python-venv-creation.md) — jak tradycyjnie tworzy się venv
