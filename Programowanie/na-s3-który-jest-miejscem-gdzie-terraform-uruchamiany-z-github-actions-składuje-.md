# Na S3 który jest miejscem gdzie terraform uruchamiany z github actions składuje

**Data:** 8 sty 2026, 21:00:52 CET

---

**User:**

Na S3 który jest miejscem gdzie terraform uruchamiany z github actions składuje pliki, znajduje się plik terraform.tfstate. Czy mogę go bezpiecznie usunąć?

---

**Gemini:**

**Nie, nie możesz bezpiecznie usunąć pliku `terraform.tfstate`**, jeśli Twoja infrastruktura (Lambda, role IAM, API Gateway itd.) już istnieje w AWS. Usunięcie tego pliku jest jedną z najbardziej destrukcyjnych czynności w pracy z Terraformem.

### Dlaczego nie wolno usuwać `terraform.tfstate`?

Plik stanu jest jedynym "źródłem prawdy" dla Terraforma, które mapuje Twoje pliki konfiguracyjne (`.tf`) na rzeczywiste identyfikatory zasobów w AWS (np. ARN funkcji Lambda, ID rest api).

**Konsekwencje usunięcia stanu:**

- **Utrata kontroli:** Terraform "zapomni", że stworzył jakiekolwiek zasoby. Przy następnym `terraform apply` spróbuje stworzyć je wszystkie od nowa.
- **Błędy konfliktów:** Otrzymasz błędy typu `ResourceAlreadyExists` lub `ConflictException`, ponieważ np. rola IAM o danej nazwie lub bucket S3 już istnieją, ale Terraform nie ma ich w swoim spisie.
- **Wyciek zasobów (Resource Leakage):** Stare zasoby będą nadal działać i generować koszty w AWS, ale nie będziesz mógł ich zaktualizować ani usunąć za pomocą Terraforma (chyba że ręcznie zaimportujesz każdy z nich poleceniem `terraform import`).

---

### Co powinieneś usunąć zamiast tego?

Jeśli Twoim celem jest rozwiązanie błędu `Failed to load plugin schemas` lub `unavailable provider "archive"`, problem leży w **lokalnych plikach binarnych** w środowisku, w którym uruchamiasz Terraform (np. runner GitHub Actions lub Twój komputer), a nie w zdalnym stanie na S3.

Powinieneś wyczyścić lokalny katalog roboczy Terraforma (to jest bezpieczne):

1. **Lokalnie (jeśli testujesz):**

   ```
   rm -rf .terraform/
   rm .terraform.lock.hcl
   ```
2. **W GitHub Actions:**
   Runner za każdym razem startuje z czystym systemem, więc błąd prawdopodobnie wynika z tego, że w Twoim kodzie w repozytorium (w folderze `terraform/`) znajdują się resztki konfiguracji providera `archive`.

### Jak naprawić błąd providera bez usuwania stanu?

Błąd, który widzisz, wynika z faktu, że Terraform widzi w konfiguracji zapotrzebowanie na providera `archive`, ale nie może go zainicjalizować.

1. Upewnij się, że w żadnym pliku `.tf` nie masz bloku `data "archive_file"`.
2. Sprawdź plik blokady: jeśli masz go w systemie kontroli wersji (Git), usuń go i pozwól Terraformowi wygenerować nowy:

   ```
   git rm terraform/.terraform.lock.hcl
   ```
3. Upewnij się, że w bloku `required_providers` nie ma już wpisu o `archive`.

### Kiedy usunięcie stanu jest dopuszczalne?

Możesz usunąć `terraform.tfstate` **wyłącznie wtedy**, gdy:

1. Ręcznie usunąłeś wszystkie zasoby w AWS (wyczyściłeś konto).
2. Chcesz zacząć projekt od całkowitego zera i nie obchodzi Cię to, co zostało wcześniej wdrożone.

---

Jeśli nadal masz problem z importem `mangum` po zmianach w strukturze ZIP, podaj treść pliku `aws_lambda_function` z Terraform, sprawdzimy czy ścieżka do artefaktu jest poprawna.

Czy chcesz, abym przygotował instrukcję jak "wyczyścić" konkretny zasób ze stanu (np. tylko samą funkcję Lambda), zamiast usuwać cały plik?