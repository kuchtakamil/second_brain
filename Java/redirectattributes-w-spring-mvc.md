# RedirectAttributes w Spring MVC

**Data:** 2024-12-06

---

**User:**

W spring mvc czy gdy w jednym kontrolerze używam RedirectAttributes redirectAttributes, robię redirectAttributes.setAttribute("key","val"), zwracam redirect:... to czy w tym drugim knontrolerze do którego zostałem przekierowany po redirect aby odczytać key mam też użyć RedirectAttributes redirectAttributes czy @RequestParam?

---

**Assistant:**

W Spring MVC, jeśli w jednym kontrolerze używasz `RedirectAttributes` i robisz `redirectAttributes.addAttribute("key", "val")` lub `redirectAttributes.setAttribute("key", "val")`, to wartości te są dodawane jako parametry w URL przekierowania. W kontrolerze, do którego następuje przekierowanie, możesz je odczytać za pomocą adnotacji `@RequestParam`.

Przykład:

### Kontroler A:
```java
@Controller
public class FirstController {

    @GetMapping("/start")
    public String start(RedirectAttributes redirectAttributes) {
        redirectAttributes.addAttribute("key", "val");
        return "redirect:/destination";
    }
}
```

### Kontroler B:
```java
@Controller
public class SecondController {

    @GetMapping("/destination")
    public String destination(@RequestParam("key") String key) {
        System.out.println("Otrzymany key: " + key);
        return "someView";
    }
}
```

### Wyjaśnienie:
1. **`RedirectAttributes` w pierwszym kontrolerze:** Służy do dodania atrybutów do przekierowania. Parametry te są automatycznie doklejane do URL (np. `/destination?key=val`).

2. **`@RequestParam` w drugim kontrolerze:** Jest używane do odczytania parametrów query z URL przekierowania.

### Uwaga:
- `RedirectAttributes.addFlashAttribute()` działa inaczej — atrybuty te są przechowywane tymczasowo w `FlashMap` i **nie** są widoczne w URL. Aby je odczytać, musisz użyć np. `Model` w metodzie docelowej.

Jeśli zależy Ci na ukryciu parametrów w URL, użyj `addFlashAttribute()` zamiast `addAttribute()`, ale pamiętaj, że wtedy `@RequestParam` nie zadziała. W takim przypadku musisz odczytać te dane przez model w widoku.