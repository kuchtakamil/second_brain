# Znam imię i nazwisko oraz miejsce zmaieszkania pewnego człowieka w Polsce. Jakic

**Data:** 29 lis 2025, 17:05:56 CET

---

**User:**

Znam imię i nazwisko oraz miejsce zmaieszkania pewnego człowieka w Polsce. Jakich narzędzi OSINT mogę użyć aby dowiedzieć się jaki biznes / firmę prowadzi?

---

**Gemini:**

W przypadku prowadzenia dochodzenia OSINT (Open Source Intelligence) na rynku polskim, dysponując imieniem, nazwiskiem i lokalizacją, masz do dyspozycji potężne, scentralizowane rejestry państwowe oraz narzędzia analityczne firm trzecich. Poniżej znajduje się techniczne zestawienie wektorów poszukiwań.

### 1. Rządowe bazy danych (Primary Sources)

To najbardziej wiarygodne źródła danych o strukturze prawnej biznesu w Polsce.

**A. CEIDG (Centralna Ewidencja i Informacja o Działalności Gospodarczej)**
Dla jednoosobowych działalności gospodarczych (JDG) oraz wspólników spółek cywilnych.

- **Zastosowanie:** Wyszukiwarka pozwala na filtrowanie po imieniu, nazwisku oraz adresie (województwo, powiat, gmina, ulica).
- **Dane wyjściowe:** NIP, REGON, adres wykonywania działalności, historia wpisów, zawieszenia, daty rozpoczęcia, kody PKD (Polska Klasyfikacja Działalności).
- **Adres:** `aplikacja.ceidg.gov.pl`

**B. KRS (Krajowy Rejestr Sądowy) – Portal e-KRS**
Dla spółek prawa handlowego (z o.o., akcyjne, komandytowe) oraz stowarzyszeń.

- **Zastosowanie:** Jeśli figurant jest członkiem zarządu, rady nadzorczej lub prokurentem.
- **Technika:** Wyszukiwanie bezpośrednie po nazwisku jest utrudnione w oficjalnej wyszukiwarce MS (wymaga numeru KRS), dlatego należy użyć *agregatorów* (patrz sekcja 2), aby uzyskać numer KRS, a następnie pobrać **Odpis Pełny** z oficjalnej strony.
- **Adres:** `ekrs.ms.gov.pl`

**C. CRBR (Centralny Rejestr Beneficjentów Rzeczywistych)**
Kluczowe narzędzie do deanonimizacji struktur korporacyjnych.

- **Zastosowanie:** Pozwala zidentyfikować osoby fizyczne sprawujące bezpośrednią lub pośrednią kontrolę nad spółką, nawet jeśli nie widnieją w KRS jako zarząd (np. posiadają >25% udziałów).
- **Technika:** Wymaga znajomości NIP-u spółki, który znajdziesz w poprzednich krokach. Jest to kluczowe do weryfikacji powiązań kapitałowych.
- **Adres:** `crbr.podatki.gov.pl`

---

### 2. Agregatory danych i analiza powiązań (Link Analysis)

Narzędzia te indeksują dane z KRS i CEIDG, umożliwiając wyszukiwanie po danych osobowych i wizualizację powiązań (graph analysis).

**A. Rejestr.io (Najbardziej zaawansowane narzędzie dla PL)**

- **Funkcjonalność:** Umożliwia wyszukiwanie po imieniu i nazwisku. Posiada moduł "Powiązania", który rysuje graf powiązań między osobami a podmiotami (kto z kim jest w spółce, w jakich innych podmiotach te osoby występują).
- **Zastosowanie:** Szybkie mapowanie całego ekosystemu biznesowego figuranta.
- **Tip:** Sprawdź zakładkę "Archiwum", aby zobaczyć historyczne powiązania, które zniknęły z bieżących odpisów.

**B. KRS-online / Aleo / Owler**

- **Zastosowanie:** Alternatywne bazy danych. Aleo często indeksuje dane kontaktowe (e-mail, telefon), których nie ma w samym odpisie KRS, a które zostały podane przy rejestracji w katalogach branżowych.

---

### 3. Google Dorking (Zaawansowane operatory wyszukiwania)

Wykorzystaj "Google Hacking" do precyzyjnego wyciągnięcia informacji z indeksu wyszukiwarki.

| Operator / Dork | Zastosowanie |
| --- | --- |
| `site:ceidg.gov.pl "Jan Kowalski"` | Wymusza szukanie tylko w domenie CEIDG (omija interfejs formularza). |
| `site:krs-online.com.pl "Jan Kowalski"` | Szukanie w popularnym serwisie agregującym KRS. |
| `"Jan Kowalski" AND "NIP" AND "Poznań"` | Łączy nazwisko ze słowem kluczowym NIP i miastem. |
| `"Jan Kowalski" AND ("Prezes" OR "Właściciel" OR "Członek Zarządu")` | Szuka powiązań ze stanowiskami biznesowymi. |
| `filetype:pdf "Jan Kowalski" "sprawozdanie"` | Szuka sprawozdań finansowych lub protokołów, gdzie figurant mógł być wymieniony. |
| `intext:"Jan Kowalski" site:linkedin.com` | Głębokie przeszukiwanie profili LinkedIn (często skuteczniejsze niż wewnętrzna wyszukiwarka LinkedIn). |

---

### 4. Geolokalizacja i weryfikacja infrastruktury

Mając adres zamieszkania, możesz zweryfikować, czy pod tym adresem zarejestrowana jest działalność (częsta praktyka w JDG).

- **Google Maps / Street View:** Sprawdź, czy na ogrodzeniu/budynku widnieją tabliczki informacyjne (wymóg prawny dla wielu typów działalności) lub logotypy.
- **Targeo:** Często posiada dokładniejsze dane adresowe dla firm w Polsce niż Google Maps.
- **Geoportal (geoportal.gov.pl):** Pozwala sprawdzić numer działki. Czasami w księgach wieczystych (dostępnych online, jeśli znasz numer KW) właścicielem nieruchomości jest firma, a nie osoba prywatna.

---

### 5. Social Media Intelligence (SOCMINT)

- **LinkedIn:** Sprawdź sekcję "Doświadczenie". Nawet jeśli nie ma tam obecnej firmy, sprawdź sekcję "Działalność" (aktywność, lajki, komentarze) – ludzie często komentują posty z oficjalnych profili swoich firm.
- **Facebook:** Użyj wyszukiwarki, aby znaleźć posty typu "Zapraszam do mojej nowej firmy". Sprawdź sekcję "Informacje -> Praca i wykształcenie".
- **GoldenLine:** Choć platforma traci na znaczeniu, często zawiera "historyczne" wpisy (tzw. digital dust), które zostały usunięte z LinkedIn.

### 6. Weryfikacja techniczna (Gdy znajdziesz potencjalną nazwę firmy)

Jeśli znajdziesz nazwę firmy, ale nie jesteś pewien powiązania:

- **Wyszukiwanie WHOIS:** Sprawdź historię domeny firmowej. Mimo RODO, historyczne rekordy (przed 2018) mogą zawierać imię i nazwisko abonenta. Narzędzia: `domaintools.com`, `whois.domaintools.com`.
- **DNS History:** Jeśli firma ma stronę, sprawdź rekordy SOA w historii DNS – czasami adres e-mail administratora (często właściciela w małych firmach) jest tam widoczny.

Would you like me to construct a specific Google Dork query set tailored to the city and surname provided to narrow down the initial search?