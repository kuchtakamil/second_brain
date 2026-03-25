# Ustawienie LIQUIBASE_HOME w macOS

**Data:** 2025-03-28

---

**User:**

W macos mam komunikat 
You should set the environment variable LIQUIBASE_HOME to
  /Users/kamil.kuchta/homebrew/opt/liquibase/libexec

---

**Assistant:**

Masz dwie opcje, aby ustawić zmienną środowiskową `LIQUIBASE_HOME` w macOS:  

### 1️⃣ Tymczasowo (dla bieżącej sesji terminala)  
Jeśli chcesz ustawić ją tylko na czas działania terminala, wpisz:  
```sh
export LIQUIBASE_HOME=/Users/kamil.kuchta/homebrew/opt/liquibase/libexec
```
To ustawienie zniknie po zamknięciu terminala.  

---

### 2️⃣ Na stałe (dla wszystkich sesji terminala)  
Jeśli chcesz, żeby zmienna była dostępna zawsze, dodaj ją do swojego pliku konfiguracyjnego powłoki:

#### Jeśli używasz **zsh** (domyślna powłoka w macOS):
```sh
echo 'export LIQUIBASE_HOME=/Users/kamil.kuchta/homebrew/opt/liquibase/libexec' >> ~/.zshrc
source ~/.zshrc
```

#### Jeśli używasz **bash**:
```sh
echo 'export LIQUIBASE_HOME=/Users/kamil.kuchta/homebrew/opt/liquibase/libexec' >> ~/.bashrc
source ~/.bashrc
```

Teraz `LIQUIBASE_HOME` będzie ustawione przy każdym uruchomieniu terminala.  

Sprawdź, czy działa, wpisując:  
```sh
echo $LIQUIBASE_HOME
```