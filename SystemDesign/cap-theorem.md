# Twierdzenie CAP (CAP Theorem)

## Krótkie podsumowanie
Twierdzenie CAP (znane również jako twierdzenie Brewera) mówi, że w rozproszonym systemie przechowującym dane nie da się zagwarantować jednocześnie trzech właściwości:
*   **Consistency (Spójność):** Każdy odczyt zwraca najnowszy zapis albo błąd (wszystkie węzły widzą te same dane w tym samym czasie).
*   **Availability (Dostępność):** Każde żądanie (niezakończone awarią węzła) otrzymuje odpowiedź (niekoniecznie zawierającą najnowszy zapis).
*   **Partition tolerance (Odporność na podział):** System działa nadal mimo utraty lub opóźnienia komunikacji między węzłami (sieć ulega podziałowi).

Zgodnie z twierdzeniem CAP, system rozproszony może w pełni zagwarantować najwyżej **dwie z tych trzech** właściwości jednocześnie.

## Dlaczego to ma znaczenie / Kiedy to stosować?
Zrozumienie CAP jest kluczowe podczas projektowania systemów rozproszonych i wyboru baz danych. Pomaga architektom podjąć świadomą decyzję o tym, z czego zrezygnować w przypadku awarii sieci (network partition). Decyzja ta wpływa bezpośrednio na architekturę (wybór np. między relacyjnymi bazami SQL gwarantującymi spójność a bazami NoSQL stawiającymi na dostępność).

## Jak to działa w systemach rozproszonych (Kombinacje CA, CP, AP)

Najczęstszym pytaniem dotyczącym twierdzenia CAP jest to, czy można dowolnie wybrać dwie z trzech właściwości (CA, CP, AP). Odpowiedź brzmi: **NIE w przypadku systemów rozproszonych.**

W prawdziwym systemie rozproszonym **podziały sieci (Partition) są nieuniknione**. Połączenia sieciowe zawsze mogą ulec awarii, wiadomości mogą zostać zgubione lub opóźnione. Ponieważ musimy założyć, że "P" nastąpi, tak naprawdę wybieramy tylko między **C** (Spójność) a **A** (Dostępność) w momencie wystąpienia awarii sieci.

*   **CP (Consistency + Partition Tolerance):** System stawia na spójność. W przypadku podziału sieci, węzły, które nie mogą się skomunikować, aby zapewnić spójność danych, przestaną przyjmować żądania zapisu (a czasem i odczytu), zgłaszając błąd (brak dostępności), dopóki sieć nie wróci do normy.
    *   *Przykłady:* MongoDB, HBase, Redis (w niektórych konfiguracjach). Używane m.in. w systemach finansowych, gdzie np. stan konta musi być precyzyjny.
*   **AP (Availability + Partition Tolerance):** System stawia na dostępność. W przypadku podziału sieci wszystkie węzły nadal obsługują żądania, ale z powodu braku komunikacji mogą zwracać nieaktualne (niespójne) dane. System polega na "ostatecznej spójności" (eventual consistency) — zsynchronizuje się, gdy sieć powróci.
    *   *Przykłady:* Cassandra, DynamoDB, CouchDB. Używane m.in. w mediach społecznościowych (wyświetlenie starszego komentarza jest akceptowalne, ale błąd całej strony - nie).
*   **CA (Consistency + Availability):** System zapewnia spójność i dostępność, ale **nie** jest odporny na podziały sieci. Taka sytuacja jest możliwa **tylko w systemach nierozproszonych** (np. pojedyncza instancja relacyjnej bazy danych działająca na jednym serwerze). Zatem w prawdziwych architekturach rozproszonych, kombinacja CA teoretycznie nie istnieje jako opcja przy projektowaniu.

## Powiązane pliki
*   [Kiedy stosować bazy SQL a kiedy NoSQL?](sql-vs-nosql-criteria.md)
*   [Pytania rekrutacyjne z System Design](system-design-pytania-rekrutacyjne.md)
