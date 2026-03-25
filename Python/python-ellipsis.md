# Znaczenie `...` (Ellipsis / Wielokropek) w kodzie Python

W podanym przykładowym kodzie:

```python
    async def generate(
        self,
        system_prompt: str,
        user_message: str,
        *,
        tools: list[Any] | None = None,
    ) -> str: ...
```

Znak `...` to wbudowany w Pythona obiekt o nazwie **Ellipsis** (wielokropek). W powyższym kontekście (na końcu definicji funkcji, na miejscu ciała funkcji), pełni on rolę **symbolu zastępczego** (ang. *placeholder*), oznaczającego celowy brak implementacji.

Najczęściej `...` używa się w następujących sytuacjach:

## 1. Pliki z deklaracjami typów (Type Stubs - `.pyi`)

Jeśli przeglądasz kod źródłowy bibliotek (lub podpowiedzi IDE), wielokropek często pojawia się w plikach `.pyi`. Oznacza on, że w tym miejscu zaprezentowana jest tylko **sygnatura funkcji** (jej argumenty i zwracany typ), a właściwa implementacja znajduje się w innym pliku. Narzędzia do analizy statycznej (np. `mypy`) używają tego do sprawdzania poprawności typów bez analizowania całego logiki.

## 2. Protokoły (`typing.Protocol`)

W nowoczesnym Pythonie, przy użyciu typowania strukturalnego (tzw. "duck typing"), definiuje się czasem interfejsy za pomocą klasy dziedziczącej po `Protocol`. Określa ona tylko, że jakaś klasa musi posiadać daną metodę, ale samej metody nie implementuje. Użycie `...` jest wtedy standardową praktyką:

```python
from typing import Protocol, Any

class LLMProvider(Protocol):
    async def generate(self, system_prompt: str, user_message: str, *, tools: list[Any] | None = None) -> str: ...
```

## 3. Metody abstrakcyjne (`@abstractmethod`)

Podobnie, w klasach bazowych z wykorzystaniem modułu `abc` (Abstract Base Classes) deklaruje się metody, które muszą zostać nadpisane przez klasy pochodne. Zamiast używać pustego ciała czy słowa `pass`, idiomatyczne jest tam użycie wielokropka:

```python
from abc import ABC, abstractmethod

class BaseGenerator(ABC):
    @abstractmethod
    async def generate(self, system_prompt: str, user_message: str) -> str: ...
```

## 4. Zastępstwo dla słowa kluczowego `pass`

Ponieważ `...` jest poprawnym wyrażeniem (ewaluuje się do obiektu `Ellipsis`), można go użyć wszędzie tam, gdzie składnia wymaga instrukcji, a my nie chcemy nic robić. Wielokropek jest często wizualnie czytelniejszy niż `pass`, symbolizując np. miejsce na przyszły kod ("TODO"):

```python
def my_function_implement_later():
    ...
```

## Podsumowanie

W zaprezentowanym kodzie wielokropek oznacza, że **pokazano sam interfejs funkcji**. Informuje on Ciebie (i narzędzia programistyczne), jak należy wywoływać testowaną/opisywaną funkcję, ale by nie zaciemniać obrazu, pominięto w tym wglądzie szczegóły tego, jak ona dokładnie działa pod maską.
