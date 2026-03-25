# Instalacja sdkman w zsh

**Data:** 2025-08-31

---

**User:**

na ubuntu chcę zainstalować sdkman.
Gdy w konsoli uruchomie
source "$HOME/.sdkman/bin/sdkman-init.sh"
wtedy w tej konsoli dostępny jest sdkman, java itp.
ale w następnej nowootwartej konsoli już nie.
Korzystam z zsh i oh my zsh

---

**Assistant:**

Na Ubuntu z **zsh** i **oh-my-zsh** musisz zadbać, żeby `sdkman-init.sh` był automatycznie ładowany przy starcie powłoki.  

Domyślnie instalator **SDKMAN!** dodaje linijkę do `~/.bashrc`, ale skoro używasz `zsh`, to trzeba ją dopisać do `~/.zshrc`.  

### Rozwiązanie:
1. Otwórz swój plik konfiguracyjny zsh:  
   ```bash
   nano ~/.zshrc
   ```
2. Dodaj na końcu:
   ```bash
   export SDKMAN_DIR="$HOME/.sdkman"
   [[ -s "$SDKMAN_DIR/bin/sdkman-init.sh" ]] && source "$SDKMAN_DIR/bin/sdkman-init.sh"
   ```
3. Zapisz plik i załaduj zmiany:  
   ```bash
   source ~/.zshrc
   ```

Od teraz `sdk`, `java`, `maven` itp. powinny być dostępne w każdej nowej konsoli.  

---

Chcesz, żebym podał Ci też jak sprawdzić, czy `zsh` faktycznie czyta Twój `~/.zshrc` (bo czasem w połączeniu z oh-my-zsh są mylące przypadki)?