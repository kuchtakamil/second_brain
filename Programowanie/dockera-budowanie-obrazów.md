# Dockera - budowanie obrazów

**Data:** 2023-05-08

---

**User:**

Znajdź błąd
version: "3.7"

services:
  build-3d-printer-monitor:
    image: 3d-printer-monitor
    build:
      context: .
      dockerfile: Dockerfile

  zookeeper:
    image: docker.io/bitnami/zookeeper:3.8
    networks:
      - kafka-net
    ports:
      - "2181:2181"
    volumes:
      - "zookeeper_data:/bitnami"
    environment:
      - ALLOW_ANONYMOUS_LOGIN=yes
  kafka:
    image: docker.io/bitnami/kafka:3.4
    networks:
      - kafka-net
    ports:
      - "9092:9092"
    volumes:
      - "kafka_data:/bitnami"
    environment:
      - KAFKA_CFG_ZOOKEEPER_CONNECT=zookeeper:2181
      - ALLOW_PLAINTEXT_LISTENER=yes
      - KAFKA_LISTENERS=INTERNAL://:9093,EXTERNAL://:9092
      - KAFKA_LISTENER_SECURITY_PROTOCOL_MAP=INTERNAL:PLAINTEXT,EXTERNAL:PLAINTEXT
      - KAFKA_INTER_BROKER_LISTENER_NAME=INTERNAL
      - KAFKA_ADVERTISED_LISTENERS=INTERNAL://kafka:9093,EXTERNAL://localhost:9092
    depends_on:
      - zookeeper
  akhq:
    container_name: akhq
    image: tchiotludo/akhq:latest
    networks:
      - kafka-net
    ports:
      - "8080:8080"
    environment:
      AKHQ_CONFIGURATION: |
        akhq:
          connections:
            kafka-dev:
              properties:
                bootstrap.servers: "kafka:9093"
    depends_on:
      - kafka

  carriage-speed-simulator:
    image: 3d-printer-monitor
    command: sbt "sensor-simulator / run carriage-speed"
    networks:
      - kafka-net
    depends_on:
      - kafka
  bed-temp-simulator:
    image: 3d-printer-monitor
    command: sbt "sensor-simulator / run bed-temp"
    networks:
      - kafka-net
    depends_on:
      - kafka
  data-consumer:
    image: 3d-printer-monitor
    command: sbt "sensor-simulator / run bed-temp,carriage-speed"
    networks:
      - kafka-net
    depends_on:
      - carriage-speed-simulator
      - bed-temp-simulator

volumes:
  zookeeper_data:
    driver: local
  kafka_data:
    driver: local

networks:
  kafka-net:
    name: kafka-net
    driver: bridge


---

**Assistant:**



Nie ma oczywistych błędów w tym pliku składniowym `docker-compose.yaml`. Jednakże, należy upewnić się, że obrazy `3d-printer-monitor` są poprawnie zbudowane przed uruchomieniem usług w środowisku Dockera.

Można to zrobić, wykonując komendę `docker build` w folderze zawierającym plik `Dockerfile` dla każdego z obrazów, które używane są w pliku `docker-compose.yaml`. Na przykład, dla usługi `build-3d-printer-monitor`, wykonaj:

```
docker build -t 3d-printer-monitor .
```

Warto również upewnić się, że wymagane zależności są zainstalowane, takie jak `sbt`, przed uruchomieniem symulatorów.

---

**User:**

carriage-speed-simulator zwraca błąd No resolvable bootstrap urls given in bootstrap.servers

---

**Assistant:**

Błąd "No resolvable bootstrap urls given in bootstrap.servers" jest związany z konfiguracją klienta Kafka, który próbuje nawiązać połączenie z brokerami Kafka.

Możliwe przyczyny tego błędu to:

1. Nieprawidłowe adresy URL dla brokerów Kafka w konfiguracji klienta. Upewnij się, że adresy URL są poprawnie skonfigurowane, aby odwoływać się do właściwych hostów i portów.

2. Nieprawidłowa nazwa hosta lub adres IP. Sprawdź, czy podana nazwa hosta lub adres IP jest poprawna i dostępna z sieci, na której działa kontener.

Aby rozwiązać ten błąd, możesz spróbować kilku rzeczy:

1. Sprawdź konfigurację klienta Kafka w symulatorze `carriage-speed-simulator` i upewnij się, że właściwe adresy URL brokerów Kafka są skonfigurowane w pliku konfiguracyjnym.

2. Upewnij się, że hosty i porty brokerów Kafka są dostępne z kontenera symulatora `carriage-speed-simulator`. Możesz to sprawdzić, uruchamiając polecenie `ping` lub `telnet` z kontenera do hostów i portów brokerów Kafka.

3. Spróbuj użyć adresów IP zamiast nazw hostów w konfiguracji klienta Kafka, jeśli adresy IP są znane i dostępne.

4. Upewnij się, że usługi `zookeeper` i `kafka` są uruchomione i działają poprawnie w środowisku Dockera. Możesz to sprawdzić, wykonując polecenie `docker-compose ps` i upewniając się, że wszystkie usługi są uruchomione i nie zwracają żadnych błędów.