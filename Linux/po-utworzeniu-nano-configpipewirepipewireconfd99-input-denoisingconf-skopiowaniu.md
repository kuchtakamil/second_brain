# Po utworzeniu  nano ~/.config/pipewire/pipewire.conf.d/99-input-denoising.conf s

**Data:** 30 gru 2025, 19:13:14 CET

---

**User:**

Po utworzeniu 
nano ~/.config/pipewire/pipewire.conf.d/99-input-denoising.conf
skopiowaniu librnnoise_ladspa.so do /usr/lib/ladspa/
a także po ustawieniu
default.clock.rate = 48000
default.clock.allowed-rates = [ 44100 48000 ]
i po restarcie dźwięk całkowicie zniknął. W setting sound widzę No Output Devices, No Input Devices

---

**Gemini:**

Zniknięcie urządzeń audio (Output/Input) oznacza, że proces `pipewire` lub `wireplumber` napotkał błąd krytyczny podczas parsowania konfiguracji i nie wystartował. Najczęstszą przyczyną jest błąd składni w pliku `.conf` lub brak cudzysłowów w ścieżkach.

### 1. Diagnostyka stanu usług

Sprawdź, która usługa zgłasza błąd:

```
systemctl --user status pipewire.service wireplumber.service
```

Następnie sprawdź logi, aby zobaczyć konkretny błąd składni:

```
journalctl --user -u pipewire | tail -n 20
```

Szukaj fraz takich jak `parse error`, `syntax error` lub `failed to load module`.

---

### 2. Przywrócenie dźwięku (Rollback)

Aby natychmiast przywrócić dźwięk, wyłącz wadliwą konfigurację:

```
mv ~/.config/pipewire/pipewire.conf.d/99-input-denoising.conf ~/.config/pipewire/pipewire.conf.d/99-input-denoising.conf.bak
systemctl --user restart pipewire pipewire-pulse wireplumber
```

---

### 3. Korekta błędu składni w `99-input-denoising.conf`

W formacie SPA-JSON, używanym przez PipeWire, ścieżki oraz nazwy modułów zawierające znaki specjalne (jak `/` lub `-`) **muszą** być ujęte w cudzysłów. W poprzednim kroku mogło dojść do błędu parsowania ścieżki pluginu.

Poprawiona treść pliku `~/.config/pipewire/pipewire.conf.d/99-input-denoising.conf`:

```
context.modules = [
{
    name = "libpipewire-module-filter-chain"
    args = {
        node.description = "Noise Suppressor"
        media.name       = "Noise Suppressor"
        filter.graph = {
            nodes = [
                {
                    type   = ladspa
                    name   = rnnoise
                    plugin = "/usr/lib/ladspa/librnnoise_ladspa.so"
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

---

### 4. Weryfikacja zmian w `/usr/share/pipewire/pipewire.conf`

Jeśli edytowałeś plik systemowy w `/usr/share/`, mogłeś naruszyć jego strukturę. Zalecane jest cofnięcie zmian w tym pliku i przeniesienie ich do katalogu użytkownika.

1. Przywróć oryginalny plik `/usr/share/pipewire/pipewire.conf` (jeśli masz kopię) lub upewnij się, że nie brakuje żadnego przecinka w tablicy `default.clock.allowed-rates`.
2. Prawidłowy wpis powinien wyglądać tak:

```
default.clock.rate = 48000
default.clock.allowed-rates = [ 44100, 48000 ]
```

*(Zwróć uwagę na przecinek między wartościami w nawiasie kwadratowym).*

---

### 5. Sprawdzenie uprawnień biblioteki

Upewnij się, że PipeWire ma uprawnienia do odczytu pliku `.so`:

```
ls -l /usr/lib/ladspa/librnnoise_ladspa.so
```

Jeśli brakuje uprawnień do odczytu dla innych użytkowników, wykonaj:

```
sudo chmod 644 /usr/lib/ladspa/librnnoise_ladspa.so
```

### 6. Ponowne uruchomienie

Po naniesieniu poprawek włącz konfigurację i zrestartuj serwer:

```
mv ~/.config/pipewire/pipewire.conf.d/99-input-denoising.conf.bak ~/.config/pipewire/pipewire.conf.d/99-input-denoising.conf
systemctl --user restart pipewire wireplumber
```

Jeśli urządzenia nadal nie są widoczne, uruchom `pipewire` bezpośrednio w terminalu, aby zobaczyć debug w czasie rzeczywistym:

```
pipewire -c pipewire.conf
```

Wypisze on dokładnie, w której linii konfiguracji znajduje się błąd (np. `token expected` lub `missing comma`).