# Generowanie Certyfikatu NSS

**Data:** 2024-01-12

---

**User:**

Przy użyciu certmonger czyli polecenia selfsign-getcert chciałbym wygenerować certyfikat który jest self signed. Ten certyfikat chciałbym zapisać w nowej bazie NSS. Baza jeszcze nie istnieje więc jeśli potrzeba, musisz go wygenerować

---

**Assistant:**

Aby wygenerować samopodpisany certyfikat przy użyciu `certmonger` i polecenia `getcert request`, i zapisać go w nowej bazie NSS (Network Security Services), musisz wykonać kilka kroków. Oto ogólny przewodnik:

1. **Instalacja Certmonger (jeśli jeszcze nie jest zainstalowany):**
   Najpierw upewnij się, że `certmonger` jest zainstalowany na Twoim systemie. Możesz to zrobić za pomocą menedżera pakietów twojego systemu, np. `yum` lub `apt`.

   ```bash
   sudo yum install certmonger # Dla systemów opartych na RedHat/CentOS
   sudo apt-get install certmonger # Dla systemów opartych na Debian/Ubuntu
   ```

2. **Utworzenie nowej bazy NSS:**
   Aby utworzyć nową bazę danych NSS, użyj narzędzia `certutil`. Jeśli `certutil` nie jest zainstalowany, możesz go zainstalować jako część pakietu `nss-tools`.

   ```bash
   certutil -N -d sql:/ścieżka/do/twojej/bazy
   ```
   Zastąp `/ścieżka/do/twojej/bazy` ścieżką, gdzie chcesz utworzyć bazę danych.

3. **Generowanie Samopodpisanego Certyfikatu:**
   Użyj `getcert request` z `certmonger` do wygenerowania samopodpisanego certyfikatu. Musisz określić lokalizację bazy danych NSS oraz inne wymagane parametry, takie jak nazwa certyfikatu i ewentualne opcje konfiguracyjne.

   ```bash
   getcert request -d sql:/ścieżka/do/twojej/bazy -n 'nazwaTwojegoCertyfikatu' -I 'nazwaZadaniaCertmonger' --selfsign
   ```
   Tutaj, `-d` określa ścieżkę do bazy danych NSS, `-n` to nazwa certyfikatu, a `-I` to identyfikator zadania w `certmonger`.

4. **Sprawdzenie Statusu Certyfikatu:**
   Po zakończeniu procesu możesz sprawdzić status certyfikatu za pomocą:

   ```bash
   getcert list -I 'nazwaZadaniaCertmonger'
   ```

Pamiętaj, że dokładne polecenia mogą się nieznacznie różnić w zależności od konfiguracji systemu i wymagań. Upewnij się, że masz odpowiednie uprawnienia (np. używając `sudo`) do wykonania tych poleceń.

---

**User:**

Przy certutil -N -d sql:/ścieżka/do/twojej/bazy dostaję 
certutil: function failed: SEC_ERROR_BAD_DATABASE: security library: bad database.

---

**Assistant:**

Błąd `SEC_ERROR_BAD_DATABASE` wskazuje na problem z bazą danych NSS. Może to być spowodowane kilkoma różnymi czynnikami. Oto kilka kroków, które możesz podjąć, aby rozwiązać ten problem:

1. **Sprawdzenie Ścieżki do Bazy:**
   Upewnij się, że ścieżka, którą podajesz do bazy danych NSS, jest poprawna i że masz odpowiednie uprawnienia do dostępu i zapisu w tej lokalizacji. Pamiętaj, że ścieżka powinna wskazywać na katalog, a nie na plik. Na przykład, jeśli chcesz utworzyć bazę danych w katalogu `/home/uzytkownik/nssdb`, polecenie powinno wyglądać tak:

   ```bash
   certutil -N -d sql:/home/uzytkownik/nssdb
   ```

   Upewnij się także, że katalog istnieje przed wykonaniem polecenia.

2. **Sprawdzenie Uprawnień:**
   Upewnij się, że masz odpowiednie uprawnienia do tworzenia i modyfikowania plików w wybranej lokalizacji. Możesz potrzebować uprawnień administratora (root) do tworzenia nowych baz danych NSS w niektórych lokalizacjach.

3. **Usuwanie Istniejących Plików Bazy Danych:**
   Jeśli próbujesz utworzyć bazę danych w lokalizacji, gdzie już wcześniej istniały pliki bazy danych NSS, może to powodować konflikty. Upewnij się, że katalog jest pusty lub użyj innej, nowej lokalizacji.

4. **Weryfikacja Instalacji NSS Tools:**
   Sprawdź, czy narzędzia NSS są poprawnie zainstalowane na Twoim systemie. Możesz to zrobić, ponownie instalując `nss-tools`:

   ```bash
   sudo yum reinstall nss-tools # Dla systemów opartych na RedHat/CentOS
   sudo apt-get install --reinstall nss-tools # Dla systemów opartych na Debian/Ubuntu
   ```

5. **Konsultacja z Dokumentacją i Społecznością:**
   Jeśli powyższe kroki nie rozwiążą problemu, warto sprawdzić dokumentację systemową lub zasięgnąć porady w społecznościach internetowych zajmujących się Twoim systemem operacyjnym lub zarządzaniem certyfikatami.

Jeśli problem nadal występuje, podaj więcej szczegółów dotyczących Twojego systemu i środowiska, abyśmy mogli lepiej zdiagnozować problem.