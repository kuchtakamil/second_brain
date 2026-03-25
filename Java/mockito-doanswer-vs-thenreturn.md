# Mockito: doAnswer vs thenReturn

**Data:** 2023-11-19

---

**User:**

Mockito, róznica między doAnswer a thenReturn

---

**Assistant:**

W bibliotece Mockito, `doAnswer` i `thenReturn` są dwiema różnymi metodami używanymi do mockowania zachowań obiektów podczas testowania. Oto krótka charakteryzacja każdej z tych metod:

1. **`doAnswer`**:
   - Metoda `doAnswer` jest ogólniejsza niż `thenReturn` i umożliwia bardziej zaawansowane operacje podczas mockowania.
   - Pozwala na zdefiniowanie zachowania mocka w oparciu o przekazany obiekt implementujący interfejs `Answer`. `Answer` to interfejs funkcjonalny z jedną metodą `answer`, która jest wywoływana, gdy mock jest używany.
   - `doAnswer` jest przydatne, gdy trzeba zwrócić różne wartości w zależności od argumentów metody mockowanej, rzucić wyjątek, czy też wykonać bardziej zaawansowane operacje podczas wywołania metody.

Przykład użycia `doAnswer`:

```java
import static org.mockito.Mockito.*;

// ...

doAnswer(invocation -> {
    Object[] args = invocation.getArguments();
    // wykonaj zaawansowane operacje na podstawie argumentów
    return wynik;
}).when(mockObject).metodaMockowana();
```

2. **`thenReturn`**:
   - Metoda `thenReturn` jest bardziej skoncentrowana na prostych przypadkach, gdzie zawsze chcemy zwrócić stałą wartość lub serię wartości podczas wywołania metody mockowanej.
   - Pozwala na zdefiniowanie, co mock ma zwrócić w przypadku konkretnego wywołania metody.

Przykład użycia `thenReturn`:

```java
import static org.mockito.Mockito.*;

// ...

when(mockObject.metodaMockowana()).thenReturn(stałaWartość);
```

Podsumowując, `doAnswer` jest bardziej elastyczne i używane, gdy potrzebujesz bardziej zaawansowanych operacji podczas mockowania, takich jak dynamiczne generowanie wartości w zależności od argumentów. Z kolei `thenReturn` jest prostsze i bardziej czytelne, gdy zawsze chcesz zwrócić stałą wartość.