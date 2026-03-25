# Scala app in Docker

**Data:** 2023-03-30

---

**User:**

Jak w jednym repozytorium aplikacji w Scala, najlepiej przy pomocy docker/docker-compose oraz opcjonalnie przy użyciu sbt, uruchomić kilka niezależnych aplikacji typu CLI?

---

**Assistant:**

Można to zrobić za pomocą docker-compose i kontenerów Docker. Każda aplikacja może być uruchomiona w oddzielnym kontenerze, a docker-compose pozwala na łatwe uruchamianie wielu kontenerów jednocześnie i konfigurowanie ich w sposób spójny.

Oto przykładowy plik `docker-compose.yml` dla trzech niezależnych aplikacji typu CLI napisanych w języku Scala:

```
version: "3.9"

services:
  app1:
    build: ./app1
    command: sbt run
    tty: true
  app2:
    build: ./app2
    command: sbt run
    tty: true
  app3:
    build: ./app3
    command: sbt run
    tty: true
```

Powyższy plik `docker-compose.yml` definiuje trzy usługi, każda z nich reprezentuje jedną aplikację. Każda usługa jest zdefiniowana przez sekcję `services` i posiada trzy kluczowe parametry:

- `build`: ścieżka do katalogu, w którym znajduje się plik Dockerfile dla aplikacji
- `command`: polecenie, które zostanie uruchomione wewnątrz kontenera
- `tty`: wartość true oznacza, że kontener będzie interaktywny, co jest potrzebne dla aplikacji typu CLI

Dla każdej aplikacji należy utworzyć osobny katalog z plikiem Dockerfile i kodem aplikacji. Na przykład, dla aplikacji `app1`, struktura katalogów powinna wyglądać następująco:

```
app1/
  Dockerfile
  src/
    main/
      scala/
        // kod aplikacji
```

Plik Dockerfile dla aplikacji `app1` mógłby wyglądać następująco:

```
FROM openjdk:11

WORKDIR /app

COPY . /app

CMD ["sbt", "run"]
```

W tym przykładzie, Dockerfile zaczyna od wyboru obrazu bazowego openjdk:11. Następnie, ustawia katalog roboczy na /app i kopiuje wszystkie pliki z bieżącego katalogu do katalogu /app w kontenerze. W końcu, ustawia polecenie CMD, które uruchamia komendę sbt run.

Po utworzeniu plików Dockerfile dla wszystkich aplikacji, można uruchomić je wszystkie naraz przy pomocy polecenia `docker-compose up`. Opcja `up` uruchamia wszystkie kontenery zdefiniowane w pliku `docker-compose.yml`.

Jeśli aplikacja zależy od innych usług, takich jak baza danych, należy dodać je jako osobne usługi w pliku `docker-compose.yml`. Wtedy można zapewnić, że kontenery będą działać w jednym sieciowaniu, co umożliwi aplikacjom komunikację ze sobą nawzajem.

Warto zwrócić uwagę, że uruchamianie aplikacji typu CLI w kontenerach może nie być najlepszym rozwiązaniem w niekt

---

**User:**

Chcę wybraną aplikację uruchomić jako kilka osobnych procesów z różnymi argumantami na wejściu. Jak to zrobić w docker-cmpose?

---

**Assistant:**

W docker-compose można uruchomić jedną aplikację jako kilka osobnych procesów z różnymi argumentami na wejściu, używając tzw. skaliwania usługi. 

Przykładowy plik `docker-compose.yml` dla takiej aplikacji może wyglądać następująco:

```
version: "3.9"

services:
  app:
    build: .
    command: ["./app.sh", "arg1"]
    deploy:
      replicas: 3
```

W powyższym przykładzie, usługa `app` ma zdefiniowane trzy repliki (czyli trzy instancje), które zostaną uruchomione z różnymi argumentami na wejściu. W tym celu, argumenty zostaną przekazane do skryptu `app.sh`, który został zdefiniowany jako wartość parametru `command`. W powyższym przykładzie, każda replika będzie uruchomiona z argumentem `arg1`.

Po uruchomieniu komendy `docker-compose up`, docker-compose uruchomi trzy kontenery z aplikacją `app`, z których każdy będzie uruchomiony z różnym argumentem na wejściu. 

Warto zauważyć, że w tym przypadku, argumenty są zdefiniowane na stałe w pliku `docker-compose.yml`. Jeśli chcemy mieć możliwość zmiany argumentów dla każdej repliki, możemy użyć tzw. plików środowiskowych. Możemy np. stworzyć plik `.env` z wartością zmiennej `APP_ARGS`:

```
APP_ARGS=arg1
```

Następnie, możemy zmienić plik `docker-compose.yml`, aby pobierał wartość argumentów z pliku `.env`:

```
version: "3.9"

services:
  app:
    build: .
    command: ["./app.sh", "${APP_ARGS}"]
    deploy:
      replicas: 3
```

Teraz, po zmianie wartości zmiennej `APP_ARGS` w pliku `.env`, możemy ponownie uruchomić usługę `app` i każda replika zostanie uruchomiona z nowym argumentem na wejściu.