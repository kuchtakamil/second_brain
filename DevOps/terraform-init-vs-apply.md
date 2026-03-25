# Różnica między `terraform init` a `terraform apply`

W cyklu automatyzacji infrastruktury i pracy z narzędziem Terraform, komendy `terraform init` oraz `terraform apply` odpowiadają za dwa zupełnie różne, ale nieodłączne względem siebie etapy – fazę przygotowania środowiska pracy oraz fazę wykonawczą, czyli wprowadzania zmian w infrastrukturze.

## Podsumowanie

- **`terraform init`** to faza weryfikacji i przygotowania. Służy do zainicjalizowania aktualnego katalogu roboczego, powiązania go z odpowiednim środowiskiem i pobrania niezbędnych wtyczek.
- **`terraform apply`** to faza wprowadzania zmian. Czyta ona pliki konfiguracyjne, weryfikuje je z obecnym stanem w chmurze, a po wygenerowaniu planu działania aplikuje konfigurację na docelowym środowisku.

## Dlaczego to jest ważne i kiedy ma zastosowanie?

Każdy nowy projekt konfiguracyjny (pliki z rozszerzeniem `.tf`) wymaga inicjalizacji. Nawet po sklonowaniu repozytorium z już napisanym i działającym kodem Terraforma, na świeżym komputerze pierwszą wpisywaną komendą zawsze musi być `terraform init`.

Z kolei `terraform apply` ma zastosowanie za każdym razem, gdy chcemy wcielić nowo napisany kod w życie (np. utworzyć nową wirtualną maszynę lub kontener), zmodyfikować obecne zasoby oraz wdrożyć całe środowisko na wybranym Providerze.

## Jak to działa w praktyce?

### 1. `terraform init` (Inicjalizacja)

Uruchomienie tej komendy polega po prostu na wpisaniu:
```bash
terraform init
```

Co dzieje się pod spodem?
- **Pobieranie providerów:** Terraform analizuje zdefiniowanych `dostawców` (np. AWS, Azure, Google Cloud) w naszych plikach `.tf` i pobiera dla nich odpowiednie wtyczki do ukrytego katalogu `.terraform/`.
- **Inicjalizacja backendu:** Jeśli nasz plik stanu konfiguracyjnego (`.tfstate`) jest przetrzymywany zdalnie (np. w S3 na AWS), ta komenda inicjuje takie zdalne połączenie z konfiguracją bezpieczeństwa.
- **Pobranie modułów:** Pobiera zewnętrzne i zdefiniowane lokalnie w kodzie moduły wielokrotnego użytku do głównego repozytorium.

> [!TIP]
> `terraform init` jest w pełni bezpieczną komendą. Nie dokonuje absolutnie żadnych zmian, czy modyfikacji na serwerach ani zasobach chmurowych. Możesz go uruchamiać wielokrotnie bez żadnych ryzyk.

### 2. `terraform apply` (Wdrożenie / Zastosowanie zmian)

Zainicjalizowany katalog daje zielone światło dla stworzenia i naniesienia zmian.
```bash
terraform apply
```

Faza wykonawcza dzieli się na kilka istotnych kroków:
1. **Odświeżenie stanu (Refresh):** Terraform odpytuje środowisko chmurowe (np. pyta API AWS-a) czy stan zasobów po stronie dostawcy nie różni się z plikiem `.tfstate`.
2. **Budowa planu:** Porównuje oczekiwania wynikające z lokalnego kodu (np. `main.tf`) z tym, co już znajduje się w pliku stanu w chmurze i buduje zarys tego co trzeba wykonać. (Nowe powstaną, nieopisane usunie, a aktualne - zaktualizuje).
3. **Pytanie o zgodę użytkownika (Akceptacja):** Po wyświetleniu zestawienia w trybie tylko do odczytu, pada pytanie z prośbą o potwierdzenie decyzji. Należy wpisać odpowiednie słowo (przeważnie **yes**) dla ostatecznego zatwierdzenia. Po nim uaktywnia się docelowe generowanie, modyfikacja bądź usuwanie zasobów.

Możemy pominąć zapytanie o ręczne potwierdzenie, co najczęściej ma zastosowanie w potokach używanych w narzędziach CI/CD (Continuous Integration/Continuous Deployment):
```bash
terraform apply -auto-approve
```

## Podsumowanie różnic

| Cecha | `terraform init` | `terraform apply` |
|-------|------------------|-------------------|
| **Cel** | Skonfigurowanie backendu, ściągnięcie zależności (modułów, dostawców). | Aplikowanie docelowej konfiguracji i infrastruktury w środowisku. |
| **Pobieranie wtyczek** | Tak (tworzy wpisy i lokalny `.terraform/`). | Nie. Mimo to nie uruchomi się, jeśli folder operacyjny nie jest zainicjalizowany. |
| **Modyfikacja zasobów** | Brak modyfikacji zasobów (komenda 100% bezpieczna). | Tak (realne modyfikacje chmury / maszyny). |
| **Kiedy używamy?** | Na początku, przy klonowaniu i po dołożeniu m.in nowych dependencji i providerów. | Po napisaniu / zmianie w kodzie i chęci wysłania tego już w stan produkcyjny. |

## Powiązane tematy
- Zamiast od razu stosować `terraform apply` zawsze powinieneś weryfikować spodziewane zmiany korzystając z bezpiecznego podglądu – `terraform plan`.
- Do budowania przejrzystych historii pracy można również wyprowadzać plan zdefiniowany i zablokowany podczas modyfikacji w plik, poprzez komendy: `terraform plan -out=tfplan`, a dla wdrożenia: `terraform apply tfplan`. Wyklucza to asynchroniczne lub niezapowiedziane modyfikacje z etapu `plan` do `apply` na współdzielonym środowisku.
