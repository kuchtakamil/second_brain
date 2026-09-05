# Testowanie aplikacji Java i Spring — kompleksowo

**Data:** 2026-06-05

---

Kompleksowy przegląd technicznych aspektów testowania aplikacji w najpopularniejszych frameworkach ekosystemu Java (ze szczególnym uwzględnieniem Springa): rodzaje testów, używane biblioteki, kluczowe klasy i adnotacje wraz z przykładami kodu.

Powiązane notatki: [[frameworki-do-testów-java]], [[junit-i-jupyter-w-javie]], [[injectmocks-w-mockito]], [[mockito-doanswer-vs-thenreturn]], [[zamokowanie-metody-statycznej]], [[weryfikacja-logów-w-junit]], [[uruchamianie-testów-w-maven]], [[próba-przetestowania-prywatnych-metod-w-junit]].

---

## 1. Piramida testów

Zdrowa strategia testowania opiera się na **piramidzie testów**:

```
        /\        E2E / UI        (mało, wolne, kruche, drogie)
       /  \
      /----\      Integracyjne    (średnio — DB, HTTP, kolejki)
     /      \
    /--------\    Jednostkowe      (dużo, szybkie, izolowane, tanie)
```

- **Testy jednostkowe (unit)** — pojedyncza klasa/metoda w izolacji, zależności mockowane. Milisekundy.
- **Testy integracyjne** — współpraca wielu komponentów (warstwa danych, kontrolery, kolejki, realna baza). Sekundy.
- **Testy E2E / akceptacyjne** — pełny przepływ z perspektywy użytkownika lub klienta API, uruchomiona aplikacja. Sekundy–minuty.

W praktyce dochodzą jeszcze: **testy kontraktowe** (Spring Cloud Contract / Pact), **testy architektury** (ArchUnit), **testy mutacyjne** (PIT) i **testy wydajnościowe** (Gatling, JMeter).

---

## 2. Fundament: JUnit 5 (Jupiter)

JUnit 5 to de facto standard. Składa się z trzech modułów (zob. [[junit-i-jupyter-w-javie]]):

- **JUnit Platform** — uruchamianie testów, integracja z IDE i CI.
- **JUnit Jupiter** — nowe API do pisania testów (adnotacje, asercje).
- **JUnit Vintage** — kompatybilność wsteczna z JUnit 3/4.

### Kluczowe adnotacje cyklu życia

| Adnotacja | Znaczenie |
|-----------|-----------|
| `@Test` | oznacza metodę testową |
| `@BeforeEach` / `@AfterEach` | przed/po każdym teście |
| `@BeforeAll` / `@AfterAll` | raz przed/po wszystkich testach (metoda `static`) |
| `@DisplayName` | czytelna nazwa testu |
| `@Disabled` | wyłącza test |
| `@Nested` | grupuje testy w klasie wewnętrznej |
| `@Tag` | tagowanie do selektywnego uruchamiania |
| `@ParameterizedTest` | test parametryzowany |
| `@RepeatedTest` | powtarzanie testu N razy |
| `@ExtendWith` | rejestracja rozszerzenia (Mockito, Spring) |
| `@Timeout` | limit czasu wykonania |

### Przykład — struktura i asercje

```java
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Kalkulator")
class CalculatorTest {

    private Calculator calc;

    @BeforeEach
    void setUp() {
        calc = new Calculator();
    }

    @Test
    @DisplayName("dodawanie dwóch liczb dodatnich")
    void addsTwoPositiveNumbers() {
        assertEquals(5, calc.add(2, 3));
    }

    @Test
    void throwsOnDivisionByZero() {
        ArithmeticException ex = assertThrows(
                ArithmeticException.class,
                () -> calc.divide(1, 0));
        assertTrue(ex.getMessage().contains("zero"));
    }

    @Test
    void groupedAssertions() {
        var user = new User("Anna", "anna@example.com");
        assertAll("user",
                () -> assertEquals("Anna", user.name()),
                () -> assertTrue(user.email().contains("@")));
    }
}
```

### Testy parametryzowane

```java
@ParameterizedTest
@ValueSource(strings = {"", " ", "\t"})
void blankStringsAreInvalid(String input) {
    assertFalse(Validator.isValid(input));
}

@ParameterizedTest
@CsvSource({"2,3,5", "0,0,0", "-1,1,0"})
void addsNumbers(int a, int b, int expected) {
    assertEquals(expected, calc.add(a, b));
}

@ParameterizedTest
@MethodSource("provideUsers")
void validatesUsers(User user, boolean expected) {
    assertEquals(expected, user.isValid());
}

static Stream<Arguments> provideUsers() {
    return Stream.of(
        Arguments.of(new User("Anna", "anna@x.pl"), true),
        Arguments.of(new User("", "bad"), false)
    );
}
```

> **TestNG** to alternatywa dla JUnit, popularna zwłaszcza w testach E2E/integracyjnych (grupy testów, zależności, parametry XML, wbudowane wsparcie dla równoległości). W projektach Springowych dominuje jednak JUnit 5.

---

## 3. Biblioteki asercji i mockowania

### AssertJ — płynne (fluent) asercje

AssertJ daje czytelniejsze, łańcuchowe asercje niż wbudowane `Assertions`:

```java
import static org.assertj.core.api.Assertions.*;

assertThat(result).isEqualTo(5);

assertThat(users)
        .hasSize(3)
        .extracting(User::name)
        .containsExactly("Anna", "Bob", "Cyryl");

assertThat(user.email())
        .isNotBlank()
        .contains("@")
        .endsWith(".pl");

assertThatThrownBy(() -> calc.divide(1, 0))
        .isInstanceOf(ArithmeticException.class)
        .hasMessageContaining("zero");
```

**Hamcrest** (matchery `assertThat(x, is(...))`) jest starszą alternatywą — wciąż spotykaną, ale AssertJ wyparł go w nowych projektach.

### Mockito — mockowanie zależności

Najpopularniejszy framework do mockowania. Zob. [[injectmocks-w-mockito]], [[mockito-doanswer-vs-thenreturn]], [[dopasowanie-argumentów-w-java]].

**Kluczowe adnotacje i klasy:**

- `@Mock` — tworzy mock zależności,
- `@InjectMocks` — wstrzykuje mocki do testowanej klasy,
- `@Spy` — częściowy mock (realny obiekt z możliwością nadpisania),
- `@Captor` — `ArgumentCaptor` do przechwytywania argumentów,
- `@ExtendWith(MockitoExtension.class)` — integracja z JUnit 5.

```java
import org.mockito.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import static org.mockito.Mockito.*;
import static org.mockito.ArgumentMatchers.*;

@ExtendWith(MockitoExtension.class)
class OrderServiceTest {

    @Mock
    private PaymentGateway gateway;

    @Mock
    private OrderRepository repository;

    @InjectMocks
    private OrderService service;

    @Captor
    private ArgumentCaptor<Order> orderCaptor;

    @Test
    void chargesAndSavesOrder() {
        // given — stubbing
        when(gateway.charge(anyLong(), eq("PLN"))).thenReturn(true);

        // when
        service.placeOrder(100L, "PLN");

        // then — weryfikacja interakcji
        verify(gateway).charge(100L, "PLN");
        verify(repository).save(orderCaptor.capture());
        assertThat(orderCaptor.getValue().status()).isEqualTo(PAID);

        verifyNoMoreInteractions(gateway);
    }

    @Test
    void rethrowsWhenGatewayFails() {
        when(gateway.charge(anyLong(), anyString()))
                .thenThrow(new GatewayException("timeout"));

        assertThatThrownBy(() -> service.placeOrder(50L, "PLN"))
                .isInstanceOf(OrderFailedException.class);

        verify(repository, never()).save(any());
    }
}
```

**Stubbing — różne style:**

```java
when(repo.findById(1L)).thenReturn(Optional.of(user));   // wartość
when(repo.findById(2L)).thenThrow(new RuntimeException()); // wyjątek
doNothing().when(repo).deleteById(anyLong());              // metoda void
doAnswer(inv -> inv.getArgument(0)).when(repo).save(any()); // dynamiczna odpowiedź
```

**Mockowanie metod statycznych** (Mockito 3.4+, `mockito-inline` / od 5.x domyślnie) — zob. [[zamokowanie-metody-statycznej]]:

```java
try (MockedStatic<Instant> mocked = mockStatic(Instant.class)) {
    mocked.when(Instant::now).thenReturn(Instant.EPOCH);
    assertThat(service.timestamp()).isEqualTo(0L);
}
```

---

## 4. Testowanie w Spring Boot

### Starter testowy

Wystarczy jedna zależność — `spring-boot-starter-test` — która ściąga JUnit 5, Spring Test, AssertJ, Hamcrest, Mockito, JSONassert i JsonPath:

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-test</artifactId>
    <scope>test</scope>
</dependency>
```

Spring oferuje dwa podejścia: **pełny kontekst** (`@SpringBootTest`) oraz **testy plasterkowe / slice tests** (ładują tylko fragment kontekstu — szybsze i bardziej ukierunkowane).

### Kluczowe adnotacje Spring Test

| Adnotacja | Zastosowanie |
|-----------|--------------|
| `@SpringBootTest` | ładuje pełny kontekst aplikacji |
| `@WebMvcTest` | tylko warstwa web MVC (kontrolery) |
| `@WebFluxTest` | warstwa web reaktywnego (WebFlux) |
| `@DataJpaTest` | warstwa JPA/repozytoria |
| `@JdbcTest` | warstwa JDBC |
| `@DataMongoTest`, `@DataRedisTest` | odpowiednie warstwy NoSQL |
| `@JsonTest` | serializacja/deserializacja JSON |
| `@RestClientTest` | klienci REST (`RestTemplate`, `RestClient`) |
| `@MockBean` / `@MockitoBean` | mock bean w kontekście Springa |
| `@SpyBean` / `@MockitoSpyBean` | spy bean w kontekście |
| `@TestConfiguration` | dodatkowa konfiguracja tylko dla testów |
| `@ActiveProfiles("test")` | aktywuje profil testowy |
| `@TestPropertySource` / `@DynamicPropertySource` | nadpisanie properties |
| `@Sql` | wykonanie skryptu SQL przed/po teście |
| `@DirtiesContext` | wymusza przebudowę kontekstu |
| `@Transactional` | rollback transakcji po teście |

> Uwaga wersyjna: w Spring Framework 6.2 / Spring Boot 3.4 `@MockBean` i `@SpyBean` zostały oznaczone jako *deprecated* na rzecz `@MockitoBean` i `@MockitoSpyBean`. W starszych projektach nadal spotyka się `@MockBean`.

### Testy jednostkowe serwisu w Springu

Najlepsza praktyka: serwis testuj **bez** kontekstu Springa — czystym Mockito (szybko). Kontekst rezerwuj dla testów integracyjnych.

```java
@ExtendWith(MockitoExtension.class)
class UserServiceTest {
    @Mock UserRepository repo;
    @InjectMocks UserService service;

    @Test
    void returnsUserName() {
        when(repo.findById(1L)).thenReturn(Optional.of(new User(1L, "Anna")));
        assertThat(service.nameOf(1L)).isEqualTo("Anna");
    }
}
```

---

## 5. Testowanie warstwy web — `@WebMvcTest` + MockMvc

`@WebMvcTest` ładuje tylko warstwę MVC (kontrolery, filtry, `@ControllerAdvice`, konwersja JSON) — **bez** warstwy serwisów i bazy. Zależności kontrolera dostarcza się jako `@MockitoBean`.

```java
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.beans.factory.annotation.Autowired;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(UserController.class)
class UserControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockitoBean   // dawniej @MockBean
    private UserService userService;

    @Test
    void returnsUserAsJson() throws Exception {
        when(userService.findById(1L))
                .thenReturn(new UserDto(1L, "Anna"));

        mockMvc.perform(get("/api/users/1")
                        .accept(MediaType.APPLICATION_JSON))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value(1))
                .andExpect(jsonPath("$.name").value("Anna"));
    }

    @Test
    void returns404WhenMissing() throws Exception {
        when(userService.findById(99L))
                .thenThrow(new UserNotFoundException(99L));

        mockMvc.perform(get("/api/users/99"))
                .andExpect(status().isNotFound());
    }

    @Test
    void validatesRequestBody() throws Exception {
        mockMvc.perform(post("/api/users")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"name\":\"\"}"))
                .andExpect(status().isBadRequest());
    }
}
```

Dla **WebFlux** (reaktywnie) używa się `@WebFluxTest` i `WebTestClient`:

```java
@WebFluxTest(UserController.class)
class UserControllerReactiveTest {
    @Autowired WebTestClient client;
    @MockitoBean UserService service;

    @Test
    void returnsUser() {
        when(service.findById(1L)).thenReturn(Mono.just(new UserDto(1L, "Anna")));

        client.get().uri("/api/users/1")
              .exchange()
              .expectStatus().isOk()
              .expectBody()
              .jsonPath("$.name").isEqualTo("Anna");
    }
}
```

---

## 6. Testowanie warstwy danych — `@DataJpaTest`

`@DataJpaTest` ładuje tylko komponenty JPA (encje, repozytoria, `EntityManager`), domyślnie z bazą **in-memory (H2)** i transakcją wycofywaną po każdym teście.

```java
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;

@DataJpaTest
class UserRepositoryTest {

    @Autowired
    private UserRepository repository;

    @Autowired
    private TestEntityManager entityManager;  // pomocnik do przygotowania danych

    @Test
    void findsByEmail() {
        entityManager.persistAndFlush(new User("Anna", "anna@x.pl"));

        Optional<User> found = repository.findByEmail("anna@x.pl");

        assertThat(found).isPresent();
        assertThat(found.get().getName()).isEqualTo("Anna");
    }
}
```

Aby testować na **realnej bazie** (a nie H2), łączy się to z Testcontainers (sekcja 7) i `@AutoConfigureTestDatabase(replace = NONE)`.

Inicjalizacja danych skryptem SQL:

```java
@Test
@Sql("/test-data/users.sql")
@Sql(scripts = "/test-data/cleanup.sql", executionPhase = AFTER_TEST_METHOD)
void worksWithSeededData() { ... }
```

---

## 7. Testy integracyjne z `@SpringBootTest` i Testcontainers

`@SpringBootTest` ładuje **cały** kontekst aplikacji. Z parametrem `webEnvironment` uruchamia realny serwer na losowym porcie.

```java
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
class UserApiIntegrationTest {

    @Autowired
    private TestRestTemplate restTemplate;   // klient HTTP do realnego serwera

    @Test
    void createsAndFetchesUser() {
        var request = new CreateUserRequest("Anna", "anna@x.pl");

        ResponseEntity<UserDto> response =
                restTemplate.postForEntity("/api/users", request, UserDto.class);

        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.CREATED);
        assertThat(response.getBody().name()).isEqualTo("Anna");
    }
}
```

### Testcontainers — realne zależności w Dockerze

[Testcontainers](https://testcontainers.com) uruchamia prawdziwe kontenery (PostgreSQL, Kafka, Redis, RabbitMQ…) na czas testów — najwierniejsze środowisko integracyjne.

**Adnotacje i klasy:** `@Testcontainers`, `@Container`, klasy `PostgreSQLContainer`, `KafkaContainer`, `GenericContainer`. Od **Spring Boot 3.1** dochodzi adnotacja `@ServiceConnection`, która automatycznie wpina kontener do konfiguracji Springa (bez ręcznego `@DynamicPropertySource`).

```java
import org.testcontainers.junit.jupiter.Testcontainers;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.containers.PostgreSQLContainer;
import org.springframework.boot.testcontainers.service.connection.ServiceConnection;

@SpringBootTest
@Testcontainers
class OrderRepositoryIT {

    @Container
    @ServiceConnection                          // Spring Boot 3.1+: auto-konfiguracja datasource
    static PostgreSQLContainer<?> postgres =
            new PostgreSQLContainer<>("postgres:16-alpine");

    @Autowired
    private OrderRepository repository;

    @Test
    void persistsOrderInRealPostgres() {
        Order saved = repository.save(new Order("ABC", 100));
        assertThat(repository.findById(saved.getId())).isPresent();
    }
}
```

Wariant klasyczny (przed 3.1) — ręczne mapowanie properties:

```java
@DynamicPropertySource
static void props(DynamicPropertyRegistry registry) {
    registry.add("spring.datasource.url", postgres::getJdbcUrl);
    registry.add("spring.datasource.username", postgres::getUsername);
    registry.add("spring.datasource.password", postgres::getPassword);
}
```

### WireMock — mockowanie zewnętrznych API

Gdy aplikacja woła zewnętrzny serwis HTTP, [WireMock](https://wiremock.org) stawia atrapę serwera ze zdefiniowanymi odpowiedziami:

```java
@SpringBootTest
@WireMockTest(httpPort = 8089)
class PaymentClientIT {

    @Test
    void handlesGatewayResponse() {
        stubFor(post("/charge")
                .willReturn(okJson("{\"status\":\"PAID\"}")));

        var result = paymentClient.charge(100L);

        assertThat(result.status()).isEqualTo("PAID");
        verify(postRequestedFor(urlEqualTo("/charge")));
    }
}
```

---

## 8. Testy E2E i testowanie API

### REST Assured — testowanie API od podstaw

REST Assured to najpopularniejsza biblioteka Javy do testowania **REST API z perspektywy klienta**: wysyła prawdziwe żądania HTTP i weryfikuje odpowiedzi za pomocą czytelnego DSL w stylu BDD `given / when / then`. Nie jest związana ze Springiem — testuje przez HTTP, więc działa tak samo z aplikacją Spring Boot, Quarkusem czy dowolnym zdalnym serwisem. Najczęściej łączy się ją z `@SpringBootTest(webEnvironment = RANDOM_PORT)`, żeby uderzać w realnie uruchomioną aplikację.

#### Zależność (Maven) i importy

```xml
<dependency>
    <groupId>io.rest-assured</groupId>
    <artifactId>rest-assured</artifactId>
    <version>5.5.0</version>
    <scope>test</scope>
</dependency>
```

DSL opiera się na statycznych importach:

```java
import static io.restassured.RestAssured.*;        // given(), when(), get()...
import static org.hamcrest.Matchers.*;             // equalTo(), hasItem()...
import io.restassured.http.ContentType;
```

Do (de)serializacji JSON RestAssured używa Jacksona albo Gsona, jeśli są na ścieżce klas — w Spring Boot są domyślnie, więc obiekty POJO „po prostu działają".

#### Anatomia testu: given / when / then

Trzy bloki opisują kolejno **stan żądania**, **akcję** i **weryfikację odpowiedzi**:

```java
given()                                  // 1. przygotowanie żądania
    .baseUri("http://localhost")
    .port(8080)
    .header("Authorization", "Bearer " + token)
    .contentType(ContentType.JSON)
    .body(payload)
.when()                                  // 2. wykonanie
    .post("/api/users")
.then()                                  // 3. asercje na odpowiedzi
    .statusCode(201)
    .body("name", equalTo("Anna"));
```

- `given()` — wszystko, co opisuje żądanie: adres, nagłówki, parametry, ciało, uwierzytelnianie.
- `when()` — metoda HTTP i ścieżka: `get`, `post`, `put`, `patch`, `delete`.
- `then()` — asercje na statusie, ciele, nagłówkach, cookies, czasie odpowiedzi.

> `given/when/then` to czytelne aliasy — technicznie wystarczyłoby `given().get("/x").then()...`. Wcięcia z kropką na początku linii (`.when()`, `.then()`) to tylko konwencja formatowania poprawiająca czytelność.

#### Budowanie żądania (blok `given`)

| Element żądania | Metoda | Przykład |
|-----------------|--------|----------|
| Adres bazowy / port / prefiks | `baseUri`, `port`, `basePath` | `.baseUri("http://localhost").port(8080)` |
| Nagłówek | `header`, `headers` | `.header("Accept", "application/json")` |
| Typ treści / akceptowany | `contentType`, `accept` | `.contentType(ContentType.JSON)` |
| Parametr zapytania (query) | `queryParam` | `.queryParam("page", 2)` |
| Parametr ścieżki (path) | `pathParam` | `.pathParam("id", 1).get("/users/{id}")` |
| Parametr formularza | `formParam` | `.formParam("user", "anna")` |
| Ciało (JSON) | `body` | `.body(new CreateUserRequest(...))` |
| Plik / multipart | `multiPart` | `.multiPart("file", new File("a.png"))` |
| Cookie | `cookie` | `.cookie("session", "abc")` |

Ciało można podać jako surowy string, mapę albo obiekt (POJO) — RestAssured sam zserializuje go do JSON:

```java
given()
    .contentType(ContentType.JSON)
    .body(Map.of("name", "Anna", "email", "anna@x.pl"));   // albo POJO, albo surowy String
```

#### Asercje na odpowiedzi (blok `then`) — JsonPath / GPath

Pola w ciele JSON adresuje się **składnią GPath** (Groovy: kropki, indeksy, filtry), a wartości sprawdza **matcherami Hamcresta**:

```java
.then()
    .statusCode(200)
    .contentType(ContentType.JSON)
    .header("Cache-Control", containsString("no-cache"))
    .time(lessThan(2000L))                       // czas odpowiedzi < 2 s
    .body("name", equalTo("Anna"))               // pole proste
    .body("address.city", equalTo("Kraków"))     // pole zagnieżdżone
    .body("roles", hasItem("ADMIN"))             // element listy
    .body("orders.size()", equalTo(3))           // rozmiar kolekcji
    .body("orders[0].id", notNullValue())        // indeks
    .body("orders.findAll { it.total > 100 }.size()", equalTo(2)); // filtr GPath
```

Najczęstsze matchery: `equalTo`, `notNullValue`, `nullValue`, `hasItem`, `hasItems`, `hasSize`, `containsString`, `startsWith`, `greaterThan`, `lessThan`, `everyItem`.

#### Wyciąganie danych z odpowiedzi (`extract`)

Gdy wartość z jednej odpowiedzi (np. `id` utworzonego zasobu) jest potrzebna w kolejnym kroku, używa się `extract()`:

```java
// pojedyncza wartość po GPath
long id =
    given().contentType(ContentType.JSON).body(payload)
    .when().post("/api/users")
    .then().statusCode(201)
    .extract().path("id");

// cała odpowiedź zdeserializowana do POJO
UserDto user =
    given()
    .when().get("/api/users/1")
    .then().statusCode(200)
    .extract().as(UserDto.class);

// lista wartości
List<String> names =
    given()
    .when().get("/api/users")
    .then().extract().jsonPath().getList("name", String.class);

// pełny obiekt Response (gdy potrzeba i statusu, i ciała, i nagłówków naraz)
Response response = given().when().get("/api/users/1");
assertThat(response.statusCode()).isEqualTo(200);
assertThat(response.jsonPath().getString("name")).isEqualTo("Anna");
```

#### Uwierzytelnianie

```java
given().auth().basic("anna", "secret")...                   // Basic Auth
given().auth().preemptive().basic("anna", "secret")...      // bez czekania na 401
given().auth().oauth2(accessToken)...                        // Bearer / OAuth2
given().header("Authorization", "Bearer " + jwt)...          // ręcznie nagłówkiem
```

#### Specyfikacje wielokrotnego użytku — `RequestSpecification` / `ResponseSpecification`

Powtarzalną konfigurację (baseURI, port, nagłówki, autoryzację) warto wyciągnąć do **specyfikacji** i współdzielić między testami — eliminuje to duplikację:

```java
RequestSpecification apiSpec = new RequestSpecBuilder()
    .setBaseUri("http://localhost")
    .setPort(port)
    .setContentType(ContentType.JSON)
    .addHeader("Authorization", "Bearer " + token)
    .build();

ResponseSpecification okJson = new ResponseSpecBuilder()
    .expectStatusCode(200)
    .expectContentType(ContentType.JSON)
    .build();

given().spec(apiSpec)
.when().get("/api/users/1")
.then().spec(okJson)
    .body("name", equalTo("Anna"));
```

Globalnie można też ustawić `RestAssured.requestSpecification = apiSpec;` w `@BeforeAll`.

#### Logowanie i diagnostyka

```java
given().log().all()                       // zaloguj całe żądanie
.when().get("/api/users/1")
.then().log().ifValidationFails()         // zaloguj odpowiedź tylko gdy asercja padnie
    .statusCode(200);
```

Przydatne warianty: `log().body()`, `log().headers()`, `log().ifError()`. Globalnie: `RestAssured.enableLoggingOfRequestAndResponseIfValidationFails();`.

#### Walidacja schematu JSON

Z modułem `json-schema-validator` można sprawdzić zgodność odpowiedzi ze schematem:

```java
.then().body(matchesJsonSchemaInClasspath("schemas/user-schema.json"));
```

#### Pełny przykład integracyjny ze Spring Boot

W teście z realnym serwerem na losowym porcie wstrzykujemy port i podajemy go RestAssured (najczystszy: w `@BeforeEach`):

```java
import static io.restassured.RestAssured.*;
import static org.hamcrest.Matchers.*;
import io.restassured.RestAssured;
import io.restassured.http.ContentType;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.server.LocalServerPort;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
class UserApiE2ETest {

    @LocalServerPort int port;

    @BeforeEach
    void setUp() {
        RestAssured.port = port;
        RestAssured.baseURI = "http://localhost";
    }

    @Test
    void createsAndReadsUser() {
        // 1. utworzenie zasobu i wyciągnięcie id
        long id =
            given()
                .contentType(ContentType.JSON)
                .body("""
                      { "name": "Anna", "email": "anna@x.pl" }
                      """)
            .when()
                .post("/api/users")
            .then()
                .statusCode(201)
                .body("name", equalTo("Anna"))
                .body("id", notNullValue())
                .extract().path("id");

        // 2. odczyt utworzonego zasobu po jego id
        given()
            .pathParam("id", id)
        .when()
            .get("/api/users/{id}")
        .then()
            .statusCode(200)
            .body("email", equalTo("anna@x.pl"));
    }
}
```

**Wariant bez startowania serwera — `RestAssuredMockMvc`.** Pozwala używać DSL RestAssured na warstwie `MockMvc` (szybkie testy kontrolera, jak przy `@WebMvcTest`, bez realnego portu):

```java
import static io.restassured.module.mockmvc.RestAssuredMockMvc.*;

RestAssuredMockMvc.mockMvc(mockMvc);          // albo .standaloneSetup(new UserController(...))

given().contentType(ContentType.JSON)
.when().get("/api/users/1")
.then().statusCode(200).body("name", equalTo("Anna"));
```

(Wymaga modułu `io.rest-assured:spring-mock-mvc`.)

#### Najczęstsze pułapki

- **Brak ustawionego portu/baseURI** → żądania lecą na domyślny `localhost:8080`. W teście z `RANDOM_PORT` zawsze ustaw `RestAssured.port = port`.
- **GPath ≠ JsonPath z MockMvc** — w RestAssured `body("orders[0].id", ...)` (GPath/Groovy), w MockMvc `jsonPath("$.orders[0].id")` (notacja `$`). Łatwo pomylić składnie.
- **Stan globalny** — `RestAssured.port`, `baseURI`, `requestSpecification` to pola statyczne; resetuj je (`RestAssured.reset()`) między klasami, by uniknąć przecieku konfiguracji.
- **Asercja vs wyciąganie** — `then().body(...)` *weryfikuje*, a `extract()` *zwraca* wartość; nie myl jednego z drugim.

### Selenium / Playwright — E2E przez przeglądarkę

Do testów UI uruchamianych w realnej przeglądarce (pełny przepływ użytkownika):

```java
// Selenium WebDriver
@Test
void userCanLogIn() {
    WebDriver driver = new ChromeDriver();
    driver.get("http://localhost:8080/login");
    driver.findElement(By.id("username")).sendKeys("anna");
    driver.findElement(By.id("password")).sendKeys("secret");
    driver.findElement(By.id("submit")).click();
    assertThat(driver.findElement(By.id("welcome")).getText())
            .contains("Witaj, Anna");
    driver.quit();
}
```

**Playwright** (nowocześniejsza alternatywa Selenium) oraz **Karate** (DSL łączące testy API i E2E) to częste wybory w nowszych projektach. Często łączy się je z Testcontainers, aby postawić całe środowisko (aplikacja + baza + przeglądarka).

### Czy test E2E przez UI przechodzi przez wszystkie warstwy backendu?

**Tak — i to jest właśnie sedno testu end-to-end.** Klikając w UI, test nie „wie" nic o wewnętrznej budowie aplikacji — odpala realny przepływ przez **całą pionową ścieżkę**:

```
Przeglądarka (Selenium/Playwright)
   │  klik / wpisanie / submit
   ▼
Frontend (HTML/JS, np. React, Thymeleaf)
   │  realne żądanie HTTP
   ▼
@Controller / @RestController   ← warstwa web (routing, walidacja, serializacja)
   ▼
@Service                         ← logika biznesowa, transakcje
   ▼
@Repository / EntityManager      ← warstwa dostępu do danych (JPA/JDBC)
   ▼
Baza danych                      ← realne zapisy/odczyty (np. PostgreSQL w Testcontainers)
   │
   └─▶ integracje zewnętrzne     ← kolejki (Kafka/Rabbit), inne API, płatności…
```

Dlatego E2E daje **najwyższą pewność**, że system działa jako całość: wyłapuje błędy, które testy izolowane przepuszczają — np. źle skonfigurowany mapping JSON, brakującą migrację bazy, niespójność kontraktu między frontendem a kontrolerem, problem z transakcją czy serializacją encji.

**Czym to różni się od pozostałych poziomów piramidy:**

| Poziom | Co realnie przechodzi |
|--------|----------------------|
| Unit (Mockito) | tylko jedna klasa; sąsiednie warstwy zamockowane |
| `@WebMvcTest` | tylko warstwa web; serwis i baza zamockowane/nieobecne |
| `@DataJpaTest` | tylko warstwa danych; brak web i logiki biznesowej |
| `@SpringBootTest` (API, bez UI) | wszystkie warstwy backendu — ale wejściem jest HTTP, nie przeglądarka |
| **E2E przez UI** | **frontend + wszystkie warstwy backendu + baza + integracje** |

**Dwa ważne niuanse:**

1. **Zewnętrzne systemy zwykle się podmienia.** „Pełny przepływ" nie znaczy, że test uderza w produkcyjną bramkę płatności czy cudze API — to byłoby niedeterministyczne i kosztowne. Realne pozostają warstwy *naszej* aplikacji i baza (często w Testcontainers), a zależności trzecich stron zastępuje się sandboxem dostawcy albo atrapą (WireMock). Wciąż jest to E2E z punktu widzenia naszego systemu.
2. **Koszt tej kompletności to wolne i kruche testy.** Skoro E2E przechodzi przez wszystko, każda zmiana w dowolnej warstwie (a także asynchroniczność, czasy ładowania UI) może go zepsuć. Dlatego — zgodnie z piramidą — E2E pisze się **mało**, pokrywając nimi tylko kluczowe ścieżki użytkownika (np. logowanie, złożenie zamówienia), a szczegółowe przypadki brzegowe spycha na niższe, szybsze poziomy.

> W skrócie: jeśli chcesz świadomie przetestować **wszystkie warstwy backendu naraz, ale bez kruchości i kosztu przeglądarki**, użyj `@SpringBootTest(webEnvironment = RANDOM_PORT)` + `TestRestTemplate`/REST Assured (sekcja 7–8). To „E2E na poziomie API" — przechodzi przez kontroler → serwis → repozytorium → bazę, pomijając jedynie warstwę UI.

---

## 9. Testowanie API na podstawie specyfikacji OpenAPI

### Czym jest OpenAPI (dawniej Swagger)

**OpenAPI Specification (OAS)** to standard opisu REST API w jednym pliku `openapi.yaml` / `openapi.json`: jakie są ścieżki (endpointy), metody HTTP, parametry, ciała żądań, kody i schematy odpowiedzi oraz sposób uwierzytelniania. Specyfikacja jest **czytelna dla człowieka i maszyny**, więc staje się *jedynym źródłem prawdy* o kontrakcie API — generuje się z niej dokumentację, klientów, serwery-atrapy i… testy.

> **Swagger vs OpenAPI.** Specyfikacja nazywała się „Swagger Specification" do 2016 r., kiedy przekazano ją pod OpenAPI Initiative (Linux Foundation) i przemianowano na OpenAPI. Dziś „Swagger" to marka narzędzi wokół standardu: **Swagger UI** (interaktywna dokumentacja), **Swagger Editor**, **Swagger Codegen**. Sam format to OpenAPI (aktualnie 3.0.x / 3.1.x).

### Przykład specyfikacji

Mały, ale realistyczny `openapi.yaml` dla API użytkowników:

```yaml
openapi: 3.0.3
info:
  title: User API
  version: 1.0.0
paths:
  /api/users/{id}:
    get:
      summary: Pobierz użytkownika po id
      parameters:
        - name: id
          in: path
          required: true
          schema: { type: integer, format: int64 }
      responses:
        '200':
          description: Znaleziony użytkownik
          content:
            application/json:
              schema: { $ref: '#/components/schemas/User' }
        '404':
          description: Nie znaleziono
  /api/users:
    post:
      summary: Utwórz użytkownika
      requestBody:
        required: true
        content:
          application/json:
            schema: { $ref: '#/components/schemas/CreateUserRequest' }
      responses:
        '201':
          description: Utworzono
          content:
            application/json:
              schema: { $ref: '#/components/schemas/User' }
        '400':
          description: Błędne dane wejściowe
components:
  schemas:
    User:
      type: object
      required: [id, name, email]
      properties:
        id:    { type: integer, format: int64 }
        name:  { type: string }
        email: { type: string, format: email }
    CreateUserRequest:
      type: object
      required: [name, email]
      properties:
        name:  { type: string, minLength: 1 }
        email: { type: string, format: email }
```

Kluczowe: schematy w `components/schemas` opisują **dokładny kształt** danych (wymagane pola, typy, formaty, ograniczenia) — i to względem nich narzędzia walidują ruch.

### Dwa podejścia: design-first vs code-first

- **Design-first** — najpierw piszesz `openapi.yaml` (kontrakt), a potem implementację. Z kontraktu generujesz szkielety serwera i klientów (np. **OpenAPI Generator**). Front i back mogą pracować równolegle wobec uzgodnionego kontraktu.
- **Code-first** — najpierw kod z adnotacjami, a specyfikacja jest **generowana** z aplikacji. W Spring Boot robi to **springdoc-openapi**:

  ```xml
  <dependency>
      <groupId>org.springdoc</groupId>
      <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
      <version>2.6.0</version>
  </dependency>
  ```

  Po dodaniu zależności aplikacja wystawia specyfikację pod `/v3/api-docs` (JSON) i interaktywną dokumentację pod `/swagger-ui.html`. Tę wygenerowaną specyfikację można potem podać narzędziom testującym.

### Po co testować *względem* specyfikacji

Bez tego specyfikacja i implementacja **rozjeżdżają się po cichu** — dokumentacja mówi jedno, API zwraca drugie. Testy kontraktowe oparte na OpenAPI wychwytują: brakujące/niezadeklarowane pola, złe typy, nieudokumentowane kody odpowiedzi, niezgodne formaty (`email`, `date-time`), zmiany łamiące kompatybilność. Najtaniej dokłada się je **jako dodatkową asercję do już istniejących testów API** (REST Assured / MockMvc).

### Walidacja zgodności — Atlassian Swagger Request Validator

Najlepiej pasuje do tej notatki, bo wpina się wprost w **REST Assured**, **MockMvc**, **WireMock** i **Pact**. Sprawdza, czy żądanie i odpowiedź są zgodne z kontraktem OpenAPI.

```xml
<dependency>
    <groupId>com.atlassian.oai</groupId>
    <artifactId>swagger-request-validator-restassured</artifactId>
    <version>2.43.0</version>
    <scope>test</scope>
</dependency>
```

**REST Assured** — dokładasz jeden filtr i każda interakcja jest walidowana względem `openapi.yaml`:

```java
import com.atlassian.oai.validator.restassured.OpenApiValidationFilter;
import static io.restassured.RestAssured.*;
import static org.hamcrest.Matchers.*;

private static final OpenApiValidationFilter contract =
        new OpenApiValidationFilter("openapi.yaml");   // ścieżka w classpath albo URL

@Test
void responseMatchesContract() {
    given()
        .filter(contract)               // ← waliduje żądanie i odpowiedź względem OpenAPI
        .port(port)
    .when()
        .get("/api/users/1")
    .then()
        .statusCode(200)
        .body("name", notNullValue());
    // brakujące wymagane pole / zły typ / nieudokumentowany status → test pada z opisem niezgodności
}
```

**MockMvc** (moduł `swagger-request-validator-mockmvc`) — bez startowania serwera:

```java
import static com.atlassian.oai.validator.mockmvc.OpenApiValidationMatchers.openApi;

mockMvc.perform(get("/api/users/1"))
       .andExpect(status().isOk())
       .andExpect(openApi().isValid("openapi.yaml"));   // ← walidacja kontraktu
```

Walidator można też wpiąć w **WireMock** (atrapa zewnętrznego API odrzuca odpowiedzi niezgodne z kontraktem) albo w **Pact** (testy konsumencko-producenckie).

### Specmatic — kontrakt jako test wykonywalny

[Specmatic](https://specmatic.io) traktuje plik OpenAPI jako **wykonywalny kontrakt**: sam generuje przypadki testowe z kontraktu i odpala je przeciw aplikacji, a w drugą stronę potrafi postawić **mock serwer** ze specyfikacji (do testów konsumenta). Integracja z JUnit:

```java
import io.specmatic.test.SpecmaticContractTest;

class ApiContractTest implements SpecmaticContractTest {
    @BeforeAll
    static void setUp() {
        System.setProperty("host", "localhost");
        System.setProperty("port", "8080");
        // contractPaths / specmatic.yaml wskazują na openapi.yaml
    }
}
```

Specmatic wygeneruje osobny test dla każdej ścieżki i wariantu odpowiedzi opisanych w kontrakcie.

### Generowanie testów i fuzzing ze specyfikacji

Narzędzia język-agnostyczne, które same wymyślają przypadki testowe (w tym brzegowe) na podstawie schematów:

```bash
# Schemathesis (Python) — property-based / fuzzing z OpenAPI
schemathesis run http://localhost:8080/v3/api-docs --checks all
st run openapi.yaml --base-url http://localhost:8080

# Dredd (Node.js) — sprawdza, czy działające API odpowiada zgodnie z opisem
dredd openapi.yaml http://localhost:8080
```

**Schemathesis** jest tu najsłynniejszy — generuje dane łamiące założenia (puste, skrajne, błędne typy) i wyłapuje 500-tki oraz odpowiedzi niezgodne ze schematem, których ręcznie byś nie wymyślił.

### Generowanie klienta do testów — OpenAPI Generator

Z kontraktu można wygenerować **typowanego klienta** (Java) i pisać testy na obiektach zamiast na surowym JSON:

```bash
openapi-generator-cli generate -i openapi.yaml -g java -o ./generated-client
```

### Przegląd narzędzi

| Narzędzie | Ekosystem | Co robi |
|-----------|-----------|---------|
| **Atlassian Swagger Request Validator** | Java/JVM | walidacja żądań/odpowiedzi względem OAS w REST Assured / MockMvc / WireMock / Pact |
| **Specmatic** | Java/JVM | OpenAPI jako wykonywalny kontrakt + mock serwer |
| **springdoc-openapi** | Spring Boot | generuje specyfikację z kodu (`/v3/api-docs`, Swagger UI) |
| **OpenAPI Generator** | wieloplatformowy | generuje klientów/serwery z kontraktu |
| **Schemathesis** | Python (CLI) | property-based / fuzzing z OAS |
| **Dredd** | Node.js (CLI) | weryfikacja implementacji względem opisu |
| **Prism** (Stoplight) | Node.js | mock serwer + proxy walidujące ruch |
| **assertj-swagger / Hikaku** | Java/JVM | porównanie implementacji z kontraktem (design ↔ code) |
| **RESTler** (Microsoft) | wieloplatformowy | stateful fuzzing REST API ze Swaggera |

> **W skrócie:** jeśli masz już testy API (REST Assured/MockMvc z sekcji 8) i specyfikację OpenAPI — najtańszy zysk daje **Atlassian Swagger Request Validator**: jedna linijka (`filter`/`openApi().isValid(...)`) pilnuje, by implementacja nie rozjechała się z kontraktem. Gdy chcesz iść w pełni „kontrakt-first" z automatycznym generowaniem testów i atrap — sięgnij po **Specmatic** lub **Schemathesis**.

---

## 10. Pozostałe rodzaje testów warte znajomości

- **Testy kontraktowe** — [Spring Cloud Contract](https://spring.io/projects/spring-cloud-contract) lub [Pact](https://pact.io): weryfikują zgodność kontraktu producent–konsument API bez uruchamiania obu stron jednocześnie.
- **Testy architektury** — [ArchUnit](https://www.archunit.org): asercje na strukturze kodu (np. „warstwa `controller` nie może zależeć od `repository`”).

  ```java
  @ArchTest
  static final ArchRule services_should_not_access_controllers =
      noClasses().that().resideInAPackage("..service..")
                 .should().dependOnClassesThat().resideInAPackage("..controller..");
  ```
- **Testy mutacyjne** — [PIT (pitest)](https://pitest.org): wprowadza mutacje do kodu i sprawdza, czy testy je wykrywają (jakość testów, nie tylko pokrycie).
- **BDD** — [Cucumber](https://cucumber.io) (scenariusze Gherkin) oraz [Spock](https://spockframework.org) (Groovy, ekspresyjny `given/when/then` + wbudowane mockowanie).
- **Testy wydajnościowe** — Gatling, JMeter, k6.

---

## 11. Pokrycie kodu i konfiguracja budowania

### JaCoCo — pokrycie kodu

```xml
<plugin>
    <groupId>org.jacoco</groupId>
    <artifactId>jacoco-maven-plugin</artifactId>
    <version>0.8.12</version>
    <executions>
        <execution><goals><goal>prepare-agent</goal></goals></execution>
        <execution>
            <id>report</id><phase>test</phase>
            <goals><goal>report</goal></goals>
        </execution>
    </executions>
</plugin>
```

### Maven — Surefire vs Failsafe

Konwencja oddziela testy jednostkowe od integracyjnych nazwą klas:

- **Surefire** uruchamia testy jednostkowe (`*Test`) w fazie `test`,
- **Failsafe** uruchamia testy integracyjne (`*IT`, `*ITCase`) w fazach `integration-test` / `verify`.

```bash
mvn test          # tylko unit (Surefire)
mvn verify        # unit + integracyjne (Failsafe)
```

Zob. [[uruchamianie-testów-w-maven]]. W Gradle odpowiednikiem jest osobny `testSet`/`sourceSet` dla `integrationTest` oraz zadania `test` i `integrationTest`.

---

## 12. Dobre praktyki — podsumowanie

1. **Trzymaj się piramidy** — dużo szybkich testów jednostkowych, mniej integracyjnych, najmniej E2E.
2. **Serwisy testuj czystym Mockito** (bez kontekstu Springa) — kontekst jest wolny i rezerwuj go dla testów integracyjnych.
3. **Używaj slice testów** (`@WebMvcTest`, `@DataJpaTest`) zamiast `@SpringBootTest`, gdy testujesz jedną warstwę.
4. **Struktura `given/when/then`** (Arrange–Act–Assert) — czytelność i jeden powód niepowodzenia na test.
5. **Testcontainers zamiast H2** dla wiarygodnych testów bazy — H2 różni się od produkcyjnego PostgreSQL/MySQL.
6. **`@MockitoBean` zamiast `@MockBean`** w Spring Boot 3.4+ (stara adnotacja deprecated).
7. **Izolacja testów** — każdy test niezależny; `@Transactional`/rollback lub czyszczenie danych między testami.
8. **Mierz jakość, nie tylko pokrycie** — wysokie pokrycie JaCoCo nie gwarantuje sensownych asercji; rozważ PIT.
9. **Nie testuj prywatnych metod bezpośrednio** — testuj przez API publiczne (zob. [[próba-przetestowania-prywatnych-metod-w-junit]]).
10. **Nazewnictwo `*Test` vs `*IT`** — pozwala rozdzielić szybkie i wolne testy w pipeline CI.

---

### Szybka ściąga: która adnotacja do czego

| Cel testu | Adnotacja / narzędzie |
|-----------|----------------------|
| Logika serwisu w izolacji | `@ExtendWith(MockitoExtension.class)` + `@Mock` / `@InjectMocks` |
| Kontroler REST (MVC) | `@WebMvcTest` + `MockMvc` + `@MockitoBean` |
| Kontroler reaktywny | `@WebFluxTest` + `WebTestClient` |
| Repozytorium / JPA | `@DataJpaTest` + `TestEntityManager` |
| Pełna aplikacja + HTTP | `@SpringBootTest(webEnvironment = RANDOM_PORT)` + `TestRestTemplate` |
| Realna baza / kolejka | Testcontainers (`@Testcontainers`, `@Container`, `@ServiceConnection`) |
| Zewnętrzne API | WireMock |
| Testy API w stylu BDD | REST Assured / Karate |
| UI E2E | Selenium / Playwright |
| Kontrakty API | Spring Cloud Contract / Pact |
| Reguły architektury | ArchUnit |
