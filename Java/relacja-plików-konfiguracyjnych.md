# Relacja plików konfiguracyjnych

**Data:** 2025-04-07

---

**User:**

w aplikacji spring mam dwa pliki yaml: application.yaml i application-hosted.yaml. Na działąjącej aplikacji mogę znaleźć plik lib/application-hosted.properties który jest zapełniony. Jaka jest ich relacja?

---

**Assistant:**

W Spring Boot relacja między plikami `application.yaml`, `application-hosted.yaml` i `application-hosted.properties` może wynikać z mechanizmu profili oraz sposobu ładowania konfiguracji przez Springa. Oto jak można to zinterpretować:

---

### 1. **`application.yaml`**
To główny plik konfiguracyjny aplikacji. Zawiera domyślne ustawienia, które są ładowane niezależnie od wybranego profilu.

---

### 2. **`application-hosted.yaml`**
To plik konfiguracji dla profilu `hosted`. Jest ładowany tylko wtedy, gdy profil `hosted` jest aktywowany, np. przez:

```bash
-Dspring.profiles.active=hosted
```

albo w `application.yaml`:

```yaml
spring:
  profiles:
    active: hosted
```

---

### 3. **`lib/application-hosted.properties`**
Ten plik wygląda jak runtime’owy artefakt. Możliwe scenariusze:

#### a) **Zamiana YAML na properties podczas builda**
Niektóre build systemy (np. Gradle z niektórymi pluginami, Maven) mogą konwertować `application-hosted.yaml` na `application-hosted.properties`, by użyć go np. w zewnętrznej lokalizacji (np. w `lib/`).

#### b) **Zewnętrzna konfiguracja**
Spring Boot pozwala na ładowanie zewnętrznych plików `.properties`. Jeśli np. aplikacja uruchamiana jest z:

```bash
java -jar app.jar --spring.config.location=lib/
```

to `application-hosted.properties` z katalogu `lib/` może być nadrzędny względem zasobów z JARa i nadpisywać wartości z `application.yaml` i `application-hosted.yaml`.

---

### 🔍 Jak sprawdzić co jest ładowane?

1. **Włącz logowanie konfiguracji**:
   Dodaj do `application.yaml`:

   ```yaml
   logging:
     level:
       org.springframework.boot.context.config: DEBUG
   ```

   W logach zobaczysz kolejność i źródła ładowanych plików.

2. **Sprawdź aktywne profile**:
   Sprawdź w logach lub dodaj do kontrolera:

   ```java
   @Value("${spring.profiles.active}")
   private String activeProfile;
   ```

---

### Podsumowanie

| Plik                           | Opis |
|-------------------------------|------|
| `application.yaml`            | Domyślna konfiguracja |
| `application-hosted.yaml`     | Konfiguracja dla profilu `hosted` |
| `lib/application-hosted.properties` | Możliwe źródło zewnętrznej konfiguracji dla profilu `hosted`, ładowane spoza JARa |

Jeśli chcesz, możemy razem sprawdzić jak Spring ładuje te pliki w Twoim przypadku — wystarczy log z uruchomienia albo struktura projektu.