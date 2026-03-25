# Pluginy Maven

**Data:** 2025-06-14

---

**User:**

Wymień pluginy do Mavena, które stosuje się bardzo często, takie np. jak Maven Compiler Plugin.

---

**Assistant:**

Oczywiście! Oto lista **najczęściej stosowanych pluginów do Mavena**, które są używane w większości projektów Java:

---

### 🔧 **Podstawowe i bardzo często używane**

1. **[maven-compiler-plugin](https://maven.apache.org/plugins/maven-compiler-plugin/)**
   - Kompilacja kodu źródłowego.
   - Pozwala ustawić wersje języka Java (`source` i `target`).

   ```xml
   <plugin>
     <groupId>org.apache.maven.plugins</groupId>
     <artifactId>maven-compiler-plugin</artifactId>
     <version>3.11.0</version>
     <configuration>
       <source>17</source>
       <target>17</target>
     </configuration>
   </plugin>
   ```

2. **[maven-surefire-plugin](https://maven.apache.org/surefire/maven-surefire-plugin/)**
   - Uruchamianie testów jednostkowych (`mvn test`).

3. **[maven-failsafe-plugin](https://maven.apache.org/surefire/maven-failsafe-plugin/)**
   - Do testów integracyjnych (często z `verify`, np. `mvn verify`).
   - Używany razem z `maven-surefire-plugin`, ale dla testów kończących się na `IT`.

4. **[maven-jar-plugin](https://maven.apache.org/plugins/maven-jar-plugin/)**
   - Buduje plik `.jar`.
   - Czasem konfigurowany, np. do ustawienia `Main-Class`.

5. **[maven-clean-plugin](https://maven.apache.org/plugins/maven-clean-plugin/)**
   - Czyści katalog `target` (używany w `mvn clean`).

6. **[maven-install-plugin](https://maven.apache.org/plugins/maven-install-plugin/)**
   - Instalacja artefaktu do lokalnego repozytorium (`mvn install`).

7. **[maven-deploy-plugin](https://maven.apache.org/plugins/maven-deploy-plugin/)**
   - Wysyła artefakt do zdalnego repozytorium (np. Nexus, Artifactory).

---

### 📦 **Do zarządzania zależnościami i budowaniem**

8. **[maven-dependency-plugin](https://maven.apache.org/plugins/maven-dependency-plugin/)**
   - Operacje na zależnościach: kopiowanie, rozpakowywanie, wyświetlanie drzewa zależności (`dependency:tree`).

9. **[maven-resources-plugin](https://maven.apache.org/plugins/maven-resources-plugin/)**
   - Kopiowanie i filtrowanie zasobów (`src/main/resources`).

10. **[maven-site-plugin](https://maven.apache.org/plugins/maven-site-plugin/)**
    - Generowanie dokumentacji projektu (`mvn site`).

---

### 🚀 **Do uruchamiania aplikacji**

11. **[exec-maven-plugin](https://www.mojohaus.org/exec-maven-plugin/)**
    - Uruchamianie dowolnego programu, klasy Javy itd.
    - Przydatne np. w czasie developmentu.

12. **[spring-boot-maven-plugin](https://docs.spring.io/spring-boot/docs/current/maven-plugin/)**
    - Uruchamianie aplikacji Spring Boot (`mvn spring-boot:run`) i tworzenie fat JAR (`repackage`).

---

### 📦 **Inne często spotykane**

13. **[maven-enforcer-plugin](https://maven.apache.org/enforcer/maven-enforcer-plugin/)**
    - Wymusza reguły np. wersje JDK, wersje pluginów, zależności itp.

14. **[build-helper-maven-plugin](https://www.mojohaus.org/build-helper-maven-plugin/)**
    - Dodawanie źródeł, zasobów itp. do kompilacji — np. `src/generated/java`.

15. **[maven-assembly-plugin](https://maven.apache.org/plugins/maven-assembly-plugin/)**
    - Tworzy archiwa ZIP, JAR, itp. z wieloma komponentami (np. z zależnościami).

16. **[maven-shade-plugin](https://maven.apache.org/plugins/maven-shade-plugin/)**
    - Tworzy tzw. uber/fat JAR z wszystkimi zależnościami. Przydatne w mikroserwisach, aplikacjach CLI, AWS Lambda itd.

---

Jeśli chcesz, mogę przygotować dla Ciebie przykładowy `pom.xml` z typowym zestawem pluginów dla projektu Java/Spring Boot lub innego typu.