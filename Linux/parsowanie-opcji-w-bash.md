# Parsowanie opcji w bash

**Data:** 2024-01-22

---

**User:**

w skrypcie bash mam argumenty --passpharse, --key-location i kilka innych. jak je sparsować? chcę móc podawać argumenty na wejściu bez znaku =

---

**Assistant:**

Aby sparsować argumenty w skrypcie bash, szczególnie takie jak `--passphrase` i `--key-location`, bez konieczności używania znaku `=`, możesz skorzystać z wbudowanego polecenia `getopts` lub z bardziej elastycznego narzędzia `getopt`. Poniżej przedstawię przykładowy skrypt używający `getopt`, ponieważ obsługuje on długie opcje (takie jak twoje `--passphrase` i `--key-location`) i jest bardziej elastyczny.

Oto przykładowy skrypt, który ilustruje, jak można to zrobić:

```bash
#!/bin/bash

# Zdefiniowanie długich opcji
OPTS=`getopt -o '' -l passphrase:,key-location: -- "$@"`

# Sprawdzenie, czy getopt zakończyło się sukcesem
if [ $? != 0 ] ; then echo "Błędne opcje zostały podane."; exit 1 ; fi

# Ustawienie argumentów po parsowaniu przez getopt
eval set -- "$OPTS"

# Parsowanie argumentów
while true ; do
    case "$1" in
        --passphrase)
            passphrase=$2
            shift 2
            ;;
        --key-location)
            key_location=$2
            shift 2
            ;;
        --)
            shift
            break
            ;;
        *)
            echo "Nieprawidłowa opcja: $1"
            exit 1
            ;;
    esac
done

# Dalsza część skryptu, używająca zmiennych $passphrase i $key_location
echo "Passphrase: $passphrase"
echo "Key location: $key_location"
```

Aby użyć tego skryptu:

1. Zapisz go w pliku, na przykład `script.sh`.
2. Nadaj mu uprawnienia do wykonania: `chmod +x script.sh`.
3. Uruchom skrypt z odpowiednimi argumentami, na przykład:
   ```
   ./script.sh --passphrase "TwojaTajnaFrazą" --key-location "/ścieżka/do/klucza"
   ```

Ten skrypt parsuje argumenty podane na wejściu, przypisując wartości po `--passphrase` i `--key-location` do zmiennych `passphrase` i `key_location` odpowiednio. Możesz dodawać więcej opcji, definiując je w odpowiednich miejscach skryptu.

---

**User:**

podaj rozwiązanie bez getopt/getopts

---

**Assistant:**

Jeśli chcesz sparsować argumenty w skrypcie bash bez użycia `getopt` czy `getopts`, możesz to zrobić ręcznie, iterując przez wszystkie argumenty i sprawdzając każdy z nich. Oto prosty przykład, jak to zrobić:

```bash
#!/bin/bash

# Inicjalizacja zmiennych dla argumentów
passphrase=""
key_location=""

# Iteracja przez wszystkie argumenty
while [[ $# -gt 0 ]]; do
    case $1 in
        --passphrase)
            passphrase=$2
            shift # Przeskocz nazwę argumentu
            shift # Przeskocz wartość argumentu
            ;;
        --key-location)
            key_location=$2
            shift # Przeskocz nazwę argumentu
            shift # Przeskocz wartość argumentu
            ;;
        *)
            # Nieznany argument
            echo "Nieznany argument: $1"
            exit 1
            ;;
    esac
done

# Wykorzystanie sparsowanych argumentów
echo "Passphrase: $passphrase"
echo "Key location: $key_location"
```

W tym skrypcie, używasz pętli `while` do iteracji przez argumenty przekazane do skryptu. Dla każdego argumentu sprawdzasz, czy jest to jeden z interesujących cię argumentów (takich jak `--passphrase` czy `--key-location`), a następnie przypisujesz odpowiednią wartość do zmiennej.

Aby użyć tego skryptu:

1. Zapisz go w pliku, na przykład `script.sh`.
2. Nadaj mu uprawnienia do wykonania: `chmod +x script.sh`.
3. Uruchom skrypt z odpowiednimi argumentami, na przykład:
   ```
   ./script.sh --passphrase "TwojaTajnaFrazą" --key-location "/ścieżka/do/klucza"
   ```

Ten sposób jest bardziej prymitywny i mniej elastyczny niż użycie `getopt` lub `getopts`, ale jest prostszy i działa dobrze, jeśli liczba argumentów i ich format jest ograniczony i dobrze znany.

---

**User:**

chciałbym mieć możliwość podawania parametrów w dowolnej  kolejności. czy ten program spełnia to zadanie

---

**Assistant:**

Tak, przedstawiony skrypt bash spełnia to zadanie. Pozwala na podanie parametrów `--passphrase` i `--key-location` (oraz ewentualnych innych, które możesz dodać) w dowolnej kolejności. Dzieje się tak, ponieważ skrypt iteruje przez wszystkie argumenty przekazane w linii poleceń i rozpoznaje każdy argument niezależnie od jego pozycji.

Każdy przypadek w instrukcji `case` odpowiada jednemu z argumentów, które chcesz obsłużyć. Kiedy skrypt napotyka znany argument (np. `--passphrase`), przypisuje jego wartość do odpowiedniej zmiennej i przeskakuje do następnego argumentu.

Dzięki temu, niezależnie od kolejności, w jakiej argumenty są podane, skrypt poprawnie rozpozna i przypisze wartości do zmiennych `passphrase` i `key_location`. To sprawia, że jest on elastyczny i przyjazny dla użytkownika, który może podać argumenty w dowolnej kolejności, jakiej preferuje.

---

**User:**

co oznacza kod 
if [ -n "$2" ] && [  "${2:0:1}" != "." ]; then

---

**Assistant:**

W skryptach bash, ta konkretna linia kodu wykonuje sprawdzenie dwóch warunków na drugim argumencie przekazanym do skryptu (oznaczonym jako `$2`). Oto szczegółowe wyjaśnienie:

1. `if [ -n "$2" ]`: Ten warunek sprawdza, czy długość drugiego argumentu (`$2`) jest większa od zera. Innymi słowy, sprawdza, czy drugi argument został podany. Opcja `-n` w testowaniu `[ ]` sprawdza, czy długość ciągu jest niezerowa. 

2. `&&`: To jest operator logiczny AND. Drugi warunek jest sprawdzany tylko wtedy, gdy pierwszy warunek jest prawdziwy (tj. gdy istnieje drugi argument).

3. `[ "${2:0:1}" != "." ]`: Ten warunek sprawdza, czy pierwszy znak (znaki od pozycji 0, długość 1) drugiego argumentu jest różny od kropki `.`. Składnia `${2:0:1}` jest formą substringu w bash, która zwraca część ciągu znaków. W tym przypadku zwraca pierwszy znak drugiego argumentu.

Łącząc te dwa warunki, instrukcja `if` sprawdza, czy drugi argument istnieje (nie jest pusty) i czy jego pierwszy znak nie jest kropką. Jest to często stosowane do rozróżnienia opcji (które mogą zaczynać się od `-` lub `--`) od innych argumentów, takich jak ścieżki plików lub inne wartości, które nie zaczynają się od kropki.

---

**User:**

co robi >&2

---

**Assistant:**

W Bash, `>&2` jest używane do przekierowania wyjścia do strumienia błędów standardowych (stderr). Wyjaśnijmy to bardziej szczegółowo:

- `>` to operator przekierowania. Używany jest do przekierowywania wyjścia z jednego miejsca do innego.
- `&` w tym kontekście wskazuje, że odnosimy się do strumienia wyjścia, a nie do pliku.
- `2` jest numerem, który identyfikuje strumień błędów standardowych (stderr). W Bash, 0 jest strumieniem wejścia standardowego (stdin), 1 jest strumieniem wyjścia standardowego (stdout), a 2 jest strumieniem błędów standardowych.

Przykład zastosowania `>&2`:

```bash
echo "To jest błąd" >&2
```

W powyższym przykładzie, komunikat "To jest błąd" zostanie przekierowany do strumienia błędów standardowych. Jest to użyteczne, gdy chcesz wyraźnie oddzielić normalne wyjście programu od komunikatów o błędach. W systemach Unix i Linux, stderr jest często używany do wyświetlania komunikatów diagnostycznych i błędów, a stdout do normalnych danych wyjściowych. Przekierowanie do stderr pomaga w przechwytywaniu i analizie błędów przez inne programy lub skrypty.