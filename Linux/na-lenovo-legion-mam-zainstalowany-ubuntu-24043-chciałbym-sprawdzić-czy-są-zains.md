# Na  Lenovo Legion mam zainstalowany Ubuntu 24.04.3. Chciałbym sprawdzić czy  są

**Data:** 28 lis 2025, 22:17:46 CET

---

**User:**

Na
 Lenovo Legion mam zainstalowany Ubuntu 24.04.3. Chciałbym sprawdzić czy
 są zainstalowane poprawne steroniki do defaultowej karty dźwiękowej. Na
 pewno jest problem z nagrywaniem dźwięku przez wbudowany mikrofon.

---

**Gemini:**

Diagnostyka audio w systemie Linux, zwłaszcza na nowoczesnych laptopach gamingowych takich jak Lenovo Legion, wymaga przeanalizowania warstwy sprzętowej (kernel/ALSA) oraz serwera dźwięku (w Ubuntu 24.04 jest to domyślnie **PipeWire**). Problemy z mikrofonem często wynikają z obsługi cyfrowych mikrofonów (DMIC) wymagających Sound Open Firmware (SOF) lub błędnej konfiguracji miksera (mute/gain).

Oto techniczna ścieżka diagnostyczna i naprawcza.

### 1. Weryfikacja wykrywania sprzętu (Kernel Level)

Najpierw sprawdźmy, czy kernel Linux w ogóle widzi kontroler audio i jakie sterowniki jądra zostały załadowane.

Wykonaj poniższe polecenie, aby wylistować urządzenia PCI związane z audio i przypisane do nich sterowniki:

```
# Check PCI devices for Audio controllers and associated kernel modules
lspci -nnk | grep -A3 Audio
```

**Analiza wyników:**

- Powinieneś zobaczyć wpisy dla kontrolera Intel/AMD oraz NVIDIA (dla HDMI audio).
- Kluczowe jest pole `Kernel driver in use`. W nowoczesnych laptopach Legion oczekujemy `snd_hda_intel` lub, co bardziej prawdopodobne dla nowszych architektur, `snd_sof_pci` (Sound Open Firmware).

Następnie sprawdź, jak ALSA (Advanced Linux Sound Architecture) mapuje karty:

```
# List all sound cards recognized by ALSA
cat /proc/asound/cards

# List capture devices (microphones)
arecord -l
```

Jeżeli `arecord -l` zwraca "no soundcards found" lub brak urządzenia na liście, problem leży w jądrze/firmware, a nie w ustawieniach głośności.

### 2. Diagnostyka serwera dźwięku (PipeWire)

Ubuntu 24.04 używa PipeWire jako menedżera multimediów. Sprawdź, czy serwer poprawnie widzi urządzenia wejściowe (Sources).

```
# Check status of PipeWire and WirePlumber
wpctl status
```

Szukaj sekcji **Audio** -> **Sources**.

- Jeśli widzisz swój mikrofon (np. "Built-in Audio Analog Stereo"), ale przy nim znajduje się znacznik `[MUTED]` lub głośność `0.00`, problem jest softwarowy.
- Jeśli w sekcji Sources nie ma wbudowanego mikrofonu, oznacza to, że PipeWire nie otrzymał urządzenia od ALSA.

### 3. Weryfikacja poziomów w ALSA (Częsty problem)

Często zdarza się, że kanały "Capture" lub "Internal Mic Boost" są wyciszone na poziomie sprzętowym, niezależnie od ustawień w GUI systemowym (GNOME). Użyj `alsamixer`, który daje bezpośredni dostęp do rejestrów karty.

```
# Open ALSA mixer
alsamixer
```

1. Wciśnij `F6` i wybierz swoją kartę dźwiękową (zazwyczaj numer 0 lub 1, unikaj "default" lub "PipeWire").
2. Wciśnij `F4`, aby przełączyć się na widok **Capture**.
3. Sprawdź słupki "Capture" oraz "Internal Mic Boost".
   - Jeśli pod słupkiem widnieje `MM`, kanał jest wyciszony. Naciśnij `m`, aby go odmutować (zmieni się na `00` na zielonym tle).
   - Podnieś suwak "Capture" oraz "Internal Mic Boost" używając strzałek.

### 4. Problem z Sound Open Firmware (SOF) i DMIC

W modelach Legion mikrofony są często podłączone przez interfejs cyfrowy (DMIC), który wymaga firmware'u SOF. Jeśli dmesg sypie błędami, może to oznaczać brakujące pliki binarne firmware'u.

Sprawdź logi systemowe pod kątem błędów audio:

```
# Search kernel ring buffer for audio/sof related errors
sudo dmesg | grep -iE "snd|sof|audio|hda"
```

Jeśli widzisz błędy typu `nocodec`, `firmware failed to load` lub problemy z inicjalizacją SOF, spróbuj wymusić starszy sterownik `snd-hda-intel` (tryb legacy), co czasem naprawia obsługę mikrofonu kosztem zaawansowanych funkcji DSP.

**Obejście (Workaround) - edycja konfiguracji modułu:**

Edytuj plik konfiguracyjny modułów ALSA:

```
# Edit alsa-base.conf
sudo nano /etc/modprobe.d/alsa-base.conf
```

Dodaj na końcu jedną z poniższych linii (testuj po kolei, restartując komputer po każdej zmianie):

**Opcja A (Wymuszenie specyficznego modelu):**

```
options snd-hda-intel model=lenovo-legion
# Or generic auto
options snd-hda-intel model=auto
```

**Opcja B (Dla problemów z wykrywaniem DMIC na procesorach AMD/Intel):**

```
options snd-hda-intel dmic_detect=0
```

**Opcja C (Wymuszenie legacy drivera zamiast SOF - jeśli używany):**

```
options snd_intel_dspcfg dsp_driver=1
```

Po edycji wykonaj restart:

```
sudo reboot
```

### 5. Aktualizacja Firmware (Lenovo specific)

Lenovo Legiony mają specyficzne układy wzmacniaczy (np. Cirrus Logic). Czasami sterowniki są poprawne, ale brakuje blobów w `/lib/firmware`. W Ubuntu 24.04 pakiety `linux-firmware` powinny być świeże, ale warto upewnić się, że masz najnowsze poprawki.

```
# Update repositories and upgrade system packages
sudo apt update && sudo apt full-upgrade -y
```

Jeśli problem nadal występuje, a masz procesor AMD (Ryzen 6000/7000+), problem może dotyczyć sterownika ACP (Audio Co-Processor). W takim przypadku upewnij się, że używasz najnowszego dostępnego kernela (Ubuntu 24.04.3 powinno mieć kernel 6.8+, co jest wystarczające, ale kernel 6.10+ wnosi wiele poprawek dla nowych Legionów).

Sprawdź wersję kernela:

```
uname -sr
```

Jeśli jest starszy niż 6.8, rozważ instalację nowszego stosu HWE (Hardware Enablement).

### Chcesz, abym pomógł Ci zinterpretować wynik konkretnej komendy (np. `dmesg` lub `pactl`)?