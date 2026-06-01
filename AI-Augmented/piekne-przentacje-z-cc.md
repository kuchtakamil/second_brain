Masz wystąpienie za trzy dni albo potrzebujesz draftu konceptu, żeby pokazać klientowi pomysł. Zamiast walczyć w PowerPoincie, mówisz Claude'owi co chcesz powiedzieć, a on generuje gotową prezentację, którą oglądasz w przeglądarce. Jeśli coś nie pasuje, mówisz po polsku co poprawić. To wszystko.

🔗 Repo: github.com/zarazhangrui/frontend-slides

Instalacja

W aktywnej sesji Claude Code wystarczy napisać:



Zainstaluj mi skill z https://github.com/zarazhangrui/frontend-slides

Claude robi resztę. Po chwili wpisujesz /frontend-slides i jesteś gotowy.

Najpierw research, dopiero prezentacja

Najważniejsza rzecz w tym wpisie. Większość ludzi otwiera narzędzie z pustą głową i liczy, że "AI coś wymyśli". Wymyśli, ale wyjdzie ogólnik bez liczb, źródeł i tez do zapamiętania.

Lepsza kolejność:

Najpierw porządny research tematu w osobnej sesji. Możesz użyć Gemini CLI z Google Search, Codexa jako drugiego zdania albo zwykłej rozmowy z Claude'em. Wychodzisz z konkretami: liczby, źródła, przykłady, tezy.


Szkic narracji slajd po slajdzie w prostym markdownie. Co chcesz powiedzieć i czego ma nauczyć się widz.



Dopiero teraz /frontend-slides. Skill nie zgaduje, tylko ubiera Twoje treści w wybrany styl.



Iterujesz po polsku: "Trzeci slajd jest za zagęszczony, rozbij na dwa". "Zmień akcent na złoty". Każda poprawka to jedno zdanie.

Skill jest świetnym wykonawcą, ale strategiem musisz być Ty.

Dlaczego to jest dramatycznie szybsze





Generujesz w minuty, nie w godziny. 10 slajdów w stylu, który podoba Ci się od razu, dostajesz w czasie, w którym w PPT walczyłbyś z trzecim layoutem.



Edycja w języku naturalnym. "Przesuń nagłówek wyżej, dorzuć cytat na drugim slajdzie" zamiast klikania kursorem co do piksela.



Wynik wygląda jak coś, co zrobił człowiek, a nie generator slajdów z fioletowymi gradientami.



Konwersja w obie strony. Stary deck .pptx skill zaimportuje, wyciągnie teksty i obrazy. W drugą stronę wynik eksportujesz do PDF (Slack, Notion) albo na darmowy hosting jako link dla klienta.



Wersjonowanie w gicie. Prezentacja to plik tekstowy, więc wchodzi do repo. Wracasz do dowolnej wersji, dzielisz się z zespołem.

W praktyce: prezentacja z pół dnia w Keynote schodzi do 30-45 minut, z czego większość czasu to research.

Jak to wygląda od strony użycia

Nowa prezentacja od zera:

/frontend-slides

> "Zrób mi pitch deck dla startupu o automatyzacji email marketingu"


Skill pyta o treść, o uczucie jakie ma wzbudzać, pokazuje kilka podglądów stylów do wyboru, generuje wersję, otwiera w przeglądarce.

Konwersja istniejącego PowerPointa:

> "Przekonwertuj prezentacja.pptx na wersję webową"


Edycja po wygenerowaniu:

> "Drugi slajd jest za pusty, dorzuć trzy bullety z liczbami"
> "Zmień tytuł całości na 'Dlaczego email wymaga automatyzacji'"
> "Wyeksportuj do PDF"

Style

W środku jest kilkanaście gotowych styli, więc nic nie projektujesz sam. Kilka przykładów: ciemny techniczny w klimacie terminala, jasny editorial z papierowymi zakładkami, neonowy cyber, minimalistyczny w stylu Bauhaus, elegancki literacki. Skill pokaże podglądy, klikasz ten który pasuje.

Z naszego doświadczenia

Na bazie tego skilla robiliśmy wiele prezentacji w ramach warsztatów Dojo i działa świetnie. Wynik wychodzi w stanie, w którym pokażesz go uczestnikom bez wstydu i dodatkowego dłubania.

Krok dalej: własny styl marki

Kiedy złapiesz flow, sprecyzuj swój styl wizualny i dorzuć go jako preset. Mówisz Claude'owi: "Wygeneruj mi nowy preset o nazwie X. Kolory takie, fonty takie. Wzoruj się na istniejącym presecie i podmień charakterystykę". Następnym razem Twój styl marki wskakuje do listy do wyboru.

W AI Ninjas idziemy w tym kierunku, mamy własny fork z presetami marki. Skill robi 80%, customizacja zamyka 20% pod konkretną tożsamość.

Źródła

Repo skilla: github.com/zarazhangrui/frontend-slides