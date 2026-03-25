# na moim kącie hostinger.com wiem jak się zalogować na VPS na konto root. Sprawdz

**Data:** 20 sty 2026, 11:50:32 CET

---

**User:**

na moim kącie hostinger.com wiem jak się zalogować na VPS na konto root. Sprawdziłem że nie ma utworzonego żadnego użytkownika typu mój nick. Czy powinienem logować się na roota?

---

**Gemini:**

Bezpośrednie logowanie się na konto **root** przez SSH oraz wykonywanie codziennych operacji administracyjnych z jego poziomu jest uznawane za **krytyczny błąd w sztuce (anti-pattern)** z punktu widzenia bezpieczeństwa i stabilności systemu.

Chociaż Hostinger (podobnie jak inni dostawcy VPS) domyślnie dostarcza dane do konta root, powinieneś traktować je jedynie jako punkt wyjścia do poprawnej konfiguracji serwera.

### Zagrożenia wynikające z pracy na koncie root

1. **Brak marginesu błędu:** Każda komenda wykonana jako root jest ostateczna. Pomyłka w składni (np. `rm -rf / path/to/dir` zamiast `rm -rf /path/to/dir`) może natychmiastowo i nieodwracalnie zniszczyć system plików.
2. **Podatność na ataki Brute-Force:** Nazwa użytkownika `root` jest znana każdemu atakującemu. Boty skanujące sieć celują niemal wyłącznie w port 22 i użytkownika root.
3. **Brak audytu:** Jeśli na serwerze pracuje więcej niż jedna osoba (lub proces), logi systemowe wskazujące na "root" nie pozwalają zidentyfikować, kto faktycznie wywołał dane polecenie.

---

### Zalecana ścieżka konfiguracji (Standard Hardening)

Zamiast korzystać z roota, powinieneś wdrożyć mechanizm **Privileged Access Management** oparty na systemowym narzędziu `sudo`.

#### 1. Utworzenie nowego użytkownika

Zaloguj się jako root po raz ostatni i stwórz własne konto:

```
# Create a new user
adduser <your_nickname>

# Add the user to the 'sudo' group (on Ubuntu/Debian)
usermod -aG sudo <your_nickname>
```

#### 2. Konfiguracja kluczy SSH (Ed25519)

Hasła są podatne na ataki typu brute-force. Najbezpieczniejszą metodą jest autentykacja kluczem publicznym. Wygeneruj klucz na swoim komputerze lokalnym:

```
# Run this on your local machine
ssh-keygen -t ed25519 -C "your_email@example.com"

# Copy the public key to your VPS
ssh-copy-id <your_nickname>@<server_ip>
```

#### 3. Zabezpieczenie demona SSH

Po upewnieniu się, że możesz zalogować się na nowe konto i użyć `sudo -i`, należy zmodyfikować plik `/etc/ssh/sshd_config`, aby zablokować dostęp dla roota oraz logowanie hasłem.

```
# Edit the SSH configuration file
sudo nano /etc/ssh/sshd_config
```

Ustaw następujące dyrektywy:

- `PermitRootLogin no` – blokuje logowanie na konto root przez SSH.
- `PasswordAuthentication no` – wymusza logowanie wyłącznie za pomocą kluczy SSH.
- `PubkeyAuthentication yes` – upewnia się, że klucze są akceptowane.

Po wprowadzeniu zmian zrestartuj usługę:

```
sudo systemctl restart ssh
```

---

### Dlaczego `sudo` jest lepsze niż `su`?

Używając `sudo`, pracujesz w kontekście ograniczonego użytkownika, a uprawnienia administracyjne podnosisz tylko dla konkretnych, świadomych operacji.

| Cecha | Konto Root | Użytkownik z Sudo |
| --- | --- | --- |
| **Bezpieczeństwo SSH** | Wysokie ryzyko (znany login) | Niskie ryzyko (unikalny login) |
| **Odporność na błędy** | Zerowa | Średnia (wymaga prefiksu `sudo`) |
| **Logowanie działań** | Trudne do śledzenia | Pełny log w `/var/log/auth.log` |
| **Zasada najmniejszych uprawnień** | Złamana | Zachowana |

W zaawansowanych środowiskach (np. produkcyjne klastry Kubernetes czy systemy CI/CD) bezpośredni dostęp do powłoki roota jest często całkowicie wyłączony, a wszelkie zmiany odbywają się poprzez narzędzia Infrastructure as Code (Terraform, Ansible), co eliminuje czynnik ludzkich błędów przy manualnym wpisywaniu komend.

Czy chcesz, abym pomógł Ci teraz przygotować skrypt w Bashu, który automatycznie wykona te kroki konfiguracyjne na Twoim nowym serwerze?