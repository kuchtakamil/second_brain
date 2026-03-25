# Konwersja @RequestParam na boolean

**Data:** 2024-12-04

---

**User:**

czy w spring mvc dodając @QueryParam(IS_ERROR) String isError, mogę sprawić abyto był od razu boolean?

---

**Assistant:**

W Spring MVC możesz użyć adnotacji `@RequestParam` do pobierania parametrów zapytania i możesz bezpośrednio konwertować je na typ `boolean`. Wystarczy zadeklarować typ parametru jako `boolean` (lub jego klasę opakowującą `Boolean`). Spring automatycznie zajmie się konwersją, jeśli parametr jest obecny i poprawnie sformatowany.

Przykład:

```java
@GetMapping("/example")
public String example(@RequestParam(name = "isError", defaultValue = "false") boolean isError) {
    if (isError) {
        // Obsługa przypadku, gdy isError jest true
    }
    return "response";
}
```

### Wyjaśnienie
1. **Automatyczna konwersja**: Spring automatycznie konwertuje parametr zapytania (`isError`) na typ `boolean`. Jeśli parametr ma wartość `"true"`, zostanie skonwertowany na `true`. W przeciwnym razie (np. `"false"`, `"0"`, itp.) zostanie ustawiony na `false`.
   
2. **Default value (`defaultValue`)**: Jeśli parametr `isError` nie zostanie przekazany w zapytaniu, Spring ustawi wartość domyślną (tutaj `"false"`).

3. **Obsługa braku parametru**: Dzięki `defaultValue`, nie musisz sprawdzać, czy parametr jest obecny w zapytaniu.

Jeśli chcesz obsłużyć przypadek, gdzie parametr może być całkowicie nieobecny i nie używać wartości domyślnej, możesz użyć klasy `Boolean`, która pozwala na wartość `null`:

```java
@GetMapping("/example")
public String example(@RequestParam(name = "isError", required = false) Boolean isError) {
    if (Boolean.TRUE.equals(isError)) {
        // Obsługa, gdy isError jest true
    }
    return "response";
}
```

W tym przypadku, jeśli parametr `isError` nie zostanie podany, zmienna `isError` będzie miała wartość `null`.

---

**User:**

to nie ma być requestparam tylko queryparam

---

**Assistant:**

Adnotacja `@QueryParam` pochodzi z JAX-RS (np. w frameworku Jersey) i nie jest natywnie wspierana w Spring MVC. W Spring MVC zwykle używa się `@RequestParam` do obsługi parametrów zapytania.

Jeśli jednak musisz użyć `@QueryParam` (np. w projekcie, który łączy Spring MVC z JAX-RS), warto wiedzieć, że JAX-RS również obsługuje automatyczną konwersję typów. Oto jak możesz to zrobić:

### Przykład z `@QueryParam`
Jeśli pracujesz w kontekście JAX-RS:

```java
@GET
@Path("/example")
public Response example(@QueryParam("isError") boolean isError) {
    if (isError) {
        // Obsługa przypadku, gdy isError jest true
    }
    return Response.ok("response").build();
}
```

### Automatyczna konwersja w JAX-RS
1. **Konwersja do `boolean`**: JAX-RS automatycznie konwertuje wartość parametru zapytania na typ `boolean`. Podobnie jak w Spring MVC, wartości takie jak `"true"` i `"false"` są poprawnie obsługiwane.
2. **Wartość domyślna**: Jeśli parametr `isError` nie zostanie przekazany, JAX-RS ustawi go na `false` (wartość domyślna typu `boolean`).

### Obsługa wartości `null`
Jeśli parametr może być nieobecny i chcesz obsługiwać przypadki, gdy nie zostanie przesłany, użyj obiektu `Boolean` zamiast prymitywnego `boolean`:

```java
@GET
@Path("/example")
public Response example(@QueryParam("isError") Boolean isError) {
    if (Boolean.TRUE.equals(isError)) {
        // Obsługa, gdy isError jest true
    } else {
        // Obsługa, gdy isError jest false lub null
    }
    return Response.ok("response").build();
}
```

### W Spring MVC z użyciem `@QueryParam`
Jeśli koniecznie chcesz używać `@QueryParam` w Spring MVC, musisz upewnić się, że Twój projekt ma wsparcie dla JAX-RS. W takim przypadku mechanika pozostaje taka sama, jak opisana powyżej. 

Jeśli jednak używasz tylko Spring MVC, sugeruję użycie `@RequestParam`, które jest bardziej natywne dla Springa i obsługuje te same przypadki.