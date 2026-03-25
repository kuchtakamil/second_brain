# Nadal mam problem. Zauważyłem podejrzane zachowanie  upower -i /org/freedesktop/

**Data:** 19 lis 2025, 19:36:23 CET

---

**User:**

Nadal mam problem. Zauważyłem podejrzane zachowanie 
upower -i /org/freedesktop/UPower/devices/battery_BAT0
wyświetla energy-rate: 0 W

---

**Gemini:**

Odczyt `energy-rate: 0 W` to kluczowa wskazówka (tzw. "smoking gun"). Oznacza to, że **komunikacja ACPI między systemem operacyjnym a kontrolerem baterii (Embedded Controller) została zerwana**.

System nie widzi przepływu prądu, ponieważ magistrala odpowiedzialna za odczyt czujników jest zablokowana. Potwierdza to, że problem z długim startem (4 minuty) wynika z **timeoutu sprzętowego** – system czeka na odpowiedź od sterownika lub sprzętu, której nigdy nie otrzymuje.

Oto plan naprawczy, zaczynając od resetu sprzętowego (specyficznego dla Lenovo), a kończąc na czystej reinstalacji sterowników, co jest teraz konieczne.

### Krok 1: Twardy reset kontrolera EC (Power Drain)

W laptopach Lenovo Legion modyfikacje stanów energetycznych GPU potrafią "ogłupić" kontroler wbudowany (EC). Objawia się to właśnie odczytem 0W, niedziałającą kontrolą jasności lub problemami z usypianiem.

1. Wyłącz laptopa całkowicie.
2. Odłącz zasilacz.
3. **Przytrzymaj przycisk zasilania (Power) przez pełne 60 sekund.** (Laptop może się włączyć i wyłączyć – trzymaj przycisk nadal).
4. Podłącz zasilacz.
5. Włącz laptopa normalnie.

*Sprawdź, czy czas uruchamiania się poprawił i czy `upower` pokazuje wartości inne niż 0W.*

### Krok 2: Całkowite usunięcie sterowników NVIDIA ("Nuclear Option")

Skoro ręczne usuwanie plików konfiguracyjnych nie pomogło, a system wisi przy starcie, oznacza to, że initramfs (obraz startowy) nadal zawiera uszkodzoną konfigurację lub skrypty startowe sterownika weszły w stan błędu.

Musimy wyczyścić wszystko do stanu "fabrycznego" Ubuntu (sterownik Nouveau).

Wykonaj te komendy w terminalu:

```
# 1. Usuń absolutnie wszystko związane z Nvidią
sudo apt purge "nvidia*" libnvidia* -y

# 2. Usuń nieużywane zależności (ważne!)
sudo apt autoremove -y

# 3. Wymuś reinstalację pakietu sterującego pulpitem (naprawia Plymouth)
sudo apt install --reinstall ubuntu-desktop-minimal gdm3

# 4. Zrestartuj system
sudo reboot
```

**Czego się spodziewać po restarcie:**

- System powinien uruchomić się znacznie szybciej (brak timeoutu sterownika Nvidia).
- Grafika może działać w niskiej rozdzielczości lub bez akceleracji (używany będzie sterownik otwarty Nouveau).
- Polecenie `nvidia-smi` nie będzie działać.

### Krok 3: Ponowna, czysta instalacja sterowników

Gdy system wstanie na czysto (i upewnisz się, że bootowanie trwa sekundy, a nie minuty), zainstaluj sterowniki ponownie, ale w sposób bezpieczny:

```
sudo apt update
sudo apt install nvidia-driver-550
```

*(Ubuntu 24.04 najlepiej współpracuje z wersją 550 na ten moment).*

Po instalacji i restarcie:

1. Nie wgrywaj żadnych ręcznych plików `.conf`.
2. Użyj `envycontrol -s hybrid`, aby ustawić tryb.
3. Sprawdź ponownie `upower`.

### Dlaczego to się stało?

Najprawdopodobniej doszło do tzw. **ACPI Race Condition**. Wymuszenie `NVreg_DynamicPowerManagement=0x02` w połączeniu ze skryptami `envycontrol` spowodowało, że sterownik próbował wyłączyć kartę w momencie, gdy Kernel próbował ją zainicjować. To zablokowało magistralę PCI, co z kolei zablokowało ACPI (stąd 0W na baterii) i spowodowało 90-sekundowy timeout na każdą usługę próbującą dostać się do sprzętu (stąd 4 minuty bootowania).

**Daj znać, czy po Kroku 2 (usunięcie sterowników) system odzyskał szybkość uruchamiania.** To pozwoli nam wyizolować problem.