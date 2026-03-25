# Zsh jako domyślny shell

**Data:** 2025-01-06

---

**User:**

Na ubuntu zainstalowałem zsh a później oh my zsh. Wydaję mi się że padło pytanie czy ustawić zsh jako domyślny shell. Odpowiedziałem tak, mimo to nadal domyślnie uruchamia się bash

---

**Assistant:**

Jeśli mimo konfiguracji i zgody na ustawienie Zsh jako domyślnego shella nadal uruchamia się Bash, warto sprawdzić kilka rzeczy:

### 1. Sprawdzenie bieżącego domyślnego shella
Uruchom polecenie:
```bash
echo $SHELL
```
To pokaże, jaki shell jest ustawiony jako domyślny.

### 2. Ustawienie Zsh jako domyślnego shella
Jeśli wynik powyższego polecenia wskazuje na Bash, możesz ustawić Zsh jako domyślny shell ręcznie:
```bash
chsh -s $(which zsh)
```
To polecenie zmieni domyślny shell użytkownika na Zsh.

### 3. Wylogowanie i ponowne zalogowanie
Zmiana domyślnego shella wymaga wylogowania i ponownego zalogowania użytkownika, aby zmiany zaczęły obowiązywać.

### 4. Sprawdzenie pliku `.bashrc`
Jeśli nadal uruchamia się Bash, upewnij się, że w pliku `~/.bashrc` (jeśli istnieje) nie ma poleceń wymuszających uruchomienie Basha. Możesz otworzyć ten plik w edytorze, np.:
```bash
nano ~/.bashrc
```
Usuń lub skomentuj wszystkie linie, które mogą włączać Bash.

### 5. Weryfikacja pliku `/etc/passwd`
Upewnij się, że w pliku `/etc/passwd` Zsh jest ustawiony jako domyślny shell:
```bash
cat /etc/passwd | grep $(whoami)
```
Powinno pojawić się coś w rodzaju:
```
username:x:1000:1000:Your Full Name:/home/username:/usr/bin/zsh
```
Jeśli na końcu widzisz `/bin/bash`, oznacza to, że domyślny shell nie został poprawnie zmieniony. W takim przypadku, możesz edytować ten plik (np. za pomocą `sudo nano /etc/passwd`) i ręcznie zmienić `/bin/bash` na `/usr/bin/zsh`.

### 6. Instalacja Zsh lub `oh-my-zsh` mogła mieć problem
Upewnij się, że Zsh jest poprawnie zainstalowany i znajduje się w lokalizacji oczekiwanej przez system:
```bash
which zsh
```
Powinno to zwrócić coś w rodzaju `/usr/bin/zsh`.

Jeśli dalej napotkasz problemy, daj znać – pomożemy debugować dalej!

---

**User:**

ok, problem rozwiązany.
Teraz widzę że po ustawieniu pewnego THEME wyświetla mi się
kamil@kamil-Legion-Pro-5-16IRX8:pts/0
jak to zmienić?

---

**Assistant:**

Aby zmienić sposób, w jaki nazwa użytkownika, hosta i terminala (np. `kamil@kamil-Legion-Pro-5-16IRX8:pts/0`) jest wyświetlana w Zsh, musisz dostosować **prompt**. Prompt jest definiowany w pliku konfiguracyjnym `~/.zshrc`, a w przypadku używania **Oh My Zsh** jest kontrolowany przez aktywny motyw (theme).

### 1. Edycja aktywnego motywu
Jeśli korzystasz z motywu Oh My Zsh, prompt jest definiowany w pliku motywu w katalogu `~/.oh-my-zsh/themes/`.

#### Krok 1: Sprawdzenie, który motyw jest aktywny
Otwórz plik `~/.zshrc`:
```bash
nano ~/.zshrc
```
Znajdź linię:
```bash
ZSH_THEME="theme_name"
```
`theme_name` to aktualnie używany motyw.

#### Krok 2: Edycja motywu
Przejdź do folderu z motywami:
```bash
cd ~/.oh-my-zsh/themes
```
Znajdź plik motywu (`theme_name.zsh-theme`) i otwórz go do edycji, np.:
```bash
nano theme_name.zsh-theme
```

Znajdź sekcję odpowiedzialną za prompt. Zazwyczaj będzie to zmienna `PROMPT` lub podobne (np. `RPROMPT` dla prawego promptu). Możesz ją dostosować według własnych potrzeb. 

Przykład uproszczonego promptu:
```zsh
PROMPT='%n@%m:%~$ '
```

- `%n` – nazwa użytkownika
- `%m` – skrócona nazwa hosta (np. `kamil-Legion-Pro`)
- `%~` – bieżący katalog
- `$` – symbol promptu (`#` dla root, `$` dla zwykłego użytkownika)

Jeśli chcesz np. usunąć nazwę hosta, zmień na:
```zsh
PROMPT='%n:%~$ '
```

### 2. Użycie narzędzia `p10k configure` (dla motywu Powerlevel10k)
Jeśli używasz motywu Powerlevel10k (bardzo popularny motyw z Oh My Zsh), możesz skonfigurować prompt za pomocą:
```bash
p10k configure
```
Ten kreator umożliwi dostosowanie wyświetlania użytkownika, hosta i innych elementów.

### 3. Bezpośrednia edycja pliku `~/.zshrc`
Jeśli chcesz ręcznie dostosować prompt bez edytowania motywu, możesz w pliku `~/.zshrc` dodać lub zmodyfikować linię:
```bash
PROMPT='%n:%~$ '
```
Po edycji zapisz plik i załaduj zmiany:
```bash
source ~/.zshrc
```

### 4. Przykłady promptów
- Minimalistyczny:
  ```zsh
  PROMPT='%~$ '
  ```
- Z pełną nazwą użytkownika i hosta:
  ```zsh
  PROMPT='%n@%m:%~$ '
  ```
- Z datą i godziną:
  ```zsh
  PROMPT='[%D{%H:%M:%S}] %n@%m:%~$ '
  ```

Jeśli nie wiesz, jak zmodyfikować swój motyw lub potrzebujesz konkretnej porady, daj znać, jaki motyw jest aktywny – dostosujemy prompt! 😊