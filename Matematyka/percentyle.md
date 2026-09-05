# Percentyle (p95, p99) - co nam dają?

## Krótkie podsumowanie
**Percentyl** to miara statystyczna, która dzieli zbiór posortowanych danych na 100 równych części. Wynik wyrażony w percentylach (np. p95, p99) mówi nam, poniżej jakiej wartości znajduje się dany procent obserwacji. W informatyce (np. przy monitorowaniu API) używamy ich zamiast średniej, aby lepiej zrozumieć **rzeczywiste doświadczenie użytkowników** i ignorować skrajne anomalie.

## Dlaczego nie średnia?
Średnia arytmetyczna jest bardzo wrażliwa na wartości skrajne (tzw. *outliery*). 
Wyobraź sobie, że 9 zapytań do serwera wykonuje się w 10 ms, a jedno (z powodu chwilowego błędu sieci) w 1000 ms.
- **Średnia** wyniesie: `(9 * 10 + 1000) / 10 = 109 ms`. 

Patrząc tylko na średnią, pomyślisz, że system działa wolno (109 ms), chociaż w rzeczywistości aż 90% użytkowników otrzymało błyskawiczną odpowiedź (10 ms). Średnia zakłamuje tu rzeczywistość.

## Co oznaczają progi p50, p95, p99?
Aby precyzyjnie mierzyć to, co widzą użytkownicy, sortujemy wszystkie czasy odpowiedzi od najszybszego do najwolniejszego i wybieramy wartość dla konkretnego progu:

- **p50 (Mediana)** – Dokładnie środkowa wartość. 50% zapytań jest szybszych, 50% wolniejszych. Pokazuje "typowe" doświadczenie użytkownika.
- **p90** – 90% zapytań wykonuje się w tym czasie lub szybciej. Zaledwie 10% jest wolniejszych.
- **p95** – 95% zapytań wykonuje się w tym czasie lub szybciej. Ignorujemy 5% najwolniejszych pomiarów.
- **p99** – 99% zapytań wykonuje się w tym czasie lub szybciej. Pokazuje zachowanie "ogona" – najgorsze doświadczenia użytkowników, odrzucając tylko 1% najbardziej skrajnych opóźnień (często wynikających z problemów z infrastrukturą).

## Przykład z życia (Monitorowanie wydajności)
Załóżmy, że z platformy monitorującej system (np. Grafana, Datadog) odczytujemy następujące wartości:
- **p50 = 20 ms** (Typowy użytkownik czeka 20 ms)
- **p95 = 50 ms** (95% użytkowników ma odpowiedź w maksymalnie 50 ms)
- **p99 = 500 ms** (99% użytkowników czeka nie więcej niż 500 ms)

**Co nam to mówi?**
Dla absolutnej większości system działa świetnie (p50 i p95 są bardzo niskie). Jednakże, z jakiegoś powodu najgorszy 1% zapytań trwa aż 500 ms (znaczny skok w stosunku do p95). Taka rozbieżność może wskazywać m.in. na:
- Operacje *Garbage Collection* w środowisku uruchomieniowym (np. Java, C#).
- Tzw. "zimne starty" (*cold starts*) w rozwiązaniach Serverless (np. AWS Lambda).
- Wyczerpywanie się puli połączeń do bazy danych lub locki na bazie.

Świadomość tych metryk pozwala skupić się na optymalizacji odpowiednich, problematycznych obszarów, o których nie dowiedzielibyśmy się patrząc na zwykłą średnią.

## Gdzie to się stosuje?
1. **SLA (Service Level Agreement)** - Umowy biznesowe na ogół precyzują jakość usług za pomocą percentyli, a nie średniej (np. "Aplikacja musi obsługiwać p99 żądań w czasie krótszym niż 200 ms").
2. **Observability i Monitoring** - To absolutny standard przy analizowaniu logów, śledzeniu (tracing) i telemetrii.
3. **Medycyna / Statystyka** - Np. siatki centylowe wagi i wzrostu dzieci (percentyl 90 oznacza, że dane dziecko jest wyższe lub cięższe niż 90% dzieci w jego wieku).
