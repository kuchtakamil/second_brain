# Przekierowanie z parametrami

**Data:** 2024-11-21

---

**User:**

Spring MVC, z kontrolera A robię redirect do kontrolera B.
W kontrolerze B chcę mieć pewną wartość w 
@RequestParam MultiValueMap<String, String> params

Jak ją zapisać w kontrolerze A?

---

**Assistant:**

W Spring MVC możesz przekazać dane do kontrolera B w parametrze zapytania (query parameter) przy wykonywaniu przekierowania. Możesz to zrobić, dodając odpowiednie parametry do URL-a przekierowania.

### Przykład
Załóżmy, że masz dwa kontrolery: **A** i **B**. Kontroler **A** przekierowuje do **B** z wartością, którą chcesz przekazać jako parametr zapytania.

#### Kontroler A
```java
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

@Controller
public class ControllerA {

    @GetMapping("/redirectToB")
    public String redirectToB(RedirectAttributes redirectAttributes) {
        // Dodanie parametru
        redirectAttributes.addAttribute("key", "value");
        return "redirect:/controllerB";
    }
}
```

W tym przypadku `RedirectAttributes` umożliwia łatwe dodanie parametrów zapytania do przekierowania.

---

#### Kontroler B
```java
import org.springframework.stereotype.Controller;
import org.springframework.util.MultiValueMap;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;

@Controller
public class ControllerB {

    @GetMapping("/controllerB")
    public String handleRedirect(@RequestParam MultiValueMap<String, String> params) {
        // Wyświetlenie otrzymanych parametrów
        System.out.println("Otrzymane parametry: " + params);
        return "resultPage";
    }
}
```

---

### Co się dzieje?
1. W kontrolerze A dodajesz parametr `key=value` do zapytania w URL.
2. Kontroler B odbiera te parametry w obiekcie `MultiValueMap<String, String>`.

---

### Wygenerowany URL
Przekierowanie wygeneruje URL w postaci:
```
/controllerB?key=value
```

W kontrolerze B będziesz miał w `params` klucz `key` z wartością `value`.

---

### Uwagi
- Jeśli potrzebujesz bardziej złożonych parametrów (np. listy wartości), możesz przekazać je jako rozdzielone przecinkiem lub JSON, a następnie je sparsować w kontrolerze B.
- Upewnij się, że URL i parametry nie zawierają znaków wymagających kodowania (np. spacji), aby uniknąć problemów. Spring automatycznie koduje parametry, jeśli korzystasz z `RedirectAttributes`.

---

**User:**

ten kotroler B to POST.
Czy nie zadziała request.setAttribute('key', 'val');?

---

**Assistant:**

Jeśli kontroler **B** obsługuje żądania **POST**, to przekazywanie parametrów przez redirect i query parameters (`RedirectAttributes`) nie będzie działać, ponieważ przekierowanie z **kontrolera A** do **kontrolera B** domyślnie wykona żądanie **GET**.

Możesz jednak skorzystać z alternatyw takich jak `request.setAttribute()`, przekazywanie parametrów przez `RedirectAttributes` w Springu nie zadziała w tym scenariuszu, ponieważ przekierowanie wymusza GET.

### Opcje przekazania danych do kontrolera B obsługującego POST:

#### 1. **Przechowywanie danych w `HttpSession`**
Możesz użyć sesji HTTP, aby przechować dane w kontrolerze A i odczytać je w kontrolerze B.

**Kontroler A:**
```java
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PostMapping;

import javax.servlet.http.HttpSession;

@Controller
public class ControllerA {

    @PostMapping("/redirectToB")
    public String redirectToB(HttpSession session) {
        // Przechowywanie danych w sesji
        session.setAttribute("key", "value");
        return "redirect:/controllerB";
    }
}
```

**Kontroler B:**
```java
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PostMapping;

import javax.servlet.http.HttpSession;

@Controller
public class ControllerB {

    @PostMapping("/controllerB")
    public String handlePost(HttpSession session) {
        // Pobranie danych z sesji
        String value = (String) session.getAttribute("key");
        System.out.println("Otrzymana wartość: " + value);

        // Opcjonalnie: usuń wartość z sesji, jeśli jest jednorazowa
        session.removeAttribute("key");
        return "resultPage";
    }
}
```

---

#### 2. **Przechowywanie danych w atrybutach request (Forward zamiast Redirect)**
Jeśli kontroler **B** musi być wywołany żądaniem POST, możesz użyć `RequestDispatcher` do przekazania atrybutów za pomocą **forward**.

**Kontroler A:**
```java
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PostMapping;

import javax.servlet.http.HttpServletRequest;

@Controller
public class ControllerA {

    @PostMapping("/redirectToB")
    public String forwardToB(HttpServletRequest request) {
        // Ustawienie atrybutu w żądaniu
        request.setAttribute("key", "value");
        return "forward:/controllerB";
    }
}
```

**Kontroler B:**
```java
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PostMapping;

import javax.servlet.http.HttpServletRequest;

@Controller
public class ControllerB {

    @PostMapping("/controllerB")
    public String handleForward(HttpServletRequest request) {
        // Pobranie atrybutu z żądania
        String value = (String) request.getAttribute("key");
        System.out.println("Otrzymana wartość: " + value);
        return "resultPage";
    }
}
```

---

#### 3. **Przechowywanie danych w modelu i wykorzystanie Spring Form**
Jeśli musisz obsłużyć redirect (przekierowanie) na POST, musisz najpierw przekierować na stronę GET i wyświetlić formularz, a potem wysłać POST.

---

#### Uwagi:
- **`request.setAttribute()`** działa tylko przy **forward**, ponieważ dane atrybutów nie są przekazywane przez redirect.
- **`HttpSession`** to dobra opcja, jeśli dane muszą być dostępne przez więcej niż jedno żądanie, ale pamiętaj o ich manualnym usuwaniu, jeśli są jednorazowe.
- Jeżeli kontroler B obsługuje tylko POST, możesz rozważyć zmianę logiki aplikacji tak, aby POST był wysyłany z formularza w przeglądarce.

---

**User:**

w kontrolerze A ustawiłem też 
request.setAttribute(View.RESPONSE_STATUS_ATTRIBUTE, HttpStatus.TEMPORARY_REDIRECT);
czy to coś zmienia? nie chcę robić forward ani HttpSession

---

**Assistant:**

Ustawienie atrybutu `View.RESPONSE_STATUS_ATTRIBUTE` na `HttpStatus.TEMPORARY_REDIRECT` w Spring MVC wpływa na sposób realizacji przekierowania, ale nie zmienia faktu, że dane przekazane przez `request.setAttribute` **nie przetrwają** przekierowania.

### Dlaczego `request.setAttribute` nie działa z przekierowaniem?
`request.setAttribute` działa jedynie w obrębie tego samego żądania (np. przy użyciu **forward**). Podczas przekierowania (**redirect**) następuje nowe żądanie HTTP wysyłane przez przeglądarkę, przez co atrybuty ustawione w oryginalnym żądaniu nie są przenoszone do nowego.

---

### Co zmienia ustawienie `View.RESPONSE_STATUS_ATTRIBUTE`?
Ustawienie `HttpStatus.TEMPORARY_REDIRECT` zmusza Spring MVC do wysłania odpowiedzi z kodem HTTP **307 (Temporary Redirect)** lub **308 (Permanent Redirect)**, zamiast domyślnego **302 (Found)**. 

Różnica między tymi kodami polega na sposobie obsługi metody HTTP:
- **302/303:** Przeglądarka zmienia metodę HTTP na **GET** podczas przekierowania, niezależnie od oryginalnej metody.
- **307/308:** Przeglądarka zachowuje oryginalną metodę HTTP (np. POST pozostaje POST-em).

Dzięki temu, jeśli ustawisz **307 Temporary Redirect**, przekierowanie pozwoli zachować POST jako metodę żądania.

---

### Rozwiązanie dla POST z przekazywaniem parametrów
Jeśli chcesz zachować POST i przekazać dane do kontrolera B, możesz:
1. Używać **307 Temporary Redirect** (jak robisz) do zachowania metody POST.
2. Przekazać dane w treści żądania POST zamiast przez `request.setAttribute`.

---

#### Przykład
**Kontroler A:**
```java
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PostMapping;

import javax.servlet.http.HttpServletRequest;

@Controller
public class ControllerA {

    @PostMapping("/redirectToB")
    public String redirectToB(HttpServletRequest request) {
        // Ustawienie atrybutu (ale to nie zadziała na redirect)
        request.setAttribute("key", "value");
        // Wymuszenie 307 Redirect
        request.setAttribute(View.RESPONSE_STATUS_ATTRIBUTE, HttpStatus.TEMPORARY_REDIRECT);
        return "redirect:/controllerB";
    }
}
```

**Kontroler B:**
```java
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;

@Controller
public class ControllerB {

    @PostMapping("/controllerB")
    public String handlePost(@RequestBody String body) {
        // Obsługa danych z treści żądania POST
        System.out.println("Treść żądania: " + body);
        return "resultPage";
    }
}
```

---

### Alternatywy:
1. **Przekazywanie parametrów przez Query Parameters** (ale dla POST jest to mniej typowe i niezalecane, dane mogą być widoczne w URL-u).
2. **Dodanie treści do POST-a w `HttpServletRequest`** (np. JSON, XML, dane formularza), co jest bardziej zgodne z semantyką POST.

Jeśli trzymasz się ustawienia `HttpStatus.TEMPORARY_REDIRECT`, upewnij się, że przeglądarka wysyła dane poprawnie w nowym żądaniu POST.