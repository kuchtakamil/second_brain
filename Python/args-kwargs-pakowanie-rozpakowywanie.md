# *args, **kwargs oraz Pakowanie i Rozpakowywanie (Packing/Unpacking)

Krótkie zestawienie operatorów `*` (asterisk) i `**` (double asterisk) w Pythonie. Służą one do **zwijania (pakowania)** wielu elementów w jedną strukturę oraz **rozwijania (rozpakowywania)** struktur na pojedyncze elementy.

## 1. W parametrach funkcji (Pakowanie / Zwija)

Pozwala funkcji przyjąć dowolną liczbę argumentów pozycyjnych (`*args`) i nazwanych (`**kwargs`).

```python
def my_func(*args, **kwargs):
    print("args (krotka):", args)
    print("kwargs (słownik):", kwargs)

my_func(1, 2, 3, name="Alice", age=30)
# args (krotka): (1, 2, 3)
# kwargs (słownik): {'name': 'Alice', 'age': 30}
```

## 2. W wywołaniach funkcji (Rozpakowywanie / Rozwija)

Przekształca kolekcje (np. listy, słowniki) na osobne argumenty przekazywane do funkcji.

```python
def add(a, b, c):
    return a + b + c

nums = [1, 2, 3]
print(add(*nums))  # Odpowiednik: add(1, 2, 3)

params = {'a': 10, 'b': 20, 'c': 30}
print(add(**params))  # Odpowiednik: add(a=10, b=20, c=30)
```

## 3. Rozpakowywanie zmiennych (Unpacking)

Rozdzielanie elementów kolekcji na osobne zmienne (z wykorzystaniem `*` do zebrania "reszty").

```python
# Zbieranie reszty - * pakuje pozostałe elementy w listę
first, *rest, last = [1, 2, 3, 4, 5]

print(first)  # 1
print(rest)   # [2, 3, 4]
print(last)   # 5
```

## 4. Łączenie/Scalanie struktur danych

Bardzo wygodny i szybki sposób scalania list, krotek, zbiorów czy słowników.

**Scalanie list:**
```python
list1 = [1, 2]
list2 = [3, 4]

merged_list = [0, *list1, *list2, 5]
# [0, 1, 2, 3, 4, 5]
```

**Scalanie słowników:**
```python
dict1 = {'a': 1, 'b': 2}
dict2 = {'b': 3, 'c': 4} # 'b' zostanie nadpisane!

merged_dict = {**dict1, **dict2, 'd': 5}
# {'a': 1, 'b': 3, 'c': 4, 'd': 5}
```

## 5. Konwersja między typami (string -> lista)

Operatora `*` można użyć szybkiego rozpakowania na przykład ciągu znaków do osobnych elementów w liście.

```python
letters = [*"HELLO"]
# ['H', 'E', 'L', 'L', 'O']
```
