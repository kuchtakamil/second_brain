# Alternatywy Remote Desktop Linux

**Data:** 2025-05-12

---

**User:**

czy jest odpowiednik Remote Desktop ale na linux?

---

**Assistant:**

Tak, na Linuksie jest wiele odpowiedników Remote Desktop z Windowsa. Oto najpopularniejsze opcje — w zależności od tego, czego dokładnie potrzebujesz:

---

### 🔹 **1. RDP (Remote Desktop Protocol) przez xrdp**
- **Opis**: xrdp to serwer RDP dla Linuksa, który pozwala łączyć się z maszyną Linuksową za pomocą standardowego klienta RDP z Windows.
- **Plusy**: Kompatybilność z klientami Windows, szybka konfiguracja.
- **Minusy**: Może być mniej stabilny lub wydajny niż inne rozwiązania.
- **Instalacja (Debian/Ubuntu)**:
  ```bash
  sudo apt install xrdp
  sudo systemctl enable xrdp
  ```

---

### 🔹 **2. VNC (np. TigerVNC, RealVNC, TightVNC)**
- **Opis**: Klasyczny sposób zdalnego pulpitu. Przesyła obraz pulpitu przez sieć.
- **Plusy**: Działa na wielu platformach, popularny w środowiskach linuksowych.
- **Minusy**: Mniejsza wydajność i jakość niż RDP; wymaga otwarcia portu (często 5900).
- **Instalacja (np. TigerVNC)**:
  ```bash
  sudo apt install tigervnc-standalone-server
  ```

---

### 🔹 **3. X2Go**
- **Opis**: Szybsza alternatywa dla VNC, bazująca na NX. Przesyła tylko zmienione fragmenty ekranu.
- **Plusy**: Bardzo wydajna, dobra kompresja, mniej zasobożerna.
- **Minusy**: Wymaga klienta X2Go.
- **Instalacja (serwer)**:
  ```bash
  sudo apt install x2goserver x2goserver-xsession
  ```

---

### 🔹 **4. SSH + X11 Forwarding**
- **Opis**: Nie jest to klasyczny zdalny pulpit, ale umożliwia uruchamianie aplikacji GUI zdalnie (np. `gedit`, `nautilus`) przez SSH.
- **Plusy**: Bardzo bezpieczne, bez potrzeby pełnego pulpitu.
- **Minusy**: Tylko pojedyncze aplikacje, nie cały pulpit.
- **Przykład**:
  ```bash
  ssh -X user@remote-host
  gedit
  ```

---

### 🔹 **5. Wayland + RDP (np. GNOME Remote Desktop w Waylandzie)**
- W nowszych środowiskach GNOME z Waylandem masz wbudowane wsparcie dla RDP, które działa bardzo dobrze i wspiera np. Windowsowy klient RDP (`mstsc`).
- Ustawienia ➝ Udostępnianie ➝ Zdalny pulpit

---

Chcesz zdalnie połączyć się z Linuksem z Windowsa, czy między dwoma Linuksami?