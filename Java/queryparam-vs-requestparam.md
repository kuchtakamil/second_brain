# @QueryParam vs @RequestParam

**Data:** 2024-11-20

---

**User:**

w spring controller używam import javax.ws.rs.QueryParam; oraz w innym kontrolerze @RequestParam MultiValueMap<String, String> params,
Czy mogę zamiast QueryParam użyć @RequestParam MultiValueMap<String, String> params żeby przekazać zmienne w url ...?isError=true ?

---

**Assistant:**

Tak, możesz użyć `@RequestParam MultiValueMap<String, String>` zamiast `@QueryParam` do przekazywania zmiennych w URL, takich jak `?isError=true`. W Springu `@RequestParam` działa z parametrami zapytania (`query parameters`) i pozwala wygodnie obsłużyć wiele wartości dla tego samego klucza.

### Przykład z `@RequestParam MultiValueMap<String, String>`:

```java
@RestController
@RequestMapping("/api")
public class MyController {

    @GetMapping("/example")
    public ResponseEntity<String> example(@RequestParam MultiValueMap<String, String> params) {
        // Dostęp do parametrów
        String isError = params.getFirst("isError");
        return ResponseEntity.ok("isError: " + isError);
    }
}
```

#### Co się stanie:
1. Jeśli wywołasz URL:  
   ```
   /api/example?isError=true
   ```
   Wartość `isError` zostanie odczytana jako `"true"`.

2. Jeśli parametr `isError` będzie miał wiele wartości, np.:  
   ```
   /api/example?isError=true&isError=false
   ```
   Możesz uzyskać wszystkie wartości za pomocą:
   ```java
   List<String> isErrorValues = params.get("isError");
   ```

### Różnica między `@RequestParam` a `@QueryParam`:
- `@RequestParam` to natywne rozwiązanie Springa i jest bardziej uniwersalne.
- `@QueryParam` pochodzi z JAX-RS (Java EE/Jakarta EE) i w Springu wymaga dodatkowej konfiguracji lub odpowiednich zależności.

Zalecane jest korzystanie z `@RequestParam` w Springowych aplikacjach, ponieważ jest bardziej spójne z jego ekosystemem.