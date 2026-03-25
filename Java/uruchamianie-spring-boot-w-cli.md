# Uruchamianie Spring Boot w CLI

**Data:** 2024-12-25

---

**User:**

Używam Intellij Comunity więc nie mam wsparcia dla uruchamiania aplikacji spring boot. W jaki sposób mogę uruchomić w konsoli aplikację java korzytającą ze spring boot? Chcę również podać profil springa z którym ma się uruchomić aplikacja

---

**Assistant:**

Możesz uruchomić aplikację Spring Boot w konsoli, używając następujących kroków:

1. **Zbudowanie aplikacji Spring Boot**:
   - Najpierw upewnij się, że Twoja aplikacja została poprawnie zbudowana jako plik jar. Możesz to zrobić, wykonując polecenie:
     ```bash
     ./mvnw clean package
     ```
     lub jeśli korzystasz z Gradle:
     ```bash
     ./gradlew clean bootJar
     ```
   - Po tym procesie, znajdziesz plik `.jar` w katalogu `target` (dla Maven) lub `build/libs` (dla Gradle).

2. **Uruchomienie aplikacji z konsoli**:
   - Możesz uruchomić aplikację za pomocą polecenia:
     ```bash
     java -jar nazwa-aplikacji.jar
     ```

3. **Podanie profilu Springa**:
   - Aby uruchomić aplikację z określonym profilem Springa (np. `dev`, `prod`), użyj flagi `--spring.profiles.active`:
     ```bash
     java -jar nazwa-aplikacji.jar --spring.profiles.active=dev
     ```
   - Możesz również ustawić zmienną środowiskową `SPRING_PROFILES_ACTIVE`:
     ```bash
     SPRING_PROFILES_ACTIVE=dev java -jar nazwa-aplikacji.jar
     ```

4. **Opcjonalne dodatkowe argumenty**:
   - Możesz dodać inne właściwości, korzystając z flag `--key=value`. Przykład:
     ```bash
     java -jar nazwa-aplikacji.jar --server.port=8081 --spring.profiles.active=prod
     ```

### Uwaga
Jeśli używasz Maven Wrapper (`mvnw`), możesz również uruchomić aplikację bez budowania `.jar`, ale tylko w trakcie developmentu:
```bash
./mvnw spring-boot:run -Dspring-boot.run.profiles=dev
```

Daj znać, jeśli potrzebujesz dalszych wskazówek!

---

**User:**

nie mam pliku mvnw. Czy mogę go szybko wygynerować?

---

**Assistant:**

Tak, możesz łatwo wygenerować plik `mvnw` (Maven Wrapper) dla swojego projektu. Wystarczy wykonać poniższe kroki:

1. **Uruchomienie polecenia generującego Maven Wrapper**:
   W katalogu głównym projektu, gdzie znajduje się plik `pom.xml`, wykonaj:
   ```bash
   mvn -N wrapper:wrapper
   ```
   Jeśli masz zainstalowanego Mavena w systemie, to polecenie wygeneruje następujące pliki:
   - `mvnw` (plik wykonywalny dla systemu Linux/MacOS)
   - `mvnw.cmd` (plik wykonywalny dla Windows)
   - Katalog `.mvn`, który zawiera plik `wrapper.jar` i konfigurację Maven Wrapper (`maven-wrapper.properties`).

2. **Uruchamianie projektu za pomocą Maven Wrapper**:
   Po wygenerowaniu plików, możesz używać `./mvnw` zamiast `mvn`. Na przykład:
   ```bash
   ./mvnw clean package
   ./mvnw spring-boot:run -Dspring-boot.run.profiles=dev
   ```

3. **Dodanie do kontroli wersji**:
   Warto dodać pliki Maven Wrapper (`mvnw`, `mvnw.cmd` i `.mvn`) do systemu kontroli wersji (np. Git), aby inne osoby pracujące nad projektem mogły używać tej samej wersji Mavena bez potrzeby instalowania go lokalnie.

Jeśli masz jakieś trudności, daj znać! 😊

---

**User:**

Dostałem błąd
Failed to execute goal org.apache.maven.plugins:maven-compiler-plugin:3.10.1:compile (default-compile) on project my-projecti: Fatal error compiling: error: release version 17 not supported

---

**Assistant:**

Błąd `release version 17 not supported` oznacza, że Twoja wersja JDK lub Maven nie obsługuje Javy 17, którą próbujesz skompilować. Oto kroki, aby to naprawić:

---

### 1. **Sprawdź wersję JDK**
Upewnij się, że masz zainstalowaną Javę 17 (lub wyższą). Sprawdź wersję, wykonując w terminalu:
```bash
java -version
```
Jeśli wersja Javy jest niższa niż 17, zaktualizuj JDK, pobierając najnowszą wersję z [Oracle](https://www.oracle.com/java/technologies/javase-downloads.html) lub [AdoptOpenJDK](https://adoptopenjdk.net/).

---

### 2. **Zaktualizuj Maven**
Niektóre starsze wersje Maven nie obsługują Javy 17. Sprawdź wersję Mavena:
```bash
mvn -version
```
Jeśli używasz starszej wersji niż 3.8.1, zaktualizuj Maven do nowszej wersji:
- Pobierz nowszą wersję z [strony Apache Maven](https://maven.apache.org/download.cgi).
- Zaktualizuj ścieżkę do Mavena w zmiennej środowiskowej `PATH`.

---

### 3. **Skonfiguruj `maven-compiler-plugin`**
Upewnij się, że w pliku `pom.xml` masz odpowiednio skonfigurowany plugin kompilatora, który obsługuje Javę 17:
```xml
<build>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-compiler-plugin</artifactId>
            <version>3.10.1</version>
            <configuration>
                <source>17</source>
                <target>17</target>
            </configuration>
        </plugin>
    </plugins>
</build>
```

---

### 4. **Sprawdź zmienną `JAVA_HOME`**
Upewnij się, że zmienna środowiskowa `JAVA_HOME` wskazuje na instalację JDK 17. Możesz to sprawdzić:
- W systemie Linux/MacOS:
  ```bash
  echo $JAVA_HOME
  ```
- W systemie Windows:
  ```cmd
  echo %JAVA_HOME%
  ```

Jeśli wskazuje na starszą wersję JDK, zaktualizuj zmienną środowiskową:
- Linux/MacOS:
  ```bash
  export JAVA_HOME=/ścieżka/do/jdk-17
  ```
- Windows:
  Zmień zmienną środowiskową w ustawieniach systemu.

---

### 5. **Wyczyść projekt i spróbuj ponownie**
Po dokonaniu zmian, uruchom czyszczenie projektu i ponowną kompilację:
```bash
./mvnw clean compile
```

Jeśli problem nadal występuje, daj znać, a pomogę znaleźć rozwiązanie! 😊

---

**User:**

jak w ./mvnw clean package mogę pominąć testy

---

**Assistant:**

Aby pominąć testy podczas budowania projektu za pomocą Maven Wrapper (`./mvnw`), możesz dodać flagę `-DskipTests` do polecenia. Na przykład:

```bash
./mvnw clean package -DskipTests
```

### Wyjaśnienie:
- `-DskipTests`: Pomija uruchamianie testów podczas budowania projektu. Testy nie są wykonywane, ale nadal będą kompilowane.
  
Jeśli chcesz również pominąć kompilację testów, użyj flagi `-Dmaven.test.skip=true`:
```bash
./mvnw clean package -Dmaven.test.skip=true
```

### Różnice:
- `-DskipTests`: Kompiluje testy, ale ich nie uruchamia.
- `-Dmaven.test.skip=true`: Całkowicie pomija zarówno kompilację, jak i uruchamianie testów.

Obie opcje są przydatne w zależności od potrzeb. Daj znać, jeśli masz dodatkowe pytania! 😊

---

**User:**

a czy mógłbym uruchomić dopowiednik ./mvnw spring-boot:run -Dspring-boot.run.profiles=dev
ale używając mvn a nie mvnw?

---

**Assistant:**

Tak, możesz uruchomić odpowiednik komendy `./mvnw spring-boot:run -Dspring-boot.run.profiles=dev` używając bezpośrednio `mvn`, o ile masz Mavena poprawnie zainstalowanego w systemie. Wystarczy wykonać:

```bash
mvn spring-boot:run -Dspring-boot.run.profiles=dev
```

### Warunki:
1. **Maven zainstalowany lokalnie**:
   Upewnij się, że Maven jest zainstalowany i dostępny w systemowej ścieżce. Możesz to sprawdzić, wykonując:
   ```bash
   mvn -version
   ```

2. **Poprawnie skonfigurowany projekt**:
   Plik `pom.xml` powinien zawierać odpowiednią konfigurację wtyczki Spring Boot, np.:
   ```xml
   <build>
       <plugins>
           <plugin>
               <groupId>org.springframework.boot</groupId>
               <artifactId>spring-boot-maven-plugin</artifactId>
           </plugin>
       </plugins>
   </build>
   ```

3. **Używanie profilu**:
   Flaga `-Dspring-boot.run.profiles=dev` ustawia aktywny profil Springa na `dev`. Jeśli nie masz tego profilu skonfigurowanego, upewnij się, że istnieje w pliku `application-dev.yml` lub `application-dev.properties`.

### Uwagi:
- Jeśli chcesz pominąć testy przy uruchamianiu, dodaj flagę `-DskipTests`:
  ```bash
  mvn spring-boot:run -Dspring-boot.run.profiles=dev -DskipTests
  ```

Daj znać, jeśli masz więcej pytań! 😊