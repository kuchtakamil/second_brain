# Dziedziczenie w Pythonie

**Data:** 2025-11-20

---

**User:**

Czy w Pythonie działa dziedziczenie po wielu klasach?

---

**Assistant:**

Tak, w Pythonie dziedziczenie wielokrotne działa.  

Możesz zdefiniować klasę dziedziczącą po kilku klasach naraz:

```python
class A:
    def foo(self):
        print("A")

class B:
    def foo(self):
        print("B")

class C(A, B):
    pass

c = C()
c.foo()  # wywoła metodę z A, bo A jest pierwsze w kolejności MRO
```

Python używa mechanizmu **MRO (Method Resolution Order)**, najczęściej algorytmu C3 linearization, aby ustalić kolejność przeszukiwania klas nadrzędnych. Dzięki temu unika konfliktów, jeśli wiele klas ma te same metody.

---

**User:**

Wyjaśnij w jaki sposób ustala się tą kolejność.

---

**Assistant:**

Kolejność wyszukiwania metod (MRO – Method Resolution Order) w Pythonie ustala się według **algorytmu C3 linearization**. Jego celem jest stworzenie jednej listy klas, po których Python będzie szukał metod, zachowując:

1. **Lokalną kolejność klas w definicji**  
   W `class C(A, B):` najpierw bierze się `A`, potem `B`.

2. **Hierarchię dziedziczenia**  
   Python stara się zachować naturalne kolejności rodziców wynikające z ich własnego MRO.

3. **Spójność (monotoniczność)**  
   Jeśli klasa X jest przed Y w MRO jakiejś klasy, to nie może być po Y w innej części hierarchii.

---

### Jak działa C3 – intuicyjnie

Dla klasy `C(A, B)` Python tworzy MRO przez połączenie:

- MRO klasy `A`
- MRO klasy `B`
- listy rodziców `[A, B]`

i **scala je podobnie do merge**:  
zawsze wybiera pierwszy element z list, który **nie jest** zależny od elementu pojawiającego się później w tych listach.

---

### Przykład:

```python
class A: pass
class B: pass
class C(A, B): pass
```

MRO:

- A → (A, object)
- B → (B, object)
- wektor baz: (A, B)

Łączenie:

1. Pierwszy kandydat: A  
   – pojawia się tylko jako pierwszy → można wziąć  
   → MRO = [C, A]

2. Następny: B  
   – również nie jest zablokowany przez niczego innego  
   → MRO = [C, A, B]

3. Na końcu `object`  
   → MRO = [C, A, B, object]

---

### Bardziej złożony przykład

```python
class A: pass
class B: pass
class C(A, B): pass
class D(B, A): pass
class E(C, D): pass  # to wywoła błąd
```

Tutaj algorytm nie da rady stworzyć spójnej kolejności  
(`C` wymaga A przed B, `D` wymaga B przed A), więc Python zgłosi błąd MRO.

---

### Jak podejrzeć MRO?

```python
print(C.__mro__)
# lub
import inspect
inspect.getmro(C)
```

---

Jeśli chcesz, mogę rozpisać MRO krok po kroku dla konkretnej hierarchii, którą podasz.