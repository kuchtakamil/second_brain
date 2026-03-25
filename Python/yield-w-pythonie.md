# Yield w Pythonie

**Data:** 2025-11-06

---

**User:**

Mam duże doświadczenie w programowaniu ale nie rozumiem generatorów i użycia yield w Pythonie.

---

**Assistant:**

To częste — wielu doświadczonych programistów (zwłaszcza z języków takich jak Java czy C#) potrzebuje chwili, by "kliknęło" im działanie generatorów i `yield`.  
Poniżej wyjaśnię to praktycznie i bez nadmiaru teorii.

---

### 🧩 Co to jest generator
Generator to **funkcja, która nie zwraca wszystkich wyników naraz**, tylko **generuje je po jednym, na żądanie**.  
Dzięki temu:
- nie musisz trzymać całej listy w pamięci,
- możesz tworzyć **leniwe iteratory**, np. przetwarzać duże pliki, streamy, dane z API itp.

---

### 🔁 Różnica między `return` a `yield`

Zwykła funkcja:
```python
def liczby_do(n):
    result = []
    for i in range(n):
        result.append(i)
    return result

print(liczby_do(5))  # [0, 1, 2, 3, 4]
```

Generator:
```python
def liczby_do(n):
    for i in range(n):
        yield i  # zamiast zwrócić całość, zwraca po jednym elemencie

for x in liczby_do(5):
    print(x)
```

Wynik:
```
0
1
2
3
4
```

Tutaj `yield` **"zatrzymuje"** funkcję — zapamiętuje jej stan (zmienne, pozycję w pętli) — i wznawia ją przy kolejnym `next()`.

---

### ⚙️ Co dzieje się wewnątrz

Każda funkcja z `yield` **zwraca generator**, czyli obiekt, który implementuje protokół iteratora (`__next__`).

```python
g = liczby_do(3)
print(next(g))  # 0
print(next(g))  # 1
print(next(g))  # 2
# następne next(g) -> StopIteration
```

---

### 💡 Przykład praktyczny

#### Przetwarzanie dużego pliku liniami
Zamiast ładować cały plik:
```python
def czytaj_linie(path):
    with open(path) as f:
        for line in f:
            yield line.strip()
```

Użycie:
```python
for linia in czytaj_linie("duzy_plik.txt"):
    if "ERROR" in linia:
        print(linia)
```
Nie trzymasz całego pliku w pamięci — każda linia jest przetwarzana osobno.

---

### 🧠 Kluczowe punkty

| Cecha | Zwykła funkcja | Generator |
|-------|----------------|------------|
| Zwraca | wynik (np. lista) | iterator |
| Pamięć | przechowuje wszystko | tylko bieżący stan |
| Czas wykonania | od razu | stopniowo, na żądanie |
| Słowo kluczowe | `return` | `yield` |

---

Jeśli chcesz, mogę pokazać **równoważny przykład w Javie** (np. z `Iterator` lub `Stream`), żeby lepiej zobrazować analogię — chcesz?