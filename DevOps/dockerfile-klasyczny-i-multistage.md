# Dockerfile — klasyczny i Multistage Build

Dockerfile to przepis opisujący, jak zbudować obraz kontenera Docker. Zawiera sekwencję instrukcji, z których każda tworzy nową warstwę (layer) w wynikowym obrazie. Znajomość typowych wzorców pozwala budować obrazy, które są bezpieczne, lekkie i szybkie do budowania.

## Dlaczego to jest ważne?

Dockerfile to fundament każdego procesu konteneryzacji. Źle napisany Dockerfile może prowadzić do:
- **ogromnych obrazów** (kilka GB zamiast kilkudziesięciu MB),
- **wolnych buildów** — za każdą zmianą kodu przebudowują się wszystkie warstwy,
- **problemów z bezpieczeństwem** — uruchamianie procesów jako root, wyciekanie sekretów.

Dobrze napisany Dockerfile wykorzystuje **cache warstw**, stosuje **użytkownika non-root** i minimalizuje liczbę zależności w finalnym obrazie.

---

## Klasyczny Dockerfile — element po elemencie

Poniższy przykład pokazuje typowy Dockerfile dla aplikacji w Pythonie (np. Flask/FastAPI). Każda linia jest opatrzona komentarzem, a szczegółowe wyjaśnienia znajdziesz poniżej.

```dockerfile
# 1. Obraz bazowy — używamy slim, żeby zmniejszyć rozmiar
FROM python:3.12-slim

# 2. Metadane — informacja o autorze/maintainerze
LABEL maintainer="kamil@example.com"

# 3. Zmienne środowiskowe
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 4. Katalog roboczy wewnątrz kontenera
WORKDIR /app

# 5. Instalacja zależności systemowych (apt, apk itp.)
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# 6. Kopiujemy NAJPIERW plik z zależnościami
COPY requirements.txt .

# 7. Instalacja zależności Pythona
RUN pip install --no-cache-dir -r requirements.txt

# 8. Kopiujemy RESZTĘ kodu aplikacji
COPY . .

# 9. Tworzymy użytkownika non-root
RUN useradd --create-home appuser
USER appuser

# 10. Eksponujemy port (dokumentacyjnie)
EXPOSE 8000

# 11. Punkt wejścia — uruchomienie aplikacji
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Wyjaśnienie poszczególnych instrukcji

#### `FROM python:3.12-slim`
Bazowy obraz, na którym budujemy. Wariant `slim` jest oparty na Debianie, ale z usuniętymi pakietami, które nie są potrzebne w typowym scenariuszu — daje to obraz ~150 MB zamiast ~900 MB pełnego `python:3.12`.

#### `LABEL`
Metadane przypisane do obrazu. Nie wpływają na działanie, ale pomagają w zarządzaniu obrazami w rejestrze (np. `docker inspect`).

#### `ENV`
Ustawia zmienne środowiskowe dostępne zarówno **w trakcie budowania**, jak i **w uruchomionym kontenerze**.

- `PYTHONDONTWRITEBYTECODE=1` — Python nie tworzy plików `.pyc`, co zmniejsza rozmiar warstw.
- `PYTHONUNBUFFERED=1` — logi z `print()` i `logging` pojawiają się natychmiast w `docker logs`.

#### `WORKDIR /app`
Ustawia katalog roboczy. Wszystkie kolejne instrukcje (`RUN`, `COPY`, `CMD`) wykonują się względem `/app`. Jeśli katalog nie istnieje, Docker go utworzy automatycznie.

#### `RUN apt-get update && ... && rm -rf /var/lib/apt/lists/*`
Instalacja paczek systemowych. Trzy najważniejsze praktyki:
1. **`update` i `install` w jednym `RUN`** — inaczej cache `update` może być stary, a `install` pobierze przestarzałe pakiety.
2. **`--no-install-recommends`** — nie instalujemy pakietów rekomendowanych, tylko te wymagane.
3. **`rm -rf /var/lib/apt/lists/*`** — czyścimy cache apt, żeby nie zwiększał rozmiaru warstwy.

#### `COPY requirements.txt .`
Kopiujemy **tylko plik z zależnościami** przed ich instalacją. Dlaczego osobno? To klucz do wykorzystania **cache'u warstw** Dockera — patrz sekcja poniżej.

#### `RUN pip install --no-cache-dir -r requirements.txt`
Instalacja pakietów Pythona. Flaga `--no-cache-dir` zapobiega zapisywaniu pobranych paczek do cache pip-a wewnątrz obrazu, oszczędzając miejsce.

#### `COPY . .` ← Dlaczego to ma sens?

To jest jeden z najczęściej niezrozumianych kroków. Oznacza:

> **Skopiuj wszystko z bieżącego katalogu na hoście (`.` po lewej) do bieżącego katalogu roboczego w kontenerze (`.` po prawej, czyli `/app`).**

**Dlaczego nie kopiujemy wszystkiego na raz na początku?**

Docker buduje obraz **warstwa po warstwie** i **cache'uje każdą warstwę**. Jeśli pliki wejściowe danej warstwy się nie zmieniły, Docker użyje wersji z cache zamiast ponownie wykonywać instrukcję.

Rozważmy dwa podejścia:

```dockerfile
# ❌ ZŁE podejście — jedno COPY na początku
COPY . .
RUN pip install -r requirements.txt
```

W tym scenariuszu **każda zmiana w kodzie** (nawet literówka w komentarzu) invaliduje cache warstwy `COPY . .`, a co za tym idzie — **ponownie instaluje wszystkie zależności**. Przy dużych projektach to może trwać minuty.

```dockerfile
# ✅ DOBRE podejście — dwuetapowe COPY
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
```

Tutaj:
1. Jeśli `requirements.txt` się **nie zmienił** → warstwa `pip install` bierze się z cache (**sekundy zamiast minut**).
2. Warstwa `COPY . .` przebudowuje się tylko wtedy, gdy zmieni się kod — ale to jest szybka operacja (kopiowanie plików).

**Podsumowując:** `COPY . .` jest celowo umieszczone **po** instalacji zależności, aby maksymalnie wykorzystać cache Dockera. Najpierw kopiujemy to, co zmienia się **rzadko** (zależności), potem to, co zmienia się **często** (kod).

#### `RUN useradd ... && USER appuser`
Domyślnie kontener działa jako **root**, co jest ryzykowne — jeśli atakujący przejmie proces w kontenerze, ma uprawnienia roota. Tworzenie dedykowanego użytkownika i przełączenie się na niego to **standardowa praktyka bezpieczeństwa**.

#### `EXPOSE 8000`
Instrukcja **dokumentacyjna** — informuje osobę czytającą Dockerfile, na jakim porcie nasłuchuje aplikacja. Sama w sobie **nie otwiera portu** — to robi flaga `-p` podczas `docker run`.

#### `CMD`
Domyślne polecenie uruchamiane po starcie kontenera. Używamy formy exec (tablica JSON) zamiast formy shell, żeby proces otrzymał sygnały (np. `SIGTERM` przy `docker stop`) bezpośrednio, a nie przez pośrednika `/bin/sh`.

---

## Multistage Build — lżejszy i bezpieczniejszy obraz

### Problem

W klasycznym Dockerfile **narzędzia potrzebne do budowania** (kompilatory, nagłówki C, narzędzia do kompilacji) trafiają do finalnego obrazu, mimo że w runtime nie są potrzebne. To:
- zwiększa rozmiar obrazu,
- rozszerza powierzchnię ataku,
- wydłuża czas pobierania obrazu.

### Rozwiązanie — Multistage Build

Multistage build pozwala na zdefiniowanie **wielu etapów** (stages) w jednym Dockerfile. Każdy etap zaczyna się od instrukcji `FROM`. Z etapu budowania kopiujemy do etapu runtime'owego **wyłącznie** artefakty (skompilowane binarki, zainstalowane pakiety), zostawiając za sobą cały "brudny" toolchain.

```dockerfile
# =========================================
# ETAP 1: Builder — budowanie i kompilacja
# =========================================
FROM python:3.12-slim AS builder

WORKDIR /app

# Instalacja narzędzi potrzebnych TYLKO do kompilacji
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Instalacja do osobnego katalogu — łatwe do skopiowania
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# =========================================
# ETAP 2: Runtime — czysty, lekki obraz
# =========================================
FROM python:3.12-slim AS runtime

WORKDIR /app

# Kopiujemy TYLKO zainstalowane pakiety z etapu builder
COPY --from=builder /install /usr/local

# Kopiujemy kod aplikacji
COPY . .

# Instalacja minimalnych zależności systemowych runtime
RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq5 && \
    rm -rf /var/lib/apt/lists/*

# Bezpieczeństwo — użytkownik non-root
RUN useradd --create-home appuser
USER appuser

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Co się dzieje krok po kroku?

```
┌─────────────────────────────────────────┐
│          ETAP 1: builder                │
│                                         │
│  python:3.12-slim                       │
│  + gcc, libpq-dev (kompilatory)         │
│  + pip install → /install               │
│                                         │
│  Ten etap jest ODRZUCANY po buildzie    │
└──────────────────┬──────────────────────┘
                   │
          COPY --from=builder
                   │
┌──────────────────▼──────────────────────┐
│          ETAP 2: runtime                │
│                                         │
│  python:3.12-slim (czysty!)             │
│  + pakiety z /install (skopiowane)      │
│  + libpq5 (runtime, nie -dev)           │
│  + kod aplikacji                        │
│                                         │
│  To jest FINALNY obraz                  │
└─────────────────────────────────────────┘
```

### Kluczowe elementy multistage

| Element | Opis |
| :--- | :--- |
| `FROM ... AS builder` | Nadaje etapowi nazwę, do której można się odwołać |
| `--prefix=/install` | Instaluje pakiety do wydzielonego katalogu |
| `COPY --from=builder` | Kopiuje pliki **z innego etapu**, a nie z hosta |
| Dwa osobne `FROM` | Docker odrzuca wszystkie warstwy etapów, które nie są finalnym etapem |

### Porównanie rozmiarów

| Podejście | Zawartość obrazu | Przykładowy rozmiar |
| :--- | :--- | :--- |
| Klasyczny Dockerfile | Python + gcc + libpq-dev + kod | ~350 MB |
| Multistage Build | Python + libpq5 + kod | ~180 MB |

Różnica wynika z tego, że `gcc` i nagłówki deweloperskie (`-dev`) są znacznie większe niż biblioteki runtime.

---

## .dockerignore — nie zapomnij!

Tak jak `.gitignore` filtruje pliki dla Gita, `.dockerignore` filtruje pliki dla kontekstu budowania Dockera. Bez niego `COPY . .` skopiuje **wszystko**, łącznie z niepotrzebnymi plikami:

```
# .dockerignore
.git
.venv
__pycache__
*.pyc
.env
.idea
.vscode
node_modules
docker-compose*.yml
Dockerfile
README.md
tests/
```

Bez `.dockerignore` instrukcja `COPY . .` skopiowałaby np. katalog `.git` (często setki MB) czy `.venv` do obrazu — co jest marnotrawstwem przestrzeni i potencjalnym zagrożeniem bezpieczeństwa.

---

## Podsumowanie najlepszych praktyk

1. **Używaj wariantu `slim` lub `alpine`** obrazu bazowego — mniejszy rozmiar, mniejsza powierzchnia ataku.
2. **Dziel `COPY` na etapy** — najpierw zależności (`requirements.txt`), potem kod (`COPY . .`) — aby maksymalnie wykorzystać cache warstw.
3. **Stosuj multistage build** — gdy potrzebujesz kompilacji, nie ciągnij narzędzi do budowania do finalnego obrazu.
4. **Uruchamiaj jako non-root** — `RUN useradd` + `USER` — standardowa praktyka bezpieczeństwa.
5. **Używaj `.dockerignore`** — aby `COPY . .` nie kopiowało śmieci.
6. **Czyść cache menedżera pakietów** — `rm -rf /var/lib/apt/lists/*` w tej samej warstwie co `apt-get install`.
7. **Używaj formy exec** (`CMD ["...", "..."]`) zamiast formy shell (`CMD uvicorn ...`).

## Powiązane pliki

- [ENTRYPOINT vs CMD w Docker](entrypoint-vs-cmd-w-docker.md)
- [Docker exec vs attach](docker-exec-vs-attach.md)
- [Docker — persistence i volumes](docker_persistence_and_volumes.md)
- [Docker — uprawnienia i non-root](docker-permissions.md)
- [Playwright w Docker jako non-root](playwright-docker-nonroot.md)
