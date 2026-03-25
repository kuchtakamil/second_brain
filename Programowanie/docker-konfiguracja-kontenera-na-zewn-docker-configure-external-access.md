# Docker: Konfiguracja kontenera na zewn. (Docker: Configure external access)

**Data:** 2023-05-12

---

**User:**

3 kontenery docker należą do jednego network. W jaki sposób skonfigurować kontener tak aby był dostępny z zewnątz, znaczy z hosta, pod jednym zdefiniowanym adresem IP razem z konkretnym portem.

---

**Assistant:**

Aby skonfigurować kontener Docker tak, aby był dostępny z zewnątrz hosta pod określonym adresem IP i portem, możesz skorzystać z opcji przekazywania portów (`port forwarding`). Oto kroki, które możesz podjąć:

1. Upewnij się, że wszystkie trzy kontenery są w tej samej sieci Docker. Jeśli wcześniej nie została utworzona sieć, można ją utworzyć za pomocą polecenia:
   ```
   docker network create nazwa_sieci
   ```

2. Uruchom kontenery, do których chcesz mieć dostęp z zewnątrz, i przypisz je do utworzonej sieci. Przykładowo:
   ```
   docker run --network=nazwa_sieci --name kontener1 -d obraz1
   docker run --network=nazwa_sieci --name kontener2 -d obraz2
   docker run --network=nazwa_sieci --name kontener3 -d obraz3
   ```

3. Teraz skonfiguruj przekazywanie portów dla kontenera, który chcesz udostępnić na zewnątrz. Możesz to zrobić podczas uruchamiania kontenera za pomocą opcji `-p` lub `-P`. 

   - Opcja `-p` pozwala na przekazywanie konkretnego portu:
     ```
     docker run --network=nazwa_sieci --name kontener1 -p adres_hosta:port_kontenera -d obraz1
     ```

     Na przykład, jeśli chcesz udostępnić kontener1 na adresie IP hosta 192.168.0.100 i porcie 8080, użyj:
     ```
     docker run --network=nazwa_sieci --name kontener1 -p 192.168.0.100:8080:port_kontenera -d obraz1
     ```

   - Opcja `-P` pozwala na losowe przypisanie portu na hoście:
     ```
     docker run --network=nazwa_sieci --name kontener1 -P -d obraz1
     ```

     Aby sprawdzić, który port został przypisany na hoście, można użyć polecenia `docker ps`:
     ```
     docker ps
     ```

4. Po wykonaniu powyższych kroków, kontener1 powinien być dostępny z zewnątrz hosta pod określonym adresem IP i porcie.

Pamiętaj, że jeśli korzystasz z adresu IP publicznego, musisz upewnić się, że twój firewall na hoście hosta pozwala na ruch przychodzący na wybrany port.