# Apache Kafka vs Amazon SQS — poznaj SQS z perspektywy Kafki

## Krótkie podsumowanie
Apache Kafka to rozproszony log zdarzeń (event streaming platform), w którym wiadomości są persystowane i odczytywane przez przesuwanie offsetu. **Amazon SQS (Simple Queue Service)** to w pełni zarządzana (fully managed) usługa kolejkowa w AWS, w której wiadomości są jednorazowo konsumowane i usuwane po potwierdzeniu przetworzenia. Kafka to „dziennik zdarzeń, z którego można czytać wiele razy", SQS to „skrzynka zadań, z której wyciągasz wiadomość i ona znika".

## Dlaczego to ma znaczenie?
Jeśli znasz Kafkę, łatwo zakładać, że każdy system do przesyłania wiadomości działa tak samo. SQS **nie jest Kafką w chmurze** — to zupełnie inna filozofia:
*   **Kafka** = log zdarzeń, replay, consumer groups, partycje, offset management.
*   **SQS** = prosta kolejka zadań, zero infrastruktury do zarządzania, wiadomość znika po przetworzeniu.

Zrozumienie tych różnic pozwala wybrać właściwe narzędzie: Kafkę do event streamingu, SQS do prostego kolejkowania zadań w ekosystemie AWS.

## Amazon SQS — co to jest i jak działa?

SQS to **w pełni zarządzana usługa AWS** — nie trzeba stawiać klastra, konfigurować replikacji ani martwić się o dostępność. AWS gwarantuje, że SQS jest zawsze dostępny (99.9% SLA) i automatycznie skaluje się do dowolnej liczby wiadomości.

### Dwa typy kolejek SQS

| Cecha | **Standard Queue** | **FIFO Queue** |
|---|---|---|
| **Kolejność** | Best-effort (przybliżona) | Ścisła kolejność (FIFO) |
| **Duplikaty** | Możliwe (at-least-once) | Wykluczone (exactly-once) |
| **Przepustowość** | Niemal nieograniczona | Do 3 000 msg/s (z batchingiem do 30 000) |
| **Nazwa kolejki** | Dowolna | Musi kończyć się `.fifo` |

> W Kafce kolejność jest gwarantowana w ramach partycji. W SQS Standard **kolejność nie jest gwarantowana w ogóle** — wiadomości mogą przychodzić w innej kolejności niż zostały wysłane. Jeśli potrzebujesz kolejności, musisz użyć **FIFO Queue**, ale tracisz na przepustowości.

### Cykl życia wiadomości w SQS

```
Producer → SQS Queue → Consumer pobiera (ReceiveMessage)
                            │
                            ▼
                   Wiadomość staje się NIEWIDOCZNA
                   (Visibility Timeout — domyślnie 30s)
                            │
                   ┌────────┴────────┐
                   │                 │
              Consumer wysyła    Timeout mija
              DeleteMessage      → wiadomość wraca
              → wiadomość        do kolejki (retry)
              usunięta na zawsze
```

**Kluczowe pojęcia:**

*   **Visibility Timeout** — po pobraniu wiadomości przez consumera jest ona niewidoczna dla innych consumerów przez ustalony czas (domyślnie 30s). Jeśli consumer nie wyśle `DeleteMessage` w tym czasie, wiadomość wraca do kolejki i inny consumer może ją pobrać. W Kafce nie ma takiego mechanizmu — offset jest commitowany ręcznie lub automatycznie.
*   **Retention Period** — jak długo wiadomość czeka w kolejce, jeśli nikt jej nie przetworzy (domyślnie 4 dni, maks. 14 dni). W Kafce retention dotyczy logu i jest niezależne od tego, czy ktoś przeczytał wiadomość.
*   **Dead Letter Queue (DLQ)** — po kilku nieudanych próbach przetworzenia (konfigurowalna wartość `maxReceiveCount`), wiadomość jest automatycznie przenoszona do osobnej kolejki DLQ. W Kafce DLQ trzeba implementować ręcznie.
*   **Long Polling** — consumer może czekać do 20s na nowe wiadomości zamiast natychmiast otrzymywać pusty wynik. Zmniejsza liczbę pustych odpowiedzi i koszty. W Kafce consumer robi `poll()` z timeout — koncepcyjnie podobne.

### Przykład: wysyłanie i odbiór w SQS (Python + boto3)

```python
import boto3
import json

sqs = boto3.client("sqs", region_name="eu-central-1")
queue_url = "https://sqs.eu-central-1.amazonaws.com/123456789/orders-queue"

# Wysłanie wiadomości (odpowiednik Kafka Producer)
sqs.send_message(
    QueueUrl=queue_url,
    MessageBody=json.dumps({"order_id": 1234, "status": "created"}),
    MessageAttributes={
        "EventType": {"StringValue": "OrderCreated", "DataType": "String"}
    }
)

# Odbiór wiadomości (odpowiednik Kafka Consumer)
response = sqs.receive_message(
    QueueUrl=queue_url,
    MaxNumberOfMessages=10,      # maks. 10 na raz (w Kafce: poll() zwraca setki/tysiące)
    WaitTimeSeconds=20,          # long polling
    MessageAttributeNames=["All"]
)

for msg in response.get("Messages", []):
    order = json.loads(msg["Body"])
    print(f"Przetwarzam zamówienie: {order['order_id']}")

    # Potwierdzenie przetworzenia — odpowiednik commitowania offsetu
    sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=msg["ReceiptHandle"]  # unikalny identyfikator pobrania
    )
```

> **ReceiptHandle** to unikalny identyfikator konkretnego pobrania wiadomości (nie samej wiadomości). Każde pobranie generuje nowy ReceiptHandle. W Kafce nie ma takiego mechanizmu — consumer po prostu commituje offset.

## Kluczowe różnice — tabela porównawcza

| Cecha | **Apache Kafka** | **Amazon SQS** |
|---|---|---|
| **Model** | Rozproszony log (pull, offset-based) | Kolejka wiadomości (pull, delete-based) |
| **Zarządzanie** | Self-managed lub Confluent Cloud / MSK | Fully managed (serverless) |
| **Wiadomość po odczycie** | Pozostaje (przesuwasz offset) | Staje się niewidoczna → usuwana po `DeleteMessage` |
| **Replay zdarzeń** | ✅ Natywny (seek to offset) | ❌ Brak — usunięta wiadomość jest utracona |
| **Consumer Groups** | ✅ Natywne (podział partycji) | ❌ Brak — ale każdy consumer pobiera niezależnie |
| **Kolejność** | Gwarantowana w partycji | Standard: brak gwarancji / FIFO: gwarantowana |
| **Duplikaty** | At-least-once (domyślnie) | Standard: at-least-once / FIFO: exactly-once |
| **Przepustowość** | Miliony msg/s | Standard: niemal nieograniczona / FIFO: ~3 000 msg/s |
| **Retencja** | Konfigurowalna (domyślnie 7 dni, do ∞) | Maks. 14 dni |
| **Dead Letter Queue** | Ręczna implementacja | ✅ Wbudowana konfiguracja |
| **Partycjonowanie** | ✅ Natywne (klucz partycji) | ❌ Brak (FIFO ma Message Group ID — koncepcyjnie podobne) |
| **Rozmiar wiadomości** | Domyślnie 1 MB (konfigurowalny) | Maks. 256 KB (większe → S3 + wskaźnik) |
| **Protokół** | Własny binarny (TCP) | HTTPS (REST API) |
| **Koszt** | Infrastruktura (serwery, dyski, ludzie) | Pay-per-use (za liczbę żądań) |
| **Złożoność operacyjna** | Wysoka (ZooKeeper/KRaft, replikacja, monitoring) | Zerowa (serverless) |
| **Ekosystem** | Kafka Streams, Connect, ksqlDB | Lambda, SNS, EventBridge, Step Functions |

## Czego NIE ma SQS (a Kafka ma)?

### 1. Brak replay / brak logu
W Kafce możesz cofnąć offset i ponownie przeczytać historyczne zdarzenia — np. przy naprawie buga albo rebuilding stanu. W SQS **po usunięciu wiadomości nie ma do niej powrotu**. Jeśli potrzebujesz replay, SQS to złe narzędzie.

### 2. Brak consumer groups
W Kafce consumer group automatycznie dzieli partycje między członków grupy. W SQS **każda wiadomość trafia do jednego consumera** (kto pierwszy ten lepszy, z wykorzystaniem visibility timeout), ale nie ma mechanizmu koordynacji. Wielu consumerów po prostu „rywalizuje" o wiadomości z tej samej kolejki.

### 3. Brak natywnego partycjonowania
Kafka dzieli topik na partycje, co umożliwia równoległe przetwarzanie z zachowaniem kolejności per klucz. SQS FIFO ma **Message Group ID**, który działa koncepcyjnie podobnie — wiadomości z tym samym Group ID są dostarczane w kolejności i przetwarzane sekwencyjnie.

### 4. Brak ekosystemu stream processing
Kafka ma Kafka Streams, ksqlDB, Kafka Connect — cały ekosystem do przetwarzania strumieniowego. SQS to „głupia rura" — dostarcza wiadomości i tyle. Logikę przetwarzania budujesz w Lambda, ECS, lub innej usłudze.

## Czego NIE ma Kafka (a SQS ma)?

### 1. Zero zarządzania infrastrukturą
SQS to usługa serverless. Nie stawiasz klastra, nie monitorujesz brokerów, nie konfigurujesz replikacji. Tworzysz kolejkę jednym kliknięciem (lub linią Terraform) i działa.

### 2. Natywne DLQ
SQS ma wbudowaną konfigurację Dead Letter Queue — ustawiasz `maxReceiveCount` i po N nieudanych próbach wiadomość automatycznie trafia do kolejki DLQ. W Kafce musisz sam implementować logikę przekierowywania na osobny topik.

**Co oznacza „nieudana próba"?** SQS **nie wie**, czy consumer przetworzył wiadomość poprawnie czy z błędem. Kolejka nie ma żadnej informacji o logice biznesowej consumera. Mechanizm jest prostszy — SQS liczy, ile razy wiadomość została **pobrana** (pole `ApproximateReceiveCount`). „Nieudana próba" to sytuacja, w której consumer pobrał wiadomość (`ReceiveMessage`), ale **nie wywołał `DeleteMessage` przed upływem Visibility Timeout**. Wtedy wiadomość wraca do kolejki, a jej `ReceiveCount` rośnie o 1. Gdy `ReceiveCount` przekroczy `maxReceiveCount`, SQS automatycznie przenosi wiadomość do DLQ.

```
Consumer pobiera wiadomość (ReceiveCount = 1)
    │
    ├── ✅ Sukces → consumer wywołuje DeleteMessage → wiadomość usunięta
    │
    └── ❌ Błąd / crash / timeout → brak DeleteMessage
            → Visibility Timeout mija
            → wiadomość wraca do kolejki (ReceiveCount = 2)
            → kolejny consumer pobiera (ReceiveCount = 3)
            → ...
            → ReceiveCount > maxReceiveCount → wiadomość → DLQ
```

Innymi słowy: z perspektywy SQS **brak potwierdzenia usunięcia = nieudana próba**. Consumer, który poprawnie przetworzył wiadomość, ale zapomniał wywołać `DeleteMessage`, spowoduje „nieudaną próbę" — mimo że przetworzenie się udało.

### 3. Natywna integracja z ekosystemem AWS
SQS jest idealnie zintegrowany z innymi usługami AWS:
*   **Lambda** — SQS może automatycznie triggerować funkcję Lambda (event source mapping).
*   **SNS** — wzorzec fan-out: jeden topic SNS → wiele kolejek SQS.
*   **Step Functions** — orchestracja workflowów z SQS jako źródłem zdarzeń.
*   **EventBridge** — routing zdarzeń do SQS na podstawie reguł.

### 4. Model cenowy pay-per-use
Kafka wymaga stałej infrastruktury (serwery, dyski, sieć) niezależnie od obciążenia. SQS kosztuje tyle, ile go używasz — przy niskim ruchu koszty są bliskie zeru.

## Wzorzec: SNS + SQS = fan-out (odpowiednik Kafka consumer groups)

W Kafce, aby wielu konsumentów odczytywało te same dane niezależnie, używasz **consumer groups**. W AWS odpowiednikiem jest wzorzec **SNS → SQS fan-out**:

```
Producer → SNS Topic: "order-events"
                ├── SQS Queue: billing-queue    → Lambda: processPayment
                ├── SQS Queue: warehouse-queue  → Lambda: reserveStock
                └── SQS Queue: analytics-queue  → Lambda: updateDashboard
```

Każda kolejka SQS subskrybuje ten sam topic SNS i otrzymuje kopię każdej wiadomości. Każda kolejka przetwarza niezależnie — dokładnie jak różne consumer groups w Kafce.

> **SNS (Simple Notification Service)** to usługa pub/sub w AWS. SNS sam nie buforuje wiadomości — dostarcza je natychmiast do subskrybentów. W połączeniu z SQS tworzy wzorzec, w którym SNS rozgłasza, a SQS buforuje i zapewnia niezawodne dostarczenie.

## Drzewo decyzyjne: Kafka vs SQS

```
Czy potrzebujesz replay zdarzeń (cofanie offsetu, odtwarzanie stanu)?
├── TAK → Kafka ✅
└── NIE
    └── Czy potrzebujesz, aby wielu niezależnych konsumentów czytało te same dane?
        ├── TAK → Kafka ✅  (lub SNS+SQS fan-out, jeśli jesteś w AWS)
        └── NIE
            └── Czy potrzebujesz przetwarzania strumieniowego (joiny, agregacje, windowing)?
                ├── TAK → Kafka + Kafka Streams ✅
                └── NIE
                    └── Czy jesteś w ekosystemie AWS i chcesz zero zarządzania?
                        ├── TAK → SQS ✅
                        └── NIE
                            └── Czy przepustowość > 100k msg/s jest krytyczna?
                                ├── TAK → Kafka ✅
                                └── NIE → SQS (lub RabbitMQ, jeśli nie AWS)
```

## Kiedy SQS jest lepszym wyborem niż Kafka?

| Scenariusz | Dlaczego SQS wygrywa |
|---|---|
| Prosty task queue (procesowanie zamówień, emaile) | Zero infrastruktury, DLQ out-of-the-box |
| Lambda-driven architektura | Natywna integracja event source mapping |
| Niski / zmienny ruch (0–1000 msg/s) | Pay-per-use, brak kosztu idle |
| Mały zespół bez DevOps | Brak konieczności zarządzania klastrem |
| Buffering między serwisami (decoupling) | Prosta kolejka z retry i DLQ |
| Szybkie prototypowanie w AWS | Kolejka gotowa w 30 sekund |

## Kiedy Kafka jest lepszym wyborem niż SQS?

| Scenariusz | Dlaczego Kafka wygrywa |
|---|---|
| Event sourcing / CQRS | Replay zdarzeń od dowolnego offsetu |
| Stream processing (agregacje, joiny) | Kafka Streams / Flink / ksqlDB |
| Wielu konsumentów tych samych danych | Consumer groups + niezależne offsety |
| Ultra-wysoka przepustowość (miliony msg/s) | Sekwencyjne I/O, zero-copy, partycjonowanie |
| Długoterminowe przechowywanie zdarzeń | Retention do ∞, tiered storage |
| Audyt / compliance (pełna historia) | Log nie jest modyfikowany, append-only |
| Multi-cloud / on-premise | SQS działa tylko w AWS |

## Częsty błąd: „użyję Kafki zamiast SQS do prostego task queue"

Jeśli Twój use case to:

```
API → wyślij zadanie do kolejki → worker przetwarza → usuń z kolejki
```

…to Kafka jest nadmiarowa. Dostajesz złożoność operacyjną (ZooKeeper/KRaft, monitoring brokerów, zarządzanie partycjami), a nie korzystasz z żadnej unikalnej cechy Kafki (replay, consumer groups, streaming). SQS zrobi to samo za ułamek kosztu i wysiłku.

## Częsty błąd: „użyję SQS do event sourcingu"

Jeśli Twój use case to:

```
Zdarzenie → zapisz w logu → odtwórz stan systemu z historii zdarzeń
```

…to SQS nie nadaje się, bo **wiadomości są usuwane po przetworzeniu**. Nie ma logu, nie ma replay, nie ma pojęcia offsetu. Do event sourcingu potrzebujesz Kafki (lub EventStore, ale to inna historia).

## Powiązane pliki
*   [Kafka vs RabbitMQ vs ActiveMQ — porównanie](kafka-rabbitmq-activemq-redis-pubsub.md)
*   [Kafka Consumer/Producer API vs Kafka Streams](kafka-vs-kafka-streams.md)
*   [Dead Letter Queue](../DevOps/dead-letter-queue.md)
*   [Twierdzenie CAP](cap-theorem.md)
