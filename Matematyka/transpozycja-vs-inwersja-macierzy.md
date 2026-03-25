# Transpozycja vs inwersja macierzy

**Data:** 2025-10-19

---

**User:**

w kontekście macierzy wyjasnij z przykładami czym różni się transpozycja od inwersji

---

**Assistant:**

Dobrze — zacznijmy od definicji i potem pokażę to na prostych przykładach, żeby różnica była jasna.  

---

## 🔹 Transpozycja macierzy

**Transpozycja** (oznaczana zwykle jako \( A^T \)) polega na **zamianie wierszy z kolumnami**.

Czyli:
\[
A_{ij}^T = A_{ji}
\]

Innymi słowy — element z wiersza \( i \) i kolumny \( j \) w macierzy \( A \) staje się elementem z wiersza \( j \) i kolumny \( i \) w macierzy \( A^T \).

### Przykład:

\[
A =
\begin{bmatrix}
1 & 2 & 3 \\
4 & 5 & 6
\end{bmatrix}
\]

Transpozycja:

\[
A^T =
\begin{bmatrix}
1 & 4 \\
2 & 5 \\
3 & 6
\end{bmatrix}
\]

➡️ **Interpretacja:**  
Wiersze stały się kolumnami.  
Nie zmienia to wartości elementów, tylko ich pozycje.

---

## 🔹 Inwersja (odwracanie macierzy)

**Inwersja** (oznaczana \( A^{-1} \)) to coś zupełnie innego.  
Odwrócona macierz jest **taką macierzą, która pomnożona przez oryginał daje macierz jednostkową**:

\[
A \cdot A^{-1} = A^{-1} \cdot A = I
\]

Nie każda macierz da się odwrócić — tylko **macierze kwadratowe** (takie same liczby wierszy i kolumn) **o niezerowym wyznaczniku** (\( \det(A) \neq 0 \)).

### Przykład:

\[
A =
\begin{bmatrix}
1 & 2 \\
3 & 4
\end{bmatrix}
\]

Wyznacznik:
\[
\det(A) = 1 \cdot 4 - 2 \cdot 3 = -2
\]

Macierz odwrotna:
\[
A^{-1} = \frac{1}{\det(A)} 
\begin{bmatrix}
4 & -2 \\
-3 & 1
\end{bmatrix}
= 
\begin{bmatrix}
-2 & 1 \\
1.5 & -0.5
\end{bmatrix}
\]

Sprawdzenie:
\[
A \cdot A^{-1} =
\begin{bmatrix}
1 & 2 \\
3 & 4
\end{bmatrix}
\begin{bmatrix}
-2 & 1 \\
1.5 & -0.5
\end{bmatrix}
=
\begin{bmatrix}
1 & 0 \\
0 & 1
\end{bmatrix}
= I
\]

---

## 🔸 Podsumowanie różnic

| Cecha | **Transpozycja** | **Inwersja** |
|:------|:------------------|:-------------|
| Operacja | Zamiana wierszy z kolumnami | Znalezienie macierzy, która odwraca mnożenie |
| Oznaczenie | \( A^T \) | \( A^{-1} \) |
| Wymaga macierzy kwadratowej? | Nie | Tak |
| Warunek istnienia | Zawsze istnieje | Tylko jeśli \(\det(A) \neq 0\) |
| Efekt | Zmiana pozycji elementów | Zmiana wartości elementów |
| Przykład efektu | \( [1\ 2; 3\ 4]^T = [1\ 3; 2\ 4] \) | \( [1\ 2; 3\ 4]^{-1} = [-2\ 1; 1.5\ -0.5] \) |

---

Chcesz, żebym pokazał jeszcze, **jak obliczać macierz odwrotną krok po kroku** (np. metodą Gaussa lub przez dopełnienia algebraiczne)?

---

**User:**

pandas/numpy wyjaśnij w = (XTX_inv @ X.T) @ y

---

**Assistant:**

Dobrze — rozbijmy ten zapis krok po kroku i wyjaśnijmy, **co dokładnie robi wyrażenie:**

\[
w = (XTX\_inv @ X.T) @ y
\]

w kontekście **NumPy / Pandas** (czyli Pythonowego kodu).

---

## 🔹 Kontekst: regresja liniowa

To równanie pochodzi z klasycznego wzoru na **rozwiązanie regresji liniowej metodą najmniejszych kwadratów (OLS – Ordinary Least Squares)**.

Celem regresji liniowej jest znalezienie wektora wag \( w \), który minimalizuje błąd między przewidywaniami \( Xw \) a obserwacjami \( y \).

Wzór analityczny:
\[
w = (X^T X)^{-1} X^T y
\]

---

## 🔹 Rozbicie składników

Zakładając, że używamy NumPy:

```python
w = (XTX_inv @ X.T) @ y
```

to oznacza:

### 1️⃣ `X`
Macierz cech (ang. *design matrix*), rozmiar:
\[
X: [n \times m]
\]
- \( n \) – liczba próbek (wierszy),
- \( m \) – liczba cech (kolumn).

Przykład:
```python
X = np.array([[1, 2],
              [3, 4],
              [5, 6]])
# 3 próbki, 2 cechy
```

---

### 2️⃣ `X.T`
Transpozycja macierzy \( X \) — zamiana wierszy z kolumnami.

\[
X^T: [m \times n]
\]

W NumPy:  
```python
X.T
```

---

### 3️⃣ `X.T @ X`
To iloczyn macierzy:
\[
X^T X
\]
czyli wynik o wymiarach \([m \times m]\).  
To tzw. **macierz Gram’a**, używana w regresji do obliczenia związków między cechami.

---

### 4️⃣ `XTX_inv`
To:
\[
(X^T X)^{-1}
\]
czyli **macierz odwrotna** do \( X^T X \).  
Obliczamy ją np. tak:
```python
XTX_inv = np.linalg.inv(X.T @ X)
```

---

### 5️⃣ `(XTX_inv @ X.T)`
To:
\[
(X^T X)^{-1} X^T
\]
czyli część wspólna wzoru.  
Wymiar: \([m \times n]\).

W NumPy `@` to operator mnożenia macierzy (jak `dot()`).

---

### 6️⃣ `((XTX_inv @ X.T) @ y)`
Teraz mnożysz to przez wektor \( y \) (rozmiar \([n \times 1]\)):

\[
w = (X^T X)^{-1} X^T y
\]

Ostatecznie otrzymujesz wektor współczynników \( w \) o rozmiarze \([m \times 1]\), czyli:
- jeden współczynnik na każdą cechę z \( X \),
- który najlepiej dopasowuje liniowy model do danych \( y \).

---

## 🔸 Przykład w Pythonie

```python
import numpy as np

# Dane wejściowe
X = np.array([[1, 1],
              [1, 2],
              [1, 3]])  # pierwsza kolumna to bias (stała 1)
y = np.array([1, 2, 2])

# Krok po kroku
XTX_inv = np.linalg.inv(X.T @ X)
w = (XTX_inv @ X.T) @ y

print(w)
```

**Wynik:**
```
[0.666..., 0.5]
```

Model liniowy:
\[
\hat{y} = 0.666... + 0.5x
\]

---

## 🔹 Intuicja

- Transpozycja `X.T` umożliwia „przekształcenie” danych tak, żeby dało się obliczyć zależność między kolumnami.
- Odwracanie `np.linalg.inv(X.T @ X)` kompensuje współzależności między cechami.
- Mnożenie przez `y` daje faktyczne współczynniki dopasowania.

---

Jeśli chcesz, mogę pokazać **wizualnie (np. na wykresie)**, jak `w = (XTX_inv @ X.T) @ y` dopasowuje prostą do punktów danych. Czy chcesz, żebym to pokazał?