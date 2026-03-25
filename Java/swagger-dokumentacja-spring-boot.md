# Swagger dokumentacja Spring Boot

**Data:** 2024-11-09

---

**User:**

Mam projekt w Spring Boot z kontrolerami opisanymi adnotacjami swaggera.
W pom.xml nie mam bezpośrednich zależności do swagger ani openapi. 
Mam tylko klasę 
@Configruation public class SwaggerCOnfiguration.

Chcę wygenerować i uruchomić dokumentację REST API utworzoną przez swagger. Co powinienem zmienić w konfiguracji? Co powinienem uruchomić aby móc korzystać z dokumentacji REST API utworzonęj przez swaggera?

---

**Assistant:**

Aby wygenerować i uruchomić dokumentację Swagger dla REST API w Spring Boot, musisz upewnić się, że masz odpowiednie zależności oraz konfigurację. 

### Krok 1: Dodaj zależności do Swaggera

W pliku `pom.xml` musisz dodać zależność do Swaggera lub OpenAPI. Użyj najnowszej wersji `springdoc-openapi`, która jest obecnie popularnym narzędziem do generowania dokumentacji OpenAPI w aplikacjach Spring Boot.

```xml
<dependency>
    <groupId>org.springdoc</groupId>
    <artifactId>springdoc-openapi-ui</artifactId>
    <version>1.6.14</version>
</dependency>
```

### Krok 2: Skonfiguruj Swaggera w aplikacji

Skoro masz już klasę `SwaggerConfiguration` oznaczoną adnotacją `@Configuration`, upewnij się, że zawiera poprawne ustawienia dla OpenAPI (choć w większości przypadków dodanie zależności automatycznie włącza Swagger UI i OpenAPI w Spring Boot).

Na przykład, konfiguracja może wyglądać tak:

```java
import io.swagger.v3.oas.models.info.Info;
import org.springdoc.core.GroupedOpenApi;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class SwaggerConfiguration {

    @Bean
    public GroupedOpenApi publicApi() {
        return GroupedOpenApi.builder()
                .group("public")
                .pathsToMatch("/**")
                .build();
    }
}
```

### Krok 3: Uruchomienie aplikacji i dostęp do dokumentacji

1. Uruchom swoją aplikację Spring Boot.
2. Po uruchomieniu aplikacji, dokumentacja Swagger powinna być dostępna pod adresem:
   - **Swagger UI**: [http://localhost:8080/swagger-ui.html](http://localhost:8080/swagger-ui.html)
   - **OpenAPI JSON**: [http://localhost:8080/v3/api-docs](http://localhost:8080/v3/api-docs)

### Dodatkowe uwagi

Jeśli chcesz, aby dokumentacja Swagger była dostępna tylko w środowiskach developerskich, możesz zabezpieczyć endpoint Swaggera lub skonfigurować go warunkowo za pomocą profilu Spring (np. `application-dev.properties`).

---

**User:**

Nie mogę się dostać do tych linków. Czy przy starcie aplikacji powinienem widzieć w logach że swagger coś generuje?

---

**Assistant:**

Tak, w logach powinieneś zobaczyć komunikaty wskazujące na inicjalizację OpenAPI lub Swagger UI podczas uruchamiania aplikacji. Jeśli nie widzisz takich komunikatów, może to oznaczać, że zależności nie zostały poprawnie zainstalowane lub konfiguracja nie jest w pełni aktywna.

Oto kroki, które warto przejrzeć:

### 1. Upewnij się, że zależność `springdoc-openapi-ui` jest poprawnie dodana

Po dodaniu zależności do `springdoc-openapi-ui` w `pom.xml`, uruchom ponownie **Maven** (np. przez `mvn clean install` lub poprzez IDE, np. IntelliJ/ Eclipse) aby upewnić się, że wszystkie zależności zostały pobrane.

### 2. Sprawdź logi startowe aplikacji

Jeśli `springdoc-openapi` jest prawidłowo dodany, powinieneś zobaczyć w logach komunikaty o załadowaniu kontekstu OpenAPI, np.:
```
o.s.s.d.SpringDocConfigProperties: Starting Swagger UI in default mode
o.s.s.w.OpenApiResource     : Initializing OpenAPI document
```

### 3. Sprawdź, czy adresy są poprawne

Sprawdź następujące domyślne adresy Swagger UI oraz dokumentacji OpenAPI:

- Swagger UI: [http://localhost:8080/swagger-ui/index.html](http://localhost:8080/swagger-ui/index.html)
- Dokumentacja OpenAPI w formacie JSON: [http://localhost:8080/v3/api-docs](http://localhost:8080/v3/api-docs)

### 4. Sprawdź konfigurację proxy lub firewalla

Czasami konfiguracje proxy lub firewalla blokują dostęp do określonych zasobów. Upewnij się, że nie masz reguł ograniczających dostęp do endpointów `swagger-ui/index.html` lub `v3/api-docs`.

### 5. Włącz profil `dev` w Spring Boot (opcjonalnie)

Jeśli korzystasz z różnych profili w Spring Boot, upewnij się, że profil, który uruchamiasz, jest skonfigurowany do włączenia Swaggera.

W `application.yml` lub `application.properties` możesz dodać:
```yaml
spring.profiles.active=dev
```

### 6. Dodaj klasę `SwaggerConfiguration` z podstawową konfiguracją (opcjonalnie)

Jeżeli poprzednie kroki nie działają, spróbuj dodać podstawową klasę konfiguracyjną bez dodatkowych ustawień.

```java
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Info;

@Configuration
public class SwaggerConfiguration {

    @Bean
    public OpenAPI customOpenAPI() {
        return new OpenAPI()
                .info(new Info()
                        .title("My API")
                        .version("1.0")
                        .description("Opis API"));
    }
}
```

Jeśli po tych krokach nadal nie możesz uzyskać dostępu do dokumentacji, daj znać – mogę pomóc w dalszej diagnozie.

---

**User:**

Używam innego profilu niż dev. Jakie properties mam ustawić w swoim profilu aby swagger był uruchomiony?

---

**Assistant:**

User uses a non-dev profile in their Spring Boot project.

---

**Assistant:**

Aby włączyć Swaggera dla innego profilu niż `dev`, nie musisz zwykle dodawać specjalnych właściwości w pliku `application-{profile}.properties` lub `application-{profile}.yml`, ponieważ `springdoc-openapi` domyślnie działa we wszystkich profilach.

Jeśli jednak Swagger jest ograniczony tylko do niektórych profili lub w ogóle się nie uruchamia, upewnij się, że masz następujące ustawienia:

### 1. Upewnij się, że `springdoc-openapi` nie jest wyłączony

W pliku `application-{profile}.properties` lub `application-{profile}.yml` (dla profilu, którego używasz) dodaj:

```properties
springdoc.api-docs.enabled=true
springdoc.swagger-ui.enabled=true
```

### 2. Zmiana konfiguracji profilowej (opcjonalnie)

Jeśli chcesz, aby Swagger był uruchamiany tylko dla określonych profili, możesz użyć warunkowego włączenia konfiguracji. Możesz na przykład dodać warunek do swojej klasy `SwaggerConfiguration`, aby włączała się tylko w wybranym profilu:

```java
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Profile;
import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Info;

@Configuration
@Profile("twoj_profil") // Zastąp "twoj_profil" nazwą profilu
public class SwaggerConfiguration {

    @Bean
    public OpenAPI customOpenAPI() {
        return new OpenAPI()
                .info(new Info()
                        .title("My API")
                        .version("1.0")
                        .description("Opis API"));
    }
}
```

Po wykonaniu tych kroków uruchom aplikację i spróbuj uzyskać dostęp do dokumentacji Swagger w wybranym profilu pod adresem [http://localhost:8080/swagger-ui/index.html](http://localhost:8080/swagger-ui/index.html).

---

**User:**

nadal nie mogę się tam dostać. Nadal brak logów swaggera

---

**Assistant:**

Skoro nadal nie masz dostępu do dokumentacji i brakuje logów Swaggera, to możliwe, że problem leży w sposobie ładowania zależności lub uruchamianiu konfiguracji. Oto kilka dodatkowych kroków diagnostycznych i konfiguracji, które mogą pomóc:

### 1. Sprawdź, czy zależność `springdoc-openapi-ui` jest poprawnie zainstalowana

Uruchom w terminalu następującą komendę Maven, aby upewnić się, że zależność została prawidłowo pobrana:

```bash
mvn dependency:tree | grep springdoc
```

Jeśli zależność `springdoc-openapi-ui` nie pojawi się w wynikach, sprawdź plik `pom.xml` i upewnij się, że masz poprawną wersję oraz nie masz konfliktujących zależności.

### 2. Wymuś ponowne pobranie zależności

Spróbuj usunąć folder `target` i uruchomić pełne czyszczenie i budowanie projektu, aby upewnić się, że zależności są aktualne:

```bash
mvn clean install
```

### 3. Sprawdź ustawienia kontekstu i portu

Upewnij się, że aplikacja działa na właściwym porcie (domyślnie 8080) lub że kontekst aplikacji nie jest zmieniony. Sprawdź plik `application-{profile}.properties` pod kątem ustawień takich jak:

```properties
server.port=8080
server.servlet.context-path=/
```

### 4. Przetestuj konfigurację `@Profile` w `SwaggerConfiguration`

Upewnij się, że klasa `SwaggerConfiguration` jest ładowana. Możesz to zrobić, tymczasowo usuwając adnotację `@Profile`, aby sprawdzić, czy sama klasa zostanie załadowana bez względu na profil.

```java
@Configuration
public class SwaggerConfiguration {
    @Bean
    public OpenAPI customOpenAPI() {
        return new OpenAPI()
                .info(new Info()
                        .title("My API")
                        .version("1.0")
                        .description("Opis API"));
    }
}
```

Po uruchomieniu aplikacji sprawdź, czy pojawia się log `Initializing OpenAPI document`.

### 5. Sprawdź, czy aplikacja startuje w odpowiednim profilu

Podczas uruchamiania aplikacji upewnij się, że używany profil jest poprawnie ustawiony. Możesz wymusić profil w konfiguracji Spring Boot, na przykład uruchamiając aplikację z flagą:

```bash
-Dspring.profiles.active=twoj_profil
```

lub w `application.properties` ustawiając:

```properties
spring.profiles.active=twoj_profil
```

### 6. Spróbuj prostszej wersji SpringFox (opcjonalnie)

Jeśli powyższe kroki nadal nie przynoszą rezultatów, możesz przetestować alternatywę w postaci `springfox-swagger2` i `springfox-swagger-ui`:

```xml
<dependency>
    <groupId>io.springfox</groupId>
    <artifactId>springfox-swagger2</artifactId>
    <version>2.9.2</version>
</dependency>
<dependency>
    <groupId>io.springfox</groupId>
    <artifactId>springfox-swagger-ui</artifactId>
    <version>2.9.2</version>
</dependency>
```

Po dodaniu tych zależności, spróbuj ponownie uzyskać dostęp do Swagger UI pod adresem [http://localhost:8080/swagger-ui.html](http://localhost:8080/swagger-ui.html). 

Daj znać, jak poszły te kroki – pomogą w dalszym diagnozowaniu, jeśli problem nadal będzie występował.

---

**User:**

Aplikację uruchamiam z klasy z adnotacją @SpringBootApplication z Intellij przy pomocy opcji Run. Czy to może być problem?

---

**Assistant:**

Uruchamianie aplikacji bezpośrednio z klasy z adnotacją `@SpringBootApplication` w IntelliJ IDEA z opcją **Run** nie powinno być problemem samo w sobie, ale mogą istnieć pewne ustawienia, które wpływają na sposób uruchamiania aplikacji w wybranym profilu. Oto kilka rzeczy, które warto sprawdzić:

### 1. Upewnij się, że profil jest aktywowany w konfiguracji Run

IntelliJ może nie uruchamiać aplikacji w domyślnym profilu, który ustawiłeś w `application.properties` lub `application.yml`. Aby wymusić aktywację wybranego profilu:

1. Przejdź do **Edit Configurations...** w IntelliJ.
2. Wybierz konfigurację aplikacji Spring Boot, którą uruchamiasz.
3. W sekcji **VM options** dodaj parametr aktywujący profil:

   ```bash
   -Dspring.profiles.active=twoj_profil
   ```

4. Zapisz konfigurację i uruchom aplikację ponownie.

### 2. Sprawdź ustawienia IntelliJ związane z Maven

Jeśli projekt korzysta z Maven, upewnij się, że IntelliJ poprawnie zarządza zależnościami. Czasami IntelliJ może przechowywać nieaktualne wersje zależności w pamięci podręcznej. Wykonaj poniższe kroki:

1. W IntelliJ kliknij prawym przyciskiem na projekt i wybierz **Reload Maven Project**.
2. Przejdź do **File > Invalidate Caches / Restart...** i wybierz **Invalidate and Restart**.

### 3. Sprawdź logi podczas startu

Podczas uruchamiania aplikacji powinieneś zobaczyć w logach, który profil został załadowany oraz ewentualne informacje o OpenAPI/Swagger UI. Jeśli profil jest niewłaściwy, możesz nie widzieć logów Swaggera.

### 4. Uruchom aplikację z linii komend (opcjonalnie)

Aby upewnić się, że problem nie leży w IntelliJ, możesz uruchomić aplikację z linii komend, co wykluczy problem z konfiguracją IDE. W głównym katalogu projektu uruchom:

```bash
mvn spring-boot:run -Dspring-boot.run.profiles=twoj_profil
```

Lub, jeśli nie korzystasz z Mavena, bezpośrednio jako `jar`:

```bash
java -jar target/twoj-projekt.jar --spring.profiles.active=twoj_profil
```

### 5. Sprawdź, czy Swagger jest dostępny na właściwym porcie i ścieżce

Po poprawnym uruchomieniu aplikacji, spróbuj uzyskać dostęp do Swagger UI na domyślnym porcie i ścieżce:

- **Swagger UI**: [http://localhost:8080/swagger-ui/index.html](http://localhost:8080/swagger-ui/index.html)
- **OpenAPI JSON**: [http://localhost:8080/v3/api-docs](http://localhost:8080/v3/api-docs)

Przechodząc przez te kroki, powinieneś mieć lepszy wgląd, czy problem wynika z konfiguracji IntelliJ czy ustawień profilowych.