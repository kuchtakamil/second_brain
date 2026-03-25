# Poprawa polecenia bash

**Data:** 2025-11-19

---

**User:**

popraw
watch -n 1 upower -i /org/freedesktop/UPower/devices/battery_BAT0 | grep enery-rate

---

**Assistant:**

Poprawiona wersja:

```bash
watch -n 1 "upower -i /org/freedesktop/UPower/devices/battery_BAT0 | grep energy-rate"
```

Zmiany:
- Literówka: `enery-rate` → `energy-rate`
- Całe polecenie po `watch` objęte w cudzysłowy, aby `grep` działał poprawnie.

---

**User:**

a  mogę pokazywać kilka wyników czyli do tego co jest np. jeszcze cat /sys/bus/pci/devices/0000:01:00.0/power/runtime_status

---

**Assistant:**

Tak, możesz. Masz kilka opcji — najprostsza to wykonanie dwóch poleceń w bloku, które `watch` będzie uruchamiać za każdym razem.

### Opcja 1: Użycie `{ ...; }`
```bash
watch -n 1 '{ upower -i /org/freedesktop/UPower/devices/battery_BAT0 | grep energy-rate; cat /sys/bus/pci/devices/0000:01:00.0/power/runtime_status; }'
```

### Opcja 2: Podwójne polecenie z `;`
(ale wymaga ujęcia całości w cudzysłowy)
```bash
watch -n 1 "upower -i /org/freedesktop/UPower/devices/battery_BAT0 | grep energy-rate; cat /sys/bus/pci/devices/0000:01:00.0/power/runtime_status"
```

### Opcja 3: Oddzielna funkcja/skrót (czytelniejsze)
```bash
mycheck() {
    upower -i /org/freedesktop/UPower/devices/battery_BAT0 | grep energy-rate
    cat /sys/bus/pci/devices/0000:01:00.0/power/runtime_status
}
watch -n 1 mycheck
```

Jeśli chcesz, mogę pomóc zrobić wersję z kolorowaniem lub formatowaniem wyniku.