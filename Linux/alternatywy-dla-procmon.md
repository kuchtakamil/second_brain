# Alternatywy dla ProcMon

**Data:** 2025-03-15

---

**User:**

Na WIndows ostatnio skorzystałem z programu Process Monitor (Sysinternals) aby zlokalizować z jakich plików korzysta dana aplikacja. Czy istnieje odpowiednik na Linux i Macos?

---

**Assistant:**

Tak, zarówno na **Linuxie**, jak i na **macOS**, istnieją odpowiedniki **Process Monitor (ProcMon)** z Sysinternals, które pozwalają monitorować, jakie pliki, procesy, biblioteki itp. są używane przez aplikacje.

---

### ✅ **Odpowiedniki ProcMon na Linuxa:**

1. **`strace`**  
   - Śledzi system calls i sygnały wykonywane przez proces.
   - Przykład użycia:
     ```bash
     strace -e trace=file -p <PID>
     ```
     lub jeśli chcesz uruchomić program i śledzić jego dostęp do plików:
     ```bash
     strace -e trace=file ./moja_aplikacja
     ```

2. **`lsof` (List Open Files)**  
   - Pokazuje wszystkie otwarte pliki (w tym gniazda, biblioteki itp.).
   - Przykład:
     ```bash
     lsof -p <PID>
     ```

3. **`inotify` narzędzia (np. inotifywait, inotifywatch)**  
   - Monitorują zmiany w systemie plików.
   - Przykład:
     ```bash
     inotifywait -m /ścieżka/do/katalogu
     ```

4. **`auditd` + `ausearch` / `auditctl`**  
   - Bardziej zaawansowane, do audytowania dostępu do plików (często używane w serwerach produkcyjnych).
   - Przykład:
     ```bash
     auditctl -w /etc/passwd -p rwxa
     ausearch -f /etc/passwd
     ```

5. **`bpftrace` / `eBPF` tools (nowoczesne i potężne)**  
   - Przykład prostego programu:
     ```bash
     sudo bpftrace -e 'tracepoint:syscalls:sys_enter_openat { printf("%s\n", str(args->filename)); }'
     ```

6. **SystemTap**  
   - Alternatywa dla eBPF, bardziej rozbudowana, ale trudniejsza w konfiguracji.

7. **`procmon` dla Linuxa (od Microsoft!)**  
   - Tak, Microsoft udostępnił wersję **ProcMon dla Linuxa (procmon-for-linux)** – projekt open-source oparty o eBPF.
   - Repozytorium: [https://github.com/microsoft/ProcMon-for-Linux](https://github.com/microsoft/ProcMon-for-Linux)
   - Możesz go zbudować i używać w podobny sposób jak na Windowsie.

---

### ✅ **Odpowiedniki ProcMon na macOS:**

1. **`fs_usage`**  
   - Pokazuje dostęp do systemu plików i I/O procesów.
   - Przykład:
     ```bash
     sudo fs_usage
     sudo fs_usage -w -f filesys <nazwa_procesu>
     ```

2. **`dtrace`**  
   - Zaawansowane narzędzie (jak eBPF/SystemTap), pozwala pisać skrypty śledzące zachowanie systemu.
   - Apple udostępnia wiele skryptów dtrace w `/usr/bin`.

3. **`lsof`** – jak na Linuxie.

4. **`Instruments` (część Xcode)**  
   - Graficzne narzędzie do monitorowania aktywności systemowej, w tym dysku, sieci, pamięci itp.

---

### Podsumowanie:

| System | Narzędzie tekstowe | Graficzne |
|--------|---------------------|------------|
| Linux  | strace, lsof, inotify, auditd, procmon-for-linux, bpftrace | brak natywnego GUI (ale można użyć np. KSystemLog, Gnome System Monitor) |
| macOS  | fs_usage, dtrace, lsof | Instruments (Xcode) |

---

Jeśli chcesz, mogę podpowiedzieć konkretne przykłady użycia pod Twoją aplikację – daj znać, co monitorujesz (np. dostęp do konkretnego katalogu, bibliotek, plików konfiguracyjnych?).