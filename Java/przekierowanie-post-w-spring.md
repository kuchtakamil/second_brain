# Przekierowanie POST w Spring

**Data:** 2024-11-21

---

**User:**

Spring MVC, z kontrolera A robię redirect do kontrolera B. Kontroler B to jest POST.
W kontrolerze B chcę mieć pewną wartość w 
@RequestParam MultiValueMap<String, String> params

Jak ją zapisać w kontrolerze A?
W kontrolerze A ustawiam również 
request.setAttribute(View.RESPONSE_STATUS_ATTRIBUTE, HttpStatus.TEMPORARY_REDIRECT);

---

**Assistant:**

W Spring MVC, gdy robisz `redirect` z kontrolera A do kontrolera B, dane nie są domyślnie przenoszone w treści POST, ponieważ `redirect` HTTP zwykle używa przekierowania z kodem 3xx i mechanizmów przeglądarki, które domyślnie nie obsługują przekazywania danych w POST.

Jeśli jednak chcesz przekazać dane w parametrze `MultiValueMap<String, String>` do kontrolera B, musisz zastosować inne podejście, ponieważ w standardowym `redirect` dane mogą być przekazane jedynie w parametrach URL (GET) lub w nagłówkach.

### Rozwiązanie 1: Użycie `RedirectAttributes`
Przekaż dane w parametrach URL jako część przekierowania:

#### Kontroler A:
```java
@GetMapping("/kontrolerA")
public String kontrolerA(RedirectAttributes redirectAttributes) {
    // Dodanie parametru do przekierowania
    redirectAttributes.addAttribute("klucz", "wartosc");

    // Przekierowanie do kontrolera B
    return "redirect:/kontrolerB";
}
```

#### Kontroler B:
```java
@PostMapping("/kontrolerB")
public ResponseEntity<String> kontrolerB(@RequestParam MultiValueMap<String, String> params) {
    // Odczytywanie parametrów
    String wartosc = params.getFirst("klucz");

    return ResponseEntity.ok("Otrzymano parametr: " + wartosc);
}
```

### Rozwiązanie 2: Użycie HTTP Session
Jeśli parametry nie mogą być widoczne w URL (np. ze względów bezpieczeństwa), możesz je przechować w sesji.

#### Kontroler A:
```java
@GetMapping("/kontrolerA")
public String kontrolerA(HttpSession session) {
    // Umieszczenie danych w sesji
    session.setAttribute("klucz", "wartosc");

    // Przekierowanie do kontrolera B
    return "redirect:/kontrolerB";
}
```

#### Kontroler B:
```java
@PostMapping("/kontrolerB")
public ResponseEntity<String> kontrolerB(HttpSession session) {
    // Pobranie danych z sesji
    String wartosc = (String) session.getAttribute("klucz");

    // Usunięcie danych z sesji, jeśli są jednorazowe
    session.removeAttribute("klucz");

    return ResponseEntity.ok("Otrzymano parametr: " + wartosc);
}
```

### Rozwiązanie 3: Przekierowanie POST-POST
Jeśli konieczne jest przekazanie danych w ciele POST, możesz użyć narzędzi takich jak Spring `RestTemplate` lub JavaScript do wykonania żądania POST zamiast standardowego przekierowania.

#### Kontroler A:
```java
@PostMapping("/kontrolerA")
public ResponseEntity<Void> kontrolerA(HttpServletResponse response) throws IOException {
    // Utworzenie formularza HTML do POST
    String html = """
        <form id="redirectForm" action="/kontrolerB" method="post">
            <input type="hidden" name="klucz" value="wartosc" />
        </form>
        <script>
            document.getElementById('redirectForm').submit();
        </script>
    """;

    response.setContentType("text/html");
    response.getWriter().write(html);

    return ResponseEntity.ok().build();
}
```

#### Kontroler B:
```java
@PostMapping("/kontrolerB")
public ResponseEntity<String> kontrolerB(@RequestParam MultiValueMap<String, String> params) {
    // Odczyt parametrów z ciała POST
    String wartosc = params.getFirst("klucz");

    return ResponseEntity.ok("Otrzymano parametr: " + wartosc);
}
```

### Wnioski
- Dla prostoty i bezpieczeństwa `RedirectAttributes` jest najczęściej stosowanym podejściem, o ile dane mogą być widoczne w URL.
- W przypadku bardziej wrażliwych danych sesja lub własna implementacja POST-POST są lepsze. Wybór metody zależy od kontekstu i wymagań bezpieczeństwa Twojej aplikacji.