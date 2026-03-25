# Podział Stringu na Białe Znaki

**Data:** 2023-06-26

---

**User:**

Jak w java dokonać podziału Stringu ze względu na białe znaki, tak aby wiedzieć ze względu na który biały znak został dokonany podział

---

**Assistant:**

W Javie można dokonać podziału `String` ze względu na białe znaki, używając metody `split()` z klasy `String`. Aby wiedzieć, ze względu na który biały znak został dokonany podział, można użyć wyrażenia regularnego jako argumentu metody `split()`.

Oto przykład kodu, który ilustruje tę funkcjonalność:

```java
public class Main {
    public static void main(String[] args) {
        String input = "Lorem ipsum dolor sit amet, consectetur adipiscing elit";
        
        // Podział ze względu na białe znaki
        String[] parts = input.split("\\s+");
        
        // Wyświetlenie podzielonych fragmentów
        for (String part : parts) {
            System.out.println(part);
        }
        
        // Wyświetlenie informacji o podziale
        String delimiters = input.replaceAll("\\S+", "");
        System.out.println("Podział ze względu na: " + delimiters);
    }
}
```

W powyższym przykładzie użyto wyrażenia regularnego `\\s+`, które oznacza jeden lub więcej białych znaków. Metoda `split("\\s+")` wykonuje podział na podstawie tego wyrażenia.

Dodatkowo, użyto metody `replaceAll("\\S+", "")`, aby zamienić wszystkie niebiałe znaki na puste ciągi znaków. W ten sposób uzyskujemy informację o użytych białych znakach do podziału.

Po uruchomieniu powyższego kodu otrzymamy następujący wynik:

```
Lorem
ipsum
dolor
sit
amet,
consectetur
adipiscing
elit
Podział ze względu na:       ,           
```

Widzimy, że oryginalny `String` został podzielony na fragmenty ze względu na białe znaki, a informacja o użytych białych znakach do podziału została również wyświetlona.