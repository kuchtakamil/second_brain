# w githubie który podałeś w kaatalogu src/ladspa jest tylko plik CMakeLists.txt,

**Data:** 30 gru 2025, 18:51:06 CET

---

**User:**

w githubie który podałeś w kaatalogu src/ladspa jest tylko plik CMakeLists.txt, plik cpp oraz pliki h. Nie ma so

---

**Gemini:**

Pliki `.cpp` i `.h` to kod źródłowy, który musi zostać skompilowany do postaci binarnej (`.so`), aby system mógł go załadować. W środowisku Linux pliki binarne rzadko są przechowywane bezpośrednio w repozytorium ze względu na różnice w architekturze procesorów i wersjach bibliotek systemowych.

Oto szczegółowa instrukcja kompilacji oraz alternatywna metoda pobrania gotowego pliku.

### 1. Kompilacja ze źródeł (Metoda zalecana)

Kompilacja na docelowej maszynie gwarantuje pełną kompatybilność z Twoją wersją jądra i bibliotek standardowych (glibc).

**Wymagania systemowe:**

```
sudo apt update
sudo apt install git cmake g++ libfreetype6-dev libcurl4-openssl-dev
```

**Proces budowania:**

```
# Clone the repository
git clone https://github.com/werman/noise-suppression-for-voice.git
cd noise-suppression-for-voice

# Create a build directory
mkdir build && cd build

# Generate build files using CMake
cmake ..

# Compile the project using all available CPU cores
make -j$(nproc)
```

Po zakończeniu kompilacji, gotowy plik `.so` znajdziesz w katalogu:
`bin/ladspa/librnnoise_ladspa.so`

**Instalacja w systemie:**

```
sudo mkdir -p /usr/lib/ladspa
sudo cp bin/ladspa/librnnoise_ladspa.so /usr/lib/ladspa/
```

---

### 2. Pobranie gotowego pliku (Releases)

Jeśli nie chcesz kompilować kodu, autor udostępnia gotowe binaria w sekcji **Releases**.

1. Wejdź na: `https://github.com/werman/noise-suppression-for-voice/releases`
2. Pobierz plik `linux-rnnoise.zip`.
3. Rozpakuj go. Plik `.so` znajduje się w folderze `ladspa`.
4. Przenieś go do `/usr/lib/ladspa/` jak w poprzednim kroku.

---

### 3. Zaawansowana weryfikacja pluginu LADSPA

Aby upewnić się, że system poprawnie rozpoznaje nową bibliotekę, użyj narzędzia `analyseplugin` z pakietu `ladspa-sdk`:

```
sudo apt install ladspa-sdk
analyseplugin /usr/lib/ladspa/librnnoise_ladspa.so
```

Powinieneś otrzymać dane o portach wejściowych/wyjściowych (Input/Output Audio) oraz parametrach kontrolnych (VAD Threshold). Jeśli otrzymasz błąd `failed to open shared object file`, oznacza to brakującą zależność biblioteki `rnnoise`.

---

### 4. Integracja z PipeWire (Dynamic Filter Chain)

Gdy masz już plik `/usr/lib/ladspa/librnnoise_ladspa.so`, musisz połączyć go z serwerem dźwięku. W Ubuntu 24.04 PipeWire zarządza węzłami audio. Możesz stworzyć wirtualny mikrofon, który w locie odcina szum.

Utwórz plik konfiguracyjny użytkownika:

```
mkdir -p ~/.config/pipewire/pipewire.conf.d/
nano ~/.config/pipewire/pipewire.conf.d/99-input-denoising.conf
```

Wklej poniższą definicję modułu:

```
context.modules = [
{
    name = libpipewire-module-filter-chain
    args = {
        node.description = "Deep Learning Noise Suppressor"
        media.name       = "Deep Learning Noise Suppressor"
        filter.graph = {
            nodes = [
                {
                    type   = ladspa
                    name   = rnnoise
                    plugin = /usr/lib/ladspa/librnnoise_ladspa.so
                    label  = noise_suppressor_mono
                    control = {
                        "VAD Threshold (%)" = 50.0
                    }
                }
            ]
        }
        capture.props = {
            node.name = "capture.rnnoise_source"
            node.passive = true
        }
        playback.props = {
            node.name = "rnnoise_source"
            media.class = Audio/Source
        }
    }
}
]
```

---

### 5. Debugowanie i monitorowanie strumienia

Po zapisaniu pliku zrestartuj stos audio:

```
systemctl --user restart pipewire pipewire-pulse wireplumber
```

Sprawdź, czy nowy węzeł jest widoczny w grafie PipeWire:

```
pw-mon -i
```

Aby sprawdzić, czy dźwięk faktycznie przechodzi przez filtr i czy nie występują błędy `underrun` (powodujące trzaski), monitoruj logi w czasie rzeczywistym podczas korzystania z mikrofonu:

```
journalctl -f | grep pipewire
```

Jeśli słyszysz metaliczny pogłos, zmniejsz `VAD Threshold (%)` do `30.0` – oznacza to Voice Activity Detection; zbyt wysoka wartość może ucinać końcówki słów przy cichym mówieniu.

Czy chciałbyś, abym wyjaśnił, jak zautomatyzować przełączanie na ten filtr w zależności od podłączonego urządzenia (np. dock Thunderbolt vs wbudowany mikrofon)?