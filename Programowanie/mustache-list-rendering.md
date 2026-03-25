# Mustache List Rendering

**Data:** 2024-12-14

---

**User:**

Mam stronę w mustache zasilaną modelem ze Spring MVC. Czy gdy pod tag np. {{additionalData}} podstawię w java obiekt  List.of("some data1", "next sentense", "tbd") to jak to się wyświetli na stronie?

---

**Assistant:**

Jeśli pod tag `{{additionalData}}` w Mustache podstawisz obiekt Java typu `List`, na stronie zobaczysz **wartość `toString()` tej listy**, ponieważ Mustache nie "wie", jak interpretować listy ani jak je iterować bez odpowiednich instrukcji.

W przypadku przykładu:

```java
model.addAttribute("additionalData", List.of("some data1", "next sentence", "tbd"));
```

Tag `{{additionalData}}` w szablonie Mustache wyświetli coś w rodzaju:

```
[some data1, next sentence, tbd]
```

### Jak poprawnie wyświetlić elementy listy?
Jeśli chcesz wyświetlić każdy element listy w oddzielnej linii (lub w innym formacie), musisz użyć iteracji w Mustache. W tym celu używasz sekcji (`{{#each}}` lub podobnej składni, np. `{{#additionalData}}`).

Przykład szablonu Mustache:

```mustache
<ul>
  {{#additionalData}}
  <li>{{.}}</li>
  {{/additionalData}}
</ul>
```

Wynik na stronie będzie wyglądał tak:

```html
<ul>
  <li>some data1</li>
  <li>next sentence</li>
  <li>tbd</li>
</ul>
```

### Wyjaśnienie:
1. `{{#additionalData}}` - oznacza początek sekcji, która iteruje po elementach listy.
2. `{{.}}` - odnosi się do bieżącego elementu w iteracji.
3. `{{/additionalData}}` - zamyka sekcję.

Jeśli lista jest pusta, sekcja `{{#additionalData}}` nie wyświetli nic (co jest standardowym zachowaniem w Mustache). Możesz dodać blok `{{^additionalData}}` (sekcja negatywna), aby wyświetlić komunikat dla pustych list:

```mustache
{{^additionalData}}
<p>Brak danych do wyświetlenia.</p>
{{/additionalData}}
```

---

**User:**

a gdybym miał 
model.addAttribute("additionalData", List.of("some data1"));
i chciał to po prostu wyświetlić jak some data1

---

**Assistant:**

Jeśli chcesz po prostu wyświetlić pojedynczy element z listy (np. "some data1"), musisz upewnić się, że **model przekazuje bezpośrednio wartość tekstową**, a nie listę. 

### 1. Rozwiązanie w Java: przekazanie pierwszego elementu listy
Możesz pobrać pierwszy element z listy i przekazać go jako wartość do modelu:

```java
List<String> dataList = List.of("some data1");
model.addAttribute("additionalData", dataList.isEmpty() ? null : dataList.get(0));
```

W szablonie Mustache możesz wtedy użyć:

```mustache
{{additionalData}}
```

A na stronie pojawi się:

```
some data1
```

---

### 2. Alternatywa: modyfikacja w Mustache (jeśli koniecznie chcesz zostawić listę)
Jeśli z jakiegoś powodu musisz przekazać całą listę do modelu, ale na stronie wyświetlać tylko pierwszy element, możesz wykorzystać iterację w Mustache i wyświetlić tylko pierwszy element listy. 

```mustache
{{#additionalData}}
{{.}}
{{/additionalData}}
```

Mustache iteruje po liście i wyświetla pierwszy element (o ile lista nie jest pusta).

---

### 3. Podejście minimalistyczne (przekazanie wartości jako String)
Jeśli chcesz uprościć logikę, możesz od razu przekazać wartość jako string w modelu:

```java
model.addAttribute("additionalData", "some data1");
```

I w szablonie Mustache:

```mustache
{{additionalData}}
```

To zdecydowanie najprostsze rozwiązanie, jeśli zawsze potrzebujesz tylko jednego elementu.