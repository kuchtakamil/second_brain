# Błąd uwierzytelniania PostgreSQL

**Data:** 2025-12-23

---

**User:**

chcę się zalogować i dostaję błąd
psql -U postgres                                                                                   ──(wto,gru23)─┘
psql: error: connection to server on socket "/var/run/postgresql/.s.PGSQL.5432" failed: FATAL:  Peer authentication failed for user "postgres"

---

**Assistant:**

Ten błąd nie dotyczy hasła ani samego `psql`, tylko **metody uwierzytelniania skonfigurowanej w PostgreSQL**.

### Co się dzieje
Komunikat:

```
FATAL:  Peer authentication failed for user "postgres"
```

oznacza, że:

- PostgreSQL próbuje użyć **peer authentication**
- przy połączeniu przez **lokalny socket Unix**
- użytkownik bazy `postgres` **musi być zalogowanym użytkownikiem systemowym `postgres`**

Ty uruchamiasz `psql -U postgres` jako **zwykły użytkownik systemu**, więc uwierzytelnianie „peer” odrzuca połączenie.

---

## Najprostsze rozwiązania (w zależności od celu)

### 1. Zaloguj się jako użytkownik systemowy `postgres` (najczęstsze)
Jeśli masz uprawnienia `sudo`:

```bash
sudo -u postgres psql
```

albo:

```bash
sudo su - postgres
psql
```

To **powinno zadziałać bez hasła**, bo peer authentication wtedy się zgadza.

---

### 2. Wymusić logowanie hasłem (jeśli chcesz łączyć się jako zwykły user)
Połącz się przez TCP zamiast socketu:

```bash
psql -U postgres -h 127.0.0.1
```

Wtedy PostgreSQL **nie użyje peer**, tylko `md5` / `scram-sha-256` (jeśli hasło jest ustawione).

Jeżeli dostaniesz pytanie o hasło i ono działa — problem rozwiązany.

---

### 3. Zmienić konfigurację PostgreSQL (trwałe rozwiązanie)
Jeżeli chcesz **zawsze logować się hasłem**, musisz zmienić `pg_hba.conf`.

1. Otwórz plik (ścieżka zależna od distro, np.):
```bash
/etc/postgresql/15/main/pg_hba.conf
```

2. Znajdź linię:
```
local   all   postgres   peer
```

3. Zmień na:
```
local   all   postgres   md5
```
lub (nowsze, bezpieczniejsze):
```
local   all   postgres   scram-sha-256
```

4. Zrestartuj PostgreSQL:
```bash
sudo systemctl restart postgresql
```

5. Upewnij się, że użytkownik `postgres` ma hasło:
```sql
ALTER USER postgres WITH PASSWORD 'haslo';
```

---

## Rekomendacja praktyczna
- **Administracja lokalna** → `sudo -u postgres psql`
- **Aplikacje / development** → TCP + hasło
- **Produkcja** → scram-sha-256 + role aplikacyjne (nie `postgres`)

Jeśli chcesz, podaj:
- dystrybucję (Ubuntu / Debian / Fedora / Docker)
- wersję PostgreSQL
- czy to lokalnie, w kontenerze czy na VM

Wtedy podam dokładną ścieżkę i najlepszą konfigurację pod Twój przypadek.

---

**User:**

zalogowałem się. Teraz to
postgres=# CREATE DATABASE litellm_db;
ERROR:  template database "template1" has a collation version mismatch
DETAIL:  The template database was created using collation version 2.35, but the operating system provides version 2.39.
HINT:  Rebuild all objects in the template database that use the default collation and run ALTER DATABASE template1 REFRESH COLLATION VERSION, or build PostgreSQL with the right library version.

---

**Assistant:**

To jest **znany problem po aktualizacji systemu (glibc)**, a nie błąd SQL ani PostgreSQL jako takiego.

### Co się stało
- PostgreSQL był **zainicjalizowany na starej wersji glibc (2.35)**
- System ma teraz **nowszą glibc (2.39)**
- Kolacje (collation) w `template1` są „stare”
- PostgreSQL **blokuje tworzenie nowych baz**, żeby uniknąć niespójności sortowania

---

## Najszybsze i poprawne rozwiązanie (zalecane)

Ponieważ **nie masz jeszcze danych produkcyjnych**, wystarczy odświeżyć kolacje w bazach szablonowych.

### 1. Odśwież `template1`
Będąc zalogowanym jako `postgres`:

```sql
ALTER DATABASE template1 REFRESH COLLATION VERSION;
```

### 2. (Opcjonalnie, ale zalecane) Odśwież `postgres`
```sql
ALTER DATABASE postgres REFRESH COLLATION VERSION;
```

### 3. Spróbuj ponownie
```sql
CREATE DATABASE litellm_db;
```

To **powinno zadziałać natychmiast**.

---

## Dlaczego to jest bezpieczne
- `template1` **nie zawiera Twoich danych**
- Operacja **nie modyfikuje rekordów**
- Aktualizuje tylko metadane kolacji
- Jest to **oficjalnie zalecane** przez PostgreSQL po update glibc

---

## Kiedy to NIE wystarczy
Jeżeli dostałbyś błąd typu:
```
ERROR: collation version mismatch detected in database X
```
w **bazie z danymi**, wtedy trzeba:
- zidentyfikować indeksy zależne od collation
- przebudować je (`REINDEX`)
- ewentualnie `REINDEX DATABASE`

Ale w Twoim przypadku (świeża instancja / dev) **nie ma takiej potrzeby**.

---

## Dodatkowa rekomendacja (dev / AI stack)
Jeżeli to jest środowisko pod **LiteLLM / lokalne LLM / kontenery**:
- rozważ **inicjalizację PostgreSQL w Dockerze**
- albo `initdb` po aktualizacji systemu
- unikniesz tego problemu przy przyszłych update’ach glibc

Jeśli chcesz, mogę:
- sprawdzić **czy wszystkie bazy są OK**
- podać **komendy diagnostyczne**
- zaproponować **czystą konfigurację PostgreSQL pod LiteLLM**

Daj znać.