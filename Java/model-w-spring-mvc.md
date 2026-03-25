# Model w Spring MVC

**Data:** 2024-11-19

---

**User:**

Używam
org.springframework.web.bind.annotation.GetMapping
org.springframework.web.bind.annotation.PostMapping
org.springframework.stereotype.Controller
oraz
org.springframework.ui.Model
Model jest przekazywany jako parametr metody adnotowanej przy pomocy GetMapping/PostMapping.
Nie wiem jak zachowuje się model w przypadku wywoływania kilku metod jednego kontrolera w sekwencji. Czy stan modelu jest zachowany i przekazywany z wywołania na wywołanie?

---

**Assistant:**

W Spring MVC model (`org.springframework.ui.Model`) jest tworzony na nowo dla każdego żądania HTTP. Oznacza to, że nie ma trwałości stanu modelu między różnymi wywołaniami metod kontrolera, nawet jeśli są one wywoływane w ramach tej samej sesji użytkownika.

### Szczegóły zachowania modelu:
- Model jest obiektem specyficznym dla żądania (`request-scoped`).
- Za każdym razem, gdy metoda kontrolera jest wywoływana w wyniku żądania HTTP, Spring tworzy nową instancję modelu i przekazuje ją do metody kontrolera.
- Dane w modelu są przekazywane do widoku (np. szablonu Thymeleaf, JSP) po zakończeniu przetwarzania żądania.

### Zachowanie modelu w sekwencji wywołań:
Jeśli w ramach jednego żądania HTTP wywoływana jest inna metoda kontrolera (np. przez przekierowanie wewnętrzne), model **nie jest automatycznie przenoszony**. Aby przenieść dane między metodami w jednym żądaniu, możesz użyć:
1. **`RedirectAttributes`** – w przypadku przekierowań (`redirect:`).
2. **Atrybutów sesji** – jeśli dane mają być dostępne między różnymi żądaniami HTTP.
3. **Bezpośrednie przekazanie danych** – przez parametry w metodach kontrolera.

### Przykład z `RedirectAttributes`:
```java
@Controller
public class ExampleController {

    @GetMapping("/step1")
    public String step1(Model model) {
        model.addAttribute("message", "Step 1 completed");
        return "step1"; // widok step1.html
    }

    @PostMapping("/step2")
    public String step2(RedirectAttributes redirectAttributes) {
        redirectAttributes.addFlashAttribute("message", "Step 2 completed");
        return "redirect:/step3";
    }

    @GetMapping("/step3")
    public String step3(Model model) {
        // Tutaj można odczytać dane przekazane jako "Flash Attributes"
        return "step3"; // widok step3.html
    }
}
```

W powyższym przykładzie dane z `step2` będą dostępne w `step3` dzięki użyciu `RedirectAttributes`.

Jeśli chcesz, aby dane były przechowywane między różnymi żądaniami, możesz użyć adnotacji `@SessionAttributes`.

### `@SessionAttributes` – przechowywanie danych między żądaniami:
```java
@Controller
@SessionAttributes("user")
public class ExampleController {

    @ModelAttribute("user")
    public User user() {
        return new User(); // inicjalizacja modelu sesji
    }

    @GetMapping("/profile")
    public String profile(@ModelAttribute("user") User user) {
        // Dane użytkownika są dostępne w modelu sesji
        return "profile";
    }

    @PostMapping("/update")
    public String update(@ModelAttribute("user") User user) {
        // Aktualizacja danych użytkownika w modelu sesji
        user.setName("Updated Name");
        return "redirect:/profile";
    }
}
```

Dzięki `@SessionAttributes` obiekt `user` będzie dostępny między różnymi żądaniami kontrolera.

Podsumowując:
- Model nie zachowuje stanu między wywołaniami metod kontrolera w różnych żądaniach.
- Aby przenieść dane, użyj `RedirectAttributes`, atrybutów sesji lub innego mechanizmu trwałości.