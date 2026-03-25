# Usuwanie znaków w Javie

**Data:** 2025-03-25

---

**User:**

jak w java usunąć wszystkie znaki "?"

---

**Assistant:**

W Javie możesz usunąć wszystkie znaki `?` z ciągu znaków na kilka sposobów:

### 1. Użycie `replace`
Najprostsza metoda, jeśli chcesz zastąpić wszystkie `?` pustym ciągiem:
```java
String text = "Hello? How are you?";
String result = text.replace("?", "");
System.out.println(result); // "Hello How are you"
```

### 2. Użycie `replaceAll` z wyrażeniem regularnym
Jeśli chcesz użyć regexa:
```java
String text = "Hello? How are you?";
String result = text.replaceAll("\\?", "");
System.out.println(result); // "Hello How are you"
```
Tutaj `\\?` oznacza dosłowny znak `?`, ponieważ `?` jest specjalnym symbolem w regexie.

### 3. Użycie `StringBuilder` dla większej wydajności
Jeśli operacja usuwania jest częsta lub na dużych tekstach:
```java
String text = "Hello? How are you?";
StringBuilder sb = new StringBuilder();

for (char c : text.toCharArray()) {
    if (c != '?') {
        sb.append(c);
    }
}

String result = sb.toString();
System.out.println(result); // "Hello How are you"
```
Ta metoda może być szybsza, gdy często modyfikujesz tekst.

Czy to rozwiązuje Twój problem? 😊