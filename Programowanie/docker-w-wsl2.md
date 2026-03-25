# Docker w WSL2

**Data:** 2024-09-11

---

**User:**

Czy mogę używać Docker w Ubuntu postawionym na wsl2 ale bez używania docker na Widows?

---

**Assistant:**

Tak, możesz korzystać z Dockera na Ubuntu uruchomionym na WSL2, ale do poprawnego działania Docker wymaga pewnej interakcji z systemem Windows. Obecnie Docker Desktop dla Windows oferuje integrację z WSL2, co pozwala na korzystanie z Dockera wewnątrz dystrybucji Linuxa (np. Ubuntu) uruchomionego na WSL2. Natomiast pełne uruchomienie Dockera wyłącznie w WSL2, bez Docker Desktop na Windows, jest bardziej złożone.

Aby to zrobić, musisz zainstalować Docker bezpośrednio w systemie Ubuntu uruchomionym w WSL2, ale musisz również uruchomić usługę Docker w tle (demon `dockerd`). Problem w tym, że WSL2 nie obsługuje natywnie systemu `systemd`, co utrudnia zarządzanie demonami.

Możesz spróbować rozwiązań typu:

1. **Instalacja Dockera w Ubuntu na WSL2:**
   - Zainstaluj Docker w WSL2 według standardowych instrukcji instalacyjnych dla Ubuntu.
   - Upewnij się, że zainstalowane są odpowiednie pakiety, takie jak `docker-ce` i `docker-ce-cli`.
   
2. **Uruchomienie demona dockerd w WSL2:**
   - Możesz spróbować ręcznie uruchamiać demona Dockera w WSL2 za pomocą komendy:
     ```
     sudo dockerd &
     ```
   - Jeśli napotkasz problemy z uruchamianiem Dockera, istnieją alternatywne rozwiązania, jak np. korzystanie z narzędzi do symulacji `systemd` (np. `genie`), które pozwalają na uruchomienie usług działających w tle.

3. **Dostęp do portów Dockera w WSL2:**
   - Kontenery uruchamiane w WSL2 są dostępne z poziomu systemu Windows, więc porty wystawiane przez kontenery mogą być bez problemu dostępne w przeglądarce lub innych narzędziach na Windowsie.

### Podsumowanie:
Docker w WSL2 może działać bez Docker Desktop, ale wymaga ręcznego uruchamiania demona Dockera lub obejścia braku wsparcia dla `systemd`. Aby uprościć konfigurację i zarządzanie Dockerem, zaleca się jednak korzystanie z Docker Desktop, który integruje się z WSL2.