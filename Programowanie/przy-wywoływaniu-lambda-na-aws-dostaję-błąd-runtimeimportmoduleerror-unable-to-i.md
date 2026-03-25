# Przy wywoływaniu lambda na aws, dostaję błąd Runtime.ImportModuleError: Unable t

**Data:** 8 sty 2026, 15:24:12 CET

---

**User:**

Przy wywoływaniu lambda na aws, dostaję błąd
Runtime.ImportModuleError: Unable to import module 'lambda_handler': No module named 'mangum'
W requirements.txt mam mangum. W oknie Code na console AWS, gdy rozwinę drzewko też widzę mangum i mangum dist info

---

**Gemini:**

Problem `Runtime.ImportModuleError` przy obecności plików w konsoli AWS Lambda zazwyczaj wynika z nieprawidłowej struktury drzewa katalogów, braku zależności przejściowych (transitive dependencies) lub niekompatybilności binarnej.

### 1. Struktura katalogów i PYTHONPATH

AWS Lambda dodaje katalog `/var/task` do `sys.path`. Aby import `mangum` zadziałał, folder biblioteki musi znajdować się bezpośrednio w głównym katalogu paczki deploymentowej, na tym samym poziomie co plik zawierający handler.

Prawidłowa struktura ZIP:

```
.
├── lambda_function.py  <-- Twój handler
├── mangum/             <-- Folder biblioteki
├── mangum-x.x.x.dist-info/
└── anyio/              <-- Mangum wymaga anyio, idna, sniffio, typing-extensions
```

Jeśli Twoje biblioteki znajdują się w podfolderze (np. `venv/` lub `package/`), Lambda ich nie znajdzie, chyba że zmodyfikujesz `sys.path` wewnątrz kodu przed importem:

```
import sys
import os

# Manual path injection if libraries are in a subdirectory
package_path = os.path.join(os.getcwd(), 'name_of_your_folder')
sys.path.append(package_path)

import mangum
```

### 2. Brakujące zależności (Transitive Dependencies)

Błąd `No module named 'mangum'` może być mylący. Czasami występuje, gdy `mangum` próbuje zaimportować swoje własne zależności (np. `anyio`), których brakuje w środowisku.

Upewnij się, że instalujesz biblioteki poleceniem:

```
pip install -t . mangum
```

Flaga `-t .` (target) wymusza instalację wszystkich zależności do bieżącego katalogu. Sprawdź, czy w konsoli AWS widzisz także foldery takie jak `anyio`, `sniffio`, `idna`.

### 3. Warstwy (AWS Layers)

Jeśli umieściłeś `mangum` w AWS Layer, struktura katalogów wewnątrz archiwum ZIP warstwy musi być ściśle określona. Dla Python 3.x musi to być:
`python/lib/python3.x/site-packages/mangum` lub po prostu `python/mangum`.

Jeśli folder `mangum` znajduje się bezpośrednio w głównym katalogu ZIP-a warstwy, Lambda go nie zaindeksuje.

### 4. Uprawnienia plików (POSIX Permissions)

Lambda wymaga, aby pliki i foldery miały uprawnienia do odczytu i wykonywania dla użytkownika `other`. Jeśli pakowałeś ZIP na Windowsie lub z restrykcyjnymi uprawnieniami na Linuxie, import może się nie udać.

Wszystkie katalogi powinny mieć maskę `755`, a pliki `644`. Możesz to naprawić przed pakowaniem:

```
chmod -R 755 .
zip -r9 deployment_package.zip .
```

### 5. Debugowanie runtime

Aby precyzyjnie zdiagnozować, gdzie Lambda szuka modułów, dodaj poniższy fragment kodu na samym początku pliku handlera (przed importem mangum):

```
import sys
import os

def lambda_handler(event, context):
    print(f"PYTHONPATH: {sys.path}")
    print(f"CWD: {os.getcwd()}")
    print(f"Directory listing: {os.listdir(os.getcwd())}")
    
    try:
        import mangum
        print("Mangum imported successfully")
    except ImportError as e:
        print(f"Import failed: {e}")
        # Look for mangum in specific subdirectories
        for root, dirs, files in os.walk(os.getcwd()):
            if 'mangum' in dirs:
                print(f"Found mangum directory at: {root}/mangum")
```

### 6. Architektura procesora (x86\_64 vs ARM64)

Choć `mangum` jest czystym modułem Pythona, jego zależności mogą kompilować rozszerzenia C (C-extensions). Jeśli instalowałeś paczki na lokalnej maszynie z procesorem M1/M2 (ARM64), a Lambda jest ustawiona na `x86_64` (lub odwrotnie), import binariów zawiedzie.

Zalecane jest budowanie paczki w środowisku identycznym z Lambda, używając obrazu Docker:

```
docker run --rm -v $(pwd):/var/task public.ecr.aws/sam/build-python3.11:latest \
pip install -r requirements.txt -t .
```

Czy Twoja funkcja korzysta z AWS Layers, czy pakujesz wszystko do jednego pliku ZIP?