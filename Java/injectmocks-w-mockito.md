# @InjectMocks w Mockito

**Data:** 2025-05-28

---

**User:**

Przykład unit testu
@ExtendWith(MockitoExtension.class)
class EmailServiceUnitTest {

    @Mock
    DeliveryPlatform platform;

    @InjectMocks
    EmailService emailService;
  
    ...
}

Opisz użycie  @InjectMocks

---

**Assistant:**

Adnotacja `@InjectMocks` w bibliotece **Mockito** służy do tworzenia instancji klasy testowanej (w tym przypadku `EmailService`) **z automatycznym wstrzyknięciem zależności**, które są oznaczone adnotacją `@Mock` (np. `DeliveryPlatform`).

### Jak to działa?

Mockito:

1. Tworzy nową instancję klasy oznaczonej `@InjectMocks` (czyli `EmailService`).
2. Przeszukuje pola tej klasy i **automatycznie wstrzykuje** odpowiednie mocki utworzone przez `@Mock`, `@Spy` lub inne.
   - Wstrzykiwanie może być przez konstruktor, settery lub bezpośrednio do pól (field injection), w zależności od tego, co jest dostępne.

### W tym przykładzie:

```java
@ExtendWith(MockitoExtension.class)
class EmailServiceUnitTest {

    @Mock
    DeliveryPlatform platform; // mockowana zależność

    @InjectMocks
    EmailService emailService; // testowany serwis z automatycznym wstrzyknięciem platform
}
```

- Mockito utworzy mock `DeliveryPlatform` i wstrzyknie go do instancji `EmailService`.
- Dzięki temu możesz testować `EmailService` w izolacji, bez faktycznej implementacji `DeliveryPlatform`.

### Przykładowy test:

```java
@Test
void shouldSendEmail() {
    // given
    String email = "test@example.com";
    when(platform.send(email)).thenReturn(true);

    // when
    boolean result = emailService.sendEmail(email);

    // then
    assertTrue(result);
    verify(platform).send(email);
}
```

### Zalety `@InjectMocks`:

- Automatyzuje i upraszcza przygotowanie testu.
- Zapewnia, że testowana klasa otrzyma odpowiednio przygotowane mocki.
- Eliminuje konieczność ręcznego wstrzykiwania zależności (np. przez konstruktory lub settery).

Jeśli chcesz, mogę też pokazać przykład ręcznego wstrzykiwania bez `@InjectMocks` dla porównania.

---

**User:**

czy można uniknąć użycia @InjectMocks?

---

**Assistant:**

Tak, **można uniknąć użycia `@InjectMocks`**, ale wtedy trzeba **ręcznie utworzyć instancję testowanej klasy i samodzielnie wstrzyknąć zależności** (mocki). Jest to podejście bardziej jawne i daje większą kontrolę nad tym, jak tworzysz test, ale wymaga nieco więcej kodu.

### Przykład bez `@InjectMocks`

```java
@ExtendWith(MockitoExtension.class)
class EmailServiceUnitTest {

    @Mock
    DeliveryPlatform platform; // mock

    EmailService emailService; // testowany serwis

    @BeforeEach
    void setUp() {
        emailService = new EmailService(platform); // ręczne wstrzyknięcie zależności
    }

    @Test
    void shouldSendEmail() {
        // given
        String email = "test@example.com";
        when(platform.send(email)).thenReturn(true);

        // when
        boolean result = emailService.sendEmail(email);

        // then
        assertTrue(result);
        verify(platform).send(email);
    }
}
```

### Kiedy warto unikać `@InjectMocks`?

**ZA użyciem `@InjectMocks`:**
- Mniej kodu do pisania – wygodne, szybkie.
- Przydatne przy wielu zależnościach, gdy nie chcesz ręcznie tworzyć obiektu.

**PRZECIW użyciu `@InjectMocks`:**
- Mniej jawne – nie masz pełnej kontroli nad tym, jak wstrzykiwane są zależności.
- Jeśli konstruktor testowanej klasy robi coś więcej (np. walidacje), jawne tworzenie instancji może być lepsze.
- Czasem trudniej debugować błędy inicjalizacji.

### Podsumowanie

Tak – **można i czasami warto unikać `@InjectMocks`**, zwłaszcza jeśli zależy Ci na przejrzystości, jawnej konfiguracji zależności lub chcesz lepiej kontrolować cykl życia testowanej klasy.

---

**User:**

czyli przy zastosowaniu @InjectMocks prawdziwy konstruktor klasy nie jest wywoływany?

---

**Assistant:**

Nie — **przy użyciu `@InjectMocks` prawdziwy konstruktor testowanej klasy **_jest wywoływany_**. Mockito nie tworzy żadnej magicznej "płaskiej" instancji – to nie jest mock, tylko normalny obiekt. Różnica polega tylko na tym, **jak wstrzykiwane są zależności** (`@Mock`, `@Spy`, itp.).

### Jak to działa?

Gdy używasz `@InjectMocks`, Mockito:

1. **Tworzy instancję klasy `EmailService`**.
2. Próbuje dobrać sposób wstrzyknięcia zależności (mocków):
   - Najpierw szuka **konstruktora**, do którego może dopasować mocki.
   - Jeśli się nie uda, próbuje użyć **setterów** lub **wstrzyknięcia bezpośredniego do pól**.

Więc jeśli `EmailService` ma konstruktor z argumentem `DeliveryPlatform`, i masz mock `platform`, to Mockito wywoła:

```java
new EmailService(platform);
```

Czyli **konstruktor zostanie wykonany normalnie**, razem z ewentualną logiką w środku.

---

### Przykład dla zobrazowania:

```java
class EmailService {
    public EmailService(DeliveryPlatform platform) {
        System.out.println("Konstruktor EmailService wywołany!");
        this.platform = platform;
    }
    ...
}
```

Jeśli masz:

```java
@Mock DeliveryPlatform platform;
@InjectMocks EmailService emailService;
```

To podczas uruchomienia testu na konsoli pojawi się:

```
Konstruktor EmailService wywołany!
```

---

### Podsumowanie

- ✅ **Tak, konstruktor jest wywoływany**.
- ❌ `@InjectMocks` **nie omija** konstruktora, chyba że to konstruktor domyślny bez argumentów.
- 🤔 Dlatego, jeśli konstruktor zawiera logikę, `@InjectMocks` jej nie pominie — i dobrze o tym pamiętać przy pisaniu testów.

---

**User:**

Więc dlaczego napisałeś że 
"Jeśli konstruktor testowanej klasy robi coś więcej (np. walidacje), jawne tworzenie instancji może być lepsze."

---

**Assistant:**

Świetne pytanie — już wyjaśniam, co miałem na myśli i dlaczego ta uwaga ma sens **pomimo** że konstruktor jest wywoływany w obu przypadkach.

---

### Różnica nie w _tym, czy_ konstruktor jest wywoływany, ale _jak_ jest wywoływany

#### 1. **Przy `@InjectMocks`:**
- Mockito **automatycznie wybiera** konstruktor (jeśli jest więcej niż jeden) i **dopasowuje do niego mocki**.
- Ty nie masz pełnej kontroli nad tym, **który konstruktor zostanie użyty**, jeśli jest kilka.
- Jeśli np. masz walidację, która zależy od konkretnego stanu argumentów, to Mockito może wstrzyknąć mocka w sposób, który nie wywoła wyjątku, ale w rzeczywistości testujesz inny scenariusz, niż Ci się wydaje.

#### 2. **Przy ręcznym tworzeniu instancji:**
- Sam **jawnie wywołujesz konkretny konstruktor** i dokładnie widzisz, jakie argumenty przekazujesz.
- To bardziej przejrzyste i **czytelne**, co jest szczególnie istotne, jeśli konstruktor:
  - wykonuje dodatkową logikę (np. rejestruje komponent, uruchamia wątek, waliduje dane),
  - ma wiele wersji (przeciążonych konstruktorów),
  - działa niepoprawnie przy null/mockach, ale Mockito tego nie pokaże od razu.

---

### Przykład

```java
class EmailService {
    public EmailService(DeliveryPlatform platform) {
        if (platform == null) {
            throw new IllegalArgumentException("platform cannot be null");
        }
        this.platform = platform;
    }
}
```

#### Z `@InjectMocks`:

Mockito spróbuje wstrzyknąć mocka `platform`. Zadziała, ale:
- jeśli coś pójdzie nie tak (np. masz inne zależności), to Mockito może użyć innego konstruktora albo wywołać błąd w nieoczywistym momencie.

#### Ręcznie:

```java
@BeforeEach
void setUp() {
    emailService = new EmailService(platform); // jawnie przekazujesz mocka
}
```

- Masz **100% kontroli** — wiadomo, co się dzieje.
- Łatwiej zauważyć błędy przy wstrzykiwaniu niekompletnych/mylących danych.

---

### TL;DR

- `@InjectMocks` **wywołuje konstruktor**, ale **Ty nie decydujesz bezpośrednio, który i jak**.
- Ręczne tworzenie instancji daje **pełną przejrzystość** — szczególnie ważne, jeśli konstruktor robi coś nietrywialnego.
- W testach, gdzie ważna jest precyzja i jawność logiki, warto tworzyć instancje samodzielnie.

---

**User:**

ok. Czy @InjectMocks poradzi sobie w sytuacji gdy mamy więcej mocków adnotowanych przez  @Mock ale tego samego typu? Skąd wiadomo który mock wstrzyknąć w które miejsce klasy testowanej?

---

**Assistant:**

Świetne pytanie — dotykasz jednej z **istotnych słabości `@InjectMocks`**. Odpowiedź w skrócie brzmi:

> **Nie, `@InjectMocks` nie poradzi sobie dobrze, gdy masz wiele mocków tego samego typu** — Mockito nie wie, który mock przypisać do którego pola.

---

### Dlaczego?

Mockito, gdy wstrzykuje zależności za pomocą `@InjectMocks`, **dopasowuje mocki na podstawie typu**, a nie na podstawie nazwy zmiennej czy kolejności.

#### Przykład:

```java
class EmailService {
    private final DeliveryPlatform primaryPlatform;
    private final DeliveryPlatform fallbackPlatform;

    public EmailService(DeliveryPlatform primaryPlatform, DeliveryPlatform fallbackPlatform) {
        this.primaryPlatform = primaryPlatform;
        this.fallbackPlatform = fallbackPlatform;
    }
}
```

Test:

```java
@ExtendWith(MockitoExtension.class)
class EmailServiceTest {

    @Mock
    DeliveryPlatform platform1;

    @Mock
    DeliveryPlatform platform2;

    @InjectMocks
    EmailService emailService;
}
```

W tym przypadku Mockito **nie wie**, czy `platform1` ma być `primaryPlatform`, czy `fallbackPlatform` — więc może:
- **wyrzucić wyjątek** (jeśli nie umie jednoznacznie przypisać),
- **wstrzyknąć przypadkowo** któryś z mocków dwa razy (to się zdarza!),
- **zignorować** jeden z mocków i wstrzyknąć `null`.

---

### Rozwiązania tego problemu

#### ✅ **1. Ręczne tworzenie instancji (zalecane w tym przypadku)**

```java
@BeforeEach
void setUp() {
    emailService = new EmailService(platform1, platform2);
}
```

Masz pełną kontrolę i jasność.

---

#### ⚠️ **2. Własne nazewnictwo i użycie `@Named` – ale nie w czystym Mockito**

Jeśli korzystasz z frameworka DI (jak Spring, CDI itp.), możesz rozróżnić zależności np. po nazwie/kwalifikatorze (`@Qualifier`, `@Named`). Mockito **samo z siebie tego nie obsługuje**.

---

#### 🔍 **3. Unikaj `@InjectMocks`, gdy masz kilka zależności tego samego typu**

To naprawdę ważna zasada. `@InjectMocks` działa dobrze tylko wtedy, gdy zależności różnią się typami.

---

### Podsumowanie

- `@InjectMocks` dopasowuje mocki **tylko po typie**, nie po nazwie.
- Gdy masz **więcej niż jeden mock tego samego typu**, Mockito **nie wie, który gdzie wstrzyknąć**.
- **Najlepsze rozwiązanie** w takiej sytuacji: **stwórz obiekt testowany ręcznie**, jawnie przekazując mocki.
- `@InjectMocks` jest wygodne, ale **ma ograniczenia** — i to jest jedno z nich.