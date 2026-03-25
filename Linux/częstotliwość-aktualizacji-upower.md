# Częstotliwość aktualizacji UPower

**Data:** 2025-11-19

---

**User:**

polecenie upower -i /org/freedesktop/UPower/devices/battery_BAT0
zmienia wyniki co 30 sekund. Czy można ustawić żeby aktualizacje zdarzały się częściej?

---

**Assistant:**

Krótka odpowiedź: **nie, w UPower nie da się ustawić częstszych aktualizacji**.

Szczegóły:

- `upower -i ...` tylko **wyświetla** dane, które zbiera demon `upowerd`.
- `upowerd` nie ma opcji konfigurowania częstotliwości odświeżania. Dane pochodzą głównie z ueventów jądra (`/sys/class/power_supply/...`).  
  Jeśli sprzęt lub sterownik wysyła aktualizacje co ~30 s, UPower po prostu je odbiera.
- W wielu laptopach to **sterownik baterii** ustala częstotliwość raportowania i tego zwykle nie da się zmienić od strony UPower.

Jeśli potrzebujesz częstszych zmian, są jedynie obejścia:

1. **Bezpośrednie czytanie z /sys**, np.:
   ```bash
   watch -n 1 cat /sys/class/power_supply/BAT0/capacity
   ```
   To odświeża co sekundę, ale wartości i tak zmienią się tylko wtedy, kiedy sterownik je zaktualizuje.

2. **Monitorowanie zdarzeń**:
   ```bash
   upower --monitor-detail
   ```
   Ale znowu – pojawią się tylko wtedy, kiedy bateria wygeneruje uevent.

3. **Narzędzia specyficzne dla ACPI** (np. `acpi -V`), ale one również korzystają z tych samych danych.

Jeżeli chcesz, opisz proszę, jaki masz cel (np. logowanie, monitoring, alerty), to zasugeruję najbardziej sensowny sposób obejścia.