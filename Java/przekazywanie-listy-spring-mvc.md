# Przekazywanie listy Spring MVC

**Data:** 2024-12-06

---

**User:**

W spring MVC chcę pomiędzy kontrolerami przekazaliś listę stringów zawierających spacje np 
["jakis niezadlugi tekst", "inny tekst", "a to bedzie juz ostatni"]
Chcę aby w drugim kontrolerze te teksty były widoczne w ten sam sposób


---

**Assistant:**

Aby przekazać listę stringów między kontrolerami w Spring MVC, można skorzystać z kilku metod w zależności od tego, czy chcesz używać przekierowania, sesji, czy atrybutów modelu. Oto trzy podejścia:

---

### **1. Przekazywanie przy użyciu parametrów URL (GET)**
Możesz zakodować listę stringów jako parametry zapytania i przekazać je podczas przekierowania.

#### Przykład:
Kontroler 1:
```java
@GetMapping("/pierwszy")
public String pierwszyKontroler(RedirectAttributes redirectAttributes) {
    List<String> lista = List.of("jakis niezadlugi tekst", "inny tekst", "a to bedzie juz ostatni");
    redirectAttributes.addAttribute("teksty", String.join(",", lista)); // Łączenie listy w jeden string
    return "redirect:/drugi";
}
```

Kontroler 2:
```java
@GetMapping("/drugi")
public String drugiKontroler(@RequestParam String teksty, Model model) {
    List<String> lista = Arrays.asList(teksty.split(",")); // Rozdzielanie stringa na listę
    model.addAttribute("lista", lista);
    return "widok";
}
```

---

### **2. Użycie sesji HTTP**
Jeżeli dane mają być tymczasowe i dostępne pomiędzy żądaniami, możesz przechować je w sesji.

#### Przykład:
Kontroler 1:
```java
@GetMapping("/pierwszy")
public String pierwszyKontroler(HttpSession session) {
    List<String> lista = List.of("jakis niezadlugi tekst", "inny tekst", "a to bedzie juz ostatni");
    session.setAttribute("listaTekstow", lista);
    return "redirect:/drugi";
}
```

Kontroler 2:
```java
@GetMapping("/drugi")
public String drugiKontroler(HttpSession session, Model model) {
    List<String> lista = (List<String>) session.getAttribute("listaTekstow");
    model.addAttribute("lista", lista);
    return "widok";
}
```

---

### **3. Użycie `Model` i atrybutów `FlashAttributes`**
FlashAttributes pozwalają na przekazywanie danych pomiędzy przekierowaniami.

#### Przykład:
Kontroler 1:
```java
@GetMapping("/pierwszy")
public String pierwszyKontroler(RedirectAttributes redirectAttributes) {
    List<String> lista = List.of("jakis niezadlugi tekst", "inny tekst", "a to bedzie juz ostatni");
    redirectAttributes.addFlashAttribute("listaTekstow", lista);
    return "redirect:/drugi";
}
```

Kontroler 2:
```java
@GetMapping("/drugi")
public String drugiKontroler(@ModelAttribute("listaTekstow") List<String> lista, Model model) {
    model.addAttribute("lista", lista);
    return "widok";
}
```

---

### Wybór podejścia
- **Parametry URL (GET)**: Jeśli dane mają być widoczne w adresie URL.
- **Sesja HTTP**: Jeśli dane muszą być dostępne w całej sesji użytkownika.
- **FlashAttributes**: Jeśli chcesz przekazać dane tylko między przekierowaniami.

Jeśli dane zawierają spacje i inne znaki specjalne, pamiętaj o odpowiednim kodowaniu/odkodowaniu w przypadku parametrów URL (`URLEncoder`/`URLDecoder`).

---

**User:**

co do metody 1, jakiego innego separatora można by użyć, ale takiego który jest dozwolony w url

---

**Assistant:**

W URL możesz użyć wielu separatorów, które są bezpieczne i nie wymagają kodowania. Oto kilka przykładów:

1. **Pionowa kreska (`|`)**  
   Jest czytelna i rzadko używana w danych tekstowych:
   ```java
   redirectAttributes.addAttribute("teksty", String.join("|", lista));
   // Rozdzielanie w drugim kontrolerze
   List<String> lista = Arrays.asList(teksty.split("\\|"));
   ```

2. **Dwukropek (`:`)**  
   Prosty i intuicyjny:
   ```java
   redirectAttributes.addAttribute("teksty", String.join(":", lista));
   List<String> lista = Arrays.asList(teksty.split(":"));
   ```

3. **Średnik (`;`)**  
   Również bezpieczny w URL:
   ```java
   redirectAttributes.addAttribute("teksty", String.join(";", lista));
   List<String> lista = Arrays.asList(teksty.split(";"));
   ```

4. **Myślnik (`-`) lub Podkreślenie (`_`)**  
   Używane często jako separatory w URL, szczególnie gdy dane są bardziej czytelne:
   ```java
   redirectAttributes.addAttribute("teksty", String.join("-", lista));
   List<String> lista = Arrays.asList(teksty.split("-"));
   ```

---

### Separator a znaki specjalne
Jeśli dane mogą zawierać potencjalnie każdy znak (nawet te wybrane jako separator), warto użyć kodowania URL (`URLEncoder.encode`) lub niestandardowego separatora, np. sekwencji, która na pewno nie wystąpi w tekstach (np. `--SEP--`):

#### Kodowanie separatora:
```java
redirectAttributes.addAttribute("teksty", String.join("--SEP--", lista));
List<String> lista = Arrays.asList(teksty.split("--SEP--"));
```

#### Kodowanie URL (dla całego tekstu):
```java
import java.net.URLEncoder;
import java.net.URLDecoder;

String teksty = URLEncoder.encode(String.join("|", lista), "UTF-8");
// Odkodowanie
List<String> lista = Arrays.asList(URLDecoder.decode(teksty, "UTF-8").split("\\|"));
```

### Dlaczego unikać przecinka (`,`)?  
Przecinek często wymaga kodowania w bardziej złożonych przypadkach, zwłaszcza gdy dane zawierają znaki specjalne lub przestrzenie. Warto go zastąpić bezpieczniejszymi separatorami, jak powyżej.

---

**User:**

ok, w takim razie mam teraz obiekt typu List<String> i zawiera albo listę stringów gotowych do pracy albo zawiera jeden string ale oddzielony --SEP--. Jak mogę otrzymać listę stringów gotowych do pracy w każdym przypadku

---

**Assistant:**

Aby przekształcić obiekt `List<String>` w listę gotowych stringów, niezależnie od tego, czy masz listę elementów, czy jeden string z separatorami, możesz zastosować następującą metodę:

```java
public List<String> przygotujListe(List<String> input) {
    if (input.size() == 1 && input.get(0).contains("--SEP--")) {
        // Rozbij jeden element na listę na podstawie separatora
        return Arrays.asList(input.get(0).split("--SEP--"));
    }
    // Jeśli lista jest już gotowa, zwróć ją bez zmian
    return input;
}
```

### Wyjaśnienie:
1. **Sprawdzenie warunku**:
   - `input.size() == 1`: Sprawdzamy, czy lista ma tylko jeden element.
   - `input.get(0).contains("--SEP--")`: Jeśli element zawiera separator, oznacza to, że trzeba go rozdzielić.

2. **Rozdzielanie stringa**:
   - `input.get(0).split("--SEP--")`: Rozbijamy string według separatora `--SEP--`.

3. **Zwracanie wyników**:
   - Jeśli lista nie wymaga rozdzielania, jest zwracana w oryginalnej formie.

### Użycie:
```java
List<String> lista1 = List.of("jakis niezadlugi tekst", "inny tekst", "a to bedzie juz ostatni");
List<String> lista2 = List.of("jakis niezadlugi tekst--SEP--inny tekst--SEP--a to bedzie juz ostatni");

System.out.println(przygotujListe(lista1)); // ["jakis niezadlugi tekst", "inny tekst", "a to bedzie juz ostatni"]
System.out.println(przygotujListe(lista2)); // ["jakis niezadlugi tekst", "inny tekst", "a to bedzie juz ostatni"]
```

---

### Dodatkowo: Obsługa pustej listy
Jeśli lista może być pusta, możesz dodać zabezpieczenie:
```java
public List<String> przygotujListe(List<String> input) {
    if (input == null || input.isEmpty()) {
        return Collections.emptyList();
    }
    if (input.size() == 1 && input.get(0).contains("--SEP--")) {
        return Arrays.asList(input.get(0).split("--SEP--"));
    }
    return input;
}
``` 

Dzięki temu metoda będzie bardziej odporna na błędy.