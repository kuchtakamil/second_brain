# Optymalizacja kodu w Javie

**Data:** 2024-12-14

---

**User:**

Jak napisać ten kod w java lepiej?
        List<Token> tokensToDisplay = getTokensToDisplay();

        List<Token> filteredTokens = tokensChosen.stream()
                .flatMap(token -> {
                    Iterator<Token> iterator = tokensToDisplay.iterator();
                    while (iterator.hasNext()) {
                        Token tmpToken = iterator.next();
                        if (tmpToken.getTokenType().equals(token)) {
                            iterator.remove();
                            return Stream.of(tmpToken);
                        }
                    }
                    return Stream.empty();
                })
                .collect(Collectors.toList());

---

**Assistant:**

Kod można poprawić, aby był bardziej czytelny, efektywny i idiomatyczny w Javie. Główne problemy w aktualnym kodzie to:

1. **Użycie iteratora wewnątrz strumienia**: To nie jest idiomatyczne. Można to rozwiązać za pomocą bardziej deklaratywnego podejścia.
2. **Modyfikowanie listy (`tokensToDisplay`) w trakcie iteracji**: Jest to potencjalnie niebezpieczne i trudne do zrozumienia. Jeśli modyfikacja listy jest konieczna, należy to robić jawnie.

Oto ulepszona wersja kodu:

```java
List<Token> tokensToDisplay = getTokensToDisplay();

Set<String> tokenTypesChosen = new HashSet<>(tokensChosen); // Używamy Set dla szybszych operacji wyszukiwania

List<Token> filteredTokens = tokensToDisplay.stream()
        .filter(token -> tokenTypesChosen.contains(token.getTokenType())) // Filtrujemy na podstawie wybranego typu tokena
        .collect(Collectors.toList());

// Usunięcie przetworzonych tokenów z listy tokensToDisplay
tokensToDisplay.removeAll(filteredTokens);
```

### Wyjaśnienie:
1. **Użycie `HashSet`**:
   - Zamiast wielokrotnie iterować przez listę `tokensChosen`, konwertujemy ją na `HashSet`, co pozwala na szybkie wyszukiwanie typu tokena w czasie O(1).

2. **Strumień z `filter`**:
   - Zamiast używać `flatMap` i iteracji wewnętrznej, strumień filtruje elementy listy `tokensToDisplay`, aby pasowały do tokenów wybranych przez użytkownika.

3. **Oddzielenie logiki filtrowania i modyfikacji**:
   - Najpierw tworzymy listę `filteredTokens`, a następnie usuwamy je z `tokensToDisplay`. Dzięki temu kod jest bardziej czytelny i mniej podatny na błędy.

### Korzyści:
- Kod jest bardziej deklaratywny i łatwiejszy do zrozumienia.
- Eliminujemy niepotrzebne modyfikacje listy w trakcie iteracji.
- Użycie `HashSet` zwiększa wydajność, szczególnie w przypadku dużych list.

---

**User:**

ok, a teraz załóżmy że tokensChosen nie jest listą/kolekcją ale pojedynczym obiektem. Czyli to co robiliśmy na kolekcji obiektów, zróbmy teraz na pojedynczym obiekcie

---

**Assistant:**

Jeśli `tokensChosen` jest teraz pojedynczym obiektem (a nie kolekcją), to kod może zostać uproszczony, ponieważ nie musimy iterować przez listę wybranych tokenów. Oto jak można dostosować kod:

### Przykładowy kod:

```java
List<Token> tokensToDisplay = getTokensToDisplay();

String chosenTokenType = tokensChosen.getTokenType(); // Zakładam, że tokensChosen to obiekt typu Token lub posiada odpowiednią metodę

// Filtrowanie tokenów pasujących do wybranego typu
List<Token> filteredTokens = tokensToDisplay.stream()
        .filter(token -> token.getTokenType().equals(chosenTokenType))
        .collect(Collectors.toList());

// Usunięcie przetworzonych tokenów z listy tokensToDisplay
tokensToDisplay.removeAll(filteredTokens);
```

### Wyjaśnienie:
1. **`tokensChosen` jako pojedynczy obiekt**:
   - Bezpośrednio pobieramy jego typ za pomocą `getTokenType()`.

2. **Filtrowanie w strumieniu**:
   - Porównujemy `token.getTokenType()` z typem wybranego tokena (`chosenTokenType`).

3. **Usuwanie z listy**:
   - Usunięcie dopasowanych tokenów z `tokensToDisplay` następuje po zakończeniu filtrowania, co jest bardziej czytelne niż modyfikacja listy w trakcie iteracji.

### Korzyści:
- Kod jest teraz jeszcze prostszy, bo pracujemy tylko z jednym obiektem zamiast kolekcji.
- Logika filtrowania i modyfikacji listy pozostaje czytelna i dobrze rozdzielona.

---

**User:**

w pierwszej wersji kodu którą podałem jaki sens ma iterator.remove();

---

**Assistant:**

W Twoim pierwszym kodzie, metoda `iterator.remove()` służy do usuwania elementu z listy `tokensToDisplay` w trakcie iteracji. Jest to mechanizm bezpiecznego usuwania elementów z kolekcji podczas iteracji, bez ryzyka wystąpienia wyjątku `ConcurrentModificationException`.

### Sens `iterator.remove()` w Twoim kodzie
1. **Usunięcie dopasowanego elementu**:
   - Gdy znajdzie się token w `tokensToDisplay`, którego `getTokenType()` pasuje do wartości z `tokensChosen`, ten token jest natychmiast usuwany z listy `tokensToDisplay`.

2. **Unikanie `ConcurrentModificationException`**:
   - Bez użycia `iterator.remove()`, gdybyś próbował usunąć element z listy w trakcie iteracji, program rzuciłby `ConcurrentModificationException`.

3. **Optymalizacja**:
   - Usunięcie elementu w trakcie iteracji może zaoszczędzić zasoby, jeśli nie chcesz, aby elementy, które już zostały przetworzone, były ponownie sprawdzane w późniejszych iteracjach.

### Problemy z takim podejściem
- **Mieszanie strumieni i iteratora**: Kod staje się mniej czytelny, ponieważ strumienie w Javie służą do deklaratywnego przetwarzania danych, a używanie iteratora wewnątrz strumienia jest sprzeczne z tą ideą.
- **Efektywność**: Usuwanie elementu z listy w trakcie iteracji może być kosztowne, szczególnie jeśli `tokensToDisplay` to lista implementująca `ArrayList`. Usunięcie elementu powoduje przesunięcie pozostałych elementów, co ma złożoność O(n).

### Alternatywne podejście
Zamiast usuwać elementy z `tokensToDisplay` w trakcie iteracji, lepiej jest to zrobić w oddzielnym kroku, jak w ulepszonej wersji kodu, którą wcześniej zaproponowałem. Dzięki temu kod będzie bardziej czytelny i lepiej oddzieli logikę filtrowania od logiki modyfikacji kolekcji.

---

**User:**

po zakończeniu tego całego kodu jak ma się tokensToDisplay do tokensChosen

---

**Assistant:**

Po zakończeniu wykonania Twojego pierwotnego kodu, relacja między `tokensToDisplay` a `tokensChosen` wygląda następująco:

1. **`tokensToDisplay`**:
   - Z listy `tokensToDisplay` zostały usunięte te elementy, które mają taki sam typ (`getTokenType()`) jak którykolwiek z elementów w `tokensChosen`. Oznacza to, że `tokensToDisplay` zawiera teraz wyłącznie te tokeny, które nie pasowały do `tokensChosen`.

2. **`tokensChosen`**:
   - `tokensChosen` pozostaje nienaruszone, ponieważ w Twoim kodzie nie jest modyfikowane.

3. **Relacja między nimi**:
   - Elementy `tokensToDisplay`, które pierwotnie były zgodne z typami w `tokensChosen`, zostały usunięte z `tokensToDisplay`.
   - W efekcie `tokensToDisplay` i `tokensChosen` są teraz rozłączne pod względem typów tokenów (`getTokenType()`).

### Wizualizacja:
Załóżmy, że:
```java
tokensToDisplay = [Token(type="A"), Token(type="B"), Token(type="C")];
tokensChosen = ["B", "C"];
```

Po wykonaniu Twojego pierwotnego kodu:
```java
tokensToDisplay = [Token(type="A")]; // Usunięto "B" i "C"
filteredTokens = [Token(type="B"), Token(type="C")]; // Dopasowane i przetworzone tokeny
```

### Kluczowe efekty:
- **`tokensToDisplay`**: Zawiera tylko te tokeny, które **nie pasują** do żadnego z typów w `tokensChosen`.
- **`filteredTokens` (lub odpowiednik w kodzie)**: Zawiera tokeny z `tokensToDisplay`, które pasowały do `tokensChosen`.
  
Twoje działanie kodu de facto filtruje i "przenosi" tokeny zgodne z `tokensChosen` z jednej listy (`tokensToDisplay`) do innej kolekcji (`filteredTokens`).