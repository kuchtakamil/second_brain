# Uruchamianie Spring Boot lokalnie

**Data:** 2024-11-28

---

**User:**

Mam aplikację SpringBoot oraz pliki application.yaml, application-local.yaml. Jak mogę uruchomić ten projekt lokalnie w intellij?

---

**Assistant:**

Aby uruchomić aplikację Spring Boot w środowisku lokalnym w IntelliJ z wykorzystaniem różnych plików konfiguracyjnych (np. `application.yaml` i `application-local.yaml`), wykonaj następujące kroki:

### 1. **Ustaw aktywny profil w IntelliJ**
Spring Boot korzysta z profili, aby wybierać odpowiednie pliki konfiguracyjne. Profil `local` będzie aktywował `application-local.yaml`.

#### Kroki:
1. Otwórz IntelliJ.
2. Przejdź do zakładki **Run/Debug Configurations** (u góry, obok przycisków uruchamiania).
3. Kliknij przycisk **+** (lub wybierz istniejącą konfigurację Spring Boot).
4. W polu **VM Options** lub **Program Arguments** dodaj:
   ```
   --spring.profiles.active=local
   ```
5. Zapisz konfigurację.

### 2. **Upewnij się, że pliki konfiguracyjne są poprawne**
- Plik `application.yaml` zawiera ustawienia globalne, które będą ładowane zawsze.
- Plik `application-local.yaml` zawiera ustawienia specyficzne dla profilu `local`.
- Upewnij się, że struktura plików YAML jest poprawna, np.:
  ```yaml
  # application.yaml
  spring:
    datasource:
      url: jdbc:mysql://localhost:3306/mydb
      username: root
      password: root
  ---
  # application-local.yaml
  spring:
    datasource:
      url: jdbc:mysql://localhost:3306/mydb_local
      username: localuser
      password: localpass
  ```

### 3. **Uruchom aplikację**
1. Wybierz utworzoną konfigurację Run/Debug w IntelliJ.
2. Kliknij **Run** (zielony trójkąt).
3. Aplikacja powinna się uruchomić z użyciem pliku `application.yaml` oraz ustawień z `application-local.yaml` (dzięki profilowi `local`).

### 4. **Sprawdź logi**
Podczas uruchamiania w logach aplikacji zobaczysz aktywny profil, np.:
```
The following profiles are active: local
```

### 5. **Inne przydatne porady**
- Jeśli plik `application-local.yaml` nie działa, sprawdź czy w głównym pliku `application.yaml` nie ma ustawionych innych profili. Możesz wyczyścić:
  ```yaml
  spring:
    profiles:
      active:
  ```
- Możesz także podać profil bezpośrednio w terminalu:
  ```bash
  ./mvnw spring-boot:run -Dspring-boot.run.profiles=local
  ```

---

**User:**

Unrecognized option: --spring.profiles.active=local 

---

**Assistant:**

Problem z błędem „Unrecognized option” wynika z niewłaściwego miejsca, w którym dodano opcję `--spring.profiles.active=local`. To polecenie powinno znaleźć się w sekcji **Program Arguments**, a nie w **VM Options**. Oto jak to poprawić w IntelliJ:

---

### **Kroki do poprawnego uruchomienia z profilem lokalnym:**

#### 1. **Otwórz konfigurację uruchamiania**
- W IntelliJ kliknij na **Edit Configurations** w menu rozwijanym obok zielonego przycisku uruchamiania.

#### 2. **Dodaj profil w polu „Program Arguments”**
- Upewnij się, że w konfiguracji Spring Boot:
  - W polu **Program Arguments** (nie VM Options) dodasz:
    ```
    --spring.profiles.active=local
    ```

#### 3. **Nie umieszczaj tej opcji w „VM Options”**
- **VM Options** służy do dodawania opcji JVM (np. `-Xmx512m`), a nie argumentów programu.

#### 4. **Zapisz i uruchom**
- Zapisz zmiany i spróbuj ponownie uruchomić aplikację.

---

### **Jak wygląda pełna konfiguracja w IntelliJ?**
1. **Program Arguments:**
   ```
   --spring.profiles.active=local
   ```
2. **VM Options:** *(opcjonalne, tylko jeśli potrzebujesz ustawić JVM)*
   ```
   -Xmx512m -Xms256m
   ```
3. **Main class:** Twoja główna klasa (np. `com.example.Application`).
4. **Classpath:** Twój projekt (ustawienia domyślne IntelliJ).

---

### **Jeśli nadal masz problem:**
1. Spróbuj uruchomić aplikację z profilu lokalnego bez IntelliJ:
   ```bash
   ./mvnw spring-boot:run -Dspring-boot.run.arguments="--spring.profiles.active=local"
   ```
   lub, jeśli używasz Gradle:
   ```bash
   ./gradlew bootRun --args="--spring.profiles.active=local"
   ```

2. Sprawdź, czy `application-local.yaml` istnieje w katalogu `resources` i ma poprawną strukturę. Spring Boot automatycznie ładuje pliki z katalogu `resources`.

Daj znać, jeśli coś jest niejasne!

---

**User:**

czy w VM Options nie da się podać profilu używająć -D....?

---

**Assistant:**

Tak, możesz ustawić profil Spring Boot w **VM Options** w IntelliJ za pomocą opcji `-Dspring.profiles.active=local`. Jest to poprawne i często używane podejście.

---

### **Jak skonfigurować profil w VM Options?**
1. Otwórz **Edit Configurations** w IntelliJ.
2. W sekcji **VM Options** dodaj:
   ```
   -Dspring.profiles.active=local
   ```
3. Zapisz i uruchom aplikację.

---

### **Jak to działa?**
- Flaga `-Dspring.profiles.active=local` ustawia właściwość systemową JVM, która jest odczytywana przez Spring Boot podczas uruchamiania.
- To równoważne podaniu opcji `--spring.profiles.active=local` jako **Program Arguments**, ale działa na poziomie JVM.

---

### **Różnica między VM Options a Program Arguments**
1. **VM Options**: Dotyczą maszyny wirtualnej JVM (np. `-Xmx`, `-D`).
   - Przykład: `-Dspring.profiles.active=local`
2. **Program Arguments**: Argumenty przekazywane do aplikacji na poziomie kodu.
   - Przykład: `--spring.profiles.active=local`

Obie metody są poprawne, ale `-D` w VM Options może być bardziej uniwersalne, np. gdy profil jest potrzebny również w trakcie debugowania lub podczas uruchamiania z Maven/Gradle.

---

### **Sprawdzenie w logach**
Po uruchomieniu aplikacji sprawdź logi. Powinieneś zobaczyć aktywny profil:
```
The following profiles are active: local
```

Daj znać, jeśli masz dodatkowe pytania! 😊