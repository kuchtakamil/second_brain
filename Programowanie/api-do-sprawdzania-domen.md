# API do sprawdzania domen

**Data:** 2025-11-16

---

**User:**

czy istnieje API do które można wykorrzystać do sprawdzenia czy dana domena jest wolna czy zajęta?

---

**Assistant:**

Tak — istnieje wiele API, które pozwalają na sprawdzenie, czy dana domena jest wolna czy już zarejestrowana. Oto kilka przykładów:  

- WhoisXML API — Domain Availability API: REST API, obsługuje wiele TLD, daje wynik JSON/XML. citeturn0search2turn0search6turn0search11  
- WhoisFreaks — API do sprawdzania dostępności domen, wspiera pojedyncze i masowe zapytania. citeturn0search1turn0search3  
- Api Ninjas — Domain API: proste sprawdzenie dostępności + dodatkowe informacje o rejestracji. citeturn0search7  
- VebAPI — Domain Availability Checker (dla pojedynczego TLD). citeturn0search5  
- Netim — REST API rejestratora Netim umożliwia sprawdzanie dostępności domen. citeturn0search10  
- Apify — Domain Availability Checker jako aktor (actor) w ich platformie, można uruchamiać przez API Apify. citeturn0search8  

Jeśli podasz, jakie TLD Cię interesują (np. `.pl`, `.com`, `.io`) i czy ważne są koszty / limit zapytań — mogę zaproponować najbardziej odpowiednie API.

---

**User:**

interesują mnie domeny .pl i jeśli jest jakieś bardzo tanie, a raczej darmowe z dużym limitem, API to mnie to interesuje

---

**Assistant:**

Tak, są pewne API, które mogą pomóc sprawdzić dostępność domen .pl — ale **nie ma wielu darmowych z bardzo dużym limitem**. Poniżej przegląd plus propozycje + ograniczenia, które musisz wziąć pod uwagę:

---

## 🔍 Kilka API, które można rozważyć

1. **Domeny.tv (API SOAP)**  
   - Mają API do .pl domen. citeturn0search2turn0search13turn1search2  
   - Dokumentacja pokazuje metodę `checkDomain`, która zwraca, czy domena jest dostępna. citeturn1search2  
   - Minusy: dostęp do produkcyjnego API wymaga wpłaty 500 zł przedpłaconej kwoty. citeturn0search2turn0search12  
   - Testowe środowisko (sandbox) ma wirtualny budżet na operacje. citeturn0search13turn0search12  
   - Protokół: SOAP. citeturn0search13turn1search2  

2. **WhoisXML API – Domain Availability API**  
   - Dają 100 darmowych zapytań na start. citeturn1search9turn1search0  
   - API wspiera wiele TLD-ów. citeturn0search0  
   - Minusem może być to, że po wyczerpaniu darmowych kredytów koszt rośnie (to już bardziej narzędzie „profesjonalne”).

3. **Whois API (apilayer)**  
   - Ich Whois API ma darmowy plan: 3 000 zapytań miesięcznie. citeturn1search1  
   - Dzięki temu możesz robić zapytania WHOIS i na jego podstawie wywnioskować, czy domena jest zajęta.  
   - Uwaga: to nie stricte „domain availability API” — raczej WHOIS, więc zależnie od TLD i stanu domeny może być mniej jednoznaczne niż dedykowane API dostępności.

4. **WhoAPI**  
   - Mają ogłoszony darmowy plan domen API: według ich komunikatu można dostać **10 000 zapytań**. citeturn1search27  
   - API zwraca informacje o dostępności domeny. citeturn1search10turn1search27  
   - Trzeba sprawdzić, czy ich API wspiera .pl — w dokumentacji nie zawsze wszystkie TLD są wymienione (warto to potwierdzić po rejestracji konta).

5. **WhoisJSON.com – Domain Availability API**  
   - Mają plan darmowy z **1000 zapytań miesięcznie**. citeturn1search21  
   - Proste REST-owe API do sprawdzania dostępności domen w czasie rzeczywistym. citeturn1search21  
   - Trzeba upewnić się, czy obsługują .pl (ich dokumentacja mówi o „wszystkich głównych TLD”).

---

## ✅ Wnioski + rekomendacje

- Jeśli potrzebujesz tylko prostego sprawdzania dostępności .pl domen i nie planujesz bardzo dużego wolumenu zapytań — **WhoisJSON.com** lub **WhoAPI** mogą być najtańszymi opcjami z sensownym limitem.  
- Jeśli chcesz większą niezawodność i masz budżet — **WhoisXML API** to solidne rozwiązanie.  
- Jeśli planujesz integrację rejestracji domen .pl (czyli nie tylko sprawdzanie, ale też rejestrowanie), to API **Domeny.tv** będzie najlepszym wyborem — ale wymaga depozytu.

---

Jeśli chcesz — mogę przejrzeć **aktualne (2025) API dostępne w Polsce** specjalnie pod .pl i dobrać te najtańsze / darmowe — chcesz, żebym to zrobił?

---

**User:**

ok, inne pytanie. Czy domena może stać się dostępna o dowolnej porze, czyli po upływie równo roku od jej kupna? Czy może są to zazwyczaj pełne godziny albo północ w wybranym czasie?

---

**Assistant:**

To bardzo dobre pytanie. To zależy od TLD (końcówki domeny) — ale w przypadku domen .pl cykl życia wygląda tak, że:

1. Po wygaśnięciu rocznego abonamentu domena wchodzi w **okres kwarantanny** („blokada”), który trwa **30 dni**. citeturn1search8turn1search16turn1search10  
2. Po tych 30 dniach, jeśli domena nie zostanie odnowiona, jest „uwalniana” — trafia z powrotem do puli domen wolnych. citeturn0search0turn1search21  
3. Dodatkowo — po usunięciu domeny przez rejestr — trwa **5-dniowy okres „delete hold”**, zanim faktycznie domena stanie się możliwa do rejestracji. citeturn1search7turn1search8  

---

**Wnioski dot. Twojego pytania:**

- Nie staje się dostępna dokładnie „po roku” w sensie jednej sekundy po rocznicy — najpierw są te fazy kwarantanny i oczekiwania.  
- „Uwolnienie” domeny następuje dopiero po upływie tych okresów — czyli dopiero po ~ 35 dniach (30 dni + 5 dni).  
- Co do godziny — rejestr .pl (NASK) nie publikuje, że domeny są uwalniane o konkretnej godzinie (np. północy); pulę domen wolnych można uważać za dostępne mniej więcej po całym dniu uwolnienia (choć dokładny moment może zależeć od działania rejestru i rejestratorów).

Jeśli chcesz — mogę sprawdzić aktualny (2025) cykl życia domen .pl (czy coś się zmieniło) — chcesz, żebym to zrobił?

---

**User:**

tak

---

**Assistant:**

Sprawdziłem — oto aktualny (stan na dziś) cykl życia domen .pl w rejestrze NASK / DNS.pl:  

---

## 🔎 Cykl życia domeny .pl (aktualne zasady)

1. **Rejestracja / okres płatny**  
   - Domena .pl rejestrowana jest na okres od 1 do 10 lat. citeturn0search3turn0search1turn0search9  
   - Umowa rozliczeniowa: po opłaceniu domeny zaczyna się roczny okres („rok rozliczeniowy”) w standardowych przypadkach. citeturn0search1turn0search3  

2. **Brak odnowienia po okresie rozliczeniowym**  
   - Jeśli domena nie zostanie odnowiona po upływie opłaconego okresu (np. po roku), wchodzi w 30-dniowy okres „blocked” — kwarantannę. citeturn0search1turn0search11turn0search3  
   - W tym czasie właściciel domeny może ją odnowić (ale w wielu przypadkach może być doliczona opłata reaktywacyjna). citeturn0search5turn0search3  

3. **Okres usunięcia („delete blocked”)**  
   - Po tych 30 dniach domena trafia w stan, w którym jest usuwana — „delete blocked” – ten okres trwa **5 dni**. citeturn0search4turn0search1  
   - Podczas tych 5 dni domena **nie jest rejestrowalna** przez osoby trzecie. citeturn0search4  

4. **Uwolnienie domeny**  
   - Po zakończeniu tych 5 dni domena zostaje faktycznie zwolniona i wraca do puli nazw wolnych. citeturn0search0turn0search1turn0search11  
   - Według home.pl, 31. dnia (czyli dzień po okresie 30-dniowej kwarantanny) domena powraca do puli wolnych nazw. citeturn0search11  

---

## ✅ Wniosek dla Twojego pytania

- Nie ma mechanizmu, który „gwarantuje”, że domena będzie uwolniona **dokładnie po jednej rocznicy rejestracji** — musisz uwzględnić dodatkowe fazy: 30-dniowy okres blokady + 5 dni usunięcia.  
- Co do godziny uwolnienia — rejestr NASK nie podaje, że domeny są uwalniane w konkretnym punkcie dnia (np. o północy). Uwolnienie następuje raczej na poziomie całodniowym po zakończeniu okresów blokady i usunięcia.

---

Jeśli chcesz — mogę sprawdzić historyczne dane (statystyki) dotyczące **ile domen .pl faktycznie wraca do puli i ile z nich da się „przechwycić”**, żeby lepiej oszacować szanse. Chcesz, abym to zrobił?