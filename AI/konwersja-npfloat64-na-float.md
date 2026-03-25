# Konwersja np.float64 na float

**Data:** 2025-10-25

---

**User:**

biblioteka pandas:
df['power'].mean() dostaję np.float64(149.65729212983547). Jak mogę dostać tylko tą liczbę?

---

**Assistant:**

Wartość typu `np.float64` to po prostu obiekt NumPy, który zachowuje się prawie jak zwykły `float` w Pythonie — tylko jego typ jest inny.  
Aby uzyskać „czystą” liczbę typu `float`, możesz:

### 🔹 Opcja 1 – rzutowanie na `float`
```python
float(df['power'].mean())
```

To najczęstszy i najprostszy sposób. Wynik będzie typu `float` (np. `149.65729212983547`).

### 🔹 Opcja 2 – użycie metody `.item()`
```python
df['power'].mean().item()
```
`.item()` konwertuje pojedynczą wartość NumPy na natywny typ Pythona (tutaj `float`).

---

💡 Oba sposoby dadzą taki sam efekt:
```python
mean_val = df['power'].mean()
print(type(mean_val))         # <class 'numpy.float64'>
print(float(mean_val))        # 149.65729212983547
print(mean_val.item())        # 149.65729212983547
```

Najczęściej stosuje się `float(...)`.

---

**User:**

skąd wzięła się nazwa funkcji iloc w pandas?

---

**Assistant:**

Nazwa `iloc` w bibliotece **pandas** pochodzi od słów:  

> **i**ndex **loc**ation  

czyli dosłownie: **lokalizacja według indeksu liczbowego**.  

---

### Szczegóły:
- `iloc` służy do **indeksowania pozycyjnego** — czyli odwoływania się do wierszy i kolumn **na podstawie ich położenia (liczby porządkowej)**, a nie nazw.  
- nazwa została utworzona analogicznie do drugiego, pokrewnego mechanizmu:
  - `loc` → **label location** (lokalizacja po etykiecie)
  - `iloc` → **integer location** (lokalizacja po liczbie całkowitej / indeksie pozycyjnym)

---

### Przykład:
```python
df.loc[5, 'name']    # dostęp po etykiecie (label)
df.iloc[5, 1]        # dostęp po pozycji (integer location)
```

Czyli:
- `loc` – po nazwie wiersza/kolumny,  
- `iloc` – po indeksie liczbowym (położeniu).  

To część spójnej konwencji nazw w pandas — czytelnej i zbliżonej do stylu z R i NumPy.

---

**User:**

Mając data frame df jak w wybranych kolumnach zastąpić nulle pewną wskazaną wartością?

---

**Assistant:**

Aby w **pandas** zastąpić wartości `NaN` (null) w **konkretnych kolumnach** wskazaną wartością, możesz użyć metody `.fillna()` z wyborem kolumn.  

Oto kilka sposobów:

---

### 🔹 1. Jedna wartość dla kilku kolumn
Jeśli chcesz np. w kolumnach `"age"` i `"salary"` zastąpić `NaN` wartością `0`:
```python
df[['age', 'salary']] = df[['age', 'salary']].fillna(0)
```

---

### 🔹 2. Różne wartości dla różnych kolumn
Jeśli dla każdej kolumny ma być inna wartość:
```python
df.fillna({'age': 0, 'salary': 1000, 'city': 'Unknown'}, inplace=True)
```
Metoda `fillna()` przyjmuje słownik: `{kolumna: wartość}` i uzupełnia tylko te kolumny, które są w słowniku.

---

### 🔹 3. Tylko dla jednej kolumny
```python
df['age'] = df['age'].fillna(0)
```

---

### 🔹 4. Jeśli chcesz, aby zmiana nie modyfikowała `df`, a zwracała nową ramkę danych:
```python
new_df = df.fillna({'age': 0, 'salary': 1000})
```

---

📌 **Podsumowanie:**
- `.fillna()` to właściwa metoda do zastępowania braków danych.  
- Można stosować:
  - na pojedynczej kolumnie,
  - na wybranym podzbiorze kolumn,
  - z różnymi wartościami przez słownik.

---

**User:**

base = ['engine_displacement', 'horsepower', 'vehicle_weight',
        'model_year']

X_train = df_train[base].fillna(44).values
ale chcę zrobić fillna tylko dla horsepower a nie dla wszystkich properties

---

**Assistant:**

Możesz to zrobić bardzo prosto — wystarczy wywołać `fillna()` **tylko dla jednej kolumny**, a pozostałe zostawić bez zmian.  
Przykładowo:

```python
base = ['engine_displacement', 'horsepower', 'vehicle_weight', 'model_year']

X_train = df_train[base].copy()
X_train['horsepower'] = X_train['horsepower'].fillna(44)

X_train = X_train.values
```

---

### 💡 Wyjaśnienie:
- `df_train[base]` tworzy podzbiór danych z wybranymi kolumnami.
- `.copy()` jest dobrą praktyką, żeby uniknąć ostrzeżenia `SettingWithCopyWarning`.
- Następnie `fillna(44)` jest stosowane tylko do kolumny `'horsepower'`.
- Na końcu `.values` konwertuje ramkę danych do tablicy NumPy.

---

Alternatywnie, w jednej linijce (mniej czytelne, ale działa):
```python
X_train = df_train[base].assign(horsepower=lambda x: x['horsepower'].fillna(44)).values
```

Oba podejścia są poprawne — pierwsze jest bardziej czytelne i typowe w praktyce.