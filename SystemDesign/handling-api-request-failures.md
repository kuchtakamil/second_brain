# Obsługa błędów przy masowych wywołaniach API (Rozwiązania Infrastrukturalne)

Gdy mamy do uruchomienia bardzo dużą liczbę wywołań API w chmurze (np. miliony requestów do zewnętrznego systemu, przetwarzanie webhooków, synchronizacja danych), proste skrypty lub synchroniczne wywołania w pętli szybko stają się niewydajne i podatne na błędy. Pojedynczy błąd sieci, rate-limiting (przekroczenie limitów zapytań) czy tymczasowa niedostępność serwisu mogą przerwać cały proces.

Aby zarządzać failami w sposób **infrastrukturalny** (zdejmując ciężar z kodu samej aplikacji), stosuje się sprawdzone wzorce i usługi chmurowe.

## Najważniejsze mechanizmy infrastrukturalne

### 1. Kolejki Komunikatów (Message Queues)
Podstawowym rozwiązaniem jest zastosowanie architektury asynchronicznej opartej o kolejki, np. **Amazon SQS**, **RabbitMQ** czy **Google Cloud Pub/Sub**.

- **Jak to działa:** Zamiast wywoływać API bezpośrednio, Twój system wysyła "zadanie" (komunikat) do kolejki. Następnie "workery" (np. instancje EC2, kontenery Kubernetes, AWS Lambda) pobierają komunikaty z kolejki w swoim własnym tempie i wykonują właściwy request API.
- **Zalety:** Jeśli worker napotka błąd (np. API zwróci kod 500 lub timeout), po prostu nie potwierdza (nie "ackuje") przetworzenia komunikatu. Komunikat po pewnym czasie wraca do kolejki i może zostać pobrany ponownie przez ten sam lub inny worker.

### 2. Dead Letter Queue (DLQ)
Kolejka "martwych listów" to specjalna kolejka, do której trafiają komunikaty, których nie udało się przetworzyć po określonej liczbie prób (tzw. *max receive count*).

- **Jak to działa:** Jeśli request API failuje np. 5 razy z rzędu dla konkretnego zadania, infrastruktura kolejki automatycznie przenosi ten komunikat z kolejki głównej do DLQ.
- **Zalety:** Chroni to system przed tzw. *poison pills* (komunikatami, które z powodu złych danych zawsze powodują błąd). Komunikaty w DLQ mogą wyzwolić alert do zespołu wsparcia. Programiści mogą je później przeanalizować, naprawić błąd (w danych lub w kodzie API) i "odtworzyć" (redrive) z powrotem do głównej kolejki.

### 3. Automatyczne ponawianie (Retry) z Exponential Backoff i Jitter
Wiele usług chmurowych wspiera automatyczne ponawianie żądań bez konieczności pisania mechanizmów `try-catch` w kodzie aplikacyjnym.

- **Exponential Backoff:** Zamiast ponawiać request natychmiast, mechanizm czeka coraz dłużej po każdym błędzie (np. 1s, 2s, 4s, 8s). Zapobiega to ostatecznemu "zabiciu" API, które właśnie podnosi się po awarii.
- **Jitter:** Dodanie losowego czasu do opóźnienia. Zapobiega to sytuacji, w której tysiące workerów zsynchronizują się i po np. 4 sekundach jednocześnie uderzą w API, znów powodując jego przeciążenie (tzw. Thundering Herd problem).
- Usługi takie jak **AWS EventBridge**, **Step Functions** czy **Pub/Sub** wspierają to natywnie z poziomu konfiguracji.

### 4. Circuit Breaker (Bezpiecznik)
Jeśli zewnętrzne API całkowicie padło, ciągłe ponawianie prób przez tysiące workerów tylko marnuje Twoje zasoby i pieniądze w chmurze.

- **Jak to działa:** Narzędzia takie jak Service Mesh (np. **Istio** w Kubernetes) czy **API Gateway** potrafią wykryć, że dany endpoint seryjnie zwraca błędy (np. 10 błędów w ciągu minuty). Wtedy "otwierają obwód" (Circuit Breaker otwiera się) i natychmiast odrzucają kolejne requesty kierowane do tego API, dając mu czas na odpoczynek. Po pewnym czasie obwód staje się "półotwarty" (przepuszcza testowy request), by sprawdzić, czy API już wstało.

### 5. Orkiestracja zadań (np. AWS Step Functions, Temporal)
Dla bardziej złożonych procesów, gdzie wywołanie API to tylko jeden z wielu kroków, korzysta się z narzędzi do orkiestracji.

- **Jak to działa:** Np. w AWS Step Functions definicję procesu trzymasz w JSON/YAML. Możesz tam zadeklarować infrastrukturze: "Wykonaj ten kod. Jeśli złapiesz błąd `TooManyRequestsException`, poczekaj 10 sekund i spróbuj ponownie. Po 3 próbach przejdź do kroku powiadomienia na Slacku".
- **Zalety:** Rozdzielasz logikę biznesową od obsługi przepływu (flow control). Stan procesu pamiętany jest na poziomie infrastruktury, dzięki czemu procesy mogą trwać nawet miesiącami.

## Podsumowanie: Typowy Flow (Przykład z AWS)

1. **Producent** wrzuca 1 milion zadań do **Amazon SQS**.
2. **Workery (AWS Lambda)** skalują się i masowo uderzają do zewnętrznego API.
3. API nie wytrzymuje obciążenia i zaczyna rzucać błędami `429 Too Many Requests`.
4. Funkcje Lambda rzucają wyjątek, infrastruktura Lambda go przechwytuje i przerywa zadanie.
5. SQS ukrywa te nieudane komunikaty na 30 sekund (*visibility timeout*), pozwalając API odetchnąć.
6. Po 30 sekundach wiadomości wracają i workery próbują ponownie (Retry).
7. Dla pechowych zadań, które sfaulowały np. 5 razy z rzędu, SQS przesuwa je do **Dead Letter Queue (DLQ)**.
8. Gdy coś trafi na DLQ, odpala się **CloudWatch Alarm**, który budzi zespół.
9. Rano wchodzisz do konsoli, jednym guzikiem włączasz "DLQ Redrive", a odłożone wiadomości z DLQ wracają do głównej kolejki by po cichu się przetworzyć.
