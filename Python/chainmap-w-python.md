# ChainMap w Pythonie

`ChainMap` to struktura danych dostępna w module standardowym `collections`, która pozwala na logiczne grupowanie wielu słowników (lub innych obiektów mapujących) w jeden spójny widok (tzw. view). Zamiast tworzyć nową, połączoną kopię wszystkich słowników (jak ma to miejsce przy użyciu metody `update()` czy operatora `|`), `ChainMap` przechowuje wewnątrz listę referencji do oryginalnych mapowań i wyszukuje w nich klucze po kolei.

## Dlaczego to jest ważne i kiedy się przydaje?

1. **Kaskadowe wyszukiwanie (Scope resolution / Fallback):** Jest to idealne rozwiązanie do obsługi konfiguracji aplikacji. Można łatwo zdefiniować priorytety wyszukiwania — np. 1. argumenty z linii poleceń, 2. zmienne środowiskowe, 3. konfiguracja z pliku, 4. wartości domyślne. Wyszukiwanie zatrzymuje się na pierwszym słowniku, w którym dany klucz istnieje.
2. **Wydajność pamięciowa i czasowa:** `ChainMap` nie tworzy pełnej kopii danych z innych słowników, co jest znacznie szybsze i oszczędza pamięć w przypadku bardzo dużych zbiorów danych.
3. **Dynamiczne odzwierciedlanie zmian:** Ponieważ `ChainMap` opiera się na referencjach, jeśli jakikolwiek oryginalny słownik ulegnie zmianie, te modyfikacje natychmiast znajdą odzwierciedlenie w naszym obiekcie `ChainMap`.

## Jak to działa?

Podczas tworzenia instancji, jako argumenty przekazujemy kolejne słowniki. Ważna jest kolejność argumentów: pierwszy z nich jest "na samym wierzchu" (najwyższy priorytet).

**Ważna zasada działania:** O ile odczyt (wyszukiwanie kluczy) polega na przeszukiwaniu wszystkich słowników po kolei, o tyle operacje modyfikujące (dodawanie, usuwanie, `pop()`, zmiana wartości pod istniejącym kluczem) są **zawsze aplikowane tylko do pierwszego (najwyższego priorytetem) słownika w łańcuchu.**

### Przykład użycia - Poziomy konfiguracji

```python
from collections import ChainMap

defaults = {'theme': 'Default', 'language': 'en', 'show_index': True}
file_config = {'language': 'pl'}
cli_args = {'theme': 'Dark'}

# Najwyższy priorytet mają argumenty CLI, następnie plik, na samym końcu wartości domyślne
config = ChainMap(cli_args, file_config, defaults)

print(config['theme'])       # Wypisze 'Dark' (wartość znaleziona w cli_args)
print(config['language'])    # Wypisze 'pl' (wartość znaleziona w file_config)
print(config['show_index'])  # Wypisze True (wartość znaleziona w defaults)

# Modyfikacja zawsze działa na pierwszym (najwyższym) słowniku!
config['show_index'] = False

# Powyższa operacja dodała 'show_index' = False do cli_args, a nie nadpisała wartości w defaults.
print(cli_args)              # {'theme': 'Dark', 'show_index': False}
print(defaults['show_index']) # True (oryginał pozostał nienaruszony)
```

### Przykład dynamicznego odzwierciedlania zmian

```python
from collections import ChainMap

dict1 = {'a': 1, 'b': 2}
dict2 = {'b': 3, 'c': 4}

chain = ChainMap(dict1, dict2)

print(chain['b']) # Wypisze 2, bo 'b' zostało znalezione w dict1

# Edytujemy źródłowy słownik, nie samego ChainMap
dict2['c'] = 40
print(chain['c']) # Wypisze 40 - ChainMap ma dostęp do aktualnego stanu źródłowych słowników
```

## Powiązane tematy

- [Zaawansowane zagadnienia w Pythonie](zaawansowane-zagadnienia-w-pythonie.md)
- [Python Cheatsheet](python-cheatsheet.md)
