# już dodałem użytkownika do docker. Jak w takim razie to odwrócić i użyć Rootless

**Data:** 20 sty 2026, 12:30:20 CET

---

**User:**

już dodałem użytkownika do docker. Jak w takim razie to odwrócić i użyć Rootless Docker?

---

**Gemini:**

Przejście na **Rootless Docker** to doskonały krok w stronę profesjonalnego hardeningu systemu. W tym trybie daemon Docker oraz kontenery działają wewnątrz **User Namespace**, co oznacza, że nawet jeśli proces w kontenerze zostanie „przełamany”, atakujący zyskuje jedynie uprawnienia nieuprzywilejowanego użytkownika na hoście.

### 1. Cofnięcie uprawnień (Revert)

Najpierw usuń swojego użytkownika z grupy `docker`, aby zlikwidować lukę bezpieczeństwa typu *root-equivalent*.

```
# Remove user from docker group
sudo gpasswd -d $USER docker

# Verify group membership (docker should be gone)
groups
```

*Uwaga: Zmiana zadziała po ponownym zalogowaniu (lub użyciu `newgrp`), ale na razie przejdź do kolejnych kroków.*

### 2. Instalacja zależności

Rootless Docker wymaga narzędzi do mapowania UID/GID oraz obsługi sieci w przestrzeni użytkownika.

```
# Install dependencies for Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y dbus-user-session uidmap slirp4netns fuse-overlayfs
```

Upewnij się, że Twój użytkownik ma przypisane zakresy sub-UID i sub-GID (standard w nowoczesnych dystrybucjach):

```
grep $USER /etc/subuid
grep $USER /etc/subgid
```

Powinieneś zobaczyć coś w stylu: `twoj_nick:100000:65536`.

### 3. Wyłączenie systemowego Daemona (Opcjonalne)

Jeśli nie planujesz używać dockera systemowego (root), warto go zatrzymać, aby nie marnować zasobów:

```
sudo systemctl disable --now docker.service docker.socket
```

### 4. Instalacja Rootless Docker

Uruchom oficjalny skrypt instalacyjny dostarczony przez Docker. Skrypt ten zainstaluje binarne pliki w Twoim katalogu domowym (`~/bin`).

```
# Run the installation script
curl -fsSL https://get.docker.com/rootless | sh
```

### 5. Konfiguracja zmiennych środowiskowych

Musisz poinstruować klienta `docker`, aby komunikował się z gniazdem (socket) w Twoim katalogu domowym, a nie z `/var/run/docker.sock`.

Dodaj poniższe linie do pliku `~/.bashrc`:

```
# Append to ~/.bashrc
export PATH=$HOME/bin:$PATH
export DOCKER_HOST=unix://$XDG_RUNTIME_DIR/docker.sock
```

Następnie przeładuj konfigurację:

```
source ~/.bashrc
```

### 6. Włączenie autostartu (Linger)

Na VPS domyślnie sesja użytkownika (i jego procesy) są zabijane po wylogowaniu z SSH. Aby kontenery działały w tle 24/7, musisz włączyć funkcję **linger** dla swojego konta:

```
# Enable lingering for the user
sudo loginctl enable-linger $USER
```

### 7. Uruchomienie i test

Uruchom serwis Dockera w trybie użytkownika (używamy `systemctl --user`, nie `sudo`!):

```
# Start the user-level docker service
systemctl --user start docker
systemctl --user enable docker

# Verification
docker run hello-world
```

### Kluczowe różnice i ograniczenia Rootless

| Funkcja | Rootless Docker | Standard Docker |
| --- | --- | --- |
| **Porty uprzywilejowane** | Nie można mapować portów < 1024 (np. 80, 443) bez dodatkowej konfiguracji `setcap`. | Pełny dostęp do wszystkich portów. |
| **Storage Driver** | Zazwyczaj `fuse-overlayfs` (wolniejszy niż natywny). | Natywny `overlay2`. |
| **Networking** | Przez `slirp4netns` (nieco mniejsza wydajność sieci). | Bezpośredni mostek (bridge) L2. |
| **Bezpieczeństwo** | Bardzo wysokie (izolacja jądra przez namespaces). | Wysokie, ale podatne na eskalację uprawnień. |

**Pro-tip dla portów 80/443:** Jeśli chcesz uruchomić serwer WWW na standardowych portach w trybie Rootless, najbezpieczniej jest użyć Reverse Proxy (np. Nginx zainstalowany systemowo przez `apt`) lub pozwolić nieuprzywilejowanym procesom na bindowanie niskich portów komendą:
`sudo sysctl net.ipv4.ip_unprivileged_port_start=80`.

Czy chcesz, abym pomógł Ci skonfigurować automatyczne odświeżanie kontenerów za pomocą **Watchtower** w tym nowym środowisku rootless?