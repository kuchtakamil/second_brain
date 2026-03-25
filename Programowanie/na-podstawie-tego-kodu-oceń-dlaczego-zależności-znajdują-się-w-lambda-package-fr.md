# Na podstawie tego kodu, oceń dlaczego zależności znajdują się w lambda-package.

**Data:** 8 sty 2026, 18:41:29 CET

---

**User:**

Na podstawie tego kodu, oceń dlaczego zależności znajdują się w lambda-package.
Fragment github actions który uruchamia deploy.sh

###
- name: Run Deployment Script
  run: |
    # Set environment variables for the script
    export AWS_ACCOUNT_ID=${{ secrets.AWS_ACCOUNT_ID }}
    export DEFAULT_AWS_REGION=${{ secrets.DEFAULT_AWS_REGION }}
    
    chmod +x scripts/deploy.sh
    ./scripts/deploy.sh ${{ github.event.inputs.environment || 'dev' }}
  env:
    AWS_ROLE_ARN: ${{ secrets.AWS_ROLE_ARN }}
###

Oto deploy.sh
###
#!/bin/bash
set -e

ENVIRONMENT=${1:-dev}          # dev | test | prod
PROJECT_NAME=${2:-twin}

echo "🚀 Deploying ${PROJECT_NAME} to ${ENVIRONMENT}..."

# 1. Build Lambda package
cd "$(dirname "$0")/.."        # project root
echo "📦 Building Lambda package..."
(cd backend && uv run deploy.py)

# 2. Terraform workspace & apply
cd terraform

AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
AWS_REGION=${DEFAULT_AWS_REGION:-us-east-1}
terraform init -input=false \
  -backend-config="bucket=twin-terraform-state-${AWS_ACCOUNT_ID}" \
  -backend-config="key=${ENVIRONMENT}/terraform.tfstate" \
  -backend-config="region=${AWS_REGION}" \
  -backend-config="dynamodb_table=twin-terraform-locks" \
  -backend-config="encrypt=true"

if ! terraform workspace list | grep -q "$ENVIRONMENT"; then
  terraform workspace new "$ENVIRONMENT"
else
  terraform workspace select "$ENVIRONMENT"
fi

# Use prod.tfvars for production environment
if [ "$ENVIRONMENT" = "prod" ]; then
  TF_APPLY_CMD=(terraform apply -var-file=prod.tfvars -var="project_name=$PROJECT_NAME" -var="environment=$ENVIRONMENT" -auto-approve)
else
  TF_APPLY_CMD=(terraform apply -var="project_name=$PROJECT_NAME" -var="environment=$ENVIRONMENT" -auto-approve)
fi

echo "🎯 Applying Terraform..."
"${TF_APPLY_CMD[@]}"

API_URL=$(terraform output -raw api_gateway_url)
FRONTEND_BUCKET=$(terraform output -raw s3_frontend_bucket)
CUSTOM_URL=$(terraform output -raw custom_domain_url 2>/dev/null || true)
###

A to deploy.py
###
import os
import shutil
import zipfile
import subprocess


def main():
    print("Creating Lambda deployment package...")

    # Clean up
    if os.path.exists("lambda-package"):
        shutil.rmtree("lambda-package")
    if os.path.exists("lambda-deployment.zip"):
        os.remove("lambda-deployment.zip")

    # Create package directory
    os.makedirs("lambda-package")

    print("Installing dependencies for Lambda runtime...")

    subprocess.run(
        [
            "docker",
            "run",
            "--rm",
            "-v",
            f"{os.getcwd()}:/var/task",
            "--platform",
            "linux/amd64",  # Force x86_64 architecture
            "--entrypoint",
            "",  # Override the default entrypoint
            "public.ecr.aws/lambda/python:3.13",
            "/bin/sh",
            "-c",
            "pip install --target /var/task/lambda-package -r /var/task/requirements.txt --platform manylinux2014_x86_64 --only-binary=:all: --upgrade",
        ],
        check=True,
    )

    # Copy application files
    print("Copying application files...")
    for file in ["server.py", "lambda_handler.py", "context.py", "resources.py"]:
        if os.path.exists(file):
            shutil.copy2(file, "lambda-package/")

    # Copy data directory
    if os.path.exists("data"):
        shutil.copytree("data", "lambda-package/data")

    # Create zip
    print("Creating zip file...")
    with zipfile.ZipFile("lambda-deployment.zip", "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk("lambda-package"):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, "lambda-package")
                zipf.write(file_path, arcname)

if __name__ == "__main__":
    main()
###

---

**Gemini:**

Z analizy Twojego kodu wynika, że problem nie leży w samym skrypcie `deploy.py` (który generuje paczkę poprawnie), ale w tym, **co Terraform wysyła do AWS**.

Log z Twojego poprzedniego pytania pokazuje, że w katalogu `/var/task` na Lambdzie znajdują się pliki takie jak `deploy.py`, `pyproject.toml` oraz folder `lambda-package`. To dowodzi, że **AWS Lambda nie uruchamia zawartości Twojego ZIP-a, lecz cały folder główny projektu**.

Oto szczegółowa analiza techniczna:

### 1. Przyczyna w `deploy.py`

W skrypcie `deploy.py` używasz flagi `--target /var/task/lambda-package`.

```
# To instaluje biblioteki DO podfolderu lambda-package
"pip install --target /var/task/lambda-package -r /var/task/requirements.txt ..."
```

Następnie kopiujesz tam pliki źródłowe i tworzysz ZIP:

```
# To poprawnie spłaszcza strukturę wewnątrz pliku .zip
with zipfile.ZipFile("lambda-deployment.zip", "w", zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk("lambda-package"):
        arcname = os.path.relpath(file_path, "lambda-package")
        zipf.write(file_path, arcname)
```

**Wniosek:** Skrypt `deploy.py` wykonuje swoją pracę prawidłowo — tworzy plik `lambda-deployment.zip`, w którym `mangum` i `lambda_handler.py` są na najwyższym poziomie.

### 2. Błąd w procesie CI/CD i Terraform

Skoro w logach Lambdy widzisz folder `lambda-package/` oraz pliki `deploy.py` i `requirements.txt`, oznacza to, że Terraform (wywoływany w `deploy.sh`) ignoruje stworzony plik `lambda-deployment.zip` i wysyła cały katalog roboczy.

Prawdopodobnie w Twoim kodzie Terraform (`.tf`) masz coś takiego:

```
# BŁĘDNA KONFIGURACJA (prawdopodobna)
data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../backend" # To pakuje WSZYSTKO, łącznie z artefaktami budowania
  output_path = "${path.module}/lambda.zip"
}

resource "aws_lambda_function" "this" {
  filename = data.archive_file.lambda_zip.output_path
  # ...
}
```

### 3. Dlaczego widnieje błąd `No module named 'mangum'`?

Gdy Lambda otrzymuje cały folder projektu jako kod:

1. Interpreter szuka `lambda_handler.py` w głównym katalogu (znajduje go).
2. Wewnątrz `lambda_handler.py` masz `import mangum`.
3. Interpreter szuka folderu `mangum/` w `/var/task`. Nie ma go tam, bo znajduje się w `/var/task/lambda-package/mangum/`.
4. Błąd zostaje rzucony, mimo że pliki fizycznie tam są.

---

### Rozwiązanie

Musisz zmienić konfigurację Terraform, aby wskazywała bezpośrednio na artefakt stworzony przez `deploy.py`, zamiast tworzyć nowy ZIP z całego folderu.

#### Krok A: Poprawka w Terraform

W pliku `.tf`, gdzie definiujesz funkcję Lambda, ustaw parametr `filename` na ścieżkę do pliku wygenerowanego przez skrypt Python:

```
resource "aws_lambda_function" "this" {
  # Ścieżka do pliku stworzonego przez deploy.py
  filename         = "${path.module}/../backend/lambda-deployment.zip"
  function_name    = "your_function_name"
  handler          = "lambda_handler.lambda_handler" # plik.funkcja
  runtime          = "python3.13"
  source_code_hash = filebase64sha256("${path.module}/../backend/lambda-deployment.zip")
  
  # ... reszta konfiguracji
}
```

#### Krok B: Usunięcie zbędnego pakowania w Terraform

Jeśli masz w Terraform blok `data "archive_file"`, usuń go. Dubluje on pracę wykonaną przez `deploy.py` i robi to błędnie (nie uwzględnia specyfiki instalacji paczek przez Docker/pip).

#### Krok C: Weryfikacja struktury ZIP

Możesz sprawdzić, czy `deploy.py` na pewno działa dobrze, uruchamiając go lokalnie i sprawdzając zawartość:

```
unzip -l backend/lambda-deployment.zip | grep mangum
```

Powinieneś zobaczyć `mangum/` bezpośrednio w spisie plików, bez żadnego prefixu folderowego.

**Czy chciałbyś, abym sprawdził Twój plik `.tf`, aby upewnić się, że ścieżki do `filename` i `source_code_hash` są poprawne?**