# Dźwięk wrócił. Pomieszałeś lokalizację librnnoise_ladspa.so  Jednak dźwięk nagry

**Data:** 1 załączony plik

---

**User:**

Dźwięk wrócił. Pomieszałeś lokalizację librnnoise_ladspa.so  Jednak dźwięk nagrywany dalej jest fatalny, bez zmian. Screen z EasyEffects

---

**Gemini:**

-  [image\_236a49.png](image_236a49-b9dbdb11d6bf485b.png)30 gru 2025, 19:37:46 CET

Komunikat w EasyEffects potwierdza, że wersja z repozytorium `apt` w Ubuntu 24.04 została skompilowana bez wbudowanej obsługi RNNoise lub nie może odnaleźć bibliotek w ścieżkach systemowych. Na systemie Ubuntu najstabilniejszym sposobem na uzyskanie pełnej funkcjonalności EasyEffects wraz z pluginami jest przejście na wersję **Flatpak**, która izoluje zależności i dostarcza kompletny zestaw filtrów.

Poniżej rozwiązanie problemu z EasyEffects oraz zaawansowana kalibracja sprzętowa dla Twojego modelu Lenovo Legion.

### 1. Naprawa EasyEffects (Przejście na Flatpak)

Wersja Flatpak zawiera w sobie `rnnoise`, `lsp-plugins` oraz `zam-plugins`, co eliminuje problemy z brakującymi efektami.

```
# Usuń wersję systemową
sudo apt remove easyeffects

# Zainstaluj Flatpak (jeśli nie masz)
sudo apt install flatpak

# Dodaj repozytorium Flathub
flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo

# Zainstaluj EasyEffects
flatpak install flathub com.github.wwmm.easyeffects
```

Po instalacji i uruchomieniu, opcja **Noise Reduction** powinna stać się aktywna.

---

### 2. Eliminacja "Fatalnej" Jakości (Hardware Clipping & Gain)

Jeśli głos brzmi "bardzo źle" (metalicznie, zniekształcony, przesterowany), problemem zazwyczaj nie jest szum, lecz **Microphone Boost** i **AGC (Auto Gain Control)**.

W modelu Legion Pro 5 mikrofony typu Array są bardzo czułe. Wykonaj poniższe kroki w terminalu:

1. Uruchom mikser ALSA:

   ```
   alsamixer
   ```
2. Wciśnij `F6` i wybierz kartę `HDA Intel PCH`.
3. Wciśnij `F5`, aby zobaczyć wszystkie suwaki.
4. Znajdź suwak **Internal Mic Boost**. Jeśli jest na czerwonym polu (> 0dB), zredukuj go do **0** lub max **+10dB**.
5. Znajdź suwak **Capture**. Ustaw go na około **40-50%**. Wyższe wartości na tym laptopie powodują cyfrowe przesterowanie (clipping), którego żaden filtr nie naprawi.

---

### 3. Zaawansowana konfiguracja PipeWire (Bypass Echo Cancellation)

Google Meet posiada własny moduł AEC (Acoustic Echo Cancellation), który często "gryzie się" z przetwarzaniem systemowym. Spróbujemy wymusić czysty strumień o wysokiej przepływności.

Utwórz plik wymuszający parametry dla konkretnego urządzenia wejściowego:

```
mkdir -p ~/.config/wireplumber/wireplumber.conf.d/
nano ~/.config/wireplumber/wireplumber.conf.d/51-microphone-fix.conf
```

Wklej poniższą konfigurację (zastępując `alsa_input.pci-0000_00_1f.3.generic-it87` nazwą swojego urządzenia, którą znajdziesz komendą `wpctl status`):

```
monitor.alsa.rules = [
  {
    matches = [
      {
        node.name = "~alsa_input.pci.*"
      }
    ]
    actions = {
      update-props = {
        audio.rate          = 48000
        audio.format        = "S32LE"
        api.alsa.period-size = 1024
        api.alsa.headroom    = 512
      }
    }
  }
]
```

---

### 4. Alternatywa dla RNNoise: DeepFilterNet

Jeśli RNNoise nadal nie daje satysfakcji (brzmi "pusto"), zainstaluj **DeepFilterNet**. Jest to obecnie najbardziej zaawansowany filtr oparty na AI dla Linuxa, który radzi sobie lepiej z echem i pogłosem w dużych pokojach.

```
# Instalacja poprzez cargo (wymaga rust)
sudo apt install cargo
cargo install deep-filter-visualizer

# Alternatywnie jako plugin PipeWire (zalecane)
# Pobierz binaria z: https://github.com/R3nzTheCodeGOD/DeepFilterNet-LADSPA
```

---

### 5. Sprawdzenie konfliktów z dmic (Intel Smart Sound Technology)

W Lenovo Legion Pro 5 (procesory 13/14 gen) mikrofony są obsługiwane przez procesor DSP (SST). Jeśli powyższe kroki nie pomogą, sprawdź czy kernel nie wyrzuca błędów ładowania topologii:

```
journalctl -k | grep -iE "sof|sst|dmic"
```

Jeśli widzisz błędy "Topology load failed", oznacza to, że potrzebujesz nowszego firmware'u. Na Ubuntu 24.04 możesz spróbować zainstalować paczkę `oem-somerville-tentacool-meta` (często zawiera poprawki dla nowych Legionów) lub ręcznie zaktualizować `linux-firmware`.

Czy chcesz, abym pomógł Ci przeanalizować wynik komendy `wpctl status` oraz `arecord -l`, aby upewnić się, że system poprawnie identyfikuje mikrofony typu Array?