# Podział danych na 3 części

**Data:** 2025-10-28

---

**User:**

W Machine Learning np. w zastosowaniu regresji zdarza się, że zbiór danych jest dzielony na 3 a nie 2 części. Wyszczególniana jest część treningowa (60%), walidacyjna (20%) i testowa (20%). Właśnie ta część walidacyjna jest nie zawsze obecna. Wyjaśnij kiedy i po co tak się robi i czy to dobry pomysł dzielić zbiór danych na 3 a nie na 2 części.

---

**Assistant:**

To bardzo dobre pytanie — rzeczywiście, w praktyce Machine Learning dane mogą być dzielone na **dwie** lub **trzy** części, i to zależy od konkretnego celu i sposobu trenowania modelu.  

---

### 🔹 Podział na 2 części: **train / test**
Najprostszy scenariusz:

- **train set (np. 80%)** – dane do trenowania modelu,  
- **test set (np. 20%)** – dane do końcowej oceny jakości modelu.

Ten podział wystarcza wtedy, gdy:
- model **nie wymaga strojenia hiperparametrów** (np. prosta regresja liniowa bez regularyzacji),
- albo do walidacji używa się **cross-validation** (walidacji krzyżowej), która pełni rolę „walidacyjnej” części, ale nie wymaga osobnego zbioru walidacyjnego.

W takim przypadku **test set jest używany tylko raz** – na samym końcu, po wybraniu najlepszego modelu, aby oszacować jego rzeczywistą skuteczność.

---

### 🔹 Podział na 3 części: **train / validation / test**
Podział na trzy części jest używany, gdy:
- model ma **hiperparametry**, które trzeba dostroić (np. regularization strength w regresji Lasso, liczba drzew w Random Forest),
- nie chcemy, aby dane testowe „wpływały” na proces wyboru modelu (czyli aby nie doszło do tzw. *data leakage*).

Wtedy:
- **train set (np. 60%)** – do uczenia modelu,  
- **validation set (np. 20%)** – do oceny modelu podczas strojenia hiperparametrów,  
- **test set (np. 20%)** – do ostatecznej, niezależnej oceny jakości po zakończeniu całego procesu.

To pozwala uniknąć sytuacji, w której nieświadomie „dopasowujesz się” do danych testowych podczas eksperymentów.

---

### 🔹 Kiedy **lepiej 3 zbiory**
- gdy danych jest **dużo**, więc możesz „poświęcić” część na walidację bez utraty jakości uczenia,  
- gdy używasz **modeli z dużą liczbą hiperparametrów** lub korzystasz z **automatycznego tuningu** (np. grid search, Bayesian optimization),  
- gdy chcesz mieć **niezależny test końcowy**, który nie był w żaden sposób użyty przy doborze hiperparametrów ani przy trenowaniu.

---

### 🔹 Kiedy **wystarczą 2 zbiory**
- gdy danych jest **mało** – wtedy lepiej zastosować **cross-validation** zamiast wydzielać osobny validation set,  
- gdy model jest prosty lub hiperparametry nie mają dużego wpływu,  
- gdy używasz technik takich jak **k-fold cross-validation**, gdzie dane treningowe są wielokrotnie dzielone na części treningowe i walidacyjne.

---

### 🔹 Podsumowanie

| Podejście | Kiedy stosować | Zalety | Wady |
|------------|----------------|--------|------|
| **2 zbiory (train/test)** | Mało danych lub proste modele | Więcej danych do trenowania | Ryzyko dopasowania do testu podczas tuningu |
| **3 zbiory (train/val/test)** | Dużo danych, tuning hiperparametrów | Czysta ocena na niezależnym teście | Mniej danych do trenowania |

---

**Wniosek:**  
Podział na 3 zbiory jest **dobrym pomysłem**, jeśli dane są wystarczająco liczne i planujesz **strojenie hiperparametrów**.  
Jeśli danych jest mało, to lepiej użyć **cross-validation** zamiast osobnego zbioru walidacyjnego — wtedy uzyskasz lepsze oszacowanie jakości modelu bez marnowania danych.

---

**User:**

czym są hiperparametry?

---

**Assistant:**

**Hiperparametry** to takie parametry modelu uczenia maszynowego, które **nie są uczone automatycznie** z danych, tylko **musisz je ustawić sam (ręcznie lub przez procedurę strojenia)** przed rozpoczęciem treningu.  

Inaczej mówiąc — to ustawienia **sterujące sposobem, w jaki model się uczy**, a nie wartości, które model sam dopasowuje.

---

### 🔹 Przykład: regresja liniowa
Model regresji liniowej ma parametry \( w_0, w_1, ..., w_n \) — to **parametry modelu**, które są wyliczane automatycznie tak, żeby zminimalizować błąd na danych treningowych.

Ale jeśli użyjesz **regularyzacji**, np. Lasso (L1) albo Ridge (L2), pojawia się współczynnik regularyzacji **λ (lambda)**:
- **λ** określa, jak silnie karzemy duże wartości wag.  
To już **hiperparametr**, bo **musisz go ustawić ręcznie** (lub dobrać za pomocą walidacji).

---

### 🔹 Przykład: las losowy (Random Forest)
Hiperparametry to m.in.:
- liczba drzew (`n_estimators`),
- maksymalna głębokość drzewa (`max_depth`),
- minimalna liczba próbek w liściu (`min_samples_leaf`).

Każdy z tych parametrów wpływa na **złożoność modelu** i **ryzyko przeuczenia** (overfittingu), ale nie jest uczony z danych — model musi wiedzieć to **z góry**, zanim zacznie się uczyć.

---

### 🔹 Przykład: sieci neuronowe
Hiperparametry to m.in.:
- liczba warstw i neuronów w każdej warstwie,  
- współczynnik uczenia (**learning rate**),  
- rozmiar batcha (ang. *batch size*),  
- liczba epok (ile razy model przejdzie przez dane),  
- rodzaj optymalizatora (np. Adam, SGD).

---

### 🔹 Jak dobiera się hiperparametry
Nie ma jednej poprawnej wartości — dlatego zwykle:
- dobiera się je **eksperymentalnie**,  
- lub automatycznie za pomocą:
  - **grid search** (pełne przeszukiwanie siatki wartości),
  - **random search** (losowanie kombinacji),
  - **Bayesian optimization**,  
  - **Hyperband** / **Optuna** (bardziej zaawansowane metody).

Do tego potrzebny jest **zbiór walidacyjny** — na nim sprawdzasz, które ustawienia hiperparametrów dają najlepsze wyniki.

---

### 🔹 Podsumowanie
| Typ parametru | Kto go ustawia | Przykład | Celem jest |
|----------------|----------------|-----------|-------------|
| **Parametr modelu** | Uczy się sam | wagi w regresji, współczynniki w neuronach | dopasowanie do danych |
| **Hiperparametr** | Ustawiasz Ty (lub tuner) | learning rate, liczba drzew, λ w Ridge | sterowanie procesem uczenia |

---

Chcesz, żebym pokazał konkretny przykład w Pythonie (np. jak hiperparametry wpływają na wynik modelu)?