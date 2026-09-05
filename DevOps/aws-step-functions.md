# AWS Step Functions

## Czym to jest?

AWS Step Functions to w pełni zarządzana usługa orkiestracji, która pozwala koordynować wiele usług AWS w wizualne, powtarzalne przepływy pracy (ang. *workflows*). Zamiast pisać skomplikowaną logikę sterowania w kodzie aplikacji (np. obsługę kolejności kroków, ponawiania, rozgałęzień i obsługi błędów), definiujemy ją deklaratywnie w formacie JSON za pomocą języka **Amazon States Language (ASL)**. Step Functions automatycznie zarządza wykonaniem każdego kroku, śledzi stan i obsługuje awarie.

## Dlaczego jest to ważne?

W architekturze mikroserwisowej i bezserwerowej (serverless) pojedyncze zadanie biznesowe często wymaga skoordynowania wielu niezależnych usług: funkcji Lambda, zapytań do DynamoDB, wywołań API, kolejek SQS czy zadań ECS. Bez orkiestratora programista musi ręcznie implementować:

- **Kolejność wykonywania** — która usługa uruchamia się po której
- **Obsługę błędów i ponawianie** — co się dzieje, gdy jeden krok zawiedzie
- **Logikę warunkową** — różne ścieżki w zależności od wyniku
- **Równoległość** — uruchamianie wielu kroków jednocześnie

Step Functions przejmują całą tę odpowiedzialność, dostarczając gotową, odporną na awarie infrastrukturę orkiestracji.

## Jak to działa?

### Maszyna stanów (State Machine)

Centralnym pojęciem jest **maszyna stanów** — graf opisujący przepływ pracy jako zbiór stanów (kroków) i przejść między nimi. Definiujemy ją w formacie JSON:

```json
{
  "Comment": "Prosty przepływ przetwarzania zamówienia",
  "StartAt": "WalidujZamowienie",
  "States": {
    "WalidujZamowienie": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:eu-central-1:123456789:function:validate-order",
      "Next": "SprawdzDostepnosc"
    },
    "SprawdzDostepnosc": {
      "Type": "Choice",
      "Choices": [
        {
          "Variable": "$.inStock",
          "BooleanEquals": true,
          "Next": "RealizujZamowienie"
        }
      ],
      "Default": "PoinformujOBraku"
    },
    "RealizujZamowienie": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:eu-central-1:123456789:function:fulfill-order",
      "Retry": [
        {
          "ErrorEquals": ["States.TaskFailed"],
          "IntervalSeconds": 3,
          "MaxAttempts": 3,
          "BackoffRate": 2.0
        }
      ],
      "End": true
    },
    "PoinformujOBraku": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:eu-central-1:123456789:function:notify-out-of-stock",
      "End": true
    }
  }
}
```

### Typy stanów

Step Functions oferuje kilka typów stanów, z których każdy pełni inną rolę:

| Typ stanu   | Opis                                                                 |
|-------------|----------------------------------------------------------------------|
| **Task**    | Wykonuje pracę — wywołuje Lambdę, API, usługę AWS (np. DynamoDB)    |
| **Choice**  | Rozgałęzienie warunkowe — odpowiednik `if/else` lub `switch`        |
| **Parallel**| Uruchamia wiele gałęzi równolegle i czeka na zakończenie wszystkich  |
| **Map**     | Iteruje po kolekcji elementów — odpowiednik pętli `for each`        |
| **Wait**    | Zatrzymuje wykonanie na określony czas lub do konkretnego momentu    |
| **Pass**    | Przekazuje dane dalej (przydatne do transformacji lub mockowania)     |
| **Succeed** | Kończy przepływ sukcesem                                            |
| **Fail**    | Kończy przepływ niepowodzeniem z komunikatem błędu                   |

### Dwa tryby wykonywania

1. **Standard Workflows** — przeznaczone do długotrwałych procesów (do 1 roku). Każdy krok jest zapisywany w historii, co zapewnia pełną powtarzalność i audytowalność. Rozliczane per przejście stanu.
2. **Express Workflows** — przeznaczone do krótkotrwałych, intensywnych zadań (do 5 minut). Znacznie tańsze przy dużym wolumenie wywołań, ale bez pełnej historii wykonania. Rozliczane per wywołanie i czas trwania.

## Obsługa błędów

Jedną z najsilniejszych stron Step Functions jest wbudowana obsługa błędów:

```json
{
  "Type": "Task",
  "Resource": "arn:aws:lambda:...:function:process-payment",
  "Retry": [
    {
      "ErrorEquals": ["ServiceUnavailable"],
      "IntervalSeconds": 5,
      "MaxAttempts": 3,
      "BackoffRate": 2.0
    }
  ],
  "Catch": [
    {
      "ErrorEquals": ["States.ALL"],
      "Next": "ObsluzBlad"
    }
  ]
}
```

- **Retry** — automatyczne ponawianie z wykładniczym opóźnieniem (*exponential backoff*)
- **Catch** — przechwytywanie błędów i przekierowanie do stanu obsługi (odpowiednik `try/catch`)

## Typowe przypadki użycia

1. **Przetwarzanie zamówień w e-commerce** — walidacja → płatność → realizacja → wysyłka → powiadomienie
2. **Pipeline ETL / przetwarzanie danych** — pobranie danych → transformacja → załadowanie do bazy/hurtowni
3. **Orkiestracja mikroserwisów** — koordynacja wielu Lambd i usług AWS w jednym procesie biznesowym
4. **Procesy wymagające zatwierdzenia** — krok `Wait` + callback (np. oczekiwanie na akceptację managera)
5. **Przetwarzanie plików multimedialnych** — upload → transkodowanie → analiza AI → zapis wyników

## Step Functions vs inne podejścia

| Cecha                     | Step Functions                      | Łańcuch Lambd (chaining)         | Kolejka SQS + Lambda          |
|---------------------------|-------------------------------------|----------------------------------|-------------------------------|
| Widoczność przepływu      | Wizualny graf w konsoli AWS         | Brak natywnej wizualizacji       | Brak natywnej wizualizacji    |
| Obsługa błędów            | Wbudowana (Retry/Catch)             | Ręczna implementacja             | Dead Letter Queue             |
| Logika warunkowa          | Choice, Parallel, Map               | Ręczna w kodzie                  | Ręczna w kodzie               |
| Śledzenie stanu           | Automatyczne                        | Wymaga zewnętrznego storage'u    | Częściowe (kolejka)           |
| Koszt przy dużym wolumenie| Wyższy (per przejście)              | Niższy                          | Niższy                       |

## Przydatne komendy AWS CLI

Uruchomienie maszyny stanów:
```bash
aws stepfunctions start-execution \
  --state-machine-arn arn:aws:states:eu-central-1:123456789:stateMachine:my-workflow \
  --input '{"orderId": "12345"}'
```

Sprawdzenie statusu wykonania:
```bash
aws stepfunctions describe-execution \
  --execution-arn arn:aws:states:eu-central-1:123456789:execution:my-workflow:exec-id
```

Lista uruchomień:
```bash
aws stepfunctions list-executions \
  --state-machine-arn arn:aws:states:eu-central-1:123456789:stateMachine:my-workflow \
  --status-filter RUNNING
```

## Powiązane tematy

- [AWS Fargate i porównanie z AWS Lambda](aws-fargate.md)
- [Wygodne czytanie logów z AWS Lambda](aws-lambda-logs.md)
- [Przydatne komendy AWS CLI](aws-cli.md)
- [Różnice między AWS ECS a AWS Fargate](czym-rozni-sie-aws-ecs-od-aws-fargate.md)
