# Użycie pliku JAR

**Data:** 2024-02-12

---

**User:**

W build.gradle buduję plik jar.
W innym tasku utworzonym w tym samym pliku build.gradle chcę użyć tego pliku jar. jak to zrobić

---

**Assistant:**

Aby użyć pliku JAR w innym zadaniu w pliku `build.gradle`, możesz skorzystać z właściwości `archives` obiektu `project` lub zdefiniować zależność między zadaniami. Poniżej znajdziesz przykłady obu podejść.

1. **Zastosowanie `archives` jako właściwości projektu:**

```gradle
apply plugin: 'java'

// Konfiguracja zadania do budowy pliku JAR
task createJar(type: Jar) {
    // konfiguracja pliku JAR
    // ...
}

// Zdefiniowanie właściwości projektu, aby przechować ścieżkę do pliku JAR
project.ext {
    myJarPath = createJar.archivePath
}

// Inne zadanie, które używa pliku JAR
task anotherTask {
    doLast {
        // Używanie ścieżki do pliku JAR z właściwości projektu
        println "Ścieżka do pliku JAR: ${project.myJarPath}"
        // Tu możesz użyć ścieżki do pliku JAR w inny sposób
    }
}
```

W tym przykładzie plik JAR jest budowany przez zadanie `createJar`, a ścieżka do pliku JAR jest przechowywana jako właściwość projektu `myJarPath`. W zadaniu `anotherTask` możesz użyć tej ścieżki do pliku JAR.

2. **Zastosowanie zależności między zadaniami:**

```gradle
apply plugin: 'java'

// Konfiguracja zadania do budowy pliku JAR
task createJar(type: Jar) {
    // konfiguracja pliku JAR
    // ...
}

// Inne zadanie, które używa pliku JAR
task anotherTask(dependsOn: createJar) {
    doLast {
        // Używanie pliku JAR z zadania createJar
        println "Ścieżka do pliku JAR: ${createJar.archivePath}"
        // Tu możesz użyć pliku JAR w inny sposób
    }
}
```

W tym podejściu zadanie `anotherTask` jest zależne od zadania `createJar`, co oznacza, że plik JAR będzie już dostępny, gdy `anotherTask` zostanie uruchomione. Możesz uzyskać dostęp do ścieżki do pliku JAR za pomocą `createJar.archivePath`.