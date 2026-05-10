# Różnica między `docker exec -it` a `docker attach`

## Krótkie podsumowanie

Główna różnica między tymi dwiema komendami polega na tym, do jakiego procesu wewnątrz kontenera jesteś podłączany:

- **`docker exec -it <container> sh`** uruchamia zupełnie **nowy proces** (w tym przypadku powłokę `sh`) wewnątrz działającego kontenera.
- **`docker attach <container>`** podłącza Twój terminal do **głównego procesu** kontenera (PID 1), czyli do tego uruchomionego przez komendę `ENTRYPOINT` lub `CMD`.

## Dlaczego jest to ważne / Kiedy stosować

Zrozumienie tej różnicy pozwala uniknąć bardzo częstego i niebezpiecznego błędu: przypadkowego "zabicia" całego serwisu (kontenera) przy próbie wyjścia z terminala.

- **Kiedy używać `docker exec`?**
  Gdy musisz wejść do działającego kontenera "z boku", np. aby przejrzeć pliki, sprawdzić konfigurację sieci, odczytać statystyki wewnętrzne, czy odpalić skrypt debugujący. Nie zakłóca on głównego procesu.
- **Kiedy używać `docker attach`?**
  Gdy chcesz wejść w interakcję ze standardowym wejściem (stdin) lub wyjściem (stdout) **głównego procesu** (np. chcąc śledzić na żywo logi lub w rzadkich przypadkach przekazywać do niego komendy, jeśli to aplikacja REPL). Często jednak do przeglądania logów bezpieczniej jest używać `docker logs -f <container>`.

## Jak to działa (przykłady)

### `docker exec -it <mycontainer> sh`

Flagi:
- `-i` (interactive) – pozwala na interakcję z nowym procesem, utrzymując otwarte STDIN.
- `-t` (tty) – allokuje pseudo-terminal (dzięki temu masz np. prompt i historię wspartą strzałkami).

**Działanie:** Wyobraź to sobie jak zalogowanie się przez SSH do pracującej maszyny (z perspektywy izolacji). Uruchamiasz nową sesję `sh`, a proces główny (np. serwer Nginx) działa całkowicie niezależnie.
**Wyjście:** Wpisanie `exit` lub wciśnięcie `Ctrl+D` zamyka powłokę `sh`, ale **kontener działa nadal bez zakłóceń**.

```bash
# Wejście do kontenera z obsługą Basha
docker exec -it my-nginx-container bash

# Po wejściu możesz przeglądać pliki
root@1a2b3c4d5e:/# ls /etc/nginx/
```

### `docker attach <mycontainer>`

Podłączasz swój lokalny terminal bezprośrednio do strumieni głównego procesu zdefiniowanego przy starcie kontenera (PID 1).

**Niebezpieczeństwo podłączenia (`attach`):** 
Ponieważ jesteś zapięty do głównego procesu, jeśli zechcesz z niego wyjść używając `Ctrl+C`, w rzeczywistości wyślesz sygnał `SIGINT`/`SIGTERM` przerwania do aplikacji (PID 1) i tym samym **zamkniesz cały kontener!**

Aby wyjść ("odłączyć się") z procesu nie zatrzymując przy tym kontenera, musisz użyć specjalnej sekwencji ewakuacyjnej (detach sequence):  
👉 **`Ctrl + P`, a następnie `Ctrl + Q`**.

```bash
# Podłączenie do głównego procesu
docker attach my-nginx-container
# (Zależnie od aplikacji, teraz mogą zacząć wylatywać logi prosto w Twój terminal)
```

## Podobne tematy
- [Uprawnienia w Dockerze](docker-permissions.md)
- [Przeglądanie logów Dockera](przegladanie_logow.md)
