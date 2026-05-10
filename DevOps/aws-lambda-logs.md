# Wygodne czytanie logów z AWS Lambda

## Czym to jest?
Czytanie logów z usług AWS (takich jak Lambda) wprost z terminala pozwala na szybkie debugowanie bez konieczności ciągłego logowania się do konsoli AWS i nawigowania po CloudWatch Logs. Narzędzie AWS CLI posiada wbudowaną komendę `tail`, która znacznie ułatwia to zadanie.

## Dlaczego jest to ważne?
Podczas wytwarzania i debugowania oprogramowania (np. funkcji Lambda), możliwość śledzenia logów w czasie rzeczywistym znacznie przyspiesza cykl rozwojowy. Zamiast ręcznie odświeżać stronę CloudWatch i klikać w poszczególne strumienie logów (Log Streams), możemy widzieć wszystko z perspektywy konsoli deweloperskiej.

## Analiza polecenia `aws logs tail`

Polecenie podane w przykładzie:
```bash
aws logs tail /aws/lambda/dd-analyze-handler --since 10m --region eu-central
```

Działa to w następujący sposób:
- `aws logs tail`: Wywołanie wbudowanej funkcji AWS CLI do ciągłego odczytu i strumieniowania logów.
- `/aws/lambda/dd-analyze-handler`: Nazwa grupy logów (Log Group) w CloudWatch. W przypadku lambd domyślnie grupa nazywa się `/aws/lambda/<nazwa-funkcji>`.
- `--since 10m`: Pobiera logi wygenerowane tylko z ostatnich 10 minut (można używać np. `1h`, `5s` czy `3d`).
- `--region eu-central`: Wskazuje region (tutaj Frankfurt), w którym stworzone są logi (jeśli nie mamy skonfigurowanego domyślnego regionu lub lambda działa w innym).

Aby śledzić logi "na żywo" w momencie ich wpadania (ang. *follow*), wystarczy dodać flagę `--follow`!
```bash
aws logs tail /aws/lambda/dd-analyze-handler --follow
```

## Inne sposoby na wygodne czytanie logów (Alternatywy)

### 1. Narzędzie AWS SAM CLI (`sam logs`)
Jeśli aplikacja zbudowana jest przy użyciu frameworku Serverless Application Model (SAM), istnieje równie wygodny sposób wbudowany w `sam`:
```bash
sam logs -n dd-analyze-handler --tail
```
Narzędzie to potrafi automatycznie dopasować grupę logów ze zdefiniowanej lambdy, a także samo odświeża i formatuje wyjście.

### 2. Zewnętrzne narzędzie `awslogs`
Zanim polecenie `tail` zostało wdrożone natywnie do AWS CLI, popularnym rozwiązaniem było użycie zewnętrznej biblioteki napisanej w Pythonie - `awslogs`.
Zaletą jest fajne formatowanie i kolorowanie wyjścia terminalowego.
Instalacja: `pip install awslogs`
Wywołanie:
```bash
awslogs get /aws/lambda/dd-analyze-handler ALL --watch
```

### 3. CloudWatch Logs Insights (w konsoli AWS)
Jeśli Twoim celem jest przeanalizowanie dużej bazy błędów, zgrupowanie ich albo wyszukanie specyficznego klucza ze struktury formatowanej jako JSON, znacznie lepszym sposobem pod kątem analitycznym będzie usługa Logs Insights z panelu WWW AWS.

Przykładowe zapytanie wyodrębniające logi z wyrazem "ERROR" z ostatnich wiadomości:
```
fields @timestamp, @message
| filter @message like /ERROR/
| sort @timestamp desc
| limit 20
```

### 4. Filtracja strumienia w `aws logs` (AWS CLI z flagą `--filter-pattern`)
Możesz filtrować wpisy już w samym terminalu za pomocą AWS CLI, tak by wyświetlać np. same błędy:
```bash
aws logs tail /aws/lambda/dd-analyze-handler --filter-pattern "ERROR" --since 1h
```

## Powiązane tematy
- [Rozwiązywanie problemów i przydatne komendy AWS CLI](aws-cli.md)
