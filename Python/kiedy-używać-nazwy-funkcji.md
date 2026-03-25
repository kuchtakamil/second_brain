# Kiedy używać nazwy funkcji

**Data:** 2025-11-01

---

**User:**

Python, w jakich przypadkach zamiast wywoływania przykładowej funkcji hello(), używa się tylko nazwy funkcji czyli hello?

---

**Assistant:**

W Pythonie samo odwołanie się do nazwy funkcji (np. `hello`) **nie wywołuje jej**, tylko **odwołuje się do obiektu funkcji** — czyli zwraca referencję do niej. To zachowanie wykorzystuje się w kilku typowych przypadkach:  

---

### 🔹 1. Przekazywanie funkcji jako argumentu
Często przekazujesz funkcję do innej funkcji, która ją później wywoła.  
Przykład:
```python
def hello():
    print("Hello!")

def run(func):
    func()  # wywołanie wewnątrz innej funkcji

run(hello)  # przekazujemy funkcję, nie wynik jej wywołania
```
Gdybyś napisał `run(hello())`, to `hello()` zostałoby wywołane natychmiast, a do `run` trafiłby `None` (bo `hello` nic nie zwraca).

---

### 🔹 2. Przypisywanie funkcji do zmiennej
Możesz przypisać funkcję do innej nazwy:
```python
def hello():
    print("Hello!")

say_hi = hello  # przypisanie, nie wywołanie
say_hi()        # działa jak hello()
```

---

### 🔹 3. Użycie w dekoratorach
Dekoratory operują na referencjach do funkcji:
```python
def decorator(func):
    def wrapper():
        print("Before")
        func()
        print("After")
    return wrapper

@decorator
def hello():
    print("Hello!")

# tutaj `hello` zostało przekazane jako referencja do dekoratora
```

---

### 🔹 4. Rejestrowanie callbacków lub handlerów
Np. w GUI, w bibliotekach asynchronicznych czy event-driven:
```python
button.on_click(hello)
```
Tu `hello` zostanie wywołane przez bibliotekę **dopiero wtedy**, gdy nastąpi kliknięcie.

---

### 🔹 5. Tworzenie list/dict funkcji
Przykład z dynamicznym wyborem funkcji:
```python
def add(x, y): return x + y
def sub(x, y): return x - y

ops = {'+': add, '-': sub}
result = ops['+'](2, 3)  # wywołanie przez referencję
```

---

Podsumowując:  
- `hello()` → **wywołanie funkcji**  
- `hello` → **referencja do funkcji** (obiekt, który można przekazać, przypisać, zarejestrować itp.)

Chcesz, żebym pokazał, jak to działa w kontekście np. funkcji wyższego rzędu albo lambd?