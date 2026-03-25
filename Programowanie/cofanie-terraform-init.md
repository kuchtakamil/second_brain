# Cofanie terraform init

**Data:** 2026-01-06

---

**User:**

uruchomiłem terraform init w niewłaściwym katalogu. jak to cofnąć?

---

**Assistant:**

Terraform `init` nie wykonuje zmian w infrastrukturze, więc „cofanie” sprowadza się do posprzątania artefaktów, które utworzył lokalnie.

### Co dokładnie robi `terraform init`
- tworzy katalog **`.terraform/`** (provider plugins, backend config),
- może utworzyć lub zmodyfikować plik **`.terraform.lock.hcl`**,
- w przypadku backendów zdalnych zapisuje lokalne metadane inicjalizacji.

### Jak to cofnąć
W katalogu, w którym uruchomiłeś `terraform init`:

1. **Usuń katalog `.terraform/`**
   ```bash
   rm -rf .terraform
   ```

2. **Usuń plik `.terraform.lock.hcl`** (jeśli nie powinien istnieć w tym katalogu)
   ```bash
   rm -f .terraform.lock.hcl
   ```

To w pełni „od-inicjalizuje” katalog.

### Ważne uwagi
- **Nie ma wpływu na chmurę / infrastrukturę** – `init` niczego nie provisionuje.
- Jeśli używasz **remote backendu** (S3, GCS, Terraform Cloud):
  - samo `init` nie tworzy zasobów,
  - wyjątkiem może być **utworzenie pustego bucketu/kontenera**, jeśli backend był skonfigurowany do auto-tworzenia (rzadkie, ale możliwe). Wtedy trzeba usunąć go ręcznie w chmurze.
- Jeżeli katalog był objęty **repozytorium Git**, sprawdź:
  ```bash
  git status
  ```
  i upewnij się, że nic nie zostało przypadkowo dodane do commita.

### Dobra praktyka na przyszłość
- Uruchamiaj Terraform z wyraźnie wydzielonych katalogów (np. `envs/dev`, `envs/prod`).
- Dodaj do `.gitignore`:
  ```
  .terraform/
  ```

Jeżeli chcesz, opisz **jaki backend i provider** były skonfigurowane – powiem, czy jest jakiekolwiek ryzyko efektów ubocznych.