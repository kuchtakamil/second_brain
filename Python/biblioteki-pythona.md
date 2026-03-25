# Biblioteki Pythona

**Data:** 2025-07-15

---

**User:**

Wymień najpopularniejsze i najważniejsze biblioteki w Python zarówno to standardowe jak i niestandardowe.

---

**Assistant:**

Oto zestawienie najważniejszych i najpopularniejszych bibliotek w Pythonie — zarówno **standardowych** (wchodzących w skład Pythona), jak i **niestandardowych** (zewnętrznych, instalowanych np. przez `pip`).

---

## 🧱 Biblioteki standardowe (standard library)

Te biblioteki są dostępne od razu po instalacji Pythona.

### 🔧 Narzędzia ogólnego użytku
- `os` – operacje systemowe (pliki, katalogi, zmienne środowiskowe)
- `sys` – dostęp do zmiennych i funkcji interpretera
- `pathlib` – nowoczesna praca z systemem plików (ścieżki jako obiekty)
- `shutil` – operacje na plikach i katalogach (kopiowanie, usuwanie, archiwizacja)

### 🧪 Testowanie i debugowanie
- `unittest` – framework do testów jednostkowych
- `doctest` – testowanie na podstawie przykładów z dokumentacji
- `logging` – zaawansowany system logowania
- `traceback` – obsługa i formatowanie wyjątków

### 🔢 Przetwarzanie danych
- `json` – kodowanie/dekodowanie JSON
- `csv` – czytanie/zapisywanie CSV
- `datetime` – operacje na datach i czasie
- `collections` – rozszerzenia typów wbudowanych (np. `Counter`, `defaultdict`)

### 🔐 Bezpieczeństwo i haszowanie
- `hashlib` – funkcje skrótu (SHA256, MD5 itd.)
- `secrets` – generowanie kryptograficznie bezpiecznych danych
- `uuid` – generowanie unikalnych identyfikatorów

### 🌐 Internet i sieci
- `http.client`, `urllib` – klient HTTP
- `socket` – niskopoziomowa obsługa sieci
- `xml.etree.ElementTree` – parsowanie XML
- `html.parser` – parsowanie HTML

---

## 📦 Najpopularniejsze biblioteki zewnętrzne (niestandardowe)

Poniżej podział według zastosowania. Wszystkie można zainstalować przez `pip`.

### 🧮 Przetwarzanie danych i nauka o danych
- **NumPy** – operacje numeryczne, tablice, wektoryzacja
- **Pandas** – analiza danych (struktury `DataFrame`, `Series`)
- **Matplotlib** / **Seaborn** – wykresy i wizualizacje danych
- **SciPy** – zaawansowane obliczenia naukowe (statystyka, algebra)
- **Plotly** – interaktywne wykresy
- **Polars** – szybka alternatywa dla Pandas

### 🤖 Sztuczna inteligencja i ML
- **scikit-learn** – klasyczne algorytmy ML
- **TensorFlow** / **Keras** – sieci neuronowe, deep learning
- **PyTorch** – deep learning, modele LLM
- **XGBoost** / **LightGBM** – uczenie gradientowe (popularne w Kaggle)

### 📊 BI i analiza danych
- **Jupyter** – interaktywne notatniki
- **Altair**, **Dash** – tworzenie interaktywnych dashboardów

### 🌐 Web development
- **Flask** – mikroframework webowy
- **Django** – pełnoprawny framework webowy
- **FastAPI** – nowoczesne, szybkie API oparte na typowaniu
- **Requests** – uproszczone wykonywanie zapytań HTTP
- **BeautifulSoup** / **lxml** – parsowanie HTML i web scraping
- **Selenium** / **Playwright** – automatyzacja przeglądarki

### 🧪 Testowanie
- **pytest** – bardzo popularny framework testowy
- **hypothesis** – testy property-based
- **tox** – automatyzacja testów w wielu środowiskach

### 🗂 Obsługa danych i formatów
- **PyYAML** – obsługa YAML
- **python-docx** / **openpyxl** / **pdfplumber** – operacje na Word, Excel, PDF
- **SQLAlchemy** – ORM i praca z bazami danych
- **Pydantic** – walidacja i serializacja danych (np. w FastAPI)

### 🐳 DevOps, chmura i systemy
- **boto3** – obsługa AWS
- **docker-py** – kontrola Dockera przez Pythona
- **fabric** – automatyzacja zadań zdalnych przez SSH

### 📦 Zarządzanie zależnościami i środowiskiem
- **pipenv**, **poetry** – zarządzanie środowiskami i zależnościami
- **virtualenv** – tworzenie środowisk wirtualnych

---

Jeśli podasz konkretny obszar (np. analiza danych, AI, backend, testowanie), mogę zawęzić listę do najważniejszych bibliotek w tej dziedzinie.