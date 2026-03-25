# Maven BOM wyjaśnienie

**Data:** 2024-11-11

---

**User:**

W kontekście maven, co to jest BOM?

---

**Assistant:**

BOM, czyli **Bill of Materials** w kontekście Maven, to specjalny plik pom.xml, który służy do zarządzania zależnościami w projekcie. BOM pomaga utrzymywać zgodność wersji w projekcie, szczególnie gdy korzystamy z wielu modułów lub bibliotek wchodzących w skład jednego większego frameworka lub zestawu narzędzi.

### Dlaczego warto używać BOM?
Często zdarza się, że zależności w projekcie Maven mają dodatkowe własne zależności, które mogą być w różnych wersjach. W takich przypadkach BOM pomaga unikać konfliktów wersji i zapewnia, że wszystkie zależności są w odpowiednich, zgodnych ze sobą wersjach.

Przykładem często używanego BOM-a jest **Spring Boot BOM**, który pozwala kontrolować wersje wszystkich bibliotek wchodzących w skład Spring Boot. Dzięki temu można łatwo uniknąć problemów z kompatybilnością pomiędzy wersjami różnych modułów Springa.

### Jak używać BOM w Maven?
Aby użyć BOM, dodajemy go do sekcji `<dependencyManagement>` w pliku `pom.xml` projektu. W BOM nie określa się wersji poszczególnych zależności bezpośrednio w `<dependencies>`, tylko w `<dependencyManagement>`, a później same zależności można dodawać już bez podawania wersji. BOM automatycznie zaciągnie odpowiednią wersję.

Przykład użycia Spring Boot BOM:

```xml
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-dependencies</artifactId>
            <version>3.0.0</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>
```

Po dodaniu tego BOM-a, można dodawać zależności Spring Boot (np. `spring-boot-starter-web`) bez określania wersji, a projekt zawsze użyje wersji zgodnej z podaną w BOM.