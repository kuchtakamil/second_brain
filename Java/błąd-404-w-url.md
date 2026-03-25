# Błąd 404 w URL

**Data:** 2024-12-06

---

**User:**

kiedy w spring controller przekazuję w url parametr np 
Tier%201%20-%20LTR%20Investor%20Application%20-%20Standard dostaję 404

---

**Assistant:**

Gdy przekazujesz parametr w URL, taki jak `Tier%201%20-%20LTR%20Investor%20Application%20-%20Standard`, Spring MVC może mieć problem z jego poprawnym mapowaniem, jeśli jest źle zakodowany lub wymaga dodatkowego przetwarzania. Oto kilka możliwych przyczyn i rozwiązań:

---

### 1. **URL Decoding**
Parametry w URL muszą być zakodowane w formacie URL-encoded. Jeśli parametr jest poprawnie zakodowany (`%20` dla spacji), ale Spring nie jest w stanie go obsłużyć, upewnij się, że masz odpowiednią konfigurację do dekodowania.

#### Rozwiązanie:
W `@RequestMapping` lub `@GetMapping` upewnij się, że adnotacja prawidłowo obsługuje parametry. Na przykład:

```java
@GetMapping("/process")
public String process(@RequestParam String name) {
    System.out.println("Name: " + name);
    return "success";
}
```

---

### 2. **Escapowanie znaków specjalnych w ścieżce**
Jeśli parametr zawiera znaki specjalne, takie jak `+`, `/`, czy `%`, mogą one być źródłem problemu.

#### Rozwiązanie:
Dodaj w konfiguracji Springa wsparcie dla pełnego dekodowania URL, ustawiając opcję `UrlPathHelper`:

```java
@Configuration
public class WebConfig implements WebMvcConfigurer {
    @Override
    public void configurePathMatch(PathMatchConfigurer configurer) {
        configurer.setUrlPathHelper(new UrlPathHelper() {{
            setAlwaysUseFullPath(true);
            setUrlDecode(true); // Domyślnie jest true, ale warto się upewnić
        }});
    }
}
```

---

### 3. **Parametry w `@PathVariable`**
Jeśli używasz parametru w ścieżce jako `@PathVariable`, upewnij się, że jest odpowiednio zakodowany. Spring wymaga, aby znaki specjalne (w tym `%`) były zakodowane.

#### Rozwiązanie:
Jeśli używasz `@PathVariable`, ustaw `encodeURIComponent` po stronie klienta. Przykład:

JavaScript:

```javascript
const param = encodeURIComponent("Tier 1 - LTR Investor Application - Standard");
const url = `/process/${param}`;
```

Controller:

```java
@GetMapping("/process/{name}")
public String process(@PathVariable String name) {
    System.out.println("Name: " + name);
    return "success";
}
```

---

### 4. **Przykładowe wywołanie z przeglądarki/Postman**
Jeśli testujesz w Postmanie, upewnij się, że znaki specjalne są poprawnie zakodowane. Na przykład:

Nieprawidłowe:  
```
/process/Tier 1 - LTR Investor Application - Standard
```

Prawidłowe:  
```
/process/Tier%201%20-%20LTR%20Investor%20Application%20-%20Standard
```

---

Jeśli te kroki nie rozwiążą problemu, podziel się szczegółami:
1. Jak wygląda Twój kontroler?
2. Jak wywołujesz żądanie?
3. Czy korzystasz z dodatkowych bibliotek (np. Spring Security, które mogą modyfikować obsługę URL)?

---

**User:**

podaj jak zrobić encodeURIComponent w java nie javascript

---

**Assistant:**

W Javie możesz użyć klasy `URLEncoder` do kodowania URL, podobnie jak `encodeURIComponent` w JavaScript. Oto przykład:

```java
import java.io.UnsupportedEncodingException;
import java.net.URLEncoder;

public class URLEncoderExample {
    public static void main(String[] args) {
        String value = "Tier 1 - LTR Investor Application - Standard";
        
        try {
            String encodedValue = URLEncoder.encode(value, "UTF-8");
            System.out.println("Encoded value: " + encodedValue);
        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
        }
    }
}
```

---

### **Jak działa `URLEncoder`?**
- **`URLEncoder.encode(String, String)`** koduje ciąg znaków w formacie URL-encoded.
- Wymaga podania nazwy kodowania znaków (np. `UTF-8`).

---

### **Przykład wyjścia**
Dla tekstu `Tier 1 - LTR Investor Application - Standard`, zakodowany wynik to:  
```
Tier+1+-+LTR+Investor+Application+-+Standard
```

Zauważ, że `URLEncoder` zamienia spacje na `+` zamiast `%20`. Jeśli chcesz zachować spacje jako `%20`, możesz zastąpić `+` ręcznie:

```java
String encodedValue = URLEncoder.encode(value, "UTF-8").replace("+", "%20");
System.out.println("Custom Encoded value: " + encodedValue);
```

---

### **Gdzie stosować?**
Zakodowany ciąg można następnie bezpiecznie przekazać w URL w żądaniu HTTP, np.:

```java
String baseUrl = "https://example.com/process";
String param = URLEncoder.encode("Tier 1 - LTR Investor Application - Standard", "UTF-8");
String fullUrl = baseUrl + "?name=" + param;
System.out.println("Full URL: " + fullUrl);
```

Rezultat:
```
https://example.com/process?name=Tier%201%20-%20LTR%20Investor%20Application%20-%20Standard
```

---

**User:**

a później jak to spring controller od czytuje to też coś trzeba zrobić?

---

**Assistant:**

W większości przypadków Spring automatycznie dekoduje parametry z URL, więc nie trzeba robić nic dodatkowego, aby poprawnie odczytać dane zakodowane przy użyciu `URLEncoder`. Jednak w zależności od miejsca, gdzie ten parametr jest przekazywany (`@PathVariable` czy `@RequestParam`), mogą być potrzebne pewne modyfikacje. Oto szczegóły:

---

### **1. Odczytanie parametru w `@RequestParam`**
Jeśli parametr jest przekazywany w zapytaniu jako `query parameter`, np.:

```
https://example.com/process?name=Tier%201%20-%20LTR%20Investor%20Application%20-%20Standard
```

Wystarczy użyć `@RequestParam` w kontrolerze:

```java
@GetMapping("/process")
public String process(@RequestParam String name) {
    System.out.println("Decoded name: " + name);
    return "success";
}
```

Spring automatycznie zdekoduje wartość `Tier%201%20-%20LTR%20Investor%20Application%20-%20Standard` do:  
```
Tier 1 - LTR Investor Application - Standard
```

---

### **2. Odczytanie parametru w `@PathVariable`**
Jeśli parametr jest częścią ścieżki, np.:

```
https://example.com/process/Tier%201%20-%20LTR%20Investor%20Application%20-%20Standard
```

Kontroler wygląda tak:

```java
@GetMapping("/process/{name}")
public String process(@PathVariable String name) {
    System.out.println("Decoded name: " + name);
    return "success";
}
```

Ważne: 
- Spring również automatycznie zdekoduje wartość, jeśli jest zakodowana w formacie URL-encoded.
- Upewnij się, że kodowanie po stronie klienta jest poprawne (`encodeURIComponent` lub `URLEncoder`).

---

### **3. Problemy z dekodowaniem znaków specjalnych**
Jeśli parametry zawierają znaki specjalne (`+`, `/`, `%` itp.) i coś nie działa:

#### Rozwiązanie 1: Ustawienia Springa
Włącz pełne dekodowanie URL w Springu, jak poniżej:

```java
@Configuration
public class WebConfig implements WebMvcConfigurer {
    @Override
    public void configurePathMatch(PathMatchConfigurer configurer) {
        UrlPathHelper urlPathHelper = new UrlPathHelper();
        urlPathHelper.setAlwaysUseFullPath(true);
        urlPathHelper.setUrlDecode(true);
        configurer.setUrlPathHelper(urlPathHelper);
    }
}
```

#### Rozwiązanie 2: Ręczne dekodowanie
Jeśli nadal pojawiają się problemy, możesz zdekodować parametr ręcznie przy użyciu `URLDecoder`:

```java
import java.net.URLDecoder;

@GetMapping("/process/{name}")
public String process(@PathVariable String name) {
    try {
        String decodedName = URLDecoder.decode(name, "UTF-8");
        System.out.println("Decoded name: " + decodedName);
        return "success";
    } catch (UnsupportedEncodingException e) {
        e.printStackTrace();
        return "error";
    }
}
```

---

### **Podsumowanie**
- **@RequestParam**: Automatyczne dekodowanie. 
- **@PathVariable**: Automatyczne dekodowanie, ale konfiguracja może pomóc w przypadku problemów.
- Jeśli znaki specjalne powodują błędy, włącz odpowiednie dekodowanie w konfiguracji Springa lub użyj `URLDecoder`.