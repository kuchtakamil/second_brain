# Logowanie w Spring Boot

**Data:** 2024-12-02

---

**User:**

mam aplikację w springboot która uruchamia się w intellij ale nic nie loguje oprócz loga spring boota. Mam plik application.properties. Widzę też pliki logback.xml i logback-local.xml

---

**Assistant:**

Jeśli Twoja aplikacja w Spring Boot loguje jedynie logo Spring Boot i nic więcej, to problem może leżeć w konfiguracji loggera (Logback w Twoim przypadku). Spring Boot domyślnie korzysta z Logbacka, ale pliki `logback.xml` i `logback-local.xml` mogą nadpisywać tę konfigurację. Oto kilka kroków, które pomogą zdiagnozować problem:

---

### 1. **Sprawdź zawartość plików `logback.xml` i `logback-local.xml`**
- Upewnij się, że konfiguracja w tych plikach pozwala na logowanie na odpowiednim poziomie (np. `INFO` lub `DEBUG`).
- Jeśli istnieją wykluczenia lub filtry, mogą one blokować logowanie.
- Przykładowa minimalna konfiguracja w `logback.xml`:

```xml
<configuration>
    <appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender">
        <encoder>
            <pattern>%d{yyyy-MM-dd HH:mm:ss} %-5level %logger{36} - %msg%n</pattern>
        </encoder>
    </appender>

    <root level="INFO">
        <appender-ref ref="CONSOLE" />
    </root>
</configuration>
```

---

### 2. **Sprawdź aktywny profil**
- Spring Boot może używać różnych plików konfiguracyjnych w zależności od aktywnego profilu. Upewnij się, że Twój plik `logback-local.xml` nie jest wybrany przez przypadek, np. za pomocą zmiennej `spring.profiles.active` w `application.properties`.
- Możesz wymusić konkretny profil w `application.properties`:
  ```properties
  spring.profiles.active=default
  ```

---

### 3. **Ustaw poziom logowania w `application.properties`**
Możesz ustawić poziom logowania w pliku `application.properties`, niezależnie od konfiguracji Logbacka. Dodaj poniższe linie, aby wymusić odpowiednie poziomy logowania:

```properties
logging.level.root=INFO
logging.level.org.springframework=DEBUG
logging.level.your.package=TRACE
```

Zastąp `your.package` Twoim głównym pakietem aplikacji.

---

### 4. **Sprawdź, czy Logback jest poprawnie załadowany**
Możesz sprawdzić, czy Logback jest używany jako framework logowania, dodając zależność w `pom.xml`:

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-logging</artifactId>
</dependency>
```

Spring Boot automatycznie instaluje tę zależność, ale jeśli została ręcznie wyłączona, może powodować brak logowania.

---

### 5. **Uruchom aplikację w trybie DEBUG**
Uruchom aplikację w trybie debugowania, aby zobaczyć, czy pojawiają się dodatkowe informacje:

```bash
mvn spring-boot:run -Dspring-boot.run.jvmArguments="-Dlogging.level.root=DEBUG"
```

---

### 6. **Użyj `-Dspring.output.ansi.enabled=always`**
Jeśli Twój terminal obsługuje kolory ANSI, spróbuj włączyć kolorowe logi dla lepszej czytelności:
```bash
-Dspring.output.ansi.enabled=always
```

---

### 7. **Usuń tymczasowo niestandardowe konfiguracje**
Aby zweryfikować, czy problem leży w konfiguracji `logback.xml` lub `logback-local.xml`, spróbuj tymczasowo usunąć te pliki. Jeśli logowanie zacznie działać, problem jest w ich konfiguracji.

---

Jeśli problem nadal występuje, podziel się przykładową zawartością plików `logback.xml` oraz `application.properties`, abyśmy mogli lepiej pomóc.