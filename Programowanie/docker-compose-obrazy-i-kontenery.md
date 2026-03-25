# Docker Compose obrazy i kontenery.

**Data:** 2023-05-07

---

**User:**

W projekcie są pliki vertex.dockerfile, square.dockerfile oraz docker-compose.yml
W docker-compose.yml chcę najpierw zbudować obrazy z vertex.dockerfile pod nazwą vertex-machine oraz square.dockerfile jako square-machine później uruchomić te obrazy. Czy mogę to wszystko zrobić z docker-compose.yml?

---

**Assistant:**

Tak, możesz to zrobić z plikiem docker-compose.yml. Aby zbudować obrazy z plików Dockerfile i uruchomić je przy użyciu Docker Compose, możesz skorzystać z poleceń `build` i `image` w pliku docker-compose.yml.

Oto przykładowy plik docker-compose.yml, który buduje obrazy i uruchamia je jako kontenery:

```
version: '3'
services:
  vertex:
    build:
      context: .
      dockerfile: vertex.dockerfile
    image: vertex-machine
  square:
    build:
      context: .
      dockerfile: square.dockerfile
    image: square-machine
  # dodaj tutaj pozostałe usługi, jeśli są potrzebne
```

W powyższym pliku docker-compose.yml zdefiniowano dwie usługi: `vertex` i `square`. Dla każdej usługi określono ścieżkę do pliku Dockerfile za pomocą klucza `build`. W przypadku usługi `vertex` jest to `vertex.dockerfile`, a dla usługi `square` jest to `square.dockerfile`.

Polecenie `image` określa nazwę obrazu, który zostanie utworzony po zakończeniu procesu budowania.

Aby zbudować i uruchomić kontenery, należy wywołać polecenie `docker-compose up` w katalogu, w którym znajduje się plik docker-compose.yml.

Jeśli chcesz zbudować obrazy bez uruchamiania ich jako kontenery, możesz użyć polecenia `docker-compose build` zamiast `docker-compose up`.