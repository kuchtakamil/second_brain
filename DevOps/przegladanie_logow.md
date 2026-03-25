# Przeglądanie logów w Dockerze i Docker Compose

Przeglądanie logów to nieodłączny element pracy z aplikacjami kontenerowymi. Poniżej znajduje się zestawienie najlepszych praktyk i najwygodniejszych sposobów na pracę z logami w ekosystemie Dockera.

## Wyjaśnienie Twojego polecenia

Polecenie, z którym się ostatnio spotkałeś:

```bash
docker compose -f /opt/stock_market_dd/docker-compose.yml logs
```

Oto co oznaczają jego poszczególne elementy:

* **`docker compose`** - wywołanie narzędzia (wtyczki CLI) do zarządzania aplikacjami składającymi się z wielu kontenerów. (W starszych wersjach zapisywane z myślnikiem jako `docker-compose`).
* **`-f /opt/stock_market_dd/docker-compose.yml`** - (od *file*) flaga ta wskazuje dokładną ścieżkę do pliku konfiguracyjnego. Dzięki temu **nie musisz znajdować się w katalogu z aplikacją**, aby zarządzać jej kontenerami. Możesz odpalić to polecenie z dowolnego miejsca w systemie.
* **`logs`** - komenda nakazująca wyświetlenie logów ze wszystkich serwisów (kontenerów) połączonych w tym pliku.

**Jak ulepszyć to polecenie?**
Samo `logs` wypisze na ekran wszystkie dotychczasowe logi i po prostu zakończy działanie. Aby przeglądać logi **na żywo**, wystarczy dodać flagę `-f` (od *follow*) na samym końcu:

```bash
docker compose -f /opt/stock_market_dd/docker-compose.yml logs -f
```

---

## Wygodne przeglądanie logów - najlepsze praktyki

### 1. Śledzenie logów na żywo (Follow)

Aby konsola nie zamykała się po wypisaniu ostatnich zdarzeń i na bieżąco "nasłuchiwała" i rysowała nowe wpisy we wbudowanych aplikacjach, używaj flagi `-f` (lub `--follow`):

```bash
docker logs -f <nazwa_kontenera>
# lub dla docker compose:
docker compose logs -f
```

### 2. Ograniczanie liczby linii (Tail)

Kontenery często działają bez przerwy miesiącami, generując gigabajty logów. Aby nie pobierać historii tysięcy starych linii tekstu, użyj flagi `--tail`, która wyświetli na start jedynie `X` ostatnich wpisów:

```bash
docker logs --tail 100 -f <nazwa_kontenera>
# Pokaże 100 ostatnich linii i "zawiśnie" śledząc logi dalej na żywo
```

### 3. Dodawanie znaczników czasu (Timestamps)

Jeśli Twoja aplikacja loguje np. samo "Server started", a Ty nie wiesz, kiedy dokładnie się to stało, Docker może wymusić doklejanie daty i godziny po swojej stronie. Użyj flagi `-t` (lub `--timestamps`):

```bash
docker logs -t <nazwa_kontenera>
```

Możesz swobodnie łączyć flagi! Np: `docker logs -f --tail 50 -t my_app`

### 4. Filtrowanie logów konkretnego serwisu w Docker Compose

Jeśli Twój plik `docker-compose.yml` uruchamia całe środowisko (np. bazę danych PostgreSQL, Redis, Backend i Frontend), wpisanie samego `docker compose logs` pokaże Ci ogromny wodospad złączonego tekstu ze wszystkich tych komponentów jednocześnie (choć w miarę możliwości w różnych kolorach).

Aby przeczytać logi pochodzące tylko od jednego konkretnego kontenera (tzw. usługi), po prostu dopisz jego nazwę używaną wewnątrz pliku yml:

```bash
# np. dla serwisu zapisanego pod kluczem 'backend':
docker compose logs -f backend
```

### 5. Wyszukiwanie błędów (Grep)

Często chcemy znaleźć tylko interesujące nas wiersze (np. zawierające słowo "Error" czy "Exception"). Standardowo osiągamy to wysyłając (przepuszczając wężykiem `|`) wyjście z dockera do linuxowego polecenia `grep`:

```bash
docker logs <nazwa_kontenera> | grep -i "error"
```

*(Uwaga: takie wyszukiwanie sprawdza się najlepiej dla przeglądania dotychczasowych logów bez używania flagi śledzącej `-f`)*

---

### Bonus: Interfejs graficzny w terminalu (Lazydocker)

Jeżeli sporo pracujesz z Dockerem na co dzień, bardzo polecam darmowe narzędzie o nazwie **lazydocker** [link to GitHub](https://github.com/jesseduffield/lazydocker).
Jest to niesamowicie wygodny "okienkowy" manager otwierany bezpośrednio z terminala. Pozwala on strzałkami przeskakiwać między kontenerami, od razu widzieć na żywo ich logi w dużym oknie, monitorować zużycie RAM/CPU oraz wyklikiwać (lub odpalać skrótami klawiszowymi) opcje takie jak restart. Znacznie zmniejsza to potrzebę wpisywania długich, wieloczłonowych komend do zarządzania logami logów.
