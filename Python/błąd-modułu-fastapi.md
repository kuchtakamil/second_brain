# Błąd modułu FastAPI

**Data:** 2025-07-10

---

**User:**

Mam plik z endpointami w FastAPI. Próbuję uruchomić idostaję błąd
fastapi dev api_main.py                         ──(czw,lip10)─┘
Traceback (most recent call last):
  File "/home/kamil/.local/bin/fastapi", line 5, in <module>
    from fastapi.cli import main
ModuleNotFoundError: No module named 'fastapi'
Jest już zaistalowane pip install 'fastapi[standard]'

---

**Assistant:**

Masz błąd **ModuleNotFoundError: No module named 'fastapi'**, chociaż zainstalowałeś `fastapi[standard]`. Oto najpewniejsze przyczyny i kroki naprawcze:

---

## 🔍 Typowe powody i rozwiązania

### 1. Środowisko wirtualne (venv)
Najczęstsza przyczyna: instalowałeś FastAPI w środowisku wirtualnym, a uruchamiasz aplikację w innym (np. globalnym lub innym venv). Upewnij się, że środowisko jest aktywne:
```bash
source path/to/venv/bin/activate  # Linux/Mac
# lub
venv\Scripts\activate.bat         # Windows cmd
venv\Scripts\Activate.ps1         # Windows PowerShell
```
Potem sprawdź:
```bash
pip list
pip show fastapi
```
Czy widać fastapi i powiązane pakiety?citeturn0search3turn0search6

### 2. Interpreter w IDE (np. VS Code)
Jeśli używasz Visual Studio Code, sprawdź, czy interpreter Python jest ustawiony na ten z aktywowanego środowiska. W VS Code: `CTRL+SHIFT+P`, wybierz „Python: Select Interpreter” i wybierz właściwy interpreterciteturn0search0turn0search6.

### 3. Zła komenda uruchamiania
Jeśli próbujesz `fastapi dev api_main.py`, a pakiet `fastapi-cli` nie został zainstalowany poprawnie, komenda może nie działać. Sprawdź obecność CLI:
```bash
which fastapi
fastapi --help
```
W razie braku, spróbuj:
```bash
pip install "fastapi[standard]"  # lub po prostu `fastapi`
```
a także:
```bash
pip install "uvicorn[standard]"
```
CLI `fastapi dev` pochodzi z `fastapi-cli`, które to zawiera się w `fastapi[standard]`citeturn0search7turn0search8.

### 4. Nazwy plików / modułów
Jeśli w katalogu masz plik o nazwie `fastapi.py`, Python może go używać zamiast właściwego pakietu. Upewnij się, że:
- nie nazwałeś własnego pliku `fastapi.py`
- żaden moduł/zmienna nie nosi nazwy `fastapi`citeturn0search6.

---

## ✅ Sugerowane kroki naprawcze

1. **(Re)utwórz środowisko wirtualne** w katalogu projektu:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install "fastapi[standard]" "uvicorn[standard]"
   ```
2. **Sprawdź instalację**:
   ```bash
   pip list
   pip show fastapi
   ```
   Sprawdź też `uvicorn`.
3. **Uruchamianie aplikacji**:
   ```bash
   fastapi dev api_main.py
   # lub
   uvicorn api_main:app --reload
   ```
   W pliku `api_main.py` upewnij się, że masz:
   ```python
   from fastapi import FastAPI
   app = FastAPI()
   ```
4. **W IDE (VS Code)** automatycznie wybierz interpreter venv przed uruchomieniem:
   `CTRL+SHIFT+P → Python: Select Interpreter`citeturn0search0turn0search6

---

## 🛠 Podsumowanie w tabela:

| Problem                           | Rozwiązanie                                         |
|----------------------------------|-----------------------------------------------------|
| FastAPI nie zainstalowany w venv | Aktywuj venv i zainstaluj ponownie moduły          |
| interpreter IDE nie ten sam      | Wybierz odpowiedni interpreter w ustawieniach IDE   |
| CLI fastapi nie dostępny         | Zainstaluj pełny pakiet lub sprawdź PATH            |
| Nazwa pliku modułu koliduje      | Zmień nazwę pliku (nie `fastapi.py`)                |

---

Jeśli po tych krokach problem dalej występuje, podaj:
- wynik `pip list` (gdy venv aktywny),
- co dokładnie masz w `api_main.py`,
- jak uruchamiasz serwer. 

Pomogę dalej.

---

**User:**

sytuacja wygląda tak że środowisko wirtualne mam w innym katalogu niż sam projekt
/home/kamil/rag_env - środowisko wirtualne
/home/kamil/rag_lab - projekt
Z którego katalogu powinienem uruchamiać fastapi? z /home/kamil/rag_env  nie będzie widoczny plik api_main.py.
Z /home/kamil/rag_lab nie jest widoczne fastapi ze śrdowiska

---

**Assistant:**

Jeśli Twoje środowisko wirtualne znajduje się w katalogu `/home/kamil/rag_env`, a kod projektu w `/home/kamil/rag_lab`, musisz:

---

## ✅ Prawidłowy sposób uruchomienia

### 1. **Aktywacja środowiska w katalogu projektu**
Musisz aktywować venv **z terminala znajdującego się w projekcie** – czyli:
```bash
cd /home/kamil/rag_lab
source ../rag_env/bin/activate
```
Po aktywacji wpisz:
```bash
which python
which pip
```
i upewnij się, że oba wskazują na `/home/kamil/rag_env/bin/...`. Jeśli nie — środowisko nie jest aktywne citeturn0search10turn0search0.

### 2. **Instalacja wymaganych pakietów**
W aktywowanym venv z katalogu projektu wykonaj:
```bash
pip install fastapi[standard] uvicorn[standard]
```
Do uruchomienia `fastapi dev` wymagany jest CLI z `fastapi-cli`, który jest częścią `fastapi[standard]` citeturn0search1turn0search0.

### 3. **Uruchamianie aplikacji**
W katalogu projektu (**po aktywacji venv**) możesz:
```bash
fastapi dev api_main.py
```
lub alternatywnie:
```bash
python -m uvicorn api_main:app --reload
```
Ta druga metoda (moduł poprzez `python -m uvicorn`) działa zawsze w kontekście aktywnego venv i rzadziej zawodna citeturn0search15.

---

## 🔄 Podsumowanie

- **Katalog projektu** i **katalog venv** mogą być osobno — to normalne i działa poprawnie.
- Kluczowe jest **aktywowanie venv przed uruchomieniem kodu** oraz **uruchamianie poleceń z katalogu projektu**, aby były widoczne endpointy i pliki aplikacji.
- Jeśli po aktywacji nie widzisz `fastapi` wśród pakietów (`pip list`), to prawdopodobnie instalacja była niepoprawna lub venv nie został aktywowany.

---

## 🧪 Sprawdzenie diagnostyczne

- W `/home/kamil/rag_lab`, przed uruchomieniem, wykonaj:
  ```bash
  source ../rag_env/bin/activate
  pip list
  pip show fastapi
  ```
- Jeśli pojawi się `fastapi` i `uvicorn`, to ok. Jeśli nie, doinstaluj je.
- Gdy venv jest aktywny, uruchom:
  ```bash
  fastapi dev api_main.py
  ```
  lub
  ```bash
  python -m uvicorn api_main:app --reload
  ```

---

Jeśli po tych krokach nadal masz problem, napisz wyniki następujących poleceń:
- `pip list` przy aktywowanym venv,
- `which python`, `which fastapi`,
- dokładne ścieżki uruchamiane w terminalu.

Pomogę dalej.

---

**User:**

jak mogę uruchomić fastapi w trybie debug i podłączyć się pod to przy pomocy cursor ai albo vs code?

---

**Assistant:**

Jeśli chcesz uruchomić **FastAPI w trybie debug** i podłączyć się przez **Cursor AI** albo **VS Code**, oto precyzyjna instrukcja jak to zrobić, bez zbędnych fraz typu „świetne pytanie”.

---

## 🐍 FastAPI + Debug w VS Code

1. W głównym pliku aplikacji (`api_main.py` lub `main.py`) dodaj (tylko na potrzeby debugowania):
   ```python
   if __name__ == "__main__":
       import uvicorn
       uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
   ```
   Dzięki temu można uruchomić aplikację z debuggera jako `python api_main.py` i breakpointy będą działać. citeturn0search13turn0search1

2. W VS Code wejdź w panel **Run and Debug → Add Configuration… → Python** i wybierz:
   - **Python: Current File (Integrated Terminal)**  
   lub  
   - opcję wybraną automatycznie przez rozszerzenie FastAPI  
   — VS Code uruchomi `api_main.py` z debugerem i możesz łapać breakpointy. citeturn0search0turn0search1

3. Alternatywnie, bardziej elegancko: stwórz `.vscode/launch.json` z konfiguracją:
   ```json
   {
     "configurations": [
       {
         "name": "FastAPI: uvicorn",
         "type": "python",
         "request": "launch",
         "module": "uvicorn",
         "args": ["api_main:app", "--reload", "--host=127.0.0.1", "--port=8000"]
       }
     ]
   }
   ```
   VS Code uruchomi wtedy `uvicorn` pod debuggerem i będziesz mógł ustawiać breakpointy w handlerach. citeturn0search2turn0search11

4. Przy aktywnym debugerze wejdź na `http://127.0.0.1:8000/docs` i kliknij “Try it out” – debugger zatrzyma się w Twoim kodzie. citeturn0search0turn0search1

---

## 🧠 Cursor AI – integracja do debugowania

- Cursor AI wspiera "AI Debug Assistant" które możesz włączyć: **Settings → Debugging → AI Debug Assistant**. W razie błędów (np. Pydantic validation failure), Cursor będzie sugerować jak sprawdzać dane i co debugować. citeturn0search7
- Nie jest typowym IDE – debugowanie działa głównie za pomocą VS Code i jego debuggera. Jeśli Cursor wspiera dodatkowe breakpointy, to zależy od jego integracji z debugpy; nie ma gotowego pipeline debugowania FastAPI. citeturn0search6turn0search7

---

## 🔁 Krok po kroku – z przykładami

### 📁 Struktura projektu:
```
/home/kamil/rag_lab
│
└── api_main.py   # Twój FastAPI app
└── .vscode/
     └── launch.json
```

### 🚀 Kod w api_main.py:
Dodaj blok:
```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
```

### 🛠 launch.json:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "FastAPI: uvicorn",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": ["api_main:app","--reload","--host=127.0.0.1","--port=8000"]
    }
  ]
}
```

### 🎯 Jak debugować:
1. Otwórz folder projektu w VS Code (`rag_lab`).
2. Upewnij się, że interpreter Pythona to ten z twojego venv.
3. Ustaw breakpoint w kodzie (np. w handlerze endpointa).
4. Naciśnij **F5** → debuger uruchomi serwer.
5. Wejdź przeglądarką na `localhost:8000/docs`, kliknij “Try it out” – debuger zatrzyma się. Możesz analizować zmienne w oknie Debug.

---

## 🤖 Debugowanie z użyciem Cursor AI

- Włącz **AI Debug Assistant** w ustawieniach Cursor.
- Cursor może zasugerować, gdzie postawić breakpoint lub jak zbadać problem (zwłaszcza przy błędach Pydantic).
- Faktyczne zatrzymywanie i śledzenie kodu nadal odbywa się przez VS Code / debugpy, nie z poziomu Cursor. citeturn0search6turn0search7

---

## 🧭 Podsumowanie

| Aspekt                   | Co zrobisz |
|--------------------------|------------|
| Uruchamianie w debug     | VS Code z `launch.json` lub blok `if __name__ == "__main__"` |
| Ustawianie breakpointów  | W handlerach FastAPI |
| Otwarcie API Swagger     | `http://127.0.0.1:8000/docs`, kliknij „Try it out” |
| Cursor AI wsparcie       | AI Debug Assistant do sugestii, ale debug działa przez VS Code |
| Zalecany workflow        | Debug w VS Code, pomoc analityczna przez Cursor |

---

Jeśli coś nie działa (np. breakpoint się nie zatrzymuje, błąd typów, czy Cursor nie widzi projektu), podaj:
- co jest w Twoim `launch.json`,
- fragment pliku `api_main.py`,
- miejsce ustawienia interpreterów w VS Code i czy venv jest aktywne.

Mogę wówczas doprecyzować konfigurację.

---

**User:**

czy muszę użyć uvicorn do tego? Nie wystarczy fastapi?

---

**Assistant:**

Nie, aby uruchomić aplikację FastAPI w trybie debugowym, **nadal musisz użyć ASGI serwera**, czyli np. **Uvicorn**. FastAPI to biblioteka‑framework, ale **nie pełni roli serwera**, więc nie można go uruchomić bez pośrednika, takiego jak Uvicorn, Daphne czy Hypercorn.

---

### 🔧 Użycie `fastapi dev` a `uvicorn`

- Komenda `fastapi dev api_main.py` pochodzi z **FastAPI CLI**, który wewnętrznie uruchamia **Uvicorn** citeturn0search1turn0search0.
- W praktyce `fastapi dev` to spakowana komenda, która działa tak samo jak `uvicorn api_main:app --reload`, z automatycznym wykrywaniem modułu aplikacji FastAPI i punktu wejścia `app` citeturn0search1turn0search0.

---

### ✅ Czy można pominąć Uvicorn? Nie.

FastAPI nie może sam pełnić funkcji serwera. Trzeba go „obsługiwać” przez ASGI-server, z którym się integruje. Użycie `fastapi dev` oznacza instalację `fastapi-cli`, ale to tylko wrapper nad Uvicorn, czyli **nadal korzystasz z Uvicorn** citeturn0search1turn0search0.

---

### 🛠 Debugowanie – najlepsze praktyki

#### Opcja 1: `fastapi dev`
- Korzystasz z CLI FastAPI:  
  ```bash
  fastapi dev api_main.py
  ```
  — uruchamia Uvicorn z opcją autoreload i hot-reload.

#### Opcja 2: `uvicorn` bezpośrednio
- Możesz pominąć `fastapi dev` i odpalić manualnie:
  ```bash
  uvicorn api_main:app --reload --host=127.0.0.1 --port=8000
  ```
  — działa identycznie, ale daje większą kontrolę nad opcjami Uvicorn citeturn0search0turn0search8.

#### Opcja 3: blok `if __main__`
- W `api_main.py`:
  ```python
  if __name__ == "__main__":
      import uvicorn
      uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
  ```
  — pozwala uruchomić serwer przez `python api_main.py`, co ułatwia debugowanie w VS Code.

---

### 📊 Co dostajesz w trybie `--reload`

| Metoda               | Autoreload | Debuggable w VS Code | Konfiguracja serwera |
|----------------------|------------|------------------------|------------------------|
| `fastapi dev`        | ✅         | ✅                     | część CLI wrappera    |
| `uvicorn ... --reload` | ✅         | ✅                     | pełna kontrola nad opcjami |
| `python api_main.py` | ✅ (jeśli używasz `uvicorn.run(... reload=True)`) | ✅ | tak jak wyżej         |

---

### 🧭 Podsumowanie

- **Tak, musisz korzystać z Uvicorn** lub innego serwera ASGI.
- `fastapi dev` jest wygodny, ale **to też działa w oparciu o Uvicorn**.
- Jeśli chcesz precyzyjną kontrolę, lepszym wyborem jest `uvicorn api_main:app --reload` lub `uvicorn.run(...)` z kodu.
- W VS Code konfiguruj `launch.json`, interpreter Pythona i breakpointy, aby debugować API, gdy serwer działa przez Uvicorn.

W razie potrzeby mogę podać gotowy `launch.json` lub konfigurację debugowania — napisz, co Ci wygodniej: debug przez `fastapi dev`, czy przez `uvicorn` w launch.json.