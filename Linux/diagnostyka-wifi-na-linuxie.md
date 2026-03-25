# Diagnostyka WiFi na Linuxie

**Data:** 2025-10-20

---

**User:**

Mam router Horizon GO z UPC i gdy łączę się z siecią WiFi to mogę się z nią połączyć ale brak jest internetu. Co na linuxie na swoim urządzeniu będąc podłączonym do tego wifi mogę sprawdzić?

---

**Assistant:**

Dobrze — jeśli masz połączenie z Wi-Fi, ale **brak internetu**, to znaczy, że:  
- warstwa **radiowa i DHCP** działa (dostałeś adres IP),  
- ale coś nie działa na poziomie **DNS / routingu / połączenia z siecią zewnętrzną**.  

Na Linuksie możesz to rozpracować krok po kroku. Poniżej pełna, rzetelna lista diagnostyczna:

---

### 🔹 1. Sprawdź, czy masz adres IP i bramę
```bash
ip addr show
ip route show
```

Zwróć uwagę:
- Czy interfejs Wi-Fi (np. `wlp3s0`) ma **adres IP z podsieci routera** (np. `192.168.x.x`)?
- Czy w `ip route show` masz wpis podobny do:
  ```
  default via 192.168.0.1 dev wlp3s0
  ```
  Jeśli nie — nie masz ustawionej bramy domyślnej.

---

### 🔹 2. Sprawdź DNS
Zobacz, jakie serwery DNS są ustawione:
```bash
cat /etc/resolv.conf
```
lub (na systemd):
```bash
resolvectl status
```
Spróbuj rozwiązać domenę:
```bash
dig google.com
# lub
nslookup google.com
```
Jeśli nie działa, ale ping po IP działa (patrz niżej), to masz problem **z DNS-ami**.

---

### 🔹 3. Sprawdź, czy router odpowiada
```bash
ping -c 4 192.168.0.1
```
Jeśli router nie odpowiada — problem z lokalnym połączeniem.

---

### 🔹 4. Sprawdź, czy masz dostęp do internetu po IP
```bash
ping -c 4 8.8.8.8
```
- Jeśli **ping 8.8.8.8 działa**, ale `ping google.com` nie — to DNS.
- Jeśli **ping 8.8.8.8 nie działa**, to brak routingu / NAT.

---

### 🔹 5. Sprawdź tablicę routingu
```bash
ip route
```
Powinieneś widzieć coś jak:
```
default via 192.168.0.1 dev wlp3s0 proto dhcp metric 600
```
Jeśli nie ma „default via” — możesz dodać ręcznie:
```bash
sudo ip route add default via 192.168.0.1
```
(oczywiście z poprawnym adresem twojego routera)

---

### 🔹 6. Sprawdź stan połączenia DHCP
```bash
sudo dhclient -v wlp3s0
```
Zobacz, czy dostajesz lease (adres IP, DNS, gateway).  
Czasem Horizon ma problem z DHCP i trzeba odświeżyć lease.

---

### 🔹 7. Sprawdź bramę pod kątem NAT / internetu
Możesz użyć `traceroute`:
```bash
traceroute 8.8.8.8
```
Zobacz, gdzie ruch się zatrzymuje. Jeśli zatrzymuje się na bramie (np. 192.168.0.1), router nie ma połączenia z siecią zewnętrzną.

---

### 🔹 8. Sprawdź firewall (ufw / iptables)
```bash
sudo ufw status
sudo iptables -L -v -n
```
Wyklucz przypadek, że lokalny firewall blokuje ruch.

---

### 🔹 9. (opcjonalnie) Sprawdź logi systemowe
```bash
sudo dmesg | grep wlp
journalctl -u NetworkManager --since "10 minutes ago"
```
Tam często widać, czy DHCP się nie powiodło, lub czy jest problem z połączeniem.

---

### 🔹 10. Restart interfejsu / NetworkManagera
Czasem Horizon nie przydziela poprawnie IP:
```bash
sudo nmcli networking off
sudo nmcli networking on
```
lub
```bash
sudo systemctl restart NetworkManager
```

---

Jeśli chcesz, mogę pomóc przeanalizować wyniki — wystarczy, że wkleisz wyjścia z:
```bash
ip addr show
ip route show
cat /etc/resolv.conf
ping -c 4 192.168.0.1
ping -c 4 8.8.8.8
```

Na tej podstawie można dokładnie wskazać, czy problem leży po stronie routera, DNS, czy konfiguracji twojego urządzenia.