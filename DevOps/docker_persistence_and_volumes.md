# Docker: gdzie sa zapisywane raporty, raw filings i ChromaDB

Data: 2026-05-14

## Krotka odpowiedz dla tego projektu

W obecnej konfiguracji produkcyjnej dane nie powinny byc zapisywane tylko w
warstwie kontenera. `docker-compose.yml` montuje katalogi z hosta do kontenera:

```yaml
services:
  dd-web:
    volumes:
      - ./output:/app/output
      - ./data:/app/data
      - ./logs:/app/logs
```

To oznacza:

| Dane | Sciezka w kontenerze | Sciezka na hoscie |
| --- | --- | --- |
| raporty `.md` / `.pdf` | `/app/output` | `./output` |
| ChromaDB | `/app/data/chroma` | `./data/chroma` |
| surowe pliki SEC | `/app/data/<TICKER>` | `./data/<TICKER>` |
| logi | `/app/logs` | `./logs` |

Wazne: `./output`, `./data` i `./logs` sa interpretowane wzgledem katalogu, z
ktorego uruchamiany jest `docker compose`, czyli zwykle wzgledem katalogu z
plikiem `docker-compose.yml`.

## Dlaczego to ma znaczenie

Kontener ma wlasny filesystem. Jesli aplikacja zapisuje plik do `/app/output`,
a ten katalog nie jest podmontowany z zewnatrz, plik trafia do zapisywalnej
warstwy kontenera.

Taka warstwa:

- przezywa zwykly restart tego samego kontenera;
- nie jest czescia obrazu Dockera;
- znika po usunieciu kontenera, np. `docker rm`, `docker compose down` i
  ponownym utworzeniu kontenera;
- nie jest dobrym miejscem na dane, ktore maja byc trwale.

Dlatego raporty, baza wektorowa i pobrane filing files powinny byc zapisywane
albo na bind mouncie, albo na Docker volume.

## Wazny haczyk: compose z mountami vs sam obraz

To jest najlatwiejsze miejsce do pomylki.

`Dockerfile` tworzy katalogi:

```dockerfile
RUN mkdir -p /app/output /app/data/chroma /app/logs
```

To nie oznacza jeszcze, ze sa one trwale. To tylko katalogi wewnatrz obrazu /
kontenera. Trwalosc pojawia sie dopiero wtedy, gdy przy uruchomieniu kontenera
podmontujemy cos z zewnatrz.

Jesli uruchomisz aplikacje przez produkcyjny `docker-compose.yml`, mounty sa
aktywne:

```bash
docker compose up -d
```

Wtedy zapis do `/app/output` trafia na hosta do `./output`, a zapis do
`/app/data/chroma` trafia na hosta do `./data/chroma`.

Jesli jednak uruchomisz sam obraz bez mountow:

```bash
docker run dd-web
```

albo:

```bash
docker run -p 8000:8000 dd-web
```

to `/app/output`, `/app/data` i `/app/logs` beda zwyklymi katalogami w
kontenerze. Dane beda wygladaly, jakby "dzialaly", ale po skasowaniu kontenera
znikna.

Poprawne uruchomienie samego obrazu wymagaloby mountow:

```bash
docker run \
  -p 8000:8000 \
  -v "$(pwd)/output:/app/output" \
  -v "$(pwd)/data:/app/data" \
  -v "$(pwd)/logs:/app/logs" \
  dd-web
```

## Haczyk lokalnego override'a

W repo jest tez `docker-compose.local.yml`:

```yaml
services:
  dd-web:
    ports:
      - "8000:8000"
```

Ten plik sam dodaje tylko mapowanie portu. Nie zawiera sekcji `volumes`.

Powinien byc uzywany jako override razem z glownym compose:

```bash
docker compose -f docker-compose.yml -f docker-compose.local.yml up -d
```

Wtedy Docker laczy oba pliki:

- `docker-compose.yml` daje build, env, volumes i siec;
- `docker-compose.local.yml` dodaje lokalne wystawienie portu `8000:8000`.

Jesli ktos uruchomilby tylko:

```bash
docker compose -f docker-compose.local.yml up -d
```

to taka konfiguracja jest niepelna. Nie ma tam builda, env file, mountow ani
reszty produkcyjnych ustawien.

## Jak aplikacja wybiera sciezki

Domyslne sciezki sa w `src/dd/config.py`:

```python
chroma_persist_dir: str = "./data/chroma"
web_output_dir: str = "./output"
```

W kontenerze katalog roboczy to `/app`, bo `Dockerfile` ma:

```dockerfile
WORKDIR /app
```

Dlatego sciezki wzgledne oznaczaja:

```text
./data/chroma -> /app/data/chroma
./output      -> /app/output
```

Plik `.env` moze nadpisac te ustawienia:

```env
CHROMA_PERSIST_DIR=./data/chroma
WEB_OUTPUT_DIR=./output
```

Jesli zmieniasz te wartosci, trzeba pilnowac, zeby nadal wskazywaly na
podmontowany katalog. Przyklad zly:

```env
CHROMA_PERSIST_DIR=/tmp/chroma
WEB_OUTPUT_DIR=/tmp/output
```

Jesli `/tmp` nie jest volume ani bind mountem, dane beda wewnatrz kontenera.

Przyklad poprawny:

```env
CHROMA_PERSIST_DIR=/app/data/chroma
WEB_OUTPUT_DIR=/app/output
```

albo zostawienie sciezek wzglednych:

```env
CHROMA_PERSIST_DIR=./data/chroma
WEB_OUTPUT_DIR=./output
```

przy zalozeniu, ze `/app/data` i `/app/output` sa podmontowane w compose.

## Bind mount vs Docker volume

W tym projekcie uzywany jest bind mount:

```yaml
volumes:
  - ./output:/app/output
  - ./data:/app/data
  - ./logs:/app/logs
```

Bind mount oznacza: "wez konkretny katalog z hosta i pokaz go w kontenerze".

Zalety bind mounta:

- latwo zobaczyc pliki na serwerze;
- latwo zrobic backup zwyklymi narzedziami;
- latwo eksportowac raporty i baze ChromaDB;
- dobre dla prostego VPS-a.

Wady bind mounta:

- trzeba pilnowac uprawnien katalogow na hoscie;
- sciezka `./data` zalezy od miejsca uruchomienia compose;
- przy deployu na inny serwer trzeba pamietac o przeniesieniu katalogow.

Alternatywa to nazwany Docker volume:

```yaml
services:
  dd-web:
    volumes:
      - dd_output:/app/output
      - dd_data:/app/data
      - dd_logs:/app/logs

volumes:
  dd_output:
  dd_data:
  dd_logs:
```

Named volume oznacza: "Docker sam zarzadza miejscem na dane".

Zalety named volume:

- niezalezne od katalogu uruchomienia compose;
- Docker pilnuje fizycznego polozenia danych;
- dobre dla standardowych wdrozen Dockerowych.

Wady named volume:

- pliki sa mniej widoczne bezposrednio w katalogu projektu;
- backup wymaga komend Dockera albo znajomosci lokalizacji volume;
- mniej wygodne, gdy chcesz szybko obejrzec wygenerowany raport na hoscie.

## Jak sprawdzic, czy mount dziala

Najprostszy test:

```bash
docker compose exec dd-web sh -lc 'pwd && ls -la /app && ls -la /app/data /app/output'
```

Potem sprawdz na hoscie:

```bash
ls -la ./data ./output ./logs
```

Mozna tez sprawdzic mounty na dzialajacym kontenerze:

```bash
docker inspect dd-web --format '{{ json .Mounts }}'
```

Wynik powinien zawierac wpisy dla:

```text
/app/output
/app/data
/app/logs
```

Jesli tych wpisow nie ma, aplikacja najpewniej zapisuje dane do filesystemu
kontenera.

## Jak skonfigurowac to poprawnie

Minimalna konfiguracja dla tego projektu:

```yaml
services:
  dd-web:
    build: .
    env_file: .env
    volumes:
      - ./output:/app/output
      - ./data:/app/data
      - ./logs:/app/logs
```

Minimalny `.env` dotyczacy sciezek:

```env
CHROMA_PERSIST_DIR=./data/chroma
WEB_OUTPUT_DIR=./output
```

Przed pierwszym startem mozna utworzyc katalogi na hoscie:

```bash
mkdir -p output data/chroma logs
```

Jesli kontener dziala jako nie-root user, katalogi musza byc zapisywalne dla
UID/GID uzywanego w kontenerze. W tym projekcie `Dockerfile` tworzy usera:

```dockerfile
RUN useradd -m -u 1000 dduser
USER dduser
```

Na typowym Linuxie UID `1000` to pierwszy lokalny uzytkownik. Jesli katalogi na
hoscie nie sa zapisywalne, aplikacja moze miec bledy typu "permission denied".

Dla prostego VPS-a praktyczna konfiguracja to:

```bash
mkdir -p output data/chroma logs
sudo chown -R 1000:1000 output data logs
```

W skrypcie deploya jest podobny krok tworzacy katalogi:

```bash
mkdir -p "${REMOTE_DIR}"/{output,data/chroma,logs}
```

## Co jest trwale, a co nie

Trwale przy obecnym compose:

- wygenerowane raporty w `./output`;
- baza ChromaDB w `./data/chroma`;
- surowe pliki SEC w `./data/<TICKER>`;
- logi w `./logs`.

Nietrwale:

- in-memory job store w `src/dd/api/jobs.py`;
- aktywne kolejki SSE;
- statusy jobow po restarcie procesu;
- wszystko zapisane poza `/app/output`, `/app/data` i `/app/logs`, chyba ze
  dodasz osobny mount.

To oznacza, ze restart kontenera nie powinien kasowac raportow ani bazy RAG, ale
skasuje stan aktywnych jobow trzymany w pamieci procesu.

## Regula praktyczna

Kazda sciezka, do ktorej aplikacja zapisuje dane warte zachowania, musi spelniac
jedno z dwoch kryteriow:

1. Jest podmontowana jako bind mount, np. `./data:/app/data`.
2. Jest podmontowana jako named volume, np. `dd_data:/app/data`.

Samo `mkdir` w `Dockerfile` nie daje trwalosci. Ono tylko zapewnia, ze katalog
istnieje w kontenerze.
