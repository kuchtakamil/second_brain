# MLflow (Machine Learning Operations)

## 1. Omówienie zagadnienia

**MLflow** to platforma open-source zaprojektowana do kompleksowego zarządzania cyklem życia projektów z zakresu uczenia maszynowego (ML lifecycle). Pozwala zespołom Data Science, ML/AI Engineering i MLOps na standaryzację procesów trenowania, śledzenia wskaźników eksperymentów, wersjonowania, wdrażania modeli i zarządzania ich konfiguracjami. 

### Dlaczego to jest ważne i kiedy ma zastosowanie?
W przeciwieństwie do tradycyjnej inżynierii oprogramowania (gdzie wersjonujemy głównie kod), w inżynierii uczenia maszynowego wynik procesu zależy od **kodu**, użytych **hiperparametrów** oraz **danych**. Bez narzędzia takiego jak MLflow trudno jest udzielić obiektywnej odpowiedzi na proste pytania: "Który konkretnie kod z jakim zestawem danych dał wynik 96% trafności zeszłego wtorku?" czy "Jaki dokładny ciąg wag jest uruchomiony na dzisiejszej produkcji?".

Główne obszary, gdzie MLflow ma zastosowanie, pokrywają się z wbudowanymi modułami platformy:
*   **MLflow Tracking:** Rejestrowanie hiperparametrów algorytmu, logowanie metryk wydajności i generowanie "artefaktów" (np. plików ze zserializowanym modelem, wykresów ewaluacji, krzywej strat). Umożliwia porównywanie poszczególnych uruchomień (Runs) wizualnie i w formie tabel.
*   **MLflow Projects:** Pakowanie projektów Data Science w zestandaryzowany, powtarzalny format ze zdefiniowanymi środowiskami (np. pliki konfiguracyjne conda, obrazy Docker), gwarantujący reprodukowalność modelu w dowolnej infrastrukturze.
*   **MLflow Models:** Pakowalny, jednorodny i otwarty system udostępniania zapisanych modeli w chmurach i urządzeniach (tzw. "MLmodel" flavour) - dzięki ujednolicaniu interfejsów MLflow bez problemu uruchomi za pomocą jednej funkcji `predict()` modele stworzone w TensorFlow, PyTorch, czy XGBoost, redukując dług wdrożeniowy.
*   **MLflow Model Registry:** Scentralizowany rejestr modeli współpracujący z Tracking Serverem. Śledzi on cały cykl życia operacyjnej strony modelu (nadawanie statusów takich jak *Staging*, *Production* czy *Archived*) oraz zarządzanie historycznymi wersjami wag we wdrożeniu.

MLflow mocno rozwija się również w sferze LLMOps we współczesnych architekturach GenAI, poszerzając swój wachlarz o natywne śledzenie promptów chociażby we frameworkach LangChain czy LlamaIndex, a także o metryki sprawdzające jakość generacji tekstowej (MLflow Evaluate i podejście LLM-as-a-judge).

### Jak to działa? (Przykłady)
MLflow zazwyczaj funkcjonuje na dwóch płaszczyznach - lokalnej w formie lekkiej usługi deweloperskiej na środowisku uczącym się, oraz produkcyjnej opartej na zewnętrznej architekturze z wydzielonym **Tracking Serwerem** (na maszynie obliczeniowej), łączącym się ze zde-duplikowaną strukturą bazy SQL (Repository PostgreSQL dla metryk/konfiguracji) i chmurowym środowiskiem obiektowym (np. AWS S3 / Azure Blob Storage dla wgrania wielogigabajtowych plików modelu jako "artefakty").

Przykład integracji śledzenia modelu ML (Python):

```python
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

# 1. Połączenie i wystartowanie rejestracji operacji logujących
mlflow.set_tracking_uri("http://moj-serwer-mlflow.com:5000")
mlflow.set_experiment("Prognoza_Sprzedazy")

with mlflow.start_run():
    # 2. Definiowanie parametrów i automatyczne logowanie
    params = {"n_estimators": 100, "max_depth": 5}
    mlflow.log_params(params)

    # 3. Klasyczne trenowanie 
    rf = RandomForestRegressor(**params)
    rf.fit(X_train, y_train)
    
    # 4. Inferencja z zestawu ewaluacji
    predictions = rf.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    
    # 5. Logowanie wyciągniętych dla modelu metryk
    mlflow.log_metric("mse", mse)

    # 6. Serializacja gotowego do wykorzystania modelu na chmurę S3
    mlflow.sklearn.log_model(rf, "random-forest-model")
```

---

## 2. Dyskusja na interwiev

Podczas rekrutacji (na role typu MLOps Engineer, Machine Learning Engineer lub Data Scientist) wiedza o MLflow niemal zawsze powraca przy pytaniach sprawdzających dojrzałość inżynieryjną, która musi stanowić wyższy poziom operacyjny u osoby zatrudnionej ponad samo projektowanie eksperymentów "na laptopie" czy "lokalnym notebook'u". Omawiając ten temat z rekruterem, warto z pewnością:
*   Wypozycjonować MLflow jako fundament automatyzacji i **Pojedyncze Źródło Prawdy** (Source of Truth) dla modelu we wskazanym procesie MLOps.
*   Przywołać pojęcia rozdzielenia cyklu ewaluacyjnych eksperymentów na modelach od samego cyklu serwowania i testowania w produkcyjnym otoczeniu, do czego powołany jest właśnie system **Model Registry**.
*   Wykazać się znajomością i uwydatnić świadomość Back-Endu technologicznego - faktu, że serwer MLflow wymaga potężnej bazy np. S3 do trzymania plików z wagami `.bin/.safetensors`.
*   Rozróżnić możliwości MLflow w zderzeniu z konkurencją - taką jak chociażby usługa Weights & Biases (które jest liderem w śledzeniu potężnych sieci głębokich DL/GenAI, ale nie posiada tak uniwersalnego rozwiązania jako open-source). Ważnym podkreśleniem jest integracja narzędzia z potęgą klastrów Databricks, gdzie z reguły system występuje natywnie podpięty dla kont Data Scientistów.
*   Wskazać świadomość innowacyjnych prądów LLMOps – że MLflow od ostatnich wersji posiada integracje m.in do platform LangChain potrafiące zapisywać ślady wywołań poszczególnych "Agentów", systemów podpięć pod wektorowe Retrieval-Augmented Generation (RAG) raz z całą drogą wejść i odpowiedzi modelu.

---

## 3. Pytania na rozmowę rekrutacyjną (bez odpowiedzi)

### Pytanie 1: Czym zajmują się i do czego dokładnie służą poszczególne z czterech głównych komponentów MLflow (Tracking, Projects, Models, Model Registry)?
### Pytanie 2: Jak zintegrował(a)byś mechanizmy Model Registry z potokami CI/CD w procesie automatycznego ciągłego wdrażania i ewaluacji modelu (np. CT/CD pipelines w GitLab CI)?
### Pytanie 3: Załóżmy, że większość badaczy Data Science preferuje Weights & Biases (W&B) podczas iteracji szkoleniowych sieci neuronowej. Zespół MLOps preferuje jednak wdrożenia infrastrukturalne oparte o Model Registry w MLflow. W jakim układzie i integracji obronił(a)byś zastosowanie tych dwóch systemów?
### Pytanie 4: Jaka jest fundamentalna struktura wielowarstwowej architektury po stronie Back-End na komercyjnej produkcji opierającej usługę MLflow? W jakich bazach trzymał(a)byś odpowiednie ślady eksperymentów i dlaczego tak ważna jest chmura obiektowa klasy S3/Blob?
### Pytanie 5: Czym odróżnia się operacyjna definicja "Run" (Eksperyment, pojedyncze uruchomienie notatnika) od gotowego modelu przypisanego w systemie ustrukturyzowanego Model Registry? 
### Pytanie 6: Twój podzespół rozwija zaawansowane czatboty na bazach generatywnych LLM (wykorzystując do orkiestracji frameworki LlamaIndex). Z jakich specyficznych we współczesnym LLMOps wbudowanych funkcji od MLflow warto byłoby skorzystać chociażby podczas analizy halucynacji bota?
### Pytanie 7: Fundamentalnym potężnym rozwiązaniem na rynku MLOps są mechanizmy platformy zwane „Flavors” (np. natywny moduł z PyTorch, Scikit-learn, flavor dedykowanego ONNX). Wytłumacz, w jaki jednorodny sposób interfejs `pyfunc` umożliwia elastyczne i ujednolicone API serwowania na produkcji mimo braku kompatybilności frameworków z samymi wagami pod maską?
### Pytanie 8: Jeden z Twoich modelów biznesowych od 3 miesięcy przebywa na produkcji z widocznym błędem spadającego Recall'a na nowych danych rynkowych, a firma utraciła pliki jego treningu w wyniku odświeżeń folderów inżynierów. W jaki sposób wykorzystując cechy mechanizmów *MLflow Projects* wyeliminował(a)byś przyszłe błędy wynikające z braku reproduktywności wyciąganych kodu i nieidentycznych zależności Pythona?
