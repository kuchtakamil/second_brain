# Odpowiedniki funkcji Java w Pythonie

**Data:** 2026-02-09

---

**User:**

W Java bardzo często stosuje się funkcje map, filter, group. Czy Python ma takie odpowiedniki?

---

**Assistant:**

Tak — i co ważne: **Python ma je w jeszcze bardziej naturalnej i czytelnej formie niż Java Streams**.

W Javie potrzebujesz Stream API, lambd, kolektorów itd.  
W Pythonie te same operacje są **wbudowanym idiomem języka**.

Odpowiedniki:

| Java Stream                     | Python idiom (najczęstszy)                  |
|---------------------------------|---------------------------------------------|
| `map()`                         | list comprehension                          |
| `filter()`                      | list comprehension                          |
| `collect(groupingBy())`        | `dict` + `defaultdict` / `itertools.groupby` |
| `collect(toList())`            | lista z comprehension                       |
| `collect(toSet())`             | set comprehension                           |
| `flatMap()`                     | nested list comprehension                   |

---

## 1. `map`

### Java
```java
List<String> names = users.stream()
    .map(User::getName)
    .collect(Collectors.toList());
```

### Python (idiomatycznie)
```python
names = [user.name for user in users]
```

Możesz użyć też `map`, ale **w Pythonie prawie się tego nie robi**:

```python
names = list(map(lambda u: u.name, users))  # mniej czytelne
```

---

## 2. `filter`

### Java
```java
List<User> adults = users.stream()
    .filter(u -> u.getAge() > 18)
    .collect(Collectors.toList());
```

### Python
```python
adults = [u for u in users if u.age > 18]
```

Znowu: czytelniejsze niż Java.

---

## 3. `map + filter` razem

### Java
```java
List<String> names = users.stream()
    .filter(u -> u.getAge() > 18)
    .map(User::getName)
    .collect(Collectors.toList());
```

### Python
```python
names = [u.name for u in users if u.age > 18]
```

Jedna linijka. Zero ceremonii.

---

## 4. `groupingBy` (najczęstszy brakujący element dla Javowców)

### Java
```java
Map<Role, List<User>> byRole =
    users.stream().collect(Collectors.groupingBy(User::getRole));
```

### Python — najczęściej
```python
from collections import defaultdict

by_role = defaultdict(list)
for u in users:
    by_role[u.role].append(u)
```

To jest **standardowy idiom Pythona**.

Alternatywa (gdy lista jest posortowana):

```python
from itertools import groupby

users.sort(key=lambda u: u.role)
by_role = {
    role: list(group)
    for role, group in groupby(users, key=lambda u: u.role)
}
```

---

## 5. `toSet`

### Java
```java
Set<String> roles = users.stream()
    .map(User::getRole)
    .collect(Collectors.toSet());
```

### Python
```python
roles = {u.role for u in users}
```

---

## 6. `flatMap`

### Java
```java
List<Order> orders = users.stream()
    .flatMap(u -> u.getOrders().stream())
    .collect(Collectors.toList());
```

### Python
```python
orders = [order for u in users for order in u.orders]
```

---

## 7. Jeszcze ważniejsze: Python robi to **leniwe** (jak Stream)

Jeśli chcesz zachowanie jak Stream (lazy):

```python
names = (u.name for u in users if u.age > 18)
```

To jest **generator expression** — odpowiednik Java Stream bez collect.

---

## Kluczowa różnica mentalna (bardzo ważne dla Javowca)

W Javie myślisz:
> "muszę zrobić stream i użyć map/filter"

W Pythonie myślisz:
> "tworzę nową listę z tej listy"

To jest fundamentalna różnica stylu.

---

## TL;DR dla Ciebie jako Javowca

Najważniejszy idiom do zapamiętania:

```python
[result_expression for item in collection if condition]
```

To zastępuje 80% użycia Stream API z Javy.

I jest:
- krótsze
- czytelniejsze
- idiomatyczne
- szybsze w pisaniu
- standardowe w Pythonie

Dlatego doświadczeni Pythonowcy prawie **nie używają** `map()` i `filter()`.