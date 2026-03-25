# Bezpieczeństwo Danych, Kontrola Dostępu i Governance AI

Zagadnienia bezpieczeństwa danych, kontroli dostępu oraz Governance (zarządzania) AI są kluczowymi elementami dojrzałego wdrażania systemów opartych na sztucznej inteligencji. Firmy kładą na to ogromny nacisk ze względów prawnych (RODO, nadchodzący EU AI Act), biznesowych (ochrona własności intelektualnej) i wizerunkowych, ponieważ awarie lub naruszenia związane z systemami AI mogą prowadzić do poważnych konsekwencji.

## 1. Bezpieczeństwo Danych (Data Security)

Jest to fundament budowy bezpiecznych i godnych zaufania cykli projektowych w dziedzinie Data Science. Obejmuje ochronę powierzonych archiwów poprzez zapobieganie ich utracie, modyfikacji lub przedostaniu się w niepowołane ręce.

- **Ochrona w cyklu życia**: Zastosowanie odpowiednich standardów ochrony danych na każdym etapie: Data at Rest (gdy dane są przechowywane – np. zaawansowane szyfrowanie dysków i magazynów), Data in Transit (gdy dane są przesyłane – komunikacja przez TLS/SSL) oraz Data in Use.
- **Anonimizacja i pseudonimazacja (PII)**: Skrupulatne usuwanie, maskowanie oraz zamazywanie Wrażliwych Danych Osobowych (Personally Identifiable Information) w zbiorach treningowych tak, aby modele nie mogły uczyć się i replikować zachowań naruszających prywatność.
- **Ochrona wektorów ataku AI**: Systemy AI mogą posiadać specyficzne podatności:
  - *Data Poisoning*: "Zatruwanie" zbiorów uczących odpowiednio spreparowanym szumem w celu błędnego wytrenowania modelu.
  - *Prompt Injection/Jailbreaking*: Próba zmuszenia modelu LLM do ominięcia zabezpieczeń aplikacyjnych. 
  - *Model Inversion / Data Extraction*: Rekonstrukcja, ekstrakcja prywatnych informacji z wytrenowanego, dostępnego powszechnie modelu.

## 2. Kontrola Dostępu (Access Control)

Zarządzanie tym, w jaki sposób i w jakim zakresie ludzie (oraz maszyny lub aplikacje M2M) mają dostęp do wrażliwego ekosystemu ML.
- **Zasada Najmniejszego Uprzywilejowania (PoLP)**: Reguła, która w środowiskach typu chmura publiczna (AWS IAM, Azure RBAC) wymaga nadawania każdemu i każdej aplikacji absolutnie minimalnych uprawnień niezbędnych do wykonania ich operacji.
- **RBAC & ABAC**: Wykorzystywanie Access Control opartego o ROLĘ (np. Data Engineer, MLOps, Data Scientist) lub globalnego opartego o ATRYBUTY dostępu (np. strefa geograficzna, powaga środowiska).
- **Zabezpieczenie Rejestrów Modeli (Model Registry)**: Narzędzia takie jak MLflow czy W&B wymagają oddzielnej warstwy zabezpieczeń. Ograniczony dostęp zapisywania nowych i wdrażania zatwierdzonych (skategoryzowanych np. jako _production_) modeli tylko przez odpowiednie i autoryzowane grupy czy narzędzia CI/CD.

## 3. Governance AI (Zarządzanie AI i Zgodność)

To szeroko pojęte ramy i polityki definiujące, w jaki sposób firma w sposób przejrzysty i etyczny korzysta ze sztucznej inteligencji, podlegając przy tym regulacjom zewnętrznym lub nakazom wewnątrzkorporacyjnym.

- **Audytowalność i XAI (Explainable AI)**: Modele – szczególnie w domenach takich jak obiektywna zdolność kredytowa, aplikacje rekrutacyjne, czy medycyna – podlegają rygorowi polegającemu na tym, że ich decyzje nie mogą być czystą zamkniętą skrzynką (black box). Konieczne jest wsparcie warstw interpretacji np. za pomocą SHAP lub LIME.
- **Raportowanie Wersjonowania**: Monitorowanie pełnego przepływu: z jakich historycznych danych, z jakimi hiperparametrami i kodem, przez kogo został wytrenowany dokładny wdrażany na środowisko produkcyjne model sztucznej inteligencji. Wersjonowanie danych to standard np. korzystając z DVC (Data Version Control).
- **Zarządzanie Ryzykiem, Bias & Drift**: 
  - *Data Drift / Concept Drift*: Nadzorowany, nieustanny monitoring na produkcji tak, aby w locie wykrywać pogarszające się statystyki skuteczności wskutek degradacji/zmian danych wejściowych w czasie.
  - *Monitorowanie Uprzedzeń (Bias)*: Śledzenie i neutralizowanie niesprawiedliwego profilowania.
- **Zgodność z przepisami (Regulatory Compliance)**: Uwzględnienie mechanizmów (oraz odpowiedniej metadokumentacji) zapewniających pełną zgodność m.in. z wytycznymi wprowadzonymi za sprawą *EU AI Act* - kategoryzacji poziomu ryzyka platform czy poszanowania *Right to be Forgotten*.

---

## Lista pytań rekrutacyjnych:

1. W jaki sposób zabezpieczyłbyś architekturę RAG (Retrieval-Augmented Generation) przed atakami typu Prompt Injection oraz przed wyciekiem danych, do których pytający użytkownik nie powinien mieć dostępu (konteksty uwierzytelniania w wektorowej bazie)?
**Odpowiedź:** 
- **Prompt Injection:** Należy zastosować walidację wejścia, wyraźne wyodrębnienie promptów systemowych (np. użycie tagów XML) oraz użycie modeli guardrails (np. Llama Guard) filtrujących zapytania przed i po przekazaniu do głównego LLMa.
- **Wyciek / Kontrola Dostępu:** Konieczne jest użycie filtrowania uwzględniającego metadane (Metadata Filtering) i Role-Based Access Control (RBAC) po stronie warstwy Retrieval. Każdy "chunk" tekstu w bazie wektorowej wymaga otagowania grupą dostępu (odpowiadającą np. uprawnieniom w systemie z którego pochodzi - jak ACL z Confluence), a zapytanie RAG modyfikuje się "w locie" o te parametry, twardo zawężając wyszukiwanie tylko do dozwolonych dokumentów.

2. Jakie są główne wyzwania i jak można zapewnić poprawną anonimizację tekstu nieustrukturyzowanego w dużych zbiorach do treningu modeli NLP?
**Odpowiedź:** 
- **Wyzwania:** Naturalna niejednoznaczność i nieregularność języka ludzkiego (odmiany i przypadki, potocyzmy czy imiona powszechnie brzmiące jak rzeczowniki) oraz niemożliwość odszukania intencji wrażliwych występujących jako ukryty kontekst.
- **Zapewnienie poprawności:** Zastosowanie metody hybrydowej: od ścisłych RegEx'ów (odnajdujących np. pesele, numery kont, kody pocztowe), po modele NLP NER (Named Entity Recognition), które klasyfikują i wykrywają skomplikowane pola Personal Identifiable Information i zamieniają je na bezpieczne uniwersalne tagi, jak [NAME/PERSON], [LOCATION]. Wykorzystuje się np. bibliotekę *Microsoft Presidio*.

3. Wytłumacz, na czym polega "Data Poisoning" i jakie kroki byś zaplanował, by uniknąć tego ryzyka w procesie uczenia się modelu w pętli ciągłej (tzw. "online learning")?
**Odpowiedź:** 
- **Definicja:** Data Poisoning (Zatruwanie danych) to wprowadzanie celowo zrobionych próbek do danych wejściowych aby zmanipulować klasyfikator/model i jego margines decyzyjny tak by zachował się przewidywalnie w wybranej błędnej, ustalonej z góry przez hakera ścieżce logicznej (np. pomijał oszustwa jako ruch organiczny). 
- **Unikanie w Online Learning:** Należy zastosować modele z góry sklejone z logiką wykrywania anomalii (Anomaly/Outlier Detection). Modele te "odrzucają" odstawiające i mało wiarygodne przypadki treningowe. Stosuje się ograniczanie i redukowanie wpływu jednej paczki danych na wagi (Gradient Clipping, progi akceptowalności), wprowadza się automatyczny proces monitoringu KPI z modelem fallback, jak również wyższe wagi i audyt manualny dla zaufanych użytkowników systemowych zgłaszających flagi incydentów.

4. Jak zorganizowałbyś zarządzanie kontrolą dostępu na platformie MLOps (np. w oparciu o narzędzia MLflow albo Vertex AI/SageMaker) współpracując z wieloma niezależnymi zespołami Data Science?
**Odpowiedź:** 
- **Izolacja klastrów/środowisk:** Tworzenie odseparowanych tzw. Workspace'ów/Namespace'ów pod każdy zespół na platformie natywnej wraz z całkowicie osobnym dostępem po stronie Cloud (osobne pule IAM Access Role do dedykowanych S3).
- **PoLP (Least Privilege / RBAC):** Użytkownicy z zespołu wprowadzają modyfikacje testów i wagi jedynie ze swojego obwodu. Rejestrem Produkcyjnym (Model Registry np. we MLflow) oraz uruchamianiem wnioskowań zarządzają twardo zdefiniowane, autoryzowane konta techniczne (Service Accounts), wywoływane dopiero z linii CI/CD.
- **Pełne Audytowanie API:** Stale włączony Data Catalog / Governance logs dokumentujący zapytania API od strony użytkowników chmury oznaczające odpalane w locie paski Jobów z platform DS.

5. Na czym polega dryf danych (Data Drift) a na czym dryf pojęć (Concept Drift) i w jaki sposób jako Inżynier MLOps powinieneś wdrożyć ich monitorowanie, by odpowiadało to regułom AI Governance?
**Odpowiedź:** 
Wyobraź sobie, że trenujesz model przewidujący, czy dany dom zostanie szybko sprzedany.
- **Data Drift (Dryf Danych) – "Zmienił się świat wokół nas":** Model otrzymuje nowe dane robocze, które wyglądają inaczej niż te z momentu treningu (zmienia się statystyka i proporcje cech), ale same prawa rządzące rynkiem pozostają takie same.
  * _Przykład:_ Model uczył się na domach o pow. 100m². Dzisiaj deweloperzy budują tylko małe metraże, więc do oceny wpadają głównie domy po 40m². Świat się zmienił, do systemu wlewa się lawina danych wcześniej będących rzadkością, więc model się myli (nie radzi sobie z gęstą ilością nowych próbek), mimo że ogólne zasady sprzedaży się nie zmieniły.
- **Concept Drift (Dryf Pojęć) – "Zmieniły się zasady gry":** Zmienia się fundamentalna relacja między rzeczywistością (wejściem) a tym, co zgadujemy (wyjściem). Kształt danych nie musi się zmieniać, ale całkowicie zmienia się to, jak ludzie na nie reagują.
  * _Przykład:_ Kiedyś domy na dalekich przedmieściach sprzedawały się koszmarnie wolno. Gdy naszła pandemia i praca zdalna, ci sami klienci zaczęli wręcz natychmiast kupować domy daleko za miastem. Dane wejściowe domów (powierzchnia, adres) są takie same jak dawniej, ale ludzkie pragnienia odwróciły się o 180 stopni.
- **Jak to monitorować (MLOps):** Model oddany do produkcji nigdy nie będzie doskonały w nieskończoność. Aby spełnić reguły AI Governance trzeba obudować go ochronnym "panelem kontrolnym".
  1. Do architektury dopina się wtyczki analityczne (np. *Evidently AI*, *SageMaker Model Monitor*). 
  2. Narzędzia te cyklicznie porównują najnowszy napływający ruch od klientów ze starymi danymi, których użyto do jego uczenia, w użyciu mając matematyczne testy (odchylenia statystyczne).
  3. Gdy tylko system zauważy, że trafność predykcji nagle opadła poniżej progu (Concept Drift) albo struktura informacji napływających przestała przypominać te "znane" (Data Drift), jest zmuszony wygenerować jasny alert dla Data Science (np. na Slack) lub wręcz automatycznie zawiesić autonomiczną decyzyjność sztucznej inteligencji, domagając się ręcznego i natychmiastowego przetrenowania wdrożenia.

6. Jakie wymagania i konsekwencje narzuca na etykę czy architekturę AI implementacja systemów zgodna z "EU AI Act" w przypadku projektów zakwalifikowanych jako systemy sztucznej inteligencji wysokiego ryzyka (High-Risk AI Systems)?
**Odpowiedź:** 
- **Wymagania Architektur i Etyka:** Tworzenie systemu według ramy "Compliance by design". Obowiązki obejmują konieczności pełnego audytu cyklicznego modelu (testy XAI - ocena przejrzystości AI, jak za pomocą metod *SHAP*), rejestrowania bardzo twardej dokumentacji analitycznej, tworzenie logów do ew. cofania algorytmiki z wbudowanym monitorowaniem stronniczości i uprzedzeń społecznych (Data Bias Mitigation).
- **Krytyczne "Human in the loop":** Zapewnienie stałego i przetestowanego nadzoru pracowniczego/ludzkiego zdolnego nadpisać, zablokować bądź odwołać wyroki platform AI. Konsekwencją lekceważenia procedur tego poziomu ryzyka są dotkliwe kary do do rzędu 35 mln Euro bądź do 7% przychodów.

7. Wyjaśnij pojęcie "Model Inversion" (lub model extraction) w środowisku udostępniającym model jako serwer API (MaaS). Jakie są główne wektory ograniczania tego zagrożenia?
**Odpowiedź:** 
- **Model Inversion / Extraction:** Zagrożenie bezpieczeństwa, które polega na wydobywaniu z serwerów udostępniających model i predykcje, prywatnych i wrażliwych parametrów z których budowany był i generowany pierwotny Dataset Treningowy (Model Inversion - np. rekonstrukcja prywatnego wizerunku człowieka) bądź kradzież struktury modelu z samych API Request/Response (Extraction).
- **Zapobieganie:** Brutalne rate-limitowanie, odcinanie próbkowych i nadzwyczajnie podobnych tysięcy zapytań z podobnych IP z drobnymi modyfikacjami. Zamaskowanie wyników dla usera ("Confidence Score") obustronnie ukrywając rozkłady prawdopodobieństw pod ogólną flagę decyzji, bądź na etapie Model-Training wykorzystanie procedury dążącej w celu Differential Privacy do sztywnego nałożenia twardego szumu modyfikującego lekko logikę predykcji a nie naruszającego wyników ostatecznych.

8. W jaki sposób zaimplementowałbyś mechanizm kontroli spójności pochodzenia danych ("Data Lineage") dla skomplikowanego potoku przetwarzania tak, by model poddający się łatwo procesowi audytowemu spełniał ostre standardy Enterprise?
**Odpowiedź:** 
Połączenie MLOps i Governance do twardej walidacji powiązań krok-po-kroku (Directed Acyclic Graph) od surowej bazy dla Modelu. W użyciu:
- **DVC (Data Version Control):** Zestawienie hashu danych użytych do produkcji by w ułamku sekund wrócić z dokładnego pliku wektoru.
- **Logika w Orchestratorach:** Pipeline Data-Eng na *Apache Airflow*, który logikalnie i w graficzny sposób taguje Run i powiązany branch w wbudowanym repozytorium (tzw. powiązanie kodu logicznego z model registries typu MLflow).
- Wszystko to jest raportowane twardo do bazy (Metadata catalog/DataHub), więc dla celów Audytora możliwe jest pełne odwzorowanie historii skąd wziął się dany endpoint (Dokładny model, Skrypt, Hash Commit na Git i zrzucenie pliku danych wejściowych).

9. Załóżmy, że użytkownik wnioskuje o "prawo do bycia zapomnianym" (usunięcie na podstawie RODO). W jaki sposób adresuje się to prawo w przypadku obecności tych danych w uprzednio wyuczonym modelu deep learningowym?
**Odpowiedź:** 
Usunięcie konkretnej, wplecionej porcji danych z "uczenia pamięci" neuronowej w Deep Learningu jest drastycznie trudne, stąd adresuje to sie w ramach:
- **Mechanizmy Prewencyjne i Maskowanie (Anonymization/PII Scrubber):** Oczyszczanie przed samym startem całego eksperymentu - na Data Lake. Dane usera nigdy nie dotykały logiki SI w sposób zidentyfikowany. Gdy zostaną zapomniane z hurtowni korporacyjnej relacja upada bez edycji.
- **Pełen Retraining Mode:** Jeśli dane były użyte wprost, z uwagi na model matematyczny - wykonuje się "Full Delete", po czym okresowe zrzuty pełnego wyrokowania/ponownego rygorystycznego przetrenowywania struktury modelu po wyrzuceniu tych wpisów od "zera" powiedzmy raz na miesiąc, a w międzyczasie odcinanie wyjść filtracyjnych.
- **Machine Unlearning:** Nowoczesna technika zacierania algorytmicznego gdzie badacze precyzyjnie nadpisują wagi/przekierowania minimalizujące zarys danej jednostki z bazy bez wymuszenia kosztownego przetrenowywania całości DeepLearning.
