# Dryf w modelach LLM (Large Language Models)

W kontekście modeli uczenia maszynowego, w tym Dużych Modeli Językowych (LLM - Large Language Models), **dryf (ang. drift)** odnosi się do zjawiska degeneracji wydajności, dokładności, zachowania lub ogólnej przydatności modelu w czasie (bądź w nowych zastosowaniach). Ponieważ świat, informacje, język ludzki oraz same oczekiwania użytkowników nieustannie się zmieniają, model, który był doskonale dopasowany (ang. *aligned*) i wysoce skuteczny podczas wdrożenia, stopniowo staje się przestarzały lub nieefektywny w nowej rzeczywistości.

Dla tradycyjnych modeli ML mówimy najczęściej o dryfie danych (data drift) i dryfie koncepcji (concept drift). W przypadku LLM zjawiska te są zdecydowanie bardziej złożone ze względu na generatywny, "czarnoskrzynkowy" charakter tych rozwiązań.

---

## Główne typy dryfu w aplikacjach opartych na LLM

### 1. Dryf koncepcji (Concept Drift / Fact Drift)

Zjawisko, w którym zmienia się podstawowa "prawda", definicja pojęcia lub weryfikowalne fakty, jakich model uczył się w fazie pre-training'u.

* **Technicznie:** Prawdopodobieństwo warunkowe $P(Y|X)$ ewoluuje w czasie dla tego samego rozkładu wejścia $P(X)$ (np. niezmienionego promptu). Reprezentacja wiedzy zakodowana w strukturze wag przestaje odpowiadać dzisiejszemu stanowi świata (ang. *stale knowledge*). Oznacza to, że z matematycznego punktu widzenia optymalny cel, który model miał osiągnąć, uległ przesunięciu.
* **Przykład:**
  * *Prompt (2022 r.):* "Kto jest premierem Wielkiej Brytanii i królem tego kraju?"
  * Jeżeli model jest "zamrożony" i dysponuje wiedzą do 2022 roku, z pełnią pewności statystycznej wygeneruje, że premierem jest Boris Johnson a monarchą Elżbieta II, mimo że stan faktyczny w świecie realnym się odwrócił. Prawda merytoryczna odłączyła się od prawdy reprezentowanej w modelu.

### 2. Dryf danych (Data Drift / Covariate Shift)

Zjawisko, w którym nadchodzące do modelu dane (prompty i wejścia od użytkowników bazy produkcyjnej) różnią się swoim rozkładem statystycznym od danych, na jakich system był trenowany bądź wstępnie kalibrowany. Zasadniczo zmienia się populacja, z którą model współdziała.

* **Technicznie:** Zmianie ulega rozkład brzegowy danych wejściowych $P(X)$, pomimo że podstawowe zasady logiki dla konkretnego zagadnienia $P(Y|X)$ nie uległy zmianie. Modele językowe budują swoje wysokie prawdopodobieństwa odpowiedzi na konkretnych konstrukcjach składniowych – wyjście poza dystrybucję (tzw. zjawisko *out-of-distribution, OOD*) silnie zwiększa zjawisko halucynacji (model nie potrafi wywnioskować kontekstu semantycznego z nieznanych wektorów słów).
* **Przykład:**
  * System asystenta e-commerce LLM wytrenowano i zewaluowano przy pomocy poprawnych gramatycznie zapytań (np. "Gdzie znajdę regulamin zwrotów w tym sklepie?").
  * System po wdrożeniu spotyka się z klientami na popularnym komunikatorze mobilnym i otrzymuje skrótowce, regionalne neologizmy, zapożyczenia czy slang ("zwrot hajsu idzie fastem pls? 💀"). Prompty różnią się kolosalnie od korpusu w jakim model ewoluował i gubi on zmysł analityczny, odpisując wadliwie lub z błędem w formatowaniu.

### 3. Zjawisko dryfu zachowania modelu (Behavioral Drift / Performance Drift modeli zamkniętych)

Dotyczy zjawiska, na które mocno narzekają deweloperzy budujący aplikacje w oparciu o płatne, zamknięte API, np. cyklicznie aktualizowane modele dostarczane przez OpenAI (np. GPT-4), Anthropic (np. Claude) czy Google (np. Gemini).

* **Technicznie:** Firmy "za kulisami" w sposób przezroczysty dla użytkownika aktualizują architekturę, kwantyzują model do mniejszej precyzji w celu obniżenia kosztu serwowania oraz przede wszystkim wykorzystują *Continuous RLHF (Reinforcement Learning from Human Feedback)*. Te małe aktualizacje modyfikują dystrybucję wag i aktywacji neuronów u dostawcy. Z powodu tzw. "efektu łóżka wodnego" (ang. *waterbed effect* w kontekście wyrównywania modeli – *alignmentu*), poprawienie jednej cechy (np. zmniejszenie skłonności do pisania złośliwego oprogramowania) powoduje degradację i spadek performancu w innej, często pozornie niezwiązanej płaszczyźnie logiczno-obliczeniowej.
* **Przykład:**
  * Zbudowałeś prompt inżynieryjny generujący obiekty JSON. Na początku roku zapytanie bezwzględnie rzucało w odpowiedzi surowy i gotowy do sparsowania JSON.
  * Kilka miesięcy później twórca modelu dodaje do warstwy systemowej instruktarz RLHF poprawiający "rozmowność" (chattiness) asystenta. Od teraz Twoje API wciąż przetwarza aplikację starą rewizją wywołania do end-pointa, ale nagle odpowiedzi zawierają dodatek tekstu typu:\n```json\n...\n``` \n*Oto twój json, mam nadzieję że pomogłem!*. Aplikacja w back-end programisty nie przewidziała tekstu jako sufiksu i aplikacja masowo powoduje wyjątki *JSON Decode Error*. To klasyczny i najczęstszy dryf z jakim walczą inżynierowie oprogramowania LLM (LLMOps). Wykrywana jest też nagła tendencja modelu na przestrzeni miesięcy (przy tych samych parametrach wejściowych) do skracania kodu programu słowami `// reszta kodu taka sama` pomimo wymuszenia w instrukcji braku skracania.

### 4. Dryf promptów (Prompt Drift)

Odwrócenie zjawiska dryfu behawioralnego, leżące stricte po stronie deweloperów używających narzędzia, polegające na kumulowaniu zmian, szumnego warunku i nakładaniu poprawek "na plaster", degradujących jakość docelową modelu.

* **Technicznie:** Aby wymusić specyficznie unikalne zachowania dla konkretnego błędu generatywnego tworzony jest gigantyczny prompt ze słowami warunkowymi IF/THEN itp. Stopniowo zwiększa on zajmowaną długość i skomplikowanie dystrybucji tokenów i zmniejsza siłę oddziaływania poszczególnych "uwag od programisty", ze względu na spadek skuteczności zjawiska atencji do bardzo gęstych tekstów poleceń dla sztucznej inteligencji. Twórcy aplikacji psują własne instrukcje ewoluując w złym kierunku.
* **Przykład:** System zaczyna od prostego "Jesteś botem do pisania e-maili marketingowych". Po roku ewoluował w dwustronicową epopeję instruująca, czego bot nie może, jak ma analizować tekst, ile słów generować oraz na co zwracać uwagę. System atencji LLM staje się "zagłuszony" regułami co prowadzi do drastycznej regresji możliwości z zadania pierwotnego.

### 5. Dryf wektorowy / modelu osadzającego RAG (Embeddings Drift)

Specyficzny i zaawansowany technicznie problem dla systemów wzbogaconej generacji Retrieval-Augmented Generation (RAG).

* **Technicznie:** RAG przekształca słowa/dokumenty w wektory bazując na danym modelu klasyfikacyjnym (tzw. Model Embeddings). Odległości topologiczne pomiędzy tokenami w tej przestrzeni ustalają podobieństwo semantyczne wykorzystywane w algorytmach przybliżonego wyszukiwania (jak *KNN*, *Cosine Similarity*). Jeśli firma w przyszłości zmieni bazowy model wykorzystywany przy konwersji (lub np. zaktualizuje bazę o nowe dokumenty ale nie odświeży starego zbioru indeksów lub semantyki słów-kluczy), relacje odległości wektorowej przestają być użyteczne. Klastry dawnego pojęcia w przestrzeni nie pokrywają się już spójnie z klastrami nowego zapytania klienta, co prowadzi do błędnego działania całego silnika.
* **Przykład:** Zmieniono model Embeddingu z generacji 2 OpenAI na v3 ze statystycznym reduktorem wymiarów wektora, a pozostawiono stare osadzenia regulaminu w bazie wektorowej (VectorDB) po czym zapętlono obieg. Aplikacja zamiast podsuwać modelowi pożądane fragmenty PDF, zaczyna jako kontekst dorzucać czysty losowy szum (śmieciowe słowa wykraczające poza próg odległości dystansu wyszukiwań z uwagi na niespójny rozmiar ukrytego wymiaru danych – hidden state shape wymuszenie macierzy do 1536 wymiarów), tworząc krytyczny dryf i powstawanie halucynacji LLMa na wyjściu.

---

## Przeciwdziałanie i monitorowanie (LLM Observability / LLMOps)

Ponieważ zapobieganie dryfom jest skrajnie trudne (i leży głównie po stronie providera), inżynieria wdrożeń wypracowała skuteczne mechanizmy i bariery zapobiegające propagacji błędów (często klasyfikowane jako techniki **AIOps/LLMOps**):

1. **Golden Datasets (Złote zbiory ewaluacyjne):** Przygotowanie statystycznie reprezentatywnej, stałej bazy np. 200 konkretnych promptów połączonych z pożądanymi asercjami co do ich wyników wyliczanymi za pomocą heurystyk klasycznych, regex'a, wyznaczników formatu lub skryptów weryfikujących poprawność kodu. Sprawdza się na nich całościowo system przy używaniu metodyki CI/CD po każdym drobnym commit'cie.
2. **Ciągła Ewaluacja z użyciem LLM-as-a-Judge:** Koncepcja polega na tym, by z wykorzystaniem o wiele większego, uchodzącego za aktualny stanu "wzorcowego" modelu (zazwyczaj drogiego i potężnego np. najnowszy Claude 3.5 Sonnet w trybie niskiej temperatury) rutynowo próbkować (np. 1% logów z produkcji) logi modelu tańszego serwowanego wdrożeniowo (np. LLaMa-3 8b) pod kątem zmian we wskazywanym zachowaniu, formacie, toksyczności, "grzeczności", zgodności z faktami; ewentualnie do porównywania czy RAG zwraca odpowiedzi zgodne z załączonym z wewnątrz bazy wektorowej kontekstem dokumentowymi.
3. **Wersjonowanie Promtów i Modeli (Pinning API / Version Control):** Bezwzględny zakaz produkcyjnego odwoływania do ruchomych aliasów API providera typu `gpt-4` a ścisłe operowanie na tzw. zamrożonych cyklach modeli typu `gpt-4-0613` co gwarantuje nam (zazwyczaj do roku kalendarzowego wytyczonego przez twórcę i jego deprecjacji rynkowej), że wagi modelu nie ulegną cichej zamianie skutkując *Behavioral Drift*. Jak i trzymanie samych promptów w formacie ustrukturyzowanych plików do weryfikacji Git.
4. **Monitorowanie Metryk Zaufania i Rozkładów Tokenów:** Śledzenie typowych metryk numerycznych i dystrybucji wyjścia np. monitorowanie średniej długości tokenów przed i po aktualizacji w ujęciu tygodniowym, liczby pustych lub powtarzających się struktur odpowiedzi. Niestandardowy spadek (powodujący wykresowy pick, gwałtowne "ucięcie", peak) na takich wykresach dobitnie diagnozuje dryf bez wnikania narazie w treści tekstowe w logach.
