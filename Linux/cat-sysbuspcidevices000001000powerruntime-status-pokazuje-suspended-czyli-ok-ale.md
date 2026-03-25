# cat /sys/bus/pci/devices/0000:01:00.0/power/runtime_status pokazuje suspended, c

**Data:** 19 lis 2025, 18:04:17 CET

---

**User:**

cat /sys/bus/pci/devices/0000:01:00.0/power/runtime_status pokazuje suspended, czyli ok ale wciąż
sudo lsof /dev/nvidia0  
lsof: WARNING: can't stat() fuse.portal file system /run/user/1000/doc
      Output information may be incomplete.
lsof: WARNING: can't stat() fuse.gvfsd-fuse file system /run/user/1000/gvfs
      Output information may be incomplete.
COMMAND  PID  USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
Xorg    2343 kamil  mem    CHR  195,0          1330 /dev/nvidia0
Xorg    2343 kamil   20u   CHR  195,0      0t0 1330 /dev/nvidia0
Xorg    2343 kamil   21u   CHR  195,0      0t0 1330 /dev/nvidia0
Xorg    2343 kamil   22u   CHR  195,0      0t0 1330 /dev/nvidia0
Xorg    2343 kamil   27u   CHR  195,0      0t0 1330 /dev/nvidia0
Xorg    2343 kamil   28u   CHR  195,0      0t0 1330 /dev/nvidia0
Xorg    2343 kamil   30u   CHR  195,0      0t0 1330 /dev/nvidia0
Xorg    2343 kamil   31u   CHR  195,0      0t0 1330 /dev/nvidia0
Xorg    2343 kamil   32u   CHR  195,0      0t0 1330 /dev/nvidia0
Xorg    2343 kamil   42u   CHR  195,0      0t0 1330 /dev/nvidia0
Xorg    2343 kamil   54u   CHR  195,0      0t0 1330 /dev/nvidia0

---

**Gemini:**

Fakt, że widzisz `suspended` w `runtime_status` to **bardzo dobra wiadomość**. Oznacza to, że kernel pomyślnie odciął zasilanie od szyny PCI karty graficznej. Karta jest w stanie *D3cold*.

Obecność procesu `Xorg` na liście `lsof` w tym scenariuszu jest **normalna i oczekiwana** w trybie Hybrid (On-Demand).

- **Dlaczego?** Serwer wyświetlania (Xorg) musi trzymać "uchwyt" (file descriptor) do sterownika NVIDIA, aby w ułamku sekundy móc wybudzić kartę, gdy uruchomisz grę. Xorg działa tu jako bramkarz (gatekeeper). Dopóki nie wysyła do karty poleceń renderowania, sterownik utrzymuje ją w uśpieniu mimo otwartego połączenia.

Jeśli mimo statusu `suspended` bateria znika szybko, musimy zweryfikować trzy inne obszary, które w laptopach Lenovo Legion są częstszymi winowajcami niż samo GPU w stanie spoczynku.

### 1. Weryfikacja stabilności stanu Suspended (Flapping)

Czasami status pokazuje `suspended`, ale w rzeczywistości karta wybudza się co kilka sekund na moment, a potem znów zasypia. To zjawisko (rapid wakeups) drenuje baterię bardziej niż ciągła praca.

Uruchom w terminalu podgląd na żywo (zostaw to okno na boku i obserwuj przez minutę, nic nie robiąc):

```
watch -n 1 cat /sys/bus/pci/devices/0000:01:00.0/power/runtime_status
```

Jeśli status jest stabilny i cały czas widnieje `suspended` – GPU jest poprawnie skonfigurowane i **nie jest** źródłem problemu.
Jeśli miga na `active` i wraca do `suspended` – masz proces, który "puka" do karty (np. monitor zasobów, widget GNOME pokazujący temperaturę GPU).

### 2. Pomiar faktycznego drenażu (Discharge Rate)

Musimy ustalić, ile dokładnie watów zużywa laptop. "Szybciej wyczerpuje" to odczucie subiektywne, a waty to twarde dane.

Wpisz:

```
upower -i /org/freedesktop/UPower/devices/battery_BAT0
```

*(Jeśli BAT0 nie istnieje, spróbuj BAT1)*.

Szukaj linii `energy-rate`.

- **< 15 W:** Wynik bardzo dobry dla laptopa gamingowego na Linuxie (GPU śpi).
- **15 W - 25 W:** Przeciętnie, coś lekko obciąża system (CPU lub ekran).
- **> 25 W:** GPU prawdopodobnie pracuje lub procesor jest na wysokich taktowaniach.

Jeśli masz `suspended` a pobór mocy wynosi np. 30W, problem leży w **CPU** lub **Ekranie**, a nie w RTX 4070.

### 3. Częstotliwość odświeżania ekranu (Legion Killer)

To najczęstszy, przeoczany powód problemów na Legionach. Ubuntu domyślnie ustawia maksymalne odświeżanie (np. 165Hz lub 240Hz).
Utrzymanie 165Hz na pulpicie powoduje, że:

1. Zintegrowana karta Intel/AMD nie może wejść w niskie stany energetyczne.
2. Procesor (CPU) rzadziej wchodzi w głębokie stany C-states.

**Co zrobić:**
Wejdź w: **Settings -> Displays**.
Zmień **Refresh Rate** na **60 Hz**.
Sprawdź ponownie `energy-rate` w `upower`. Różnica może wynosić nawet 5-8 Watów.

### 4. Agresywne taktowanie CPU (Turbo Boost)

Linuxowe zarządcy (governors) często utrzymują procesory Intel Core (szczególnie serii H/HX w Legionach) na zbyt wysokich taktowaniach, nawet gdy przeglądasz internet.

Zalecam instalację narzędzia **auto-cpufreq**, które dynamicznie "dusi" procesor na baterii, a "puszcza" na kablu. Działa znacznie lepiej niż domyślny `power-profiles-daemon` w Ubuntu.

**Instalacja:**

```
git clone https://github.com/AdnanHodzic/auto-cpufreq.git
cd auto-cpufreq && sudo ./auto-cpufreq-installer
```

Podczas instalacji narzędzie wykryje konflikt z `power-profiles-daemon` i zaproponuje jego wyłączenie – zgódź się. Po restarcie narzędzie automatycznie zoptymalizuje taktowanie CPU.

### Podsumowanie diagnostyki

Skoro `runtime_status` to `suspended`, to **problem z RTX 4070 został rozwiązany**. Xorg na liście procesów to fałszywy alarm w tym kontekście.

Twój plan działania teraz:

1. Zmień odświeżanie ekranu na 60Hz.
2. Sprawdź `energy-rate` przez `upower`.
3. Zainstaluj `auto-cpufreq` dla okiełznania procesora.

Czy po zmianie odświeżania na 60Hz widzisz znaczący spadek w `energy-rate`?