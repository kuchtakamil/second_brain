# nie chcę na stałe wyłączać RTX. Nie da się zrobić tak jak jest na Windows że jes

**Data:** 19 lis 2025, 17:56:12 CET

---

**User:**

nie chcę na stałe wyłączać RTX. Nie da się zrobić tak jak jest na Windows że jest używana tylko wtedy gdy jest potrzebna?

---

**Gemini:**

Tak, jest to możliwe i tak właśnie powinien działać domyślny tryb w Linuxie, znany jako **NVIDIA On-Demand** (w Windows nazywa się to NVIDIA Optimus / MS Hybrid). W tym trybie pulpit (GNOME) jest renderowany przez zintegrowaną kartę Intela (iGPU), a RTX 4070 powinien być **całkowicie uśpiony** (zużycie energii bliskie 0W) i wybudzać się tylko wtedy, gdy uruchomisz grę lub ciężką aplikację.

Skoro na Ubuntu bateria "znika", oznacza to, że mechanizm usypiania (**Runtime D3 Power Management**) nie działa poprawnie i karta, mimo że nieużywana, pozostaje w stanie aktywnym ("idle"), pobierając około 10-20W.

Oto techniczna konfiguracja, aby uzyskać zachowanie "jak w Windows" (cisza na pulpicie, moc w grach):

### 1. Włącz tryb Hybrid (On-Demand)

Skoro masz już `envycontrol`, najbezpieczniej użyć go do poprawnego ustawienia trybu hybrydowego (narzędzie to automatycznie konfiguruje parametry jądra, o których często zapomina domyślny `prime-select`):

```
sudo envycontrol -s hybrid
```

*Wymagany restart systemu.*

### 2. Wymuszenie zaawansowanego zarządzania energią (NVreg)

Aby RTX 4070 mógł wejść w stan głębokiego uśpienia (D3cold), sterownik musi mieć jawnie włączone odpowiednie flagi.

Sprawdź, czy parametry są aktywne:

```
cat /proc/driver/nvidia/params/DynamicPowerManagement
```

Jeśli wynik to `0` lub plik nie istnieje, zarządzanie energią jest wyłączone. Wynik musi wynosić `0x02` (lub `2`).

**Jak to włączyć na stałe:**
Utwórz plik konfiguracyjny dla sterownika:

```
sudo nano /etc/modprobe.d/nvidia-power-management.conf
```

Wklej do środka następującą treść:

```
options nvidia "NVreg_DynamicPowerManagement=0x02"
```

Zapisz (Ctrl+O, Enter) i wyjdź (Ctrl+X). Następnie zaktualizuj initramfs i zrestartuj:

```
sudo update-initramfs -u
sudo reboot
```

### 3. Weryfikacja, czy karta "śpi" (Kluczowy krok)

Po restarcie, nie uruchamiaj żadnych gier. Otwórz terminal i sprawdź status zasilania karty PCI.

Najpierw znajdź adres PCI swojej karty NVIDIA (zazwyczaj `01:00.0`):

```
lspci | grep -i nvidia
```

Następnie sprawdź jej stan (podstawiając odpowiedni adres, np. `0000:01:00.0`):

```
cat /sys/bus/pci/devices/0000:01:00.0/power/runtime_status
```

- **`suspended`** – **SUKCES.** Karta jest wyłączona, bateria powinna trzymać długo.
- **`active`** – **PROBLEM.** Karta jest wybudzona. Coś ją blokuje.

### 4. Co zrobić, jeśli status to nadal `active`?

Jeśli mimo powyższych ustawień karta jest `active`, winowajcą jest zazwyczaj jeden z poniższych:

**A. Sterownik Audio HDMI**
Karta graficzna ma swój układ audio (do przesyłania dźwięku przez HDMI). Często karta graficzna usypia, ale jej układ audio pozostaje aktywny, co wybudza całość.
Sprawdź, czy masz regułę `udev`, która pozwala usypiać audio. Utwórz plik:

```
sudo nano /lib/udev/rules.d/80-nvidia-pm.rules
```

Upewnij się, że zawiera linie (szczególnie te dotyczące audio):

```
# Enable runtime PM for NVIDIA VGA/3D controller devices on driver bind
ACTION=="bind", SUBSYSTEM=="pci", ATTR{vendor}=="0x10de", ATTR{class}=="0x030000", TEST=="power/control", ATTR{power/control}="auto"
ACTION=="bind", SUBSYSTEM=="pci", ATTR{vendor}=="0x10de", ATTR{class}=="0x030200", TEST=="power/control", ATTR{power/control}="auto"

# Enable runtime PM for NVIDIA Audio devices on driver bind
ACTION=="bind", SUBSYSTEM=="pci", ATTR{vendor}=="0x10de", ATTR{class}=="0x040300", TEST=="power/control", ATTR{power/control}="auto"
```

**B. Zewnętrzny monitor**
W laptopach Lenovo Legion wyjście HDMI jest często podłączone *bezpośrednio* do RTX 4070 (tzw. hardwired).

- Jeśli podłączysz zewnętrzny monitor -> RTX 4070 **musi** być włączony non-stop. Nie da się tego ominąć (chyba że masz port USB-C z Thunderbolt/DP podłączony do iGPU, w co wątpię przy tej konfiguracji).
- Aby oszczędzać baterię, musisz odłączyć monitor zewnętrzny.

**C. Procesy "widmo"**
Niekiedy narzędzia systemowe odpytują kartę, nie pozwalając jej zasnąć. Sprawdź co używa sterownika:

```
sudo lsof /dev/nvidia0
sudo lsof /dev/nvidia-modeset
```

Jeśli lista jest pusta, a status to `active`, problem leży w sterowniku/BIOS. Jeśli widzisz tam procesy (np. `Xorg`, `gnome-shell`), oznacza to, że sesja graficzna uruchomiła się na NVIDIA zamiast na Intelu.

### 5. Jak uruchamiać gry na NVIDIA w tym trybie?

Gdy system jest w trybie Hybrid i karta jest uśpiona (`suspended`), musisz jawnie powiedzieć systemowi, kiedy użyć mocy RTX 4070.

1. **Steam:** Kliknij prawym na grę -> Właściwości -> Opcje uruchamiania:

   ```
   __NV_PRIME_RENDER_OFFLOAD=1 __GLX_VENDOR_LIBRARY_NAME=nvidia %command%
   ```
2. **GNOME (Pulpit):** Kliknij prawym przyciskiem myszy na ikonę aplikacji -> wybierz **"Uruchom przy użyciu dedykowanej karty graficznej"**.
3. **Terminal:**

   ```
   __NV_PRIME_RENDER_OFFLOAD=1 __GLX_VENDOR_LIBRARY_NAME=nvidia nazwa_programu
   ```

Czy chcesz, abym pomógł Ci zinterpretować wynik komendy `cat /sys/bus/pci/devices/.../power/runtime_status` po wykonaniu konfiguracji?