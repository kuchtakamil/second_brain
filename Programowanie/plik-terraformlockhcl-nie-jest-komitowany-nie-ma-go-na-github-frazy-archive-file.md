# plik .terraform.lock.hcl nie jest komitowany. Nie ma go na github. Frazy archive

**Data:** 8 sty 2026, 21:09:41 CET

---

**User:**

plik .terraform.lock.hcl nie jest komitowany. Nie ma go na github.
Frazy archive_file też nigdzie nie ma. Jedynie w pliku terraform.tfstate na S3 jest wpis o archive_file

---

**Gemini:**

To, że wpis o `archive_file` znajduje się w pliku stanu (`.tfstate`), jest bezpośrednią przyczyną Twojego błędu. Terraform podczas inicjalizacji i planowania odczytuje plik stanu, widzi w nim zasoby lub źródła danych (data sources) powiązane z providerem `archive` i próbuje pobrać jego schemat, aby wiedzieć, jak je obsłużyć.

Skoro usunąłeś kod, ale dane w stanie zostały, musisz "wyczyścić" stan z tych nieistniejących odniesień.

### 1. Dlaczego `archive_file` jest w stanie?

Nawet jeśli `archive_file` było używane jako `data source`, Terraform przechowuje wynik tego zapytania w stanie, aby optymalizować kolejne uruchomienia. Dopóki nie powiesz Terraformowi, że ma "zapomnieć" o tym obiekcie, będzie on szukał providera `archive`.

### 2. Rozwiązanie: Usunięcie obiektu ze stanu

Musisz usunąć konkretne wpisy dotyczące `archive_file` z pliku stanu za pomocą CLI. **Nie edytuj pliku `.tfstate` ręcznie na S3.**

Wykonaj poniższe kroki (najlepiej lokalnie, mając dostęp do tego samego backendu S3):

1. **Zainicjalizuj backend** (jeśli jeszcze tego nie zrobiłeś lokalnie):
   Upewnij się, że masz skonfigurowane dane uwierzytelniające AWS, a następnie wykonaj `terraform init` z takimi samymi parametrami `-backend-config`, jakich używa GitHub Actions.
2. **Wyświetl listę obiektów w stanie**:

   ```
   terraform state list
   ```

   Poszukaj linii zaczynającej się od `data.archive_file.<nazwa>`.
3. **Usuń problematyczny obiekt ze stanu**:

   ```
   # Przykład: jeśli w liście widnieje data.archive_file.lambda_zip
   terraform state rm data.archive_file.lambda_zip
   ```

   To polecenie usunie metadane dotyczące pakowania z pliku `terraform.tfstate` na S3. Jest to operacja bezpieczna, ponieważ `data source` nie reprezentuje fizycznego zasobu w AWS, który mógłby zostać "osierocony".

### 3. Alternatywa: Jeśli nie masz dostępu lokalnego

Jeśli musisz to zrobić przez GitHub Actions, możesz dodać tymczasowy krok w workflow przed `terraform apply`:

```
- name: Force remove archive_file from state
  run: |
    terraform state rm data.archive_file.your_data_source_name || true
  working-directory: ./terraform
```

*(Zamień `your_data_source_name` na nazwę, którą miałeś wcześniej w kodzie).*

### 4. Weryfikacja zasobu Lambda w `.tf`

Po usunięciu obiektu ze stanu, upewnij się, że Twój zasób `aws_lambda_function` nie odwołuje się już do żadnej zmiennej pochodzącej z `archive_file`.

**Błędny kod (powodujący błąd):**

```
resource "aws_lambda_function" "this" {
  filename         = data.archive_file.lambda_zip.output_path # <-- TO USUNĄŁEŚ, WIĘC TU BĘDZIE BŁĄD
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  # ...
}
```

**Poprawny kod (współpracujący z Twoim `deploy.py`):**

```
resource "aws_lambda_function" "this" {
  # Ścieżka do pliku ZIP wygenerowanego przez Twój skrypt Python
  filename         = "${path.module}/../backend/lambda-deployment.zip"
  source_code_hash = filebase64sha256("${path.module}/../backend/lambda-deployment.zip")
  
  handler = "lambda_handler.lambda_handler"
  runtime = "python3.13"
  # ...
}
```

### 5. Finalna inicjalizacja

Po wykonaniu `terraform state rm`, usuń folder `.terraform` i wykonaj ponownie `terraform init`. Terraform nie powinien już prosić o providera `archive`, ponieważ w grafie zależności (zarówno w kodzie `.tf`, jak i w pliku `.tfstate`) nie będzie już po nim śladu.

Czy po usunięciu obiektu ze stanu i zmianie ścieżek w `aws_lambda_function` na bezpośredni plik ZIP, `terraform plan` przechodzi poprawnie?