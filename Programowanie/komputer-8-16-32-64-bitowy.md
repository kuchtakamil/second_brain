# Co znaczy, że komputer jest 8-, 16-, 32- albo 64-bitowy

Każdy inżynier używa tych określeń codziennie i prawie nikt nie potrafi ich obronić, gdy ktoś dopyta. „64-bitowy procesor" – czyli co dokładnie ma 64 bity? Rejestry? Szyna danych? Adres? Wskaźnik? Instrukcja? Okazuje się, że w jednej maszynie te liczby bywają zupełnie różne, a mimo to nazwa jest jedna i wcale nie przypadkowa.

Ten artykuł rozdziela pięć rzeczy, które ludzie wrzucają do jednego worka, pokazuje na historycznych i współczesnych procesorach, że potrafią się rozjeżdżać, i odpowiada na najważniejsze pytanie: **która z tych szerokości decyduje o tym, jak nazywamy maszynę** – i dlaczego akurat ta.

## 1. Pięć różnych szerokości w jednym układzie

Kiedy mówimy „procesor N-bitowy", kandydatów do tytułu jest co najmniej pięciu:

1. **Szerokość rejestrów ogólnego przeznaczenia** – ile bitów mieści się w jednej „szufladzie" procesora (`EAX` ma 32 bity, `RAX` ma 64).
2. **Szerokość ALU** – na jak szerokich liczbach jednostka arytmetyczna wykonuje dodawanie w jednej operacji.
3. **Szerokość szyny danych** – ile bitów przechodzi między procesorem a pamięcią w jednym transferze.
4. **Szerokość szyny adresowej / przestrzeni adresowej** – ile różnych komórek pamięci umiesz w ogóle wskazać.
5. **Szerokość słowa instrukcji** – ile bitów zajmuje zakodowany rozkaz.

Te wielkości są **niezależne** i historia sprzętu składa się w dużej mierze z ich rozjeżdżania się, zwykle z powodów ekonomicznych. Zanim wejdziemy w szczegóły, jedna tabela, która jest właściwie streszczeniem całego artykułu:

| Procesor | Rejestry | ALU | Szyna danych | Adresowanie | Nazywany |
|---|---|---|---|---|---|
| MOS 6502 (1975) | 8 | 8 | 8 | 16 bitów (64 kB) | 8-bitowy |
| Zilog Z80 (1976) | 8 | **4** (dwa przebiegi) | 8 | 16 bitów (64 kB) | 8-bitowy |
| Intel 8086 (1978) | 16 | 16 | 16 | 20 bitów (1 MB) | 16-bitowy |
| Intel 8088 (1979) | 16 | 16 | **8** | 20 bitów (1 MB) | 16-bitowy |
| Motorola 68000 (1979) | 32 | 16 | 16 | 24 bity (16 MB) | 16/32-bitowy |
| Intel 386SX (1988) | 32 | 32 | 16 | 24 bity (16 MB) | 32-bitowy |
| Intel 386DX (1985) | 32 | 32 | 32 | 32 bity (4 GB) | 32-bitowy |
| Intel Pentium (1993) | 32 | 32 | **64** | 32 bity (4 GB) | 32-bitowy |
| x86-64 dzisiaj | 64 | 64 | 64 na kanał × 2–8 | 48 bitów wirt., ~46 fiz. | 64-bitowy |
| ARMv8-A (AArch64) | 64 | 64 | zależy od SoC | 48/52 bity | 64-bitowy |

Kilka wierszy tej tabeli warto przeczytać dwa razy. Z80 nazywamy 8-bitowym, choć ma 4-bitową ALU. Pentium nazywamy 32-bitowym, choć wozi dane 64-bitową szyną. 8088 i 8086 mają tę samą nazwę „16-bitowy" i uruchamiają identyczne binaria, mimo że jeden ma szynę danych dwa razy węższą od drugiego. Żaden z 8-bitowców nie awansował do miana 16-bitowego, choć wszystkie adresują pamięć 16-bitowym adresem.

Wniosek narzuca się sam i wrócę do niego w rozdziale 5: **ani szyna danych, ani szyna adresowa nie decydują o nazwie**. Najpierw jednak trzeba je porządnie rozdzielić, bo to najczęstsze źródło zamieszania.

## 2. Szyna adresowa a szyna danych – pytanie i odpowiedź

Najprostszy model, który wystarcza do końca życia zawodowego: **szyna adresowa niesie pytanie, szyna danych niesie odpowiedź**.

```text
        ┌───────────┐   adres: "podaj zawartość komórki 0x1F40"   ┌────────┐
        │           │ ─────────────── 20 linii ─────────────────► │        │
        │ PROCESOR  │                                             │ PAMIĘĆ │
        │           │ ◄────────────── 8 linii ──────────────────  │        │
        └───────────┘   dane: 0x42                                └────────┘
```

Procesor wystawia na linie adresowe numer komórki, pamięć odpowiada, wystawiając jej zawartość na linie danych. To dwa fizycznie osobne pęki drutów (w starszych układach czasem multipleksowane w czasie, jak `AD0–AD7` w 8085 – najpierw adres, potem dane po tych samych nogach).

Z tego wynikają dwie różne konsekwencje:

- **Szerokość szyny adresowej określa, ILE komórek umiesz rozróżnić.** `n` linii adresowych to `2^n` możliwych adresów. Przy adresowaniu bajtowym daje to wprost rozmiar przestrzeni adresowej: 16 linii → 64 kB, 20 → 1 MB, 24 → 16 MB, 32 → 4 GB, 48 → 256 TB. Ta liczba nic nie mówi o tym, ile danych przechodzi na raz.
- **Szerokość szyny danych określa, ILE bitów przechodzi w jednym transferze.** To czysta przepustowość. Przy 8-bitowej szynie pobranie 16-bitowej liczby wymaga dwóch cykli magistrali, przy 16-bitowej – jednego. Ta liczba nic nie mówi o tym, ile pamięci umiesz zaadresować.

### Dlaczego to się myli: adres też jest wartością

Tu leży pułapka, o którą rozbija się większość intuicji. Adres jest **jednocześnie** sygnałem sterującym na szynie adresowej i zwykłą liczbą, którą trzymasz w rejestrze i przesyłasz szyną danych. Kiedy robisz w C:

```c
int **pp = ...;
int *p = *pp;      // wczytanie wskaźnika z pamięci
int x = *p;        // dopiero teraz użycie go jako adresu
```

...to w pierwszej linijce adres jest **danymi** – jedzie szyną danych, jak każda inna liczba. W drugiej ten sam ciąg bitów trafia na szynę adresową jako pytanie. Ten sam bajtowy wzorzec pełni dwie zupełnie różne role, w zależności od tego, na którą szynę go położysz.

Dlatego pytanie „czy szyna adresowa jest szersza od danych?" nie ma uniwersalnej odpowiedzi, ale ma dwa dobre skrajne przykłady:

**Adres szerszy niż wszystko inne – Intel 8086.** Rejestry mają 16 bitów, więc największa liczba, jaką procesor przechowa w jednym rejestrze, to 65 535. Tymczasem szyna adresowa ma 20 linii i pozwala zaadresować 1 MB. Skąd wziąć 20-bitowy adres, jeśli nie ma 20-bitowego rejestru? Ze składania dwóch:

```text
adres_fizyczny = (segment << 4) + offset
                  ↑ 16 bitów      ↑ 16 bitów   →  20 bitów
```

Stąd wzięła się cała pamięć segmentowa DOS-a, `far` i `near` pointery, model pamięci `small`/`medium`/`large` w Turbo Pascalu i wieczne 640 kB. Architektura potrafiła zaadresować więcej pamięci, niż mieściło się w jej własnym rejestrze – i zapłaciła za to dwiema dekadami udręki programistów.

**Dane szersze niż architektura – Intel Pentium.** Programowo to procesor 32-bitowy: rejestry `EAX`–`EDI` mają 32 bity, wskaźnik ma 32 bity, przestrzeń adresowa to 4 GB. Ale zewnętrzna szyna danych ma **64 bity**, bo skoro i tak wypełniamy 32-bajtową linię cache, opłaca się wozić po dwa słowa naraz. Żaden program tego nie widzi. Widzi to tylko benchmark.

### Trzecia szerokość, o której się zapomina: adres fizyczny ≠ wskaźnik

W nowoczesnych systemach z pamięcią wirtualną te dwie liczby to naprawdę dwie różne liczby:

- **Adres wirtualny** – to, co widzi program, szerokość wskaźnika w ABI.
- **Adres fizyczny** – to, co MMU wystawia po translacji na kontroler pamięci.

Klasyczny przykład rozjazdu to **PAE** (Physical Address Extension) na 32-bitowym x86: wskaźnik nadal ma 32 bity, każdy proces widzi maksymalnie 4 GB, ale adres fizyczny ma 36 bitów, więc system operacyjny może obsłużyć **64 GB RAM** i rozdać go wielu procesom. Maszyna z PAE mimo to była i pozostała 32-bitowa – bo bitness dotyczy tego, co widzi program, a nie tego, co widzi kontroler pamięci.

Dziś ten sam rozjazd występuje w drugą stronę. Nominalnie 64-bitowy x86-64 implementuje tylko **48 bitów adresu wirtualnego** (57 przy włączonym 5-poziomowym stronicowaniu, LA57) i typowo 39–46 bitów adresu fizycznego. Górne bity wskaźnika muszą być kopią bitu 47 – to tak zwana postać kanoniczna. Adres `0x0000_1234_5678_9ABC` jest poprawny, a `0x1234_5678_9ABC_DEF0` powoduje wyjątek, choć oba mieszczą się w 64 bitach. Nikt nie ciągnie 64 linii adresowych, bo 256 TB przestrzeni na razie wystarcza, a każdy bit adresu kosztuje krzem w TLB i tablicach stron.

### Co zostało z „szyny" dzisiaj

W literaturze sprzed 30 lat szyna to dosłownie pęk równoległych drutów wspólnych dla wszystkich układów. Współcześnie to abstrakcja:

- **DDR** ma multipleksowane linie adresowe (adres wiersza `RAS`, potem adres kolumny `CAS`), 64-bitową szynę danych na kanał i transferuje **burstami** – zawsze całą 64-bajtową linię cache, nigdy pojedynczy bajt.
- **PCIe, Infinity Fabric, ARM AMBA/CHI** to sieci pakietowe. Adres jest polem w nagłówku pakietu, nie osobnym pękiem przewodów.
- Przepustowość liczysz jako `szerokość × transfery/s × liczba kanałów`, a nie jako „szerokość szyny".

Pojęcie zostało jednak w praktyce inżynierskiej i wraca pod innymi nazwami: linia cache ma 64 bajty, bo tyle wynosi jednostka transferu; wyrównanie (alignment) ma znaczenie, bo odczyt przekraczający granicę transferu kosztuje dwa transfery zamiast jednego (a na ARMv5 czy SPARC potrafił wywalić program); false sharing boli, bo jednostką koherencji jest cała linia, nie zmienna.

## 3. Arytmetyka, czyli co naprawdę daje N-bitowa ALU

Druga połowa pytania: co wynika z tego, że procesor jest N-bitowy, dla samych obliczeń.

**Instrukcja arytmetyczna operuje na operandach o szerokości rejestru.** Dodanie dwóch liczb 64-bitowych na maszynie 64-bitowej to jedna instrukcja. Na maszynie 32-bitowej to co najmniej dwie:

```asm
; long long a + b na 32-bitowym x86 – liczba w parze rejestrów EDX:EAX
add eax, ecx        ; młodsze 32 bity, ustawia flagę przeniesienia (carry)
adc edx, ebx        ; starsze 32 bity + przeniesienie z poprzedniej instrukcji
```

Dodawanie i odejmowanie kosztują więc dwa razy więcej. Mnożenie kosztuje trzy mnożenia i kilka dodawań (schemat szkolny na połówkach). A dzielenie 64/64 na 32-bitowej maszynie nie mieści się już rozsądnie w kilku instrukcjach – kompilator wstawia **wywołanie funkcji bibliotecznej**, w GCC to `__udivdi3` z `libgcc`. Stąd typowa obserwacja: `long long` na 32-bitowej platformie działa, ale dzielenie na nim jest kilkanaście razy wolniejsze niż na 64-bitowej.

Drugi, ważniejszy skutek to **zakres liczb**:

| Szerokość | Zakres bez znaku | Zakres ze znakiem |
|---|---|---|
| 8 bitów | 0 … 255 | −128 … 127 |
| 16 bitów | 0 … 65 535 | −32 768 … 32 767 |
| 32 bity | 0 … ~4,29 mld | −2 147 483 648 … 2 147 483 647 |
| 64 bity | 0 … ~1,8 × 10¹⁹ | ±~9,22 × 10¹⁸ |

Praktyczne konsekwencje tej tabeli to znaczna część historii bugów w naszej branży:

- **Problem roku 2038.** `time_t` jako 32-bitowa liczba ze znakiem, licząca sekundy od 1970, przekręci się **19 stycznia 2038**. Migracja na 64-bitowe `time_t` w Linuksie ciągnęła się latami właśnie dlatego, że zmienia ABI.
- **Pliki powyżej 2 GB.** 32-bitowy `off_t` nie zaadresuje większego pliku – stąd `_FILE_OFFSET_BITS=64`, `open64()` i cały Large File Support.
- **Liczniki.** 32-bitowy licznik bajtów na interfejsie sieciowym przy 10 Gb/s przekręca się co ~3,4 sekundy. Dlatego SNMP dorobiło 64-bitowe liczniki `ifHCInOctets`.
- **Identyfikatory.** `INT` autoincrement w bazie kończy się po 2,1 mld wierszy – z czego regularnie ktoś dowiaduje się produkcyjnie.

Warto od razu odciąć dwa fałszywe skojarzenia:

**Bitness ≠ szerokość zmiennoprzecinkowa.** Koprocesor 8087 dołączany do 16-bitowego 8086 liczył na rejestrach **80-bitowych**. Dzisiejsze rejestry SIMD mają 128 (SSE), 256 (AVX2) lub 512 bitów (AVX-512), a nikt nie nazywa Xeona procesorem 512-bitowym. Jednostka wektorowa to osobna ścieżka danych i osobna szerokość.

**Bitness ≠ typy w języku wysokiego poziomu.** W Javie `int` ma 32 bity, a `long` 64 bity – na każdej platformie, bo specyfikacja JVM tak mówi. Uruchomienie 64-bitowej JVM nie zmienia arytmetyki `int`, zmienia rozmiar wskaźników wewnątrz sterty i maksymalny rozmiar tej sterty. W C jest odwrotnie: to właśnie typy zależą od platformy i stąd cały bałagan z modelami danych (o tym w rozdziale 6).

## 4. Instrukcje – szerokość, która nie ma z tym nic wspólnego

Dla porządku, bo to szósty kandydat na „bitowość", regularnie mylony z resztą. Szerokość kodowania instrukcji jest niezależna od szerokości danych:

- **AArch64 (ARM 64-bitowy)** ma rejestry 64-bitowe, ale **każda instrukcja zajmuje dokładnie 32 bity**. 64-bitowy procesor z 32-bitowymi instrukcjami – i to jest zaleta, nie kompromis, bo dekoder jest prosty i przewidywalny.
- **x86-64** ma instrukcje o długości od 1 do 15 bajtów.
- **AVR (ATmega)** to podręcznikowy przykład, że w jednym układzie żyją naraz różne szyny: 8-bitowe rejestry i 8-bitowa szyna danych, ale 16-bitowe słowo instrukcji na osobnej szynie programu (architektura harwardzka) i 16- lub 22-bitowy licznik rozkazów.

Nikt nigdy nie nazwał ATmegi procesorem 16-bitowym, choć jej instrukcje mają 16 bitów.

## 5. Więc co decyduje o nazwie?

Odpowiedź brzmi: **szerokość rejestrów ogólnego przeznaczenia i operującej na nich ALU, a wraz z nią szerokość wskaźnika widzianego przez program.** Czyli to, co widzi kompilator i co utrwala ABI. Obie szyny są szczegółem implementacyjnym.

Sprawdźmy tę regułę na kontrprzykładach z tabeli z rozdziału 1 – bo dobra definicja to taka, która przechodzi przez trudne przypadki:

- **8088 kontra 8086.** Ta sama architektura programowa, szyny danych 8 i 16 bitów. Ten sam kod maszynowy działa na obu, tylko wolniej na 8088. Skoro program nie potrafi ich rozróżnić inaczej niż stoperem, szyna danych nie może być kryterium. Oba są 16-bitowe.
- **386SX kontra 386DX.** Dokładnie ta sama historia dekadę później: SX miał 16-bitową szynę danych i 24-bitowe adresowanie, żeby dało się go wsadzić na tanie płyty z czasów 286. Oba są 32-bitowe, bo oba mają 32-bitowe rejestry i 32-bitowy model programowy.
- **Pentium.** 64-bitowa szyna danych, a jednak procesor 32-bitowy. Gdyby liczyła się szyna danych, mielibyśmy 64-bitowe komputery już w 1993.
- **6502 i Z80.** 16-bitowe adresowanie, a jednak procesory 8-bitowe. Gdyby liczyło się adresowanie, cała era ośmiobitowców nazywałaby się erą szesnastobitowców.
- **Z80 raz jeszcze.** Wewnętrzna ALU ma cztery bity i wykonuje operację 8-bitową w dwóch przebiegach. Programista widzi 8-bitowe rejestry i 8-bitowe operacje – i to widzenie wygrywa. Podobnie 68000: rejestry 32-bitowe, ALU 16-bitowa, operacje 32-bitowe realizowane w dwóch przebiegach. Motorola sprzedawała go jako „16/32-bit", branża pisała o „16-bitowej erze" (Amiga, Atari ST, Mega Drive), ale kod pisało się jak na maszynę 32-bitową i to on przetrwał – programy z 68000 przenosiły się na w pełni 32-bitowe 68020 bez zmian.
- **PAE.** 36-bitowy adres fizyczny, 64 GB RAM w systemie, a procesor nadal 32-bitowy, bo pojedynczy proces nadal ma 32-bitowy wskaźnik i 4 GB przestrzeni.

Reguła w jednym zdaniu, którą warto zapamiętać:

> **Komputer jest N-bitowy, jeśli jego procesor wykonuje operacje na N-bitowych liczbach całkowitych w pojedynczej instrukcji i adresuje pamięć N-bitowym wskaźnikiem mieszczącym się w jednym rejestrze.**

W praktyce, gdy chcesz sprawdzić bitness maszyny albo procesu, nie patrzysz na płytę główną, tylko na ABI:

```c
sizeof(void*)     // 4 → 32-bit, 8 → 64-bit
```

```bash
uname -m          # x86_64 / aarch64 / i686 / armv7l
getconf LONG_BIT  # 64
file /bin/ls      # ELF 64-bit LSB pie executable, x86-64
```

### Który wymiar jest ważniejszy: adresowanie czy arytmetyka?

Historycznie te dwie rzeczy szły w parze, ale przy każdym przeskoku waga była inna – i warto rozumieć, dlaczego.

Przejścia **8 → 16 → 32 bity** napędzały obie potrzeby naraz. Ośmiobitowiec z zakresem 0–255 to udręka nawet przy zwykłej arytmetyce (dodanie dwóch liczb powyżej 255 wymaga rozbicia na bajty), a 64 kB pamięci ograniczało wszystko. Wygrywało jedno i drugie.

Przejście **32 → 64 bity** napędzało prawie wyłącznie **adresowanie**. 32-bitowa arytmetyka wystarcza do ogromnej większości kodu biznesowego i nadal wystarcza – dlatego `int` w Javie, C# i Rust (`i32` jako domyślny typ literałów) został przy 32 bitach. Ale 4 GB przestrzeni adresowej przestało wystarczać: bazy danych, JVM z dużą stertą, obróbka wideo, mapowanie plików w pamięć. Kiedy AMD wypuściło Opterona w 2003 roku, argumentem sprzedażowym była pamięć, nie arytmetyka. (Pierwszym komercyjnym 64-bitowcem był zresztą MIPS R4000 w 1991, a zaraz po nim DEC Alpha – ale to serwerownie, nie desktop.)

To zresztą jedyny sensowny powód, dla którego można powiedzieć, że adresowanie jest „ważniejsze": zabrakło go pierwsze. Ale odpowiedź na pytanie o nazwę zostaje ta sama: **nazwa idzie za architekturą programową – rejestrem i wskaźnikiem – a nie za szynami.** Szyny decydują o tym, jak szybko maszyna chodzi, nie o tym, czym jest.

Warto też mieć w głowie odporność na marketing, bo ta terminologia była nagminnie naginana w sprzedaży. Atari Jaguar reklamowano jako konsolę „64-bitową", bo miała 64-bitową szynę do pamięci – przy 32-bitowych procesorach. PlayStation 2 sprzedawano jako „128-bitową" ze względu na 128-bitowe rejestry SIMD Emotion Engine, którego rdzeń był 64-bitowym MIPS-em. Kiedy ktoś rzuca liczbą bitów bez podania, czego ona dotyczy, to zwykle znaczy, że wybrał największą liczbę, jaką znalazł w specyfikacji.

## 6. Co z tego wynika w codziennej pracy

Cała ta anatomia ma bardzo konkretne skutki, na które trafiasz co miesiąc.

**Modele danych w C i C++.** To bitness architektury zdecydował, ile bajtów ma `long` – i różne systemy zdecydowały inaczej:

| Model | `int` | `long` | `long long` | wskaźnik | Gdzie |
|---|---|---|---|---|---|
| ILP32 | 4 | 4 | 8 | 4 | 32-bitowy Linux/Windows |
| LP64 | 4 | **8** | 8 | 8 | 64-bitowy Linux, macOS, BSD |
| LLP64 | 4 | **4** | 8 | 8 | 64-bitowy Windows |

Stąd klasyczny bug przy przenoszeniu kodu: `long` na 64-bitowym Windowsie ma 4 bajty, a na Linuksie 8. I stąd zasada, żeby w kodzie przenośnym używać `int64_t`, `size_t`, `uintptr_t` zamiast `long` i nigdy nie zakładać, że wskaźnik zmieści się w `int`.

**Rozmiar wskaźnika kosztuje pamięć i cache.** Przejście na 64 bity podwoiło rozmiar każdego wskaźnika, a struktury danych w językach obiektowych to głównie wskaźniki. Dlatego HotSpot ma **compressed oops**: przy stercie do ~32 GB referencje trzymane są jako 32-bitowe liczby przeskalowane o wyrównanie do 8 bajtów (`adres = base + (oop << 3)`). Praktyczna konsekwencja, którą warto znać: sterta 31 GB potrafi mieścić więcej obiektów niż sterta 33 GB, bo powyżej progu JVM wyłącza kompresję i wszystkie referencje puchną. To jedna z niewielu sytuacji, w których zmniejszenie `-Xmx` zwiększa pojemność.

Z tego samego powodu powstały ABI typu **x32** na Linuksie i `arm64ilp32`: pełny 64-bitowy zestaw instrukcji i rejestrów, ale 32-bitowe wskaźniki. Pomysł logiczny, w praktyce niszowy i dziś praktycznie martwy – koszt utrzymania dodatkowego ABI okazał się większy niż zysk.

**64-bitowy nie znaczy dwa razy szybszy.** Wskaźniki są większe, więc cache mieści mniej. Na x86-64 wygrywa się mimo to, ale z zupełnie innego powodu: tryb 64-bitowy podwoił liczbę rejestrów ogólnego przeznaczenia z 8 do 16 i dorzucił adresowanie względem `RIP`. Zysk bierze się z rejestrów, nie z szerokości. Na innych architekturach, gdzie liczba rejestrów się nie zmieniła, przejście na 64 bity potrafiło kod spowolnić.

**Procesy 32-bitowe na 64-bitowym systemie.** Bitness dotyczy nie tylko sprzętu, ale i każdej warstwy z osobna: procesor, jądro, proces. 64-bitowe jądro spokojnie uruchamia 32-bitowe procesy (WoW64 na Windowsie, `ia32` na Linuksie), każdy w swojej 4 GB piaskownicy. Dlatego 32-bitowa aplikacja nie zaalokuje 5 GB pamięci na maszynie z 64 GB RAM, a błąd `OutOfMemoryError` przy `-Xmx3g` na 32-bitowej JVM nie ma nic wspólnego z ilością RAM w serwerze.

**Wyrównanie i linia cache.** To miejsce, w którym szerokość ścieżki danych wraca do twojego kodu. Struktura ułożona tak, że pole przekracza granicę 64 bajtów, wymaga dwóch transferów zamiast jednego. Dwa wątki piszące do sąsiednich pól tej samej linii cache tłuką się o nią (false sharing) – stąd `@Contended` w JVM i ręczne wyściełanie struktur w kodzie współbieżnym.

## 7. Podsumowanie

Określenie „komputer N-bitowy" nie jest ani marketingiem, ani przypadkiem – jest skrótem od **szerokości architektury programowej**: rejestrów ogólnego przeznaczenia, operującej na nich ALU i wskaźnika, którym adresuje się pamięć. To wielkości, które widzi kompilator i które utrwala ABI, więc zmiana któregokolwiek z nich łamie binaria. Dlatego to one dostały nazwę.

Szyna danych i szyna adresowa to co innego. Szyna danych mówi, **ile bitów przechodzi w jednym transferze** – czysta przepustowość, dla poprawności programu niewidoczna, dla wydajności kluczowa. Szyna adresowa mówi, **ile komórek umiesz w ogóle wskazać** – i bywa węższa (48 bitów w x86-64) albo szersza (20 bitów w 8086, 36 przy PAE) niż rejestry procesora. Obie były w historii dowolnie przycinane, żeby obniżyć koszt układu, i nigdy nie zmieniało to nazwy architektury: 8088 pozostał szesnastobitowy, Pentium trzydziestodwubitowy.

Jeśli miałbym zostawić jedno rozróżnienie, to to: **adres jest pytaniem, dane są odpowiedzią, a bitowość to szerokość szuflady, w której procesor trzyma jedno i drugie.**

**Ściągawka:**

| Pytanie | Co decyduje | Jak sprawdzić |
|---|---|---|
| Ile pamięci zaadresuje proces? | szerokość wskaźnika w ABI | `sizeof(void*)`, `getconf LONG_BIT` |
| Ile pamięci obsłuży system? | szerokość adresu fizycznego | `/proc/cpuinfo` → `address sizes` |
| Jak duże liczby w jednej instrukcji? | szerokość rejestru i ALU | ISA, `long`/`int64_t` w kodzie |
| Ile danych na jeden transfer? | szyna danych, linia cache | 64 B linia; `getconf LEVEL1_DCACHE_LINESIZE` |
| Jak nazywamy tę maszynę? | rejestry + wskaźnik w ISA | `uname -m`, `file <binarka>` |

**Dalsza lektura:**

- Randal Bryant, David O'Hallaron, *Computer Systems: A Programmer's Perspective* – rozdziały 2 i 3 to najlepszy istniejący opis związku między reprezentacją liczb, rejestrem a ABI.
- Intel SDM, tom 1, rozdział o trybie IA-32e – definicja postaci kanonicznej adresu i tego, dlaczego 64-bitowy wskaźnik ma 48 znaczących bitów.
- ARM *Architecture Reference Manual for A-profile*, sekcja o AArch64 – przykład 64-bitowej architektury z 32-bitowym kodowaniem instrukcji.
- Dokumentacja HotSpot do `-XX:+UseCompressedOops` – praktyczny wykład o tym, ile kosztuje szerszy wskaźnik.

**Powiązane notatki:** [[operacje-bitowe]] – kod U2, maski i to, co procesor naprawdę robi z bitami w rejestrze. [[reprezentacja-liczb-w-python]] – co się dzieje, gdy język w ogóle rezygnuje ze stałej szerokości liczby całkowitej.
