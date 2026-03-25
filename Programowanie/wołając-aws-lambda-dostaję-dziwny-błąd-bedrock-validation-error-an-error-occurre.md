# Wołając AWS Lambda dostaję dziwny błąd Bedrock validation error: An error  occur

**Data:** 13 sty 2026, 17:33:58 CET

---

**User:**

Wołając AWS Lambda dostaję dziwny błąd
Bedrock validation error: An error
 occurred (ValidationException) when calling the Converse operation: 
Invocation of model ID amazon.nova-micro-v1:0 with on-demand throughput 
isn’t supported. Retry your request with the ID or ARN of an inference 
profile that contains this model.

Dziwne jest to też że w kodzie mam że chcę korzystać z  nova-lite a nie micro.

---

**Gemini:**

Ten błąd jest specyficzny dla nowych modeli z rodziny **AWS Nova**. Wskazuje on na dwa niezależne problemy: problem logiczny w Twoim kodzie/wdrożeniu (dlaczego `micro` a nie `lite`) oraz problem z samą konstrukcją zapytania do Bedrock API (wymóg Inference Profile).

Poniżej znajduje się szczegółowa analiza techniczna i rozwiązanie.

### 1. Dlaczego błąd dotyczy `nova-micro` zamiast `nova-lite`?

Skoro w kodzie masz `nova-lite`, a błąd zwraca `nova-micro`, przyczyna leży zazwyczaj w warstwie konfiguracyjnej Lambdy, a nie w samym pliku źródłowym. Sprawdź kolejno:

- **Environment Variables (Zmienne środowiskowe):** To najczęstsza przyczyna. Jeśli w kodzie używasz konstrukcji typu `os.environ.get('MODEL_ID', 'amazon.nova-lite-v1:0')`, a w konfiguracji Lambdy w konsoli AWS zmienna `MODEL_ID` jest ustawiona na `amazon.nova-micro-v1:0`, to zmienna środowiskowa zawsze nadpisze wartość domyślną z kodu.
- **Stale Deployment (Nieaktualne wdrożenie):** Jeśli używasz IaC (Terraform, CDK, SAM) lub edytora online, upewnij się, że przycisk **Deploy** został kliknięty lub `terraform apply` przeszedł sukcesem. Lambda może wykonywać starą wersję kodu, w której testowałeś model Micro.
- **Lambda Aliases/Versions:** Upewnij się, że wywołujesz wersję `$LATEST` lub alias, który wskazuje na nową wersję kodu. Często zdarza się, że API Gateway lub Event Source triggeruje starszą, "zapieczętowaną" wersję funkcji.

### 2. Rozwiązanie błędu `ValidationException` (Inference Profile)

Modele Amazon Nova (Micro, Lite, Pro) wymuszają korzystanie z tzw. **System-defined Inference Profiles**. W przeciwieństwie do modeli Claude czy Titan, nie można ich wywoływać, podając jedynie bazowe `modelId` (np. `amazon.nova-lite-v1:0`) w trybie on-demand.

Musisz użyć identyfikatora profilu wnioskowania, który zawiera prefiks regionu (cross-region inference).

**Błędny ID:**
`amazon.nova-lite-v1:0`

**Poprawny ID (przykład dla regionu US):**
`us.amazon.nova-lite-v1:0`

AWS automatycznie przekierowuje ruch w obrębie strefy US (np. us-east-1, us-east-2, us-west-2), aby zapewnić wyższą przepustowość i dostępność.

### Poprawiona implementacja (Python/Boto3)

Poniżej znajduje się kod, który rozwiązuje problem formatowania ID oraz dodaje logowanie, abyś miał pewność, jaki model jest faktycznie wywoływany.

```
import boto3
import json
import os
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    bedrock = boto3.client(service_name='bedrock-runtime')

    # 1. Correct Model ID specifically for Nova family
    # Nova requires the region prefix (System-defined inference profile)
    # Valid examples: 'us.amazon.nova-lite-v1:0', 'eu.amazon.nova-lite-v1:0'
    model_id = os.environ.get('MODEL_ID', 'us.amazon.nova-lite-v1:0')
    
    print(f"DEBUG: Attempting to invoke model: {model_id}")

    # 2. Nova message structure (Converse API is recommended)
    messages = [{
        "role": "user",
        "content": [{"text": "Explain quantum mechanics in one sentence."}]
    }]

    # 3. Inference Configuration
    inference_config = {
        "maxTokens": 512,
        "temperature": 0.7,
        "topP": 0.9
    }

    try:
        response = bedrock.converse(
            modelId=model_id,
            messages=messages,
            inferenceConfig=inference_config
        )
        
        output_text = response['output']['message']['content'][0]['text']
        return {
            'statusCode': 200,
            'body': json.dumps({'response': output_text})
        }

    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        print(f"ERROR: {error_code} - {error_message}")
        
        return {
            'statusCode': 500,
            'body': json.dumps({'error': error_message, 'attempted_model': model_id})
        }
```

### Lista poprawnych ID dla modeli Nova (Inference Profiles)

Musisz wybrać ID zgodne z regionem, w którym znajduje się Twoja Lambda (lub najbliższym dostępnym regionem wnioskowania):

| Model | Region US (Cross-region) | Region EU (Cross-region) |
| --- | --- | --- |
| **Nova Micro** | `us.amazon.nova-micro-v1:0` | `eu.amazon.nova-micro-v1:0` |
| **Nova Lite** | `us.amazon.nova-lite-v1:0` | `eu.amazon.nova-lite-v1:0` |
| **Nova Pro** | `us.amazon.nova-pro-v1:0` | `eu.amazon.nova-pro-v1:0` |

### Co musisz zrobić teraz?

1. Zmień wartość `modelId` w kodzie (lub zmiennej środowiskowej) na `us.amazon.nova-lite-v1:0` (lub `eu...`).
2. Zweryfikuj w konsoli AWS w zakładce **Configuration -> Environment variables** swojej Lambdy, czy nie masz tam ustawionego starego `amazon.nova-micro-v1:0`.