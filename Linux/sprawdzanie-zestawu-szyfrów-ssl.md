# Sprawdzanie zestawu szyfrów SSL

**Data:** 2024-01-22

---

**User:**

Mam certyfikat w postaci pliku pem na dysku. W jaki sposób z command line mogę sprawdzić jakie cipher suite ten certyfikat używa

---

**Assistant:**

Aby sprawdzić, jakie zestawy szyfrów (cipher suites) są obsługiwane przez certyfikat SSL, znajdujący się w pliku `.pem`, możesz użyć narzędzia `openssl`. Jest to potężne narzędzie do pracy z certyfikatami SSL i kluczami, dostępne na większości systemów Unixowych, w tym Linux i MacOS.

Oto kroki, które możesz wykonać:

1. **Sprawdzenie certyfikatu**: Najpierw upewnij się, że masz certyfikat i że jest on w formacie PEM. Możesz to zrobić za pomocą polecenia:

   ```bash
   openssl x509 -in sciezka/do/twojego/certyfikatu.pem -text -noout
   ```

   To polecenie wyświetli szczegółowe informacje o certyfikacie, w tym jego algorytm podpisu, ważność i inne atrybuty, ale nie pokaże bezpośrednio obsługiwanych zestawów szyfrów.

2. **Testowanie zestawów szyfrów**: Aby sprawdzić, jakie zestawy szyfrów są obsługiwane przez serwer używający tego certyfikatu, musisz przetestować połączenie SSL z tym serwerem. Możesz to zrobić za pomocą polecenia `openssl s_client`. Na przykład:

   ```bash
   openssl s_client -connect adres_serwera:port -cert sciezka/do/twojego/certyfikatu.pem
   ```

   W tym miejscu `adres_serwera:port` powinien być adres serwera, z którym certyfikat jest używany, na przykład `www.twojastrona.com:443`.

3. **Analiza wyników**: Odpowiedź z tego polecenia zawiera informacje o zestawie szyfrów używanym podczas nawiązywania połączenia. Szukaj linii zaczynających się od "Cipher Suite" w sekcji "SSL-Session".

Pamiętaj, że zestaw szyfrów używany w połączeniu SSL zależy nie tylko od certyfikatu, ale także od konfiguracji serwera i klienta. Certyfikat sam w sobie nie "używa" zestawu szyfrów; zamiast tego określa on metody szyfrowania, które są akceptowalne podczas nawiązywania bezpiecznego połączenia.