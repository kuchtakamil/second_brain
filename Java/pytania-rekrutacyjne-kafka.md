# Kafka: Pytania Rekrutacyjne (Senior Java Developer)

Lista pytań na rozmowę kwalifikacyjną z zakresu **Apache Kafka** na poziomie Senior Java Developer. Pytania pogrupowane tematycznie — od podstaw architektury po zaawansowane scenariusze produkcyjne.

---

## 1. Architektura i podstawowe koncepcje

1. **Czym jest Apache Kafka i jaki problem rozwiązuje? Czym różni się od tradycyjnych kolejek wiadomości (np. RabbitMQ, ActiveMQ)?**
   - **Kafka** to platforma do strumieniowania zdarzeń (distributed event streaming platform). Została zaprojektowana do obsługi ogromnych wolumenów danych w czasie rzeczywistym. Rozwiązuje problem integracji systemów, analizy logów, stream processingu oraz rozprzęgania (decoupling) producentów i konsumentów danych.
   - **Różnice:**
     - *Tradycyjne kolejki:* Skupiają się na dostarczaniu wiadomości do konkretnego odbiorcy z potwierdzeniem odbioru "na poziomie brokera" powodującym usunięcie wiadomości (smart broker, dumb consumer).
     - *Kafka:* Działa jak rozproszony log (append-only log). Wiadomości nie są usuwane zaraz po odczytaniu (retencja). Konsumenci sami śledzą, gdzie skończyli czytać (dumb broker, smart consumer). Oferuje gigantyczną przepustowość.

2. **Opisz architekturę Kafki: broker, klaster, topic, partycja, offset, segment.**
   - **Broker:** Pojedynczy węzeł serwera w klastrze Kafki. Przechowuje dane i obsługuje żądania zapisu/odczytu.
   - **Klaster:** Grupa brokerów współpracujących w celu zapewnienia skalowalności i wysokiej dostępności.
   - **Topic:** Logiczny kanał lub strumień zdarzeń (kategoria), do którego trafiają komunikaty.
   - **Partycja:** Zrównoleglenie topicu. Każda partycja to uporządkowany log. Rozrzucenie partycji na wiele brokerów pozwala skalować zapis i odczyt.
   - **Offset:** Unikalny, sekwencyjny identyfikator (liczba całkowita) wiadomości w konkretnej partycji.
   - **Segment:** Plik fizyczny na dysku brokera. Partycja dzieli się na mniejsze segmenty logu, co ułatwia usuwanie przestarzałych danych przez mechanizm retencji.

3. **Czym jest topic i jak jest podzielony na partycje? Dlaczego partycjonowanie jest kluczowe dla skalowalności?**
   - **Topic** dzieli się na **partycje** (np. 10 partycji dla topicu "orders").
   - **Skalowalność:** Brak podziału wymusiłby przechowywanie całości danych topicu u jednego brokera i przetwarzanie ich przez jednego konsumenta (bottleneck). Partycje pozwalają współbieżnie produkować na wiele brokerów i równolegle czytać dane przez wielu konsumentów w ramach Consumer Group.

4. **Jak działa mechanizm replikacji w Kafce? Czym jest leader, follower, ISR (In-Sync Replicas)?**
   - **Leader:** Tylko jedna z replik partycji obsługuje odczyty i zapisy w danym momencie (Lider).
   - **Follower:** Pozostałe repliki pasywnie ciągną dane od lidera. Jeśli lider ulegnie awarii, follower może go zastąpić.
   - **ISR (In-Sync Replicas):** Lista zsynchronizowanych followersów. Jeśli follower przestaje nadążać za liderem (np. duże lagi sieciowe), odpada z listy ISR. Wybór nowego lidera po awarii odbywa się bezpiecznie tylko spośród replik z listy ISR.

5. **Czym jest replication factor i min.insync.replicas? Jak wpływają na trwałość danych?**
   - **Replication factor:** Liczba kopii danej partycji na różnych brokerach (zwykle 3).
   - **min.insync.replicas:** Minimalna liczba węzłów ISR, która musi udanie zapisać wiadomość, zanim broker potwierdzi jej otrzymanie (przy acks=all).
   - Ich połączenie chroni system przed utratą danych. Dla RF=3 i min.insync=2, klaster przetwarza ruch bezawaryjnie przy utracie 1 węzła i blokuje zapis, gdy liczba zdrowych węzłów spada poniżej 2 (zapobiegając utracie tzw. quorum trwałości).

6. **Jak Kafka zapewnia kolejność wiadomości? Czy kolejność jest gwarantowana globalnie czy per-partycja?**
   - Kolejność jest gwarantowana **wyłącznie na poziomie pojedynczej partycji**. Kafka nie oferuje globalnej gwarancji na przestrzeni całego topicu ze względu na architekturę rozproszoną.
   - Aby zachować rygorystyczną kolejność zdarzeń dla danego bytu (np. ID klienta), wykorzystuje się klucze wiadomości — producent mapuje określony klucz do stałej partycji na podstawie hasha.

7. **Czym jest log i dlaczego Kafka opiera się na strukturze append-only log?**
   - **Log** to najprostsza baza danych — liniowy ciąg rekordów.
   - **Append-only** oznacza, że Kafka tylko dopisuje dane do końca pliku. Nie dokonuje modyfikacji już zapisanych wiadomości.
   - Zapobiega to losowym odczytom i zapisom po dysku (random I/O), przez co zapis dyskowy zachowuje wysoką wydajność zbliżoną do zapisu w pamięci RAM, optymalnie korzystając ze wsparcia page cache systemu operacyjnego.

8. **Czym jest ZooKeeper w kontekście Kafki? Czym jest KRaft (Kafka Raft) i dlaczego Kafka odchodzi od ZooKeepera?**
   - **ZooKeeper:** Zewnętrzna baza utrzymująca metadane o brokerach, stanach leaderów i konfiguracji ACL w starszych wersjach.
   - **KRaft:** Wewnętrzny, scentralizowany protokół konsensusu wprowadzony by Kafka zarządzała metadanymi własnymi siłami z użyciem mechanizmu event sourcingu.
   - **Dlaczego:** Pozbycie się zewnętrznej zależności ułatwia architekturę, przyspiesza znacząco start klastrów i wyłanianie nowych liderów przy awariach oraz redukuje koszty operacyjne do zarządzania jednym serwerem/systemem, a nie dwoma.

9. **Jak działa mechanizm retencji wiadomości? Czym różni się retencja czasowa od retencji opartej na rozmiarze?**
   - Retencja w Kafce wymazuje stare wiadomości poprzez skasowanie całych segmentów logów na dysku.
   - **Retencja czasowa (`log.retention.hours`):** Kasuje segmenty na podstawie metadanej czasowej np. starsze niż 7 dni.
   - **Retencja rozmiarowa (`log.retention.bytes`):** Ustala limit dyskowy per partycja np. do 1GB. Gdy limit jest przekroczony, starsze segmenty są skasowane niezależnie od ich wieku. Obie opcje można złączyć ze sobą.

10. **Czym jest log compaction i w jakich scenariuszach jest przydatny?**
    - **Log compaction** to strategia zatrzymywania danych polegająca na usunięciu starych wersji danego rekordu, zostawiając w logu jedynie **najnowszą wartość dla każdego klucza wiadomości**.
    - **Scenariusze:** Gdy interesuje nas tylko aktualny i ostateczny stan systemu (np. balans konta użytkownika), a nie jego pełna ścieżka zmian transakcji. Wykorzystywana intensywnie dla stanów bazodanowych KTable w Kafka Streams.

---

## 2. Producer API

11. **Jak działa Kafka Producer? Opisz cykl życia wiadomości od wywołania `send()` do potwierdzenia zapisu.**
    - Wywołanie asynchronicznego `send(record)`.
    - **Serialization:** Klucz i wartość są zmieniane na postaci bajtowe w oparciu o skonfigurowane Serializers.
    - **Partitioning:** Ustalenie do której partycji wyślemy rekord na podstawie klucza i partitionera.
    - **Accumulator:** Rekord ląduje w buforze pamięci (`RecordAccumulator`), grupując się w batche dla konkretnych partycji z innymi rekordami.
    - **Sender thread:** Działający w tle wątek zbiera batche, gdy są pełne (lub przejdzie czas limitu `linger.ms`) i transmituje je żądaniami po sieci do brokerów Liderów. 
    - Odebranie odpowiedzi ACK od brokera wyzwala zakończenie promisów (`Future`), bądź w przypadku błędu aktywowane zostaje ponowienie żądania (retry).

12. **Czym jest parametr `acks` (0, 1, all) i jak wpływa na gwarancje dostarczenia wiadomości?**
    - `acks=0`: Producent wysyła i od razu zamyka operację nie czekając w ogóle na odp. Maksymalna przepustowość i najniższa odporność — dane idą potencjalnie w pustkę.
    - `acks=1`: Producent oczekuje na zapis wyłącznie w logu lokalnym Lidera. Standardowy kompromis, narażony na pojedynczą awarię sprzętową przed synchronizacją do followersów.
    - `acks=all (-1)`: Lider czeka na synchronizację u wszystkich followersów aktualnie z listy `ISR`. Producent gwarantuje niezawodność zapisu kosztem czasu odpowiedzi. Aktualnie domyślnie od wersji 3.0.

13. **Jak działa partycjonowanie wiadomości w producencie? Czym jest klucz wiadomości i jaka jest domyślna strategia partycjonowania?**
    - Jeśli producent określa klucz (tzw. string/long identifier z kontekstem logiki biznesowej), defaultowy partitioner wylicza z niego Hash (Murmur2) modyfikowany przez liczbę partycji - dzięki czemu wiadomości lądują zawsze na tę samą i dobrą partycję, dbając o ich ścisłą kolejność przetwarzania.
    - W sytuacji gdy brakuje klucza (rekord to czysta wartość dla logu), stosowana jest "Sticky Partitioner", dopychająca jeden batch przed przeskoczeniem na kolejną losową partycję.

14. **Czym jest sticky partitioner i dlaczego został wprowadzony jako domyślna strategia w nowszych wersjach Kafki?**
    - Przed wejściem do Kafki sticky partitioning, w rekordach pozbawionych klucza stosowano metodę round-robin. Rekord 1 lądował na partycję 1, drugi na 2 itd., tworząc u klienta mnóstwo małych batchów sieciowych zamiast pojedynczej, solidnej paczki.
    - Sticky "przykleja" się do jednej partycji w buforze przez krótki czas. Optymalizuje znacząco rozmiar pakietów do wysyłki dla brokerów i oszczędza CPU po stronie serwera oraz klienta.

15. **Jak napisać własny `Partitioner`? Kiedy jest to potrzebne?**
    - Opcja tworzenia własnej logiki implementująca interfejs `org.apache.kafka.clients.producer.Partitioner` zastępująca standardowe hashowanie klucza. 
    - **Przypadki użycia:** Gdy występuje tzw. problem nieodpowiednio rozłożonych kluczy w strumieniu (data skew). 95% rekordów pochodzi od jednego ID gigantycznego Klienta – wyliczony hash zarżnie obciążeniem jedną partycję i spowolni system. Customowy mechanizm może wyłapać wielkie ID i wymuszać np. "round-robin dla tego jednego klienta na wybrany podzbiór wszystkich partycji".

16. **Czym jest batching i linger.ms? Jak wpływają na throughput i latency?**
    - Paczkowanie to klucz dla optymalizacji ruchu TCP u producenta. `batch.size` definiuje docelowy maksymalny rozmiar bajtowy paczek trzymanych w buforze do wysłania Liderowi.
    - Jeśli paczki zapełniają się powoli, `linger.ms` dyktuje ile czasu klient Kafki poczeka w nadziei, że aplikacja podrzuci kolejne rekordy, aż wymusi "niepełny batch" do wysłania w eter.
    - Efekt opóźnienia do np. 10ms nie jest kluczowy dla latencji, jednak zwielokrotni **throughput** (liczbę operacji wysyłki wiadomości w jednostce czasu na łączu i brokerze).

17. **Czym jest idempotentny producent (`enable.idempotence=true`) i jak zapobiega duplikacji wiadomości?**
    - Podczas braku uzyskania od brokera potwierdzenia (ACK), klient ponawia zapis retry by ratować dane. Czasami broker zapisał komunikat ale odpowiedź padła na sieci. Wtedy dochodzi do zdublowania danych (at-least-once).
    - Idempotencja (wymóg w najnowszych wersjach Kafki) pozwala uchronić się od powtórzeń nakładając ukryty "Producer ID" i wewnętrzne numery sekwencyjne do paczek, więc po przymusowym ponowieniu wysyłania (retry), lider brokera poznaje i kasuje dubla dla zabezpieczenia.

18. **Jak działa transakcyjny producent? Czym jest `transactional.id` i gwarancja exactly-once semantics (EOS)?**
    - Kafkowa odpowiedź w architekturze mikrousług dla atomowych i złożonych transakcji z wieloma partycjami na zapleczu. Gwarantuje zapis i proces albo we wszystkich żądanych topicach, albo w żadnym (Commit / Abort marker na logu brokera).
    - Opiera się o zdefiniowane powiązanie logicznego wątku procesów jako stałe ID transakcji (`transactional.id`). Pomaga to ratować zablokowane operacje na skutek awarii producenta, bez naruszania struktury exactly-once, gwarantującej brak duplikatów przy odczytach danych po rebalancingach procesowych.

19. **Jak producent obsługuje błędy? Czym jest retry, `max.in.flight.requests.per.connection` i ryzyko zmiany kolejności wiadomości?**
    - Niskopoziomowy błąd np. "Brak lidera" dla partycji powoduje odpalenie parametrów ponawiania `retries`.
    - `max.in.flight.requests.per.connection` kontroluje ilość "niewiadomych" requestów, które odjechały po otwartym na sieci sokecie dla jednego powiązania brokera w tym samym momencie i producent na nie czeka.
    - Zmiana kolejności zachodzi bez włączonej Idempotencji, jeśli batch w kolejce 1 padnie, 2 przejdzie prawidłowo na broker, ale ponowiony batch 1 znowu wbije i wyląduje już fizycznie za batchem 2. Aby od tego uciec bez włączenia EOS/idempotencji, trzeba było wymuszać in-flight wynoszący maksymalnie wartość "1" by ratować ścisły ordering.

20. **Czym jest `buffer.memory` i `max.block.ms`? Co się dzieje, gdy bufor producenta jest pełny?**
    - `buffer.memory` ustala bufor akumulatorowy u klienta (limit alokowania w RAM dla batche'y). Standard to ok. 32MB. 
    - Gdy ruch przekracza limity łącza lub gdy klaster Kafki jest przeciążony i zamula, akumulator po stronie producenta wypełnia pamięć bajt za bajtem.
    - Zapełnienie na 100% zablokuje wykonanie aplikacji Java na operacji `.send()`, czekając `max.block.ms` (zwykle ok. 60 sekund), i dopiero po tym czasie zrzuci fatalny `TimeoutException` pozbywając się back-pressure.

21. **Czym jest `Callback` w producencie i jak obsługiwać asynchroniczne potwierdzenia zapisu?**
    - Ominięcie standardowej w Javie blokady synchronicznej (tj. wywołania `Future.get()`). 
    - W API implementuje się dodatkowy argument jako Callback w wywołaniu metody `send(record, callback)`, gdzie odpowiedź z wewnątrz wewnętrznych struktur sieciowych powróci jako powiadomienie `onCompletion`. Obsłuży to informacje ze statusem powodzenia jak np. zrzuci warning do logów przy błędach sieciowych lub zapis do bazy z błędnymi danymi awaryjnymi w tle (DLQ na dysk) w oddzielnym wątku bez pauzowania rdzenia programu głównego.

---

## 3. Consumer API

22. Jak działa Kafka Consumer? Opisz mechanizm pollowania (`poll()`) i pętlę konsumenta.
23. Czym jest consumer group i jak Kafka realizuje load balancing wiadomości między konsumentami w grupie?
24. Jak działa rebalancing w consumer group? Jakie są jego przyczyny i konsekwencje?
25. Czym jest eager rebalancing vs cooperative (incremental) rebalancing? Jakie są różnice?
26. Czym są strategie przydzielania partycji (`partition.assignment.strategy`): RangeAssignor, RoundRobinAssignor, StickyAssignor, CooperativeStickyAssignor?
27. Jak działa commit offsetów? Czym różni się auto-commit od ręcznego commitu (`commitSync()`, `commitAsync()`)?
28. Jakie problemy mogą wynikać z auto-commitu offsetów? Kiedy warto go wyłączyć?
29. Czym jest `__consumer_offsets` topic? Jak Kafka przechowuje informacje o postępie konsumentów?
30. Czym jest `max.poll.records`, `max.poll.interval.ms` i `session.timeout.ms`? Jak wpływają na stabilność konsumenta?
31. Co się dzieje, gdy konsument nie wywołuje `poll()` w wymaganym czasie? Jak Kafka wykrywa „martwe" konsumenty?
32. Czym jest `seek()` i `seekToBeginning()` / `seekToEnd()`? Kiedy warto ręcznie kontrolować pozycję odczytu?
33. Jak konsumować wiadomości z konkretnej partycji bez consumer group (`assign()` vs `subscribe()`)?

---

## 4. Serializacja i Schema Registry

34. **Czym są Serializer i Deserializer w Kafce? Jak napisać własny?**
    - **Serializer** (u Producenta) przekształca obiekty (np. klasy Java) na ciąg bajtów (`byte[]`), z kolei **Deserializer** (u Konsumenta) zamienia pobrane z Kafki bajty z powrotem na obiekty aplikacyjne. Kafka wewnętrznie operuje tylko na bajtach i nie rozumie typów wysokopoziomowych.
    - **Własna implementacja:** Należy zaimplementować interfejs `org.apache.kafka.common.serialization.Serializer<T>` lub `Deserializer<T>`, nadpisując metody `serialize(String topic, T data)` (lub `deserialize`). Często wykorzystuje się biblioteki jak Jackson (dla JSON) czy wewnętrzne klasy do obsługi niestandardowych formatów binarnych.

35. **Czym jest Schema Registry (np. Confluent Schema Registry) i jaki problem rozwiązuje?**
    - To niezależny komponent (serwer HTTP), który przechowuje wersjonowane schematy wiadomości (np. Avro, Protobuf, JSON Schema) dla topiców.
    - **Problem rozwiązany:** Zapobiega sytuacjom, w których Producent zmienia strukturę wysyłanych danych (np. usuwa kluczowe pole lub zmienia typ danych), przez co istniejący Konsumenci rzucają wyjątki podczas deserializacji. Centralizuje zarządzanie formatem i "kontraktem" między różnymi mikroserwisami, sprawdzając poprawność schematu na etapie samej produkcji wiadomości.

36. **Jak działa Apache Avro w kontekście Kafki? Dlaczego jest preferowany nad JSON/Protobuf w pewnych scenariuszach?**
    - Avro to binarny format serializacji danych, który do zapisu/odczytu wymaga dostarczenia schematu (zazwyczaj napisanego w JSON). W systemach kafkowych schemat jest składowany w Schema Registry.
    - Producent wysyła do Kafki niepełną wiadomość: tylko krótki, 4-bajtowy identyfikator (`schema ID`) z Schema Registry, a następnie spakowane binarnie dane.
    - **Przewaga nad JSON:** Binarna forma i odcięcie metadanych schematu (nazwy pół) od samej wiadomości redukują drastycznie wagę paczek (nawet 10-krotnie mniej bajtów).
    - **Przewaga nad Protobuf/Thrift:** Schema w Avro jest reprezentowana w przyjaznym formacie JSON i pozwala na elastyczną, dynamiczną typizację (klient nie musi generować silnie typowanych klas przed uruchomieniem aplikacji, co jest kluczowe w narzędziach Big Data typu Hadoop/Spark/Kafka Connect).

37. **Czym jest kompatybilność schematów (backward, forward, full, none)? Jak Schema Registry wymusza kompatybilność?**
    - SR pozwala na skonfigurowanie reguł ewolucji dla każdego topicu. Kiedy Producent próbuje zarejestrować nowy schemat, SR analizuje go ze starszymi wersjami i odrzuca w przypadku złamania reguły.
    - **Backward compatibility (Wsteczna):** Nowy schemat pozwala na czytanie danych zapisanych według starszych schematów (np. dodanie nowego pola musi mieć wartość domyślną). Najpierw aktualizujemy konsumentów, potem producentów.
    - **Forward compatibility (Wprzód):** Stary schemat potrafi przeczytać nowe dane (stare aplikacje nie wybuchną z powodu nowych pól; pola są po prostu ignorowane). Najpierw aktualizujemy producentów, potem konsumentów.
    - **Full:** Kompatybilność dwukierunkowa. Oba warunki (wsteczna i wprzód) są spełnione.
    - **None:** Całkowite odpięcie zabezpieczeń (brak kontroli ewolucji).

38. **Jak obsługiwać ewolucję schematów wiadomości Kafki w aplikacji produkcyjnej?**
    - Najlepszą praktyką jest ustawienie Schema Registry na tryb **Backward** lub **Full compatibility**.
    - Ewolucja wymaga dodawania pól *wyłącznie opcjonalnych (z przypisaną wartością domyślną)* oraz unikania usuwania pól, które w poprzednim schemacie były obowiązkowe.
    - W CI/CD wdraża się pluginy (np. `kafka-schema-registry-maven-plugin`), które przed deployem weryfikują nowy schemat lokalny z tym trzymanym w zdalnym środowisku, blokując złe commity na etapie builda.

---

## 5. Kafka Streams

39. **Czym jest Kafka Streams i czym różni się od Kafka Consumer API? Kiedy użyć Kafka Streams zamiast zwykłego konsumenta?**
    - **Kafka Streams** to potężna biblioteka kliencka (część ekosystemu Apache Kafka) służąca do budowania aplikacji przetwarzających i transformujących dane w czasie rzeczywistym w sposób ciągły.
    - **Różnice:**
      - *Consumer API* to niskopoziomowe API służące wyłącznie do wyciągania bajtów/rekordów z Kafki do aplikacji, linia po linii. Zmusza programistę do ręcznego zarządzania stanem, agregacjami, back-pressure i łączeniami (joinami).
      - *Kafka Streams* to wyższy poziom abstrakcji oparty o Consumer/Producer API. Zapewnia gotowe operatory transformacyjne (map, filter, join), silnik do składowania stanu (RocksDB), tolerancję na awarie (odbudowa stanu z logu changelog) oraz koncepcję czasu i okien czasowych (windowing).
    - **Kiedy użyć:** Jeśli Twoja aplikacja zdejmuje dane z jednego topicu, dokonuje agregacji, mapowania lub łączenia wielu strumieni w jeden, by następnie odłożyć wynik na inny topic – użyj Kafka Streams. Zwykły Consumer jest lepszy na "końcu rury", kiedy np. zrzucamy dane do zewnętrznej bazy, wysyłamy maila lub wywołujemy zewnętrzne REST API.

40. **Czym jest KStream a czym KTable? Jaka jest fundamentalna różnica między nimi?**
    - To dwie podstawowe abstrakcje reprezentujące strumienie w Kafka Streams (tzw. Stream-Table Duality).
    - **KStream (Strumień zdarzeń):** Każdy nowy rekord to niezależny, dopisywany (insert-only) fakt. Nic nie jest nadpisywane. Przypomina tradycyjny strumień lub bazodanowy log transakcyjny. Przykład: Strumień pojedynczych transakcji kartą kredytową.
    - **KTable (Tabela stanu):** Reprezentuje aktualny stan, będący wynikiem aktualizacji ze strumienia po konkretnym kluczu głównym (upsert-only). Nowa wiadomość o kluczu "K" nadpisuje starą wiadomość pod kluczem "K". Podobnie do bazy danych z tabelami i kluczami głównymi lub kompaktorowanych logów (Log Compaction). Przykład: Ostateczne, aktualne saldo konta bankowego.
41. Czym jest GlobalKTable i kiedy ją stosować?
42. Jak działa DSL API w Kafka Streams? Opisz podstawowe operacje: `map()`, `filter()`, `flatMap()`, `groupBy()`, `aggregate()`.
43. Czym jest Processor API (niski poziom) i kiedy warto go użyć zamiast DSL?
44. Jak działają operacje windowing w Kafka Streams (tumbling, hopping, sliding, session windows)?
45. Jak działają joiny w Kafka Streams (stream-stream, stream-table, table-table)? Jakie są wymagania dotyczące partycjonowania?
46. Czym jest state store w Kafka Streams? Jak działa lokalne przechowywanie stanu (RocksDB)?
47. Czym są Interactive Queries i jak umożliwiają odpytywanie stanu aplikacji?
48. Jak Kafka Streams obsługuje odporność na awarie? Czym jest changelog topic i standby replicas?
49. Czym jest exactly-once semantics (EOS) w Kafka Streams i jak jest realizowana?
50. Jak testować topologię Kafka Streams (TopologyTestDriver)?

---

## 6. Kafka Connect

51. Czym jest Kafka Connect i jaki problem rozwiązuje?
52. Czym różni się Source Connector od Sink Connector?
53. Jak działa tryb standalone vs distributed w Kafka Connect?
54. Czym są transformacje (SMT — Single Message Transforms) w Kafka Connect?
55. Jak Kafka Connect zarządza offsetami i zapewnia odporność na awarie?
56. Jak napisać własny konektor Kafka Connect?

---

## 7. Bezpieczeństwo

57. Jakie mechanizmy uwierzytelniania obsługuje Kafka (SSL/TLS, SASL/PLAIN, SASL/SCRAM, SASL/GSSAPI, SASL/OAUTHBEARER)?
58. Jak działa autoryzacja w Kafce (ACL — Access Control Lists)? Jak skonfigurować uprawnienia per topic/per group?
59. Czym jest szyfrowanie in-transit (SSL/TLS) vs szyfrowanie at-rest w Kafce?
60. Jak zabezpieczyć komunikację między brokerami (inter-broker security)?

---

## 8. Wydajność i tuning

61. **Dlaczego Kafka jest tak wydajna? Opisz mechanizmy: zero-copy, page cache, sekwencyjny I/O, batching.**
    - **Sekwencyjny I/O (Sequential I/O):** Kafka dopisuje dane wyłącznie na końcu plików (append-only). Nowoczesne dyski (nawet talerzowe HDD, ale też SSD) są drastycznie szybsze w operacjach ciągłych niż przy losowym dostępie (random I/O), ze względu na brak konieczności relokacji głowicy/odszukiwania bloków.
    - **Page Cache (OS Cache):** Broker Kafki ufa całkowicie pamięci RAM zarządzanej przez system operacyjny. Wszelkie operacje zapisu i odczytu odbywają się na page cache'u, omijając garbage collection JVM (dzięki czemu brokerzy mogą operować na małym Heap Space jak 4GB-8GB nawet przy terabajtowych zapisach). Dane trafiają z page cache bezpośrednio do sieci bez kopiowania ich do user-space.
    - **Zero-copy (np. `sendfile` w Linuksie):** Konwencjonalny przepływ (dysk -> RAM jądra -> aplikacja/JVM -> socket buforu OS -> sieć) wymaga 4 kopiowań pamięci. Kafka wykorzystuje syscall `sendfile()`, gdzie dane przepisywane są z dysku/page-cache prosto do kontrolera sieciowego z pominięciem warstwy użytkownika (aplikacji). Daje to drastyczny wzrost przepustowości przy konsumowaniu strumieni.
    - **Batching:** W Kafce wszystko jest paczkowane po stronie klienta (producenta, konsumenta). Rozmiary I/O to zwykle kilkadziesiąt-kilkaset kilobajtów, co optymalizuje użycie sieci i CPU (mniej, ale grubszych requestów).
62. Jak dobrać liczbę partycji dla topicu? Jakie czynniki należy wziąć pod uwagę?
63. Jak dobrać replication factor w kontekście trwałości vs wydajności?
64. Jakie parametry producenta wpływają na throughput (batch.size, linger.ms, compression.type, buffer.memory)?
65. Jakie parametry konsumenta wpływają na throughput (fetch.min.bytes, fetch.max.wait.ms, max.partition.fetch.bytes)?
66. Czym jest kompresja wiadomości w Kafce (gzip, snappy, lz4, zstd)? Kiedy stosować jaką kompresję?
67. Jak monitorować Kafkę? Jakie metryki są kluczowe (lag konsumenta, ISR shrink, under-replicated partitions, request latency)?
68. Jak działa quota mechanism w Kafce (limity na producenta/konsumenta)?

---

## 9. Wzorce i architektura

69. **Czym jest wzorzec Event Sourcing i jak Kafka może go wspierać?**
    - **Event Sourcing** polega na tym, że źródłem prawdy nie jest aktualny snapshot encji w tabeli, tylko niezmienny ciąg zdarzeń domenowych opisujących wszystkie zmiany stanu. Zamiast zapisać `Order.status = PAID`, system zapisuje np. `OrderCreated`, `PaymentAuthorized`, `OrderPaid`, `OrderShipped`.
    - Stan obiektu jest odtwarzany przez replay zdarzeń w poprawnej kolejności. To daje pełny audyt, możliwość cofnięcia się w czasie, debugowania decyzji biznesowych i budowania nowych projekcji z historycznych danych.
    - Kafka dobrze pasuje do tego modelu, bo topic/partycja jest append-only logiem. Rekordy są niezmienne, mają offset, timestamp, klucz i mogą być odtwarzane wielokrotnie przez różnych konsumentów. Dla danego agregatu domenowego klucz wiadomości, np. `orderId`, kieruje zdarzenia do tej samej partycji, dzięki czemu Kafka zachowuje ich kolejność per agregat.
    - W praktyce zdarzenia event-sourcingowe powinny być zdarzeniami domenowymi, a nie technicznymi komunikatami typu "row updated". Dobre zdarzenie opisuje fakt biznesowy w czasie przeszłym, zawiera identyfikator agregatu, wersję zdarzenia, korelację/causation ID, timestamp i minimalny zestaw danych potrzebny do interpretacji faktu.
    - Kafka może pełnić rolę logu dystrybucyjnego dla zdarzeń, ale nie zawsze powinna być jedynym event storem. Trzeba świadomie dobrać retencję. Klasyczny Event Sourcing wymaga zachowania pełnej historii przez bardzo długi czas lub bezterminowo, więc zwykła retencja czasowa typu 7 dni łamie założenia wzorca. Często stosuje się długą retencję, archiwizację do storage'u obiektowego albo dedykowany event store plus publikację zdarzeń do Kafki.
    - **Log compaction** bywa przydatny do projekcji aktualnego stanu, np. topic `customer-current-state`, ale nie zastępuje pełnego event logu. Kompakcja usuwa stare wartości dla klucza, więc niszczy historię potrzebną do odtworzenia całej ścieżki zmian.
    - Typowe problemy projektowe: ewolucja schematów zdarzeń, idempotentne odtwarzanie projekcji, snapshoty dla przyspieszenia replayu, obsługa błędnych zdarzeń, wersjonowanie agregatów i rozdzielenie zdarzeń domenowych od integracyjnych. W Javie warto oprzeć kontrakty o Avro/Protobuf + Schema Registry i testy kompatybilności.

70. **Czym jest wzorzec CQRS (Command Query Responsibility Segregation) i jak Kafka wpasowuje się w tę architekturę?**
    - **CQRS** rozdziela model zapisu (commands/write model) od modelu odczytu (queries/read model). Część zapisowa waliduje intencję biznesową i zmienia stan domeny, a część odczytowa jest zoptymalizowana pod konkretne zapytania, widoki, raporty lub API.
    - Command nie jest zdarzeniem. Command to żądanie wykonania akcji, np. `PlaceOrderCommand`, które może zostać odrzucone. Event to fakt, który już zaszedł, np. `OrderPlaced`, i powinien być traktowany jako nieodwracalna informacja o zmianie.
    - Kafka jest naturalnym mechanizmem propagacji zmian z write modelu do wielu read modeli. Serwis domenowy po zaakceptowaniu komendy publikuje zdarzenie, a niezależni konsumenci budują projekcje w Elasticsearchu, Redisie, PostgreSQL, ClickHouse, cache'u lub materializowanych widokach.
    - Dzięki consumer groups jeden read model może być skalowany równolegle, a dzięki niezależnym grupom wiele projekcji może czytać ten sam strumień bez wpływania na siebie. Replay od wybranego offsetu pozwala odbudować projekcję po zmianie logiki albo utracie danych w magazynie odczytowym.
    - CQRS z Kafką jest zwykle **eventually consistent**. Po zapisie komendy odpowiedni widok odczytowy może być przez chwilę nieaktualny, bo konsument dopiero przetwarza zdarzenie. API musi to uwzględniać, np. przez status "processing", read-your-writes z lokalnego write modelu albo zwracanie identyfikatora operacji.
    - Kluczowe decyzje: granice bounded contextów, nazewnictwo topiców, klucz partycjonowania zgodny z agregatem, obsługa replayu bez efektów ubocznych, wersjonowanie eventów i idempotentne aktualizowanie projekcji. Projekcja nie powinna wysyłać maili ani wołać płatności podczas replayu, chyba że jest to jawnie kontrolowane.
    - Kafka Streams może budować read modele strumieniowo przez agregacje, joiny i state store'y. Dla prostych projekcji wystarczy zwykły consumer, dla złożonych agregacji, okien i przetwarzania stanowego Kafka Streams daje mniej kodu infrastrukturalnego.

71. **Czym jest Outbox Pattern i jak rozwiązuje problem dual write w mikroserwisach z Kafką?**
    - **Dual write** występuje, gdy serwis musi atomowo wykonać dwie operacje w różnych systemach, np. zapisać zamówienie w PostgreSQL i opublikować `OrderCreated` do Kafki. Jeśli zapis do bazy się uda, a publikacja do Kafki padnie, system ma niespójność. Jeśli najpierw wyślemy event, a potem rollbacknie się transakcja w bazie, inni konsumenci zobaczą zdarzenie dla stanu, który faktycznie nie istnieje.
    - **Outbox Pattern** rozwiązuje to przez zapis danych biznesowych i komunikatu do publikacji w jednej lokalnej transakcji bazy danych. W tej samej transakcji zapisujemy np. rekord w tabeli `orders` oraz rekord w tabeli `outbox_events`.
    - Osobny publisher czyta outbox i publikuje zdarzenia do Kafki. Po udanej publikacji oznacza rekord jako opublikowany, usuwa go albo zapisuje timestamp publikacji. Dzięki temu baza jest jedynym miejscem atomowego commitu, a Kafka jest aktualizowana asynchronicznie.
    - Najczęstsza implementacja w Javie/Springu: metoda aplikacyjna z `@Transactional` zapisuje agregat i encję outbox; scheduler, worker albo osobny proces pobiera nieopublikowane rekordy partiami z blokadą typu `SELECT ... FOR UPDATE SKIP LOCKED`; publikuje przez `KafkaTemplate`; po potwierdzeniu oznacza event jako wysłany.
    - Bardziej skalowalny wariant to CDC, np. Debezium. Aplikacja tylko zapisuje tabelę outbox, a connector czyta log transakcyjny bazy i publikuje eventy do Kafki. To redukuje kod publishera i dobrze działa przy dużym ruchu, ale dodaje zależność operacyjną od Kafka Connect/CDC.
    - Outbox zwykle daje **at-least-once delivery**, nie exactly-once dla całego świata. Publisher może opublikować event, a potem paść przed oznaczeniem rekordu jako wysłany. Po restarcie opublikuje go ponownie. Dlatego event musi mieć stabilne `eventId`, a konsumenci muszą być idempotentni.
    - Dobre praktyki: unikalny identyfikator eventu, typ eventu, wersja schematu, aggregate ID jako Kafka key, payload w kontrolowanym formacie, metadane korelacyjne, retry z backoffem, monitoring wieku najstarszego wpisu w outboxie i proces czyszczenia starych opublikowanych rekordów.

72. **Czym jest Saga Pattern i jak Kafka pomaga w orkiestracji/choreografii transakcji rozproszonych?**
    - **Saga Pattern** to sposób modelowania długiej transakcji biznesowej, która obejmuje wiele mikroserwisów bez jednej globalnej transakcji ACID. Każdy krok ma lokalną transakcję, a w razie błędu wykonuje się akcje kompensujące.
    - Przykład: złożenie zamówienia wymaga rezerwacji płatności, rezerwacji towaru i zlecenia wysyłki. Jeśli rezerwacja magazynowa się nie uda, serwis płatności musi dostać polecenie anulowania autoryzacji. Nie robimy 2PC między bazami, tylko modelujemy proces jawnie.
    - W wariancie **choreografii** nie ma centralnego koordynatora. Serwisy reagują na zdarzenia z Kafki: `OrderCreated` powoduje `PaymentReserved`, to powoduje `InventoryReserved`, potem `ShipmentRequested`. Błąd publikuje event typu `InventoryReservationFailed`, na który inne serwisy reagują kompensacją.
    - Choreografia dobrze skaluje się organizacyjnie i technicznie, ale przy wielu krokach trudniej zrozumieć cały proces. Logika przepływu jest rozproszona po serwisach, więc potrzebne są dobre nazwy eventów, korelacja, tracing i dokumentacja kontraktów.
    - W wariancie **orkiestracji** istnieje centralny orchestrator/process manager, który zna stan sagi i wysyła komendy do kolejnych serwisów, np. `ReservePayment`, `ReserveInventory`, `CancelPayment`. Kafka przenosi komendy i odpowiedzi, a orchestrator przechowuje stan procesu w bazie, Kafka Streams state store albo innym trwałym magazynie.
    - Orkiestracja daje czytelny model procesu i łatwiejsze time-outy, retry oraz kompensacje, ale tworzy komponent centralny, który trzeba skalować i utrzymywać. Dla krytycznych procesów biznesowych często jest bardziej czytelna niż czysta choreografia.
    - Kafka pomaga przez trwały log zdarzeń, retry, consumer groups, zachowanie kolejności per klucz sagi, możliwość replayu i integrację z outboxem. Klucz wiadomości powinien zwykle być `sagaId` albo `aggregateId`, żeby zdarzenia danej sagi zachowały kolejność.
    - Trzeba projektować idempotencję, bo retry i duplikaty są normalne. Każdy krok sagi powinien tolerować ponowne otrzymanie tej samej komendy/eventu, a kompensacja powinna być semantycznie bezpieczna, np. anulowanie już anulowanej rezerwacji nie może wywrócić procesu.

73. **Jak zaimplementować Dead Letter Queue (DLQ) w Kafce? Kiedy jest to potrzebne?**
    - **DLQ** to osobny topic, do którego trafiają wiadomości, których konsument nie potrafi poprawnie przetworzyć po określonej liczbie prób albo z powodu błędu nieretryowalnego. Celem jest odblokowanie głównego strumienia bez utraty problematycznych danych.
    - DLQ jest potrzebny przy błędach deserializacji, niekompatybilnych schematach, brakujących polach wymaganych przez logikę, niepoprawnych danych domenowych, permanentnych błędach walidacji albo sytuacji, w której dalsze retry nie ma sensu.
    - Typowa implementacja: konsument pobiera rekord, wykonuje przetwarzanie w bloku `try/catch`, klasyfikuje wyjątek jako retryowalny albo nieretryowalny, dla retryowalnych stosuje ograniczoną liczbę prób z backoffem, a po przekroczeniu limitu publikuje rekord do topicu DLQ i dopiero wtedy commituje offset oryginalnej wiadomości.
    - Rekord w DLQ powinien zawierać oryginalny key, value, topic, partition, offset, timestamp, headers oraz metadane błędu: klasę wyjątku, komunikat, stack trace w rozsądnym limicie, nazwę aplikacji, wersję konsumenta i czas trafienia do DLQ. W Kafka headers można przenieść techniczne metadane, a payload zostawić możliwie blisko oryginału.
    - Nazewnictwo DLQ powinno być przewidywalne, np. `orders.events.dlq`, `orders.events.retry.5m`, `orders.events.retry.1h`. Retry topics są często lepsze niż blokowanie partycji przez `Thread.sleep`, bo pozwalają zachować przepustowość konsumenta.
    - W Spring Kafka można użyć `DefaultErrorHandler`, `DeadLetterPublishingRecoverer`, `BackOff` i `ErrorHandlingDeserializer`. Ważne jest, aby błędy deserializacji obsłużyć jeszcze przed logiką listenera, bo zwykły listener może nawet nie dostać poprawnego obiektu.
    - DLQ nie jest śmietnikiem bez właściciela. Musi mieć monitoring liczby wiadomości, alerty, retencję, proces reprocessingu i reguły bezpieczeństwa danych. W przeciwnym razie tylko ukrywa problemy produkcyjne.
    - Trzeba uważać na kolejność. Jeśli wymagamy ścisłego orderingu per klucz, pominięcie jednego eventu do DLQ i przetworzenie następnych może złamać semantykę domenową. Wtedy lepiej zatrzymać przetwarzanie danego klucza/agregatu, użyć parking lot topic albo ręcznej interwencji.

74. **Czym jest wzorzec Request-Reply w Kafce? Jak go zaimplementować i kiedy ma sens?**
    - **Request-Reply** w Kafce symuluje synchroniczny styl komunikacji na asynchronicznym brokerze. Jeden serwis publikuje request do topicu, drugi go przetwarza i publikuje odpowiedź do topicu reply. Klient koreluje odpowiedź z żądaniem przez `correlationId`.
    - Implementacja wymaga co najmniej topicu request, topicu reply, unikalnego `correlationId`, timeoutu oczekiwania, mapy oczekujących odpowiedzi po stronie requester'a oraz ustalonego kontraktu odpowiedzi sukces/błąd. Często w headers dodaje się `replyTo`, `correlationId`, `requesterId`, `traceId`.
    - W Javie można to zbudować na `KafkaTemplate` + osobny `@KafkaListener` dla odpowiedzi, przechowując `CompletableFuture` w mapie po `correlationId`. W Spring Kafka istnieje też `ReplyingKafkaTemplate`, który opakowuje ten mechanizm.
    - Reply topic może być wspólny dla instancji albo dedykowany per serwis/instancja. Przy wspólnym topicu trzeba zadbać, aby odpowiedź trafiła do instancji, która czeka na dany `correlationId`, np. przez partycjonowanie, assignment albo filtrowanie nie swoich odpowiedzi. Przy dedykowanych reply topicach rośnie liczba topiców i obciążenie operacyjne.
    - Wzorzec ma sens, gdy chcemy zachować komunikację przez Kafkę ze względów infrastrukturalnych, audytowych, bezpieczeństwa albo rozłączenia temporalnego, ale potrzebujemy odpowiedzi w ograniczonym czasie. Przykład: zapytanie do systemu scoringowego, który naturalnie działa jako konsument Kafki.
    - Nie należy nadużywać Request-Reply jako zamiennika HTTP/gRPC dla typowych niskolatencyjnych zapytań online. Kafka dodaje narzut brokera, kolejkowania, pollingu i rebalancingu. Jeśli potrzebna jest prosta, natychmiastowa odpowiedź i brak wartości z trwałego logu, REST/gRPC zwykle jest prostsze.
    - Trzeba zaprojektować timeouty, retry, idempotencję requestów i odpowiedzi spóźnione. Odpowiedź może przyjść po timeoutcie, requester może już nie istnieć, a retry requestu może spowodować podwójne wykonanie operacji po stronie respondera.

75. **Jak projektować topiki Kafki — jeden duży topic vs wiele małych? Jakie są trade-offy?**
    - Topic powinien zwykle reprezentować spójny strumień zdarzeń o wspólnym kontrakcie, semantyce, właścicielu, retencji, wymaganiach bezpieczeństwa i sposobie partycjonowania. Nie projektuje się topiców wyłącznie pod klasę Javy ani pod każdy endpoint API.
    - **Jeden duży topic** upraszcza liczbę zasobów i może mieć sens, gdy zdarzenia mają wspólny model, podobną retencję i ci sami konsumenci czytają większość danych. Daje prostszy routing produkcji i mniej topiców do administracji.
    - Wady jednego dużego topicu: konsumenci muszą filtrować niepotrzebne zdarzenia, trudniej dobrać retencję i ACL dla różnych typów danych, rośnie ryzyko niekontrolowanej ewolucji schematu, a błędny producent może zakłócić wiele przypadków użycia. Przy wielu typach zdarzeń w jednym topicu trzeba mieć mocną strategię envelope'a i wersjonowania.
    - **Wiele małych topiców** daje lepszą izolację domenową, osobne ACL, retencję, kompakcję, liczbę partycji, właścicieli i metryki. Konsument subskrybuje dokładnie to, czego potrzebuje, a kontrakt topicu jest czytelniejszy.
    - Wady wielu topiców: większy koszt operacyjny, więcej metadanych w klastrze, więcej partycji do zarządzania, potencjalnie więcej małych plików segmentów, trudniejsza obserwowalność i większe ryzyko chaotycznego nazewnictwa. Zbyt wiele topiców z małym ruchem może niepotrzebnie obciążać kontrolerów i brokerów.
    - Kryteria projektowe: bounded context, właściciel danych, typ danych osobowych i ACL, retencja, potrzeba log compaction, wymagany ordering, wolumen, liczba konsumentów, kompatybilność schematu, SLA i sposób reprocessingu.
    - Częsty kompromis: topic per rodzina zdarzeń domenowych, np. `orders.events`, z kilkoma typami zdarzeń w kontrolowanym envelope, albo topic per ważny agregat/strumień, np. `orders`, `payments`, `shipments`. Nie miesza się zdarzeń o kompletnie innych wymaganiach retencji i bezpieczeństwa tylko dlatego, że technicznie da się je zserializować do JSON.
    - Przy projektowaniu trzeba pamiętać, że zwiększenie liczby partycji jest możliwe, ale może zmienić mapowanie kluczy do partycji i wpłynąć na ordering względem historycznych danych. Zmniejszenie liczby partycji nie jest wspierane bez utworzenia nowego topicu i migracji.

76. **Jak obsługiwać poison pill (zatrutą wiadomość), która blokuje konsumenta?**
    - **Poison pill** to wiadomość, która deterministycznie powoduje błąd przetwarzania i przez to blokuje konsumenta na tym samym offsetcie. Może wynikać z uszkodzonego payloadu, niezgodnego schematu, błędu domenowego, nieobsłużonego edge case'u albo błędu w kodzie konsumenta.
    - Najgorszy wariant to nieskończony retry bez commitu offsetu. Konsument po każdej próbie wraca do tej samej wiadomości, lag rośnie, a kolejne poprawne rekordy z tej partycji nie są przetwarzane.
    - Pierwszy krok to klasyfikacja błędu. Błędy przejściowe, np. timeout zależnej usługi, powinny iść w retry z backoffem. Błędy permanentne, np. brak wymaganego pola albo nieznany typ eventu, powinny trafić do DLQ/parking lot po ograniczonej liczbie prób.
    - Bezpieczny algorytm: przetwórz rekord; jeśli sukces, commit offset; jeśli błąd retryowalny, ponów z limitem i backoffem albo przenieś do retry topic; jeśli limit wyczerpany lub błąd nieretryowalny, opublikuj oryginalny rekord z metadanymi błędu do DLQ; po potwierdzonej publikacji do DLQ commituj offset źródłowy.
    - Dla błędów deserializacji trzeba obsłużyć problem przed kodem biznesowym. W Spring Kafka służy do tego `ErrorHandlingDeserializer`, bo inaczej listener może nie dostać rekordu i aplikacja będzie zapętlać się na poziomie poll/deserialization.
    - Jeżeli kolejność per klucz jest krytyczna, automatyczne "przeskoczenie" poison pilla może być błędne. Przykładowo nie wolno przetworzyć `OrderShipped`, jeśli `OrderPaid` dla tego samego `orderId` trafiło do DLQ. Wtedy stosuje się blokadę konkretnego agregatu, parking lot topic, ręczną naprawę danych albo reprocessing po poprawce.
    - Konsument powinien być idempotentny, bo poison pill często ujawnia się razem z retry i częściowo wykonanymi efektami ubocznymi. Zapis do bazy, wywołanie API czy wysłanie maila powinny być chronione przez deduplikację, klucze idempotencji albo transakcyjne aktualizacje stanu.
    - Operacyjnie potrzebne są metryki i alerty: liczba błędów per typ wyjątku, tempo DLQ, najstarsza wiadomość w DLQ, lag partycji, liczba retry i czas przetwarzania. Dobrą praktyką jest procedura replayu z DLQ po poprawce kodu lub danych, zamiast ręcznego kopiowania rekordów bez kontroli.

---

## 10. Gwarancje dostarczenia i semantyka

77. Opisz trzy semantyki dostarczenia wiadomości: at-most-once, at-least-once, exactly-once. Jak je osiągnąć w Kafce?
78. Czym jest exactly-once semantics (EOS) w Kafce i jak działa end-to-end (producent → Kafka → konsument)?
79. Jak realizować idempotentność po stronie konsumenta, gdy nie używamy EOS?
80. Czym jest transakcja w Kafce? Jak działa `beginTransaction()`, `commitTransaction()`, `abortTransaction()`?
81. Czym jest `isolation.level` (`read_committed` vs `read_uncommitted`) po stronie konsumenta?
82. Jak Kafka gwarantuje trwałość danych? Co się dzieje, gdy leader partycji ulegnie awarii?

---

## 11. Operacje i administracja

83. Jak dodać nowe brokery do klastra Kafka bez przestoju?
84. Jak przeprowadzić rebalancing partycji między brokerami (partition reassignment)?
85. Jak zwiększyć liczbę partycji istniejącego topicu? Jakie są konsekwencje?
86. Czy można zmniejszyć liczbę partycji topicu? Dlaczego?
87. Jak przeprowadzić rolling upgrade klastra Kafka?
88. Czym jest unclean leader election i dlaczego domyślnie jest wyłączona?
89. Jak debugować lag konsumenta? Jakie narzędzia do tego służą (kafka-consumer-groups.sh, Burrow, Kafka UI)?
90. Czym jest rack awareness w Kafce i jak wpływa na rozmieszczenie replik?

---

## 12. Kafka w ekosystemie Java / Spring

91. Jak działa Spring Kafka (`spring-kafka`)? Czym jest `KafkaTemplate` i `@KafkaListener`?
92. Jak skonfigurować Spring Kafka z obsługą retry i DLQ?
93. Czym jest `ConcurrentKafkaListenerContainerFactory` i jak konfigurować współbieżność konsumentów w Springu?
94. Jak obsługiwać deserializację błędnych wiadomości w Spring Kafka (`ErrorHandlingDeserializer`)?
95. Jak testować integrację z Kafką w Javie (Embedded Kafka, Testcontainers)?
96. Jak skonfigurować transakcje Kafki w Spring Boot (`@Transactional` + `KafkaTransactionManager`)?

---

## 13. Scenariusze problemowe i debugging

97. Konsument wykazuje rosnący lag — jakie mogą być przyczyny i jak to rozwiązać?
98. Producent zgłasza `TimeoutException` — co mogło pójść nie tak?
99. Wiadomości pojawiają się w niewłaściwej kolejności — jakie mogą być przyczyny?
100. Po restarcie konsumenta przetwarza on ponownie wiadomości — dlaczego i jak temu zapobiec?
101. Rebalancing consumer group trwa zbyt długo i powoduje przestoje — jak to zoptymalizować?
102. Klaster Kafka ma problem z „under-replicated partitions" — jak diagnozować i naprawić?
103. Producent wysyła duplikaty wiadomości — jak je wykrywać i eliminować?
104. Aplikacja Kafka Streams wpadła w pętlę restartów — jakie mogą być przyczyny?

---

## Powiązane materiały

- [Kafka Streams — Podstawy](kafka-streams.md)
- [Pytania Rekrutacyjne — Java (Senior)](pytania-rekrutacyjne-java-senior.md)
- [Pytania Rekrutacyjne — Spring 3.0](pytania-rekrutacyjne-spring-3-0.md)
- [Mikroserwisy: Pytania Rekrutacyjne](../SystemDesign/mikroserwisy-pytania-rekrutacyjne.md)
