# Ustawienie JAVA_HOME przez SDKMAN

**Data:** 2025-03-28

---

**User:**

chcę używając sdkman ustawić zmienną java_home

---

**Assistant:**

SDKMAN! automatycznie ustawia zmienną środowiskową `JAVA_HOME`, ale jeśli chcesz ją ręcznie sprawdzić lub ustawić, oto jak to zrobić:

### 1. Sprawdzenie aktualnej wersji Javy w SDKMAN!:
```sh
sdk current java
```
Powinno zwrócić coś takiego:
```
Using java version 17.0.8-tem
```

### 2. Automatyczne ustawienie `JAVA_HOME`
SDKMAN! automatycznie ustawia `JAVA_HOME`, ale jeśli chcesz ręcznie zobaczyć jej wartość:
```sh
echo $JAVA_HOME
```

Jeśli jednak `JAVA_HOME` nie jest ustawione poprawnie, możesz wymusić jego ustawienie.

### 3. Ręczne ustawienie `JAVA_HOME`
Jeśli chcesz ręcznie wymusić ustawienie `JAVA_HOME`, dodaj to do swojego `.bashrc`, `.bash_profile`, `.zshrc` lub innego pliku konfiguracyjnego powłoki:

```sh
export JAVA_HOME=$(sdk home java)
export PATH=$JAVA_HOME/bin:$PATH
```

Po zapisaniu zmian uruchom:
```sh
source ~/.bashrc  # lub `source ~/.zshrc` jeśli używasz Zsh
```

### 4. Ustawienie konkretnej wersji Javy jako domyślnej:
Jeśli masz wiele wersji Javy i chcesz ustawić jedną jako domyślną:
```sh
sdk default java 17.0.8-tem  # Wstaw odpowiednią wersję
```

Albo jeśli chcesz ustawić wersję tylko dla aktualnej sesji:
```sh
sdk use java 17.0.8-tem
```

Po tym powinieneś mieć poprawnie ustawioną zmienną `JAVA_HOME`. Sprawdź to jeszcze raz:
```sh
echo $JAVA_HOME
java -version
```

---

**User:**

Co w bash oznacza pushd $PRODCAT_REPO_PATH

---

**Assistant:**

W Bashu polecenie:  

```sh
pushd $PRODCAT_REPO_PATH
```
oznacza:  

1. **`pushd`** – polecenie, które zapisuje bieżący katalog na stosie katalogów i przechodzi do nowego katalogu. Jest to alternatywa dla `cd`, ale z możliwością powrotu do poprzedniego katalogu za pomocą `popd`.

2. **`$PRODCAT_REPO_PATH`** – zmienna środowiskowa, która zawiera ścieżkę do katalogu. Wartość tej zmiennej jest używana jako docelowy katalog, do którego `pushd` przechodzi.

### Jak to działa?
- Jeśli np. `PRODCAT_REPO_PATH="/home/user/project"`, to  
  ```sh
  pushd $PRODCAT_REPO_PATH
  ```
  spowoduje przejście do `/home/user/project`, ale jednocześnie zapisze poprzedni katalog na stosie.

- Możesz wrócić do poprzedniego katalogu za pomocą:
  ```sh
  popd
  ```
  co zdejmie go ze stosu i wróci do katalogu, w którym znajdowałeś się przed `pushd`.

### Zaleta `pushd` nad `cd`
- Możesz przełączać się między katalogami i wracać do poprzednich lokalizacji w bardziej elastyczny sposób niż używając `cd` i `cd -`.

Przykład użycia:
```sh
pushd /var/log
# Robisz coś w /var/log
pushd /etc
# Teraz jesteś w /etc, ale /var/log jest na stosie
popd  # Wraca do /var/log
popd  # Wraca do katalogu początkowego
```

---

**User:**

Wyjaśnij docker-compose up -d --wait && time liquibase

---

**Assistant:**

### Polecenie:
```sh
docker-compose up -d --wait && time liquibase
```
Składa się z dwóch części:

---

### 1. `docker-compose up -d --wait`
To polecenie uruchamia kontenery zdefiniowane w `docker-compose.yml`.

- **`up`** – Tworzy i uruchamia kontenery na podstawie `docker-compose.yml`.
- **`-d`** – Uruchamia kontenery w tle (ang. *detached mode*).
- **`--wait`** – Opcja dostępna w nowszych wersjach Docker Compose. Powoduje, że `docker-compose up` nie zwróci kontroli, dopóki wszystkie kontenery nie będą gotowe do użycia (tj. zdrowe, jeśli mają skonfigurowane `healthcheck`).

Dzięki `--wait`, kolejne polecenie (`time liquibase`) wykona się dopiero, gdy kontenery będą w pełni gotowe.

---

### 2. `&& time liquibase`
To drugie polecenie uruchomi się tylko jeśli `docker-compose up -d --wait` zakończy się sukcesem (bez błędów).

- **`liquibase`** – Narzędzie do zarządzania migracjami bazy danych.
- **`time`** – Mierzy czas wykonania polecenia `liquibase` i na końcu wypisuje statystyki (`real`, `user`, `sys`), np.:
  ```
  real    0m12.345s
  user    0m0.456s
  sys     0m0.123s
  ```

---

### Podsumowanie
To polecenie:
1. Uruchamia usługi Dockera w tle i czeka, aż będą gotowe.
2. Gdy usługi są gotowe, wykonuje migracje bazy danych za pomocą Liquibase.
3. Mierzy czas wykonania migracji.

To dobre rozwiązanie, jeśli Liquibase wymaga gotowej bazy danych w kontenerze przed rozpoczęciem pracy.