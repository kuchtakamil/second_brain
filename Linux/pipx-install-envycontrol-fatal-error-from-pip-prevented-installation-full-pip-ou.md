# pipx install envycontrol Fatal error from pip prevented installation. Full pip o

**Data:** 19 lis 2025, 17:52:49 CET

---

**User:**

pipx install envycontrol
Fatal error from pip prevented installation. Full pip output in file:
    /home/kamil/.local/state/pipx/log/cmd_2025-11-19_17.52.31_pip_errors.log

Some possibly relevant errors from pip install:
    ERROR: Could not find a version that satisfies the requirement envycontrol (from versions: none)
    ERROR: No matching distribution found for envycontrol

Error installing envycontrol.

---

**Gemini:**

Wygląda na to, że pakiet `envycontrol` nie jest dostępny w domyślnym repozytorium PyPI (lub występuje problem z jego indeksowaniem), przez co `pip` nie może go znaleźć.

Najpewniejszym sposobem instalacji w tej sytuacji jest pobranie narzędzia **bezpośrednio z oficjalnego repozytorium GitHub**.

Zalecam instalację globalną (z flagą `--break-system-packages`), ponieważ `envycontrol` to narzędzie systemowe wymagające uprawnień `sudo` do działania. Instalacja przez `pipx` w katalogu użytkownika utrudniałaby późniejsze wywoływanie go z uprawnieniami administratora.

### Rozwiązanie: Instalacja z GitHub

1. **Upewnij się, że masz zainstalowanego gita:**

   ```
   sudo apt install git -y
   ```
2. **Zainstaluj EnvyControl bezpośrednio ze źródła (globalnie):**

   ```
   sudo pip install git+https://github.com/bayasdev/envycontrol.git --break-system-packages
   ```

### Co zrobić po instalacji?

Gdy instalacja przebiegnie pomyślnie, wykonaj poniższe kroki, aby zdiagnozować i naprawić problem z baterią:

1. **Sprawdź obecny tryb:**

   ```
   sudo envycontrol --query
   ```

   Jeśli wynik to `hybrid`, to tu leży problem (RTX 4070 jest w stanie czuwania, ale nie `D3cold`).
2. **Przełącz na tryb zintegrowany (Integrated):**
   To całkowicie odetnie zasilanie od RTX 4070. Wymagany będzie restart systemu lub menedżera logowania.

   ```
   sudo envycontrol -s integrated
   ```

   *Uwaga: Po tej operacji zewnętrzne wyjścia wideo (HDMI/DP) mogą przestać działać, jeśli są fizycznie podpięte pod kartę NVIDIA (typowe w Legionach).*
3. **Weryfikacja po restarcie:**
   Uruchom ponownie `nvidia-smi`. Jeśli otrzymasz komunikat błędu (np. "NVIDIA-SMI has failed because it couldn't communicate with the NVIDIA driver"), to **dobry znak** w tym kontekście. Oznacza to, że karta jest fizycznie odłączona/wyłączona i nie zużywa baterii.

Czy instalacja z linku GitHub przebiegła pomyślnie?