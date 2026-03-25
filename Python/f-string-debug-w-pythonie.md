# F-string debug w Pythonie

**Data:** 2026-02-04

---

**User:**

Python
def foo(var):
   print(f'{var=}')
Co oznacza to = po var?

---

**Assistant:**

To jest **f-string debug syntax** wprowadzony w **Pythonie 3.8** (PEP 498 rozszerzony przez PEP 572/PEP 563 work).

Zapis:

```python
print(f'{var=}')
```

oznacza:

> „wypisz nazwę zmiennej oraz jej wartość”

czyli **Python sam dokleja nazwę wyrażenia** po lewej stronie.

### Przykład

```python
var = 42
print(f'{var=}')
```

wynik:

```
var=42
```

To jest skrót dla:

```python
print(f'var={var}')
```

ale działa dla **dowolnego wyrażenia**, nie tylko zmiennej.

---

### Prawdziwa siła — wyrażenia

```python
x = 10
y = 5
print(f'{x+y=}')
```

wynik:

```
x+y=15
```

albo:

```python
print(f'{len("hello")=}')
```

wynik:

```
len("hello")=5
```

---

### Formatowanie dalej działa

Możesz dalej stosować formatowanie:

```python
pi = 3.14159
print(f'{pi=:.2f}')
```

wynik:

```
pi=3.14
```

---

### Do czego to jest stworzone?

To jest **narzędzie stricte debugowe** — żeby:

- nie pisać ręcznie nazw zmiennych
- szybko logować stan programu
- łatwo dodawać/usuwać debug printy

Bardzo użyteczne przy szybkim diagnozowaniu, dużo czytelniejsze niż:

```python
print("x:", x, "y:", y)
```

vs

```python
print(f'{x=} {y=}')
```

---

### Podsumowanie

`{expr=}` w f-stringu znaczy:

> wypisz tekst wyrażenia + `=` + jego wartość

I to jest jedna z najbardziej niedocenionych, a bardzo praktycznych funkcji Pythona 3.8+.