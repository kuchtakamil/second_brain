# Dostaję error przy próbie instalacji pip install envycontrol

**Data:** 19 lis 2025, 17:46:30 CET

---

**User:**

Dostaję error przy próbie instalacji
pip install envycontrol                                                                                                                  ──(śro,lis19)─┘
error: externally-managed-environment

---

**Gemini:**

Ten błąd wynika z wprowadzenia standardu **PEP 668** w Ubuntu 24.04. System blokuje instalację pakietów Python przez `pip` na poziomie globalnym, aby uniknąć konfliktów z menedżerem pakietów systemowych (`apt`). Ponieważ `envycontrol` jest narzędziem systemowym wymagającym uprawnień administratora (`sudo`) do modyfikacji plików startowych, standardowe obejścia (jak instalacja w środowisku użytkownika) są problematyczne w użyciu.

Oto dwa rozwiązania, jak zainstalować `envycontrol` na Ubuntu 24.04:

### Metoda 1: Użycie flagi `--break-system-packages` (Najszybsza)

Dla narzędzi systemowych takich jak EnvyControl, które nie mają swoich paczek `.deb` w repozytorium, dopuszczalne jest wymuszenie instalacji. Ponieważ EnvyControl ma minimalne zależności, ryzyko uszkodzenia systemu jest znikome.

Wpisz w terminalu:

```
sudo pip install envycontrol --break-system-packages
```

Po tej operacji komenda `sudo envycontrol` powinna być dostępna globalnie.

### Metoda 2: Instalacja poprzez `pipx` (Bezpieczniejsza, "czysta")

`pipx` tworzy izolowane środowiska dla aplikacji Python, nie zaśmiecając systemu. Jest to zalecana metoda w nowoczesnym Pythonie, ale wymaga specyficznego wywoływania przy użyciu `sudo`.

1. **Zainstaluj pipx:**

   ```
   sudo apt install pipx
   pipx ensurepath
   ```

   *(Może być konieczne przelogowanie lub ponowne otwarcie terminala)*.
2. **Zainstaluj EnvyControl:**

   ```
   pipx install envycontrol
   ```
3. **Uruchamianie:**
   Ponieważ `pipx` instaluje pakiety w katalogu użytkownika (`~/.local/bin`), komenda `sudo` ich domyślnie nie widzi. Musisz podać pełną ścieżkę lub przekazać środowisko:

   ```
   sudo $(which envycontrol) -s integrated
   # LUB jeśli powyższe nie zadziała:
   sudo /home/$USER/.local/bin/envycontrol -s integrated
   ```

### Konfiguracja po instalacji (Kluczowe dla GDM/Ubuntu)

Ponieważ używasz Ubuntu 24.04, domyślnym menedżerem logowania jest GDM (GNOME Display Manager). EnvyControl musi być skonfigurowany tak, aby poprawnie nim zarządzać, w przeciwnym razie po przełączeniu grafiki możesz zobaczyć czarny ekran (black screen).

Upewnij się, że masz zainstalowany menedżer wyświetlania (zazwyczaj jest, ale warto sprawdzić):

```
sudo apt install gdm3
```

Przykładowe przełączenie na tryb zintegrowany (oszczędzanie baterii) z wymuszeniem resetu GDM:

```
sudo envycontrol -s integrated --dm gdm3
```

*(Flagę `--dm gdm3` warto dodać dla pewności, choć narzędzie zazwyczaj wykrywa GDM automatycznie).*

---

**Czy po wykonaniu instalacji (Metodą 1 lub 2) komenda `sudo envycontrol --query` zwraca aktualny tryb pracy?**