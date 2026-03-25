# Dobór podejść ML/LLM pod konkretne przypadki użycia

## Podsumowanie
Wybór odpowiedniego podejścia z obszaru uczenia maszynowego (ML) lub dużych modeli językowych (LLM) jest kluczowy w budowie efektywnych i skalowalnych systemów AI. Nie każdy problem wymaga użycia najpotężniejszego modelu LLM na rynku. Często tańsze, szybsze i równie skuteczne mogą okazać się tradycyjne metody ML lub inżynieria cech we współpracy z mniejszymi modelami. Proces decyzyjny zależy od całej gamy czynników, takich jak rodzaj danych, dostępne zasoby, budżet, wymagane opóźnienia (latency), wielkość istniejącego zbioru danych treningowych oraz potrzeba interpretowalności.

## Dlaczego to ma znaczenie?
Błędny dobór technologii i ślepe podążanie za "hype'm" może prowadzić do poważnych problemów projektowych i biznesowych:
- **Koszty i Przekroczenie budżetu:** (np. używanie potężnego modelu GPT-4 przez API do prostej klasyfikacji sentymentu miliona krótkich tweetów wygeneruje ogromne koszty, podczas gdy model BERT lub naiwny klasyfikator Bayesa byłyby niemal darmowe po wytrenowaniu).
- **Problemy z wydajnością (Latency):** Wymagania systemów czasu rzeczywistego często wykluczają powolną inferencję LLMów i opóźnienia związane z wywołaniami API.
- **Brak interpretowalności:** Sieci neuronowe traktuje się w dużej mierze jako tzw. czarne skrzynki (black boxes). Trudno wytłumaczyć, dlaczego model odrzucił wniosek o kredyt, w przeciwieństwie do przejrzystych modeli typu drzewa decyzyjne z jasnymi regułami.
- **Overengineering:** Zastosowanie nadmiarowych, trudnych w utrzymaniu struktur tam, gdzie wystarczyłoby znacznie prostsze i pewniejsze podejście.

## Jak to działa w praktyce (Dostępne podejścia)

Zwykle rozważamy następujące opcje – uszeregowane rosnąco według złożoności lub zasobożerności:

### 1. Heurystyki, wyrażenia regularne i systemy regułowe (Rule-based)
- **Kiedy stosujemy:** Gdy problem jest bardzo prosty i deterministyczny. Np. wykrywanie we wpisach konkretnych słów zakazanych, parsowanie i walidacja formatu adresu email, wyłapywanie twardych logik biznesowych.
- **Zalety:** 100% przewidywalności, pełna interpretowalność, zerowe koszty treningu i natychmiastowe działanie. Brak halucynacji.

### 2. Tradycyjne uczenie maszynowe (Traditional ML - np. XGBoost, Random Forest, Regresja Logistyczna)
- **Kiedy stosujemy:** Mamy ustrukturyzowane (tabelaryczne) dane historyczne. Zadania, takie jak predykcja "churnu" (rezygnacji klientów), szacowanie cen, prosta klasyfikacja predefiniowanych danych liczbowych.
- **Zalety:** Świetne radzenie sobie z danymi ustrukturyzowanymi. Model taki jest znacznie łatwiejszy do zinterpretowania za pomocą technik XAI (Explainable AI) jak SHAP czy LIME. Wymaga niewiele pamięci i mocy obliczeniowej podczas wnioskowania (inferencji).

### 3. Klasyczne modele Głębokiego Uczenia (Deep Learning - sieci CNN, RNN) oraz starsze Transformersy (BERT)
- **Kiedy stosujemy:** Przy pracy ze specyficznymi danymi nienumerycznymi, z dużą ilością danych własnych – np. wykrywanie obiektów na zdjęciach, segmentacja, przetwarzanie sygnałów lub osadzanie mniejszych porcji tekstu według własnych reguł domenowych. 
- **Zalety:** Bardzo wysoka skuteczność na nieustrukturyzowanych danych, gdy posiadamy pokaźny wolumen dobrze otagowanych przykładów uczących.

### 4. Duże Modele Językowe (LLMy) po API - klasyczny Prompt Engineering
- **Kiedy stosujemy:** Na etapie budowy MVP, podczas szerokich zadań związanych z przetwarzaniem języka naturalnego (NLU/NLG) – streszczanie i parsowanie dużych nieustrukturyzowanych bloków tekstu, czatowanie, pisanie treści, tłumaczenia.
- **Zalety:** Gotowość do pracy zaraz po podpięciu (zero-shot/few-shot learning), niezwykła wszechstronność bez inwestycji we własne szkolenie. Często najlepsza relacja czasu wdrożenia do efektu.

### 5. LLM + Retrieval-Augmented Generation (RAG)
- **Kiedy stosujemy:** Kiedy potrzebujemy odpowiadać na pytania użytkownika dokładnie na podstawie konkretnej i zamkniętej bazy wiedzy firmy (np. polityki HR, wewnętrzne instrukcje techniczne). 
- **Zalety:** Ogromna redukcja tzw. halucynacji (model nie musi "pamiętać", bo otrzymuje wiedzę w kontekście). Rozwiązanie skalowalne – aby "douczyć" system nowej wiedzy, po prostu dosilamy bazę wektorową, nie dotykając wag modelu.

### 6. Fine-Tuning (Dostrojenie) / Small Language Models (SLM) np. Llama 3 8B z LoRA
- **Kiedy stosujemy:** Kiedy chcemy wymusić ściśle określony format/styl odpowiedzi, zależy nam na wiedzy z określonej niszy (np. skomplikowanej terminologii medycznej), a użycie RAGa lub potężnych promptów z przykładami staje się zbyt drogie i obciąża context-window. Równolegle to technika migracji z płatnych zewnętrznych usług (jak OpenAI) do własnych, szybkich, tańszych hostowanych modeli lokalnych.
- **Zalety:** Znaczące zoptymalizowanie długofalowych kosztów inferencji i opóźnień (mniejszy model odpowiada szybciej), zwiększona celność i zapanowanie nad outputem w wąskim zastosowaniu. Własny model = własna polityka prywatności i przechowywania danych.

### 7. Trening modelu od zera (Pre-training / Train from scratch)
- **Kiedy stosujemy:** Praktycznie nigdzie z punktu widzenia zwykłej optymalizacji procesów firmy. Robi się to tylko by uzyskać tzw. *Foundational Model*, w przypadku nowatorskich dziedzin rynkowych lub jako inicjatywy naukowe (np. model od zera dla skrajnie nowego języka/dialektu albo wielomiliardowe budżety Big Techu).

---

## Pytania i odpowiedzi ułatwiające przygotowanie do rozmowy

**1. W jakich przypadkach zdecydowałbyś się na wytrenowanie tradycyjnego modelu ML (np. XGBoost) zamiast wdrażania zaawansowanego modelu LLM?**
**Odpowiedź:** 
Tradycyjne modele ML (jak XGBoost, Random Forest) są preferowane, gdy:
- Pracujemy z danymi ustrukturyzowanymi/tabelarycznymi (np. pliki CSV, bazy SQL z danymi numerycznymi lub kategorycznymi).
- Problem to typowa klasyfikacja, regresja lub klasteryzacja (np. przewidywanie churnu, ocena ryzyka kredytowego).
- Zależy nam na wysokiej interpretowalności i wyjaśnialności modelu (XAI), z możliwością zbadania feature importance (ważności cech).
- Mamy w systemie rygorystyczne wymagania co do czasu wnioskowania (bardzo niskie latency), kosztów infrastruktury oraz przewidywalności (brak "halucynacji").

**2. Jakie są różnice w kosztach (zarówno wdrożenia jak i późniejszej eksploatacji) pomiędzy systemem wykorzystującym architekturę RAG, a wykonaniem Fine-tuningu LLMa na specyficznych danych operacyjnych firmy? Kiedy odpowiedniejsze będzie zastosowanie każdej z tych metod?**
**Odpowiedź:** 
- **RAG (Retrieval-Augmented Generation):** Niższe koszty wdrożenia (wymaga stworzenia bazy wektorowej i prostej orkiestracji, możemy użyć szybkiego modelu po API bez kosztownego ustrukturyzowanego treningu QA). Koszty eksploatacji zależą od skali tokenów, ale dodawanie nowej wiedzy do bazy jest praktycznie darmowe (tylko embedowanie). RAG jest odpowiedni, gdy wiedza często się zmienia i chcemy uniknąć halucynacji podając twarde fakty z systemu (szczególnie niszowe dokumenty firmy).
- **Fine-Tuning:** Ekstremalnie wysokie relatywnie koszty wdrożenia (wymaga przygotowania bardzo czystych, specyficznych datasetów instruktarzowych oraz użycia farmy GPU do treningu) i wysokie koszty utrzymania jeśli hostujemy wysoce wyspecjalizowany model samodzielnie pod wysokie obciążenia. Fine-tuning stosuje się na rzadszych przypadkach: gdy musimy narzucić modelowi konkretny **format, styl opowiadania, zachowanie i konkretny ton głosu**, a niekoniecznie zasilać go gigantyczną bazą wiedzy, lub gdy chcemy wdrożyć mały model w celu szybkiej realizacji bardzo wybiórczego specjalistycznego skilla nie marnując tokenów w prompcie.

**3. Powierzono Ci zaprojektowanie systemu RAG dla działu prawnego firmy. System jednak nie zawsze udziela wystarczająco dokładnych odpowiedzi. Jakie kroki podejmiesz weryfikując jego architekturę u podstaw operacyjnych, zanim zasugerujesz zespołowi, że trzeba dotrenować model (Fine-Tuning)?**
**Odpowiedź:** 
Przed zasugerowaniem kosztownego fine-tuningu, przeanalizowałbym lejek RAG:
- **Jakość i strategię chunkingu:** Czy podziały dokumentów nie ucinały ważnego prawnego kontekstu? Przeprowadziłbym eksperymenty z rozmiarem chunków oraz ich overlappingiem (np. 1000 znaków i 200 znaków zakładki) czy nawet semantycznym chunkingiem dopasowanym do struktur dokumentów.
- **Proces Embeddingu:** Czy model wektorowy (embedding model) np. `text-embedding-3-small` radzi sobie dobrze operując w specyfice skomplikowanego języka polskiego świata prawniczego?
- **Strategię pobierania (Retrieval):** Użycie technik takich jak HyDE (Hypothetical Document Embeddings), a zwłaszcza **Re-ranking** (np. Cohere Re-rank, Cross-Encoders) aby upewnić się, że to co baza wektorowa znajduje na 1-wym miejscu faktycznie odpowiada zapytaniu.
- **Jakość promptu podsumowującego i instrukcje:** Upewnienie się, że model generujący końcową odpowiedź ma bardzo stanowczą systemową deklarację zmuszającą go do korzystania "tylko z dostarczonego kontekstu pod rygorem zwrotu 'nie potrafię precyzyjnie odpowiedzieć na podstawie materiałów'". Najczęściej powodem słabego RAG nie jest model, tylko śmieciowy kontekst wejściowy (garbage in - garbage out).

**4. Twoim zadaniem jest stworzenie klasyfikatora zgłoszeń od klientów do odpowiednich działów (masz około 15 zdefiniowanych kategorii). Dysponujesz bazą z historycznymi przypisaniami dla 200 tysięcy zgłoszeń. Jakiego podejścia użyjesz zaczynając projekt (faza MVP), a co zrobisz, aby zoptymalizować go w fazie wejścia na dużą skalę produkcyjną i dlaczego?**
**Odpowiedź:** 
- **MVP (Faza początkowa w kilka dni):** Zastosowałbym potężny gotowy model po API LLM (np. GPT-4o-mini lub Claude 3.5 Haiku) poprzez bardzo dobry Prompt (tzw. Few-Shot Prompting). W instrukcji opisałbym definicję owych 15 kategorii, dałbym kilka złotych przykładów i zbudowałbym parsowanie wyniku przez JSON. Pozwala to przetestować ideę z zerowymi kosztami tworzenia modelu.
- **Wielka Skala (Produkcja):** Skoro mam zaufany zbiór "otagowanych" 200 tysięcy biletów, natychmiast wytrenowałbym tradycyjny algorytm MLowy na TF-IDF albo dotrenował klasyczny mały model głęboki dedykowany do klasyfikacji zadań językowych (np. dystrybucje opierające się o architekturę BERT/RoBERTa lub po prostu polski HerBERT). Da to radykalny spadek kosztów związanych z API cloud providerów, zaoferuje ułamkowe koszty środowiskowe z bliskim zera procentowym stopniem "halucynacji" nowej wyimaginowanej klasy.

**5. Kiedy byś doradził CTO inwestycję w trenowanie własnego, małego modelu językowego (SLM - np. poprzez fine-tuning używając PEFT/LoRA), a kiedy postawiłbyś twardo na poleganie na potężnych modelach zewnętrznych dostępnych jedynie przez API (np. Claude 3 / GPT-4)?**
**Odpowiedź:** 
- **Własny SLM (z PEFT/LoRA/QLoRA):** Rekomendowałbym w sytuacjach skrajnej poufności danych, gdzie reguły operacyjne zakazują rzucania danych poza lokalną, certyfikowaną infrastrukturę do np. USA (sektor bankowy, tajne procedury obronne). Często też optymalny ruch przy problemach jednozadaniowych uderzanych pod ciężkim "loadem", gdzie setki tysięcy wywołań specyficznego tasku powoduje olbrzymie miesięczne koszta w topowych komercyjnych modelach cloudowych. Szybkość (latency) mniejszego lokalnego modelu 8B będzie też zauważalnie lepsza.
- **Zewnętrzne modele (OAI / Anthropic):** Wybieramy, gdy rozwiązujemy szeroki wielorakowy problem analityczny, gdzie na najwyższej wadze stawiane jest potężne rozumowanie ogólne problemu, logiczna analiza dokumentacyjna skomplikowanych zagadnień, tworzenie zaawansowanego kodu. Jeżeli jakość abstrakcji wnioskowania ma największy priorytet ekonomiczny (często większy od ewentualnego rachunku per API), to topowe modele nie mają realnej lokalnej alternatywy nie wymagającej serwerów z farmami wielkich H100 GPU do prostej inferencji.

**6. W jaki sposób opóźnienia środowiskowe dla czasu wnioskowania (inference latency) i ograniczone zasoby obliczeniowe mogą wpłynąć na Twoją decyzję przy wyborze architektury AI dla systemu weryfikującego operacje bankowe / fraudy w ułamkach sekund? Z czego wolałbyś zrezygnować?**
**Odpowiedź:** 
Jeżeli SLA wymaga oceny rekordu transakcji w np. 25 milisekundach, wyklucza to totalnie koncepcje korzystające z chmurowego API opartego o generatywne LLMy z racji opóźnienia sieciowego RTT oraz specyfiki architektury generatywnej autoregresji samego modelu wielomiliardowego. Zmusza to do korzystania z wbudowanej tuż obok lekkiej heurystyki lub tradycyjnych metod ML (jak skompresowane i kwantyzowane struktury Drzew (XGBoost / LightGBM)). Zrezygnowałbym ze wspaniale wyedukowanego ogólnego intelektu maszyny i zdolności rozmowy na rzecz deterministycznego i morderczo precyzyjnego narzędzia zdolnego wykrywać skoki odchyleń wektorów powiązanych z transakcjami oszukańczymi np. analiza wariantywna ip, kwot i mac-adresów sprzętu.

**7. W jakich sytuacjach lepiej sprawdzi się tradycyjny system deterministyczny (rozbudowane wyrażenia regularne np. Regex / If-ologia) niż jakikolwiek model uczenia maszynowego lub sparametryzowany LLM?**
**Odpowiedź:** 
Przede wszystkim tam, gdzie obowiązuje "Zero Tolerance Policy" do jakichkolwiek barier logicznych pomyłek. 
- Parsowanie logów w locie w poszukiwaniu maskowania numeru NIP klienta przed zrzuceniem do hurtowni (kompresowanie problemu bezpieczeństwa pod probabilistyczny model LLM jest ekstremalnie groźne bo "może mu się akurat zapomnieć omaskować jednego NIPu").
- Klasyczne proste walidacje inputu ze stron i skanowanie przeciw prostemu wykluczeniu logicznemu słowami kluczowymi. 
- Logiki opierające się bezpośrednio o kalkulacje finansowe o wysokim rygorze zgodności księgowej (obliczanie rocznej marży, amortyzacji sprzętu IT bazujące bezpośrednio z dokumentu faktury). Tradycyjne metody matematyczne w Pythonie dają po rzutowaniu danych stałą gwarancję rezultatu.

**8. Jak rozwiązałbyś problem, kiedy przepisy prawne lub regulacje (np. GDPR, lub tzw. AI Act) bezwzględnie wymagają interpretowalności decyzji podejmowanych przez model (XAI - Explainable AI) przy jednoczesnym generowaniu wysokiego R.O.I przez głębokie sieci neuronowe dla tego samego zadania?**
**Odpowiedź:** 
Istnieją dwa potężne popularne podejścia na rozwiązanie takiego braku zaufania prawnego i zbalansowanie tej luki:
- Opracowywanie wnioskowań i opieranie uzasadnień sieci nakładając na nie techniki Post-Hoc z potężną metryką SHAP (SHapley Additive exPlanations) lub LIME. Taki algorytm oblicza, jak konkretnie dany ficzer wpłynął kierunkowo na decyzję uświadamiając audytorowi m.in dlaczego wyedukowana czarna skrzynka odrzuciła wniosek poślizgnięciem w wektorze braku zatrudnienia od X miesięcy.
- Trenowanie hybrydowe modeli na tzw "Teacher - Student distillation" albo proxy-models: trenujemy rewelacyjny "nieczytelny" model DL, po czym uczymy bardzo przejrzystą, interpretowalną metodę strukturalną (jak białe drzewo decyzyjne) symulować odruchy czarnej sieci i wdrażamy bezpieczny legalnie wariant uproszczony, potrafiący klarownie wyliczyć ścieżki przejścia wektorów w poszczególnych "gałęziach" decyzyjnych przed prawnikami.

**9. Na czym według Ciebie polega powszechnie występujący dzisiaj problem "overengineeringu" przy aplikowaniu LLMów i jakie może to nieść konsekwencje dla startupu będącego w początkowej fazie MVP z ograniczonym początkowym finansowaniem?**
**Odpowiedź:** 
"Overengineering" polega na próbach kompresowania całej architektury naokoło systemów RAG, rozbudowanych multi-agentowych środowisk orkiestrowanych w ciężkich abstrakcyjnych bibliotekach (jak Langchain/Llamaindex) z łączeniem się ze skomplikowanymi bazami wektorowymi tylko na zadania, które można by rozwiązać starą, dobrą wyszukiwarką ElasticSearch / OpenSearch wykorzystując tradycyjne wyszukiwanie ustrukturyzowane pełnotektstowe (BM25), oraz na ignorowaniu tradycyjnego Data Science na rzecz wciskanej do wszystkiego technologii GenAI kosztem sprawności i racjonalności. 
W startupach w powijakach na seedowej pętli finansowania, niesie to konsekwencje natury ogromnego spalania budżetu w API lub długiego długu technologicznego na powolne wdrożenie niedziałających rozwiązań. Utrzymanie takiej niepotrzebnie gigantycznej struktury (gdzie zamiast tego wystarczyła "IFologia") spowalnia weryfikację rynkowego pozycjonowania (Product Market Fit).

**10. Jak pogodzisz problem bardzo długiego okna kontekstowego (koszty za input toną w pieniądzach / uderzają w rate - limity API providera) w sytuacji, gdzie użytkownik wysyła sterty wielkich dokumentów, o które twój system RAG uderza non stop bez większej koncepcji? Wskaż alternatywne drogi rozwiązania takiego "wąskiego gardła".**
**Odpowiedź:** 
Zmniejszenie presji na okno powierzonego problemu to de facto sedno inżynierii RAG. Rozwiązałbym to po stronie operacji pobierania i strukturyzowania bez pompowania kontekstu i limitu rate modelów:
- Ulepszyłbym krok pretraning vector search wdrożeniem tzw **Re-rankingu (Cross-Encoderowania)** pozwalając obcinać podawaną pulę dla LLMa z "najlepszych 25 trafień z wektora wyszukiwania na pałę" do potężnie przefiltrowanych top 3 wyników idealnie dopasowanych pod promt szukającego, redukując koszt "inputowych tokenów" rdr by ułamek procentowy. 
- **Chunking z redukcją i podsumowywaniem:** Zamiast ładować gigantyczne całe fragmenty dokumentu, proces podczas embeddowania podsumowywałby za pomocą bardzo małego (szybkiego/taniego w API) modelu wielkie dokumenty na kluczowe wylistowane streszczenie w wektorach. Główny wielki potężny model nie musiałby przeglądać setek tysięcy wejściowych słów na darmo. 
- Filtry metadanych: Podkreślenie dodania do każdego fragmentu embeddingu sztywnych znaczników i wstępnej autoryzacji pytania poprzez prostą wytyczną `WHERE date="2023"` w bazie omijającą śmieciowe zanieczyszczanie okna starymi fakturami.
