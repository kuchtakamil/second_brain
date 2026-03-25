# RequireJS i ładowanie skryptów

**Data:** 2025-03-19

---

**User:**

Mam stronę z <head> w którym mam dodane wiele tagów <script>.
W takim przypadku po wyświetleniu strony widzę w DevTools że wszystkie pliki js z tagów <script> są dostępne.
Jednak gdy w body dodam
<script type="text/javascript" charset="utf-8" async="" data-requirecontext="_" data-requiremodule="widgets/MyNewJs" src="/src/js/MyNewJs.js"></script>
wtedy w DevTools widzę że dostępny jest tylko MyNewJs.js a pliki js z <head> już nie.

---

**Assistant:**

Dzięki za dokładny opis — to, co opisujesz, bardzo prawdopodobnie wynika ze sposobu działania **RequireJS** albo podobnego **loadera modułów AMD**, ponieważ w Twoim tagu `<script>` są atrybuty `data-requirecontext` i `data-requiremodule`, które są charakterystyczne właśnie dla RequireJS.

### Co się prawdopodobnie dzieje:

1. **RequireJS** tworzy swój własny kontekst ładowania modułów, który izoluje je od wcześniej załadowanych skryptów, chyba że wcześniej zadeklarowane skrypty również zostały załadowane przez RequireJS.
2. Jeśli skrypty w `<head>` zostały załadowane klasycznie (po prostu `<script src="..."></script>`), a potem **RequireJS** zaczyna ładować swój własny kontekst (`data-requirecontext="_"`), to mogą nie być widoczne (w kontekście RequireJS).
3. W DevTools może się wydawać, że są „niedostępne”, ale w rzeczywistości **są dostępne w globalnym kontekście przeglądarki**, tylko nie są „widoczne” z poziomu RequireJS (jeśli go używasz).

---

### Jak to naprawić lub obejść — zależnie od tego, czego potrzebujesz:

#### 🔸 Opcja 1: Jeśli **nie używasz RequireJS świadomie**, usuń `data-requirecontext` i `data-requiremodule`:
```html
<script src="/src/js/MyNewJs.js" type="text/javascript" charset="utf-8" async=""></script>
```
Wtedy `MyNewJs.js` po prostu załaduje się klasycznie jak pozostałe skrypty w `<head>`.

#### 🔸 Opcja 2: Jeśli **używasz RequireJS i chcesz wszystko ładować w jego kontekście**, to najlepiej całą aplikację ładować przez RequireJS — również te skrypty z `<head>`.

Przykład:
```html
<script data-main="/src/js/main" src="/src/js/require.js"></script>
```

A w `/src/js/main.js`:
```js
require.config({
    paths: {
        jquery: 'libs/jquery',
        someLib: 'libs/someLib',
        myNewJs: 'widgets/MyNewJs'
    }
});

require(['jquery', 'someLib', 'myNewJs'], function ($, someLib, myNewJs) {
    // kod inicjalizujący
});
```

Wtedy wszystkie moduły są ładowane przez RequireJS, a nie ręcznie przez `<script>`.

---

### ✳️ Dodatkowe wyjaśnienie:
- Atrybuty `data-requirecontext` i `data-requiremodule` są zwykle dodawane przez **RequireJS automatycznie**, kiedy generuje `<script>` dynamicznie.
- Jeśli wrzucisz `<script>` z tymi atrybutami ręcznie, może to zaburzyć działanie loadera.

---

Chcesz, żebym pomógł Ci przekształcić całą stronę w taki sposób, żeby skrypty były ładowane jednolicie przez RequireJS (albo odwrotnie — całkowicie bez RequireJS)? Jeśli dasz kawałek kodu HTML z `<head>` i `body`, mogę podpowiedzieć konkretniej.