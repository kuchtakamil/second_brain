# Maven JAXBException Fix

**Data:** 2024-12-02

---

**User:**

Przy mvn install dostaję błąd
 Failed to execute goal org.apache.maven.plugins:maven-enforcer-plugin:1.4.1:enforce (enforce) on project ipt-shared-ui-v2: Execution enforce of goal org.apache.maven.plugins:maven-enforcer-plugin:1.4.1:enforce failed: A required class was missing while executing org.apache.maven.plugins:maven-enforcer-plugin:1.4.1:enforce: javax/xml/bind/JAXBException

---

**Assistant:**

Błąd, który widzisz, wynika z faktu, że `javax.xml.bind.JAXBException` nie jest już domyślnie dostępny w JDK od wersji 9 wzwyż. W JDK 9 i późniejszych, moduły JAXB zostały usunięte z JDK i przeniesione do osobnej biblioteki.

### Rozwiązania:

#### 1. **Dodanie zależności do JAXB w projekcie**
Jeśli Twój projekt wymaga JAXB, musisz dodać odpowiednie zależności do `pom.xml`:

```xml
<dependencies>
    <!-- JAXB API -->
    <dependency>
        <groupId>javax.xml.bind</groupId>
        <artifactId>jaxb-api</artifactId>
        <version>2.3.1</version>
    </dependency>
    <!-- Implementacja JAXB -->
    <dependency>
        <groupId>com.sun.xml.bind</groupId>
        <artifactId>jaxb-impl</artifactId>
        <version>2.3.1</version>
    </dependency>
    <!-- Narzędzia JAXB -->
    <dependency>
        <groupId>com.sun.xml.bind</groupId>
        <artifactId>jaxb-core</artifactId>
        <version>2.3.1</version>
    </dependency>
</dependencies>
```

#### 2. **Dodanie argumentów JVM przy budowie projektu**
Jeśli chcesz uniknąć modyfikacji `pom.xml` i używasz JDK 9+, możesz dodać JAXB do swojej aplikacji podczas jej uruchamiania za pomocą modułów Java:

```bash
mvn clean install -DargLine="--add-modules java.xml.bind"
```

#### 3. **Przejście na nowszą wersję wtyczki Maven Enforcer Plugin**
Sprawdź, czy jest dostępna nowsza wersja wtyczki `maven-enforcer-plugin`. Czasami problem może być rozwiązany przez aktualizację:

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-enforcer-plugin</artifactId>
    <version>3.0.0</version>
    <executions>
        <execution>
            <id>enforce</id>
            <goals>
                <goal>enforce</goal>
            </goals>
        </execution>
    </executions>
</plugin>
```

#### 4. **Użycie JDK 8**
Jeśli Twój projekt nie wymaga nowszych wersji JDK, tymczasowym rozwiązaniem może być użycie JDK 8, gdzie JAXB jest wbudowane.

#### 5. **Weryfikacja konfiguracji Maven**
Sprawdź konfigurację wtyczki Maven Enforcer Plugin w swoim `pom.xml`. Możliwe, że zawiera ustawienia wymagające aktualizacji.

Jeśli potrzebujesz dodatkowej pomocy, prześlij fragment swojego `pom.xml` lub więcej szczegółów dotyczących konfiguracji projektu. 😊