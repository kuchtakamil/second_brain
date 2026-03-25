# Weryfikacja logów w JUnit

**Data:** 2025-08-14

---

**User:**

Używam Java 8 i JUnit 4. Czy jest możliwość, aby zweryfikować, czy został wywołany log z konkretnej sytuacji? Zweryfikować mam na myśli użyć EXPECT. Log mam skonfigurowany przy użyciu adnotacji SLS4J.

---

**Assistant:**

Tak, da się to zrobić, ale w JUnit 4 i z Java 8 nie masz tego „out-of-the-box” w SLF4J — musisz przechwycić logi za pomocą dodatkowej biblioteki albo własnego appendera.  

Najczęstsze podejścia:  

---

**1. `slf4j-test`**  
Biblioteka [slf4j-test](https://github.com/systemoutprintln/slf4j-test) pozwala w testach zbierać logi do pamięci i weryfikować je asercjami.  
Przykład:

```java
import static com.github.valfirst.slf4jtest.LoggingEvent.info;
import static com.github.valfirst.slf4jtest.LoggingEvent.error;
import static org.assertj.core.api.Assertions.assertThat;

import com.github.valfirst.slf4jtest.LoggerFactory;
import com.github.valfirst.slf4jtest.TestLogger;
import com.github.valfirst.slf4jtest.TestLoggerFactory;
import org.junit.Test;

public class MyServiceTest {

    private final TestLogger logger = TestLoggerFactory.getTestLogger(MyService.class);

    @Test
    public void shouldLogError() {
        MyService service = new MyService();
        service.doSomethingBad();

        assertThat(logger.getLoggingEvents()).contains(
            error("Something went wrong")
        );
    }
}
```
Tu logger przechwytuje logi tylko dla tej klasy, więc nie musisz grzebać w konfiguracji produkcyjnej.

---

**2. Własny `Appender` w Logback** (jeśli używasz Logbacka)  
Tworzysz `Appender` zapisujący logi w liście, a w teście go podłączasz:

```java
import ch.qos.logback.classic.AppenderBase;
import ch.qos.logback.classic.spi.ILoggingEvent;
import java.util.ArrayList;
import java.util.List;

public class InMemoryAppender extends AppenderBase<ILoggingEvent> {
    private final List<ILoggingEvent> log = new ArrayList<>();

    @Override
    protected void append(ILoggingEvent eventObject) {
        log.add(eventObject);
    }

    public List<ILoggingEvent> getLog() {
        return new ArrayList<>(log);
    }
}
```

W teście:

```java
import static org.junit.Assert.assertTrue;
import ch.qos.logback.classic.Logger;
import org.junit.Before;
import org.junit.Test;
import org.slf4j.LoggerFactory;

public class MyServiceTest {
    private InMemoryAppender appender;

    @Before
    public void setUp() {
        Logger logger = (Logger) LoggerFactory.getLogger(MyService.class);
        appender = new InMemoryAppender();
        logger.addAppender(appender);
        appender.start();
    }

    @Test
    public void shouldLogSomething() {
        new MyService().doWork();
        assertTrue(appender.getLog().stream()
            .anyMatch(e -> e.getFormattedMessage().contains("expected log text")));
    }
}
```

---

**3. System Rules (`SystemOutRule`)** – jeśli logi idą na `System.out`/`System.err`  
Nie polecam, bo logback/SLF4J może nie wypisywać bezpośrednio na stdout, ale w prostych przypadkach można tymczasowo przechwycić strumień.

---

🔹 Jeśli chcesz użyć **`EXPECT`** w sensie „given/when/then” (np. z AssertJ lub Hamcrest), to najlepiej pasuje podejście z `slf4j-test` — wtedy logi są kolekcją obiektów, które można asercyjnie sprawdzić.  

Jeśli chcesz, mogę Ci przygotować minimalny przykład **dla JUnit 4 + Java 8 + SLF4J** bez dodatkowych bibliotek poza `slf4j-test`, gotowy do uruchomienia.  
Czy chcesz taki przykład?