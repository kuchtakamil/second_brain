# Switch user without bash

**Data:** 2024-06-27

---

**User:**

W linux jestem zalogowany na root. Robię su dconnectadmin. Czy jest możliwe aby po przełączeniu się na użytkownika dconnectadmin nie był uruchamiany bash?

---

**Assistant:**

Tak, jest możliwe, aby po przełączeniu się na użytkownika `dconnectadmin` nie był uruchamiany `bash`. Można to zrobić na kilka sposobów, w zależności od tego, jaki shell chcesz uruchomić zamiast `bash` lub jakie polecenie chcesz wykonać po przełączeniu.

1. **Użycie opcji `-s` do wskazania innego shella:**

   Możesz użyć opcji `-s` z poleceniem `su`, aby wskazać inny shell do uruchomienia. Na przykład, jeśli chcesz uruchomić `/bin/sh` zamiast `bash`:

   ```sh
   su -s /bin/sh dconnectadmin
   ```

2. **Wykonanie konkretnego polecenia bez uruchamiania interaktywnego shella:**

   Możesz również użyć `su` do wykonania konkretnego polecenia zamiast uruchamiania interaktywnego shella. Na przykład, jeśli chcesz uruchomić `uptime` jako `dconnectadmin`:

   ```sh
   su -c "uptime" dconnectadmin
   ```

3. **Zmiana domyślnego shella dla użytkownika:**

   Możesz zmienić domyślny shell dla użytkownika `dconnectadmin`, edytując plik `/etc/passwd`. Znajdź linię odpowiadającą użytkownikowi `dconnectadmin` i zmień ścieżkę do shella. Na przykład:

   ```plaintext
   dconnectadmin:x:1001:1001::/home/dconnectadmin:/bin/sh
   ```

   Zamiast `/bin/bash`, możesz ustawić `/bin/sh` lub dowolny inny shell.

4. **Korzystanie z `sudo` do uruchomienia polecenia jako inny użytkownik:**

   Możesz również użyć `sudo` do uruchomienia polecenia jako `dconnectadmin` bez przełączania na tego użytkownika w interaktywnym shellu. Na przykład:

   ```sh
   sudo -u dconnectadmin uptime
   ```

Każda z tych metod pozwoli na uzyskanie efektu, w którym po przełączeniu się na użytkownika `dconnectadmin` nie zostanie uruchomiony `bash`. Wybierz metodę, która najlepiej pasuje do Twoich potrzeb.

---

**User:**

czy zawartość pliku .profile jest uruchamiana tylko w przypadku gdy użytkownik korzysta z bash?

---

**Assistant:**

Zawartość pliku `.profile` jest uruchamiana przez sh-compatible powłoki przy logowaniu użytkownika. Domyślnie, `bash` oraz inne powłoki kompatybilne z `sh` uruchamiają ten plik. Jednakże, istnieją różne pliki startowe, które są wykorzystywane przez różne powłoki. Oto kilka szczegółów:

1. **Bash:**
   - **Interaktywna sesja logowania**: `bash` uruchomi plik `/etc/profile` (jeśli istnieje) oraz pierwsze istniejące pliki z: `~/.bash_profile`, `~/.bash_login`, lub `~/.profile`.
   - **Interaktywna sesja nie-logowania**: `bash` uruchomi plik `~/.bashrc`.
   - **Interaktywna sesja logowania dla root**: `bash` uruchomi `~/.profile` zamiast `~/.bash_profile`.

2. **sh, dash, i inne powłoki kompatybilne z POSIX**:
   - Te powłoki uruchamiają plik `/etc/profile` oraz `~/.profile` przy logowaniu użytkownika.

3. **Zsh:**
   - **Interaktywna sesja logowania**: `zsh` uruchomi plik `/etc/zprofile`, `~/.zprofile`, a następnie `~/.zshrc`.

4. **Ksh (Korn Shell):**
   - **Interaktywna sesja logowania**: `ksh` uruchomi plik `/etc/profile` oraz `~/.profile`.

### Podsumowanie

- **`.profile`** jest uruchamiany przez `sh` oraz `bash` w sesji logowania.
- **`.bashrc`** jest uruchamiany przez `bash` w interaktywnej sesji nie-logowania.
- Inne powłoki, takie jak `zsh` i `ksh`, używają własnych specyficznych plików startowych.

Aby `.profile` było uruchamiane przez `bash`, musisz być w sesji logowania, a `bash` nie może znaleźć `~/.bash_profile` ani `~/.bash_login`.

Jeśli chcesz upewnić się, że konkretne ustawienia są zawsze ładowane niezależnie od rodzaju powłoki lub sesji, możesz umieścić je w odpowiednich plikach startowych dla danej powłoki.