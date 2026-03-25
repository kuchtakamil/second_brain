# systemd-analyze blame

**Data:** 19 lis 2025, 18:52:40 CET

---

**User:**

systemd-analyze blame                                                                         ──(śro,lis19)─┘
1min 25.258s systemd-journald.service
     21.246s plymouth-quit-wait.service
      5.727s NetworkManager-wait-online.service
      2.181s postgresql@16-main.service
      1.823s gpu-manager.service
      1.816s nvidia-persistenced.service
      1.401s snapd.seeded.service
      1.397s snapd.service

Oraz drugi wynik
systemd-analyze critical-chain                                                                ──(śro,lis19)─┘
The time when unit became active or started is printed after the "@" character.
The time the unit took to start is printed after the "+" character.

graphical.target @1min 48.233s
└─multi-user.target @1min 48.233s
  └─plymouth-quit-wait.service @1min 26.986s +21.246s
    └─systemd-user-sessions.service @1min 26.982s +3ms
      └─network.target @1min 26.966s
        └─NetworkManager.service @1min 25.978s +988ms
          └─dbus.service @1min 25.923s +45ms
            └─basic.target @1min 25.823s
              └─sockets.target @1min 25.823s
                └─snapd.socket @1min 25.822s +617us
                  └─sysinit.target @1min 25.810s
                    └─systemd-resolved.service @1min 25.757s +52ms
                      └─systemd-tmpfiles-setup.service @1min 25.713s +29ms
                        └─systemd-journal-flush.service @1min 25.639s +55ms
                          └─systemd-journald.service @336ms +1min 25.258s
                            └─systemd-journald.socket @333ms

---

**Gemini:**

Winowajcą jest jednoznacznie **`systemd-journald.service`**, który blokuje start systemu na **1 min 25 s**. To usługa odpowiedzialna za zapisywanie logów systemowych.

Skoro modyfikowałeś sterowniki i restartowałeś komputer (być może "na twardo" przy zawieszeniu), doszło do jednego z dwóch scenariuszy:

1. **Uszkodzenie plików dziennika (Corruption):** Pliki binarne logów zostały uszkodzone, a system przy starcie próbuje je naprawić/zweryfikować, co trwa wieki.
2. **Spam błędami (Log flood):** Coś (prawdopodobnie sterownik Nvidii lub pętla w udev) generuje gigabajty błędów w ułamku sekundy, zapychając dziennik.

Oto procedura naprawcza:

### Krok 1: Weryfikacja i naprawa dziennika (Najbezpieczniejsza metoda)

Sprawdźmy, ile miejsca zajmują logi i czy są uszkodzone.

1. **Sprawdź rozmiar:**

   ```
   journalctl --disk-usage
   ```

   Jeśli wynik idzie w gigabajty (np. >4GB), to jest Twój problem.
2. **Sprawdź spójność:**

   ```
   sudo journalctl --verify
   ```

   Jeśli zobaczysz dużo komunikatów na czerwono (`FAIL`, `CORRUPTED`), pliki są uszkodzone.
3. **Wyczyść dziennik (Vacuum):**
   To polecenie usunie stare logi, zostawiając tylko te z ostatniej 1 sekundy (skuteczny reset):

   ```
   sudo journalctl --vacuum-time=1s
   ```

   *Uwaga: Operacja może chwilę potrwać, jeśli pliki są ogromne.*

Po wykonaniu `vacuum`, zrestartuj komputer i sprawdź czas uruchamiania.

### Krok 2: Metoda "Nuklearna" (Jeśli krok 1 nie działa)

Jeśli `journalctl` zawiesza się przy próbie czyszczenia (co zdarza się przy silnym uszkodzeniu plików), trzeba ręcznie usunąć katalog logów. Systemd automatycznie utworzy nowy, czysty katalog przy starcie.

```
# Zatrzymujemy usługę logowania (może chwilę potrwać)
sudo systemctl stop systemd-journald

# Przenosimy uszkodzone logi w bezpieczne miejsce (backup) lub usuwamy
sudo mv /var/log/journal /var/log/journal_backup

# Restartujemy usługę (stworzy nowy katalog)
sudo systemctl restart systemd-journald
```

### Krok 3: Sprawdzenie, czy problem powraca (Log flood)

Gdy system wstanie już szybko, musisz upewnić się, że logi nie są ponownie zalewane błędami, co doprowadziłoby do powrotu problemu za kilka dni.

Uruchom podgląd na żywo:

```
journalctl -f
```

Jeśli tekst "płynie" tak szybko, że nie da się go czytać, masz "Log Flood".

- Czy widzisz powtarzające się komunikaty związane z `nvidia`, `pci`, `acpi` lub `udev`?
- Jeśli tak, wklej przykładowy fragment błędu.

Jeśli logi są spokojne (kilka linii na minutę), problemem było jednorazowe uszkodzenie plików przy twardym resecie i **system jest naprawiony**.