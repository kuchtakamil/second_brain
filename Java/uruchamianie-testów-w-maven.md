# Uruchamianie testów w Maven

**Data:** 2025-02-16

---

**User:**

jak w maven mogę uruchomić konkretny unit test?

---

**Assistant:**

W Mavenie możesz uruchomić konkretny unit test na kilka sposobów:

### 1. **Użycie parametru `-Dtest`**
Najprostszy sposób to użycie flagi `-Dtest` i podanie nazwy testu:

```sh
mvn test -Dtest=NazwaTestu
```

Przykłady:
```sh
mvn test -Dtest=MyUnitTest
mvn test -Dtest=MyUnitTest#specificMethod
```
Drugi przykład uruchomi tylko metodę `specificMethod` z klasy `MyUnitTest`.

### 2. **Użycie Surefire Plugin (`maven-surefire-plugin`)**
Maven używa **Surefire Plugin** do uruchamiania testów. Możesz jawnie podać test w `pom.xml`:

```xml
<build>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-surefire-plugin</artifactId>
            <version>3.1.2</version>
            <configuration>
                <includes>
                    <include>**/MyUnitTest.java</include>
                </includes>
            </configuration>
        </plugin>
    </plugins>
</build>
```
I uruchomić:
```sh
mvn test
```

### 3. **Uruchamianie wielu testów**
Jeśli chcesz uruchomić kilka testów:
```sh
mvn test -Dtest=TestClass1,TestClass2
```

Lub testy pasujące do wzorca (np. wszystkie zaczynające się od `MyTest`):
```sh
mvn test -Dtest=MyTest*
```

### 4. **Użycie `-DfailIfNoTests=false`**
Jeżeli Maven nie znajduje testów, może wyświetlać błąd. Możesz temu zapobiec:
```sh
mvn test -Dtest=MyUnitTest -DfailIfNoTests=false
```

To powinno wystarczyć. Jeśli masz jakąś specyficzną konfigurację, daj znać! 🚀