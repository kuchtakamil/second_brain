# Kafka: Tryb "exactly once"

**Data:** 2024-06-07

---

**User:**

Jakie ustawienie Kafki sprawi że będzie ona działać w trybie excactly once

---

**Assistant:**

Aby Kafka działała w trybie "exactly once", konieczne jest skonfigurowanie kilku ustawień zarówno na poziomie brokera, jak i producenta i konsumenta. Oto kroki, które należy wykonać:

### Ustawienia brokera:
1. **transaction.state.log.replication.factor**
   - Ustaw na wartość większą niż 1, zwykle 3. To zapewnia replikację logów transakcyjnych.
   - Przykład: `transaction.state.log.replication.factor=3`

2. **transaction.state.log.min.isr**
   - Ustaw na wartość większą niż 1, zwykle 2. To zapewnia, że co najmniej 2 replikowane logi transakcyjne są dostępne przed zakończeniem zapisu.
   - Przykład: `transaction.state.log.min.isr=2`

### Ustawienia producenta:
1. **enable.idempotence**
   - Musi być ustawione na `true`. To zapewnia, że każdy rekord jest zapisany dokładnie raz.
   - Przykład: `enable.idempotence=true`

2. **acks**
   - Ustaw na `all`. To zapewnia, że lider czeka na potwierdzenia od wszystkich replik.
   - Przykład: `acks=all`

3. **retries**
   - Ustaw na wysoką wartość (np. `Integer.MAX_VALUE`). To zapewnia, że producent będzie ponawiał wysyłkę w razie potrzeby.
   - Przykład: `retries=Integer.MAX_VALUE`

4. **max.in.flight.requests.per.connection**
   - Ustaw na 5 lub mniej. To ogranicza liczbę nierozstrzygniętych zapytań, które mogą być w drodze do tego samego brokera.
   - Przykład: `max.in.flight.requests.per.connection=5`

5. **transactional.id**
   - Ustaw unikalny identyfikator transakcji dla każdego producenta. To identyfikuje sesję transakcyjną producenta.
   - Przykład: `transactional.id=my-transactional-id`

### Ustawienia konsumenta:
1. **isolation.level**
   - Ustaw na `read_committed`. To zapewnia, że konsument widzi tylko zatwierdzone transakcje.
   - Przykład: `isolation.level=read_committed`

### Konfiguracja transakcji:
1. Producent musi używać metod transakcyjnych do rozpoczęcia, zatwierdzenia i wycofania transakcji.
   - `producer.initTransactions()`
   - `producer.beginTransaction()`
   - `producer.sendOffsetsToTransaction(...)`
   - `producer.commitTransaction()`
   - `producer.abortTransaction()`

### Przykładowa konfiguracja:

#### Broker:
```plaintext
transaction.state.log.replication.factor=3
transaction.state.log.min.isr=2
```

#### Producent:
```java
Properties props = new Properties();
props.put("bootstrap.servers", "localhost:9092");
props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer");
props.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer");
props.put("acks", "all");
props.put("enable.idempotence", "true");
props.put("retries", Integer.MAX_VALUE);
props.put("max.in.flight.requests.per.connection", 5);
props.put("transactional.id", "my-transactional-id");

KafkaProducer<String, String> producer = new KafkaProducer<>(props);
producer.initTransactions();
```

#### Konsument:
```java
Properties props = new Properties();
props.put("bootstrap.servers", "localhost:9092");
props.put("group.id", "my-group-id");
props.put("key.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
props.put("value.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
props.put("isolation.level", "read_committed");

KafkaConsumer<String, String> consumer = new KafkaConsumer<>(props);
```

Dzięki tym ustawieniom i konfiguracjom, Kafka będzie działać w trybie "exactly once".

---

**User:**

Jakie ustawienia dla at least once

---

**Assistant:**

Aby Kafka działała w trybie "at least once", należy skonfigurować producenta i konsumenta tak, aby zapewnić, że każdy rekord zostanie przetworzony co najmniej raz. Oto odpowiednie ustawienia:

### Ustawienia producenta:

1. **acks**
   - Ustaw na `all` lub `1`. `all` oznacza, że lider czeka na potwierdzenia od wszystkich replik, natomiast `1` oznacza, że lider czeka tylko na swoje własne potwierdzenie.
   - Przykład: `acks=all` lub `acks=1`

2. **retries**
   - Ustaw na wartość większą niż 0, aby producent ponawiał próby wysłania w razie błędów tymczasowych.
   - Przykład: `retries=5`

3. **enable.idempotence**
   - Może być ustawione na `false`. W trybie "at least once" idempotencja nie jest wymagana.
   - Przykład: `enable.idempotence=false`

### Ustawienia konsumenta:

1. **enable.auto.commit**
   - Ustaw na `false`. Konsument powinien ręcznie potwierdzać przetworzenie wiadomości po jej przetworzeniu.
   - Przykład: `enable.auto.commit=false`

2. **auto.offset.reset**
   - Ustaw na `earliest` lub `latest` w zależności od tego, czy chcesz rozpocząć konsumpcję od początku czy od końca, gdy nie ma zapisanych offsetów.
   - Przykład: `auto.offset.reset=earliest`

3. **max.poll.records**
   - Ustaw na odpowiednią wartość, aby kontrolować, ile rekordów jest przetwarzanych na raz.
   - Przykład: `max.poll.records=500`

### Przykładowa konfiguracja:

#### Producent:
```java
Properties props = new Properties();
props.put("bootstrap.servers", "localhost:9092");
props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer");
props.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer");
props.put("acks", "all");
props.put("retries", 5);
props.put("enable.idempotence", "false");

KafkaProducer<String, String> producer = new KafkaProducer<>(props);
```

#### Konsument:
```java
Properties props = new Properties();
props.put("bootstrap.servers", "localhost:9092");
props.put("group.id", "my-group-id");
props.put("key.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
props.put("value.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
props.put("enable.auto.commit", "false");
props.put("auto.offset.reset", "earliest");
props.put("max.poll.records", "500");

KafkaConsumer<String, String> consumer = new KafkaConsumer<>(props);

// Konsumpcja wiadomości
while (true) {
    ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(100));
    for (ConsumerRecord<String, String> record : records) {
        // Przetwarzanie wiadomości
        System.out.printf("offset = %d, key = %s, value = %s%n", record.offset(), record.key(), record.value());
        
        // Ręczne potwierdzenie offsetu po przetworzeniu wiadomości
        consumer.commitSync(Collections.singletonMap(new TopicPartition(record.topic(), record.partition()), new OffsetAndMetadata(record.offset() + 1)));
    }
}
```

### Podsumowanie:
- **Producent**: Włączenie odpowiednich potwierdzeń (`acks=all` lub `acks=1`) i ponawiania wysyłki (`retries=5`).
- **Konsument**: Wyłączenie automatycznego potwierdzania (`enable.auto.commit=false`) i ręczne potwierdzanie przetworzonych wiadomości (`commitSync`).

Konfiguracja tych ustawień zapewni, że każdy rekord zostanie przetworzony co najmniej raz, nawet w przypadku błędów.