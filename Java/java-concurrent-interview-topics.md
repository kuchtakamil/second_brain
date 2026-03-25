# Java Concurrent Interview Topics.

**Data:** 2023-04-23

---

**User:**

Wymień tematy na interview dotyczące java concurrent. Pomiń wait i notify.

---

**Assistant:**

Oto kilka przykładowych tematów na rozmowę kwalifikacyjną dotyczącą Java Concurrent, z pominięciem wait i notify:

1. Co to jest "concurrency" i jakie są sposoby jej realizacji w Javie?
2. Co to jest "race condition"? Jakie są sposoby na zapobieganie temu zjawisku?
3. Jakie mechanizmy Java oferuje do synchronizacji dostępu do danych między wątkami?
4. Co to jest "thread pool" i jakie są zalety jego użycia w porównaniu z tworzeniem wątków "na żądanie"?
5. Jakie są różnice między synchronizacją wątków za pomocą "synchronized" a biblioteki "java.util.concurrent.locks"?
6. Co to jest "volatile" i jakie są jego zastosowania?
7. Co to jest "atomic variable" i jakie są jego zastosowania?
8. Co to jest "concurrent collection" i jakie są różnice między nimi a zwykłymi kolekcjami Javy?
9. Co to jest "deadlock" i jakie są sposoby na zapobieganie temu zjawisku?
10. Jakie są różnice między "Thread" a "Runnable"?

---

**User:**

Jakie mechanizmy Java oferuje do synchronizacji dostępu do danych między wątkami?

---

**Assistant:**

Java oferuje kilka mechanizmów do synchronizacji dostępu do danych między wątkami, w tym:

1. Słowo kluczowe "synchronized": pozwala na zabezpieczenie bloku kodu lub metody, dzięki czemu tylko jeden wątek może mieć do niego dostęp w danym momencie. Dzięki temu unika się wyścigów (race conditions) i synchronizuje dostęp do współdzielonych danych.

2. Klasa "ReentrantLock": oferuje bardziej elastyczne mechanizmy synchronizacji, niż słowo kluczowe "synchronized", dzięki czemu jest bardziej odpowiednia w bardziej zaawansowanych scenariuszach. Oferuje możliwość przerwania wątku oczekującego na dostęp do zasobu (interaptible locking), zaawansowane mechanizmy blokowania i odblokowania, a także możliwość wykrywania i zapobiegania zakleszczeniom.

3. Klasa "Semaphore": pozwala na kontrolowanie dostępu do zasobów, np. poprzez limitowanie liczby wątków, które mogą korzystać z danego zasobu jednocześnie.

4. Klasa "CountDownLatch": pozwala na synchronizację działań wielu wątków poprzez oczekiwanie na wykonanie określonej liczby zdarzeń.

5. Klasa "CyclicBarrier": pozwala na synchronizację wielu wątków, tak żeby wszystkie wątki czekały na siebie nawzajem, zanim kontynuują swoje działania.

6. Klasa "Phaser": umożliwia synchronizację działania wielu wątków poprzez podzielenie ich na etapy i kontrolowanie, które wątki mogą przechodzić do kolejnych etapów.

7. Klasa "Exchanger": pozwala na wymianę danych między dwoma wątkami, co może być przydatne w niektórych scenariuszach, np. w przetwarzaniu strumieniowym.

Te mechanizmy umożliwiają programistom w Javie synchronizowanie dostępu do danych między wątkami i unikanie wyścigów (race conditions) i innych problemów związanych z jednoczesnym dostępem do zasobów.

---

**User:**

Jakie są różnice między synchronizacją wątków za pomocą "synchronized" a biblioteki "java.util.concurrent.locks"?

---

**Assistant:**

Synchronizacja wątków za pomocą słowa kluczowego "synchronized" a biblioteki "java.util.concurrent.locks" mają wiele podobieństw, ale istnieją też pewne różnice.

Oto kilka z tych różnic:

1. Zakres synchronizacji: Słowo kluczowe "synchronized" synchronizuje cały blok kodu lub całą metodę. W przypadku biblioteki "java.util.concurrent.locks" programista może wybrać zakres synchronizacji - może to być blok kodu, metoda lub nawet pojedyncza zmienna.

2. Typ blokady: "synchronized" wykorzystuje blokadę wewnętrzną, a biblioteka "java.util.concurrent.locks" umożliwia użycie różnych rodzajów blokad - np. blokady wspinaczkowej (spinlock), blokady z uśpieniem (sleep lock), itp.

3. Wyjątki: W przypadku "synchronized" wyjątki są automatycznie propagowane do wywołującego, co może prowadzić do trudnych do zdiagnozowania błędów. W bibliotece "java.util.concurrent.locks" wyjątki są przechwytywane i obsługiwane przez programistę, co ułatwia diagnostykę błędów.

4. Przerwanie wątków: Biblioteka "java.util.concurrent.locks" umożliwia przerwanie wątków czekających na blokadę, co może być przydatne w niektórych scenariuszach. Słowo kluczowe "synchronized" nie oferuje takiej możliwości.

5. Właściciel blokady: W przypadku "synchronized" blokada jest automatycznie zwalniana, gdy wątek, który ją zajął, kończy swoje działanie. W bibliotece "java.util.concurrent.locks" blokada może być zwalniana przez dowolny wątek, który posiada referencję do niej.

6. Wydajność: W niektórych przypadkach użycie biblioteki "java.util.concurrent.locks" może być bardziej wydajne niż "synchronized", zwłaszcza gdy wiele wątków konkurruje o dostęp do tych samych zasobów. To wynika z faktu, że biblioteka umożliwia bardziej elastyczną i efektywną synchronizację wątków.

Podsumowując, oba mechanizmy synchronizacji wątków - "synchronized" i biblioteka "java.util.concurrent.locks" - mają swoje zalety i wady. Ostatecznie wybór między nimi zależy od specyfiki danego projektu i konkretnych wymagań dotyczących synchronizacji dostępu do danych.

---

**User:**

Co to jest "atomic variable" i jakie są jego zastosowania?

---

**Assistant:**

"Atomic variable" to specjalny typ zmiennej w programowaniu wielowątkowym, który zapewnia atomowość operacji na tej zmiennej. Oznacza to, że operacja na "atomic variable" jest niepodzielna - wątki wykonujące tę operację nie są w stanie przerwać jej wykonania w połowie, co zapewnia spójność danych.

W Javie, klasa "java.util.concurrent.atomic.Atomic" zawiera kilka klas, które umożliwiają tworzenie atomowych zmiennych, takich jak AtomicBoolean, AtomicInteger, AtomicLong itp.

Zastosowanie "atomic variable" jest szerokie i obejmuje wiele przypadków, w których wiele wątków konkurruje o dostęp do współdzielonych zasobów. Przykłady zastosowań to:

1. Liczniki: w przypadku gdy wiele wątków wykonuje inkrementację lub dekrementację zmiennej licznika, atomowe operacje na AtomicLong lub AtomicInteger zapewniają spójność licznika.

2. Flagi: flagi takie jak AtomicBoolean, zapewniają spójność flagi, która może być zmieniana przez wiele wątków.

3. Cache: Atomowe zmienne są używane w niektórych implementacjach cache do zarządzania dostępem do danych w pamięci podręcznej. W takim przypadku, jeśli wiele wątków próbuje pobrać wartość z pamięci podręcznej, atomowe operacje zapewniają, że tylko jeden wątek będzie miał dostęp do danych w pamięci podręcznej.

4. Synchronizacja: Atomowe zmienne są wykorzystywane jako zmienna pomocnicza przy synchronizacji wątków, np. w celu weryfikacji warunku przed wejściem do sekcji krytycznej.

Wszystkie te zastosowania mają na celu zapewnienie spójności danych i eliminację problemów związanych z wyścigami między wątkami i nieprawidłowymi operacjami na współdzielonych zasobach.

---

**User:**

Podaj więcej tematów na interview dotyczących java concurrent.

---

**Assistant:**

Oto kilka dodatkowych tematów na interview dotyczących programowania współbieżnego w Javie:

1. "Thread pools" i ich zastosowanie w wielowątkowym środowisku.

2. Różnice między "synchronized" a "volatile" w Javie, i kiedy należy używać jednego lub drugiego.

3. Klasa "ConcurrentHashMap" w Javie i jej zastosowanie w wielowątkowym środowisku.

4. "Fork/Join" framework w Javie i jego zastosowanie w problemach "divide and conquer".

5. Koncepcja "deadlock" i "livelock" w wielowątkowym środowisku, i jak ich unikać.

6. Synchroniczne i asynchroniczne operacje w Javie, i jak je stosować w zależności od potrzeb.

7. Klasa "Semaphore" w Javie i jej zastosowanie w synchronizacji wątków.

8. "ReentrantLock" w Javie i jego zastosowanie w synchronizacji wątków.

9. Koncepcja "race condition" i jak jej unikać w wielowątkowym środowisku.

10. "ConcurrentLinkedQueue" w Javie i jego zastosowanie w wielowątkowym środowisku.

---

**User:**

Rozwiń temat asynchroniczne operacje w Javie

---

**Assistant:**

Asynchroniczne operacje w Javie pozwalają na wykonywanie operacji bez konieczności oczekiwania na ich zakończenie przed kontynuowaniem działania programu. W takiej sytuacji, aplikacja nie blokuje wątku, który wywołał asynchroniczną operację, co pozwala na równoległe wykonywanie innych operacji.

W Javie asynchroniczne operacje są realizowane za pomocą klasy "CompletableFuture". Klasa ta reprezentuje potencjalny wynik operacji asynchronicznej, który może być dostarczony w przyszłości. W momencie wywołania operacji asynchronicznej, jest ona uruchamiana na oddzielnym wątku, a wynik jest zwracany do obiektu CompletableFuture, gdy operacja zostanie ukończona.

CompletableFuture umożliwia również łączenie operacji asynchronicznych w łańcuchy, gdzie wynik jednej operacji jest używany jako argument dla kolejnej operacji. To pozwala na tworzenie skomplikowanych scenariuszy obliczeniowych, które wymagają wykonywania wielu operacji równolegle.

Do innych mechanizmów asynchronicznych w Javie należy "Future" i "Callable". Future reprezentuje wynik operacji asynchronicznej, który nie został jeszcze obliczony, natomiast Callable reprezentuje zadanie, które ma być wykonywane asynchronicznie.

Asynchroniczne operacje są szczególnie przydatne w aplikacjach internetowych, gdzie czas odpowiedzi jest krytyczny. Przykładowo, asynchroniczne wywołanie zdalnego API może umożliwić wykonywanie innych operacji, podczas gdy aplikacja czeka na odpowiedź. W ten sposób, aplikacja jest bardziej wydajna i responsywna, co poprawia ogólną jakość użytkowania.

Warto jednak pamiętać, że asynchroniczne operacje wymagają uważnej implementacji, ponieważ nieprawidłowe użycie może prowadzić do problemów związanych z wyścigami między wątkami, brak spójności danych i trudne do debugowania błędy.