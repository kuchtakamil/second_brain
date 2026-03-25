# Gradle Dependencies: Key Concepts

**Data:** 2023-12-18

---

**User:**

W gradle definiując dependencies mogę napisać implementation nazwa zależności. Co oznacza tu implementation i jakie są jeszcze inne możliwości?

---

**Assistant:**

W systemie budowania Gradle, słowo kluczowe `implementation` jest jednym z kilku sposobów definiowania zależności w projekcie. Oznacza ono, że dana zależność jest używana tylko wewnątrz danego modułu (projektu) i nie jest eksportowana na zewnątrz, co oznacza, że nie będzie dostępna dla innych modułów, które zależą od tego modułu.

Oprócz `implementation`, istnieją inne słowa kluczowe, które można użyć w sekcji `dependencies` w pliku `build.gradle`. Oto kilka z nich:

1. **api**: Zależności oznaczone jako `api` są widoczne dla zewnętrznych modułów, które korzystają z danego modułu. Są one eksportowane na zewnątrz.

    ```gradle
    api 'com.example:library:1.0'
    ```

2. **compileOnly**: Zależności oznaczone jako `compileOnly` są dostępne tylko podczas kompilacji i nie są dostępne podczas wykonywania (runtime). 

    ```gradle
    compileOnly 'com.example:dependency:1.0'
    ```

3. **runtimeOnly**: Zależności oznaczone jako `runtimeOnly` są dostępne tylko podczas wykonywania i nie są dostępne podczas kompilacji.

    ```gradle
    runtimeOnly 'com.example:dependency:1.0'
    ```

4. **testImplementation**: Zależności oznaczone jako `testImplementation` są używane tylko podczas wykonywania testów jednostkowych.

    ```gradle
    testImplementation 'junit:junit:4.12'
    ```

5. **androidTestImplementation**: Zależności oznaczone jako `androidTestImplementation` są używane tylko podczas wykonywania testów na poziomie Androida.

    ```gradle
    androidTestImplementation 'com.android.support.test.espresso:espresso-core:3.0.2'
    ```

Dokładne znaczenie tych słów kluczowych zależy od tego, czy pracujesz nad projektem Java, Android, czy innym rodzajem projektu obsługiwanego przez Gradle. Warto zauważyć, że `implementation` jest często używane w kontekście projektów Java.

---

**User:**

Co oznacza że zależności są dostępne tylko podczas wykonywania i nie są dostępne podczas kompilacji?

---

**Assistant:**

Kiedy mówimy, że zależności są dostępne tylko podczas wykonywania i nie są dostępne podczas kompilacji, odnosi się to do etapów procesu budowania oprogramowania. W języku Java, ten proces zazwyczaj składa się z dwóch głównych etapów: kompilacji i wykonania.

1. **Kompilacja**: W tym etapie kod źródłowy jest przekształcany z postaci czytelnej dla programisty na postać zrozumiałą dla maszyny wirtualnej Java (JVM). Kompilacja sprawdza poprawność składniową i semantyczną kodu, ale nie wykonuje go. W tym etapie kompilator tworzy pliki bytecode.

2. **Wykonywanie (Runtime)**: W tym etapie pliki bytecode są wykonywane na maszynie wirtualnej Java, co prowadzi do faktycznego działania programu.

Terminy `compileOnly` i `runtimeOnly` w Gradle odnoszą się do tego podziału.

- **compileOnly**: Zależności oznaczone jako `compileOnly` są dostępne tylko podczas kompilacji. Oznacza to, że są one potrzebne tylko w czasie kompilacji, ale nie są wymagane do uruchomienia programu. Te zależności nie są dołączane do pliku JAR ani nie są dostępne podczas faktycznego wykonania programu. Są one używane głównie do rozwiązania problemów związanych z kompilacją.

    ```gradle
    compileOnly 'com.example:dependency:1.0'
    ```

- **runtimeOnly**: Zależności oznaczone jako `runtimeOnly` są dostępne tylko podczas wykonywania programu. Oznacza to, że są one potrzebne tylko w czasie wykonania, ale nie są konieczne podczas kompilacji. Są one używane do dostarczania zasobów potrzebnych podczas uruchomienia programu, ale które nie są wymagane w czasie kompilacji.

    ```gradle
    runtimeOnly 'com.example:dependency:1.0'
    ```

Użycie odpowiedniego słowa kluczowego zależy od wymagań projektu i od tego, czy dana zależność jest potrzebna tylko podczas kompilacji, tylko podczas wykonania, czy w obu przypadkach.