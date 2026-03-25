# Zamokowanie metody statycznej.

**Data:** 2023-07-07

---

**User:**

Java, mam klasę A której motody chcę przetestować. W klasie A jest jedna metoda statyczna którą chcę zamokować. Chciałbym aby w testach wywoływana była zamokowana wersja metody klasy A a nie prawdziwa metoda klasy A.

---

**Assistant:**

Aby przetestować metodę statyczną klasy A i zamokować jej działanie, można skorzystać z narzędzia do mockowania w języku Java, takiego jak framework Mockito. Mockito pozwala na tworzenie atrap obiektów i definiowanie, jakie działanie mają one zwracać podczas testowania.

Oto przykład, jak użyć Mockito do zamokowania metody statycznej klasy A:

1. Zainstaluj bibliotekę Mockito, dodając odpowiednią zależność do pliku pom.xml (w przypadku Maven) lub dodając bibliotekę do ścieżki projektu.

2. Utwórz testową klasę, w której przeprowadzisz testy metody statycznej klasy A.

3. W metodzie testowej utwórz atrapę klasy A, używając statycznej metody Mockito.mock():

```java
import static org.mockito.Mockito.*;

public class ATest {

    @Test
    public void testStaticMethod() {
        // Utwórz atrapę klasy A
        A mockedA = mock(A.class);

        // Zdefiniuj, jaką wartość ma zwrócić zamokowana metoda statyczna
        when(mockedA.staticMethod()).thenReturn("Mocked value");

        // Wywołaj metodę testowaną, która korzysta z metody statycznej
        String result = SomeClass.methodThatUsesStaticMethod();

        // Sprawdź, czy wynik jest zgodny z oczekiwaniami
        assertEquals("Mocked value", result);

        // Sprawdź, czy zamokowana metoda została wywołana
        verify(mockedA, times(1)).staticMethod();
    }
}
```

W powyższym przykładzie używamy Mockito, aby utworzyć atrapę klasy A (`A mockedA = mock(A.class)`). Następnie definiujemy zachowanie atrapy za pomocą `when(mockedA.staticMethod()).thenReturn("Mocked value")`, mówiąc atrapie, że podczas wywołania metody statycznej `staticMethod()` ma zwrócić wartość "Mocked value". 

W ostatnim kroku sprawdzamy, czy wynik testu jest zgodny z oczekiwaniami oraz czy zamokowana metoda została wywołana za pomocą `assertEquals("Mocked value", result)` i `verify(mockedA, times(1)).staticMethod()`.

---

**User:**

dlaczego mockedA.staticMethod() wywoływana jest w ten sposób skoto to statyczna metoda

---

**Assistant:**

Przepraszam za zamieszanie. Faktycznie, Mockito nie obsługuje mockowania bezpośrednio statycznych metod w Javie. Jest ono zaprojektowane głównie do mockowania instancji obiektów i ich metod niestatycznych.

W przypadku statycznych metod w Javie, mockowanie ich zachowania staje się bardziej skomplikowane. Musisz zastosować różne techniki, takie jak modyfikowanie kodu źródłowego, używanie bibliotek specjalnie stworzonych do mockowania statycznych metod, takich jak PowerMock lub Mockito + PowerMock, lub refactorować kod, aby używał instancji obiektu zamiast metod statycznych.

Oto krótkie przykłady tych dwóch podejść:

1. Użycie biblioteki PowerMock:
   PowerMock to biblioteka, która rozszerza funkcjonalność Mockito i dodaje obsługę mockowania statycznych metod.

```java
import static org.junit.Assert.assertEquals;
import static org.powermock.api.mockito.PowerMockito.*;

@RunWith(PowerMockRunner.class)
@PrepareForTest(A.class)
public class ATest {

    @Test
    public void testStaticMethod() throws Exception {
        // Mockowanie statycznej metody klasy A
        mockStatic(A.class);
        when(A.staticMethod()).thenReturn("Mocked value");

        // Wywołanie metody testowanej
        String result = SomeClass.methodThatUsesStaticMethod();

        // Sprawdzenie wyniku
        assertEquals("Mocked value", result);
    }
}
```

2. Refaktoryzacja kodu:
   Refaktoryzacja kodu może być dobrym rozwiązaniem, jeśli jesteś w stanie przenieść logikę z metody statycznej do instancji obiektu. Następnie możesz łatwo mockować metody na tej instancji.

```java
public class A {
    public String nonStaticMethod() {
        return "Original value";
    }
}

public class ATest {

    @Test
    public void testNonStaticMethod() {
        // Utworzenie instancji klasy A
        A mockedA = mock(A.class);
        when(mockedA.nonStaticMethod()).thenReturn("Mocked value");

        // Wywołanie metody testowanej
        String result = SomeClass.methodThatUsesNonStaticMethod(mockedA);

        // Sprawdzenie wyniku
        assertEquals("Mocked value", result);
    }
}
```

W drugim podejściu refactorujesz kod, aby korzystał z instancji klasy A i mockujesz metody na tej instancji. W ten sposób omijasz problem mockowania bezpośrednio statycznej metody.

---

**User:**

Nowsze Mockito potrafi mokować statyczne metody

---

**Assistant:**

Przepraszam za nieścisłość w mojej wcześniejszej odpowiedzi. Faktycznie, w najnowszych wersjach biblioteki Mockito (od wersji 3.4.0) wprowadzono eksperymentalne wsparcie dla mockowania statycznych metod przy użyciu tzw. "Mockito Extensions". Dzięki temu możesz mockować statyczne metody bez konieczności używania innych bibliotek lub narzędzi.

Oto przykład, jak użyć nowego wsparcia w Mockito do mockowania statycznych metod:

1. Dodaj zależność do najnowszej wersji biblioteki Mockito w pliku pom.xml (w przypadku Maven) lub dodaj bibliotekę do ścieżki projektu:

```xml
<dependency>
    <groupId>org.mockito</groupId>
    <artifactId>mockito-core</artifactId>
    <version>3.4.0</version> <!-- lub nowsza wersja -->
    <scope>test</scope>
</dependency>
```

2. Utwórz testową klasę, w której przeprowadzisz testy metody statycznej klasy A:

```java
import static org.junit.Assert.assertEquals;
import static org.mockito.Mockito.*;

import org.junit.jupiter.api.Test;
import org.mockito.MockedStatic;

public class ATest {

    @Test
    public void testStaticMethod() {
        try (MockedStatic<A> mockedA = mockStatic(A.class)) {
            // Zdefiniuj, jaką wartość ma zwrócić zamokowana metoda statyczna
            mockedA.when(A::staticMethod).thenReturn("Mocked value");

            // Wywołaj metodę testowaną, która korzysta z metody statycznej
            String result = SomeClass.methodThatUsesStaticMethod();

            // Sprawdź, czy wynik jest zgodny z oczekiwaniami
            assertEquals("Mocked value", result);
        }
    }
}
```

W tym przykładzie używamy nowej funkcjonalności Mockito, tworząc atrapę statycznej klasy A za pomocą `MockedStatic<A> mockedA = mockStatic(A.class)`. Następnie definiujemy zachowanie atrapy przy użyciu `mockedA.when(A::staticMethod).thenReturn("Mocked value")`, mówiąc atrapie, że podczas wywołania metody statycznej `staticMethod()` ma zwrócić wartość "Mocked value". 

Zauważ, że używamy bloku `try` z zasobami oraz korzystamy z metody `mockedA.close()`, aby wyczyścić i przywrócić normalne zachowanie metody statycznej po zakończeniu testu.

Dzięki tym nowym rozszerzeniom Mockito, jesteś w stanie mockować statyczne metody bez konieczności używania dodatkowych bibliotek takich jak PowerMock.

---

**User:**

a jak poradzić sobie z przypadkiem gdyby testowana metoda i mokowana metoda była w jednej klasie czyli
 String result = A.methodThatUsesStaticMethod();

---

**Assistant:**

Jeśli testowana metoda i mokowana metoda są w tej samej klasie i chcesz zamokować tylko wywołanie metody statycznej `methodThatUsesStaticMethod()` w tej klasie, możesz skorzystać z narzędzia do mockowania zachowania na poziomie klasy, takiego jak PowerMockito lub Mockito + PowerMock.

Oto przykład, jak użyć PowerMockito do mockowania wywołania metody statycznej w tej samej klasie:

```java
import static org.junit.Assert.assertEquals;
import static org.powermock.api.mockito.PowerMockito.*;

@RunWith(PowerMockRunner.class)
@PrepareForTest(A.class)
public class ATest {

    @Test
    public void testMethodThatUsesStaticMethod() throws Exception {
        // Mockowanie metody statycznej w tej samej klasie
        mockStatic(A.class);
        when(A.methodThatUsesStaticMethod()).thenReturn("Mocked value");

        // Wywołanie metody testowanej
        String result = A.methodThatUsesStaticMethod();

        // Sprawdzenie wyniku
        assertEquals("Mocked value", result);
    }
}
```

W tym przykładzie używamy PowerMockito, aby zmockować wywołanie metody statycznej `methodThatUsesStaticMethod()` w klasie A. Dzięki temu możemy zdefiniować, jaką wartość ma zwrócić zamokowana metoda.

Należy zauważyć, że używamy adnotacji `@PrepareForTest(A.class)`, która wskazuje PowerMock, aby przygotował klasę A do mockowania. Może to wymagać odpowiedniej konfiguracji w pom.xml lub w pliku z testami, w zależności od narzędzia budującego i środowiska testowego.

Jeśli używasz wersji Mockito + PowerMock, upewnij się, że masz odpowiednie zależności w pliku pom.xml, takie jak `mockito-core` i `powermock-module-junit4` lub `powermock-module-junit5`, w zależności od wersji JUnit, którą używasz.

Ważne jest również, aby pamiętać, że mockowanie statycznych metod wprowadza pewne ograniczenia i wymaga specjalnej konfiguracji, ponieważ jest to niestandardowe zachowanie w języku Java. Dlatego też wymaga użycia narzędzi takich jak PowerMockito lub Mockito + PowerMock.