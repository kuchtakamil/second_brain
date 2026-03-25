# kolejny problem.. The table `public.LiteLLM_UserTable` does not exist in the cur

**Data:** 24 gru 2025, 14:41:12 CET

---

**User:**

kolejny problem..
The table `public.LiteLLM_UserTable` does not exist in the current database.

---

**Gemini:**

Ten błąd potwierdza, że o ile klient Prisma został wygenerowany w Pythonie, o tyle sama baza PostgreSQL jest pusta i nie zawiera wymaganej struktury tabel. LiteLLM nie stworzył ich automatycznie, prawdopodobnie z powodu braku uprawnień lub problemów ze ścieżkami podczas startu serwisu.

Musisz wymusić synchronizację schematu z bazą danych (tzw. Schema Push).

### 1. Ręczne wypchnięcie schematu do bazy

Użyjemy komendy `db push`, która porównuje plik `schema.prisma` z bazą danych i tworzy brakujące tabele (w tym `LiteLLM_UserTable`). Pamiętaj o zachowaniu poprawnego `PATH` i `DATABASE_URL`.

```
sudo -u litellm bash -c "
export PATH='/opt/litellm-proxy/venv/bin:\$PATH' && \
export DATABASE_URL='postgresql://litellm_user:your_secure_password@localhost:5432/litellm_db' && \
export HOME='/home/litellm' && \
export XDG_CACHE_HOME='/home/litellm/.cache' && \
/opt/litellm-proxy/venv/bin/prisma db push --schema /opt/litellm-proxy/venv/lib/python3.12/site-packages/litellm/proxy/schema.prisma
"
```

### 2. Weryfikacja uprawnień w PostgreSQL

Komenda `db push` wymaga uprawnień do tworzenia tabel (CREATE). Jeśli użytkownik `litellm_user` ma ograniczone uprawnienia, proces się nie powiedzie. Upewnij się w konsoli `psql`:

```
-- Zaloguj się do bazy litellm_db
\c litellm_db

-- Nadaj uprawnienia do schematu public (wymagane w Postgres 15+)
GRANT ALL ON SCHEMA public TO litellm_user;
ALTER DATABASE litellm_db OWNER TO litellm_user;
```

### 3. Sprawdzenie czy tabele powstały

Po wykonaniu `db push`, sprawdź listę tabel w PostgreSQL:

```
sudo -u postgres psql -d litellm_db -c "\dt"
```

Powinieneś zobaczyć listę tabel, m.in.:

- `LiteLLM_UserTable`
- `LiteLLM_ProxyAPIKeys`
- `LiteLLM_Config`
- `LiteLLM_SpendLogs`

### 4. Restart i logi serwisu

Gdy tabele fizycznie istnieją w bazie, zrestartuj serwis systemowy:

```
sudo systemctl restart litellm
journalctl -u litellm -f
```

### Dlaczego to się dzieje?

LiteLLM przy starcie próbuje wykonać migracje automatycznie, ale robi to poprzez wywołanie binarnego silnika Prismy. Jeśli środowisko `systemd` nie ma poprawnie ustawionych zmiennych `PATH` (tak jak robiliśmy to ręcznie w punkcie 1), to proces startowy nie może odnaleźć generatorów i cicho pomija tworzenie tabel, co skutkuje błędem przy pierwszej próbie zapisu/odczytu użytkownika.

### Poprawka w serwisie systemd (Pre-start)

Aby uniknąć tego problemu w przyszłości, możesz dodać `ExecStartPre` do pliku `/etc/systemd/system/litellm.service`, co wymusi sprawdzenie bazy przed każdym startem:

```
[Service]
# ... inne ustawienia ...
Environment="PATH=/opt/litellm-proxy/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
ExecStartPre=/opt/litellm-proxy/venv/bin/prisma db push --schema /opt/litellm-proxy/venv/lib/python3.12/site-packages/litellm/proxy/schema.prisma
ExecStart=/opt/litellm-proxy/venv/bin/litellm --config /etc/litellm/config.yaml --port 4000
```

Jeśli po wykonaniu `db push` tabele są widoczne w `\dt`, ale serwis nadal zgłasza błąd, podaj proszę treść logów z `journalctl` tuż po restarcie.