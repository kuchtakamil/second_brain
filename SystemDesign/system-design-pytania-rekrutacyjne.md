# System Design: Pytania Rekrutacyjne

Poniżej znajduje się przekład pięciu popularnych pytań rekrutacyjnych z obszaru System Design, wraz z odpowiedziami przygotowanymi z perspektywy kandydata biorącego udział w rozmowie kwalifikacyjnej. Odpowiedzi celowo zachowują techniczny i doradczy charakter oczekiwany na pozycjach Mid/Senior.

---

## Pytanie 1: Koszty aplikacji z ciężkim przetwarzaniem i kontentem

**Oryginał:** How can we reduce server farm costs for a mobile app that animates children's drawings and downloads interactive environments?  
**Tłumaczenie:** Jak możemy zmniejszyć koszty farmy serwerów dla aplikacji mobilnej, która animuje rysunki dzieci i pobiera interaktywne środowiska?

**Odpowiedź na rozmowie:**  
> "Z architektonicznego punktu widzenia głównym wyzwaniem w takiej aplikacji jest intensywne obciążenie obliczeniowe wideo lub AI (animacja rysunków) oraz duże koszty transferu danych przy serwowaniu statycznego, ciężkiego contentu (interaktywne środowiska). Moje podejście do maksymalnej optymalizacji tych kosztów obejmuje:
> 
> 1. **Offloading na urządzenie klienta (Edge Computing):** Animacji na serwerze unikałbym za wszelką cenę. Nowoczesne tablety mają wbudowane dedykowane czipy AI/GPU. Wykorzystanie np. CoreML (iOS) do renderowania na żywo znacząco odciąży backend, ograniczając konieczność utrzymywania drogich serwerów wyposażonych w GPU.
> 2. **Użycie CDN (Content Delivery Network):** Duże, interaktywne środowiska są idealne do serwowania nie bezpośrednio z naszej aplikacji, a np. ze specjalizujących się w dużym transferze brzegowych serwerów CDN. Zwykle opłaty dostawcy chmurowego (egress traffic) są niebotyczne – cacheowanie przez proxy całkowicie minimalizuje to zjawisko.
> 3. **Inteligentny Caching:** Implementacja precyzyjnego cache'owania lokalnego na urządzeniach zapobiega redundantnemu i wielokrotnemu pobieraniu tego samego świata na aplikacji w momencie, kiedy np. straci się łączność internetową. 
> 4. **Asynchroniczne Job Queues (Instancje pre-emptible/Spot):** Jeśli wciąż musielibyśmy renderować na serwerach z powodu wsparcia starszych generacji tabletów, przeniósłbym te zadania do kolejek komunikatów, używając do przetwarzania "Instancji Przerwanych" używająć Auto-Skalowania. Skutkuje to oszczędnością blisko 75-90% wobec kosztów konwencjonalnych maszyn chmurowych, za cenę nieznacznego opóźnienia zwrotu animacji do klienta."

---

## Pytanie 2: Uniezależnienie się od zawodnych usług zewnętrznych (API)

**Oryginał:** How can we reduce the impact of unreliable third-party APIs with frequent outages on a sports statistics web service?  
**Tłumaczenie:** Jak możemy zmniejszyć wpływ zawodnych zewnętrznych API z częstymi przerwami w działaniu na serwis internetowy ze statystykami sportowymi?

**Odpowiedź na rozmowie:**  
> "Niestabilne strumienie danych stron trzecich to jeden z najczęstszych problemów integracyjno-kaskadowych w chmurze. Aby zapewnić stabilność i wysoką dostępność naszego portalu statystyk, zintegrowałbym następujące wzorce projektowe:
> 
> 1. **Circuit Breaker (Wyłącznik Obwodu):** Kiedy zidentyfikujemy przeciążenie i problemy usługi trzeciej, nasz programowy „obwód” otwiera się – ucinamy wszelkie wysyłki do awaryjnego serwisu. Oszczędzamy nasze wątki oczekujące na time-outy, chroniąc system przed samounieruchomieniem z powodu zewnętrznych opóźnień (cascading failure).
> 2. **Cache w strategii „Stale-while-revalidate”**: Bazując na typie danych (sport), w momencie przerw wyświetlałbym wyniki delikatnie przedawnione z rozproszonej pamięci podręcznej (jak Redis), jednocześnie asynchronicznie próbując dociągnąć świeżą walidację. Użytkownik widzi działającą stronę na bazie starszego contentu i status (np. 'aktualizowanie'), zamiast niedziałającej pustej ramki HTML z 500 server error.
> 3. **Zasady Fallback i inteligentne podejścia z ponawianiem (Retries z Exponential Backoff i Jitter):** Skonfigurowałbym mechanizmy retry z wykładniczym czasem opóźnień między wezwaniami przy błędach, chroniąc m.in serwery strony wznawiającej przed tym by gwałtowny zalew setek requestów po naprawie ("thundering herd") natychmiast nie powalił integracji jeszcze raz.
> 4. **Model PUSH przez worker'a w tle:** Zamiast odpalać zapytania prosto z logiki obsługi usera (gdzie user face to face czeka na API) przeniósłbym by zaciąganie danych odbywało się z użyciem procesów wsadowych pobierających obiekty i uzupełniających naszą, wewnętrzną, stabilną bazę. FrontEnd czytałby tylko nasze, bezpieczne serwery."

---

## Pytanie 3: Estimacja wymagań Capacity (Capacity Planning) dla streamingu

**Oryginał:** What information is required to estimate next year's resource costs for a popular video-sharing app?  
**Tłumaczenie:** Jakie informacje są potrzebne, aby oszacować koszty zasobów na przyszły rok dla popularnej aplikacji do udostępniania wideo?

**Odpowiedź na rozmowie:**  
> "Budowanie niezawodnego rocznego Capacity Planning dla aplikacji typowo streamującej, opartej na odtwarzaniu dużej masie plikowej (video-sharing), determinuje przede wszystkim specyfika generowania wysokiego zużycia zasobów. Do przeprowadzenia budżetowania podzieliłbym zapytania na trzy kluczowe filary modelowania:
> 
> 1. **Szacunki Ingress/Storage (Przechowywanie napływającego materiału):** Potrzebujemy prognozy – w oparciu o trendy historyczne – wielkości nadesłanych dziennie nowych filmów. Musimy brać pod uwagę nie tylko oryginalny narzut wagowy formatów (średni czas i rozdzielczość uploaderów), ale wskaźnik konwersji i transkodowania wideo, po ile replik rzędu SD/HD/4K utworzy program. Rzutuje to radykalnie po ilu Terabajtach w cold i hot-storage chmurowego zamkniemy się per miesiąc.
> 2. **Metryki Ruchu (Przesył wyjściowy/Egress & CDN):** Musimy uzyskać wskaźniki Daily/Monthly Active Users oraz prognozy jak długo per os trwają średnio sesje i jaki bandwidth obciążają. Większość rachunków za hosting dla projektów jak Netflix / YouTube zjada fizyczny koszt pasma wyjściowego podanego do graczy internetowych z centrów brzegowych CDN.
> 3. **Obliczenia – Transkodowanie:** Dane potrzebne z analityki - to zapotrzebowanie obciążeniowe procesów konwertujących i mikroserwisów dostarczających odnośniki wideo (średnica procesów backendu per żądanie R/W - odczyt oraz operacji bazodanowych metadanych filmów).
> 
> Zdobywając te składowe stworzyłbym arkusz matematyczny szacujący przewidywane poziomy ruchu z marginesem błędu na piki sezonowe i w oparciu o to rezerwował z góry długoletnie instancje chmurowe za część standardowych ratalnych cen."

---

## Pytanie 4: Architektura Single vs Multi-Server

**Oryginał:** How would you evaluate the advantages and disadvantages of using multiple servers versus a single dedicated server for hosting a music streaming application that supports various playlists for different activities?  
**Tłumaczenie:** Jak oceniłbyś wady i zalety korzystania z wielu serwerów (architektura rozproszona) w porównaniu z jednym dedykowanym serwerem do hostowania aplikacji do strumieniowego przesyłania muzyki oferującej różne playlisty do różnych aktywności?

**Odpowiedź na rozmowie:**  
> "Rozpoczynanie małego proof of concept jako Single Server ma dużo racjonalnych punktów, ale w realiach aplikacji usługujących przesyłem muzycznym o dużym obciążeniu (Streaming) to ścieżka do ściany technologicznych limitów. Moja ewaluacja tego wyboru wygląda następująco:
> 
> **Pojedynczy dedykowany serwer (Monolithic / Single Machine Architecture)**
> *   *Zalety:* Minimalny nakład operacyjny (nie ma skomplikowanych rurociągów wdrażania), niskie koszty inżynierii procesowej. Rozwiązywanie logów i problemów opiera się na prostym wglądzie na jedną jednostkę - omijamy problemy rozproszonego środowiska.
> *   *Wady:* **Single Point of Failure (SPOF)**. W razie najmniejszej usterki sieciowej, dyskowej lub chmurowej aktualizacji, aplikacja doświadcza czarnej dziury. Skalowanie jest jedynie "w pionie" (lepsze czipy dla jednej fizycznej wnęki o ustalonej z góry granicy i drogocennej stawce skalowalnej), i nie może radzić sobie z globalizacją – puszczanie playlisty do osób po drogiej stronie w Europie stwarza okropne opóźnienia i lag.
> 
> **Wiele serwerów (Distributed, Multi-Server Architecture via Load Balancer)**
> *   *Zalety:* **Wysoka dostępność (High Availability) oraz Fault Tolerancy**. Serwis muzyczny skaluje wdrożenia – jeżeli awaria skasuje grupę serwerów hostującą jedną z playlist aktywności, pozostałe mikro-komponenty w innych miejscach przejmują na siebie request'y a serwis działa dalej niezburzenie bez zaważenia użytkownikom błędami przerwania odtworzeń. Gwarantuje także zrzuciłowanie wdrożeń przez wiele punktów geograficznych skracając czas opóźnień klientom z różnych rejonów geograficznych.
> *   *Wady:* Znacząca i bolesna na początku cena złożoności zarządzaniatej skali. Ekipa inżynierska musi posiadać mocnego DevOpsa utrzymującego środowiska (np. w oparciu o Kubernetes), rozdzielić wdrożenia by były czysto "Bezstanowe" (Stateless logic), zagwarantować spójność replikacji bazy danych po odcięciach oraz udrękę przy monitorowaniu skomplikowanej orkiestracji logowania w architekturze. 
> 
> Aplikacja do streamingu natywnie od początku powinna zrzeszać multi-serwerowe wsparcie load balancerem."

---

## Pytanie 5: Skalowanie IoT na dziesiątki tysięcy automatów 

**Oryginał:** What concerns might arise when designing a payment system for entertainment machines, where players use preloaded game cards and can recharge through cash or credit card, especially given plans to install the system on approximately 125,000 machines next year?  
**Tłumaczenie:** Jakie obawy (trudności) mogą pojawić się podczas projektowania systemu płatności dla maszyn rozrywkowych, w których gracze używają pre-paidowanych (przedpłaconych) kart gier, doładowując je gotówką lub kartą kredytową – w kontekście instalacji rzędu 125 000 urządzeń na całym terytorium?

**Odpowiedź na rozmowie:**  
> "Zarządzanie ogromną flotą ponad stu tysięcy dystansowych instancji fizycznych wyposażonych w portfele klientów i płatności to kolosalne wyzwanie architektoniczne w domenie Internet of Things oraz compliance. Obawy sprowadzają się do trzech wektorów: Konsystencji przy utracie sieci, bezpieczeństwa i spójności floty, a projekt musiałby je skrupulatnie roztrząsnąć z deweloperami:
> 
> 1. **Działanie Offline i Spójność Danych (Network Partitions & Eventual Consistency)**
>    Skala maszyn gwarantuje przebywanie automatów w regionach centrów handlowych bez dedykowanej dobrej sieci komórkowej albo LAN. Główny problem to: Jak zachowa się maszyna przy restarcie bez komunikacji sieciowej, w momencie gdy osoba wkłada banknot? Model płatności pre-paidowych będzie musiał stosować bardzo odporne zasady przechowywania wartości portfela "lokalnego" na kartach czy podbicia serwera oraz zabezpieczający zaufany asynchroniczny log zdarzeń płatniczych po powrotach sieci minimalizujący incydenty podwojonych obciążeń, bądź straconych doładowań żetonów (Double-Spending i Split-Brain problem). Wymagałoby logiki ostatecznej spójności finansowej per maszyna.
> 
> 2. **Rygor Bezpieczeństwa płatności (Compliance & Fraud)**
>     Podpięcie 125 tysięcy systemów terminalowych przyjmujących wrażliwe płatności bankowe (Credit Cards) to ogromne wymaganie implementacyjne spełnienia surowych norm **PCI-DSS**. Urządzenia muszą wspierać lokalną sprzętową detekcję na zabezpieczenie złośliwego osprzętu (tamper-proofing) do czytników, chronioną kryptograficznie autoryzację komunikacji do chmury (End-to-End Encryption) a cała warstwa płatnicza oprogramowania powinna być silnie i czysto odizolowana od kodu standardowej symulacji/gier we wnętrzu samej maszyny w obawie na ewentualne furtki hackerskie (ang. Security Sandbox). Dochodzi zresztą wektor wyłudzeń pre-paidów kartami fizycznymi przez luki w logice.
> 
> 3. **Orkiestracja aktualizacji (Fleet Management & Bricking)**
>     Zastosowanie w pełni poprawnych paczek programowych na tę liczbnosć rozrzuconych instalacji to zmora z perspektywy wdrażania OTA (Over The Air updates). Bug w logice waluty wpuszczony natychmiast na 125 000 maszyn doprowadziłby giganta komercyjnego na straty miliona dolarów w chwilę, bądź zbugował (zjawisko zceglenia 'bricked' maszyn) je na przymus fizycznego i ręcznego restartu obsługowego z portów serwisowych co pogrąży budżet. Aktualizacje musi kontrolować ekstremalnie stabilna i zautomatyzowana machina Canary Deployments i odtwarzania do tyłu (Rollback na stabilnych mniejszych pulach regionalnych po kolei w przypadku padów)."
