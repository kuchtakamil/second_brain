# Warunkowa rejestracja kontrolera

**Data:** 2025-05-13

---

**User:**

W projekcie Java + Spring mam zmienną pobieraną tak
@Value("MY_FEATURE_SWITCH")
Teraz od wartości tej zmiennej chciałbym uzależnić która wersja kontrolera (@Controller) będzie używana. 

---

**Assistant:**

Aby na podstawie wartości feature switcha (np. zmiennej środowiskowej lub wpisu z `application.properties`) dynamicznie wybrać, która wersja kontrolera Springowego ma być używana, można podejść do tego na kilka sposobów. Poniżej przedstawię 3 najczęstsze:

---

## ✅ **1. Warunkowa rejestracja beanów (kontrolerów) z użyciem `@ConditionalOnProperty`**

To najczystsze i najczęściej używane podejście w Spring Boot.

### Krok 1: Zmień `@Value` na konfigurację property

W `application.properties` (lub jako zmienna środowiskowa):
```properties
my.feature.enabled=true
```

### Krok 2: Zastosuj warunkowe kontrolery

```java
@Controller
@ConditionalOnProperty(name = "my.feature.enabled", havingValue = "true")
public class NewController {
    @GetMapping("/feature")
    public ResponseEntity<String> newVersion() {
        return ResponseEntity.ok("Nowa wersja");
    }
}
```

```java
@Controller
@ConditionalOnProperty(name = "my.feature.enabled", havingValue = "false", matchIfMissing = true)
public class OldController {
    @GetMapping("/feature")
    public ResponseEntity<String> oldVersion() {
        return ResponseEntity.ok("Stara wersja");
    }
}
```

> Dzięki temu tylko jeden z kontrolerów zostanie zarejestrowany jako Spring bean — w zależności od wartości property.

---

## ✅ **2. Jeden kontroler, ale delegowanie logiki**

Jeśli nie możesz mieć dwóch kontrolerów z tą samą ścieżką, możesz użyć **jednego kontrolera**, który deleguje do różnych implementacji na podstawie feature switcha:

```java
@RestController
public class FeatureController {

    @Value("${my.feature.enabled:false}")
    private boolean featureEnabled;

    @GetMapping("/feature")
    public ResponseEntity<String> handleFeature() {
        if (featureEnabled) {
            return ResponseEntity.ok("Nowa wersja");
        } else {
            return ResponseEntity.ok("Stara wersja");
        }
    }
}
```

Lub użyć strategii/iniekcji przez interfejsy, np.:

```java
public interface FeatureHandler {
    String handle();
}
```

```java
@Component
@ConditionalOnProperty(name = "my.feature.enabled", havingValue = "true")
public class NewFeatureHandler implements FeatureHandler {
    public String handle() {
        return "Nowa wersja";
    }
}

@Component
@ConditionalOnProperty(name = "my.feature.enabled", havingValue = "false", matchIfMissing = true)
public class OldFeatureHandler implements FeatureHandler {
    public String handle() {
        return "Stara wersja";
    }
}
```

A w kontrolerze:

```java
@RestController
public class FeatureController {
    private final FeatureHandler handler;

    public FeatureController(FeatureHandler handler) {
        this.handler = handler;
    }

    @GetMapping("/feature")
    public String getFeature() {
        return handler.handle();
    }
}
```

---

## 🚫 **3. Dynamiczna rejestracja kontrolerów w runtime**

Teoretycznie możliwe (np. przez `RequestMappingHandlerMapping`), ale **niezalecane** — jest to skomplikowane i nieczytelne, a nie zyskujesz wiele w porównaniu do prostszych sposobów wyżej.

---

## Podsumowanie

Najlepsze podejścia:

- **`@ConditionalOnProperty`** – pozwala rejestrować różne kontrolery na podstawie feature switcha.
- **Delegowanie logiki** – użyteczne, jeśli endpointy muszą być te same.

Jeśli chcesz, mogę Ci pomóc zaimplementować jedno z tych podejść dokładnie w Twoim przypadku.