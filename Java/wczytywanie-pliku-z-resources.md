# Wczytywanie pliku z resources

**Data:** 2024-12-03

---

**User:**

jak w java 17 wczytać plik tekstowy który znajduje się w resources

---

**Assistant:**

W Javie 17 możesz użyć klasy `ClassLoader` lub `Class` do wczytywania plików znajdujących się w katalogu `resources`. Oto przykład:

### Przygotowanie
Upewnij się, że plik znajduje się w katalogu `src/main/resources`. W czasie budowania projektu plik ten zostanie automatycznie dodany do ścieżki zasobów.

Przykład struktury projektu:
```
src/
└── main/
    ├── java/
    │   └── com/example/MyApp.java
    └── resources/
        └── example.txt
```

### Wczytywanie pliku

#### Użycie `ClassLoader`:
```java
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardCharsets;
import java.util.List;

public class MyApp {
    public static void main(String[] args) {
        try {
            // Wczytanie pliku jako InputStream
            var inputStream = MyApp.class.getClassLoader().getResourceAsStream("example.txt");
            if (inputStream == null) {
                throw new IllegalArgumentException("Plik nie został znaleziony!");
            }

            // Odczytanie zawartości pliku jako String
            String content = new String(inputStream.readAllBytes(), StandardCharsets.UTF_8);
            System.out.println("Zawartość pliku:");
            System.out.println(content);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
```

#### Użycie `Path` i `ClassLoader` (tylko do odczytu lokalnego):
Jeśli plik może być dostępny jako ścieżka plikowa (lokalny system plików), możesz użyć `Path`:
```java
import java.nio.file.Files;
import java.nio.file.Path;

public class MyApp {
    public static void main(String[] args) {
        try {
            var uri = MyApp.class.getClassLoader().getResource("example.txt").toURI();
            Path path = Path.of(uri);
            String content = Files.readString(path);
            System.out.println("Zawartość pliku:");
            System.out.println(content);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

#### Użycie `Files.lines` dla większych plików:
Jeśli plik jest większy, można wczytać go liniami:
```java
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.stream.Stream;

public class MyApp {
    public static void main(String[] args) {
        try {
            var uri = MyApp.class.getClassLoader().getResource("example.txt").toURI();
            Path path = Path.of(uri);
            try (Stream<String> lines = Files.lines(path)) {
                lines.forEach(System.out::println);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

### Uwagi:
1. Użycie `ClassLoader` jest bezpieczniejsze, ponieważ działa niezależnie od lokalizacji zasobu (np. w przypadku JAR).
2. Metoda z `Path` wymaga, aby plik istniał jako lokalny zasób systemu plików, co nie zawsze jest możliwe w środowisku produkcyjnym.