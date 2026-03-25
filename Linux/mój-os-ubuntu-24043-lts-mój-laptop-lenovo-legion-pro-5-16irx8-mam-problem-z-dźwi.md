# Mój OS: Ubuntu 24.04.3 LTS  Mój laptop: Lenovo Legion pro 5 16IRX8 Mam problem z

**Data:** 30 gru 2025, 18:24:36 CET

---

**User:**

Mój OS: Ubuntu 24.04.3 LTS 
Mój laptop: Lenovo Legion pro 5 16IRX8
Mam problem z dźwiękiem wchodzącym do komputera. Mój głos na Google Meet czy recorderze brzmi bardzo źle.

---

**Gemini:**

Problem z jakością dźwięku w laptopach Lenovo Legion na systemie Linux wynika najczęściej z błędnej implementacji sterownika **snd\_hda\_intel** dla kodeka Realtek (zazwyczaj ALC287) oraz braku zaawansowanego przetwarzania sygnału, które w systemie Windows realizowane jest przez oprogramowanie Nahimic lub Dolby.

Poniżej znajduje się zaawansowana ścieżka diagnostyczna i naprawcza dla Ubuntu 24.04 (PipeWire).

---

### 1. Parametryzacja Modułu ALSA (Fixing Codec Initialization)

Wiele modeli Legion ma problem z mapowaniem pinów mikrofonu. Możesz wymusić konkretny model sterownika, aby poprawić inicjalizację sprzętu.

Edytuj plik konfiguracyjny ALSA:

```
sudo nano /etc/modprobe.d/alsa-base.conf
```

Dodaj na końcu pliku następującą linię:

```
options snd-hda-intel model=alc285-hp-spectre-x360
```

*(Uwaga: Mimo że to Legion, model `alc285-hp-spectre-x360` często wymusza poprawne zachowanie pinów dla mikrofonów typu array w kodekach ALC287).*

Następnie zaktualizuj initramfs i zrestartuj system:

```
sudo update-initramfs -u
sudo reboot
```

---

### 2. Implementacja Aktywnej Redukcji Szumów (PipeWire Filter Chain)

Ubuntu 24.04 używa PipeWire. Domyślnie mikrofony w laptopach zbierają szum wentylatorów i zakłócenia EMI. Najskuteczniejszym rozwiązaniem jest użycie algorytmu **RNNoise**.

1. Zainstaluj niezbędne wtyczki:

```
sudo apt update
sudo apt install pipewire-audio-client-libraries libspa-0.2-bluetooth libspa-0.2-jack
```

1. Utwórz konfigurację filtra RNNoise dla PipeWire:

```
mkdir -p ~/.config/pipewire/pipewire.conf.d/
nano ~/.config/pipewire/pipewire.conf.d/99-input-denoising.conf
```

1. Wklej poniższą konfigurację:

```
context.modules = [
    {   name = libpipewire-module-filter-chain
        args = {
            node.description = "Noise Canceling Source"
            media.name       = "Noise Canceling Source"
            filter.graph = {
                nodes = [
                    {
                        type   = ladspa
                        name   = rnnoise
                        plugin = /usr/lib/x86_64-linux-gnu/ladspa/librnnoise_ladspa.so
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
                audio.rate = 48000
            }
            playback.props = {
                node.name = "rnnoise_source"
                media.class = Audio/Source
                audio.rate = 48000
            }
        }
    }
]
```

*(Upewnij się, że plik `librnnoise_ladspa.so` znajduje się w podanej ścieżce. Jeśli nie, zainstaluj `librnnoise-gadget` lub skompiluj plugin).*

1. Zrestartuj usługi audio:

```
systemctl --user restart pipewire pipewire-pulse wireplumber
```

W ustawieniach dźwięku wybierz teraz **"Noise Canceling Source"** jako domyślne urządzenie wejściowe.

---

### 3. Optymalizacja Sample Rate w PipeWire

Niezgodność częstotliwości próbkowania między sprzętem a serwerem dźwięku często powoduje artefakty (metaliczny dźwięk).

Edytuj konfigurację PipeWire:

```
sudo nano /usr/share/pipewire/pipewire.conf
```

Znajdź sekcję `default.clock.rate` i ustaw ją sztywno na 48000 (standard dla Google Meet i większości kodeków Realtek):

```
default.clock.rate = 48000
default.clock.allowed-rates = [ 44100 48000 ]
```

---

### 4. Wyłączenie programowego wzmocnienia (Auto Gain Control) w Chrome/Meet

Google Meet posiada własne mechanizmy AGC, które często kłócą się z systemowym zarządzaniem energią w Linuxie, powodując "pływanie" głośności i szumów.

1. Otwórz Chrome/Chromium.
2. Przejdź do: `chrome://flags/#enable-webrtc-allow-input-volume-adjustment`.
3. Ustaw na **Disabled**.

Dodatkowo, sprawdź poziom `Capture` w `alsamixer`:

```
alsamixer
```

Wciśnij `F6`, wybierz swoją kartę dźwiękową, `F5`, aby zobaczyć wszystkie suwaki. Upewnij się, że **Internal Mic Boost** nie jest ustawiony na 100% (zalecane 0dB lub +10dB), ponieważ powoduje to ogromny clipping sygnału.

---

### 5. Aktualizacja Firmware (SOF)

Lenovo Legion Pro 5 korzysta z procesorów Intel Core 13/14 generacji, które wymagają **Sound Open Firmware (SOF)**.

Sprawdź, czy masz zainstalowane najnowsze pliki firmware:

```
sudo apt install firmware-sof-signed
```

Sprawdź logi kernela pod kątem błędów ładowania DSP:

```
dmesg | grep -i sof
```

Jeśli widzisz błędy typu `IPC message timeout`, konieczne może być dodanie parametru kernela w `/etc/default/grub`:

```
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash snd_hda_intel.dmic_detect=0"
```

*(Uwaga: Użyj tego tylko, jeśli mikrofon nie jest w ogóle wykrywany. Jeśli jest wykrywany, ale brzmi źle, pomiń ten krok).*

Czy chcesz, abym pomógł Ci zweryfikować logi systemowe `journalctl` pod kątem błędów PipeWire, aby precyzyjnie zdiagnozować przyczynę zniekształceń?