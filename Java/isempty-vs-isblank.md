# isEmpty vs isBlank

**Data:** 2025-01-14

---

**User:**

Java, czy mając string trzeba sprawdzać string.isEmpty oraz string.isBlank

---

**Assistant:**

W języku Java różnice między metodami `isEmpty()` i `isBlank()` mogą prowadzić do pytania, którą z nich używać. Oto wyjaśnienie:

### 1. **`isEmpty()`**
Metoda `isEmpty()` zwraca `true`, jeśli długość łańcucha wynosi zero, czyli jeśli `string.length() == 0`. Nie bierze pod uwagę białych znaków. Na przykład:

```java
String str = "   "; // same spacje
System.out.println(str.isEmpty()); // false
```

### 2. **`isBlank()`**
Metoda `isBlank()` (wprowadzona w **Java 11**) zwraca `true`, jeśli łańcuch jest pusty **lub zawiera tylko białe znaki** (np. spacje, tabulatory, nowe linie). Przykład:

```java
String str = "   "; // same spacje
System.out.println(str.isBlank()); // true
```

### Kiedy używać której?

- **`isEmpty()`**:
  - Używaj, gdy interesuje Cię wyłącznie to, czy łańcuch jest dosłownie pusty (bez żadnych znaków).
  - Przykład: Walidacja formularza, gdzie pole powinno zawierać co najmniej jeden znak.

- **`isBlank()`**:
  - Używaj, gdy chcesz sprawdzić, czy łańcuch jest pusty **lub** składa się wyłącznie z białych znaków.
  - Przykład: Sprawdzanie danych wejściowych użytkownika, gdzie białe znaki również są traktowane jako brak treści.

### Czy trzeba używać obu?

Nie ma potrzeby sprawdzania obu metod jednocześnie, ponieważ:
- Jeśli sprawdzisz `isBlank()`, automatycznie pokrywa ono przypadki sprawdzane przez `isEmpty()`.
- Jeśli chcesz jedynie sprawdzić długość, wystarczy `isEmpty()`.

### Przykłady:

#### Sprawdzenie pustego lub "białego" łańcucha (lepsze podejście):
```java
if (str.isBlank()) {
    System.out.println("String jest pusty lub zawiera tylko białe znaki.");
}
```

#### Tylko sprawdzenie, czy łańcuch jest pusty:
```java
if (str.isEmpty()) {
    System.out.println("String jest pusty.");
}
```

### Podsumowanie:
- Używaj **`isBlank()`** w większości przypadków, gdy interesuje Cię, czy string zawiera coś "znaczącego".
- Używaj **`isEmpty()`** tylko wtedy, gdy białe znaki są dla Ciebie akceptowalne.