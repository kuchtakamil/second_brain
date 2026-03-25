# KQL zapytanie błędne

**Data:** 2025-04-15

---

**User:**

co jest nie tak w zapytaniu do kibana
"62af6a36d" AND SEVERITY: ERROR

---

**Assistant:**

Twoje zapytanie do Kibany:

```
"62af6a36d" AND SEVERITY: ERROR
```

jest **bliskie poprawności**, ale może nie działać prawidłowo w zależności od kilku czynników:

---

### ✅ Sprawdź, co może być nie tak:

#### 1. **Składnia zapytania Kibana Query Language (KQL)**

KQL **nie używa** operatora `AND` w ten sposób między frazami. Powinno to wyglądać tak:

```kql
"62af6a36d" and SEVERITY : "ERROR"
```

Zwróć uwagę na:
- małe litery `and`
- cudzysłów wokół wartości `ERROR`

---

#### 2. **Czy pole `SEVERITY` istnieje i jest indeksowane jako keyword/tekstowe?**
- Możliwe, że pole nazywa się inaczej (np. `severity`, `log.level`, `level`, etc.)
- Upewnij się, że masz dokładną nazwę pola (możesz to sprawdzić w "Discover" lub "Index Pattern")

---

#### 3. **Czy `"62af6a36d"` występuje jako część większego pola?**
Jeśli ten ciąg znaków to np. fragment `message`, zapytanie szuka jego wystąpienia w dowolnym polu. Jeśli chcesz go ograniczyć do konkretnego pola, np.:

```kql
message : "62af6a36d" and SEVERITY : "ERROR"
```

---

### ✅ Przykład poprawnego zapytania:

```kql
message : "62af6a36d" and SEVERITY : "ERROR"
```

albo ogólne:

```kql
"62af6a36d" and SEVERITY : "ERROR"
```

---

Jeśli nadal nie działa — daj znać, co dokładnie zwraca Kibana (np. błąd składni, brak wyników), to spróbuję pomóc dokładniej.