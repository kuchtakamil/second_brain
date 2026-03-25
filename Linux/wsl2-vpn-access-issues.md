# WSL2 VPN Access Issues

**Data:** 2024-09-13

---

**User:**

Na Windows 11 mam VPN, dzięki któremu mogę dostać się do strony x.yz. Mam też tutaj zainstalowany WSL2, a na nim Ubuntu. Gdy jestem podłączony w Windows do VPN, mogę dostać się do strony x.yz. Jednak w tym samym momencie korzystając z Ubuntu na WSL2 nie mogę tego zrobić. Jak to naprawić?

---

**Assistant:**

Problem, który opisujesz, wynika z tego, że domyślnie WSL2 korzysta z własnego wirtualnego interfejsu sieciowego i nie dziedziczy ustawień sieciowych ani połączeń VPN skonfigurowanych w systemie Windows. Aby rozwiązać ten problem i umożliwić dostęp do sieci VPN z Ubuntu na WSL2, można spróbować kilku metod:

### 1. Skonfiguruj przekierowanie ruchu przez Windows

Możesz skonfigurować WSL2, aby używał tej samej bramy, co system Windows:

1. **Sprawdź bramę domyślną Windows:**
   W wierszu poleceń Windows (CMD lub PowerShell) wpisz:
   ```
   ipconfig
   ```
   Znajdź adres bramy domyślnej dla interfejsu VPN. Będzie to adres IP, który wygląda jak „192.168.x.x” lub podobny.

2. **Skonfiguruj WSL2 do korzystania z tej samej bramy:**
   W terminalu WSL2 wpisz:
   ```
   ip route add default via [adres_bramy] dev eth0
   ```
   Zastąp `[adres_bramy]` rzeczywistym adresem bramy domyślnej uzyskanym w kroku 1.

3. **Sprawdź, czy działa połączenie:**
   Po tej zmianie sprawdź, czy możesz uzyskać dostęp do strony `x.yz`.

### 2. Przekierowanie ruchu do WSL2 przez NAT

Inna opcja to skonfigurowanie przekierowania NAT na interfejsie VPN:

1. **Włącz udostępnianie połączenia sieciowego:**
   - Przejdź do ustawień połączenia sieciowego VPN na Windows.
   - W zakładce „Udostępnianie” włącz opcję „Zezwalaj innym użytkownikom sieci na łączenie się przez połączenie internetowe tego komputera”.

2. **Skonfiguruj interfejs WSL2:**
   Musisz dodać regułę przekierowania NAT z interfejsu Windows do WSL2. W tym celu uruchom PowerShell z uprawnieniami administratora i wpisz:
   ```
   netsh interface portproxy add v4tov4 listenport=80 listenaddress=0.0.0.0 connectport=80 connectaddress=[adres_wsl2]
   ```
   Zastąp `[adres_wsl2]` adresem IP WSL2, który można uzyskać, wpisując w terminalu WSL2:
   ```
   ip addr show eth0
   ```

### 3. Zaktualizuj plik `/etc/resolv.conf` w WSL2

Czasami problemem jest także rozdzielność DNS. Aby WSL2 korzystał z tego samego DNS, co Windows:

1. **Edytuj plik `/etc/resolv.conf`:**
   Otwórz terminal WSL2 i zedytuj plik `/etc/resolv.conf`:
   ```
   sudo nano /etc/resolv.conf
   ```

2. **Dodaj adresy serwerów DNS z Windows:**
   Sprawdź serwery DNS w systemie Windows, używając polecenia `ipconfig /all` w CMD, i skopiuj je do pliku `resolv.conf`.

3. **Zablokuj automatyczne nadpisywanie pliku:**
   Aby WSL2 nie nadpisywał tego pliku przy każdym uruchomieniu, zablokuj jego edytowanie:
   ```
   sudo chattr +i /etc/resolv.conf
   ```

### 4. Aktualizacja WSL i Windows

Upewnij się, że masz najnowsze wersje Windows i WSL, ponieważ Microsoft stale aktualizuje WSL2, wprowadzając nowe funkcje i poprawki błędów, które mogą rozwiązać twój problem.

### 5. Skonfiguruj VPN bezpośrednio na WSL2

Jeśli powyższe metody nie działają, można spróbować skonfigurować klienta VPN bezpośrednio na Ubuntu (WSL2). To podejście zapewni bezpośredni dostęp do VPN na poziomie Ubuntu, niezależnie od ustawień Windows.

1. Zainstaluj klienta VPN odpowiedniego dla twojego dostawcy VPN (np. OpenVPN, WireGuard, Cisco VPN itp.).
2. Skonfiguruj klienta VPN na WSL2, korzystając z plików konfiguracyjnych dostarczonych przez twojego dostawcę.

Jeśli będziesz potrzebować dalszej pomocy, daj znać!