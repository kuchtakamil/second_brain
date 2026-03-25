# Tekst zwracany przez subprocess.

**Data:** 2024-05-17

---

**User:**

Mam skrypt python - main.py - który wywołuje inny skrypt python.
W main.py wywołuje skrypty przy pomocy 
res = subprocess.run(cmd, capture_output=True, text=True)

W wywoływanym skrypcie chcę zwracać dowolny tekst. Powinienem zrobić print("Moj text"), czy return "Moj text"?

Próbuję na oba sposoby i w res zawsze res.stdout jest puste.

---

**Assistant:**

Aby wywołany skrypt zwracał tekst do skryptu głównego (main.py) przy użyciu `subprocess.run`, musisz użyć funkcji `print` w wywoływanym skrypcie. Funkcja `return` służy do zwracania wartości z funkcji w obrębie tego samego skryptu i nie działa w kontekście komunikacji między różnymi procesami.

Jeśli `res.stdout` jest puste, upewnij się, że:

1. Skrypt, który wywołujesz, faktycznie używa `print` do wyświetlania tekstu.
2. Sprawdzasz `res.stdout` po zakończeniu wywołania `subprocess.run`.
3. Używasz właściwej komendy w `subprocess.run`.

Poniżej przykład, jak to powinno wyglądać:

**main.py:**
```python
import subprocess

cmd = ["python", "script.py"]
res = subprocess.run(cmd, capture_output=True, text=True)

print("Standard Output:", res.stdout)
print("Standard Error:", res.stderr)
```

**script.py:**
```python
print("Mój tekst")
```

Gdy uruchomisz `main.py`, powinieneś zobaczyć "Mój tekst" w `res.stdout`.

Jeśli `res.stdout` nadal jest puste, możesz sprawdzić następujące rzeczy:

1. Upewnij się, że `script.py` jest w tej samej ścieżce, co `main.py`, albo podaj pełną ścieżkę do `script.py`.
2. Upewnij się, że uruchamiasz `main.py` w odpowiednim środowisku (na przykład, czy python zainstalowany w ścieżce systemowej to właściwa wersja).

Możesz także dodać trochę debugowania, aby zobaczyć więcej informacji:

**main.py:**
```python
import subprocess

cmd = ["python", "script.py"]
res = subprocess.run(cmd, capture_output=True, text=True)

print(f"Return code: {res.returncode}")
print(f"Standard Output: {res.stdout}")
print(f"Standard Error: {res.stderr}")
```

Jeśli po tych krokach `res.stdout` nadal jest puste, sprawdź, czy są jakieś komunikaty o błędach w `res.stderr` oraz czy wywoływana komenda jest poprawna i skrypt `script.py` działa poprawnie samodzielnie.