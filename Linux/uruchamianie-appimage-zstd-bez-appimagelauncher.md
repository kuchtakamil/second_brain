---
tags: [claude-code, linux, appimage]
date: 2026-06-02
---
# Uruchamianie AppImage (zstd) bez AppImageLauncher

## Problem / objawy
Przy uruchamianiu AppImage (np. Handy 0.8.3) sypały się błędy:
- 'Squashfs image uses (null) compression, this version supports only xz, zlib.'
- 'Failed to register AppImage in system via libappimage'
- 'appimage_shall_not_be_integrated ... sqfs_open_image error'
- 'Permission denied' (po zdjęciu prawa wykonywania)

## Przyczyna źródłowa
Winowajcą NIE był sam AppImage, tylko stary **AppImageLauncher 2.2.0**:
- rejestruje w jądrze handler binfmt_misc (interpreter /usr/bin/AppImageLauncher), więc przechwytuje KAŻDE uruchomienie AppImage,
- jego libsquashfs czyta tylko kompresję xz/zlib,
- nowoczesne AppImage (m.in. budowane w Tauri) używają **zstd** -> AppImageLauncher nie umie ich otworzyć ani zintegrować, a jego demon potrafi zdjąć +x z pliku (stąd 'Permission denied').

## Jak zweryfikować, że plik jest zdrowy
AppImage type-2 = mały ELF (runtime) + doklejony obraz squashfs.

Typ pliku i kandydaci na offset payloadu:

    file plik.AppImage              # ELF 64-bit ... pie executable
    grep -aboF 'hsqs' plik.AppImage # offsety magii squashfs

Odczyt superbloku systemowym unsquashfs (squashfs-tools 4.4+ obsługuje zstd):

    unsquashfs -s -o <offset> plik.AppImage

Szukamy: 'Found a valid SQUASHFS ... superblock' oraz 'Compression zstd'.
Uwaga: pierwsze trafienie hsqs bywa przypadkowe wewnątrz ELF - właściwy offset to ten, na którym superblok jest poprawny.

## Rozwiązanie (czyste, trwałe)
Usunąć AppImageLauncher - jest nierozwijany i psuje każdy nowy AppImage:

    sudo apt remove -y appimagelauncher   # usuwa binarki + handler binfmt
    sudo apt purge  -y appimagelauncher   # opcjonalnie kasuje resztki konfiguracji (status rc)

Sprawdzenie, że handler binfmt zniknął:

    ls /proc/sys/fs/binfmt_misc/ | grep appimage   # brak = OK

Uruchomienie natywne (runtime AppImage sam obsługuje zstd):

    chmod +x plik.AppImage
    ./plik.AppImage

Status w dpkg: rc = removed+config (binarki usunięte), ii = zainstalowany.

## Integracja z menu (ikona + .desktop)
Wyciągnięcie ikony i .desktop z wnętrza obrazu:

    unsquashfs -o <offset> -d /tmp/wy plik.AppImage /usr/share/applications/Nazwa.desktop /Nazwa.png

Pliki integracji XDG:
- ikona: ~/.local/share/icons/hicolor/256x256/apps/handy.png
- wpis:  ~/.local/share/applications/handy.desktop

Przykładowy wpis menu:

    [Desktop Entry]
    Type=Application
    Name=Handy
    Exec=/home/kamil/handy/Handy_0.8.3_amd64.AppImage
    Icon=handy
    Terminal=false
    Categories=Utility;
    StartupWMClass=handy

Odświeżenie i walidacja:

    update-desktop-database ~/.local/share/applications
    gtk-update-icon-cache -f -t ~/.local/share/icons/hicolor
    desktop-file-validate ~/.local/share/applications/handy.desktop

Uwaga: zostaw jedną główną kategorię (np. Utility;), inaczej apka pojawi się w menu dwa razy.

## Autostart przy logowaniu
Standard XDG - wpis .desktop w ~/.config/autostart/ (działa w GNOME/KDE/XFCE mimo prefiksu X-GNOME-):

    [Desktop Entry]
    Type=Application
    Name=Handy
    Exec=/home/kamil/handy/Handy_0.8.3_amd64.AppImage
    Terminal=false
    X-GNOME-Autostart-enabled=true
    X-GNOME-Autostart-Delay=5

- X-GNOME-Autostart-enabled=true -> włącza autostart
- X-GNOME-Autostart-Delay=5 -> kilka sekund zwłoki, by sesja (audio, tray, sieć) zdążyła wstać
Wyłączenie: rm ~/.config/autostart/handy.desktop

## Wnioski na przyszłość
- Błąd '(null) compression / only xz, zlib' = za stary czytnik squashfs (zwykle AppImageLauncher), a nie uszkodzony plik.
- AppImage ma własny runtime z obsługą zstd - wystarczy ominąć przechwytywanie.
- binfmt_misc sprawia, że nawet ./plik trafia do interpretera AppImageLauncher.
- Systemowy unsquashfs to niezależne narzędzie do diagnozy i rozpakowania AppImage.

## Rezygnacja z Handy (deinstalacja)

### 1. Wyłączenie autostartu (najważniejsze)
Autostart to wyłącznie plik wpisu XDG - usunięcie pliku = koniec autostartu:

    rm ~/.config/autostart/handy.desktop

Alternatywnie, bez kasowania, można go tylko dezaktywować zmieniając flagę na false:

    X-GNOME-Autostart-enabled=false

W GUI: GNOME Tweaks -> Startup Applications (albo Ustawienia/menedżer sesji w KDE/XFCE) -> usuń Handy z listy.
Weryfikacja: po wylogowaniu i zalogowaniu Handy nie powinno wstać samo.

### 2. Zatrzymanie działającej instancji

    pkill -f Handy_0.8.3_amd64.AppImage

(lub zamknij z ikony w trayu).

### 3. Usunięcie wpisu z menu i ikony

    rm ~/.local/share/applications/handy.desktop
    rm ~/.local/share/icons/hicolor/256x256/apps/handy.png
    update-desktop-database ~/.local/share/applications
    gtk-update-icon-cache -f -t ~/.local/share/icons/hicolor

### 4. Usunięcie samego AppImage

    rm ~/handy/Handy_0.8.3_amd64.AppImage

### 5. Usunięcie danych i konfiguracji aplikacji (opcjonalnie)
Handy trzyma dane (baza historii, pobrane modele Whisper, ustawienia) w katalogach aplikacji:

    rm -rf ~/.local/share/com.pais.handy
    rm -rf ~/.config/com.pais.handy
    rm -rf ~/.cache/com.pais.handy

Uwaga: to kasuje historię transkrypcji i pobrane modele - po reinstalacji trzeba je pobrać na nowo.

### Szybka checklista
- [ ] rm ~/.config/autostart/handy.desktop   (autostart off)
- [ ] zamknięcie działającej instancji (pkill)
- [ ] rm wpisu menu + ikony (+ odświeżenie baz)
- [ ] rm pliku AppImage
- [ ] (opcjonalnie) rm katalogów com.pais.handy