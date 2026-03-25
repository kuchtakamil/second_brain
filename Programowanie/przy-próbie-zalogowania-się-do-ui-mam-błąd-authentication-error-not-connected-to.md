# przy próbie zalogowania się do UI mam błąd Authentication Error, Not connected t

**Data:** 22 gru 2025, 19:30:07 CET

---

**User:**

przy próbie zalogowania się do UI mam błąd
Authentication Error, Not connected to DB!
BTW. Chciałbym użyć PostgreSQL jako bazy

---

**Gemini:**

Błąd `Authentication Error, Not connected to DB!` wynika z faktu, że panel administracyjny (UI) LiteLLM wymaga relacyjnej bazy danych do przechowywania informacji o użytkownikach, kluczach wirtualnych oraz uprawnieniach. Bez skonfigurowanego połączenia z bazą, mechanizm uwierzytelniania nie ma gdzie zweryfikować Twoich poświadczeń.

Aby zaimplementować PostgreSQL jako backend dla LiteLLM, wykonaj poniższe kroki techniczne.

### 1. Instalacja sterownika bazy danych

LiteLLM używa biblioteki SQLAlchemy do komunikacji z bazami danych. Musisz zainstalować sterownik `psycopg2` (lub jego wersję binarną) wewnątrz środowiska wirtualnego, które stworzyliśmy wcześniej.

```
sudo -u litellm /opt/litellm-proxy/venv/bin/pip install psycopg2-binary
```

### 2. Konfiguracja bazy danych PostgreSQL

Upewnij się, że masz przygotowaną bazę i użytkownika. Z poziomu konsoli `psql`:

```
CREATE DATABASE litellm_db;
CREATE USER litellm_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE litellm_db TO litellm_user;
-- W nowszych wersjach Postgresa (15+) konieczne może być nadanie uprawnień do schematu:
\c litellm_db
GRANT ALL ON SCHEMA public TO litellm_user;
```

### 3. Aktualizacja `config.yaml`

Zmień sekcję `general_settings`, aby wskazać na instancję PostgreSQL. Format połączenia to: `postgresql://[user]:[password]@[host]:[port]/[db_name]`.

```
model_list:
  # ... Twoja lista modeli ...

general_settings:
  database_url: "postgresql://litellm_user:your_secure_password@localhost:5432/litellm_db"
  master_key: "sk-1234-admin-key" # To będzie Twój token do logowania w UI
  store_model_costs: true
```

### 4. Dostosowanie serwisu systemd (Opcjonalnie)

Jeśli wolisz nie trzymać hasła do bazy w pliku YAML, możesz przekazać `DATABASE_URL` przez zmienną środowiskową w pliku `/etc/systemd/system/litellm.service`:

```
[Service]
# ... reszta konfiguracji ...
Environment="DATABASE_URL=postgresql://litellm_user:your_secure_password@localhost:5432/litellm_db"
Environment="LITELLM_MASTER_KEY=sk-1234-admin-key"
# Jeśli używasz zmiennej środowiskowej, usuń database_url z config.yaml
```

Po zmianach przeładuj serwis:

```
sudo systemctl daemon-reload
sudo systemctl restart litellm
```

### 5. Logowanie do UI

Po poprawnym podłączeniu bazy danych:

1. Przejdź pod adres `http://localhost:4000/ui`.
2. Gdy system poprosi o klucz (Password/Token), wprowadź wartość zdefiniowaną jako `master_key` w Twojej konfiguracji.
3. LiteLLM automatycznie zainicjalizuje tabele (migracje bazy danych zostaną wykonane przy pierwszym starcie).

### Rozwiązywanie problemów (Advanced)

- **Błąd połączenia (Connection Refused):** Sprawdź, czy PostgreSQL nasłuchuje na porcie 5432 (`netstat -plnt`) oraz czy plik `pg_hba.conf` pozwala na połączenia lokalne dla użytkownika `litellm_user`.
- **Brak tabel:** Jeśli baza jest pusta, sprawdź logi serwisu: `journalctl -u litellm -f`. Szukaj komunikatów o błędach podczas "Auto-migrating database".
- **Metryki:** Po podłączeniu Postgresa, LiteLLM zacznie zapisywać każde zapytanie w tabeli `LiteLLM_Config`. Możesz tam bezpośrednio zapytać o zużycie tokenów:

  ```
  SELECT model, sum(total_tokens) FROM "LiteLLM_Table" GROUP BY model;
  ```