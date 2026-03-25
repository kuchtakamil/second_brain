# Tagi Mustache

**Data:** 2025-03-17

---

**User:**

W mustache wyrażenie   {{#errorBanners}} to chyba iteracja po elementach kolekcji errorBanners. Popraw mnie jeśli się mylę. Wypisz wszystkie inne możliwe tagi których można używać w mustache

---

**Assistant:**

Masz rację – w Mustache `{{#errorBanners}}` oznacza **początek sekcji**, czyli iterację po kolekcji `errorBanners`, **jeśli jest to tablica/array lub lista elementów**. Każdy element kolekcji zostanie przetworzony przy użyciu zawartości tej sekcji.

### ✅ Co oznaczają poszczególne tagi w Mustache?

Poniżej wypisuję wszystkie podstawowe typy tagów, jakie można używać w Mustache:

---

### 1. `{{name}}` — **Interpolacja (zmienna)**
Wstawia wartość zmiennej `name` w odpowiednie miejsce.

Przykład:
```mustache
Hello, {{userName}}!
```

---

### 2. `{{{name}}}` lub `{{&name}}` — **Nieskładana interpolacja (raw HTML)**
Nieescapowana wersja – wstawia wartość bez HTML escapingu.

```mustache
{{{htmlContent}}}
```
lub
```mustache
{{&htmlContent}}
```

---

### 3. `{{#section}} ... {{/section}}` — **Sekcja warunkowa lub iteracyjna**
- Jeśli `section` to kolekcja → iteruje po elementach.
- Jeśli `section` to obiekt → przetwarza sekcję raz (można używać właściwości obiektu).
- Jeśli `section` to boolean true → przetwarza sekcję.
- Jeśli `section` to funkcja → może działać jako lambda (bardziej zaawansowane przypadki).

Przykład iteracji:
```mustache
{{#items}}
  <li>{{name}}</li>
{{/items}}
```

---

### 4. `{{^section}} ... {{/section}}` — **Sekcja odwrotna (inverted section)**
Wykonywana tylko, gdy `section` jest **false**, `null`, `undefined` lub **pusta kolekcja**.

Przykład:
```mustache
{{^items}}
  <p>No items found.</p>
{{/items}}
```

---

### 5. `{{! comment }}` — **Komentarz**
Komentarze są ignorowane.

```mustache
{{! This is a comment }}
```

---

### 6. `{{> partialName}}` — **Partial (wstawienie innego szablonu)**
Pozwala wstawiać częściowe szablony (partials).

Przykład:
```mustache
{{> header}}
```

---

### 7. `{{= new_open new_close =}}` — **Zmiana znaczników otwierających/zamykających**
Umożliwia zmianę domyślnych znaczników `{{ }}` na inne, np. `[[ ]]`.

Przykład:
```mustache
{{= [[ ]] =}}
Hello [[name]]!
```

---

### 8. **Lambdy (funkcje jako pola kontekstu)** – bardziej zaawansowane:
Możesz przekazać do kontekstu funkcję, która będzie dynamicznie przetwarzać zawartość sekcji. To już bardziej zaawansowany temat, ale Mustache to umożliwia.

---

Jeśli chcesz, mogę dać Ci krótką ściągawkę w formie tabelki albo pokazać przykładowy plik `.mustache` z różnymi tagami. Chcesz?