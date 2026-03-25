# Docker-compose Kafka network.

**Data:** 2023-05-08

---

**User:**

W jednym docker-compose definiuję kontener z kafka oraz aplikację Java łączącą się z kafka. W jaki sposób mam ustawić network aby kafka była dostępna dla aplikacji

---

**Assistant:**

Aby aplikacja Java była w stanie połączyć się z kontenerem Kafka w Docker Compose, należy skonfigurować odpowiednią sieć. 

Można to zrobić w pliku docker-compose.yml, dodając sekcję "networks" i definiując sieć. Na przykład:

```yaml
version: "3"
services:
  kafka:
    image: <kafka-image>
    ports:
      - "9092:9092"
    networks:
      - kafka-network
  java-app:
    image: <java-app-image>
    networks:
      - kafka-network
networks:
  kafka-network:
```

W tym przykładzie dodajemy sieć o nazwie "kafka-network", a następnie przypisujemy ją do kontenerów Kafka i Java-app. Dzięki temu, kontener Kafka będzie dostępny dla kontenera Java-app pod adresem `kafka:9092`.

Ważne jest również, aby upewnić się, że aplikacja Java jest skonfigurowana do połączenia się z adresem `kafka:9092`. Można to zrobić na przykład w pliku konfiguracyjnym aplikacji lub w kodzie źródłowym, korzystając z odpowiedniego adresu serwera Kafka.