# Automat do sprawdzania wizyt

**Data:** 2025-03-11

---

**User:**

Chciałbym stworzyć automat który będzie za mnie sprawdzał dostępność wizyt lekarskich na pewnym portalu który dostępny jest po zalogowaniu się. jak się do tego zabrać

---

**Assistant:**

Świetny pomysł — to klasyczny przykład użycia automatyzacji z wykorzystaniem web scrapingu lub automatyzacji przeglądarki. Poniżej krok po kroku podpowiem Ci, jak się za to zabrać:

---

### 🔧 Krok 1: Wybór technologii
Najwygodniejsza droga to użycie **automatyzacji przeglądarki**, np.:
- **Selenium** (najpopularniejsze),
- **Playwright** (bardziej nowoczesna i szybsza alternatywa dla Selenium),
- ewentualnie **Puppeteer** (bardziej popularny w Node.js).

Jeśli znasz Pythona lub Node.js, to Playwright lub Selenium to dobre wybory.

---

### 🔐 Krok 2: Obsługa logowania
1. Zautomatyzuj zalogowanie się do portalu.
   - Znajdź elementy HTML odpowiedzialne za login/hasło (np. `input[name="username"]`).
   - Wprowadź dane logowania.
   - Kliknij przycisk logowania i poczekaj na przekierowanie lub załadowanie panelu.

💡 W razie potrzeby możesz też zapisać cookies po zalogowaniu, by nie logować się za każdym razem od nowa.

---

### 🔍 Krok 3: Sprawdzenie dostępności wizyt
Po zalogowaniu:
- Przejdź do odpowiedniego widoku (np. kalendarza czy listy lekarzy),
- Zidentyfikuj elementy, które reprezentują dostępne terminy (np. przyciski, oznaczenia zielonym kolorem, teksty typu „dostępny termin”),
- Zbierz te dane i przetwórz.

---

### 📣 Krok 4: Powiadomienie
Kiedy wykryjesz dostępny termin:
- Wyślij sobie e-maila (np. przez SMTP),
- Lub użyj powiadomienia push (np. Pushover, Telegram Bot, Discord Webhook),
- Albo nawet zrób prosty interfejs webowy pokazujący aktualny status.

---

### ⏱️ Krok 5: Harmonogram uruchamiania
Uruchamiaj automat np. co 15 minut:
- W systemie Linux/Unix – przez `cron`,
- W Windows – przez Harmonogram zadań,
- Albo zrób to jako usługę działającą stale.

---

### ✍️ Przykład (Python + Playwright)
```bash
pip install playwright
playwright install
```

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://twojportal.pl/login")

    # Logowanie
    page.fill("input[name='username']", "twoj_login")
    page.fill("input[name='password']", "twoje_haslo")
    page.click("button[type='submit']")

    page.wait_for_load_state("networkidle")

    # Przejście do kalendarza
    page.goto("https://twojportal.pl/kalendarz")

    # Sprawdzenie dostępnych wizyt
    available = page.query_selector_all(".termin.dostepny")
    if available:
        print("✅ Dostępne terminy!")
        # Tutaj możesz np. wysłać maila

    browser.close()
```

---

Jeśli chcesz, mogę pomóc Ci przygotować działający szkielet projektu w Pythonie lub Node.js — tylko powiedz, jakiego języka chcesz użyć i czy masz już jakieś dane logowania/testowy dostęp do tego portalu.

Chcesz, żebym zrobił Ci gotowy starter w Pythonie z obsługą logowania i sprawdzania dostępności?

---

**User:**

czy jest możliwość aby stworzyć automat który nie bazowałby na kodzie html strony lecz po prostu klikał na wybrane elementy interfejsu w zadanej kolejności? chciałbym otworzyć mu przeglądarkę, ustawić że ma klikać w wybrane miejsca, czekać pewien czas i analizować rezultat w postaci tego co jest wyświetlane na ekranie. Chciałbym żeby było to jak najbardziej bezpieczne. Nie chciałbym dostać ban na tym portalu

---

**Assistant:**

Tak, jak najbardziej — to podejście, które bazuje bardziej na **automatyzacji GUI / interfejsu użytkownika**, a nie na analizie kodu HTML strony. To bardziej przypomina **symulowanie działań użytkownika**, czyli kliknięcia, poruszanie myszką, odczytywanie tego, co jest widoczne na ekranie.

To bardzo dobry kierunek, szczególnie jeśli chcesz być **„niewidzialny” dla systemów zabezpieczających portal** (które mogą wykrywać web scrapery czy automatyzację przeglądarki).

---

### ✅ Jakie są opcje?
Możesz użyć narzędzi takich jak:

#### 1. **AutoHotkey (Windows)**  
– Skryptowy język do automatyzacji GUI: klikanie, wpisywanie tekstu, rozpoznawanie obrazków.  
– Bardzo prosty, ale mocny.

#### 2. **Python + pyautogui**
– Automatyzuje mysz, klawiaturę, wykonuje zrzuty ekranu.
– Możesz kliknąć w konkretne współrzędne lub używać „template matching” (szukać przycisków na podstawie obrazka).
– Bardzo prosty i multiplatformowy.

#### 3. **Python + opencv + pyautogui**
– Połączenie: pyautogui klika, opencv rozpoznaje zawartość ekranu.
– Pozwala szukać konkretnych ikon/przycisków.

#### 4. **SikuliX (Java)**
– Automatyzacja oparta w całości na rozpoznawaniu obrazów — kliknięcia, oczekiwania, działania warunkowe.
– Super narzędzie, zwłaszcza jeśli jesteś Javerem :)

---

### 🔐 Bezpieczeństwo (ważne!)
To podejście:
- Nie wchodzi w interakcję z kodem strony,
- Nie generuje nienaturalnych requestów do backendu,
- Działa jak człowiek → bardzo niskie ryzyko bana.

Jeśli dodatkowo:
- losowo opóźnisz kliknięcia (małe różnice czasowe),
- unikniesz klikania 24/7 bez przerwy,
to nikt nie zauważy, że to automat.

---

### 📸 Jak działa takie podejście w praktyce?

#### Przykład: `pyautogui` (Python)
```bash
pip install pyautogui opencv-python pillow
```

```python
import pyautogui
import time

# Przesuń myszkę i kliknij w konkretne miejsce
pyautogui.moveTo(500, 400, duration=1)  # płynny ruch
pyautogui.click()

# Czekaj na załadowanie strony
time.sleep(3)

# Zrób screenshot i zapisz
screenshot = pyautogui.screenshot()
screenshot.save("screen.png")

# Albo szukaj konkretnego obrazka na ekranie:
location = pyautogui.locateOnScreen('przycisk_dalej.png', confidence=0.9)
if location:
    pyautogui.click(location)
```

---

### 👁️‍🗨️ Alternatywa z rozpoznawaniem tekstu (OCR)
Jeśli chcesz analizować to, co jest **wyświetlane jako tekst**, możesz dodać **OCR**:
- `pytesseract` (OCR z Tesseractem)
- Zrobisz screenshot ekranu i wydobędziesz z niego tekst:
```python
from pytesseract import image_to_string
from PIL import Image

text = image_to_string(Image.open("screen.png"))
if "Dostępny termin" in text:
    print("🎯 Termin znaleziony!")
```

---

### 💡 Czy chcesz przykładowy projekt?
Mogę Ci przygotować:
- pełen starter w Pythonie,
- konfigurację do znajdowania przycisków,
- przykładowy plik ze zrzutami ekranów jako „wzorce” do kliknięcia,
- powiadomienie (np. e-mail lub alert dźwiękowy).

Chcesz, żebym Ci coś takiego złożył jako bazę? Jeśli tak – napisz:
1. Czy chcesz użyć `pyautogui` czy `SikuliX` (Java),
2. Czy masz już zrzuty ekranów tych przycisków (jeśli nie, podpowiem jak je zrobić),
3. Jaką formę powiadomień preferujesz (e-mail, dźwięk, log, co innego).

Działamy? :)