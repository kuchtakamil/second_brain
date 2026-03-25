# Foldery źródłowe w VS Code

**Data:** 2025-10-12

---

**User:**

w intellij można wskazać foldery zawierające źródła, testy. Czy można to samo zrobić w vs code?

---

**Assistant:**

Tak, ale w Visual Studio Code nie ma tego rozwiązania wbudowanego tak “systemowo” jak w IntelliJ IDEA — czyli nie istnieje centralny mechanizm projektu, który rozróżnia np. *Source Root*, *Test Root* itp.  
W VS Code konfiguracja zależy od **języka**, **rozszerzenia** i **narzędzi buildujących**.  
Poniżej dokładnie jak to działa w zależności od kontekstu:

---

### 🟦 1. Dla Javy
Jeśli używasz **VS Code + Extension Pack for Java** (czyli `Language Support for Java(TM)` + `Debugger for Java` + `Test Runner for Java` itd.), to:
- Możesz oznaczać foldery jako **source** i **test** w pliku `.vscode/settings.json`.
- Przykład:

```json
{
  "java.project.sourcePaths": ["src/main/java"],
  "java.project.testPaths": ["src/test/java"],
  "java.project.outputPath": "bin"
}
```

To dokładnie odpowiada temu, co IntelliJ robi automatycznie przy importowaniu projektu Maven/Gradle.  
Jeśli projekt ma strukturę `mavenową` lub `gradleową`, VS Code zwykle sam rozpozna foldery.

---

### 🟦 2. Dla TypeScript / JavaScript
VS Code używa konfiguracji w pliku `tsconfig.json` lub `jsconfig.json`:

```json
{
  "include": ["src"],
  "exclude": ["node_modules", "dist", "test"]
}
```

lub bardziej szczegółowo:

```json
{
  "compilerOptions": {
    "rootDirs": ["src", "tests"],
    "outDir": "dist"
  }
}
```

Nie ma tu wizualnego rozróżnienia na "source/test", ale można to odzwierciedlić przez strukturę katalogów i konfigurację test runnera (np. Jest, Mocha itp.).

---

### 🟦 3. Dla Pythona
Nie ma pojęcia „source root”, ale można ustawić ścieżki importów w `.env` lub w `settings.json`, np.:

```json
{
  "python.analysis.extraPaths": ["src"],
  "python.testing.unittestArgs": [
    "-v",
    "-s",
    "./tests",
    "-p",
    "test_*.py"
  ]
}
```

---

### 🟦 4. Dla C/C++ (lub innych)
Często określa się ścieżki do źródeł i nagłówków w `c_cpp_properties.json`, np.:

```json
{
  "configurations": [
    {
      "includePath": ["${workspaceFolder}/src", "${workspaceFolder}/include"],
      "browse": {
        "path": ["${workspaceFolder}/src", "${workspaceFolder}/tests"]
      }
    }
  ]
}
```

---

### 🟩 Podsumowanie

| Język | Odpowiednik "source/test folder" | Gdzie się ustawia |
|--------|----------------------------------|-------------------|
| **Java** | `java.project.sourcePaths`, `java.project.testPaths` | `.vscode/settings.json` |
| **TypeScript/JS** | `include`, `exclude`, `rootDirs` | `tsconfig.json` |
| **Python** | `extraPaths`, `testing.unittestArgs` | `.vscode/settings.json` |
| **C/C++** | `includePath`, `browse.path` | `.vscode/c_cpp_properties.json` |

---

Chcesz, żebym pokazał dokładny przykład konfiguracji dla Javy w VS Code, działający tak jak w IntelliJ (np. `src/main/java`, `src/test/java`, `target/classes`)?