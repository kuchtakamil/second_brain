# chcę spróbować z podejściem - name: Force remove archive_file from state   run:

**Data:** 13 sty 2026, 14:07:26 CET

---

**User:**

chcę spróbować z podejściem
- name: Force remove archive_file from state
  run: |
    terraform state rm data.archive_file.your_data_source_name || true 
 working-directory: ./terraform

ale co wstawić za your_data_source_name?

---

**Gemini:**

Aby dowiedzieć się, jaką nazwę wstawić zamiast `your_data_source_name`, musisz sprawdzić, jak ten zasób został nazwany w kodzie, zanim go usunąłeś. Ponieważ jednak pliku już nie ma, najprostszym sposobem jest **wypisanie listy zasobów aktualnie znajdujących się w stanie**.

Dodaj tymczasowo poniższy krok do swojego workflow w GitHub Actions, przed krokiem `terraform apply`:

```
- name: List Terraform State
  run: |
    terraform state list | grep archive_file
  working-directory: ./terraform
```

### Jak odczytać wynik?

Po uruchomieniu Action, zajrzyj w logi tego kroku. Zobaczysz tam wpis w formacie:
`data.archive_file.nazwa_ktorej_szukasz`

Wtedy w swoim docelowym poleceniu używasz **pełnej nazwy**, np.:
`terraform state rm data.archive_file.lambda_zip`

---

### Inna metoda: Sprawdzenie pliku `.tfstate` na S3

Jeśli masz dostęp do pliku `terraform.tfstate` (pobrałeś go z S3), otwórz go w edytorze tekstowym i wyszukaj frazę `"type": "archive_file"`.

Szukaj bloku, który wygląda mniej więcej tak:

```
{
  "mode": "data",
  "type": "archive_file",
  "name": "TUTAJ_JEST_TWOJA_NAZWA",
  "provider": "provider[\"registry.terraform.io/hashicorp/archive\"]",
  ...
}
```

Wartość z pola `"name"` to właśnie to, co musisz wstawić po `data.archive_file.`.

### Jeśli chcesz zadziałać "w ciemno" (sprytny skrypt)

Możesz użyć poniższego skryptu w GitHub Actions, który sam znajdzie wszystkie zasoby typu `archive_file` i je usunie, bez konieczności wpisywania nazwy ręcznie:

```
- name: Force remove all archive_file data sources from state
  run: |
    # Pobierz listę wszystkich archive_file i usuń je jeden po drugim
    RESOURCES=$(terraform state list | grep "data.archive_file" || true)
    if [ -n "$RESOURCES" ]; then
      echo "Removing resources: $RESOURCES"
      for res in $RESOURCES; do
        terraform state rm "$res"
      done
    else
      echo "No archive_file resources found in state."
    fi
  working-directory: ./terraform
```

**Dlaczego to zadziała?**

- `terraform state list` wyciąga wszystko, co Terraform "pamięta".
- `grep` odfiltrowuje tylko te powiązane z nieszczęsnym providerem `archive`.
- Pętla `for` usuwa każdy znaleziony wpis, czyszcząc Twój stan na S3 i uwalniając Cię od błędu `Failed to load plugin schemas`.

Czy po uruchomieniu tego skryptu i wyczyszczeniu stanu chciałbyś, abyśmy sprawdzili, czy Twoja Lambda poprawnie widzi teraz moduł `mangum`?