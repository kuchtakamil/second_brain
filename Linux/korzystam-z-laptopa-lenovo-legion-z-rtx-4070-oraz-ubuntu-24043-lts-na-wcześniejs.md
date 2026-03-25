# Korzystam z laptopa Lenovo Legion z RTX 4070 oraz Ubuntu 24.04.3 LTS.  Na wcześn

**Data:** 19 lis 2025, 17:03:05 CET

---

**User:**

Korzystam z laptopa Lenovo Legion z RTX 4070 oraz Ubuntu 24.04.3 LTS. 
Na wcześniejszych wersjach ubuntu miałem problem z zainstalowaniem sterowników do RTX 4070, ale teraz wydaje się że jest ok, chociaż nie jestem pewny.
Porównując czas pracy na baterii na Windows 11 oraz na wspomnianym Ubuntu, niestety Ubuntu wypada dużo gorzej. Laptop znacznie szybciej wyczerpuje baterię na Ubuntu.
Jaki może być tego powód? Jak to sprawdzić? Weź pod uwagę kwestię RTX 4070, weryfikacji poprawności zainstalowanych sterowników na Ubuntu oraz inne problemy które mogą powodować ten problem.

---

**Gemini:**

W przypadku laptopów gamingowych, takich jak Lenovo Legion, głównym powodem drenażu baterii na Linuxie jest niewłaściwe zarządzanie stanem energetycznym dedykowanej karty graficznej (dGPU) – w Twoim przypadku RTX 4070. Jeśli system nie potrafi całkowicie wyłączyć dGPU (wprowadzić w stan *D3cold*), karta ta, nawet "bezczynna", może pobierać 10-30W energii, co drastycznie skraca czas pracy.

Poniżej znajduje się techniczna procedura diagnostyki i naprawy tego stanu na Ubuntu 24.04.

### 1. Weryfikacja sterowników i stanu GPU

Ubuntu 24.04 zazwyczaj dobrze radzi sobie z instalacją sterowników, ale sterownik otwarty (Nouveau) nie posiada zaawansowanych funkcji zarządzania energią dla architektury Ada Lovelace (RTX 4000 series).

**Krok A: Sprawdzenie aktywnego sterownika**
Wpisz w terminalu:

```
nvidia-smi
```

Jeśli komenda zwraca tabelę z informacjami o GPU, sterowniki są załadowane. Sprawdź wersję (Driver Version). Dla RTX 4070 powinna to być wersja z serii 535, 550 lub nowsza (proprietary).
Jeśli komenda nie działa (`command not found`) lub zwraca błąd komunikacji, sterowniki nie są zainstalowane poprawnie.

**Krok B: Instalacja właściwych sterowników**
Upewnij się, że używasz sterowników własnościowych:

```
sudo ubuntu-drivers devices
```

Zainstaluj rekomendowany sterownik (oznaczony jako `recommended`), np.:

```
sudo apt install nvidia-driver-550
sudo reboot
```

### 2. Konfiguracja NVIDIA PRIME (Hybrid Graphics)

To najważniejszy punkt. Lenovo Legion posiada system hybrydowy (iGPU Intel/AMD + dGPU NVIDIA). Jeśli w BIOS-ie masz ustawiony tryb "Discrete Graphics" (tylko NVIDIA), bateria zniknie błyskawicznie.

**Krok A: Ustawienia BIOS/UEFI**
Wejdź do BIOS-u i upewnij się, że tryb graficzny to **Dynamic Graphics**, **Hybrid Mode** lub **Switchable Graphics**. Nie może to być "Discrete Only".

**Krok B: Wybór profilu w Ubuntu**
W Ubuntu zarządzanie hybrydą odbywa się przez `prime-select`. Sprawdź aktualny tryb:

```
prime-select query
```

- `performance`: RTX 4070 jest stale włączona i renderuje pulpit. Największe zużycie energii.
- `on-demand`: Pulpit renderuje iGPU, RTX 4070 wybudza się tylko dla konkretnych aplikacji (Render Offload). To jest zalecany tryb.
- `integrated`: Całkowite programowe wyłączenie RTX 4070. Najlepsza bateria, ale brak dostępu do GPU Nvidii.

Aby naprawić drenaż baterii, przełącz na tryb on-demand:

```
sudo prime-select on-demand
sudo reboot
```

### 3. Weryfikacja stanu energetycznego (PCI D3 Power State)

Nawet w trybie `on-demand`, sterownik może nie usypiać karty (nie wchodzić w stan `D3cold`), jeśli jakiś proces trzyma uchwyt do sterownika (np. narzędzia monitorujące, HDMI podpięte do dGPU).

**Diagnostyka:**
Użyj poniższej pętli, aby sprawdzić status zasilania (zamień ścieżkę, jeśli Twoja karta ma inny adres PCI, zazwyczaj `0000:01:00.0`):

```
cat /sys/bus/pci/devices/0000:01:00.0/power/runtime_status
```

Powinieneś widzieć `suspended`. Jeśli widzisz `active` podczas pracy na pulpicie (bez gier), coś trzyma kartę "przy życiu".

Możesz również sprawdzić, które procesy używają karty:

```
sudo lsof /dev/nvidia0
```

Wszelkie procesy (nawet Xorg lub Gnome Shell) widoczne tutaj w trybie spoczynku oznaczają problem z konfiguracją Offloadingu.

### 4. Zaawansowane zarządzanie energią (EnvyControl / Supergfxctl)

Standardowe narzędzia Ubuntu bywają kapryśne na laptopach gamingowych. Społeczność Linuxa stworzyła bardziej precyzyjne narzędzia do kontroli magistrali PCIe dla GPU.

Rekomenduję **EnvyControl** (prostsze, bazuje na Pythonie) lub **Supergfxctl** (napisane w Rust, używane w ASUS-ach, ale działa na innych).

**Instalacja EnvyControl:**

```
pip install envycontrol
```

(Upewnij się, że masz `gnome-shell-extension-appindicator` dla łatwiejszego przełączania, jeśli dostępny jest dodatek GUI).

Ustawienie trybu zintegrowanego (całkowite odcięcie zasilania od RTX 4070):

```
sudo envycontrol -s integrated
```

To powinno drastycznie wydłużyć czas pracy. Gdy będziesz chciał grać, przełączasz z powrotem:

```
sudo envycontrol -s hybrid
```

### 5. Analiza zużycia przez PowerTOP

Narzędzie Intela do diagnozy stanów procesora i wybudzeń (wakeups).

```
sudo apt install powertop
sudo powertop
```

1. Przejdź do zakładki **Tunables** (Tab).
2. Wszystkie pozycje powinny być "Good". Jeśli widzisz "Bad" przy urządzeniach PCI/Runtime PM, system nie zarządza nimi poprawnie.
3. Możesz tymczasowo włączyć autokalibrację:

   ```
   sudo powertop --auto-tune
   ```
4. W zakładce **Overview** sprawdź sekcję "Discharge rate". Na pulpicie powinna wynosić ok. 10-15W (zależnie od jasności ekranu). Jeśli wynosi >25W, RTX 4070 nadal pracuje.

### 6. Częstotliwość odświeżania ekranu

Lenovo Legion często ma matryce 165Hz lub 240Hz. Ubuntu 24.04 domyślnie może ustawić najwyższą wartość.

- Wysokie odświeżanie uniemożliwia procesorowi i iGPU wejście w głębokie stany oszczędzania energii (C-states).
- **Rozwiązanie:** W ustawieniach ekranu (Settings -> Displays) zmień Refresh Rate na **60Hz** podczas pracy na baterii.

### 7. Konflikt TLP vs power-profiles-daemon

Ubuntu 24.04 domyślnie używa `power-profiles-daemon` (zintegrowany z menu systemowym - tryby Power Saver / Balanced / Performance).
Wielu użytkowników instaluje **TLP** z przyzwyczajenia.

- **Uwaga:** Nie używaj obu jednocześnie bez konfiguracji, ponieważ wchodzą w konflikt.
- Dla nowoczesnych Legionów często lepszym rozwiązaniem jest pozostanie przy `power-profiles-daemon` i ustawienie trybu "Power Saver" w menu systemowym, LUB całkowite usunięcie go i przejście na `auto-cpufreq` (który dynamicznie zarządza częstotliwością CPU i jest świetny dla baterii).

**Instalacja auto-cpufreq (opcjonalnie, zamiast TLP):**

```
git clone https://github.com/AdnanHodzic/auto-cpufreq.git
cd auto-cpufreq && sudo ./auto-cpufreq-installer
```

Po instalacji wybierz tryb `--install` aby usługa działała w tle.

---

**Czy chciałbyś, abym przeanalizował wynik polecenia `nvidia-smi` lub `powertop` jeśli wkleisz go w kolejnej wiadomości, aby potwierdzić, czy karta wchodzi w stan uśpienia?**