# Chcę zrobić aplikację która na wstępie dostanie link do wybranego kanału na yout

**Data:** 7 lis 2025, 13:00:35 CET

---

**User:**

Chcę zrobić aplikację która na wstępie dostanie link do wybranego kanału na youtube związanego z nauką języka angielskiego. Kanał ten w swoich shortach prezentuje scenki w których zazwyczaj jedna osoba mówi słabo po angielsku, a druga osoba mówi jej jak można to powiedzieć w poprawny sposób.
Następnie pobierze transkrypcję ze wszystkich shortów na tym kanale youtube.
Następnie każdą transkrypcję osobno wyślę do LLM tak aby LLM napisał z każdego rodzaju krótką lekcję.

Napisz plan techniczny dla takiej aplikacji. Teraz skup się na części pobierania transkrypcji ze wszystkich shortów na wybranym kanale.
Przy okazji tworzenia tej aplikacji, chcę poznać popularne frameworki i techniki pracy z pythonem. Uwzględnij to w swoich planach, lecz nie dodawaj żadnej zbędnej technologii tylko w celu nauczenia się jej. Priorytetem tu jest produkt, nauka to dodatek.

---

**Gemini:**

Oto ułożony plan działania. Jeśli chcesz go zmienić, poinformuj mnie o tym.

(1) Zbadaj proces konfiguracji projektu w Google Cloud Console w celu uzyskania klucza API dla YouTube Data API v3. Przeanalizuj dokumentację dotyczącą włączania API i zarządzania poświadczeniami.\
(2) Wyszukaj metody użycia YouTube Data API v3 do pobrania wszystkich identyfikatorów filmów (Video IDs) z określonego kanału. Skoncentruj się na znalezieniu identyfikatora playlisty "uploads" kanału i iterowaniu przez jej zawartość.\
(3) Przeanalizuj techniki filtrowania wyników z API (krok 2), aby zidentyfikować wyłącznie filmy typu "Shorts". Zbadaj, czy można filtrować po czasie trwania filmu (poniżej 60 sekund) lub innych metadanych dostępnych w API.\
(4) Znajdź i oceń popularne biblioteki Pythona przeznaczone do pobierania transkrypcji z YouTube, takie jak `youtube-transcript-api`. Sprawdź przykłady implementacji pobierania transkrypcji przy użyciu identyfikatora wideo.\
(5) Zbadaj mechanizmy obsługi błędów (error handling) na wypadek, gdyby dany film "Short" nie posiadał dostępnej transkrypcji (ani automatycznej, ani dodanej ręcznie). Opracuj logikę, która pozwoli aplikacji pominąć taki film i kontynuować proces.\
(6) Przeanalizuj najlepsze praktyki dotyczące strukturyzowania projektów w Pythonie oraz nowoczesne narzędzia do zarządzania zależnościami, takie jak `Poetry` lub standardowe `venv` z plikiem `requirements.txt`, aby zarządzać bibliotekami `google-api-python-client` i `youtube-transcript-api`.\
(7) Zbadaj, jak prawidłowo obsługiwać paginację (stronicowanie) wyników z YouTube Data API (przy użyciu `nextPageToken`), aby zapewnić pobranie *wszystkich* filmów z kanału, nawet jeśli ma on tysiące publikacji.\
(8) Zaprojektuj prosty format przechowywania pobranych transkrypcji (np. jako oddzielne pliki tekstowe lub pliki JSON, mapujące Video ID do treści transkrypcji), aby przygotować je do kolejnego etapu, czyli przetwarzania przez LLM.