# Gitignore dla IntelliJ i Maven.

**Data:** 2023-08-05

---

**User:**

wygeneruj zawartość .gitignore dla projektu w intellij, maven itp

---

**Assistant:**

Oto przykładowa zawartość pliku .gitignore dla projektu Java stworzonego w IntelliJ i używającego Maven:

```
# IntelliJ IDE
.idea/

# Maven
target/
pom.xml.tag
pom.xml.releaseBackup
pom.xml.versionsBackup
pom.xml.next
release.properties
dependency-reduced-pom.xml
buildNumber.properties
.mvn/timing.properties

# Compiled Java files
*.class

# Compiled Java source files
*.java~

# Compiled Kotlin files
*.kotlin_builtins

# Compiled Kotlin source files
*.kt~

# Compiled Groovy files
*.class

# Compiled Groovy source files
*.groovy~

# Eclipse IDE
.classpath
.project
.settings/

# NetBeans IDE
/nbproject/private/
/build/
/nbbuild/
/dist/
/nbdist/
/.nb-gradle/

# VSCode IDE
.vscode/

# Gradle
.gradle/
/build/

# Logs
*.log
logs/

# OS-specific files
.DS_Store
Thumbs.db

# Maven Wrapper
.mvntask

# Compiled files for SBT
.target/

# JAR files
*.jar

# WAR files
*.war

# IDE metadata
*.iml
```

Ten plik .gitignore ignoruje katalogi i pliki wygenerowane przez różne narzędzia deweloperskie takie jak IntelliJ, Maven, Eclipse, NetBeans, Visual Studio Code, Gradle, SBT, itp. Dodatkowo ignoruje także pliki skompilowanych klas, pliki logów, pliki wykonywalne (JAR, WAR) i inne pliki specyficzne dla systemu operacyjnego. Dzięki temu unikniemy przypadkowego dodania niepotrzebnych plików do repozytorium Git.