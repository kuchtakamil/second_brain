# Kafka vs RabbitMQ vs ActiveMQ — porównanie systemów kolejkowych

## Krótkie podsumowanie
Kafka, RabbitMQ i ActiveMQ to trzy najpopularniejsze systemy do przesyłania wiadomości (messaging), ale różnią się fundamentalnie w architekturze, modelu dostarczania i zastosowaniach. **Apache Kafka** to rozproszony log zdarzeń (event streaming platform), **RabbitMQ** to klasyczny broker wiadomości (message broker) oparty na protokole AMQP, a **ActiveMQ** to tradycyjny broker JMS stworzony w ekosystemie Java. Dodatkowo **Redis Pub/Sub** to lekki mechanizm publikacji/subskrypcji wbudowany w Redis, ale bez gwarancji persystencji ani kolejkowania.

## Dlaczego to ma znaczenie / Kiedy to stosować?
Wybór systemu do przesyłania wiadomości wpływa na:
*   **Niezawodność** — czy wiadomości mogą zostać utracone?
*   **Przepustowość** — ile wiadomości na sekundę system obsłuży?
*   **Kolejność** — czy kolejność zdarzeń jest gwarantowana?
*   **Skalowanie** — czy system będzie działał przy milionach zdarzeń?
*   **Złożoność operacyjną** — jak trudny jest w utrzymaniu?

Źle dobrany system oznacza albo nadmierną złożoność (Kafka do prostych zadań), albo brak skalowalności (Redis Pub/Sub przy krytycznych zdarzeniach).

## Jak działają — kluczowe różnice architektoniczne

### Apache Kafka — rozproszony log zdarzeń

Kafka **nie jest klasyczną kolejką**. To rozproszony, persystentny log (append-only log), w którym wiadomości (rekordy) są zapisywane na dysku i przechowywane przez konfigurowalny czas (retention period — np. 7 dni, miesiąc, lub bezterminowo).

**Kluczowe cechy:**
*   **Topiki i partycje** — wiadomości trafiają do topiców (topics), a topiki dzielą się na partycje (partitions). Partycje zapewniają równoległy odczyt i skalowanie.
*   **Consumer Groups** — konsumenci w tej samej grupie dzielą się partycjami (każda partycja → jeden konsument). Różne grupy czytają te same dane niezależnie.
*   **Wiadomości nie znikają po odczycie** — konsument przesuwa jedynie swój offset. Inny konsument (lub ten sam po restarcie) może przeczytać te same dane od początku.
*   **Kolejność gwarantowana w ramach partycji** (nie globalnie w topiku).
*   **Przepustowość:** Miliony wiadomości/s dzięki sekwencyjnemu I/O na dysku i zero-copy.

```
Producer → [Topic: orders]
               ├── Partition 0 → Consumer A (group: billing)
               ├── Partition 1 → Consumer B (group: billing)
               └── Partition 0 → Consumer X (group: analytics)  ← ta sama partycja, inna grupa
```

**Kiedy używać Kafki:**
*   Event sourcing, CQRS
*   Streaming danych w czasie rzeczywistym (logi, metryki, IoT)
*   Komunikacja między mikroserwisami wymagająca replay zdarzeń
*   Pipeliny ETL (extract-transform-load)
*   Sytuacje, w których wielu konsumentów musi odczytać te same dane

---

### RabbitMQ — klasyczny broker wiadomości (AMQP)

RabbitMQ to broker oparty na protokole **AMQP 0-9-1**. Działa w modelu push — broker aktywnie wysyła wiadomości do konsumentów. Wspiera zaawansowane mechanizmy routingu wiadomości.

**Kluczowe cechy:**
*   **Exchange + Routing Key + Queue** — producent wysyła do exchange'a, a ten na podstawie reguł (binding) kieruje wiadomość do odpowiedniej kolejki.
*   **Typy exchange:** Direct (dokładne dopasowanie klucza), Fanout (broadcast do wszystkich kolejek), Topic (dopasowanie wzorcowe), Headers.
*   **Wiadomość znika po potwierdzeniu (ACK)** — domyślne zachowanie to jednorazowe dostarczenie. Konsument potwierdza odbiór i wiadomość jest usuwana z kolejki.
*   **Kolejność gwarantowana** w ramach pojedynczej kolejki z jednym konsumentem.
*   **Przepustowość:** Tysiące–dziesiątki tysięcy wiadomości/s (znacznie mniej niż Kafka).
*   **Smart broker / dumb consumer** — logika routingu leży po stronie brokera.

```
Producer → [Exchange: order.exchange]
               ├── routing_key=order.created → Queue: billing-queue → Consumer A
               ├── routing_key=order.created → Queue: notification-queue → Consumer B
               └── routing_key=order.cancelled → Queue: refund-queue → Consumer C
```

**Kiedy używać RabbitMQ:**
*   Klasyczny task queue (dystrybucja zadań do workerów)
*   RPC (Request-Reply) między serwisami
*   Skomplikowany routing wiadomości (np. po nagłówkach, wzorcach kluczy)
*   Systemy wymagające priorytetów wiadomości (priority queues)
*   Gdy potrzebujemy potwierdzenia przetworzenia (ACK/NACK) i dead-letter queue

---

### Apache ActiveMQ — broker JMS

ActiveMQ (i nowsza wersja **Artemis**) to broker wiadomości oparty na specyfikacji **JMS (Java Message Service)**. Historycznie dominował w ekosystemie Java/Enterprise.

**Kluczowe cechy:**
*   **Dwa modele dostarczania:** Queue (Point-to-Point — jeden konsument) i Topic (Pub/Sub — wielu subskrybentów).
*   **Wsparcie dla wielu protokołów:** AMQP, STOMP, MQTT, OpenWire.
*   **Transakcje JMS i XA** — wsparcie dla rozproszonych transakcji (two-phase commit), co jest unikalne na tle Kafki i RabbitMQ.
*   **Wolniejszy i mniej skalowalny** niż Kafka i RabbitMQ w architekturach cloud-native.
*   Idealny dla firm już zainwestowanych w stos Java EE.

**Kiedy używać ActiveMQ:**
*   Systemy enterprise oparte na Java EE / Jakarta EE
*   Potrzeba transakcji rozproszonych (XA transactions)
*   Integracja z istniejącą infrastrukturą JMS
*   Projekty legacy wymagające stabilnego, sprawdzonego brokera

## Porównanie w tabeli

| Cecha | **Kafka** | **RabbitMQ** | **ActiveMQ** |
|---|---|---|---|
| **Model** | Rozproszony log (pull) | Broker AMQP (push) | Broker JMS (push) |
| **Persystencja** | Tak (konfigurowalny retention) | Opcjonalna (durable queues) | Opcjonalna (persistent delivery) |
| **Wiadomość po odczycie** | Pozostaje (offset) | Usuwana (po ACK) | Usuwana (po ACK) |
| **Kolejność** | W ramach partycji | W ramach kolejki | W ramach kolejki |
| **Przepustowość** | Miliony msg/s | Dziesiątki tysięcy msg/s | Tysiące msg/s |
| **Routing** | Prosty (topik + partycja) | Zaawansowany (exchange types) | Prosty (queue/topic) |
| **Replay zdarzeń** | ✅ Natywny | ❌ Brak | ❌ Brak |
| **Consumer Groups** | ✅ Natywne | ❌ Ręczna konfiguracja | ❌ Brak |
| **Transakcje XA** | ❌ Brak | ❌ Brak | ✅ Wsparcie JMS/XA |
| **Dead Letter Queue** | ❌ Ręczna implementacja | ✅ Wbudowane | ✅ Wbudowane |
| **Protokół** | Własny (binarny) | AMQP 0-9-1 | OpenWire, AMQP, STOMP, MQTT |
| **Złożoność operacyjna** | Wysoka (ZooKeeper/KRaft) | Średnia | Niska–Średnia |
| **Ekosystem** | JVM, Python, Go, ... | Dowolny język | Głównie Java |

---

## Redis Pub/Sub vs Kafka — kiedy co wybrać?

### Redis Pub/Sub — jak działa

Redis Pub/Sub to mechanizm **fire-and-forget**. Producent publikuje wiadomość na kanale, a Redis natychmiast rozsyła ją do wszystkich aktualnie podłączonych subskrybentów. Wiadomości **nie są nigdzie zapisywane**.

```python
# Publisher
import redis
r = redis.Redis()
r.publish("notifications", "Nowe zamówienie #1234")

# Subscriber (musi być podłączony w momencie publikacji!)
p = r.pubsub()
p.subscribe("notifications")
for message in p.listen():
    print(message)
```

**Kluczowe ograniczenia Redis Pub/Sub:**
*   **Brak persystencji** — jeśli subskrybent nie jest podłączony, wiadomość przepadnie bezpowrotnie.
*   **Brak kolejki** — nie ma bufora, backpressure ani retry.
*   **Brak consumer groups** — wszyscy subskrybenci dostają wszystko (broadcast). Nie można podzielić pracy.
*   **Brak potwierdzenia (ACK)** — nie wiadomo, czy subskrybent przetworzył wiadomość.
*   **Brak replay** — nie można cofnąć się i przeczytać starszych wiadomości.

> **Uwaga:** Redis od wersji 5.0 oferuje **Redis Streams**, które są dużo bliższe Kafce — mają persystencję, consumer groups, ACK i replay. Redis Streams to **zupełnie inny mechanizm** niż Pub/Sub.

### Kiedy Redis Pub/Sub?

| Scenariusz | Dlaczego Pub/Sub wystarczy |
|---|---|
| Powiadomienia w czasie rzeczywistym (WebSocket broadcast) | Utrata jednego powiadomienia nie jest krytyczna |
| Invalidacja cache w wielu instancjach | Jeśli nie dotrze, cache wygaśnie po TTL |
| Chat / Live updates | Wiadomości są efemeryczne, nie wymagają historii |
| Sygnalizacja zdarzeń (eventy UI) | Prosty mechanizm, niska latencja < 1ms |

### Kiedy Kafka zamiast Redis Pub/Sub?

| Scenariusz | Dlaczego Kafka jest konieczna |
|---|---|
| Przetwarzanie zamówień / płatności | Utrata wiadomości = utrata pieniędzy |
| Event sourcing (odtwarzanie stanu) | Potrzebny replay od początku logu |
| Wielu niezależnych konsumentów | Consumer groups + niezależne offsety |
| Pipeline danych (ETL) | Persystencja + gwarancja at-least-once delivery |
| Audyt / compliance | Pełna historia zdarzeń z retencją |
| Backpressure / wolni konsumenci | Kafka buforuje dane; Redis Pub/Sub — nie |

### Reguła kciuka

> **Redis Pub/Sub** → gdy wiadomość jest jak ogłoszenie przez megafon: kto słyszy — słyszy, kto nie — trudno.
>
> **Kafka** → gdy wiadomość jest jak list polecony: musi dotrzeć, musi być potwierdzony, i musi istnieć dowód wysyłki.

## Przykład: system e-commerce

```
[Użytkownik składa zamówienie]
        │
        ▼
   Kafka topic: "orders"            ← krytyczne zdarzenia, persystencja
        ├── Consumer Group: billing  ← przetwarzanie płatności
        ├── Consumer Group: warehouse ← rezerwacja towaru
        └── Consumer Group: analytics ← raportowanie
        
   Redis Pub/Sub: "order-updates"    ← powiadomienia UI w czasie rzeczywistym
        ├── WebSocket server 1       ← broadcast do przeglądarek
        └── WebSocket server 2       ← broadcast do przeglądarek
```

W powyższym przykładzie **Kafka** obsługuje krytyczny przepływ biznesowy (zamówienia), a **Redis Pub/Sub** służy jedynie do powiadomienia frontendów o zmianach stanu — jeśli użytkownik odświeży stronę, i tak pobierze aktualny stan z API.

## Powiązane pliki
*   [Twierdzenie CAP](cap-theorem.md)
*   [SQL vs NoSQL — kryteria wyboru](sql-vs-nosql-criteria.md)
*   [Pytania rekrutacyjne z mikroserwisów](mikroserwisy-pytania-rekrutacyjne.md)
*   [Pytania rekrutacyjne z System Design](system-design-pytania-rekrutacyjne.md)
