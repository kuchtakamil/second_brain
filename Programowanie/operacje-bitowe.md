# Operacje bitowe – co tak naprawdę liczysz, przesuwając bity

Operacje bitowe mają w sobie coś z magii dla wtajemniczonych. Większość programistów pamięta ze studiów, że `&` to koniunkcja, a `<<` przesuwa bity w lewo – i na tym kończy się ich znajomość tematu. Tymczasem te operatory nie są ciekawostką dla ludzi piszących na mikrokontrolery. To arytmetyka modulo 2, algebra zbiorów i sposób na upakowanie danych, który siedzi wewnątrz `HashMapy`, maski podsieci, formatu Protocol Buffers i silnika szachowego.

W tym artykule pokażę, **co operacje bitowe znaczą matematycznie** i **gdzie realnie ich używasz, nawet o tym nie wiedząc**. Same definicje operatorów potraktuję skrótowo – bo są w miarę oczywiste i zajmują jedną tabelkę. Cała reszta odpowiada na pytanie: co z tego wynika.

## 1. Wstęp – dlaczego to nie jest tylko ciekawostka

Zacznijmy od trzech linijek kodu wyjętych z bibliotek, których używasz na co dzień:

```java
// java.util.HashMap – wybór kubełka dla klucza
int index = hash & (table.length - 1);

// Protocol Buffers – kodowanie liczby ze znakiem (zigzag)
int encoded = (n << 1) ^ (n >> 31);

// Linux, wywołanie open() – sprawdzenie flagi
if (flags & O_CREAT) { ... }
```

Każda z nich wygląda jak szyfr, a każda robi coś banalnego: pierwsza liczy resztę z dzielenia, druga zamienia małe liczby ujemne na małe dodatnie, trzecia sprawdza, czy element należy do zbioru.

Wspólny mianownik jest taki, że **procesor nie zna „liczb" ani „zbiorów"**. Zna rejestr o szerokości 64 bitów i garść bramek logicznych, które potrafią te bity porównywać i przesuwać. Wszystko, co uważamy za arytmetykę, jest na tym poziomie zbudowane z operacji bitowych. Kiedy piszesz `x & 7`, nie robisz nic egzotycznego – schodzisz po prostu piętro niżej, na poziom, na którym maszyna faktycznie pracuje.

Po lekturze tych czterech rozdziałów wszystkie trzy linijki powyżej będą dla Ciebie oczywiste. Będziesz też wiedzieć, kiedy taki zapis jest sprytny, a kiedy to zwykłe chwalipięstwo, które szkodzi czytelności.

## 2. Fundament, czyli jedyna teoria, jaka jest potrzebna

Liczba całkowita w pamięci to ciąg bitów o ustalonej długości (w Javie: 32 bity dla `int`, 64 dla `long`). Każdy bit ma swoją **wagę** – kolejną potęgę dwójki, liczoną od prawej strony:

```text
  waga bitu:    128   64   32   16    8    4    2    1
  potęga:       2^7  2^6  2^5  2^4  2^3  2^2  2^1  2^0
  liczba 172:     1    0    1    0    1    1    0    0   →  128 + 32 + 8 + 4 = 172
```

To wszystko. Reszta artykułu jest konsekwencją tego jednego rysunku.

### Dwa sposoby patrzenia na tę samą liczbę

Ta sama sekwencja bitów ma dwie zupełnie różne interpretacje – i to jest oś całego tekstu:

1. **Liczba.** Wtedy operacje bitowe są arytmetyką: przesunięcie mnoży przez potęgę dwójki, maska liczy resztę z dzielenia, XOR dodaje modulo 2. Tym zajmiemy się w rozdziale 3.
2. **Zbiór (wektor flag).** Bit numer `i` odpowiada na pytanie „czy element `i` należy do zbioru?". Wtedy operacje bitowe są teorią mnogości: `&` to przecięcie, `|` to suma, `^` to różnica symetryczna. O tym jest rozdział 4.

Sprawny programista przełącza się między tymi dwoma widokami tak samo naturalnie, jak między patrzeniem na tablicę jak na listę i jak na mapę indeks → wartość.

### Liczby ujemne, czyli kod U2

Jeden akapit teorii, bez którego kilka późniejszych sztuczek wygląda jak przypadek. W kodzie uzupełnień do dwóch (U2) najstarszy bit ma wagę **ujemną**: dla `int` jest to `-2^31`. Dzięki temu dodawanie działa identycznie dla liczb dodatnich i ujemnych – procesor nie musi wiedzieć, czy operuje na liczbie ze znakiem. Praktyczna konsekwencja, którą warto zapamiętać:

```text
-x  ==  ~x + 1        czyli: odwróć wszystkie bity i dodaj jeden
~x  ==  -x - 1        to samo równanie przestawione
```

Stąd biorą się „dziwne" wyniki w konsoli: `~5` to nie `-5`, tylko `-6`.

### Ściąga z operatorów

| Operator | Na bicie | Na liczbie | Na zbiorze |
|---|---|---|---|
| `a & b` | 1, gdy oba bity są 1 | maskowanie, reszta z dzielenia przez `2^k` | przecięcie |
| `a \| b` | 1, gdy którykolwiek jest 1 | ustawianie bitów | suma |
| `a ^ b` | 1, gdy bity są różne | **dodawanie modulo 2 bez przeniesienia** | różnica symetryczna |
| `~a` | odwrócenie każdego bitu | `-a - 1` | dopełnienie |
| `a << k` | przesunięcie w lewo, z prawej zera | `a * 2^k` | przenumerowanie elementów w górę |
| `a >> k` | przesunięcie w prawo, z lewej powielony bit znaku | `floor(a / 2^k)` | – |
| `a >>> k` | przesunięcie w prawo, z lewej zera (Java) | dzielenie bez znaku | – |

Z całej tabeli jedno zdanie jest naprawdę warte zapamiętania: **XOR to dodawanie modulo 2 bez przeniesienia**. `0+0=0`, `0+1=1`, `1+1=2`, a `2 mod 2 = 0`. To dlatego XOR wypłynie później przy CRC, kryptografii, RAID 5 i kodach korekcyjnych – wszędzie tam, gdzie liczy się arytmetyka nad ciałem dwuelementowym.

## 3. Interpretacja matematyczna – co te operacje naprawdę liczą

### 3.1 Przesunięcia to mnożenie i dzielenie

Przesunięcie w lewo o `k` pozycji dopisuje `k` zer na końcu, czyli zwiększa wagę każdego bitu `2^k` razy:

```text
x << k  ==  x * 2^k
x >> k  ==  floor(x / 2^k)
```

Zwróć uwagę na `floor` w drugim wzorze. To nie jest to samo, co dzielenie w Javie czy w C, które **obcina w stronę zera**. Dla liczb dodatnich różnicy nie ma, dla ujemnych – jest, i jest to klasyczne źródło błędów:

```java
-7 >> 1   // == -4   (podłoga z -3.5)
-7 /  2   // == -3   (obcięcie w stronę zera)
```

Zapamiętaj to jako regułę: **przesunięcie w prawo zaokrągla w dół, a nie do zera**.

#### Dlaczego akurat podłoga?

To nie jest arbitralna decyzja projektantów procesora, tylko nieunikniona konsekwencja zapisu pozycyjnego. Każdą liczbę całkowitą da się jednoznacznie rozłożyć na iloraz i resztę:

```text
x  =  q * 2^k  +  r,      gdzie  0 <= r < 2^k
```

`q` to wszystkie bity od pozycji `k` w górę, a `r` to `k` najmłodszych bitów. Kluczowa jest jedna obserwacja: **`r` jest zawsze nieujemne**. Młodsze bity mają dodatnie wagi (`1, 2, 4, 8, …`) niezależnie od tego, czy cała liczba jest dodatnia, czy ujemna – w kodzie U2 znak siedzi wyłącznie w najstarszym bicie. Przesunięcie w prawo po prostu wyrzuca `r` i zostawia `q`. Skoro odrzucamy wielkość nieujemną, wynik nigdy nie może urosnąć – zawsze schodzimy w dół osi liczbowej, także po jej ujemnej stronie.

Zobaczmy to na `-7` zapisanym w ośmiu bitach:

```text
-7       = 1111 1001   = -128 + 64 + 32 + 16 + 8 + 1  = -7
                    ^
                    odrzucany bit:  r = 1   (nieujemny!)

-7 >> 1  = 1111 1100   = -128 + 64 + 32 + 16 + 8 + 4  = -4
```

Rozkład się zgadza: `-7 == (-4) * 2 + 1`. Żeby przesunięcie dało `-3`, reszta musiałaby wynosić `-1` – a bity o ujemnej wadze poza pozycją znaku po prostu nie istnieją. Powielanie bitu znaku przy `>>` (tzw. przesunięcie arytmetyczne) nie jest więc protezą doklejoną do liczb ujemnych; to dokładnie to, czego wymaga powyższy rozkład.

#### Podłoga zwykle jest tym, czego chcesz

Obcinanie w stronę zera ma brzydką właściwość: przedział wokół zera jest **dwa razy szerszy** od pozostałych. Widać to jak na dłoni przy mapowaniu współrzędnej na siatkę kafelków 16 × 16:

```java
x / 16    // -15..15 → 0        kafelek przy zerze jest dwa razy szerszy
x >> 4    // -16..-1 → -1,  0..15 → 0     wszystkie kafelki równe
```

Wszędzie tam, gdzie oś ze znakiem dzielisz na równe kubełki – kafelki mapy, chunki, strony pamięci, przedziały histogramu, numery tygodni liczone od jakiejś daty – **podłoga jest poprawną semantyką, a `/` jest błędem**. Java ma na to `Math.floorDiv`, a dla potęg dwójki `x >> k` to dokładnie `Math.floorDiv(x, 1 << k)`. W Pythonie problem nie występuje, bo `//` z definicji zaokrągla w dół.

#### Dlaczego kompilator nie zamienia `/ 2` na `>> 1`

Bo nie może – te dwie operacje różnią się wynikiem dla liczb ujemnych. Żeby z podłogi zrobić obcięcie do zera, trzeba przed przesunięciem dodać poprawkę, i dokładnie taki kod generują kompilatory:

```java
x / 2          ≡   (x + (x >>> 31)) >> 1
x / (1 << k)   ≡   (x + ((x >> 31) & ((1 << k) - 1))) >> k
```

`x >> 31` daje same jedynki dla liczb ujemnych i same zera dla nieujemnych, więc działa jak przełącznik „dodaj poprawkę tylko wtedy, gdy liczba jest ujemna". Sama poprawka `2^k - 1` przepycha wynik o jeden w górę, zamieniając podłogę na obcięcie. To jedna z niewielu sytuacji, w których **ręczne `>> k` jest realnie tańsze niż `/ 2^k`** – pod warunkiem, że semantyka podłogi jest tym, czego chcesz, a nie przypadkiem, którego nie zauważyłeś.

Na koniec ostrzeżenie, żeby nie nadpisać jednej pomyłki drugą: `>>>` **nie jest** dzieleniem liczby ze znakiem. Traktuje wzorzec bitowy jako liczbę bez znaku, więc `-8 >>> 1` to nie `-4`, tylko `2147483644`. Przydaje się do wyciągania bitu znaku (`x >>> 31`) i do arytmetyki bez znaku, ale nie do dzielenia przez dwa.

### 3.2 Maska to reszta z dzielenia

Najczęściej używana operacja bitowa świata:

```text
x & (2^k - 1)  ==  x mod 2^k
```

Dlaczego? `2^k - 1` to liczba złożona z samych jedynek na `k` najmłodszych pozycjach (`8 - 1 = 0111`). Iloczyn bitowy z taką maską wycina dokładnie te `k` bitów i kasuje całą resztę. A skoro każdy skasowany bit miał wagę będącą wielokrotnością `2^k`, to jego usunięcie nie zmienia reszty z dzielenia przez `2^k`.

```java
173 & 7    // == 5,  bo 173 = 21*8 + 5
```

To działa **wyłącznie dla potęg dwójki** – i właśnie dlatego biblioteki wymuszają, żeby pojemność tablicy haszującej była potęgą dwójki. Jedna instrukcja `AND` zamiast dzielenia, które na procesorze jest kilkadziesiąt razy wolniejsze.

Ciekawostka, która ładnie domyka poprzedni punkt: maska liczy resztę **matematyczną**, zawsze nieujemną, podczas gdy operator `%` w Javie potrafi zwrócić wynik ujemny.

```java
-7 & 3    // ==  1   (bo -7 = -2*4 + 1)
-7 % 4    // == -3
```

Zarówno `>>`, jak i `&` konsekwentnie realizują dzielenie z podłogą – to ta sama arytmetyka, widziana z dwóch stron.

### 3.3 Dodawanie rozłożone na czynniki pierwsze

Skoro XOR to dodawanie bez przeniesień, to gdzie podziały się przeniesienia? W operatorze `&` – bo przeniesienie powstaje dokładnie tam, gdzie oba bity są jedynkami, i wędruje o jedną pozycję w lewo:

```text
x + y  ==  (x ^ y) + ((x & y) << 1)
           ^^^^^^^     ^^^^^^^^^^^^
           suma bez     przeniesienia
           przeniesień
```

To jest dosłownie schemat sumatora, z którego zbudowana jest jednostka arytmetyczna procesora. Powtarzając ten krok w pętli, aż przeniesienia się wyzerują, dodasz dwie liczby bez użycia `+`. Z tej samej obserwacji wynika kilka tożsamości, które czasem oszczędzają obliczeń:

```text
x + y  ==  (x | y) + (x & y)
x ^ y  ==  x + y - 2*(x & y)
```

Intuicja za pierwszą z nich: `|` liczy każdy wspólny bit raz, a `&` dokłada brakującą drugą kopię.

### 3.4 Trzy wyrażenia, które warto znać na pamięć

**`x & (x - 1)` – zeruje najniższy ustawiony bit.**

Odjęcie jedynki zamienia najniższą jedynkę w zero, a wszystkie zera pod nią w jedynki. Iloczyn z oryginałem zostawia więc wszystko powyżej nietknięte, a najniższą jedynkę kasuje:

```text
x       = 1011 0000
x - 1   = 1010 1111
x & (x-1) = 1010 0000
```

Dwa zastosowania. Po pierwsze, test potęgi dwójki – liczba jest potęgą dwójki wtedy i tylko wtedy, gdy ma dokładnie jeden ustawiony bit, więc po jego skasowaniu zostaje zero:

```java
boolean isPowerOfTwo(int x) {
    return x > 0 && (x & (x - 1)) == 0;
}
```

Po drugie, zliczanie bitów metodą Kernighana – pętla wykonuje się tyle razy, ile jest jedynek, a nie 32 razy:

```java
int count = 0;
while (x != 0) { x &= x - 1; count++; }
```

**`x & -x` – zostawia tylko najniższy ustawiony bit.**

Tutaj przydaje się wiedza o U2. Skoro `-x == ~x + 1`, to negacja odwraca wszystkie bity, a dodanie jedynki „cofa" odwrócenie na najniższej jedynce i wszystkim poniżej. W efekcie `x` i `-x` zgadzają się dokładnie na jednej pozycji:

```text
x       = 0000 1100   ( 12)
-x      = 1111 0100   (-12)
x & -x  = 0000 0100   (  4)
```

To wyrażenie (zwane *lowbit*) jest fundamentem drzewa Fenwicka i najwygodniejszym sposobem iterowania po ustawionych bitach maski.

**`(x + m - 1) & ~(m - 1)` – zaokrąglenie w górę do wielokrotności `m = 2^k`.**

Dodanie `m - 1` przepycha liczbę powyżej najbliższej wielokrotności, a maska `~(m - 1)` kasuje młodsze bity, czyli zaokrągla w dół. Złożenie obu daje zaokrąglenie w górę:

```java
int alignedSize = (size + 7) & ~7;   // do pełnych 8 bajtów
```

Spotkasz to wszędzie tam, gdzie coś musi być wyrównane: alokatory pamięci, rozmiary bloków na dysku, paginacja, nagłówki formatów binarnych.

### 3.5 Bity jako źródło informacji o liczbie

Trzy funkcje, które w nowoczesnych procesorach są **pojedynczymi instrukcjami**, a nie pętlami:

| Operacja | Java | Co daje |
|---|---|---|
| liczba jedynek (*popcount*) | `Integer.bitCount(x)` | np. rozmiar zbioru zapisanego jako maska |
| liczba zer na końcu (*ctz*) | `Integer.numberOfTrailingZeros(x)` | indeks najniższego ustawionego bitu |
| liczba zer na początku (*clz*) | `Integer.numberOfLeadingZeros(x)` | rząd wielkości liczby |

Z ostatniej z nich wyliczysz logarytm dwójkowy bez arytmetyki zmiennoprzecinkowej:

```java
int log2 = 31 - Integer.numberOfLeadingZeros(x);   // dla x > 0
```

Nie pisz tych funkcji ręcznie. `Integer.bitCount` kompiluje się do jednej instrukcji `POPCNT`, a Twoja pętla – nie.

## 4. Liczba jako zbiór – maski bitowe

Skoro bit przechowuje odpowiedź „tak/nie", to 64-bitowy `long` przechowuje 64 takie odpowiedzi. A zbiór to nic innego niż odpowiedź „czy element należy?" dla każdego kandydata. Stąd wniosek: **`long` to zbiór do 64 elementów mieszczący się w jednym rejestrze procesora**.

### 4.1 Słownik: teoria mnogości → operatory

| Operacja na zbiorze | Zapis bitowy |
|---|---|
| suma `A ∪ B` | `a \| b` |
| przecięcie `A ∩ B` | `a & b` |
| różnica `A \ B` | `a & ~b` |
| różnica symetryczna | `a ^ b` |
| dodanie elementu `i` | `a \| (1 << i)` |
| usunięcie elementu `i` | `a & ~(1 << i)` |
| przełączenie elementu `i` | `a ^ (1 << i)` |
| test przynależności | `(a >> i & 1) == 1` |
| test podzbioru `B ⊆ A` | `(a & b) == b` |
| liczność zbioru | `Integer.bitCount(a)` |
| zbiór pusty | `a == 0` |

Warto zwrócić uwagę na dwa wiersze. `a & ~b` – różnica zbiorów – to najczęściej zapominana konstrukcja, choć przydaje się nie rzadziej niż suma. A `(a & b) == b` jako test podzbioru jest wręcz elegancki: „przecięcie nie zabrało nic z `b`, więc całe `b` siedziało w `a`".

### 4.2 To już znasz – flagi w API

Maski bitowe widziałeś setki razy, tylko bez tej etykiety:

```java
// Java
Pattern.compile(regex, Pattern.CASE_INSENSITIVE | Pattern.MULTILINE);

// C / Linux
int fd = open(path, O_WRONLY | O_CREAT | O_APPEND);
mmap(addr, len, PROT_READ | PROT_WRITE, ...);
```

Uprawnienia uniksowe to ten sam mechanizm zapisany ósemkowo: `chmod 644` to trzy trójki bitów – `110 100 100`, czyli `rw- r-- r--`. Cyfra ósemkowa to dokładnie trzy bity, dlatego `chmod` używa systemu ósemkowego, a nie dziesiętnego.

Ten pionowy `|` to nie jest „lub" w sensie wyboru jednej opcji – to **suma zbiorów flag**. Dlatego przekazanie kilku flag naraz działa i dlatego kolejność nie ma znaczenia.

### 4.3 Jak zdefiniować własne flagi

Reguła jest jedna: nigdy nie wpisuj wartości ręcznie, tylko zapisuj je jako przesunięcia. Wtedy widać na pierwszy rzut oka, że każda flaga zajmuje osobny bit i że nic się nie dubluje:

```java
static final int READ    = 1 << 0;   // 1
static final int WRITE   = 1 << 1;   // 2
static final int EXECUTE = 1 << 2;   // 4
static final int DELETE  = 1 << 3;   // 8

int perms = READ | WRITE;

perms |= EXECUTE;                    // dodaj
perms &= ~WRITE;                     // usuń
boolean canRead = (perms & READ) != 0;
```

Uwaga na typ: przy więcej niż 31 flagach musisz pisać `1L << i`, bo `1 << 32` w Javie **nie daje zera**, tylko `1` (licznik przesunięcia brany jest modulo 32). To jedna z najbardziej podstępnych pułapek w całym temacie – wrócę do niej w rozdziale o błędach.

W Javie masz też `EnumSet`, który jest czytelniejszy i który – co nie jest przypadkiem – wewnętrznie trzyma zbiór jako maskę na `long`. Jeśli Twoje flagi są enumem i nie musisz ich serializować do liczby, użyj `EnumSet`. Ręczne maski zostaw dla protokołów, formatów binarnych i interfejsów z kodem natywnym, gdzie liczba jest wymuszona z zewnątrz.

### 4.4 Kiedy maska naprawdę bije `HashSet`

Porównanie `HashSet<Integer>` z maską na `long` przy zbiorze małych liczb wypada dość brutalnie:

- **Pamięć.** `HashSet` z 20 elementami to tablica kubełków plus 20 obiektów `Node` plus 20 opakowanych `Integer`. Maska to 8 bajtów.
- **Brak alokacji.** Operacje na masce nie tworzą obiektów, więc nie obciążają garbage collectora.
- **Cache.** Cały zbiór mieści się w jednym rejestrze, a nie w kilkunastu miejscach na stercie.
- **Operacje zbiorowe w jednej instrukcji.** Suma dwóch zbiorów to jedno `|`. Porównanie dwóch zbiorów to jedno `==`.

Warunek jest oczywisty: elementy muszą być małymi liczbami całkowitymi z ustalonego, wąskiego zakresu. Dla zbioru stringów albo dla identyfikatorów rzędu milionów wracamy do normalnych struktur (albo do `BitSet`, który jest maską rozciągniętą na tablicę `long`ów).

Iterowanie po elementach takiego zbioru wygląda tak – i jest to najczęstsze zastosowanie omawianych wcześniej `ctz` i `x & (x-1)`:

```java
int m = mask;
while (m != 0) {
    int i = Integer.numberOfTrailingZeros(m);   // najniższy element zbioru
    process(i);
    m &= m - 1;                                 // usuń go i leć dalej
}
```

### 4.5 Przeglądanie wszystkich podzbiorów

Skoro zbiór to liczba, to **wszystkie podzbiory zbioru `n`-elementowego to po prostu liczby od `0` do `2^n - 1`**. Zapętlenie po nich jest trywialne:

```java
for (int s = 0; s < (1 << n); s++) {
    // s reprezentuje jeden z 2^n podzbiorów
}
```

Trudniejszy wariant: przejść po wszystkich podzbiorach *konkretnej* maski `m`, a nie całego zbioru. Służy do tego zgrabna sztuczka z odejmowaniem jedynki:

```java
for (int s = m; s > 0; s = (s - 1) & m) {
    // s przebiega wszystkie niepuste podzbiory m
}
```

Odejmowanie `1` „pożycza" z wyższych bitów, a `& m` natychmiast przycina wynik do bitów należących do `m` – w efekcie odliczamy w dół, ale wyłącznie po podzbiorach. Warto wiedzieć, że przejście po wszystkich podzbiorach wszystkich masek kosztuje `3^n`, a nie `4^n`, bo każdy element jest albo poza maską, albo w masce i poza podzbiorem, albo w podzbiorze.

### 4.6 Bitmask DP – zbiór jako stan algorytmu

Ostatni krok tego rozumowania: skoro zbiór jest liczbą, to zbiór może być **indeksem w tablicy**. Na tym opiera się cała rodzina algorytmów programowania dynamicznego po podzbiorach.

Kanoniczny przykład to problem komiwojażera. Stan definiujemy jako parę: „zbiór już odwiedzonych miast" oraz „miasto, w którym aktualnie stoję":

```java
// dp[mask][i] = najtańsza trasa odwiedzająca dokładnie miasta z mask,
//               kończąca się w mieście i
int[][] dp = new int[1 << n][n];

for (int mask = 1; mask < (1 << n); mask++) {
    for (int i = 0; i < n; i++) {
        if ((mask & (1 << i)) == 0) continue;        // i musi być w mask
        int prev = mask & ~(1 << i);                 // stan przed wejściem do i
        for (int j = 0; j < n; j++) {
            if ((prev & (1 << j)) == 0) continue;
            dp[mask][i] = Math.min(dp[mask][i], dp[prev][j] + cost[j][i]);
        }
    }
}
```

Ten kod jest ilustracją całego rozdziału: `mask & (1 << i)` to test przynależności, `mask & ~(1 << i)` to usunięcie elementu, a `1 << n` to liczność zbioru potęgowego. Złożoność `O(2^n · n²)` jest wykładnicza, więc podejście działa dla `n` rzędu 20 – ale dla takich rozmiarów bije na głowę przeszukiwanie wszystkich `n!` permutacji.

Ta sama technika obsługuje przydział zadań do pracowników, pokrycie zbioru, układanie klocków na planszy i kilkanaście innych klasycznych problemów. Wspólny mianownik: **liczba stanów jest wykładnicza, ale każdy stan mieści się w jednym `int`.**

## 5. Zastosowania praktyczne – gdzie to realnie siedzi

Poprzednie dwa rozdziały dały narzędzia. Ten pokazuje warsztat, w którym są używane. Cel jest prosty: po tej lekturze masz rozpoznawać te wzorce w cudzym kodzie i wiedzieć, po co tam są.

### 5.1 Pakowanie danych w jedno słowo maszynowe

Skoro `int` ma 32 bity, a Twoje pole potrzebuje ośmiu, to marnujesz 24 bity. Pakowanie polega na wciśnięciu kilku pól w jedną liczbę: przesunięciem ustawiasz pole na właściwej pozycji, a `|` je skleja.

Kanoniczny przykład to kolor ARGB, w którym cztery kanały po 8 bitów mieszczą się w jednym `int`:

```java
int argb = (a << 24) | (r << 16) | (g << 8) | b;

int red   = (argb >> 16) & 0xFF;   // przesuń na pozycję 0, odetnij resztę
int alpha = argb >>> 24;           // uwaga: >>> , bo bit 31 to bit znaku!
```

Odczyt to zawsze ten sam schemat: **przesuń, potem zamaskuj**. Maska `& 0xFF` jest konieczna, bo przesunięcie nie kasuje bitów leżących wyżej.

Ten sam mechanizm w większej skali to identyfikatory Snowflake z Twittera – jeden `long` niosący trzy pola:

```text
 1 bit │        41 bitów        │  10 bitów  │  12 bitów
 zero  │  znacznik czasu (ms)   │  id węzła  │  licznik
```

Zysk nie polega tylko na oszczędności pamięci. Skoro znacznik czasu leży na najstarszych bitach, to **zwykłe sortowanie liczbowe sortuje identyfikatory chronologicznie**, a klucz główny w bazie jest rosnący. Ta sama sztuczka działa dla kluczy złożonych: pakując `(priorytet, timestamp)` w jednego `long`, dostajesz porównanie leksykograficzne za darmo, jednym `<`.

Bardzo praktyczny wariant to spakowanie dwóch `int`-ów w klucz mapy bez alokowania obiektu:

```java
long key = ((long) x << 32) | (y & 0xFFFFFFFFL);   // maska jest OBOWIĄZKOWA
```

Bez `& 0xFFFFFFFFL` ujemny `y` rozszerzy się znakiem na całe 64 bity i zamaże górną połowę klucza. To jedna z najczęstszych pomyłek w tym temacie – wrócę do niej w rozdziale 6.

Cena pakowania jest realna: kod robi się mniej czytelny, a każde pole ma sztywny limit zakresu, o który prędzej czy później ktoś się otrze. Rób to tam, gdzie format i tak jest wymuszony z zewnątrz (protokół, plik binarny, klucz cache'a) albo gdzie liczba rekordów idzie w miliony.

### 5.2 Sieci – maski podsieci

Zapis `192.168.1.0/24` to nie jest żadna abstrakcja – to dosłownie maska bitowa z 24 jedynkami:

```text
maska /24 = 11111111 11111111 11111111 00000000
```

Wszystkie operacje na podsieciach są jednolinijkowcami z rozdziału 3:

```java
int mask      = prefix == 0 ? 0 : -1 << (32 - prefix);  // /24 → 0xFFFFFF00
int network   = ip & mask;                              // adres sieci
int broadcast = ip | ~mask;                             // adres rozgłoszeniowy
boolean same  = ((a ^ b) & mask) == 0;                  // ta sama podsieć?
int hosts     = (1 << (32 - prefix)) - 2;               // adresowalne hosty
```

`-1` to same jedynki, więc `-1 << (32 - prefix)` przesuwa je w lewo, zostawiając na końcu tyle zer, ile bitów należy do hosta. Warunek na `prefix == 0` nie jest przesadną ostrożnością: `-1 << 32` w Javie daje `-1`, a nie zero – o czym za chwilę w rozdziale o pułapkach.

Zwróć uwagę na test „ta sama podsieć". XOR daje jedynki dokładnie tam, gdzie adresy się różnią; maska zostawia z tego tylko część sieciową. Jeśli po zamaskowaniu nie ma żadnej jedynki, adresy różnią się wyłącznie w części hosta.

To najlepszy przykład na to, że `&` czyta się jako **„wytnij prefiks"**, a nie jako „koniunkcja logiczna". Router robi to samo miliony razy na sekundę, szukając najdłuższego pasującego prefiksu w tablicy routingu.

### 5.3 Tablice haszujące i mieszanie bitów

Wracamy do linijki ze wstępu:

```java
int index = hash & (table.length - 1);
```

To jest po prostu `hash mod table.length` z punktu 3.2 – jedna instrukcja zamiast dzielenia. Ale ta optymalizacja ma ukryty koszt: **maska bierze wyłącznie najmłodsze bity**. Jeśli funkcja haszująca umieści całą swoją zmienność na starszych bitach, wszystkie klucze wylądują w jednym kubełku, a mapa zdegeneruje się do listy.

Dlatego `HashMap` w Javie nie używa `hashCode()` bezpośrednio, tylko najpierw miesza:

```java
static int hash(Object key) {
    int h = key.hashCode();
    return h ^ (h >>> 16);       // złóż starszą połowę na młodszą
}
```

Jedno `^` i jedno `>>>` sprawiają, że każdy z 16 górnych bitów wpływa na któryś z dolnych – dokładnie tych, które przetrwają maskowanie. To najtańsze możliwe ubezpieczenie od słabego `hashCode()`.

Ta sama para operacji jest podstawą całej rodziny funkcji mieszających. Finalizator z MurmurHash3 to naprzemienne składanie bitów i mnożenie przez stałe:

```java
h ^= h >>> 16;  h *= 0x85ebca6b;
h ^= h >>> 13;  h *= 0xc2b2ae35;
h ^= h >>> 16;
```

Mnożenie rozprowadza informację z młodszych bitów na starsze, a `^ (h >>> k)` zawraca ją z powrotem w dół. Generatory typu *xorshift* i *splitmix* działają na tej samej zasadzie: **XOR z własnym przesunięciem to najtańszy znany sposób na wymieszanie bitów**.

Na koniec ładny szczegół z tej samej klasy. Przy powiększaniu tablicy dwukrotnie element albo zostaje na swoim indeksie, albo przesuwa się dokładnie o starą pojemność – i decyduje o tym jeden bit:

```java
if ((e.hash & oldCap) == 0)  // zostaje na indeksie j
else                          // ląduje na j + oldCap
```

Nie trzeba przeliczać reszty z dzielenia dla żadnego elementu. Cała operacja rehashowania sprowadza się do sprawdzenia jednego bitu, który właśnie „wszedł" do maski.

### 5.4 XOR, czyli operacja odwracalna

XOR ma jedną własność, z której wynika zaskakująco dużo:

```text
a ^ b ^ b == a
```

Jest sam sobie odwrotnością (matematyk powie: jest inwolucją). Zaszyfrowanie i odszyfrowanie to ta sama operacja.

**Szyfr XOR i one-time pad.** Jeśli klucz jest losowy, tak długi jak wiadomość i użyty raz, to `c = m ^ k` jest szyfrem doskonałym – matematycznie nie do złamania. Cały haczyk tkwi w warunkach. Kiedy ten sam klucz zostanie użyty dwa razy, atakujący liczy `c1 ^ c2 == m1 ^ m2`, klucz znika z równania i zostaje zależność między dwiema wiadomościami jawnymi. Dlatego „szyfrowanie" XOR-em z krótkim, powtarzanym hasłem to nie jest szyfrowanie, tylko zaciemnianie.

**RAID 5.** Parzystość zapisywana na dysku nadmiarowym to XOR pozostałych:

```text
P = D1 ^ D2 ^ D3
```

Gdy padnie `D2`, odzyskujemy go z `D2 = P ^ D1 ^ D3`. Jedna operacja procesora ratuje dane po awarii dysku – i działa niezależnie od tego, który dysk zniknął, bo wszystkie występują w tym równaniu symetrycznie.

**Wykrywanie i korekcja błędów.** Bit parzystości to XOR wszystkich bitów słowa – wykrywa każdą nieparzystą liczbę przekłamań. Kod Hamminga idzie krok dalej: bity kontrolne stoją na pozycjach będących potęgami dwójki, a XOR indeksów wszystkich ustawionych bitów daje tzw. syndrom. Jeśli syndrom jest zerem, transmisja była poprawna; jeśli nie – **jego wartość jest wprost numerem przekłamanego bitu**, który wystarczy odwrócić.

**CRC i LFSR.** Suma kontrolna CRC to reszta z dzielenia wielomianów nad ciałem dwuelementowym GF(2). Brzmi groźnie, ale sprowadza się do jednego zdania: to zwykłe dzielenie pisemne, w którym odejmowanie jest XOR-em, bo nie ma przeniesień. Stąd implementacja CRC to pętla z `^` i `>>`, a nie żadna arytmetyka.

**I zagadka rekrutacyjna.** „W tablicy każda liczba występuje parzyście wiele razy oprócz jednej – znajdź ją." Skoro `x ^ x == 0`, to wystarczy zXOR-ować wszystko; pary się skasują, zostanie szukana liczba. Trudniejszy wariant z **dwiema** takimi liczbami rozwiązuje `x & -x` z punktu 3.4: XOR całości daje `x ^ y`, jego najniższy ustawiony bit wskazuje pozycję, na której `x` i `y` się różnią, więc dzielimy tablicę na dwie grupy według tego bitu i XOR-ujemy każdą osobno.

### 5.5 Kodowanie i kompresja

**Zigzag encoding.** Formaty takie jak Protocol Buffers zapisują liczby zmiennej długości (*varint*) – małe wartości zajmują jeden bajt, duże więcej. Problem: `-1` w U2 to `11111111 11111111 11111111 11111111`, czyli maksymalnie niekorzystny wzorzec, który zajmie pięć bajtów. Rozwiązaniem jest przeplecenie liczb dodatnich i ujemnych, tak żeby małe co do modułu trafiały na małe kody:

```java
int encode(int n) { return (n << 1) ^ (n >> 31); }
int decode(int n) { return (n >>> 1) ^ -(n & 1);  }
```

Rozłóżmy to na czynniki. `n << 1` robi miejsce na bit znaku na najmłodszej pozycji. `n >> 31` (przesunięcie **arytmetyczne**!) daje same zera dla liczb nieujemnych i same jedynki dla ujemnych, więc XOR albo nie robi nic, albo odwraca wszystkie bity. Efekt:

| `n` | 0 | -1 | 1 | -2 | 2 |
|---|---|---|---|---|---|
| kod | 0 | 1 | 2 | 3 | 4 |

To najładniejszy przykład w całym artykule: dwie operacje, zero warunków, a liczba `-1` schudła z pięciu bajtów do jednego.

**Varint / LEB128.** Sam format zmiennej długości też jest schematem bitowym: w każdym bajcie siedem młodszych bitów niesie dane, a najstarszy jest flagą „jest jeszcze ciąg dalszy". Odczyt to pętla z `b & 0x7F`, `<<= 7` i testem `(b & 0x80) != 0`.

**UTF-8.** Też jest kodem bitowym i to wyjątkowo przemyślanym:

```text
0xxxxxxx                             – ASCII, 1 bajt
110xxxxx 10xxxxxx                    – 2 bajty
1110xxxx 10xxxxxx 10xxxxxx           – 3 bajty
```

Każdy bajt kontynuacji zaczyna się od `10`, czego nie robi żaden bajt początkowy. Dlatego test `(b & 0xC0) == 0x80` odpowiada na pytanie „czy wylądowałem w środku znaku", a wyszukiwanie tekstu w UTF-8 nigdy nie da fałszywego trafienia w środku wielobajtowej sekwencji. Ta własność nazywa się samosynchronizacją i jest głównym powodem, dla którego UTF-8 wygrał z konkurencją.

### 5.6 Struktury danych zbudowane na bitach

**`BitSet`.** To maska bitowa rozciągnięta na tablicę `long`-ów – i jej implementacja jest podręcznikowym zastosowaniem rozdziału 3:

```java
words[i >> 6] |= 1L << i;     // i >> 6  ==  i / 64  (numer słowa)
                              // 1L << i ==  1L << (i & 63)  (bit w słowie)
```

Java sama maskuje licznik przesunięcia do sześciu bitów, więc `i & 63` nie musi być zapisane wprost. Zysk pamięciowy: milion flag w `boolean[]` to megabajt, w `BitSet` – 125 kB, czyli różnica między „nie mieści się w cache'u L2" a „mieści się".

**Filtr Bloom'a.** Kilka funkcji haszujących ustawia bity w dużej masce. Jeśli którykolwiek z bitów dla danego klucza jest zerem, klucza na pewno nie ma w zbiorze; jeśli wszystkie są jedynkami, prawdopodobnie jest. Probabilistyczna struktura, która za cenę fałszywych trafień daje stałą pamięć – używana m.in. przez bazy LSM (Cassandra, RocksDB) do unikania czytania z dysku.

**Roaring Bitmap.** Nowoczesna, kompresowana bitmapa, na której stoją indeksy w Lucene, ClickHouse czy Druidzie. Dzieli przestrzeń na fragmenty i dla każdego wybiera reprezentację (gęsta bitmapa albo posortowana tablica), po czym operacje typu „wszystkie dokumenty pasujące do A i B" wykonuje jako `AND` na milionach bitów naraz.

**Bitboardy.** Szachownica ma 64 pola, a `long` ma 64 bity – to zbieżność zbyt piękna, żeby jej nie wykorzystać. Silniki szachowe trzymają pozycję jako komplet masek (białe pionki, czarne wieże, pola zajęte…), a generowanie ruchów to przesunięcia:

```java
long pushes  = (whitePawns << 8) & empty;             // ruch o jedno pole
long attacksNE = (whitePawns & ~FILE_H) << 9;         // bicie w prawo
```

Wykluczenie linii H maską `& ~FILE_H` zapobiega „przewinięciu" pionka na drugą stronę planszy. Liczba figur to `Long.bitCount(mask)`, a iterowanie po nich to znany z 4.4 duet `numberOfTrailingZeros` + `m &= m - 1`. Cała ocena pozycji sprowadza się do kilkunastu operacji na rejestrach.

### 5.7 Programowanie bezgałęziowe i sprytne jednolinijkowce

Znasz je z rozmów kwalifikacyjnych. Wartość bezwzględna bez `if`:

```java
int mask = x >> 31;              // -1 dla ujemnych, 0 dla reszty
int abs  = (x ^ mask) - mask;    // dla ujemnych: ~x + 1, czyli -x
```

Zamiana zmiennych bez zmiennej pomocniczej:

```java
a ^= b;  b ^= a;  a ^= b;
```

I od razu uczciwe postawienie sprawy: **nie pisz tak w kodzie produkcyjnym**. Zamiana przez XOR jest wolniejsza od trzech zwykłych przypisań (tworzy łańcuch zależności, którego procesor nie może zrównoleglić) i cicho psuje dane, gdy oba argumenty wskazują na tę samą komórkę. Warianty `min`/`max`/`abs` bez skoków kompilator i tak wygeneruje sam, używając instrukcji `cmov`.

Są jednak dwa miejsca, w których to podejście ma sens. Pierwsze to dydaktyka – rozłożenie takiej linijki na czynniki uczy myślenia o bitach. Drugie jest znacznie poważniejsze: **kryptografia**. Kod wykonujący się w stałym czasie, niezależnie od danych, nie zdradza sekretów przez pomiar czasu ani przez zachowanie predyktora skoków. Dlatego biblioteki kryptograficzne konsekwentnie zastępują `if` maskami – tam brak gałęzi to nie optymalizacja, tylko wymóg bezpieczeństwa.

## 6. Pułapki, na których wykłada się każdy

Ten rozdział ma jeden cel: oszczędzić Ci wieczoru z debuggerem.

**Priorytet operatorów.** Operatory bitowe mają w C, C++ i Javie **niższy** priorytet niż operatory porównania. To dziedzictwo lat siedemdziesiątych i najczęstsza pomyłka w całym temacie:

```c
if (flags & MASK == 0)      // parsuje się jako:  flags & (MASK == 0)
```

W C kompiluje się to bez ostrzeżenia i po cichu robi coś innego, niż napisałeś. Java uratuje Cię błędem kompilacji (bo `int & boolean` nie ma sensu), ale tylko w tym konkretnym układzie typów. Reguła: **przy operatorach bitowych zawsze stawiaj nawiasy**, nawet gdy jesteś pewien priorytetów.

**Przesunięcie o więcej niż szerokość typu.** Intuicja mówi, że `1 << 32` powinno dać zero. Nie daje:

```java
1 << 32     // == 1   ! licznik jest brany modulo 32
1L << 64    // == 1L  ! dla long modulo 64
1 << 40     // == 256 (bo 40 mod 32 == 8)
```

Java maskuje licznik przesunięcia do pięciu bitów dla `int` i sześciu dla `long`. W C jest jeszcze gorzej – to zachowanie niezdefiniowane, więc wynik zależy od procesora i poziomu optymalizacji. Praktyczna konsekwencja: **przy więcej niż 31 flagach pisz `1L << i`, nie `1 << i`**. Sam literał decyduje o typie, więc `long mask = 1 << 40;` jest błędem, mimo że zmienna jest 64-bitowa.

**`>>` kontra `>>>`.** W Javie `>>` powiela bit znaku, a `>>>` wstawia zera. Jeśli traktujesz liczbę jako wzorzec bitowy (kolor, hash, spakowane pola), chcesz `>>>`; jeśli jako liczbę ze znakiem – `>>`. W C decyduje typ: dla `unsigned` przesunięcie jest logiczne, dla `signed` arytmetyczne. W Pythonie `>>>` nie istnieje i nie jest potrzebny, bo liczby nie mają ustalonej szerokości.

**Rozszerzanie znaku przy rzutowaniu.** Klasyk przy parsowaniu danych binarnych:

```java
byte b = (byte) 0xFF;
int  i = b;              // == -1, nie 255!
int  v = b & 0xFF;       // == 255  ← tak trzeba
```

`byte` w Javie jest zawsze ze znakiem, więc konwersja do `int` powiela bit 7 na całą górę. Lekarstwem jest maska `& 0xFF`. Ta sama pułapka w wersji 64-bitowej to spakowanie dwóch `int`-ów z punktu 5.1 – bez `& 0xFFFFFFFFL` ujemna dolna połowa zamaże górną.

**Zerowanie górnych bitów przy przesunięciu w lewo na `long`.** `(long) (x << 32)` to nie to samo co `((long) x) << 32`. W pierwszej wersji przesunięcie wykonuje się na `int`, więc licznik idzie modulo 32 i nie dzieje się nic. Rzutuj **przed** przesunięciem.

**Python działa inaczej.** Liczby całkowite mają nieskończoną precyzję, więc nie ma przepełnienia ani ustalonej szerokości słowa:

```python
1 << 1000     # działa, daje liczbę o 302 cyfrach
~5            # == -6, a nie 250 czy 4294967290
```

Jeśli symulujesz arytmetykę 32-bitową (np. implementując hash albo CRC), musisz domykać każdą operację maską `& 0xFFFFFFFF` – inaczej wyniki rozjadą się po pierwszym przepełnieniu, którego w Pythonie po prostu nie ma.

**`|=` kontra `+=` przy flagach.** Dodawanie flag „prawie działa": `READ + WRITE` daje to samo co `READ | WRITE`, dopóki żadna flaga nie zostanie dodana dwa razy. Za drugim razem `+` wygeneruje przeniesienie i zapali sąsiedni bit, czyli włączy zupełnie inną flagę. To błąd, który ujawnia się miesiąc po wdrożeniu. Do składania flag zawsze `|`.

**Kolejność bajtów to nie kolejność bitów.** *Endianness* opisuje, w jakiej kolejności bajty liczby leżą w pamięci, i nie ma nic wspólnego z numeracją bitów wewnątrz liczby. Operacje `<<`, `>>` i `&` działają na wartości, a nie na jej układzie w pamięci, więc są od endianness całkowicie niezależne. Problem pojawia się dopiero na granicy: przy `ByteBuffer`, `mmap`, odczycie z gniazda albo parsowaniu pliku binarnego. Wtedy ustaw kolejność jawnie (`ByteBuffer.order(ByteOrder.BIG_ENDIAN)`) zamiast liczyć na domyślną.

**`Math.abs(Integer.MIN_VALUE)` jest ujemne.** To bezpośrednia konsekwencja `-x == ~x + 1`: `Integer.MIN_VALUE` nie ma dodatniego odpowiednika w zakresie typu, więc negacja przepełnia się z powrotem na siebie. Każda funkcja przyjmująca „wartość bezwzględną" ma tu jeden przypadek brzegowy, o którym zwykle nikt nie pamięta.

## 7. Wydajność – kiedy to naprawdę ma sens

Zacznijmy od rozprawienia się z mitem, który ciągnie się od trzydziestu lat: **„zamienię `* 2` na `<< 1` i będzie szybciej"**. Nie będzie. Każdy kompilator od dekad robi redukcję siły sam i to lepiej od Ciebie, bo zna docelowy procesor. Zamiana `* 7` na `(x << 3) - x` też nie ma sensu – kompilator już to rozważył i wybrał wariant tańszy na tej architekturze. Jak pokazałem w 3.1, jedyny wyjątek dotyczy dzielenia liczb ze znakiem, gdzie `>> k` naprawdę jest krótsze niż `/ 2^k` – ale wyłącznie dlatego, że **liczy coś innego**.

Są za to miejsca, w których operacje bitowe dają zysk nie do podrobienia:

- **Gorące pętle i parsery protokołów** – gdy kod wykonuje się miliardy razy, każda instrukcja mniej jest widoczna w profilu.
- **Systemy wbudowane** – rejestry sprzętowe są bitowe z natury, a pamięci jest tyle, ile jest.
- **Kolumnowe silniki baz danych i wyszukiwarki** – filtrowanie milionów wierszy jako `AND` na bitmapach, po 64 wiersze na instrukcję.
- **SIMD** – instrukcje wektorowe operują na 256 czy 512 bitach naraz, a maski wyboru elementów są… maskami bitowymi.

Najważniejszy argument nie dotyczy jednak liczby cykli, tylko pamięci. **Gęstość danych to mniej chybień cache'a**, a chybienie w cache'u kosztuje kilkaset cykli – czyli tyle, co setka operacji arytmetycznych. Milion flag w `boolean[]` zajmuje megabajt i wypada z L2; ten sam milion w `BitSet` to 125 kB i mieści się z zapasem. Tu nie chodzi o zaoszczędzenie instrukcji, tylko o to, żeby dane w ogóle były pod ręką.

I zasada praktyczna, ważniejsza od wszystkiego powyżej: **korzystaj z gotowców zamiast pisać pętle**.

| Zamiast | Użyj | Kompiluje się do |
|---|---|---|
| pętli zliczającej jedynki | `Integer.bitCount(x)` | `POPCNT` |
| szukania najniższego bitu | `Integer.numberOfTrailingZeros(x)` | `TZCNT` / `BSF` |
| logarytmu przez `Math.log` | `31 - Integer.numberOfLeadingZeros(x)` | `LZCNT` / `BSR` |
| ręcznej zamiany bajtów | `Integer.reverseBytes(x)` | `BSWAP` |

Te metody są w JVM *intrinsics* – JIT zamienia je na pojedyncze instrukcje procesora. W C odpowiednikiem jest rodzina `__builtin_popcount`, w Pythonie `int.bit_count()` (od 3.10) oraz `numpy` i `bitarray` dla operacji masowych.

Regułę na koniec sformułowałbym tak: **używaj bitów tam, gdzie domena jest bitowa** – protokół, flagi, zbiór, maska, indeks kolumnowy. Nie używaj ich po to, żeby udowodnić, że umiesz. Kod z `x >> 1` zamiast `x / 2` w regule biznesowej nie jest szybszy, jest tylko trudniejszy do czytania. A jeśli już schodzisz na ten poziom, zmierz to – w Javie JMH, nie `System.nanoTime()` w pętli.

## 8. Ćwiczenia do samodzielnego przerobienia

*(sekcja w planie – do napisania)*

1. Sprawdź, czy liczba jest potęgą dwójki (jedno wyrażenie).
2. Policz jedynki w `int` na dwa sposoby i porównaj z `Integer.bitCount`.
3. Zamień kolejność bajtów w 32-bitowej liczbie (bswap).
4. Zaimplementuj `set/clear/toggle/test` na własnej klasie flag.
5. Znajdź dwie liczby występujące pojedynczo w tablicy, gdzie reszta jest parami (XOR + `x & -x`).
6. Wygeneruj wszystkie podzbiory zbioru `n`-elementowego przez zliczanie od `0` do `2^n - 1`.
7. Zaimplementuj zigzag encode/decode i sprawdź na `-1, 0, 1, -64`.

## 9. Podsumowanie i ściągawka

Operacje bitowe wyglądają na sztuczkę dla wtajemniczonych, a są trzema zwyczajnymi rzeczami naraz. Po pierwsze, są **arytmetyką**: przesunięcie mnoży i dzieli przez potęgi dwójki, maska liczy resztę, XOR dodaje modulo 2. Po drugie, są **algebrą zbiorów**: jedna liczba to zbiór, a `&`, `|`, `^` to przecięcie, suma i różnica symetryczna. Po trzecie, są **sposobem pakowania danych** – kilku pól w jedno słowo maszynowe, miliona flag w 125 kB. Wszystko, co pokazałem w rozdziale 5, od maski podsieci po bitboardy, jest konsekwencją jednej z tych trzech rzeczy.

Ich prawdziwa wartość nie leży w oszczędzaniu cykli – od tego jest kompilator. Leży w tym, że gdy domena problemu **jest** bitowa, zapis bitowy jest najkrótszym i najuczciwszym opisem tego, co się dzieje. `ip & mask` to nie jest zoptymalizowana wersja czegoś innego; to jest definicja adresu sieci.

**Ściągawka do zapamiętania:**

| Wyrażenie | Znaczenie |
|---|---|
| `x << k` / `x >> k` | `x * 2^k` / `floor(x / 2^k)` – uwaga: podłoga, nie obcięcie |
| `x & (2^k - 1)` | `x mod 2^k` (tylko dla potęg dwójki) |
| `x & (x - 1)` | wyzeruj najniższy ustawiony bit → test potęgi dwójki, popcount |
| `x & -x` | zostaw tylko najniższy ustawiony bit (*lowbit*) |
| `(x + m - 1) & ~(m - 1)` | zaokrąglij w górę do wielokrotności `m = 2^k` |
| `x ^ y ^ y` | `x` – XOR jest odwracalny |
| `x + y` | `(x ^ y) + ((x & y) << 1)` – suma i przeniesienia |
| `~x` | `-x - 1` |
| `a \| b`, `a & b`, `a ^ b` | suma, przecięcie, różnica symetryczna zbiorów |
| `a & ~b` | różnica zbiorów `A \ B` |
| `(a & b) == b` | test podzbioru `B ⊆ A` |
| `a \| (1 << i)`, `a & ~(1 << i)` | dodaj / usuń element `i` |
| `Integer.bitCount(a)` | liczność zbioru |
| `x >> 31` | maska `-1` dla ujemnych, `0` dla reszty |

**Dalsza lektura:**

- Henry S. Warren Jr., *Hacker's Delight* – biblia tematu, jeden rozdział na każdą sztuczkę z tego artykułu i sto kolejnych.
- *Bit Twiddling Hacks* (Sean Eron Anderson, Stanford) – darmowa kolekcja jednolinijkowców z wyprowadzeniami.
- Dokumentacja `java.lang.Integer`, `java.lang.Long` i `java.util.BitSet` – warto przeczytać listę metod raz w życiu, żeby wiedzieć, czego nie trzeba pisać samemu.
- Źródła `java.util.HashMap` – krótkie, czytelne i pełne omówionych tu wzorców.

**Powiązane notatki:** [[zrozumienie-binary-search]] – przepełnienie przy `(l + r) / 2` i `>>> 1` jako lekarstwo.
