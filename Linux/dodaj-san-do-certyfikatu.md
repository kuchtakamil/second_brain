# Dodaj SAN do certyfikatu

**Data:** 2024-01-18

---

**User:**

Generuję certyfikat.
openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 3650 -subj '/CN=Motorola' -nodes
Ale powinienem dodać jeszcze coś, nie jestem pewny co, związane z altName. jak to zrobic

---

**Assistant:**

Jeśli chcesz dodać `Subject Alternative Name` (SAN) do swojego certyfikatu SSL, będziesz potrzebował utworzyć plik konfiguracyjny dla OpenSSL, który zawiera tę informację. SAN pozwala na określenie dodatkowych nazw hostów, które będą zabezpieczone przez certyfikat SSL. Oto jak to zrobić:

1. **Utwórz Plik Konfiguracyjny OpenSSL**: Stwórz plik tekstowy (np. `openssl.cnf`) i dodaj w nim sekcję [v3_req], gdzie zdefiniujesz SAN. Oto przykład:

    ```
    [req]
    distinguished_name = req_distinguished_name
    req_extensions = v3_req
    prompt = no

    [req_distinguished_name]
    CN = Motorola

    [v3_req]
    basicConstraints = CA:FALSE
    keyUsage = nonRepudiation, digitalSignature, keyEncipherment
    subjectAltName = @alt_names

    [alt_names]
    DNS.1 = example.com
    DNS.2 = www.example.com
    ```

    Zmień `DNS.1`, `DNS.2`, itd. na odpowiednie nazwy, które chcesz dodać do certyfikatu.

2. **Generuj Klucz Prywatny i Certyfikat z SAN**: Następnie użyj tego pliku konfiguracyjnego przy generowaniu klucza i certyfikatu:

    ```
    openssl req -new -newkey rsa:2048 -nodes -keyout key.pem -out cert.pem -days 3650 -subj '/CN=Motorola' -config openssl.cnf -extensions 'v3_req'
    ```

3. **Weryfikacja Certyfikatu**: Po utworzeniu certyfikatu, możesz sprawdzić, czy SAN został poprawnie dodany:

    ```
    openssl x509 -in cert.pem -text -noout
    ```

Upewnij się, że edytujesz plik konfiguracyjny zgodnie z własnymi potrzebami, w tym dodając odpowiednie nazwy DNS lub adresy IP pod sekcją [alt_names].

---

**User:**

nie chcę tworzyć pliku konfiguracyjnego, chę wszystko zrobić w linii komend

---

**Assistant:**

Rozumiem, w takim przypadku możesz wygenerować certyfikat z SAN (Subject Alternative Name) bezpośrednio z linii komend, korzystając z opcji `-extensions` i `-config` w OpenSSL. Oto jak to zrobić:

1. **Rozszerz Polecenie OpenSSL**: Musisz modyfikować polecenie OpenSSL, aby zawierało informacje o SAN. Użyjesz tutaj "heredoc" w shellu, aby dostarczyć dodatkową konfigurację bezpośrednio z linii komend. Oto przykład polecenia:

    ```bash
    openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 3650 \
    -subj '/CN=Motorola' -nodes \
    -extensions SAN \
    -config <(cat /etc/ssl/openssl.cnf \
    <(printf '[SAN]\nsubjectAltName=DNS:example.com,DNS:www.example.com'))
    ```

    W tym przykładzie `example.com` i `www.example.com` to nazwy, które chcesz dodać jako SAN. Możesz dostosować je według potrzeb.

2. **Wyjaśnienie Polecenia**:
    - `-extensions SAN`: Określa, że chcesz dodać rozszerzenia SAN.
    - `-config <(...)`: To polecenie tworzy tymczasowy plik konfiguracyjny "w locie". 
    - `cat /etc/ssl/openssl.cnf`: Cat zaczyna od aktualnej konfiguracji OpenSSL.
    - `<(...)`: To jest "heredoc", który dodaje dodatkowe konfiguracje.
    - `[SAN]\nsubjectAltName=DNS:example.com,DNS:www.example.com`: Dodaje sekcję SAN z odpowiednimi nazwami DNS.

3. **Weryfikacja Certyfikatu**: Po utworzeniu certyfikatu, możesz go zweryfikować, aby upewnić się, że SAN został poprawnie dodany:

    ```bash
    openssl x509 -in cert.pem -text -noout
    ```

Upewnij się, że podajesz odpowiednie nazwy w części `subjectAltName`. Możesz także dodać inne typy SAN, takie jak adresy IP, jeśli to konieczne.