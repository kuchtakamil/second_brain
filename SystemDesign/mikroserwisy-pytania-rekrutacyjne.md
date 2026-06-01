# Mikroserwisy: Pytania Rekrutacyjne

Lista pytań na rozmowę kwalifikacyjną z zakresu **architektury mikroserwisowej**. Pytania pogrupowane tematycznie — od fundamentów po zaawansowane wzorce operacyjne. Obejmują poziomy od Mid do Senior/Staff.

---

## 1. Fundamenty i koncepcje

1. Czym jest architektura mikroserwisowa i czym różni się od monolitu?

Architektura mikroserwisowa dzieli system na zestaw małych, niezależnie rozwijanych usług, z których każda odpowiada za konkretną zdolność biznesową. Serwis ma własny kod, cykl wydawniczy, odpowiedzialność operacyjną i najczęściej własny model danych. Komunikacja między serwisami odbywa się przez jawne kontrakty: API synchroniczne, zdarzenia, kolejki lub strumienie.

Monolit to jedna aplikacja wdrażana jako całość. Może być dobrze zaprojektowany modularnie, ale granice modułów są zwykle egzekwowane w kodzie i procesie builda, a nie przez sieć, osobne wdrożenia i osobne bazy danych. W monolicie wywołanie między modułami jest tanie, spójność transakcyjna jest prostsza, a debugowanie łatwiejsze. W mikroserwisach wywołanie między komponentami staje się wywołaniem rozproszonym: może mieć timeout, błąd sieci, częściową niedostępność, retry, duplikaty i opóźnienia.

Najważniejsza różnica nie polega na liczbie repozytoriów ani technologii. Chodzi o niezależność zmian. Mikroserwis ma sens, gdy zespół może zmienić, przetestować, wdrożyć i skalować fragment domeny bez koordynowania całej aplikacji. Jeżeli wszystkie usługi muszą być wdrażane razem, współdzielą jedną bazę i zmiana jednej wymusza zmiany w wielu innych, system jest raczej rozproszonym monolitem niż architekturą mikroserwisową.

2. Jakie są główne zalety i wady mikroserwisów w porównaniu z architekturą monolityczną?

Zalety mikroserwisów:

- Niezależne wdrożenia. Zespół może wypuścić zmianę w jednym obszarze bez deployowania całego systemu.
- Skalowanie wybranych części. Serwis intensywnie używany, na przykład wyszukiwarka lub koszyk, można skalować niezależnie od panelu administracyjnego.
- Lepsze dopasowanie organizacyjne. Zespoły mogą posiadać konkretne zdolności biznesowe end-to-end: kod, dane, deployment i monitoring.
- Izolacja technologiczna. Serwis może używać innej bazy, języka lub biblioteki, jeśli problem tego wymaga.
- Mniejszy blast radius przy dobrze zaprojektowanej izolacji. Awaria jednego serwisu nie musi oznaczać awarii całej aplikacji.

Wady mikroserwisów:

- Duża złożoność operacyjna. Potrzebne są CI/CD, monitoring, logowanie centralne, tracing, service discovery, zarządzanie sekretami, alerting i automatyzacja infrastruktury.
- Trudniejsza spójność danych. Transakcje lokalne są proste, ale procesy przekraczające granice serwisów wymagają sag, zdarzeń, kompensacji i obsługi niespójności tymczasowej.
- Większy koszt testowania. Dochodzą testy kontraktowe, integracyjne, środowiska testowe i ryzyko niezgodności wersji.
- Opóźnienia i błędy sieci. Każde wywołanie zdalne wymaga timeoutów, retry, circuit breakerów i idempotencji.
- Ryzyko rozproszonego monolitu. Jeżeli granice są źle wybrane, system ma koszt mikroserwisów bez ich korzyści.

Praktyczna ocena jest taka: monolit wygrywa prostotą, mikroserwisy wygrywają niezależnością. Mikroserwisy są opłacalne dopiero wtedy, gdy koszt koordynacji w monolicie jest większy niż koszt systemu rozproszonego.

3. Czym jest **Bounded Context** z Domain-Driven Design (DDD) i jak wpływa na granulację mikroserwisów?

Bounded Context to granica, w której dany model domenowy ma jednoznaczne znaczenie. Ten sam termin może znaczyć coś innego w różnych kontekstach. Na przykład `Klient` w kontekście sprzedaży oznacza podmiot składający zamówienia, w księgowości płatnika faktur, a w marketingu odbiorcę kampanii. Próba zrobienia jednego uniwersalnego modelu `Customer` często prowadzi do modelu przeładowanego, pełnego pól opcjonalnych i zależności między zespołami.

Bounded Context pomaga wyznaczać granice mikroserwisów, ponieważ mikroserwis powinien zwykle chronić jeden spójny model domenowy. Nie oznacza to automatycznie zasady jeden bounded context równa się jeden serwis. Czasem jeden kontekst jest za duży i trzeba go podzielić, a czasem kilka małych kontekstów może pozostać w jednym serwisie lub modularnym monolicie. DDD daje język do rozmowy o granicach, ale decyzja musi uwzględniać wolumen zmian, wymagania skalowania, własność zespołów i przepływy danych.

Dobra granulacja oznacza, że serwis ma wysoką spójność wewnętrzną i niskie sprzężenie z innymi. Jeżeli reguły biznesowe często zmieniają się razem, dane są modyfikowane w jednej transakcji, a pojęcia są częścią tego samego języka domeny, zwykle powinny zostać razem. Jeżeli modele mają inne znaczenie, inny cykl życia i inne zespoły właścicielskie, warto rozważyć osobne granice.

4. Na jakiej podstawie decydujesz, gdzie przebiega granica jednego mikroserwisu? Jakie heurystyki stosujesz?

Najpierw patrzę na granice biznesowe, nie techniczne. Serwis powinien reprezentować zdolność biznesową, na przykład płatności, fakturowanie, katalog produktów, realizację zamówienia albo zarządzanie dostawą. Granice typu `UserControllerService`, `DatabaseService` albo `EmailHelperService` zwykle wskazują na podział techniczny, który zwiększa liczbę wywołań bez poprawy autonomii.

Heurystyki:

- Wspólna zmienność. Elementy, które często zmieniają się razem, powinny być razem.
- Własność danych. Serwis powinien być właścicielem danych, które modyfikuje na podstawie własnych reguł biznesowych.
- Spójność transakcyjna. Jeżeli operacje wymagają silnej transakcji ACID, rozdzielenie może być kosztowne.
- Język domenowy. Jeżeli pojęcia mają inne znaczenie w różnych częściach organizacji, to sygnał osobnych bounded contexts.
- Autonomia zespołu. Granica powinna pozwalać zespołowi dostarczać zmianę bez ciągłego czekania na inne zespoły.
- Kierunek zależności. Stabilne, publiczne kontrakty są lepsze niż częste wywołania w obie strony.
- Wymagania niefunkcjonalne. Różne potrzeby skalowania, bezpieczeństwa, dostępności lub retencji danych mogą uzasadniać osobny serwis.

Antywzorcem jest dzielenie według tabel bazy danych albo warstw technicznych. Mikroserwis `OrderService` i `OrderItemService` zwykle nie mają sensu, jeśli `OrderItem` nie żyje niezależnie biznesowo od zamówienia. Zbyt małe serwisy powodują chatty communication, trudne transakcje i duży narzut operacyjny.

5. Kiedy **nie** warto rozdzielać monolitu na mikroserwisy?

Nie warto zaczynać od mikroserwisów, gdy domena jest słabo poznana. Na początku projektu granice często się zmieniają, a rozdzielenie ich przez sieć utrudnia refaktoryzację. Modularny monolit jest wtedy lepszy: pozwala pilnować granic w kodzie, ale nie wymusza kosztu operacyjnego systemu rozproszonego.

Nie warto rozdzielać monolitu, gdy organizacja nie ma dojrzałości operacyjnej. Mikroserwisy wymagają automatycznych wdrożeń, testów kontraktowych, obserwowalności, reagowania na incydenty, zarządzania wersjami API i infrastruktury jako kodu. Bez tego liczba awarii i koszt koordynacji rosną szybciej niż korzyści.

Nie warto też, gdy problemem monolitu nie jest architektura, tylko jakość kodu. Jeżeli aplikacja ma brak testów, przypadkowe zależności, niejasne moduły i brak właścicielstwa, przeniesienie tego do mikroserwisów da ten sam chaos, ale z siecią, brokerem i Kubernetesem. Najpierw trzeba uporządkować moduły, zależności i dane.

Sygnały, że rozdzielanie jest przedwczesne:

- mały zespół i niska równoległość prac,
- niewielki ruch i brak osobnych potrzeb skalowania,
- wymagania silnej spójności w większości operacji,
- brak automatyzacji deployów,
- brak jasnych granic domenowych,
- częste zmiany przekrojowe obejmujące większość systemu.

6. Czym jest wzorzec **Strangler Fig** i jak go zastosować przy migracji z monolitu?

Strangler Fig to wzorzec stopniowej migracji, w którym nowy system przejmuje kolejne funkcje starego monolitu, aż stary kod można usunąć. Nazwa pochodzi od rośliny, która oplata drzewo i z czasem je zastępuje. W praktyce nie przepisuje się całego monolitu od razu. Buduje się nowe komponenty wokół niego i przekierowuje do nich wybrane ścieżki ruchu.

Typowy proces:

- Ustalić granicę funkcji do wydzielenia, najlepiej taką, która ma jasną wartość biznesową i ograniczone zależności.
- Postawić warstwę przekierowania: API Gateway, reverse proxy, routing w aplikacji albo adapter.
- Zbudować nowy serwis z własnym modelem i kontraktem.
- Synchronizować dane tylko tam, gdzie jest to konieczne, najlepiej przez zdarzenia, CDC albo jawne API.
- Przekierować małą część ruchu i porównać wyniki.
- Stopniowo zwiększać zakres, monitorować błędy i usuwać stary kod po przejęciu odpowiedzialności.

Najważniejsze jest ograniczanie ryzyka. Migracja powinna mieć punkty kontrolne, możliwość rollbacku i jasne kryteria zakończenia. Najgorszy wariant to wieloletnia migracja, w której monolit i nowe serwisy dublują logikę, a żaden fragment starego systemu nie jest usuwany.

7. Jakie zasady SOLID mają bezpośrednie przełożenie na projektowanie mikroserwisów?

SOLID dotyczy projektowania obiektowego, ale część zasad dobrze przenosi się na poziom usług.

Single Responsibility Principle oznacza, że serwis powinien mieć jedną spójną odpowiedzialność biznesową. Nie chodzi o jedną klasę ani jedną tabelę, tylko o jeden powód do zmiany. Serwis płatności zmienia się z powodów związanych z autoryzacją płatności, zwrotami, dostawcami płatności i regułami finansowymi, a nie z powodów związanych z prezentacją katalogu produktów.

Open/Closed Principle przekłada się na projektowanie kontraktów, które można rozszerzać bez łamania istniejących klientów. Przykładem jest dodawanie opcjonalnych pól w odpowiedziach, nowych typów zdarzeń albo nowych endpointów zamiast zmiany znaczenia istniejących pól.

Interface Segregation Principle oznacza, że konsumenci nie powinni zależeć od dużych, ogólnych API. Lepiej mieć kontrakty dopasowane do przypadków użycia niż jeden endpoint zwracający pełny obiekt domenowy dla wszystkich. W mikroserwisach duże kontrakty zwiększają sprzężenie, bo każda zmiana modelu zaczyna dotykać wielu klientów.

Dependency Inversion Principle oznacza zależność od kontraktów, nie implementacji. Serwis powinien znać publiczne API innego serwisu, schemat zdarzenia albo kontrakt gRPC, a nie jego wewnętrzne tabele, klasy czy szczegóły wdrożenia.

Liskov Substitution Principle ma mniejsze bezpośrednie zastosowanie na poziomie usług, ale jest istotna przy wersjonowaniu API. Nowa wersja kontraktu nie powinna łamać założeń klientów, którzy poprawnie używali starego kontraktu.

8. Czym różni się **orkiestracja** od **choreografii** w kontekście koordynacji mikroserwisów?

Orkiestracja oznacza, że istnieje centralny koordynator procesu. Na przykład `OrderSagaOrchestrator` mówi: zarezerwuj produkt, pobierz płatność, utwórz wysyłkę, wyślij potwierdzenie. Koordynator zna kolejność kroków, reaguje na błędy i uruchamia kompensacje. Zaletą jest czytelny przebieg procesu i łatwiejsze monitorowanie stanu. Wadą jest ryzyko centralizacji logiki procesu i dodatkowy komponent, od którego zależy przepływ.

Choreografia oznacza, że serwisy reagują na zdarzenia bez centralnego dyrygenta. `OrderCreated` uruchamia rezerwację produktu, `InventoryReserved` uruchamia płatność, `PaymentCaptured` uruchamia wysyłkę. Zaletą jest luźniejsze sprzężenie i naturalne dopasowanie do event-driven architecture. Wadą jest trudniejsza obserwowalność procesu, większe ryzyko ukrytych zależności i trudniejsze zrozumienie całości po samym kodzie jednego serwisu.

Wybór zależy od procesu. Dla długiego, krytycznego przepływu biznesowego z kompensacjami orkiestracja często jest prostsza operacyjnie. Dla niezależnych reakcji na zdarzenie, takich jak wysłanie maila, aktualizacja projekcji czy naliczenie analityki, choreografia jest naturalna.

9. Czym jest **autonomia serwisu** i dlaczego jest kluczowa w architekturze rozproszonej?

Autonomia serwisu oznacza, że serwis może samodzielnie realizować swoją odpowiedzialność biznesową, rozwijać się, wdrażać, skalować i przechowywać dane bez wymagania równoczesnych zmian w wielu innych serwisach. Autonomia nie oznacza braku zależności. Oznacza, że zależności są jawne, stabilne i kontrolowane przez kontrakty.

Autonomiczny serwis:

- posiada własny model danych i nie pozwala innym serwisom zapisywać bezpośrednio do swojej bazy,
- publikuje jasne API lub zdarzenia,
- ma własny pipeline wdrożeniowy,
- ma monitoring, alerty i health checki,
- może obsłużyć awarię zależności przez timeout, retry, fallback albo kolejkę,
- nie wymaga deploymentu lockstep z innymi usługami.

Autonomia jest kluczowa, bo bez niej mikroserwisy tracą główną zaletę. Jeżeli mała zmiana wymaga uzgodnień między pięcioma zespołami, wspólnego release train i ręcznego sprawdzania kompatybilności, architektura jest rozproszona fizycznie, ale sprzężona logicznie. Wtedy koszt sieci i operacji pozostaje, a niezależność dostarczania nie powstaje.

---

## 2. Komunikacja między serwisami

10. Jakie są różnice między komunikacją **synchroniczną** (REST, gRPC) a **asynchroniczną** (message broker)?

Komunikacja synchroniczna oznacza, że klient wysyła żądanie i czeka na odpowiedź. Typowe przykłady to REST over HTTP i gRPC. Ten model jest prosty do zrozumienia, dobrze pasuje do zapytań oraz operacji, w których użytkownik potrzebuje natychmiastowej odpowiedzi. Wadą jest silniejsze sprzężenie czasowe: jeśli serwis zależny jest wolny albo niedostępny, klient odczuwa to bezpośrednio.

Komunikacja asynchroniczna oznacza, że producent publikuje wiadomość lub zdarzenie, a konsument przetwarza je później. Producent nie musi czekać na wykonanie całego procesu. Ten model dobrze działa dla procesów długich, integracji między domenami, zdarzeń biznesowych i wyrównywania obciążenia przez kolejki. Wadą jest większa trudność debugowania, opóźnienia, potrzeba idempotencji i obsługa duplikatów.

Różnice praktyczne:

- Synchronicznie łatwiej zwrócić wynik użytkownikowi, ale trudniej izolować awarie zależności.
- Asynchronicznie łatwiej odseparować serwisy czasowo, ale trudniej pokazać natychmiastowy stan końcowy.
- REST/gRPC wymagają timeoutów, retry i circuit breakerów.
- Broker wymaga obsługi ponawiania, DLQ, kolejności, schematów zdarzeń i semantyki dostarczenia.

Dobry system zwykle używa obu modeli. Zapytanie o szczegóły zamówienia może być synchroniczne, ale proces po złożeniu zamówienia, taki jak rezerwacja, płatność, faktura i mail, często lepiej modelować zdarzeniowo.

11. Kiedy wybrałbyś gRPC zamiast REST i odwrotnie? Jakie są kompromisy?

gRPC wybieram głównie do komunikacji wewnętrznej między serwisami, gdy ważne są wydajność, silnie typowany kontrakt i niskie opóźnienia. gRPC używa zwykle Protocol Buffers, daje generowanie klientów i serwerów, wspiera streaming i dobrze sprawdza się w środowiskach kontrolowanych przez jedną organizację.

REST wybieram dla publicznych API, integracji z zewnętrznymi klientami, prostych CRUD-owych zasobów i sytuacji, w których ważna jest łatwość użycia z przeglądarki, curl, Postmana i standardowych narzędzi HTTP. REST jest powszechnie zrozumiały, dobrze współpracuje z cache HTTP, proxy i dokumentacją OpenAPI.

Kompromisy:

- gRPC ma lepszą typizację i zwykle mniejszy narzut, ale jest mniej wygodny dla prostych integracji publicznych.
- REST jest prostszy operacyjnie na brzegu systemu, ale kontrakty JSON bywają luźniejsze i bardziej podatne na niejawne zmiany.
- gRPC wymaga dobrej dyscypliny przy ewolucji schematów Protobuf.
- REST wymaga dyscypliny przy wersjonowaniu endpointów, kodach statusu, modelu błędów i kompatybilności odpowiedzi.

Przykład decyzji: komunikacja między serwisem koszyka i serwisem cenowym w tym samym klastrze może używać gRPC. Publiczne API dla aplikacji mobilnej albo partnerów biznesowych częściej powinno używać REST lub GraphQL/BFF, zależnie od potrzeb klienta.

12. Czym jest wzorzec **API Gateway** i jakie problemy rozwiązuje?

API Gateway to warstwa wejściowa przed mikroserwisami. Klient nie musi znać adresów wszystkich usług, ich protokołów ani topologii. Gateway przyjmuje ruch z zewnątrz, wykonuje wspólne funkcje techniczne i przekazuje żądania do właściwych serwisów.

Typowe odpowiedzialności:

- routing do usług,
- TLS termination,
- uwierzytelnianie na brzegu,
- rate limiting,
- walidacja podstawowych nagłówków,
- agregacja prostych odpowiedzi,
- transformacja protokołów, na przykład HTTP na gRPC,
- centralne logowanie wejściowego ruchu,
- obsługa CORS,
- ukrywanie wewnętrznej topologii systemu.

Gateway nie powinien stać się miejscem całej logiki biznesowej. Jeżeli zaczyna zawierać reguły zamówień, płatności i promocji, powstaje centralny monolit na brzegu systemu. Dobra praktyka to trzymanie w gatewayu logiki przekrojowej i technicznej, a reguł domenowych w serwisach właścicielskich.

13. Jak działa **service discovery**? Porównaj podejście client-side vs server-side.

Service discovery rozwiązuje problem znajdowania instancji usług w środowisku, w którym instancje pojawiają się, znikają i zmieniają adresy. W mikroserwisach nie powinno się wpisywać na stałe adresu IP konkretnej instancji. Klient powinien odwoływać się do nazwy usługi, a infrastruktura powinna znaleźć zdrową instancję.

W podejściu client-side klient pyta rejestr usług, na przykład Consul, Eureka albo Kubernetes API, dostaje listę instancji i sam wybiera jedną z nich. Klient odpowiada wtedy za load balancing, retry i obsługę niedostępnych instancji. Zaletą jest większa kontrola po stronie klienta. Wadą jest bardziej złożona biblioteka kliencka i konieczność wdrożenia tego mechanizmu w wielu językach.

W podejściu server-side klient wysyła żądanie do stabilnego adresu, na przykład load balancera, Kubernetes Service albo proxy. Warstwa pośrednia wybiera instancję. Zaletą jest prostszy klient i centralizacja routingu. Wadą jest dodatkowy komponent na ścieżce ruchu oraz mniejsza kontrola klienta nad wyborem instancji.

W Kubernetes typowy model jest server-side z perspektywy aplikacji: serwis odwołuje się do DNS typu `orders.default.svc.cluster.local`, a Kubernetes Service kieruje ruch do zdrowych Podów.

14. Czym jest **service mesh** (np. Istio, Linkerd) i jakie problemy komunikacyjne rozwiązuje?

Service mesh to warstwa infrastrukturalna do zarządzania komunikacją service-to-service. Najczęściej działa przez sidecar proxy obok każdej aplikacji albo przez mechanizmy bezsidecarowe w nowszych modelach. Aplikacja wysyła ruch lokalnie, a proxy obsługuje funkcje sieciowe i bezpieczeństwa.

Service mesh rozwiązuje problemy przekrojowe:

- mTLS między serwisami,
- polityki autoryzacji między usługami,
- retry, timeouty i circuit breaking,
- traffic splitting dla canary deployment,
- metryki połączeń,
- distributed tracing na poziomie ruchu,
- kontrola egress,
- spójne reguły routingu bez implementowania ich w każdej aplikacji.

Mesh ma koszt. Dodaje złożoność, opóźnienie, konfigurację i wymaga kompetencji operacyjnych. Nie powinien być pierwszym narzędziem w małym systemie, który nie ma jeszcze problemów z komunikacją między dziesiątkami usług. Jest wartościowy tam, gdzie liczba usług, wymagania bezpieczeństwa i potrzeba kontroli ruchu uzasadniają dodatkową warstwę.

15. Jak zaprojektować **idempotentne** endpointy i dlaczego jest to istotne w systemach rozproszonych?

Operacja idempotentna może zostać wykonana wiele razy, a efekt końcowy pozostaje taki sam jak po jednym wykonaniu. Jest to krytyczne, bo w systemie rozproszonym klient może nie wiedzieć, czy żądanie się udało. Timeout nie oznacza, że operacja nie została wykonana. Retry może więc wysłać to samo żądanie drugi raz.

Techniki projektowania:

- Używać naturalnie idempotentnych metod, gdzie to pasuje. `PUT /users/123/email` ustawiający konkretny adres jest idempotentny, a `POST /payments` tworzący nową płatność zwykle nie jest.
- Stosować `Idempotency-Key` dla operacji tworzących skutki biznesowe. Klient wysyła unikalny klucz, a serwer zapisuje wynik pierwszego przetworzenia i zwraca go przy powtórzeniu.
- Wymuszać unikalne identyfikatory komend, płatności, zamówień lub wiadomości.
- Projektować konsumentów zdarzeń tak, aby zapisywali przetworzone `messageId` albo używali operacji upsert.
- Rozdzielać walidację od skutku ubocznego i zapisywać stan w transakcji lokalnej.

Przykład: klient wysyła żądanie utworzenia płatności z `Idempotency-Key: checkout-123-payment-1`. Serwis płatności zapisuje klucz i wynik. Jeżeli klient ponowi żądanie po timeoutcie, serwis nie pobiera pieniędzy drugi raz, tylko zwraca poprzedni rezultat.

16. Czym jest wzorzec **Backend for Frontend (BFF)** i kiedy go stosować?

Backend for Frontend to osobna warstwa backendowa dopasowana do konkretnego typu klienta, na przykład aplikacji webowej, mobilnej albo panelu administracyjnego. BFF agreguje dane z mikroserwisów i wystawia API wygodne dla danego frontendu.

Stosuję BFF, gdy różne klienty mają różne potrzeby:

- aplikacja mobilna potrzebuje małych odpowiedzi i mniejszej liczby round-tripów,
- web potrzebuje innego kształtu danych,
- panel administracyjny ma inne uprawnienia i widoki,
- publiczne API nie powinno ujawniać wewnętrznych modeli usług,
- frontend nie powinien sam składać danych z wielu mikroserwisów.

BFF zmniejsza sprzężenie frontendu z mikroserwisami. Frontend nie musi znać topologii systemu, a zmiany w usługach wewnętrznych można ukryć w warstwie BFF. Trzeba jednak pilnować, aby BFF nie stał się miejscem duplikacji logiki biznesowej. Powinien orkiestratorować potrzeby prezentacyjne, autoryzację widoków i agregację, ale decyzje domenowe powinny pozostać w serwisach.

17. Jak zarządzać **wersjonowaniem API** w ekosystemie mikroserwisów?

Najlepsza strategia to projektować API tak, aby większość zmian była kompatybilna wstecz. Wersjonowanie powinno być wyjątkiem dla zmian łamiących kontrakt, nie zamiennikiem dyscypliny projektowej.

Zmiany zwykle kompatybilne:

- dodanie opcjonalnego pola w odpowiedzi,
- dodanie nowego endpointu,
- dodanie nowego typu zdarzenia,
- rozszerzenie enum tylko wtedy, gdy konsumenci obsługują nieznane wartości,
- dodanie opcjonalnego pola w schemacie Protobuf z nowym numerem pola.

Zmiany łamiące:

- usunięcie pola,
- zmiana znaczenia pola,
- zmiana typu danych,
- zmiana wymagalności pola,
- zmiana kodów błędów, na których polegają klienci,
- zmiana semantyki operacji.

REST często wersjonuje się przez ścieżkę, na przykład `/v1/orders`, albo przez nagłówek negocjacji treści. Publiczne API częściej korzysta z wersji w URL, bo jest czytelne dla klientów. Wewnętrzne API może używać nagłówków albo kompatybilnej ewolucji bez jawnej wersji. Dla zdarzeń i gRPC ważna jest zgodność schematów oraz reguły ewolucji, na przykład w Schema Registry.

Proces jest równie ważny jak technika. Trzeba mieć właściciela API, dokumentację, testy kontraktowe, okres deprecjacji, telemetrykę użycia starych wersji i jasną komunikację z konsumentami.

18. Czym jest **contract testing** (np. Pact) i jak zapobiega regresji w komunikacji między serwisami?

Contract testing sprawdza, czy dostawca API i konsumenci rozumieją kontrakt w ten sam sposób. Zamiast uruchamiać cały system end-to-end, testuje się oczekiwania na granicy usług. Konsument definiuje, jakich żądań i odpowiedzi potrzebuje, a dostawca weryfikuje, czy jego implementacja spełnia te oczekiwania.

W podejściu consumer-driven contract testing konsument publikuje kontrakt, na przykład Pact. Dostawca uruchamia testy w swoim pipeline i sprawdza, czy nadal obsługuje wymagane przypadki. Jeżeli dostawca zmieni pole, kod statusu albo strukturę odpowiedzi w sposób łamiący klienta, test wykryje regresję przed wdrożeniem.

Korzyści:

- szybsza informacja zwrotna niż pełne E2E,
- wykrywanie niekompatybilnych zmian API,
- dokumentacja faktycznych oczekiwań konsumentów,
- mniejsza potrzeba uruchamiania wszystkich usług w jednym środowisku,
- większa pewność przy niezależnych deployach.

Contract testing nie zastępuje testów integracyjnych ani E2E. Sprawdza kontrakt, ale nie udowadnia, że cały proces biznesowy działa produkcyjnie. Jest szczególnie wartościowy tam, gdzie wiele zespołów rozwija usługi niezależnie i często wdraża zmiany.

---

## 3. Zarządzanie danymi

19. Czym jest wzorzec **Database per Service** i dlaczego jest zalecany w mikroserwisach?

Database per Service oznacza, że każdy mikroserwis jest właścicielem swoich danych i tylko on może je modyfikować bezpośrednio. Inne serwisy komunikują się z nim przez API, komendy lub zdarzenia, a nie przez współdzielone tabele. Baza może być fizycznie osobna albo logicznie wydzielona, ale granica własności musi być jasna.

Ten wzorzec jest zalecany, bo chroni autonomię. Jeżeli kilka serwisów zapisuje do tych samych tabel, nie da się niezależnie zmieniać modelu danych. Każda migracja schematu staje się zmianą globalną. Powstaje ukryte sprzężenie, którego nie widać w API, ale które blokuje deploye i refaktoryzację.

Korzyści:

- serwis może zmieniać swój schemat bez koordynacji z całym systemem,
- reguły integralności są blisko właściciela domeny,
- można dobrać technologię bazy do problemu,
- awarie i obciążenie bazy są lepiej izolowane,
- łatwiej egzekwować odpowiedzialność zespołu za dane.

Koszt jest istotny: zapytania przekrojowe, raportowanie i transakcje między domenami stają się trudniejsze. Trzeba stosować API composition, projekcje, zdarzenia, sagi albo hurtownie danych. Współdzielona baza upraszcza start, ale zwykle niszczy niezależność, dla której wprowadzono mikroserwisy.

20. Jak realizować zapytania wymagające danych z wielu serwisów, skoro każdy ma swoją bazę? Opisz wzorzec **API Composition**.

API Composition polega na tym, że osobny komponent składa odpowiedź z danych pobranych z wielu serwisów. Kompozytorem może być API Gateway, BFF albo dedykowany serwis zapytań. Przykład: ekran szczegółów zamówienia potrzebuje danych z serwisu zamówień, płatności, dostawy i katalogu produktów. Kompozytor wywołuje te usługi i buduje odpowiedź dla klienta.

Zalety:

- nie łamie własności danych,
- jest proste dla niewielkiej liczby zależności,
- pozwala dopasować odpowiedź do potrzeb konkretnego klienta,
- unika replikowania danych, jeśli zapytanie nie jest częste ani ciężkie.

Wady:

- rośnie latency, bo odpowiedź zależy od kilku wywołań,
- trzeba obsłużyć częściowe błędy,
- łatwo stworzyć zbyt dużo ruchu między serwisami,
- kompozytor może stać się miejscem logiki biznesowej,
- trudniej utrzymać stabilny czas odpowiedzi przy wielu zależnościach.

API Composition działa dobrze dla prostych ekranów i małej liczby źródeł. Dla ciężkich raportów, list z filtrowaniem po wielu domenach albo widoków o dużym ruchu lepsze są materializowane projekcje, CQRS albo osobny read model zasilany zdarzeniami.

21. Czym jest wzorzec **CQRS** (Command Query Responsibility Segregation) i kiedy go stosować?

CQRS rozdziela model zapisu od modelu odczytu. Komendy zmieniają stan systemu i przechodzą przez reguły biznesowe. Zapytania nie zmieniają stanu i mogą korzystać z modelu zoptymalizowanego pod czytanie. W prostym systemie oba modele mogą nadal korzystać z tej samej bazy, ale w architekturze mikroserwisowej często tworzy się osobne projekcje odczytowe.

Przykład: serwis zamówień zapisuje zamówienie w modelu domenowym, który pilnuje reguł statusów, płatności i anulowania. Dla ekranu listy zamówień tworzy projekcję zawierającą numer zamówienia, nazwę klienta, kwotę, status płatności i status dostawy. Ta projekcja może być zasilana zdarzeniami z kilku serwisów.

CQRS stosuję, gdy:

- model zapisu i odczytu mają różne potrzeby,
- zapytania są złożone i przekrojowe,
- odczyt ma dużo większy ruch niż zapis,
- trzeba budować szybkie widoki dla UI lub raportowania,
- domena zapisu wymaga ścisłych reguł, a odczyt potrzebuje denormalizacji.

Nie warto stosować CQRS automatycznie. Wprowadza dodatkowe komponenty, synchronizację, opóźnienia i konieczność obsługi niespójności. Dla prostego CRUD-u klasyczny model jest zwykle lepszy.

22. Czym jest **Event Sourcing** i jakie problemy rozwiązuje? Jakie wprowadza?

Event Sourcing oznacza, że źródłem prawdy nie jest aktualny stan rekordu, tylko sekwencja zdarzeń, które do tego stanu doprowadziły. Zamiast zapisywać tylko `order.status = PAID`, zapisujemy zdarzenia: `OrderCreated`, `PaymentAuthorized`, `PaymentCaptured`. Aktualny stan można odtworzyć przez odtworzenie zdarzeń w kolejności.

Rozwiązuje problemy:

- pełna historia zmian jest dostępna z natury modelu,
- można odtworzyć stan z dowolnego momentu,
- łatwiej audytować decyzje biznesowe,
- zdarzenia mogą zasilać projekcje, integracje i analitykę,
- niektóre domeny naturalnie myślą zdarzeniami, na przykład finanse, księgowość, rezerwacje.

Wprowadza problemy:

- trudniejsza ewolucja schematów zdarzeń,
- potrzeba snapshotów dla długich strumieni,
- większa złożoność modelowania,
- trudniejsze usuwanie lub anonimizacja danych osobowych,
- konieczność idempotentnych projekcji,
- debugowanie wymaga rozumienia historii, nie tylko aktualnego rekordu.

Event Sourcing nie oznacza automatycznie Kafki. Event store jest bazą zdarzeń dla agregatu i musi gwarantować poprawną kolejność oraz kontrolę współbieżności. Broker zdarzeń może publikować fakty na zewnątrz, ale nie zawsze powinien być jedynym miejscem przechowywania historii domenowej.

23. Jak zapewnić **spójność danych** między mikroserwisami bez transakcji rozproszonych?

W mikroserwisach unika się transakcji rozproszonych, bo blokują autonomię, są trudne operacyjnie i źle skalują się przy awariach częściowych. Zamiast tego używa się lokalnych transakcji oraz mechanizmów koordynacji procesu.

Techniki:

- Saga. Proces biznesowy składa się z kroków lokalnych i kompensacji.
- Outbox. Serwis zapisuje zmianę danych i zdarzenie w jednej lokalnej transakcji, a osobny proces publikuje zdarzenie do brokera.
- Idempotentni konsumenci. Konsument może przetworzyć duplikat bez podwójnego skutku.
- Eventual consistency. System dopuszcza krótką niespójność między widokami.
- Materializowane projekcje. Dane z kilku serwisów są replikowane do modelu odczytowego.
- Reconciliation. Okresowe procesy porównują stan i naprawiają rozjazdy.

Przykład: po utworzeniu zamówienia serwis zamówień zapisuje `OrderCreated` w outboxie. Publisher publikuje zdarzenie. Serwis płatności pobiera płatność i publikuje `PaymentCaptured`. Serwis zamówień aktualizuje status. Przez krótki czas zamówienie może być `PENDING_PAYMENT`, ale system zna ten stan i umie go pokazać użytkownikowi.

24. Czym jest wzorzec **Saga** i jakie są różnice między sagą opartą na orkiestracji a choreografii?

Saga to sposób realizacji procesu biznesowego obejmującego wiele serwisów bez jednej transakcji rozproszonej. Każdy krok wykonuje lokalną transakcję w swoim serwisie. Jeśli dalszy krok się nie uda, system wykonuje akcje kompensujące dla kroków już zakończonych.

Saga orkiestracyjna ma centralnego koordynatora. Koordynator zna stan procesu, wysyła komendy do serwisów, czeka na odpowiedzi lub zdarzenia i decyduje o następnym kroku. Jest łatwiejsza do monitorowania i debugowania, bo stan procesu jest w jednym miejscu. Pasuje do krytycznych procesów, takich jak zamówienie, płatność i wysyłka.

Saga choreograficzna nie ma centralnego koordynatora. Serwisy publikują zdarzenia i reagują na zdarzenia innych. Jest bardziej luźno sprzężona, ale trudniej zobaczyć cały przepływ. Przy wielu krokach łatwo ukryć logikę procesu w sieci subskrypcji.

Wybór praktyczny: dla prostych reakcji na zdarzenia choreografia jest dobra. Dla procesu z wieloma krokami, kompensacjami, SLA i potrzebą śledzenia stanu orkiestracja zwykle jest bardziej przewidywalna.

25. Jak obsłużyć **kompensację** (rollback) w Sadze, gdy jeden z kroków zakończy się niepowodzeniem?

Kompensacja to biznesowe odwrócenie skutku, a nie techniczny rollback transakcji bazodanowej. Jeżeli płatność została pobrana, kompensacją może być zwrot środków. Jeżeli produkt został zarezerwowany, kompensacją jest zwolnienie rezerwacji. Jeżeli etykieta wysyłkowa została utworzona, kompensacją może być anulowanie przesyłki.

Projektując kompensację, trzeba:

- zdefiniować kompensację dla każdego kroku, który może zostać zatwierdzony,
- zapisywać stan sagi, żeby wiedzieć, które kroki wymagają odwrócenia,
- wykonywać kompensacje idempotentnie,
- obsłużyć sytuację, w której kompensacja też się nie uda,
- mieć retry z backoffem i DLQ lub ręczną interwencję dla przypadków nierozwiązywalnych automatycznie,
- komunikować użytkownikowi stan pośredni, na przykład `CANCELING` albo `REFUND_PENDING`.

Nie każdy krok da się całkowicie odwrócić. Wysłany e-mail nie zostanie cofnięty, można jedynie wysłać korektę. Dlatego kolejność kroków ma znaczenie. Operacje nieodwracalne warto wykonywać jak najpóźniej albo projektować je tak, aby ich skutki były akceptowalne przy awarii późniejszego kroku.

26. Czym jest **eventual consistency** i jak wytłumaczyć ją biznesowi?

Eventual consistency oznacza, że różne części systemu mogą przez krótki czas widzieć różne stany, ale przy braku nowych zmian system dojdzie do spójnego stanu końcowego. To nie jest brak spójności. To świadoma zgoda na opóźnienie propagacji danych między serwisami.

Biznesowi warto tłumaczyć to językiem procesu, nie technologii. Przykład: po kliknięciu "zapłać" zamówienie może przez kilka sekund mieć status `Płatność w toku`. System nie obiecuje, że wszystkie ekrany natychmiast pokażą finalny stan. Obiecuje, że proces jest śledzony, ma stany pośrednie, retry i mechanizmy naprawcze.

Ważne pytania biznesowe:

- Jak długo może trwać niespójność: sekundy, minuty, godziny?
- Które dane muszą być silnie spójne?
- Jak pokazywać użytkownikowi stan pośredni?
- Jakie są konsekwencje podwójnego wykonania albo opóźnienia?
- Kiedy potrzebna jest ręczna interwencja?

Eventual consistency jest akceptowalna, gdy proces biznesowy naturalnie ma etapy. Nie jest akceptowalna tam, gdzie natychmiastowa spójność jest wymogiem regulacyjnym lub bezpieczeństwa, na przykład przy niektórych limitach finansowych. Wtedy granica serwisu albo model transakcyjny muszą to uwzględnić.

27. Czym jest **Change Data Capture (CDC)** i jak narzędzia takie jak Debezium wspierają synchronizację danych?

Change Data Capture to technika przechwytywania zmian z bazy danych i publikowania ich dalej. Zamiast ręcznie dopisywać kod publikujący zdarzenie po każdej zmianie, CDC czyta log transakcyjny bazy, na przykład WAL w PostgreSQL albo binlog w MySQL, i zamienia zmiany na strumień zdarzeń.

Debezium jest popularnym narzędziem CDC. Działa jako connector, który obserwuje log bazy i publikuje zmiany do brokera, najczęściej Kafki. Dzięki temu można zasilać projekcje, cache, wyszukiwarki, hurtownie danych albo inne serwisy.

Zastosowania:

- migracja z monolitu przez publikowanie zmian ze starej bazy,
- budowa read modeli,
- synchronizacja danych do Elasticsearch,
- analityka near-real-time,
- integracje, gdy aplikacja nie ma jeszcze poprawnego outboxa.

Ryzyka:

- zdarzenia techniczne z CDC nie zawsze są dobrymi zdarzeniami domenowymi,
- konsumenci mogą zacząć zależeć od struktury tabel,
- trzeba obsłużyć zmiany schematu,
- trzeba rozumieć kolejność i semantykę transakcji,
- usuwanie danych i dane wrażliwe wymagają ostrożności.

Najbezpieczniejszy wzorzec to często Outbox plus CDC: aplikacja zapisuje zdarzenie domenowe do tabeli outbox w tej samej transakcji co zmianę biznesową, a Debezium publikuje outbox do brokera. Dzięki temu konsumenci dostają zdarzenia domenowe, a publikacja jest odporna na awarię między zapisem do bazy a wysłaniem wiadomości.

---

## 4. Odporność i niezawodność (Resilience)

28. Czym jest wzorzec **Circuit Breaker** i jak zapobiega awariom kaskadowym?

Circuit Breaker chroni system przed ciągłym wywoływaniem zależności, która jest niedostępna albo bardzo wolna. Działa podobnie do bezpiecznika. Gdy liczba błędów, timeoutów albo odrzuconych połączeń przekroczy próg, circuit breaker przechodzi w stan `open` i przez pewien czas od razu odrzuca kolejne wywołania zamiast wysyłać je do uszkodzonego serwisu.

Typowe stany:

- `closed`: ruch przechodzi normalnie, błędy są liczone.
- `open`: wywołania są szybko odrzucane lub kierowane do fallbacku.
- `half-open`: po czasie przerwy przepuszczana jest mała liczba próbnych żądań. Jeśli się udają, obwód wraca do `closed`; jeśli nie, wraca do `open`.

Circuit Breaker zapobiega awariom kaskadowym, bo ogranicza zużycie zasobów przez oczekiwanie na zależność, która i tak nie odpowiada. Bez niego wątki, połączenia HTTP, connection pool i pamięć mogą zostać zajęte przez czekające żądania. Wtedy awaria jednego serwisu przenosi się na serwisy wyżej w łańcuchu.

Ważne jest dobranie progów i timeoutów do charakterystyki usługi. Zbyt agresywny breaker będzie odcinał zdrowy ruch przy krótkich pikach błędów. Zbyt łagodny nie ochroni systemu przed przeciążeniem.

29. Jak działają mechanizmy **retry z exponential backoff i jitter**? Dlaczego sam retry bez backoff jest niebezpieczny?

Retry ponawia operację po błędzie, który może być tymczasowy. Nadaje się do timeoutów, chwilowej niedostępności sieci, błędów `429`, `503` albo konfliktów współbieżności. Nie powinien automatycznie ponawiać błędów walidacji, błędów autoryzacji ani operacji nieidempotentnych bez zabezpieczeń.

Exponential backoff oznacza, że kolejne próby są coraz bardziej oddalone w czasie, na przykład po 100 ms, 200 ms, 400 ms, 800 ms. Dzięki temu zależność ma czas na odzyskanie sprawności. Jitter dodaje losowość do opóźnienia, na przykład zamiast dokładnie 400 ms klient czeka losowo między 300 a 600 ms.

Sam retry bez backoff jest niebezpieczny, bo może wzmocnić awarię. Jeżeli serwis jest przeciążony, a tysiące klientów natychmiast ponawiają żądania, dostaje jeszcze większy ruch. To może zamienić krótką degradację w długą niedostępność. Jitter jest ważny, bo bez losowości klienci mogą synchronizować ponowienia i tworzyć fale ruchu.

Dobre retry ma:

- limit liczby prób,
- całkowity deadline,
- backoff z jitterem,
- rozróżnienie błędów ponawialnych i nieponawialnych,
- idempotencję operacji,
- metryki pokazujące liczbę ponowień.

30. Czym jest wzorzec **Bulkhead** i jak izoluje awarie w systemie?

Bulkhead dzieli zasoby systemu na izolowane pule, żeby awaria jednej części nie zużyła wszystkiego. Nazwa pochodzi od grodzi w statku, ale w praktyce chodzi o izolację techniczną: osobne pule wątków, connection poole, limity równoległości, kolejki albo instancje.

Przykład: serwis agregujący dane woła płatności, katalog i rekomendacje. Jeżeli wszystkie wywołania używają tej samej puli 100 wątków, wolny serwis rekomendacji może zająć całą pulę i zablokować również płatności. Bulkhead polega na tym, że rekomendacje dostają własny limit, na przykład 20 wątków, a płatności osobny. Awaria rekomendacji nie zabiera zasobów krytycznym operacjom.

Poziomy izolacji:

- osobne connection poole dla zależności,
- limity równoległości per endpoint,
- osobne kolejki dla typów zadań,
- osobne Deploymenty dla funkcji krytycznych i niekrytycznych,
- osobne bazy lub repliki dla odczytu i zapisu,
- izolacja tenantów w systemach multi-tenant.

Bulkhead nie usuwa awarii, ale ogranicza jej zasięg. Dobrze działa razem z timeoutami, circuit breakerami i fallbackami.

31. Jak działa **rate limiting** i **throttling**? Jakie algorytmy znasz (Token Bucket, Leaky Bucket, Sliding Window)?

Rate limiting ogranicza liczbę żądań w określonym czasie. Chroni system przed przeciążeniem, nadużyciami i klientami generującymi zbyt duży ruch. Throttling to aktywne spowalnianie lub ograniczanie klienta, często przez opóźnianie żądań albo zwracanie `429 Too Many Requests`.

Popularne algorytmy:

- Token Bucket. Do kubełka wpadają tokeny z określoną szybkością. Każde żądanie zużywa token. Jeśli tokeny są dostępne, żądanie przechodzi. Algorytm pozwala na krótkie bursty, jeśli kubełek wcześniej się napełnił.
- Leaky Bucket. Żądania wypływają ze stałą szybkością. Nadmiar jest kolejkowany albo odrzucany. Dobrze wygładza ruch, ale gorzej obsługuje naturalne krótkie piki.
- Fixed Window. Liczy żądania w stałych oknach czasu, na przykład na minutę. Jest prosty, ale ma problem na granicy okien, gdzie klient może wysłać prawie podwójny limit.
- Sliding Window. Liczy ruch w przesuwającym się oknie, dzięki czemu jest dokładniejszy i mniej podatny na problem granicy okien.

Limity można nakładać per użytkownik, tenant, IP, API key, endpoint albo typ operacji. Dla API publicznego ważne jest zwracanie informacji o limitach, na przykład nagłówków `RateLimit-Remaining` i czasu resetu, oraz projektowanie wyjątków dla klientów wewnętrznych i operacji krytycznych.

32. Czym jest **timeout budget** (deadline propagation) i jak go propagować przez łańcuch wywołań?

Timeout budget to całkowity czas, jaki system ma na obsłużenie żądania, rozdzielony między kolejne kroki. Deadline propagation oznacza przekazywanie pozostałego deadline'u dalej w łańcuchu wywołań. Chodzi o to, żeby serwisy niżej nie wykonywały pracy, której wynik i tak nie zdąży wrócić do klienta.

Przykład: API ma odpowiedzieć w 1000 ms. Gateway zużywa 50 ms, BFF ma 950 ms. BFF woła serwis zamówień i daje mu deadline 700 ms, zostawiając czas na agregację odpowiedzi. Serwis zamówień, wołając płatności, przekazuje już tylko pozostały budżet, na przykład 300 ms.

Bez deadline propagation każdy serwis może mieć własny timeout 1 sekundy. Przy kilku poziomach zależności końcowy czas odpowiedzi może urosnąć do wielu sekund, mimo że klient dawno zrezygnował. To marnuje zasoby i pogarsza przeciążenie.

Implementacyjnie deadline można przekazywać przez:

- nagłówek HTTP z absolutnym czasem zakończenia,
- kontekst gRPC deadline,
- trace context uzupełniony o budżet czasu,
- wewnętrzny request context w aplikacji.

Ważne, żeby propagować absolutny deadline, a nie tylko timeout relatywny. Absolutny deadline jest odporniejszy na opóźnienia i clock drift można ograniczać przez krótkie horyzonty oraz spójny czas w infrastrukturze.

33. Jak zaprojektować system odporny na **thundering herd** po awarii?

Thundering herd występuje, gdy wiele klientów lub procesów jednocześnie próbuje wykonać tę samą operację po awarii, wygaśnięciu cache albo przywróceniu zależności. Przykład: cache dla popularnego produktu wygasa, tysiące żądań jednocześnie trafia do bazy i przeciąża ją.

Techniki ochrony:

- jitter przy retry i odświeżaniu cache,
- request coalescing, czyli tylko jedno odświeżenie danych dla danego klucza, a reszta żądań czeka na wynik,
- stale-while-revalidate, czyli zwracanie starej wartości przez krótki czas i odświeżanie w tle,
- stopniowe przywracanie ruchu po awarii,
- circuit breaker i limity równoległości,
- warm-up cache przed przełączeniem ruchu,
- rozproszone locki z krótkim TTL dla kosztownych rekalkulacji,
- backpressure i kolejki dla prac w tle.

Po restarcie dużej liczby instancji warto unikać sytuacji, w której wszystkie jednocześnie ładują konfigurację, nawiązują połączenia i odświeżają cache. Pomaga losowy opóźniony start, limity połączeń i gotowość (`readiness`) dopiero po rozgrzaniu aplikacji.

34. Czym jest wzorzec **fallback** i jakie strategie degradacji jakości (graceful degradation) stosujesz?

Fallback to alternatywne zachowanie, gdy podstawowa zależność nie działa albo nie mieści się w czasie. Celem nie jest udawanie, że wszystko działa, tylko dostarczenie ograniczonej, ale kontrolowanej funkcjonalności.

Przykłady fallbacków:

- zwrócenie danych z cache,
- pominięcie sekcji rekomendacji na stronie produktu,
- pokazanie ostatnio znanego statusu z informacją o odświeżaniu,
- użycie domyślnej ceny dostawy, jeśli kalkulator dostawy jest niedostępny,
- zapisanie komendy do kolejki zamiast natychmiastowego wykonania,
- przełączenie na prostszy algorytm,
- ograniczenie funkcji niekrytycznych dla części użytkowników.

Dobry fallback musi być jawny biznesowo. Nie można po cichu zaakceptować płatności, jeśli serwis płatności jest niedostępny. Można natomiast przyjąć zamówienie w stanie `PENDING_PAYMENT` i dokończyć płatność później, jeśli biznes akceptuje taki proces.

Graceful degradation wymaga klasyfikacji funkcji. Funkcje krytyczne, takie jak logowanie, płatność albo zapis zamówienia, mają inne wymagania niż rekomendacje, analityka czy personalizacja. System powinien umieć utrzymać ścieżkę krytyczną kosztem funkcji pomocniczych.

35. Jak przetestować odporność systemu? Czym jest **Chaos Engineering** (np. Chaos Monkey)?

Odporność testuje się przez celowe sprawdzanie, jak system zachowuje się przy awariach zależności, opóźnieniach, błędach sieci, restarcie instancji i przeciążeniu. Same testy jednostkowe nie wystarczają, bo wiele problemów odporności ujawnia się dopiero na granicy usług.

Poziomy testowania:

- testy jednostkowe polityk retry, timeoutów i fallbacków,
- testy integracyjne z symulacją błędów zależności,
- testy kontraktowe dla API,
- testy obciążeniowe i soak testy,
- testy awarii brokera, bazy, DNS albo zewnętrznego API,
- game days, czyli kontrolowane ćwiczenia incydentowe,
- chaos experiments na środowisku staging lub produkcji z ograniczonym blast radius.

Chaos Engineering to dyscyplina polegająca na stawianiu hipotez o odporności systemu i celowym wprowadzaniu zakłóceń, żeby je zweryfikować. Przykład hipotezy: "Jeżeli jedna instancja serwisu płatności zostanie zabita, ruch zostanie przejęty przez pozostałe instancje, a współczynnik błędów nie przekroczy 1%". Eksperyment powinien mieć metryki, automatyczne przerwanie przy przekroczeniu progów i ograniczony zakres.

Chaos Monkey to narzędzie spopularyzowane przez Netflix, które losowo wyłącza instancje, żeby wymusić projektowanie systemów odpornych na utratę pojedynczych komponentów. W praktyce chaos testing zaczyna się ostrożnie: od stagingu, pojedynczych usług i znanych scenariuszy, a dopiero potem przechodzi do produkcji.

---

## 5. Deployment i DevOps

36. Jak wygląda pipeline **CI/CD** dla ekosystemu mikroserwisów? Czym różni się od monorepo vs polyrepo?

Pipeline CI/CD dla mikroserwisu powinien pozwalać na niezależne, powtarzalne i bezpieczne wdrożenie jednej usługi. Typowy przepływ obejmuje: build, testy jednostkowe, analizę statyczną, testy kontraktowe, budowę obrazu kontenera, skanowanie podatności, publikację artefaktu, deployment na środowisko testowe, testy integracyjne, promocję na produkcję i monitoring po wdrożeniu.

W mikroserwisach ważne jest, żeby pipeline nie wymagał przebudowy całego systemu dla każdej małej zmiany. Jeżeli zmiana w serwisie płatności wymaga ręcznego deployu katalogu, koszyka i wysyłki, niezależność jest pozorna.

Monorepo:

- cały kod jest w jednym repozytorium,
- łatwiej robić globalne refaktoryzacje,
- łatwiej utrzymać wspólne standardy i narzędzia,
- trzeba mieć dobre wykrywanie zakresu zmian, żeby nie budować wszystkiego,
- ryzykiem jest zbyt łatwe tworzenie zależności między modułami.

Polyrepo:

- każdy serwis ma osobne repozytorium,
- naturalnie wspiera niezależność zespołów i deployów,
- trudniej wykonywać zmiany przekrojowe,
- trudniej utrzymać spójne standardy bez platformy i szablonów,
- wersjonowanie bibliotek wspólnych wymaga większej dyscypliny.

Niezależnie od modelu repozytoriów kluczowe są: automatyzacja, małe releasy, szybki rollback lub roll-forward, testy kontraktowe i obserwowalność po wdrożeniu.

37. Czym jest **konteneryzacja** (Docker) i jak wspiera mikroserwisy?

Konteneryzacja pakuje aplikację razem z jej zależnościami runtime do obrazu, który można uruchomić w przewidywalny sposób na różnych środowiskach. Dockerfile opisuje, jak zbudować obraz, a runtime kontenerowy uruchamia proces z izolacją systemu plików, sieci i zasobów.

W mikroserwisach kontenery pomagają, bo każdy serwis może mieć własne zależności, wersję języka, konfigurację uruchomieniową i cykl wdrożenia. Obraz kontenera staje się artefaktem release'u. Ten sam obraz powinien przejść przez środowiska od testów do produkcji, a różnice powinny wynikać z konfiguracji, nie z przebudowy kodu.

Dobre praktyki:

- małe obrazy bazowe,
- build wieloetapowy,
- uruchamianie jako użytkownik nie-root,
- brak sekretów w obrazie,
- tagowanie obrazów nie tylko `latest`, ale też wersją lub SHA commita,
- health checki,
- szybkie i przewidywalne startowanie procesu,
- logowanie na stdout/stderr.

Kontener nie rozwiązuje automatycznie problemów architektury. Źle zaprojektowany serwis w kontenerze nadal będzie źle zaprojektowany. Konteneryzacja daje standard uruchomienia i wdrożenia, a nie granice domenowe.

38. Jak **Kubernetes** orkiestruje mikroserwisy? Opisz rolę Podów, Deploymentów i Service'ów.

Kubernetes orkiestruje kontenery: uruchamia je na węzłach, pilnuje liczby replik, restartuje po awarii, kieruje ruch, zarządza konfiguracją i umożliwia rolling update. Dla mikroserwisów jest platformą uruchomieniową, która automatyzuje wiele zadań operacyjnych.

Pod to najmniejsza jednostka uruchomieniowa w Kubernetes. Zawiera jeden lub więcej kontenerów współdzielących sieć i wolumeny. Najczęściej jeden Pod zawiera jeden kontener aplikacyjny, a dodatkowe kontenery pojawiają się przy wzorcu sidecar, na przykład proxy service mesh albo agent logujący.

Deployment opisuje pożądany stan aplikacji: jaki obraz uruchomić, ile replik, jakie zasoby, jakie strategie aktualizacji. Deployment zarządza ReplicaSetami i umożliwia rolling update oraz rollback do poprzedniej wersji.

Service daje stabilny adres sieciowy dla grupy Podów. Pody są nietrwałe i mogą mieć zmienne IP, więc klient nie powinien odwoływać się do konkretnego Poda. Service wybiera Pody na podstawie labeli i kieruje do nich ruch. Dla ruchu zewnętrznego często używa się Ingress, Gateway API albo load balancera.

W praktyce Kubernetes nie zastępuje projektowania odporności w aplikacji. Nadal potrzebne są poprawne timeouty, readiness probes, obsługa zamykania procesu, limity zasobów i metryki.

39. Czym jest strategia **Blue-Green Deployment** i jak minimalizuje ryzyko wdrożeń?

Blue-Green Deployment utrzymuje dwa środowiska produkcyjne lub dwie równoległe wersje aplikacji: `blue` i `green`. Jedna wersja obsługuje ruch produkcyjny, a druga jest przygotowywana z nowym wydaniem. Po testach ruch przełącza się z wersji starej na nową.

Zalety:

- szybkie przełączenie na nową wersję,
- prosty rollback przez powrót ruchu na poprzednią wersję,
- możliwość testowania nowej wersji w środowisku bardzo podobnym do produkcji,
- mniejsze ryzyko częściowo wykonanego deploymentu.

Ryzyka i ograniczenia:

- potrzeba podwójnych zasobów na czas wdrożenia,
- migracje bazy muszą być kompatybilne z obiema wersjami,
- długotrwałe połączenia i stan sesji mogą utrudniać przełączenie,
- zewnętrzne efekty uboczne, takie jak wysyłka maili, muszą być kontrolowane podczas testów green.

Blue-Green minimalizuje ryzyko, bo nowa wersja jest uruchomiona przed przejęciem ruchu. Nie eliminuje jednak ryzyka błędów logicznych, które ujawnią się dopiero pod realnym ruchem. Dlatego często łączy się go z testami smoke, monitorowaniem i automatycznym rollbackiem.

40. Czym jest **Canary Deployment** i jak się różni od Blue-Green?

Canary Deployment polega na wypuszczeniu nowej wersji dla małej części ruchu, na przykład 1%, 5%, 25%, a potem stopniowym zwiększaniu udziału, jeśli metryki są dobre. Nazwa pochodzi od historycznej praktyki używania kanarków w kopalniach jako wczesnego sygnału zagrożenia.

Różnica względem Blue-Green:

- Blue-Green zwykle przełącza cały ruch naraz między dwiema wersjami.
- Canary zwiększa ruch stopniowo i pozwala wykryć problemy na małej grupie użytkowników.
- Blue-Green daje prostszy mentalnie rollback.
- Canary daje lepszą kontrolę ryzyka przy zmianach, których nie da się w pełni przetestować syntetycznie.

Canary wymaga dobrych metryk. Trzeba obserwować błędy, latency, saturację, logi, metryki biznesowe i porównanie wersji. Jeżeli patrzymy tylko na status Podów, canary może przepuścić błąd, który technicznie nie zabija aplikacji, ale psuje konwersję albo proces płatności.

W Kubernetes canary można realizować przez service mesh, Ingress controller, progressive delivery narzędziami typu Argo Rollouts lub Flagger, albo ręcznie przez osobne Deploymenty i reguły routingu.

41. Jak realizować **rolling update** bez przestojów (zero-downtime deployment)?

Rolling update stopniowo zastępuje stare instancje nowymi. Zero-downtime wymaga, żeby przez cały czas istniała wystarczająca liczba gotowych instancji, a ruch trafiał tylko do tych, które są faktycznie gotowe.

Warunki:

- aplikacja ma poprawny `readiness probe`, który zgłasza gotowość dopiero po inicjalizacji,
- `liveness probe` nie jest zbyt agresywny i nie restartuje aplikacji podczas chwilowego obciążenia,
- proces obsługuje graceful shutdown,
- po sygnale zakończenia aplikacja przestaje przyjmować nowe żądania i kończy trwające,
- timeouty load balancera i `terminationGracePeriodSeconds` są spójne,
- jest ustawione `maxUnavailable` i `maxSurge`,
- migracje bazy są kompatybilne wstecz i w przód,
- kontrakty API nie łamią starych klientów.

Najczęstszy problem zero-downtime to baza danych. Jeśli nowa wersja wymaga zmiany schematu, migracja powinna być etapowa. Przykład: najpierw dodać nową kolumnę jako opcjonalną, potem wdrożyć aplikację zapisującą oba formaty, potem przepisać stare dane, potem przełączyć odczyt, a dopiero na końcu usunąć stare pole.

Zero-downtime to nie tylko strategia Kubernetes. To kompatybilność wersji, poprawne zamykanie procesów, kontrola ruchu i obserwowalność po wdrożeniu.

42. Czym jest **Infrastructure as Code** (Terraform, Pulumi) i dlaczego jest kluczowe w środowisku mikroserwisowym?

Infrastructure as Code oznacza zarządzanie infrastrukturą przez kod, a nie ręczne klikanie w konsoli. Kod opisuje sieci, klastry, bazy, kolejki, load balancery, uprawnienia, DNS, buckety, alarmy i inne zasoby. Terraform używa deklaratywnych plików konfiguracyjnych i stanu, a Pulumi pozwala definiować infrastrukturę w językach programowania.

IaC jest kluczowe w mikroserwisach, bo liczba zasobów szybko rośnie. Każdy serwis może potrzebować deploymentu, bazy, topiców, kolejek, sekretów, alertów, dashboardów i polityk IAM. Ręczne zarządzanie prowadzi do dryfu konfiguracji, niepowtarzalnych środowisk i trudnych audytów.

Korzyści:

- powtarzalne środowiska,
- code review zmian infrastruktury,
- historia zmian w Git,
- automatyczne tworzenie zasobów dla nowych serwisów,
- łatwiejszy disaster recovery,
- spójne standardy bezpieczeństwa,
- mniejszy drift między staging i produkcją.

IaC wymaga dyscypliny. Trzeba zarządzać stanem, blokadami, sekretami, modułami, uprawnieniami i procesem przeglądu. Sama obecność Terraformu nie gwarantuje jakości, jeśli zmiany nadal są omijane ręcznie w konsoli.

43. Jak zarządzać **konfiguracją** w rozproszonym systemie (Config Server, Consul, Vault)?

Konfiguracja w mikroserwisach powinna być zewnętrzna względem obrazu aplikacji. Ten sam artefakt powinien działać na różnych środowiskach z inną konfiguracją. Konfiguracją są na przykład adresy zależności, limity, feature flagi, nazwy topiców, poziomy logowania i parametry timeoutów. Sekrety, takie jak hasła i klucze API, powinny być traktowane osobno.

Sposoby zarządzania:

- zmienne środowiskowe dla prostych wartości,
- pliki ConfigMap w Kubernetes,
- Spring Cloud Config lub podobny Config Server dla scentralizowanej konfiguracji,
- Consul lub etcd dla konfiguracji dynamicznej i service discovery,
- Vault lub cloud secret manager dla sekretów,
- feature flag platform dla kontrolowanego włączania funkcji.

Dobre praktyki:

- walidować konfigurację przy starcie aplikacji,
- rozróżniać konfigurację jawną i sekrety,
- wersjonować zmiany konfiguracji,
- mieć audyt dostępu do sekretów,
- rotować sekrety,
- nie logować wartości wrażliwych,
- definiować domyślne wartości tylko tam, gdzie są bezpieczne,
- jasno określić, które ustawienia można zmieniać dynamicznie.

Dynamiczna konfiguracja jest przydatna, ale ryzykowna. Zmiana timeoutu albo limitu bez deploymentu może szybko naprawić problem, ale może też natychmiast zepsuć produkcję. Dlatego potrzebne są uprawnienia, historia zmian, testy i możliwość rollbacku konfiguracji.

44. Czym jest wzorzec **Sidecar** i jak jest wykorzystywany np. w Service Mesh?

Sidecar to dodatkowy proces lub kontener uruchomiony obok głównej aplikacji, który rozszerza ją o funkcje techniczne bez zmiany kodu biznesowego. W Kubernetes sidecar zwykle znajduje się w tym samym Podzie co aplikacja, współdzieli z nią sieć i może przechwytywać ruch lokalny.

Przykłady sidecarów:

- proxy service mesh, na przykład Envoy w Istio,
- agent zbierający logi,
- agent metryk,
- synchronizator sekretów,
- lokalny cache lub adapter protokołu,
- proces obsługujący połączenie z zewnętrznym systemem.

W service mesh sidecar proxy przejmuje komunikację przychodzącą i wychodzącą aplikacji. Dzięki temu mesh może zapewnić mTLS, retry, timeouty, routing, telemetrykę i polityki bezpieczeństwa bez implementowania tych funkcji w każdym serwisie. Aplikacja może dalej wykonywać zwykłe wywołanie HTTP, a sidecar zajmuje się warstwą sieciową.

Koszt sidecara to dodatkowe zużycie CPU i pamięci, większa złożoność debugowania oraz kolejny element, który może mieć błędną konfigurację. Sidecar jest dobry dla funkcji przekrojowych, ale nie powinien służyć do ukrywania logiki domenowej poza aplikacją.

---

## 6. Obserwowalność (Observability)

45. Jakie są trzy filary obserwowalności (**logi, metryki, tracing**) i dlaczego wszystkie trzy są konieczne?

Trzy filary obserwowalności to logi, metryki i tracing. Każdy odpowiada na inne pytanie podczas diagnozowania systemu.

Logi pokazują konkretne zdarzenia. Dają szczegóły: jaki użytkownik, jaki identyfikator zamówienia, jaki błąd walidacji, jaka odpowiedź zależności. Są najlepsze do analizy pojedynczego przypadku. W mikroserwisach logi muszą być strukturalne, czyli w formacie łatwym do filtrowania, na przykład JSON. Log tekstowy typu `Something failed` ma małą wartość, jeśli nie zawiera `service`, `traceId`, `requestId`, `userId`, typu błędu i kontekstu biznesowego.

Metryki pokazują zachowanie systemu w czasie. Odpowiadają na pytania: czy rośnie liczba błędów, czy latency przekracza SLO, czy kolejka się zapycha, czy CPU i connection pool są wysycone. Metryki są tanie do agregacji i dobre do alertingu. Nie powiedzą jednak same, dlaczego konkretne żądanie się zepsuło.

Tracing pokazuje przepływ jednego żądania przez wiele usług. Pozwala zobaczyć, że żądanie weszło przez API Gateway, potem przeszło przez BFF, serwis zamówień, płatności i bazę, a opóźnienie powstało w wywołaniu do dostawcy płatności. W systemie mikroserwisowym tracing jest często jedynym sposobem na zrozumienie zależności runtime.

Wszystkie trzy są konieczne, bo pojedynczy filar daje niepełny obraz. Metryka mówi, że `p95 latency` wzrosło. Trace pokazuje, który fragment łańcucha jest wolny. Logi pokazują konkretny błąd, payload techniczny albo decyzję biznesową. Dobra obserwowalność pozwala przejść od alertu do przyczyny bez ręcznego zgadywania topologii systemu.

46. Jak działa **distributed tracing** (np. Jaeger, Zipkin, OpenTelemetry)? Czym jest **trace ID** i **span**?

Distributed tracing śledzi pojedynczą operację przez wiele procesów i usług. Gdy żądanie trafia do systemu, dostaje identyfikator śladu, czyli `trace ID`. Ten identyfikator jest propagowany dalej w nagłówkach HTTP, metadanych gRPC albo wiadomościach z brokera. Każdy serwis tworzy własne fragmenty śladu, czyli `spany`.

`Trace` to pełna historia jednego żądania lub procesu. `Span` to pojedynczy odcinek pracy, na przykład obsługa endpointu `POST /orders`, zapytanie do bazy, wywołanie `PaymentService` albo publikacja zdarzenia do Kafki. Span ma czas startu, czas trwania, nazwę operacji, identyfikator rodzica, status oraz atrybuty, takie jak `http.status_code`, `db.statement`, `messaging.topic` albo `customer.tier`.

Przykład:

- trace ID: całe żądanie złożenia zamówienia,
- span 1: API Gateway przyjmuje `POST /checkout`,
- span 2: BFF waliduje koszyk,
- span 3: Order Service tworzy zamówienie,
- span 4: Payment Service autoryzuje płatność,
- span 5: Kafka publish `OrderCreated`.

Jaeger i Zipkin są systemami do zbierania i wizualizacji trace'ów. OpenTelemetry jest standardem instrumentacji: dostarcza API, SDK i collectory do zbierania trace'ów, metryk i logów niezależnie od konkretnego backendu. Dzięki temu aplikacja może emitować dane w standardowym formacie, a organizacja może zmienić backend observability bez przepisywania kodu instrumentacji.

Ważne jest propagowanie kontekstu przez wszystkie granice: HTTP, gRPC, kolejki i joby asynchroniczne. Jeśli trace ID ginie przy publikacji zdarzenia, proces biznesowy urywa się w narzędziu tracingowym i debugowanie znowu wymaga ręcznego łączenia faktów.

47. Jak implementować **centralne logowanie** w ekosystemie mikroserwisów (ELK Stack, Loki)?

Centralne logowanie oznacza, że logi ze wszystkich usług trafiają do jednego systemu, gdzie można je wyszukiwać, filtrować, korelować i retencjonować. W mikroserwisach nie da się skutecznie diagnozować awarii przez logowanie na pojedyncze instancje, bo Pody są nietrwałe, instancji jest wiele, a żądanie przechodzi przez kilka usług.

Typowy przepływ:

- aplikacja pisze logi strukturalne na stdout/stderr,
- agent na węźle lub sidecar zbiera logi,
- logi trafiają do systemu pośredniego lub bezpośrednio do backendu,
- backend indeksuje albo etykietuje logi,
- użytkownik analizuje je w Kibanie, Grafanie lub innym narzędziu.

ELK Stack to Elasticsearch, Logstash i Kibana. Elasticsearch przechowuje i indeksuje logi, Logstash przetwarza i wzbogaca strumień, Kibana służy do wyszukiwania i wizualizacji. W praktyce często używa się też Filebeat lub Fluent Bit jako agentów.

Loki działa inaczej: indeksuje głównie etykiety, a nie pełną treść logów. Jest przez to tańszy przy dużym wolumenie, ale wymaga rozsądnego projektowania labeli. Etykiety powinny mieć niską lub umiarkowaną kardynalność, na przykład `service`, `namespace`, `environment`, `level`. Nie powinno się robić labela z `userId` albo `requestId`, bo liczba unikalnych wartości eksploduje.

Dobre praktyki:

- logować w JSON,
- zawsze dodawać `timestamp`, `level`, `service`, `environment`, `traceId`, `correlationId`,
- oddzielać komunikat od pól strukturalnych,
- nie logować sekretów, tokenów, haseł i pełnych danych osobowych,
- ustalić retencję zależnie od wartości i kosztu,
- unikać nadmiernego logowania na poziomie `INFO` w gorących ścieżkach,
- logować błędy z typem wyjątku i kontekstem biznesowym.

Centralne logowanie jest użyteczne dopiero wtedy, gdy logi mają wspólny format i wspólne pola korelacyjne. Bez tego narzędzie staje się dużym magazynem tekstu, a nie systemem diagnostycznym.

48. Jak zaprojektować **health checks** i **readiness/liveness probes** w Kubernetes?

Health check powinien odpowiadać na konkretne pytanie operacyjne. W Kubernetes najważniejsze są `readiness probe`, `liveness probe` i czasem `startup probe`.

`Readiness probe` mówi, czy instancja jest gotowa przyjmować ruch. Jeśli readiness zwraca błąd, Kubernetes usuwa Poda z endpointów Service i nie kieruje do niego nowych żądań. Readiness powinien sprawdzać, czy aplikacja zakończyła inicjalizację, ma załadowaną konfigurację, może obsługiwać żądania i nie jest w stanie lokalnego przeciążenia.

`Liveness probe` mówi, czy proces jest żywy, czy trzeba go zrestartować. Powinna wykrywać stany, z których aplikacja sama nie wyjdzie, na przykład deadlock głównego procesu. Liveness nie powinna zależeć od chwilowej niedostępności bazy albo zewnętrznego API. Jeśli liveness sprawdza bazę, awaria bazy może spowodować restart wszystkich Podów, co pogorszy incydent.

`Startup probe` przydaje się dla aplikacji długo startujących. Chroni przed sytuacją, w której liveness zabija aplikację zanim zdąży się poprawnie uruchomić.

Dobre projektowanie:

- osobny endpoint dla readiness i liveness,
- readiness może sprawdzać krytyczne zależności, ale z krótkimi timeoutami,
- liveness powinna być lokalna i tania,
- endpointy health nie powinny wykonywać ciężkich zapytań,
- odpowiedzi powinny być stabilne i szybkie,
- probe powinny mieć sensowne `initialDelaySeconds`, `periodSeconds`, `timeoutSeconds` i `failureThreshold`,
- system powinien rozróżniać degradację od całkowitej niezdolności do obsługi ruchu.

Health check nie zastępuje monitoringu biznesowego. Aplikacja może być `healthy`, a mimo to nie przyjmować płatności z powodu błędnej konfiguracji dostawcy. Dlatego health check jest mechanizmem routingu i restartu, a nie pełnym testem poprawności systemu.

49. Jakie **metryki** (RED: Rate, Errors, Duration / USE: Utilization, Saturation, Errors) monitorujesz w mikroserwisach?

Dla usług request/response stosuję metodę RED:

- Rate: liczba żądań na sekundę, najlepiej per endpoint, metoda i status.
- Errors: liczba i procent błędów, rozdzielone na błędy klienta, serwera, timeouty i błędy zależności.
- Duration: czas odpowiedzi, zwykle percentyle `p50`, `p95`, `p99`, a nie tylko średnia.

RED dobrze odpowiada na pytanie, czy użytkownik doświadcza problemu. Jeżeli `p95` rośnie i rośnie liczba `5xx`, usługa degraduje się z perspektywy klienta.

Dla zasobów stosuję metodę USE:

- Utilization: wykorzystanie zasobu, na przykład CPU, pamięć, dysk, połączenia.
- Saturation: kolejka lub stopień zapchania, na przykład liczba oczekujących requestów, zajętość thread poola, pending messages.
- Errors: błędy zasobu, na przykład błędy dysku, odrzucone połączenia, OOM, connection timeout.

Dla mikroserwisów monitoruję też:

- dependency latency i dependency error rate per zależność,
- retry count i circuit breaker state,
- kolejki: consumer lag, throughput, DLQ count, czas przebywania wiadomości w kolejce,
- bazy: czas zapytań, liczba połączeń, locki, deadlocki, cache hit ratio,
- JVM/CLR/runtime: GC pause, heap, thread count, event loop lag,
- metryki biznesowe: liczba zamówień, płatności, anulowań, rejestracji, nieudanych checkoutów.

Metryki techniczne pokazują stan komponentów, ale metryki biznesowe pokazują, czy system realizuje cel. Można mieć wszystkie Pody zielone i jednocześnie zerową liczbę złożonych zamówień, jeśli błąd dotyczy logiki biznesowej.

50. Jak skonfigurować **alerting** tak, aby unikać alert fatigue, a jednocześnie nie przegapić krytycznych incydentów?

Alert powinien oznaczać problem wymagający działania człowieka. Jeśli alert nie wymaga reakcji, powinien być metryką, dashboardem albo logiem, nie powiadomieniem nocnym. Alert fatigue powstaje, gdy system generuje dużo powiadomień o niskiej wartości, przez co zespół przestaje traktować je poważnie.

Dobre zasady:

- alertować na objawy widoczne dla użytkownika, a nie tylko na przyczyny techniczne,
- używać SLO i error budgetów,
- ustalać progi na podstawie danych historycznych,
- dodawać czas trwania warunku, na przykład błąd musi trwać 5 minut,
- grupować alerty z tej samej awarii,
- definiować severity i ścieżkę eskalacji,
- dołączać runbook, dashboard i właściciela usługi,
- mierzyć jakość alertów po incydentach.

Przykłady dobrych alertów:

- `5xx rate` dla publicznego API przekracza 2% przez 5 minut.
- `p95 latency` checkoutu przekracza SLO przez 10 minut.
- Consumer lag dla krytycznego topicu rośnie przez 15 minut i przekracza próg biznesowy.
- Liczba udanych płatności spada o 80% względem normalnego poziomu.

Przykłady słabszych alertów:

- CPU przekroczyło 80% przez 30 sekund.
- Pojedynczy Pod się zrestartował.
- W logach pojawił się dowolny błąd bez wpływu na użytkownika.

Alerty techniczne są potrzebne, ale powinny wspierać diagnozę lub chronić przed znanym ryzykiem. Najważniejsze alerty powinny wynikać z SLO: dostępności, latency, poprawności i świeżości danych.

51. Czym jest **correlation ID** i jak go propagować przez cały łańcuch wywołań?

Correlation ID to identyfikator pozwalający połączyć logi i zdarzenia związane z jednym żądaniem, procesem albo operacją biznesową. W systemie mikroserwisowym pojedyncza akcja użytkownika generuje logi w wielu usługach. Bez wspólnego identyfikatora trzeba zgadywać, które wpisy należą do tej samej akcji.

Correlation ID powinien powstać na brzegu systemu, na przykład w API Gateway, jeśli klient go nie dostarczył. Następnie powinien być przekazywany dalej:

- w nagłówkach HTTP,
- w metadanych gRPC,
- w wiadomościach brokera,
- w jobach asynchronicznych,
- w logach strukturalnych,
- w kontekście tracingowym.

Warto rozróżnić kilka identyfikatorów:

- `requestId`: identyfikator konkretnego requestu HTTP.
- `correlationId`: identyfikator większej operacji obejmującej wiele requestów lub wiadomości.
- `traceId`: identyfikator trace'a w distributed tracing.
- identyfikator biznesowy: na przykład `orderId`, `paymentId`, `customerId`.

W praktyce `traceId` i `correlationId` bywają tym samym, ale nie zawsze. Trace może dotyczyć technicznego przepływu jednego żądania, a correlation ID może obejmować dłuższy proces asynchroniczny. Najważniejsze, żeby organizacja ustaliła standard nazw nagłówków i konsekwentnie instrumentowała wszystkie serwisy oraz biblioteki klienckie.

---

## 7. Bezpieczeństwo

52. Jak działa **uwierzytelnianie** i **autoryzacja** w architekturze mikroserwisowej?

Uwierzytelnianie odpowiada na pytanie: kim jest podmiot wykonujący żądanie. Podmiotem może być użytkownik, aplikacja mobilna, serwis wewnętrzny, job batchowy albo partner zewnętrzny. Autoryzacja odpowiada na pytanie: czy ten podmiot może wykonać daną operację na danym zasobie.

W mikroserwisach najczęściej uwierzytelnianie użytkownika odbywa się na brzegu systemu: w identity providerze, API Gateway albo BFF. Po poprawnym logowaniu system wystawia token lub sesję. Dalej żądanie przechodzi przez serwisy z informacją o użytkowniku, tenantcie, rolach, uprawnieniach lub claimach.

Autoryzacja nie powinna być wyłącznie globalną kontrolą typu "użytkownik jest zalogowany". Serwis domenowy musi egzekwować reguły dotyczące własnych zasobów. Przykład: gateway może sprawdzić, że użytkownik ma token i rolę `customer`, ale serwis zamówień musi sprawdzić, czy użytkownik ma prawo zobaczyć konkretne `orderId`.

Typowe poziomy kontroli:

- autentykacja na brzegu,
- autoryzacja techniczna dostępu do endpointu,
- autoryzacja domenowa w serwisie właścicielskim,
- autoryzacja service-to-service,
- polityki sieciowe i mTLS,
- audyt operacji wrażliwych.

Największe ryzyko to mylenie autentykacji z autoryzacją. Poprawny token nie oznacza automatycznie prawa do każdego zasobu.

53. Czym jest **OAuth 2.0** i **OpenID Connect**? Jak wpisują się w ekosystem mikroserwisów?

OAuth 2.0 to framework autoryzacji. Pozwala aplikacji uzyskać ograniczony dostęp do zasobów w imieniu użytkownika lub samej aplikacji. OAuth definiuje role, takie jak resource owner, client, authorization server i resource server, oraz przepływy, na przykład Authorization Code Flow z PKCE dla aplikacji użytkownika albo Client Credentials Flow dla komunikacji machine-to-machine.

OpenID Connect jest warstwą tożsamości zbudowaną na OAuth 2.0. Dodaje standardowy sposób uwierzytelniania użytkownika i token `id_token`, który zawiera informacje o tożsamości. OAuth mówi głównie o dostępie do zasobów, a OIDC mówi, kim jest użytkownik.

W mikroserwisach typowy układ wygląda tak:

- Identity Provider, na przykład Keycloak, Auth0, Okta lub Azure AD, uwierzytelnia użytkownika.
- Klient dostaje tokeny.
- API Gateway lub BFF weryfikuje token przy wejściu.
- Serwisy otrzymują kontekst użytkownika albo token z odpowiednimi claimami.
- Serwisy domenowe wykonują autoryzację zasobów.

Dla komunikacji service-to-service często używa się Client Credentials Flow albo mTLS z tożsamością workloadu. Nie należy przekazywać bezrefleksyjnie tokenu użytkownika do wszystkich usług, jeśli nie wszystkie potrzebują pełnego kontekstu. Czasem lepszy jest token wymieniony na węższy zakres uprawnień, czyli token exchange.

54. Jak działa wzorzec **API Gateway jako centralny punkt autoryzacji** vs autoryzacja na poziomie każdego serwisu?

API Gateway jako centralny punkt autoryzacji sprawdza żądanie zanim trafi do usług wewnętrznych. Może weryfikować podpis tokenu, datę ważności, issuer, audience, podstawowe scope'y, limity i dostęp do grup endpointów. To ogranicza duplikację technicznej walidacji w wielu serwisach i odcina niepoprawny ruch wcześnie.

Zalety centralnej kontroli:

- spójne reguły wejściowe,
- mniej powtarzalnego kodu,
- prostsze rate limiting i blokowanie klientów,
- ukrycie usług wewnętrznych przed Internetem,
- jeden punkt egzekwowania części polityk bezpieczeństwa.

Ograniczenie jest zasadnicze: gateway zwykle nie zna pełnej logiki domenowej. Może wiedzieć, że użytkownik ma scope `orders:read`, ale nie powinien sam decydować, czy użytkownik może zobaczyć konkretne zamówienie, jeśli wymaga to reguł domenowych, stanu zamówienia, relacji tenantów albo wyjątków biznesowych.

Autoryzacja w każdym serwisie oznacza, że serwis właścicielski sam sprawdza uprawnienia do swoich zasobów. To jest bezpieczniejsze dla reguł domenowych, ale wymaga bibliotek, standardów i testów, żeby nie powstała niespójność między usługami.

Najlepsza praktyka to model warstwowy:

- gateway weryfikuje tożsamość i podstawowe polityki wejściowe,
- service mesh lub infrastruktura kontroluje, które usługi mogą rozmawiać,
- każdy serwis egzekwuje autoryzację domenową dla własnych operacji.

55. Czym jest **JWT** (JSON Web Token) i jakie są jego zalety oraz ryzyka w komunikacji między serwisami?

JWT to format tokenu zawierający zestaw claimów, zwykle podpisany kryptograficznie. Składa się z nagłówka, payloadu i podpisu. Payload może zawierać takie pola jak `sub`, `iss`, `aud`, `exp`, `scope`, `roles`, `tenantId`. Podpis pozwala odbiorcy sprawdzić, że token nie został zmieniony.

Zalety:

- token można weryfikować lokalnie bez zapytania do centralnego serwera,
- dobrze działa w środowiskach rozproszonych,
- może przenosić kontekst użytkownika i zakres uprawnień,
- jest standardowo obsługiwany przez wiele bibliotek i bramek API,
- pasuje do stateless API.

Ryzyka:

- JWT nie jest domyślnie szyfrowany; payload jest tylko zakodowany Base64URL, więc nie powinien zawierać sekretów ani wrażliwych danych.
- Odwołanie tokenu przed `exp` jest trudniejsze niż w sesji serwerowej.
- Zbyt długi czas życia zwiększa ryzyko nadużycia po wycieku.
- Błędna walidacja `aud`, `iss`, algorytmu podpisu lub klucza może prowadzić do przejęcia dostępu.
- Duży token zwiększa narzut w każdym żądaniu.
- Przenoszenie zbyt wielu ról i uprawnień powoduje problem świeżości danych.

Dobre praktyki:

- krótkie życie access tokenów,
- refresh tokeny tylko tam, gdzie są potrzebne i dobrze chronione,
- walidacja podpisu, `issuer`, `audience`, `expiration`,
- rotacja kluczy przez JWKS,
- minimalny zestaw claimów,
- rozróżnienie tokenów użytkownika i tokenów service-to-service.

56. Jak zarządzać **sekretami** (hasła, klucze API) w rozproszonym systemie (HashiCorp Vault, Kubernetes Secrets)?

Sekrety to dane, których ujawnienie daje dostęp do systemu lub danych: hasła do baz, klucze API, klucze prywatne, tokeny, certyfikaty, connection stringi. W mikroserwisach liczba sekretów szybko rośnie, więc zarządzanie nimi musi być zautomatyzowane.

Zasady:

- nie trzymać sekretów w repozytorium,
- nie umieszczać sekretów w obrazach kontenerów,
- ograniczać dostęp zasadą least privilege,
- rotować sekrety,
- audytować odczyty,
- szyfrować sekrety w spoczynku i w transmisji,
- nie logować sekretów,
- oddzielać sekrety per środowisko i per usługa.

Kubernetes Secrets są natywnym mechanizmem przechowywania sekretów w klastrze. Same w sobie nie są pełnym systemem zarządzania sekretami. Wymagają poprawnej konfiguracji szyfrowania etcd, RBAC, ograniczenia dostępu i często integracji z zewnętrznym secret managerem.

HashiCorp Vault daje centralne zarządzanie sekretami, polityki dostępu, audyt, dynamiczne sekrety i rotację. Dynamiczny sekret do bazy może być wygenerowany dla konkretnej aplikacji na określony czas, zamiast używać jednego stałego hasła przez lata.

W środowiskach chmurowych podobną rolę pełnią AWS Secrets Manager, GCP Secret Manager albo Azure Key Vault. Ważny jest nie wybór konkretnego narzędzia, tylko proces: kto może odczytać sekret, jak długo jest ważny, jak jest rotowany i jak wykrywamy nadużycie.

57. Czym jest zasada **Zero Trust** w kontekście mikroserwisów?

Zero Trust oznacza, że system nie ufa automatycznie żadnemu żądaniu tylko dlatego, że pochodzi z sieci wewnętrznej. Każde żądanie powinno być uwierzytelnione, autoryzowane i obserwowalne. Dawny model zakładał twardą granicę: ruch z Internetu jest niebezpieczny, ruch w sieci prywatnej jest zaufany. W mikroserwisach ten model jest słaby, bo po przejęciu jednej usługi atakujący może poruszać się lateralnie po sieci.

W praktyce Zero Trust obejmuje:

- silną tożsamość użytkowników i usług,
- mTLS między usługami,
- autoryzację service-to-service,
- least privilege dla uprawnień,
- segmentację sieci i Network Policies,
- krótkotrwałe poświadczenia,
- ciągłe logowanie i audyt,
- weryfikację kontekstu, na przykład środowiska, workloadu, tenanta.

Zero Trust nie oznacza braku zaufania do zespołów. Oznacza brak niejawnego zaufania technicznego. Serwis płatności powinien przyjmować żądania tylko od usług, które naprawdę muszą go wołać, i tylko z operacjami, do których mają prawo. Sama obecność w tym samym klastrze Kubernetes nie powinna wystarczyć.

58. Jak zabezpieczyć komunikację między serwisami (**mTLS** — mutual TLS)?

mTLS, czyli mutual TLS, zapewnia szyfrowanie komunikacji i wzajemne uwierzytelnienie obu stron. W zwykłym TLS klient weryfikuje serwer. W mTLS również serwer weryfikuje klienta na podstawie certyfikatu. Dzięki temu usługa wie, z jaką inną usługą rozmawia.

W mikroserwisach mTLS można wdrożyć bezpośrednio w aplikacjach albo przez service mesh. Service mesh, na przykład Istio lub Linkerd, często upraszcza wdrożenie, bo sidecar proxy obsługuje certyfikaty, rotację, szyfrowanie i polityki komunikacji bez zmian w kodzie biznesowym.

Co daje mTLS:

- szyfrowanie ruchu wewnętrznego,
- tożsamość workloadu,
- ograniczenie podszywania się pod usługę,
- podstawę do polityk autoryzacji między usługami,
- lepszą ochronę przy przejęciu części sieci.

Elementy wdrożenia:

- zaufany certificate authority,
- automatyczna rotacja certyfikatów,
- polityki określające, które usługi mogą rozmawiać,
- obserwowalność odrzuconych połączeń,
- plan migracji, bo nagłe wymuszenie mTLS może odciąć starsze usługi.

mTLS nie zastępuje autoryzacji domenowej. Potwierdza, że żądanie pochodzi z konkretnej usługi, ale serwis nadal musi sprawdzić, czy dana operacja jest dozwolona.

59. Jak chronić się przed atakami **SSRF** (Server-Side Request Forgery) w systemie mikroserwisowym?

SSRF polega na zmuszeniu serwera do wykonania żądania do adresu wskazanego przez atakującego. Jest groźny w mikroserwisach, bo serwer ma dostęp do sieci wewnętrznej, metadanych chmurowych, paneli administracyjnych albo usług niedostępnych z Internetu. Atakujący może podać URL, który wygląda niewinnie, ale prowadzi do `localhost`, adresu link-local, metadanych cloud providera albo wewnętrznej usługi.

Ochrona:

- nie wykonywać żądań do dowolnych URL-i podanych przez użytkownika,
- stosować allowlistę hostów i schematów,
- blokować adresy prywatne, loopback, link-local i metadata endpoints,
- rozwiązywać DNS i walidować wynikowy adres IP, nie tylko tekst hosta,
- bronić się przed DNS rebinding,
- ograniczać metody HTTP, nagłówki i przekierowania,
- ustawiać krótkie timeouty i limit rozmiaru odpowiedzi,
- używać egress proxy z politykami,
- blokować dostęp do metadanych chmurowych lub wymagać bezpiecznej wersji protokołu, na przykład IMDSv2 w AWS,
- segmentować sieć, żeby pojedyncza usługa nie miała dostępu do wszystkiego.

Przykład ryzyka: funkcja "pobierz obrazek z URL" może zostać użyta do żądania `http://169.254.169.254/...` i odczytu metadanych instancji. Poprawna implementacja nie ufa URL-owi, tylko przepuszcza go przez walidator, allowlistę, egress policy i limity wykonania.

---

## 8. Skalowalność i wydajność

60. Jak **skalować mikroserwisy horyzontalnie** i jakie warunki musi spełniać serwis, aby to było możliwe?

Skalowanie horyzontalne oznacza dodawanie kolejnych instancji usługi zamiast powiększania jednej maszyny. W Kubernetes najczęściej oznacza zwiększenie liczby replik Podów za Deploymentem. Load balancer lub Service rozdziela ruch między instancje.

Warunki:

- serwis powinien być stateless albo trzymać stan poza procesem,
- każda instancja powinna być równoważna,
- operacje powinny być idempotentne tam, gdzie występują retry,
- połączenia do baz i zależności muszą mieć limity, żeby więcej replik nie przeciążyło backendu,
- aplikacja musi mieć poprawne readiness i graceful shutdown,
- dane sesji, cache i locki muszą być zaprojektowane dla wielu instancji,
- background joby nie mogą wykonywać tej samej pracy wielokrotnie bez koordynacji,
- serwis musi emitować metryki pozwalające ocenić, czy skalowanie pomaga.

Skalowanie aplikacji nie rozwiązuje automatycznie wąskich gardeł niżej. Jeśli każda nowa replika otwiera 50 połączeń do bazy, zwiększenie replik z 10 do 100 może zabić bazę. Dlatego skalowanie trzeba analizować end-to-end: aplikacja, baza, broker, zewnętrzne API, sieć, limity rate limiting i koszty.

61. Czym jest zasada **statelessness** i dlaczego jest kluczowa dla skalowalności?

Statelessness oznacza, że instancja serwisu nie przechowuje lokalnie stanu potrzebnego do obsługi przyszłych żądań. Każde żądanie zawiera potrzebny kontekst albo serwis pobiera go z zewnętrznego trwałego magazynu, na przykład bazy, cache rozproszonego albo systemu sesji.

Statelessness jest kluczowe, bo pozwala dowolnej instancji obsłużyć dowolne żądanie. Load balancer nie musi pamiętać, że użytkownik ma trafiać na konkretny Pod. Instancję można zrestartować, zastąpić, wyskalować i przenieść bez utraty stanu biznesowego.

Przykłady stanu, którego nie warto trzymać wyłącznie w procesie:

- sesja użytkownika,
- koszyk,
- postęp procesu płatności,
- lock biznesowy,
- offset przetwarzania,
- dane wymagane po restarcie.

Nie znaczy to, że aplikacja nie może mieć żadnej pamięci lokalnej. Może mieć lokalny cache, connection pool albo tymczasowe bufory, ale system musi działać poprawnie po utracie tej instancji. Lokalny cache jest optymalizacją, nie źródłem prawdy.

Sticky sessions są czasem używane, ale utrudniają autoscaling, rolling update i odporność. Lepiej projektować serwis tak, aby sesja była przechowywana poza instancją lub zakodowana w bezpiecznym tokenie, jeśli pasuje to do przypadku użycia.

62. Jak działa **auto-scaling** (HPA w Kubernetes) i jakie metryki są najlepsze do wyzwalania skalowania?

Horizontal Pod Autoscaler w Kubernetes automatycznie zmienia liczbę replik Deploymentu, StatefulSetu albo podobnego zasobu na podstawie metryk. HPA cyklicznie odczytuje metryki, porównuje je z celem i wylicza pożądaną liczbę replik.

Najprostszy przykład to skalowanie po CPU: jeśli średnie CPU przekracza 70%, HPA dodaje repliki. To działa dla aplikacji CPU-bound, ale jest słabe dla usług, które czekają na I/O, bazę, kolejkę albo zewnętrzne API. Wtedy CPU może być niskie, a latency wysokie.

Lepsze metryki zależą od charakteru usługi:

- request rate per Pod,
- `p95` latency, ostrożnie, bo latency bywa skutkiem problemu zależności, a nie braku replik,
- liczba żądań w kolejce,
- consumer lag w Kafka,
- liczba wiadomości w kolejce,
- aktywne połączenia,
- saturacja thread poola albo event loop lag,
- metryki biznesowe, jeśli dają stabilny sygnał obciążenia.

Dobre autoskalowanie wymaga:

- ustawionych requestów i limitów zasobów,
- sensownych `minReplicas` i `maxReplicas`,
- stabilizacji scale down, żeby uniknąć flappingu,
- uwzględnienia czasu startu aplikacji,
- gotowości zależności na większy ruch,
- testów obciążeniowych.

Autoscaling nie jest mechanizmem ratunkowym dla nagłego nieskończonego ruchu. Ma opóźnienie: metryka musi wzrosnąć, HPA musi zareagować, scheduler musi uruchomić Pody, aplikacja musi wystartować i przejść readiness. Dla ostrych pików potrzebne są też cache, limity, kolejki i zapas pojemności.

63. Jak zaprojektować efektywne **cache'owanie** w architekturze mikroserwisowej (local cache vs distributed cache)?

Cache zmniejsza latency, koszt i obciążenie zależności przez przechowywanie wyniku bliżej klienta lub usługi. W mikroserwisach cache trzeba projektować razem z własnością danych i spójnością. Najważniejsze pytania to: co cache'ujemy, na jak długo, jak unieważniamy, czy możemy zwrócić starą wartość i co jest źródłem prawdy.

Local cache znajduje się w pamięci instancji aplikacji. Jest bardzo szybki i prosty, ale każda instancja ma własną kopię. Po wdrożeniu, restarcie lub zmianie danych cache może być pusty albo niespójny między instancjami. Nadaje się do danych mało zmiennych, konfiguracji, słowników, wyników drogich obliczeń i krótkich TTL.

Distributed cache, na przykład Redis albo Memcached, jest współdzielony przez wiele instancji. Ułatwia spójniejsze cache'owanie, sesje i rate limiting. Ma większe opóźnienie niż pamięć lokalna i sam staje się zależnością, którą trzeba monitorować, skalować i zabezpieczyć.

Strategie:

- cache-aside: aplikacja najpierw sprawdza cache, przy braku pobiera z bazy i zapisuje do cache,
- write-through: zapis przechodzi przez cache do bazy,
- write-behind: zapis trafia do cache i później do bazy, co zwiększa ryzyko utraty danych,
- read-through: cache sam ładuje dane przez skonfigurowany loader,
- stale-while-revalidate: zwracamy starą wartość i odświeżamy w tle.

Dobre cache'owanie wymaga ochrony przed cache stampede, kontrolowania kardynalności kluczy, metryk hit ratio, latency cache i fallbacku przy awarii cache. Cache nie powinien być jedynym miejscem przechowywania danych krytycznych, jeśli nie został zaprojektowany jako trwały system danych.

64. Czym jest **cache invalidation** i dlaczego jest to „jeden z dwóch najtrudniejszych problemów w informatyce"?

Cache invalidation to proces usuwania lub odświeżania danych w cache po zmianie źródła prawdy. Jest trudny, bo trzeba pogodzić świeżość, wydajność, koszt i odporność. Zbyt agresywne unieważnianie zmniejsza korzyść z cache. Zbyt luźne unieważnianie pokazuje użytkownikowi stare albo błędne dane.

Typowe strategie:

- TTL: wpis wygasa po czasie. Proste, ale dopuszcza starość danych do końca TTL.
- Explicit invalidation: serwis po zmianie usuwa konkretny klucz. Wymaga znajomości wszystkich zależnych kluczy.
- Event-based invalidation: zmiana publikuje zdarzenie, konsumenci odświeżają lub usuwają cache.
- Versioned keys: klucz zawiera wersję danych, więc nowa wersja naturalnie omija stary wpis.
- Write-through: cache aktualizuje się przy zapisie.

Problemy:

- jedno zdarzenie biznesowe może wpływać na wiele kluczy,
- konsumenci mogą przegapić zdarzenie unieważnienia,
- cache lokalne w wielu instancjach wymagają osobnego odświeżenia,
- równoległe zapisy mogą przywrócić starą wartość,
- usuwanie całych prefiksów bywa kosztowne,
- brak cache może spowodować nagły wzrost ruchu do bazy.

Dlatego trzeba określić tolerancję na stare dane. Cena produktu w checkoutcie wymaga większej świeżości niż lista popularnych produktów na stronie głównej. Dla danych krytycznych warto sprawdzać źródło prawdy w momencie decyzji biznesowej, nawet jeśli wcześniejszy widok korzystał z cache.

65. Jak zaprojektować system obsługujący **10x lub 100x wzrost ruchu** (capacity planning)?

Capacity planning zaczyna się od zrozumienia obecnego ruchu i ograniczeń. Trzeba znać request rate, latency, wykorzystanie CPU, pamięci, bazy, brokera, zewnętrznych API, koszt jednego żądania i sezonowość. Dopiero potem można modelować wzrost 10x lub 100x.

Kroki:

- ustalić SLO, na przykład dostępność i latency,
- zmierzyć obecny baseline,
- znaleźć wąskie gardła testami obciążeniowymi,
- rozdzielić ścieżki krytyczne od niekrytycznych,
- ocenić limity baz, brokerów, cache, sieci i dostawców zewnętrznych,
- zaprojektować skalowanie aplikacji i danych,
- dodać mechanizmy ochronne: rate limiting, backpressure, kolejki, circuit breakery,
- przygotować plan kosztów,
- przetestować scenariusze awarii przy wysokim ruchu.

Przy wzroście 10x często wystarczy horyzontalne skalowanie aplikacji, optymalizacja zapytań, cache i zwiększenie pojemności bazy. Przy 100x zwykle trzeba zmienić architekturę: partycjonować dane, użyć asynchronicznego przetwarzania, oddzielić odczyt od zapisu, denormalizować read modele, stosować CDN i ograniczać operacje synchroniczne.

Ważne jest projektowanie degradacji. System przy ruchu większym niż planowany powinien odrzucać lub opóźniać mniej ważne operacje, zamiast upaść w całości. Przykład: rekomendacje i analityka mogą być wyłączone, ale checkout powinien dostać priorytet zasobów.

66. Czym jest **backpressure** i jak go zaimplementować w systemie opartym na kolejkach komunikatów?

Backpressure to mechanizm informowania producentów albo warstwy wejściowej, że system nie nadąża z przetwarzaniem. Bez backpressure kolejki rosną bez kontroli, opóźnienia stają się ogromne, a system może zużyć pamięć, dysk albo limity brokera.

W systemie kolejkowym backpressure można zaimplementować przez:

- limity wielkości kolejki,
- kontrolę tempa produkcji,
- odrzucanie lub opóźnianie nowych zadań,
- pause/resume konsumentów,
- skalowanie konsumentów na podstawie lag,
- priorytety kolejek,
- dead letter queue dla wiadomości trwale błędnych,
- retry z opóźnieniem zamiast natychmiastowego ponawiania,
- limity równoległości po stronie konsumenta,
- informowanie API, że operacja zostanie przyjęta później albo jest chwilowo niedostępna.

Przykład: API przyjmuje zadania eksportu raportów do kolejki. Jeśli kolejka przekroczy próg, API może zwrócić `429` albo przyjąć zadanie z dłuższym ETA. Konsumenci przetwarzają zadania z limitem równoległości, a błędne wiadomości po kilku próbach trafiają do DLQ.

Backpressure powinien być świadomy biznesowo. Nie wszystkie wiadomości mają tę samą ważność. Płatności i zamówienia mogą mieć priorytet nad analityką albo wysyłką maili marketingowych.

67. Jak wykorzystać **sharding** i **partycjonowanie** do skalowania warstwy danych?

Partycjonowanie dzieli dane wewnątrz jednej bazy lub klastra na mniejsze części, na przykład według czasu, tenanta, regionu albo identyfikatora. Sharding rozkłada dane na wiele niezależnych shardów, często na osobnych węzłach lub klastrach. Celem jest zmniejszenie rozmiaru pojedynczego zbioru danych, rozłożenie obciążenia i umożliwienie równoległego skalowania.

Partycjonowanie według czasu dobrze pasuje do logów, zdarzeń, transakcji i danych historycznych. Ułatwia usuwanie starych danych i zapytania po zakresie czasu. Partycjonowanie według tenanta pasuje do SaaS, jeśli tenant jest naturalną granicą izolacji. Partycjonowanie hashem po ID daje równomierny rozkład, ale utrudnia zapytania zakresowe.

Sharding wymaga wyboru shard key. Dobry shard key:

- równomiernie rozkłada dane,
- jest znany przy większości zapytań,
- minimalizuje zapytania między shardami,
- nie tworzy hot shardów,
- pasuje do wzorców dostępu.

Problemy:

- transakcje między shardami są trudne,
- zapytania przekrojowe wymagają fan-out albo osobnych projekcji,
- migracja danych między shardami jest skomplikowana,
- hot tenant może przeciążyć jeden shard,
- zmiana shard key później jest bardzo kosztowna.

Sharding powinien być decyzją wynikającą z realnych limitów, nie domyślnym wyborem. Najpierw warto wykorzystać indeksy, optymalizację zapytań, read replicas, cache, archiwizację i partycjonowanie. Sharding daje skalę, ale zwiększa złożoność operacyjną i aplikacyjną.

---

## 9. Event-Driven Architecture

68. Czym jest architektura **zdarzeniowa** (Event-Driven) i jak współgra z mikroserwisami?

Architektura zdarzeniowa opiera się na publikowaniu i konsumowaniu zdarzeń opisujących fakty, które już zaszły w systemie. Zdarzenie powinno być nazwane w czasie przeszłym, na przykład `OrderCreated`, `PaymentCaptured`, `ShipmentDispatched`. Producent publikuje fakt, a konsumenci samodzielnie decydują, jak na niego zareagować.

W mikroserwisach event-driven architecture pomaga zmniejszyć sprzężenie czasowe między usługami. Serwis zamówień nie musi synchronicznie wołać fakturowania, maili, analityki i programu lojalnościowego. Może zapisać zamówienie, opublikować zdarzenie, a inne serwisy przetworzą je niezależnie.

Korzyści:

- luźniejsze sprzężenie między producentem i konsumentami,
- lepsza odporność na chwilowe awarie konsumentów,
- możliwość dodawania nowych reakcji bez zmiany producenta,
- naturalna obsługa procesów asynchronicznych,
- łatwiejsze budowanie projekcji i integracji.

Koszty:

- trudniejsze debugowanie przepływów,
- eventual consistency,
- obsługa duplikatów i idempotencji,
- wersjonowanie schematów zdarzeń,
- monitoring lag, DLQ i przetwarzania,
- ryzyko ukrytej choreografii biznesowej.

EDA dobrze współgra z mikroserwisami, gdy zdarzenia reprezentują fakty domenowe i nie są tylko technicznymi komunikatami o zmianach tabel. Zdarzenie powinno mieć właściciela, schemat, semantykę i zasady kompatybilności.

69. Jakie są różnice między **event notification**, **event-carried state transfer** a **event sourcing**?

Event notification to lekkie powiadomienie, że coś się stało. Zawiera zwykle identyfikator i minimalny kontekst. Przykład: `OrderCreated { orderId }`. Konsument, jeśli potrzebuje szczegółów, pobiera je z API właściciela danych. Zaletą jest mały payload i mniejsze ryzyko duplikowania danych. Wadą jest dodatkowe wywołanie synchroniczne i zależność od dostępności producenta przy przetwarzaniu.

Event-carried state transfer oznacza, że zdarzenie niesie dane potrzebne konsumentom. Przykład: `OrderCreated { orderId, customerId, totalAmount, currency, items }`. Konsument może zaktualizować własną projekcję bez dodatkowego wywołania do producenta. Zaletą jest mniejsze sprzężenie runtime. Wadą jest większy kontrakt zdarzenia, ryzyko publikowania zbyt wielu danych i konieczność ewolucji schematu.

Event Sourcing to inny poziom wzorca. W nim zdarzenia są źródłem prawdy dla stanu agregatu. System nie zapisuje tylko aktualnego stanu, ale całą sekwencję faktów domenowych. Aktualny stan jest odtwarzany z historii zdarzeń. To daje audyt i możliwość rekonstrukcji stanu, ale zwiększa złożoność modelu, wersjonowania i projekcji.

Krótko:

- notification mówi: "coś się zmieniło, zapytaj mnie o szczegóły",
- event-carried state transfer mówi: "coś się zmieniło i tu są dane potrzebne do reakcji",
- event sourcing mówi: "historia zdarzeń jest bazą prawdy".

70. Jak działa **Apache Kafka** w kontekście mikroserwisów? Czym jest topic, partition, consumer group?

Apache Kafka to rozproszona platforma strumieniowa. Przechowuje zdarzenia w topicach, pozwala producentom publikować rekordy, a konsumentom czytać je we własnym tempie. Kafka nie jest klasyczną kolejką, która usuwa wiadomość po odczycie. Rekordy są przechowywane przez określony czas lub według limitów rozmiaru, a konsumenci śledzą własne offsety.

Topic to nazwany strumień rekordów, na przykład `orders.events` albo `payments.events`. Producenci publikują rekordy do topicu, a konsumenci je odczytują.

Partition to uporządkowany fragment topicu. Topic może mieć wiele partycji, co pozwala skalować zapis i odczyt równolegle. Wewnątrz jednej partycji Kafka zachowuje kolejność rekordów. Między partycjami nie ma globalnej kolejności.

Klucz rekordu decyduje zwykle, do której partycji trafi wiadomość. Jeśli kluczem jest `orderId`, wszystkie zdarzenia danego zamówienia trafią do tej samej partycji i zachowają kolejność względem siebie.

Consumer group to grupa instancji konsumenta współdzieląca odczyt topicu. Każda partycja jest przypisana do maksymalnie jednego konsumenta w danej grupie, więc grupa skaluje przetwarzanie równolegle. Jeśli są 3 partycje i 3 konsumenci, każdy może dostać jedną partycję. Jeśli konsumentów jest więcej niż partycji, nadmiarowe instancje nie będą miały pracy dla tego topicu.

Kafka dobrze pasuje do mikroserwisów, gdy potrzebny jest trwały strumień zdarzeń, wiele niezależnych konsumentów, replay danych, wysoki throughput i kolejność per klucz.

71. Jak zapewnić **kolejność zdarzeń** w systemie opartym na message brokerze?

Najpierw trzeba zdefiniować, jaka kolejność jest naprawdę wymagana. Globalna kolejność wszystkich zdarzeń w systemie jest kosztowna i zwykle niepotrzebna. Najczęściej potrzebna jest kolejność per agregat biznesowy, na przykład per `orderId`, `paymentId` albo `customerId`.

W Kafka kolejność jest gwarantowana tylko w ramach jednej partycji. Dlatego zdarzenia, które muszą być przetwarzane w kolejności, powinny mieć ten sam klucz partycjonowania. Jeśli wszystkie zdarzenia zamówienia mają klucz `orderId`, trafią do tej samej partycji.

Techniki:

- używać stabilnego klucza partycjonowania zgodnego z wymaganiem kolejności,
- unikać wielu producentów publikujących zdarzenia tego samego agregatu bez kontroli wersji,
- dodawać numer wersji agregatu lub sekwencję zdarzenia,
- po stronie konsumenta wykrywać luki i zdarzenia poza kolejnością,
- projektować idempotentne przetwarzanie,
- nie zwiększać równoległości przetwarzania w sposób łamiący kolejność per klucz.

Trzeba też uważać na retry. Jeśli jedna wiadomość się nie przetwarza, a kolejne są przetwarzane dalej, kolejność logiczna może zostać złamana. Dla ścisłej kolejności per klucz często trzeba zatrzymać przetwarzanie danego klucza lub partycji do czasu rozwiązania problemu. Dla mniej krytycznych przepływów można dopuścić przetwarzanie poza kolejnością i naprawę przez wersjonowanie.

72. Czym jest **dead letter queue (DLQ)** i jak obsługiwać wiadomości, których nie udało się przetworzyć?

Dead letter queue to miejsce, do którego trafiają wiadomości, których konsument nie potrafił poprawnie przetworzyć po określonej liczbie prób albo z powodu błędu nieponawialnego. DLQ chroni główny strumień przed zablokowaniem przez jedną wadliwą wiadomość.

Wiadomość może trafić do DLQ z powodu:

- niezgodnego schematu,
- błędu walidacji,
- braku wymaganych danych,
- błędu biznesowego,
- przekroczenia liczby retry,
- błędu, którego nie da się naprawić automatycznie.

Dobra obsługa DLQ:

- zapisać oryginalną wiadomość,
- dodać metadane błędu: typ wyjątku, czas, liczba prób, nazwa konsumenta,
- alertować, jeśli DLQ rośnie dla krytycznego przepływu,
- mieć narzędzia do inspekcji wiadomości,
- mieć procedurę replay po naprawie problemu,
- rozróżniać błędy tymczasowe od trwałych,
- nie wrzucać wiadomości w nieskończoną pętlę między retry i DLQ.

DLQ nie jest śmietnikiem, którego nikt nie czyta. Jeśli DLQ zawiera zdarzenia płatności albo zamówień, to jest stan biznesowo istotny. Musi mieć właściciela, SLO obsługi i proces naprawczy.

73. Jak zagwarantować semantykę **exactly-once** delivery (lub dlaczego jest to praktycznie niemożliwe)?

W systemach rozproszonych praktyczne "exactly-once" end-to-end jest bardzo trudne, bo obejmuje brokera, konsumenta, bazę danych, zewnętrzne API i awarie w dowolnym momencie. Broker może dostarczyć wiadomość raz, ale konsument może przetworzyć ją, zapisać wynik i paść przed commitem offsetu. Po restarcie wiadomość zostanie przetworzona ponownie.

Kafka ma mechanizmy exactly-once semantics dla określonych scenariuszy, szczególnie Kafka-to-Kafka z transakcjami producenta i konsumenta. Nie oznacza to automatycznie exactly-once dla efektów ubocznych w zewnętrznej bazie, API płatności albo wysłanym e-mailu.

W praktyce projektuje się system na `at-least-once delivery` plus idempotentne przetwarzanie:

- każda wiadomość ma unikalny `messageId` lub klucz biznesowy,
- konsument zapisuje informację o przetworzonych wiadomościach,
- operacje w bazie używają upsertów, unikalnych constraintów albo wersjonowania,
- zewnętrzne API dostaje idempotency key,
- offset jest commitowany dopiero po trwałym zapisie skutku,
- przetwarzanie jest odporne na duplikaty.

Można też stosować `effectively-once`, czyli gwarancję, że mimo duplikatów efekt biznesowy wystąpi raz. To jest właściwy cel w większości systemów. Użytkownika interesuje, żeby karta nie została obciążona dwa razy, a nie to, czy broker technicznie dostarczył bajty dokładnie raz.

74. Czym jest wzorzec **Outbox** i jak zapobiega utracie zdarzeń przy zapisie do bazy i wysyłce na kolejkę?

Outbox rozwiązuje problem dual write: aplikacja musi zapisać zmianę w bazie i opublikować zdarzenie do brokera. Jeśli zapis do bazy się uda, a publikacja do brokera nie, system traci zdarzenie. Jeśli publikacja się uda, a zapis do bazy nie, konsumenci zobaczą fakt, który nie istnieje w źródle prawdy.

Wzorzec Outbox polega na zapisaniu danych biznesowych i zdarzenia do tabeli outbox w tej samej lokalnej transakcji. Potem osobny proces, relay albo CDC publikuje zdarzenia z outboxa do brokera i oznacza je jako opublikowane.

Przebieg:

- serwis obsługuje komendę,
- w jednej transakcji zapisuje zmianę domenową i rekord outbox,
- transakcja się zatwierdza,
- publisher odczytuje outbox,
- publikuje zdarzenie do brokera,
- oznacza rekord jako wysłany albo polega na CDC i offsetach.

Korzyść jest taka, że nie ma momentu, w którym baza mówi jedno, a zdarzenie bezpowrotnie ginie. Możliwe są duplikaty publikacji, więc konsumenci nadal muszą być idempotentni. Outbox daje niezawodną publikację, nie zwalnia z obsługi at-least-once.

Outbox jest szczególnie mocny z CDC, na przykład Debezium. Aplikacja zapisuje zdarzenie domenowe do tabeli outbox, a Debezium czyta log transakcyjny i publikuje zdarzenie do Kafki.

75. Jak zaprojektować **schema evolution** w zdarzeniach (Avro, Protobuf, Schema Registry)?

Schema evolution to zasady zmieniania schematów zdarzeń bez łamania istniejących producentów i konsumentów. W architekturze zdarzeniowej zdarzenia żyją długo: mogą być przechowywane w brokerze, replayowane, przetwarzane przez wiele zespołów i używane do projekcji. Nie można traktować ich jak prywatnego DTO jednej aplikacji.

Dobre zasady:

- dodawać pola jako opcjonalne albo z wartością domyślną,
- nie usuwać pól używanych przez konsumentów bez procesu deprecjacji,
- nie zmieniać znaczenia istniejącego pola,
- nie zmieniać typu pola w sposób niekompatybilny,
- obsługiwać nieznane pola i nieznane wartości enum,
- wersjonować schematy,
- testować kompatybilność w pipeline,
- dokumentować semantykę, nie tylko strukturę.

Avro i Protobuf pomagają definiować formalne schematy. Schema Registry przechowuje wersje schematów i może wymuszać reguły kompatybilności, na przykład backward, forward albo full compatibility. Dzięki temu producent nie może opublikować schematu, który złamie konsumentów, jeśli polityka na to nie pozwala.

Trzeba odróżnić zmianę schematu od zmiany znaczenia. Technicznie kompatybilna zmiana może być biznesowo łamiąca. Jeśli pole `totalAmount` wcześniej oznaczało kwotę brutto, a po zmianie oznacza netto, schema registry tego nie wykryje. Dlatego schema evolution wymaga też przeglądu kontraktów i komunikacji między właścicielem zdarzenia a konsumentami.

---

## 10. Testowanie mikroserwisów

76. Jak wygląda **piramida testów** w kontekście mikroserwisów?

Piramida testów w mikroserwisach nadal opiera się na dużej liczbie szybkich testów jednostkowych, mniejszej liczbie testów integracyjnych i niewielkiej liczbie testów end-to-end. Różnica polega na tym, że granice usług stają się krytycznym miejscem testowania. Trzeba sprawdzać nie tylko logikę wewnątrz serwisu, ale też kontrakty API, zdarzenia, integrację z bazą, brokerem i zachowanie przy awariach zależności.

Warstwy:

- Testy jednostkowe: logika domenowa, walidacje, mapowanie stanów, polityki retry, reguły autoryzacji. Są szybkie i powinny być najliczniejsze.
- Testy integracyjne serwisu: aplikacja z prawdziwą bazą, brokerem, migracjami i konfiguracją, często przez Testcontainers.
- Testy kontraktowe: zgodność API lub zdarzeń między producentem i konsumentem.
- Testy komponentowe: cały mikroserwis uruchomiony jako czarna skrzynka, z zależnościami zastąpionymi stubami lub kontenerami.
- Testy E2E: kilka lub kilkanaście usług razem, sprawdzające krytyczne przepływy biznesowe.

W mikroserwisach nie należy przenosić ciężaru na E2E. Pełne testy systemowe są wolne, kruche i trudne diagnostycznie. Dobra strategia to dużo testów lokalnych i kontraktowych, a E2E tylko dla najważniejszych ścieżek, takich jak rejestracja, checkout, płatność, anulowanie i procesy regulacyjne.

77. Czym jest **testowanie kontraktowe** (contract testing) i jak różni się od testów integracyjnych?

Testowanie kontraktowe sprawdza, czy dwie strony komunikacji zgadzają się co do formatu i semantyki wymiany. Kontraktem może być REST API, gRPC, zdarzenie Kafka, wiadomość kolejki albo plik. Test nie musi uruchamiać całego systemu. Sprawdza granicę między producentem i konsumentem.

Test integracyjny sprawdza, czy kilka komponentów działa razem w konkretnym środowisku. Na przykład serwis zamówień z prawdziwą bazą PostgreSQL i brokerem Kafka. Test kontraktowy sprawdza natomiast, czy serwis zamówień nadal zwraca odpowiedź, której oczekuje BFF, albo publikuje zdarzenie, które rozumie serwis fakturowania.

Różnice:

- Test kontraktowy jest zwykle szybszy i bardziej precyzyjny.
- Test integracyjny daje większą pewność co do realnego działania komponentów technicznych.
- Test kontraktowy wykrywa breaking changes przed deployem dostawcy.
- Test integracyjny wykrywa problemy konfiguracji, migracji, serializacji, transakcji i połączeń.

Przykład: jeśli dostawca API zmieni `customerId` z liczby na string, test kontraktowy konsumenta może to wykryć bez uruchamiania całego przepływu zamówienia. Test integracyjny może natomiast wykryć, że aplikacja nie startuje z nową migracją bazy.

78. Jak testować mikroserwis w **izolacji** (mockowanie zależności, WireMock, Testcontainers)?

Testowanie w izolacji oznacza, że sprawdzamy jeden serwis bez uruchamiania całego ekosystemu. Celem jest szybka i deterministyczna informacja, czy serwis poprawnie realizuje swoją odpowiedzialność.

Techniki:

- Mocki w testach jednostkowych dla portów i zależności aplikacyjnych.
- WireMock albo podobne narzędzia do stubowania zewnętrznych API HTTP.
- Fake implementacje dla prostych zależności, jeśli zachowanie jest stabilne.
- Testcontainers dla zależności infrastrukturalnych, takich jak PostgreSQL, Redis, Kafka, RabbitMQ.
- Contract stubs wygenerowane z kontraktów konsumenckich.
- In-memory broker tylko wtedy, gdy semantyka jest wystarczająco podobna do produkcyjnej.

Granica jest ważna. Bazy danych i brokerów często nie warto mockować na poziomie testów integracyjnych, bo wiele błędów wynika z SQL, migracji, transakcji, offsetów i serializacji. Lepiej uruchomić prawdziwy PostgreSQL lub Kafkę w kontenerze niż udawać ich zachowanie ręcznie.

Mockowanie zależności HTTP ma sens, gdy zależność jest poza zakresem testu. WireMock pozwala zdefiniować odpowiedzi, opóźnienia, błędy i timeouty. Dzięki temu można sprawdzić retry, fallback, circuit breaker i mapowanie błędów.

Dobre testy izolowane powinny sprawdzać także przypadki awaryjne: timeout zależności, duplikat wiadomości, błąd walidacji, niedostępność cache, konflikt wersji i ponowne przetworzenie tej samej komendy.

79. Czym są **testy End-to-End (E2E)** w ekosystemie mikroserwisów i dlaczego są trudne do utrzymania?

Testy E2E sprawdzają pełny przepływ przez wiele usług i komponentów, często od API lub UI aż do bazy, brokera i zewnętrznych integracji zastąpionych sandboxem. Przykład: użytkownik dodaje produkt do koszyka, składa zamówienie, płaci, system tworzy wysyłkę i wysyła potwierdzenie.

Są wartościowe, bo dają pewność, że krytyczna ścieżka biznesowa działa jako całość. Problem polega na tym, że są drogie i kruche.

Trudności:

- wymagają uruchomienia wielu usług w zgodnych wersjach,
- awaria jednej zależności psuje test niezwiązany z badaną zmianą,
- dane testowe są trudne do przygotowania i czyszczenia,
- asynchroniczność wymaga oczekiwania i pollingów,
- diagnoza porażki jest trudna, bo błąd może być w dowolnym komponencie,
- testy są wolne,
- środowiska E2E często różnią się od produkcji,
- równoległe testy mogą sobie przeszkadzać.

Dlatego E2E powinny obejmować mały zestaw najważniejszych przepływów. Nie powinny zastępować testów jednostkowych, integracyjnych i kontraktowych. Dobre E2E są stabilne, mają izolowane dane, jasne timeouty, dobry logging, trace ID i sprawdzają efekt biznesowy, nie szczegóły implementacji UI lub wewnętrznych API.

80. Jak wykorzystać **Testcontainers** do testów integracyjnych z bazą danych i brokerem komunikatów?

Testcontainers pozwala uruchamiać prawdziwe zależności infrastrukturalne jako kontenery na czas testów. Zamiast używać mocka PostgreSQL albo współdzielonej bazy testowej, test startuje własny kontener bazy, wykonuje migracje i uruchamia aplikację przeciwko tej instancji. To zwiększa wiarygodność testów i zmniejsza problemy z konfliktami danych.

Zastosowania:

- PostgreSQL, MySQL, MongoDB do testowania repozytoriów, migracji i transakcji,
- Kafka lub RabbitMQ do testowania publikacji i konsumpcji wiadomości,
- Redis do cache i locków,
- Elasticsearch/OpenSearch do indeksowania i wyszukiwania,
- LocalStack do wybranych usług AWS.

Dobry test z Testcontainers:

- uruchamia wersję zależności zbliżoną do produkcji,
- wykonuje migracje schematu,
- tworzy dane testowe jawnie,
- czyści stan między testami albo używa izolowanych baz,
- nie zależy od kolejności testów,
- sprawdza realną serializację, constraints, indeksy i offsety.

Trzeba kontrolować czas wykonania. Kontenery mogą spowolnić pipeline, jeśli każdy test startuje osobną infrastrukturę. Często używa się współdzielenia kontenera w ramach klasy lub modułu testowego, przy zachowaniu izolacji danych. Testcontainers nie zastępuje testów kontraktowych, ale świetnie sprawdza warstwę integracji z technologią.

81. Czym jest **Consumer-Driven Contract Testing** i jakie problemy rozwiązuje w architekturze mikroserwisowej?

Consumer-Driven Contract Testing oznacza, że kontrakt jest definiowany przez potrzeby konsumenta API, a dostawca weryfikuje, czy nadal spełnia te oczekiwania. To odwraca perspektywę: nie dostawca publikuje ogromną specyfikację "na wszelki wypadek", tylko konsumenci mówią, których endpointów, pól, statusów i zdarzeń faktycznie używają.

Przebieg:

- konsument pisze test swoich oczekiwań wobec dostawcy,
- narzędzie generuje kontrakt,
- kontrakt jest publikowany do brokera kontraktów,
- dostawca pobiera kontrakty i uruchamia je przeciwko swojej implementacji,
- pipeline dostawcy blokuje zmianę łamiącą aktywnych konsumentów.

Rozwiązywane problemy:

- breaking changes wykrywane przed produkcją,
- mniejsza potrzeba wspólnych środowisk integracyjnych,
- jasna informacja, kto używa których części API,
- bezpieczniejsze niezależne wdrożenia,
- lepsza komunikacja między zespołami,
- możliwość usuwania pól dopiero po potwierdzeniu, że nikt ich nie używa.

Consumer-driven contracts są szczególnie dobre dla API między zespołami. Wymagają jednak dyscypliny. Kontrakty nie powinny odtwarzać całej implementacji dostawcy ani zamieniać się w kruche snapshoty. Powinny opisywać ważne oczekiwania konsumenta: strukturę, typy, wymagane pola, kody statusu i kluczowe scenariusze błędów.

---

## 11. Wzorce organizacyjne i zespołowe

82. Jak **Prawo Conwaya** wpływa na projektowanie mikroserwisów?

Prawo Conwaya mówi, że organizacje projektują systemy odzwierciedlające swoje struktury komunikacji. Jeśli zespoły są podzielone według warstw technicznych, na przykład frontend, backend, baza danych i QA, system często też będzie miał silne zależności warstwowe. Jeśli zespoły są podzielone wokół zdolności biznesowych, łatwiej zbudować usługi odpowiadające tym zdolnościom.

W mikroserwisach ma to bezpośrednie znaczenie. Architektura zakłada autonomiczne usługi, ale autonomia techniczna nie powstanie, jeśli każda zmiana wymaga uzgodnienia z kilkoma zespołami funkcyjnymi. Granice serwisów powinny pasować do granic odpowiedzialności zespołów.

Przykład: jeśli istnieje zespół odpowiedzialny za cały checkout, od API przez logikę biznesową po monitoring produkcji, naturalną granicą są usługi związane z checkoutem, zamówieniami i integracjami płatniczymi. Jeśli odpowiedzialność jest rozbita między kilka zespołów, proces będzie wymagał koordynacji i kolejki zależności.

Inverse Conway Maneuver polega na świadomym dostosowaniu struktury organizacji do architektury, którą chce się uzyskać. Jeśli firma chce mieć niezależne mikroserwisy domenowe, powinna tworzyć zespoły posiadające domenę end-to-end, a nie tylko fragment techniczny.

83. Czym jest model **„You build it, you run it"** i jak zmienia odpowiedzialność zespołów?

`You build it, you run it` oznacza, że zespół tworzący usługę odpowiada także za jej działanie na produkcji. Nie przekazuje kodu osobnemu działowi operacji jako zamkniętego pakietu. Zespół ma odpowiedzialność za jakość, wdrożenie, monitoring, alerty, incydenty, koszty i utrzymanie.

Zmienia to sposób projektowania. Jeśli zespół będzie budzony przez własne alerty, zacznie inwestować w observability, prostsze wdrożenia, lepsze testy, odporność i redukcję długu technicznego. Odpowiedzialność operacyjna zamyka pętlę informacji zwrotnej między decyzją projektową a skutkiem produkcyjnym.

Wymagania:

- zespół ma dostęp do metryk, logów i trace'ów,
- pipeline wdrożeniowy jest samoobsługowy,
- istnieją runbooki i standardy incydentowe,
- on-call jest wspierany przez proces i narzędzia,
- platforma zapewnia bezpieczne domyślne mechanizmy,
- zespół ma realny wpływ na architekturę swojej usługi.

Model nie oznacza, że każdy zespół ma samodzielnie budować Kubernetes, monitoring i CI/CD od zera. Platform team powinien dostarczać wspólne narzędzia, a zespoły produktowe powinny odpowiadać za swoje usługi na tej platformie.

84. Jak zorganizować zespoły wokół mikroserwisów — **feature teams** vs **platform teams**?

Feature team to zespół zorganizowany wokół wartości biznesowej lub domeny. Ma kompetencje potrzebne do dostarczenia funkcji end-to-end: backend, frontend, testy, dane, podstawy operacji. W mikroserwisach taki zespół powinien posiadać jedną lub kilka usług domenowych i odpowiadać za ich cykl życia.

Platform team buduje wewnętrzne narzędzia i standardy, które zmniejszają koszt pracy feature teamów. Dostarcza CI/CD, szablony usług, observability, service mesh, zarządzanie sekretami, moduły Terraform, klastry, runtime, standardy bezpieczeństwa i golden paths.

Różnica:

- feature team dostarcza funkcje użytkownikom lub biznesowi,
- platform team dostarcza możliwości techniczne innym zespołom,
- feature team powinien być autonomiczny w domenie,
- platform team powinien standaryzować i automatyzować powtarzalne problemy.

Dobre rozdzielenie nie tworzy blokady. Platforma nie powinna być zespołem, przez który trzeba ręcznie przejść z każdą zmianą. Powinna być produktem wewnętrznym: udokumentowanym, samoobsługowym, z API, szablonami i wsparciem. Feature teamy nie powinny omijać platformy przez własne niestandardowe rozwiązania, jeśli platforma spełnia potrzeby.

85. Czym jest **wewnętrzna platforma deweloperska (Internal Developer Platform)** i jak wspiera ekosystem mikroserwisów?

Internal Developer Platform to zestaw narzędzi, automatyzacji i standardów, który pozwala zespołom tworzyć, wdrażać i utrzymywać usługi bez ręcznego składania całej infrastruktury. Platforma nie jest tylko Kubernetesem ani portalem. To produkt wewnętrzny, który zapewnia powtarzalną ścieżkę od pomysłu do działającej usługi.

Typowe elementy:

- szablony nowych serwisów,
- standardowy pipeline CI/CD,
- rejestr usług i właścicieli,
- automatyczne tworzenie repozytoriów, deploymentów i dashboardów,
- moduły IaC,
- zarządzanie sekretami,
- logi, metryki i tracing domyślnie włączone,
- standardy health checków,
- mechanizmy konfiguracji,
- skanowanie bezpieczeństwa,
- dokumentacja i runbooki.

Platforma wspiera mikroserwisy, bo obniża koszt operacyjny dużej liczby usług. Bez platformy każdy zespół rozwiązuje te same problemy inaczej: inne logowanie, inne alerty, inne deploymenty, inne sekrety. To utrudnia utrzymanie i zwiększa ryzyko.

Dobra platforma daje golden path, czyli rekomendowaną, najłatwiejszą i bezpieczną drogę tworzenia usługi. Nie musi blokować wszystkich wyjątków, ale wyjątki powinny być świadome i uzasadnione. Platforma powinna być mierzona jak produkt: czas utworzenia usługi, czas wdrożenia, awaryjność pipeline, satysfakcja developerów, zgodność ze standardami.

86. Jak zarządzać **zależnościami między zespołami** w dużym ekosystemie mikroserwisowym?

Zależności między zespołami są jednym z głównych kosztów mikroserwisów. Jeżeli każda zmiana wymaga synchronizacji roadmap, spotkań, ręcznych akceptacji i wspólnego release'u, architektura nie daje niezależności.

Techniki zarządzania:

- jasne ownership usług i danych,
- publiczne kontrakty API i zdarzeń,
- testy kontraktowe,
- wersjonowanie i polityki deprecjacji,
- katalog usług z dokumentacją, SLA/SLO i właścicielem,
- asynchroniczna komunikacja tam, gdzie zmniejsza sprzężenie,
- unikanie współdzielonych baz danych,
- regularne przeglądy zależności i architektury,
- platformowe standardy dla typowych integracji,
- ADR-y dla ważnych decyzji.

Warto rozróżnić zależności runtime i delivery. Zależność runtime oznacza, że usługa A woła usługę B w czasie działania. Zależność delivery oznacza, że zespół A nie może dostarczyć zmiany bez pracy zespołu B. Mikroserwisy mogą akceptować zależności runtime, jeśli są stabilne i odporne. Najbardziej bolesne są zależności delivery, bo spowalniają organizację.

Dobrą praktyką jest traktowanie API jak produktu. Serwis powinien mieć właściciela, dokumentację, kompatybilność wstecz, changelog i proces wsparcia konsumentów. Zespoły nie powinny integrować się przez prywatne tabele, wewnętrzne klasy ani nieudokumentowane endpointy.

87. Kiedy mikroserwisy wprowadzają więcej problemów niż rozwiązują (**distributed monolith** antipattern)?

Distributed monolith to system fizycznie podzielony na wiele usług, ale logicznie sprzężony jak jeden monolit. Ma koszty systemu rozproszonego, ale nie ma niezależności mikroserwisów.

Objawy:

- usługi muszą być wdrażane razem,
- zmiana jednej usługi wymaga zmian w wielu innych,
- wiele usług współdzieli jedną bazę danych,
- wywołania są bardzo częste i drobnoziarniste,
- proces biznesowy wymaga synchronicznego łańcucha wielu usług,
- brak jasnych właścicieli danych,
- testy E2E są jedynym sposobem uzyskania pewności,
- awaria jednej usługi zatrzymuje większość systemu,
- zespoły są zorganizowane według warstw technicznych, a nie domen,
- kontrakty API są niestabilne i niekompatybilne.

Mikroserwisy wprowadzają więcej problemów niż rozwiązują, gdy skala organizacji, domeny albo ruchu nie uzasadnia kosztu rozproszenia. Jeśli zespół jest mały, domena szybko się zmienia, a system nie ma osobnych potrzeb skalowania, modularny monolit często będzie lepszy.

Naprawa distributed monolith nie zawsze oznacza tworzenie jeszcze większej liczby usług. Czasem lepsze jest scalenie zbyt drobnych usług, wzmocnienie granic modułów, usunięcie współdzielonej bazy, uporządkowanie kontraktów i dopasowanie zespołów do domen. Celem nie jest maksymalna liczba mikroserwisów, tylko niezależność zmian przy akceptowalnym koszcie operacyjnym.

---

## Powiązane materiały

- [System Design: Pytania Rekrutacyjne](system-design-pytania-rekrutacyjne.md)
