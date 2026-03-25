# Na AWS uruchomiłem App Runner z własnym obrazem docker. Czy taka instancja App R

**Data:** 2 sty 2026, 23:52:43 CET

---

**User:**

Na AWS uruchomiłem App Runner z własnym obrazem docker. Czy taka instancja App Runner generuje koszty gdy jest włączona ale nikt nie korzysta z aplikacji?

---

**Gemini:**

Tak, instancja **AWS App Runner** generuje koszty nawet wtedy, gdy nie obsługuje żadnego ruchu (stan idle), o ile usługa nie została jawnie wprowadzona w stan **Paused**.

Model rozliczeniowy App Runnera opiera się na rozróżnieniu dwóch stanów instancji kontenerowych: **Provisioned** oraz **Active**.

### 1. Provisioned Instance (Stan bezczynności)

Gdy Twoja aplikacja nie przetwarza żadnych żądań, instancja znajduje się w stanie "zarezerwowanym" (provisioned). Ma to na celu wyeliminowanie problemu tzw. *cold startu*, znanego z AWS Lambda.

- **Koszt RAM:** Płacisz za zarezerwowaną pamięć RAM przez cały czas, gdy usługa jest uruchomiona.
- **Koszt CPU:** W stanie bezczynności zasoby CPU są drastycznie ograniczane (throttled), a AWS **nie nalicza opłat za vCPU**.
- **Cel:** Utrzymanie instancji "ciepłej", aby mogła natychmiast zareagować na pierwsze przychodzące żądanie.

### 2. Active Instance (Obsługa żądań)

W momencie pojawienia się ruchu, App Runner natychmiast przydziela zasoby procesora, a instancja przechodzi w stan aktywny.

- **Koszt RAM + vCPU:** Płacisz za oba parametry zgodnie z wybraną konfiguracją (`Cpu` i `Memory`).
- **Naliczanie:** Opłata za vCPU jest naliczana od momentu otrzymania pierwszego żądania do momentu, gdy aplikacja zakończy przetwarzanie wszystkich aktywnych requestów (plus krótki czas buforowy po zakończeniu ostatniego żądania).

---

### Porównanie kosztów (Przykładowe stawki w regionie us-east-1)

| Składnik kosztów | Stan: **Provisioned** (Idle) | Stan: **Active** (Processing) |
| --- | --- | --- |
| **vCPU** | $0 (Brak opłat) | $0.064 / vCPU-godzina |
| **Pamięć (RAM)** | $0.007 / GB-godzina | $0.007 / GB-godzina |

### Kluczowe parametry w konfiguracji Auto Scaling

Wpływ na koszty ma Twoja definicja `AutoScalingConfiguration`. Jeśli ustawisz `MinSize` na wartość większą niż 0 (minimum to zazwyczaj 1), zawsze będziesz ponosić koszt co najmniej jednej "zarezerwowanej" instancji (pamięć RAM).

```
# Przykład fragmentu CloudFormation / Terraform dla AutoScalingConfiguration
AutoScalingConfiguration:
  MinSize: 1
  MaxSize: 10
  MaxConcurrency: 100
```

### Strategie optymalizacji kosztów

Jeśli posiadasz środowiska deweloperskie lub testowe, które nie muszą być dostępne 24/7, możesz zredukować koszty do zera za pomocą operacji **Pause** i **Resume**:

- **Pause:** Powoduje całkowite zatrzymanie instancji i wstrzymanie naliczania opłat za vCPU oraz RAM. Aplikacja przestaje jednak odpowiadać (zwraca błąd 404/503).
- **Automatyzacja:** Możesz użyć AWS SDK lub CLI do wywoływania `PauseService` i `ResumeService` zgodnie z harmonogramem (np. przez AWS EventBridge i Lambdę), aby wyłączać serwis na noc lub weekendy.

```
# Wstrzymanie usługi za pomocą AWS CLI
aws apprunner pause-service --service-arn <your-service-arn>

# Wznowienie usługi
aws apprunner resume-service --service-arn <your-service-arn>
```

Podsumowując: w przeciwieństwie do Google Cloud Run (który potrafi skalować się do prawdziwego zera i nie pobierać opłat za RAM w stanie spoczynku), AWS App Runner zawsze pobiera opłatę za pamięć RAM dla minimalnej liczby instancji zdefiniowanej w konfiguracji skalowania, chyba że usługa zostanie ręcznie lub skryptowo zapauzowana.

Czy chciałbyś, abym przygotował przykładowy skrypt w Pythonie (boto3) do automatycznego pauzowania i wznawiania Twojej usługi w określonych godzinach?