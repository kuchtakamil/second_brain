# Automatyzacja wdrożeń modeli LLM (LLMOps)

## 1. Omówienie zagadnienia

Automatyzacja wdrożeń modeli Large Language Models (LLM) jest kluczowym, ale wysoce skomplikowanym obszarem tzw. LLMOps (Machine Learning Operations dla zastosowań Generative AI). Ze względu na ogromne rozmiary modeli, specjalistyczne środowiska uruchomieniowe (GPU/TPU) oraz unikalną charakterystykę generowania tekstu (np. strumieniowanie tokenów), tradycyjne podejścia CI/CD i MLOps muszą zostać znacząco zaadaptowane.

### Kluczowe elementy automatyzacji i wdrożeń (LLMOps):

*   **Podejście do infrastruktury i serwowania (Serving Engines):**
    *   Bezpośrednie wystawianie modeli przez proste API (np. Flask/FastAPI) jest nieefektywne. W produkcyjnych i zautomatyzowanych wdrożeniach stosuje się dedykowane silniki inferencyjne: **vLLM**, **TGI** (Text Generation Inference od Hugging Face), **NVIDIA Triton Inference Server** czy **LMDeploy**.
    *   Te silniki dostarczają kluczowe optymalizacje: *Continuous Batching*, *PagedAttention*, a także wbudowane wsparcie dla modeli skwantyzowanych (AWQ, GPTQ).
*   **Wersjonowanie i rejestry modeli (Model Registry):**
    *   Konieczne jest dokładne wersjonowanie zarówno kodu inferencyjnego, promptów bazowych, jak i samych wielogigabajtowych plików z wagami (zazwyczaj format `.safetensors`).
    *   Narzędzia takie jak **MLflow**, **Weights & Biases**, czy dedykowane repozytoria (Hugging Face Hub prywatny, chmurowe rejestry w AWS/GCP/Azure) stają się źródłem prawdy (Source of Truth) dla systemów CI/CD.
*   **CI/CD i Orkiestracja MLOps:**
    *   Kluczem jest automatyzacja potoków: **CT (Continuous Training)** -> **CI (Continuous Integration)** -> **CD (Continuous Deployment)**.
    *   Pipeline (np. w Airflow, Kubeflow, GitHub Actions, GitLab CI) może automatycznie uruchamiać douczanie (np. adapterów LoRA o zdefiniowanym interwale lub po zebraniu danych z feedbacku), oceniać nowy model (często zjawiskiem *LLM-as-a-judge*) i – jeśli nowy wariant przewyższa aktualny – wypychać model do odpowiednich klastrów.
*   **Konteneryzacja, Kubernetes (K8s) i strategie wdrażania:**
    *   Modele są niemal zawsze konteneryzowane.
    *   Mnożą się wyzwania związane ze strategiami deploymentu: **Blue/Green** (bardzo drogie sprzętowo z powodu dublowania VRAM), **Canary Deployments** lub **Shadow Deployments**. Używa się narzędzi takich jak KServe, Seldon czy Ray Serve do orkiestracji modeli na K8s.
*   **Optymalizacja rozmiaru i prędkości w locie:**
    *   Zautomatyzowane pipeline'y często wykonują krok optymalizacji bazowych zagadnień: kwantyzację z oryginalnej precyzji (np. bfloat16 do INT8 lub INT4), co po stronie wdrożenia drastycznie redukuje wymóg na VRAM oraz koszty compute'u.
*   **Observability (Monitorowanie LLM na produkcji):**
    *   Automatyzacja kończy się na monitorowaniu i auto-rollbackach.
    *   Trzeba śledzić unikalne metryki infrastrukturalne: **TTFT** (Time To First Token), **TPOT** (Time Per Output Token), zajętość GPU, a także metryki jakościowe: dryft modelu i promptów, obecność halucynacji czy toksyczności (np. narzędzia LangSmith, Phoenix od Arize AI).

---

## 2. Pytania na rozmowę rekrutacyjną i odpowiedzi

### Pytanie 1: Czym różni się wdrożenie i utrzymanie na produkcji LLM-a od klasycznego modelu Machine Learning (np. Random Forest czy XGBoost)?
**Odpowiedź:**
Główną różnicą są **wymagania sprzętowe i wielkość modeli**. Klasyczny model waży często kilkadziesiąt megabajtów (uruchamiany na zwykłym CPU). LLM waży dziesiątki/setki gigabajtów (wymaga drogich i trudno dostępnych GPU np. A100/H100 z odpowiednią przepustowością pamięci).
Drugą kwestią jest **natura inferencji**. Klasyczne modele zwracają wynik (skalar/wektor) asynchronicznie, w bardzo krótkim czasie. LLM-y generują wyjście sekwencyjnie (token po tokenie), co wymaga zarządzania strumieniami pamięci oraz rozróżnienia na fazę *prefill* promptu od fazy *decode* znaków.
Trzecią rzeczą są **metryki**. W tradycyjnym ML mierzymy po prostu latencję zapytań i przepustowość. W LLM musimy mierzyć latencję do pierwszego tokena (TTFT) – krytyczne dla User Experience – oraz czas generowania pojedynczego tokena (TPOT). Złożone jest też monitorowanie wyjścia, m.in. zjawisk detekcji halucynacji.

### Pytanie 2: Do czego służą takie rozwiązania jak vLLM lub TGI (Text Generation Inference) i dlaczego nie użyć po prostu czystego modelu (Pipeline z biblioteki transformers) opakowanego w we Flask/FastAPI?
**Odpowiedź:**
Umieszczenie modelu prosto we webowym frameworku działa sprawnie tyko w systemach Proof of Concept dla pojedynczych zapytań naraz (batch 1).
Kiedy model ulega deploymentowi na serwer pod duży ruch produkcyjny, używa się vLLM lub TGI, ponieważ posiadają one wbudowane rozwiązania jak **Continuous Batching (Dynamic Batching)** czy techniki alokacji bliskie systemom operacyjnym jak **PagedAttention**. 
Zwykłe API czekałoby, aż proces wygeneruje całą sekcję wyników wszystkich sekwencji w batczu GPU. Continuous Batching wyciąga z GPU i wysyła do klienta wynik generacji każdego pojedynczego promptu (najkrótszego) tuż po tym jak natrafi on na token EOF. Puste "slociki" na karcie od razu zastępowane są nowymi zapytaniami z kolejki, podnosząc nawet 10-20 krotnie throughput serwera LLM.

### Pytanie 3: Jak zaimplementował(a)byś Continuous Deployment dla zmian modelu językowego na produkcji, chroniąc system przed całkowitą wpadką, gdyby wprowadzony model po tuningu był niedokładny lub za bardzo zjadał VRAM?
**Odpowiedź:**
Najbezpieczniejszym z punktu widzenia biznesu mechanizmem do zarządzania dużymi modelami jest zastosowanie **Canary Deployment** z proxy (np. przez routery Envoy/Istio).
Kroki CI/CD:
1. Skompilowany i zoptymalizowany kwantyzacją nowy model ląduje obok bieżącej produkcji na Kubernetes. Będzie przyjmował 5% losowego ruchu klientów.
2. Monitorowanie śledzi logi nowego wariantu OOM (Out Of VRAM memory error), opóźnieniowe i ewentualnie odrzucanie zapytania.
3. Jeśli alert Grafana/Prometheus po pierwszych kilkunastu minutach pokaże masowe halucynacje z LLM AS a Judge metric albo error-rate poszybuje do nieba to narzędzie GitOps w ciągu sekund robi rollback routingu w 100% z powrotem na starą stabilną wersję produkcyjną. Jeśli wskaźniki u nowego LLM-a są wyższe i dobre, deployment stopniowo i bezawaryjnie zwiększa nań wolumen żądań do 100%.
(Należy pamiętać, że podwójne równoległe Blue/Green bywa uciążliwe ze względu na horrendalne koszty chmurowych GPU utrzymywanych obok siebie do momentu ukończonego przełączenia).

### Pytanie 4: Środowisko K8s obsługujące duże chatboty napotyka w nocy zerowy ruch a w ciągu dnia nagłe skoki (Spikes Request). Jak zoptymalizujesz koszty takiej instalacji chmurowej?
**Odpowiedź:**
Należy skonfigurować tzw. autoskalowanie dynamiczne – czyli dynamiczne dobieranie Node-ów GPU w miarę aktualnego lub wręcz zaplanowanego (prze-konfigurowanego po godzinach) zapotrzebowania.
Ale uwaga, auto-scalling HPA po wektorach limitów CPU lub pamięci w K8S się nie nadaje, bo model vLLM potrafi często zużywać 100% zablokowanego VRAMu do cache'owania w KV Cache niezależnie czy przychodzą zapytania.
Użyłbym Event-driven skalowania np. przy użyciu **KEDA** (Kubernetes Event-driven Autoscaling).
Metryką do skalowania byłoby tu **Pending Requests in Queue** samego serwera modelu językowego. Kiedy kolejka gwałtownie rośnie i przekracza np. 10 nieobsłużonych próśb o tokeny – natychmiast KEDA wystawia i stawia od nowa z obrazu (tzw. Cold Start) dedykowane następne GPU. Gdy kolejka wraca do 0 używamy funkcji tzw. **Scale to Zero**, aby zredukować wyceny AWS za potężne maszyny obliczeniowe generujących bezruchem straty w nocy.

### Pytanie 5: Czym jest LoRAX lub tzw. Multi-LoRA Serving i jakie obciążenia architektoniczne LLMOps redukuje?
**Odpowiedź:**
Podejście takie odpowiada na wyzwanie wielodostępnych produktów SaaS (np. aplikacji CRM lub firmowej, dla której tworzymy po każdym nowym użytkowniku spersonalizowaną instancję dla każdego z 300 jej biznesowych B2B partnerów za pomocą trenowanego Fine Tuningu / LoRA. Czysty instancjowanie 300 różnych LLMów i dedykowanego VRAMu po kilkadziesiąt Gigabajtów to nieopisywalne straty i bankructwo MLOps.
Silniki wyposażone w mechanikę Multi-LoRA Serving (np. LoRAX od Predibase lub natywna funkcja serwera vLLM / S-LoRA) ładują w warstwie produkcyjnej **jeden jedyny wyjściowy ("gruby") model LLM we wspólnej pamięci GPU**. Gdy na API wpadnie request dla firmy "A", do karty wysyłanych z dysku lub RAM szybciej (doraźnie na warstwy tego samego podbudowanego modelu w locie) są wgrywane oparte o małe paczuszki (ważące np.100 MB w rank=8) adaptacyjne wagi różniczkowe. W tym samym wektorze Requestu 2 używa innej wagi w locie. Obsługa tysięcy instancji na jednym GPU to miliony zaoszczędzonych w DevOps kosztów.

### Pytanie 6: Jak wyglądałby Twój kompletny pipeline automatyzujący Continuous Training (re-training LLMa) oparty na bazie logów wsparcia IT pobieranych codziennie?
**Odpowiedź:**
Przykładowy potok wykorzystujący Airflow, MLFlow i CI/CD:
1. **Pobieranie i Czyszczenie (Ingestion Task):** Potok budzi się sam codziennie w nocy. Podpina się poprzez pipeline Sparkowy bądź dBT DBt / Snowflake Data do bazy gdzie trzymane są wyexportowane wysoko-oceniane chato-pary QA z Userami i aplikuje za darmo maskowanie i usuwanie brzydkiego słownictwa (PII redacting). 
2. **LoRA Fine-tuning Task:** Po przygotowaniu zbioru JSONL, Airflow wykonuje np. Ray Task albo dedykowany Batchjob na AWS Sagemaker tworzącego mały uaktualniony adepter PEFT. 
3. **Automated Evaluation / LLM As A JUDGE (Bardzo ważne w AI):** Nie wdrażamy po ślepu. Job połączony z CI uruchamia asynchroniczny potok w środowisku TEsting wzywającego najtęższy LLM z rynku (np. GPT-4, albo darmowy przodownik Open-Source Mixtral), aby ocenił model "świeży" kontra model przed-wczorajszy poprzez scoring (jako sędzia obiektywny) ze standardowego Benchmarking testu. Dwa modele są porównywane np. prompcikami i metryką dokładności ROUGE/BLEU.
4. **Rozprowadzanie (Deployment pipeline):** Skoro nowy adapter (uznajmy że w rejestrze MLFlow) zatwierdził metryki sukcesu jako o 3% polepszające stosunek wobec starszego modelu bota IT – model zostaje otagowany stanem STAGING -> PRODUCTION. Pipeline CI (np. GitLab runners) automatycznie wgrywa go na Helm/K8s do zasobów gdzie stery i podmiany ruchu za chwile poweźmie chociażby wtyczka ArgoCD załatwiona na Canary Deploymentzie.
5. Zamknięcie statusów na Slacku informuje o powodzeniu działania całego nocnego CT/CD.

### Pytanie 7: Klient mówi: "Czas serwowania pierwszego tokenu przez naszego chatbota produkcyjnego nagle w pośpiechu wystrzelił i trwa nieakceptowalne 9 sekund". Podziel się tokowaniem procesu dedukcyjnego LLMOps poszukania powodu awarii.
**Odpowiedź:**
Krótki strumień dedukcji opierający się na standardach Observability modelami:
1. Analizuje Grafane metryką TTFT (*Time To First Token*). Zjawisko nagłego wydłużenia często omija fazę dekompozycji modeli, leżąc bezpośrednio poprzez potężny obciążony *prefill time*. 
2. Sprawdzam, czy po niedawnym wdrożeniu API nie pozwoliliśmy Użytkownikom wrzucać zbyt monstrualnie dużych dokumentów w Kontekst w ramach (np. RAG workflowa!). Przetworzenie całego wielkiego napływu na raz w bloku zapytania uniemożliwia GPU procesowanie innych zapytań przez tzw Context Window, a w rezultacie serwer poddaje się czkajacymi przerwami. Problem nie jest modelem tylko za dużą dawkę wiedzy po API.
3. Obserwuję długość oczekujące kolejki. Jeżeli skok RPS (Requests Per Second) wystrzelił lawinę wejść i spalił całe wolne dedykowane dla serwera pojemności GPU to w rezultacie, zgłaszanie TTFT się na nim pogrąża dopóki nie skończy dotychczasowych.
4. Jeżeli błędy skoczyły OOM (brak VRAM w logach Podów w Kubernetesie) – oznacza to, że alokujący KV-Cache pamięci na starym modelu wyciekł u wdrożeniowca, zapomniał zmniejszyć max-limit okna do odpowiedniej ilości wielkości procentowych parametru `gpu-memory-utilization=0.9` co doprowadza w rezygnacji GPU alokującego tokenu. Wszyscy Userzy stoją zawieszeni. Szybki rollback poprawka to restart pody i usztywnienie na stabilny limit.
