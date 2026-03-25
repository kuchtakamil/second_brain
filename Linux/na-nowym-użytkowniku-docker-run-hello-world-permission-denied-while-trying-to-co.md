# Na nowym użytkowniku: docker run hello-world permission denied while trying to c

**Data:** 20 sty 2026, 12:27:44 CET

---

**User:**

Na nowym użytkowniku:
docker run hello-world
permission denied while trying to connect to the docker API at unix:///var/run/docker.sock

---

**Gemini:**

Błąd ten wynika z faktu, że demon Docker (proces tła zarządzający kontenerami) domyślnie komunikuje się przez gniazdo UNIXowe `/var/run/docker.sock`. Właścicielem tego gniazda jest użytkownik `root`, a dostęp do niego ma jedynie grupa `docker`. Nowo utworzony użytkownik nie posiada domyślnie tych uprawnień.

Oto jak rozwiązać ten problem w sposób poprawny technicznie:

### 1. Dodanie użytkownika do grupy `docker`

Musisz dodać swój profil do grupy systemowej `docker`. Użyj do tego polecenia `usermod`:

```
# Add your current user to the docker group
sudo usermod -aG docker $USER
```

- `-a` (append) – dodaje użytkownika do grupy bez usuwania go z innych grup.
- `-G` (groups) – określa grupę docelową.
- `$USER` – zmienna środowiskowa przechowująca nazwę aktualnie zalogowanego użytkownika.

### 2. Aktywacja zmian w bieżącej sesji

Zmiany w grupach użytkownika są zaczytywane dopiero przy logowaniu. Zamiast wylogowywać się i logować ponownie, możesz wymusić przeładowanie grup dla bieżącej powłoki (shell):

```
# Apply group changes to the current session
newgrp docker
```

### 3. Weryfikacja uprawnień do gniazda

Możesz sprawdzić, kto ma uprawnienia do pliku gniazda, aby zrozumieć mechanizm blokady:

```
ls -l /var/run/docker.sock
```

Wynik powinien wyglądać mniej więcej tak:
`srw-rw---- 1 root docker 0 Jan 20 12:00 /var/run/docker.sock`

Litera `s` oznacza socket, a uprawnienia `rw` dla grupy `docker` potwierdzają, że członkostwo w tej grupie rozwiązuje problem bez używania `sudo`.

---

### Istotna uwaga dot. bezpieczeństwa (Security Implication)

Dodanie użytkownika do grupy `docker` jest **równoważne z nadaniem mu uprawnień roota** (root equivalent). Wynika to z faktu, że Docker pozwala na montowanie dowolnych katalogów z hosta w kontenerze. Użytkownik z grupy `docker` może uruchomić kontener montując w nim systemowy rootfs:

```
# Example of potential privilege escalation (educational purposes)
docker run -v /:/host -it alpine sh
```

Dzięki temu ma on pełny dostęp do odczytu i zapisu wszystkich plików systemowych hosta (np. `/etc/shadow`). W środowiskach produkcyjnych, gdzie bezpieczeństwo jest priorytetem, warto rozważyć tryb **Rootless Docker**, który pozwala na uruchamianie demona bez uprawnień roota.

### 4. Test działania

Po wykonaniu powyższych kroków, komenda powinna przejść pomyślnie bez `sudo`:

```
docker run hello-world
```

Czy chciałbyś, abym przedstawił instrukcję konfiguracji **Docker Rootless**, aby jeszcze bardziej utwardzić (harden) Twój system VPS?