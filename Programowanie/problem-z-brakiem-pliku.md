# Problem z brakiem pliku

**Data:** 2026-01-07

---

**User:**

Gdy nie mam pliku lambda-deployment, ten fragment filebase64sha256("${path.module}/../backend/lambda-deployment.zip") wyrzuca błąd .

resource "aws_lambda_function" "api" {
  filename         = "${path.module}/../backend/lambda-deployment.zip"
  function_name    = "${local.name_prefix}-api"
  role             = aws_iam_role.lambda_role.arn
  handler          = "lambda_handler.handler"
  source_code_hash = filebase64sha256("${path.module}/../backend/lambda-deployment.zip")
  runtime          = "python3.13"
  architectures    = ["x86_64"]
  timeout          = var.lambda_timeout
  tags             = local.common_tags
  environment {
    variables = {
      CORS_ORIGINS     = var.use_custom_domain ? "https://${var.root_domain},https://www.${var.root_domain}" : "https://${aws_cloudfront_distribution.main.domain_name}"
      S3_BUCKET        = aws_s3_bucket.memory.id
      USE_S3           = "true"
      BEDROCK_MODEL_ID = var.bedrock_model_id
    }
  }

---

**Assistant:**

To zachowanie jest oczekiwane: `filebase64sha256()` **wymaga istnienia pliku w czasie `terraform plan`**, a nie dopiero przy `apply`. Jeśli plik nie istnieje, Terraform kończy się błędem.

Masz kilka **poprawnych i praktycznych rozwiązań** — wybór zależy od tego, *dlaczego* pliku czasami nie ma.

---

## Opcja 1 (REKOMENDOWANA): `data "archive_file"` zamiast ręcznego ZIP-a

Jeżeli ZIP powstaje z kodu źródłowego Lambdy, **nie trzymaj go jako artefaktu zewnętrznego**.

```hcl
data "archive_file" "lambda" {
  type        = "zip"
  source_dir  = "${path.module}/../backend"
  output_path = "${path.module}/../backend/lambda-deployment.zip"
}

resource "aws_lambda_function" "api" {
  filename         = data.archive_file.lambda.output_path
  source_code_hash = data.archive_file.lambda.output_base64sha256

  function_name = "${local.name_prefix}-api"
  role          = aws_iam_role.lambda_role.arn
  handler       = "lambda_handler.handler"
  runtime       = "python3.13"
  architectures = ["x86_64"]
  timeout       = var.lambda_timeout
  tags          = local.common_tags
}
```

### Dlaczego to najlepsze rozwiązanie
- Terraform **sam gwarantuje istnienie ZIP-a**
- `source_code_hash` zawsze poprawny
- brak błędów przy `plan`
- automatyczny redeploy przy zmianach kodu

To jest **oficjalnie zalecany pattern Terraforma**.

---

## Opcja 2: warunkowe tworzenie Lambdy (gdy ZIP bywa opcjonalny)

Jeśli Lambda **czasami w ogóle nie powinna powstać**, użyj `count` + `fileexists()`:

```hcl
locals {
  lambda_zip = "${path.module}/../backend/lambda-deployment.zip"
}

resource "aws_lambda_function" "api" {
  count = fileexists(local.lambda_zip) ? 1 : 0

  filename         = local.lambda_zip
  source_code_hash = filebase64sha256(local.lambda_zip)

  function_name = "${local.name_prefix}-api"
  role          = aws_iam_role.lambda_role.arn
  handler       = "lambda_handler.handler"
  runtime       = "python3.13"
}
```

⚠️ Wady:
- zasób znika/pojawia się → możliwe destrukcje
- trzeba uważać na referencje (`aws_lambda_function.api[0]`)

---

## Opcja 3: `try()` (działa, ale **niezalecane produkcyjnie**)

```hcl
source_code_hash = try(
  filebase64sha256("${path.module}/../backend/lambda-deployment.zip"),
  null
)
```

### Dlaczego to jest słabe
- Lambda **nie zdeployuje się poprawnie**
- Terraform może nie wykrywać zmian kodu
- łatwo o „silent failure”

Używaj tylko do prototypów.

---

## Opcja 4: ZIP budowany poza Terraformem (CI/CD)

Jeżeli ZIP powstaje np. w pipeline:

- **warunek konieczny**: plik **musi istnieć przed `terraform plan`**
- Terraform **nie nadaje się** do „czekania” na pliki

W takim wypadku:
- build → zip
- dopiero potem `terraform plan/apply`

---

## Rekomendacja końcowa

| Scenariusz | Rozwiązanie |
|----------|------------|
| Kod Lambdy w repo | `archive_file` |
| Lambda opcjonalna | `count + fileexists()` |
| CI/CD build | build **przed** Terraformem |
| Prototyp | `try()` (tymczasowo) |

Jeżeli chcesz, mogę:
- dopasować rozwiązanie do **Twojego pipeline’u**
- pokazać **wzorcową strukturę repo** (Terraform + backend)
- pomóc rozwiązać problem z **Python 3.13 + dependencies** w ZIP-ie

Daj znać, w którym wariancie jesteś.