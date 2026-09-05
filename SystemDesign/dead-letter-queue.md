# Dead Letter Queue (DLQ)

## Czym to jest?

Dead Letter Queue (DLQ), czyli **kolejka martwych wiadomości**, to specjalna kolejka, do której trafiają komunikaty, których system nie potrafił poprawnie przetworzyć po określonej liczbie prób. Zamiast blokować główny przepływ lub tracić wiadomości, infrastruktura automatycznie przenosi je do osobnej kolejki, gdzie czekają na analizę, naprawę i ewentualne ponowne przetworzenie (*redrive*).

Nazwa pochodzi z tradycyjnej poczty — *dead letter office* to biuro, do którego trafiają listy, których nie da się doręczyć (błędny adres, brak odbiorcy). W systemach kolejkowych idea jest identyczna: wiadomość, która wielokrotnie powoduje błąd, zostaje „odłożona na bok", aby nie zatruć reszty strumienia.

## Dlaczego jest to ważne?

W architekturze opartej na kolejkach komunikatów (SQS, RabbitMQ, Kafka) każda wiadomość, której konsument nie potrafi przetworzyć, staje się problemem:

- **Bez DLQ** — wadliwa wiadomość wraca do kolejki, jest pobierana ponownie, znowu powoduje błąd i tak w nieskończoność. To zjawisko nazywa się **poison pill** (zatruta wiadomość). Blokuje konsumenta, marnuje zasoby i opóźnia przetwarzanie poprawnych wiadomości.
- **Z DLQ** — po wyczerpaniu limitu prób (*max receive count*) wiadomość trafia do DLQ. Główna kolejka działa dalej bez przeszkód, a zespół może spokojnie przeanalizować problem.

DLQ chroni system przed:

- **Zablokowaniem głównego strumienia** przez jedną wadliwą wiadomość
- **Nieskończonymi pętlami retry** marnującymi zasoby obliczeniowe
- **Utratą danych** — wiadomość nie jest usuwana, tylko przenoszona
- **Cichymi awariami** — rosnąca DLQ wyzwala alerty i informuje zespół o problemie

## Jak to działa?

### Ogólny mechanizm

```
┌──────────────┐      retry 1, 2, 3...     ┌──────────────┐
│  Główna      │ ──────────────────────────▶│   Konsument  │
│  Kolejka     │                            │   (Worker)   │
└──────┬───────┘                            └──────┬───────┘
       │                                           │
       │  po N nieudanych próbach                  │ błąd!
       │                                           │
       ▼                                           │
┌──────────────┐                                   │
│  Dead Letter  │◀──────────────────────────────────┘
│  Queue (DLQ)  │
└──────────────┘
       │
       ▼
  Analiza → Naprawa → Redrive
```

1. **Producent** wysyła wiadomość do głównej kolejki
2. **Konsument** pobiera wiadomość i próbuje ją przetworzyć
3. Jeśli przetwarzanie się nie powiedzie, wiadomość wraca do kolejki
4. Po przekroczeniu limitu prób (np. 3–5 razy) infrastruktura automatycznie przenosi wiadomość do **DLQ**
5. Zespół analizuje wiadomości w DLQ, naprawia problem (w kodzie lub danych) i uruchamia **redrive** — ponowne przetworzenie

### Powody trafienia wiadomości do DLQ

Wiadomość może trafić do DLQ z wielu powodów:

| Kategoria | Przykłady |
|-----------|-----------|
| **Błędy danych** | Niezgodny schemat, brakujące wymagane pola, niepoprawny format JSON |
| **Błędy biznesowe** | Nieistniejący użytkownik, anulowane zamówienie, przekroczony limit |
| **Błędy infrastrukturalne** | Timeout bazy danych, niedostępna zależność po wyczerpaniu retry |
| **Błędy kodu** | Wyjątek w konsumencie, null pointer, nieobsłużony edge case |
| **Poison pills** | Wiadomość, która z powodu swoich danych *zawsze* powoduje błąd |

## DLQ w konkretnych technologiach

### Amazon SQS

W SQS konfigurujemy DLQ przez **Redrive Policy** na głównej kolejce:

```json
{
  "deadLetterTargetArn": "arn:aws:sqs:eu-central-1:123456789:my-queue-dlq",
  "maxReceiveCount": 5
}
```

- `maxReceiveCount` — liczba nieudanych prób, po których wiadomość trafia do DLQ
- DLQ to zwykła kolejka SQS — można ją monitorować, czytać i przetwarzać jak każdą inną
- AWS udostępnia funkcję **DLQ Redrive** w konsoli — jednym kliknięciem wiadomości wracają do głównej kolejki

### Amazon SNS

SNS może kierować niedostarczone powiadomienia do SQS DLQ, gdy subskrybent (np. Lambda, HTTP endpoint) nie potwierdzi odbioru:

```json
{
  "deadLetterTargetArn": "arn:aws:sqs:eu-central-1:123456789:sns-dlq"
}
```

### AWS Lambda (z SQS jako event source)

Gdy Lambda jest wyzwalana przez SQS i rzuca wyjątek, wiadomość wraca do kolejki. Po `maxReceiveCount` próbach trafia do DLQ. W przypadku asynchronicznych wywołań Lambda można też skonfigurować **on-failure destination** bezpośrednio na funkcji Lambda.

### Apache Kafka

Kafka **nie ma wbudowanego DLQ** — trzeba go zaimplementować samodzielnie. Typowy wzorzec:

```
1. Konsument próbuje przetworzyć rekord z topicu "orders.events"
2. Jeśli przetwarzanie zawiedzie N razy:
   - Publikuje rekord do topicu "orders.events.dlq"
   - Commituje offset oryginalnego rekordu
3. Osobny proces monitoruje topic DLQ
```

Frameworki takie jak **Spring Kafka** oferują gotowe mechanizmy `DefaultErrorHandler` z `DeadLetterPublishingRecoverer`.

### RabbitMQ

RabbitMQ wspiera DLQ natywnie przez **Dead Letter Exchange (DLX)**:

```json
{
  "x-dead-letter-exchange": "dlx.exchange",
  "x-dead-letter-routing-key": "dlq.orders",
  "x-message-ttl": 60000
}
```

Wiadomość trafia do DLX, gdy zostanie odrzucona (`nack` bez requeue), przekroczy TTL lub kolejka osiągnie limit rozmiaru.

## Dobre praktyki

### Projektowanie DLQ

- **Osobna DLQ na przepływ** — nie wrzucaj wszystkich błędnych wiadomości do jednej globalnej DLQ. Oddzielne kolejki DLQ dla zamówień, płatności i powiadomień ułatwiają diagnozę.
- **Zachowuj oryginalne dane** — wiadomość w DLQ powinna zawierać oryginalny payload bez modyfikacji.
- **Dodawaj metadane błędu** — typ wyjątku, czas błędu, liczba prób, nazwa konsumenta, stack trace.
- **Ustaw dłuższy retention** — DLQ powinna przechowywać wiadomości dłużej niż główna kolejka (np. 14 dni zamiast 4).

### Monitoring i alerting

- **Alarm na niepustą DLQ** — każda wiadomość w DLQ to potencjalny problem biznesowy.
- **Metryki**: liczba wiadomości w DLQ, tempo przyrostu, czas przebywania najstarszej wiadomości.
- **Dashboard** — wizualizacja DLQ obok metryk głównej kolejki.

```bash
# Sprawdzenie liczby wiadomości w SQS DLQ
aws sqs get-queue-attributes \
  --queue-url https://sqs.eu-central-1.amazonaws.com/123456789/my-queue-dlq \
  --attribute-names ApproximateNumberOfMessages
```

### Obsługa wiadomości z DLQ

- **Nie ignoruj DLQ** — to nie śmietnik. Jeśli DLQ zawiera zdarzenia płatności lub zamówień, to jest stan biznesowo istotny.
- **Ustal właściciela i SLO** — kto odpowiada za DLQ i w jakim czasie wiadomości muszą być obsłużone.
- **Procedura redrive** — po naprawie problemu przenieś wiadomości z powrotem do głównej kolejki.
- **Rozróżniaj błędy tymczasowe od trwałych** — tymczasowe (timeout) mogą zadziałać po redrive. Trwałe (błędne dane) wymagają naprawy danych lub kodu.

## Typowy scenariusz z AWS

```
1. Producent wrzuca zadania do Amazon SQS
2. Lambda pobiera wiadomości i wywołuje zewnętrzne API
3. API zwraca 500 → Lambda rzuca wyjątek
4. SQS ukrywa wiadomość na 30s (visibility timeout)
5. Po 30s wiadomość wraca → Lambda próbuje ponownie
6. Po 5 nieudanych próbach → wiadomość trafia do DLQ
7. CloudWatch Alarm wykrywa wiadomości w DLQ → powiadomienie na Slacku
8. Zespół naprawia problem → DLQ Redrive → wiadomości wracają do głównej kolejki
```

## Powiązane tematy

- [AWS Step Functions — orkiestracja z wbudowanym Retry/Catch](aws-step-functions.md)
- [AWS Lambda — czytanie logów](aws-lambda-logs.md)
- [Obsługa błędów przy masowych wywołaniach API](../SystemDesign/handling-api-request-failures.md)
- [Kafka, RabbitMQ, ActiveMQ — porównanie systemów kolejkowych](../SystemDesign/kafka-rabbitmq-activemq-redis-pubsub.md)
- [Mikroserwisy — pytania rekrutacyjne (DLQ, backpressure, event-driven)](../SystemDesign/mikroserwisy-pytania-rekrutacyjne.md)
