# Pytania rekrutacyjne — Spring 3.0

Lista pytań na rozmowę kwalifikacyjną dotyczących ekosystemu **Spring Framework 3.x** i powiązanych modułów. Pytania pogrupowane tematycznie.

---

## 1. Spring Core / IoC Container

### 1. Czym jest kontener IoC w Spring i jakie są jego dwie główne implementacje (`BeanFactory` vs `ApplicationContext`)?

**IoC (Inversion of Control)** to zasada, w której kontener przejmuje odpowiedzialność za tworzenie obiektów i zarządzanie ich zależnościami — zamiast tego, żeby programista ręcznie wywoływał `new`.

Dwie główne implementacje:

| Cecha | `BeanFactory` | `ApplicationContext` |
|---|---|---|
| Inicjalizacja beanów | **Lazy** — bean tworzony dopiero przy pierwszym wywołaniu `getBean()` | **Eager** — wszystkie singletony tworzone przy starcie kontekstu |
| Event system | ❌ Brak | ✅ `ApplicationEvent` / `@EventListener` |
| Internacjonalizacja (i18n) | ❌ Brak | ✅ `MessageSource` |
| Integracja z AOP | Ograniczona | Pełna |
| Typowe użycie | Środowiska z ograniczonymi zasobami (rzadko spotykane) | Standardowy wybór w każdej aplikacji Spring |

`ApplicationContext` rozszerza `BeanFactory` i dodaje funkcjonalności enterprise. W praktyce **zawsze** używa się `ApplicationContext` (np. `AnnotationConfigApplicationContext`, `ClassPathXmlApplicationContext` lub — w Spring Boot — automatycznie tworzony kontekst).

```java
// Programistyczne tworzenie kontekstu
ApplicationContext ctx = new AnnotationConfigApplicationContext(AppConfig.class);
MyService service = ctx.getBean(MyService.class);
```

---

### 2. Jakie są różnice między wstrzykiwaniem przez konstruktor, setter i pole (`@Autowired` na polu)?

**Konstruktor:**
```java
@Service
public class OrderService {
    private final PaymentGateway gateway;

    // @Autowired opcjonalne dla jedynego konstruktora (od Spring 4.3)
    public OrderService(PaymentGateway gateway) {
        this.gateway = gateway;
    }
}
```
- Zależność jest **wymagana** (nie może być `null`)
- Pole może być `final` → obiekt jest **niemutowalny**
- Łatwe do testowania — wystarczy `new OrderService(mockGateway)`

**Setter:**
```java
@Service
public class OrderService {
    private PaymentGateway gateway;

    @Autowired
    public void setGateway(PaymentGateway gateway) {
        this.gateway = gateway;
    }
}
```
- Zależność **opcjonalna** (można ustawić `@Autowired(required = false)`)
- Pole **nie może** być `final`
- Przydatne przy zależnościach opcjonalnych lub rekonfigurowalnych

**Pole (field injection):**
```java
@Service
public class OrderService {
    @Autowired
    private PaymentGateway gateway;
}
```
- Najkrótszy zapis, ale **najtrudniejszy do testowania** (wymaga refleksji lub frameworka mockującego)
- Ukrywa zależności — nie widać ich w API klasy
- Pole nie może być `final`

---

### 3. Kiedy i dlaczego warto preferować wstrzykiwanie przez konstruktor?

Wstrzykiwanie przez konstruktor jest **oficjalnie rekomendowane** przez zespół Spring. Powody:

1. **Niemutowalność** — pola mogą być `final`, co gwarantuje thread-safety i zapobiega przypadkowej zmianie referencji.
2. **Wymagane zależności są jawne** — konstruktor wymusza podanie wszystkich zależności, nie da się stworzyć obiektu w nieprawidłowym stanie.
3. **Łatwe testowanie** — `new MyService(mockA, mockB)` bez Springa, refleksji ani `@InjectMocks`.
4. **Detekcja cykli** — Spring rzuci `BeanCurrentlyInCreationException` przy starcie, a nie w runtime.
5. **Czytelność** — lista parametrów konstruktora od razu pokazuje, od czego zależy klasa. Jeśli jest ich dużo, to sygnał do refaktoryzacji (Single Responsibility Principle).

> Od Spring 4.3 adnotacja `@Autowired` jest opcjonalna, jeśli klasa ma **dokładnie jeden** konstruktor.

---

### 4. Czym różni się `@Component` od `@Bean`?

| Cecha | `@Component` | `@Bean` |
|---|---|---|
| Gdzie się stosuje | Na **klasie** | Na **metodzie** (w klasie `@Configuration`) |
| Wykrywanie | Automatyczne przez **component scanning** | Jawna deklaracja w konfiguracji |
| Kontrola nad tworzeniem | Ograniczona (Spring sam wywołuje konstruktor) | Pełna — programista pisze logikę fabrykowania |
| Kiedy używać | Własne klasy, nad którymi masz kontrolę | Klasy z zewnętrznych bibliotek, złożona logika tworzenia |

```java
// @Component — automatyczne wykrywanie
@Component
public class EmailValidator { }

// @Bean — jawna konfiguracja (np. klasa z biblioteki)
@Configuration
public class AppConfig {
    @Bean
    public ObjectMapper objectMapper() {
        return new ObjectMapper()
            .registerModule(new JavaTimeModule())
            .disable(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS);
    }
}
```

---

### 5. Jakie są stereotypy komponentów w Spring (`@Component`, `@Service`, `@Repository`, `@Controller`) i czym się różnią?

Wszystkie stereotypy to specjalizacje `@Component` — Spring traktuje je identycznie pod kątem wykrywania i rejestracji beanów. Różnice leżą w **semantyce** i **dodatkowym zachowaniu**:

| Adnotacja | Warstwa | Dodatkowe zachowanie |
|---|---|---|
| `@Component` | Ogólna | Brak — bazowy stereotyp |
| `@Service` | Logika biznesowa | Brak (czysto semantyczna) |
| `@Repository` | Dostęp do danych (DAO) | **Translacja wyjątków** — wyjątki specyficzne dla technologii (np. `SQLException`) są automatycznie opakowywane w `DataAccessException` |
| `@Controller` | Warstwa web (MVC) | Obsługa żądań HTTP, integracja z `DispatcherServlet` |

Stosowanie właściwego stereotypu poprawia **czytelność kodu** i umożliwia Spring precyzyjne zastosowanie aspektów (np. translacja wyjątków tylko dla `@Repository`).

---

### 6. Jak działa mechanizm `@Qualifier` i kiedy jest potrzebny?

`@Qualifier` pozwala wskazać **konkretny bean** do wstrzyknięcia, gdy w kontekście istnieje więcej niż jedna implementacja danego interfejsu.

```java
public interface NotificationSender {
    void send(String message);
}

@Component("emailSender")
public class EmailNotificationSender implements NotificationSender { ... }

@Component("smsSender")
public class SmsNotificationSender implements NotificationSender { ... }

@Service
public class AlertService {
    private final NotificationSender sender;

    public AlertService(@Qualifier("smsSender") NotificationSender sender) {
        this.sender = sender;
    }
}
```

Bez `@Qualifier` (i bez `@Primary`) Spring rzuci `NoUniqueBeanDefinitionException`, bo nie wie, który bean wybrać.

Alternatywnie można tworzyć **własne adnotacje kwalifikujące**:
```java
@Target({ElementType.FIELD, ElementType.PARAMETER})
@Retention(RetentionPolicy.RUNTIME)
@Qualifier
public @interface Sms { }
```

---

### 7. Czym jest `@Primary` i jak współpracuje z `@Qualifier`?

`@Primary` oznacza bean jako **domyślny** — zostanie wybrany automatycznie, gdy istnieje kilka kandydatów, a miejsce wstrzyknięcia **nie** ma `@Qualifier`.

```java
@Primary
@Component
public class EmailNotificationSender implements NotificationSender { ... }

@Component
public class SmsNotificationSender implements NotificationSender { ... }
```

Reguły rozwiązywania:
1. Jeśli jest `@Qualifier` → wygrywa **@Qualifier** (zawsze, nawet nad `@Primary`)
2. Jeśli nie ma `@Qualifier`, ale jest `@Primary` → wygrywa **@Primary**
3. Jeśli nie ma żadnego → `NoUniqueBeanDefinitionException`

`@Primary` jest wygodne, gdy jeden bean to „domyślna" implementacja, a drugi — specjalistyczna.

---

### 8. Jakie są zakresy (scopes) beanów w Spring? Opisz `singleton`, `prototype`, `request`, `session`.

| Scope | Opis | Cykl życia |
|---|---|---|
| **singleton** (domyślny) | Jedna instancja na cały kontekst Spring | Tworzony przy starcie, niszczony przy zamknięciu kontekstu |
| **prototype** | Nowa instancja przy **każdym** wywołaniu `getBean()` lub wstrzyknięciu | Spring **nie zarządza** niszczeniem — `@PreDestroy` nie zostanie wywołane |
| **request** | Jedna instancja per żądanie HTTP | Tworzony i niszczony z żądaniem (wymaga kontekstu webowego) |
| **session** | Jedna instancja per sesja HTTP | Żyje tak długo jak sesja użytkownika |

```java
@Component
@Scope("prototype")
public class ShoppingCart { ... }
```

> **Pułapka:** Wstrzyknięcie beana `prototype` do beana `singleton` spowoduje, że singleton **zawsze** będzie trzymał tę samą instancję prototype'a. Rozwiązania: `ObjectProvider<T>`, `@Lookup`, lub `Provider<T>` z JSR-330.

```java
@Service
public class OrderService {
    private final ObjectProvider<ShoppingCart> cartProvider;

    public OrderService(ObjectProvider<ShoppingCart> cartProvider) {
        this.cartProvider = cartProvider;
    }

    public void placeOrder() {
        ShoppingCart cart = cartProvider.getObject(); // nowa instancja za każdym razem
    }
}
```

---

### 9. Jaka jest domyślna strategia tworzenia beanów (eager vs lazy) i jak można ją zmienić?

Domyślnie **singleton** beany są tworzone **eagerly** — wszystkie przy starcie `ApplicationContext`. Beany **prototype** są zawsze lazy (tworzone na żądanie).

Sposoby zmiany:

```java
// 1. Na pojedynczym beanie
@Component
@Lazy
public class HeavyService { ... }

// 2. Na całej klasie konfiguracyjnej
@Configuration
@Lazy
public class AppConfig {
    @Bean
    public ExpensiveClient client() { ... }
}

// 3. Globalnie w application.properties
spring.main.lazy-initialization=true
```

**Eager** (domyślne) — zalety:
- Błędy konfiguracji wykrywane przy starcie
- Brak opóźnienia przy pierwszym żądaniu

**Lazy** — zalety:
- Szybszy start aplikacji
- Beany, które nigdy nie zostaną użyte, nie zajmują pamięci

> W produkcji lazy initialization może maskować błędy — bean, który nigdy się nie tworzy, nigdy nie pokaże problemu.

---

### 10. Czym jest `@PostConstruct` i `@PreDestroy`? W jakiej kolejności wywoływane są callbacki cyklu życia beana?

`@PostConstruct` — metoda wywoływana **po** wstrzyknięciu wszystkich zależności, **przed** udostępnieniem beana.
`@PreDestroy` — metoda wywoływana **przed** zniszczeniem beana (przy zamykaniu kontekstu).

```java
@Component
public class CacheWarmer {

    @PostConstruct
    public void init() {
        // załadowanie cache'a, nawiązanie połączeń itp.
    }

    @PreDestroy
    public void cleanup() {
        // zamknięcie połączeń, zwolnienie zasobów
    }
}
```

**Pełna kolejność callbacków cyklu życia:**

1. Instancjonowanie (konstruktor)
2. Wstrzyknięcie zależności (setter / field injection)
3. `BeanPostProcessor.postProcessBeforeInitialization()`
4. **`@PostConstruct`**
5. `InitializingBean.afterPropertiesSet()`
6. `@Bean(initMethod = "...")`
7. `BeanPostProcessor.postProcessAfterInitialization()`
8. Bean gotowy do użycia
9. ...
10. **`@PreDestroy`**
11. `DisposableBean.destroy()`
12. `@Bean(destroyMethod = "...")`

> **Uwaga:** `@PreDestroy` **nie** zostanie wywołane dla beanów `prototype` — Spring nie śledzi ich cyklu życia po utworzeniu.

---

### 11. Jak działa `@Conditional` i do czego służą warunki rejestracji beanów?

`@Conditional` pozwala zarejestrować bean **tylko wtedy**, gdy spełniony jest określony warunek w momencie startu kontekstu.

```java
public class RedisAvailableCondition implements Condition {
    @Override
    public boolean matches(ConditionContext context, AnnotatedTypeMetadata metadata) {
        String redisHost = context.getEnvironment().getProperty("spring.redis.host");
        return redisHost != null && !redisHost.isEmpty();
    }
}

@Configuration
public class CacheConfig {
    @Bean
    @Conditional(RedisAvailableCondition.class)
    public CacheManager redisCacheManager() { ... }
}
```

Spring Boot dostarcza wiele gotowych wariantów:

| Adnotacja | Warunek |
|---|---|
| `@ConditionalOnClass` | Klasa istnieje w classpath |
| `@ConditionalOnMissingBean` | Bean danego typu jeszcze nie istnieje |
| `@ConditionalOnProperty` | Właściwość ma określoną wartość |
| `@ConditionalOnBean` | Inny bean istnieje w kontekście |
| `@ConditionalOnWebApplication` | Aplikacja jest webowa |

To fundament mechanizmu **autokonfiguracji** Spring Boot — startery rejestrują beany warunkowo.

---

### 12. Czym jest `BeanPostProcessor` i jaki ma wpływ na cykl życia beana?

`BeanPostProcessor` to interfejs, który pozwala **modyfikować lub opakowywać** instancje beanów **przed** i **po** ich inicjalizacji. Działa na **każdym** beanie w kontekście.

```java
@Component
public class LoggingBeanPostProcessor implements BeanPostProcessor {

    @Override
    public Object postProcessBeforeInitialization(Object bean, String beanName) {
        // wywoływane PRZED @PostConstruct
        return bean;
    }

    @Override
    public Object postProcessAfterInitialization(Object bean, String beanName) {
        // wywoływane PO @PostConstruct
        // tu można np. owinąć bean w proxy
        if (bean instanceof MyService) {
            return Proxy.newProxyInstance(...);
        }
        return bean;
    }
}
```

Spring wewnętrznie korzysta z `BeanPostProcessor` m.in. do:
- **`AutowiredAnnotationBeanPostProcessor`** — obsługa `@Autowired`
- **`CommonAnnotationBeanPostProcessor`** — obsługa `@PostConstruct`, `@PreDestroy`
- **AOP proxy** — tworzenie proxy dla `@Transactional`, `@Cacheable` itd.

> **Ważne:** `BeanPostProcessor` przetwarza **gotowe instancje** beanów. Nie modyfikuje definicji beanów (metadata) — do tego służy `BeanFactoryPostProcessor`.

---

### 13. Czym jest `BeanFactoryPostProcessor` i czym różni się od `BeanPostProcessor`?

`BeanFactoryPostProcessor` działa na **definicjach beanów** (metadata / `BeanDefinition`) — **zanim** zostaną utworzone jakiekolwiek instancje.

```java
@Component
public class CustomBeanFactoryPostProcessor implements BeanFactoryPostProcessor {

    @Override
    public void postProcessBeanFactory(ConfigurableListableBeanFactory factory) {
        BeanDefinition bd = factory.getBeanDefinition("myService");
        bd.setScope("prototype"); // zmiana scope'u zanim bean zostanie utworzony
    }
}
```

| Cecha | `BeanFactoryPostProcessor` | `BeanPostProcessor` |
|---|---|---|
| Kiedy działa | **Przed** tworzeniem beanów | **Podczas** tworzenia każdego beana |
| Na czym operuje | `BeanDefinition` (metadata) | Instancja beana (obiekt) |
| Przykład w Springu | `PropertySourcesPlaceholderConfigurer` (rozwiązywanie `${...}`) | `AutowiredAnnotationBeanPostProcessor` |
| Typowe zastosowanie | Modyfikacja konfiguracji, dodawanie definicji beanów | Opakowywanie beanów w proxy, walidacja |

Kolejność: `BeanFactoryPostProcessor` → tworzenie beanów → `BeanPostProcessor`

---

### 14. Jak Spring rozwiązuje zależności cykliczne (circular dependencies)?

Zależność cykliczna: A zależy od B, B zależy od A.

**Wstrzykiwanie przez konstruktor** → Spring **nie może** rozwiązać cyklu → `BeanCurrentlyInCreationException` przy starcie. To zachowanie jest **celowe** — cykle konstruktorowe są błędem projektowym.

**Wstrzykiwanie przez setter/pole** → Spring rozwiązuje to za pomocą **cache trzech poziomów** (three-level cache):
1. **singletonObjects** — w pełni zainicjalizowane beany
2. **earlySingletonObjects** — częściowo zainicjalizowane (instancja istnieje, ale zależności nie są jeszcze wstrzyknięte)
3. **singletonFactories** — fabryki zwracające wczesne referencje

Mechanizm:
1. Spring tworzy instancję A (konstruktorem)
2. Umieszcza „wczesną referencję" A w cache
3. Próbuje wstrzyknąć zależności A → potrzebuje B
4. Tworzy instancję B
5. B potrzebuje A → pobiera „wczesną referencję" A z cache
6. B jest w pełni zainicjalizowany
7. A dostaje gotowe B → A jest w pełni zainicjalizowany

> **Od Spring Boot 2.6+** cykliczne zależności są **domyślnie zabronione** (nawet przez setter). Aby je włączyć: `spring.main.allow-circular-references=true` — ale lepiej **zrefaktoryzować kod** (wydzielić wspólną logikę do trzeciej klasy lub użyć zdarzeń).

---

### 15. Czym jest profil (`@Profile`) i jak go aktywować?

Profil pozwala warunkowo rejestrować beany w zależności od **środowiska uruchomieniowego** (dev, test, prod).

```java
@Configuration
@Profile("dev")
public class DevDataSourceConfig {
    @Bean
    public DataSource dataSource() {
        return new EmbeddedDatabaseBuilder()
            .setType(EmbeddedDatabaseType.H2)
            .build();
    }
}

@Configuration
@Profile("prod")
public class ProdDataSourceConfig {
    @Bean
    public DataSource dataSource() {
        return DataSourceBuilder.create()
            .url("jdbc:postgresql://prod-db:5432/app")
            .build();
    }
}
```

Sposoby aktywacji:

```properties
# application.properties
spring.profiles.active=dev,metrics
```

```bash
# JVM argument
java -jar app.jar -Dspring.profiles.active=prod

# Zmienna środowiskowa
SPRING_PROFILES_ACTIVE=prod java -jar app.jar
```

```java
// W testach
@ActiveProfiles("test")
@SpringBootTest
class MyTest { ... }
```

Wyrażenia negacji: `@Profile("!prod")` — rejestruj bean we **wszystkich** profilach **oprócz** `prod`.

---

### 16. Jak działa mechanizm `@Value` i `@ConfigurationProperties`?

**`@Value`** — wstrzykiwanie **pojedynczych** wartości:

```java
@Component
public class MailService {
    @Value("${mail.smtp.host}")
    private String host;

    @Value("${mail.smtp.port:587}")  // wartość domyślna po dwukropku
    private int port;

    @Value("#{2 * T(Math).PI}")  // SpEL — Spring Expression Language
    private double tau;
}
```

**`@ConfigurationProperties`** — mapowanie **grupy** właściwości na obiekt POJO (type-safe):

```java
@ConfigurationProperties(prefix = "mail.smtp")
public class MailProperties {
    private String host;
    private int port = 587;
    private boolean auth;
    // gettery i settery
}

@Configuration
@EnableConfigurationProperties(MailProperties.class)
public class MailConfig { ... }
```

```yaml
# application.yml
mail:
  smtp:
    host: smtp.example.com
    port: 465
    auth: true
```

| Cecha | `@Value` | `@ConfigurationProperties` |
|---|---|---|
| Granularność | Pojedyncza wartość | Cała grupa właściwości |
| Walidacja | Brak (manualna) | `@Validated` + Bean Validation (`@NotNull`, `@Min`) |
| Type-safety | Ograniczone | Pełne — kompilator sprawdza typy |
| Relaksowne bindowanie | ❌ | ✅ (`smtp-host` = `smtpHost` = `SMTP_HOST`) |
| Zalecane użycie | Proste, jednorazowe wartości | Konfiguracja modułów / bibliotek |

---

### 17. Jak działa component scanning i jakie są jego ograniczenia?

Component scanning automatycznie wykrywa klasy z adnotacjami stereotypowymi (`@Component`, `@Service`, `@Repository`, `@Controller`) i rejestruje je jako beany.

```java
@Configuration
@ComponentScan(basePackages = "com.example.app")
public class AppConfig { }

// Spring Boot — @SpringBootApplication zawiera @ComponentScan
// skanuje pakiet klasy głównej + podpakiety
```

**Filtry:**
```java
@ComponentScan(
    basePackages = "com.example",
    includeFilters = @Filter(type = FilterType.ANNOTATION, classes = MyCustomAnnotation.class),
    excludeFilters = @Filter(type = FilterType.REGEX, pattern = ".*Test.*")
)
```

**Ograniczenia:**
1. **Skanuje tylko podpakiety** pakietu bazowego — klasy w pakiecie nadrzędnym lub siostrzanym nie zostaną znalezione.
2. **Klasy z zewnętrznych bibliotek** nie zostaną wykryte (nie masz kontroli nad ich adnotacjami) → użyj `@Bean`.
3. **Spowalnia start** w dużych projektach z wieloma pakietami — warto zawężać `basePackages`.
4. **Niejawność** — trudno prześledzić, skąd pochodzi bean (brak jawnej deklaracji).
5. **Nie działa na klasach wewnętrznych** (non-static inner classes).

---

### 18. Czym jest `@Configuration` i jak Spring tworzy proxy dla klas konfiguracyjnych?

`@Configuration` oznacza klasę jako źródło definicji beanów. Spring tworzy dla niej **proxy CGLIB** (podklasę), aby zapewnić semantykę **singleton** przy wywołaniach metod `@Bean`.

```java
@Configuration
public class AppConfig {

    @Bean
    public ServiceA serviceA() {
        return new ServiceA(commonDependency()); // ← nie tworzy nowej instancji!
    }

    @Bean
    public ServiceB serviceB() {
        return new ServiceB(commonDependency()); // ← ta sama instancja
    }

    @Bean
    public CommonDependency commonDependency() {
        return new CommonDependency();
    }
}
```

**Bez proxy (CGLIB)** — każde wywołanie `commonDependency()` stworzyłoby **nowy** obiekt. Dzięki proxy Spring przechwytuje wywołanie i zwraca **istniejący singleton** z kontekstu.

**`@Configuration(proxyBeanMethods = false)`** — tryb „lite" (bez proxy CGLIB):
- Metody `@Bean` **nie** są przechwytywane → każde wywołanie tworzy nowy obiekt
- Szybszy start, mniejsze zużycie pamięci
- Bezpieczne, gdy metody `@Bean` nie wywołują się nawzajem

**`@Component` z metodami `@Bean`** (tzw. lite mode):
- Zachowuje się jak `proxyBeanMethods = false`
- Metody `@Bean` działają jak zwykłe metody fabrykujące — **bez** gwarancji singletona przy wzajemnych wywołaniach

---

## 2. Spring MVC

### 1. Opisz przepływ żądania HTTP w Spring MVC (od `DispatcherServlet` do odpowiedzi).

Standardowy przepływ w aplikacji z systemem widoków (np. Thymeleaf):
1. Klient wysyła żądanie HTTP, które trafia do **`DispatcherServlet`** (Front Controller).
2. `DispatcherServlet` odpytuje **`HandlerMapping`**, aby znaleźć kontroler odpowiedni dla danego URL.
3. `DispatcherServlet` przekazuje żądanie do **`HandlerAdapter`**, który wywołuje właściwą metodę na kontrolerze.
4. Kontroler wykonuje logikę biznesową (często wołając serwisy) i zwraca obiekt **`ModelAndView`** (logiczną nazwę widoku oraz model danych).
5. `DispatcherServlet` przekazuje nazwę widoku do **`ViewResolver`**, który tłumaczy ją na konkretny szablon (np. plik HTML).
6. Widok jest renderowany z wykorzystaniem przekazanego modelu, a wygenerowany HTML jest zwracany jako odpowiedź HTTP do klienta.

> **W przypadku REST API (`@RestController`)**: Krok 4 i 5 ulega zmianie. Kontroler nie zwraca nazwy widoku, lecz obiekt domenowy/DTO. Zamiast używać `ViewResolver`, `HandlerAdapter` wykorzystuje **`HttpMessageConverter`** (np. Jackson), aby od razu zserializować obiekt do formatu JSON/XML i zapisać go bezpośrednio w ciele odpowiedzi HTTP.

---

### 2. Czym jest `DispatcherServlet` i jaką pełni rolę?

`DispatcherServlet` to implementacja wzorca architektonicznego **Front Controller**. 
Jest to główny punkt wejścia (serwlet) dla każdego żądania HTTP w aplikacji Spring MVC.

Jego główne role to:
- Przechwytywanie wszystkich żądań przychodzących do aplikacji.
- Centralne zarządzanie przepływem sterowania (dispatching) – delegowanie zadań do odpowiednich komponentów (np. `HandlerMapping`, `Controller`, `ViewResolver`).
- Inicjalizacja kontekstu webowego (`WebApplicationContext`), który jest podrzędny wobec głównego kontekstu aplikacji (`ApplicationContext`).

Dzięki niemu unika się powielania logiki związanej z np. parsowaniem parametrów HTTP, routingiem i obsługą odpowiedzi w każdym kontrolerze z osobna.

---

### 3. Jakie są różnice między `@Controller` a `@RestController`?

| Cecha | `@Controller` | `@RestController` |
|---|---|---|
| Główne zastosowanie | Tradycyjne aplikacje webowe (z widokami HTML) | RESTful Web Services (API) |
| Typowa wartość zwracana | `String` (logiczna nazwa widoku) lub `ModelAndView` | Obiekt domenowy / DTO / kolekcja |
| Format odpowiedzi | HTML wyrenderowany przez system szablonów | Zazwyczaj JSON / XML (serializowane) |
| `@ResponseBody` | Wymaga ręcznego dodania na metodzie, jeśli chcemy zwrócić JSON | Zastosowane automatycznie na każdej metodzie |

`@RestController` to po prostu adnotacja złożona (meta-adnotacja), która zawiera w sobie `@Controller` i `@ResponseBody`.

```java
// Zapisy równoważne:
@Controller
@ResponseBody
public class MyApi { ... }

@RestController
public class MyApi { ... }
```

---

### 4. Jak działają adnotacje `@RequestMapping`, `@GetMapping`, `@PostMapping` itd.?

Adnotacje te służą do mapowania żądań HTTP na konkretne metody (tzw. handlery) w kontrolerze.

**`@RequestMapping`** to najbardziej ogólna adnotacja. Można ją stosować na poziomie klasy i metody. Pozwala precyzyjnie definiować ścieżkę, metodę HTTP, nagłówki czy parametry `consumes` i `produces`.

```java
@RequestMapping(value = "/users", method = RequestMethod.GET)
public List<User> getUsers() { ... }
```

**`@GetMapping`, `@PostMapping`, `@PutMapping`, `@DeleteMapping`, `@PatchMapping`** to skrócone (composed) adnotacje wprowadzone w Spring 4.3. Poprawiają one czytelność i intencję kodu. Odpowiadają one `@RequestMapping` ze z góry określoną metodą HTTP.

```java
@GetMapping("/users")
public List<User> getUsers() { ... }
```

---

### 5. Czym jest `@PathVariable` i czym różni się od `@RequestParam`?

Obie adnotacje służą do wyciągania danych z żądania HTTP, ale z różnych miejsc.

**`@PathVariable`**:
- Pobiera wartość bezpośrednio ze **ścieżki URL** (np. `/users/123`).
- Idealne w architekturach REST do identyfikacji konkretnego zasobu.
```java
@GetMapping("/users/{id}")
public User getUser(@PathVariable("id") Long id) { ... }
```

**`@RequestParam`**:
- Pobiera wartość z **parametrów zapytania** (query parameters po znaku zapytania np. `/users?role=admin`) lub z pól formularza URL-encoded (`application/x-www-form-urlencoded`).
- Stosowane najczęściej do filtrowania wyników, paginacji czy opcjonalnych parametrów wyszukiwania.
```java
@GetMapping("/users")
public List<User> getUsersByRole(@RequestParam(value = "role", defaultValue = "user") String role) { ... }
```

---

### 6. Jak działa mechanizm `@ModelAttribute`?

`@ModelAttribute` można użyć na dwa sposoby:

1. **Jako parametr metody (wiązanie danych żądania):**
Wiąże dane z żądania (najczęściej wysłany formularz POST/PUT) z obiektem POJO. Spring próbuje dopasować pola z formularza do setterów w obiekcie modelu.
```java
@PostMapping("/register")
public String registerUser(@ModelAttribute UserForm form) { ... }
```

2. **Na metodzie (na poziomie kontrolera):**
Metoda oznaczona jako `@ModelAttribute` wywoła się **przed** wywołaniem jakiejkolwiek innej metody oznaczanej `@RequestMapping` w tym samym kontrolerze. Używa się tego do wstawiania do modelu danych referencyjnych, wspólnych dla wielu widoków (np. lista dostępnych krajów w dropdownie).
```java
@ModelAttribute("countries")
public List<String> populateCountries() {
    return List.of("Polska", "Niemcy", "Francja");
}
```

---

### 7. Jak Spring MVC obsługuje walidację danych wejściowych (`@Valid`, `@Validated`, `BindingResult`)?

Spring bezproblemowo integruje się z mechanizmami **Bean Validation (JSR 380)**, m.in. implementacją Hibernate Validator.

Mechanizm działania:
1. Argument metody kontrolera adnotujemy przez **`@Valid`** (standard Java) lub **`@Validated`** (rozszerzenie Spring, pozwalające na użycie Validation Groups).
2. Odbierany obiekt (DTO) posiada wewnątrz walidacje, np. `@NotNull`, `@Min`, `@Email`.
3. Podczas bindowania żądania, Spring uruchamia proces walidacji.

**Obsługa błędów:**
- Jeśli zaraz po argumentach walidowanego obiektu dodamy parametr **`BindingResult`**, Spring nie rzuci wyjątku przy błędzie, ale przekaże wynik do tego obiektu. Możemy wtedy np. zwrócić widok z błędami przy formularzu.
- Jeśli **nie dodamy** `BindingResult`, w razie błędów wyrzucany jest wyjątek `MethodArgumentNotValidException` (przy REST) lub `BindException`, co kończy się odpowiedzią 400 Bad Request.

```java
@PostMapping("/users")
public ResponseEntity<?> createUser(@Valid @RequestBody UserDto dto, BindingResult result) {
    if (result.hasErrors()) {
        return ResponseEntity.badRequest().body("Błędy walidacji!");
    }
    return ResponseEntity.ok("Zapisano");
}
```

---

### 8. Czym jest `@ControllerAdvice` i jak wspiera centralne zarządzanie wyjątkami?

`@ControllerAdvice` to wdrożenie wzorca Intercepting Filter / AOP dla warstwy webowej w Springu. Jest to globalny interceptor dla kontrolerów.

Jego główne zastosowanie to **globalna obsługa wyjątków**. Zamiast dodawać logikę łapania wyjątków do każdego kontrolera z osobna, robimy to w jednym centralnym miejscu, co drastycznie redukuje duplikację kodu i utrzymuje DRY.

W klasie z adnotacją `@ControllerAdvice` możemy m.in.:
- Używać `@ExceptionHandler` do łapania wyjątków lecących ze wszystkich kontrolerów.
- Używać `@InitBinder` by zdefiniować globalne konwertery i formatery (np. jak parsować daty).
- Używać `@ModelAttribute` aby dostarczać wspólne obiekty do widoków wszystkich aplikacji.

Dla aplikacji typu REST zamiast `@ControllerAdvice` często używa się meta-adnotacji **`@RestControllerAdvice`**, która dodatkowo dokłada do metod `@ResponseBody`.

---

### 9. Jak działa `@ExceptionHandler`?

`@ExceptionHandler` pozwala na przechwycenie konkretnego typu wyjątku rzuconego w trakcie wykonywania metody kontrolera i odesłanie przygotowanej odpowiedzi.

Może być stosowany:
1. **Lokalnie** (w konkretnej klasie z `@Controller`) – obsłuży wyjątek rzucony tylko przez metody tej konkretnej klasy.
2. **Globalnie** (w klasie `@ControllerAdvice`) – przechwytuje wyjątki z całej aplikacji.

```java
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(UserNotFoundException.class)
    @ResponseStatus(HttpStatus.NOT_FOUND) // Modyfikuje kod HTTP
    public ErrorResponse handleUserNotFound(UserNotFoundException ex) {
        return new ErrorResponse(ex.getMessage(), 404);
    }
}
```

---

### 10. Czym jest `HandlerInterceptor` i czym różni się od filtra serwletów?

Obydwa mechanizmy służą do wstrzykiwania akcji przed lub po przetworzeniu żądania HTTP, ale na różnych etapach:

| Cecha | Filtr (Servlet Filter) | `HandlerInterceptor` (Spring MVC) |
|---|---|---|
| Pochodzenie | Standard Java EE (Servlet API) | Ekosystem Spring MVC |
| Etap działania | Uruchamiany zanim żądanie w ogóle trafi do `DispatcherServlet` | Uruchamiany **w obrębie** `DispatcherServlet` |
| Dostęp do kontekstu | Operuje na nagich `ServletRequest` i `ServletResponse` | Ma dostęp do kontekstu Springa, do docelowego *handlera* (metody kontrolera) i obiektu `ModelAndView` |
| Zastosowanie | Filtrowanie globalne: CORS, uwierzytelnianie (np. Spring Security filter chain), audyt wejścia/wyjścia na poziomie serwera | Logika zależna od kontrolera np. zmiana widoku przed wyrenderowaniem, sprawdzanie adnotacji wywoływanej metody kontrolera, logowanie czasu trwania samej logiki biznesowej |

`HandlerInterceptor` dostarcza metody: `preHandle()` (przed kontrolerem), `postHandle()` (po kontrolerze, ale przed wyrenderowaniem widoku) i `afterCompletion()` (po zakończeniu całego procesu żądania).

---

### 11. Jak skonfigurować obsługę plików statycznych w Spring MVC?

W **Spring Boot** obsługa plików statycznych jest autokonfigurowana. Wystarczy umieścić pliki (np. `style.css`, `logo.png`) w classpath w jednym z dedykowanych folderów:
- `/static`
- `/public`
- `/resources`
- `/META-INF/resources`
Będą one zaserwowane pod głównym kontekstem aplikacji (np. `http://localhost:8080/style.css`). Można zmienić te ścieżki propertysem `spring.web.resources.static-locations`.

W **„czystym” Spring MVC** należy jawnie zarejestrować handlery (implementując interfejs `WebMvcConfigurer`):

```java
@Configuration
@EnableWebMvc
public class WebConfig implements WebMvcConfigurer {
    @Override
    public void addResourceHandlers(ResourceHandlerRegistry registry) {
        registry.addResourceHandler("/assets/**")
                .addResourceLocations("classpath:/static/");
    }
}
```

---

### 12. Czym jest `ViewResolver` i jakie są jego popularne implementacje?

`ViewResolver` to interfejs pozwalający oddzielić logikę kontrolera od silnika renderowania widoków. Odpowiada za przetłumaczenie zwracanej z kontrolera "logicznej nazwy widoku" (np. `"home"`) na rzeczywisty obiekt widoku, który jest w stanie wyrenderować dokument (np. wskazać plik pod `/WEB-INF/views/home.jsp`).

Popularne implementacje to:
- **`ThymeleafViewResolver`** – najpopularniejszy w Spring Boot, wspierający nowoczesny system szablonów HTML Thymeleaf.
- **`InternalResourceViewResolver`** – tradycyjny i najczęstszy wybór do renderowania starych widoków typu JSP (JavaServer Pages).
- **`FreeMarkerViewResolver`** / **`GroovyMarkupViewResolver`** – dla innych silników (Freemarker, Groovy).

W nowoczesnych architekturach REST (używających `@RestController`) `ViewResolver` nie bierze udziału – używany jest `HttpMessageConverter`.

---

### 13. Jak działa negocjacja treści (content negotiation) w Spring MVC?

Content negotiation (negocjacja treści) to mechanizm polegający na określaniu preferowanego formatu danych podczas komunikacji klienta z serwerem. Przydatny w aplikacjach RESTowych by ten sam endpoint potrafił zwracać, zależnie od potrzeb, zarówno JSON, jak i XML.

Mechanizm rozpatruje następujące wytyczne w kolejności priorytetów:
1. **Zmienna w URI** – parametr rozszerzenia (np. `/users.json` vs `/users.xml`). *Uwaga: Uznawane dziś za antywzorzec. Domyślnie wyłączone od Spring Framework 5.3.*
2. **Parametr zapytania (query param)** – np. `/users?format=xml`.
3. **Nagłówek HTTP `Accept`** – (najbardziej zgodne ze standardami REST). W żądaniu przesyłany jest nagłówek np. `Accept: application/json`.

Na podstawie powyższych, Spring wybiera właściwy `HttpMessageConverter` (np. Jackson zmapuje na JSON, lub JAXB na XML) by przeprowadzić serializację. Można dodatkowo określić limity w adnotacji np. `@RequestMapping(produces = "application/json")`.

---

### 14. Czym jest `@ResponseStatus` i kiedy się go stosuje?

`@ResponseStatus` wymusza ustawienie konkretnego kodu statusu HTTP oraz opcjonalnego komunikatu (reason), jako odpowiedź na żądanie.

Stosuje się go przeważnie w dwóch miejscach:
1. **Na metodzie kontrolera**: 
   Kiedy chcemy nadpisać standardowe zachowanie (w którym po bezbłędnym przetworzeniu oddawany jest 200 OK). Przydatne dla wymuszania np. `201 Created` po metodach POST (tworzących), czy `204 No Content` po usunięciu (DELETE).
   ```java
   @PostMapping
   @ResponseStatus(HttpStatus.CREATED)
   public void createUser(...) { ... }
   ```
2. **Na własnej klasie wyjątków**: 
   Gdy rzucenie danego wyjątku ma jednoznacznie oznaczać konkretny błąd w odpowiedzi, co pozwala uniknąć obsługi przez dedykowany `@ExceptionHandler`.
   ```java
   @ResponseStatus(value = HttpStatus.NOT_FOUND, reason = "Nie znaleziono pracownika")
   public class EmployeeNotFoundException extends RuntimeException { ... }
   ```

---

### 15. Jak obsłużyć uploading plików w Spring MVC?

Wysyłanie plików bazuje na formacie `multipart/form-data`. W Spring MVC głównym interfejsem reprezentującym nadchodzący plik jest **`MultipartFile`**.

Spring Boot ma automatycznie aktywowaną obsługę formatu multipart przez serwlet i ustawia dozwolone maksymalne rozmiary (domyślnie m.in. `spring.servlet.multipart.max-file-size=1MB`).

Obsługa po stronie kontrolera polega na odczytaniu parametru przy użyciu `@RequestParam`:

```java
@PostMapping("/upload")
public String handleFileUpload(@RequestParam("file") MultipartFile file) {
    if (!file.isEmpty()) {
        try {
            // Zapis do lokalnego pliku
            file.transferTo(new File("/tmp/" + file.getOriginalFilename()));
            return "Pomyślnie wgrano " + file.getOriginalFilename();
        } catch (IOException e) {
            return "Błąd wgrywania.";
        }
    }
    return "Wybierz plik.";
}
```
Obiekt `MultipartFile` pozwala wygodnie sprawdzać rozmiar pliku, oryginalną nazwę czy uzyskać zeń strumień `InputStream`.

---

## 3. Spring REST

### 1. Jak zbudować RESTful API w Spring i jakie adnotacje są kluczowe?

Aby zbudować RESTful API, używa się modułu Spring MVC (lub reaktywnego Spring WebFlux).
Kluczowe adnotacje to:
- **`@RestController`** – to meta-adnotacja łącząca `@Controller` oraz `@ResponseBody`. Informuje Springa, by wszystkie zwrócone wartości serializować i wstawić bezpośrednio w ciało odpowiedzi HTTP.
- **Adnotacje mapujące** – np. `@RequestMapping`, `@GetMapping`, `@PostMapping`, `@PutMapping`, `@DeleteMapping`, `@PatchMapping` mapują żądania HTTP na odpowiednie metody i URI.
- **`@PathVariable`** – służy do pobierania zmiennych prosto ze ścieżki URI (np. `/users/{id}`).
- **`@RequestParam`** – służy do pobierania parametrów z tzw. *query parameters* URL (np. `/users?page=1`).
- **`@RequestBody`** – umożliwia pobranie i zdeserializowanie ciała przychodzącego żądania HTTP (np. JSONa) i przypisanie go do obiektu POJO w Javie.
- **`@ResponseStatus`** lub klasa **`ResponseEntity`** – pozwalają na przejęcie ścisłej kontroli nad zwracanym kodem statusu i nagłówkami odpowiedzi HTTP.

---

### 2. Czym jest `@ResponseBody` i jak wpływa na serializację odpowiedzi?

`@ResponseBody` to adnotacja oznaczająca, że obiekt zwracany przez daną metodę ma zostać wpisany bezpośrednio do strumienia odpowiedzi (body) żądania HTTP, zamiast traktować go jako logiczną nazwę widoku do wyrenderowania.

**Wpływ na serializację:**
Jeśli do metody kontrolera dodamy tę adnotację, `DispatcherServlet` przekaże zwracany obiekt przez system zwany **`HttpMessageConverter`**. Konwertery sprawdzają nagłówek klienta (`Accept`) oraz dostępność bibliotek na ścieżce classpath (np. obecność biblioteki Jackson dodaje domyślne mapowanie na JSON). Następuje konwersja obiektu POJO (z wykorzystaniem getterów i odpowiednich ustawień) na format np. JSON, który ostatecznie jest widoczny dla frontendu dzwoniącego pod wskazany adres.

*W nowoczesnym kodzie nie musimy tej adnotacji umieszczać jawnie, jeśli użyjemy meta-adnotacji `@RestController` na poziomie klasy.*

---

### 3. Czym jest `@RequestBody` i jak Spring deserializuje dane wejściowe?

`@RequestBody` to adnotacja wymuszająca powiązanie i zdeserializowanie całego ciała przychodzącego żądania HTTP (tzw. request payload) do obietku domenowego/DTO w Javie jako argumentu metody.

**Proces deserializacji:**
Działa to jako proces odwrotny do serializacji w `@ResponseBody`. `DispatcherServlet` przy wywoływaniu handlera analizuje typ argumentu podanego w metodzie oraz nagłówek żądania `Content-Type` wysłany przez klienta (np. `application/json`). Następnie przepuszcza dane wejściowe w formie byte stream do łańcucha **`HttpMessageConverter`**, gdzie odpowiedni konwerter (często Jackson) odczytuje strukturę JSON i za pomocą mechanizmu refleksji w Javie mapuje właściwości JSONa na pola docelowego obiektu POJO.

---

### 4. Jak skonfigurować niestandardowy `HttpMessageConverter`?

Aby dodać niestandardowy konwerter (np. jeśli chcemy serializować odpowiedź w formacie YAML, CSV, lub nadpisać domyślną konfigurację Jacksona), implementujemy interfejs `WebMvcConfigurer` w klasie konfiguracyjnej:

```java
@Configuration
public class WebConfig implements WebMvcConfigurer {

    @Override
    public void configureMessageConverters(List<HttpMessageConverter<?>> converters) {
        // Konfiguracja własnego niestandardowego konwertera 
        converters.add(new MyCustomYamlConverter());

        // Lub niestandardowa modyfikacja defaultowego konwertera Jacksona
        MappingJackson2HttpMessageConverter converter = new MappingJackson2HttpMessageConverter();
        converter.setObjectMapper(new ObjectMapper().registerModule(new JavaTimeModule()));
        converters.add(converter);
    }
}
```

*Wskazówka:* W przypadku czystego Spring Boot, znacznie prościej jest po prostu zadeklarować wstrzykiwany bean samego `ObjectMapper` bądź modyfikować jego właściwości poprzez flagi w pliku `application.properties` (np. `spring.jackson.serialization.write-dates-as-timestamps=false`).

---

### 5. Jak poprawnie zwracać kody statusu HTTP (`ResponseEntity`, `@ResponseStatus`)?

1. **Stosując adnotację `@ResponseStatus`**
Używana głównie wtedy, gdy chcemy na stałe z góry przypisać dany status danej metodzie lub klasie wyjątku. Zaletą jest jej zwięzłość, jednak brakuje w niej dynamiki.
```java
@PostMapping
@ResponseStatus(HttpStatus.CREATED) // Zawsze ustawi kod 201
public void createUser(@RequestBody User user) { ... }
```

2. **Stosując obiekt `ResponseEntity`**
Podejście zalecane w sytuacjach w których odpowiedź HTTP, i jej statusy, mogą się zmieniać na skutek np. walidacji wywołanej logiki biznesowej, i wymagają nałożenia w headerach np. linków w HATEOAS. Pełna kontrola dynamiczna.
```java
@PostMapping("/users")
public ResponseEntity<User> createUser(@RequestBody User user) {
    User savedUser = service.save(user);
    // Skonstruowanie headera Location wg. wytycznych standardów REST
    URI location = ServletUriComponentsBuilder.fromCurrentRequest()
            .path("/{id}").buildAndExpand(savedUser.getId()).toUri();
    
    return ResponseEntity.created(location).body(savedUser); // Odesłanie statusu 201
}
```

---

### 6. Jak wersjonować REST API w Spring (ścieżka, nagłówek, parametr)?

Możemy skorzystać z kilku strategii do obsługi jednoczesnych różnych wersji API. Implementujemy je poprzez argumenty wewnątrz `@RequestMapping`.

1. **Wersjonowanie w ścieżce URI** (Najpopularniejsze podejście u gigantów np. Twitter)
    - W kontrolerze modyfikujemy path: `@GetMapping("/v1/users")` oraz oddzielna dla `@GetMapping("/v2/users")`.
2. **Wersjonowanie poprzez Query Parameter** (Podejście preferowane przez Amazon)
    - Klienci wołają: `/users?version=1`
    - W kontrolerze wymuszamy to tak: `@GetMapping(value = "/users", params = "version=1")`
3. **Wersjonowanie poprzez Custom Header**
    - Klienci przekazują customowy nagłówek np. `X-API-Version: 1`
    - Spring rozwiązuje to tak: `@GetMapping(value = "/users", headers = "X-API-Version=1")`
4. **Wersjonowanie przez Content Negotiation (Accept Header)** (Tzw. prawdziwy architektonicznie styl REST np. GitHub)
    - Klient przekazuje w żądaniu MediaType: `Accept: application/vnd.company.app-v1+json`
    - Ograniczamy to w kodzie poprzez: `@GetMapping(value = "/users", produces = "application/vnd.company.app-v1+json")`

---

### 7. Jak obsłużyć HATEOAS w Spring?

HATEOAS (*Hypermedia as the Engine of Application State*) zakłada, że zasoby API w odpowiedzi same instruują klienta swoimi linkami, jakie powiązane obiekty może odwiedzić, bądź jakie inne interakcje stanowe na owym zasobie można wykonać (co sprawia, że klienci potrzebują wiedzieć z góry zdecydowanie mniej).

Do aplikacji dodajemy dedykowany moduł **Spring HATEOAS**. Najważniejsze w nim struktury do stosowania to:
- `EntityModel<T>` (dla pojedynczego zasobu) 
- `CollectionModel<T>` (dla zbioru)
- `WebMvcLinkBuilder` służące do bezpiecznego typologicznie generowania linków (tzw. "link-to" methods).

```java
@GetMapping("/{id}")
public EntityModel<User> getUser(@PathVariable Long id) {
    User user = userService.findById(id);
    EntityModel<User> resource = EntityModel.of(user); // Opakowujemy model do Resource
    
    // Generowanie i doklejenie do wyniku linku "self"
    resource.add(linkTo(methodOn(UserController.class).getUser(id)).withSelfRel());
    // Inny link: "wszyscy użytkownicy"
    resource.add(linkTo(methodOn(UserController.class).getAllUsers()).withRel("users"));
    
    return resource; // Konwerter automatycznie uwzględni pole "links" do JSONa
}
```

---

### 8. Czym jest `RestTemplate` i jakie są jego ograniczenia?

`RestTemplate` to klasyczny klient usług HTTP (zewnętrznych) dołączany wbudowany do frameworka w ramach Spring Web (od Springa 3.0). Pozwala poprzez metody oparte na szablonach jak np. `getForObject()`, w bardzo wysokopoziomowy sposób bez znajomości bibliotek bazowych Apache itp., wykonywać wewnątrz logiki aplikacji połączenia do innych zewnętrznych i wewnętrznych REST API.

**Ograniczenia:**
`RestTemplate` działa jako klient synchroniczny (blokujący). To oznacza, że kiedy wykonamy z niego uderzenie na zewnątrz np. by pobrać powiązane dane klienta z innej bazy/mikroserwisu, dany wyizolowany wątek Tomcat który to obsługiwał po naszej stronie, stoi całkowicie poblokowany czekając bezczynnie na strumień odpowiedzi. Przy ogromnym ruchu zapycha to całą dostępną na puli sieć wątków aplikacji.
Z tego powodu Spring uważa go na ten moment za oprogramowanie będące we wczesnym **deprecated** odnośnie pisania nowych projektów (chociaż wciąż używany przez większość starzejących się baz kodu korporacyjnego).

---

### 9. Czym jest `WebClient` i czym różni się od `RestTemplate`?

`WebClient` został przedstawiony w Springu 5, w pakiecie Spring WebFlux jako docelowy i wydajniejszy zamiennik dla starzejącego się synchronicznego `RestTemplate`. 

Podstawowe różnice:
- `WebClient` działa w 100% nieblokująco - jest w pełni klientem **asynchronicznym i reaktywnym**.
- Koncept na którym stoi do obsługi połączeń to architektura "Project Reactor" oparta na event loopie (`Mono`, `Flux`). Dzięki temu w ogóle nie blokuje on wątków przy czekaniu na odbieranie danych HTTP.
- Budowa zapytań nie jest już skonstruowana jako typowe metody proste w szablonach klasowych, a jako bardzo nowoczesny łańcuch wywołań w architekturze *Fluent API (Builder Pattern)*.
- Warto pamiętać, że chociaż domyślnie jest nieblokujący i jest standardem, sam z siebie posiada metodę `.block()` - używana w architekturach konwencjonalnego Spring MVC w celu by celowo zblokować dany strumień danych udając synchroniczność pod płaszczem nowoczesnego kodu, gdy pracujemy np. z bazą danych na blokującym Hibernate JPA.

---

### 10. Jak zaimplementować paginację i sortowanie w endpointach REST?

Aby zaimplementować paginację ze stronicowaniem, wystarczy w głównej mierze podpiąć wbudowane wsparcie ze **Spring Data**. Kluczowym interfejsem staje się tu abstrakcja z repozytorium **`Pageable`**. 

Umożliwia to zlecającemu klientowi podać z góry w URL tzw. query parameters, przykładowo: `?page=0&size=10&sort=name,asc`. 

Spring z automatu w warstwie obsługi kontrolera samodzielnie przetłumaczy wartości stronicowania ze stringów, w obiekt `Pageable`, więc dodajemy go czysto jako parametr:
```java
@GetMapping("/users")
public Page<User> getUsers(Pageable pageable) {
    // pageable ze swoim numerem, wielkością z URL idzie z kontrolera prosto do Spring Data 
    return userRepository.findAll(pageable);
}
```
Zwracany obiekt repozytorium nie będzie typowym `List<T>`, a zostanie obłożony typem `Page<T>`, który Spring z automatu w sposób poprawny przerobi do wyplucia JSON-a do przeglądarki klienta uwzględniającego metadane (łącznie stron, numerów itp).

---

### 11. Jak obsłużyć globalną obsługę wyjątków dla REST API?

Aby unikać duplikowania w każdym kontrolerze wielokrotnych bloków na klauzule `try-catch`, błędy w obrębie zapytań API chwytane są asymetrycznie globalnie. 

Odbywa się to poprzez stworzenie odseparowanej klasy zawierającej centralną logikę z adnotacją meta: **`@RestControllerAdvice`**. Pozwala ona przechwycić exception z dowolnie zdefiniowanej operacji w serwerze, mapując w jeden format opakowania odpowiedzi po stronie widoku. 
```java
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(UserNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleMissingUser(UserNotFoundException ex) {
        ErrorResponse body = new ErrorResponse("User missing", ex.getMessage(), 404);
        return new ResponseEntity<>(body, HttpStatus.NOT_FOUND);
    }
}
```
Dla uproszczenia życia programistów klasa advice często ma nadane rozszerzenie np. o wbudowaną formę abstrakcji `ResponseEntityExceptionHandler`, co pozwala nadpisać domyślne generyczne wyjątki frameworka i połączyć je z naszym spersonalizowanym standardem powiadomień DTO do wysyłanych po JSON.

---

### 12. Jak zabezpieczyć REST API przed atakami CSRF i CORS?

**Zabezpieczenie CORS (Cross-Origin Resource Sharing):**
Zjawisko, gdzie w przeglądarce frontend uruchomiony na adresie *http://domainA.com* woła endpoint API udostępniany z adresu serwera *http://domainB.com*. Dla przeglądarek jest to zablokowane ze względów bezpieczeństwa. By odpowiednio pozwolić np. serwerowi React użyć naszego API:
- Używa się konfiguracji bezpośredniej z nałożeniem adnotacji: `@CrossOrigin(origins = "http://localhost:3000")` nad metodą w klasie rest.
- Bądź na gruncie ogólnym definiując własny bean nadpisując po interfejsie klasy `WebMvcConfigurer` funkcję `.addCorsMappings(CorsRegistry)`.

**Zabezpieczenie CSRF (Cross-Site Request Forgery):**
Jest formą ataku hakerskiego wykorzystującą podatność stanową polegająca na uwikłaniu domyślnych ciastk do odtworzenia spreparowanych wywołań w tle. Standardową polityką jest w REST w pełni **wyłączenie zabezpieczeń CSRF** w klasie implementującej logikę zabezpieczeń autoryzacji z modułu Security (`http.csrf().disable()`).
Podejście takie jest dozwolone i pożądane, z prostego tytułu – bezstanowe natywne protokoły architektury REST chronione uwierzytelnianiem i autoryzacją za pomocą nagłówków żądań w locie (np. Bearer Token z JWT), nie wykorzystują do utrzymania sesji systemów plików *Cookies*, na których luki tych ataków w pełni polegają.

---

## 4. Spring Data / JPA

### 1. Czym jest Spring Data JPA i jakie problemy rozwiązuje?

**Spring Data JPA** to moduł z rodziny Spring Data, który dostarcza warstwę abstrakcji nad specyfikacją JPA (Java Persistence API) oraz jej implementacjami (najczęściej Hibernate). 

**Główne problemy, które rozwiązuje:**
1. **Boilerplate code (powtarzalny kod)** – Eliminuje potrzebę pisania setek linii powtarzalnego kodu (tzw. DAO - Data Access Object) do podstawowych operacji CRUD (Create, Read, Update, Delete).
2. **Generowanie zapytań z nazw metod** – Pozwala na automatyczne generowanie zapytań SQL/JPQL na podstawie odpowiednio skonstruowanej nazwy metody w interfejsie (tzw. Query Derivation).
3. **Paginacja i sortowanie** – Wbudowane i proste w użyciu mechanizmy do stronicowania i sortowania wyników bez konieczności pisania skomplikowanego SQL.
4. **Integracja z ekosystemem Springa** – Automatyczna obsługa transakcji (`@Transactional`), integracja ze Spring MVC (automatyczne rozwiązywanie parametrów `Pageable`).

W praktyce, programista definiuje jedynie interfejs dziedziczący np. po `JpaRepository`, a Spring Data w czasie działania aplikacji (runtime) tworzy dla niego proxy i implementację.

---

### 2. Jak działają interfejsy repozytoriów (`CrudRepository`, `JpaRepository`, `PagingAndSortingRepository`)?

W Spring Data występuje hierarchia interfejsów repozytoriów:

1. **`Repository<T, ID>`** – Bazowy interfejs znacznikowy (marker interface). Sam w sobie nie dodaje żadnych metod, ale pozwala Springowi wykryć, że dany interfejs jest repozytorium.
2. **`CrudRepository<T, ID>`** – Rozszerza `Repository` i dostarcza podstawowe metody CRUD: `save()`, `findById()`, `findAll()`, `count()`, `delete()`, `existsById()`.
3. **`PagingAndSortingRepository<T, ID>`** – Rozszerza `CrudRepository` i dodaje metody ułatwiające sortowanie i paginację wyników: `findAll(Sort sort)` oraz `findAll(Pageable pageable)`.
4. **`JpaRepository<T, ID>`** – Najbardziej rozbudowany interfejs. Rozszerza `PagingAndSortingRepository` (oraz `QueryByExampleExecutor`). 
   - Zwraca `List<T>` zamiast `Iterable<T>`.
   - Dodaje operacje specyficzne dla JPA, takie jak: `flush()`, `saveAndFlush()`, `deleteInBatch()`.

**Kiedy którego używać?**
Najczęściej używa się `JpaRepository`, ponieważ zwraca listy i pozwala na ręczne zarządzanie sesją Hibernate (`flush()`). Jeśli zależy nam na ścisłym oddzieleniu technologii (np. by nie używać klas z JPA, gdy w przyszłości zmienimy bazę na NoSQL), można rozważyć `CrudRepository` lub własny interfejs.

---

### 3. Jak Spring generuje implementację metod na podstawie nazwy (query derivation)?

**Query derivation** to mechanizm pozwalający tworzyć zapytania do bazy danych wyłącznie poprzez nazewnictwo metod w interfejsie repozytorium.

Zasada działania opiera się na analizie prefiksu i słów kluczowych:
- **Prefiksy:** `find...By`, `read...By`, `query...By`, `count...By`, `delete...By`, `exists...By`.
- **Właściwości:** Nazwy pól z encji (np. `FirstName`).
- **Operatory logiczne i warunki:** `And`, `Or`, `Between`, `LessThan`, `GreaterThan`, `Like`, `IgnoreCase`, `OrderBy`.

**Przykłady:**
```java
// WHERE email = ?
Optional<User> findByEmail(String email);

// WHERE age > ? AND status = ?
List<User> findByAgeGreaterThanAndStatus(int age, String status);

// WHERE last_name LIKE ? ORDER BY first_name DESC
List<User> findByLastNameLikeOrderByFirstNameDesc(String lastNamePattern);
```

Podczas ładowania kontekstu, Spring przetwarza nazwę metody, mapuje ją na zapytanie JPQL (Java Persistence Query Language) i tworzy implementację w locie.

---

### 4. Czym jest `@Query` i kiedy warto z niego korzystać?

`@Query` to adnotacja pozwalająca na ręczne zdefiniowanie zapytania (w JPQL lub natywnym SQL) bezpośrednio nad metodą w interfejsie repozytorium.

**Kiedy warto używać?**
1. **Zbyt skomplikowane query derivation** – Gdy nazwa metody staje się absurdalnie długa (np. `findByFirstNameAndLastNameAndAgeGreaterThanAndStatusOrderByCreatedAtDesc`), `@Query` poprawia czytelność.
2. **Zapytania ze złączeniami (JOIN)** – Kiedy musimy połączyć kilka tabel (np. pobrać użytkownika z jego rolami i zamówieniami w jednym zapytaniu za pomocą `JOIN FETCH`, aby uniknąć problemu N+1).
3. **Specyficzne dla bazy danych operacje** – Gdy używamy natywnego SQL i chcemy wykorzystać specyficzne funkcje konkretnego silnika relacyjnego (np. `COALESCE`, `DATE_TRUNC` w PostgreSQL).
4. **Zapytania modyfikujące (Update/Delete)** – Masowe aktualizacje lub usuwanie rekordów bezpośrednio w bazie, zamiast ładowania encji do pamięci.

---

### 5. Jakie są różnice między JPQL a natywnym SQL w `@Query`?

| Cecha | JPQL (Java Persistence Query Language) | Natywny SQL (Native SQL) |
|---|---|---|
| **Adnotacja** | `@Query("SELECT u FROM User u WHERE u.age > ?1")` | `@Query(value = "SELECT * FROM users WHERE age > ?1", nativeQuery = true)` |
| **Na czym operuje** | Na klasach **encji** i ich polach (obiektowo) | Na rzeczywistych **tabelach** i kolumnach w bazie danych |
| **Przenośność** | **Wysoka** (Hibernate przetłumaczy JPQL na dialekt odpowiedniej bazy danych, np. PostgreSQL, MySQL) | **Niska** (zapytanie może przestać działać, jeśli zmienimy silnik bazy danych na inny) |
| **Walidacja na etapie startu** | Tak (Spring weryfikuje składnię przy starcie aplikacji) | Ograniczona (baza rzuci błąd dopiero przy wywołaniu zapytania) |
| **Zwracany typ** | Encje (lub DTO przez projekcje i `new`) | Tablice `Object[]` lub projekcje interfejsów (od Spring Data 2.0+) |

Domyślnie w `@Query` stosuje się JPQL. Natywnego SQL używa się w ostateczności dla optymalizacji lub bardzo specyficznych konstrukcji bazy.

---

### 6. Jak działa mechanizm projekcji (projections) w Spring Data?

Projekcje pozwalają na zdefiniowanie i pobranie z bazy danych tylko wymaganych pól (kolumn), zamiast całej encji. Zmniejsza to zużycie pamięci (RAM) oraz obciążenie sieci.

Mamy dwa główne typy projekcji w Spring Data:

1. **Interfejsy (Interface-based projections)**
Wystarczy stworzyć interfejs posiadający gettery dopasowane do właściwości encji.
```java
public interface UserSummary {
    String getFirstName();
    String getLastName();
}

// W repozytorium:
List<UserSummary> findByStatus(String status);
```
Spring stworzy proxy interfejsu (closed projection) i zoptymalizuje zapytanie SQL, wyciągając tylko imię i nazwisko.

2. **Klasy/DTO (Class-based projections)**
Tworzymy klasę (np. rekord) i używamy w zapytaniu, najczęściej w JPQL za pomocą konstrukcji `new`.
```java
public record UserDto(String firstName, String lastName) {}

@Query("SELECT new com.example.UserDto(u.firstName, u.lastName) FROM User u WHERE u.status = ?1")
List<UserDto> findDtosByStatus(String status);
```

---

### 7. Czym jest problem N+1 w Hibernate i jak go rozwiązać w kontekście Spring Data?

**Problem N+1 zapytań** to jedno z najczęstszych wąskich gardeł wydajnościowych w aplikacjach korzystających z ORM. Występuje, gdy system wykonuje 1 główne zapytanie SQL w celu pobrania listy encji (np. 10 użytkowników), a następnie dla każdej wyciągniętej encji wykonuje N dodatkowych zapytań, aby doczytać powiązane z nią dane relacyjne (np. adresy użytkownika). Zamiast 1 zapytania, aplikacja uderza do bazy 1 + N razy.

**Rozwiązania w Spring Data JPA:**

1. **Użycie `JOIN FETCH` w JPQL:** (najlepsze i najczęstsze podejście)
Wymusza na Hibernate dołączenie powiązanych encji w tym samym, jednym zapytaniu SQL.
```java
@Query("SELECT u FROM User u JOIN FETCH u.addresses WHERE u.status = :status")
List<User> findUsersWithAddresses(@Param("status") String status);
```

2. **`@EntityGraph`:**
Rozwiązanie czysto "Spring Data" omijające ręczne pisanie JPQL. Pozwala zadeklarować nad metodą, które relacje mają być dociągnięte w sposób *EAGER*.
```java
@EntityGraph(attributePaths = {"addresses", "roles"})
List<User> findAll();
```

3. **Użycie Batch Fetching:**
Zamiast pobierać relacje pojedynczo, Hibernate zbierze N identyfikatorów i wykona zapytanie z `IN (id1, id2, ..., idN)`. Włączane globalnie w properties:
`spring.jpa.properties.hibernate.default_batch_fetch_size=100`

---

### 8. Jak skonfigurować relacje `@OneToMany`, `@ManyToOne`, `@ManyToMany` i jakie są pułapki?

Konfiguracja relacji w JPA opiera się na adnotacjach w encjach.

- **`@ManyToOne`**: Strona posiadająca obcy klucz (FK). Jest właścicielem relacji.
- **`@OneToMany`**: Zwykle odwrotna strona relacji (inverse). Posiada parametr `mappedBy`, wskazujący na pole w encji właściciela.
- **`@ManyToMany`**: Zwykle wymaga tabeli łączącej (`@JoinTable`). Jedna strona musi mieć `mappedBy`.

**Przykład poprawnej relacji dwukierunkowej `@OneToMany` / `@ManyToOne`:**
```java
@Entity
public class Post {
    @Id @GeneratedValue
    private Long id;

    // mappedBy - ta strona NIE zapisuje klucza obcego
    @OneToMany(mappedBy = "post", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<Comment> comments = new ArrayList<>();

    // Metody pomocnicze (synchronizacja obu stron relacji)
    public void addComment(Comment comment) {
        comments.add(comment);
        comment.setPost(this);
    }
}

@Entity
public class Comment {
    @Id @GeneratedValue
    private Long id;

    // Właściciel relacji (ta tabela ma kolumnę post_id)
    @ManyToOne(fetch = FetchType.LAZY) 
    @JoinColumn(name = "post_id")
    private Post post;
}
```

**Pułapki i Best Practices:**
1. **Niespójność obiektu w pamięci:** Zawsze twórz tzw. metody pomocnicze (np. `addComment()`), które aktualizują obie strony relacji dwukierunkowej, żeby kontekst persystencji się nie pomylił.
2. **Kolekcje w Hibernate to nie zwykłe listy:** Hibernate używa własnych kolekcji (np. `PersistentBag`). Dlatego listy w encjach inicjuj jako `= new ArrayList<>()` i nigdy nie podmieniaj całej listy setterem, tylko dodawaj/usuwaj obiekty z istniejącej kolekcji.
3. **`toString()` / `hashCode()` / `equals()` i rekurencja:** W relacjach dwukierunkowych lombokowe `@Data` lub `@ToString` spowoduje błąd `StackOverflowError`, gdy Post wywoła toString na Comment, a Comment na Post. Używaj `@ToString.Exclude` i bazuj `equals/hashCode` na naturalnym kluczu biznesowym (nie na zmiennym ID bazodanowym).

---

### 9. Czym jest `FetchType.LAZY` vs `FetchType.EAGER` i jakie mają konsekwencje?

Parametr `fetch` określa politykę ładowania danych powiązanych (z relacji) dla konkretnej encji.

- **`FetchType.EAGER` (chciwe, wczesne)**
  Dociąga dane relacyjne od razu podczas pobierania encji nadrzędnej (tworząc `JOIN` w SQL lub uruchamiając dodatkowe zapytania).
  - Domyślne dla relacji pojedynczych: `@ManyToOne`, `@OneToOne`.
  - **Konsekwencje:** Może prowadzić do olbrzymich spadków wydajności i ciągnięcia do pamięci całej bazy danych (np. jeśli User ma EAGER do Address, a Address ma EAGER do City itp.). Z reguły uznawane za **antywzorzec**, jeśli używane pochopnie.

- **`FetchType.LAZY` (leniwe, opóźnione)**
  Hibernate nie wykonuje zapytania do powiązanej tabeli od razu. W miejsce relacji podstawia pusty obiekt-zastępstwo zwany **Proxy**. Dopiero w momencie wywołania pierwszej metody na tej relacji (np. `user.getAddress().getCity()`), Hibernate doczytuje obiekt (wysyła SQL).
  - Domyślne dla kolekcji: `@OneToMany`, `@ManyToMany`.
  - **Konsekwencje:** Znacznie oszczędniejsze, ale jeśli Proxy spróbujemy odpytać z zamkniętą transakcją/sesją (np. w warstwie kontrolera podczas serializacji na JSON), otrzymamy słynny wyjątek `LazyInitializationException`.
  
**Złota zasada JPA:** Zawsze wymuszaj we wszystkich relacjach `fetch = FetchType.LAZY`, a potrzebne grafy obiektów inicjalizuj jawnie dla danego Use-Case za pomocą `JOIN FETCH` (w `@Query`) lub `@EntityGraph`.

---

### 10. Jak działa `@Transactional` — propagacja, izolacja, rollback?

`@Transactional` to adnotacja Springa zapewniająca właściwości ACID (Atomicity, Consistency, Isolation, Durability) dla bloku kodu (np. metody w warstwie `@Service`). Spring owija wywołanie tej metody w proxy AOP, które zarządza otwieraniem i zatwierdzaniem (`commit`) transakcji bazodanowej.

- **Propagacja (Propagation):**
  Określa zachowanie, gdy metoda transakcyjna zostanie wywołana z wewnątrz innej metody transakcyjnej.
  - `REQUIRED` (domyślna) – Dołącz do istniejącej transakcji, a jeśli nie ma, utwórz nową.
  - `REQUIRES_NEW` – Zawiesza obecną transakcję i zawsze tworzy nową (np. dla logowania błędu, który musi się zapisać nawet jeśli transakcja nadrzędna zrollbackuje).
  - `MANDATORY` – Rzuca wyjątek, jeśli nie jesteśmy aktualnie w transakcji.

- **Poziom izolacji (Isolation):**
  Zabezpiecza przez anomaliami w przypadku współbieżnych modyfikacji (`DIRTY READ`, `NON_REPEATABLE READ`, `PHANTOM READ`).
  - Domyślnie (`DEFAULT`) przyjmuje ustawienie wybrane przez silnik bazy danych (np. `READ_COMMITTED` dla PostgreSQL/Oracle).
  - Możliwe wartości np. `REPEATABLE_READ` lub `SERIALIZABLE` (najbardziej rygorystyczna, w całości blokuje wiersze).

- **Wycofywanie (Rollback):**
  Domyślnie Spring wycofuje transakcję (rollback) **tylko** dla wyjątków niesprawdzanych (`RuntimeException`) i typu `Error`. Wyjątki sprawdzane (checked exceptions, dziedziczące po `Exception`) powodują zatwierdzenie (commit)!
  - Aby zmienić to zachowanie: `@Transactional(rollbackFor = Exception.class)`.

---

### 11. Czym jest `@Modifying` i kiedy jest wymagane?

Adnotacja `@Modifying` musi być dodana w repozytorium Spring Data JPA nad każdą metodą korzystającą z własnego `@Query`, która **modyfikuje** stan bazy danych, czyli dla instrukcji typu `UPDATE` lub `DELETE` oraz wywołań DDL. 

Bez dodania tej adnotacji, Hibernate potraktuje zapytanie jako instrukcję selektującą (`SELECT`), co zakończy się wyrzuceniem `InvalidDataAccessApiUsageException`.

```java
@Modifying
@Query("UPDATE User u SET u.active = false WHERE u.lastLoginDate < :date")
int deactivateOldUsers(@Param("date") LocalDate date);
```

**Uwaga:** Adnotacja często idzie w parze z flagą `clearAutomatically = true` (np. `@Modifying(clearAutomatically = true)`), co zapewnia wymuszone wyczyszczenie obiektu w persystentnym kontekście z pamięci RAM (czyszczenie Level 1 Cache) tuż po wykonaniu aktualizacji. Zapobiega to sytuacji w której w tej samej transakcji, inna metoda wyciągnęłaby niezaktualizowane dane danego użytkownika z pamięci podręcznej Hibernate.

---

### 12. Jak skonfigurować auditing (`@CreatedDate`, `@LastModifiedDate`)?

Auditing w JPA to mechanizm pozwalający automatycznie uzupełniać określone kolumny audytowe (kto i kiedy modyfikował wiersz), bez konieczności ręcznego wstawiania wartości podczas wykonywania `.save()`.

**Kroki konfiguracyjne:**
1. W klasie z konfiguracją aplikacji musimy dodać włączenie obsługi: `@EnableJpaAuditing`.
2. Encję należy ubrać na poziomie klasy w specyficznego Listenera: `@EntityListeners(AuditingEntityListener.class)`.
3. Do pól należy dodać stosowne adnotacje:
```java
@Entity
@EntityListeners(AuditingEntityListener.class)
public class Article {
    @Id @GeneratedValue
    private Long id;

    @CreatedDate
    @Column(updatable = false)
    private LocalDateTime createdAt;

    @LastModifiedDate
    private LocalDateTime updatedAt;
    
    @CreatedBy
    private String author; // Wymaga beana implementującego AuditorAware<String> by wyjąć usera z SecurityContext
}
```

---

### 13. Czym jest Specification API i kiedy warto go używać?

`Specification` to interfejs stanowiący nakładkę i abstrakcję na Hibernate Criteria API pozwalający na skrajnie zaawansowane budowanie dynamicznych zapytań SQL od podstaw po stronie aplikacji, nie wymagając od nas pisania hardcodowanego Stringa.

**Kiedy warto go używać?**
Gdy musimy napisać generyczne sortowanie bazy z kilkudziesięcioma opcjonalnymi i łączonymi warunkami "AND/OR" wysyłanymi z formatki szukania na froncie, zbudowanymi podczas działania aplikacji (runtime). Napisanie tego w `@Query` lub czystym JPQL zmusiłoby nas do żmudnego concatenowania Stringów i masy instrukcji if-else.

Wymaga ujęcia interfejsu repozytorium przez dodatkowe odziedziczenie `JpaSpecificationExecutor<T>`.

---

### 14. Jak działa cache pierwszego i drugiego poziomu w Hibernate?

1. **First-level Cache (L1 Cache – Cache sesji):**
  - **Domyślnie WŁĄCZONY** i nie da się go na stałe wyłączyć.
  - Jest związany pojedynczą transakcją / sesją JPA (`EntityManager`).
  - Działa przez cały cykl życia `@Transactional`. Jeśli wyciągniemy encję po ID dwa razy w jednej metodzie transakcyjnej, Hibernate nie wyśle do bazy dwóch zapytań SQL — przy drugim żądaniu zwróci wprost obiekt już siedzący z ramu.

2. **Second-level Cache (L2 Cache – Cache fabryki):**
  - **Domyślnie WYŁĄCZONY**. Trzeba skonfigurować zewnętrznego providera (np. Ehcache, Hazelcast, Redis).
  - Skupia się na współdzieleniu danych pomiędzy wieloma sesjami globalnymi całej aplikacji, a w połączeniu z chmurą - całymi klastrami serwerów.
  - Optymalne włącza się tylko przy mocno doczytywanych, ale niezwykle rzadko modyfikowanych tabelach słownikowych (Kraje, Statusy, Typy walut), co redukuje narzut do relacyjnej bazy o tysiące niepotrzebnych Selectów na minutę. Konfiguracja polega zazwyczaj na nadaniu `@Cacheable` ze strony adnotacji Hibernate (nie Springowej) bezpośrednio nad definicją `@Entity`.

---

### 15. Czym jest optimistic locking (`@Version`) i jak działa w Spring Data?

**Optimistic Locking (blokowanie optymistyczne)** to zapobieganie nadpisaniu sobie danych w bazie przez dwóch użytkowników w przypadku jednoczesnej edycji (concurrent modification), stosowane zamiast kosztownego pełnego ryglowania wiersza dla innych transakcji na etapie wczesnym (Pessimistic Locking).

Implementacja w JPA odbywa się tylko poprzez nadanie pojedynczemu liczbowemu polu w klasie encji adnotacji `@Version`:

```java
@Entity
public class BankAccount {
    @Id @GeneratedValue private Long id;
    private BigDecimal balance;
    
    @Version
    private Long version;
}
```

**Jak to działa?**
Kiedy encja jest zaczytywana z bazy do pamięci RAM klienta A, widzi on np. `version = 1`. 
Klient B zaczytuje te same rekordy i też dostaje `version = 1`. 
Gdy klient A finalizuje zmianę salda, podczas wykonywania UPDATE powiększy on wersję z 1 do 2. Kiedy klient B chwilę później zapisuje swoje zmiany, aplikacja wykonuje `UPDATE BankAccount SET balance=?, version=2 WHERE id=? AND version=1`. A że wersja w bazie ma już numer 2 zaktualizowany przed sekundą przez klienta A – dla klienta B warunek klauzuli zawiedzie i dotknie 0 wierszy bazy. Hibernate natychmiast wyrzuci specyficzny błąd `ObjectOptimisticLockingFailureException`, odrzucając niespójne zapisanie zdezaktualizowanych zmian.

---

### 16. Jak obsłużyć migracje bazy danych (Flyway / Liquibase) w projekcie Spring?

W profesjonalnych projektach poleganie na hibernate'owskim `spring.jpa.hibernate.ddl-auto=update` jest kategorycznie zablokowane na produkcji – schemat ewolucji bazy powinien być w sposób uporządkowany zdefiniowany w formie konkretnych plików skryptów modyfikujących.

Dwie wiodące biblioteki narzędzi to **Flyway** oraz **Liquibase**. 
Gdy podłączymy do projektu np. `flyway-core`, Spring Boot auto-konfiguruje środowisko. 

Pliki migracji oznaczamy prefiksem wersji (np. `V1__init_schema.sql`, `V2__add_users_table.sql`) i wrzucamy do odpowiedniego folderu classpath: `src/main/resources/db/migration/`.

Podczas każdorazowego startu aplikacji w systemie:
1. Skrypt czyta ze swojej roboczej tabeli ewidencyjnej w DB (tworzonej samoczynnie), czy baza danych posiada zapamiętany wariant bazy v1.
2. Odpala i wykonuje różnicowe pliki ewolucyjne z nowszymi wersjami, zabezpieczając system. 
3. Wersjonowanie znajduje swoje miejsce odzwierciedlone w commicie na Github.

---

## 5. Spring AOP (Aspect-Oriented Programming)

1. Czym jest programowanie aspektowe i jakie problemy rozwiązuje?
2. Jakie są kluczowe pojęcia AOP: aspekt, advice, pointcut, join point, weaving?
3. Jakie typy advice oferuje Spring AOP (`@Before`, `@After`, `@Around`, `@AfterReturning`, `@AfterThrowing`)?
4. Czym jest pointcut expression i jak je definiować?
5. Jak działa mechanizm proxy w Spring AOP (JDK dynamic proxy vs CGLIB)?
6. Dlaczego wywołanie metody wewnątrz tej samej klasy omija aspekt (self-invocation problem)?
7. Czym różni się Spring AOP od pełnego AspectJ?
8. Jak zaimplementować logowanie cross-cutting za pomocą AOP?
9. Jak `@Transactional` wykorzystuje AOP pod spodem?
10. Jakie są ograniczenia Spring AOP?

---

## 6. Spring Security

1. Jak działa łańcuch filtrów (filter chain) w Spring Security?
2. Czym jest `SecurityFilterChain` i jak go konfigurować w Spring 3.x?
3. Jak zaimplementować uwierzytelnianie (authentication) w Spring Security?
4. Czym jest `UserDetailsService` i jak go dostosować?
5. Jak działa autoryzacja (authorization) — `@PreAuthorize`, `@Secured`, `@RolesAllowed`?
6. Czym jest `PasswordEncoder` i dlaczego nie wolno przechowywać haseł w plain text?
7. Jak skonfigurować uwierzytelnianie JWT w Spring Security?
8. Jak skonfigurować OAuth2 Login i Resource Server?
9. Jak działa CSRF protection i kiedy warto ją wyłączyć?
10. Jak skonfigurować CORS w Spring Security?
11. Jak zaimplementować method-level security?
12. Czym jest `SecurityContext` i jak jest przechowywany (ThreadLocal)?
13. Jak obsłużyć sesje i zabezpieczenie przed session fixation?
14. Jak testować Spring Security w testach integracyjnych (`@WithMockUser`)?

---

## 7. Spring Boot

### 1. Czym jest Spring Boot i jakie problemy rozwiązuje w porównaniu do „czystego" Spring?

**Spring Boot** to ewolucja i rozszerzenie ekosystemu Spring Framework, które ma na celu maksymalne uproszczenie i przyspieszenie procesu tworzenia aplikacji (tzw. podejście *opinionated* — Spring narzuca własne, domyślne rozwiązania z najlepszych praktyk).

**Problemy, które rozwiązuje (różnice względem czystego Springa):**
1. **Konfiguracja XML / Boilerplate Java Config:** "Czysty" Spring wymagał potężnej ręcznej konfiguracji komponentów (m.in. transakcji, widoków, źródeł danych). Boot dostarcza mechanizm **autokonfiguracji**, samoczynnie włączając potrzebne moduły na podstawie dostępnych w classpathie bibliotek.
2. **Piekło zależności (Dependency Hell):** Zamiast dobierać kompatybilne ze sobą wersje kilkunastu bibliotek (Spring Core, Hibernate, Jackson, Tomcat), Boot używa **Starterów** (np. `spring-boot-starter-web`), które pociągają za sobą gwarantowane, zgrane i przetestowane wersje zależności z tzw. Spring Boot BOM (Bill of Materials).
3. **Zewnętrzne serwery aplikacyjne:** Tradycyjny Spring budował plik `.war`, który należało ręcznie wgrać na osobny serwer (Tomcat/WildFly). Boot posiada serwer **wbudowany (Embedded Server)** — aplikacja to plik uruchamialny `.jar` odpalany przez `java -jar`.
4. **Brak gotowości produkcyjnej:** Boot dostarcza gotowe do uruchomienia na produkcji moduły (Spring Boot Actuator), oferujące endpointy sprawdzające zdrowie (health checks), metryki czy konfigurację, bez pisania linijki kodu.

---

### 2. Jak działa mechanizm autokonfiguracji (`@EnableAutoConfiguration`, `spring.factories` / `AutoConfiguration.imports`)?

Mechanizm autokonfiguracji to rdzeń Spring Boot. Jego zadaniem jest odgadnięcie i skonfigurowanie beanów, których najprawdopodobniej będziesz potrzebować, zwalniając z tego programistę.

**Jak to działa krok po kroku:**
1. Adnotacja **`@EnableAutoConfiguration`** (będąca częścią `@SpringBootApplication`) po odpaleniu aplikacji uruchamia pod maską klasę `AutoConfigurationImportSelector`.
2. Spring Boot skanuje pliki z jarów (do wersji Boot 2.7.x szukał w pliku `META-INF/spring.factories`, od Spring Boot 3.0.x oficjalnie przeszedł w pełni na plik tekstowy: `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports`).
3. Plik ten zawiera długą listę referencji do tzw. klas autokonfiguracji (np. `DataSourceAutoConfiguration`, `JacksonAutoConfiguration`).
4. Każda z tych klas konfiguracyjnych jest naszpikowana adnotacjami warunkowymi (np. `@ConditionalOnClass(DataSource.class)` lub `@ConditionalOnMissingBean`). 
5. Boot ocenia te warunki i jeśli widzi w projekcie sterownik bazy, a my nie napisaliśmy własnego DataSource – autokonfiguracja tworzy go i ustawia ze wbudowanych `application.properties`.

---

### 3. Czym jest `@SpringBootApplication` i co zawiera?

`@SpringBootApplication` to kluczowa meta-adnotacja nakładana na główną klasę projektu. W uproszczeniu jest to agregacja trzech potężnych adnotacji Springa:

1. **`@SpringBootConfiguration`** — To techniczny alias na tradycyjne `@Configuration`. Oznacza, że główna klasa aplikacji może definiować własne metody fabrykujące (`@Bean`).
2. **`@EnableAutoConfiguration`** — Włącza opisany wyżej mechanizm autokonfiguracji, nakazujący Springowi Boot podłączyć domyślne rozwiązania dla obecnych w classpath zależności.
3. **`@ComponentScan`** — Instruuje środowisko o automatycznym skanowaniu pakietów (domyślnie: od pakietu, w którym znajduje się ta główna klasa, w dół do wszystkich podpakietów) w celu znalezienia Twoich `@Component`, `@Service`, `@Controller` itp.

---

### 4. Jak Spring Boot rozwiązuje zarządzanie zależnościami (starter POMs, BOM)?

1. **Starter POMs (Startery):**
To zestawy pustych projektów z zależnościami wbudowanymi przez Springa, służące jako deskryptory. Dodając do Mavena/Gradle np. `spring-boot-starter-web`, Boot uwalnia programistę od dodawania paczek typu: `spring-webmvc`, `spring-core`, `tomcat-embed-core`, `jackson-databind`. Starter zaciągnie je w odpowiednim zestawie.

2. **BOM (Bill of Materials):**
BOM gwarantuje zgodność wersji wszystkich bibliotek zaciąganych przez startery w całym ekosystemie Springa. Dzięki projektowi `spring-boot-dependencies` dodanym do `<dependencyManagement>`, definiując własną zależność ze środowiska Spring, nie podajemy elementu `<version>`. Wersja jest narzucana odgórnie przez zainstalowaną globalnie wersję Spring Boot, rozwiązując odwieczny problem z konfliktami i nakładaniem się bibliotek (tzw. "Jar Hell").

---

### 5. Czym są profile (`application-{profile}.yml`) i jak je aktywować?

Profile to sposób na segregację i warunkowe ładowanie różnych zestawów konfiguracji (properties/beans) w zależności od środowiska, w którym uruchomiana jest aplikacja (np. `dev`, `test`, `prod`).

**Tworzenie profili:**
Aplikacja ma zazwyczaj wspólny plik `application.yml` oraz wiele profili pobocznych:
- `application-dev.yml` (baza H2, pełne logi SQL)
- `application-prod.yml` (baza PostgreSQL na chmurze AWS)

**Zasada działania:**
Cokolwiek znajduje się w aktywnym profilu specjalistycznym, nadpisze odpowiadający mu parametr w bazowym, bezprofilowym `application.yml`.

**Aktywacja profilu (sposoby):**
- Flaga w terminalu (najczęstsze w DevOps): `java -jar app.jar --spring.profiles.active=prod`
- Zmienna systemowa OS: `SPRING_PROFILES_ACTIVE=prod`
- W pliku `application.yml`: `spring.profiles.active: dev`
- Adnotacją w kodzie testów: `@ActiveProfiles("test")`

---

### 6. Jak działa externalized configuration i jaki jest priorytet źródeł konfiguracji?

Externalized Configuration to zasada pozwalająca oddzielić kod źródłowy aplikacji od jej właściwości. Możesz używać tego samego spakowanego pliku `.jar` na wszystkich środowiskach, zmieniając tylko zewnętrzne zmienne.

Spring Boot scala dane z różnych miejsc w jedną strukturę `Environment`. Mają one swoją ścisłą hierarchię priorytetów (kolejne punkty z listy nadpisują te zdefiniowane wcześniej). Najważniejsze z nich to:

1. Właściwości domyślne aplikacji (`SpringApplication.setDefaultProperties`).
2. Plik `application.yml` zaszyty w spakowanym JAR.
3. Plik `application-{profile}.yml` zaszyty w spakowanym JAR.
4. Zewnętrzny plik `application.yml` / `application-{profile}.yml` umieszczony luzem w tym samym katalogu systemu co obok plik JAR.
5. Zmienne środowiskowe z systemu operacyjnego (OS environment variables, np. zapisane dużymi literami `SERVER_PORT=8081`).
6. Właściwości argumentów przekazywanych do JVM podczas uruchamiania systemu np. ( `-Dserver.port=8082`).
7. **(NAJWYŻSZY PRIORYTET):** Argumenty wiersza poleceń uruchomienia samej apki (np. `--server.port=8083`).

---

### 7. Jak utworzyć własny starter Spring Boot?

Stworzenie własnego startera jest użyteczne w korporacjach do standaryzacji, żeby jednym dependency narzucać wspólną bibliotekę, jej beansy i domyślną strukturę (np. logowanie do Kafki z autokonfiguracją bezpieczeństwa).

**Kroki budowy startera:**
1. Zbudować standardowy projekt Maven. Powinien mieć on nazewnictwo nie kradnące słowa "spring", najczęściej nazywa się je formatem `{twoja-nazwa}-spring-boot-starter`.
2. Dodać kod konfiguracji – piszemy klasę oznaczoną adnotacją `@AutoConfiguration` (lub `@Configuration`). Dodajemy adnotacje typu `@ConditionalOnMissingBean` dla zadeklarowanych usług.
3. Zarejestrować konfigurację we wbudowanych plikach konfiguracyjnych SPI:
   W katalogu `src/main/resources/META-INF/spring/` tworzymy plik o precyzyjnej nazwie: `org.springframework.boot.autoconfigure.AutoConfiguration.imports`. Wpisujemy do niego FQDN (pełną nazwę z pakietem) naszej klasy konfiguracji.
4. Publikujemy plik do zdalnego/lokalnego repozytorium Maven i od teraz każdy inny podzespół deweloperski może tylko zaciągnąć Twoją bibliotekę z pom.xml, a Spring Boot natychmiast wykryje wpis i załaduje obiekty sam.

---

### 8. Czym jest embedded server i jak zmienić domyślny serwer (Tomcat → Jetty / Undertow)?

Embedded server (Wbudowany Serwer) oznacza architekturę, w której aplikacja Java *wewnątrz* swoich bibliotek przechowuje logikę kompletnego serwera http. W "czystym" starym Java EE, Tomcat był oddzielnym programem, do którego wrzucaliśmy gotowe i spakowane artefakty. W Spring Boot to uruchomiana sama w sobie aplikacja startuje swój prywatny serwer i w nim odpina swoje gniazda HTTP. Z punktu widzenia systemu to standardowy proces Javy wywoływany przez `java -jar`. Domyślnie Spring Boot ma wbudowany serwer **Apache Tomcat**.

**Zmiana domyślnego serwera z Tomcat na np. Undertow:**
1. Trzeba jawnie zablokować startera pobierania Tomcata (używając znaczników `<exclusion>` dla paczki web).
2. Dociągnąć paczkę wybranego serwera z repozytorium Mavena.
```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
    <exclusions>
        <exclusion>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-tomcat</artifactId>
        </exclusion>
    </exclusions>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-undertow</artifactId>
</dependency>
```

---

### 9. Jak działa mechanizm `@ConditionalOnClass`, `@ConditionalOnProperty` itd.?

Mechanizm warunkowy pozwala zablokować z góry próbę zaczytywania klas jako beanów przez Springa w locie, w oparciu o ustalone i podane z góry kryteria dla danej weryfikacji. 

Wykorzystywane jest to masowo we wbudowanej autokonfiguracji Springa, zapobiegając wysypaniu aplikacji ze względu na brak wymaganych obiektów w Classpathie do połączenia w pary.

Najważniejsze z nich to:
- **`@ConditionalOnClass(DataSource.class)`** – Wykonaj i załaduj beany konfiguracji, ale *Tylko* wtedy gdy programista dodał do `pom.xml` zewnętrzny sterownik biblioteki dający w projekcie klasę z podanym bytem.
- **`@ConditionalOnMissingBean(MyService.class)`** – Jeżeli podepniesz ten sam interfejs usługi w głównej apce do `pom.xml`, autokonfigurator odsunie wbudowany w Spring default. W skrócie (Stwórz i nadaj domyślne, o ile programista tego wcześniej celowo nie przeciążył własnym beanem).
- **`@ConditionalOnProperty(name = "features.mailer", havingValue = "true")`** – Załaduje tego beana, *Tylko* gdy w pliku `application.yml` istnieje przypisanie `features.mailer: true`.

---

### 10. Czym jest `CommandLineRunner` i `ApplicationRunner`?

To dwa funkcjonalne, wbudowane ze Springa interfejsy. Implementując jako bean z nich dowolny w środowisku, sprawimy, że zawarty kod wykona się automatycznie, samodzielnie i gwarantowanie **tylko raz**, dokładnie tuż po w pełni poprawnym podniesieniu Springowego Kontekstu Zależności, ale przed oddaniem konsoli w terminal użytkownika.

Stosowane zazwyczaj do:
- Szybkiego podpięcia i wygenerowania losowych przykładowych danych do testów do bazy w środowiskach dev.
- Walidacji stanów portów bądź pobrania plików certyfikatów startowych z zewnętrznego serwera plików.
- Przeliczania bądź zrzuceń bazowych cache.

**Różnice między nimi:**
Oba robią dokładnie to samo, różnią się tylko formą obsługi nadciągających z terminala argumentów od dewelopera. 
- `CommandLineRunner` dostarcza wejściowe parametry jako nagi i czysty tablicowy `String... args`.
- `ApplicationRunner` przekłada to wyżej wyłapując w obiekt po parsingu jako instancję obiektu `ApplicationArguments` z wieloma możliwościami map, metod wyciągających iteratory itp.

---

### 11. Jak działa graceful shutdown w Spring Boot?

Graceful shutdown (łagodne zamykanie aplikacji) to potężny mechanizm w projektach wielo-serwerowych polegający na tym, że po wpłynięciu nakazu zamknięcia procesu dla np. Tomcata u Springa (często wysłanego przez instancję orkiestratora Kubernetes przy ubijaniu Poda w którym aplikacja żyła), serwer wbudowany podejmuje dwa kroki przed ubiciem:

1. Na port serwera przestają być natychmiastowo akceptowane absolutnie jakiekolwiek nowe żądania przychodzące.
2. Zostaje odliczony zadany odgórnie konfiguracyjnie margines "Timeout" przeznaczony na ciche wymieranie i zakończenie bez przerw obsługi żądań i przetwarzających obciążeń tych wywołań na Endpointy, które system wpuścił w sieć Tomcat i zdążył przetwarzać na ułamek sekundy przed odebraniem wywołanego odłączenia bazy zasilania.

**Aktywacja w YAML od Spring Boot 2.3+:**
```yaml
server:
  shutdown: graceful  # domyślnie jest immediate
spring:
  lifecycle:
    timeout-per-shutdown-phase: 30s # Czeka max 30 sek przed brutalnym killem
```

---

### 12. Czym jest DevTools i jak wspomaga development?

**Spring Boot DevTools** to dedykowana poboczna paczka narzędzi w środowisku `pom.xml` nastawiona optymalnie i stricte tylko pod ułatwienie lokalnej pracy programisty w IDE (narzędzia ignorują odpalanie gdy kod kompiluje się z wbudowanego spakowanego paczkowanego `.jar`).

**Co oferuje?**
1. **Automatyczny restart (Live Reload):** Spring ucieka się od pełnego, zajmującego wieki stawiania JVM pod start Tomcata. Za pomocą systemów obserwacji dwóch klasładowerów, pozwala na odpalenie zmian w kodzie javy w serwerze od zera do kilku milisekund, wystarczy nadpisać przebudowanie kodu klasy (Ctrl+S / Build).
2. **Wyłączenie lokalnego cache na sztywno:** Na lokalce od razu wymusza na wbudowanych silnikach np. Thymeleaf/Freemarker pomijanie opcji szukania zcacheowanych templatów od plików .html w RAM serwera, każdorazowo dobierając to z plików – dzięki czemu odświeżenie samej strony załapie zmiany we wbudowanym formacie w ułamku sekundy, z nałożonym z automatu przez DevTools nasłuchiwaniem *LiveReload* po stronie samej zakładki w Chrome.

---

## 8. Spring Boot Actuator / Monitoring

1. Czym jest Spring Boot Actuator i jakie endpointy udostępnia?
2. Jak zabezpieczyć endpointy Actuatora?
3. Jak dodać własny endpoint do Actuatora?
4. Jak skonfigurować health indicators i custom health checks?
5. Jak zintegrować Actuator z Prometheus i Grafana?
6. Czym są metryki Micrometer i jak je wykorzystać?
7. Jak skonfigurować distributed tracing (np. Zipkin, Jaeger)?

---

## 9. Spring WebFlux / Programowanie reaktywne

1. Czym jest Spring WebFlux i czym różni się od Spring MVC?
2. Czym jest `Mono` i `Flux` w kontekście Project Reactor?
3. Kiedy warto wybrać model reaktywny zamiast imperatywnego?
4. Jak działa backpressure w programowaniu reaktywnym?
5. Czym jest `WebClient` i dlaczego zastępuje `RestTemplate` w aplikacjach reaktywnych?
6. Jak obsłużyć błędy w łańcuchach reaktywnych (`onErrorResume`, `onErrorReturn`)?
7. Czym jest `RouterFunction` i jak definiować endpointy funkcyjnie?
8. Jakie bazy danych wspierają R2DBC i jak go skonfigurować ze Spring Data?
9. Jak testować kod reaktywny (`StepVerifier`)?
10. Jakie są pułapki mieszania kodu blokującego z reaktywnym?

---

## 10. Spring Testing

1. Czym jest `@SpringBootTest` i kiedy go używać?
2. Jakie są różnice między testem jednostkowym a testem integracyjnym w kontekście Spring?
3. Jak działa `@MockBean` i `@SpyBean`?
4. Czym jest `@DataJpaTest` i jakie warstwy ładuje?
5. Czym jest `@WebMvcTest` i jak testować kontrolery w izolacji?
6. Jak działa `MockMvc` i jak weryfikować odpowiedzi HTTP?
7. Czym jest `@Testcontainers` i jak wykorzystać kontenery w testach?
8. Jak testować endpointy REST z `TestRestTemplate` lub `WebTestClient`?
9. Jak używać profili testowych (`@ActiveProfiles("test")`)?
10. Czym jest slice testing i jakie slices są dostępne?
11. Jak zarządzać kontekstem testowym (`@DirtiesContext`)?

---

## 11. Spring Cache

1. Jak działa abstrakcja cache w Spring (`@Cacheable`, `@CacheEvict`, `@CachePut`)?
2. Jakie implementacje cache wspiera Spring (EhCache, Caffeine, Redis)?
3. Jak skonfigurować klucze cache i niestandardowy `KeyGenerator`?
4. Jak działa warunkowe cachowanie (`condition`, `unless`)?
5. Jakie są pułapki korzystania z `@Cacheable` w połączeniu z proxy AOP?

---

## 12. Spring Events / Messaging

1. Jak działa mechanizm zdarzeń w Spring (`ApplicationEvent`, `@EventListener`)?
2. Czym jest `@TransactionalEventListener` i kiedy go używać?
3. Jak skonfigurować asynchroniczną obsługę zdarzeń?
4. Jak zintegrować Spring z Apache Kafka / RabbitMQ?
5. Czym jest Spring Cloud Stream i jak upraszcza messaging?

---

## 13. Spring Scheduling / Async

1. Jak skonfigurować zadania cykliczne (`@Scheduled`, `@EnableScheduling`)?
2. Jakie są strategie harmonogramowania (fixedRate vs fixedDelay vs cron)?
3. Jak działa `@Async` i `@EnableAsync`?
4. Jak skonfigurować pulę wątków (`TaskExecutor`) dla operacji asynchronicznych?
5. Jak obsłużyć wyjątki w metodach `@Async`?
6. Czym jest `CompletableFuture` w kontekście `@Async`?

---

## 14. Spring Cloud (mikroserwisy)

1. Czym jest Spring Cloud i jakie moduły wchodzą w jego skład?
2. Jak działa Service Discovery (Eureka / Consul)?
3. Czym jest Spring Cloud Config i jak centralizować konfigurację?
4. Jak działa wzorzec Circuit Breaker (Resilience4j)?
5. Czym jest API Gateway (Spring Cloud Gateway) i jak konfigurować routing?
6. Jak zaimplementować distributed tracing w mikroserwisach?
7. Czym jest Feign Client i jak upraszcza komunikację między serwisami?
8. Jak działa load balancing po stronie klienta (Spring Cloud LoadBalancer)?

---

## 15. Architektura i dobre praktyki

1. Jak zorganizować warstwy aplikacji Spring (controller → service → repository)?
2. Czym jest wzorzec DTO i dlaczego warto oddzielać model domeny od API?
3. Jak stosować zasadę Dependency Inversion w Spring?
4. Czym jest hexagonal architecture i jak ją zaimplementować ze Spring?
5. Jak obsłużyć transakcje w serwisach rozproszonych (Saga pattern)?
6. Jak zarządzać migracjami schematu bazy danych w dużych projektach?
7. Jak projektować idempotentne endpointy REST?
8. Czym jest CQRS i jak go zaimplementować ze Spring?
9. Jak efektywnie logować i monitorować aplikację Spring w produkcji?
10. Jak zarządzać konfiguracją wrażliwych danych (secrets) w aplikacji Spring?

---

## Powiązane notatki

- [Konfiguracja boolean w Springu](konfiguracja-boolean-w-springu.md)
- [Model w Spring MVC](model-w-spring-mvc.md)
- [Przekazywanie danych w Spring MVC](przekazywanie-danych-w-spring-mvc.md)
- [Problem N+1 w Hibernate](problem-n1-w-hibernate.md)
- [Stany obiektów Hibernate](stany-obiektów-hibernate.md)
- [Logowanie w Spring Boot](logowanie-w-spring-boot.md)
- [InjectMocks w Mockito](injectmocks-w-mockito.md)
- [Sposoby tworzenia beanów](sposoby-tworzenia-beanów.md)
