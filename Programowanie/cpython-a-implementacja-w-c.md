# CPython a implementacja w C

**Data:** 2026-02-02

---

**User:**

Domyślna implementacy Pythona to CPython. Cyz to znaczy że został on stworzony w C?

---

**Assistant:**

Tak — **dokładnie to to znaczy**.

Nazwa **CPython** oznacza, że *referencyjna, domyślna implementacja interpretera Pythona jest napisana w języku C*.

### Co to implikuje technicznie

CPython to:
- interpreter Pythona
- kompilator do bytecode
- maszyna wirtualna wykonująca bytecode
- garbage collector
- cała implementacja obiektowego modelu Pythona

…i to wszystko jest zaimplementowane w C.

Dlatego m.in.:

- moduły rozszerzeń Pythona pisze się w C (C API Pythona)
- łatwo go osadzić w innych programach C/C++
- ma GIL (bo model pamięci i wątki są zarządzane w C)
- operacje na obiektach Pythona to operacje na strukturach C (`PyObject*`)
- reference counting jest robiony ręcznie w C (`Py_INCREF`, `Py_DECREF`)

### Przykład: obiekt w Pythonie to struktura w C

Np. integer w Pythonie to w CPythonie:

```c
typedef struct {
    PyObject ob_base;
    long ob_ival;
} PyLongObject;
```

Każdy obiekt w Pythonie to tak naprawdę `PyObject*` w C.

### Dlaczego to ważne

To tłumaczy:
- wydajność (i jej ograniczenia)
- GIL
- czemu numpy/pandas są szybkie (bo schodzą do C)
- czemu alternatywne implementacje istnieją

### Inne implementacje Pythona

Bo Python to **specyfikacja języka**, a nie CPython:

| Implementacja | W czym napisana | Cechy |
|---|---|---|
| CPython | C | domyślna |
| PyPy | RPython | JIT, często szybszy |
| Jython | Java | działa na JVM |
| IronPython | C# | działa na .NET |
| MicroPython | C | mikrokontrolery |

### Ciekawostka (bardzo istotna)

To, że Python jest wolny, **nie wynika z Pythona jako języka**.

Wynika z tego, że:
> CPython to interpreter napisany w C, który wykonuje dynamiczny model obiektów przez pointery i reference counting.

PyPy pokazuje, że ten sam język może być znacznie szybszy.

---

Krótko:

> **CPython = Python zaimplementowany w C.**