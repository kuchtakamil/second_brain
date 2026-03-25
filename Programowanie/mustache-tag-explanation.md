# Mustache tag explanation

**Data:** 2024-12-02

---

**User:**

czasami w plikach .mustache widzę w tagach znaki #, ^, / a czasem są tagi bez takich znaków
jaki sens ma taka linia
{{#validationMessage}}{{{validationMessage}}}{{/validationMessage}}

---

**Assistant:**

Linia `{{#validationMessage}}{{{validationMessage}}}{{/validationMessage}}` w szablonie Mustache wykorzystuje te specjalne symbole do warunkowego renderowania zawartości. Wyjaśnijmy ich znaczenie:

1. **`{{#...}}`**: Otwiera "blok warunkowy". Oznacza, że zawartość w tym bloku zostanie wyrenderowana tylko wtedy, gdy wartość klucza `validationMessage` jest:
   - Prawdziwa (truthy) w sensie logiki JavaScript, tj. różna od `null`, `undefined`, pustego ciągu znaków, liczby `0`, `false` itd.
   - Jeśli `validationMessage` jest tablicą, blok zostanie powtórzony dla każdego elementu tej tablicy.

2. **`{{{...}}}`**: To tak zwane "potrójne nawiasy". Powodują, że zawartość klucza `validationMessage` zostanie wyrenderowana **bez uciekania HTML**. Oznacza to, że potencjalne znaczniki HTML w wartości zostaną wyrenderowane jako część strony, a nie potraktowane jako zwykły tekst.

3. **`{{/...}}`**: Zamknięcie bloku otwartego przez `{{#...}}`.

### Sens tej linii
Linia oznacza:
- Jeśli `validationMessage` istnieje i jest prawdziwe, to zawartość zostanie wyrenderowana.
- Wartość `validationMessage` zostanie wyrenderowana "surowo", bez ucieczki HTML.
- Jeśli `validationMessage` jest puste lub nie istnieje, całość (łącznie z otaczającymi nawiasami) zostanie pominięta.

### Przykład w praktyce
Załóżmy, że `validationMessage` zawiera:

#### Przykład 1: `validationMessage = "<b>Invalid input</b>"`
Rezultat:
```html
<b>Invalid input</b>
```

#### Przykład 2: `validationMessage = ""`
Rezultat: (nic się nie pojawia, blok jest pomijany).

#### Przykład 3: `validationMessage` nie istnieje
Rezultat: (również nic).

Taka konstrukcja jest często używana w celu wyświetlania komunikatów o błędach, które mogą być dynamicznie ustawiane w zależności od logiki w aplikacji.

---

**User:**

Mój mustache renderuje plik w którym jest kilka znaczników div jeden po drugim. W nich są inputy z typem radio button.
<div class="radio"> <input type=checkbox..../>
<div class="radio"> <input type=checkbox..../>
<div class="radio"> <input type=checkbox..../>
<div class="radio"> <input type=checkbox..../>

mustache w uproszczeniu wygląda tak
{{#mygroup}}
<div class="radio"> <input type=checkbox..../>
{{/groupedOptions}}
Chciałbym uzyskać efekt że po pierwszym divie będzie wstawiony jakiś inny div z inną klasą. Dodatkowo, a nie zamiast.

<div class="radio"> <input type=checkbox..../>
<div class="my-indent">.....</div>
<div class="radio"> <input type=checkbox..../>
<div class="radio"> <input type=checkbox..../>
<div class="radio"> <input type=checkbox..../>

---

**Assistant:**

Aby uzyskać efekt, w którym po pierwszym `<div class="radio">` wstawiasz dodatkowy `<div class="my-indent">...</div>`, możesz wykorzystać funkcję Mustache w połączeniu z logiką w danych wejściowych. Ponieważ Mustache nie obsługuje bezpośrednio numerowania iteracji w pętli, musisz przygotować dane w sposób, który umożliwi rozpoznanie pierwszego elementu.

### Rozwiązanie
W danych wejściowych dodaj pole wskazujące, że dany element jest "pierwszy".

#### Przykład danych wejściowych:
```json
{
  "groupedOptions": [
    { "isFirst": true, "value": "Option 1" },
    { "isFirst": false, "value": "Option 2" },
    { "isFirst": false, "value": "Option 3" },
    { "isFirst": false, "value": "Option 4" }
  ]
}
```

#### Zaktualizowany szablon Mustache:
```html
{{#groupedOptions}}
  <div class="radio">
    <input type="checkbox" value="{{value}}">
  </div>
  {{#isFirst}}
  <div class="my-indent">...</div>
  {{/isFirst}}
{{/groupedOptions}}
```

### Jak to działa?
1. Każdy element w `groupedOptions` generuje `<div class="radio">`.
2. Dodatkowo, dla pierwszego elementu (`isFirst: true`), zostaje wyrenderowany `<div class="my-indent">...</div>`.

#### Wynik renderowania:
Dla powyższych danych wynikowy HTML będzie wyglądał tak:
```html
<div class="radio">
  <input type="checkbox" value="Option 1">
</div>
<div class="my-indent">...</div>
<div class="radio">
  <input type="checkbox" value="Option 2">
</div>
<div class="radio">
  <input type="checkbox" value="Option 3">
</div>
<div class="radio">
  <input type="checkbox" value="Option 4">
</div>
```

### Alternatywa z preprocesowaniem danych
Jeśli nie możesz modyfikować danych wejściowych, możesz wstawić logikę, która podczas generowania danych na backendzie oznaczy pierwszy element np. za pomocą jakiejś funkcji przetwarzającej. W Mustache samodzielnie nie możesz używać skomplikowanej logiki iteracyjnej.

---

**User:**

ok, a czy możliwe jest to aby mustache wstrzykiwał iinny kod html
<div class="my-indent">
{{ myIndentContent }}
</div>
Chciałbym aby myIndentContent był htmlem który przekażę gdzieś indziej... 

---

**Assistant:**

Tak, jest to możliwe w Mustache, ale wymaga zastosowania potrójnych nawiasów `{{{` i `}}}` zamiast standardowych `{{` i `}}}`, ponieważ standardowe nawiasy automatycznie "uciekają" (escape) HTML, co powoduje, że znaki HTML są traktowane jako zwykły tekst.

### Jak to zrobić?

#### Przykład danych wejściowych:
```json
{
  "mygroup": [
    { "value": "Option 1", "myIndentContent": "<strong>Important Info</strong>" },
    { "value": "Option 2", "myIndentContent": "<em>Additional Detail</em>" }
  ]
}
```

#### Szablon Mustache:
```html
{{#mygroup}}
<div class="radio">
  <input type="checkbox" value="{{value}}">
</div>
<div class="my-indent">
  {{{myIndentContent}}}
</div>
{{/mygroup}}
```

### Wyjaśnienie:
1. **`{{{myIndentContent}}}`**: Użycie potrójnych nawiasów pozwala wstrzyknąć zawartość pola `myIndentContent` jako surowy HTML. To oznacza, że np. `<strong>` czy `<em>` zostaną wyrenderowane jako znaczniki HTML na stronie.
2. **`{{value}}`**: Tutaj używamy standardowych nawiasów, ponieważ chcemy, aby zawartość była bezpieczna i ewentualne znaki HTML zostały "ucieczone".

#### Wynikowy HTML:
Dla powyższych danych Mustache wygeneruje następujący kod:
```html
<div class="radio">
  <input type="checkbox" value="Option 1">
</div>
<div class="my-indent">
  <strong>Important Info</strong>
</div>
<div class="radio">
  <input type="checkbox" value="Option 2">
</div>
<div class="my-indent">
  <em>Additional Detail</em>
</div>
```

### Bezpieczeństwo
Jeśli `myIndentContent` pochodzi z zewnętrznych źródeł, pamiętaj, że użycie potrójnych nawiasów może wprowadzić ryzyko związane z wstrzykiwaniem kodu (XSS). W takich przypadkach upewnij się, że:
- Zawartość `myIndentContent` jest odpowiednio walidowana i oczyszczana przed wstrzyknięciem.
- Alternatywnie, jeśli HTML jest opcjonalny, używaj standardowych nawiasów (`{{}}`), aby uniknąć takich ryzyk.

---

**User:**

Jaki byłby dobry sposób na dostarczenie htmla do myIndentContent? Chcę czegoś lepszego niż trzymanie html w stringu

---

**Assistant:**

Trzymanie HTML-a jako ciągu znaków w danych nie jest idealne, ponieważ jest trudne do zarządzania, utrzymania i testowania. Oto kilka lepszych sposobów dostarczania HTML-a do `myIndentContent`:

---

### 1. **Użycie szablonów częściowych (partials)**
Mustache obsługuje mechanizm **partials**, który pozwala na wstawianie zewnętrznych fragmentów HTML-a do głównego szablonu.

#### Struktura projektu:
- Plik główny szablonu (`main.mustache`):
  ```html
  {{#mygroup}}
  <div class="radio">
    <input type="checkbox" value="{{value}}">
  </div>
  {{> myIndentContent }}
  {{/mygroup}}
  ```
- Plik częściowy (`myIndentContent.mustache`):
  ```html
  <div class="my-indent">
    <strong>Dynamic content for {{value}}</strong>
  </div>
  ```

#### Dane wejściowe:
```json
{
  "mygroup": [
    { "value": "Option 1" },
    { "value": "Option 2" }
  ]
}
```

#### Wynik:
Mustache wstawi zawartość pliku `myIndentContent.mustache` dla każdej iteracji. Dzięki temu HTML jest zarządzany w osobnym pliku, co ułatwia jego edycję i testowanie.

---

### 2. **Generowanie zawartości po stronie backendu**
Zamiast przechowywać HTML w danych, możesz generować go po stronie backendu, a następnie przekazywać jako pole w danych.

#### Backend (przykład w Kotlinie z Spring Boot):
```kotlin
data class Option(val value: String, val myIndentContent: String)

fun generateOptions(): List<Option> {
    return listOf(
        Option("Option 1", renderHtmlForIndent("Option 1")),
        Option("Option 2", renderHtmlForIndent("Option 2"))
    )
}

fun renderHtmlForIndent(option: String): String {
    return "<div class='my-indent'><strong>Details for $option</strong></div>"
}
```

#### Szablon Mustache:
```html
{{#mygroup}}
<div class="radio">
  <input type="checkbox" value="{{value}}">
</div>
{{{myIndentContent}}}
{{/mygroup}}
```

#### Wynik:
Backend generuje odpowiedni HTML, co daje większą kontrolę nad treścią i umożliwia użycie bardziej zaawansowanych mechanizmów generowania.

---

### 3. **Osadzanie komponentów po stronie frontendowej**
Jeśli korzystasz z frameworków frontendowych (np. React, Vue.js), możesz dostarczyć dane JSON i wygenerować HTML bezpośrednio na frontendzie.

#### Przekazywanie JSON-a:
Dane wejściowe (np. w JSON):
```json
{
  "mygroup": [
    { "value": "Option 1", "extra": "Dynamic Content 1" },
    { "value": "Option 2", "extra": "Dynamic Content 2" }
  ]
}
```

#### Generowanie na frontendzie:
W szablonie Mustache po prostu renderujesz placeholder:
```html
{{#mygroup}}
<div class="radio">
  <input type="checkbox" value="{{value}}">
</div>
<div class="my-indent" data-content="{{extra}}"></div>
{{/mygroup}}
```

JavaScript może później zamienić te placeholdery na bardziej złożony HTML.

---

### 4. **Użycie preprocesora szablonów**
Jeśli nie chcesz przechowywać HTML-a jako stringu, możesz użyć preprocesora na backendzie, który przekształci dane na gotowy HTML przed przekazaniem ich do Mustache.

#### Preprocesowanie:
1. Stwórz osobne pliki HTML dla dynamicznej zawartości.
2. Załaduj i przetwórz je (np. wczytaj plik jako string na backendzie).
3. Wstrzyknij wynik w dane wejściowe Mustache.

---

### Rekomendacja
Najbardziej elastycznym i łatwym w utrzymaniu podejściem jest użycie **partials** w Mustache, ponieważ:
- HTML jest zarządzany w dedykowanych plikach szablonów.
- Oddziela logikę aplikacji od widoku.
- Łatwo aktualizować zawartość bez ingerencji w dane.

---

**User:**

trzymając się metody Użycie szablonów częściowych (partials) czy mogę dynamicznie ustawić który plik partials będzie użyty używając spring mvc?

---

**Assistant:**

Tak, w Spring MVC możesz dynamicznie ustawić, który plik partials będzie użyty w szablonie Mustache. Mustache umożliwia wstawianie dynamicznych częściowych szablonów poprzez interpolację nazw szablonów w danych. Oto, jak można to osiągnąć w Spring MVC:

---

### Przykład

#### 1. **Szablon główny (`main.mustache`)**
W szablonie Mustache, zamiast statycznej nazwy częściowego szablonu, używasz dynamicznego odniesienia:
```html
{{#mygroup}}
<div class="radio">
  <input type="checkbox" value="{{value}}">
</div>
{{> partialName }}
{{/mygroup}}
```

- `{{> partialName }}`: Nazwa częściowego szablonu (`partialName`) będzie określana dynamicznie na podstawie danych przekazanych do widoku.

---

#### 2. **Pliki częściowe**
Załóżmy, że masz dwa pliki częściowe w katalogu `templates`:
- `option1Content.mustache`:
  ```html
  <div class="my-indent">
    <strong>Content for Option 1</strong>
  </div>
  ```
- `option2Content.mustache`:
  ```html
  <div class="my-indent">
    <em>Content for Option 2</em>
  </div>
  ```

---

#### 3. **Kontroler Spring MVC**
W kontrolerze określasz dynamicznie, który plik częściowy ma zostać użyty dla każdego elementu grupy.

```java
@Controller
public class MyController {

    @GetMapping("/example")
    public String example(Model model) {
        List<Map<String, Object>> mygroup = List.of(
            Map.of("value", "Option 1", "partialName", "option1Content"),
            Map.of("value", "Option 2", "partialName", "option2Content")
        );
        model.addAttribute("mygroup", mygroup);
        return "main";
    }
}
```

- Każdy element grupy ma pole `partialName`, które wskazuje na nazwę pliku częściowego (`option1Content` lub `option2Content`).

---

#### 4. **Renderowanie**
Spring MVC przekazuje dane do szablonu, a Mustache wybiera odpowiednie częściowe szablony na podstawie wartości w `partialName`.

Wynikowy HTML:
```html
<div class="radio">
  <input type="checkbox" value="Option 1">
</div>
<div class="my-indent">
  <strong>Content for Option 1</strong>
</div>
<div class="radio">
  <input type="checkbox" value="Option 2">
</div>
<div class="my-indent">
  <em>Content for Option 2</em>
</div>
```

---

### Zalety tego podejścia
1. **Elastyczność**: Możesz dodawać nowe pliki częściowe bez zmieniania kodu szablonu głównego.
2. **Czystość kodu**: Logika wyboru pliku częściowego jest w pełni odseparowana od widoku i kontrolera.
3. **Reużywalność**: Częściowe szablony mogą być używane w innych miejscach aplikacji.

---

### Ważne uwagi
1. **Lokalizacja szablonów**: Upewnij się, że pliki częściowe znajdują się w odpowiednim katalogu szablonów Spring (np. `src/main/resources/templates`).
2. **Silnik Mustache w Spring Boot**: Jeśli używasz Mustache w Spring Boot, upewnij się, że masz odpowiednią zależność:
   ```xml
   <dependency>
       <groupId>org.springframework.boot</groupId>
       <artifactId>spring-boot-starter-mustache</artifactId>
   </dependency>
   ```
3. **Debugowanie**: Jeśli częściowy szablon nie zostanie znaleziony, Mustache może zgłaszać wyjątek. Sprawdź nazwę pliku i konfigurację ścieżki szablonów.