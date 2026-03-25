# nie ma u mnie katalogu /usr/lib/x86_64-linux-gnu/ladspa jak mam zainstalować lib

**Data:** 30 gru 2025, 18:38:26 CET

---

**User:**

nie ma u mnie katalogu /usr/lib/x86_64-linux-gnu/ladspa
jak mam zainstalować librnnoise-gadget? próbowałem tak:
udo apt install librnnoise-gadget
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
E: Unable to locate package librnnoise-gadget

---

**Gemini:**

Błąd wynika z faktu, że pakiet o nazwie `librnnoise-gadget` nie znajduje się w standardowych repozytoriach Ubuntu (Main/Universe). W systemie Ubuntu 24.04 (Noble Numbat) pluginy LADSPA oraz biblioteka RNNoise wymagają specyficznej ścieżki instalacyjnej lub użycia nowocześniejszego rozwiązania zintegrowanego z PipeWire poprzez **EasyEffects** lub ręczną kompilację pluginu.

Oto kroki, aby poprawnie zainstalować i skonfigurować odszumianie w Twoim środowisku:

### 1. Instalacja bibliotek RNNoise i LADSPA SDK

Zamiast szukać nieistniejącego pakietu, zainstaluj implementację odszumiania opartą na projekcie Werman, która jest standardem dla Linux Audio.

```
sudo apt update
sudo apt install autoconf automake libtool build-essential ladspa-sdk
```

Najprostszym sposobem na uzyskanie pliku `.so` bez kompilacji całego projektu jest instalacja pakietu `librnnoise-vst`, ale ponieważ Ubuntu preferuje PipeWire, najstabilniejszą metodą w 2025 roku jest użycie **EasyEffects**, który zawiera w sobie wszystkie niezbędne filtry (w tym RNNoise).

### 2. Rozwiązanie zalecane: EasyEffects

Dla użytkownika Ubuntu 24.04, EasyEffects jest de facto standardem zarządzania procesami DSP (Digital Signal Processing).

1. **Instalacja:**

```
sudo apt install easyeffects
```

1. **Konfiguracja odszumiania:**
   - Otwórz aplikację **EasyEffects**.
   - Przejdź do zakładki **Input** (wejście mikrofonowe).
   - Kliknij **Add Effects** i wybierz **Noise Reduction**.
   - W ustawieniach efektu wybierz metodę **RNNoise**.
   - Aktywuj przełącznik przy efekcie.

EasyEffects automatycznie stworzy wirtualny węzeł w PipeWire. W ustawieniach Google Meet wybierz urządzenie wejściowe **"EasyEffects Source"**.

---

### 3. Ręczna instalacja pluginu LADSPA (Jeśli wolisz Filter Chain)

Jeśli chcesz pozostać przy konfiguracji plikowej `99-input-denoising.conf`, musisz samodzielnie dostarczyć bibliotekę.

1. **Pobierz skompilowany plugin:**
   Możesz pobrać gotowy plik `librnnoise_ladspa.so` z zaufanych źródeł projektów GitHub (np. [werman/noise-suppression-for-voice](https://github.com/werman/noise-suppression-for-voice)).
2. **Stwórz brakujący katalog i przenieś plik:**

```
sudo mkdir -p /usr/lib/ladspa
# Po pobraniu pliku (załóżmy, że jest w ~/Downloads):
sudo cp ~/Downloads/librnnoise_ladspa.so /usr/lib/ladspa/
```

1. **Zaktualizuj ścieżkę w konfiguracji PipeWire:**
   W pliku `~/.config/pipewire/pipewire.conf.d/99-input-denoising.conf` zmień linię `plugin`:

```
plugin = "/usr/lib/ladspa/librnnoise_ladspa.so"
```

---

### 4. Diagnostyka struktury katalogów LADSPA

W Ubuntu 24.04 standardowe ścieżki poszukiwania pluginów LADSPA to:

1. `/usr/lib/ladspa/`
2. `/usr/local/lib/ladspa/`
3. `~/.ladspa/lib/`

Możesz sprawdzić, gdzie PipeWire szuka bibliotek, wykonując:

```
export LADSPA_PATH=/usr/lib/ladspa:/usr/local/lib/ladspa
```

### 5. Dlaczego `apt install` nie zadziałał?

Nazwa `librnnoise-gadget` pochodzi z niektórych niszowych repozytoriów PPA lub starszych instrukcji dla Arch Linux (AUR). W Ubuntu pakiety te są często częścią `pipewire-audio-effects` lub wymagają zewnętrznych repozytoriów takich jak:

```
sudo add-apt-repository ppa:apandada1/easyeffects
sudo apt update
```

### 6. Weryfikacja po instalacji

Po skonfigurowaniu filtra (czy to przez EasyEffects, czy Filter Chain), sprawdź czy system widzi nowy "sink" wejściowy:

```
pw-link -i -l
```

Powinieneś zobaczyć na liście `rnnoise_source` lub `easyeffects_source`.

Czy chciałbyś, abym przygotował gotowy skrypt Bash, który pobierze odpowiednią bibliotekę `.so`, umieści ją w poprawnym katalogu i wygeneruje za Ciebie plik konfiguracyjny PipeWire?