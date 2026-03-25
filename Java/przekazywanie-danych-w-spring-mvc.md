# Przekazywanie danych w Spring MVC

**Data:** 2024-12-04

---

**User:**

Czy w Spring MVC można z jednego kontrolera do drugiego kontrolera przekazać obiekt typy Map<String, Boolean> ?

---

**Assistant:**

Tak, w Spring MVC możesz przekazać obiekt typu `Map<String, Boolean>` między kontrolerami, ale wymaga to odpowiedniego podejścia w zależności od tego, jak te kontrolery komunikują się ze sobą. Oto kilka możliwych sposobów:

---

### 1. **Przekazanie przez `Model` lub `RedirectAttributes`**

Jeśli pierwszy kontroler wykonuje przekierowanie (redirect) do drugiego kontrolera, możesz przekazać dane przy użyciu `RedirectAttributes`:

```java
@Controller
public class FirstController {

    @GetMapping("/first")
    public String handleRequest(RedirectAttributes redirectAttributes) {
        Map<String, Boolean> map = new HashMap<>();
        map.put("key1", true);
        map.put("key2", false);
        redirectAttributes.addFlashAttribute("map", map);
        return "redirect:/second";
    }
}

@Controller
public class SecondController {

    @GetMapping("/second")
    public String handleRedirect(@ModelAttribute("map") Map<String, Boolean> map, Model model) {
        // Odbieranie mapy
        System.out.println("Received map: " + map);
        model.addAttribute("map", map); // Opcjonalnie dla widoku
        return "secondView";
    }
}
```

- W tym przypadku dane są przekazywane jako atrybuty `FlashAttribute`, które są dostępne tylko podczas jednego przekierowania.

---

### 2. **Przekazanie przez sesję (`HttpSession`)**

Jeśli dane muszą być przechowywane dłużej niż na czas jednego żądania, możesz użyć `HttpSession`:

```java
@Controller
public class FirstController {

    @GetMapping("/first")
    public String handleRequest(HttpSession session) {
        Map<String, Boolean> map = new HashMap<>();
        map.put("key1", true);
        map.put("key2", false);
        session.setAttribute("map", map);
        return "redirect:/second";
    }
}

@Controller
public class SecondController {

    @GetMapping("/second")
    public String handleRedirect(HttpSession session, Model model) {
        @SuppressWarnings("unchecked")
        Map<String, Boolean> map = (Map<String, Boolean>) session.getAttribute("map");
        System.out.println("Received map: " + map);
        model.addAttribute("map", map); // Opcjonalnie dla widoku
        return "secondView";
    }
}
```

- Tutaj mapa zostaje przechowana w sesji i może być dostępna przez dłuższy czas.

---

### 3. **Przekazanie przez żądanie (`HttpServletRequest`)**

Jeśli oba kontrolery obsługują różne metody w ramach jednego żądania, można użyć `HttpServletRequest`:

```java
@Controller
public class FirstController {

    @GetMapping("/first")
    public String handleRequest(HttpServletRequest request) {
        Map<String, Boolean> map = new HashMap<>();
        map.put("key1", true);
        map.put("key2", false);
        request.setAttribute("map", map);
        return "forward:/second";
    }
}

@Controller
public class SecondController {

    @GetMapping("/second")
    public String handleForward(HttpServletRequest request, Model model) {
        @SuppressWarnings("unchecked")
        Map<String, Boolean> map = (Map<String, Boolean>) request.getAttribute("map");
        System.out.println("Received map: " + map);
        model.addAttribute("map", map); // Opcjonalnie dla widoku
        return "secondView";
    }
}
```

- Tutaj dane są przekazywane w ramach jednego żądania przy użyciu mechanizmu przekierowania `forward`.

---

### 4. **Przekazanie przez parametr w adresie URL**

Jeśli mapa zawiera niewiele danych, można je serializować i przekazać jako parametry w adresie URL:

```java
@Controller
public class FirstController {

    @GetMapping("/first")
    public String handleRequest() {
        return "redirect:/second?key1=true&key2=false";
    }
}

@Controller
public class SecondController {

    @GetMapping("/second")
    public String handleRedirect(@RequestParam Map<String, String> params, Model model) {
        Map<String, Boolean> map = params.entrySet().stream()
            .collect(Collectors.toMap(Map.Entry::getKey, entry -> Boolean.valueOf(entry.getValue())));
        System.out.println("Received map: " + map);
        model.addAttribute("map", map);
        return "secondView";
    }
}
```

- Uwaga: Ten sposób jest odpowiedni tylko dla małych zestawów danych i gdy mapa nie zawiera wrażliwych informacji.

---

Który sposób wybrać zależy od Twojego przypadku użycia. Jeśli dane mają być dostępne tylko podczas jednej sesji użytkownika, najlepszym wyborem jest `HttpSession`. Jeśli dane są jednorazowe, `RedirectAttributes` lub `HttpServletRequest` mogą być bardziej odpowiednie.

---

**User:**

Drugim kontrolerem jest POST, czy to coś zmienia?

---

**Assistant:**

Jeśli drugim kontrolerem jest metoda POST, to sposób przekazania danych między kontrolerami zmienia się, ponieważ standardowy mechanizm `redirect` w HTTP wymaga żądania GET. Możesz jednak użyć kilku technik:

---

### 1. **Przekazanie danych przez `HttpSession`**

`HttpSession` pozwala przechować dane między żądaniami, niezależnie od ich typu (GET lub POST):

#### Przykład:
**Pierwszy kontroler (GET):**
```java
@Controller
public class FirstController {

    @GetMapping("/first")
    public String handleRequest(HttpSession session) {
        Map<String, Boolean> map = new HashMap<>();
        map.put("key1", true);
        map.put("key2", false);
        session.setAttribute("map", map);
        return "redirect:/second";
    }
}
```

**Drugi kontroler (POST):**
```java
@Controller
public class SecondController {

    @PostMapping("/second")
    public String handlePost(HttpSession session, Model model) {
        @SuppressWarnings("unchecked")
        Map<String, Boolean> map = (Map<String, Boolean>) session.getAttribute("map");
        if (map != null) {
            System.out.println("Received map: " + map);
            model.addAttribute("map", map);
            session.removeAttribute("map"); // Usunięcie danych, jeśli są jednorazowe
        }
        return "secondView";
    }
}
```

- **Zaleta:** Działa z POST.
- **Wadą** może być konieczność ręcznego zarządzania sesją, jeśli dane są jednorazowe.

---

### 2. **Przekazanie przez przekierowanie z POST na POST**

Możesz użyć `HttpServletRequest` i mechanizmu `forward`, jeśli oba kontrolery obsługują to samo żądanie.

#### Przykład:
**Pierwszy kontroler (GET):**
```java
@Controller
public class FirstController {

    @GetMapping("/first")
    public String handleRequest(HttpServletRequest request) {
        Map<String, Boolean> map = new HashMap<>();
        map.put("key1", true);
        map.put("key2", false);
        request.setAttribute("map", map);
        return "forward:/second";
    }
}
```

**Drugi kontroler (POST):**
```java
@Controller
public class SecondController {

    @PostMapping("/second")
    public String handlePost(HttpServletRequest request, Model model) {
        @SuppressWarnings("unchecked")
        Map<String, Boolean> map = (Map<String, Boolean>) request.getAttribute("map");
        if (map != null) {
            System.out.println("Received map: " + map);
            model.addAttribute("map", map);
        }
        return "secondView";
    }
}
```

- **Zaleta:** Działa z POST i przekazuje dane w ramach jednego żądania.
- **Wada:** Wymaga użycia `forward`, a nie `redirect`.

---

### 3. **Przekazanie przez atrybuty formularza (POST z danymi w body)**

Możesz przekazać dane jako atrybuty formularza i przesłać je w ciele żądania POST.

#### Przykład:
**Pierwszy kontroler (GET):**
```java
@Controller
public class FirstController {

    @GetMapping("/first")
    public String handleRequest(Model model) {
        Map<String, Boolean> map = new HashMap<>();
        map.put("key1", true);
        map.put("key2", false);
        model.addAttribute("map", map);
        return "redirectForm"; // Widok formularza
    }
}
```

**Widok formularza (`redirectForm.mustache`):**
```html
<form action="/second" method="post">
    <input type="hidden" name="key1" value="true" />
    <input type="hidden" name="key2" value="false" />
    <button type="submit">Submit</button>
</form>
```

**Drugi kontroler (POST):**
```java
@Controller
public class SecondController {

    @PostMapping("/second")
    public String handlePost(@RequestParam Map<String, String> params, Model model) {
        Map<String, Boolean> map = params.entrySet().stream()
            .collect(Collectors.toMap(Map.Entry::getKey, entry -> Boolean.valueOf(entry.getValue())));
        System.out.println("Received map: " + map);
        model.addAttribute("map", map);
        return "secondView";
    }
}
```

- **Zaleta:** Dane trafiają do ciała żądania POST.
- **Wada:** Wymaga wygenerowania widoku formularza.

---

### 4. **Użycie API (REST lub JSON)**

Możesz przesłać dane jako `JSON` w ciele żądania POST, jeśli oba kontrolery pracują z REST.

#### Przykład:
**Pierwszy kontroler:**
```java
@Controller
public class FirstController {

    @GetMapping("/first")
    public String handleRequest(Model model) {
        Map<String, Boolean> map = new HashMap<>();
        map.put("key1", true);
        map.put("key2", false);
        model.addAttribute("map", map);
        return "redirectToApi"; // Widok z wywołaniem POST API
    }
}
```

**Widok (`redirectToApi.mustache`):**
```html
<script>
    fetch('/second', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ key1: true, key2: false })
    }).then(response => response.text()).then(data => console.log(data));
</script>
```

**Drugi kontroler (POST):**
```java
@RestController
public class SecondController {

    @PostMapping("/second")
    public ResponseEntity<String> handlePost(@RequestBody Map<String, Boolean> map) {
        System.out.println("Received map: " + map);
        return ResponseEntity.ok("Success");
    }
}
```

- **Zaleta:** Skuteczne przy dużej ilości danych i użyciu JSON.
- **Wada:** Więcej konfiguracji.

---

Najlepszym rozwiązaniem jest zależne od kontekstu. Jeśli to jednorazowe przekierowanie, najlepszy będzie `HttpSession` lub `forward`. Jeśli dane są bardziej dynamiczne, warto użyć formularza lub API.