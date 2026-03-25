# Oto log z debugowania runtime, który zaproponowałeś. Struktura katalogów i plikó

**Data:** 1 załączony plik

---

**User:**

Oto log z debugowania runtime, który zaproponowałeś.
Struktura katalogów i plików na screenie

PYTHONPATH: ['/var/task', '/opt/python/lib/python3.13/site-packages', '/opt/python', '/var/lang/lib/python3.13/site-packages', '/var/runtime', '/var/lang/lib/python313.zip', '/var/lang/lib/python3.13', '/var/lang/lib/python3.13/lib-dynload', '/var/lang/lib/python3.13/site-packages', '/opt/python/lib/python3.13/site-packages', '/opt/python']
CWD: /var/task
Directory listing: ['.python-version', 'context.py', 'data', 'deploy.py', 'lambda-deployment.zip', 'lambda-package', 'lambda_handler.py', 'pyproject.toml', 'requirements.txt', 'resources.py', 'server.py']
Import failed: No module named 'mangum'
Found mangum directory at: /var/task/lambda-package/mangum
END RequestId: ff09e3f9-691f-4006-b566-ce40b25ba4eb
REPORT RequestId: ff09e3f9-691f-4006-b566-ce40b25ba4eb	Duration: 558.78 ms	Billed Duration: 669 ms	Memory Size: 128 MB	Max Memory Used: 38 MB	Init Duration: 109.44 ms

---

**Gemini:**

-  [image\_77efc5.png](image_77efc5-ade099afa2e26b5a.png)8 sty 2026, 17:27:08 CET

Analiza logów jednoznacznie wskazuje przyczynę błędu: **biblioteka `mangum` znajduje się w podkatalogu `lambda-package`, który nie jest uwzględniony w `PYTHONPATH`**.

Python w środowisku Lambda szuka modułów bezpośrednio w `/var/task` (główny katalog Twojej paczki) oraz w warstwach (`/opt`). Twój log debugowania potwierdza:
`Found mangum directory at: /var/task/lambda-package/mangum`

Masz dwie drogi rozwiązania tego problemu:

### Opcja 1: Poprawna struktura paczki ZIP (Zalecane)

Zależności powinny znajdować się w głównym katalogu archiwum ZIP, a nie w folderze `lambda-package`. Musisz zmienić sposób pakowania projektu.

Jeśli używasz CLI do tworzenia paczki, wykonaj:

```
# Wejdź do katalogu z zależnościami
cd lambda-package
# Dodaj zawartość katalogu do głównego poziomu ZIPa
zip -r ../lambda-deployment.zip .
# Wróć i dodaj pliki źródłowe
cd ..
zip -g lambda-deployment.zip lambda_handler.py server.py resources.py context.py
```

Po operacji, struktura wewnątrz `lambda-deployment.zip` powinna wyglądać tak:

```
.
├── mangum/
├── anyio/
├── lambda_handler.py
├── server.py
└── ...
```

---

### Opcja 2: Programowe dodanie ścieżki do `sys.path`

Jeśli z jakiegoś powodu musisz trzymać zależności w osobnym folderze wewnątrz Lambdy, musisz poinstruować interpreter, gdzie ma ich szukać **zanim** spróbujesz zaimportować `mangum`.

W pliku `lambda_handler.py` dodaj na samym początku:

```
import sys
import os

# Add the subdirectory to PYTHONPATH
package_path = os.path.join(os.getcwd(), 'lambda-package')
if package_path not in sys.path:
    sys.path.insert(0, package_path)

# Now you can import mangum and its dependencies (anyio, etc.)
import mangum
from server import app

handler = mangum.Mangum(app)

def lambda_handler(event, context):
    return handler(event, context)
```

### Dlaczego to jest istotne technicznie?

1. **Dependency Tree**: `mangum` wymaga do działania bibliotek takich jak `anyio`, `idna` i `sniffio`. Przesunięcie samego folderu `mangum` nie wystarczy – wszystkie one muszą być widoczne dla interpretera. Dodanie `lambda-package` do `sys.path` rozwiązuje problem dla całego zestawu zależności.
2. **Runtime Environment**: AWS Lambda ustawia `CWD` (Current Working Directory) na `/var/task`. Python domyślnie dodaje `''` (pusty string reprezentujący CWD) do `sys.path`, ale nie przeszukuje rekurencyjnie podfolderów w poszukiwaniu modułów.

**Rekomendacja:** Zdecydowanie wybierz **Opcję 1**. Utrzymywanie czystej struktury w `/var/task` jest standardem AWS i zapobiega problemom z importami relatywnymi wewnątrz samych bibliotek.

Czy chcesz, abym pomógł Ci zoptymalizować skrypt `deploy.py` widoczny na Twoim screenie, aby poprawnie generował strukturę paczki?