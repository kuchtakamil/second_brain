# Regex błędna składnia

**Data:** 2025-07-20

---

**User:**

co robi taki regex [[az]]+

---

**Assistant:**

Wyrażenie regularne `[[az]]+` wygląda na błędne lub przynajmniej nieintencjonalne, ale rozłóżmy je dokładnie, by wyjaśnić, co robi:

1. `[` — początek klasy znaków (ang. *character class*)
2. `[az]` — klasa znaków zawierająca dwa znaki: `a` i `z`
3. `]` — koniec klasy znaków
4. `+` — oznacza "jeden lub więcej wystąpień"

Czyli tak naprawdę parser regexa interpretuje to jako:

```
[[az]]+  ≡  [\[az\]]+
```

Co oznacza: **jeden lub więcej znaków należących do zbioru `[\`, `a`, `z`, `]`**.

### Podsumowanie
Regex `[[az]]+` **dopasowuje ciągi zbudowane z dowolnej liczby znaków `a`, `z`, `[` lub `]`**.

Jeśli chcesz dopasować wszystkie małe litery od `a` do `z`, poprawna składnia to:

```
[a-z]+
```

Jeśli potrzebujesz innej analizy – daj znać.