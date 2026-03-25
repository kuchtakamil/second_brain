# Techniki rekomendacji ML

**Data:** 2025-10-30

---

**User:**

jaka technika / metoda Machine Learning nadaje się do zbudowania własnego prostego systemu rekomendacji np. zakupu perfum?

---

**Assistant:**

Dobre pytanie — wszystko zależy od tego, **jakie masz dane** o użytkownikach i perfumach. Ale poniżej przedstawiam konkretne techniki Machine Learning, które możesz dobrać do rodzaju danych i celu (rekomendacje perfum):  

---

### 🔹 1. **Collaborative Filtering (Filtrowanie kolaboratywne)**
**Najczęściej stosowane podejście** w systemach rekomendacji.

#### ➕ Kiedy stosować:
- Masz dane o tym, **które perfumy użytkownicy oceniali / kupili / polubili**.  
- Nie masz zbyt szczegółowych opisów perfum (tylko relacje użytkownik–produkt).

#### ➕ Przykłady technik:
- **User-based CF:** znajdź użytkowników podobnych do danego użytkownika i poleć produkty, które im się podobały.  
- **Item-based CF:** znajdź produkty podobne do tych, które użytkownik już lubił (często skuteczniejsze).  

#### ➕ Narzędzia:
- `surprise` (Python) – biblioteka do rekomendacji (np. `KNNBasic`, `SVD`).
- `implicit` – do modeli uczenia bez nadzoru (np. ALS – *Alternating Least Squares*).

---

### 🔹 2. **Content-Based Filtering (Rekomendacje oparte na cechach produktu)**
Polecane, jeśli **masz opisy perfum**: nuty zapachowe, rodzaj, marka, intensywność, kategoria (np. kwiatowe, drzewne, cytrusowe).

#### ➕ Jak działa:
- Budujesz **wektory cech** dla każdego produktu.
- Użytkownik ma swój „profil zapachowy” (średnia wektorów perfum, które lubi).
- Rekomendacje to perfumy **podobne w przestrzeni cech**.

#### ➕ Przykładowe techniki:
- TF-IDF + **cosine similarity** (dla opisów tekstowych).
- Embeddingi (np. z modelu Sentence-BERT) dla opisów perfum.

---

### 🔹 3. **Hybrid Approach (Podejście hybrydowe)**
Łączy oba podejścia powyżej – typowe w komercyjnych systemach.

#### ➕ Przykład:
- Jeśli użytkownik jest nowy → użyj **content-based**.  
- Jeśli ma historię zakupów → użyj **collaborative filtering**.  
- Wyniki można łączyć np. przez uśrednienie lub ważenie wyników.

---

### 🔹 4. **Clustering (np. K-Means)**
Dobre dla **prostej wersji systemu rekomendacji**, gdy nie masz danych o użytkownikach.

#### ➕ Jak działa:
- Grupujesz perfumy na podstawie ich cech (np. nut zapachowych, producenta, typu).
- Użytkownik wybiera jedne perfumy → pokazujesz inne z tego samego klastra.

---

### 🔹 5. **Deep Learning (bardziej zaawansowane podejście)**
Dla ciekawości – w komercyjnych systemach (Netflix, Amazon):
- **Autoencodery** do uczenia reprezentacji użytkowników i produktów.  
- **Neural Collaborative Filtering (NCF)** – modeluje interakcje użytkownik–produkt nieliniowo.

---

### 🔸 Dla prostego systemu perfum:
Jeśli chcesz **coś prostego, działającego lokalnie**:
1. Zbierz dane o perfumach (nuty, kategorie, opis).  
2. Zrób wektory TF-IDF opisów lub zakoduj cechy ręcznie.  
3. Licz **cosine similarity** i polecaj najbliższe produkty.  

Przykład w Pythonie (prosty content-based):

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

# dane
data = pd.DataFrame({
    "name": ["Dior Sauvage", "Chanel Bleu", "Versace Eros"],
    "notes": ["bergamot ambroxan pepper", "grapefruit incense cedar", "mint vanilla tonka bean"]
})

# wektory TF-IDF
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(data["notes"])

# podobieństwa
similarity = cosine_similarity(X)

# rekomendacje dla Dior Sauvage
idx = 0
similar_items = similarity[idx].argsort()[::-1][1:]
print(data.iloc[similar_items])
```

---

Jeśli powiesz mi, **jakie dane masz dostępne (np. tylko opisy, czy też oceny użytkowników)** — mogę zaproponować dokładną architekturę i model.  
Czy chcesz, żebym pokazał przykład małego systemu rekomendacji perfum w Pythonie (np. w Jupyter / konsolowy)?