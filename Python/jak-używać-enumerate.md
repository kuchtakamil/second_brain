# Jak używać enumerate

**Data:** 2025-08-03

---

**User:**

jak zobaczyć co tworzy enumerate?
l = ["wyraz", "jedne", "dewaad"]
>>> print(enumerate(l))
<enumerate object at 0x7fdbe91a8810>

---

**Assistant:**

Funkcja `enumerate()` w Pythonie zwraca obiekt typu `enumerate`, który jest iteratorem zwracającym krotki `(indeks, element)` przy każdej iteracji. Żeby zobaczyć, co zawiera ten obiekt, musisz go przekonwertować na listę lub przeiterować po nim.

Przykład:

```python
l = ["wyraz", "jedne", "dewaad"]

# Konwersja na listę
print(list(enumerate(l)))
```

Wynik:
```python
[(0, 'wyraz'), (1, 'jedne'), (2, 'dewaad')]
```

Alternatywnie, możesz przeiterować:

```python
for index, value in enumerate(l):
    print(index, value)
```

Wynik:
```
0 wyraz
1 jedne
2 dewaad
```

Jeśli tylko napiszesz `print(enumerate(l))`, to dostajesz domyślną reprezentację obiektu iteratora, a nie jego zawartość.