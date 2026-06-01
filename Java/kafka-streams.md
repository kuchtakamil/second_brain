User: Czy różnica między Azure EventHub a Apache Kafka jest duża?
Model: # Azure Event Hubs vs Apache Kafka

## Krótka odpowiedź
Różnica **nie jest duża** pod względem koncepcji i API – Event Hubs celowo oferuje **kompatybilność z protokołem Kafka**.

---

## Porównanie

| Cecha | Azure Event Hubs | Apache Kafka |
|-------|-----------------|--------------|
| **Typ** | Managed SaaS (Azure) | Open-source, self-hosted lub managed |
| **Protokół** | AMQP, HTTP, **Kafka Protocol** | Kafka Protocol |
| **Partycje** | do 32 (Basic/Standard), więcej w Premium/Dedicated | Praktycznie nieograniczone |
| **Retencja** | max 90 dni | Konfigurowalna (nawet nieskończona) |
| **Zarządzanie** | W pełni zarządzany przez Azure | Wymaga administracji (ZooKeeper/KRaft) |
| **Skalowanie** | Automatyczne (Throughput Units) | Ręczne dodawanie brokerów |
| **Consumer Groups** | ✅ | ✅ |
| **Schema Registry** | ✅ (wbudowany) | Oddzielny (Confluent SR) |

---

## Kompatybilność z Kafka

```
# Aplikacja Kafka może połączyć się z Event Hubs
# zmieniając tylko konfigurację!

bootstrap.servers=your-namespace.servicebus.windows.net:9093
security.protocol=SASL_SSL
sasl.mechanism=PLAIN
```

✅ Działa z Kafka SDK  
✅ Kafka Streams (częściowo)  
✅ Kafka Connect  

---

## Główne różnice praktyczne

### 🔴 Czego brakuje w Event Hubs
- Brak **Kafka Transactions**
- Brak **log compaction**
- Brak pełnej swobody konfiguracji brokerów
- Mniejsza liczba partycji w niższych tierach
- Wyższe koszty przy dużym ruchu

### 🟢 Przewagi Event Hubs
- **Zero ops** – brak zarządzania infrastrukturą
- Natywna integracja z Azure (Stream Analytics, Functions, etc.)
- **Automatyczne skalowanie**
- SLA gwarantowane przez Microsoft

---

## Kiedy co wybrać?

```
Jeśli używasz Azure i chcesz prostoty → Event Hubs
Jeśli potrzebujesz pełnej kontroli/funkcji → Apache Kafka
Jeśli masz już kod Kafka → Event Hubs zadziała bez dużych zmian
```

---

## Podsumowanie

> Dla większości przypadków użycia (event streaming, telemetria, logi) **różnica jest minimalna**. Problemy pojawiają się przy zaawansowanych funkcjach Kafki (transakcje, log compaction) lub bardzo dużej skali z ograniczonym budżetem.
User: Napisz podstawy użycia i wykorzystania Apache Kafka Streams
Model: # Apache Kafka Streams – Podstawy

## Czym jest Kafka Streams?

**Kafka Streams** to biblioteka Java/Scala do przetwarzania strumieniowego danych **bezpośrednio w aplikacji** – bez potrzeby osobnego klastra (jak Spark czy Flink).

```
Kafka Topic (input) → [Kafka Streams App] → Kafka Topic (output)
```

---

## Setup – Maven

```xml
<dependencies>
    <dependency>
        <groupId>org.apache.kafka</groupId>
        <artifactId>kafka-streams</artifactId>
        <version>3.6.0</version>
    </dependency>
    
    <!-- Serdes dla JSON (opcjonalnie) -->
    <dependency>
        <groupId>com.fasterxml.jackson.core</groupId>
        <artifactId>jackson-databind</artifactId>
        <version>2.15.0</version>
    </dependency>
</dependencies>
```

---

## Konfiguracja podstawowa

```java
Properties props = new Properties();

// Wymagane
props.put(StreamsConfig.APPLICATION_ID_CONFIG, "moja-aplikacja");
props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");

// Serializacja/Deserializacja
props.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, 
          Serdes.String().getClass());
props.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG, 
          Serdes.String().getClass());

// Opcjonalne
props.put(StreamsConfig.NUM_STREAM_THREADS_CONFIG, 2);
props.put(StreamsConfig.REPLICATION_FACTOR_CONFIG, 1);
```

---

## Dwa API

```
┌─────────────────────────────────────────┐
│           Kafka Streams API             │
├─────────────────┬───────────────────────┤
│   DSL (wysoki   │  Processor API        │
│   poziom)       │  (niski poziom)       │
│                 │                       │
│  map, filter,   │  Pełna kontrola       │
│  groupBy, join  │  nad przetwarzaniem   │
└─────────────────┴───────────────────────┘
```

---

## DSL API – Przykłady

### 1. Hello World – Filtrowanie i transformacja

```java
StreamsBuilder builder = new StreamsBuilder();

// Czytaj z topicu "input-topic"
KStream<String, String> stream = builder.stream("input-topic");

stream
    .filter((key, value) -> value != null && !value.isEmpty())
    .mapValues(value -> value.toUpperCase())
    .to("output-topic");  // Zapisz do topicu

// Uruchom
KafkaStreams streams = new KafkaStreams(builder.build(), props);
streams.start();

// Graceful shutdown
Runtime.getRuntime().addShutdownHook(
    new Thread(streams::close)
);
```

---

### 2. Operacje na KStream

```java
KStream<String, String> stream = builder.stream("orders");

// MAP – zmień klucz i wartość
KStream<String, String> mapped = stream
    .map((key, value) -> KeyValue.pair(
        value.toUpperCase(),    // nowy klucz
        "processed:" + value    // nowa wartość
    ));

// MAP VALUES – zmień tylko wartość
KStream<String, Integer> lengths = stream
    .mapValues(value -> value.length());

// FILTER
KStream<String, String> filtered = stream
    .filter((key, value) -> value.startsWith("URGENT"));

// FILTER NOT
KStream<String, String> withoutNulls = stream
    .filterNot((key, value) -> value == null);

// PEEK – podgląd bez modyfikacji (np. logowanie)
stream.peek((key, value) -> 
    System.out.println("Key: " + key + ", Value: " + value));

// BRANCH – rozdziel strumień
Map<String, KStream<String, String>> branches = stream
    .split(Named.as("branch-"))
    .branch((key, value) -> value.contains("ERROR"), 
             Branched.as("errors"))
    .branch((key, value) -> value.contains("WARN"),  
             Branched.as("warnings"))
    .defaultBranch(Branched.as("info"));

branches.get("branch-errors").to("error-topic");
branches.get("branch-warnings").to("warning-topic");
branches.get("branch-info").to("info-topic");
```

---

### 3. Agregacje – Zliczanie słów (Word Count)

```java
StreamsBuilder builder = new StreamsBuilder();

KStream<String, String> textStream = builder.stream("text-input");

KTable<String, Long> wordCounts = textStream
    .flatMapValues(value -> 
        Arrays.asList(value.toLowerCase().split("\\W+")))
    .groupBy((key, word) -> word)           // Grupuj po słowie
    .count(Materialized.as("word-count-store")); // Policz

// Zapisz wyniki
wordCounts
    .toStream()
    .to("word-count-output", 
        Produced.with(Serdes.String(), Serdes.Long()));
```

---

### 4. KStream vs KTable

```java
// KStream – każda wiadomość to nowe zdarzenie (append-only)
KStream<String, String> stream = builder.stream("events");
// [A=1, B=2, A=3] → przetwarza WSZYSTKIE trzy rekordy

// KTable – ostatnia wartość dla klucza (jak tabela w DB)
KTable<String, String> table = builder.table("users");
// [A=Jan, B=Anna, A=Janusz] → A=Janusz (ostatnia wartość)

// Zamiana
KTable<String, Long> tableFromStream = stream
    .groupByKey()
    .count();

KStream<String, String> streamFromTable = table.toStream();
```

---

### 5. Windowing – Okna czasowe

```java
KStream<String, String> events = builder.stream("events");

// TUMBLING WINDOW – nienachodzone okna co 1 minutę
events
    .groupByKey()
    .windowedBy(TimeWindows.ofSizeWithNoGrace(Duration.ofMinutes(1)))
    .count()
    .toStream()
    .map((windowedKey, count) -> KeyValue.pair(
        windowedKey.key() + "@" + windowedKey.window().start(),
        count
    ))
    .to("windowed-counts");

// HOPPING WINDOW – okno 5 min, przesuwa się co 1 min
events
    .groupByKey()
    .windowedBy(
        TimeWindows.ofSizeAndGrace(
            Duration.ofMinutes(5),   // rozmiar okna
            Duration.ofSeconds(30)   // grace period
        ).advanceBy(Duration.ofMinutes(1))  // hop
    )
    .count();

// SESSION WINDOW – grupuje po aktywności użytkownika
events
    .groupByKey()
    .windowedBy(SessionWindows.ofInactivityGapWithNoGrace(
        Duration.ofMinutes(5)  // nieaktywność = koniec sesji
    ))
    .count();
```

---

### 6. Joins – Łączenie strumieni

```java
KStream<String, String> orders = builder.stream("orders");
KStream<String, String> payments = builder.stream("payments");
KTable<String, String> customers = builder.table("customers");

// STREAM-STREAM JOIN (okno czasowe wymagane)
JoinWindows joinWindow = JoinWindows.ofTimeDifferenceWithNoGrace(
    Duration.ofMinutes(5)
);

KStream<String, String> orderWithPayment = orders.join(
    payments,
    (orderValue, paymentValue) -> 
        "Order: " + orderValue + ", Payment: " + paymentValue,
    joinWindow
);

// STREAM-TABLE JOIN (bez okna czasowego)
KStream<String, String> enrichedOrders = orders.join(
    customers,
    (orderValue, customerValue) -> 
        "Order: " + orderValue + " by " + customerValue
);

// LEFT JOIN – zachowaj order nawet bez płatności
KStream<String, String> allOrders = orders.leftJoin(
    payments,
    (orderValue, paymentValue) ->
        paymentValue != null 
            ? "Paid: " + orderValue 
            : "Unpaid: " + orderValue,
    joinWindow
);
```

---

## State Store – Stan lokalny

```java
// Tworzenie store'a
StoreBuilder<KeyValueStore<String, Long>> storeBuilder =
    Stores.keyValueStoreBuilder(
        Stores.persistentKeyValueStore("my-store"),
        Serdes.String(),
        Serdes.Long()
    );

builder.addStateStore(storeBuilder);

// Użycie w Processor API
stream.process(() -> new Processor<String, String, String, String>() {
    private KeyValueStore<String, Long> store;

    @Override
    public void init(ProcessorContext<String, String> context) {
        store = context.getStateStore("my-store");
    }

    @Override
    public void process(Record<String, String> record) {
        Long current = store.get(record.key());
        long newCount = (current == null ? 0L : current) + 1;
        store.put(record.key(), newCount);
        
        context().forward(record.withValue(
            "Count: " + newCount
        ));
    }
}, "my-store");

// Odpytywanie store'a z zewnątrz (Interactive Queries)
ReadOnlyKeyValueStore<String, Long> queryStore = streams
    .store(StoreQueryParameters.fromNameAndType(
        "my-store",
        QueryableStoreTypes.keyValueStore()
    ));

Long count = queryStore.get("someKey");
```

---

## Processor API – Pełna kontrola

```java
Topology topology = new Topology();

topology
    .addSource("Source", "input-topic")
    .addProcessor("MyProcessor", MyProcessor::new, "Source")
    .addSink("Sink", "output-topic", "MyProcessor");

class MyProcessor implements Processor<String, String, String, String> {
    private ProcessorContext<String, String> context;

    @Override
    public void init(ProcessorContext<String, String> context) {
        this.context = context;
        // Harmonogram – co 1000ms
        context.schedule(
            Duration.ofMillis(1000),
            PunctuationType.WALL_CLOCK_TIME,
            timestamp -> System.out.println("Tick: " + timestamp)
        );
    }

    @Override
    public void process(Record<String, String> record) {
        String processed = record.value().toUpperCase();
        context.forward(record.withValue(processed));
    }

    @Override
    public void close() {
        // Cleanup
    }
}
```

---

## Error Handling

```java
// Handler dla błędów deserializacji
props.put(
    StreamsConfig.DEFAULT_DESERIALIZATION_EXCEPTION_HANDLER_CLASS_CONFIG,
    LogAndContinueExceptionHandler.class  // lub LogAndFailExceptionHandler
);

// Custom handler
class MyExceptionHandler implements DeserializationExceptionHandler {
    @Override
    public DeserializationHandlerResponse handle(
            ProcessorContext context,
            ConsumerRecord<byte[], byte[]> record,
            Exception exception) {
        
        System.err.println("Błąd deserializacji: " + exception.getMessage());
        return DeserializationHandlerResponse.CONTINUE; // lub FAIL
    }
}

// Handler dla błędów produkcji
props.put(
    StreamsConfig.DEFAULT_PRODUCTION_EXCEPTION_HANDLER_CLASS_CONFIG,
    DefaultProductionExceptionHandler.class
);
```

---

## Monitorowanie stanu aplikacji

```java
KafkaStreams streams = new KafkaStreams(builder.build(), props);

// Listener zmian stanu
streams.setStateListener((newState, oldState) -> {
    System.out.println(oldState + " → " + newState);
    
    if (newState == KafkaStreams.State.ERROR) {
        System.err.println("Aplikacja w stanie błędu!");
        // alert, restart, etc.
    }
});

// Handler nieprzechwyconych wyjątków
streams.setUncaughtExceptionHandler(exception -> {
    System.err.println("Nieoczekiwany błąd: " + exception);
    return StreamThreadExceptionResponse.REPLACE_THREAD; // lub SHUTDOWN
});

streams.start();

// Sprawdź metryki
Map<MetricName, ? extends Metric> metrics = streams.metrics();
metrics.forEach((name, metric) -> 
    System.out.println(name.name() + ": " + metric.metricValue())
);
```

---

## Topologia – Wizualizacja

```java
Topology topology = builder.build();

// Wydrukuj topologię (debugging)
System.out.println(topology.describe());

/*
Output:
Topologies:
   Sub-topology: 0
    Source: KSTREAM-SOURCE-0000 (topics: [input-topic])
      --> KSTREAM-FILTER-0001
    Processor: KSTREAM-FILTER-0001 (stores: [])
      --> KSTREAM-SINK-0002
    Sink: KSTREAM-SINK-0002 (topic: output-topic)
*/
```

---

## Kompletny przykład – Pipeline zamówień

```java
public class OrderProcessingApp {

    public static void main(String[] args) {
        Properties props = buildConfig();
        StreamsBuilder builder = new StreamsBuilder();

        // Topiki wejściowe
        KStream<String, String> orders = builder.stream("orders");
        KTable<String, String> customers = builder.table("customers");

        // Pipeline
        orders
            .filter((id, order) -> order != null)
            .peek((id, order) -> System.out.println("New order: " + id))
            // Wzbogać o dane klienta
            .join(customers,
                (order, customer) -> order + "|customer:" + customer)
            // Rozdziel na pilne i zwykłe
            .split(Named.as("priority-"))
            .branch(
                (id, order) -> order.contains("URGENT"),
                Branched.withConsumer(s -> s.to("urgent-orders"))
            )
            .defaultBranch(
                Branched.withConsumer(s -> s.to("normal-orders"))
            );

        // Statystyki co minutę
        orders
            .groupBy((id, order) -> 
                order.split(":")[0])  // grupuj po typie
            .windowedBy(
                TimeWindows.ofSizeWithNoGrace(Duration.ofMinutes(1)))
            .count()
            .toStream()
            .mapValues(count -> "Count: " + count)
            .to("order-stats");

        KafkaStreams streams = new KafkaStreams(builder.build(), props);
        streams.start();

        Runtime.getRuntime().addShutdownHook(
            new Thread(() -> streams.close(Duration.ofSeconds(10)))
        );
    }

    private static Properties buildConfig() {
        Properties props = new Properties();
        props.put(APPLICATION_ID_CONFIG, "order-processor");
        props.put(BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
        props.put(DEFAULT_KEY_SERDE_CLASS_CONFIG, 
                  Serdes.String().getClass());
        props.put(DEFAULT_VALUE_SERDE_CLASS_CONFIG, 
                  Serdes.String().getClass());
        return props;
    }
}
```

---

## Podsumowanie

```
┌──────────────────────────────────────────────┐
│           Kiedy używać Kafka Streams?        │
├──────────────────────────────────────────────┤
│ ✅ Przetwarzanie w czasie rzeczywistym       │
│ ✅ Transformacje i agregacje na topicach     │
│ ✅ Join między różnymi strumieniam           │
│ ✅ Aplikacje stateful (liczniki, sesje)      │
│ ✅ Nie chcesz osobnego klastra (Spark/Flink) │
├──────────────────────────────────────────────┤
│ ❌ Batch processing (użyj Spark)             │
│ ❌ Bardzo złożone ML pipeline'y             │
│ ❌ Źródła inne niż Kafka                    │
└──────────────────────────────────────────────┘
```