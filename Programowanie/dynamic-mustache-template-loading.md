# Dynamic Mustache Template Loading

**Data:** 2024-12-03

---

**User:**

Pracuję z framework mustache oraz Spring MVC. Chę dynamicznie decydować w spring mvc o rodzaju mustache jaki będzie ładowany. Nie chodzi mi jednak o główny widok tylko o składowe widoku głównego. 
Np. to mój widok główny
{{#mygroup}}
<div class="radio">
  <input type="checkbox" value="{{value}}">
</div>
{{> myIndentContent }}
{{/mygroup}}

Ato dwa przykłady w plikach mustache które powinny znaleźć się w widoku główny zamiast myIndentContent:

dynamic1.mustache
<div class="my-indent">
  <strong>Dynamic content for {{value}}</strong>
</div>

dynamic2.mustache
<div class="my-indent">
  <strong>My even more dynamic content for {{value}} !! Enjoy</strong>
</div>

---

**Assistant:**

User works with the Mustache framework and Spring MVC.

---

**Assistant:**

Aby dynamicznie decydować o zawartości sekcji `{{> myIndentContent }}` w Mustache, możesz skorzystać z mechanizmu Spring MVC do przekazywania dynamicznych danych do widoków. Możesz to zrobić w następujący sposób:

1. **Przekazanie dynamicznej nazwy szablonu do widoku**: W kontrolerze Springa określaj, który szablon powinien być załadowany.

2. **Stworzenie własnej implementacji `TemplateLoader`**: Mustache pozwala na tworzenie niestandardowego ładowania szablonów.

### Przykładowa implementacja

#### 1. **Pliki Mustache**

- `dynamic1.mustache`:
  ```html
  <div class="my-indent">
    <strong>Dynamic content for {{value}}</strong>
  </div>
  ```

- `dynamic2.mustache`:
  ```html
  <div class="my-indent">
    <strong>My even more dynamic content for {{value}} !! Enjoy</strong>
  </div>
  ```

- `main.mustache`:
  ```html
  {{#mygroup}}
  <div class="radio">
    <input type="checkbox" value="{{value}}">
  </div>
  {{> dynamicPartial }}
  {{/mygroup}}
  ```

#### 2. **Kontroler Springa**

```java
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

import java.util.List;
import java.util.Map;

@Controller
public class DynamicController {

    @GetMapping("/dynamic")
    public String getDynamicContent(Model model) {
        // Przygotowanie danych
        List<Map<String, String>> mygroup = List.of(
            Map.of("value", "Option 1"),
            Map.of("value", "Option 2")
        );
        
        model.addAttribute("mygroup", mygroup);
        
        // Decyzja o dynamicznym szablonie
        String dynamicTemplate = "dynamic1"; // lub dynamic2 na podstawie logiki
        model.addAttribute("dynamicPartial", dynamicTemplate);

        return "main"; // Główny szablon
    }
}
```

#### 3. **Konfiguracja Mustache**

Spring domyślnie wspiera `TemplateLoader`. Możesz dostosować go do ładowania różnych nazw szablonów.

#### 4. **Ustawienia dynamiczne**

Dynamiczna część jest kontrolowana przez wartość `dynamicPartial` w modelu. Dzięki temu Mustache automatycznie załaduje odpowiedni szablon.

W ten sposób możesz dynamicznie wstawiać różne widoki w sekcji `{{> dynamicPartial }}` w zależności od potrzeb aplikacji.

---

**User:**

Tylko że w moim przypadku mustache chce załadować widok o nazwie dynamicPartial zamiast zastąpić tą nazwę nazwą przekazaną w springu

---

**Assistant:**

Rozumiem problem. Mustache interpretuje `{{> dynamicPartial }}` jako próbę załadowania widoku o stałej nazwie `dynamicPartial`. Aby dynamicznie podmienić nazwę wstawianego widoku, musisz zastosować inne podejście, ponieważ Mustache nie obsługuje wprost dynamicznych nazw części (partials).

Poniżej znajdziesz rozwiązanie tego problemu:

---

### Rozwiązanie: Dynamiczna zamiana treści w kontrolerze

Możesz przygotować dane w kontrolerze, łącząc dynamicznie zawartość części widoków i przekazując ją jako dane do głównego widoku.

#### 1. **Plik główny Mustache (main.mustache)**

Zmodyfikuj główny widok, aby używał zmiennej dla treści dynamicznej:

```html
{{#mygroup}}
<div class="radio">
  <input type="checkbox" value="{{value}}">
</div>
{{{dynamicContent}}} <!-- Treść wstawiona dynamicznie -->
{{/mygroup}}
```

Zamiast `{{> dynamicPartial }}`, użyj `{{{dynamicContent}}}`, aby Mustache wstawił treść HTML z modelu.

---

#### 2. **Kontroler Springa**

W kontrolerze załaduj odpowiednią zawartość z pliku lub wygeneruj ją dynamicznie.

```java
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.util.Map;

@Controller
public class DynamicController {

    @GetMapping("/dynamic")
    public String getDynamicContent(Model model) throws Exception {
        // Dane do głównego widoku
        List<Map<String, String>> mygroup = List.of(
            Map.of("value", "Option 1"),
            Map.of("value", "Option 2")
        );
        model.addAttribute("mygroup", mygroup);

        // Logika wyboru dynamicznej zawartości
        String dynamicTemplate = "dynamic1"; // lub dynamic2 na podstawie logiki
        String dynamicContent = Files.readString(Path.of("templates/" + dynamicTemplate + ".mustache"));

        model.addAttribute("dynamicContent", dynamicContent);

        return "main"; // Główny szablon
    }
}
```

---

#### 3. **Pliki dynamiczne (dynamic1.mustache i dynamic2.mustache)**

Pliki mogą pozostać takie same, ale ich zawartość jest teraz ładowana jako zwykły tekst.

---

### Wyjaśnienie

- **Problem dynamicznej nazwy**: Mustache sam w sobie nie pozwala na dynamiczne zastępowanie nazw części, więc musisz załadować zawartość pliku w kontrolerze.
- **Rozwiązanie z `{{{dynamicContent}}}`**: Wykorzystanie `{{{...}}}` w Mustache pozwala na wstawienie przetworzonego HTML-a w widoku głównym.
- **Zalety**: Daje pełną kontrolę nad dynamicznym wyborem zawartości, pozwalając na załadowanie dowolnej części widoku.