# Dynamic JS Loading RequireJS

**Data:** 2025-03-20

---

**User:**

Mam aplikację webową której kod jest mi dostępny. Przeglądam kod w tagu <head> i nie widzę tam żadnych tagów <script> które włączałyby jakieś pliki js.
Jednak w uruchomionej aplikacji, w narzędziu DevTools od chrome na końcu sekcji head widzę wiele tagów <script> np.
<script type="text/javascript" charset="utf-8" async="" data-requirecontext="_" data-requiremodule="widgets/MyItem" src="/v2/src/js/widgets/MyItem.js"></script>
Skąd się one tam wzięły?

---

**Assistant:**

Świetne pytanie — wygląda na to, że Twoja aplikacja korzysta z **dynamicznego ładowania skryptów JavaScript**, najprawdopodobniej przez **RequireJS** (lub podobny **modułowy loader JS**).

Wskazuje na to m.in. ten fragment tagu `<script>`:

```html
data-requirecontext="_" data-requiremodule="widgets/MyItem"
```

To **cecha charakterystyczna RequireJS**, który dynamicznie ładuje moduły JavaScript zgodnie z ich zależnościami, a następnie wstawia je jako `<script src="...">` do DOM-u.

---

### 📌 Skąd się biorą te `<script>` w `<head>` mimo że ich nie ma w HTML?

1. W kodzie aplikacji (prawdopodobnie gdzieś w `index.html` lub głównym pliku HTML), jest załadowany tylko jeden podstawowy plik JS, np.:

   ```html
   <script data-main="main" src="require.js"></script>
   ```

   - `require.js` to loader.
   - `data-main="main"` oznacza, że loader ma załadować plik `main.js` jako pierwszy moduł.

2. Następnie `main.js` zawiera coś w stylu:

   ```js
   require(["widgets/MyItem", "inny/moduł", ...], function(MyItem, InnyModul, ...) {
       // kod uruchamiający aplikację
   });
   ```

3. W odpowiedzi na to `require.js` dynamicznie tworzy `<script src="/v2/src/js/widgets/MyItem.js">` i dodaje go do `<head>` w przeglądarce — właśnie to widzisz w DevTools.

---

### 🔍 Jak to potwierdzić?

- Poszukaj w kodzie **`require.js` lub `define()` / `require()`** — to będzie jednoznaczna wskazówka.
- Sprawdź w `index.html` czy jest `data-main`, albo zobacz w konsoli DevTools jaka jest kolejność ładowania skryptów.
- W narzędziach DevTools możesz też znaleźć, który kod wywołał `require("widgets/MyItem")`.

---

### 🧠 Dodatkowe uwagi

- RequireJS był bardzo popularny przed czasami Webpacka, ES6 modules i bundlerów.
- Jeśli to starsza aplikacja (albo jakiś system enterprise), to nadal może intensywnie go używać.

---

Chcesz, żebym pomógł Ci zidentyfikować dokładnie miejsce w kodzie, które inicjuje ten `require("widgets/MyItem")`? Możesz wkleić fragment HTML lub JS, to spojrzę.