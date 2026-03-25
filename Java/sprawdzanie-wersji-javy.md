# Sprawdzanie wersji Javy

**Data:** 2025-04-20

---

**User:**

mam projekt java z maven złożony z kilku podprojektów/modułów. Jak mogę się dowiedzieć jakiej wersji java używa cały projekt

---

**Assistant:**

W Mavenie wersja Javy używana do kompilacji projektu (czyli tzw. *source* i *target*) jest zazwyczaj określona w pliku `pom.xml`, zwykle w `pom.xml` projektu głównego (roota). Aby sprawdzić, jaka wersja Javy jest używana w całym projekcie, możesz:

---

### 🔍 1. Sprawdzić `maven-compiler-plugin` w głównym `pom.xml`

Znajdź sekcję podobną do tej:

```xml
<build>
  <plugins>
    <plugin>
      <groupId>org.apache.maven.plugins</groupId>
      <artifactId>maven-compiler-plugin</artifactId>
      <version>3.11.0</version> <!-- wersja pluginu -->
      <configuration>
        <source>17</source>
        <target>17</target>
      </configuration>
    </plugin>
  </plugins>
</build>
```

To definiuje wersję Javy, z którą projekt jest kompilowany.

---

### 🔁 2. Alternatywnie – sprawdź `maven.compiler.source` i `maven.compiler.target` w `<properties>`

```xml
<properties>
  <maven.compiler.source>17</maven.compiler.source>
  <maven.compiler.target>17</maven.compiler.target>
</properties>
```

To podejście jest bardziej centralne, bo możesz potem użyć tych właściwości w pluginach albo dziedziczyć je w podmodułach.

---

### 📦 3. Jeśli masz wiele modułów – sprawdź, czy dziedziczą z głównego `pom.xml`

W podmodułach (submodułach) sprawdź, czy nie mają własnych ustawień `maven-compiler-plugin` lub własnych właściwości `maven.compiler.source` – mogą one nadpisywać wersję z głównego POM-a.

---

### 🛠 4. Użyj komendy Maven do sprawdzenia konfiguracji

Możesz uruchomić:

```bash
mvn help:effective-pom
```

Ta komenda pokaże ci „efektywny” POM po uwzględnieniu dziedziczenia, właściwości itp. Wygodnie jest grepować wynik:

```bash
mvn help:effective-pom | grep -A 2 maven-compiler-plugin
```

albo:

```bash
mvn help:effective-pom | grep -A 2 maven.compiler
```

---

### 🧠 Dodatkowo

Wersja JDK, z jaką uruchamiasz Mavena, **nie musi być** taka sama jak `source/target`, ale musi być przynajmniej tak nowa, żeby kompilator Javy mógł wygenerować klasę w odpowiednim formacie. Tzn. żeby kompilować na poziomie `--release 17`, musisz mieć przynajmniej JDK 17 zainstalowane.

---

Chcesz, żebym pomógł Ci przeanalizować konkretny `pom.xml` albo efekt `help:effective-pom`?

---

**User:**

lubię pomysł z mvn help:effective-pom  ale filtrowanie z grep nic mi nie zwraca

---

**Assistant:**

Dobra, to znaczy że prawdopodobnie `maven-compiler-plugin` albo właściwości `maven.compiler.source/target` **nie są jawnie zadeklarowane** w Twoim POM-ie (ani w parentach), więc Maven używa domyślnych ustawień.

---

### 🧠 Domyślne ustawienia `maven-compiler-plugin`:

Jeśli nie zadeklarujesz nic, Maven użyje:

- domyślnej wersji pluginu (`3.1` w starszych Mavenach),
- domyślnej wersji kompilatora (zwykle `1.5` albo `1.6` 🤯 w bardzo starych konfiguracjach!),
- albo tego, co zadeklaruje **parent POM** – np. `spring-boot-starter-parent` ustawia `source/target` na zgodne z wersją Javy w danym Springu.

---

### ✅ Co możesz zrobić zamiast `grep`:

Spróbuj przeszukać wynik `effective-pom` ręcznie (albo z lepszym kontekstem), np.:

```bash
mvn help:effective-pom > eff-pom.xml
```

Potem otwórz `eff-pom.xml` i przeszukaj:

- `maven-compiler-plugin`
- `maven.compiler.source`
- `<source>` / `<target>`

---

### 🔄 Alternatywa: uruchom `mvn compiler:compile -X`

Ta komenda z `-X` (debug) wypisze **dużo logów**, ale gdzieś w nich będzie linijka podobna do:

```
[DEBUG] Using compiler 'javac' with target '17' and source '17'
```

lub:

```
[INFO] Compiling 15 source files to /target/classes
[DEBUG] Source level: 17
[DEBUG] Target level: 17
```

To będzie dokładnie to, czego szukasz.

---

Chcesz, żebym pomógł Ci to przeanalizować? Możesz mi wrzucić `pom.xml` albo wynik `effective-pom` i sprawdzę co się tam dzieje.

---

**User:**

znalazłem  <source default-value="1.8">${maven.compiler.source}</source

---

**Assistant:**

Super! To znaczy, że w `effective-pom` znalazłeś sekcję `maven-compiler-plugin`, a dokładniej jego domyślną konfigurację. Ten fragment:

```xml
<source default-value="1.8">${maven.compiler.source}</source>
```

oznacza:

- Domyślna wartość to `1.8` (czyli Java 8),
- Ale tak naprawdę użyta zostanie **wartość z `${maven.compiler.source}`** – jeśli jest ustawiona gdzieś wyżej.

---

### ✅ Co teraz?

Musisz teraz sprawdzić, **czy i gdzie ustawiono wartość `maven.compiler.source`**. Szukaj w `effective-pom` czegoś takiego:

```xml
<properties>
  <maven.compiler.source>17</maven.compiler.source>
  <maven.compiler.target>17</maven.compiler.target>
</properties>
```

Jeśli tego **nie ma nigdzie**, to Maven przyjmie **domyślną wersję `1.8`**, co może być niezgodne z Twoimi oczekiwaniami, jeśli np. używasz Javy 17 lub 21.

---

### ✏️ Jak ustawić wersję Javy jawnie?

Najprościej: dodaj do głównego `pom.xml` (projektu rootowego):

```xml
<properties>
  <maven.compiler.source>17</maven.compiler.source>
  <maven.compiler.target>17</maven.compiler.target>
</properties>
```

albo, jak chcesz bardziej precyzyjnie:

```xml
<build>
  <plugins>
    <plugin>
      <groupId>org.apache.maven.plugins</groupId>
      <artifactId>maven-compiler-plugin</artifactId>
      <version>3.11.0</version> <!-- lub nowsza -->
      <configuration>
        <source>17</source>
        <target>17</target>
        <!-- albo <release>17</release> -->
      </configuration>
    </plugin>
  </plugins>
</build>
```

---

Jeśli chcesz, mogę rzucić okiem na Twój `pom.xml` i podpowiedzieć dokładnie, gdzie to dodać.