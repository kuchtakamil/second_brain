# Callback'i w Java. Podaj zastosowania i przykłady. Odpowiedz wyczerpująco i tech

**Data:** 25 wrz 2025, 14:49:25 CET

---

**User:**

Callback'i w Java. Podaj zastosowania i przykłady. Odpowiedz wyczerpująco i technicznie.

---

**Gemini:**

Callbacki w Javie to mechanizm, który umożliwia przekazanie kodu (w formie obiektu) do innego fragmentu kodu, który następnie może ten przekazany kod wykonać w odpowiednim momencie. Jest to fundamentalna koncepcja wzorca projektowego **odwrócenia sterowania (Inversion of Control - IoC)**. Zamiast wywoływać metody z niższych warstw systemu, wyższa warstwa dostarcza logikę, która ma zostać "zawołana z powrotem" (called back) przez niższą warstwę.

### **Sposoby Implementacji Callbacków**

Java, jako język silnie typowany i zorientowany obiektowo, realizuje mechanizm callbacków na kilka sposobów, które ewoluowały wraz z rozwojem języka.

#### **1. Interfejsy**

To klasyczne i najbardziej fundamentalne podejście. Definiuje się interfejs z jedną lub kilkoma metodami, które będą stanowiły callback. Klasa, która chce dostarczyć implementację callbacka, implementuje ten interfejs.

- **Zalety**: Jasno zdefiniowany kontrakt, silne typowanie, możliwość przekazania wielu metod callback w jednym obiekcie.
- **Wady**: Wymaga zdefiniowania interfejsu i często osobnej klasy implementującej, co prowadzi do większej ilości kodu (boilerplate).

#### **2. Anonimowe Klasy Wewnętrzne**

Przed Javą 8 było to popularne rozwiązanie do zwięzłego implementowania interfejsów "w locie", bez tworzenia osobnych, nazwanych plików `.java`.

- **Zalety**: Zmniejsza ilość kodu w porównaniu do osobnych klas, logika jest zdefiniowana w miejscu użycia.
- **Wady**: Składnia jest dosyć rozwlekła i może być nieczytelna przy bardziej skomplikowanej logice.

#### **3. Wyrażenia Lambda (Java 8+)**

Wprowadzenie wyrażeń lambda zrewolucjonizowało sposób implementacji callbacków w Javie. Lambda może być użyta do implementacji dowolnego **interfejsu funkcyjnego** (interfejsu z dokładnie jedną metodą abstrakcyjną).

- **Zalety**: Bardzo zwięzła i czytelna składnia, promuje programowanie funkcyjne.
- **Wady**: Ograniczone do interfejsów funkcyjnych.

#### **4. Referencje do Metod (Java 8+)**

Jest to jeszcze bardziej zwięzła forma wyrażenia lambda, używana, gdy lambda jedynie wywołuje istniejącą już metodę.

- **Zalety**: Maksymalna zwięzłość i czytelność kodu, gdy logika callbacka już istnieje w innej metodzie.
- **Wady**: Jak w przypadku lambd, ograniczone do interfejsów funkcyjnych.

---

### **Zastosowania i Przykłady Techniczne**

Callbacki są wszechobecne w nowoczesnym programowaniu w Javie. Poniżej znajdują się kluczowe obszary ich zastosowań wraz z przykładami kodu.

#### **1. Obsługa Zdarzeń (Event Handling)**

To kanoniczny przykład użycia callbacków, zwłaszcza w programowaniu GUI (Swing, JavaFX, Android). Kod dewelopera (callback) jest wykonywany w odpowiedzi na akcję użytkownika (zdarzenie).

**Przykład w Swing z użyciem lambdy:**
Framework Swing (warstwa niższa) wywołuje kod aplikacji (warstwa wyższa), gdy użytkownik kliknie przycisk.

```
import javax.swing.*;

public class EventHandlingExample {
    public static void main(String[] args) {
        JFrame frame = new JFrame("Callback Demo");
        JButton button = new JButton("Execute Callback");

        // The addActionListener method accepts an object that implements the
        // ActionListener interface. ActionListener is a functional interface.
        // We provide a lambda expression as the callback implementation.
        button.addActionListener(event -> {
            System.out.println("Button clicked! Event source: " + event.getSource());
            JOptionPane.showMessageDialog(frame, "Callback executed!");
        });

        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(300, 200);
        frame.getContentPane().add(button);
        frame.setVisible(true);
    }
}
```

W tym kodzie, `button.addActionListener(...)` rejestruje callback. Wątek dystrybucji zdarzeń Swinga wywoła go, gdy nastąpi zdarzenie `ActionEvent`.

---

#### **2. Programowanie Asynchroniczne**

Callbacki są niezbędne do obsługi wyników operacji, które wykonują się w tle (np. zapytania sieciowe, operacje na plikach, skomplikowane obliczenia), bez blokowania głównego wątku aplikacji.

**Przykład z `CompletableFuture` (Java 8+):**
`CompletableFuture` pozwala na tworzenie potoków (pipelines) asynchronicznych operacji, gdzie wynik jednego etapu jest przekazywany do callbacka w kolejnym etapie.

```
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.TimeUnit;

public class AsyncCallbackExample {

    // Simulates a long-running network request
    public static CompletableFuture<String> fetchData() {
        return CompletableFuture.supplyAsync(() -> {
            try {
                System.out.println("Fetching data on thread: " + Thread.currentThread().getName());
                TimeUnit.SECONDS.sleep(2);
            } catch (InterruptedException e) {
                throw new IllegalStateException(e);
            }
            return "{\"data\":\"some_json_payload\"}";
        });
    }

    public static void main(String[] args) throws InterruptedException {
        System.out.println("Main thread started.");

        fetchData()
            // Callback 1: executed upon successful completion of fetchData
            .thenAccept(result -> {
                System.out.println("Callback received data on thread: " + Thread.currentThread().getName());
                System.out.println("Result: " + result);
            })
            // Callback 2: executed if any exception occurred in the chain
            .exceptionally(error -> {
                System.err.println("An error occurred: " + error.getMessage());
                return null; // Must return a value of the expected type
            });

        System.out.println("Main thread continues execution without blocking...");
        // Keep the main thread alive to see the async result
        TimeUnit.SECONDS.sleep(3);
        System.out.println("Main thread finished.");
    }
}
```

Metody `thenAccept` i `exceptionally` rejestrują callbacki, które zostaną wykonane przez pulę wątków `ForkJoinPool` po zakończeniu asynchronicznej operacji `fetchData`.

---

#### **3. Przetwarzanie Strumieni (Stream API)**

Całe API Strumieni w Javie jest zbudowane na idei przekazywania zachowań (czyli callbacków) do operacji na kolekcjach.

**Przykład z referencjami do metod i lambdami:**
Metody takie jak `filter`, `map`, `forEach` przyjmują interfejsy funkcyjne (`Predicate`, `Function`, `Consumer`) jako argumenty.

```
import java.util.Arrays;
import java.util.List;

public class StreamApiCallbackExample {
    public static void main(String[] args) {
        List<String> names = Arrays.asList("Alice", "Bob", "Charlie", "Anna");

        names.stream()
             // Callback for filtering: a method reference
             .filter(StreamApiCallbackExample::startsWithA)
             // Callback for transformation: a lambda expression
             .map(name -> name.toUpperCase())
             // Callback for terminal operation: a method reference
             .forEach(System.out::println);
    }

    private static boolean startsWithA(String name) {
        return name.startsWith("A");
    }
}
```

Dla każdego elementu strumienia, metoda `filter` "woła z powrotem" naszą metodę `startsWithA`. Podobnie `map` wywołuje lambdę, a `forEach` metodę `println`.

---

#### **4. Dostosowywanie Algorytmów i Frameworków (Wzorzec Strategia)**

Callbacki pozwalają na implementację wzorca projektowego **Strategia**, gdzie ogólny algorytm jest zdefiniowany w jednym miejscu, a klient może dostarczyć specyficzne "strategie" jego wykonania.

**Przykład z `Arrays.sort()` i `Comparator`:**
Metoda `Arrays.sort` implementuje wydajny algorytm sortowania, ale nie wie, jak porównywać niestandardowe obiekty. Tę logikę dostarczamy jako callback w postaci obiektu `Comparator`.

```
import java.util.Arrays;
import java.util.Comparator;

class Product {
    private String name;
    private double price;

    public Product(String name, double price) { this.name = name; this.price = price; }
    public String getName() { return name; }
    public double getPrice() { return price; }
    @Override public String toString() { return name + ": $" + price; }
}

public class StrategyCallbackExample {
    public static void main(String[] args) {
        Product[] products = {
            new Product("Laptop", 1200.50),
            new Product("Mouse", 25.00),
            new Product("Keyboard", 75.99)
        };

        // Callback providing a strategy to sort by price
        Comparator<Product> byPrice = Comparator.comparingDouble(Product::getPrice);
        Arrays.sort(products, byPrice);
        System.out.println("Sorted by price: " + Arrays.toString(products));

        // Callback providing a strategy to sort by name length
        Comparator<Product> byNameLength = (p1, p2) -> Integer.compare(p1.getName().length(), p2.getName().length());
        Arrays.sort(products, byNameLength);
        System.out.println("Sorted by name length: " + Arrays.toString(products));
    }
}
```

Algorytm sortowania wielokrotnie wywołuje metodę `compare` z dostarczonego komparatora, aby podjąć decyzję o kolejności elementów. My, jako klienci API, dostarczamy jedynie strategię porównania.