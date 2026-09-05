---
tags: [claude-code]
date: 2026-06-03
---
# Plan — Wiedza o testach i automatyzacji testów (przygotowanie na rozmowę AI Engineer)

Cel: zbudować rozumienie automatyzacji testów na poziomie, który pozwala (1) rozmawiać z QA wspólnym językiem, (2) wskazać gdzie LLM/agenty realnie wnoszą wartość, (3) zaprojektować platformę testową. Konkretne narzędzia (Selenium, REST Assured) traktowane jako przykłady szerszych kategorii, nie jako temat sam w sobie.
Status: rozdziały 1–8 rozwinięte (wersja opisowa) + rozdział 9 (pogłębienie: BDD/Gherkin). Dokument kompletny.

## Spis treści

- [1. Fundamenty testowania (wspólny język z QA)](#1-fundamenty-testowania-wspólny-język-z-qa)
- [2. E2E w praktyce — model mentalny (Selenium jako przykład)](#2-e2e-w-praktyce--model-mentalny-selenium-jako-przykład)
- [3. Testy API i kontraktowe (REST Assured jako przykład)](#3-testy-api-i-kontraktowe-rest-assured-jako-przykład)
- [4. Gdzie LLM i agenty wnoszą wartość w testach (rdzeń stanowiska)](#4-gdzie-llm-i-agenty-wnoszą-wartość-w-testach-rdzeń-stanowiska)
- [5. Ewaluacja samego systemu AI do testów (poziom meta)](#5-ewaluacja-samego-systemu-ai-do-testów-poziom-meta)
- [6. Architektura platformy do automatyzacji testów (bo masz ją budować)](#6-architektura-platformy-do-automatyzacji-testów-bo-masz-ją-budować)
- [7. Krajobraz narzędzi (orientacyjnie, bez przywiązania)](#7-krajobraz-narzędzi-orientacyjnie-bez-przywiązania)
- [8. Pytania rozmowy + mapowanie na Twoje doświadczenie](#8-pytania-rozmowy--mapowanie-na-twoje-doświadczenie)
- [9. BDD i opisywanie testów językiem naturalnym (Cucumber/Gherkin) — pogłębienie](#9-bdd-i-opisywanie-testów-językiem-naturalnym-cucumbergherkin--pogłębienie)

## 1. Fundamenty testowania (wspólny język z QA)

### 1.1 Piramida testów, trofeum testów, poziomy

Punktem wyjścia każdej rozmowy o automatyzacji jest pytanie, ile i jakich testów pisać oraz na jakim poziomie. Najstarszą i wciąż najużyteczniejszą odpowiedzią jest **piramida testów** Mike'a Cohna. Jej idea jest prosta: testów powinno być tym mniej, im wyżej w stosie się znajdują, ponieważ wraz z poziomem rośnie koszt napisania testu, czas jego wykonania oraz podatność na losowe awarie. U podstawy leży gruba warstwa szybkich, tanich testów jednostkowych, nad nią cieńsza warstwa testów integracyjnych, a na samym szczycie wąski pas testów end-to-end, które są najwolniejsze i najbardziej kruche.

Kolejne poziomy różnią się przede wszystkim tym, jak duży wycinek systemu obejmują i jak realistyczne jest środowisko, w którym działają:

- **Unit** — testuje pojedynczą jednostkę kodu (funkcję lub klasę) w pełnej izolacji od reszty świata: bez bazy danych, sieci czy systemu plików. Dzięki temu wykonuje się w milisekundach i daje najszybszą pętlę informacji zwrotnej, a gdy się wywali, od razu wiadomo, która konkretnie jednostka zawiodła. To podstawowy poziom, na którym wyłapuje się logiczne pomyłki.
- **Integration** — sprawdza współpracę kilku komponentów albo komponentu z realną zależnością, taką jak baza danych, kolejka czy inny serwis. Wykrywa całą klasę błędów niewidocznych dla testów jednostkowych: niezgodności kontraktów, problemy z serializacją, błędną konfigurację, źle obsłużone transakcje. To na tym styku najczęściej pęka oprogramowanie złożone z wielu części.
- **Component** — poziom pośredni: testuje pojedynczy serwis w całości, przez jego publiczne API, ale z zamockowanymi zależnościami zewnętrznymi. Pozwala zweryfikować zachowanie usługi jako spójnej całości bez kosztu stawiania całego ekosystemu wokół niej.
- **Contract** — zamiast uruchamiać równocześnie konsumenta i dostawcę API, sprawdza osobno, że obie strony trzymają się wspólnie ustalonego interfejsu. To sposób na bezpieczne testowanie integracji bez kruchości pełnego E2E (szczegóły w sekcji 3).
- **E2E** — uruchamia cały system od strony użytkownika lub publicznego wejścia, na realistycznych zależnościach, odtwarzając prawdziwy scenariusz użycia. Daje najwięcej pewności, że aplikacja faktycznie działa jako całość, ale płaci się za to najwyższą cenę: powolnością, kosztem i kruchością.

Nowszą propozycją, popularną zwłaszcza w świecie frontendu, jest **trofeum testów** Kenta C. Doddsa. Powstało jako reakcja na dwa zjawiska: odwróconą piramidę (mnóstwo wolnych E2E, garstka testów jednostkowych) oraz nadmiar testów jednostkowych przywiązanych do szczegółów implementacji, które pękają przy każdym refaktorze, choć zachowanie się nie zmienia. Trofeum przesuwa największą wagę na **testy integracyjne**, argumentując, że to one mają najlepszy stosunek pewności do kosztu — sprawdzają zachowanie zbliżone do tego, czego doświadcza użytkownik, a wciąż są szybsze i stabilniejsze niż E2E. U podstawy trofeum leży analiza statyczna (typy, lintery) jako najtańsza linia obrony. Naczelna zasada brzmi: testuj zachowanie, a nie szczegóły implementacji.

Warto umieć płynnie wyjaśnić, dlaczego testy E2E są tak drogie i kruche, bo to wątek, który regularnie wraca na rozmowach. Składa się na to kilka rzeczy naraz. Są wolne, bo uruchamiają realny system: przeglądarkę, sieć, backend. Są niedeterministyczne, ponieważ zależą od czasu, asynchroniczności i stanu środowiska, co prowadzi do flakiness — testów, które raz przechodzą, raz nie, bez żadnej zmiany w kodzie. Są drogie w utrzymaniu, bo każda zmiana w interfejsie lub strukturze DOM potrafi unieważnić selektory, na których się opierają. Wreszcie słabo lokalizują błąd: czerwony test E2E mówi tylko tyle, że coś na całej ścieżce nie zadziałało, nie wskazując, która funkcja zawiodła.

Płynie stąd konkretny wniosek architektoniczny, będący zarazem mostem do reszty tego dokumentu: testów E2E nie da się wyeliminować, bo tylko one weryfikują krytyczne ścieżki w realnych warunkach, ale ich liczbę trzyma się celowo nisko, spychając maksimum logiki na tańsze poziomy. I właśnie ten najbardziej bolesny obszar — utrzymanie i flakiness E2E — jest głównym miejscem, w którym platforma oparta na AI ma realnie się przydać: poprzez samonaprawiające się selektory, automatyczne generowanie testów i inteligentny triage awarii (rozwijam to w sekcjach 4 i 6).

Na koniec nazwa, którą warto znać: **odwrócona piramida**, czyli ice-cream cone — antywzorzec, w którym ciężar testów spoczywa na E2E, a testów jednostkowych jest niewiele. Efektem jest wolny pipeline, kruchy zestaw testów i wysoki koszt utrzymania.

### 1.2 Funkcjonalne vs niefunkcjonalne

Drugi podział, który warto mieć poukładany, przebiega w poprzek poziomów piramidy i dotyczy tego, *co* właściwie testujemy. Testy **funkcjonalne** odpowiadają na pytanie, czy system robi to, co ma robić — czy jego zachowanie zgadza się z wymaganiami. To do nich odnosi się większość tego dokumentu. Testy **niefunkcjonalne** pytają natomiast nie o to, *czy* coś działa, lecz *jak* działa pod względem atrybutów jakości, których użytkownik wprost nie widzi, ale boleśnie odczuwa, gdy ich zabraknie.

Najważniejsze rodzaje testów niefunkcjonalnych to:

- **Wydajność (performance)** — mierzy czas odpowiedzi, przepustowość i latencję. Istotny niuans: dojrzałe zespoły raportują je w percentylach (`p95`, `p99`), a nie jako średnią, bo to właśnie ogon rozkładu — najwolniejsze odpowiedzi — psuje doświadczenie użytkownika.
- **Testy obciążeniowe** — sprawdzają zachowanie systemu pod ruchem. Rozróżnia się tu *load* (oczekiwane, normalne obciążenie), *stress* (celowe wyjście poza limit, by znaleźć punkt załamania) oraz *soak* (długotrwałe obciążenie ujawniające wycieki pamięci i powolne wyczerpywanie zasobów).
- **Bezpieczeństwo** — obejmuje wyszukiwanie podatności, weryfikację kontroli dostępu i walidacji wejścia. W praktyce korzysta się z narzędzi `SAST`/`DAST`, testów penetracyjnych i list ryzyk w rodzaju `OWASP`.
- **Dostępność (a11y)** — bada zgodność ze standardem `WCAG`: odpowiedni kontrast, możliwość nawigacji samą klawiaturą, poprawną obsługę przez czytniki ekranu i właściwe role `ARIA`.
- **Testy wizualne (visual regression)** — porównują wyrenderowany interfejs z zapisanym wzorcem (baseline) i wychwytują regresje wyglądu, których nie zauważy żadna asercja funkcjonalna, bo logicznie wszystko działa. To naturalny punkt wejścia dla modeli multimodalnych, do których wracam w sekcji 4.

Świadomość tego podziału przydaje się na rozmowie, bo pytanie „jak przetestujesz X" ma zwykle drugie dno — chodzi nie tylko o poprawność funkcjonalną, lecz także o to, czy pamiętasz o atrybutach jakości. Cały, w pełni rozpisany przykład odpowiedzi na takie pytanie znajdziesz w sekcji 8.11.

### 1.3 Techniki projektowania przypadków testowych

Skoro wiadomo już, na jakich poziomach i w jakich wymiarach testujemy, pojawia się praktyczne pytanie: które konkretnie przypadki wybrać? Przestrzeń możliwych wejść jest zwykle nieskończona, a testów ma być jak najmniej przy jak największej zdolności wykrywania błędów. Odpowiadają na to klasyczne techniki projektowania przypadków — wszystkie w podejściu black-box, czyli wyprowadzane ze specyfikacji, a nie z kształtu kodu.

- **Klasy równoważności (equivalence partitioning)** — opierają się na obserwacji, że system traktuje całe grupy wejść identycznie. Zamiast testować wszystkie wartości, dzieli się wejścia na takie grupy i bierze po jednym reprezentancie z każdej, pamiętając, by uwzględnić zarówno klasy poprawne, jak i niepoprawne.
- **Analiza wartości brzegowych (boundary value analysis)** — wychodzi z faktu, że błędy najczęściej gnieżdżą się na granicach klas, nie w ich środku. Dla zakresu od 1 do 100 testuje się więc wartości 0, 1, 2 oraz 99, 100, 101. Technika ta naturalnie uzupełnia klasy równoważności.
- **Tablice decyzyjne (decision tables)** — przydają się, gdy wynik zależy od kombinacji wielu warunków. Buduje się tabelę, w której wiersze to warunki i wynikające z nich akcje, a kolumny to poszczególne reguły, co gwarantuje, że wszystkie istotne kombinacje warunków zostaną świadomie przełożone na oczekiwane wyniki.
- **Testy przejść stanów (state transition)** — stosuje się tam, gdzie zachowanie zależy nie tylko od bieżącego wejścia, ale i od historii: koszyk zakupowy, sesja użytkownika, maszyna stanów. Modeluje się stany oraz dozwolone przejścia między nimi i — co równie ważne — sprawdza, że przejścia niedozwolone faktycznie są blokowane.
- **Pairwise (all-pairs)** — odpowiedź na eksplozję kombinatoryczną, gdy parametrów jest wiele i każdy przyjmuje wiele wartości. Zamiast testować wszystkie kombinacje, generuje się minimalny zestaw pokrywający każdą *parę* wartości, wychodząc z empirycznej obserwacji, że większość błędów wynika z interakcji zaledwie dwóch parametrów. Liczba przypadków spada wtedy dramatycznie.

To nie jest wiedza czysto teoretyczna: dokładnie te reguły powinien stosować LLM, gdy generuje testy (sekcja 4). Znajomość ich nazw pozwala świadomie oceniać i ukierunkowywać wynik — można wprost poprosić model o przypadki brzegowe albo o pełne pokrycie konkretnej tablicy decyzyjnej.

### 1.4 Pojęcia jakości

Wokół samych testów narosło kilka pojęć opisujących ich jakość i wiarygodność. Warto rozumieć je dokładnie, bo część kryje pułapki, na które łatwo nadziać się w rozmowie.

**Pokrycie kodu (coverage)** to odsetek kodu wykonanego przez testy — mierzony liniowo, gałęziowo (`branch`) lub po ścieżkach. Pułapka polega na tym, że wysokie pokrycie wcale nie oznacza dobrych testów: metryka mówi tylko, że dany kod *został wykonany*, a nie że jego wynik *został zweryfikowany*. Można przejść przez całą funkcję bez jednej sensownej asercji i wciąż pokazać 100%. Dlatego pokrycie łatwo „ogrywać", a samo w sobie jest słabym celem — popularne 80% to co najwyżej proxy. Mocniejszym sygnałem jest **mutation testing**, który celowo wprowadza drobne mutacje do kodu i sprawdza, czy testy je wychwycą (zabiją); to mierzy realną zdolność wykrywania błędów, a nie samo wykonanie.

**Defect escape rate** to odsetek defektów, które prześlizgnęły się przez testy i ujawniły dopiero na produkcji. Jest to miara biznesowa, oceniająca skuteczność całej siatki testów z perspektywy użytkownika, i w praktyce mówi więcej niż pokrycie. Pokrewnym wskaźnikiem jest `DDP` (defect detection percentage).

**Flakiness** opisuje test, który raz przechodzi, raz nie, mimo że kod się nie zmienił — czyli daje wynik niedeterministyczny. Źródeł jest wiele: zależności czasowe i asynchroniczność, kolejność wykonywania testów, współdzielony stan, sieć, dane czy strefy czasowe. Flaky testy są szczególnie szkodliwe, bo niszczą zaufanie do całego zestawu (znowu czerwony, po prostu puść jeszcze raz) i potrafią maskować prawdziwe regresje. To główny wróg testów E2E.

**Determinizm** jest ich przeciwieństwem i zarazem fundamentem wiarygodnego testu: ten sam stan wejściowy ma zawsze dawać ten sam wynik. Duża część inżynierii testów sprowadza się do walki o determinizm — okiełznania czasu, losowości, współbieżności i danych. Dla platformy opartej na AI to pojęcie jest wręcz newralgiczne, bo generator (LLM) jest z natury niedeterministyczny, podczas gdy *wygenerowane* testy muszą być w pełni deterministyczne; temu napięciu poświęcam sekcję 5.

**Izolacja** oznacza, że testy nie zależą od siebie nawzajem ani od kolejności wykonania — każdy samodzielnie przygotowuje i sprząta swój stan. To warunek zarówno bezpiecznego zrównoleglania, jak i wiarygodnego wskazywania źródła awarii. Przeciwieństwem są testy łańcuchowe, dzielące jedną bazę danych (dlaczego to nie to samo, co testowanie współbieżności systemu — 2.7).

**Powtarzalność (repeatability)** to gwarancja, że test da ten sam wynik niezależnie od maszyny, środowiska i momentu uruchomienia. Wymaga zapanowania nad zależnościami zewnętrznymi: konteneryzacji, mockowania, ustalenia stałego ziarna (`seed`) losowości i zamrożenia czasu.

### 1.5 Test doubles i testy kontraktowe

Wiele z powyższych własności — izolację, szybkość, determinizm — osiąga się, podmieniając realne zależności na ich udawane wersje. Zbiorczo nazywa się je **test doubles** (termin Gerarda Meszárosa) i rozróżnia pięć rodzajów, które w praktyce bywają mylone:

- **Dummy** to obiekt, który jedynie wypełnia wymagany parametr i nigdy nie jest realnie używany.
- **Stub** zwraca z góry zaprogramowane odpowiedzi, pozwalając sterować tym, co „widzi" testowany kod; służy do testów stanu.
- **Spy** jest stubem, który dodatkowo zapisuje, jak został wywołany, co umożliwia późniejszą weryfikację.
- **Mock** jest zaprogramowany z konkretnymi oczekiwaniami i weryfikuje *interakcje* — sprawdza, czy i w jaki sposób został wywołany; służy do testów zachowania.
- **Fake** to działająca, lecz uproszczona implementacja (np. baza danych trzymana w pamięci, `in-memory`), która ma prawdziwą logikę, ale nie nadaje się na produkcję.

Tu czai się klasyczna pułapka: nadużywanie mocków prowadzi do testów ściśle sprzężonych z implementacją — kruchych, bo sprawdzają, *jak* coś zostało zrobione, zamiast *co* zostało osiągnięte. To kolejny argument, dla którego trofeum testów stawia na integrację na realnych zależnościach.

Osobnym, szerszym narzędziem jest **service virtualization** — symulacja całej zewnętrznej usługi wraz z jej zachowaniem, latencją i scenariuszami błędów. Stosuje się ją, gdy prawdziwa usługa jest niedostępna, kosztowna, wolna albo trudna do wprowadzenia w konkretny stan, jak zewnętrzny system płatności. W odróżnieniu od pojedynczego stuba odwzorowuje protokół i stany całej usługi.

Wreszcie **testy kontraktowe (contract testing)** rozwiązują problem testowania integracji między usługami bez stawiania obu naraz i bez kruchości pełnego E2E. W podejściu **consumer-driven contracts (CDC)** to konsument definiuje, czego oczekuje od API, a dostawca weryfikuje u siebie, że ten kontrakt spełnia — kontrakt staje się w ten sposób wykonywalną umową. Najpopularniejszym narzędziem jest **Pact**: konsument generuje kontrakt ze swoich testów, broker go dystrybuuje, a dostawca sprawdza go w swoim CI. Dzięki temu złamanie kontraktu, na przykład usunięcie pola z odpowiedzi, wychodzi na jaw, zanim trafi na produkcję — taniej i stabilniej niż przez E2E. Do tematu wracam szerzej w sekcji 3.

## 2. E2E w praktyce — model mentalny (Selenium jako przykład)

Ten rozdział buduje model mentalny tego, jak w ogóle działa automatyzacja przeglądarki i co decyduje o tym, że testy E2E są szybkie albo wolne, stabilne albo kruche. Selenium służy tu jako reprezentant całej kategorii, a różnice wobec nowszych narzędzi (Playwright, Cypress) pokazuję tam, gdzie wyjaśniają, dlaczego pewne rozwiązania wyparły inne.

### 2.1 Architektura: WebDriver, protokół W3C i model sterowania

Aby zrozumieć Selenium, trzeba zobaczyć, że nie jest to jeden program, lecz warstwowa układanka. Kod testu posługuje się biblioteką kliencką (w dowolnym języku — Java, Python, JavaScript), która wysyła polecenia do **drivera** specyficznego dla przeglądarki (np. chromedriver dla Chrome). Komunikacja odbywa się po HTTP, zgodnie ze standardem **W3C WebDriver** — to właśnie ten ustandaryzowany protokół sprawia, że ten sam test działa na różnych przeglądarkach i z różnych języków. Driver tłumaczy polecenia na akcje w prawdziwej przeglądarce i odsyła wyniki.

Kluczowa cecha tego modelu to sterowanie **out-of-process**: automatyzacja żyje poza przeglądarką i rozmawia z nią przez protokół. Ma to swoją cenę — każde pojedyncze polecenie (znajdź element, kliknij, odczytaj tekst) to osobny round-trip HTTP, co przy długich scenariuszach sumuje się w zauważalną latencję. To również historyczny powód, dla którego klasyczne Selenium bywa wolniejsze od nowszych narzędzi.

Dla kontrastu warto znać dwa inne podejścia. **Cypress** działa **in-process** — wykonuje się wewnątrz tej samej pętli zdarzeń co aplikacja, bezpośrednio w przeglądarce. Daje to dużą szybkość i bezpośredni dostęp do wnętrza aplikacji, ale kosztem ograniczeń (silne związanie z JavaScriptem, trudniejsza obsługa wielu kart czy różnych domen). **Playwright** pozostaje out-of-process, ale zamiast pojedynczych żądań HTTP utrzymuje jedno trwałe, dwukierunkowe połączenie z przeglądarką (przez protokoły w rodzaju CDP) i operuje pojęciem kontekstów przeglądarki; to, w połączeniu z wbudowanym auto-waitingiem, czyni go szybszym i mniej kruchym niż klasyczne Selenium.

Te trzy modele sterowania najłatwiej zapamiętać obok siebie:

```text
SELENIUM — out-of-process, osobny round-trip HTTP na każdą komendę

  ┌───────────────┐   HTTP / protokół W3C WebDriver    ┌──────────────┐       ┌───────────────┐
  │   Kod testu   │   (jedno żądanie na komendę)        │   Driver     │ akcje │  Przeglądarka  │
  │  + biblioteka │ ── findElement ───────────────────▶│ chromedriver │──────▶│    Chrome      │
  │   kliencka    │ ── click ─────────────────────────▶│ geckodriver  │──────▶│    Firefox     │
  │ (Java/Py/JS)  │ ◀─ wynik / stan ───────────────────│   ...        │◀──────│    ...         │
  └───────────────┘                                    └──────────────┘  stan └───────────────┘
   N komend = N round-tripów HTTP  →  latencja się sumuje (stąd historyczna „powolność")


PLAYWRIGHT — out-of-process, ale JEDNO trwałe połączenie dwukierunkowe

  ┌───────────────┐    trwały kanał (WebSocket / CDP)   ┌────────────────────────────┐
  │   Kod testu   │ ═══════════════════════════════════▶│  Przeglądarka               │
  │  (auto-wait)  │ ◀═══ zdarzenia, sygnały gotowości ══│  context A │ context B │ …   │
  └───────────────┘    w czasie rzeczywistym            └────────────────────────────┘
   jeden strumień zamiast round-tripów  +  auto-waiting (czeka na stan PRZED akcją)
   →  szybciej i mniej krucho niż klasyczne Selenium


CYPRESS — in-process, wewnątrz tej samej pętli zdarzeń co aplikacja

  ┌──────────────────────────────────────────────────┐
  │                  Przeglądarka                     │
  │   ┌──────────────┐  bezpośrednio  ┌─────────────┐ │
  │   │  Test (JS)   │ ◀────────────▶ │  Aplikacja  │ │
  │   └──────────────┘  wspólny loop  └─────────────┘ │
  └──────────────────────────────────────────────────┘
   brak warstwy protokołu / drivera  →  bardzo szybko i blisko aplikacji,
   ale: tylko JavaScript, trudniej z wieloma kartami / różnymi domenami
```

Model mentalny do zapamiętania: po jednej stronie jest runner testów, pośrodku warstwa protokołu i drivera, po drugiej przeglądarka — a o charakterystyce narzędzia decydują głównie dwie osie: czy sterowanie jest in- czy out-of-process oraz jak bogaty i trwały jest protokół komunikacji. Atutem Selenium jest standard W3C, dojrzałość oraz najszersze wsparcie języków i przeglądarek; jego kosztem — latencja per-polecenie i brak (historycznie) automatycznego czekania, o którym za chwilę.

### 2.2 Lokatory i strategia selektorów

Zanim test cokolwiek zrobi, musi **znaleźć element** na stronie — i to właśnie tu rodzi się większość kruchości E2E. Selenium oferuje kilka strategii lokalizacji: po identyfikatorze, nazwie, selektorze CSS, wyrażeniu XPath czy tekście odnośnika. Problem polega na tym, że selektor związany ze strukturą DOM albo z wyglądem psuje się przy każdej zmianie interfejsu, nawet gdy logika aplikacji pozostaje ta sama.

Dlatego o selektorach warto myśleć w kategoriach odporności, od najbardziej trwałych do najbardziej kruchych:

- **Dedykowane atrybuty testowe (`data-testid`)** — najbardziej odporne, bo celowo oddzielone od stylu i struktury. Stanowią jawny kontrakt: to jest punkt zaczepienia dla testów, którego nikt nie zmieni przypadkiem przy refaktorze CSS.
- **Selektory dostępnościowe (rola/ARIA, dostępna nazwa)** — wyszukiwanie elementu tak, jak zrobiłby to użytkownik lub czytnik ekranu (filozofia Testing Library). Odporne na zmiany struktury, a przy okazji wymuszają dostępny, semantyczny markup.
- **Selektory CSS** — zwięzłe i szybkie, ale przywiązane do klas i struktury, które zmieniają się często, zwłaszcza przy CSS-in-JS czy frameworkach utility-first.
- **XPath** — najpotężniejszy (potrafi nawigować w górę drzewa i dopasowywać po tekście), ale zarazem kruchy, wolniejszy i trudny w czytaniu; XPath bezwzględny (liczony od korzenia) to wręcz antywzorzec, względny — z stabilnym punktem zaczepienia — bywa akceptowalny.

Kruchość lokatorów to bezpośrednia przyczyna, dla której utrzymanie E2E jest tak kosztowne — i dokładnie ten ból adresują samonaprawiające się selektory oparte na AI, do których wracam w sekcji 4.

### 2.3 Synchronizacja: waity i źródło flakiness

Drugim wielkim źródłem kruchości jest **synchronizacja**. Aplikacja jest z natury asynchroniczna — dane przychodzą z sieci, interfejs renderuje się i animuje we własnym tempie — podczas gdy automatyzacja działa swoim rytmem. Jeśli test spróbuje kliknąć element, zanim ten się pojawi i będzie gotowy, padnie; jeśli robi to raz skutecznie, a raz nie, mamy flakiness.

Sposoby radzenia sobie z tym układają się w wyraźną hierarchię dojrzałości:

- **Sztywny sleep** (np. `Thread.sleep`) — antywzorzec. Albo ustawisz go za krótko (test bywa niestabilny), albo za długo (niepotrzebnie spowalnia cały zestaw). Czasu nie da się dobrze nastroić na stałe.
- **Implicit wait** w Selenium — globalne ustawienie: czekaj do N sekund na pojawienie się elementu. Rozwiązanie zgrubne; bywa, że źle współgra z waitami jawnymi i czeka jedynie na obecność elementu, nie na jego gotowość do interakcji.
- **Explicit wait** (`WebDriverWait` z warunkami w rodzaju element klikalny, widoczny, tekst obecny) — poprawne podejście w Selenium: czekasz dokładnie na ten warunek, którego potrzebujesz, odpytując stronę aż do skutku lub do limitu czasu.
- **Auto-waiting** (Playwright, Cypress) — framework sam, przed każdą akcją, czeka, aż element będzie podłączony, widoczny, stabilny i gotowy na zdarzenia. Eliminuje większość jawnych waitów i jest jednym z głównych powodów, dla których te narzędzia są mniej podatne na flakiness. To dzisiejszy standard.

Reguła do zapamiętania jest jedna: **nigdy nie czekaj na czas, czekaj na warunek (stan)**. Flakiness to niemal zawsze niewystarczająca lub błędna synchronizacja — i jest to praktyczne rozwinięcie walki o determinizm z sekcji 1.4.

### 2.4 Wzorce organizacji testów

Intuicja jest prosta: **surowy skrypt klikający po stronie się nie skaluje**. Selektory i kroki techniczne wplątują się w logikę testu, ten sam fragment (np. logowanie) kopiujesz do dziesiątek testów, a gdy projektant zmieni jeden przycisk, poprawiasz go wszędzie. Wzorce organizacji testów to po prostu sposoby na **rozdzielenie *co* test sprawdza (intencja biznesowa) od *jak* to robi technicznie (selektory, kliknięcia)**.

**Page Object Model (POM)** — wzorzec domyślny. Każdy ekran staje się klasą, która wystawia metody w języku biznesu (`login(user)`, `dodajDoKoszyka(produkt)`) i chowa w sobie selektory. Najlepiej widać to na kontraście.

Bez POM — selektory wplecione w test i powtórzone w każdym scenariuszu:

```python
def test_logowanie():
    driver.find_element(By.ID, "user").send_keys("kamil")
    driver.find_element(By.ID, "pass").send_keys("tajne")
    driver.find_element(By.CSS_SELECTOR, "button[type=submit]").click()
    assert driver.find_element(By.CSS_SELECTOR, ".welcome").text == "Witaj, kamil"
# gdy #user zmieni się na #login → poprawiasz to w KAŻDYM teście, który loguje
```

Z POM — selektory żyją w jednym miejscu, a test czyta się jak opis zachowania:

```python
class LoginPage:
    def __init__(self, page):
        self.page = page
        self.user = page.locator("#user")
        self.haslo = page.locator("#pass")
        self.zaloguj = page.get_by_role("button", name="Zaloguj")

    def login(self, login, haslo):
        self.user.fill(login)
        self.haslo.fill(haslo)
        self.zaloguj.click()
        return DashboardPage(self.page)        # metoda zwraca obiekt następnej strony

class DashboardPage:
    def __init__(self, page):
        self.powitanie = page.locator(".welcome")


def test_logowanie(page):
    dashboard = LoginPage(page).login("kamil", "tajne")
    assert dashboard.powitanie.inner_text() == "Witaj, kamil"
# zmiana selektora #user → #login: poprawiasz JEDNĄ linię w LoginPage
```

Korzyść jest podwójna: test mówi językiem domeny (czytelność), a cała wiedza o strukturze strony siedzi w jednym miejscu (utrzymanie). To bezpośrednia odpowiedź na kruchość lokatorów z 2.2.

**Screenplay** — ewolucja POM dla złożonych przepływów. Zamiast „stron z metodami" modeluje **aktorów**, którzy wykonują **zadania** złożone z mniejszych **interakcji**. Przy dużych aplikacjach obiekty strony puchną (jedna klasa robi wszystko); Screenplay rozbija to na małe, komponowalne, wielokrotnego użytku zadania:

```text
actor("Kamil").attemptsTo(
    Login.withCredentials("kamil", "tajne"),
    AddToCart.theProduct("Książka"),
    Checkout.now(),
)
actor("Kamil").should(see(OrderConfirmation.isVisible()))
```

Czyta się to niemal jak zdanie (aktor → próbuje wykonać → zadania), lepiej skaluje i sprzyja reużyciu, ale kosztem większej ceremonialności (dużo małych klas). Dla prostych zestawów POM zwykle w zupełności wystarcza.

**Fixtures oraz setup/teardown** — mechanizm doprowadzenia systemu do znanego stanu *przed* testem i posprzątania *po* nim. To tutaj fizycznie realizuje się izolacja i powtarzalność z 1.4. Nowoczesne frameworki robią to komponowalnie, przez wstrzykiwanie zależności — fixture deklarujesz raz, a test dostaje gotowy stan jako argument:

```python
@pytest.fixture
def zalogowany_uzytkownik(page, api):
    user = api.utworz_uzytkownika()            # SETUP: świeży, izolowany stan
    LoginPage(page).login(user.login, user.haslo)
    yield user                                  # tu wykonuje się test
    api.usun_uzytkownika(user.id)               # TEARDOWN: sprzątanie po sobie


def test_zamowienie(page, zalogowany_uzytkownik):
    # test startuje od razu z zalogowanym, świeżym użytkownikiem
    ...
```

Kluczowy szczegół: fixture daje *każdemu* testowi własny, świeży stan (osobny użytkownik, osobne dane), dzięki czemu testy nie wchodzą sobie w drogę i można je bezpiecznie zrównoleglać — wątek, który rozwijam w 2.5 i 2.7.

### 2.5 Środowisko, dane testowe i skalowanie

Test E2E, w odróżnieniu od jednostkowego, potrzebuje **działającego systemu i danych** — co czyni zarządzanie środowiskiem osobnym wyzwaniem.

- **Środowisko** — wdrożona instancja aplikacji (staging lub środowisko efemeryczne). Powtarzalność wymaga, by było kontrolowane; współczesnym ideałem są środowiska tworzone na żądanie dla każdego pull requesta, stawiane z kontenerów i kasowane po teście.
- **Dane testowe** — każdy test potrzebuje znanego stanu danych. Można je zasiać przez API lub bazę przed testem, użyć fabryk, albo tworzyć i sprzątać w obrębie samego testu. Czego unikać: polegania na współdzielonych, modyfikowalnych danych, bo to wprost łamie izolację.
- **Równoległość** — ponieważ E2E są wolne, uruchamia się je równolegle, co z kolei wymaga izolacji (osobne dane, osobni użytkownicy dla równoległych testów). To zrównoleglanie *wykonania* testów to co innego niż testowanie współbieżności samego systemu — różnicę rozwijam w 2.7.
- **Selenium Grid** — rozdziela testy na wiele węzłów z przeglądarkami, umożliwiając zarówno zrównoleglenie, jak i pokrycie wielu przeglądarek naraz; jego odpowiednikami w chmurze są usługi w rodzaju BrowserStack czy Sauce Labs.
- **Konteneryzacja** — uruchamianie przeglądarek w kontenerach (Docker) dla powtarzalności i wygody w CI; Selenium udostępnia oficjalne obrazy przeglądarek, Playwright dostarcza własne.

### 2.6 Diagnostyka awarii

Gdy test E2E padnie na serwerze CI, musisz zrozumieć przyczynę bez odtwarzania problemu na własnej maszynie — dlatego diagnostyka jest integralną częścią dojrzałego zestawu:

- **Raporty** (JUnit XML, HTML, Allure) — agregują wyniki, pokazują historię i trendy.
- **Zrzuty ekranu przy błędzie** — utrwalają stan interfejsu w momencie awarii.
- **Nagranie wideo** — pozwala odtworzyć cały przebieg testu.
- **Trace** (np. trace viewer w Playwright) — złoty standard: rejestruje krok po kroku migawki DOM, ruch sieciowy, konsolę i akcje, pozwalając cofać się w czasie przez nieudany test podczas analizy post-mortem. Selenium było tu historycznie słabsze i taki obraz trzeba składać samodzielnie ze zrzutów i logów.

Dla platformy opartej na AI diagnostyka ma podwójne znaczenie: bogate artefakty awarii — DOM, zrzuty ekranu, logi, trace — są dokładnie tymi danymi wejściowymi, których model (w tym multimodalny) potrzebuje, by automatycznie klasyfikować i grupować awarie albo naprawiać selektory (sekcje 4 i 6).

### 2.7 Izolacja a współbieżność — i testy zachowań równoległych

To częste i słuszne pytanie: skoro testy mają być izolowane, to czym ich przypadkowe równoległe wykonanie na jednym środowisku różni się od produkcji, gdzie i tak lecą równolegle tysiące żądań? Klucz w tym, że **izolacja jest własnością uprzęży testowej, a nie tezą, że system nie radzi sobie ze współbieżnością**. To dwie różne warstwy, które łatwo pomylić.

**Dlaczego równoległe testy na jednym środowisku to nie to samo, co produkcyjna współbieżność.** Na produkcji równoległe żądania zwykle operują na *rozłącznych* danych — użytkownik A grzebie w swoim koszyku, użytkownik B w swoim; nie wchodzą sobie w drogę, bo stan jest podzielony (per-user, per-tenant). Kolizja w testach pojawia się dopiero wtedy, gdy dwa testy **współdzielą ten sam zasób** — to samo konto, ten sam rekord, ten sam licznik. Wtedy test A modyfikuje stan, na którym test B robi asercję, i dostajesz *fałszywą porażkę* (flakiness), która nie ma nic wspólnego z błędem systemu, tylko z dzieleniem fixture'ów. Izolacja polega więc na tym, by każdemu równoległemu testowi dać **własne** dane (osobny użytkownik, osobny tenant, transakcja z rollbackiem) — czyli ręcznie odtworzyć tę samą rozłączność, którą produkcja ma z natury. Innymi słowy: kolizja równoległych testów to artefakt współdzielonego stanu testowego, a nie dowód współbieżnościowego buga — i dlatego nie wolno mieszać tych dwóch rzeczy, bo jedno maskuje drugie.

**Testy łańcuchowe — masz rację co do nazwy.** „Łańcuchowe" znaczy *sekwencyjne*: test B zależy od efektu testu A (A tworzy zamówienie, B je opłaca, C wysyła). To **antywzorzec**, dokładne przeciwieństwo izolacji (wspomniane w 1.4) — a nie mechanizm badania równoległości. Są kruche (gdy A padnie, B i C lecą za nim), nie da się ich zrównoleglić ani uruchomić pojedynczo, a awaria nie wskazuje źródła. Czyli: testy łańcuchowe to *nie* są testy współbieżności — to po prostu testy źle odizolowane.

**Czy są testy badające równoległe zachowanie systemu? Tak — to osobna, świadoma kategoria.** Tutaj robi się odwrotność izolacji: *celowo* puszcza się wiele równoczesnych operacji na **tym samym** zasobie, żeby wydobyć błędy współbieżności, których test sekwencyjny nigdy nie zobaczy:

- **Wyścigi (race conditions) / zgubiona aktualizacja (lost update)** — dwóch klientów czyta saldo 100, każdy dodaje 50, naiwny zapis daje 150 zamiast 200. Klasyczny cel takiego testu.
- **Zakleszczenia (deadlock) i zagłodzenie (starvation)** — wzajemne blokowanie zasobów albo wątek, który nigdy nie dostaje dostępu.
- **Idempotentność pod współbieżnością** — równoległe POST-y z tym samym kluczem idempotencji mają utworzyć *jeden* rekord, nie N (łączy się z 3.3).
- **Blokady optymistyczne/pesymistyczne** — czy wersjonowanie (`@Version`, ETag / If-Match) poprawnie odrzuca nadpisanie nieaktualnym stanem.

Wygląda to tak — kluczem jest *zsynchronizowany start* (bariera/latch), żeby wątki realnie się zderzyły, oraz asercja **niezmiennika**, a nie konkretnej kolejności:

```python
def test_brak_zgubionych_aktualizacji(api):
    konto = api.utworz_konto(saldo=0)
    N = 100
    start = Barrier(N)                     # wszyscy ruszają w tym samym momencie

    def wplata():
        start.wait()                       # zsynchronizowany start → realna kolizja
        api.doladuj(konto.id, 1)           # N równoległych operacji na TYM SAMYM koncie

    uruchom_rownolegle(wplata, powtorz=N)
    assert api.saldo(konto.id) == N        # niezmiennik: żadna wpłata nie zginęła
```

Warto odróżnić to od **testów obciążeniowych** (load/stress/soak z 1.2): obciążeniowe też generują współbieżny ruch, ale ich celem jest głównie *wydajność* (czas odpowiedzi, przepustowość), podczas gdy testy współbieżności celują w *poprawność* pod równoległością (niezmienniki, brak wyścigów). W praktyce bywają łączone, ale pytają o co innego.

Na koniec niuans spinający to z determinizmem z 1.4: race condition jest z natury niedeterministyczny „od strony systemu", więc taki test trzeba pisać tak, by **deterministycznie eksponował** warunek wyścigu, a nie był flaky z powodu własnej, złej synchronizacji. Stąd: latch/bariera zamiast `sleep`, wiele powtórzeń (wyścig ujawnia się losowo) i asercja niezmiennika zamiast oczekiwania konkretnej kolejności. Do cięższych przypadków służą wyspecjalizowane narzędzia: **jcstress** (Java Concurrency Stress — poluje na race'y na JVM milionami powtórzeń), **ThreadSanitizer** (wykrywa data race w C/C++/Go), a dla systemów rozproszonych **Jepsen** (bada liniowość i spójność pod partycjami sieci) oraz model checking w rodzaju **TLA+**. To już pogranicze inżynierii niezawodności, ale dobrze wiedzieć, że ta kategoria istnieje i umieć ją nazwać na rozmowie.

## 3. Testy API i kontraktowe (REST Assured jako przykład)

Poziom testów API leży w piramidzie poniżej E2E: zamiast klikać po interfejsie, odpytuje warstwę usług bezpośrednio przez HTTP. Dzięki temu jest szybszy, stabilniejszy i łatwiejszy w utrzymaniu — i to właśnie tu, a nie w E2E, powinna trafiać większość weryfikacji logiki biznesowej. REST Assured (biblioteka dla Javy) służy jako przykład całej kategorii; ten sam model myślenia odnajdziesz w supertest dla Node, w requests z pytest w Pythonie czy w Karate.

### 3.1 Anatomia testu API: schemat Given/When/Then

REST Assured organizuje test wokół czytelnego schematu **Given/When/Then**, który jest po prostu wariantem klasycznego Arrange-Act-Assert. W części **given** przygotowujesz żądanie: nagłówki, dane uwierzytelniające, parametry, treść (body) i adres bazowy. W części **when** wykonujesz właściwą akcję — wywołanie metody HTTP (GET, POST, PUT, DELETE) na konkretnym zasobie. W części **then** weryfikujesz odpowiedź. Ta weryfikacja rozkłada się zwykle na trzy poziomy:

- **Status code** — pierwszy i najważniejszy sygnał. Warto asercjonować konkretny kod, nie tylko klasę odpowiedzi: 200 vs 201 vs 204 niosą różne znaczenie, podobnie jak rozróżnienie 400 (błędne żądanie), 401 (brak uwierzytelnienia), 403 (brak uprawnień) czy 404 (brak zasobu). Sprawdzanie dokładnego kodu wychwytuje subtelne regresje w semantyce API.
- **Nagłówki** — `Content-Type`, nagłówki cache'owania, uwierzytelniania czy własne nagłówki aplikacji. Często pomijane, a potrafią ujawnić błędy konfiguracji niewidoczne w samym body.
- **Body** — struktura i wartości odpowiedzi, najczęściej odpytywane przez JSONPath (w REST Assured: składnia GPath). Tu sprawdzasz, czy zwrócone dane są poprawne co do treści.

Mentalnie: test API to spisana umowa „dla takiego żądania spodziewam się takiej odpowiedzi", rozpisana na status, nagłówki i treść.

### 3.2 Walidacja schematów i kontrakty między usługami

Asercjonowanie pojedynczych pól szybko staje się żmudne i niekompletne — łatwo przeoczyć, że odpowiedź zmieniła kształt. Dlatego dojrzalsze podejście to **walidacja całej odpowiedzi względem schematu**. Za pomocą JSON Schema (często wyprowadzonego ze specyfikacji **OpenAPI**) sprawdzasz naraz strukturę, typy pól, pola wymagane i formaty — jednym ruchem wychwytując dryf kontraktu, którego ręczne asercje by nie złapały. Warto rozróżniać dwie rzeczy: walidacja schematu odpowiada na pytanie „czy odpowiedź ma uzgodniony kształt", a asercja wartości — „czy ta konkretna wartość jest poprawna". Obie są potrzebne.

Stąd już krok do **testów kontraktowych** między usługami, zapowiedzianych w sekcji 1.5. Zamiast stawiać równocześnie konsumenta i dostawcę API (co sprowadzałoby się do kruchego E2E), weryfikujesz osobno, że obie strony trzymają się wspólnego kontraktu — w podejściu consumer-driven to konsument definiuje oczekiwania, a dostawca potwierdza, że je spełnia (narzędzie: `Pact`). W tym świecie **OpenAPI** pełni rolę jednego źródła prawdy: z tej samej specyfikacji można generować testy, mocki i walidatory, a zmiana łamiąca kontrakt (usunięte pole, zmieniony typ) wychodzi na jaw tanio i wcześnie.

### 3.3 Przekrojowe aspekty: uwierzytelnianie, dane wrażliwe, idempotentność, retry

Niezależnie od pojedynczego asserta, testy API muszą radzić sobie z kilkoma przekrojowymi zagadnieniami:

- **Uwierzytelnianie i autoryzacja** — większość API wymaga tokenu (Bearer/JWT, przepływy OAuth2), klucza API lub sesji. Testować trzeba oba wymiary: uwierzytelnienie (poprawne i niepoprawne dane logowania) oraz autoryzację (czy użytkownik o danej roli ma dostęp do zasobu, a inny dostaje 403). Te negatywne przypadki — sprawdzające, że dostęp jest poprawnie blokowany — są tu szczególnie ważne i łączą się z wątkiem bezpieczeństwa z sekcji 1.2.
- **Dane wrażliwe** — sekretów (tokenów, haseł) nigdy nie umieszcza się na sztywno w kodzie testu; pobiera się je ze zmiennych środowiskowych lub menedżera sekretów i maskuje w logach oraz raportach. Do testów używa się dedykowanych kont i danych, nie produkcyjnych.
- **Idempotentność** — w semantyce HTTP metody GET, PUT i DELETE są idempotentne (powtórzenie daje ten sam efekt), a POST nie. Ma to dwie konsekwencje dla testów: po pierwsze, ponawiany POST tworzy duplikaty i potrafi złamać powtarzalność, więc test musi sam po sobie sprzątać; po drugie, czasem to właśnie gwarancji idempotentności API się testuje (np. klucz idempotencji w płatnościach, chroniący przed podwójnym obciążeniem).
- **Retry** — trzeba odróżnić uprawnione ponawianie od maskowania błędu. Ponawianie z wycofaniem (backoff) jest poprawne tam, gdzie system jest naprawdę asynchroniczny lub spójny ostatecznie (eventual consistency) — odpytujesz wtedy aż do osiągnięcia oczekiwanego stanu. Natomiast ponawianie po to, by przepchnąć niestabilny test, jest antywzorcem ukrywającym realną wadę i znów sprowadza się do walki o determinizm.

### 3.4 Dlaczego API jest tańsze i stabilniejsze niż E2E — przesuwanie testów w dół piramidy

Na koniec sedno, które warto umieć wyłożyć wprost: dlaczego testy API są tańsze i stabilniejsze od E2E. Odpowiedź wynika wprost z rozdziału 2 — znikają tu dwa główne źródła kruchości E2E. Nie ma przeglądarki, renderowania ani DOM, więc nie ma kruchych selektorów (2.2); nie ma asynchronicznego interfejsu do zsynchronizowania, więc znika większość problemów z waitami (2.3). W efekcie testy API są szybsze (brak startu przeglądarki, bezpośredni HTTP), łatwo je zrównoleglić i są bardziej deterministyczne, a gdy padną, od razu wskazują konkretny endpoint czy kontrakt, a nie mgliste „coś na stronie nie działa".

Płynie z tego strategia **przesuwania testów w dół piramidy** (shift down): maksimum logiki biznesowej i przypadków brzegowych weryfikuj na poziomie API/integracji, a nieliczne E2E rezerwuj dla prawdziwych, pełnych ścieżek użytkownika, które naprawdę muszą przejść przez interfejs. Trzeba przy tym pamiętać o granicy: testy API nie wychwycą błędów samego UI ani jego integracji z frontendem — są uzupełnieniem E2E, nie ich zamiennikiem, a cała sztuka polega na właściwych proporcjach.

Dla platformy opartej na AI ten poziom jest szczególnie wdzięczny: API jest ustrukturyzowane i opisane maszynowo (specyfikacja OpenAPI), deterministyczne i pozbawione wizualnej dwuznaczności. To czyni je najłatwiejszym i najmniej ryzykownym obszarem automatycznego generowania testów przez LLM — od scenariuszy wyprowadzonych z OpenAPI, przez przypadki brzegowe, po walidację względem schematu — i naturalnym punktem startu dla platformy, do czego wracam w sekcji 4.

## 4. Gdzie LLM i agenty wnoszą wartość w testach (rdzeń stanowiska)

To jest serce stanowiska i miejsce, w którym Twoja wiedza o LLM-ach spotyka się z testowaniem. Zamiast pytać luźno „gdzie wcisnąć AI", warto nałożyć je na **cykl życia testu**: projektowanie przypadków → pisanie (authoring) → wykonanie → utrzymanie → diagnoza awarii. AI dotyka każdego z tych etapów, ale z różną wartością i różnym ryzykiem. Przez cały rozdział przewijają się dwie osie, które warto mieć w głowie. Pierwsza: wartość AI jest największa tam, gdzie wejście jest ustrukturyzowane i czytelne maszynowo (kod, OpenAPI, DOM), a najmniejsza tam, gdzie panuje dwuznaczność (intencja biznesowa). Druga: trzeba rozróżniać **AI offline** (na etapie projektowania i generowania, poza ścieżką wykonania) od **AI online** (w czasie działania testu — self-healing, agent), bo mają zupełnie inne wymagania co do determinizmu, latencji i kosztu (rozwijam to w sekcji 6).

### 4.1 Rama nadrzędna: problem wyroczni (oracle problem)

Zanim przejdziemy do konkretów, jedno pojęcie spina cały rozdział i wyznacza granice tego, co AI może zrobić: **problem wyroczni**. Żeby stwierdzić, czy zaobserwowane zachowanie jest poprawne, potrzebujesz wyroczni — źródła prawdy o tym, jak system *powinien* się zachować. Tradycyjnie tą wyrocznią jest człowiek, który na podstawie wymagań pisze asercje. LLM potrafi i proponować testy, i pełnić rolę wyroczni, ale sam z siebie nie wie, jakie zachowanie jest poprawne — wnioskuje je albo z kodu (co grozi tautologią: test utrwala to, co kod *robi*, a nie co *powinien* robić), albo z wymagań (lepiej, ale tylko jeśli wymagania istnieją i są jednoznaczne). Cała wartość tego rozdziału jest ograniczona przez to, jak dobrze radzimy sobie z problemem wyroczni — dlatego tak wielką wagę mają grounding (4.3), człowiek w pętli i dobrze opisana intencja.

### 4.2 Generowanie testów: źródła wejścia i ryzyko over-fittingu

Generowanie testów to najbardziej oczywiste zastosowanie, ale jego jakość zależy całkowicie od tego, *z czego* generujemy:

- **Z wymagań i historyjek użytkownika** — najwartościowsze źródło, bo opisuje *intencję*, czyli właśnie to, czego brakuje wyroczni. LLM przekłada historyjkę i kryteria akceptacji na konkretne przypadki, stosując techniki z sekcji 1.3 (wartości brzegowe, klasy równoważności). Warunek: wymagania muszą istnieć i być precyzyjne, bo każda dwuznaczność wprost przenosi się na testy.
- **Z kodu** — model czyta funkcję czy endpoint i generuje testy. Szybkie, ale obarczone ryzykiem **over-fittingu / tautologii**: test koduje istniejące zachowanie, więc utrwala także istniejące błędy zamiast je wykrywać. Bywa to świadomie pożądane przy tzw. testach charakteryzujących (characterization tests) wokół zastanego kodu (legacy) przed refaktorem, gdzie celem jest właśnie „zamrożenie" obecnego zachowania — ale wtedy trzeba to wprost nazwać.
- **Z ruchu produkcyjnego** — zapisany realny ruch (logi, nagrania żądań) zamieniany na testy i realistyczne dane. Wychwytuje prawdziwe wzorce użycia, których nikt by nie wymyślił przy biurku; wymaga anonimizacji danych wrażliwych.
- **Z raportów błędów** — z treści zgłoszenia model generuje test reprodukujący błąd (regression test), który najpierw failuje, a po naprawie pilnuje, by problem nie wrócił. Naturalne wsparcie cyklu poprawiania błędów.

Wspólny mianownik: wygenerowane testy trzeba przejrzeć (problem wyroczni), a generacja jest wsparciem autora, nie autopilotem. Drugi wątek to unikanie nadmiarowości — generowanie dziesiątego niemal identycznego testu obniża wartość i podnosi koszt utrzymania, co prowadzi nas do groundingu i do analizy pokrycia (4.11).

### 4.3 Grounding: RAG i context engineering dla generacji

Naiwna generacja, ignorująca istniejące repozytorium, produkuje testy, które się nie kompilują, dublują już istniejące, łamią konwencje i wymyślają na nowo obiekty stron czy fixtury. Lekarstwem jest **grounding** — i tu wprost przekłada się Twoje doświadczenie z RAG i structured output:

- **RAG nad repozytorium** testów, page objektów, fixtur, helperów i konwencji zespołu sprawia, że model używa istniejących komponentów ponownie, trzyma się nazewnictwa i nie duplikuje pokrycia.
- **Context engineering** to świadome decydowanie, *co* podać modelowi: właściwy fragment specyfikacji, kod pod testem, powiązane istniejące testy, DOM lub OpenAPI, przewodnik stylu. Jakość wygenerowanych testów zależy bardziej od jakości kontekstu niż od rozmiaru modelu.
- **Structured output** — wymuszenie, by model emitował testy w ściśle określonym schemacie albo w DSL projektu, znacznie ułatwia ich walidację i automatyczną integrację.

To jest jeden z najmocniejszych mostów do Twojego CV: dokładnie te techniki (LangChain/LangGraph, RAG, structured output) decydują o tym, czy generator testów jest zabawką, czy narzędziem produkcyjnym.

### 4.4 Język naturalny a test (dwukierunkowo)

Most między językiem naturalnym a wykonywalnym testem działa w obie strony:

- **Opis → test**: scenariusz opisany po ludzku zamieniany w wykonywalny test. Obniża próg wejścia (testerzy manualni, product ownerzy mogą definiować scenariusze). To ewolucja idei BDD/Gherkin, ale bez sztywnej składni — kosztem rosnącego ryzyka niejednoznaczności i niedeterminizmu (ten sam opis może dać różne testy). Stąd kluczowa zasada: opis należy „skompilować" do deterministycznego, wersjonowanego artefaktu, a nie odpalać go na żywo przy każdym przebiegu.
- **Test → opis**: z istniejącego testu lub kodu generujemy czytelny opis, dokumentację albo raport „co ten test właściwie sprawdza". Pomaga w utrzymaniu, onboardingu, audycie pokrycia w języku biznesu oraz w śledzeniu powiązań wymaganie–test (traceability).

Niuans do zapamiętania: warstwę czytelną dla człowieka i wykonywalny artefakt trzyma się osobno — język naturalny jest interfejsem, ale to skompilowany, deterministyczny test pozostaje źródłem prawdy.

### 4.5 LLM jako wyrocznia i generator asercji

To najbardziej ryzykowne, a zarazem najbardziej wartościowe zastosowanie — bezpośrednie zmierzenie się z problemem wyroczni. LLM potrafi zaproponować asercje, czyli to, *co* sprawdzić w odpowiedzi lub stanie. Jest to cenne, bo autorzy notorycznie asercjonują za słabo (kruche, płytkie testy — wraca pułapka pokrycia z 1.4). Ryzyko: model bywa pewną siebie, lecz błędną wyrocznią — generuje „prawdopodobnie poprawne" oczekiwania, które są halucynacją poprawności. Dlatego stosuje się wzorce, które omijają potrzebę absolutnej wyroczni:

- **Człowiek w pętli (HITL)** — model proponuje asercje, człowiek je zatwierdza.
- **Testowanie metamorficzne** — zamiast znać dokładny oczekiwany wynik, sprawdzamy *relacje*, które muszą zachodzić (np. posortowanie dwa razy daje to samo co raz; przeskalowanie nie zmienia liczby elementów; porównanie z implementacją referencyjną). LLM dobrze radzi sobie z proponowaniem takich relacji.
- **Testowanie własnościowe (property-based)** — model proponuje własności/niezmienniki, a framework (Hypothesis, jqwik) generuje setki wejść je sprawdzających. Bardzo mocne połączenie, bo łączy kreatywność modelu z deterministyczną maszynerią.

### 4.6 Testy wizualne, UI i dostępność z modelami multimodalnymi

Modele multimodalne (vision) czytają zrzuty ekranu i DOM, co otwiera obszary nieosiągalne dla klasycznych asercji:

- **Regresja wizualna ponad pixel-diff** — porównanie piksel po pikselu jest hałaśliwe i samo bywa źródłem flakiness (drobna zmiana renderowania psuje test). Model multimodalny ocenia *semantyczną* równoważność („czy to wciąż ta sama, poprawna strona?"), odróżniając zmianę zamierzoną od regresji i redukując fałszywe alarmy.
- **Walidacja UI** — model ocenia ze zrzutu, czy ekran odpowiada projektowi, zawiera oczekiwane elementy i czy układ się nie rozjechał.
- **Dostępność** — model wychwytuje braki (brakujący tekst alternatywny, słaby kontrast, nielogiczną strukturę) wykraczające poza to, co złapie checker regułowy (nawiązanie do a11y z 1.2).

Zastrzeżenia są te same co zwykle: niedeterminizm modelu, koszt i latencja — dlatego vision stosuje się raczej jako sędziego/triage, utrzymując deterministyczne punkty odniesienia tam, gdzie się da. To także domyka wątek artefaktów diagnostycznych z 2.6, które są tu wejściem.

### 4.7 Self-healing locators

Bezpośrednia odpowiedź na ból kruchych selektorów z 2.2. **Mechanizm**: gdy selektor przestaje pasować, system zamiast od razu failować szuka elementu po innych sygnałach. Na etapie pisania zapamiętuje o elemencie wiele cech (tekst, rola, dostępna nazwa, sąsiedzi, pozycja), a po zmianie DOM dopasowuje najlepszego kandydata — heurystyką, embeddingami albo LLM-em — i opcjonalnie proponuje poprawiony selektor.

**Granice zaufania** są tu najważniejsze i często stanowią pytanie na rozmowie. Self-healing potrafi *zamaskować prawdziwy błąd*: jeśli element zniknął, bo to autentyczna regresja, „uleczenie" do czegoś podobnego daje fałszywe zaliczenie testu. Dlatego healing musi być: obserwowalny (logowany, sygnalizowany jako ostrzeżenie), przeglądalny (proponuje poprawkę do akceptacji człowieka, nie po cichu przepisuje test) i ograniczony (próg pewności — lepiej, by test padł, niż żeby zgadywał na ślepo). To świadomy handel części determinizmu za odporność i sztandarowy przykład „AI online", do którego wraca sekcja 6 przy granicy deterministyczny kod vs LLM.

### 4.8 Agentowe i eksploracyjne E2E (tool use)

Tu wprost wchodzi Twoje doświadczenie z agentami i tool use. Agent samodzielnie nawiguje aplikacją, a **runner (Selenium/Playwright) staje się narzędziem (tool)**, które agent wywołuje: kliknij, wpisz, odczytaj DOM, zrób zrzut. Agent dostaje cel („dokończ zakup", „eksploruj i znajdź zepsute stany"), postrzega stan (DOM/zrzut), decyduje o następnej akcji i obserwuje wynik — klasyczna pętla postrzegaj–decyduj–działaj. To testowanie eksploracyjne z intencją: odkrywa ścieżki i przypadki brzegowe, których nikt nie oskryptował, i znajduje wywrotki czy ślepe uliczki.

Architektonicznie (zapowiedź sekcji 6) pojawiają się tu znajome wzorce: planner/executor/krytyk, guardrails (żadnych destrukcyjnych akcji na produkcji, praca w piaskownicy) oraz — co kluczowe dla pogodzenia agenta z wymogiem determinizmu — agent służy do *odkrywania* scenariuszy, które następnie *utrwala się* jako deterministyczne testy regresyjne, zamiast traktować sam nondeterministyczny przebieg agenta jako zestaw regresyjny.

### 4.9 Utrzymanie i automatyczna naprawa testów

Utrzymanie jest dominującym kosztem E2E (motyw przewija się przez cały dokument), więc to tutaj AI daje największy zwrot:

- Gdy test pęka z powodu zmiany UI/API, a nie realnego błędu, LLM analizuje różnicę i proponuje zaktualizowany test, selektor lub asercję — pokrewne self-healingowi, ale na poziomie kodu i w formie pull requesta.
- Wykrywanie i refaktoryzacja kruchych testów, usuwanie martwych i zduplikowanych.
- Utrzymywanie testów w zgodzie ze zmianami specyfikacji (różnica w OpenAPI → aktualizacja dotkniętych testów API).

Zasada przewodnia jak wyżej: zmiany prezentowane jako przeglądalne diffy/PR-y, nigdy po cichu.

### 4.10 Triage awarii: klasteryzacja i wykrywanie flaky

Gdy padają setki testów, potrzebujesz wiedzieć *dlaczego* i *ile jest odrębnych przyczyn*:

- **Klasteryzacja awarii według przyczyny źródłowej** (embeddingi nad stack trace'ami, logami, diffami) pozwala powiedzieć „te 40 awarii to jeden błąd, a tamte 3 to inny", redukując szum i przyspieszając reakcję.
- **Wykrywanie i predykcja flaky** — model nad historią przebiegów i kontekstem zmiany ocenia, czy awaria jest prawdopodobnie flaky, czy realna, albo przewiduje, które testy są niestabilne. Pozwala kwarantannować flaky zamiast ślepo ponawiać cały zestaw (antywzorzec z 3.3).
- **Hipotezy o przyczynie** — LLM czyta artefakty awarii (trace, logi, ostatni diff z 2.6) i proponuje prawdopodobną przyczynę, przyspieszając debugowanie.

To domyka pętlę z 2.6: bogata diagnostyka istnieje właśnie po to, by stać się wejściem dla modelu.

### 4.11 Pokrycie, priorytetyzacja i selekcja (Test Impact Analysis)

- **Analiza luk pokrycia** — wykraczająca poza pokrycie liniowe ku pokryciu *behawioralnemu*: model rozumuje, jakich scenariuszy i przypadków brzegowych brakuje względem specyfikacji, i proponuje brakujące (nawiązanie do technik z 1.3 i pułapki pokrycia z 1.4). Może celować w mutanty, które przetrwały mutation testing, generując testy faktycznie wzmacniające zestaw.
- **Test Impact Analysis / selekcja** — dla danej zmiany kodu przewiduje, które testy są istotne, i uruchamia tylko je (lub najpierw je), skracając czas CI. Klasyczne podejścia (mapowanie zależności) wzmacnia tu rozumienie diffa przez LLM.
- **Priorytetyzacja oparta na ryzyku** — porządkuje testy według iloczynu prawdopodobieństwa awarii i wpływu biznesowego, by najcenniejsze dawały najszybszy feedback.

To zastosowanie ma wysoki zwrot dla platformy, bo uderza wprost w czas i koszt CI.

### 4.12 Generowanie syntetycznych danych testowych

LLM generuje realistyczne, zróżnicowane i zgodne ze schematem dane: przypadki brzegowe, dane zlokalizowane (nazwiska, adresy), wejścia adwersarialne (pod bezpieczeństwo i fuzzing) oraz dane spełniające złożone więzy i relacje. Bije naiwne generatory (faker) pod względem realizmu i pokrycia przypadków brzegowych, a przy okazji potrafi celować w konkretne klasy równoważności i wartości brzegowe z 1.3. Zastrzeżenia: prywatność (dane syntetyczne zamiast produkcyjnych to wręcz przewaga compliance), determinizm (wygenerowane zbiory trzeba zamrozić — seed/snapshot — by testy pozostały powtarzalne, a nie regenerować ich na żywo) oraz zgodność ze schematem (structured/constrained output).

### 4.13 Granice, ryzyka i antywzorce (spinka do sekcji 5 i 6)

Świadomość ograniczeń jest tu najmocniejszym sygnałem dojrzałości na rozmowie — warto umieć wyłożyć je wprost:

- **Problem wyroczni i fałszywa pewność** — wygenerowany test może być zielony i błędny zarazem. AI wspiera, ale to człowiek odpowiada za poprawność; nie wolno wpuszczać niezweryfikowanych wygenerowanych testów jako siatki bezpieczeństwa.
- **Niedeterminizm generatora vs determinizm testu** — generuj offline, zamroź artefakt, wersjonuj go; nie trzymaj LLM-a na ścieżce asercji tam, gdzie da się tego uniknąć (rozwinięcie w sekcji 5).
- **Koszt i latencja** — LLM w gorącej ścieżce (healing w runtime, agent) kosztuje tokeny i czas; trzeba budżetować, cache'ować i mieć deterministyczny fallback (sekcja 6).
- **Paradoks utrzymania** — AI generujące dziesięciokrotnie więcej testów potrafi wygenerować dziesięciokrotnie więcej utrzymania; liczy się *netto* redukcja kosztu utrzymania, nie surowa liczba testów.
- **Bezpieczeństwo i dane** — karmienie modelu danymi produkcyjnymi, DOM-em czy sekretami; PII; ryzyko prompt injection z treści aplikacji do eksplorującego agenta.
- **Guardrails i HITL jako nić przewodnia** — każda mocna zdolność z tego rozdziału jest obwarowana przeglądem, obserwowalnością i jasną granicą między tym, co deterministyczne, a tym, co robi LLM (sekcja 6).
- **Właściwe metryki sukcesu** (sekcja 5) — nie liczba wygenerowanych testów, lecz defect escape rate, odsetek flaky, koszt utrzymania i czas CI.

## 5. Ewaluacja samego systemu AI do testów (poziom meta)

Ten rozdział wchodzi o poziom wyżej: przestajemy pytać, czy działa aplikacja, a zaczynamy pytać, czy działa AI, które tę aplikację testuje. Warto nazwać wprost tkwiącą tu rekursję — budujesz narzędzie do testowania, więc musisz przetestować swój tester. To czyni ewaluację rdzeniem inżynierskiej wiarygodności platformy i częstym, rozróżniającym tematem na rozmowie: wielu kandydatów potrafi coś wygenerować LLM-em, niewielu potrafi udowodnić, że to działa i się nie psuje.

### 5.1 Rama: co właściwie oceniamy

Pierwszym krokiem jest rozdzielenie trzech warstw oceny, bo ich mylenie to częsty błąd:

1. **Jakość artefaktu** — pojedynczego wygenerowanego testu: czy jest poprawny, mocny i czytelny.
2. **Jakość decyzji AI online** — uleczenia selektora, klasyfikacji flaky, hipotezy triage, ruchu agenta.
3. **Jakość całej platformy jako produktu** — czy w skali zespołu spada defect escape rate i koszt utrzymania, a rośnie zaufanie.

Każda warstwa wymaga innych metryk i innej metodyki, a sukces na poziomie 1 nie gwarantuje sukcesu na poziomie 3 — można generować technicznie poprawne testy, które nie przekładają się na mniej błędów na produkcji.

### 5.2 Jakość wygenerowanego testu (artefaktu)

Dobry test ma kilka wymiarów, które trzeba mierzyć osobno:

- **Poprawność techniczna** — kompiluje się, uruchamia, jest deterministyczny i przechodzi na poprawnym kodzie.
- **Siła wykrywania** — failuje na zepsutym kodzie. Test, który zawsze przechodzi, jest bezwartościowy; tu wraca tautologia i over-fitting z 4.2 oraz pułapka pokrycia z 1.4.
- **Pokrycie behawioralne** — czy dotyka istotnych przypadków (brzegowych, negatywnych), a nie tylko szczęśliwej ścieżki.
- **Czytelność i utrzymywalność** — test trudny do zrozumienia i utrzymania sam generuje dług.

Szczególnie ważne są dwa rodzaje błędów, w terminologii dostosowanej do testów:

- **False positive** — test failuje, choć kod jest poprawny (test zły lub flaky). Koszt to szum i erozja zaufania: zespół zaczyna ignorować czerwień.
- **False negative** — test przechodzi, choć kod jest zepsuty (przepuszcza defekt). To najgroźniejszy przypadek: fałszywa pewność, bezpośrednia konsekwencja problemu wyroczni z 4.1 — błędna wyrocznia daje zielony, lecz bezwartościowy test.

W tej domenie false negative boli bardziej niż false positive, bo niweczy sam cel istnienia testów.

### 5.3 Jakość decyzji AI online

Generowanie wytwarza artefakt offline, ale platforma podejmuje też decyzje w locie, które trzeba oceniać osobnym aparatem:

- **Self-healing** — dwie metryki naraz: czy uleczył, gdy powinien (recall odporności), i czy *nie* zamaskował realnej regresji (precyzja, by nie produkować false negative). Ten drugi wymiar jest krytyczny i wprost wynika z granic zaufania z 4.7.
- **Triage i klasteryzacja** — czy klaster faktycznie odpowiada jednej przyczynie (czystość klastrów) i jak trafne są hipotezy o przyczynie źródłowej.
- **Wykrywanie flaky** — precision/recall klasyfikacji flaky vs realna awaria.
- **Agent eksploracyjny** — ile realnych defektów odkrył, jakie pokrycie eksploracji osiągnął i jaki jest odsetek fałszywych zgłoszeń (szum).

### 5.4 Metodyka: golden sets, eval harness, mutation testing, LLM-as-judge

Aby mierzyć to wszystko powtarzalnie, składa się kilka narzędzi:

- **Golden set (zbiór referencyjny)** — ręcznie zweryfikowane pary wejście → oczekiwany dobry wynik (test lub decyzja). Wersjonowany i traktowany jak aktywo; to podstawa każdej powtarzalnej oceny.
- **Eval harness** — automatyczne odpalanie modelu na golden secie i liczenie metryk, uruchamiane przy każdej zmianie modelu, promptu czy kontekstu. Czyni jakość mierzalną i porównywalną między wersjami (regresja jakości).
- **Mutation testing jako twarda, deterministyczna wyrocznia** — wstrzykujesz drobnego buga i sprawdzasz, czy wygenerowany test go łapie. Omija subiektywność i daje obiektywny sygnał „czy ten test cokolwiek wykrywa", wyjątkowo cenny akurat w tej domenie.
- **LLM-as-a-judge** — użycie LLM do oceny jakości testów/asercji w skali. Wygodne, ale obarczone własnymi biasami i niespójnością; trzeba je kalibrować względem ocen ludzkich i mierzyć zgodność. Traktuj sędziego-LLM jako tani filtr wstępny, nie ostateczną prawdę.
- **Offline vs online** — offline na golden secie; online przez shadow mode (AI działa równolegle, nie wpływając na wynik, a Ty porównujesz jego decyzje z rzeczywistością) oraz testy A/B przy stopniowym wdrażaniu.

### 5.5 Determinizm vs niedeterminizm — minimalizacja powierzchni

To centralne napięcie całej domeny: testy muszą być deterministyczne (1.4), a LLM z natury nie jest. Sztuka polega na **minimalizacji powierzchni niedeterminizmu**:

- Najważniejsza zasada: **generuj offline, zamroź artefakt, wersjonuj**. LLM tworzy test raz, a potem znika z toru wykonania — odpala się deterministyczny, zatwierdzony kod, nie model na żywo.
- `temperature=0` i seed tam, gdzie to możliwe (choć nie gwarantują pełnej powtarzalności), oraz structured/constrained output zawężający przestrzeń wyjścia.
- **Brama jakości po generacji** — deterministyczna walidacja (kompilacja, zgodność ze schematem, mutation check) odsiewa złe wyjścia, zanim trafią do zestawu.
- Dla nieuniknionego AI online (healing, agent) — progi pewności, deterministyczne fallbacki, idempotentne narzędzia, a wynik agenta utrwalany jako deterministyczny test (4.8).

Kluczowe rozróżnienie: niedeterminizm w *generacji* jest akceptowalny, bo obwarowany bramą jakości i przeglądem; niedeterminizm w *wyniku wykonania testu* jest nieakceptowalny, bo to po prostu flakiness. Umiejętność postawienia tej granicy to mocny punkt na rozmowie i bezpośrednia zapowiedź sekcji 6.

### 5.6 Regresja jakości i dryf

Platforma oparta na LLM psuje się także bez Twojej ingerencji, więc trzeba aktywnie pilnować trzech rodzajów dryfu:

- **Dryf modelu** — dostawca aktualizuje model i jego zachowanie się zmienia, przez co jakość generacji czy decyzji może spaść z dnia na dzień. Obrona: pinowanie konkretnej wersji modelu i przepuszczanie każdej zmiany wersji przez eval harness (regression eval), zanim ją zaakceptujesz.
- **Dryf aplikacji i danych** — aplikacja ewoluuje, DOM i API się zmieniają, golden set się starzeje i przestaje reprezentować rzeczywistość; wymaga okresowego odświeżania.
- **Dryf promptu i kontekstu** — prompt to kod: każda jego zmiana powinna być wersjonowana i przejść przez eval, a nie być wprowadzana „na czuja".

Do tego dochodzi monitoring produkcyjny: śledzenie metryk online w czasie i alerty na degradację (np. nagły spadek odsetka akceptowanych uleczeń).

### 5.7 Metryki w warstwach

Metryki warto poukładać warstwami, dopasowanymi do warstw oceny z 5.1:

- **Jakość testów** — mutation score, skuteczność wykrywania defektów (precision/recall), odsetek false positive/false negative, flaky rate generowanych testów.
- **Decyzje AI online** — precyzja i recall self-healingu, trafność triage, odsetek spraw rozwiązanych automatycznie.
- **Operacyjne i biznesowe** — defect escape rate (1.4), *netto* koszt utrzymania, czas CI, koszt w tokenach/$ na test, latencja. To one łączą platformę z wartością dla biznesu.
- **Adopcja i zaufanie** — odsetek wygenerowanych testów zaakceptowanych bez zmian wobec nadpisanych czy odrzuconych. To bodaj najszczerszy sygnał realnej wartości, bo mierzy zachowanie użytkowników, a nie deklaracje.

Antywzorcem są **metryki próżności**: liczba wygenerowanych testów albo samo pokrycie procentowe. Gdy metryka staje się celem, przestaje być dobrą metryką (prawo Goodharta) — łatwo wygenerować tysiące bezwartościowych, zielonych testów i pochwalić się świetnymi liczbami przy zerowej wartości.

### 5.8 Pętla feedback i człowiek w pętli jako ewaluacja ciągła

Akceptacje i odrzucenia ludzi to nie tylko bramka jakości — to ciągły, darmowy sygnał ewaluacyjny i zarazem dane uczące. Zamknięcie pętli polega na tym, że decyzje z przeglądu (zaakceptowano, poprawiono w taki sposób, odrzucono z takiego powodu) zasilają poprawę promptów, przykładów few-shot, groundingu i samego golden setu. Dzięki temu platforma uczy się na własnych błędach w sposób mierzalny. Architekturę tej pętli rozwijam w sekcji 6.

### 5.9 Ekonomia: koszt, jakość i ROI

Ewaluacja nie odpowiada wyłącznie na pytanie „czy działa", ale i „czy się opłaca". Wchodzą tu znane dźwignie: routing i kaskadowanie modeli (tani model do prostych przypadków, drogi tylko do trudnych), cache'owanie oraz fundamentalna decyzja, kiedy w ogóle użyć LLM, a kiedy wystarczy deterministyczny kod lub klasyczne ML. Każda zdolność z rozdziału 4 powinna przejść próbę ROI: czy oszczędność czasu i utrzymania przewyższa koszt tokenów, latencji oraz ryzyka. Często najlepszą odpowiedzią jest hybryda — LLM do części kreatywnej, tani deterministyczny mechanizm do reszty.

### 5.10 Pułapki ewaluacji

Na koniec katalog błędów, które warto umieć nazwać:

- **Prawo Goodharta / granie metryką** — optymalizacja pod liczbę testów albo coverage zamiast pod realne wykrywanie defektów.
- **Kontaminacja / przeciek golden setu** — gdy przykłady ewaluacyjne wyciekają do kontekstu lub promptu, metryki kłamią (zawyżają).
- **Zbyt mała próba i wariancja** — ocena na kilku przykładach przy niedeterministycznym modelu jest niewiarygodna; potrzebna jest odpowiednia liczność i świadomość rozrzutu między uruchomieniami.
- **Bias i niespójność sędziego-LLM** — ocenianie modelu modelem bez kalibracji do ludzi.
- **Mierzenie proxy zamiast wyniku** — pokrycie zamiast uciekających defektów, liczba testów zamiast skróconego czasu i kosztu. Dobre proxy bywa potrzebne, ale nie wolno mylić go z celem.

## 6. Architektura platformy do automatyzacji testów (bo masz ją budować)

Tu wszystko się zbiega: nie chodzi już o używanie AI do testów, lecz o zbudowanie platformy, która to robi w skali zespołu. Warto od razu nazwać zasadę organizującą całość — **deterministyczny rdzeń, AI na obrzeżach**. Istniejąca infrastruktura (Selenium, REST Assured, CI) pozostaje deterministycznym kręgosłupem, a AI dokłada się jako otaczające go usługi: obwarowane bramą jakości, przeglądem i obserwowalnością. Drugą osią porządkującą jest podział offline/online z sekcji 4–5, a trzecią zasadą — nieprzekombinowanie: po agenta sięgasz dopiero wtedy, gdy deterministyczny pipeline albo pojedyncze wywołanie LLM nie wystarczą.

### 6.1 Zasady architektoniczne (rama)

Pięć założeń, na których opiera się reszta rozdziału:

- **AI opakowuje, nie zastępuje** istniejącej infrastruktury — runner i CI zostają rdzeniem, AI jest warstwą dokładaną wokół.
- **Deterministyczny rdzeń, LLM na obrzeżach**, z jawnie postawioną granicą (6.4).
- **Offline vs online** jako główna oś projektowa (6.5), bo te dwa reżimy mają zupełnie inne wymagania.
- **Drabina złożoności** — zaczynaj od najprostszego mechanizmu wystarczającego do zadania (kod → pojedyncze wywołanie LLM → łańcuch → agent → system wieloagentowy); agent to ostateczność, nie domyślność.
- **Każda zdolność AI ma bramę jakości, przegląd i obserwowalność** (wprost z sekcji 5) — to nie dodatki, lecz warunek wpuszczenia zdolności na produkcję.

### 6.2 Komponenty logiczne

Platformę da się rozłożyć na kilkanaście współpracujących elementów:

- **Orchestrator** — koordynuje przepływy (generuj → waliduj → przedstaw do przeglądu → zintegruj). Bywa prostym pipeline'em, a przy złożonych, warunkowych przepływach grafem (np. LangGraph).
- **Warstwa groundingu/kontekstu** — retrieval nad repozytorium, specyfikacją i konwencjami (RAG z 4.3), dostarczający modelowi właściwy kontekst.
- **Generatory** — usługi wytwarzające testy, asercje i dane dla różnych poziomów (API, E2E).
- **Brama jakości** — deterministyczna walidacja wygenerowanych artefaktów (kompilacja, zgodność ze schematem, mutation check) z 5.5.
- **Executory / runnery** — warstwa wykonania opakowująca Selenium/Playwright/REST Assured za wspólnym interfejsem (adapter/repozytorium), tak by dało się je wymieniać, a reszta platformy nie była przywiązana do jednego narzędzia.
- **Magazyn i wersjonowanie testów** — testy jako kod w git (źródło prawdy), plus magazyn artefaktów i golden setów.
- **Warstwa danych testowych** — generacja i zarządzanie danymi (4.12), fixtury, seedy.
- **Model gateway** — pojedynczy punkt dostępu do modeli: routing/kaskadowanie, cache, limity i rozliczanie kosztu (6.7).
- **Raportowanie i obserwowalność** — wyniki, trace, metryki (6.9).
- **Pętla feedback** — zbieranie decyzji z przeglądu jako sygnału uczącego (5.8).
- **Eval harness** — offline ocena jakości (sekcja 5), będąca de facto CI dla samej platformy.

### 6.3 Wzorce agentowe

Tu wprost przekłada się Twoje doświadczenie z systemami agentowymi, ale kluczem jest powściągliwość:

- **Drabina złożoności** — deterministyczny kod → pojedyncze wywołanie LLM → łańcuch → agent z narzędziami → system wieloagentowy. Wspinasz się tylko, gdy prostsze naprawdę nie wystarcza.
- **Planner / executor / krytyk** — planista rozkłada cel, wykonawca działa narzędziami, krytyk ocenia wynik i wymusza samokorektę. Naturalne dla generacji i eksploracji.
- **Supervisor / multi-agent** — wyspecjalizowani agenci (generator API, generator E2E, agent triage) pod nadzorcą; sięgasz po to przy realnej potrzebie podziału, nie dla mody.
- **Tool use** — runner jako narzędzie agenta (4.8); narzędzia muszą być idempotentne i bezpieczne.
- **Stan, pamięć, checkpointing** — długie przebiegi agenta wymagają trwałego stanu (checkpointery), by móc je wznawiać, audytować i wstrzykiwać człowieka (interrupt/HITL).
- **HITL i guardrails** traktowane jako elementy pierwszorzędne, nie dodatek (6.8).

### 6.4 Granica deterministyczny kod vs LLM

To kręgosłup architektury i bezpośrednie odzwierciedlenie minimalizacji niedeterminizmu z 5.5. Reguła: LLM tam, gdzie naprawdę potrzeba rozumienia języka, kreatywności i radzenia sobie z niejednoznacznością; deterministyczny kod albo klasyczne ML wszędzie indziej. Powierzchnię LLM minimalizujesz świadomie.

Pomocna ramka decyzyjna: czy da się to zrobić regułą, zapytaniem lub parserem? Jeśli tak — bez LLM. Czy wynik musi być powtarzalny i leży w gorącej ścieżce wykonania? Jeśli tak — wypchnij LLM do offline albo otocz go bramą walidacji. Każde użycie LLM powinno mieć deterministyczny fallback i walidację wyjścia, żeby model nigdy nie był ostatnim, niekontrolowanym ogniwem.

### 6.5 AI offline vs online (dwa reżimy o różnych SLO)

To pierwsza rzecz, którą warto naszkicować na tablicy, bo determinuje wybór modelu, cache i infrastrukturę:

- **Offline** (generacja, analiza pokrycia, eval, klasteryzacja po fakcie) — działa wsadowo, latencja jest nieistotna, koszt amortyzuje się w czasie, można sięgnąć po najmocniejszy (droższy) model, a wynik jest wersjonowany i raz na zawsze zamrożony. Ryzyko niskie, bo na końcu jest przegląd.
- **Online** (self-healing, agent w runtime, triage na żywo) — działa w pętli CI, więc latencja jest krytyczna, koszt liczy się per uruchomienie, preferujesz tani i szybki model, agresywny cache, twarde limity czasu, guardrails i fallback. Ryzyko wyższe, bo nie ma człowieka w pętli na bieżąco.

Ten podział napędza praktycznie wszystkie pozostałe decyzje infrastrukturalne.

### 6.6 Integracja z CI/CD

Platforma musi wpiąć się w istniejący potok, nie obok niego:

- **Punkty wpięcia** — wyzwalane przez pull request generowanie testów (jako PR do przeglądu), selekcja i priorytetyzacja testów (TIA z 4.11) dla skrócenia CI, uruchamianie zestawów, raport zwrotny do PR oraz bramkowanie merge'a.
- **Kiedy co** — szybkie, wyselekcjonowane testy pre-merge; pełny zestaw nocą; generacja i eval poza ścieżką krytyczną, by nie wydłużać pętli developera.
- **Shadow mode w CI** (5.4) do bezpiecznego wdrażania nowych zdolności bez wpływu na wynik.
- **Środowiska efemeryczne per-PR** (2.5) jako podłoże dla E2E.
- **Żelazna zasada** — generacja zawsze jako artefakt do przeglądu, nigdy automatyczny merge niezweryfikowanych testów (4.13).

### 6.7 Skalowanie, latencja, koszt, cache

- **Zrównoleglenie wykonania** (Grid/chmura z 2.5) — zwykle główna dźwignia na czas E2E, niezależnie od AI.
- **Model gateway** — routing i kaskadowanie (tani model najpierw, eskalacja do drogiego tylko gdy trzeba — 5.9), prompt caching, cache semantyczny wyników, batching oraz kontrola współbieżności i limitów.
- **Kontrola kosztu** — budżety, rozliczanie tokenów per zdolność, kolejki dla pracy offline.
- **Latencja** — trzymaj LLM poza krytyczną ścieżką wykonania, gdzie się da, i prekomputuj offline. Najtańszy i najszybszy LLM to ten, którego nie wywołujesz, bo wynik jest już zamrożony.

### 6.8 Bezpieczeństwo, izolacja i guardrails

- **Sekrety** — zero wartości zaszytych w kodzie; menedżer sekretów lub zmienne środowiskowe (3.3), maskowanie w logach i promptach.
- **Dane wrażliwe i governance** — DOM, logi i ruch produkcyjny karmiące model mogą zawierać PII; konieczna anonimizacja i kontrola, a dla danych najwrażliwszych rozważenie modelu self-hosted lub lokalnego zamiast publicznego API. Trzeba wiedzieć, gdzie dane wypływają.
- **Sandbox agenta** — brak akcji destrukcyjnych, izolowane środowisko (nigdy produkcja), kontrola ruchu wychodzącego; agent klikający „po omacku" musi być ogrodzony.
- **Prompt injection** — treść aplikacji (DOM, teksty) to niezaufane wejście trafiające do agenta i triage; trzeba zakładać, że ktoś może umieścić w stronie instrukcje próbujące przejąć kontrolę nad modelem (4.13).
- **Izolacja danych testowych** (1.4, 2.5) oraz kontrola dostępu i audyt akcji podejmowanych przez AI.

### 6.9 Obserwowalność i operacje (LLMOps)

- **Tracing wywołań LLM** — co, z jakim kontekstem, jakim modelem i jakim kosztem; odtwarzalność decyzji AI jest wymogiem, nie luksusem.
- **Wspólne wersjonowanie** — prompty, wersja modelu, golden sety i kod razem, tak by każdą decyzję dało się zreprodukować.
- **Dashboardy** kosztu, latencji i jakości oraz alerty na dryf (5.6).
- **Logowanie decyzji online** (uleczenia, klasyfikacje) do późniejszej oceny i zasilania pętli feedback.

### 6.10 Niezawodność i degradacja

AI nie może być pojedynczym punktem awarii CI. Gdy gateway lub model padnie albo wyczerpie się budżet, platforma musi zgrabnie zejść do zachowania deterministycznego: uruchomić istniejące testy, pominąć healing, zachować się bezpiecznie (fail safe). Do tego potrzebne są limity czasu, świadome ponawianie (z pamięcią o maskowaniu z 3.3) i bezpieczniki (circuit breaker) wokół wywołań modelu. Złota zasada: developer ma móc domknąć CI nawet wtedy, gdy cała warstwa AI leży.

### 6.11 Stopniowe wdrażanie (dojrzałość platformy)

Najlepsza strategia to crawl-walk-run: zacznij od najbezpieczniejszych i najwyżej ROI zdolności offline (generacja testów API z OpenAPI — 3.4), udowodnij ich wartość evalami (sekcja 5), a dopiero potem rozszerzaj na ryzykowne funkcje online (self-healing, agent) za flagami i w shadow mode. To zarazem najlepsza odpowiedź na rozmowie na pytanie „jak byś to wdrożył" — pokazuje, że rozumiesz ryzyko i mierzysz wartość, zamiast rzucać agentem prosto na produkcję.

### 6.12 Wrap, nie replace; build vs buy

Platforma opakowuje istniejące narzędzia (Selenium, REST Assured, CI), dokładając warstwę AI, zamiast je zastępować — to niższe ryzyko i wykorzystanie dojrzałej infrastruktury. Decyzja build vs buy sprowadza się do tego, że część zdolności oferują gotowe narzędzia AI-native: integrujesz je tam, gdzie budowanie nie ma sensu, a budujesz tam, gdzie potrzebna jest ścisła integracja z własnym stackiem i danymi. Katalog konkretnych narzędzi do tej decyzji — w sekcji 7.

## 7. Krajobraz narzędzi (orientacyjnie, bez przywiązania)

To mapa, nie ranking. Rekrutacja wprost zaznaczyła, by nie fiksować się na konkretnych technologiach, więc wartość tego rozdziału leży w **osiach porównania** (7.4), a nie w nazwach — narzędzia zmieniają się szybko, a deklaracje producentów bywają hojniejsze od rzeczywistości. Traktuj poniższe jako orientację i weryfikuj aktualny stan, zanim coś wybierzesz.

### 7.1 E2E klasyczne (codeful)

Recap pozycjonowania z rozdziału 2: to narzędzia, w których test pisze się jako kod.

- **Selenium** — standard W3C WebDriver, najszersze wsparcie języków i przeglądarek, dojrzałość, Grid do skalowania. Cena: sterowanie out-of-process (latencja per polecenie) i historyczny brak auto-waitingu, czyli więcej boilerplate'u i ręcznej synchronizacji.
- **Playwright** (Microsoft) — out-of-process, ale przez trwałe połączenie; wbudowany auto-waiting, wiele przeglądarek (Chromium, Firefox, WebKit) i języków, znakomity trace viewer oraz codegen. Współczesny domyślny wybór dla nowych projektów.
- **Cypress** — działa in-process, w pętli przeglądarki; świetny developer experience i debugowanie z „podróżą w czasie", auto-retry. Kosztem są ograniczenia (głównie JavaScript/TypeScript, rodzina Chromium jako pierwszoplanowa, trudniejsze scenariusze wielokartowe). Mocny do aplikacji webowych i testów komponentów.

### 7.2 AI-native i niskokodowe (record/replay + wizualne)

Druga rodzina to narzędzia, które obiecują niższy próg wejścia i mniejsze utrzymanie dzięki AI: samonaprawiające się selektory, nagrywanie zamiast pisania kodu, czasem tworzenie testów z opisu w języku naturalnym, zwykle w modelu SaaS/chmura.

- **Testim**, **Mabl**, **Functionize** — platformy low-code z AI-owymi lokatorami i auto-healingiem; nagrywanie plus edycja, integracja z CI, część oferuje też API i testy wydajności.
- **Reflect** — podejście no-code, nagrywanie w przeglądarce w chmurze.
- **Meticulous** — pozycjonuje się wokół idei „bez pisania asercji": nagrywa realne sesje i automatycznie generuje oraz utrzymuje testy regresji (głównie wizualnej), odtwarzając sesje i porównując wynik.
- **Applitools** — punkt odniesienia dla testów wizualnych (Visual AI): percepcyjne porównanie wyglądu zamiast kruchego pixel-diff, walidacja w wielu przeglądarkach i rozdzielczościach (nawiązanie do 4.6).

Zastrzeżenia, o których warto wspomnieć na rozmowie: te narzędzia kuszą szybkim startem, ale niosą ryzyko lock-inu, kosztu licencji, słabszej kontroli i wersjonowalności (testy żyją w platformie, nie w git) oraz pytań o dane wrażliwe wysyłane do chmury (6.8). Deklarowany „self-healing" trzeba też oceniać przez pryzmat granic zaufania z 4.7 — może maskować realne błędy.

### 7.3 API i kontraktowe

- **REST Assured** — codeful, Java, fluent Given/When/Then (rozdział 3).
- **Postman / Newman** — GUI z kolekcjami plus Newman jako runner CLI do CI; bardzo niski próg wejścia, skrypty w JavaScript, szerokie zastosowanie również do eksploracji API.
- **Karate** — testy API w stylu BDD (składnia zbliżona do Gherkina), bez pisania kodu Java do podstawowych przypadków; łączy w sobie testy API, kontraktowe i mockowanie usług.
- **Pact** — standard testów kontraktowych consumer-driven (rozdziały 1.5 i 3.2).

### 7.4 Osie porównania (najważniejsza część)

Zamiast zapamiętywać narzędzia, warto umieć rozłożyć je na osiach — bo to one przetrwają każdą zmianę mody:

- **Record-replay vs codeful vs agentowe** — to główna oś sposobu tworzenia testów. *Record-replay* (nagraj akcje → skrypt) ma najniższy próg i najszybszy start, ale daje testy kruche, trudne do wersjonowania i przeglądu, z ryzykiem lock-inu; dobre dla osób nietechnicznych. *Codeful* (test jako kod) wymaga więcej pracy, ale daje pełną kontrolę, wersjonowalność, przeglądalność i integrację z procesem developerskim — to poziom inżynierski. *Agentowe* (agent eksploruje i generuje, 4.8) obiecują niski koszt tworzenia i adaptacyjność, ale wnoszą niedeterminizm i problem wyroczni, więc dziś sprawdzają się raczej do odkrywania niż jako stabilny zestaw regresyjny.
- **Osie wtórne, które też warto nazwać** — in-process vs out-of-process (2.1); open-source vs komercyjny SaaS; code-first vs spec-first; self-hosted/lokalny vs chmura (kluczowe przy danych wrażliwych — 6.8); kontrola i determinizm vs wygoda i szybkość startu.

Synteza spinająca z rozdziałem 6: platforma, którą realnie buduje AI Engineer, najczęściej opiera się na **codeful** runnerach (kontrola, wersjonowalność, integracja z git i CI) i *dokłada* do nich warstwę AI tam, gdzie boli utrzymanie — czyli stara się uzyskać korzyści narzędzi AI-native (mniej utrzymania, self-healing) bez ich wad (lock-in, utrata kontroli). To dokładnie zasada „wrap, nie replace" z 6.12.

## 8. Pytania rozmowy + mapowanie na Twoje doświadczenie

Ten rozdział zamienia cały dokument w amunicję na rozmowę: prawdopodobne pytania z rdzeniami odpowiedzi, playbook na pytanie system design, jawny mostek z Twojego CV, pytania, które warto zadać samemu, oraz ściągę najmocniejszych tez. Rdzenie odpowiedzi są celowo krótkie — to punkty zaczepienia do rozwinięcia własnymi słowami, nie gotowe formułki do recytacji.

### 8.1 Jak ustawić tę rozmowę (pozycjonowanie)

Stoisz na styku QA i inżynierii AI. Twoją przewagą jest głębia w LLM-ach i agentach, rzadka wśród osób z QA; luką do nadrobienia są klasyczne fundamenty testowania — i to właśnie domyka ten dokument. Strategicznie: prowadź **dojrzałością inżynierską** (kompromisy, determinizm, koszt, świadomość granic), a nie entuzjazmem dla AI. Zdanie „AI nie naprawi wszystkiego — oto gdzie realnie pomaga, a gdzie nie" jest samo w sobie mocnym sygnałem. Wszystko kotwicz w prawdziwym bólu platformy: utrzymaniu i flakiness testów E2E.

### 8.2 Fundamenty testów — pytania i rdzenie odpowiedzi (rozdz. 1–3)

- **Piramida vs trofeum; po co E2E, skoro kruche?** — E2E daje pewność na krytycznych ścieżkach w realnych warunkach, ale jest najdroższe i najbardziej kruche, więc trzyma się go mało, a logikę spycha niżej (shift down). Trofeum przesuwa ciężar na testy integracyjne (najlepszy stosunek pewności do kosztu).
- **Mock vs stub — i kiedy nie mockować?** — stub steruje wejściem (test stanu), mock weryfikuje interakcje (test zachowania). Nadużycie mocków sprzęga test z implementacją; stąd nacisk na integrację na realnych zależnościach.
- **Dlaczego coverage to słaba metryka?** — mierzy wykonanie, nie weryfikację; łatwo ją grać. Lepsze: mutation score i defect escape rate.
- **Jak walczysz z flaky?** — to niemal zawsze zła synchronizacja; czekaj na warunek, nie na czas; zapewnij izolację i determinizm; flaky kwarantannuj, nie ukrywaj ślepym retry.
- **Strategia selektorów?** — od najbardziej odpornych: `data-testid` → role/ARIA → CSS → XPath; kruchość selektorów to główny koszt utrzymania E2E.
- **Po co testy kontraktowe?** — weryfikują zgodność konsumenta i dostawcy API bez stawiania obu naraz i bez kruchości E2E (CDC/Pact); łapią złamanie kontraktu tanio i wcześnie.
- **Dlaczego API jest tańsze i stabilniejsze od E2E?** — znikają oba źródła kruchości E2E: brak DOM/selektorów i brak asynchronicznego UI do synchronizacji.

### 8.3 AI w testach — pytania i rdzenie odpowiedzi (rozdz. 4–5)

- **Gdzie LLM realnie pomaga, a gdzie nie?** — pomaga tam, gdzie wejście jest ustrukturyzowane (kod, OpenAPI, DOM) i gdzie boli utrzymanie; ogranicza go problem wyroczni — model nie wie, co jest poprawne, więc człowiek wciąż odpowiada za poprawność.
- **Jak pogodzisz niedeterminizm LLM z determinizmem testu?** — generuj offline, zamroź artefakt, wersjonuj; LLM znika z toru wykonania. Niedeterminizm w generacji jest OK (obwarowany bramą jakości i przeglądem), w wyniku wykonania testu — nie, bo to flakiness.
- **Self-healing — jak działa i jak nie zamaskuje buga?** — dopasowanie elementu po wielu cechach przy zmianie DOM; musi być obserwowalny, przeglądalny i ograniczony progiem pewności, bo „uleczenie" realnej regresji daje false negative.
- **Jak ocenisz jakość wygenerowanego testu?** — mutation testing jako twarda wyrocznia (czy łapie wstrzyknięty błąd) + nacisk na false negative; nie liczba testów, lecz ich siła wykrywania.
- **Ryzyko generacji z kodu?** — over-fitting/tautologia: test utrwala obecne zachowanie wraz z błędami; sensowne świadomie jako characterization tests przy refaktorze legacy.
- **Agent eksploracyjny — jak utrwalasz wynik?** — agent służy do *odkrywania* scenariuszy, które potem *kodyfikujesz* jako deterministyczne testy regresyjne, a nie traktujesz jego nondeterministycznego przebiegu jako zestawu.

### 8.4 System design: „zaprojektuj platformę testową" — playbook

To prawdopodobnie główne pytanie pod to stanowisko. Odpowiadaj według schematu (kompresja rozdziału 6):

1. **Doprecyzuj wymagania** — jaki rodzaj testów (API/E2E), skala, język/stack, gdzie boli najbardziej (flaky? utrzymanie? czas CI?), ograniczenia danych.
2. **Zasada nadrzędna** — deterministyczny rdzeń (runner + CI), AI na obrzeżach; AI opakowuje istniejącą infrę, nie zastępuje jej.
3. **Komponenty** — orchestrator, grounding/RAG, generatory, brama jakości, runnery za wspólnym interfejsem, magazyn testów w git, model gateway, raportowanie, pętla feedback, eval harness.
4. **Podział offline/online** — naszkicuj dwa reżimy o różnych SLO (offline: drogi model, batch, wersjonowane; online: tani, szybki, cache, fallback, guardrails).
5. **Granica LLM vs kod** — gdzie LLM, gdzie deterministyka; każde użycie LLM ma walidację i fallback.
6. **Integracja z CI/CD** — generacja jako PR do przeglądu, selekcja testów (TIA), bramkowanie, shadow mode dla nowych zdolności.
7. **Ewaluacja i metryki** — golden sets, mutation, defect escape rate, koszt netto utrzymania, czas CI.
8. **Skalowanie, koszt, bezpieczeństwo** — zrównoleglenie, routing/cache, sekrety, PII, sandbox agenta.
9. **Wdrożenie** — crawl-walk-run: od bezpiecznej generacji API offline, przez eval, po ryzykowne online za flagami.

Samo trzymanie się tego schematu (zamiast skoku do „użyję GPT do pisania testów") pokazuje dojrzałość.

### 8.5 Produkt, metryki i sukces — pytania i rdzenie (rozdz. 5)

- **Jak zmierzysz sukces platformy?** — spadek defect escape rate, spadek *netto* kosztu utrzymania, niższy flaky rate, krótszy czas CI, wysoka adopcja (odsetek wygenerowanych testów akceptowanych bez zmian). Nie liczba testów ani samo coverage (metryki próżności, prawo Goodharta).
- **Jak udowodnisz, że AI działa, a nie psuje?** — eval harness na golden secie, mutation testing, shadow mode i A/B przy wdrażaniu, monitoring dryfu i pinowanie wersji modelu.
- **Kiedy NIE użyć LLM?** — gdy wystarczy reguła/parser/deterministyczny kod; gdy koszt/latencja nie przechodzą próby ROI; gdy wynik musi być w pełni powtarzalny w gorącej ścieżce.

### 8.6 Mostek: Twoje doświadczenie → platforma testowa

Przygotuj jednozdaniowe przejścia od tego, co już robiłeś, do potrzeb platformy — to one sprzedają Twoje CV:

- **LangGraph / orkiestracja** → orchestrator przepływów i agentowe E2E; checkpointing dla długich, wznawialnych przebiegów agenta.
- **Multi-agent / supervisor** → wzorzec planner/executor/krytyk, wyspecjalizowani generatorzy (API, E2E, triage) pod nadzorcą.
- **Tool use** → runner (Selenium/Playwright) jako narzędzie agenta; idempotentne, bezpieczne narzędzia.
- **Structured output** → generacja testów w ścisłym schemacie/DSL, walidowalna deterministyczną bramą jakości.
- **RAG** → grounding generacji w repozytorium testów, page objektach i konwencjach (mniej duplikacji, zgodność ze stylem).
- **Guardrails** → sandbox agenta, obrona przed prompt injection z treści strony, HITL jako brama.
- **Evals / metryki / dryf** → ewaluacja samej platformy (rozdz. 5), pinowanie modelu, regresja jakości.
- **Pamięć / session handling** → stan agenta i pętla feedback ucząca się na decyzjach z przeglądu.

### 8.7 Pytania behawioralne i o podejście

Spodziewaj się też pytań miękkich — odpowiadaj konkretnymi przykładami z własnych projektów (samodzielnie rozwijane systemy agentowe to Twój atut):

- **Opowiedz o projekcie z LLM, który doprowadziłeś** — wybierz taki, w którym pojawił się kompromis (koszt vs jakość, determinizm, guardrails) i pokaż, jak go rozstrzygnąłeś.
- **Jak debugujesz nieprzewidywalny system?** — systematycznie: izolacja zmiennej, obserwowalność, reprodukcja; podkreśl tracing i wersjonowanie (LLMOps).
- **Jak podchodzisz do niepewności/niejednoznacznych wymagań?** — dopytanie, najmniejszy wystarczający mechanizm, walidacja przez eval, iteracja.

### 8.8 Pytania, które zadasz Ty (sygnał dojrzałości)

Dobre pytania pokazują, że myślisz jak współwłaściciel platformy, a nie wykonawca:

- Jaki jest obecny stan platformy i co jest największym bólem — flaky rate, koszt utrzymania, czas CI?
- Jakie metryki dziś zbieracie i co uznacie za sukces w pierwszych 6 miesiącach?
- Jaki jest stosunek testów API do E2E i gdzie jest najwięcej kruchości?
- Build vs buy — czy są już używane narzędzia AI-native, jakie jest nastawienie do lock-inu?
- Jakie są ograniczenia co do danych (PII, chmura vs self-hosted) wpływające na wybór modeli?
- Jak wygląda proces przeglądu wygenerowanych testów i kto jest człowiekiem w pętli?

### 8.9 Czerwone flagi — czego unikać

- Sprzedawanie LLM jako srebrnej kuli; brak słowa o granicach i problemie wyroczni.
- Pomijanie determinizmu — propozycja „odpalania" LLM w wyniku testu.
- Auto-merge niezweryfikowanych wygenerowanych testów jako siatki bezpieczeństwa.
- Lekceważenie fundamentów QA („AI to załatwi") — utrata wiarygodności u testerów.
- Fiksacja na jednym narzędziu zamiast myślenia osiami i kompromisami.
- Mylenie metryk próżności (liczba testów, coverage) z realną wartością.

### 8.10 Ściąga: najmocniejsze tezy (soundbity)

Garść zdań destylujących cały dokument — do szybkiej powtórki tuż przed rozmową:

- „E2E to najdroższy i najbardziej kruchy poziom — dlatego AI atakuje przede wszystkim jego utrzymanie i flakiness."
- „Generuj offline, zamroź artefakt, wersjonuj: niedeterminizm w generacji jest OK, w wyniku wykonania testu — nie."
- „False negative jest groźniejszy niż false positive, bo daje fałszywą pewność."
- „Coverage to proxy, nie cel; mutation score i defect escape rate mówią więcej."
- „Self-healing musi być obserwowalny, przeglądalny i ograniczony — inaczej maskuje realne błędy."
- „Deterministyczny rdzeń, AI na obrzeżach; minimalizuj powierzchnię LLM."
- „API to najłatwiejszy i najmniej ryzykowny punkt startu dla AI — ustrukturyzowane, deterministyczne, opisane OpenAPI."
- „Czekaj na warunek, nie na czas — to istota walki z flakiness."
- „Agent służy do odkrywania scenariuszy, które potem kodyfikujesz jako deterministyczne testy."
- „Wrap, nie replace — opakowuj istniejące runnery, nie zastępuj ich."
- „Mierz netto redukcję kosztu utrzymania, nie liczbę wygenerowanych testów."
- „Problem wyroczni wyznacza granicę: AI proponuje, człowiek odpowiada za poprawność."

### 8.11 Pełny przykład: „jak przetestujesz X?" — rozpisany przypadek

To pytanie (zapowiedziane w 1.2) bada nie tyle wiedzę o konkretnej funkcji, ile **sposób myślenia**: czy potrafisz uporządkować przestrzeń testów, czy pamiętasz o drugim dnie (atrybutach jakości z 1.2) i czy dobierzesz właściwy poziom piramidy. Dlatego nie wyliczaj przypadków losowo — przejdź na głos przez stały szkielet, który działa dla dowolnego X (pole, endpoint, ekran, funkcja):

1. **Doprecyzuj X i wyrocznię** — co dokładnie robi, jakie są reguły i co jest źródłem prawdy (wymaganie, nie domysł). To ten sam problem wyroczni co w 4.1: bez reguł nie wiesz, co asercjonować.
2. **Przypadki funkcjonalne — technikami z 1.3**, nie z głowy: klasy równoważności, wartości brzegowe, tablica decyzyjna dla kombinacji warunków, przejścia stanów tam, gdzie jest stan.
3. **Przypadki negatywne i błędy** — złe wejście, brak uprawnień, stany niedozwolone (świadomie, nie tylko happy path).
4. **Drugie dno — atrybuty niefunkcjonalne (1.2)**: wydajność, bezpieczeństwo (zwłaszcza autoryzacja), współbieżność (2.7), idempotentność (3.3), dostępność.
5. **Poziom piramidy (1.1)** — zdecyduj, co schodzi na unit/API, a co naprawdę musi być E2E (shift down z 3.4).
6. **Gdzie pomaga AI** — generacja przypadków brzegowych i walidacja schematu z OpenAPI, ale z przeglądem (4.2–4.3).

Zastosujmy szkielet do konkretu: **„jak przetestujesz endpoint przelewu kwoty z konta A na konto B" (`POST /transfers`)**.

**1. Doprecyzowanie.** Zanim cokolwiek napiszę, pytam o reguły: czy kwota musi być dodatnia i z jaką dokładnością (grosze), czy waluty obu kont muszą się zgadzać, co przy niewystarczających środkach (odrzucenie czy debet), czy jest dzienny limit, czy przelew jest synchroniczny czy asynchroniczny (status `pending` → `completed`) i czy istnieje klucz idempotencji. Każda odpowiedź to przyszła asercja — i jednocześnie zabezpieczenie przed zgadywaniem wyroczni (4.1).

**2. Funkcjonalne — technikami, nie z głowy.**
- *Klasy równoważności i wartości brzegowe (1.3):* kwota = 0, 0.01, wartość typowa, dokładnie całe saldo, saldo + 0.01 (tuż za granicą), wartość ujemna, więcej miejsc po przecinku niż grosze, maksymalny limit i tuż powyżej.
- *Tablica decyzyjna* dla kombinacji warunków: {konto źródłowe istnieje?} × {wystarczające środki?} × {waluty zgodne?} × {w limicie?} — każda reguła ma z góry zdefiniowany wynik (sukces albo konkretny kod błędu).
- *Przejścia stanów* dla wariantu asynchronicznego: `pending → completed`, `pending → failed`; sprawdź też, że przejście niedozwolone (np. `completed → pending`) jest blokowane.

**3. Negatywne.** Nieistniejące konto B (404), przelew na to samo konto (A = B), niewystarczające środki (422/409 z **saldem bez zmian** — to kluczowa asercja niezmiennika), zły format kwoty (400).

**4. Drugie dno — niefunkcjonalne (to odróżnia dobrą odpowiedź od płytkiej).**
- *Bezpieczeństwo/autoryzacja (1.2, 3.3):* czy użytkownik może zlecić przelew z **cudzego** konta? Musi dostać 403 — ten negatywny przypadek autoryzacyjny jest tu ważniejszy niż happy path.
- *Współbieżność (2.7):* dwa równoległe przelewy na całe saldo nie mogą oba przejść (zgubiona aktualizacja / podwójne wydanie) — test z barierą/latchem i asercją niezmiennika „suma sald obu kont stała".
- *Idempotentność (3.3):* ponowiony `POST` z tym samym kluczem idempotencji tworzy *jeden* przelew, nie dwa — chroni przed podwójnym obciążeniem przy retry.
- *Wydajność (1.2):* p95/p99 latencji pod obciążeniem, nie średnia.

**5. Poziom piramidy (1.1, 3.4).** Walidację kwoty i samą regułę salda testuję na **unit** (milisekundy, pełne pokrycie przypadków brzegowych). Logikę przelewu, kody odpowiedzi, autoryzację, idempotentność i współbieżność — na **API/integracji** (tu trafia większość ciężaru). E2E rezerwuję dla **jednej** ścieżki: użytkownik zleca przelew przez UI i widzi potwierdzenie — bo tylko ona weryfikuje integrację z frontendem. To wprost shift down z 3.4.

**6. Gdzie AI.** Przypadki brzegowe i walidację schematu odpowiedzi generuję z OpenAPI (4.2–4.3), ale wyrocznię „poprawnego salda" potwierdza człowiek lub wymaganie — to granica problemu wyroczni z 4.1.

Pointa do wypowiedzenia na głos: *„Zacznę od reguł, potem przejdę przez przypadki funkcjonalne technikami projektowania — ale najważniejsze jest drugie dno: autoryzacja, współbieżność i idempotentność — i zepchnięcie maksimum tych testów poniżej E2E."* To jedno zdanie pokazuje dokładnie tę dojrzałość, o którą podpytuje pytanie z 1.2.

## 9. BDD i opisywanie testów językiem naturalnym (Cucumber/Gherkin) — pogłębienie

Rozdział odpowiada na konkretne pytanie o frameworki, w których przypadki testowe opisuje się niemal językiem naturalnym, i rozwija wątek „język naturalny ↔ test" z 4.4 oraz oś record-replay/codeful/agentowe z 7.4. Z góry jedno doprecyzowanie, które jest tu kluczowe: te narzędzia nie używają *wolnego* języka naturalnego, lecz **ustrukturyzowanego, ograniczonego DSL** (Gherkin), który tylko *wygląda* jak zwykły tekst. Ta różnica decyduje o całej analizie pod kątem AI.

### 9.1 Cucumber + Gherkin (Java) — jak to działa

Najpopularniejszym przedstawicielem tej rodziny w świecie Javy jest **Cucumber** (implementacja `Cucumber-JVM`), oparty na języku **Gherkin**. Cała idea wywodzi się z BDD (Behaviour-Driven Development), a sednem jest rozdzielenie dwóch warstw:

- **Warstwa czytelna — plik `.feature`** napisany w Gherkinie. Zawiera `Feature` (opis funkcjonalności), jeden lub więcej `Scenario`, a każdy scenariusz to kroki `Given` (stan początkowy), `When` (akcja), `Then` (oczekiwany wynik), łączone przez `And`/`But`. Dochodzą do tego konstrukcje: `Background` (wspólny wstęp dla scenariuszy), `Scenario Outline` z sekcją `Examples` (ten sam scenariusz odpalany dla tabeli danych — odpowiednik testów parametryzowanych), `Data Tables` (tabele danych w kroku) oraz `Tagi` (`@smoke`, do filtrowania uruchomień). Przykładowy krok wygląda po prostu jak zdanie: „Given użytkownik jest zalogowany jako administrator".
- **Warstwa wykonywalna — step definitions (glue code)**. Każdy krok z `.feature` jest dopasowywany do metody w kodzie (w Javie adnotowanej `@Given`, `@When`, `@Then`), a dopasowanie odbywa się przez wyrażenie regularne lub Cucumber Expressions. To właśnie w tych metodach żyje prawdziwa automatyzacja — wywołania Selenium, REST Assured itd. Krok „użytkownik jest zalogowany" zamienia się tu na konkretne kliknięcia albo żądania HTTP.

Całość uruchamia runner (przez JUnit/TestNG), a `Hooks` (`@Before`/`@After`) obsługują setup i teardown. Kluczowa obserwacja, do której wrócimy: **plik `.feature` sam w sobie nie jest wykonywalny** — bez warstwy glue jest tylko czytelną specyfikacją. Mamy więc jawnie rozdzielone „co" (czytelny, biznesowy opis intencji) od „jak" (deterministyczny kod).

Warto znać dwa nazwiska z sąsiedztwa: **JBehave** to pierwszy frameworek BDD dla Javy (autorstwa Dana Northa, który ukuł termin BDD), a **Serenity BDD** to popularna warstwa nadbudowana (zwykle nad Cucumber/JBehave) dająca bogate raportowanie i wsparcie wzorca Screenplay z 2.4. Wartość tej rodziny to żywa dokumentacja i współpraca z biznesem (kryteria akceptacji stają się testami); koszt to utrzymanie warstwy glue i ryzyko „teatru Gherkina" — pisania scenariuszy, których żaden nietechniczny odbiorca nie czyta.

### 9.2 Czy w Pythonie też? — behave i pytest-bdd

Tak, ekosystem Pythona ma bezpośrednie odpowiedniki, oparte na tym samym Gherkinie:

- **behave** — najbliższy duchowi Cucumbera: pliki `.feature` w Gherkinie, a step definitions to funkcje Pythona z dekoratorami `@given`, `@when`, `@then`. Model dwuwarstwowy jest identyczny.
- **pytest-bdd** — Gherkin osadzony w ekosystemie `pytest`: kroki to funkcje pytest, a całość korzysta z fixtur i bogatego świata wtyczek pytest (raporty, równoległość, parametryzacja). Dla zespołu już używającego pytest często wygodniejszy, bo nie wprowadza osobnego runnera.
- Pomniejsze/historyczne: **lettuce** (w dużej mierze nieutrzymywany) oraz **radish** (rozszerza Gherkin o m.in. preconditions i pętle).

Praktyczny wniosek: ten sam model „czytelny `.feature` + kod kroków" jest przenośny między Javą a Pythonem, więc platforma nie musi być przywiązana do jednego języka.

### 9.3 Konkretny przykład: ten sam scenariusz w Javie i Pythonie

Najlepiej widać to na małym przykładzie logowania. Najpierw warstwa czytelna — jeden plik `.feature` (Gherkin), wspólny niezależnie od języka implementacji. Słowa kluczowe są tu po angielsku, ale treść kroków po polsku; sam Gherkin pozwala też zlokalizować słowa kluczowe (dyrektywa `# language: pl` daje `Funkcja`, `Scenariusz`, `Zakładając, że`, `Gdy`, `Wtedy`).

```gherkin
# language: en
Feature: Logowanie do panelu administracyjnego

  Scenario: Poprawne logowanie administratora
    Given użytkownik jest na stronie logowania
    When loguje się jako "admin" z hasłem "tajne123"
    Then widzi panel administracyjny
```

Ten sam plik napędza step definitions w **Javie (Cucumber-JVM)**. Zwróć uwagę, jak krok z cudzysłowami mapuje się na metodę z parametrami przez Cucumber Expressions (`{string}`), a w środku siedzi zwykła automatyzacja Selenium (z `data-testid` z 2.2 i jawnym waitem z 2.3):

```java
public class LogowanieSteps {

    private final WebDriver driver = new ChromeDriver();

    @Given("użytkownik jest na stronie logowania")
    public void otworzStroneLogowania() {
        driver.get("https://app.example.com/login");
    }

    @When("loguje się jako {string} z hasłem {string}")
    public void zaloguj(String login, String haslo) {
        driver.findElement(By.cssSelector("[data-testid=login]")).sendKeys(login);
        driver.findElement(By.cssSelector("[data-testid=password]")).sendKeys(haslo);
        driver.findElement(By.cssSelector("[data-testid=submit]")).click();
    }

    @Then("widzi panel administracyjny")
    public void sprawdzPanel() {
        WebElement panel = new WebDriverWait(driver, Duration.ofSeconds(5))
            .until(ExpectedConditions.visibilityOfElementLocated(
                By.cssSelector("[data-testid=admin-panel]")));
        assertTrue(panel.isDisplayed());
    }
}
```

Dokładnie ten sam `.feature` można obsłużyć w **Pythonie (behave)** — struktura jest bliźniacza, zmienia się tylko składnia (dekoratory `@given/@when/@then`, przekazywanie stanu przez `context`):

```python
from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@given('użytkownik jest na stronie logowania')
def otworz_strone(context):
    context.driver = webdriver.Chrome()
    context.driver.get("https://app.example.com/login")

@when('loguje się jako "{login}" z hasłem "{haslo}"')
def zaloguj(context, login, haslo):
    d = context.driver
    d.find_element(By.CSS_SELECTOR, "[data-testid=login]").send_keys(login)
    d.find_element(By.CSS_SELECTOR, "[data-testid=password]").send_keys(haslo)
    d.find_element(By.CSS_SELECTOR, "[data-testid=submit]").click()

@then('widzi panel administracyjny')
def sprawdz_panel(context):
    el = WebDriverWait(context.driver, 5).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-testid=admin-panel]")))
    assert el.is_displayed()
```

Morał z przykładu jest wprost wejściem do następnej podsekcji: **warstwa czytelna (`.feature`) jest jedna i niezależna od języka**, a warstwa glue (Java lub Python) to wymienialna, deterministyczna implementacja. To właśnie ten górny plik generowałaby platforma AI — krótki, czytelny, zatwierdzalny przez człowieka — podczas gdy katalog kroków pozostaje stabilnym, reużywalnym kodem.

### 9.4 Wariant: ten sam scenariusz w pytest-bdd (Python)

`pytest-bdd` używa tego samego pliku `login.feature`, ale glue żyje w świecie `pytest`: stan przechodzi przez **fixtury** (nie przez `context` jak w behave), parametry wyciąga się przez `parsers.parse`, a scenariusze wiąże funkcją `scenarios(...)`. Dzięki temu dostajesz cały ekosystem pytest — fixtury, wtyczki, parametryzację, równoległość przez `pytest-xdist`:

```python
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# powiąż wszystkie scenariusze z pliku .feature
scenarios("login.feature")

@pytest.fixture
def driver():
    d = webdriver.Chrome()
    yield d
    d.quit()

@given("użytkownik jest na stronie logowania")
def otworz_strone(driver):
    driver.get("https://app.example.com/login")

@when(parsers.parse('loguje się jako "{login}" z hasłem "{haslo}"'))
def zaloguj(driver, login, haslo):
    driver.find_element(By.CSS_SELECTOR, "[data-testid=login]").send_keys(login)
    driver.find_element(By.CSS_SELECTOR, "[data-testid=password]").send_keys(haslo)
    driver.find_element(By.CSS_SELECTOR, "[data-testid=submit]").click()

@then("widzi panel administracyjny")
def sprawdz_panel(driver):
    el = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-testid=admin-panel]")))
    assert el.is_displayed()
```

Różnica wobec behave jest czysto „pythonowa": behave ma własny runner i współdzielony `context`, a pytest-bdd dokłada Gherkina do pytest, więc lepiej integruje się z projektem, który już na pytest stoi. Model dwuwarstwowy (`.feature` + kroki) pozostaje identyczny.

### 9.5 Wariant API w stylu BDD: Karate

Karate to osobny, ważny przypadek, bo **łamie model dwuwarstwowy**. W Cucumber/behave/pytest-bdd plik `.feature` jest nieczytelny dla maszyny bez warstwy glue. Karate natomiast dostarcza wbudowany DSL do HTTP i asercji wprost w składni Gherkina — wywołania i sprawdzenia piszesz bezpośrednio w pliku `.feature`, bez osobnych step definitions. Dla testów API obie warstwy zlewają się w jedną: plik jest zarazem czytelny i wykonywalny.

```gherkin
Feature: API użytkowników

  Background:
    * url 'https://api.example.com'

  Scenario: Pobranie istniejącego użytkownika zwraca 200 i poprawne dane
    Given path 'users', 1
    When method GET
    Then status 200
    And match response ==
      """
      {
        "id": 1,
        "login": "#string",
        "rola": "#regex (admin|user)"
      }
      """

  Scenario: Utworzenie użytkownika zwraca 201 i nagłówek Location
    Given path 'users'
    And request { login: 'nowy', haslo: 'tajne123', rola: 'user' }
    When method POST
    Then status 201
    And match responseHeaders['Location'][0] contains '/users/'
    And match response.login == 'nowy'
```

Warto zwrócić uwagę na kilka rzeczy. `url`, `path`, `request`, `method`, `status` to wbudowane słowa kluczowe Karate — to one zastępują glue. Konstrukcja `match response == {...}` z **rozmytymi dopasowaniami** (`#string`, `#regex`, `#number`, `#uuid`, `#notnull`) to inline walidacja zbliżona do walidacji schematu z 3.2 — sprawdzasz *kształt i typy*, nie tylko konkretne wartości. `Background` trzyma wspólny setup (bazowy adres). Efekt: jeden samowystarczalny, czytelny i wykonywalny artefakt na scenariusz API.

### 9.6 Czy platforma AI mogłaby to wykorzystać? (sedno)

Tak — i to jest jeden z czystszych sposobów zastosowania generowania przez LLM przy zachowaniu determinizmu. Powody, dla których BDD/Gherkin pasuje wyjątkowo dobrze:

- **Gherkin to ustrukturyzowany cel dla structured output (4.3).** Ograniczone słownictwo kroków i sztywna gramatyka czynią generację przewidywalną i — co ważniejsze — *walidowalną maszynowo*: można statycznie sprawdzić, czy każdy wygenerowany krok wiąże się z istniejącą definicją. To gotowa **brama jakości** z 5.5/6.2.
- **Rozdzielenie warstw rozwiązuje konflikt determinizmu (5.5).** LLM generuje plik `.feature` (czytelna intencja, wyrocznia w języku biznesu), ale *wykonanie* opiera się na deterministycznym kodzie step definitions — model znika z toru wykonania. To dokładna realizacja zasady „generuj offline, zamroź artefakt, wersjonuj": feature trafia do gita i odtąd jest powtarzalny.
- **Naturalny human-in-the-loop (4.1).** Scenariusz w Gherkinie może przeczytać i zatwierdzić product owner czy QA, co wprost adresuje problem wyroczni — człowiek potwierdza, że opisana intencja jest poprawna, zanim powstanie kod.
- **Reużycie kroków przez grounding/RAG (4.3).** BDD zachęca do budowania biblioteki wielokrotnych kroków; platforma może wykryć, które step definitions już istnieją, i generować tylko brakujące glue oraz scenariusze złożone z istniejącego słownika.
- **Kierunek odwrotny (4.4).** Z istniejących testów LLM może generować scenariusze Gherkina jako żywą dokumentację i ścieżkę traceability wymaganie–test.

Napięcia, o których trzeba pamiętać (i które warto wymienić na rozmowie):

- **Eksplozja i duplikacja kroków.** Bez groundingu LLM tworzy kroki o nieco innym brzmieniu do tej samej akcji, rozsadzając katalog i mnożąc glue. Grounding w istniejącym słowniku kroków jest tu obowiązkowy, nie opcjonalny.
- **Teatr Gherkina i paradoks utrzymania (4.13).** Auto-generowanie warstwy czytelnej tam, gdzie nikt z biznesu jej nie czyta, to narzut bez korzyści — wtedy lżejsze są zwykłe testy codeful. BDD opłaca się, gdy warstwa naturalna ma realnych odbiorców.
- **Glue to wciąż kod.** AI przesuwa koszt utrzymania (mniej ręcznego pisania scenariuszy), ale go nie likwiduje — definicje kroków trzeba utrzymywać tak samo jak każdy inny kod testowy.

Osobnym przypadkiem jest Karate (9.5) — model **jednowarstwowy**, w którym LLM generuje jeden samowystarczalny plik `.feature` zamiast pary feature plus glue. Determinizm wykonania zostaje zachowany, bo to wciąż zamrożony, wersjonowany artefakt, a rozmyte dopasowania (`#string`, `#regex`) pełnią rolę wbudowanej bramy walidacji. Zaleta dla platformy: mniej kodu glue do utrzymania i jeden artefakt do przeglądu. Cena: to DSL specyficzny dla Karate, który model musi znać, i ograniczony do API — mniej ogólny niż zwykły kod kroków.

Pozycjonując to na osi z 7.4: **BDD/Gherkin to „ustrukturyzowany język naturalny nad warstwą codeful"** — daje przeglądalny artefakt pośredni, który spina intencję biznesu z deterministycznym kodem. Dla platformy AI jest atrakcyjny właśnie dlatego, że łączy zaletę narzędzi NL/low-code (czytelność, akceptacja przez nietechnicznych) z zaletami codeful (wersjonowanie w git, pełna kontrola, determinizm wykonania) — czyli wpisuje się w zasadę „wrap, nie replace" z 6.12. Krótko: to jeden z najbezpieczniejszych punktów, w których LLM może *generować*, bo wynik jest czytelny dla człowieka, zatwierdzalny i wykonywany w pełni deterministycznie.



### Zapytać później
- jak byś przetestował X? → rozpisane jako pełny przykład w 8.11
- flakiness - jakie mogą być konkretne przykłady: zależności czasowe i asynchroniczność, kolejność wykonywania testów, współdzielony stan, sieć, dane
