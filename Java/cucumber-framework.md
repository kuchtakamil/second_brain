# Cucumber – framework do BDD w Javie

**Data:** 2026-06-05

---

## Czym jest Cucumber?

**Cucumber** to framework do testów automatycznych w stylu **BDD** (*Behavior-Driven Development*). Pozwala opisywać zachowanie aplikacji **językiem naturalnym** (zrozumiałym dla biznesu), a następnie wiązać te opisy z kodem wykonawczym w Javie.

```
Plik .feature (Gherkin)        Step Definitions (Java)        Aplikacja
─────────────────────          ───────────────────────        ─────────
Given konto z saldem 100   ──▶  @Given("konto z saldem {int}") ──▶  Account
When wpłacam 50            ──▶  @When("wpłacam {int}")          ──▶  account.deposit()
Then saldo wynosi 150      ──▶  @Then("saldo wynosi {int}")     ──▶  assertEquals(...)
```

Kluczowa idea: **jeden opis** scenariusza służy jednocześnie jako:
- **dokumentacja** (czytelna dla product ownera / analityka),
- **specyfikacja wykonywalna** (uruchamiana jako test),
- **kryterium akceptacji** (definicja "skończone").

---

## Dlaczego BDD i Cucumber?

| Zaleta | Opis |
|--------|------|
| **Wspólny język** | Biznes, QA i dev rozmawiają jednym językiem (*ubiquitous language*) |
| **Żywa dokumentacja** | Scenariusze nie dezaktualizują się – jeśli są nieaktualne, testy padają |
| **Skupienie na zachowaniu** | Testy opisują *co* system robi, nie *jak* jest zaimplementowany |
| **Reużywalność kroków** | Te same kroki Gherkin można składać w wiele scenariuszy |
| **Łatwa współpraca** | Analityk może pisać `.feature`, dev tylko implementuje kroki |

> ⚠️ **Uwaga:** Cucumber świetnie sprawdza się dla testów **akceptacyjnych / E2E / integracyjnych** opisujących logikę biznesową. Do czystych testów jednostkowych jest zwykle nadmiarowy – tam lepszy jest goły **JUnit**.

---

## Architektura – trzy elementy

```
┌──────────────────────────────────────────────────────┐
│  1. Pliki .feature   → scenariusze w języku Gherkin    │
│  2. Step Definitions → metody Java mapujące kroki      │
│  3. Runner           → uruchamia testy (JUnit Platform)│
└──────────────────────────────────────────────────────┘
```

---

## Setup – Maven

```xml
<properties>
    <cucumber.version>7.18.0</cucumber.version>
    <junit.jupiter.version>5.10.2</junit.jupiter.version>
</properties>

<dependencies>
    <!-- Cucumber + JUnit 5 (JUnit Platform) -->
    <dependency>
        <groupId>io.cucumber</groupId>
        <artifactId>cucumber-java</artifactId>
        <version>${cucumber.version}</version>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>io.cucumber</groupId>
        <artifactId>cucumber-junit-platform-engine</artifactId>
        <version>${cucumber.version}</version>
        <scope>test</scope>
    </dependency>

    <!-- Platforma JUnit 5 -->
    <dependency>
        <groupId>org.junit.platform</groupId>
        <artifactId>junit-platform-suite</artifactId>
        <version>1.10.2</version>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.junit.jupiter</groupId>
        <artifactId>junit-jupiter</artifactId>
        <version>${junit.jupiter.version}</version>
        <scope>test</scope>
    </dependency>
</dependencies>
```

### Setup – Gradle (Kotlin DSL)

```kotlin
dependencies {
    testImplementation("io.cucumber:cucumber-java:7.18.0")
    testImplementation("io.cucumber:cucumber-junit-platform-engine:7.18.0")
    testImplementation("org.junit.platform:junit-platform-suite:1.10.2")
    testImplementation("org.junit.jupiter:junit-jupiter:5.10.2")
}

tasks.test {
    useJUnitPlatform()
}
```

---

## Gherkin – składnia plików `.feature`

Gherkin to język słów kluczowych. Najważniejsze:

| Słowo kluczowe | Rola |
|----------------|------|
| `Feature` | opis funkcjonalności (jeden plik = jedna funkcjonalność) |
| `Scenario` | pojedynczy przypadek testowy |
| `Given` | warunek początkowy (stan systemu) |
| `When` | akcja / zdarzenie |
| `Then` | oczekiwany rezultat |
| `And` / `But` | kontynuacja poprzedniego kroku (czytelność) |
| `Background` | wspólne kroki uruchamiane przed każdym scenariuszem |
| `Scenario Outline` + `Examples` | scenariusz parametryzowany (tabela danych) |
| `@tag` | etykieta do filtrowania scenariuszy |

### Przykład: `src/test/resources/features/konto.feature`

```gherkin
# language: pl
Funkcja: Obsługa konta bankowego
  Jako klient banku
  Chcę móc wpłacać i wypłacać środki
  Aby zarządzać swoimi finansami

  Założenia:
    Zakładając, że istnieje konto o numerze "PL123" z saldem 100 zł

  Scenariusz: Udana wpłata środków
    Kiedy wpłacam 50 zł na konto "PL123"
    Wtedy saldo konta "PL123" wynosi 150 zł

  Scenariusz: Wypłata przekraczająca saldo
    Kiedy próbuję wypłacić 500 zł z konta "PL123"
    Wtedy operacja kończy się błędem "Niewystarczające środki"
    Oraz saldo konta "PL123" wynosi 100 zł
```

> 💡 Pierwsza linia `# language: pl` włącza polskie słowa kluczowe (`Funkcja`, `Scenariusz`, `Zakładając`, `Kiedy`, `Wtedy`, `Oraz`). Domyślnie Gherkin jest po angielsku (`Feature`, `Scenario`, `Given`, `When`, `Then`, `And`).

### Wersja angielska (klasyczna)

```gherkin
Feature: Bank account operations

  Background:
    Given an account "PL123" with balance 100

  Scenario: Successful deposit
    When I deposit 50 to account "PL123"
    Then the balance of account "PL123" is 150
```

---

## Step Definitions – wiązanie kroków z kodem

Każdy krok Gherkin mapuje się na metodę Javy z adnotacją (`@Given`, `@When`, `@Then`). Wyrażenia w `{}` to **Cucumber Expressions** – automatyczna konwersja typów.

```java
package steps;

import io.cucumber.java.en.Given;
import io.cucumber.java.en.When;
import io.cucumber.java.en.Then;
import static org.junit.jupiter.api.Assertions.*;

public class AccountSteps {

    private final Bank bank = new Bank();
    private String lastError;

    @Given("an account {string} with balance {int}")
    public void anAccountWithBalance(String accountId, int balance) {
        bank.createAccount(accountId, balance);
    }

    @When("I deposit {int} to account {string}")
    public void iDeposit(int amount, String accountId) {
        bank.deposit(accountId, amount);
    }

    @When("I try to withdraw {int} from account {string}")
    public void iTryToWithdraw(int amount, String accountId) {
        try {
            bank.withdraw(accountId, amount);
        } catch (InsufficientFundsException e) {
            lastError = e.getMessage();
        }
    }

    @Then("the balance of account {string} is {int}")
    public void theBalanceIs(String accountId, int expected) {
        assertEquals(expected, bank.getBalance(accountId));
    }

    @Then("the operation fails with {string}")
    public void theOperationFailsWith(String message) {
        assertEquals(message, lastError);
    }
}
```

### Cucumber Expressions – wbudowane typy parametrów

| Wzorzec | Dopasowuje | Typ Java |
|---------|-----------|----------|
| `{int}` | liczbę całkowitą | `int` / `Integer` |
| `{long}` | długą liczbę | `long` |
| `{float}` / `{double}` | liczbę zmiennoprzecinkową | `float` / `double` |
| `{word}` | pojedyncze słowo (bez spacji) | `String` |
| `{string}` | tekst w cudzysłowie `"..."` | `String` |
| `{}` | dowolny tekst (anonymous) | `String` |

### Własny typ parametru – `@ParameterType`

Gdy potrzebujesz konwersji do własnego typu (np. enum, data, obiekt domeny):

```java
import io.cucumber.java.ParameterType;
import java.time.LocalDate;

public class CustomParameterTypes {

    @ParameterType("\\d{4}-\\d{2}-\\d{2}")   // regex: 2026-06-05
    public LocalDate iso8601Date(String date) {
        return LocalDate.parse(date);
    }

    @ParameterType("ACTIVE|BLOCKED|CLOSED")
    public AccountStatus status(String value) {
        return AccountStatus.valueOf(value);
    }
}

// Użycie w step definition:
// @Given("account opened on {iso8601Date} with status {status}")
// public void openAccount(LocalDate date, AccountStatus status) { ... }
```

### Regex zamiast Cucumber Expressions

Można też używać klasycznych wyrażeń regularnych (otoczonych `^...$`):

```java
@Given("^an account \"([^\"]*)\" with balance (\\d+)$")
public void anAccount(String id, int balance) { ... }
```

---

## Runner – uruchamianie testów

### JUnit 5 (JUnit Platform Suite) – zalecane

```java
package runner;

import org.junit.platform.suite.api.*;
import static io.cucumber.junit.platform.engine.Constants.*;

@Suite
@IncludeEngines("cucumber")
@SelectClasspathResource("features")          // folder z plikami .feature
@ConfigurationParameter(
    key = GLUE_PROPERTY_NAME,
    value = "steps")                          // pakiet ze step definitions
@ConfigurationParameter(
    key = PLUGIN_PROPERTY_NAME,
    value = "pretty, html:target/cucumber-report.html, json:target/cucumber.json")
public class RunCucumberTest {
}
```

Alternatywnie konfiguracja przez `src/test/resources/junit-platform.properties`:

```properties
cucumber.glue=steps
cucumber.plugin=pretty, html:target/cucumber-report.html
cucumber.publish.quiet=true
cucumber.filter.tags=@smoke and not @wip
```

### JUnit 4 (starsze projekty)

```java
import io.cucumber.junit.Cucumber;
import io.cucumber.junit.CucumberOptions;
import org.junit.runner.RunWith;

@RunWith(Cucumber.class)
@CucumberOptions(
    features = "src/test/resources/features",
    glue = "steps",
    plugin = {"pretty", "html:target/cucumber-report.html"},
    tags = "@smoke"
)
public class RunCucumberTest {
}
```

---

## Hooks – `@Before`, `@After`, `@BeforeStep`, `@AfterStep`

Hooki to metody uruchamiane wokół scenariuszy/kroków – do setupu i sprzątania (analog `@BeforeEach`/`@AfterEach` w JUnit).

```java
import io.cucumber.java.*;

public class Hooks {

    @Before                       // przed KAŻDYM scenariuszem
    public void setUp(Scenario scenario) {
        System.out.println("Start: " + scenario.getName());
        Database.startTransaction();
    }

    @After                        // po KAŻDYM scenariuszu
    public void tearDown(Scenario scenario) {
        if (scenario.isFailed()) {
            // np. zrzut ekranu w testach UI
            scenario.attach(screenshot(), "image/png", "failure");
        }
        Database.rollback();
    }

    @Before("@db")                // tylko dla scenariuszy z tagiem @db
    public void setUpDatabase() {
        Database.seed();
    }

    @BeforeStep
    public void beforeStep() { /* przed każdym krokiem */ }

    @AfterStep
    public void afterStep() { /* po każdym kroku */ }
}
```

**Kolejność wykonania:**

```
@Before (global) → @Before("@tag") → Background → kroki scenariusza → @After("@tag") → @After (global)
```

---

## Scenario Outline – scenariusze parametryzowane

Zamiast pisać 5 prawie identycznych scenariuszy, używamy tabeli `Examples`:

```gherkin
Feature: Walidacja siły hasła

  Scenario Outline: Sprawdzanie hasła
    When the user enters password "<password>"
    Then the password strength is "<strength>"

    Examples:
      | password      | strength |
      | abc           | WEAK     |
      | abc123        | MEDIUM   |
      | Abc123!@#xyz  | STRONG   |
      | 12345678      | WEAK     |
```

```java
@When("the user enters password {string}")
public void enterPassword(String password) {
    this.result = validator.check(password);
}

@Then("the password strength is {string}")
public void strengthIs(String expected) {
    assertEquals(Strength.valueOf(expected), result);
}
```

Cucumber wykona scenariusz **raz dla każdego wiersza** tabeli (tu: 4 testy).

---

## Data Tables – przekazywanie tabel danych

Gdy krok potrzebuje strukturalnych danych, można przekazać tabelę bezpośrednio:

```gherkin
  Scenario: Import wielu klientów
    Given the following customers exist:
      | name     | email             | age |
      | Jan Kowalski | jan@example.com | 30  |
      | Anna Nowak   | anna@example.com| 25  |
    Then the system has 2 customers
```

```java
import io.cucumber.java.en.Given;
import java.util.List;
import java.util.Map;

@Given("the following customers exist:")
public void customersExist(List<Map<String, String>> rows) {
    for (Map<String, String> row : rows) {
        Customer c = new Customer(
            row.get("name"),
            row.get("email"),
            Integer.parseInt(row.get("age"))
        );
        repository.save(c);
    }
}
```

### Automatyczne mapowanie na obiekty (`@DataTableType`)

```java
import io.cucumber.java.DataTableType;

public class DataTableTypes {
    @DataTableType
    public Customer customerEntry(Map<String, String> row) {
        return new Customer(
            row.get("name"),
            row.get("email"),
            Integer.parseInt(row.get("age")));
    }
}

// Wtedy step może przyjąć List<Customer> bezpośrednio:
@Given("the following customers exist:")
public void customersExist(List<Customer> customers) {
    customers.forEach(repository::save);
}
```

### Doc String – długi tekst (np. JSON)

```gherkin
  Scenario: Wysłanie żądania z body
    When I send a POST request with body:
      """
      {
        "name": "Jan",
        "amount": 100
      }
      """
    Then the response status is 201
```

```java
@When("I send a POST request with body:")
public void sendPost(String jsonBody) {
    response = httpClient.post("/api/orders", jsonBody);
}
```

---

## Tagi – filtrowanie scenariuszy

```gherkin
@smoke @regression
Feature: Logowanie

  @critical
  Scenario: Poprawne logowanie
    ...

  @wip
  Scenario: Logowanie z 2FA
    ...
```

Uruchamianie wybranych tagów:

```bash
# Maven – tylko smoke, ale bez wip
mvn test -Dcucumber.filter.tags="@smoke and not @wip"

# Tagi krytyczne LUB regresyjne
mvn test -Dcucumber.filter.tags="@critical or @regression"
```

Wyrażenia tagów obsługują `and`, `or`, `not` oraz nawiasy.

---

## Współdzielenie stanu – Dependency Injection

Step definitions są często rozbite na wiele klas. Aby dzielić stan między nimi (np. obiekt `World`/kontekst), używa się **wstrzykiwania zależności**. Najprostszy moduł to **PicoContainer**:

```xml
<dependency>
    <groupId>io.cucumber</groupId>
    <artifactId>cucumber-picocontainer</artifactId>
    <version>7.18.0</version>
    <scope>test</scope>
</dependency>
```

```java
// Obiekt współdzielonego stanu – tworzony świeży dla każdego scenariusza
public class TestContext {
    public String accountId;
    public Response lastResponse;
    public Exception lastError;
}

// Klasa kroków A – wstrzyknięcie przez konstruktor
public class GivenSteps {
    private final TestContext ctx;
    public GivenSteps(TestContext ctx) { this.ctx = ctx; }   // PicoContainer wstrzyknie

    @Given("account {string}")
    public void account(String id) { ctx.accountId = id; }
}

// Klasa kroków B – ten SAM obiekt ctx w obrębie scenariusza
public class ThenSteps {
    private final TestContext ctx;
    public ThenSteps(TestContext ctx) { this.ctx = ctx; }

    @Then("the response is OK")
    public void responseOk() {
        assertEquals(200, ctx.lastResponse.status());
    }
}
```

> 💡 PicoContainer tworzy **nową instancję** kontekstu na każdy scenariusz → automatyczna izolacja testów. Alternatywy: `cucumber-spring`, `cucumber-guice`.

---

## Integracja ze Spring Boot

Najczęstszy scenariusz przemysłowy – testy akceptacyjne na realnym kontekście Springa.

```xml
<dependency>
    <groupId>io.cucumber</groupId>
    <artifactId>cucumber-spring</artifactId>
    <version>7.18.0</version>
    <scope>test</scope>
</dependency>
```

```java
import io.cucumber.spring.CucumberContextConfiguration;
import org.springframework.boot.test.context.SpringBootTest;

@CucumberContextConfiguration
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
public class CucumberSpringConfiguration {
    // Pusta klasa – tylko konfiguracja kontekstu Springa dla Cucumbera
}
```

```java
public class OrderSteps {

    @Autowired                          // pełne wstrzykiwanie beanów Springa
    private OrderService orderService;

    @Autowired
    private TestRestTemplate restTemplate;

    @When("I create an order for {int} items")
    public void createOrder(int qty) {
        order = orderService.create(qty);
    }

    @Then("the order is saved in the database")
    public void orderSaved() {
        assertTrue(orderService.exists(order.getId()));
    }
}
```

---

## Praktyczny przykład E2E: testowanie REST API (Cucumber + REST-assured)

```gherkin
Feature: API zamówień

  Scenario: Utworzenie zamówienia
    Given the API is available
    When I POST to "/api/orders" with body:
      """
      { "product": "laptop", "quantity": 2 }
      """
    Then the response status is 201
    And the response field "status" equals "CREATED"
```

```java
import io.cucumber.java.en.*;
import io.restassured.response.Response;
import static io.restassured.RestAssured.*;
import static org.hamcrest.Matchers.*;

public class ApiSteps {

    private Response response;
    private String requestBody;

    @Given("the API is available")
    public void apiAvailable() {
        baseURI = "http://localhost:8080";
    }

    @When("I POST to {string} with body:")
    public void postWithBody(String path, String body) {
        response = given()
            .contentType("application/json")
            .body(body)
            .when()
            .post(path);
    }

    @Then("the response status is {int}")
    public void responseStatusIs(int status) {
        response.then().statusCode(status);
    }

    @Then("the response field {string} equals {string}")
    public void responseFieldEquals(String field, String value) {
        response.then().body(field, equalTo(value));
    }
}
```

---

## Raporty

Cucumber generuje raporty przez pluginy (parametr `cucumber.plugin`):

| Plugin | Wynik |
|--------|-------|
| `pretty` | czytelny wynik w konsoli |
| `html:target/report.html` | raport HTML |
| `json:target/cucumber.json` | JSON (do dalszej obróbki, np. Allure) |
| `junit:target/cucumber.xml` | JUnit XML (dla CI/Jenkins) |
| `cucumber.publish.enabled=true` | publikacja na reports.cucumber.io |

Dla bogatych raportów popularny jest plugin Maven **`maven-cucumber-reporting`** (na podstawie pliku JSON) lub integracja z **Allure**.

---

## Struktura projektu

```
src
├── main/java/...                    # kod produkcyjny
└── test
    ├── java
    │   ├── runner
    │   │   └── RunCucumberTest.java  # runner
    │   └── steps
    │       ├── AccountSteps.java     # step definitions
    │       ├── Hooks.java
    │       └── TestContext.java
    └── resources
        ├── features
        │   ├── konto.feature         # scenariusze Gherkin
        │   └── api.feature
        └── junit-platform.properties # konfiguracja
```

---

## Dobre praktyki

✅ **Pisz Gherkin językiem biznesu** – unikaj szczegółów technicznych (`kliknij przycisk #submit`). Opisuj *intencję*, nie *implementację*.

✅ **Deklaratywnie, nie imperatywnie:**
```gherkin
# ŹLE (imperatywnie, kruche):
When I enter "jan" in field "username"
And I enter "pass" in field "password"
And I click button "login"

# DOBRZE (deklaratywnie):
When I log in as a registered user
```

✅ **Reużywaj kroków** – jeden dobrze napisany krok obsługuje wiele scenariuszy.

✅ **Jeden scenariusz = jedno zachowanie** – nie testuj 10 rzeczy w jednym scenariuszu.

✅ **Izoluj stan** – używaj DI (PicoContainer/Spring), nie pól statycznych.

✅ **Używaj `Background`** dla wspólnych warunków wstępnych.

❌ **Nie używaj Cucumbera do testów jednostkowych** – narzut Gherkina nie ma tam sensu.

❌ **Unikaj logiki w plikach `.feature`** – żadnych `if`/pętli; logika należy do kodu Java.

---

## Podsumowanie

```
┌────────────────────────────────────────────────────┐
│              Kiedy używać Cucumbera?                 │
├────────────────────────────────────────────────────┤
│ ✅ Testy akceptacyjne opisujące logikę biznesową    │
│ ✅ Współpraca biznes ↔ QA ↔ dev (wspólny język)     │
│ ✅ Testy E2E / integracyjne z czytelną dokumentacją │
│ ✅ Gdy potrzebna "żywa dokumentacja" wymagań         │
├────────────────────────────────────────────────────┤
│ ❌ Czyste testy jednostkowe (użyj JUnit)            │
│ ❌ Gdy nikt z biznesu nie czyta scenariuszy         │
│ ❌ Bardzo techniczne testy niskopoziomowe            │
└────────────────────────────────────────────────────┘
```

> **TL;DR:** Cucumber = Gherkin (`.feature`) + Step Definitions (Java) + Runner (JUnit Platform). Opisujesz zachowanie po ludzku, wiążesz je z kodem przez adnotacje `@Given/@When/@Then`, a Cucumber wykonuje to jako test. Największa wartość: **żywa dokumentacja** i **wspólny język** zespołu.

---

## Powiązane notatki

- [[frameworki-do-testów-java]] – przegląd frameworków testowych w Javie
- [[junit-i-jupyter-w-javie]] – JUnit 5 / JUnit Platform (silnik uruchamiający Cucumbera)
- [[testowanie-aplikacji-java-spring-kompleksowo]] – testowanie aplikacji Spring
- [[frameworki-do-testów-java]] – Karate jako alternatywa BDD dla API
