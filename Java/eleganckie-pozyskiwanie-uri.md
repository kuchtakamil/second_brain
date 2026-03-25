# Eleganckie pozyskiwanie URI

**Data:** 2024-12-03

---

**User:**

Czy jest jakiś bardziej elegancki sposób aby pozyskać uri do pliku?
var uri = MyClass.class.getClassLoader().getResource("/myFile.txt").toURI();

---

**Assistant:**

Tak, możesz uprościć i uczynić bardziej eleganckim sposób uzyskiwania URI do pliku, eliminując błędną ścieżkę i potencjalne ryzyka. Nie dodawaj wiodącego ukośnika `/` do nazwy pliku, ponieważ `ClassLoader.getResource` szuka zasobów w odniesieniu do korzenia ścieżki klas.

Poniżej poprawiona wersja:

```java
var uri = MyClass.class.getClassLoader().getResource("myFile.txt").toURI();
```

### Dodatkowe wskazówki:
1. **Unikaj potencjalnych błędów**:
   Jeśli plik nie istnieje, metoda `getResource` zwróci `null`, co może prowadzić do wyjątku `NullPointerException`. Dlatego warto dodać walidację:

   ```java
   var resource = MyClass.class.getClassLoader().getResource("myFile.txt");
   if (resource == null) {
       throw new IllegalArgumentException("File not found: myFile.txt");
   }
   var uri = resource.toURI();
   ```

2. **Rozważ użycie `Path` lub `Files` dla plików**:
   Jeśli potrzebujesz operować na plikach lokalnych w bardziej nowoczesny sposób, możesz wykorzystać `java.nio.file.Path`:

   ```java
   var path = Path.of(MyClass.class.getClassLoader().getResource("myFile.txt").toURI());
   ```

3. **Przy pracy w kontekście Springa**:
   Jeżeli korzystasz z frameworka Spring, możesz użyć klasy `ResourceLoader` lub `@Value` do bardziej idiomatycznego ładowania zasobów, np.:

   ```java
   @Autowired
   private ResourceLoader resourceLoader;

   public void loadFile() throws IOException {
       var resource = resourceLoader.getResource("classpath:myFile.txt");
       try (var inputStream = resource.getInputStream()) {
           // Operacje na pliku
       }
   }
   ```

Czy takie podejście spełnia Twoje wymagania? 😊

---

**User:**

A gdy używam springa?

---

**Assistant:**

Jeśli używasz Springa, masz do dyspozycji bardziej idiomatyczne i elastyczne sposoby ładowania zasobów. Możesz wykorzystać klasy Springa, takie jak `ResourceLoader` lub `Resource`, albo zastosować bezpośrednie wstrzykiwanie plików przy użyciu adnotacji `@Value`.

### Przykład użycia `ResourceLoader`
`ResourceLoader` pozwala na ładowanie zasobów z różnych miejsc (np. classpath, system plików, URL).

```java
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.Resource;
import org.springframework.core.io.ResourceLoader;
import org.springframework.stereotype.Service;

import java.nio.file.Files;
import java.nio.file.Path;

@Service
public class FileService {

    @Autowired
    private ResourceLoader resourceLoader;

    public void loadFile() throws Exception {
        Resource resource = resourceLoader.getResource("classpath:myFile.txt");
        if (!resource.exists()) {
            throw new IllegalArgumentException("File not found: myFile.txt");
        }
        Path path = resource.getFile().toPath(); // Możesz uzyskać ścieżkę
        System.out.println("File content: " + Files.readString(path)); // Przykładowa operacja
    }
}
```

### Przykład użycia `@Value`
Jeśli plik jest mały, a jego zawartość można wczytać jako tekst, możesz użyć `@Value` do wstrzyknięcia zawartości pliku lub samej jego ścieżki:

#### 1. Wstrzyknięcie zawartości pliku:
```java
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

@Service
public class FileService {

    @Value("classpath:myFile.txt")
    private Resource resource;

    public void loadFile() throws Exception {
        try (var inputStream = resource.getInputStream()) {
            String content = new String(inputStream.readAllBytes());
            System.out.println("File content: " + content);
        }
    }
}
```

#### 2. Wstrzyknięcie ścieżki do pliku:
```java
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.nio.file.Files;
import java.nio.file.Path;

@Service
public class FileService {

    @Value("classpath:myFile.txt")
    private Resource resource;

    public void loadFile() throws Exception {
        Path path = resource.getFile().toPath();
        System.out.println("File content: " + Files.readString(path));
    }
}
```

### Dlaczego to jest lepsze?
1. **Elastyczność**: Możesz w łatwy sposób przełączyć się między różnymi źródłami plików (np. z `classpath:` na `file:` lub `http:`).
2. **Obsługa wyjątków**: Klasy Springa dostarczają mechanizmy do eleganckiego zarządzania wyjątkami związanymi z dostępem do zasobów.
3. **Integracja**: Rozwiązanie lepiej wpisuje się w styl Springa i jest łatwiejsze do testowania dzięki wstrzykiwaniu zależności.

Czy takie podejście Ci odpowiada? 😊