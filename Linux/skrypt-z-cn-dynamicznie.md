# Skrypt z CN dynamicznie

**Data:** 2024-01-18

---

**User:**

Przerób ten skrypt
#!/bin/bash

set -u
echo changeit > passfile.txt
openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 3650 -subj '/CN=Motorola' -addext "subjectAltName = DNS:foo.co.uk" -nodes
openssl pkcs12 -export -out DConnectKeyStore.pkcs12 -inkey key.pem -in cert.pem -name "websocket_cert" -passout file:./passfile.txt
rm -rf cert.pem key.pem

Wartość CN ma być ustawiana z parametru skryptu. Jeśli parametr nie jest podany, wartość CN ustawiana jest przy pomocy wywołania polecenia linuxoweggo hostname.

---

**Assistant:**

Aby zmodyfikować podany skrypt tak, aby wartość CN (Common Name) była ustawiana z parametru skryptu, a w przypadku braku parametru używała wartości zwróconej przez polecenie `hostname`, możemy użyć prostego sprawdzenia warunkowego w skrypcie Bash. Poniżej znajduje się zmodyfikowana wersja Twojego skryptu:

```bash
#!/bin/bash

set -u

# Przypisz wartość CN do zmiennej, użyj pierwszego argumentu skryptu, jeśli dostępny
CN="${1:-$(hostname)}"

echo "Użyto CN: $CN"

echo changeit > passfile.txt
openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 3650 -subj "/CN=$CN" -addext "subjectAltName = DNS:foo.co.uk" -nodes
openssl pkcs12 -export -out DConnectKeyStore.pkcs12 -inkey key.pem -in cert.pem -name "websocket_cert" -passout file:./passfile.txt
rm -rf cert.pem key.pem
```

Co zostało zmienione:

1. Dodano linię `CN="${1:-$(hostname)}"`, która przypisuje zmiennej `CN` wartość pierwszego argumentu przekazanego do skryptu (`$1`). Jeśli argument nie został podany, zostanie użyta wartość zwrócona przez polecenie `hostname`.
2. W linii z poleceniem `openssl req`, wartość `/CN=$CN` wstawia wartość zmiennej `CN` do pola CN w certyfikacie.
3. Dodano linię `echo "Użyto CN: $CN"`, która wyświetla użyty CN, abyś mógł zweryfikować, czy skrypt działa poprawnie.

Teraz, aby użyć tego skryptu, możesz wywołać go w następujący sposób:

- Z parametrem CN: `./nazwa_skryptu.sh MojaNazwa`
- Bez parametru (użyje wyniku polecenia `hostname`): `./nazwa_skryptu.sh`

---

**User:**

chciałbym dołożyć jeszcze paramet podstawiany pod subjectAltName

---

**Assistant:**

Aby dodać dodatkowy parametr do skryptu, który pozwoli na dynamiczne ustawienie wartości `subjectAltName`, możesz zmodyfikować skrypt w następujący sposób. Drugi argument przekazany do skryptu będzie używany do ustawienia wartości `subjectAltName`. Jeśli drugi argument nie zostanie podany, możemy ustawić domyślną wartość.

Oto zmodyfikowany skrypt:

```bash
#!/bin/bash

set -u

# Przypisz wartość CN do zmiennej, użyj pierwszego argumentu skryptu, jeśli dostępny
CN="${1:-$(hostname)}"
# Przypisz wartość subjectAltName do zmiennej, użyj drugiego argumentu skryptu, jeśli dostępny, lub domyślną wartość
SAN="${2:-DNS:foo.co.uk}"

echo "Użyto CN: $CN"
echo "Użyto SAN: $SAN"

echo changeit > passfile.txt
openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 3650 -subj "/CN=$CN" -addext "subjectAltName = $SAN" -nodes
openssl pkcs12 -export -out DConnectKeyStore.pkcs12 -inkey key.pem -in cert.pem -name "websocket_cert" -passout file:./passfile.txt
rm -rf cert.pem key.pem
```

Jak korzystać z tego skryptu:

1. Jeśli chcesz podać zarówno CN, jak i SAN: `./nazwa_skryptu.sh MojaNazwa DNS:moj.domena.com`
2. Jeśli chcesz podać tylko CN (SAN będzie miał wartość domyślną `DNS:foo.co.uk`): `./nazwa_skryptu.sh MojaNazwa`
3. Jeśli nie podasz żadnego argumentu, CN zostanie ustawiony za pomocą `hostname`, a SAN będzie miał wartość domyślną `DNS:foo.co.uk`.

Wartość `subjectAltName` jest teraz elastycznie ustawiana za pomocą drugiego argumentu skryptu.

---

**User:**

nie chcę wstawiać domyślnej wartości, chę aby zawsze była ona podowana z cmd

---

**Assistant:**

Rozumiem, w takim przypadku zaktualizuję skrypt, aby wymagał podania wartości `subjectAltName` jako drugiego argumentu z linii poleceń. Jeśli argument ten nie zostanie podany, skrypt zakończy działanie z odpowiednim komunikatem. Oto zmieniony skrypt:

```bash
#!/bin/bash

set -u

# Sprawdź, czy zostały podane oba wymagane argumenty
if [ "$#" -ne 2 ]; then
    echo "Użycie: $0 <CN> <subjectAltName>"
    exit 1
fi

# Przypisz wartość CN i SAN do zmiennych
CN="$1"
SAN="$2"

echo "Użyto CN: $CN"
echo "Użyto SAN: $SAN"

echo changeit > passfile.txt
openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 3650 -subj "/CN=$CN" -addext "subjectAltName = $SAN" -nodes
openssl pkcs12 -export -out DConnectKeyStore.pkcs12 -inkey key.pem -in cert.pem -name "websocket_cert" -passout file:./passfile.txt
rm -rf cert.pem key.pem
```

Jak korzystać z tego skryptu:

1. Musisz podać oba argumenty: CN oraz SAN, na przykład: `./nazwa_skryptu.sh MojaNazwa DNS:moj.domena.com`
2. Jeśli nie podasz obu argumentów, skrypt wyświetli instrukcję użycia i zakończy działanie.

Teraz skrypt wymaga podania zarówno CN, jak i SAN z linii poleceń, co zapewnia pełną kontrolę nad tymi parametrami podczas generowania certyfikatu.

---

**User:**

Napisz help dla tego skryptu. Help ma przyjąć postać szeregu komend echo.
Wprowadz nazwane argumenty czyli passphrase, subAltName, keystoreName, commonName

---

**Assistant:**

Aby dodać sekcję pomocy (help) do skryptu, która wyjaśnia sposób użycia i opisuje argumenty, możemy użyć serii komend `echo`. Dodatkowo, zmodyfikuję skrypt, aby przyjmował nazwane argumenty: `passphrase`, `subAltName`, `keystoreName`, `commonName`. Użyjemy konwencji `--nazwa_argumentu=wartość` dla każdego z nich.

Oto przykład, jak może wyglądać taki skrypt z sekcją pomocy:

```bash
#!/bin/bash

# Funkcja wyświetlająca pomoc
show_help() {
    echo "Użycie: $0 --commonName=CN --subAltName=SAN --keystoreName=KEYSTORE --passphrase=PASS"
    echo
    echo "Gdzie:"
    echo "  --commonName=CN       Ustawia Common Name dla certyfikatu"
    echo "  --subAltName=SAN      Ustawia Subject Alternative Name dla certyfikatu"
    echo "  --keystoreName=KEYSTORE  Nazwa pliku keystore PKCS12"
    echo "  --passphrase=PASS     Hasło dla pliku keystore"
    echo
    echo "Przykład:"
    echo "  $0 --commonName=\"example.com\" --subAltName=\"DNS:example.com\" --keystoreName=\"DConnectKeyStore.pkcs12\" --passphrase=\"mojeHaslo\""
}

# Sprawdź, czy skrypt został wywołany z argumentami
if [ "$#" -eq 0 ]; then
    show_help
    exit 1
fi

# Przetwarzanie argumentów
for i in "$@"
do
case $i in
    --commonName=*)
    CN="${i#*=}"
    shift
    ;;
    --subAltName=*)
    SAN="${i#*=}"
    shift
    ;;
    --keystoreName=*)
    KEYSTORE="${i#*=}"
    shift
    ;;
    --passphrase=*)
    PASSPHRASE="${i#*=}"
    shift
    ;;
    *)
    # Nieznany argument
    show_help
    exit 1
    ;;
esac
done

# Sprawdzenie, czy wszystkie wymagane argumenty zostały podane
if [ -z "${CN}" ] || [ -z "${SAN}" ] || [ -z "${KEYSTORE}" ] || [ -z "${PASSPHRASE}" ]; then
    echo "Błąd: Nie wszystkie wymagane argumenty zostały podane."
    show_help
    exit 1
fi

echo "Użyto CN: $CN"
echo "Użyto SAN: $SAN"
echo "Nazwa pliku keystore: $KEYSTORE"
echo "Hasło do keystore: $PASSPHRASE"

echo "$PASSPHRASE" > passfile.txt
openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 3650 -subj "/CN=$CN" -addext "subjectAltName = $SAN" -nodes
openssl pkcs12 -export -out "$KEYSTORE" -inkey key.pem -in cert.pem -name "websocket_cert" -passout file:./passfile.txt
rm -rf cert.pem key.pem passfile.txt
```

Zmiany w skrypcie obejmują:

1. Funkcję `show_help`, która wyświetla instrukcje i informacje o argumentach.
2. Przetwarzanie nazwanych argumentów za pomocą pętli `for` i instrukcji `case`.
3. Sprawdzenie, czy wszystkie wymagane argumenty zostały podane.
4. Użycie wartości argumentów w odpowiednich miejscach skryptu.

Teraz, aby skorzystać ze skryptu, użytkownik musi podać wszystkie wymagane argumenty w postaci nazwanej. Jeśli skrypt zostanie uruchomiony bez argumentów lub z nieprawidłowymi argumentami, zostanie wyświetlona pomoc.

---

**User:**

jak dodać tam jeszcze wartości domyślne dla wybranych parametrół np subAltName

---

**Assistant:**

Aby dodać wartości domyślne dla wybranych parametrów, takich jak `subAltName`, w skrypcie, można ustawić te wartości domyślne w skrypcie przed przetwarzaniem argumentów przekazanych do skryptu. Jeśli użytkownik poda wartość dla danego argumentu, zostanie ona użyta; w przeciwnym razie skrypt wykorzysta wartość domyślną.

Oto zmodyfikowany skrypt z wartością domyślną dla `subAltName`:

```bash
#!/bin/bash

# Wartości domyślne
SAN="DNS:default.example.com" # Domyślna wartość dla subAltName
KEYSTORE="DConnectKeyStore.pkcs12" # Domyślna nazwa pliku keystore

# Funkcja wyświetlająca pomoc
show_help() {
    echo "Użycie: $0 --commonName=CN [--subAltName=SAN] [--keystoreName=KEYSTORE] --passphrase=PASS"
    echo
    echo "Gdzie:"
    echo "  --commonName=CN          Ustawia Common Name dla certyfikatu"
    echo "  --subAltName=SAN         Ustawia Subject Alternative Name dla certyfikatu (domyślnie $SAN)"
    echo "  --keystoreName=KEYSTORE  Nazwa pliku keystore PKCS12 (domyślnie $KEYSTORE)"
    echo "  --passphrase=PASS        Hasło dla pliku keystore"
    echo
    echo "Przykład:"
    echo "  $0 --commonName=\"example.com\" --subAltName=\"DNS:example.com\" --keystoreName=\"MyKeyStore.pkcs12\" --passphrase=\"mojeHaslo\""
}

# Sprawdź, czy skrypt został wywołany z argumentami
if [ "$#" -eq 0 ]; then
    show_help
    exit 1
fi

# Przetwarzanie argumentów
for i in "$@"
do
case $i in
    --commonName=*)
    CN="${i#*=}"
    shift
    ;;
    --subAltName=*)
    SAN="${i#*=}"
    shift
    ;;
    --keystoreName=*)
    KEYSTORE="${i#*=}"
    shift
    ;;
    --passphrase=*)
    PASSPHRASE="${i#*=}"
    shift
    ;;
    *)
    # Nieznany argument
    show_help
    exit 1
    ;;
esac
done

# Sprawdzenie, czy wszystkie wymagane argumenty zostały podane
if [ -z "${CN}" ] || [ -z "${PASSPHRASE}" ]; then
    echo "Błąd: Nie wszystkie wymagane argumenty zostały podane."
    show_help
    exit 1
fi

echo "Użyto CN: $CN"
echo "Użyto SAN: $SAN"
echo "Nazwa pliku keystore: $KEYSTORE"
echo "Hasło do keystore: $PASSPHRASE"

echo "$PASSPHRASE" > passfile.txt
openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 3650 -subj "/CN=$CN" -addext "subjectAltName = $SAN" -nodes
openssl pkcs12 -export -out "$KEYSTORE" -inkey key.pem -in cert.pem -name "websocket_cert" -passout file:./passfile.txt
rm -rf cert.pem key.pem passfile.txt
```

Zmiany w skrypcie obejmują:

1. Ustawienie wartości domyślnych dla `SAN` i `KEYSTORE` na początku skryptu.
2. Modyfikacja funkcji `show_help`, aby informować o wartościach domyślnych.
3. Użycie tych wartości domyślnych, jeśli użytkownik nie poda własnych wartości dla tych parametrów.

Teraz skrypt użyje wartości domyślnych dla `subAltName` i `keystoreName`, chyba że użytkownik zdecyduje się je zastąpić własnymi wartościami.