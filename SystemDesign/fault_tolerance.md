# Fault Tolerance – jak budować systemy odporne na awarie?

W dzisiejszym cyfrowym świecie przerwy w działaniu systemów informatycznych oznaczają nie tylko straty finansowe, ale i ogromny uszczerbek na wizerunku. W zależności od charakteru systemu, awaria może skutkować przerwaniem ważnych transakcji, paraliżem łańcucha dostaw, a w skrajnych przypadkach – zagrożeniem życia. Właśnie dlatego inżynierowie i architekci tak dużą wagę przykładają do tworzenia rozwiązań odpornych na błędy. Odpowiedzią na to wyzwanie jest **Fault Tolerance**.

W tym artykule przyjrzymy się, czym jest tolerancja na błędy, w jaki sposób odróżnić ją od High Availability oraz jak zaprojektować architekturę, która przetrwa niemal wszystko.

## 1. Czym jest Fault Tolerance?

**Fault Tolerance (FT)**, czyli tolerancja na błędy, to właściwość systemu informatycznego, która pozwala mu na nieprzerwane i poprawne działanie, nawet jeśli jeden lub więcej jego komponentów (sprzętowych lub oprogramowania) ulegnie awarii. Z perspektywy użytkownika końcowego wystąpienie błędu w systemie fault-tolerant jest całkowicie niezauważalne – aplikacja po prostu działa dalej, bez żadnych opóźnień czy komunikatów o błędach.

W architekturze chmurowej i rozproszonej awarie nie są kwestią "czy", ale "kiedy". Dyski się psują, instancje wirtualne znikają z powodu braku zasobów, a sieć bywa zawodna. Budowanie systemów Fault Tolerant polega na założeniu z góry, że elementy infrastruktury będą ulegać uszkodzeniu, i zaprojektowaniu całości tak, aby te incydenty omijać bez przerywania pracy całości.

## 2. Fault Tolerance a High Availability – krótkie rozróżnienie

Pojęcia te często bywają używane zamiennie, jednak w świecie inżynierii oznaczają coś zupełnie innego. 

* **High Availability (HA – Wysoka Dostępność):** Celem HA jest minimalizacja czasu przestoju. Gdy nastąpi awaria serwera, ruch jest kierowany na inny serwer. Może to jednak zająć od kilku sekund do kilku minut, w trakcie których użytkownicy mogą odczuć przerwę w działaniu, zobaczyć błąd 503 lub zostać wylogowani. System ostatecznie szybko "wstaje".
* **Fault Tolerance (FT):** Zapewnia **brak jakichkolwiek przerw**. Jeśli serwer A przestaje działać, serwer B płynnie i natychmiastowo przejmuje jego zadania. Użytkownik, który akurat klikał w przycisk na stronie, nie odczuje żadnego błędu ani opóźnienia.

**Przykład z życia:** 
Wyobraź sobie przebitą oponę w samochodzie podczas jazdy.
* **Wysoka Dostępność (HA):** Zjeżdżasz na pobocze, wyciągasz z bagażnika koło zapasowe, zmieniasz je i jedziesz dalej. Nastąpiła krótka przerwa w podróży, ale szybko wznowiłeś działanie.
* **Fault Tolerance (FT):** Masz założone opony typu *run-flat*. Przebijasz oponę, ale system nośny opony pozwala Ci jechać dalej bez zatrzymywania się. Nie ma żadnej przerwy w podróży.

## 3. Kluczowe mechanizmy i koncepcje

Zapewnienie tolerancji na awarie wymaga połączenia kilku kluczowych mechanizmów:

### Redundancja (nadmiarowość)
Jest to absolutna podstawa FT. Polega na zapewnieniu zapasowych komponentów, które mogą przejąć pracę w przypadku awarii elementów podstawowych. Redundancja może występować na wielu poziomach:
* **Sprzętowym:** nadmiarowe dyski (macierze RAID), zasilacze (np. dwa podpięte do różnych źródeł), podwójne przełączniki sieciowe.
* **Oprogramowania i infrastruktury:** uruchamianie aplikacji na kilku niezależnych serwerach jednocześnie (klastrowanie).

### Replikacja
Aby węzeł zapasowy mógł natychmiastowo przejąć pracę, musi posiadać te same dane, co węzeł uszkodzony. Replikacja polega na ciągłym, synchronicznym lub asynchronicznym kopiowaniu danych i stanu aplikacji pomiędzy serwerami. Często stosuje się tu model *Active-Active* (gdzie oba węzły jednocześnie obsługują ruch i synchronizują dane), co jest fundamentem rozwiązań FT.

### Failover i Failback
* **Failover:** to proces automatycznego i bezprzerwowego przełączenia ruchu z uszkodzonego komponentu na zapasowy.
* **Failback:** to powrotne przełączenie ruchu na podstawowy komponent po tym, jak awaria zostanie naprawiona. Systemy FT wykonują te operacje w tle, w sposób przezroczysty dla użytkownika.

### Checkpointing i Rollback
W niektórych przypadkach (np. w systemach przetwarzania wielkich zbiorów danych) system regularnie zapisuje "migawki" swojego stanu (tzw. punkty kontrolne – checkpoints). W razie awarii aplikacja nie zaczyna pracy od zera, lecz wczytuje ostatni poprawny punkt kontrolny (rollback) i kontynuuje działanie od tego momentu.

## 4. Strategie i wzorce projektowe 

Z punktu widzenia projektanta (System Design), aby system był Fault Tolerant, musimy zaimplementować odpowiednie wzorce w architekturze:

* **Eliminacja SPOF (Single Point of Failure):** Pierwszym krokiem do FT jest audyt systemu w poszukiwaniu "pojedynczych punktów awarii". Jeśli cały ruch w systemie przechodzi przez jeden load balancer lub zapisuje do jednej instancji bazy danych, jest to SPOF. Jego awaria kładzie cały system. Aby pozbyć się SPOF, należy zwielokrotnić każdy element na ścieżce żądania.
* **Circuit Breaker (Bezpiecznik):** Wzorzec znany z architektury mikroserwisów. Zabezpiecza przed kaskadowymi awariami. Jeżeli jeden serwis przestaje odpowiadać na czas, bezpiecznik "odcina" połączenia do niego i zwraca domyślną wartość lub komunikat błędu natychmiastowo. Zapobiega to przeciążaniu reszty infrastruktury wiszącymi żądaniami.
* **Bulkhead Pattern (Grodzie):** Wzorzec zapożyczony z budowy statków. Statek podzielony jest na szczelne przedziały (grodzie). Jeśli statek nabiera wody, tonie tylko jeden przedział, ratując resztę statku. W IT oznacza to podział zasobów (np. puli wątków bazy danych) na niezależne sekcje przypisane różnym klientom, tak by przeciążenie jednego modułu nie wpłynęło na inne.
* **Graceful Degradation (Łagodna degradacja):** W momencie wystąpienia awarii częściowej, system zamiast wyświetlać błąd 500, ukrywa niedziałające moduły, pozostawiając kluczowe funkcje aktywne. Jeśli w sklepie internetowym padnie silnik rekomendacji, klient nie zobaczy polecanych produktów, ale nadal będzie mógł dodać coś do koszyka i opłacić zamówienie.

## 5. Wyzwania i koszty – dlaczego FT nie jest wszędzie?

Skoro tolerancja na błędy jest tak wspaniała, dlaczego nie każda aplikacja jest projektowana w ten sposób? Odpowiedź sprowadza się głównie do trzech czynników:

1. **Wysokie koszty infrastruktury:** Zapewnienie Fault Tolerance oznacza de facto, że musisz opłacać i utrzymywać podwójną lub potrójną infrastrukturę (serwery, dyski, bazy danych), z której część może stać bezczynnie i czekać na awarię, lub działać z ogromnym naddatkiem zasobów.
2. **Znaczna złożoność (Complexity):** Systemy w pełni Fault Tolerant są niezwykle trudne w zaprojektowaniu, kodowaniu i wdrażaniu. Utrzymanie spójności danych przy replikacji synchronicznej w systemach rozproszonych to potężne wyzwanie inżynieryjne. Bardzo trudne staje się również testowanie (korzysta się m.in. z narzędzi *Chaos Engineering*, które losowo ubijają serwery na produkcji, by sprawdzać odporność architektury).
3. **Narzut wydajnościowy:** Mechanizmy gwarantujące stuprocentową pewność danych (np. rozproszone transakcje i konsensus) potrafią zauważalnie wpłynąć na wydajność. Zanim system zwróci informację "sukces", musi upewnić się, że dane zostały bezpiecznie zapisane na kilku fizycznych węzłach.

## 6. Gdzie Fault Tolerance to absolutna konieczność?

Ze względu na koszty i stopień skomplikowania, FT wdraża się tylko w systemach, w których jakikolwiek przestój lub utrata transakcji niosą za sobą katastrofalne skutki. Przykłady obejmują:

* **Systemy finansowe i giełdowe:** Transakcje, w których liczą się ułamki sekund, a przerwa może oznaczać straty rzędu milionów dolarów.
* **Kontrola lotów i systemy wbudowane w samolotach:** Awaria radaru lub systemów nawigacji na czas "ponownego uruchomienia" (High Availability) byłaby tragiczna w skutkach. Wymagana jest bezprzerwowa redundancja.
* **Urządzenia medyczne i systemy podtrzymywania życia:** Ułamek sekundy przerwy zasilania lub błąd oprogramowania w aparaturze może kosztować ludzkie życie.
* **Wojsko i przemysł kosmiczny:** Zespoły NASA projektujące oprogramowanie sond kosmicznych polegają na ekstremalnej redundancji komponentów (tzw. n-modular redundancy).

## Podsumowanie

Fault Tolerance to wyższa szkoła jazdy w projektowaniu systemów IT. Stanowi ewolucję pojęcia High Availability, oferując użytkownikowi w pełni przezroczyste ominięcie jakiejkolwiek awarii. Projektowanie takich systemów wymaga ogromnej wiedzy architektonicznej (eliminacja SPOF, replikacja, grodzie) i wiąże się ze znacznymi kosztami.

Dla zdecydowanej większości biznesowych aplikacji internetowych i SaaS-ów, dobrze zaprojektowane High Availability (gwarantujące np. 99.99% czasu działania) jest w zupełności wystarczające i znacznie bardziej opłacalne. Jednak tam, gdzie stawką są gigantyczne pieniądze lub ludzkie życie, bezwzględna odporność na awarie (Fault Tolerance) jest jedynym słusznym wyborem.
