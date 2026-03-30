# Repozytorium datasetów oraz wersjonowanie danych

## Krótkie podsumowanie
Repozytorium datasetów to scentralizowane środowisko służące do przechowywania, organizowania i udostępniania zbiorów danych na potrzeby projektów Machine Learning. Z kolei **wersjonowanie danych** to praktyka śledzenia i zarządzania zmianami w tych zbiorach na przestrzeni czasu — analogicznie do tego, jak systemy kontroli wersji (np. Git) zarządzają zmianami w kodzie źródłowym.

## Dlaczego ma to znaczenie i gdzie znajduje zastosowanie
- **Identyczność i Powtarzalność (Reproducibility):** Jakość rozwiązań ML w równym stopniu zależy od kodu, co od użytych danych. Śledzenie wersji danych pozwala na precyzyjne odtworzenie historycznego eksperymentu w przypadku, gdy chcemy przeprowadzić audyt lub ponowny trening.
- **Audytowalność i Compliance:** W branżach regulowanych (np. finanse, medycyna) wymagana jest zdolność do udowodnienia pochodzenia danych (Data Lineage) oraz wskazania, na bazie jakich dokładnie informacji podejmowane były określone decyzje modelu.
- **Ochrona przed psuciem danych:** Odporność na błędy lub np. Data Poisoning. Jeśli nowa zaktualizowana paczka danych będzie zabrudzona i uszkodzi proces szkoleniowy, odpowiednie narzędzia pozwolą błyskawicznie cofnąć zbiór do poprzedniego, "czystego" stanu.
- **Skalowalna współpraca:** Ułatwia inżynierom równoległą pracę oraz bezpieczne testowanie odrębnych koncepcji bez obaw nadpisywania sobie nawzajem postępów na współdzielonym klastrze zasobów.

## Jak to działa w praktyce
Narzędzia używane w tym obszarze charakteryzują się konkretną separacją plików oraz metadanych:
1. **Podejście rozszerzające Gita (DVC - Data Version Control):**
   Główny problem klasycznego Gita polega na jego ułomności w konfrontacji z setkami gigabajtów danych. DVC traktuje Git jako "mózg" śledzący małe pliki typu `.dvc` (z haszami identyfikującymi daną wersję pliku danych), a potężne, setkach iteracji mierzone zbiory trzymane są na odpowiednim obiektywnym storage'u (Azure Blob, AWS S3, local storage).
2. **Platformy MLOps i Rejestry Artefaktów (W&B Artifacts, MLFlow):**
   Platformy służące do śledzenia eksperymentów mają wyspecjalizowane sekcje tzw. Artefaktów. Razem z wrzucanymi parametrami wrzucana jest (lub jej hash) instancja danych użytych w sesji, dzięki czemu klikając w model `ResNet_v2` od razu widzisz z jakich danych na wejściu on skorzystał.
3. **Data Lake i Hurtownie – "Time Travel" (np. Delta Lake, Apache Iceberg):**
   Środowiska oparte o logi transakcyjne potrafią zapytać silnik typu Spark o odfiltrowanie danych z konkretnego "snapshota", np. `SELECT * FROM table TIMESTAMP AS OF '2023-11-01'`.

**Uproszczony przykład workflow u użyciem DVC:**
```bash
# Zamiast normalnego 'git add dataset.csv', używasz dvc by przenieść uciążliwy ciężar ze zwykłego repo
dvc add data/wielki_dataset.csv

# Powstaje mały plik instrukcyjny np. data/wielki_dataset.csv.dvc
# To on w rzeczywistości zostaje dodany do repozytorium GitHub / GitLab:
git add data/wielki_dataset.csv.dvc
git commit -m "Aktualizacja treningowego datasetu do v3"

# Fizyczny i wielki wagowo uścisk następuje pomiędzy DVC a podpiętą chmurą:
dvc push
```

## Lista pytań (Job Interview)

**1. Dlaczego powszechnie lubiany i standardowy protokół Git nie jest optymalnym i skalowalnym rozwiązaniem do wersjonowania ogromnych wolumenów surowych danych treningowych?**

Git przechowuje w swoim wewnętrznym repozytorium (katalogu `.git`) pełną historię każdego pliku jako kolejne snapshoty i delty zmian. To sprawdza się doskonale dla plików tekstowych (kodu), gdzie zmiany są małe i rzadkie. Problem pojawia się przy danych:
- **Rozmiar:** Dodanie pliku 50 GB do `git add` powoduje, że jego pełna kopia ląduje w katalogu `.git/objects`. Przy każdej kolejnej wersji (nawet z małą zmianą) Git przechowuje całą nową kopię, co powoduje eksplozję rozmiaru lokalnego repozytorium.
- **Wydajność:** Klonowanie, fetch i push całej historii danych zajmuje godziny i wymaga ogromnej przepustowości sieci.
- **Ograniczenia platform:** GitHub/GitLab narzucają limity na rozmiar pliku (np. 100 MB na GitHub) i całego repozytorium, co czyni je bezużytecznymi jako storage dla surowych danych ML.
- **Brak semantyki danych:** Git nie rozumie formatów Parquet, CSV czy obrazów — nie może np. pokazać diffa między dwiema wersjami datasetu w sensowny sposób.

Dlatego właśnie narzędzia jak DVC oddzielają metadane (małe pliki `.dvc` z hashami) śledzone przez Gita od fizycznych danych trzymanych na zewnętrznym storage (S3, Azure Blob, GCS).

---

**2. Wyjaśnij na jakiej zasadzie współdziałają ze sobą Git oraz DVC w procesie MLOps. Które elementy trafiają gdzie?**

Współpraca opiera się na zasadzie **podziału odpowiedzialności**:

| Co | Gdzie trafia | Za pomocą |
|---|---|---|
| Kod, konfiguracje, skrypty pipeline'ów | Repozytorium Git (GitHub/GitLab) | `git add`, `git commit` |
| Pliki `.dvc` (małe pliki z hashami danych) | Repozytorium Git | `git add *.dvc`, `git commit` |
| Fizyczne dane (CSV, Parquet, obrazy, modele) | Zewnętrzny storage (S3, Azure Blob, GDrive) | `dvc push` / `dvc pull` |

W praktyce: `dvc add data/dataset.csv` tworzy plik `data/dataset.csv.dvc` zawierający hash MD5 pliku danych oraz metadane. Ten mały plik `.dvc` jest commitowany do Gita, stając się „wskaźnikiem" do konkretnej wersji danych. `dvc push` wysyła fizyczny plik na storage. Dzięki temu `git checkout` na starszym commicie + `dvc pull` precyzyjnie odtwarza historyczny stan danych.

---

**3. Czym w strukturze przepływu produkcyjnego jest "Data Lineage"? Jakie problemy biznesowe pomaga to rozwiązać?**

**Data Lineage** (rodowód danych) to zdolność do prześledzenia całej drogi, jaką przechodzą dane: od źródła ich pochodzenia (np. bazy transakcyjnej, API zewnętrznego), przez kolejne transformacje (czyszczenie, agregacje, feature engineering), aż do finalnego artefaktu, którym może być wytrenowany model lub raport.

Pierwotnie rozwiązuje następujące problemy biznesowe:
- **Compliance i regulacje:** W sektorze finansowym (MiFID II) czy medycznym (HIPAA/RODO) audytorzy mogą wymagać udowodnienia, skąd pochodziły dane użyte do podjęcia konkretnej decyzji przez model — np. przy odmowie udzielenia kredytu. Bez Data Lineage jest to niemożliwe.
- **Debugowanie błędów:** Gdy model zaczyna dawać błędne wyniki, Data Lineage pozwala szybko wskazać, na którym etapie transformacji pojawiła się usterka lub "zatrucie" danych.
- **Impact analysis:** Zmiana w schemacie tabeli źródłowej może kaskadowo wpłynąć na dziesiątki downstream pipeline'ów. Lineage pozwala z wyprzedzeniem ocenić zakres takiej zmiany.

---

**4. Co masz na myśli mówiąc o pojęciu "Time Travel" w ujęciu formatów przechowywania dużych danych, takich jak Delta Lake lub Apache Iceberg?**

**Time Travel** to funkcjonalność formatów tabelarycznych opartych na **logach transakcyjnych** (transaction log / snapshot log), która pozwala odpytywać dane w stanie, w jakim znajdowały się w konkretnym momencie w przeszłości — bez konieczności przechowywania ręcznych kopii.

Mechanizm działania (na przykładzie Delta Lake):
- Każda operacja zapisu (INSERT, UPDATE, DELETE) jest zapisywana jako nowy wpis w logu transakcyjnym (`_delta_log/`).
- Dane fizyczne (pliki Parquet) nie są nadpisywane — nowe wersje danych są dopisywane jako nowe pliki.
- Silnik (Spark, Trino) może odczytać log i zrekonstruować stan tabeli dla dowolnego punktu w czasie.

Przykłady użycia:
```sql
-- Dane sprzed konkretnej daty
SELECT * FROM tabela TIMESTAMP AS OF '2023-11-01';

-- Dane z konkretnej wersji snapshot
SELECT * FROM tabela VERSION AS OF 42;
```

W kontekście ML jest to niezwykle przydatne do odtwarzania dokładnie tego datasetu, który był użyty do treningu modelu w danym momencie — bez ręcznych archiwów.

---

**5. Twoja aplikacja z nowym modelem przeszła testy integracyjne, jednak na produkcji obserwujemy zauważalne pogarszanie się (drift) dokładności. Na jaki sposób kontrola wersji danych ułatwi analizę tej awarii?**

Kontrolę wersji danych można wykorzystać w tej sytuacji w kilku krokach:
1. **Identyfikacja wersji danych treningowych:** Dzięki powiązaniu modelu z konkretnym hashem datasetu (np. przez DVC lub W&B Artifacts), wiem dokładnie, na jakich danych model był trenowany.
2. **Porównanie z danymi produkcyjnymi:** Mogę zestawić rozkłady statystyczne (średnia, odchylenie, proporcje klas) historycznej wersji treningowej z bieżącymi danymi wejściowymi. To pozwoli wykryć **data drift** — zmianę rozkładu cech.
3. **Analiza zmian w pipeline'ie danych:** Historia commitów DVC/Git pozwala zobaczyć, czy między treningiem poprzedniego a nowego modelu zmieniły się filtry, transformacje lub źródła danych (np. zmiana dostawcy danych, nowy format kolumny).
4. **Szybki rollback:** Jeśli drift wynika z "zabrudzenia" nowych danych (np. błąd w ETL), wersjonowanie pozwala natychmiast cofnąć pipeline do ostatniej sprawdzonej wersji datasetu i wznowić trening.
5. **Retrain na historycznych danych:** Można dokładnie odtworzyć środowisko z momentu treningu starego, działającego modelu — ten sam kod + ta sama wersja danych — by zweryfikować, czy problem leży w danych czy w architekturze.

---

**6. Rozwijasz system w 5-osobowym zespole Data Science. Twoi współpracownicy, tworząc paczki danych, regularnie polegają na konwencji nazewnictwa typu `dataset_ostateczny`, `dataset_ostateczny_v2_naprawiony.csv`. Opisz konsekwencje jakie to niesie i jak wersjonowanie ich rozwiązuje.**

Konsekwencje konwencji nazewnictwa ręcznego:
- **Brak jednoznaczności:** Nikt nie wie, która wersja jest "naprawdę ostateczna". Po tygodniu zespół ma 6 plików z podobnymi nazwami i nikt nie pamięta różnic.
- **Brak historii zmian:** Nie wiadomo, co konkretnie zmieniło się między `v1` a `v2_naprawiony` — brak diffów, opisów, autorstwa.
- **Problem współpracy:** Dwie osoby mogą jednocześnie produkować swoje "ostateczne" wersje, nadpisując wspólny zasób lub tworząc dywergencję.
- **Brak powiązania z modelem:** Nie wiadomo, który model był trenowany na której wersji pliku. Audyt jest niemożliwy.
- **Błędy ludzkie:** Literówka w nazwie, zapis w złym folderze, przypadkowe nadpisanie — to wszystko prowadzi do utraty danych.

Jak wersjonowanie rozwiązuje te problemy:
- Każda zmiana datasetu jest commitowana z opisowym komunikatem (`git commit -m "Usunięto duplikaty z kolumny customer_id"`), tworząc niezmienną historię.
- DVC/W&B Artifacts przypisuje unikalny hash do każdej wersji — nie można pomylić wersji pliku.
- Eksperymenty w MLflow lub W&B automatycznie zapisują, który hash datasetu został użyty, co tworzy trwałe powiązanie model–dane.
- Praca zespołowa odbywa się na branchach — każdy testuje własną wersję danych bez ryzyka nadpisania wspólnego zasobu.

---

**7. Opowiedz w jaki sposób utrzymałbyś bezkolizyjne i jednoczesne linkowanie dwóch różnych wersji jednego konkretnego modelu uczenia maszynowego do precyzyjnych i właściwych paczek danych dla nich z osobna?**

Rozwiązanie opiera się na **niezmiennych, unikalnych identyfikatorach** (hashach) po obu stronach — dla modelu i dla danych. Przykładowe podejście z wykorzystaniem W&B Artifacts lub MLflow:

1. **Rejestr modeli z metadanymi datasetu:** Każdy run treningowy rejestruje model wraz z artefaktem danych (lub jego hashem) jako parametr:
   ```python
   # W&B
   run.log_artifact(dataset_artifact)  # linkuje dataset v1 do tego runu
   run.log_artifact(model_artifact)    # rejestruje model
   ```
   Wówczas model `ResNet_v2` ma w swoich metadanych jawne odwołanie do `dataset:v1`, a model `ResNet_v3` do `dataset:v2`.

2. **DVC + Git branches/tags:** Każdy model-branch ma własny plik `.dvc` wskazujący na odpowiednią wersję danych:
   ```
   branch: experiment/resnet-v2  →  data/train.csv.dvc (hash: abc123)
   branch: experiment/resnet-v3  →  data/train.csv.dvc (hash: def456)
   ```
   `dvc pull` na danym branchu pobierze zawsze właściwy zestaw danych.

3. **Delta Lake / Iceberg z Time Travel:** Zamiast plików, można linkować modele do konkretnej wersji snapshot tabeli, np. `VERSION AS OF 42` — ta wersja jest immutowalna i niezależna od kolejnych zmian w tabeli.

Efekt: dwa modele działają równolegle, każdy jednoznacznie "wie", na jakich danych był trenowany, a przywrócenie pełnego środowiska dla każdego z nich jest operacją deterministyczną.

## Powiązane pliki z repozytorium
- [[budowa-pipeline-danych-i-praca-w-skali-produkcyjnej]]
