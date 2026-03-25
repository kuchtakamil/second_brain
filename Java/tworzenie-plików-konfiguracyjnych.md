# Tworzenie plików konfiguracyjnych

**Data:** 2025-05-12

---

**User:**

Java + Spring; opisz jak tworzyć pliki ze zmiennymi środowiskowymi

---

**Assistant:**

W Javie z użyciem Springa (szczególnie Spring Boot), zmienne środowiskowe są często używane do konfiguracji aplikacji – np. danych do połączenia z bazą, tajnych kluczy czy trybu działania aplikacji. Spring umożliwia wiele sposobów na ich zdefiniowanie i użycie. Poniżej opisuję, jak je tworzyć i wykorzystywać:

---

### 🔧 1. **Plik `application.properties` lub `application.yml`**

To domyślne miejsce na konfigurację w Spring Boot.

#### `application.properties`
```properties
app.name=MyApp
app.env=dev
```

#### `application.yml`
```yaml
app:
  name: MyApp
  env: dev
```

W kodzie:
```java
@Value("${app.name}")
private String appName;
```

Lub przez klasę konfiguracyjną:
```java
@ConfigurationProperties(prefix = "app")
@Component
public class AppConfig {
    private String name;
    private String env;
    // gettery i settery
}
```

---

### 🌍 2. **Zmienna środowiskowa systemu operacyjnego**

Można ustawić np. w Linuxie:
```bash
export APP_NAME=MyApp
```

A w Springu:
```java
@Value("${APP_NAME}")
private String appName;
```

Spring najpierw szuka w plikach `.properties`, potem w zmiennych środowiskowych, potem w parametrach JVM (`-D...`), ale można to nadpisać przez `application.properties`.

---

### 🧩 3. **Plik `.env` (gdy używasz np. Docker lub dotenv)**

Spring Boot natywnie **nie obsługuje** `.env`, ale można użyć biblioteki [dotenv-java](https://github.com/cdimascio/dotenv-java) lub odczytywać je ręcznie.

Alternatywnie, Docker Compose może ładować `.env` i przekazywać je jako zmienne środowiskowe.

---

### 💡 4. **Pliki `application-{profile}.properties/yml`**

Przydatne przy wielu środowiskach (np. `dev`, `prod`, `test`).

Struktura:
```
application.properties       # ustawienia ogólne
application-dev.yml          # środowisko dev
application-prod.yml         # środowisko prod
```

Uruchamiasz z profilem:
```bash
java -Dspring.profiles.active=dev -jar app.jar
```

---

### 📦 5. **Zmienna przekazywana przez JVM (`-D`)**

```bash
java -Dapp.name=MyApp -jar app.jar
```

---

### ✅ Dobre praktyki

- **Sekrety (np. hasła)** trzymaj poza repozytorium – najlepiej w zmiennych środowiskowych lub managerze sekretów (np. AWS Secrets Manager).
- **Profile środowiskowe** (`spring.profiles.active`) pozwalają łatwo zmieniać konfiguracje między np. `dev`, `test`, `prod`.
- **Nie wrzucaj `.env` do repo**, jeśli zawiera sekrety.

---

Chcesz przykład z Dockerem albo plik `.env` z podpięciem do Springa?

---

**User:**

tak

---

**Assistant:**

Świetnie — oto przykład jak zintegrować plik `.env` z aplikacją Spring Boot działającą w **Dockerze**. Pokażę to krok po kroku:

---

## ✅ 1. Struktura katalogów
```
my-app/
├── src/
├── Dockerfile
├── .env
├── application.properties
├── docker-compose.yml
└── pom.xml
```

---

## 📝 2. Plik `.env`

Plik `.env` będzie zawierał zmienne środowiskowe (nie wersjonuj go w Git!):

```env
APP_NAME=MyEnvApp
APP_PORT=8081
```

---

## 🧾 3. Plik `application.properties` w Spring Boot

```properties
app.name=${APP_NAME:DefaultApp}
server.port=${APP_PORT:8080}
```

Dzięki `${...:default}` możesz podać wartość domyślną, jeśli zmienna nie zostanie znaleziona.

---

## 🐳 4. Plik `docker-compose.yml`

```yaml
version: '3.8'

services:
  myapp:
    build: .
    ports:
      - "${APP_PORT}:8080"
    env_file:
      - .env
    environment:
      - APP_NAME
      - APP_PORT
```

---

## 🐳 5. Dockerfile (prosty Spring Boot)

```Dockerfile
FROM openjdk:17
ARG JAR_FILE=target/my-app.jar
COPY ${JAR_FILE} app.jar
ENTRYPOINT ["java", "-jar", "/app.jar"]
```

---

## ▶️ 6. Budowanie i uruchamianie

```bash
# budujemy jar
mvn clean package

# uruchamiamy z Docker Compose
docker-compose up --build
```

---

## 🧪 7. Weryfikacja

Utwórz kontroler testowy:

```java
@RestController
public class EnvController {

    @Value("${app.name}")
    private String appName;

    @GetMapping("/env")
    public String getAppName() {
        return "App name from env: " + appName;
    }
}
```

Wejdź na `http://localhost:8081/env`, powinieneś zobaczyć:  
`App name from env: MyEnvApp`

---

Chcesz przykład z użyciem `dotenv-java` (czyli działającym też poza Dockerem lokalnie)?

---

**User:**

W intellij można w okienkach ustawić Environmental Variables.  A gdybym chciał to mieć w pliku zamiast w okienku w intellij to jaki jest plikowy odpowiednik?

---

**Assistant:**

Tak, w IntelliJ IDEA możesz ręcznie ustawiać zmienne środowiskowe w konfiguracji run/debug (okienko `Run -> Edit Configurations…`). Ale jeśli chcesz **zamiast tego używać pliku**, możesz osiągnąć to na kilka sposobów — ale ważne: **IntelliJ nie obsługuje plików `.env` domyślnie** w konfiguracji aplikacji Java.

### 🔹 Sposób 1: Plugin `.env files support` (zalecany)

1. Zainstaluj plugin: `Settings > Plugins > Marketplace > .env files support`
2. Umieść plik `.env` w katalogu głównym projektu, np.:

   ```env
   APP_NAME=MyAppFromDotEnv
   SPRING_PROFILES_ACTIVE=dev
   ```

3. Plugin może automatycznie załadować zmienne lub ustawić je w oknie konfiguracji IntelliJ (podgląd: „Environment variables”).

   > UWAGA: Plugin nie działa z każdą konfiguracją, a niektóre typy aplikacji wymagają ręcznego wskazania pliku `.env`.

---

### 🔹 Sposób 2: Ręczne źródło `.env` w skrypcie uruchamiającym

Utwórz plik `run.sh`:

```bash
#!/bin/bash
export $(grep -v '^#' .env | xargs)
java -jar target/my-app.jar
```

Plik `.env`:

```env
APP_NAME=MyApp
APP_PORT=8080
```

I uruchamiaj aplikację przez ten skrypt (z terminala albo z IntelliJ jako "External Tool").

---

### 🔹 Sposób 3: Ustawianie zmiennych JVM z pliku (`.vmoptions`)

Możesz przekazać wartości z pliku `.env` jako opcje JVM:

1. Utwórz plik `my.env`:

   ```env
   -DAPP_NAME=MyApp
   -DSPRING_PROFILES_ACTIVE=dev
   ```

2. W IntelliJ, wejdź w:
   `Run > Edit Configurations > VM Options`

   I zrób coś takiego:

   ```text
   @path/to/my.env
   ```

   IntelliJ odczyta wtedy opcje z pliku.

---

### 🔹 Sposób 4: `application.properties` wczytywany ręcznie

To podejście "springowe", ale nie dotyczy `Environment Variables`, tylko konfiguracji.

---

## 🧾 Podsumowanie

| Metoda                | Typ zmiennych        | Kompatybilność | Wygoda |
|-----------------------|----------------------|----------------|--------|
| `.env` + plugin       | Env vars             | IntelliJ + plugin | 👍 |
| Skrypt bash (`run.sh`) | Env vars             | niezależne od IDE | 👍👍 |
| `.vmoptions` z `-D...`| JVM system properties| natywne IntelliJ | ✅ |
| `application.properties` | Spring config     | tylko Spring Boot | 🔄 |

---

Chcesz żebym przygotował gotowy `run.sh` lub przykład `.env` i jak go połączyć ze Springiem w zwykłym lokalnym uruchomieniu?