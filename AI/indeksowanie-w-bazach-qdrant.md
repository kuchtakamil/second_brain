# Indeksowanie w bazach Qdrant

**Data:** 2024-12-17

---

**User:**

W wektorowych bazach danych np. Qdrant czym jest indeksowanie?

---

**Assistant:**

**Indeksowanie** w wektorowych bazach danych, takich jak **Qdrant**, odnosi się do procesu tworzenia struktury umożliwiającej szybkie wyszukiwanie wektorów podobnych do zapytania. 

### **Czym jest indeksowanie w kontekście wektorów?**
W bazach wektorowych operujemy na **wektorach osadzania (embeddingach)** — wielowymiarowych reprezentacjach danych, które przechowują ich cechy (np. tekst, obraz). Wyszukiwanie wektorów polega na znajdowaniu tych, które są **najbardziej podobne** do danego wektora zapytania, na podstawie miary odległości, np.:
- **cosine similarity** (similarity cosinusowa),
- **L2 distance** (odległość euklidesowa),
- **dot product** (iloczyn skalarny).

### **Dlaczego potrzebujemy indeksowania?**
Wyszukiwanie wektorów na dużych zbiorach danych wymaga sprawnej metody przeszukiwania, aby było **szybkie** i **efektywne obliczeniowo**. Pełne przeszukiwanie (ang. **brute-force**) jest czasochłonne i ma złożoność **O(n)**, gdzie *n* to liczba wektorów.

Indeksowanie umożliwia:
- **Ograniczenie przestrzeni przeszukiwania** — wyszukiwanie odbywa się tylko w podzbiorze wektorów,
- **Szybkie odnalezienie przybliżonych wyników** zamiast dokładnego przeszukiwania.

### **Jakie metody indeksowania są stosowane?**
W bazach takich jak Qdrant stosuje się algorytmy **przybliżonego wyszukiwania najbliższych sąsiadów (ANN, Approximate Nearest Neighbor)**. Popularne techniki indeksowania to:

1. **HNSW (Hierarchical Navigable Small World)** — struktura grafowa, w której wektory są połączone w sieć. Pozwala na szybkie przechodzenie między "warstwami" grafu w celu zawężania wyników.
2. **IVF (Inverted File Index)** — podział przestrzeni na klastry (grupy) wektorów i wyszukiwanie tylko w wybranych klastrach.
3. **PQ (Product Quantization)** — technika kwantyzacji zmniejszająca rozmiar danych poprzez podział wektorów na mniejsze segmenty i kompresowanie ich.

### **Jak działa indeksowanie HNSW w Qdrant?**
- **Tworzenie indeksu**: Na podstawie wektorów budowany jest graf wielopoziomowy, w którym wierzchołki (wektory) są ze sobą połączone, tworząc hierarchię.
- **Wyszukiwanie**: Zapytanie rozpoczyna się od "górnej warstwy" grafu, skąd szybko schodzi do niższych poziomów, aby odnaleźć wektory najbardziej zbliżone do zapytania.

### **Podsumowanie**
Indeksowanie w wektorowych bazach danych, takich jak Qdrant, polega na budowaniu struktur, które umożliwiają szybkie, przybliżone wyszukiwanie najbliższych sąsiadów. Dzięki algorytmom takim jak **HNSW** lub **IVF**, wyszukiwanie staje się znacznie szybsze niż przeszukiwanie liniowe, co jest kluczowe dla dużych zbiorów danych.