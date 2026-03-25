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
*Odpowiedzi, zgodnie z życzeniem, pozostały niewypełnione – do zastanowienia samemu.*

1. Dlaczego powszechnie lubiany i standardowy protokół Git nie jest optymalnym i skalowalnym rozwiązaniem do wersjonowania ogromnych wolumenów surowych danych treningowych?
2. Wyjaśnij na jakiej zasadzie współdziałają ze sobą Git oraz DVC w procesie MLOps. Które elementy trafiają gdzie?
3. Czym w strukturze przepływu produkcyjnego jest "Data Lineage"? Jakie problemy biznesowe pomaga to rozwiązać?
4. Co masz na myśli mówiąc o pojęciu "Time Travel" w ujęciu formatów przechowywania dużych danych, takich jak Delta Lake lub Apache Iceberg?
5. Twoja aplikacja z nowym modelem przeszła testy integracyjne, jednak na produkcji obserwujemy zauważalne pogarszanie się (drift) dokładności. Na jaki sposób kontrola wersji danych ułatwi analizę tej awarii?
6. Rozwijasz system w 5-osobowym zespole Data Science. Twoi współpracownicy, tworząc paczki danych, regularnie polegają na konwencji nazewnictwa typu `dataset_ostateczny`, `dataset_ostateczny_v2_naprawiony.csv`. Opisz konsekwencje jakie to niesie i jak wersjonowanie ich rozwiązuje.
7. Opowiedz w jaki sposób utrzymałbyś bezkolizyjne i jednoczesne linkowanie dwóch różnych wersji jednego konkretnego modelu uczenia maszynowego do precyzyjnych i właściwych paczek danych dla nich z osobna?

## Powiązane pliki z repozytorium
- [[budowa-pipeline-danych-i-praca-w-skali-produkcyjnej]]
