# Automatically Run Program After Login

**Data:** 2024-06-27

---

**User:**

W systemie linux chcę aby po zalogowaniu się na danego użytkownika w konsoli, uruchamiany był konkretny program o nazwie am. Jak to zrobić?

---

**Assistant:**

Aby uruchomić konkretny program (w tym przypadku `am`) automatycznie po zalogowaniu się na użytkownika w systemie Linux, można skorzystać z kilku metod w zależności od powłoki, której używa użytkownik. Poniżej przedstawiam najpopularniejsze sposoby:

### 1. Edycja pliku `.bashrc` lub `.profile`
Jeśli użytkownik korzysta z powłoki `bash`, można dodać odpowiednią komendę do pliku `.bashrc` lub `.profile` w katalogu domowym użytkownika.

1. Otwórz plik `.bashrc` w edytorze tekstowym:
   ```sh
   nano ~/.bashrc
   ```

2. Dodaj komendę do uruchomienia programu na końcu pliku:
   ```sh
   am
   ```

3. Zapisz plik i wyjdź z edytora (dla `nano` jest to kombinacja klawiszy `Ctrl+X`, następnie `Y`, a potem `Enter`).

4. Aby natychmiast zastosować zmiany, wykonaj:
   ```sh
   source ~/.bashrc
   ```

Podobnie można dodać tę komendę do pliku `.profile`:
   ```sh
   nano ~/.profile
   ```
   a następnie dodać `am` na końcu pliku i zapisać zmiany.

### 2. Edycja pliku `.bash_profile`
Jeśli istnieje plik `.bash_profile` w katalogu domowym użytkownika, można również tam dodać komendę:

1. Otwórz plik `.bash_profile`:
   ```sh
   nano ~/.bash_profile
   ```

2. Dodaj komendę:
   ```sh
   am
   ```

3. Zapisz zmiany i zamknij edytor.

4. Aby natychmiast zastosować zmiany, wykonaj:
   ```sh
   source ~/.bash_profile
   ```

### 3. Edycja pliku `.zshrc`
Jeśli użytkownik korzysta z powłoki `zsh`, dodaj komendę do pliku `.zshrc`:

1. Otwórz plik `.zshrc`:
   ```sh
   nano ~/.zshrc
   ```

2. Dodaj komendę:
   ```sh
   am
   ```

3. Zapisz zmiany i zamknij edytor.

4. Aby natychmiast zastosować zmiany, wykonaj:
   ```sh
   source ~/.zshrc
   ```

### 4. Użycie skryptu `~/.bash_login`
Jeśli pliki `.bashrc` lub `.profile` są już zbyt obciążone, można stworzyć osobny plik `~/.bash_login`:

1. Stwórz lub otwórz plik `~/.bash_login`:
   ```sh
   nano ~/.bash_login
   ```

2. Dodaj komendę:
   ```sh
   am
   ```

3. Zapisz zmiany i zamknij edytor.

### 5. Systemd User Service
Alternatywnie, można utworzyć usługę `systemd` dla użytkownika:

1. Stwórz katalog dla usług użytkownika, jeśli jeszcze nie istnieje:
   ```sh
   mkdir -p ~/.config/systemd/user
   ```

2. Stwórz plik usługi, np. `am.service`:
   ```sh
   nano ~/.config/systemd/user/am.service
   ```

3. Dodaj następujące treści do pliku:
   ```ini
   [Unit]
   Description=Uruchamianie programu am po zalogowaniu

   [Service]
   ExecStart=/usr/bin/am

   [Install]
   WantedBy=default.target
   ```

4. Zapisz zmiany i zamknij edytor.

5. Włącz i uruchom usługę:
   ```sh
   systemctl --user enable am.service
   systemctl --user start am.service
   ```

### Podsumowanie
Wybór metody zależy od preferencji oraz używanej powłoki. Edycja plików `.bashrc`, `.profile`, `.bash_profile`, `.zshrc` jest najprostszym rozwiązaniem dla większości przypadków, natomiast użycie `systemd` zapewnia większą kontrolę nad usługą.

---

**User:**

czy sposób z edycją pliku .bashrc lub pliku .profile zadziała gdy na zalogowanym użytkowniku nie będzie działał bash?

---

**Assistant:**

Jeśli na zalogowanym użytkowniku nie będzie działał `bash`, edycja plików `.bashrc` lub `.profile` nie zadziała. W takim przypadku trzeba dostosować rozwiązanie do powłoki, której używa użytkownik, lub skorzystać z innej metody, która nie zależy od konkretnej powłoki. Oto kilka alternatywnych metod:

### 1. Edycja pliku `.zshrc` dla `zsh`
Jeśli użytkownik korzysta z powłoki `zsh`, należy edytować plik `.zshrc`:

1. Otwórz plik `.zshrc`:
   ```sh
   nano ~/.zshrc
   ```

2. Dodaj komendę:
   ```sh
   am
   ```

3. Zapisz zmiany i zamknij edytor.

### 2. Edycja pliku `.cshrc` dla `csh` lub `tcsh`
Jeśli użytkownik korzysta z powłoki `csh` lub `tcsh`, należy edytować plik `.cshrc`:

1. Otwórz plik `.cshrc`:
   ```sh
   nano ~/.cshrc
   ```

2. Dodaj komendę:
   ```csh
   am
   ```

3. Zapisz zmiany i zamknij edytor.

### 3. Użycie `~/.xinitrc` dla sesji X
Jeśli użytkownik loguje się w środowisku graficznym korzystając z `startx` lub innej sesji X, można edytować plik `.xinitrc`:

1. Otwórz plik `.xinitrc`:
   ```sh
   nano ~/.xinitrc
   ```

2. Dodaj komendę przed uruchomieniem środowiska graficznego:
   ```sh
   am &
   ```

3. Zapisz zmiany i zamknij edytor.

### 4. Użycie `systemd` User Service
Niezależnie od powłoki, można użyć `systemd` do uruchamiania programu